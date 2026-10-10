#!/usr/bin/env python3
"""Validate the skill package, and optionally its agreement with a Heraldry repo checkout.

  python scripts/validate_skill.py                       the skill folder this script lives in
  python scripts/validate_skill.py --zip skill.zip       an unextracted zip
  python scripts/validate_skill.py --repo /path/to/repo  also check the reference images, families table and queue

Only reads files. Python files are compiled to check syntax, never run."""
import argparse, hashlib, json, re, sys, tempfile, zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:                                           # pragma: no cover
    sys.exit("Pillow is required: pip install pillow")

HERE = Path(__file__).resolve().parents[1]
SIZES = {"3:2": "1536x1024", "2:3": "1024x1536", "1:1": "1024x1024"}
REQUIRED = ["SKILL.md", "README.md", "OPERATOR_CARD.md", "manifest.json", "scripts/heraldry_art.py", "scripts/validate_skill.py",
            "references/STYLE.md", "references/QA_CHECKLIST.md", "references/REPAIR.md", "references/FAMILIES.md",
            "references/AD_HOC.md", "references/images/SOURCES.json"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check_package(base):
    errors = []
    for rel in REQUIRED:
        if not (base / rel).is_file():
            errors.append(f"missing {rel}")
    mf = base / "manifest.json"
    manifest = json.loads(mf.read_text()) if mf.is_file() else {"files": {}}
    on_disk = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts} - {"manifest.json"}
    for rel, rec in manifest["files"].items():
        f = base / rel
        if not f.is_file():
            errors.append(f"manifest lists a missing file: {rel}")
        elif sha(f.read_bytes()) != rec["sha256"] or f.stat().st_size != rec["bytes"]:
            errors.append(f"hash mismatch: {rel}")
    for rel in sorted(on_disk - set(manifest["files"])):
        errors.append(f"file not in manifest: {rel}")
    skill = (base / "SKILL.md").read_text() if (base / "SKILL.md").is_file() else ""
    m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", skill)
    if not m or m.group(1) != "heraldry-classic-ink-art":
        errors.append("SKILL.md front matter must be name then description, name heraldry-classic-ink-art")
    elif len(m.group(2)) > 1024:
        errors.append("SKILL.md description exceeds 1024 characters")
    for ref in set(re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", skill)):
        if not (base / ref).exists():
            errors.append(f"SKILL.md names a missing file: {ref}")
    for py in (base / "scripts").glob("*.py"):
        try:
            compile(py.read_text(), str(py), "exec")
        except SyntaxError as e:
            errors.append(f"{py.name}: {e}")
    src = base / "references/images/SOURCES.json"
    images = json.loads(src.read_text())["images"] if src.is_file() else []
    for rec in images:
        f = base / rec["file"]
        try:
            with Image.open(f) as im:
                im.verify()
            if sha(f.read_bytes()) != rec["sha256"]:
                errors.append(f"{rec['file']}: differs from SOURCES.json")
        except Exception as e:
            errors.append(f"{rec['file']}: unreadable image ({e})")
    return errors, images


def check_repo(base, repo, images):
    errors = []
    for rec in images:
        f = repo / rec["repo_path"]
        if not f.is_file():
            errors.append(f"repo file missing: {rec['repo_path']}")
        elif sha(f.read_bytes()) != rec["sha256"]:
            errors.append(f"{rec['repo_path']} differs from the copy in the skill: rebuild with tools/art_skill_build.py")
    cfg = json.loads((repo / "config/art_style.json").read_text())
    rows = {}
    for line in (base / "references/FAMILIES.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0] in cfg["families"]:
            rows[cells[0]] = cells
    att = cfg["gpt_max_attempts"]
    for fam, spec in cfg["families"].items():
        want = [fam, cfg["gpt_reference_sets"]["register_of_family"][fam], SIZES[spec["aspect"]], f"{spec['print_w_in']} in", str(att.get(fam, att["default"]))]
        if rows.get(fam, [])[:5] != want:
            errors.append(f"FAMILIES.md row for {fam} is {rows.get(fam, [])[:5]}, repo says {want}")
    qf = repo / "production/art/gpt/QUEUE.json"
    if not qf.is_file():
        errors.append("QUEUE.json not found in the repo")
    else:
        q = json.loads(qf.read_text())
        if q.get("schema", 1) < 2:
            errors.append("QUEUE.json is schema 1")
        for it in q["items"]:
            pf = repo / it["prompt"]
            text = pf.read_text() if pf.is_file() else None
            if text is None or sha((text[:-1] if text.endswith("\n") else text).encode()) != it["prompt_sha256"]:
                errors.append(f"{it['id']}: prompt file missing or not matching the queue hash")
            for r in it["references"]:
                if not (repo / r).is_file():
                    errors.append(f"{it['id']}: reference missing {r}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", type=Path)
    ap.add_argument("--repo", type=Path)
    a = ap.parse_args()
    tmp = None
    base = HERE
    errors = []
    if a.zip:
        tmp = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(a.zip) as z:
            if z.testzip() is not None:
                errors.append("zip CRC error")
            if "SKILL.md" not in z.namelist():
                errors.append("SKILL.md is not at the zip root")
            z.extractall(tmp.name)
        base = Path(tmp.name)
    pk, images = check_package(base)
    errors += pk
    if a.repo:
        errors += check_repo(base, a.repo.resolve(), images)
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "checked": str(a.zip or base), "repo": str(a.repo) if a.repo else None,
                      "errors": errors}, indent=1))
    if tmp:
        tmp.cleanup()
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
