#!/usr/bin/env python3
"""Page-review aids for the exact cream PDF: all-page contact sheets, detail pages, the calibration sheet, and a manifest.

Written into production/qa/review/ (Git LFS; replaced on every build, so main holds only the latest). A reviewer views every
file and records what was seen. Deterministic for a given PDF. Producing these aids changes no gate and no ledger.

    python tools/review_aids.py build --pdf dist/X_inkjet-borderless.pdf --calibration dist/X_inkjet-calibration.pdf --covers dist/X_covers-front-back.pdf [--out DIR]

The inkjet edition has no covers inside it (they are the separate covers PDF: page 1 is the title page and the last page is the end of the
index), so the covers get their own images, cover-front.jpg and cover-back.jpg.
"""
import argparse
import hashlib
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PER_SHEET, COLS, SHEET_DPI, DETAIL_DPI, EVERY = 24, 6, 34, 100, 50


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def render(doc, i, dpi):
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(dpi / 72, dpi / 72))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def detail_pages(doc):
    """(page, reason): first and last page, every chapter opener (outline level 1), and every EVERY-th page."""
    n = len(doc)
    pick = {1: "first page (title page; the covers are in the covers PDF)", n: "last page"}
    for lvl, title, page in doc.get_toc():
        if lvl == 1 and 1 <= page <= n:
            pick.setdefault(page, f"chapter opener: {title[:60]}")
    for p in range(EVERY, n, EVERY):
        pick.setdefault(p, f"every {EVERY}th page")
    return sorted(pick.items())


def build(pdf, calibration, covers, out):
    out.mkdir(parents=True, exist_ok=True)
    for old in list(out.glob("*.jpg")) + list(out.glob("manifest.json")):
        old.unlink()
    doc = pymupdf.open(pdf)
    n = len(doc)
    font = ImageFont.load_default(size=15)
    sheets = []
    for s, a in enumerate(range(0, n, PER_SHEET), 1):
        pages = list(range(a, min(a + PER_SHEET, n)))
        thumbs = [render(doc, i, SHEET_DPI) for i in pages]
        w, h = thumbs[0].size
        rows = -(-len(pages) // COLS)
        sheet = Image.new("RGB", (COLS * (w + 8) + 8, rows * (h + 26) + 8), (150, 150, 150))
        d = ImageDraw.Draw(sheet)
        for k, (i, t) in enumerate(zip(pages, thumbs)):
            x, y = 8 + (k % COLS) * (w + 8), 8 + (k // COLS) * (h + 26)
            sheet.paste(t, (x, y))
            d.text((x + 2, y + h + 4), f"p{i + 1}", fill=(255, 255, 255), font=font)
        f = out / f"sheet-{s:02d}.jpg"
        sheet.save(f, quality=72)
        sheets.append({"file": f.name, "pages": [pages[0] + 1, pages[-1] + 1], "sha256": sha(f)})
    details = []
    for p, why in detail_pages(doc):
        f = out / f"page-{p:04d}.jpg"
        render(doc, p - 1, DETAIL_DPI).save(f, quality=80)
        details.append({"file": f.name, "page": p, "reason": why, "sha256": sha(f)})
    cal = pymupdf.open(calibration)
    cal_file = out / "calibration.jpg"
    render(cal, 0, 60).save(cal_file, quality=80)
    cov = pymupdf.open(covers)
    cover_items = []
    for role, idx in (("front", 0), ("back", len(cov) - 1)):
        f = out / f"cover-{role}.jpg"
        render(cov, idx, DETAIL_DPI).save(f, quality=80)
        cover_items.append({"file": f.name, "role": role, "sha256": sha(f)})
    man = {"pdf": Path(pdf).name, "covers": cover_items, "pdf_sha256": sha(pdf), "pages": n, "sheets": sheets, "details": details,
           "calibration": {"file": cal_file.name, "sha256": sha(cal_file)},
           "note": f"{len(sheets)} contact sheets of {PER_SHEET} pages at {SHEET_DPI} dpi cover every page; {len(details)} detail pages at {DETAIL_DPI} dpi."}
    (out / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print(f"{len(sheets)} sheets, {len(details)} detail pages, calibration -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["build"])
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--covers", required=True)
    ap.add_argument("--out", default=str(ROOT / "production/qa/review"))
    a = ap.parse_args()
    build(a.pdf, a.calibration, a.covers, Path(a.out))


if __name__ == "__main__":
    main()
