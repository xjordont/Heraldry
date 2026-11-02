#!/usr/bin/env python3
"""Extract the representative stress specimen (production material, not the book)
from the interior composition by locating actual-content anchors."""
import json
from pathlib import Path
import pymupdf

from manuscript import version
from content_anchors import resolve
ROOT = Path(__file__).resolve().parents[1]

# (purpose, search text) — first page containing the text after the contents pages
TARGETS = [
    ("Chapter opening", "2.1 Core Terms"),
    ("Two-column rules + worked example", "Example: An effect pushes a Skeleton"),
    ("Facing page: sustained procedure", "3.1 Overview of a Round"),
    ("Short random-result table", "ANCHOR:specimen-short-table"),
    ("Numeric equipment table (multi-page, repeated header)", "7.8 Melee Weapons"),
    ("Widest source table as labelled entries (T082, 12 columns)", "ANCHOR:specimen-wide-table"),
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
    anchors = resolve()
    audit = json.loads((ROOT / "production/qa/table-audit.json").read_text())
    tpages = {r["id"]: r["pdf_pages"][0] - 1 for r in audit["rows"] if r["pdf_pages"]}
    for purpose, needle in TARGETS:
        if needle.startswith("ANCHOR:"):
            picks.append((purpose, tpages.get(anchors[needle[7:]])))
            continue
        for i in range(start, len(doc)):
            if doc[i].search_for(needle):
                picks.append((purpose, i))
                break
        else:
            picks.append((purpose, None))
    missing = [purpose for purpose, page in picks if page is None]
    if missing:
        raise SystemExit(f"Specimen targets missing: {missing}")
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
                      f"PRODUCTION SPECIMEN — representative pages extracted from the {version()} build for design review. "
                      "Not the finished book.", fontsize=10, fontname="helv", align=1)
    dst = ROOT / f"dist/specimen/Heraldry_{version()}_specimen.pdf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, garbage=3, deflate=True)
    from pypdf import PdfReader
    labels = PdfReader(str(src)).page_labels
    manifest = [{"purpose": p, "book_page_index": (i + 1 if i is not None else None),
                 "folio": (labels[i] if i is not None else None)} for p, i in picks]
    (ROOT / "dist/specimen/specimen_pages.json").write_text(json.dumps(manifest, indent=1))
    print(json.dumps(manifest, indent=0))


if __name__ == "__main__":
    main()
