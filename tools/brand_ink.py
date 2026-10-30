#!/usr/bin/env python3
"""Publisher logo (Escutcheon Press, owner-supplied 2026-10-30) -> pure-black ink on transparent alpha.

Like tools/art_ink.py, the paper is removed so one asset prints on cream and white. The logo's
scanned paper is textured (paper 219-252), so the paper level sits below its darkest grain and
isolated specks are cleared; the crop keeps only the mark and its lettering.

usage: python tools/brand_ink.py [SRC] [DST]
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/art/brand/escutcheon-press-logo-source.jpg"
DST = ROOT / "assets/art/brand/escutcheon-press-logo.png"
PAPER, INK, MARGIN = 205, 40, 20


def prep(src=SRC, dst=DST):
    g = Image.open(src).convert("L")

    def alpha(v):
        if v >= PAPER:
            return 0
        if v <= INK:
            return 255
        return int(round(255 * ((PAPER - v) / (PAPER - INK)) ** 0.85))
    a = g.point(alpha)
    # clear isolated grain: keep alpha only where a small neighbourhood holds real ink
    core = a.filter(ImageFilter.MaxFilter(9)).point(lambda v: 255 if v > 150 else 0)
    a = Image.composite(a, Image.new("L", a.size, 0), core)
    l, t, r, b = a.point(lambda v: 255 if v > 40 else 0).getbbox()
    a = a.crop((max(0, l - MARGIN), max(0, t - MARGIN), min(a.width, r + MARGIN), min(a.height, b + MARGIN)))
    out = Image.new("LA", a.size, 0)
    out.putalpha(a)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, optimize=True)
    return {"src": str(Path(src).relative_to(ROOT)), "dst": str(Path(dst).relative_to(ROOT)),
            "ink_px": list(a.size), "max_print_w_in_300ppi": round(a.size[0] / 300, 3)}


if __name__ == "__main__":
    args = [Path(x).resolve() for x in sys.argv[1:3]]
    print(json.dumps(prep(*args)))
