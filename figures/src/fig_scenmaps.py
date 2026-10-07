"""Scenario deployment maps (FIG-20 onward): one compact column-width top-down map per Core Scenario.

Data-driven: every map is drawn from one entry of figures/src/scenario_specs.json.
Board coordinates are inches, origin at the top-left corner, x to the right, y downward; North is drawn at the
top (the Setup Roll-off winner designates North in play, 10.1).  Short edges = North/South (top/bottom),
long edges = East/West (left/right), even on a square battlefield (10.1).

Statuses recorded per spec element:
  MANDATORY_POSITION  the source fixes the location (drawn solid)
  CONSTRAINED         the source gives a range or relation (drawn solid with its dimension/ring)
  ILLUSTRATIVE        the source leaves the location open; one legal arrangement is drawn in light grey dashes
Elements may carry "draw": "open" to force the light dashed style where only the extent is fixed.

Scale: the board, zones and every stated distance are drawn at SC pt per inch; markers are enlarged
(Large and Huge Monsters are drawn at their 2"x2" and 3"x3" footprints).  A 6" scale bar is included.
"""
import json
import math
import os
import re

from svgkit import (Svg, COL_W, FULL_W, INK, DARK, MID, LIGHT, PALE, WHITE, PAT, tw, wrap, hexpts, token,
                    arrow, DEFS, f1, callout, box, pill)  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SPEC_PATH = os.path.join(HERE, "scenario_specs.json")

SC = 5.2                 # pt per inch
BX = (COL_W - 36 * SC) / 2.0
BY = 14.0
GREY = "#777"            # ILLUSTRATIVE outline
LGREY = "#aaa"
INFO = "grey dashed = one legal arrangement; position not fixed by the rules"
NOTE_STD = "Grey dashed = one legal arrangement; position not fixed by the rules"

EXTRA_DEFS = """<defs>
<pattern id="p-cover-l" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#fff"/><path d="M0 0.5H5M0.5 0V5" stroke="#aaa" stroke-width="0.6" fill="none"/></pattern>
<pattern id="p-diff-l" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#fff"/><circle cx="1" cy="1" r="0.7" fill="#999"/><circle cx="3" cy="3" r="0.7" fill="#999"/></pattern>
<pattern id="p-imp-l" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.6" height="2.6" fill="#fff"/><path d="M0.4 0V2.6" stroke="#aaa" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-mon-l" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="3.2" height="3.2" fill="#fff"/><path d="M0.5 0V3.2" stroke="#999" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-water" width="6" height="4" patternUnits="userSpaceOnUse"><rect width="6" height="4" fill="#fff"/><path d="M0 2.2Q1.5 0.4 3 2.2T6 2.2" stroke="#333" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-water-l" width="6" height="4" patternUnits="userSpaceOnUse"><rect width="6" height="4" fill="#fff"/><path d="M0 2.2Q1.5 0.4 3 2.2T6 2.2" stroke="#aaa" stroke-width="0.8" fill="none"/></pattern>
<pattern id="p-slip" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><rect width="6" height="6" fill="#fff"/><path d="M0.5 1.5H3.5M3.5 4.5H5.5" stroke="#333" stroke-width="0.9" fill="none"/></pattern>
<pattern id="p-slip-l" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><rect width="6" height="6" fill="#fff"/><path d="M0.5 1.5H3.5M3.5 4.5H5.5" stroke="#aaa" stroke-width="0.9" fill="none"/></pattern>
<clipPath id="bclip"><rect x="22.5" y="14" width="198" height="198"/></clipPath>
<pattern id="p-dark" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#d9d9d9"/><path d="M0 4L4 0" stroke="#fff" stroke-width="0.9" fill="none"/></pattern>
</defs>"""

# terrain kind -> (solid fill, light fill)
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
}


class MapSvg(Svg):
    def render(self, height, title=None, desc=None):
        t = Svg.render(self, height, title=title, desc=desc)
        return t.replace("</defs>", "</defs>\n" + EXTRA_DEFS, 1)

    def vtext(self, x, y, s, size=9, weight=600, anchor="middle", fill=INK):
        """Text rotated -90 deg about (x, y)."""
        self.raw('<g transform="rotate(-90 %s %s)">' % (f1(x), f1(y)))
        self.text(x, y, s, size, weight, anchor, fill)
        self.raw("</g>")


# ---------------------------------------------------------------------------------------------
# spec loading and source helpers
# ---------------------------------------------------------------------------------------------
_SPEC = None
_SRC = None


def spec():
    global _SPEC
    if _SPEC is None:
        with open(SPEC_PATH, encoding="utf-8") as f:
            _SPEC = json.load(f)
    return _SPEC


def source_lines():
    global _SRC
    if _SRC is None:
        ver = json.load(open(os.path.join(ROOT, "source", "versions.json")))
        cur = [r for r in ver["revisions"] if r["number"] == ver["current"]][0]
        with open(os.path.join(ROOT, cur["path"]), encoding="utf-8") as f:
            _SRC = f.read().split("\n")
    return _SRC


def scenario_spans():
    """{key: (heading_line, last_line, climate_no, scenario_no, title)} computed from the manuscript."""
    L = source_lines()
    out = {}
    climates = []
    cur_climate = None
    start = None
    keys = []
    for i, t in enumerate(L, 1):
        m = re.match(r"^#### Climate (\d+): (.+?) Scenarios\s*$", t)
        if m:
            cur_climate = (int(m.group(1)), m.group(2))
        m = re.match(r"^##### Scenario (\d+): (.+?)(?: \[Intro\])?\s*$", t)
        if m and cur_climate:
            keys.append((i, "%s %s" % (cur_climate[1], m.group(1)), cur_climate, int(m.group(1)), m.group(2)))
    # end of each span: next heading of level <= 5 after the start
    for k, (i, key, cl, n, title) in enumerate(keys):
        end = len(L)
        for j in range(i, len(L)):
            if re.match(r"^#{1,5} ", L[j]):
                end = j          # 0-based index j == line j+1; last line of span is j
                break
        out[key] = (i, end, cl[0], n, title, cl[1])
    return out


def norm(s):
    return s.replace("*", "").replace("”", '"').replace("“", '"')


def cited_text(lines):
    L = source_lines()
    return norm(" ".join(L[n - 1] for n in lines))


def inch_tokens(text):
    """Inch values printed in a label: ['6–8"', '36"', ...] (number or range followed by a double quote)."""
    return re.findall(r'(\d+(?:\.\d+)?(?:[–-]\d+(?:\.\d+)?)?)"', text)


# ---------------------------------------------------------------------------------------------
# geometry (inches) for legality assertions
# ---------------------------------------------------------------------------------------------
def footprint(e):
    k = e["kind"]
    if k == "zone":
        return ("r",) + tuple(e["rect"])
    if k == "feature":
        g = e["g"]
        if e["shape"] == "rect":
            return ("r",) + tuple(g)
        if e["shape"] == "circle":
            return ("c", g[0], g[1], g[2])
        xs = [p[0] for p in g]
        ys = [p[1] for p in g]
        return ("r", min(xs), min(ys), max(xs), max(ys))
    if k == "marker":
        return ("c", e["at"][0], e["at"][1], 0.5)
    if k == "monster":
        x, y = e["at"]
        h = {"S": 0.5, "M": 0.5, "L": 1.0, "H": 1.5}[e.get("sz", "M")]
        return ("r", x - h, y - h, x + h, y + h) if e.get("sz", "M") in ("L", "H") else ("c", x, y, 0.5)
    return None


def _pt_rect(px_, py_, r):
    dx = max(r[1] - px_, 0, px_ - r[3])
    dy = max(r[2] - py_, 0, py_ - r[4])
    return math.hypot(dx, dy)


def shape_dist(a, b):
    if a[0] == "c" and b[0] == "c":
        return max(0.0, math.hypot(a[1] - b[1], a[2] - b[2]) - a[3] - b[3])
    if a[0] == "r" and b[0] == "c":
        a, b = b, a
    if a[0] == "c" and b[0] == "r":
        return max(0.0, _pt_rect(a[1], a[2], b) - a[3])
    dx = max(a[1] - b[3], b[1] - a[3], 0)
    dy = max(a[2] - b[4], b[2] - a[4], 0)
    return math.hypot(dx, dy)


def centre(e):
    s = footprint(e)
    if s[0] == "c":
        return (s[1], s[2])
    return ((s[1] + s[3]) / 2.0, (s[2] + s[4]) / 2.0)


def inside(inner, outer):
    c = centre(inner)
    s = footprint(outer)
    if s[0] == "c":
        return math.hypot(c[0] - s[1], c[1] - s[2]) <= s[3] + 1e-9
    return s[1] - 1e-9 <= c[0] <= s[3] + 1e-9 and s[2] - 1e-9 <= c[1] <= s[4] + 1e-9


def closest_points(a, b):
    """Closest points between two footprints (inches), used to draw dimension lines."""
    ca, cb = centre_shape(a), centre_shape(b)

    def toward(s, p):
        if s[0] == "c":
            d = math.hypot(p[0] - s[1], p[1] - s[2]) or 1e-9
            return (s[1] + (p[0] - s[1]) / d * s[3], s[2] + (p[1] - s[2]) / d * s[3])
        return (min(max(p[0], s[1]), s[3]), min(max(p[1], s[2]), s[4]))
    # iterate twice: point on a nearest to b, then point on b nearest to that
    pa = toward(a, cb)
    pb = toward(b, pa)
    pa = toward(a, pb)
    return pa, pb


def centre_shape(s):
    if s[0] == "c":
        return (s[1], s[2])
    return ((s[1] + s[3]) / 2.0, (s[2] + s[4]) / 2.0)


# ---------------------------------------------------------------------------------------------
# drawing
# ---------------------------------------------------------------------------------------------
def X(x):
    return BX + x * SC


def Y(y):
    return BY + y * SC


class Ctx:
    def __init__(self, sp):
        self.sp = sp
        self.s = MapSvg(COL_W)
        self.occ = []          # occupied rects (x0, y0, x1, y1) in pt
        self.labels = []       # deferred labels
        self.inches = []       # (printed text, element id) for audit
        self.warn = []
        self.els = {e["id"]: e for e in sp["elements"]}
        self.illus = False
        self.tokens = []
        self.bs = 36 * SC

    # ---- occupancy ----
    def occupy(self, x0, y0, x1, y1):
        self.occ.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)))

    def free(self, r, ignore=0):
        for o in self.occ:
            if r[0] < o[2] and r[2] > o[0] and r[1] < o[3] and r[3] > o[1]:
                return False
        return True

    def overlap_area(self, r):
        a = 0.0
        for o in self.occ:
            w = min(r[2], o[2]) - max(r[0], o[0])
            h = min(r[3], o[3]) - max(r[1], o[1])
            if w > 0 and h > 0:
                a += w * h
        return a

    # ---- labels ----
    def add_label(self, eid, text, ax, ay, cr, pref="rltb", fixed=None, weight=600, leader=True):
        self.labels.append(dict(eid=eid, text=text, ax=ax, ay=ay, cr=cr, pref=pref, fixed=fixed, weight=weight,
                                leader=leader))
        for v in inch_tokens(text):
            self.inches.append((v + '"', eid))

    def place_labels(self):
        s = self.s
        bx0, by0, bx1, by1 = BX + 1, BY + 1, BX + self.bs - 1, BY + self.bs - 1
        # fixed-position labels first, then others in order
        order = sorted(self.labels, key=lambda l: 0 if l["fixed"] else 1)
        for lb in order:
            lines = lb["text"].split("\n")
            w = max(tw(t, 9, lb["weight"]) for t in lines) + 3.2
            h = len(lines) * 10 + 1.2
            cands = []
            ax, ay, cr = lb["ax"], lb["ay"], lb["cr"]
            for ring in (2.0, 11.0, 20.0):
                d = cr + ring
                pos = {
                    "r": (ax + d, ay - h / 2), "l": (ax - d - w, ay - h / 2),
                    "t": (ax - w / 2, ay - d - h), "b": (ax - w / 2, ay + d),
                    "R": (ax + d, ay - h - 1), "L": (ax - d - w, ay - h - 1),
                    "u": (ax + d * 0.7, ay - d * 0.7 - h), "v": (ax - d * 0.7 - w, ay - d * 0.7 - h),
                    "d": (ax + d * 0.7, ay + d * 0.7), "e": (ax - d * 0.7 - w, ay + d * 0.7),
                }
                prefs = lb["pref"] + "".join(c for c in "rltbuvde" if c not in lb["pref"])
                for c in prefs:
                    if c in pos:
                        cands.append(pos[c])
            if lb["fixed"] is not None:
                cands = [(lb["ax"] - w / 2, lb["ay"] - h / 2)] + cands if lb["fixed"] == "c" else [lb["fixed"]] + cands
            best = None
            for (x0, y0) in cands:
                r = (x0, y0, x0 + w, y0 + h)
                if r[0] < bx0 or r[2] > bx1 or r[1] < by0 or r[3] > by1:
                    continue
                a = self.overlap_area(r)
                if a == 0:
                    best = (x0, y0, 0)
                    break
                if best is None or a < best[2]:
                    best = (x0, y0, a)
            if best is None:
                x0, y0 = ax - w / 2, ay - h / 2
                x0 = min(max(x0, bx0), bx1 - w)
                y0 = min(max(y0, by0), by1 - h)
                best = (x0, y0, 9e9)
            if best[2] > 0:
                self.warn.append("label overlap %s %r (%.0f pt2)" % (lb["eid"], lb["text"], best[2]))
            x0, y0 = best[0], best[1]
            if cr > 0 and lb.get("leader", True):
                # nearest point of the label box to the anchor; draw a leader when the label sits away from its glyph
                nx_ = min(max(ax, x0), x0 + w)
                ny_ = min(max(ay, y0), y0 + h)
                dd = math.hypot(nx_ - ax, ny_ - ay)
                if dd > cr + 5:
                    ang_ = math.atan2(ny_ - ay, nx_ - ax)
                    s.line(ax + math.cos(ang_) * (cr + 0.5), ay + math.sin(ang_) * (cr + 0.5), nx_, ny_, "#555", 0.6)
            s.rect(x0, y0, w, h, fill=WHITE, stroke=None)
            for i, t in enumerate(lines):
                s.text(x0 + 1.6, y0 + 8.4 + i * 10, t, 9, lb["weight"])
            self.occupy(x0, y0, x0 + w, y0 + h)


def _tfill(terrain, open_):
    if terrain == "open":
        return "none"
    if terrain == "gap":
        return WHITE
    a, b = TER[terrain]
    return b if open_ else a


def draw_board(c):
    s = c.s
    s.rect(BX, BY, c.bs, c.bs, fill=WHITE, stroke=INK, sw=1.3)


def is_open(e):
    return e.get("draw") == "open" or (e["status"] == "ILLUSTRATIVE" and e.get("draw") != "fixed")


def draw_zone(c, e):
    s = c.s
    x0, y0, x1, y1 = e["rect"]
    s.rect(X(x0), Y(y0), (x1 - x0) * SC, (y1 - y0) * SC, fill=PALE, stroke=INK, sw=0.9, dash="3.2 2.2")
    party = e["party"]
    # edge band along the board edge(s) the zone is measured from (strip zones: the long edge only)
    bw = 3.2
    bands = []
    strip = min(x1 - x0, y1 - y0) <= 8.01 and max(x1 - x0, y1 - y0) >= 20
    horiz = (x1 - x0) > (y1 - y0)
    if x0 <= 0 and not (strip and horiz):
        bands.append((X(x0), Y(y0), bw, (y1 - y0) * SC))
    if x1 >= 36 and not (strip and horiz):
        bands.append((X(x1) - bw, Y(y0), bw, (y1 - y0) * SC))
    if y0 <= 0 and not (strip and not horiz):
        bands.append((X(x0), Y(y0), (x1 - x0) * SC, bw))
    if y1 >= 36 and not (strip and not horiz):
        bands.append((X(x0), Y(y1) - bw, (x1 - x0) * SC, bw))
    for (bx_, by_, bw_, bh_) in bands:
        if party == "A":
            s.rect(bx_, by_, bw_, bh_, fill=INK, stroke=None)
        elif party == "AB":
            s.rect(bx_, by_, bw_, bh_, fill=INK, stroke=None)
            if bw_ > bh_:
                s.line(bx_, by_ + bh_ / 2, bx_ + bw_, by_ + bh_ / 2, WHITE, 1.0, dash="3 3")
            else:
                s.line(bx_ + bw_ / 2, by_, bx_ + bw_ / 2, by_ + bh_, WHITE, 1.0, dash="3 3")
        else:
            s.rect(bx_, by_, bw_, bh_, fill=WHITE, stroke=INK, sw=0.8)
    c.occupy(X(x0), Y(y0), X(x1), Y(y1)) if False else None
    # hero tokens
    w, h = x1 - x0, y1 - y0
    toks = e.get("tokens")
    if toks is None and party == "AB":
        toks = []
    if toks is None:
        if min(w, h) <= 8.01 and max(w, h) >= 20:      # strip zone
            if w < h:
                toks = [[x0 + w / 2, y0 + h * f] for f in (0.1, 0.72, 0.9)]
            else:
                toks = [[x0 + w * f, y0 + h / 2] for f in (0.1, 0.72, 0.9)]
        else:
            toks = [[x0 + w * 0.28, y0 + h * 0.25], [x0 + w * 0.72, y0 + h * 0.25]]
    for tk in toks:
        tx, ty = tk[0], tk[1]
        tp = tk[2] if len(tk) > 2 else party
        c.tokens.append((tp, X(tx), Y(ty)))
        c.occupy(X(tx) - 5, Y(ty) - 5, X(tx) + 5, Y(ty) + 5)
    # depth dimension
    if e.get("depth"):
        at = e.get("dim_at")
        if abs(w - h) < 0.01:     # corner zone: horizontal dimension, label gives both sides
            yy = at if at is not None else y0 + h * 0.72
            dim_line(c, e["id"], X(x0), Y(yy), X(x1), Y(yy), e["depth"], vertical=False)
        elif w < h:       # vertical strip: depth is horizontal
            yy = at if at is not None else y0 + h * 0.3
            xa, xb = x0, x1
            dim_line(c, e["id"], X(xa), Y(yy), X(xb), Y(yy), e["depth"], vertical=False)
        else:
            xx = at if at is not None else x0 + w * 0.3
            dim_line(c, e["id"], X(xx), Y(y0), X(xx), Y(y1), e["depth"], vertical=True)


def dim_line(c, eid, x1, y1, x2, y2, label, vertical=None, ticks=3.0, sw=0.8, lp="c"):
    s = c.s
    s.line(x1, y1, x2, y2, INK, sw)
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    for (px_, py_) in ((x1, y1), (x2, y2)):
        s.line(px_ - nx * ticks, py_ - ny * ticks, px_ + nx * ticks, py_ + ny * ticks, INK, sw)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    length = math.hypot(x2 - x1, y2 - y1)
    lines = label.split("\n")
    wlab = max(tw(t, 9, 600) for t in lines)
    if lp == "c" and length >= wlab + 8 and abs(math.sin(ang)) < 0.3:
        c.add_label(eid, label, mx, my, 0, fixed="c")
    else:
        # place beside the line
        c.add_label(eid, label, mx, my, 2.5 + (0 if abs(math.sin(ang)) > 0.7 else 0), pref="tbrl" if abs(math.sin(ang)) < 0.5 else "rlbt")
    # reserve small boxes along the line so other labels avoid sitting on the dimension
    n = max(1, int(length // 5))
    for i in range(n + 1):
        qx, qy = x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n
        c.occupy(qx - 1.6, qy - 1.6, qx + 1.6, qy + 1.6)


def feat_path(e):
    """SVG geometry helper: returns (kind, params) in pt."""
    g = e["g"]
    if e["shape"] == "rect":
        return "rect", (X(g[0]), Y(g[1]), (g[2] - g[0]) * SC, (g[3] - g[1]) * SC)
    if e["shape"] == "circle":
        return "circle", (X(g[0]), Y(g[1]), g[2] * SC)
    if e["shape"] == "line":
        return "line", [(X(p[0]), Y(p[1])) for p in g]
    return "poly", [(X(p[0]), Y(p[1])) for p in g]


def draw_feature(c, e):
    s = c.s
    open_ = is_open(e)
    t = e.get("terrain", "open")
    fill = _tfill(t, open_)
    stroke = GREY if open_ else INK
    dash = "3 2" if open_ else None
    sw = e.get("sw", 0.9)
    if e.get("outline") == "none":
        stroke = None
    kind, p = feat_path(e)
    if kind == "rect":
        s.rect(p[0], p[1], p[2], p[3], fill=fill, stroke=stroke, sw=sw, dash=dash)
        bb = (p[0], p[1], p[0] + p[2], p[1] + p[3])
    elif kind == "circle":
        s.circle(p[0], p[1], p[2], fill=fill, stroke=stroke, sw=sw, dash=dash)
        bb = (p[0] - p[2], p[1] - p[2], p[0] + p[2], p[1] + p[2])
    elif kind == "line":
        s.polyline(p, INK, e.get("sw", 2.4))
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        bb = (min(xs), min(ys), max(xs), max(ys))
    else:
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, f1(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        s.raw('<polygon points="%s"%s/>' % (" ".join("%s,%s" % (f1(x), f1(y)) for x, y in p), a))
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        bb = (min(xs), min(ys), max(xs), max(ys))
    e["_bb"] = bb
    if e.get("label"):
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        lp = e.get("lp", "c")
        if lp == "i":
            lines_ = e["label"].split("\n")
            c.add_label(e["id"], e["label"], cx, cy, 0, pref="t", fixed=(bb[0] + 1.5, bb[1] + 1.5), weight=600,
                        leader=False)
            return_ = True
        elif e.get("lat"):
            cx, cy = X(e["lat"][0]), Y(e["lat"][1])
        elif lp not in ("c",) and (bb[2] - bb[0]) < 40 and (bb[3] - bb[1]) < 40:
            half = max(bb[2] - bb[0], bb[3] - bb[1]) / 2.0
            c.add_label(e["id"], e["label"], cx, cy, half, pref=lp + "rltb", weight=600, leader=True)
            lp = "done"
        elif lp == "t":
            cy = bb[1]
        elif lp == "b":
            cy = bb[3]
        elif lp == "l":
            cx = bb[0]
        elif lp == "r":
            cx = bb[2]
        if lp not in ("i", "done"):
            c.add_label(e["id"], e["label"], cx, cy, 0, pref=lp, fixed="c" if lp == "c" else None, weight=600,
                        leader=False)


def glyph_marker(s, g, x, y, open_=False, r=5.2):
    if g == "chest":
        if open_:
            s.rect(x - r * 0.85, y - r * 0.65, r * 1.7, r * 1.3, fill=WHITE, stroke=GREY, sw=1.0, dash="2.4 1.6")
            s.line(x - r * 0.85, y - r * 0.1, x + r * 0.85, y - r * 0.1, GREY, 0.8)
        else:
            token(s, "chest", x, y, r)
    elif g == "obj":
        if open_:
            s.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=WHITE, stroke=GREY, sw=1.1)
            s.line(x - r * 0.5, y, x + r * 0.5, y, GREY, 0.9)
            s.line(x, y - r * 0.5, x, y + r * 0.5, GREY, 0.9)
        else:
            token(s, "obj", x, y, r)
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


def glyph_monster(s, sz, x, y, open_=False):
    """Returns the half-size (pt) of the drawn glyph.  Large and Huge are drawn at their 2"x2" / 3"x3" footprints."""
    if sz in ("M", "S"):
        r = 4.6
        if open_:
            s.polygon(hexpts(x, y, r * 1.08), fill="url(#p-mon-l)", stroke=GREY, sw=1.0)
        else:
            token(s, "M", x, y, r)
        return r * 1.1
    half = {"L": 1.0, "H": 1.5}[sz] * SC
    if open_:
        s.rect(x - half, y - half, 2 * half, 2 * half, fill="url(#p-mon-l)", stroke=GREY, sw=1.4, dash="3 2")
    else:
        s.rect(x - half, y - half, 2 * half, 2 * half, fill=PAT["monster"], stroke=INK, sw=1.4)
    return half


def draw_marker(c, e):
    x, y = X(e["at"][0]), Y(e["at"][1])
    r = 5.2
    glyph_marker(c.s, e["glyph"], x, y, is_open(e), r)
    c.occupy(x - r - 0.5, y - r - 0.5, x + r + 0.5, y + r + 0.5)
    if e.get("label"):
        c.add_label(e["id"], e["label"], x, y, r, pref=e.get("lp", "rltb"))


def draw_monster(c, e):
    x, y = X(e["at"][0]), Y(e["at"][1])
    half = glyph_monster(c.s, e.get("sz", "M"), x, y, is_open(e))
    c.occupy(x - half - 0.5, y - half - 0.5, x + half + 0.5, y + half + 0.5)
    if e.get("label"):
        c.add_label(e["id"], e["label"], x, y, half, pref=e.get("lp", "rltb"))


def ray_point(shape, d, ang_deg):
    """Point at closest-point distance d from `shape` along the ray from its centre at angle ang (deg, y down)."""
    cx, cy = centre_shape(shape)
    ca, sa = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    lo, hi = 0.0, 200.0
    for _ in range(60):
        mid = (lo + hi) / 2
        px_, py_ = cx + ca * mid, cy + sa * mid
        if shape_dist(shape, ("c", px_, py_, 0.0)) < d:
            lo = mid
        else:
            hi = mid
    return cx + ca * hi, cy + sa * hi


def outline_within(c, sh, d, dash="3 2.5"):
    """Dashed outline at distance d (inches, closest point) around a footprint."""
    s = c.s
    if sh[0] == "c":
        s.circle(X(sh[1]), Y(sh[2]), (sh[3] + d) * SC, fill="none", stroke=INK, sw=0.9, dash=dash)
        return
    x0, y0, x1, y1 = sh[1:]
    r = d * SC
    X0, Y0, X1, Y1 = X(x0), Y(y0), X(x1), Y(y1)
    path = ("M%s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s Z" % (
        f1(X0), f1(Y0 - r), f1(X1), f1(r), f1(r), f1(X1 + r), f1(Y0), f1(Y1), f1(r), f1(r), f1(X1), f1(Y1 + r),
        f1(X0), f1(r), f1(r), f1(X0 - r), f1(Y1), f1(Y0), f1(r), f1(r), f1(X0), f1(Y0 - r)))
    s.raw('<g clip-path="url(#bclip)">')
    s.path(path, fill="none", stroke=INK, sw=0.9, dash=dash)
    s.raw("</g>")


def target_shape(c, e, to):
    if isinstance(to, list):
        return ("c", to[0], to[1], 0.0)
    return footprint(c.els[to])


def draw_anno(c, e, a):
    """Annotations (drawn constraint geometry).  Each is also asserted in check_map()."""
    s = c.s
    t = a["t"]
    eid = e["id"]
    me = footprint(e)
    if a.get("hide"):
        return
    if t == "ring":                       # radius ring about a centre/origin point (stated "from its centre")
        ctr = a.get("centre")
        if isinstance(ctr, list):
            cx, cy = ctr
        elif ctr in (None, "self"):
            cx, cy = centre(e)
        else:
            cx, cy = centre(c.els[ctr])
        s.raw('<g clip-path="url(#bclip)">')
        s.circle(X(cx), Y(cy), a["r"] * SC, fill="none", stroke=INK, sw=0.9, dash="3 2.5")
        s.raw("</g>")
        if a.get("label"):
            ang = math.radians(a.get("ang", -45))
            lx, ly = X(cx) + math.cos(ang) * a["r"] * SC, Y(cy) + math.sin(ang) * a["r"] * SC
            c.add_label(eid, a["label"], lx, ly, 0, pref=a.get("lp", "uvde"))
    elif t == "rel":                      # "within d of" / "at least d from" the target: ring outline or ruler
        tsh = target_shape(c, e, a["of"])
        d = a["d"]
        if a.get("style", "ruler") == "ring":
            outline_within(c, tsh, d)
            if a.get("label"):
                px_, py_ = ray_point(tsh, d, a.get("ang", -45))
                c.add_label(eid, a["label"], X(px_), Y(py_), 0, pref=a.get("lp", "uvde"))
        else:                              # ruler: a segment of exactly d from the reference toward this element
            p1, p2 = closest_points(tsh, me)
            ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) if p1 != p2 else math.radians(a.get("ang", 0))
            if "ang" in a:
                ang = math.radians(a["ang"])
                cs_ = centre_shape(tsh)
                # start on the reference boundary along that direction
                p1 = ray_point(tsh, 0.0, a["ang"])
            q2 = (p1[0] + math.cos(ang) * d, p1[1] + math.sin(ang) * d)
            dim_line(c, eid, X(p1[0]), Y(p1[1]), X(q2[0]), Y(q2[1]), a["label"], lp=a.get("lp", "c"),
                     ticks=2.6, sw=0.8)
    elif t == "edgein":                   # distance d measured inward from the boundary of a circular feature
        tsh = footprint(c.els[a["of"]])
        cx, cy = tsh[1], tsh[2]
        mx, my = centre(e)
        ang = math.atan2(my - cy, mx - cx)
        p1 = (cx + math.cos(ang) * tsh[3], cy + math.sin(ang) * tsh[3])
        q2 = (p1[0] - math.cos(ang) * a["d"], p1[1] - math.sin(ang) * a["d"])
        dim_line(c, eid, X(p1[0]), Y(p1[1]), X(q2[0]), Y(q2[1]), a["label"], lp=a.get("lp", "c"), ticks=2.6, sw=0.8)
    elif t == "pdim":                     # dimension between two Hero footprints (1" tokens) given as points
        pa = ("c", a["p"][0], a["p"][1], 0.5)
        pb = ("c", a["q"][0], a["q"][1], 0.5)
        p1, p2 = closest_points(pa, pb)
        dim_line(c, eid, X(p1[0]), Y(p1[1]), X(p2[0]), Y(p2[1]), a["label"], lp=a.get("lp", "c"), ticks=2.6)
    elif t == "dim":                      # dimension between closest points of two things (the actual drawn gap)
        tsh = target_shape(c, e, a["to"])
        p1, p2 = closest_points(me, tsh)
        dim_line(c, eid, X(p1[0]), Y(p1[1]), X(p2[0]), Y(p2[1]), a["label"], lp=a.get("lp", "c"))
    elif t in ("inside", "adj"):
        pass
    else:
        raise ValueError(t)


def draw_edge(c, e):
    s = c.s
    mode = e["mode"]
    edges = e.get("edges") or [e["edge"]]
    L = 15.0
    for ed in edges:
        pos = e.get("pos", 18)
        if ed == "N":
            x, y, dx, dy = X(pos), Y(0), 0, 1
        elif ed == "S":
            x, y, dx, dy = X(pos), Y(36), 0, -1
        elif ed == "W":
            x, y, dx, dy = X(0), Y(pos), 1, 0
        else:
            x, y, dx, dy = X(36), Y(pos), -1, 0
        gcol = INK if not is_open(e) else GREY
        if mode == "arrive":
            x1, y1, x2, y2 = x, y, x + dx * L, y + dy * L
        else:        # exit: arrow ends at the edge
            x1, y1, x2, y2 = x + dx * L, y + dy * L, x, y
        if is_open(e):
            ang = math.atan2(y2 - y1, x2 - x1)
            s.line(x1, y1, x2 - math.cos(ang) * 7, y2 - math.sin(ang) * 7, GREY, 1.4, dash="3 2")
            s.polygon([(x2, y2), (x2 - math.cos(ang) * 7 - math.sin(ang) * 3.4, y2 - math.sin(ang) * 7 + math.cos(ang) * 3.4),
                       (x2 - math.cos(ang) * 7 + math.sin(ang) * 3.4, y2 - math.sin(ang) * 7 - math.cos(ang) * 3.4)], GREY)
        else:
            arrow(s, x1, y1, x2, y2, "move", sw=1.8)
        c.occupy(min(x1, x2) - 2, min(y1, y2) - 2, max(x1, x2) + 2, max(y1, y2) + 2)
        if e.get("label") and (ed == edges[0] or e.get("label_all")):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            c.add_label(e["id"], e["label"], mx, my, 4, pref=e.get("lp", "rltb"))


def draw_edgeband(c, e):
    """Edge-attached feature (wall band, gateway) drawn as a thin rect in terrain pattern."""
    draw_feature(c, e)


def draw_title(c):
    sp = c.sp
    s = c.s
    s.text(BX, 10.2, sp["tag"], 9, 700)
    w = tw(sp["tag"], 9, 700)
    dims = '36"×36"'
    s.text(BX + w + 5, 10.2, "·  " + dims, 9, 400)
    c.inches.append(('36"', "board"))
    c.inches.append(('36"', "board"))
    # North arrow (top right)
    ax = BX + c.bs - 5
    s.polygon([(ax, 3), (ax - 3.2, 9.5), (ax + 3.2, 9.5)], INK)
    s.text(ax - 6, 10.2, "N", 9, 700, "end")
    # E / W / S letters
    s.text(BX - 4, Y(18) + 3.4, "W", 9, 700, "end")
    s.text(BX + c.bs + 4, Y(18) + 3.4, "E", 9, 700, "start")


def draw_footer(c):
    s = c.s
    y = BY + c.bs + 13
    # scale bar (6")
    x0 = BX
    s.line(x0, y - 3, x0 + 6 * SC, y - 3, INK, 1.4)
    s.line(x0, y - 6, x0, y, INK, 1.0)
    s.line(x0 + 6 * SC, y - 6, x0 + 6 * SC, y, INK, 1.0)
    s.line(x0 + 3 * SC, y - 5, x0 + 3 * SC, y - 1, INK, 0.8)
    s.text(x0 + 6 * SC + 4, y, '6" scale', 9, 400)
    sw_ = tw('6" scale', 9, 400)
    s.text(x0 + 6 * SC + 4 + sw_ + 12, y, "Schematic", 9, 600)
    s.text(BX + c.bs, y + 0.0, "", 9)
    # S letter below board, right end
    s.text(BX + c.bs + 4, BY + c.bs + 9, "S", 9, 700, "start")
    y += 12.5
    for ln in c.foot_lines():
        for sub in wrap(ln, COL_W - 2 * 6, 9, 400):
            s.text(6, y, sub, 9, 400)
            y += 10.4
    return y


def foot_lines_impl(c):
    out = []
    sp = c.sp
    if c.illus:
        out.append(NOTE_STD)
    for t in sp.get("foot", []):
        out.append(t["text"])
        for v in inch_tokens(t["text"]):
            c.inches.append((v + '"', "foot:" + t["text"][:20]))
    return out


Ctx.foot_lines = foot_lines_impl


ORDER = {"zone": 0, "feature": 1, "edgeband": 1, "marker": 3, "monster": 4, "edge": 5}


def draw_map(sp):
    c = Ctx(sp)
    s = c.s
    c.illus = any(e["status"] == "ILLUSTRATIVE" or e.get("draw") == "open" for e in sp["elements"])
    draw_board(c)
    for e in sp["elements"]:
        if e["kind"] == "zone":
            draw_zone(c, e)
    for e in sp["elements"]:
        if e["kind"] in ("feature", "edgeband"):
            draw_feature(c, e)
    for e in sp["elements"]:
        for a in e.get("anno", []):
            draw_anno(c, e, a) if a["t"] in ("within", "ring") else None
    for e in sp["elements"]:
        for a in e.get("anno", []):
            draw_anno(c, e, a) if a["t"] not in ("within", "ring") else None
    for e in sp["elements"]:
        if e["kind"] == "marker":
            draw_marker(c, e)
    for e in sp["elements"]:
        if e["kind"] == "monster":
            draw_monster(c, e)
    for e in sp["elements"]:
        if e["kind"] == "edge":
            draw_edge(c, e)
    for (party, tx, ty) in c.tokens:
        token(s, party, tx, ty, 4.4)
    c.place_labels()
    draw_title(c)
    yend = draw_footer(c)
    for eid, text in [(l["eid"], l["text"]) for l in c.labels]:
        pass
    return c, yend + 2


fig_audit = {}
FIRST_MAP_FIG = 21
LEGEND_FIG = "FIG-20"
LEGEND_ANCHOR_LINE = 11970
TEMPLATE_ANCHOR_LINE = 11062
LEGEND_LINES = [594, 618, 619, 11035, 11056, 11058, 11072]
TEMPLATE_LINES = [592, 11062, 11068, 11069, 11071, 11072, 11073]
SHARED_OK = list(range(11029, 11077)) + list(range(14870, 14967)) + [10984, 594, 592]


def build_fig(key):
    sp = spec()["scenarios"][key]
    c, h = draw_map(sp)
    fig_audit[key] = c
    return c.s, h


# ---------------------------------------------------------------------------------------------
# FIG-20: legend for the 10.4 deployment maps (full width)
# ---------------------------------------------------------------------------------------------
def _sw_zone(s, x, y, party):
    s.rect(x, y - 7, 30, 14, fill=PALE, stroke=INK, sw=0.9, dash="3.2 2.2")
    if party == "A":
        s.rect(x, y - 7, 3.2, 14, fill=INK, stroke=None)
        token(s, "A", x + 18, y, 4.4)
    elif party == "B":
        s.rect(x, y - 7, 3.2, 14, fill=WHITE, stroke=INK, sw=0.8)
        token(s, "B", x + 18, y, 4.4)
    else:
        s.rect(x, y - 7, 3.2, 14, fill=INK, stroke=None)
        s.line(x + 1.6, y - 7, x + 1.6, y + 7, WHITE, 1.0, dash="3 3")
        token(s, "A", x + 12, y, 3.9)
        token(s, "B", x + 23, y, 3.9)


def _sw_terrain(s, x, y, kind, open_=False):
    fill = TER[kind][1 if open_ else 0] if kind != "open" else "none"
    s.rect(x + 2, y - 6, 26, 12, fill=fill, stroke=GREY if open_ else INK, sw=0.9, dash="3 2" if open_ else None)


def _sw_ruler(s, x, y):
    s.line(x + 2, y, x + 28, y, INK, 0.8)
    s.line(x + 2, y - 3, x + 2, y + 3, INK, 0.8)
    s.line(x + 28, y - 3, x + 28, y + 3, INK, 0.8)


def _sw_ring(s, x, y):
    s.circle(x + 15, y, 6.5, fill="none", stroke=INK, sw=0.9, dash="3 2.5")
    s.circle(x + 15, y, 1.6, fill=INK, stroke=None)


def _sw_arrow(s, x, y, out):
    s.line(x + 2, y + 7, x + 28, y + 7, INK, 1.3)
    if out:
        arrow(s, x + 15, y - 6, x + 15, y + 6, "move", sw=1.6)
    else:
        arrow(s, x + 15, y + 6, x + 15, y - 6, "move", sw=1.6)


def _legend_col(s, x, y, title, entries, width, audit):
    s.text(x, y, title, 9.5, 700)
    y += 7
    for fn, text in entries:
        lines = wrap(text, width - 36, 9)
        h = max(15, len(lines) * 10.4 + 4)
        fn(s, x, y + h / 2)
        for k, ln in enumerate(lines):
            s.text(x + 36, y + 7.6 + k * 10.4 + (h - len(lines) * 10.4) / 2 - 1, ln, 9)
        audit.append(text)
        y += h
    return y


def fig20():
    s = MapSvg(FULL_W)
    audit = []
    s.text(0, 10, "Key to the deployment maps in 10.4", 10.5, 700)
    cw = 122
    xs = [0, 127, 254, 381]
    col = [
        ("Parties and zones", [
            (lambda s_, x, y: _sw_zone(s_, x, y, "A"), "Party A zone: black Heroes, solid edge band"),
            (lambda s_, x, y: _sw_zone(s_, x, y, "B"), "Party B zone: dotted Heroes, open edge band"),
            (lambda s_, x, y: _sw_zone(s_, x, y, "AB"), "Zone both parties share (both Hero symbols)"),
            (lambda s_, x, y: s_.text(x + 15, y + 3.4, "A  B", 9, 700, "middle"), "Positions of Heroes inside a zone are free; two or three are drawn"),
        ]),
        ("Markers and Monsters", [
            (lambda s_, x, y: glyph_marker(s_, "obj", x + 15, y), "Objective or carried objective"),
            (lambda s_, x, y: glyph_marker(s_, "chest", x + 15, y), "Treasure Chest"),
            (lambda s_, x, y: glyph_marker(s_, "haz", x + 15, y), "Hazard marker"),
            (lambda s_, x, y: glyph_marker(s_, "mk", x + 15, y), "Other marker or token"),
            (lambda s_, x, y: glyph_monster(s_, "M", x + 15, y), "Monster Group: G1 is Group 1, R Resting, A Awake"),
            (lambda s_, x, y: glyph_monster(s_, "L", x + 15, y), "Large Monster (2\"×2\"), drawn at footprint scale"),
        ]),
        ("Terrain", [
            (lambda s_, x, y: _sw_terrain(s_, x, y, "blocking"), "Blocking"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "impassable"), "Impassable"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "cover"), "Cover"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "difficult"), "Difficult"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "water"), "Shallow or Deep Water"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "slippery"), "Slippery"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "obstacle"), "Impassable or Blocking, decided per piece (2.9.1)"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "hazard"), "Hazard area (Unstable Ground)"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "shade"), "Deep Shadow or Darkness"),
            (lambda s_, x, y: s_.line(x + 2, y, x + 28, y, INK, 2.4), "Blocking wall, drawn as a line"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "open"), "Open feature: room, clearing, path"),
        ]),
        ("Distances, edges, status", [
            (_sw_ruler, "Stated distance at map scale; 'min' means at least"),
            (_sw_ring, "Ring: within the stated distance"),
            (lambda s_, x, y: pill(s_, x + 15, y + 3.4, '6–8"'), "A range: any value inside it is legal"),
            (lambda s_, x, y: _sw_arrow(s_, x, y, True), "Exit or extraction through that edge"),
            (lambda s_, x, y: _sw_arrow(s_, x, y, False), "Arrival from off the battlefield (R3 is Round 3)"),
            (lambda s_, x, y: _sw_terrain(s_, x, y, "cover", True), "Grey dashed: one legal arrangement; position not fixed by the rules"),
        ]),
    ]
    yend = 0
    for (title, entries), x in zip(col, xs):
        yy = _legend_col(s, x, 28, title, entries, cw, audit)
        yend = max(yend, yy)
    y = yend + 8
    s.line(0, y - 3, FULL_W, y - 3, INK, 0.6)
    notes = [
        "**Orientation.** North is drawn at the top. The Setup Roll-off winner designates the North edge before setup; North and South are the short battlefield edges and East and West the long ones, even on a square battlefield (10.1).",
        "**Scale.** The battlefield, zones and stated distances are drawn to scale at 5.2 pt per inch, with a 6\" scale bar; markers are enlarged, and Large and Huge Monsters are drawn at their 2\"×2\" and 3\"×3\" footprints. Distances are measured between closest points, except from a centre or origin where the rule says so (2.6).",
        "**Counts.** Scattered terrain is drawn as a few representative pieces; the printed counts and the 10.6 scaling stay in the scenario text. Group numbers are the scenario's own. Hidden contents (face-down markers) are never drawn.",
        "**Solid and dashed.** A solid marker or zone with a distance symbol is one position that meets that printed limit, not a fixed position; only the battlefield, zone depths and stated distances are exact. Letters A and B beside exit arrows or zones are the drawn zones' parties; where a scenario assigns Party A or B by die roll, the drawn zones do not say who is which.",
        "**Where a scenario is silent**, 10.1 step 11 applies: the Setup Roll-off winner chooses the edge or corner zone and the other party takes the opposite one; each zone extends 6\" from its edge, a corner zone is 8\"×8\", and parties alternate placing Heroes, starting with the party that lost the Roll-off.",
    ]
    for n in notes:
        y = s.para(0, y + 6, n, FULL_W, 9, 400, lead=10.8) - 1
        audit.append(n)
    fig20.audit = audit
    return s, y + 4


# ---------------------------------------------------------------------------------------------
# procedural template (10.1 Preparation Steps)
# ---------------------------------------------------------------------------------------------
TPL_STEPS = [
    ("Determine Average Party Level (APL).", False),
    ("Choose Climate.", False),
    ("Choose the Core Scenario.", False),
    ("Generate Secondary Objectives: record only.", False),
    ("Generate Weather: record only.", False),
    ("Resolve the Setup Roll-off.", False),
    ("**Place Terrain.** Major Blocking or Impassable Terrain stays 3\" from a battlefield edge and 6\" from a deployment zone unless the scenario says otherwise.", True),
    ("Place Objectives and Markers.", False),
    ("Generate and Place Monsters.", False),
    ("Assign Guard Points.", False),
    ("**Deploy the Parties** as the scenario instructs. Where it is silent: the Roll-off winner chooses an edge or corner zone and the other party takes the opposite one; alternate placing Heroes, the Roll-off loser first.", True),
    ("Begin Round 1 with the Initiative Phase.", False),
]
ST = 3.3                     # template pt per inch


def template_geometry():
    """Step 7 exclusion region for the step 11 defaults, derived from the stated distances (3", 6", 8")."""
    edge_margin, clear, depth, corner = 3.0, 6.0, 6.0, 8.0
    edge_rect = (depth + clear, edge_margin, 36 - depth - clear, 36 - edge_margin)           # (12, 3, 24, 33)
    return dict(edge_margin=edge_margin, clear=clear, depth=depth, corner=corner, edge_rect=edge_rect)


def _tpl_board(s, ox, oy, variant, audit):
    g = template_geometry()
    bs = 36 * ST

    def P(x, y):
        return ox + x * ST, oy + y * ST
    s.rect(ox, oy, bs, bs, fill=PAT["aoe"], stroke=None)
    if variant == "edge":
        x0, y0, x1, y1 = g["edge_rect"]
        s.rect(ox + x0 * ST, oy + y0 * ST, (x1 - x0) * ST, (y1 - y0) * ST, fill=WHITE, stroke=INK, sw=0.8, dash="3 2")
        zones = [("A", (0, 0, g["depth"], 36)), ("B", (36 - g["depth"], 0, 36, 36))]
    else:
        c_, r_ = g["corner"], g["clear"]
        e_ = g["edge_margin"]
        pts = "M%s %s H%s V%s H%s A%s %s 0 0 0 %s %s V%s H%s V%s H%s A%s %s 0 0 0 %s %s V%s Z" % (
            f1(ox + (c_ + r_) * ST), f1(oy + e_ * ST), f1(ox + (36 - e_) * ST), f1(oy + (36 - c_ - r_) * ST),
            f1(ox + (36 - c_) * ST), f1(r_ * ST), f1(r_ * ST), f1(ox + (36 - c_ - r_) * ST), f1(oy + (36 - c_) * ST),
            f1(oy + (36 - e_) * ST), f1(ox + e_ * ST), f1(oy + (c_ + r_) * ST), f1(ox + c_ * ST),
            f1(r_ * ST), f1(r_ * ST), f1(ox + (c_ + r_) * ST), f1(oy + c_ * ST), f1(oy + e_ * ST))
        s.path(pts, fill=WHITE, stroke=INK, sw=0.8, dash="3 2")
        zones = [("A", (0, 0, c_, c_)), ("B", (36 - c_, 36 - c_, 36, 36))]
    s.rect(ox, oy, bs, bs, fill="none", stroke=INK, sw=1.2)
    for party, (x0, y0, x1, y1) in zones:
        s.rect(ox + x0 * ST, oy + y0 * ST, (x1 - x0) * ST, (y1 - y0) * ST, fill=PALE, stroke=INK, sw=0.9, dash="3.2 2.2")
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if variant == "edge":
            for f in (0.2, 0.5, 0.8):
                token(s, party, ox + cx * ST, oy + (y0 + (y1 - y0) * f) * ST, 3.6)
        else:
            token(s, party, ox + (x0 + 2.6) * ST, oy + (y0 + 2.6) * ST, 3.6)
            token(s, party, ox + (x1 - 2.6) * ST, oy + (y1 - 2.6) * ST, 3.6)
    # dimensions
    lab = []
    if variant == "edge":
        _tpl_dim(s, ox + 0 * ST, oy + 17.5 * ST, ox + 6 * ST, oy + 17.5 * ST, '6"')
        _tpl_dim(s, ox + 6 * ST, oy + 17.5 * ST, ox + 12 * ST, oy + 17.5 * ST, '6"')
        _tpl_dim(s, ox + 18 * ST, oy + 0 * ST, ox + 18 * ST, oy + 3 * ST, '3"')
        audit += ['6"', '6"', '3"']
    else:
        _tpl_dim(s, ox + 0 * ST, oy + 9.5 * ST, ox + 8 * ST, oy + 9.5 * ST, '8"')
        _tpl_dim(s, ox + 18 * ST, oy + 0 * ST, ox + 18 * ST, oy + 3 * ST, '3"')
        s.line(ox + 8 * ST, oy + 8 * ST, ox + (8 + 6 * math.cos(math.radians(45))) * ST, oy + (8 + 6 * math.sin(math.radians(45))) * ST, INK, 0.8)
        pill(s, ox + 14.6 * ST, oy + 13.6 * ST, '6"', 9, 600)
        audit += ['8"', '3"', '6"']
    return bs


def _tpl_dim(s, x1, y1, x2, y2, label):
    s.line(x1, y1, x2, y2, INK, 0.8)
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    for (px_, py_) in ((x1, y1), (x2, y2)):
        s.line(px_ - nx * 2.6, py_ - ny * 2.6, px_ + nx * 2.6, py_ + ny * 2.6, INK, 0.8)
    pill(s, (x1 + x2) / 2, (y1 + y2) / 2 + 3.2, label, 9, 600)


def fig57():
    s = MapSvg(FULL_W)
    audit = []
    g = template_geometry()
    assert g["depth"] + g["clear"] == 12 and 36 - 12 == 24 and g["corner"] + g["clear"] == 14
    s.text(0, 10, "10.1 Preparation Steps", 10.5, 700)
    # flow
    fw = 214
    y = 22
    for i, (txt, hot) in enumerate(TPL_STEPS, 1):
        lines = wrap(txt, fw - 24, 9)
        h = max(15, len(lines) * 10.4 + 4)
        if hot:
            s.rect(0, y - 1, fw, h + 1, fill=PALE, stroke=INK, sw=0.9, rx=2)
        callout(s, 9.5, y + h / 2, i, 6.6)
        for k, ln in enumerate(lines):
            s.text(22, y + 8.2 + k * 10.4 + (h - len(lines) * 10.4) / 2 - 1, ln, 9)
        audit.append(txt)
        if i < len(TPL_STEPS):
            s.line(9.5, y + h / 2 + 6.8, 9.5, y + h + 3.6, INK, 1.0)
        y += h + 4
    yflow = y
    # right: label + two boards
    rx = 232
    box_w = FULL_W - rx
    s.rect(rx, 6, box_w, 17, fill=WHITE, stroke=INK, sw=1.2, rx=2)
    s.text(rx + box_w / 2, 18.2, "Template — not a fixed battlefield", 10, 700, "middle")
    bw = 36 * ST
    gap = 14
    ox1, ox2 = rx + 6, rx + 6 + bw + gap
    oy = 44
    s.text(ox1, 36.8, "Step 11 default: edge zones", 9, 700)
    s.text(ox2, 36.8, "Step 11 default: corner zones", 9, 700)
    _tpl_board(s, ox1, oy, "edge", audit)
    _tpl_board(s, ox2, oy, "corner", audit)
    yb = oy + bw + 12
    t1 = "Zones are 6\" deep. The other pair of opposite edges works the same way."
    t2 = "Corner zones are 8\"×8\"; the second zone is diagonally opposite."
    ya = s.para(ox1, yb, t1, bw + 6, 9, 400, lead=10.4)
    yb2 = s.para(ox2, yb, t2, bw + 6, 9, 400, lead=10.4)
    audit += [t1, t2]
    yk = max(ya, yb2) + 6
    # key
    s.rect(rx, yk - 8, 22, 11, fill=PAT["aoe"], stroke=INK, sw=0.8)
    s.text(rx + 28, yk + 1, "Step 7: no major Blocking or Impassable Terrain here", 9)
    s.rect(rx, yk + 7, 22, 11, fill=WHITE, stroke=INK, sw=0.8, dash="3 2")
    s.text(rx + 28, yk + 16, "Step 7: major Blocking or Impassable Terrain allowed", 9)
    s.rect(rx, yk + 22, 22, 11, fill=PALE, stroke=INK, sw=0.9, dash="3.2 2.2")
    s.text(rx + 28, yk + 31, "Deployment zone (Party A black, Party B dotted)", 9)
    nt = "Drawn to scale at 3.3 pt per inch on a 36\"×36\" battlefield; the 3\" edge margin and the 6\" distance from a zone are measured from the zone's outline, so corner zones leave a rounded exclusion."
    ye = s.para(rx, yk + 44, nt, box_w, 9, 400, lead=10.4)
    audit += [nt]
    fig57.audit = audit
    return s, max(yflow, ye) + 4


# ---------------------------------------------------------------------------------------------
# metadata for figdata (manifest and placements)
# ---------------------------------------------------------------------------------------------
def _sec(key):
    return key


def scenario_order():
    spans = scenario_spans()
    return sorted(spans, key=lambda k: spans[k][0])


def meta_entries():
    spans = scenario_spans()
    sc = spec()["scenarios"]
    out = {}
    out[LEGEND_FIG] = dict(
        title="Key to the 10.4 deployment maps",
        purpose="One shared key for the 36 column-width deployment maps in 10.4: party zones, markers, Monster Group notation, terrain patterns, distance and edge symbols, map scale and the status convention for open positions.",
        source_refs=["10.1 Random Direction and Battlefield Edges (11056-11058)", "10.1 Setup Roll-off (11035) and Preparation Steps, step 11 (11072)",
                     "2.6 Measurement (594) and Size and Footprints (618-619)", "2.9.1 Terrain Types (832-878)"],
        geometry_spec="Four columns of swatches (parties and zones; markers and Monsters; terrain patterns; distances, edges and status) above four short notes on orientation, scale, counts and the step 11 default; no board geometry beyond the swatches.",
        caption="Key to the deployment maps in 10.4: symbols for zones, markers, Monster Groups, terrain, distances and edges, with the orientation, scale and open-position conventions every map follows (see 10.4).",
        insert_after="B%05d" % LEGEND_ANCHOR_LINE, scope="full", schematic=False,
        semantic_check="Swatches reuse the figures/README visual grammar; every inch value printed (6\", 8\"x8\", 2\"x2\", 3\"x3\") is checked against lines 594, 618-619 and 11072; North/short/long edge naming against 11056-11058; closest-point measurement against 594.",
        ambiguity="None in the key. Terrain pieces whose type the scenario leaves to 2.9.1 ('Impassable or Blocking') use a neutral grey swatch rather than either type.",
        new_figure=True)
    for key in scenario_order():
        sp = sc[key]
        hl, end, cno, sno, title, climate = spans[key]
        cnt = {"MANDATORY_POSITION": 0, "CONSTRAINED": 0, "ILLUSTRATIVE": 0}
        for e in sp["elements"]:
            cnt[e["status"]] += 1
        refs = ["10.4 %s Scenario %d: %s (source lines %d-%d)" % (climate, sno, title, hl, end),
                "10.1 Preparation Steps, step 11 (11072)" if any(11072 in e.get("shared", []) for e in sp["elements"]) else "10.1 Preparation Steps (11060-11073)"]
        out[sp["fig"]] = dict(
            title="%s Scenario %d: %s, deployment map" % (climate, sno, title),
            purpose="Column-width top-down map of the setup for %s %d: battlefield, both deployment zones with depth, objectives and markers, required terrain, Monster placement and any entry or exit edges, using only values the scenario states." % (climate, sno),
            source_refs=refs,
            geometry_spec="36\"x36\" battlefield at 5.2 pt per inch (zones and stated distances to scale; markers enlarged; Large and Huge Monsters at footprint scale). %d mandatory, %d constrained and %d illustrative elements, each citing its source lines in scenario_specs.json; illustrative elements are light grey dashed." % (cnt["MANDATORY_POSITION"], cnt["CONSTRAINED"], cnt["ILLUSTRATIVE"]),
            caption=sp["caption"],
            insert_after="B%05d" % sp["insert_after_line"], scope="column", schematic=True,
            semantic_check="Each element's source lines lie inside lines %d-%d; every printed inch value is found in its cited lines; distances, containments and 'at least' / 'within' relations are asserted in make_figures.selfcheck (check_scenmaps); zones, markers and Blocking or Impassable pieces are checked against the 10.1 step 7 and step 8 distances." % (hl, end),
            ambiguity=("; ".join(sp["ambiguities"]) if sp["ambiguities"] else "None affecting the drawing. Positions the source leaves open are drawn as one legal arrangement in grey dashes."),
            new_figure=True)
    out["FIG-%d" % (FIRST_MAP_FIG + 36)] = dict(
        title="10.1 Preparation Steps: procedural template",
        purpose="Template, not a fixed battlefield: the twelve Preparation Steps, with the step 11 default deployment zones and the step 7 terrain exclusion distances on a generic battlefield.",
        source_refs=["10.1 Preparation Steps, steps 1-12 (11062-11073)", "2.6 Measurement (592)"],
        geometry_spec="Left: the 12 Preparation Steps as numbered rows (steps 7 and 11 highlighted). Right: two 36\"x36\" boards at 3.3 pt per inch. Edge default: zones 6\" deep on opposite edges, exclusion = 3\" from an edge and 6\" from a zone (allowed region 12\"-24\" across, 3\"-33\" down). Corner default: 8\"x8\" corner zones diagonally opposite, exclusion with rounded 6\" corners.",
        caption="Template, not a fixed battlefield: the twelve Preparation Steps, with the step 11 default zones (6\" deep or 8\"×8\" corners) and the step 7 limits on major Blocking and Impassable Terrain (3\" from an edge, 6\" from a zone) (see 10.1).",
        insert_after="B%05d" % TEMPLATE_ANCHOR_LINE, scope="full", schematic=True,
        semantic_check="Step text compared with lines 11062-11073; 3\" and 6\" from step 7 (11068), 6\", 8\"x8\" and alternate placing from step 11 (11072); selfcheck asserts 6+6=12, 36-12=24, 8+6=14 and that the printed inch values appear in the cited lines.",
        ambiguity="None. Which edge pair or corner pair is used is chosen by the Setup Roll-off winner; the figure shows one example of each and says so.",
        new_figure=True)
    return out


# ---------------------------------------------------------------------------------------------
# checks (called from make_figures.selfcheck)
# ---------------------------------------------------------------------------------------------
KINDS = {"zone", "feature", "marker", "monster", "edge"}
LEGEND_TERRAIN = {"blocking", "impassable", "cover", "difficult", "water", "slippery", "obstacle", "open", "hazard", "shade", "gap"}
STATUSES = {"MANDATORY_POSITION", "CONSTRAINED", "ILLUSTRATIVE"}
TOL = 0.06


def _text_of(lines):
    return cited_text(lines)


def _anno_checks(sp, e, errs, key):
    els = {x["id"]: x for x in sp["elements"]}
    me = footprint(e)
    for a in e.get("anno", []):
        t = a["t"]
        tag = "%s/%s/%s" % (key, e["id"], t)
        if t == "rel":
            to = a["of"]
            tsh = ("c", to[0], to[1], 0.0) if isinstance(to, list) else footprint(els[to])
            d = shape_dist(me, tsh)
            rel = a.get("rel", "le")
            if rel == "le" and d > a["d"] + TOL:
                errs.append("%s: distance %.2f exceeds 'within %s'" % (tag, d, a["d"]))
            if rel == "ge" and d < a["d"] - TOL:
                errs.append("%s: distance %.2f below 'at least %s'" % (tag, d, a["d"]))
            if rel == "eq" and abs(d - a["d"]) > TOL:
                errs.append("%s: distance %.2f is not %s" % (tag, d, a["d"]))
        elif t == "ring":
            ctr = a.get("centre")
            cx, cy = ctr if isinstance(ctr, list) else (centre(e) if ctr in (None, "self") else centre(els[ctr]))
            if ctr in (None, "self"):
                continue
            if isinstance(ctr, str):
                my = centre(e)
                dd = math.hypot(my[0] - cx, my[1] - cy)
                rel = a.get("rel", "eq")
                if rel == "eq" and abs(dd - a["r"]) > TOL + 0.01:
                    errs.append("%s: centre distance %.2f is not %s" % (tag, dd, a["r"]))
        elif t == "edgein":
            sh = footprint(els[a["of"]])
            my = centre(e)
            dd = sh[3] - math.hypot(my[0] - sh[1], my[1] - sh[2])
            if abs(dd - a["d"]) > TOL + 0.01:
                errs.append("%s: inward distance %.2f is not %s" % (tag, dd, a["d"]))
        elif t == "inside":
            if not inside(e, els[a["of"]]):
                errs.append("%s: not inside %s" % (tag, a["of"]))
        elif t == "dim":
            to = a["to"]
            tsh = ("c", to[0], to[1], 0.0) if isinstance(to, list) else footprint(els[to])
            d = shape_dist(me, tsh)
            if d < a["lo"] - TOL or (a.get("hi") is not None and d > a["hi"] + TOL):
                errs.append("%s: dimension %.2f outside %s-%s" % (tag, d, a["lo"], a.get("hi")))
        elif t == "pdim":
            d = math.hypot(a["p"][0] - a["q"][0], a["p"][1] - a["q"][1]) - 1.0
            if d < a["lo"] - TOL or (a.get("hi") is not None and d > a["hi"] + TOL):
                errs.append("%s: Hero gap %.2f outside %s-%s" % (tag, d, a["lo"], a.get("hi")))
        else:
            errs.append("%s: unknown annotation" % tag)


def check_scenmaps():
    """Returns a list of problems (empty when every map passes)."""
    errs = []
    spans = scenario_spans()
    sc = spec()["scenarios"]
    if len(spans) != 36:
        errs.append("expected 36 scenario headings in 10.4, found %d" % len(spans))
    if set(spans) != set(sc):
        errs.append("scenario heading/spec mismatch: %s" % sorted(set(spans) ^ set(sc)))
    order = scenario_order()
    figs = [sc[k]["fig"] for k in order if k in sc]
    if figs != ["FIG-%d" % (FIRST_MAP_FIG + i) for i in range(len(order))]:
        errs.append("map figure ids are not sequential in book order")
    if len(set(figs)) != len(figs):
        errs.append("a scenario has more than one map or two scenarios share a map")
    L = source_lines()
    for key in order:
        if key not in sc:
            continue
        sp = sc[key]
        hl, end = spans[key][0], spans[key][1]
        if sp["tag"] != key:
            errs.append("%s: tag %r" % (key, sp["tag"]))
        if not (hl <= sp["insert_after_line"] <= end):
            errs.append("%s: insertion line outside the scenario" % key)
        if not (hl <= sp["board_line"] <= end) or '36"×36"' not in L[sp["board_line"] - 1]:
            errs.append("%s: board_line does not state 36\"x36\"" % key)
        ids = set()
        zones = []
        for e in sp["elements"]:
            tag = "%s/%s" % (key, e.get("id"))
            if e["id"] in ids:
                errs.append("%s: duplicate id" % tag)
            ids.add(e["id"])
            if e["kind"] not in KINDS:
                errs.append("%s: kind %s" % (tag, e["kind"]))
            if e["status"] not in STATUSES:
                errs.append("%s: status %s" % (tag, e["status"]))
            if not e["lines"]:
                errs.append("%s: no source lines" % tag)
            for n in e["lines"]:
                if not (hl <= n <= end):
                    errs.append("%s: line %d outside %d-%d" % (tag, n, hl, end))
            for n in e.get("shared", []):
                if n not in SHARED_OK:
                    errs.append("%s: shared line %d is not a 10.1 / 10.6 rule line" % (tag, n))
            if e["kind"] == "zone":
                zones.append(e)
            if e["kind"] == "feature" and e.get("terrain", "open") not in LEGEND_TERRAIN:
                errs.append("%s: terrain %s has no legend swatch" % (tag, e.get("terrain")))
            if e["kind"] == "edge" and e["mode"] == "arrive" and "midpoint" in _text_of(e["lines"]) and e.get("pos") != 18:
                errs.append("%s: arrival at an edge midpoint must be drawn at 18\"" % tag)
        for t in sp.get("foot", []):
            for n in t["lines"]:
                if not (hl <= n <= end):
                    errs.append("%s: foot line %d outside" % (key, n))
        for u in sp.get("undrawn", []):
            for n in u["lines"]:
                if not (hl <= n <= end):
                    errs.append("%s: undrawn line %d outside" % (key, n))
        # draw and audit printed inch values
        spc = json.loads(json.dumps(sp))
        c, h = draw_map(spc)
        if h > 275:
            errs.append("%s: map height %.0f pt exceeds the column height" % (key, h))
        for w in c.warn:
            if float(w.rsplit("(", 1)[1].split(" ")[0]) > 6:
                errs.append("%s: %s" % (key, w))
        els = {e["id"]: e for e in sp["elements"]}
        for (tok, eid) in c.inches:
            if eid == "board":
                txt = _text_of([sp["board_line"]])
            elif eid.startswith("foot:"):
                txt = _text_of([n for t in sp["foot"] if t["text"].startswith(eid[5:]) for n in t["lines"]])
            else:
                e = els[eid]
                txt = _text_of(e["lines"] + e.get("shared", []))
            if tok not in txt:
                errs.append("%s/%s: printed %s not found in cited source lines" % (key, eid, tok))
        # legality
        for e in sp["elements"]:
            _anno_checks(sp, e, errs, key)
        zshapes = [footprint(z) for z in zones]
        for e in sp["elements"]:
            tag = "%s/%s" % (key, e["id"])
            fp = footprint(e) if e["kind"] != "edge" else None
            if fp is not None:
                for v in (fp[1], fp[2]) if fp[0] == "c" else (fp[1], fp[2], fp[3], fp[4]):
                    if v < -0.01 or v > 36.01:
                        errs.append("%s: footprint outside the 36\"x36\" battlefield" % tag)
                        break
            if e["kind"] in ("marker", "monster") and not e.get("zone_ok"):
                for z, zs in zip(zones, zshapes):
                    if shape_dist(fp, zs) < 0.01:
                        errs.append("%s: marker or Monster inside deployment zone %s (10.1 step 8)" % (tag, z["id"]))
            if e["kind"] == "feature" and e.get("terrain") in ("blocking", "impassable", "obstacle") and not e.get("exempt"):
                bb_ = fp if fp[0] == "r" else ("r", fp[1] - fp[3], fp[2] - fp[3], fp[1] + fp[3], fp[2] + fp[3])
                if bb_[1] < 3 - 0.01 or bb_[2] < 3 - 0.01 or bb_[3] > 33 + 0.01 or bb_[4] > 33 + 0.01:
                    errs.append("%s: Blocking/Impassable piece within 3\" of an edge (10.1 step 7)" % tag)
                for z, zs in zip(zones, zshapes):
                    if shape_dist(fp, zs) < 6 - 0.01:
                        errs.append("%s: Blocking/Impassable piece within 6\" of zone %s (10.1 step 7)" % (tag, z["id"]))
            if e["kind"] == "zone":
                for tk in e.get("tokens") or []:
                    if not (e["rect"][0] <= tk[0] <= e["rect"][2] and e["rect"][1] <= tk[1] <= e["rect"][3]):
                        errs.append("%s: Hero token outside its zone" % tag)
    # legend and template inch audit
    for name, fn, lines in (("legend", fig20, LEGEND_LINES), ("template", fig57, TEMPLATE_LINES)):
        fn()
        txt = _text_of(lines)
        for t in fn.audit:
            for v in inch_tokens(t):
                if v + '"' not in txt:
                    errs.append("%s: printed %s\" not in the cited lines" % (name, v))
    return errs


FIG14_SCENARIOS = {"Greenmark 3", "Greenmark 4", "Undermarches 2", "Undermarches 3"}


def _detail_figures(key, sp):
    """Existing detail figures that explain the same deployment: FIG-13 (generic patterns) unless FIG-14 covers it."""
    det = []
    if key not in FIG14_SCENARIOS:
        det.append("FIG-13")
    for f in sp["detail_figures"]:
        if f not in det:
            det.append(f)
    if key == "Undermarches 2" and "FIG-14" not in det:
        det.insert(0, "FIG-14")
    return det


def coverage_matrix(dims=None):
    """production/qa/scenario-coverage.json content."""
    spans = scenario_spans()
    sc = spec()["scenarios"]
    blocked = {"Undermarches 1", "Sun-Drowned 3", "The Mire 2", "The Mire 5"}
    rows = []
    summ = {"MANDATORY_POSITION": 0, "CONSTRAINED": 0, "ILLUSTRATIVE": 0}
    amb_total = 0
    for key in scenario_order():
        sp = sc[key]
        hl, end, cno, sno, title, climate = spans[key]
        cnt = {"mandatory": 0, "constrained": 0, "illustrative": 0}
        for e in sp["elements"]:
            cnt[{"MANDATORY_POSITION": "mandatory", "CONSTRAINED": "constrained", "ILLUSTRATIVE": "illustrative"}[e["status"]]] += 1
            summ[e["status"]] += 1
        amb_total += len(sp["ambiguities"])
        rows.append(dict(
            key=key, climate=climate, climate_number=cno, number=sno, title=title, source_lines=[hl, end],
            map_figure=sp["fig"], detail_figures=_detail_figures(key, sp), insert_after="B%05d" % sp["insert_after_line"],
            setup_rules=sp["setup_rules"],
            elements=cnt, undrawn_conditional=[dict(u) for u in sp.get("undrawn", [])],
            ambiguities=sp["ambiguities"],
            status="blocked-by-ambiguity" if key in blocked else "drawn"))
    return rows, summ, amb_total


def _install():
    for key, sp in spec()["scenarios"].items():
        n = int(sp["fig"].split("-")[1])
        globals()["fig%d" % n] = (lambda k=key: build_fig(k))


_install()
