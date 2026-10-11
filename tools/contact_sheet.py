#!/usr/bin/env python3
"""Render PDF pages to contact sheets or single page PNGs for visual review (scratch output)."""
import argparse
from pathlib import Path
import pymupdf
from PIL import Image


def render(doc, i, dpi):
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(dpi / 72, dpi / 72))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pages", help="1-based range a-b (contact sheet) or list a,b,c")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--dpi", type=float, default=28)
    ap.add_argument("--single", action="store_true", help="write one PNG per page instead of a sheet")
    ap.add_argument("--crop", help="x0,y0,x1,y1 in pt for detail crops")
    ap.add_argument("--scale", type=float, default=1.0, help="centre scale for overscan stress (e.g. 1.03)")
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    if a.pages and "-" in a.pages:
        s, e = a.pages.split("-")
        pages = list(range(int(s) - 1, min(int(e), len(doc))))
    elif a.pages:
        pages = [int(x) - 1 for x in a.pages.split(",")]
    else:
        pages = list(range(len(doc)))
    out = Path(a.out)
    if a.single:
        out.mkdir(parents=True, exist_ok=True)
        for i in pages:
            page = doc[i]
            mat = pymupdf.Matrix(a.dpi / 72, a.dpi / 72)
            if a.scale != 1.0:
                s = a.scale
                w, h = page.rect.width, page.rect.height
                pix = page.get_pixmap(matrix=pymupdf.Matrix(s * a.dpi / 72, s * a.dpi / 72), alpha=False)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                W, H = round(w * a.dpi / 72), round(h * a.dpi / 72)
                x0, y0 = (img.width - W) // 2, (img.height - H) // 2
                img = img.crop((x0, y0, x0 + W, y0 + H))
            elif a.crop:
                x0, y0, x1, y1 = map(float, a.crop.split(","))
                pix = page.get_pixmap(matrix=mat, clip=pymupdf.Rect(x0, y0, x1, y1))
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            else:
                img = render(doc, i, a.dpi)
            img.save(out / f"p{i+1:03d}.png")
        return
    ims = [render(doc, i, a.dpi) for i in pages]
    w, h = ims[0].size
    rows = (len(ims) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * (w + 6) + 6, rows * (h + 6) + 6), (90, 90, 90))
    for k, im in enumerate(ims):
        sheet.paste(im, (6 + (k % a.cols) * (w + 6), 6 + (k // a.cols) * (h + 6)))
    sheet.save(out)


if __name__ == "__main__":
    main()
