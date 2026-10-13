#!/usr/bin/env python3
"""Composition guides for the Codex backgrounds (owner 2026-10-13).

Writes production/art/composition/<ID>.jpg from the Nano Banana comparison version named in GUIDES.json:
greyscale, paper tone pushed to white, 1024 px. The guide shows layout only (what sits where, on what, from
which angle); the prompt tells the worker to take the ink style from the style references, not from the guide.

    python3 tools/art_composition.py build
"""
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "production/art/composition"


def guides():
    return json.loads((DIR / "GUIDES.json").read_text())["guides"]


def guide_path(i):
    """Repo-relative path of an entry's guide image, or None."""
    return f"production/art/composition/{i}.jpg" if i in guides() else None


def build():
    for i, n in guides().items():
        im = ImageOps.autocontrast(Image.open(ROOT / f"assets/art/variants/{i}/nb-{n}.png").convert("L"), cutoff=2)
        im = im.point(lambda v: 255 if v > 215 else v).resize((1024, 1024), Image.LANCZOS)
        im.save(DIR / f"{i}.jpg", quality=90)
        print(f"{i}: nb-{n}")


if __name__ == "__main__":
    build()
