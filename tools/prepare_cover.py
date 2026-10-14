#!/usr/bin/env python3
"""Front-cover art supplied by the owner (2026-10-14): assets/art/cover/front-owner.jpg.

The picture carries its own lettering (HERALDRY and the subtitle), so it is used as the whole front cover,
not as a vignette under live type. Deterministic conversion only, no redrawing: the greyscale is upscaled
3x (Lanczos), paper white is cut to transparent and the ink is pure black, so the paper colour of the
cream or white edition shows through. build_extras.cover_art() fits it inside the 0.375 in safe edge.

    python3 tools/prepare_cover.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/art/cover/front-owner.jpg"
OUT = ROOT / "assets/art/cover/front.png"
SCALE = 3
WHITE, BLACK = 238, 40      # levels: at or above WHITE is paper, at or below BLACK is solid ink


def main():
    g = Image.open(SRC).convert("L")
    g = g.resize((g.width * SCALE, g.height * SCALE), Image.LANCZOS)
    a = np.asarray(g, dtype=np.float32)
    alpha = np.clip((WHITE - a) / (WHITE - BLACK), 0, 1) * 255
    rgba = np.zeros(a.shape + (4,), dtype=np.uint8)
    rgba[..., 3] = alpha.astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT, optimize=True)
    print(f"{OUT.relative_to(ROOT)}: {rgba.shape[1]}x{rgba.shape[0]} (source {g.width // SCALE}x{g.height // SCALE})")


if __name__ == "__main__":
    main()
