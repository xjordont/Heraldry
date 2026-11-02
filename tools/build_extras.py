#!/usr/bin/env python3
"""Cover data (verbatim manuscript text) for the digital edition's front and back covers: build/cover.json."""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from content_anchors import resolve
from parse_source import plain  # noqa: E402


def cover_art():
    """Owner-supplied full-page front cover when present (assets/art/cover/front.png, from tools/prepare_cover.py):
    fitted inside the 0.375 in safe edge of US Letter. Otherwise generated ink cover art when selected, else the original master; fits 4.8 x 3.67 in at <= native 300 ppi."""
    from PIL import Image
    from build_book import load_spot_art
    full = ROOT / "assets/art/cover/front.png"
    if full.is_file():
        wpx, hpx = Image.open(full).size
        w = min(8.5 - 2 * 0.375, (11 - 2 * 0.375) * wpx / hpx)
        return {"path": "../assets/art/cover/front.png", "w_in": round(w, 3), "h_in": round(w * hpx / wpx, 3), "full_page": True}
    _, ids = load_spot_art()
    if "ART-COVER-002" in ids:
        rel, w = ids["ART-COVER-002"]
        wpx, hpx = Image.open(ROOT / rel[3:]).size
        h = w * hpx / wpx
        if h > 3.667:
            w, h = w * 3.667 / h, 3.667
        return {"path": rel, "w_in": round(w, 3), "h_in": round(h, 3)}
    return {"path": "../assets/art/incoming/ART-COVER-001.png", "w_in": 4.767, "h_in": 3.667}


def back_cover_art():
    """The approved ink party scene (ART-COVER-002) for the back cover once the owner's full-page
    picture fronts the book: at most 4.4 in wide and never above native 300 ppi."""
    from PIL import Image
    from build_book import load_spot_art
    _, ids = load_spot_art()
    if "ART-COVER-002" not in ids:
        return None
    rel, w = ids["ART-COVER-002"]
    wpx, hpx = Image.open(ROOT / rel[3:]).size
    w = min(4.4, wpx / 300)
    return {"path": rel, "w_in": round(w, 3), "h_in": round(w * hpx / wpx, 3)}


def cover_data():
    m = json.loads((ROOT / "build/blocks.json").read_text())
    blocks = {}

    def walk(bs):
        for b in bs:
            blocks[b["id"]] = b
            for it in b.get("items", []):
                walk(it["blocks"])
            walk(b.get("blocks", []))
    for ch in m["chapters"]:
        walk(ch["blocks"])
    fr = m["chapters"][0]["blocks"]
    t1, _, t2 = fr[0]["title"].partition(": ")
    anchors = resolve()
    lead = plain(blocks[anchors["cover-lead"]]["c"])
    # verbatim sentences from 1.1 (B00169, B00173, B00175)
    facts = []
    for bid, take in ((anchors["cover-fact-1"], None), (anchors["cover-fact-2"], 1), (anchors["cover-fact-3"], None)):
        txt = plain(blocks[bid]["c"])
        facts.append(txt if take is None else txt.split(". ")[0] + ".")
    # The back cover opens with its own blurb (editorial/back_cover.json), so the first words a reader
    # sees outside the book are not repeated word for word as the Chapter 1 lead (design review 2026-10-29).
    blurb = ROOT / "editorial/back_cover.json"
    if blurb.exists():
        lead = json.loads(blurb.read_text(encoding="utf-8"))["blurb"]
    meta = json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))["verified_publication_metadata"]
    data = {"title": [t1, t2], "subtitle": plain(fr[1]["c"]), "version": plain(fr[2]["c"]),
            "lead": lead, "facts": facts, "art": cover_art(), "publisher": meta.get("publisher"),
            "author": meta.get("author_credit"),
            "source_blocks": ["h-heraldry-skirmish-the-dying-lands", "B00003", "B00005", "B00169", "B00173", "B00175"]}
    if data["art"].get("full_page"):
        data["back_art"] = back_cover_art()
    (ROOT / "build/cover.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return data


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    d = cover_data()
    print(json.dumps({k: d[k] for k in ("title", "version")}))


if __name__ == "__main__":
    main()
