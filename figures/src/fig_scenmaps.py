"""Scenario setup maps: FIG-21 to FIG-56 (the 36 Core Scenarios), the board panels of FIG-18 and FIG-19 (Appendix A and B),
the shared key FIG-20 and the 10.1 template FIG-57.

Data-driven: every map is drawn from one entry of figures/src/scenario_specs.json by the one renderer in this module,
using only the glyph functions of scenkit.py (the same functions draw the key, FIG-13 to FIG-16 and the appendix figures).
Board coordinates are inches, origin at the top-left corner, x to the right, y downward; North is drawn at the top
(the Setup Roll-off winner designates North in play, 10.1).  Short edges = North/South (top/bottom), long edges =
East/West (left/right), even on a square battlefield (10.1).

Statuses recorded per spec element:
  MANDATORY_POSITION  the source fixes the location (drawn solid)
  CONSTRAINED         the source gives a range or relation (drawn solid with its dimension/ring)
  ILLUSTRATIVE        the source leaves the location open; one legal arrangement is drawn in light grey dashes
  UNRESOLVED          the text does not place the element (kind "unresolved"): shown as a ? tag with a short note
Elements may carry "draw": "open" to force the light dashed style where only the extent is fixed.

Scale: the board, zones and every stated distance are drawn at `sc` pt per inch (6 for the 36" maps, 7 for the 24"
Appendix panels); markers are enlarged (Large and Huge Monsters are drawn at their 2"x2" and 3"x3" footprints).
"""
import json
import math
import os
import re

import scenkit as K
from scenkit import MapSvg, GREY, LGREY
from svgkit import (Svg, COL_W, FULL_W, INK, DARK, MID, LIGHT, PALE, WHITE, PAT, tw, wrap, hexpts, f1, box)  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SPEC_PATH = os.path.join(HERE, "scenario_specs.json")

NOTE_STD = "Grey dashed = position not fixed by the rules"
KEY_REF = "Key: FIG-20"


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
    """{key: (heading_line, last_line, climate_no, scenario_no, title, climate)} computed from the manuscript."""
    L = source_lines()
    out = {}
    cur_climate = None
    keys = []
    for i, t in enumerate(L, 1):
        m = re.match(r"^#### Climate (\d+): (.+?) Scenarios\s*$", t)
        if m:
            cur_climate = (int(m.group(1)), m.group(2))
        m = re.match(r"^##### Scenario (\d+): (.+?)(?: \[Intro\])?\s*$", t)
        if m and cur_climate:
            keys.append((i, "%s %s" % (cur_climate[1], m.group(1)), cur_climate, int(m.group(1)), m.group(2)))
    for k, (i, key, cl, n, title) in enumerate(keys):
        end = len(L)
        for j in range(i, len(L)):
            if re.match(r"^#{1,5} ", L[j]):
                end = j
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
    if k in ("marker", "hero"):
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


def centre_shape(s):
    if s[0] == "c":
        return (s[1], s[2])
    return ((s[1] + s[3]) / 2.0, (s[2] + s[4]) / 2.0)


def closest_points(a, b):
    """Closest points between two footprints (inches), used to draw dimension lines."""
    ca, cb = centre_shape(a), centre_shape(b)

    def toward(s, p):
        if s[0] == "c":
            d = math.hypot(p[0] - s[1], p[1] - s[2]) or 1e-9
            return (s[1] + (p[0] - s[1]) / d * s[3], s[2] + (p[1] - s[2]) / d * s[3])
        return (min(max(p[0], s[1]), s[3]), min(max(p[1], s[2]), s[4]))
    pa = toward(a, cb)
    pb = toward(b, pa)
    pa = toward(a, pb)
    return pa, pb


# ---------------------------------------------------------------------------------------------
# the map context: board frame, occupancy and labels
# ---------------------------------------------------------------------------------------------
DIRS = {"r": 0, "d": 45, "b": 90, "e": 135, "l": 180, "v": 225, "t": 270, "u": 315, "R": 0, "L": 180}


class Ctx:
    def __init__(self, sp, width=COL_W, bx=None, by=14.0):
        self.sp = sp
        self.n = sp.get("board_in", 36)
        self.sc = sp.get("sc", 6.0)
        self.bs = self.n * self.sc
        self.width = width
        self.bx = (width - self.bs) / 2.0 if bx is None else bx
        self.by = by
        self.s = MapSvg(width)
        self.s.add_def('<clipPath id="bclip"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (
            f1(self.bx), f1(self.by), f1(self.bs), f1(self.bs)))
        self.occ = []          # hard occupied rects (x0, y0, x1, y1, owner)
        self.soft = []         # outlines a label should avoid but may cross
        self.labels = []
        self.inches = []       # (printed text, element id) for audit
        self.warn = []
        self.els = {e["id"]: e for e in sp["elements"]}
        self.illus = False
        self.tokens = []
        self.notes = []
        self.placed = []       # (element id, text, ring distance, hard overlap, soft overlap) per placed label

    def X(self, x):
        return self.bx + x * self.sc

    def Y(self, y):
        return self.by + y * self.sc

    # ---- occupancy ----
    def occupy(self, x0, y0, x1, y1, owner=None):
        self.occ.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), owner))

    def outline_soft(self, pts, closed=True, step=3.0):
        n = len(pts)
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            L = math.hypot(x2 - x1, y2 - y1)
            k = max(1, int(L // step))
            for j in range(k + 1):
                qx, qy = x1 + (x2 - x1) * j / k, y1 + (y2 - y1) * j / k
                self.soft.append((qx - 1.4, qy - 1.4, qx + 1.4, qy + 1.4, None))

    def overlap(self, r, lst, owner=None):
        a = 0.0
        for o in lst:
            if owner is not None and o[4] == owner:
                continue
            w = min(r[2], o[2]) - max(r[0], o[0])
            h = min(r[3], o[3]) - max(r[1], o[1])
            if w > 0 and h > 0:
                a += w * h
        return a

    # ---- labels ----
    def add_label(self, eid, text, ax, ay, cr, pref="rltb", fixed=None, weight=600, leader=True, own=None):
        self.labels.append(dict(eid=eid, text=text, ax=ax, ay=ay, cr=cr, pref=pref, fixed=fixed, weight=weight,
                                leader=leader, own=own))
        for v in inch_tokens(text):
            self.inches.append((v + '"', eid))

    def place_labels(self):
        s = self.s
        bx0, by0, bx1, by1 = self.bx + 1, self.by + 1, self.bx + self.bs - 1, self.by + self.bs - 1
        order = sorted(self.labels, key=lambda l: 0 if l["fixed"] else 1)
        for lb in order:
            lines = lb["text"].split("\n")
            w = max(tw(t, 9, lb["weight"]) for t in lines) + 3.4
            h = len(lines) * 10 + 1.6
            ax, ay, cr = lb["ax"], lb["ay"], lb["cr"]
            own = lb["own"]
            cands = []        # (x0, y0, extra_penalty, dist)
            fx = lb["fixed"]
            if fx == "c":
                cands.append((ax - w / 2, ay - h / 2, -50.0, 0))
            elif fx is not None:
                cands.append((fx[0], fx[1], -50.0, 0))
            prefs = [DIRS[c] for c in lb["pref"] if c in DIRS] or [0, 90, 180, 270]
            for k in range(16):
                th = k * 22.5
                dev = min(min(abs((th - p + 180) % 360 - 180) for p in prefs[i:i + 1]) / 45.0 * 1.4 + i * 0.7
                          for i in range(len(prefs)))
                if th not in prefs:
                    dev += 0.8
                c_, s_ = math.cos(math.radians(th)), math.sin(math.radians(th))
                ext = abs(c_) * w / 2 + abs(s_) * h / 2
                for D in (1.5, 4.5, 9.0, 15.0, 23.0, 33.0):
                    d = cr + D + ext
                    cands.append((ax + c_ * d - w / 2, ay + s_ * d - h / 2, dev + D * 0.3, D))
            best = None
            for (x0, y0, pen, D) in cands:
                r = (x0, y0, x0 + w, y0 + h)
                if r[0] < bx0 or r[2] > bx1 or r[1] < by0 or r[3] > by1:
                    continue
                hard = self.overlap(r, self.occ, own)
                soft = self.overlap(r, self.soft, own)
                score = hard * 40 + soft * 0.3 + pen
                if best is None or score < best[0]:
                    best = (score, x0, y0, hard, D, soft)
            if best is None:
                x0, y0 = ax - w / 2, ay - h / 2
                x0 = min(max(x0, bx0), bx1 - w)
                y0 = min(max(y0, by0), by1 - h)
                best = (9e9, x0, y0, 9e9, 0, 0)
            _, x0, y0, hard, D, soft_ = best
            self.placed.append((lb["eid"], lb["text"], D, hard, soft_))
            if hard > 0:
                self.warn.append("label overlap %s %r (%.0f pt2)" % (lb["eid"], lb["text"], hard))
            if cr > 0 and lb.get("leader", True):
                nx_ = min(max(ax, x0), x0 + w)
                ny_ = min(max(ay, y0), y0 + h)
                dd = math.hypot(nx_ - ax, ny_ - ay)
                if dd > cr + 5:
                    ang_ = math.atan2(ny_ - ay, nx_ - ax)
                    K.leader(s, ax + math.cos(ang_) * (cr + 0.5), ay + math.sin(ang_) * (cr + 0.5), nx_, ny_)
            for i, t in enumerate(lines):
                K.pill_label(s, x0 + 1.7, y0 + 8.6 + i * 10, t, 9, lb["weight"], "start")
            self.occupy(x0, y0, x0 + w, y0 + h)


def is_open(e):
    return e.get("draw") == "open" or (e["status"] == "ILLUSTRATIVE" and e.get("draw") != "fixed")


# ---------------------------------------------------------------------------------------------
# elements
# ---------------------------------------------------------------------------------------------
def draw_zone(c, e):
    s = c.s
    x0, y0, x1, y1 = e["rect"]
    party = e["party"]
    open_ = is_open(e) if e["status"] == "ILLUSTRATIVE" else False
    sides = [b[0] for b in K.band_sides(e["rect"], c.n)]
    K.zone(s, c.X(x0), c.Y(y0), (x1 - x0) * c.sc, (y1 - y0) * c.sc, party, sides, open_)
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
        c.tokens.append((tp, c.X(tx), c.Y(ty)))
        c.occupy(c.X(tx) - 5, c.Y(ty) - 5, c.X(tx) + 5, c.Y(ty) + 5)
    if e.get("depth"):
        at = e.get("dim_at")
        if abs(w - h) < 0.01:     # corner zone: horizontal dimension, label gives both sides
            yy = at if at is not None else y0 + h * 0.72
            dim_line(c, e["id"], c.X(x0), c.Y(yy), c.X(x1), c.Y(yy), e["depth"])
        elif w < h:       # vertical strip: depth is horizontal
            yy = at if at is not None else y0 + h * 0.3
            dim_line(c, e["id"], c.X(x0), c.Y(yy), c.X(x1), c.Y(yy), e["depth"])
        else:
            xx = at if at is not None else x0 + w * 0.3
            dim_line(c, e["id"], c.X(xx), c.Y(y0), c.X(xx), c.Y(y1), e["depth"])


def dim_line(c, eid, x1, y1, x2, y2, label, ticks=3.0, sw=0.8, lp="c", off=0.0, lf=0.5):
    s = c.s
    if off:
        ox, oy = K.dim_offset(s, x1, y1, x2, y2, off * c.sc, ticks, sw)
        x1, y1, x2, y2 = x1 + ox, y1 + oy, x2 + ox, y2 + oy
    else:
        K.dim(s, x1, y1, x2, y2, ticks, sw)
    ang = math.atan2(y2 - y1, x2 - x1)
    mx, my = x1 + (x2 - x1) * lf, y1 + (y2 - y1) * lf
    length = math.hypot(x2 - x1, y2 - y1)
    lines = label.split("\n")
    wlab = max(tw(t, 9, 600) for t in lines)
    own = "dim%d" % len(c.labels)
    if lp == "c" and length >= wlab + 8 and abs(math.sin(ang)) < 0.3:
        c.add_label(eid, label, mx, my, 0, fixed="c", own=own)
    else:
        c.add_label(eid, label, mx, my, 2.5, pref="tbrl" if abs(math.sin(ang)) < 0.5 else "rlbt", own=own)
    n = max(1, int(length // 5))
    for i in range(n + 1):
        qx, qy = x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n
        c.soft.append((qx - 1.6, qy - 1.6, qx + 1.6, qy + 1.6, own))


def feat_path(c, e):
    g = e["g"]
    if e["shape"] == "rect":
        return "rect", (c.X(g[0]), c.Y(g[1]), (g[2] - g[0]) * c.sc, (g[3] - g[1]) * c.sc)
    if e["shape"] == "circle":
        return "circle", (c.X(g[0]), c.Y(g[1]), g[2] * c.sc)
    if e["shape"] == "line":
        return "line", [(c.X(p[0]), c.Y(p[1])) for p in g]
    return "poly", [(c.X(p[0]), c.Y(p[1])) for p in g]


def draw_feature(c, e):
    s = c.s
    open_ = is_open(e)
    t = e.get("terrain", "open")
    sw = e.get("sw", 0.9)
    outline = e.get("outline") != "none"
    kind, p = feat_path(c, e)
    # Open land over a surrounding water/terrain layer must clear that hatch.
    # Opt in per source feature; ordinary room/cavern outlines stay transparent.
    if e.get("knockout"):
        if kind == "rect":
            s.rect(*p, fill=WHITE, stroke=None)
        elif kind == "circle":
            s.circle(*p, fill=WHITE, stroke=None)
        elif kind == "poly":
            s.polygon(p, fill=WHITE, stroke=None)
    if kind == "rect":
        K.terrain_shape(s, t, "rect", p, open_, sw, outline)
        bb = (p[0], p[1], p[0] + p[2], p[1] + p[3])
        c.outline_soft([(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])
    elif kind == "circle":
        K.terrain_shape(s, t, "circle", p, open_, sw, outline)
        bb = (p[0] - p[2], p[1] - p[2], p[0] + p[2], p[1] + p[2])
        c.outline_soft([(p[0] + p[2] * math.cos(a * math.pi / 12), p[1] + p[2] * math.sin(a * math.pi / 12)) for a in range(24)])
    elif kind == "line":
        K.wall_line(s, p, e.get("sw", 2.4))
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        bb = (min(xs), min(ys), max(xs), max(ys))
        c.outline_soft(p, closed=False)
    else:
        K.terrain_shape(s, t, "poly", p, open_, sw, outline)
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        bb = (min(xs), min(ys), max(xs), max(ys))
        c.outline_soft(p)
    e["_bb"] = bb
    if e.get("label"):
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        lp = e.get("lp", "c")
        if lp == "i":
            lines_ = e["label"].split("\n")
            wl = max(tw(t_, 9, 600) for t_ in lines_) + 3.4
            hl_ = len(lines_) * 10 + 1.6
            if wl <= (bb[2] - bb[0]) - 1.5 and hl_ <= (bb[3] - bb[1]) - 1.5:
                c.add_label(e["id"], e["label"], cx, cy, 0, pref="t", fixed=(bb[0] + 1.5, bb[1] + 1.5), weight=600, leader=False)
                return
            lp = "r"
        if e.get("lat"):
            if e.get("lead"):        # label sits in clear space outside a thin piece: leader from the label anchor to a point on the piece
                K.leader(s, c.X(e["lat"][0]), c.Y(e["lat"][1]), c.X(e["lead"][0]), c.Y(e["lead"][1]))
            c.add_label(e["id"], e["label"], c.X(e["lat"][0]), c.Y(e["lat"][1]), 0, pref=lp if lp != "c" else "rltb",
                        fixed="c" if lp == "c" else None, weight=600, leader=False)
            return
        if lp != "c" and (bb[2] - bb[0]) < 40 and (bb[3] - bb[1]) < 40:
            half = max(bb[2] - bb[0], bb[3] - bb[1]) / 2.0
            c.add_label(e["id"], e["label"], cx, cy, half, pref=lp + "rltb", weight=600, leader=True)
            return
        if lp == "t":
            cy = bb[1]
        elif lp == "b":
            cy = bb[3]
        elif lp == "l":
            cx = bb[0]
        elif lp == "r":
            cx = bb[2]
        c.add_label(e["id"], e["label"], cx, cy, 0, pref=lp, fixed="c" if lp == "c" else None, weight=600, leader=False)


def glyph_label(c, e, x, y, radius):
    """Optional explicit label centre moves copy without moving the rules glyph."""
    fixed = None
    if e.get("label_at"):
        lines = e["label"].split("\n")
        w = max(tw(t, 9, 600) for t in lines) + 3.4
        h = len(lines) * 10 + 1.6
        fixed = (c.X(e["label_at"][0]) - w / 2, c.Y(e["label_at"][1]) - h / 2)
    c.add_label(e["id"], e["label"], x, y, radius, pref=e.get("lp", "rltb"), fixed=fixed)


def draw_marker(c, e):
    x, y = c.X(e["at"][0]), c.Y(e["at"][1])
    r = 5.2
    if e.get("on"):
        K.on_piece(c.s, e["on"], x, y, r)
    K.marker(c.s, e["glyph"], x, y, is_open(e), r)
    c.occupy(x - r - 0.5, y - r - 0.5, x + r + 0.5, y + r + 0.5)
    if e.get("label"):
        glyph_label(c, e, x, y, r)


def draw_monster(c, e):
    x, y = c.X(e["at"][0]), c.Y(e["at"][1])
    half = K.monster(c.s, e.get("sz", "M"), x, y, is_open(e), c.sc)
    c.occupy(x - half - 0.5, y - half - 0.5, x + half + 0.5, y + half + 0.5)
    if e.get("label"):
        glyph_label(c, e, x, y, half)


def draw_hero(c, e):
    x, y = c.X(e["at"][0]), c.Y(e["at"][1])
    r = 4.8
    K.hero(c.s, e["party"], x, y, r)
    c.occupy(x - r - 0.5, y - r - 0.5, x + r + 0.5, y + r + 0.5)
    if e.get("label"):
        c.add_label(e["id"], e["label"], x, y, r, pref=e.get("lp", "bltr"))


def draw_unres(c, e):
    """Element the text does not place: always a note under the map with the ? tag; on the board only if `at` is given."""
    if e.get("at"):
        x, y = c.X(e["at"][0]), c.Y(e["at"][1])
        K.unresolved(c.s, x, y)
        c.occupy(x - 6, y - 6, x + 6, y + 6)
        if e.get("label"):
            c.add_label(e["id"], e["label"], x, y, 6, pref=e.get("lp", "rltb"))
    c.notes.append(e["note"])


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


def outline_within(c, sh, d):
    """Dashed outline at distance d (inches, closest point) around a footprint."""
    s = c.s
    if sh[0] == "c":
        K.ring(s, c.X(sh[1]), c.Y(sh[2]), (sh[3] + d) * c.sc, clip="bclip")
        return
    x0, y0, x1, y1 = sh[1:]
    r = d * c.sc
    X0, Y0, X1, Y1 = c.X(x0), c.Y(y0), c.X(x1), c.Y(y1)
    path = ("M%s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 1 %s %s V%s A%s %s 0 0 1 %s %s Z" % (
        f1(X0), f1(Y0 - r), f1(X1), f1(r), f1(r), f1(X1 + r), f1(Y0), f1(Y1), f1(r), f1(r), f1(X1), f1(Y1 + r),
        f1(X0), f1(r), f1(r), f1(X0 - r), f1(Y1), f1(Y0), f1(r), f1(r), f1(X0), f1(Y0 - r)))
    K.ring_path(s, path, clip="bclip")


def target_shape(c, e, to):
    if isinstance(to, list):
        return ("c", to[0], to[1], 0.0)
    return footprint(c.els[to])


def _ring_soft(c, cx, cy, r):
    c.outline_soft([(cx + r * math.cos(a * math.pi / 18), cy + r * math.sin(a * math.pi / 18)) for a in range(36)], step=5.0)


def draw_anno(c, e, a):
    """Annotations (drawn constraint geometry).  Each is also asserted in check_one()."""
    s = c.s
    t = a["t"]
    eid = e["id"]
    me = footprint(e)
    if a.get("hide"):
        return
    if t == "ring":                       # radius ring about a centre/origin point
        ctr = a.get("centre")
        if isinstance(ctr, list):
            cx, cy = ctr
        elif ctr in (None, "self"):
            cx, cy = centre(e)
        else:
            cx, cy = centre(c.els[ctr])
        K.ring(s, c.X(cx), c.Y(cy), a["r"] * c.sc, clip="bclip")
        _ring_soft(c, c.X(cx), c.Y(cy), a["r"] * c.sc)
        if a.get("label"):
            ang = math.radians(a.get("ang", -45))
            lx, ly = c.X(cx) + math.cos(ang) * a["r"] * c.sc, c.Y(cy) + math.sin(ang) * a["r"] * c.sc
            c.add_label(eid, a["label"], lx, ly, 0, pref=a.get("lp", "uvde"), fixed="c")
    elif t == "rel":                      # "within d of" / "at least d from" the target: ring outline or ruler
        tsh = target_shape(c, e, a["of"])
        d = a["d"]
        if a.get("style", "ruler") == "ring":
            outline_within(c, tsh, d)
            if a.get("label"):
                px_, py_ = ray_point(tsh, d, a.get("ang", -45))
                c.add_label(eid, a["label"], c.X(px_), c.Y(py_), 0, pref=a.get("lp", "uvde"), fixed="c")
        else:                              # ruler: a segment of exactly d from the reference toward this element
            p1, p2 = closest_points(tsh, me)
            ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) if p1 != p2 else math.radians(a.get("ang", 0))
            if "ang" in a:
                ang = math.radians(a["ang"])
                p1 = ray_point(tsh, 0.0, a["ang"])
            q2 = (p1[0] + math.cos(ang) * d, p1[1] + math.sin(ang) * d)
            dim_line(c, eid, c.X(p1[0]), c.Y(p1[1]), c.X(q2[0]), c.Y(q2[1]), a["label"], lp=a.get("lp", "c"), ticks=2.6, off=a.get("off", 0), lf=a.get("lf", 0.5))
    elif t == "edgein":                   # distance d measured inward from the boundary of a circular feature
        tsh = footprint(c.els[a["of"]])
        cx, cy = tsh[1], tsh[2]
        mx, my = centre(e)
        ang = math.atan2(my - cy, mx - cx)
        p1 = (cx + math.cos(ang) * tsh[3], cy + math.sin(ang) * tsh[3])
        q2 = (p1[0] - math.cos(ang) * a["d"], p1[1] - math.sin(ang) * a["d"])
        dim_line(c, eid, c.X(p1[0]), c.Y(p1[1]), c.X(q2[0]), c.Y(q2[1]), a["label"], lp=a.get("lp", "c"), ticks=2.6, off=a.get("off", 0))
    elif t == "pdim":                     # dimension between two Hero footprints (1" tokens) given as points
        pa = ("c", a["p"][0], a["p"][1], 0.5)
        pb = ("c", a["q"][0], a["q"][1], 0.5)
        p1, p2 = closest_points(pa, pb)
        dim_line(c, eid, c.X(p1[0]), c.Y(p1[1]), c.X(p2[0]), c.Y(p2[1]), a["label"], lp=a.get("lp", "c"), ticks=2.6, off=a.get("off", 0))
    elif t == "cdim":                     # dimension between two points (centre to centre)
        dim_line(c, eid, c.X(a["p"][0]), c.Y(a["p"][1]), c.X(a["q"][0]), c.Y(a["q"][1]), a["label"], lp=a.get("lp", "c"), ticks=2.6, off=a.get("off", 0))
    elif t == "dim":                      # dimension between closest points of two things (the actual drawn gap)
        tsh = target_shape(c, e, a["to"])
        p1, p2 = closest_points(me, tsh)
        dim_line(c, eid, c.X(p1[0]), c.Y(p1[1]), c.X(p2[0]), c.Y(p2[1]), a["label"], lp=a.get("lp", "c"), off=a.get("off", 0))
    elif t in ("inside", "adj", "cring"):
        pass
    else:
        raise ValueError(t)


def draw_edge(c, e):
    s = c.s
    mode = e["mode"]
    edges = e.get("edges") or [e["edge"]]
    L = 15.0
    n = c.n
    for ed in edges:
        pos = e.get("pos", n / 2)
        if ed == "N":
            x, y, dx, dy = c.X(pos), c.Y(0), 0, 1
        elif ed == "S":
            x, y, dx, dy = c.X(pos), c.Y(n), 0, -1
        elif ed == "W":
            x, y, dx, dy = c.X(0), c.Y(pos), 1, 0
        else:
            x, y, dx, dy = c.X(n), c.Y(pos), -1, 0
        if mode == "arrive":
            x1, y1, x2, y2 = x, y, x + dx * L, y + dy * L
        else:        # exit: arrow ends at the edge
            x1, y1, x2, y2 = x + dx * L, y + dy * L, x, y
        K.edge_arrow(s, x1, y1, x2, y2, mode, is_open(e))
        c.occupy(min(x1, x2) - 2, min(y1, y2) - 2, max(x1, x2) + 2, max(y1, y2) + 2)
        if e.get("label") and (ed == edges[0] or e.get("label_all")):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            c.add_label(e["id"], e["label"], mx, my, 4, pref=e.get("lp", "rltb"))


def draw_title(c):
    sp = c.sp
    s = c.s
    n = c.n
    dims = '%d"×%d"' % (n, n)
    if sp.get("title_mode", "full") == "full":
        s.text(c.bx, 10.2, sp["tag"], 9, 700)
        w = tw(sp["tag"], 9, 700)
        s.text(c.bx + w + 5, 10.2, "·  " + dims, 9, 400)
    else:
        s.text(c.bx, 10.2, dims, 9, 400)
    c.inches.append(('%d"' % n, "board"))
    ax = c.bx + c.bs - 5
    K.compass(s, ax)
    L = 6 * c.sc
    K.scale_bar(s, ax - 20.5 - (L + 4 + tw('6"', 9, 400)), 10.2, c.sc, 6, '6"')
    s.text(c.bx - 4, c.Y(n / 2) + 3.4, "W", 9, 700, "end")
    s.text(c.bx + c.bs + 4, c.Y(n / 2) + 3.4, "E", 9, 700, "start")


def draw_footer(c):
    s = c.s
    s.text(c.bx + c.bs + 4, c.by + c.bs + 9, "S", 9, 700, "start")
    y = c.by + c.bs + 11
    fw = c.width - 24
    for ln in foot_lines_impl(c):
        for sub in wrap(ln, fw, 9, 400):
            s.text(6, y, sub, 9, 400)
            y += 10.4
    for note in c.notes:
        K.unresolved(s, 6 + 6.2, y - 3)
        lines = wrap(note, fw - 6, 9, 400)
        for sub in lines:
            s.text(6 + 16, y, sub, 9, 400)
            y += 10.4
    return y


def foot_lines_impl(c):
    out = []
    sp = c.sp
    if c.illus:
        out.append(sp.get("std_note", "Schematic. " + NOTE_STD + "."))
    else:
        out.append("Schematic.")
    for t in sp.get("foot", []):
        out.append(t["text"])
        for v in inch_tokens(t["text"]):
            c.inches.append((v + '"', "foot:" + t["text"][:20]))
    return out


ORDER = {"zone": 0, "feature": 1, "edgeband": 1, "marker": 3, "monster": 4, "edge": 5}


def draw_map(sp, width=COL_W, bx=None, by=14.0):
    c = Ctx(sp, width, bx, by)
    s = c.s
    c.illus = any(e["status"] == "ILLUSTRATIVE" or e.get("draw") == "open" for e in sp["elements"])
    s.rect(c.bx, c.by, c.bs, c.bs, fill=WHITE, stroke=INK, sw=1.3)
    for e in sp["elements"]:
        if e["kind"] == "zone":
            draw_zone(c, e)
    for e in sp["elements"]:
        if e["kind"] in ("feature", "edgeband"):
            draw_feature(c, e)
    for e in sp["elements"]:
        for a in e.get("anno", []):
            if a["t"] == "ring":
                draw_anno(c, e, a)
    for e in sp["elements"]:
        for a in e.get("anno", []):
            if a["t"] != "ring":
                draw_anno(c, e, a)
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
        K.hero(s, party, tx, ty, 4.4)
    for e in sp["elements"]:
        if e["kind"] == "hero":
            draw_hero(c, e)
    for e in sp["elements"]:
        if e["kind"] == "unresolved":
            draw_unres(c, e)
    c.place_labels()
    draw_title(c)
    yend = draw_footer(c)
    c.height = yend + 2
    return c, yend + 2


fig_audit = {}
FIRST_MAP_FIG = 21
LEGEND_FIG = "FIG-20"
LEGEND_ANCHOR_LINE = 12017
TEMPLATE_ANCHOR_LINE = 11105
LEGEND_LINES = [600, 602, 604, 610, 624, 625, 11078, 11099, 11101, 11111, 11115]
TEMPLATE_LINES = [598, 600, 602, 604, 610, 11105, 11111, 11112, 11114, 11115, 11116]
SHARED_OK = list(range(11072, 11120)) + list(range(14922, 15019)) + [11027, 598, 596]


def build_fig(key):
    sp = spec()["scenarios"][key]
    c, h = draw_map(sp)
    fig_audit[key] = c
    return c.s, h


def embed_map(s, sp, x, y, width, bx=None, by=14.0):
    """Draw an Appendix map into the composite figure svg `s` at offset (x, y); returns (ctx, height)."""
    c, h = draw_map(sp, width, bx, by)
    s.raw('<g transform="translate(%s %s)">' % (f1(x), f1(y)))
    s.body.extend(c.s.body)
    s.raw("</g>")
    s.defs.extend(c.s.defs)
    return c, h


# ---------------------------------------------------------------------------------------------
# FIG-20: the shared key (full width), one swatch per registry entry
# ---------------------------------------------------------------------------------------------
KEY_COLS = [
    ("Parties and zones", ["hero-A", "hero-B", "zone-A", "zone-B", "zone-AB", "compass", "scale", "illus", "leader"]),
    ("Markers, Monsters, steps", ["obj", "chest", "haz", "mk", "mon", "mon-L", "mon-H", "step", "los"]),
    ("Terrain", ["ter-blocking", "ter-impassable", "ter-cover", "ter-difficult", "ter-coverdiff", "ter-water", "ter-slippery",
                 "ter-obstacle", "ter-hazard", "ter-shade", "ter-chasm"]),
    ("Pieces, lines, status", ["line-wall", "ter-open", "ledge", "ledge-crumbling", "dim", "ring", "range", "arr-exit",
                               "arr-arrive", "ter-excl"]),
]


def key_ids():
    return [g for _, ids in KEY_COLS for g in ids]


def _legend_col(s, x, y, title, ids, width, audit):
    s.text(x, y, title, 9.5, 700)
    y += 7
    for gid in ids:
        text = K.REG[gid]["label"]
        lines = wrap(text, width - 36, 9)
        h = max(15, len(lines) * 10.4 + 4)
        if gid == "mon-L":
            h = max(h, 22)
        elif gid == "mon-H":
            h = max(h, 28)
        K.swatch(s, gid, x, y + h / 2)
        for k, ln in enumerate(lines):
            s.text(x + 36, y + 7.6 + k * 10.4 + (h - len(lines) * 10.4) / 2 - 1, ln, 9)
        audit.append(text)
        y += h
    return y


def fig20():
    s = MapSvg(FULL_W)
    audit = []
    s.text(0, 10, "Key to the setup and deployment diagrams", 10.5, 700)
    cw = 122
    xs = [0, 127, 254, 381]
    yend = 0
    for (title, ids), x in zip(KEY_COLS, xs):
        yy = _legend_col(s, x, 28, title, ids, cw, audit)
        yend = max(yend, yy)
    y = yend + 8
    s.line(0, y - 3, FULL_W, y - 3, INK, 0.6)
    notes = [
        "**Orientation.** North is drawn at the top. The Setup Roll-off winner designates the North edge before setup; North and South are the short battlefield edges and East and West the long ones, even on a square battlefield (10.1).",
        "**Scale and measurement.** The battlefield, zones and stated distances are drawn to scale; markers are enlarged, and Large and Huge Monsters use 2\"×2\" and 3\"×3\" footprints. **Tabletop:** measure between closest points, except from a point or origin where specified. **Grid:** apply 2.6 to occupied squares and terrain; use shortest grid distances at 1\" orthogonally and 1.5\" diagonally unless a rule says otherwise.",
        "**Counts and labels.** Scattered terrain is drawn as a few representative pieces; the printed counts and the 10.6 scaling stay in the scenario text. G1, G2 and so on are Monster Group numbers. A means Awake; R means Resting. R2, R3 and R4 beside arrival arrows mean arrival at the start of that round. Hidden contents (face-down markers) are never drawn.",
        "**Solid and dashed.** A solid marker or zone with a distance symbol is one position that meets the printed limit; only the battlefield, zone depths and stated distances are exact. Grey dashed pieces show one legal arrangement of something the rules leave open. Letters A and B name the drawn zones; where a scenario assigns the parties by die roll, the zones do not say who is which.",
        "**Where a scenario is silent**, 10.1 steps 7 and 11 apply: the Setup Roll-off winner chooses the edge or corner zone and the other party takes the opposite one; zones are 6\" deep or 8\"×8\" corners, marked \"(default)\" on a map, and parties alternate placing Heroes, starting with the party that lost the Roll-off.",
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
    ("**Place Terrain.** Determine deployment zones first (scenario instructions; otherwise the Roll-off winner chooses opposite edges or corners). Defaults: 6\" deep or 8\"×8\" corners. Alternate remaining major terrain, Roll-off loser first. Unless overridden, alternately placed Blocking or Impassable Terrain cannot be inside a zone; Blocking pieces must be more than 2\" apart.", True),
    ("Place Objectives and Markers.", False),
    ("Generate and Place Monsters.", False),
    ("Assign Guard Points.", False),
    ("**Deploy the Parties** in the zones determined in step 7. Follow scenario instructions; otherwise alternate placing Heroes, the Roll-off loser first.", True),
    ("Begin Round 1 with the Initiative Phase.", False),
]
ST = 3.3                     # template pt per inch


def template_geometry():
    """Step 7 deployment zones; no obsolete edge or zone clearance bands."""
    return dict(edge_margin=0.0, clear=0.0, depth=6.0, corner=8.0,
                edge_rect=(6.0, 0.0, 30.0, 36.0))


def _tpl_board(s, ox, oy, variant, audit):
    g = template_geometry()
    bs = 36 * ST
    s.rect(ox, oy, bs, bs, fill=WHITE, stroke=None)
    if variant == "edge":
        zones = [("A", (0, 0, g["depth"], 36)), ("B", (36 - g["depth"], 0, 36, 36))]
    else:
        c_ = g["corner"]
        zones = [("A", (0, 0, c_, c_)), ("B", (36 - c_, 36 - c_, 36, 36))]
    s.rect(ox, oy, bs, bs, fill="none", stroke=INK, sw=1.2)
    for party, (x0, y0, x1, y1) in zones:
        sides = [b[0] for b in K.band_sides((x0, y0, x1, y1), 36)]
        K.zone(s, ox + x0 * ST, oy + y0 * ST, (x1 - x0) * ST, (y1 - y0) * ST, party, sides, fill=PAT["aoe"])
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if variant == "edge":
            for f in (0.2, 0.5, 0.8):
                K.hero(s, party, ox + cx * ST, oy + (y0 + (y1 - y0) * f) * ST, 3.6)
        else:
            K.hero(s, party, ox + (x0 + 2.6) * ST, oy + (y0 + 2.6) * ST, 3.6)
            K.hero(s, party, ox + (x1 - 2.6) * ST, oy + (y1 - 2.6) * ST, 3.6)
    if variant == "edge":
        K.dim_labeled(s, ox, oy + 12.6 * ST, ox + 6 * ST, oy + 12.6 * ST, '6"')
        audit += ['6"']
    else:
        K.dim_labeled(s, ox, oy + 9.5 * ST, ox + 8 * ST, oy + 9.5 * ST, '8"')
        audit += ['8"']
    return bs


def fig57():
    s = MapSvg(FULL_W)
    audit = []
    g = template_geometry()
    assert g["depth"] == 6 and g["corner"] == 8 and g["clear"] == 0
    s.text(0, 10, "10.1 Preparation Steps", 10.5, 700)
    fw = 214
    y = 22
    for i, (txt, hot) in enumerate(TPL_STEPS, 1):
        lines = wrap(txt, fw - 24, 9)
        h = max(15, len(lines) * 10.4 + 4)
        if hot:
            s.rect(0, y - 1, fw, h + 1, fill=PALE, stroke=INK, sw=0.9, rx=2)
        K.step(s, 9.5, y + h / 2, i, 6.6)
        for k, ln in enumerate(lines):
            s.text(22, y + 8.2 + k * 10.4 + (h - len(lines) * 10.4) / 2 - 1, ln, 9)
        audit.append(txt)
        if i < len(TPL_STEPS):
            s.line(9.5, y + h / 2 + 6.8, 9.5, y + h + 3.6, INK, 1.0)
        y += h + 4
    yflow = y
    rx = 232
    box_w = FULL_W - rx
    s.rect(rx, 6, box_w, 17, fill=WHITE, stroke=INK, sw=1.2, rx=2)
    s.text(rx + box_w / 2, 18.2, "Template - not a fixed battlefield", 10, 700, "middle")
    bw = 36 * ST
    gap = 14
    ox1, ox2 = rx + 6, rx + 6 + bw + gap
    s.text(rx, 34, "Deployment zones determined before terrain.", 9, 600)
    oy = 58
    s.text(ox1, 50.8, "Step 7 default: edge zones", 9, 700)
    s.text(ox2, 50.8, "Step 7 default: corner zones", 9, 700)
    _tpl_board(s, ox1, oy, "edge", audit)
    _tpl_board(s, ox2, oy, "corner", audit)
    yb = oy + bw + 12
    t1 = "Zones are 6\" deep. The other pair of opposite edges works the same way."
    t2 = "Corner zones are 8\"×8\"; the second zone is diagonally opposite."
    ya = s.para(ox1, yb, t1, bw + 6, 9, 400, lead=10.4)
    yb2 = s.para(ox2, yb, t2, bw + 6, 9, 400, lead=10.4)
    audit += [t1, t2]
    yk = max(ya, yb2) + 6
    yk = K.key_strip(s, ["zone-A", "zone-B", "hero-A", "hero-B", "dim"], rx, yk, box_w, title=None) + 2
    yk = s.para(rx, yk + 7, "Hatched zones: alternately placed Blocking or Impassable Terrain cannot be inside these zones unless the scenario says otherwise. Required scenario terrain follows its printed instructions.", box_w, 9, 400, lead=10.4) - 3
    nt = "**Tabletop:** Unless the scenario says otherwise, alternately placed Blocking Terrain must be more than 2\" from all other Blocking Terrain, measured between nearest edges. **Grid:** The same restriction is more than 2 squares. No general battlefield-edge or deployment-zone clearance band applies."
    ye = s.para(rx, yk + 14, nt, box_w, 9, 400, lead=10.4)
    audit += [nt]
    fig57.audit = audit
    return s, max(yflow, ye) + 4


# ---------------------------------------------------------------------------------------------
# metadata for figdata (manifest and placements)
# ---------------------------------------------------------------------------------------------
def scenario_order():
    spans = scenario_spans()
    return sorted(spans, key=lambda k: spans[k][0])


STATUS_KEYS = {"MANDATORY_POSITION": "mandatory", "CONSTRAINED": "constrained", "ILLUSTRATIVE": "illustrative",
               "UNRESOLVED": "unresolved"}


def meta_entries():
    spans = scenario_spans()
    sc = spec()["scenarios"]
    out = {}
    out[LEGEND_FIG] = dict(
        title="Key to the setup and deployment diagrams",
        purpose="One shared key for every setup and deployment diagram (the deployment patterns, the Chasm Crossing and Whispering Grove details, the Appendix A and B maps and the 36 Core Scenario maps): one swatch per glyph, pattern, line type and status convention, drawn by the same functions as the diagrams.",
        source_refs=["10.1 Random Direction and Battlefield Edges (11099-11101)", "10.1 Setup Roll-off (11078) and Preparation Steps, steps 7 and 11 (11111, 11115)",
                     "2.6 Measurement (598-608) and Size and Footprints (622-623)", "2.9.1 Terrain Types (836-882)"],
        geometry_spec="Four columns of swatches (parties and zones; markers, Monsters and steps; terrain; pieces, distances, edges and status), %d entries, one per glyph id in scenkit.REG, above five short notes on orientation, scale, counts and labels, solid and dashed, and the steps 7 and 11 default; no board geometry beyond the swatches. make_figures checks that every glyph and pattern id emitted by any setup diagram appears here." % len(key_ids()),
        caption="Key to the setup and deployment diagrams: symbols for Heroes, zones, markers, Monster Groups, terrain, distances and edges, with the orientation, scale and grey-dashed conventions every such diagram follows (see 10.4).",
        insert_after="B%05d" % LEGEND_ANCHOR_LINE, scope="full", schematic=False,
        semantic_check="Swatches are drawn by the same shared glyph functions as the diagrams; printed inch values are checked against lines 598-608, 622-623 and 11115; North/short/long edge naming against 11099-11101; paired Tabletop/Grid measurements against 598-608. The registry check proves the key covers every id used on FIG-13 to FIG-16 and FIG-18 to FIG-57.",
        ambiguity="None in the key. Terrain pieces whose type the scenario leaves to 2.9.1 ('Impassable or Blocking') use a neutral grey swatch rather than either type.",
        new_figure=True)
    for key in scenario_order():
        sp = sc[key]
        hl, end, cno, sno, title, climate = spans[key]
        cnt = dict.fromkeys(STATUS_KEYS.values(), 0)
        for e in sp["elements"]:
            cnt[STATUS_KEYS[e["status"]]] += 1
        refs = ["10.4 %s Scenario %d: %s (source lines %d-%d)" % (climate, sno, title, hl, end),
                "10.1 Preparation Steps, steps 7 and 11 (11111, 11115)" if any(11115 in e.get("shared", []) for e in sp["elements"]) else "10.1 Preparation Steps (11103-11116)"]
        out[sp["fig"]] = dict(
            title="%s Scenario %d: %s, deployment map" % (climate, sno, title),
            purpose="Column-width top-down map of the setup for %s %d: battlefield, both deployment zones with depth, objectives and markers, required terrain, Monster placement and any entry or exit edges, using only values the scenario states and the shared symbols of FIG-20." % (climate, sno),
            source_refs=refs,
            geometry_spec="36\"x36\" battlefield at 6 pt per inch (zones and stated distances to scale; markers enlarged; Large and Huge Monsters at footprint scale), drawn with the shared glyph set of FIG-20. %d mandatory, %d constrained and %d illustrative elements, each citing its source lines in scenario_specs.json; illustrative elements are grey dashed." % (cnt["mandatory"], cnt["constrained"], cnt["illustrative"]) + ("" if not cnt["unresolved"] else " %d unresolved elements carry a ? tag and a note." % cnt["unresolved"]),
            caption=sp["caption"],
            insert_after="B%05d" % sp["insert_after_line"], scope="column", schematic=True,
            semantic_check="Each element's source lines lie inside lines %d-%d; every printed inch value is found in its cited lines; distances, containments and 'at least' / 'within' relations are asserted in make_figures.selfcheck (check_scenmaps); zones, markers and Blocking or Impassable pieces are checked against the 10.1 step 7 and step 8 distances; every glyph and pattern emitted is listed in FIG-20." % (hl, end),
            ambiguity=("; ".join(sp["ambiguities"]) if sp["ambiguities"] else "None affecting the drawing. Positions the source leaves open are drawn as one legal arrangement in grey dashes."),
            new_figure=True)
    out["FIG-%d" % (FIRST_MAP_FIG + 36)] = dict(
        title="10.1 Preparation Steps: procedural template",
        purpose="Template of the twelve Preparation Steps, zones determined at step 7, terrain placement restrictions, and deployment at step 11.",
        source_refs=["10.1 Preparation Steps, steps 1-12 (11105-11116)", "2.6 Measurement (596-608)"],
        geometry_spec="Twelve numbered steps; two 36-inch boards at 3.3 pt per inch with 6-inch edge zones or 8-inch corner zones hatched. No obsolete battlefield-edge or zone-clearance bands. Text states Blocking spacing more than 2 inches (Grid: more than 2 squares).",
        caption="Template, not a fixed battlefield: twelve Preparation Steps, step 7 default zones and terrain restrictions, and step 11 deployment; key: FIG-20 (see 10.1).",
        insert_after="B%05d" % TEMPLATE_ANCHOR_LINE, scope="full", schematic=True,
        semantic_check="Compared with RC512 lines 11105-11116: determine zones at step 7, 6-inch edge or 8-inch corner defaults, alternately placed Blocking/Impassable outside zones, Blocking spacing more than 2 inches (Grid: more than 2 squares), and alternate Hero placement at step 11. Geometry asserts default depths and absence of former clearance bands.",
        ambiguity="None. Which edge pair or corner pair is used is chosen by the Setup Roll-off winner; the figure shows one example of each and says so.",
        new_figure=True)
    return out


# ---------------------------------------------------------------------------------------------
# checks (called from make_figures.selfcheck)
# ---------------------------------------------------------------------------------------------
KINDS = {"zone", "feature", "marker", "monster", "edge", "hero", "unresolved"}
LEGEND_TERRAIN = set(K.TERRAIN_KINDS)
STATUSES = {"MANDATORY_POSITION", "CONSTRAINED", "ILLUSTRATIVE", "UNRESOLVED"}
TOL = 0.06


def _text_of(lines):
    return cited_text(lines)


# 2.9.1 standard assignments (source lines 853-876) for the named terrain pieces the maps draw.  A piece is named by its label
# (or, if unlabelled, by the labelled sibling with the same id letters, e.g. tr2 -> tr1).  Types the scenario states itself
# (Mother Tree, Barrow, Tent, Towers, Colossus, Dais, Collapsed edges, Heated ground, Ravine floor, Beams ...) carry no entry here.
TERRAIN_2_9_1 = [
    # (label keyword, allowed drawn terrain kinds, 2.9.1 row)
    ("fallen pillar", {"impassable"}, "fallen pillars: Impassable"),
    ("tree", {"cover"}, "tree areas: Cover"), ("thicket", {"cover"}, "thickets: Cover"), ("palm", {"cover"}, "trees: Cover"),
    ("razor reeds", {"cover"}, "reeds: Cover"), ("reeds", {"cover"}, "reeds: Cover"), ("mangroves", {"cover"}, "mangroves: Cover"),
    ("reed screen", {"coverdiff"}, "reed screens: Cover + Difficult"), ("curtain", {"cover"}, "scenario: Cover"),
    ("camp", {"cover"}, "scenario: Cover"),
    ("undergrowth", {"coverdiff"}, "undergrowth: Cover + Difficult"), ("rubble", {"coverdiff"}, "rubble fields: Cover + Difficult"),
    ("debris", {"coverdiff"}, "debris fields: Cover + Difficult"), ("dune", {"coverdiff"}, "dunes: Cover + Difficult"),
    ("outcrop", {"coverdiff"}, "rocky outcrops: Cover + Difficult"), ("thorny vines", {"coverdiff"}, "scenario: Cover + Difficult"),
    ("deep sand", {"difficult"}, "deep sand: Open + Difficult"), ("deep mud", {"difficult"}, "mud: Open + Difficult"), ("muck", {"difficult"}, "muck: Open + Difficult"),
    ("workbench", {"impassable"}, "workbenches: Impassable"), ("low wall", {"impassable"}, "low walls: Impassable"),
    ("ice barricade", {"impassable"}, "scenario: Impassable"), ("barricade", {"impassable"}, "barricades: Impassable"),
    ("altar", {"impassable"}, "altars: Impassable"), ("column", {"impassable"}, "broken columns: Impassable"),
    ("statue", {"impassable"}, "statue bases: Impassable"), ("statuary", {"impassable"}, "statue bases: Impassable"),
    ("cart or wall", {"impassable"}, "scenario Basic Mode: Impassable"),
    ("shelves", {"obstacle"}, "shelving: Impassable or Blocking"), ("stalagmite", {"obstacle"}, "stalagmites: Impassable or Blocking"),
    ("rocks", {"obstacle"}, "boulders: Impassable or Blocking"),
    ("ice wall", {"blocking"}, "wall sections: Blocking"), ("cave wall", {"blocking"}, "cave walls: Blocking"),
    ("building", {"blocking"}, "building footprints: Blocking"), ("ruin", {"blocking"}, "ruins: Blocking"),
    ("pillar", {"blocking"}, "standing pillars: Blocking"), ("wall", {"blocking"}, "wall sections: Blocking"),
    ("cracked ice", {"slippery"}, "scenario: Slippery"), ("shallow", {"water"}, "Shallow Water"),
]


def terrain_name(sp, e):
    lab = e.get("label")
    if not lab:
        import re as _re
        pre = _re.sub(r"[^a-zA-Z_].*$", "", e["id"]).rstrip("_")
        for o in sp["elements"]:
            if o is not e and o.get("label") and o["kind"] == "feature" and _re.sub(r"[^a-zA-Z_].*$", "", o["id"]).rstrip("_") == pre:
                lab = o["label"]
                break
    return lab


def check_terrain_types(key, sp, errs):
    """Every named terrain piece must be drawn with the type 2.9.1 assigns to it (unless the scenario types it: flag typed_by_scenario)."""
    for e in sp["elements"]:
        if e["kind"] != "feature" or e.get("typed_by_scenario"):
            continue
        lab = terrain_name(sp, e)
        if not lab:
            continue
        low = lab.lower()
        for kw, kinds, row in TERRAIN_2_9_1:
            if re.match(re.escape(kw) + r"\b", low) or (" " in kw and kw in low):
                if e.get("terrain", "open") not in kinds:
                    errs.append("%s/%s: %r drawn as %s but 2.9.1 gives %s (%s)" % (key, e["id"], lab, e.get("terrain", "open"), sorted(kinds), row))
                break


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
            if ctr in (None, "self"):
                continue
            cx, cy = ctr if isinstance(ctr, list) else centre(els[ctr])
            my = centre(e)
            dd = math.hypot(my[0] - cx, my[1] - cy)
            rel = a.get("rel", "eq")
            if rel == "eq" and abs(dd - a["r"]) > TOL + 0.01:
                errs.append("%s: centre distance %.2f is not %s" % (tag, dd, a["r"]))
        elif t == "cring":                     # centre-to-centre distance from a point lies in [lo, hi]
            cx, cy = a["centre"]
            my = centre(e)
            dd = math.hypot(my[0] - cx, my[1] - cy)
            if dd < a["lo"] - TOL or dd > a["hi"] + TOL:
                errs.append("%s: centre distance %.2f outside %s-%s" % (tag, dd, a["lo"], a["hi"]))
        elif t == "cdim":
            dd = math.hypot(a["p"][0] - a["q"][0], a["p"][1] - a["q"][1])
            if abs(dd - a["d"]) > TOL:
                errs.append("%s: centre distance %.2f is not %s" % (tag, dd, a["d"]))
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


def check_one(key, sp, spans, errs, L, width=COL_W):
    """Checks for one map spec.  spans: list of (first, last) source line ranges the spec may cite."""
    def in_span(n):
        return any(a <= n <= b for a, b in spans)
    n = sp.get("board_in", 36)
    if not any(in_span(sp["insert_after_line"]) for _ in (0,)):
        errs.append("%s: insertion line outside the scenario" % key)
    if not in_span(sp["board_line"]) or '%d"×%d"' % (n, n) not in L[sp["board_line"] - 1]:
        errs.append("%s: board_line does not state %d\"x%d\"" % (key, n, n))
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
        if (e["kind"] == "unresolved") != (e["status"] == "UNRESOLVED"):
            errs.append("%s: kind unresolved and status UNRESOLVED go together" % tag)
        if not e["lines"]:
            errs.append("%s: no source lines" % tag)
        for ln in e["lines"]:
            if not in_span(ln):
                errs.append("%s: line %d outside the cited spans %s" % (tag, ln, spans))
        for ln in e.get("shared", []):
            if ln not in SHARED_OK:
                errs.append("%s: shared line %d is not a 10.1 / 10.6 rule line" % (tag, ln))
        if e["kind"] == "zone":
            zones.append(e)
        if e["kind"] == "feature" and e.get("terrain", "open") not in LEGEND_TERRAIN:
            errs.append("%s: terrain %s has no legend swatch" % (tag, e.get("terrain")))
        if e["kind"] == "marker" and e["glyph"] not in ("obj", "chest", "haz", "mk"):
            errs.append("%s: glyph %s" % (tag, e["glyph"]))
        if e["kind"] == "marker" and e.get("on") and e["on"] not in LEGEND_TERRAIN:
            errs.append("%s: on-terrain %s" % (tag, e["on"]))
        if e["kind"] == "edge" and e["mode"] == "arrive" and "midpoint" in _text_of(e["lines"]) and e.get("pos") != n / 2:
            errs.append("%s: arrival at an edge midpoint must be drawn at %s\"" % (tag, n / 2))
        if e.get("guards"):      # "guarding the item nearest the battlefield centre" (13994): drawn beside that item, and it must be the nearest
            g = e["guards"]
            cand = {i: next(x for x in sp["elements"] if x["id"] == i) for i in g["among"]}
            near = min(cand, key=lambda i: math.hypot(cand[i]["at"][0] - n / 2, cand[i]["at"][1] - n / 2))
            if near != g["of"]:
                errs.append("%s: guarded item %s is not the one nearest the battlefield centre (%s)" % (tag, g["of"], near))
            tx, ty = cand[g["of"]]["at"]
            if math.hypot(e["at"][0] - tx, e["at"][1] - ty) > 2.0:
                errs.append("%s: Monster is not drawn beside the item it guards" % tag)
            if any(math.hypot(e["at"][0] - c_["at"][0], e["at"][1] - c_["at"][1]) < math.hypot(e["at"][0] - tx, e["at"][1] - ty) for i, c_ in cand.items() if i != g["of"]):
                errs.append("%s: Monster is nearer another item than the one it guards" % tag)
        if e["kind"] == "unresolved" and not e.get("note"):
            errs.append("%s: unresolved element without a note" % tag)
    for t in sp.get("foot", []):
        for ln in t["lines"]:
            if not in_span(ln):
                errs.append("%s: foot line %d outside" % (key, ln))
    for u in sp.get("undrawn", []):
        for ln in u["lines"]:
            if not in_span(ln):
                errs.append("%s: undrawn line %d outside" % (key, ln))
    spc = json.loads(json.dumps(sp))
    c, h = draw_map(spc, width)
    if h > sp.get("max_height", 275):
        errs.append("%s: map height %.0f pt exceeds the allowed height" % (key, h))
    for w in c.warn:
        if float(w.rsplit("(", 1)[1].split(" ")[0]) > 6:
            errs.append("%s: %s" % (key, w))
    els = {e["id"]: e for e in sp["elements"]}
    for (tok, eid) in c.inches:
        if eid == "board":
            txt = _text_of([sp["board_line"]])
        elif eid.startswith("foot:"):
            txt = _text_of([ln for t in sp["foot"] if t["text"].startswith(eid[5:]) for ln in t["lines"]])
        else:
            e = els[eid]
            txt = _text_of(e["lines"] + e.get("shared", []))
        if tok not in txt:
            errs.append("%s/%s: printed %s not found in cited source lines" % (key, eid, tok))
    for e in sp["elements"]:
        _anno_checks(sp, e, errs, key)
    check_terrain_types(key, sp, errs)
    for e in sp["elements"]:
        for note_key in ("note",):
            if note_key in e:
                for v in inch_tokens(e[note_key]):
                    if v + '"' not in _text_of(e["lines"]):
                        errs.append("%s/%s: printed %s\" in note not found in cited lines" % (key, e["id"], v))
    zshapes = [footprint(z) for z in zones]
    for e in sp["elements"]:
        tag = "%s/%s" % (key, e["id"])
        fp = footprint(e) if e["kind"] not in ("edge", "unresolved") else None
        if fp is not None:
            for v in (fp[1], fp[2]) if fp[0] == "c" else (fp[1], fp[2], fp[3], fp[4]):
                if v < -0.01 or v > n + 0.01:
                    errs.append("%s: footprint outside the %d\"x%d\" battlefield" % (tag, n, n))
                    break
        if e["kind"] in ("marker", "monster") and not e.get("zone_ok"):
            for z, zs in zip(zones, zshapes):
                if shape_dist(fp, zs) < 0.01:
                    errs.append("%s: marker or Monster inside deployment zone %s (10.1 step 8)" % (tag, z["id"]))
        if e["kind"] == "feature" and e.get("terrain") in ("blocking", "impassable", "obstacle") and not e.get("exempt") and sp.get("step7", True):
            for z, zs in zip(zones, zshapes):
                if shape_dist(fp, zs) < 0.01:
                    errs.append("%s: alternately placed Blocking/Impassable piece inside zone %s (10.1 step 7)" % (tag, z["id"]))
            if e.get("terrain") == "blocking" and not e.get("typed_by_scenario"):
                for other in sp["elements"]:
                    if other["id"] != e["id"] and other["kind"] == "feature" and other.get("terrain") == "blocking":
                        if shape_dist(fp, footprint(other)) <= 2 + 0.01:
                            errs.append("%s: alternately placed Blocking piece not more than 2 inches from %s (10.1 step 7)" % (tag, other["id"]))
        if e["kind"] == "zone":
            for tk in e.get("tokens") or []:
                if not (e["rect"][0] <= tk[0] <= e["rect"][2] and e["rect"][1] <= tk[1] <= e["rect"][3]):
                    errs.append("%s: Hero token outside its zone" % tag)
        if e["kind"] == "hero":
            ok = False
            for z in zones:
                if z["party"] in (e["party"], "AB"):
                    r = z["rect"]
                    if r[0] - 0.51 <= e["at"][0] <= r[2] + 0.51 and r[1] - 0.51 <= e["at"][1] <= r[3] + 0.51:
                        ok = True
            if not ok:
                errs.append("%s: Hero not in (or at the edge of) a zone of its party" % tag)
    return c


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
        if sp["tag"] != key:
            errs.append("%s: tag %r" % (key, sp["tag"]))
        hl, end = spans[key][0], spans[key][1]
        check_one(key, sp, [(hl, end)], errs, L)
        if not re.search(r"; key: FIG-20 \(see [^)]+\)\.$", sp["caption"]):
            errs.append("%s: caption must end with '; key: FIG-20 (see ...).'" % key)
    for akey, sp in spec().get("appendix", {}).items():
        check_one("Appendix " + akey, sp, [tuple(r) for r in sp["spans"]], errs, L, width=sp.get("check_width", 192))
        for e in sp["elements"]:
            if e.get("shared"):
                errs.append("Appendix %s/%s: Appendix maps must not cite 10.1 / 10.6 rule lines" % (akey, e["id"]))
    for name, fn, lines in (("legend", fig20, LEGEND_LINES), ("template", fig57, TEMPLATE_LINES)):
        fn()
        txt = _text_of(lines)
        for t in fn.audit:
            for v in inch_tokens(t):
                if v + '"' not in txt:
                    errs.append("%s: printed %s\" not in the cited lines" % (name, v))
    return errs


SETUP_FIGS = ["FIG-%02d" % i for i in (13, 14, 15, 16, 18, 19)] + ["FIG-%d" % i for i in range(20, 58)]


def check_registry(out_dir):
    """Every glyph id and pattern emitted on any setup or deployment diagram must be explained by the FIG-20 key.
    FIG-13 to FIG-16, FIG-18 and FIG-19 must also carry a compact key strip with exactly the glyphs their diagrams use
    (Appendix readers may not have seen the key in 10.4)."""
    errs = []
    info = {}
    for fid in SETUP_FIGS:
        with open(os.path.join(out_dir, fid + ".svg"), encoding="utf-8") as f:
            info[fid] = K.ids_in_svg(f.read())
    key = info["FIG-20"]["key"]
    reg = set(K.REG)
    if key != reg:
        errs.append("FIG-20 key swatches %s differ from the registry %s" % (sorted(key ^ reg), "(missing or extra)"))
    used_all = set()
    for fid in SETUP_FIGS:
        i = info[fid]
        if i["unknown"]:
            errs.append("%s: pattern ids not in the registry: %s" % (fid, sorted(i["unknown"])))
        ids = i["used"] | i["patterns"]
        used_all |= ids
        if fid != "FIG-20":
            missing = ids - key
            if missing:
                errs.append("%s: glyph or pattern ids not explained by FIG-20: %s" % (fid, sorted(missing)))
        if fid in ("FIG-13", "FIG-14", "FIG-15", "FIG-16", "FIG-18", "FIG-19"):
            if i["strip"] != ids:
                errs.append("%s: compact key strip %s does not match the glyphs used %s" % (fid, sorted(i["strip"]), sorted(ids)))
        elif fid != "FIG-20" and i["strip"] - key:
            errs.append("%s: key strip uses ids outside the key" % fid)
    unused = key - used_all
    if unused:
        errs.append("FIG-20 explains ids that no setup diagram uses: %s" % sorted(unused))
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
    rows = []
    summ = dict.fromkeys(STATUS_KEYS, 0)
    amb_total = 0
    for key in scenario_order():
        sp = sc[key]
        hl, end, cno, sno, title, climate = spans[key]
        cnt = dict.fromkeys(STATUS_KEYS.values(), 0)
        for e in sp["elements"]:
            cnt[STATUS_KEYS[e["status"]]] += 1
            summ[e["status"]] += 1
        amb_total += len(sp["ambiguities"])
        blocked = any(e["status"] == "UNRESOLVED" for e in sp["elements"])
        rows.append(dict(
            key=key, climate=climate, climate_number=cno, number=sno, title=title, source_lines=[hl, end],
            map_figure=sp["fig"], detail_figures=_detail_figures(key, sp), insert_after="B%05d" % sp["insert_after_line"],
            setup_rules=sp["setup_rules"],
            elements=cnt, undrawn_conditional=[dict(u) for u in sp.get("undrawn", [])],
            unresolved_elements=[dict(id=e["id"], note=e["note"], lines=e["lines"]) for e in sp["elements"] if e["kind"] == "unresolved"],
            ambiguities=sp["ambiguities"],
            iconography="shared-v2",
            status="blocked-by-ambiguity (one element shown as unresolved with a ? tag; owner decision needed)" if blocked else "drawn"))
    return rows, summ, amb_total


APPX_COVERAGE = {
    "A": dict(
        key="Appendix A: Learn to Play, A.4 Quickstart Scenario: The Broken Courier",
        setup_rules=["A.2 terrain list", "A.4 Setup Roll-off (short edge, 4\" zones)", "A.11 Initial Positions"],
        drawn_in_figure=["24\"x24\" battlefield drawn by the shared map renderer at 7.5 pt per inch", "4\" deployment zones on the two short edges (16239, 16409)",
                         "3\"x3\" centre ruin, Blocking (16162)", "low wall about 2\"x3\", Impassable, 4-6\" from the centre on one flank (16163; flank open, grey dashed)",
                         "rubble about 3\"x3\", Cover tagged Difficult, 4-6\" from the centre on the opposite flank (16164; grey dashed)",
                         "two Cover scatter pieces (16165; grey dashed)",
                         "Dispatch Satchel adjacent to the centre ruin (16235, 16413; side not stated, so one legal arrangement in grey dashes)",
                         "4 Dire Wolves within 2\" of the Satchel (16237; grey dashed) with the A.11 relative layout shown as a labelled inset",
                         "Treasure Chest 5\" east of centre (A.11 table, 16414), Heroes Edric, Mara, Varek, Senna at the A.11 table positions (16415-16418)",
                         "extraction through any battlefield edge (16249)"],
        not_drawn=["the third scatter piece (A.2 allows 2-3; positions open)"],
        ambiguities=["Which side of the centre ruin the Satchel (and therefore the Dire Wolves) stands on is not stated; drawn as one legal arrangement."]),
    "B": dict(
        key="Appendix B: Basic Mode, B.6 Basic Scenario: The Courier's Strongbox",
        setup_rules=["B.6 deployment (4\" of opposite edges)", "B.6 Monster Setup (3 Monster Entry markers, 5-7\" from centre, 4\" apart)"],
        drawn_in_figure=["24\"x24\" battlefield drawn by the shared map renderer at 7.5 pt per inch", "4\" zones on opposite edges (17641; which edges is not stated, so grey dashed, north and south drawn)",
                         "road across the centre (17639; width not stated)", "Strongbox at the centre (17645)",
                         "Monster Entry markers 5-7\" from the centre, at least 4\" apart, outside both zones (17643)", "one Monster group and one Satchel on each marker, drawn beside it (17643, 17645)",
                         "2 ruins/carts/low walls within 4\" of centre, 4 quarter pieces of 3\"x3\" (17639)", "extraction through the own deployment edge (17653)", "no Advanced Mode rules shown"],
        not_drawn=["which opposite edges are the deployment edges and who places the Entry markers are not stated (north and south drawn as one legal arrangement)"],
        ambiguities=[]),
}


def appendix_coverage():
    """Coverage rows for the two Appendix maps (FIG-18, FIG-19), generated from their specs."""
    rows = []
    for akey, sp in spec()["appendix"].items():
        cnt = dict.fromkeys(STATUS_KEYS.values(), 0)
        for e in sp["elements"]:
            cnt[STATUS_KEYS[e["status"]]] += 1
        r = dict(APPX_COVERAGE[akey])
        r.update(source_lines=[sp["spans"][1][0] if akey == "A" else sp["spans"][0][0], sp["spans"][1][1] if akey == "A" else sp["spans"][0][1]],
                 map_figure=sp["fig"], detail_figures=[], insert_after=None, elements=cnt, iconography="shared-v2",
                 status="drawn with the shared map renderer and glyph set; compact key strip on the figure")
        rows.append(r)
    return rows


def _install():
    for key, sp in spec()["scenarios"].items():
        n = int(sp["fig"].split("-")[1])
        globals()["fig%d" % n] = (lambda k=key: build_fig(k))


_install()
