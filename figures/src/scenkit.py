"""scenkit: the one iconography for every setup and deployment diagram (FIG-13 to FIG-16, FIG-18 to FIG-57).

Every symbol on those diagrams is drawn by a function in this module, and every function wraps its output in
<g data-glyph="ID"> (plus data-state="illus" when it is drawn in the grey-dashed "one legal arrangement" style).
REG is the registry of glyph ids.  FIG-20 draws one swatch for every REG entry, using the same functions; the
selfcheck (fig_scenmaps.check_registry) reads the ids back out of the generated SVG files and fails if any figure
emits an id or a pattern that the key does not explain.

Stdlib only.  User units are pt.  Grayscale only.
"""
import math
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import svgkit
from svgkit import (Svg, COL_W, FULL_W, INK, DARK, MID, LIGHT, PALE, WHITE, PAT, DEFS, tw, wrap, hexpts, f1)  # noqa: F401

GREY = "#777"            # grey dashed = illustrative (one legal arrangement)
LGREY = "#aaa"
HALO = 2.6               # white halo width behind label text (pt)

EXTRA_DEFS = """<defs>
<pattern id="p-cover-l" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#fff"/><path d="M0 0.5H5M0.5 0V5" stroke="#aaa" stroke-width="0.6" fill="none"/></pattern>
<pattern id="p-diff-l" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#fff"/><circle cx="1" cy="1" r="0.7" fill="#999"/><circle cx="3" cy="3" r="0.7" fill="#999"/></pattern>
<pattern id="p-imp-l" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.6" height="2.6" fill="#fff"/><path d="M0.4 0V2.6" stroke="#aaa" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-mon-l" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="3.2" height="3.2" fill="#fff"/><path d="M0.5 0V3.2" stroke="#999" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-water" width="6" height="4" patternUnits="userSpaceOnUse"><rect width="6" height="4" fill="#fff"/><path d="M0 2.2Q1.5 0.4 3 2.2T6 2.2" stroke="#333" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-water-l" width="6" height="4" patternUnits="userSpaceOnUse"><rect width="6" height="4" fill="#fff"/><path d="M0 2.2Q1.5 0.4 3 2.2T6 2.2" stroke="#aaa" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-slip" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><rect width="6" height="6" fill="#fff"/><path d="M0.5 1.5H3.5M3.5 4.5H5.5" stroke="#333" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-slip-l" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><rect width="6" height="6" fill="#fff"/><path d="M0.5 1.5H3.5M3.5 4.5H5.5" stroke="#aaa" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-dark" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#d9d9d9"/><path d="M0 4L4 0" stroke="#fff" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-diffo" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="#222"/><circle cx="3" cy="3" r="0.8" fill="#222"/></pattern>
<pattern id="p-diffo-l" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="#999"/><circle cx="3" cy="3" r="0.8" fill="#999"/></pattern>
<pattern id="p-chasm" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#d4d4d4"/><path d="M1.5 0V6M4.5 0V6" stroke="#333" stroke-width="1.1" stroke-dasharray="2.6 1.6" fill="none"/></pattern>
<pattern id="p-chasm-l" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#efefef"/><path d="M1.5 0V6M4.5 0V6" stroke="#aaa" stroke-width="1.1" stroke-dasharray="2.6 1.6" fill="none"/></pattern>
</defs>"""

# terrain kind -> (solid fill, light fill used when the piece is illustrative)
TER = {
    "cover": ("url(#p-cover)", "url(#p-cover-l)"),
    "difficult": ("url(#p-diff)", "url(#p-diff-l)"),
    "impassable": ("url(#p-imp)", "url(#p-imp-l)"),
    "blocking": (DARK, "#c4c4c4"),
    "water": ("url(#p-water)", "url(#p-water-l)"),
    "slippery": ("url(#p-slip)", "url(#p-slip-l)"),
    "open": (WHITE, WHITE),
    "obstacle": ("#a3a3a3", "#d4d4d4"),
    "hazard": ("#cfcfcf", "#ececec"),
    "gap": (WHITE, WHITE),
    "shade": ("url(#p-dark)", "url(#p-dark)"),
    "chasm": ("url(#p-chasm)", "url(#p-chasm-l)"),
    "ledge": (WHITE, WHITE),
    "crumbling": (WHITE, WHITE),
    "coverdiff": ("url(#p-cover)", "url(#p-cover-l)"),
}
OVERLAY = {"coverdiff": ("url(#p-diffo)", "url(#p-diffo-l)")}
TERRAIN_KINDS = set(TER)
TERID = {"cover": "ter-cover", "difficult": "ter-difficult", "impassable": "ter-impassable", "blocking": "ter-blocking",
         "water": "ter-water", "slippery": "ter-slippery", "open": "ter-open", "obstacle": "ter-obstacle",
         "hazard": "ter-hazard", "gap": "ter-open", "shade": "ter-shade", "chasm": "ter-chasm", "ledge": "ledge",
         "crumbling": "ledge-crumbling", "coverdiff": "ter-coverdiff"}
# every pattern id that may appear -> the registry id that explains it in the key
PATMAP = {"p-cover": "ter-cover", "p-cover-l": "ter-cover", "p-diff": "ter-difficult", "p-diff-l": "ter-difficult",
          "p-imp": "ter-impassable", "p-imp-l": "ter-impassable", "p-mon": "mon", "p-mon-l": "mon",
          "p-water": "ter-water", "p-water-l": "ter-water", "p-slip": "ter-slippery", "p-slip-l": "ter-slippery",
          "p-dark": "ter-shade", "p-chasm": "ter-chasm", "p-chasm-l": "ter-chasm", "p-aoe": "ter-excl",
          "p-diffo": "ter-coverdiff", "p-diffo-l": "ter-coverdiff"}


class MapSvg(Svg):
    """Svg with the map patterns, per-figure clip paths and haloed label text."""

    def __init__(self, width):
        Svg.__init__(self, width)
        self.defs = []

    def add_def(self, s):
        self.defs.append(s)

    def render(self, height, title=None, desc=None):
        t = Svg.render(self, height, title=title, desc=desc)
        extra = EXTRA_DEFS
        if self.defs:
            extra = extra.replace("</defs>", "\n".join(self.defs) + "\n</defs>")
        return t.replace("</defs>", "</defs>\n" + extra, 1)

    def vtext(self, x, y, s, size=9, weight=600, anchor="middle", fill=INK):
        self.raw('<g transform="rotate(-90 %s %s)">' % (f1(x), f1(y)))
        self.text(x, y, s, size, weight, anchor, fill)
        self.raw("</g>")

    def htext(self, x, y, s, size=9, weight=600, anchor="start", fill=INK, halo=HALO):
        """Text with a white halo that hugs the letter shapes (paint-order stroke); baseline at y."""
        attrs = ' font-family="%s" font-size="%s" font-weight="%d" fill="%s" stroke="#fff" stroke-width="%s" stroke-linejoin="round" paint-order="stroke"' % (
            svgkit.FONT, f1(size), weight, fill, f1(halo))
        if anchor != "start":
            attrs += ' text-anchor="%s"' % anchor
        self.raw('<text x="%s" y="%s"%s>%s</text>' % (f1(x), f1(y), attrs, escape(s)))


# ----------------------------------------------------------------------------------------------------------------
# glyph wrappers
# ----------------------------------------------------------------------------------------------------------------
def _open(s, gid, illus=False):
    s.raw('<g data-glyph="%s"%s>' % (gid, ' data-state="illus"' if illus else ""))


def _close(s):
    s.raw("</g>")


def tfill(kind, open_=False):
    if kind == "open":
        return "none"
    a, b = TER[kind]
    return b if open_ else a


# ---- heroes, Monsters, markers ---------------------------------------------------------------------------------
def hero(s, party, x, y, r=4.4):
    """Party A Hero = black disc; Party B Hero = white disc with centre dot."""
    _open(s, "hero-" + party)
    svgkit.token(s, party, x, y, r)
    _close(s)


def monster(s, sz, x, y, open_=False, sc=6.0):
    """Monster Group member: hatched hexagon (Sz S or M); hatched square at footprint scale for Large (2") and Huge (3").
    Returns the half-size of the drawn glyph in pt."""
    if sz in ("M", "S"):
        r = 4.6
        _open(s, "mon", open_)
        if open_:
            s.polygon(hexpts(x, y, r * 1.08), fill="url(#p-mon-l)", stroke=GREY, sw=1.0)
        else:
            svgkit.token(s, "M", x, y, r)
        _close(s)
        return r * 1.1
    half = {"L": 1.0, "H": 1.5}[sz] * sc
    _open(s, "mon-" + sz, open_)
    if open_:
        s.rect(x - half, y - half, 2 * half, 2 * half, fill="url(#p-mon-l)", stroke=GREY, sw=1.4, dash="3 2")
    else:
        s.rect(x - half, y - half, 2 * half, 2 * half, fill=PAT["monster"], stroke=INK, sw=1.4)
    _close(s)
    return half


def marker(s, g, x, y, open_=False, r=5.2):
    """g: obj (diamond with cross), chest (bar rectangle), haz (grey square with !), mk (square with dot)."""
    _open(s, g, open_)
    if g == "chest":
        if open_:
            s.rect(x - r * 0.85, y - r * 0.65, r * 1.7, r * 1.3, fill=WHITE, stroke=GREY, sw=1.0, dash="2.4 1.6")
            s.line(x - r * 0.85, y - r * 0.1, x + r * 0.85, y - r * 0.1, GREY, 0.8)
        else:
            svgkit.token(s, "chest", x, y, r)
    elif g == "obj":
        if open_:
            s.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=WHITE, stroke=GREY, sw=1.1)
            s.line(x - r * 0.5, y, x + r * 0.5, y, GREY, 0.9)
            s.line(x, y - r * 0.5, x, y + r * 0.5, GREY, 0.9)
        else:
            svgkit.token(s, "obj", x, y, r)
    elif g == "haz":
        s.rect(x - r * 0.8, y - r * 0.8, r * 1.6, r * 1.6, fill="#c4c4c4" if not open_ else WHITE,
               stroke=INK if not open_ else GREY, sw=1.0, dash="2.4 1.6" if open_ else None)
        s.text(x, y + 3.4, "!", 9, 700, "middle", INK if not open_ else GREY)
    elif g == "mk":
        s.rect(x - r * 0.75, y - r * 0.75, r * 1.5, r * 1.5, fill=WHITE, stroke=INK if not open_ else GREY, sw=1.5,
               dash="2.4 1.6" if open_ else None)
        s.circle(x, y, 1.3, fill=INK if not open_ else GREY, stroke=None)
    else:
        raise ValueError(g)
    _close(s)


def unresolved(s, x, y, r=5.2):
    """Tag for an element the scenario text does not place: white rounded tag with a bold question mark."""
    _open(s, "unres")
    s.rect(x - r * 1.05, y - r * 0.95, r * 2.1, r * 1.9, fill=WHITE, stroke=INK, sw=1.2, rx=2.6)
    s.text(x, y + 3.5, "?", 9.5, 700, "middle")
    _close(s)


def on_piece(s, kind, x, y, r=5.2):
    """Small square of terrain pattern drawn under an objective marker that is also a terrain piece."""
    terrain_shape(s, kind, "rect", (x - r - 1.6, y - r - 1.6, 2 * r + 3.2, 2 * r + 3.2), sw=1.0)


def step(s, cx, cy, n, r=6.4):
    _open(s, "step")
    svgkit.callout(s, cx, cy, n, r)
    _close(s)


def target_line(s, x1, y1, x2, y2):
    """Sight or targeting line: dashed black line with a dot at each end."""
    _open(s, "los")
    svgkit.arrow(s, x1, y1, x2, y2, "los")
    _close(s)


# ---- terrain ---------------------------------------------------------------------------------------------------
def terrain_shape(s, kind, shape, p, open_=False, sw=0.9, outline=True):
    """shape 'rect' (x, y, w, h), 'circle' (cx, cy, r) or 'poly' [(x, y)...] in pt."""
    gid = TERID[kind]
    fill = tfill(kind, open_)
    stroke = (GREY if open_ else INK) if outline else None
    dash = "3 2" if open_ else None
    _open(s, gid, open_)
    if shape == "rect":
        s.rect(p[0], p[1], p[2], p[3], fill=fill, stroke=stroke, sw=sw, dash=dash)
        if kind == "crumbling":
            x, y, w, h = p
            col = GREY if open_ else INK
            s.polyline([(x + w * 0.1, y + h * 0.3), (x + w * 0.4, y + h * 0.55), (x + w * 0.3, y + h * 0.75),
                        (x + w * 0.9, y + h * 0.9)], col, 0.9)
    elif shape == "circle":
        s.circle(p[0], p[1], p[2], fill=fill, stroke=stroke, sw=sw, dash=dash)
    else:
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, f1(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        s.raw('<polygon points="%s"%s/>' % (" ".join("%s,%s" % (f1(x), f1(y)) for x, y in p), a))
    if kind in OVERLAY:
        ov = OVERLAY[kind][1 if open_ else 0]
        if shape == "rect":
            s.rect(p[0], p[1], p[2], p[3], fill=ov, stroke=None)
        elif shape == "circle":
            s.circle(p[0], p[1], p[2], fill=ov, stroke=None)
        else:
            s.raw('<polygon points="%s" fill="%s"/>' % (" ".join("%s,%s" % (f1(x), f1(y)) for x, y in p), ov))
    _close(s)


def wall_line(s, pts, sw=2.4):
    _open(s, "line-wall")
    s.polyline(pts, INK, sw)
    _close(s)


# ---- zones ----------------------------------------------------------------------------------------------------
def band_sides(rect, n):
    """Board edge(s) a deployment zone is measured from: list of (side, x0, y0, x1, y1) in board inches for the edge
    band of the zone.  Strip zones (at most 8" deep, at least 20" long) are measured from their long edge only."""
    x0, y0, x1, y1 = rect
    out = []
    w, h = x1 - x0, y1 - y0
    strip = min(w, h) <= 8.01 and max(w, h) >= 20
    horiz = w > h
    if x0 <= 0 and not (strip and horiz):
        out.append(("L", x0, y0, x0, y1))
    if x1 >= n and not (strip and horiz):
        out.append(("R", x1, y0, x1, y1))
    if y0 <= 0 and not (strip and not horiz):
        out.append(("T", x0, y0, x1, y0))
    if y1 >= n and not (strip and not horiz):
        out.append(("B", x0, y1, x1, y1))
    return out


def zone(s, x, y, w, h, party, bands, open_=False, bw=3.2, fill=PALE):
    """Deployment zone: pale area with a dashed outline.  `bands` is a list of sides 'L','R','T','B' where the zone
    touches the battlefield edge it is measured from.  Party A: solid black band; Party B: open band;
    both parties: black band with white dashes. `fill` preserves an explicit exclusion overlay in the setup template."""
    _open(s, "zone-" + party, open_)
    s.rect(x, y, w, h, fill=fill, stroke=GREY if open_ else INK, sw=0.9, dash="3.2 2.2")
    for side in bands:
        if side == "L":
            r_ = (x, y, bw, h)
        elif side == "R":
            r_ = (x + w - bw, y, bw, h)
        elif side == "T":
            r_ = (x, y, w, bw)
        else:
            r_ = (x, y + h - bw, w, bw)
        bx_, by_, bw_, bh_ = r_
        if party == "A":
            s.rect(bx_, by_, bw_, bh_, fill=LGREY if open_ else INK, stroke=None)
        elif party == "AB":
            s.rect(bx_, by_, bw_, bh_, fill=LGREY if open_ else INK, stroke=None)
            if bw_ > bh_:
                s.line(bx_, by_ + bh_ / 2, bx_ + bw_, by_ + bh_ / 2, WHITE, 1.0, dash="3 3")
            else:
                s.line(bx_ + bw_ / 2, by_, bx_ + bw_ / 2, by_ + bh_, WHITE, 1.0, dash="3 3")
        else:
            s.rect(bx_, by_, bw_, bh_, fill=WHITE, stroke=GREY if open_ else INK, sw=0.8)
    _close(s)


# ---- lines: dimensions, rings, arrows ----------------------------------------------------------------------------
def dim(s, x1, y1, x2, y2, ticks=3.0, sw=0.8):
    """Dimension line (a stated distance at map scale): line with a short tick at each end."""
    _open(s, "dim")
    s.line(x1, y1, x2, y2, INK, sw)
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    for (px, py) in ((x1, y1), (x2, y2)):
        s.line(px - nx * ticks, py - ny * ticks, px + nx * ticks, py + ny * ticks, INK, sw)
    _close(s)


def dim_offset(s, x1, y1, x2, y2, off, ticks=3.0, sw=0.8):
    """Dimension line drawn `off` pt to the side of the measured points, with thin extension lines back to them."""
    ang = math.atan2(y2 - y1, x2 - x1)
    ox, oy = -math.sin(ang) * off, math.cos(ang) * off
    _open(s, "dim")
    s.line(x1, y1, x1 + ox, y1 + oy, INK, 0.5)
    s.line(x2, y2, x2 + ox, y2 + oy, INK, 0.5)
    _close(s)
    dim(s, x1 + ox, y1 + oy, x2 + ox, y2 + oy, ticks, sw)
    return ox, oy


def pill_label(s, x, y, text, size=9, weight=600, anchor="middle"):
    """Label of a dimension or range: haloed text, baseline at y.  Ranges (6–8") are also registered as 'range'."""
    rng = bool(re.search(r"\d[–-]\d", text))
    if rng:
        _open(s, "range")
    s.htext(x, y, text, size, weight, anchor)
    if rng:
        _close(s)


def dim_labeled(s, x1, y1, x2, y2, label, ticks=2.8, off=None, size=9, weight=700):
    """Dimension line with its label centred on the line (off=None) or beside it at the signed offset `off` (pt)."""
    dim(s, x1, y1, x2, y2, ticks)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if off is None:
        pill_label(s, mx, my + 3.2, label, size, weight)
    else:
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = -math.sin(ang), math.cos(ang)
        pill_label(s, mx + nx * off, my + ny * off + 3.2, label, size, weight)


def ring(s, cx, cy, r, clip=None, dash="3 2.5"):
    """Ring: dashed black circle = within the stated distance of its centre."""
    _open(s, "ring")
    if clip:
        s.raw('<g clip-path="url(#%s)">' % clip)
    s.circle(cx, cy, r, fill="none", stroke=INK, sw=0.9, dash=dash)
    if clip:
        s.raw("</g>")
    _close(s)


def ring_path(s, d, clip=None, dash="3 2.5"):
    _open(s, "ring")
    if clip:
        s.raw('<g clip-path="url(#%s)">' % clip)
    s.path(d, fill="none", stroke=INK, sw=0.9, dash=dash)
    if clip:
        s.raw("</g>")
    _close(s)


def leader(s, x1, y1, x2, y2):
    """Thin grey leader line from a label to the symbol it names."""
    _open(s, "leader")
    s.line(x1, y1, x2, y2, "#555", 0.6)
    _close(s)


def edge_arrow(s, x1, y1, x2, y2, mode, open_=False):
    """Entry (arrive) or exit arrow across a battlefield edge; grey dashed when the point on the edge is open."""
    _open(s, "arr-" + mode, open_)
    if open_:
        ang = math.atan2(y2 - y1, x2 - x1)
        s.line(x1, y1, x2 - math.cos(ang) * 7, y2 - math.sin(ang) * 7, GREY, 1.4, dash="3 2")
        s.polygon([(x2, y2), (x2 - math.cos(ang) * 7 - math.sin(ang) * 3.4, y2 - math.sin(ang) * 7 + math.cos(ang) * 3.4),
                   (x2 - math.cos(ang) * 7 + math.sin(ang) * 3.4, y2 - math.sin(ang) * 7 - math.cos(ang) * 3.4)], GREY)
    else:
        svgkit.arrow(s, x1, y1, x2, y2, "move", sw=1.8)
    _close(s)


def compass(s, ax, y0=10.2):
    """North arrow, right edge at ax, baseline of the N at y0."""
    _open(s, "compass")
    s.polygon([(ax, y0 - 7.2), (ax - 3.2, y0 - 0.7), (ax + 3.2, y0 - 0.7)], INK)
    s.text(ax - 6, y0, "N", 9, 700, "end")
    _close(s)


def scale_bar(s, x0, y, sc, inches=6, label=None):
    """Scale bar of `inches` at sc pt per inch with a half-way tick; returns the x after its label."""
    _open(s, "scale")
    L = inches * sc
    s.line(x0, y - 3, x0 + L, y - 3, INK, 1.4)
    s.line(x0, y - 6, x0, y, INK, 1.0)
    s.line(x0 + L, y - 6, x0 + L, y, INK, 1.0)
    s.line(x0 + L / 2, y - 5, x0 + L / 2, y - 1, INK, 0.8)
    lab = label if label is not None else '%d" scale' % inches
    s.text(x0 + L + 4, y, lab, 9, 400)
    _close(s)
    return x0 + L + 4 + tw(lab, 9, 400)


# ----------------------------------------------------------------------------------------------------------------
# the registry and the key swatches (30 pt wide, centred on y)
# ----------------------------------------------------------------------------------------------------------------
SWW = 30


def _sw_zone(s, x, y, party):
    zone(s, x, y - 7, 30, 14, party, ["L"])
    if party == "AB":
        hero(s, "A", x + 12, y, 3.9)
        hero(s, "B", x + 23, y, 3.9)
    else:
        hero(s, party, x + 18, y, 4.4)


def _sw_terrain(kind, open_=False):
    def f(s, x, y):
        terrain_shape(s, kind, "rect", (x + 2, y - 6, 26, 12), open_)
    return f


def _sw_ruler(s, x, y):
    dim(s, x + 2, y, x + 28, y, 3.0)


def _sw_ring(s, x, y):
    ring(s, x + 15, y, 6.5)
    s.circle(x + 15, y, 1.6, fill=INK, stroke=None)


def _sw_range(s, x, y):
    pill_label(s, x + 15, y + 3.4, '6–8"')


def _sw_arrow(out):
    def f(s, x, y):
        s.line(x + 2, y + 7, x + 28, y + 7, INK, 1.3)
        if out:
            edge_arrow(s, x + 15, y - 6, x + 15, y + 6, "exit")
        else:
            edge_arrow(s, x + 15, y + 6, x + 15, y - 6, "arrive")
    return f


def _sw_scale(s, x, y):
    L = 26
    s.line(x + 2, y + 1, x + 2 + L, y + 1, INK, 1.4)
    s.line(x + 2, y - 3, x + 2, y + 4, INK, 1.0)
    s.line(x + 2 + L, y - 3, x + 2 + L, y + 4, INK, 1.0)
    s.line(x + 2 + L / 2, y - 1, x + 2 + L / 2, y + 3, INK, 0.8)


def _sw_compass(s, x, y):
    s.polygon([(x + 17, y - 7), (x + 13.8, y), (x + 20.2, y)], INK)
    s.text(x + 10, y + 3.4, "N", 9, 700, "end")


def _sw_los(s, x, y):
    target_line(s, x + 2, y, x + 28, y)


def _sw_excl(s, x, y):
    s.rect(x + 2, y - 6, 26, 12, fill=PAT["aoe"], stroke=INK, sw=0.8)


def _sw_ledge(crumbling):
    def f(s, x, y):
        terrain_shape(s, "crumbling" if crumbling else "ledge", "rect", (x + 5, y - 6, 20, 12), False, 1.3)
    return f


def _sw_wall(s, x, y):
    wall_line(s, [(x + 2, y), (x + 28, y)])


# id -> (group, key label, short label for compact strips, swatch drawer)
REG = {}
ORDER = []


def _reg(gid, group, label, short, sw):
    REG[gid] = dict(group=group, label=label, short=short, sw=sw)
    ORDER.append(gid)


_reg("hero-A", "Parties and zones", "Party A Hero (black disc)", "Party A Hero", lambda s, x, y: hero(s, "A", x + 15, y, 5.0))
_reg("hero-B", "Parties and zones", "Party B Hero (disc, centre dot)", "Party B Hero", lambda s, x, y: hero(s, "B", x + 15, y, 5.0))
_reg("zone-A", "Parties and zones", "Party A zone: solid edge band", "Party A zone", lambda s, x, y: _sw_zone(s, x, y, "A"))
_reg("zone-B", "Parties and zones", "Party B zone: open edge band", "Party B zone", lambda s, x, y: _sw_zone(s, x, y, "B"))
_reg("zone-AB", "Parties and zones", "Zone both parties use", "Zone both use", lambda s, x, y: _sw_zone(s, x, y, "AB"))
_reg("compass", "Parties and zones", "North arrow (top of the map)", "North", _sw_compass)
_reg("scale", "Parties and zones", "Scale bar (map is to scale)", "Scale bar", _sw_scale)
_reg("obj", "Markers and Monsters", "Objective or carried objective", "Objective", lambda s, x, y: marker(s, "obj", x + 15, y))
_reg("chest", "Markers and Monsters", "Treasure Chest", "Treasure Chest", lambda s, x, y: marker(s, "chest", x + 15, y))
_reg("haz", "Markers and Monsters", "Hazard marker", "Hazard marker", lambda s, x, y: marker(s, "haz", x + 15, y))
_reg("mk", "Markers and Monsters", "Other marker or token", "Marker", lambda s, x, y: marker(s, "mk", x + 15, y))
_reg("mon", "Markers and Monsters", "Monster Group (G1 Group 1, R Resting, A Awake)", "Monster", lambda s, x, y: monster(s, "M", x + 15, y))
_reg("mon-L", "Markers and Monsters", "Large Monster, 2\"×2\"", "Large Monster 2\"×2\"", lambda s, x, y: monster(s, "L", x + 15, y))
_reg("mon-H", "Markers and Monsters", "Huge Monster, 3\"×3\"", "Huge Monster 3\"×3\"", lambda s, x, y: monster(s, "H", x + 15, y))
_reg("step", "Markers and Monsters", "Numbered step", "Numbered step", lambda s, x, y: step(s, x + 15, y, "1", 6.2))
_reg("ter-blocking", "Terrain", "Blocking", "Blocking", _sw_terrain("blocking"))
_reg("ter-impassable", "Terrain", "Impassable", "Impassable", _sw_terrain("impassable"))
_reg("ter-cover", "Terrain", "Cover", "Cover", _sw_terrain("cover"))
_reg("ter-difficult", "Terrain", "Difficult", "Difficult", _sw_terrain("difficult"))
_reg("ter-water", "Terrain", "Shallow or Deep Water", "Water", _sw_terrain("water"))
_reg("ter-slippery", "Terrain", "Slippery", "Slippery", _sw_terrain("slippery"))
_reg("ter-obstacle", "Terrain", "Impassable or Blocking per piece (2.9.1)", "Piece type per 2.9.1", _sw_terrain("obstacle"))
_reg("ter-coverdiff", "Terrain", "Cover and Difficult", "Cover and Difficult", _sw_terrain("coverdiff"))
_reg("ter-hazard", "Terrain", "Hazard area", "Hazard area", _sw_terrain("hazard"))
_reg("ter-shade", "Terrain", "Deep Shadow or Darkness", "Deep Shadow", _sw_terrain("shade"))
_reg("ter-chasm", "Terrain", "Chasm (not walkable)", "Chasm", _sw_terrain("chasm"))
_reg("line-wall", "Terrain", "Blocking wall (line)", "Blocking wall", _sw_wall)
_reg("ter-open", "Terrain", "Open feature: room, clearing, path", "Open feature", _sw_terrain("open"))
_reg("ledge", "Terrain", "Ledge over a Chasm", "Ledge", _sw_ledge(False))
_reg("ledge-crumbling", "Terrain", "Crumbling Ledge", "Crumbling Ledge", _sw_ledge(True))
_reg("dim", "Distances, edges, status", "Stated distance; 'min' = at least", "Stated distance", _sw_ruler)
_reg("ring", "Distances, edges, status", "Ring: within the distance", "Within the distance", _sw_ring)
_reg("range", "Distances, edges, status", "A range: any value in it is legal", "Range", _sw_range)
_reg("arr-exit", "Distances, edges, status", "Exit or extraction edge", "Exit edge", _sw_arrow(True))
_reg("arr-arrive", "Distances, edges, status", "Arrival edge (R3 = Round 3)", "Arrival edge", _sw_arrow(False))
_reg("los", "Distances, edges, status", "Sight or targeting line", "Targeting line", _sw_los)
_reg("leader", "Distances, edges, status", "Label leader line", "Leader line", lambda s, x, y: leader(s, x + 2, y + 3, x + 28, y - 3))
_reg("illus", "Distances, edges, status", "Grey dashed: one legal arrangement", "Grey dashed: one legal arrangement", _sw_terrain("cover", True))
_reg("ter-excl", "Distances, edges, status", "Step 7 exclusion (10.1 template)", "Step 7 exclusion", _sw_excl)


def swatch(s, gid, x, y, attr="data-key"):
    """Draw the key swatch of registry entry gid inside <g data-key=gid> (or data-strip) so that the extractor can tell
    key and strip glyphs from glyphs used on the diagram itself."""
    s.raw('<g %s="%s">' % (attr, gid))
    REG[gid]["sw"](s, x, y)
    s.raw("</g>")


def key_strip(s, items, x, y, width, row_h=15.5, title="Key"):
    """Compact key strip: only the glyphs the figure uses.  items: list of gid or (gid, label).  Returns y below."""
    cx = x
    rowy = y + 8
    if title:
        s.text(x, y + 8, title, 9, 700)
        cx = x + tw(title, 9, 700) + 8
    for it in items:
        gid, lab = (it, REG[it]["short"]) if isinstance(it, str) else it
        w = SWW + 4 + tw(lab, 9, 400) + 9
        if cx + w - 9 > x + width and cx > x + 0.1:
            cx = x
            rowy += row_h
        swatch(s, gid, cx, rowy - 2.5, "data-strip")
        s.text(cx + SWW + 4, rowy + 0.5, lab, 9, 400)
        cx += w
    return rowy + row_h - 4


def step_list(s, x, y, steps, width, size=9, lead=10.5, gap=4, num_r=6.6):
    """Numbered steps with the shared `step` glyph.  steps: list of strings.  Returns y after."""
    for i, st in enumerate(steps, 1):
        lines = wrap(st, width - 2 * num_r - 6, size)
        step(s, x + num_r, y + num_r - 1.6, i, num_r)
        for k, ln in enumerate(lines):
            s.text(x + 2 * num_r + 6, y + 6 + k * lead, ln, size)
        y += max(2 * num_r, len(lines) * lead) + gap
    return y


def strip_for(s, x, y, width, labels=None, extra=(), title="Key"):
    """Compact key strip with exactly the glyph ids already drawn on `s` (plus `extra`), in registry order."""
    ids = ids_in_svg(s.render(10))
    used = ids["used"] | ids["patterns"] | set(extra)
    labels = labels or {}
    items = [(g, labels.get(g, REG[g]["short"])) for g in ORDER if g in used]
    return key_strip(s, items, x, y, width, title=title)


# ----------------------------------------------------------------------------------------------------------------
# extraction (selfcheck)
# ----------------------------------------------------------------------------------------------------------------
def ids_in_svg(text):
    """Returns dict(used=ids emitted by the diagram, key=ids drawn as key swatches, strip=ids drawn in a compact strip,
    patterns=pattern-derived ids used by the diagram, unknown=pattern ids that are not in PATMAP)."""
    root = ET.fromstring(text)
    used, key, strip, pats, unknown = set(), set(), set(), set(), set()

    def walk(el, mode):
        a = el.attrib
        if "data-key" in a:
            key.add(a["data-key"])
            mode = "key"
        elif "data-strip" in a:
            strip.add(a["data-strip"])
            mode = "strip"
        if "data-glyph" in a and mode is None:
            used.add(a["data-glyph"])
        if "data-state" in a and mode is None:
            used.add(a["data-state"])
        for k in ("fill", "stroke"):
            m = re.match(r"url\(#(p-[a-z-]+)\)", a.get(k, ""))
            if m:
                pid = m.group(1)
                if pid in PATMAP:
                    if mode is None:
                        pats.add(PATMAP[pid])
                else:
                    unknown.add(pid)
        for ch in el:
            walk(ch, mode)
    walk(root, None)
    return dict(used=used, key=key, strip=strip, patterns=pats, unknown=unknown)
