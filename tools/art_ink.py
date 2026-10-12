#!/usr/bin/env python3
"""Deterministic ink preparation: generated RGB master -> pure-black ink on transparent alpha.

The page substrate (cream or white) shows through, so one asset prints on both editions.
Never upscales; reports the native print width at 300 ppi and simple defect flags
(colour, gray wash, ink touching the image border, which suggests a frame or box)."""
import argparse, json
from pathlib import Path
from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def prep(src: Path, dst: Path, margin_px: int = 12) -> dict:
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im)
    im = im.convert("RGB")
    # colour = HSV saturation over 60 and a channel spread over 24 levels (the skill helper uses the same formula),
    # so near-black ink with a faint warm tint does not count as colour
    r, gch, b = im.split()
    spread = ImageChops.subtract(ImageChops.lighter(ImageChops.lighter(r, gch), b),
                                 ImageChops.darker(ImageChops.darker(r, gch), b))
    sat = ImageChops.multiply(im.convert("HSV").getchannel("S").point(lambda v: 255 if v > 60 else 0),
                              spread.point(lambda v: 255 if v > 24 else 0))
    colour_frac = sum(sat.histogram()[255:]) / (im.width * im.height)
    g = ImageOps.grayscale(im)
    hist = g.histogram()
    n = im.width * im.height

    def pct(p):
        acc = 0
        for v, c in enumerate(hist):
            acc += c
            if acc >= p * n:
                return v
        return 255
    # paper level = bright percentile; ink level = dark percentile (robust to noise)
    white = max(pct(0.90), 200)
    black = min(pct(0.01), 90)
    lo, hi = black + 10, white - 18
    span = max(hi - lo, 1)

    def alpha(v):
        if v >= hi:
            return 0
        if v <= lo:
            return 255
        t = (hi - v) / span          # 0 at paper, 1 at ink
        return int(round(255 * min(1.0, t ** 0.8 * 1.15)))
    a = g.point(alpha)
    # gray wash: substantial mid-tone area that is neither paper nor ink
    mids = sum(hist[lo + 25:hi - 25]) / n if hi - lo > 60 else 0.0
    bbox = a.point(lambda v: 255 if v > 24 else 0).getbbox()
    if bbox is None:
        raise ValueError(f"{src}: no ink found")
    edge = 3
    border_ink = 0
    bw = a.point(lambda v: 255 if v > 128 else 0)
    for box in ((0, 0, a.width, edge), (0, a.height - edge, a.width, a.height), (0, 0, edge, a.height), (a.width - edge, 0, a.width, a.height)):
        h = bw.crop(box).histogram()
        border_ink += h[255] / max(1, (box[2] - box[0]) * (box[3] - box[1]))
    border_ink /= 4
    l, t, r, b = bbox
    l, t = max(0, l - margin_px), max(0, t - margin_px)
    r, b = min(a.width, r + margin_px), min(a.height, b + margin_px)
    a = a.crop((l, t, r, b))
    out = Image.new("LA", a.size, 0)
    out.putalpha(a)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, optimize=True)
    flags = []
    if colour_frac > 0.10:
        flags.append("colour")
    if mids > 0.60:
        flags.append("gray_wash")
    if border_ink > 0.25:
        flags.append("frame_or_box")
    return {"src": str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src), "dst": str(dst.relative_to(ROOT)) if dst.is_relative_to(ROOT) else str(dst),
            "native_px": [im.width, im.height], "ink_px": list(a.size), "max_print_w_in_300ppi": round(a.size[0] / 300, 3),
            "levels": [lo, hi], "colour_frac": round(colour_frac, 4), "midtone_frac": round(mids, 4),
            "border_ink": round(border_ink, 4), "flags": flags}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    a = ap.parse_args()
    print(json.dumps(prep(a.src.resolve(), a.dst.resolve())))


if __name__ == "__main__":
    main()
