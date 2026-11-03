#!/usr/bin/env python3
"""Art catalogue and prompt helpers shared by art_intake, art_gpt_pack, and art_list.

The catalogue, the selections, owner-authored prompts, the structured image prompt, composition guides, and
contact sheets. Images are generated through the owner's ChatGPT plan (docs/ART_AUTOMATION.md); nothing here
calls an image API."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/art_style.json").read_text())
CATALOG = ROOT / "production/art/SPOT_CATALOG.json"
SELECTIONS = ROOT / "production/art/SELECTIONS.json"
ANCHORS = ROOT / "production/art/ANCHORS.json"
COMPOSITION = ROOT / "production/art/composition"
INK = ROOT / "assets/art/ink"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(p, default):
    return json.loads(p.read_text()) if p.exists() else default


def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ prompts
OWNER_PROMPTS = ROOT / "production/art/OWNER_PROMPTS.json"
ASPECT_WORDS = {"3:2": "Wide 3:2 landscape", "16:9": "Wide 16:9 landscape", "4:3": "4:3 landscape",
                "1:1": "Square 1:1", "2:3": "Tall 2:3 portrait", "3:4": "3:4 portrait"}


def label(e):
    if e["family"] == "cover":
        return "FRONT COVER"
    if e["family"] == "chapter":
        return "CHAPTER " + str(int(e["id"][6:8])) + " OPENER"
    return e["title"].upper()


GUIDE_TEXT = ("COMPOSITION GUIDE (the LAST attached image)\n"
              "The last attached image is a rough composition guide, not a style reference. Copy its arrangement: which objects appear, "
              "where each one sits, what it rests on, leans against or hangs from, the camera angle and the relative sizes. Keep its "
              "gravity and layout exactly. Do NOT copy its rendering: draw every object in the line character of the first style "
              "references (bold rough contours, heavy solid blacks, dense scratchy hatching and dry-brush), pure black ink on pure white, "
              "no cream tone, no grey wash, no soft or thin line. The subject is isolated on white with the usual white vignette, not cropped by the frame. "
              "If the guide and the written brief disagree about an object's form, the written brief wins.")


def guides():
    """Entry ID -> the variant each committed composition guide was made from (GUIDES.json)."""
    return json.loads((COMPOSITION / "GUIDES.json").read_text())["guides"]


def guide_path(i):
    """Repo-relative composition guide for an entry (production/art/composition), or None."""
    return f"production/art/composition/{i}.jpg" if i in guides() else None


def prompt_for(e, with_refs, guided=False):
    """Structured prompt (owner's Greythorn prompt is the model): title, intro, format and
    vignette/isolation, composition, subject details, activity, verbatim source text, style and
    atmosphere, final requirements. An owner-authored prompt overrides the whole entry."""
    owner = load(OWNER_PROMPTS, {}).get(e["id"])
    v2 = CFG["prompt_v2"]
    if owner:
        return owner + ("\n\nSTYLE REFERENCES\n" + v2["reference"] if with_refs else "")
    fam = CFG["families"][e["family"]]
    b = e.get("brief") or {}
    kind = "scene" if e["family"] in v2["scene_families"] else "still" if e["family"] in v2["still_families"] else "figure"
    where = " / ".join(e.get("context", []))
    identity = b.get("identity", "").rstrip(".") or (e.get("subject") or f"{e['title']} ({where})")
    out = [label(e) + " - GRITTY OLD-SCHOOL INK ILLUSTRATION", v2["intro"].format(identity=identity[0].lower() + identity[1:] if identity[:2] == "A " or identity[:3] == "An " or identity[:4] == "The " else identity)]
    aw = ASPECT_WORDS.get(fam["aspect"], fam["aspect"])
    out.append(("FORMAT AND WHITE VIGNETTE" if kind == "scene" else "FORMAT AND ISOLATION") + "\n"
               + "\n".join(x.format(aspect_words=aw) for x in v2["format_" + kind]))
    comp = []
    if e["family"] in ("cover", "chapter"):
        comp.append(e["subject"].rstrip(".") + ".")
        if not b.get("composition"):   # the brief's composition restates and supersedes the plan's
            comp.append(e["composition"].rstrip(".") + ".")
    if b.get("composition"):
        comp.append(b["composition"])
    if e.get("direction") and not b.get("composition"):
        comp.append(e["direction"])   # a brief expands the plan's direction and supersedes it
    if kind != "scene" or not b.get("composition"):
        comp.append(fam["framing"])
    if e["family"] in ("monster", "boss"):
        size = CFG["size_words"].get((e.get("facts") or {}).get("size_code") or "", "")
        if size:
            comp.append("Size: " + size + ".")
    out.append("COMPOSITION\n" + "\n".join(comp))
    if b.get("details") or b.get("must"):
        out.append("SUBJECT DETAILS\n" + "\n".join("* " + d for d in b.get("details", []))
                   + ("\nMust be shown exactly:\n" + "\n".join("* " + d for d in b["must"]) if b.get("must") else ""))
    if b.get("activity"):
        out.append(("HUMAN ACTIVITY" if kind == "scene" else "ACTION") + "\n" + "\n".join("* " + d for d in b["activity"]))
    if e.get("flavour"):
        out.append("SOURCE TEXT\nDepict this faithfully and invent nothing that contradicts it:\n\"" + e["flavour"] + "\"")
    atm = b.get("atmosphere", "The atmosphere is grounded, austere, mysterious and subtly ominous.")
    out.append("ARTISTIC STYLE AND ATMOSPHERE\n" + atm + "\n" + (fam.get("style") or v2.get("style_" + kind, v2["style_figure"])))
    final = ["Do not draw:"] + ["* " + x.rstrip(".") + "." for x in b["avoid"]] if b.get("avoid") else []
    final.append(fam.get("final") or v2["final_" + ("scene" if kind == "scene" else "figure")])
    out.append("FINAL VISUAL REQUIREMENTS\n" + "\n".join(final))
    if with_refs:
        out.append("STYLE REFERENCES\n" + (b.get("reference_direction") or v2["reference"]))
        if guided and guide_path(e["id"]):
            out.append(GUIDE_TEXT)
    return "\n\n".join(out)


def entries():
    return load(CATALOG, {})["entries"]


def sheet(ids, out, cell=360, cols=6):
    sels = load(SELECTIONS, {})
    ids = [i for i in ids if i in sels]
    if not ids:
        return
    rows = (len(ids) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell, rows * cell), (252, 250, 245))
    for k, i in enumerate(ids):
        im = Image.open(ROOT / sels[i]["ink"]["path"])
        im.thumbnail((cell - 16, cell - 16))
        x, y = (k % cols) * cell + (cell - im.width) // 2, (k // cols) * cell + (cell - im.height) // 2
        canvas.paste((0, 0, 0), (x, y, x + im.width, y + im.height), mask=im.getchannel("A"))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
