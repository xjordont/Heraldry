#!/usr/bin/env python3
"""Extract the representative stress specimen (production material, not the book)
from the cream interior by locating actual-content anchors, plus overscan stress renders."""
import json, sys
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[1]

# (purpose, search text) — first page containing the text after the contents pages
TARGETS = [
    ("Chapter opening", "2.1 Core Terms"),
    ("Two-column rules + worked example", "Example: An effect pushes a Skeleton"),
    ("Facing page: sustained procedure", "3.1 Overview of a Round"),
    ("Short random-result table", "Random Background Table (d20)"),
    ("Numeric equipment table (multi-page, repeated header)", "7.8 Melee Weapons"),
    ("Widest source table as labelled entries (T082, 12 columns)", "Tier 5 Legendary Artifact Armour and Shields"),
    ("Longest prose cells / long-description table", "Specialist Hireling Roster"),
    ("Monster profiles", "Giant Tarantula [Skirmisher]"),
    ("Scenario with canonical scaling fields", "Scenario 2: The Whispering Grove"),
    ("Appendix reference page", "C.5 Reactions Summary"),
    ("Rules diagram", "FIG-"),
    ("Index slice", "Main entries follow the terms"),
]


def main():
    src = ROOT / "build/book-cream.pdf"
    doc = pymupdf.open(src)
    start = 6
    picks = []
    for purpose, needle in TARGETS:
        for i in range(start, len(doc)):
            if doc[i].search_for(needle):
                picks.append((purpose, i))
                break
        else:
            picks.append((purpose, None))
    pages = []
    for p, i in picks:
        if i is not None and i not in pages:
            pages.append(i)
    # keep a facing pair for the first two-column example page
    out = pymupdf.open()
    out.insert_pdf(doc, from_page=0, to_page=0)  # title page as label carrier
    for i in sorted(pages):
        out.insert_pdf(doc, from_page=i, to_page=i)
    # stamp page 1 as production material
    pg = out[0]
    pg.insert_textbox(pymupdf.Rect(72, 640, 540, 720),
                      "PRODUCTION SPECIMEN — representative pages extracted from the RC484 build for design review. "
                      "Not the finished book.", fontsize=10, fontname="helv", align=1)
    dst = ROOT / "dist/specimen/Heraldry_RC484_specimen.pdf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, garbage=3, deflate=True)
    manifest = [{"purpose": p, "book_page_index": (i + 1 if i is not None else None),
                 "folio": (doc[i].get_label() if i is not None else None)} for p, i in picks]
    (ROOT / "dist/specimen/specimen_pages.json").write_text(json.dumps(manifest, indent=1))
    # overscan stress renders (1.03 centred scale, clipped to sheet)
    od = ROOT / "build/overscan"
    od.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    dpi = 80
    for i in sorted(pages):
        page = doc[i]
        s = 1.03
        pix = page.get_pixmap(matrix=pymupdf.Matrix(s * dpi / 72, s * dpi / 72), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        W, H = round(page.rect.width * dpi / 72), round(page.rect.height * dpi / 72)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im.crop((x0, y0, x0 + W, y0 + H)).save(od / f"overscan_p{i+1:03d}.png")
    print(json.dumps(manifest, indent=0))


if __name__ == "__main__":
    main()
