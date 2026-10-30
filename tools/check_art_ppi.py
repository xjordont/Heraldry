#!/usr/bin/env python3
"""Fail if any placed raster image in the given PDFs prints below 300 ppi at its placed size.

Owner instruction 2026-10-29: all art must reach at least 300 ppi in print. Effective resolution is
pixels divided by placed inches, on the image's tighter axis, for every placement on every page.

usage: python tools/check_art_ppi.py FILE.pdf [FILE.pdf ...] [--minimum 300]
"""
import argparse
import sys

import pymupdf


def lowest(path):
    worst = (float("inf"), None)
    with pymupdf.open(path) as doc:
        for number, page in enumerate(doc, 1):
            for image in page.get_image_info():
                box = pymupdf.Rect(image["bbox"])
                if box.width < 2 or box.height < 2:
                    continue
                ppi = min(image["width"] / (box.width / 72), image["height"] / (box.height / 72))
                if ppi < worst[0]:
                    worst = (ppi, {"page": number, "pixels": [image["width"], image["height"]],
                                   "placed_in": [round(box.width / 72, 3), round(box.height / 72, 3)]})
    return worst


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--minimum", type=float, default=300)
    a = ap.parse_args()
    failed = False
    for path in a.pdfs:
        ppi, where = lowest(path)
        if where is None:
            print(f"PASS {path}: no raster art")
        elif ppi + 0.5 < a.minimum:
            failed = True
            print(f"FAIL {path}: {ppi:.0f} ppi at {where}")
        else:
            print(f"PASS {path}: lowest placed art {ppi:.0f} ppi")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
