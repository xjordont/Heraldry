"""Deterministic text-width estimates from the bundled static fonts (advance widths, no kerning)."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parents[1] / "fonts/static"


class Face:
    def __init__(self, file: str):
        with TTFont(FONTS / file, lazy=True) as f:
            self.upem = f["head"].unitsPerEm
            cmap = f.getBestCmap()
            hmtx = f["hmtx"].metrics
            self.adv = {cp: hmtx[g][0] for cp, g in cmap.items()}
            self.default = hmtx[cmap.get(ord("n"))][0]

    def width(self, s: str, size: float) -> float:
        return sum(self.adv.get(ord(ch), self.default) for ch in s) * size / self.upem


@lru_cache(None)
def face(name: str) -> Face:
    return Face(name)


def width(s: str, size: float, family="SourceSans3", weight="Regular") -> float:
    return face(f"{family}-{weight}.ttf").width(s, size)
