#!/usr/bin/env python3
"""Build the ChatGPT Work illustration skill zip.

  python3 tools/art_skill_build.py [--out ZIP]   write references/FAMILIES.md and build the zip
                                                (default build/art/Heraldry_Classic_Ink_Art_Skill_v8_0.zip)
  python3 tools/art_skill_build.py --check        fail if FAMILIES.md is out of date with config/art_style.json

Source: production/art/skill/heraldry-classic-ink-art/. The build adds the reference images (byte-identical
copies of the repo's own files, listed in references/images/SOURCES.json) and manifest.json, then writes a
deterministic zip with SKILL.md at its root. The queue, prompts and reference selection stay in the repo.
The zip is a build output, never committed: build it when someone needs to install the skill (docs/LARGE_FILES.md)."""
import io
import argparse, hashlib, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "production/art/skill/heraldry-classic-ink-art"
ZIP = ROOT / "build/art/Heraldry_Classic_Ink_Art_Skill_v8_0.zip"
VERSION = "8.0.0"
STAMP = (2026, 10, 10, 0, 0, 0)
def _images():
    """Every reference image any queue item can attach (config gpt_reference_sets)."""
    rs = json.loads((ROOT / "config/art_style.json").read_text(encoding="utf-8"))["gpt_reference_sets"]
    use = {}
    for name, refs in [*rs["sets"].items(), *rs.get("family_sets", {}).items(), *((k, v["refs"]) for k, v in rs.get("kind_sets", {}).items())]:
        for r in refs:
            if "/" in r:
                use.setdefault(r, []).append(name)
    out = {}
    for r in sorted(use):
        out["references/images/" + Path(r).name] = (r, "reference for: " + ", ".join(sorted(set(use[r]))))
    return out


IMAGES = _images()
ORDER = ["bastion", "climate", "monster", "class", "ancestry", "boss", "scenario", "world", "campaign",
         "tradition", "background", "item", "chapter", "cover"]
SIZES = {"3:2": "1536x1024", "2:3": "1024x1536", "1:1": "1024x1024"}
NOTES = {  # family: (looks right when, typical failure)
    "bastion": ("The town seen from its approach road, its defining feature unmistakable, believable density.", "A generic castle; a dozen cottages for a large town; a road that does not reach the gate."),
    "climate": ("The climate's diagnostic terrain and danger; tiny figures for scale only if the prompt lists them.", "Generic scenery; large figures; people where the prompt says none; no signature feature of the climate."),
    "monster": ("One creature, whole body, isolated; size class respected; must-list counts exact.", "Scenery behind it; wrong limb counts; a scale figure on a Small or Medium creature; a cropped tail or weapon."),
    "class": ("One full-length adventurer, action-ready, class-typical gear, isolated.", "Gear not held properly; background scenery; a cropped weapon."),
    "ancestry": ("One full-length adventurer of the ancestry in travel-worn gear, traits as stated.", "Stock ears or horns the source does not give; scenery; the same pose as the class art."),
    "boss": ("The unique named individual in its own setting, dramatic in scale; Size line respected.", "A generic monster; a poster-symmetric composition; a human where the prompt says none."),
    "scenario": ("The place and situation as the parties arrive; named creatures only small, partial or in silhouette.", "A creature portrait instead of a place; a copy of the bestiary art."),
    "world": ("One telling scene of the section's subject, readable at 3.3 in.", "A generic landscape that could belong to any section."),
    "campaign": ("One working room or stronghold interior whose function reads at once; figures only if listed.", "The wrong function (a forge for an armoury); figures nobody listed; a hard box edge."),
    "tradition": ("A small vignette of the tradition's magic at work; light drawn only with line and white space.", "Glow, halo, grey wash or swirling energy; lettered sigils."),
    "background": ("A still life of the trade's tools and keepsakes; no figure; isolated.", "A figure or hands appear; the class kit; clutter that fills the frame."),
    "item": ("A still-life arrangement of the described objects, worn and used, isolated.", "Objects merged or missing; a table scene with scenery; invented lettering."),
    "chapter": ("A wide scene with a low horizon and black foreground framing, lighter finer distance, vignette on all four sides.", "A hard rectangular crop; foreground that does not fade; the cover's composition again."),
    "cover": ("A cinematic establishing scene with one clear focal group and open white sky above for the typeset title.", "Title lettering drawn into the art; the sky filled with detail; a frame."),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def families_markdown(cfg=None):
    cfg = cfg or json.loads((ROOT / "config/art_style.json").read_text(encoding="utf-8"))
    reg = cfg["gpt_reference_sets"]["register_of_family"]
    att = cfg["gpt_max_attempts"]
    assert sorted(NOTES) == sorted(cfg["families"]) == sorted(ORDER), "family list changed: update NOTES and ORDER"
    rows = ["| Family | Register | Size | Printed width | Tries | Looks right when | Typical failure |", "|---|---|---|---|---|---|---|"]
    for f in ORDER:
        fam = cfg["families"][f]
        rows.append(f"| {f} | {reg[f]} | {SIZES[fam['aspect']]} | {fam['print_w_in']} in | {att.get(f, att['default'])} | {NOTES[f][0]} | {NOTES[f][1]} |")
    return ("# Families\n\nGenerated by `tools/art_skill_build.py` from `config/art_style.json`; do not edit by hand. "
            "These are family defaults: an item's own prompt, must list and do-not-draw list override them, and `QUEUE.json` is authoritative if it ever "
            "disagrees with this table.\n\n" + "\n".join(rows) + "\n")


def source_files():
    return sorted(p.relative_to(SRC).as_posix() for p in SRC.rglob("*") if p.is_file() and "__pycache__" not in p.parts)


def zip_bytes():
    """The deterministic skill zip, in memory, from the committed sources (FAMILIES.md as it stands)."""
    blobs = {rel: (SRC / rel).read_bytes() for rel in source_files() if rel != "manifest.json"}
    sources = []
    for name, (repo_path, role) in IMAGES.items():
        data = (ROOT / repo_path).read_bytes()
        if data[:7] == b"version":
            raise SystemExit(f"{repo_path} is an LFS pointer")
        blobs[name] = data
        sources.append({"file": name, "repo_path": repo_path, "sha256": sha(data), "role": role})
    blobs["references/images/SOURCES.json"] = (json.dumps({"note": "Byte-identical copies of repo files. The queue's own reference paths are authoritative; "
                                                           "scripts/validate_skill.py --repo checks these still match.", "images": sources}, indent=1) + "\n").encode()
    manifest = {"skill": "heraldry-classic-ink-art", "version": VERSION,
                "repo_contract": {"queue_schema": 2, "queue": "production/art/gpt/QUEUE.json", "receipts": "production/art/gpt/RECEIPTS.jsonl",
                                  "images": "assets/art/incoming/<ID>.png|jpg|webp", "min_python": "3.9"},
                "files": {rel: {"sha256": sha(b), "bytes": len(b)} for rel, b in sorted(blobs.items())}}
    blobs["manifest.json"] = (json.dumps(manifest, indent=1) + "\n").encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(blobs):
            zi = zipfile.ZipInfo(rel, STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o755 if rel.startswith("scripts/") else 0o644) << 16
            z.writestr(zi, blobs[rel])
    return buf.getvalue()


def build(out=None):
    out = Path(out or ZIP)
    (SRC / "references/FAMILIES.md").write_text(families_markdown())
    data = zip_bytes()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {"zip": str(out), "bytes": len(data), "sha256": sha(data)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.check:
        ok = (SRC / "references/FAMILIES.md").read_text(encoding="utf-8") == families_markdown()
        print("FAMILIES.md up to date" if ok else "FAMILIES.md is stale: run tools/art_skill_build.py")
        return 0 if ok else 1
    print(json.dumps(build(a.out), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
