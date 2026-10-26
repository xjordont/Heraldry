#!/usr/bin/env python3
"""Render the Hero Record from its HTML sources.

  python3 assets/hero-record/render.py [--pdf OUT.pdf]

Always writes 2550x3300 (300 dpi, US Letter) PNGs to assets/hero-record/previews/.
With --pdf, also writes the two-page print PDF to the given path (PDFs are never committed;
publish through a GitHub Release). Needs Playwright with Chromium.
"""
import argparse
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SIDES = [("hero-record-front", "Hero_Record_Front_2550x3300.png"),
         ("hero-record-reverse", "Hero_Record_Reverse_2550x3300.png")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=pathlib.Path)
    args = ap.parse_args()
    (HERE / "previews").mkdir(exist_ok=True)
    pdfs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for stem, png in SIDES:
            pg = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2550 / 816)
            pg.goto((HERE / f"{stem}.html").as_uri())
            pg.wait_for_timeout(800)
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(HERE / "previews" / png))
            if args.pdf:
                out = HERE / "previews" / f"_{stem}.pdf"
                pg.pdf(path=str(out), width="8.5in", height="11in", print_background=True, page_ranges="1")
                pdfs.append(out)
        b.close()
    if args.pdf:
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter()
        for f in pdfs:
            w.add_page(PdfReader(str(f)).pages[0])
            f.unlink()
        w.write(str(args.pdf))


if __name__ == "__main__":
    main()
