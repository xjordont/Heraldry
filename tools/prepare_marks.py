#!/usr/bin/env python3
"""Turn the owner-approved heraldic mark candidates into the book's production marks.

Owner approval 2026-10-13 ("Approved. Make sure they are big enough to see."); the choices are in
production/art/marks/APPROVED.json. For each chapter arm, the charge inside the shield is lifted out
of its candidate and set inside one shared shield (the rim of the template candidate), so all fifteen
match exactly. The result is traced to vector paths (potrace; `pip install potracer`) and written as
cream and white SVG variants to typst/templates/marks/<substrate>/arms-NN.svg; the logo goes to
logo.svg. The paper colour fills the shield field, black ink is everything else. A contact sheet goes
to build/marks/. Deterministic for a given set of inputs.

    python3 tools/prepare_marks.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "production/art/marks/APPROVED.json"
OUT = ROOT / "typst/templates/marks"
SHEET = ROOT / "build/marks"
PAPER = {"cream": "#FCFAF5", "white": "#FFFFFF"}


def binary(path):
    return np.array(Image.open(path).convert("L")) < 128          # True = ink


def outside(ink):
    """White pixels connected to the image border (the background around the shield)."""
    h, w = ink.shape
    seen = np.zeros_like(ink)
    stack = [(y, x) for y in (0, h - 1) for x in range(w)] + [(y, x) for x in (0, w - 1) for y in range(h)]
    while stack:
        y, x = stack.pop()
        if seen[y, x] or ink[y, x]:
            continue
        seen[y, x] = True
        if y > 0: stack.append((y - 1, x))
        if y < h - 1: stack.append((y + 1, x))
        if x > 0: stack.append((y, x - 1))
        if x < w - 1: stack.append((y, x + 1))
    return seen


def erode(mask, px):
    im = Image.fromarray((mask * 255).astype("uint8"))
    while px > 0:
        k = min(px, 7) * 2 - 1 if px > 1 else 3
        im = im.filter(ImageFilter.MinFilter(k))
        px -= (k - 1) // 2
    return np.array(im) > 127


def rim_depth(ink, shield):
    """Depth of the double rim, measured inward from the left edge along the middle rows."""
    ys, xs = np.nonzero(shield)
    depths = []
    for y in range(int(ys.min() + 0.35 * (ys.max() - ys.min())), int(ys.min() + 0.55 * (ys.max() - ys.min())), 6):
        row = ink[y]
        x = int(np.nonzero(shield[y])[0].min())
        runs = 0
        state = row[x]
        while x < len(row) - 1 and runs < 3:
            x += 1
            if row[x] != state:
                runs += 1
                state = row[x]
        depths.append(x - int(np.nonzero(shield[y])[0].min()))
    return int(np.median(depths))


def parts(path):
    ink = binary(path)
    out = outside(ink)
    shield = ~out
    depth = rim_depth(ink, shield)
    interior = erode(shield, depth + 6)
    return ink, shield, interior


def bbox(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def components(mask):
    """Connected ink components (8-connected) as lists of flat indices."""
    h, w = mask.shape
    flat = mask.ravel()
    seen = np.zeros(flat.size, bool)
    out = []
    for start in np.flatnonzero(flat):
        if seen[start]:
            continue
        seen[start] = True
        stack, comp = [start], []
        while stack:
            i = stack.pop()
            comp.append(i)
            y, x = divmod(i, w)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        j = ny * w + nx
                        if flat[j] and not seen[j]:
                            seen[j] = True
                            stack.append(j)
        out.append(comp)
    return out


def clean_charge(ink, interior, band=40):
    """The charge alone: ink inside the field, minus fragments of the source's own rim, which lie
    mostly in a band just inside the field's edge."""
    charge = ink & interior
    ring = (interior & ~erode(interior, band)).ravel()
    keep = np.zeros(charge.size, bool)
    for comp in components(charge):
        idx = np.array(comp)
        if ring[idx].mean() < 0.6:
            keep[idx] = True
    return keep.reshape(charge.shape)


def compose(template, source, fill_w=0.80, fill_h=0.76, lift=0.06):
    """The template's shield and rim with the source's charge set into the template's field.

    The charge's own bounding box is fitted into a box fill_w x fill_h of the field, centred and
    lifted a little because the heater shield narrows towards its point; anything that would still
    cross the field's edge is clipped."""
    t_ink, t_shield, t_int = template
    s_ink, _, s_int = source
    charge = clean_charge(s_ink, s_int)
    cx0, cy0, cx1, cy1 = bbox(charge)
    tx0, ty0, tx1, ty1 = bbox(t_int)
    bw, bh = (tx1 - tx0) * fill_w, (ty1 - ty0) * fill_h
    scale = min(bw / (cx1 - cx0), bh / (cy1 - cy0))
    nw, nh = round((cx1 - cx0) * scale), round((cy1 - cy0) * scale)
    crop = Image.fromarray((charge[cy0:cy1, cx0:cx1] * 255).astype("uint8"))
    crop = np.array(crop.resize((nw, nh), Image.LANCZOS)) > 127
    canvas = np.zeros_like(t_ink)
    ox = tx0 + ((tx1 - tx0) - nw) // 2
    oy = ty0 + ((ty1 - ty0) - nh) // 2 - round((ty1 - ty0) * lift)
    canvas[oy:oy + nh, ox:ox + nw] = crop
    ink = (t_ink & ~t_int) | (canvas & erode(t_int, 10))
    return ink, t_shield


def trace(mask):
    import potrace
    path = potrace.Bitmap(~mask).trace(  # potracer traces False pixels
        turdsize=6, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    for curve in path:
        p = curve.start_point
        d.append(f"M{p.x:.1f},{p.y:.1f}")
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
            else:
                d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        d.append("Z")
    return "".join(d)


def svg(ink, shield, paper, pad=8):
    x0, y0, x1, y1 = bbox(shield | ink)
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad
    ink, shield = ink[y0:y1, x0:x1], shield[y0:y1, x0:x1]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x1 - x0} {y1 - y0}">'
            f'<path fill="{paper}" fill-rule="evenodd" d="{trace(shield)}"/>'
            f'<path fill="#000" fill-rule="evenodd" d="{trace(ink)}"/></svg>\n'), (ink, shield)


def main():
    spec = json.loads(APPROVED.read_text())
    cand = ROOT / spec["candidates"]
    template = parts(cand / spec["shield_template"])
    SHEET.mkdir(parents=True, exist_ok=True)
    previews = []
    jobs = [(f"arms-{int(k):02d}", v) for k, v in spec["arms"].items()] + [("logo", spec["logo"])]
    if spec.get("coin"):
        jobs.append(("coin", spec["coin"]))
    traced = {}
    for name, src in jobs:
        if name in ("logo", "coin"):
            ink = binary(cand / src)
            shield = ~outside(ink)
        else:
            ink, shield = compose(template, parts(cand / src))
        traced[name] = (ink, shield)
        print(f"{name}: {src}")
    for sub, paper in PAPER.items():
        d = OUT / sub
        d.mkdir(parents=True, exist_ok=True)
        for name, (ink, shield) in traced.items():
            text, crop = svg(ink, shield, paper)
            (d / f"{name}.svg").write_text(text)
            if name == "coin":
                # reversed coin for black header bands: the ink in paper colour, the field left open
                rev = text.replace(f'<path fill="{paper}" fill-rule="evenodd"', '<path fill="none" fill-rule="evenodd"', 1)
                rev = rev.replace('<path fill="#000"', f'<path fill="{paper}"')
                (d / "coin-reversed.svg").write_text(rev)
            if sub == "cream":
                previews.append((name, crop))
    cell = 220
    sheet = Image.new("RGB", (cell * 8, cell * 2), "white")
    for i, (name, (ink, shield)) in enumerate(previews):
        im = Image.fromarray(np.where(ink, 0, 255).astype("uint8")).convert("RGB")
        im.thumbnail((cell - 12, cell - 12))
        sheet.paste(im, ((i % 8) * cell + 6, (i // 8) * cell + 6))
    sheet.save(SHEET / "approved-marks.png")
    print(f"{len(traced)} marks written to {OUT.relative_to(ROOT)}/<substrate>/; sheet {(SHEET / 'approved-marks.png').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
