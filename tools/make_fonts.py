#!/usr/bin/env python3
"""Derive static font instances from the bundled OFL variable fonts.

Sources: fonts/variable/* downloaded from github.com/google/fonts (ofl/sourceserif4,
ofl/sourcesans3, ofl/cinzel); licences in fonts/licences/. Static instances are
renamed so every style shares one family name (Typst groups by family name).
Source Serif 4 is pinned at optical size 11 (text) for body sizes.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
VAR, OUT = ROOT / "fonts/variable", ROOT / "fonts/static"

JOBS = [
    ("SourceSerif4[opsz,wght].ttf", "Source Serif 4", "SourceSerif4", {"Regular": 400, "Semibold": 600, "Bold": 700}, False, {"opsz": 11}),
    ("SourceSerif4-Italic[opsz,wght].ttf", "Source Serif 4", "SourceSerif4", {"Italic": 400, "SemiboldItalic": 600, "BoldItalic": 700}, True, {"opsz": 11}),
    ("SourceSans3[wght].ttf", "Source Sans 3", "SourceSans3", {"Regular": 400, "Semibold": 600, "Bold": 700}, False, {}),
    ("SourceSans3-Italic[wght].ttf", "Source Sans 3", "SourceSans3", {"Italic": 400, "SemiboldItalic": 600, "BoldItalic": 700}, True, {}),
    ("Cinzel[wght].ttf", "Cinzel", "Cinzel", {"Regular": 400, "Semibold": 600, "Bold": 700}, False, {}),
]


def style_name(style):
    return {"Regular": "Regular", "Italic": "Italic", "Bold": "Bold", "BoldItalic": "Bold Italic",
            "Semibold": "Semibold", "SemiboldItalic": "Semibold Italic"}[style]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for src, family, ps, styles, italic, extra in JOBS:
        for style, w in styles.items():
            f = instantiateVariableFont(TTFont(VAR / src), {"wght": w, **extra}, updateFontNames=False)
            name = f["name"]
            for rec in list(name.names):
                if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 25):
                    name.removeNames(nameID=rec.nameID)
            sub = style_name(style)
            name.setName(family, 1, 3, 1, 0x409)
            name.setName(sub, 2, 3, 1, 0x409)
            name.setName(f"{family} {sub}", 4, 3, 1, 0x409)
            name.setName(f"{ps}-{style}", 6, 3, 1, 0x409)
            name.setName(f"{ps}-{style};heraldry-static", 3, 3, 1, 0x409)
            os2 = f["OS/2"]
            os2.usWeightClass = w
            sel = 0
            if italic:
                sel |= 1
            if w >= 700:
                sel |= 1 << 5
            if not italic and w < 700 and w == 400:
                sel |= 1 << 6
            os2.fsSelection = (os2.fsSelection & ~0b1100001) | sel
            f["head"].macStyle = (1 if w >= 700 else 0) | (2 if italic else 0)
            if "STAT" in f:
                del f["STAT"]
            f.save(OUT / f"{ps}-{style}.ttf")
            print(OUT / f"{ps}-{style}.ttf")


if __name__ == "__main__":
    main()
