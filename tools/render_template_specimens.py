#!/usr/bin/env python3
"""Render the book-template specimen sheets (typst/templates/specimens.typ) to PNG pages.

Specimens show each page template set with real manuscript excerpts and approved art. They are
design evidence, not a book build: the output is PNG only (build/specimens/), never a PDF.

    python3 tools/render_template_specimens.py [--ppi 110] [--substrate cream|white] [--sheet]
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "typst/templates/specimens.typ"
OUT = ROOT / "build/specimens"
FONTS = [str(ROOT / "fonts/static")]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ppi", type=float, default=110)
    ap.add_argument("--substrate", choices=("cream", "white"), default="cream")
    ap.add_argument("--lead", choices=("justify", "center"), default="justify", help="flavour alignment (justify is the design)")
    ap.add_argument("--sheet", action="store_true", help="also write a contact sheet of all pages")
    a = ap.parse_args()
    import typst
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob(f"specimen-{a.substrate}-*.png"):
        old.unlink()
    pages = typst.compile(str(SRC), root=str(ROOT), format="png", ppi=a.ppi, font_paths=FONTS,
                          sys_inputs={"substrate": a.substrate, "lead": a.lead})
    pages = pages if isinstance(pages, list) else [pages]
    files = []
    for i, data in enumerate(pages, 1):
        f = OUT / f"specimen-{a.substrate}-{i:02d}.png"
        f.write_bytes(data)
        files.append(f)
    print(f"{len(files)} specimen pages in {OUT.relative_to(ROOT)}")
    if a.sheet and files:
        from PIL import Image
        ims = [Image.open(f).convert("RGB") for f in files]
        w, h = ims[0].size
        scale = 360 / w
        tw, th = int(w * scale), int(h * scale)
        cols = min(4, len(ims))
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + 16) + 16, rows * (th + 16) + 16), (120, 120, 120))
        for k, im in enumerate(ims):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (16 + (k % cols) * (tw + 16), 16 + (k // cols) * (th + 16)))
        s = OUT / f"specimen-{a.substrate}-sheet.jpg"
        sheet.save(s, quality=88)
        print(f"contact sheet {s.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
