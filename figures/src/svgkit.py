"""Shared SVG drawing kit for the HERALDRY SKIRMISH RC484 rules diagrams.

Stdlib only.  User units = pt.  Grayscale only.  Font: "Source Sans 3".
Text widths come from figures/src/fontmetrics.json (measured from the bundled
Source Sans 3 static fonts) so that layout is deterministic.
"""
import json
import math
import os
from xml.sax.saxutils import escape

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "fontmetrics.json"), encoding="utf-8") as _f:
    _M = json.load(_f)

FONT = "'Source Sans 3'"
INK = "#000"
DARK = "#4a4a4a"      # Blocking Terrain solid fill
MID = "#8c8c8c"
LIGHT = "#d9d9d9"
PALE = "#f0f0f0"
WHITE = "#fff"

COL_W = 243
FULL_W = 504


def _segments(s):
    """Split '**bold**' markup into (text, bold) segments."""
    parts = s.split("**")
    return [(p, i % 2 == 1) for i, p in enumerate(parts) if p != ""]


def tw(s, size=9, weight=400):
    """Estimated advance width of s (with **bold** markup)."""
    total = 0.0
    for seg, bold in _segments(s):
        w = "700" if bold and weight < 700 else str(weight)
        tbl = _M[w]
        total += sum(tbl.get(c, 520) for c in seg)
    return total * size / 1000.0


def wrap(s, width, size=9, weight=400):
    """Greedy word wrap; returns list of lines (markup preserved per line)."""
    words = s.split(" ")
    lines, cur = [], ""
    open_bold = False
    for w in words:
        trial = (cur + " " + w) if cur else w
        if tw(trial, size, weight) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    # repair bold markup that spans a wrap boundary
    fixed = []
    for ln in lines:
        if open_bold:
            ln = "**" + ln
        if ln.count("**") % 2 == 1:
            ln = ln + "**"
            open_bold = True
        else:
            open_bold = False
        fixed.append(ln)
    return fixed


def f1(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


class Svg:
    def __init__(self, width):
        self.w = width
        self.h = 0
        self.body = []

    # ---- primitives -------------------------------------------------
    def raw(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=0.75, rx=0, dash=None, opacity=None):
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (stroke, f1(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if rx:
            a += ' rx="%s"' % f1(rx)
        self.raw('<rect x="%s" y="%s" width="%s" height="%s"%s/>' % (f1(x), f1(y), f1(w), f1(h), a))

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.0, dash=None, cap="butt"):
        a = ' stroke="%s" stroke-width="%s" stroke-linecap="%s"' % (stroke, f1(sw), cap)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        self.raw('<line x1="%s" y1="%s" x2="%s" y2="%s"%s/>' % (f1(x1), f1(y1), f1(x2), f1(y2), a))

    def polyline(self, pts, stroke=INK, sw=1.0, dash=None, cap="butt", fill="none"):
        a = ' fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"' % (fill, stroke, f1(sw), cap)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        self.raw('<polyline points="%s"%s/>' % (" ".join("%s,%s" % (f1(x), f1(y)) for x, y in pts), a))

    def polygon(self, pts, fill=INK, stroke=None, sw=0.75):
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, f1(sw))
        self.raw('<polygon points="%s"%s/>' % (" ".join("%s,%s" % (f1(x), f1(y)) for x, y in pts), a))

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=0.75, dash=None):
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (stroke, f1(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        self.raw('<circle cx="%s" cy="%s" r="%s"%s/>' % (f1(cx), f1(cy), f1(r), a))

    def path(self, d, fill="none", stroke=INK, sw=0.75, dash=None, cap="butt"):
        a = ' fill="%s"' % fill
        if stroke:
            a += ' stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"' % (stroke, f1(sw), cap)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        self.raw('<path d="%s"%s/>' % (d, a))

    def text(self, x, y, s, size=9, weight=400, anchor="start", fill=INK, italic=False):
        """Draw one line of text with baseline at y.  **bold** markup allowed."""
        segs = _segments(s)
        attrs = ' font-family="%s" font-size="%s" fill="%s"' % (FONT, f1(size), fill)
        if italic:
            attrs += ' font-style="italic"'
        if anchor != "start":
            attrs += ' text-anchor="%s"' % anchor
        if len(segs) == 1 and not segs[0][1]:
            self.raw('<text x="%s" y="%s" font-weight="%d"%s>%s</text>' % (f1(x), f1(y), weight, attrs, escape(segs[0][0])))
            return
        inner = ""
        for seg, bold in segs:
            wt = 700 if bold and weight < 700 else weight
            inner += '<tspan font-weight="%d">%s</tspan>' % (wt, escape(seg))
        self.raw('<text x="%s" y="%s"%s>%s</text>' % (f1(x), f1(y), attrs, inner))

    def para(self, x, y, s, width, size=9, weight=400, lead=11, anchor="start", fill=INK):
        """Wrapped paragraph; y is first baseline; returns y after last line (next baseline)."""
        lines = wrap(s, width, size, weight)
        for i, ln in enumerate(lines):
            xx = x if anchor == "start" else (x + width / 2 if anchor == "middle" else x + width)
            self.text(xx, y + i * lead, ln, size, weight, anchor, fill)
        return y + len(lines) * lead

    def group(self, transform=None):
        self.raw('<g%s>' % (' transform="%s"' % transform if transform else ""))

    def endgroup(self):
        self.raw("</g>")

    # ---- output -----------------------------------------------------
    def render(self, height, title=None, desc=None):
        defs = DEFS
        head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%spt" height="%spt" viewBox="0 0 %s %s">\n'
                % (f1(self.w), f1(height), f1(self.w), f1(height)))
        t = ""
        if title:
            t += "<title>%s</title>\n" % escape(title)
        if desc:
            t += "<desc>%s</desc>\n" % escape(desc)
        return head + t + defs + "\n" + "\n".join(self.body) + "\n</svg>\n"


DEFS = """<defs>
<pattern id="p-cover" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#fff"/><path d="M0 0.5H5M0.5 0V5" stroke="#444" stroke-width="0.7" fill="none"/></pattern>
<pattern id="p-diff" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#fff"/><circle cx="1" cy="1" r="0.75" fill="#222"/><circle cx="3" cy="3" r="0.75" fill="#222"/></pattern>
<pattern id="p-imp" width="2.4" height="2.4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.4" height="2.4" fill="#fff"/><path d="M0.4 0V2.4" stroke="#000" stroke-width="0.95" fill="none"/></pattern>
<pattern id="p-mon" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="3.2" height="3.2" fill="#fff"/><path d="M0.5 0V3.2" stroke="#000" stroke-width="1" fill="none"/></pattern>
<pattern id="p-aoe" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="4" height="4" fill="#fff"/><path d="M0.5 0V4" stroke="#777" stroke-width="1.4" fill="none"/></pattern>
</defs>"""


# ---------------------------------------------------------------------
# Visual grammar helpers
# ---------------------------------------------------------------------
PAT = {"cover": "url(#p-cover)", "difficult": "url(#p-diff)", "impassable": "url(#p-imp)",
       "blocking": DARK, "monster": "url(#p-mon)", "aoe": "url(#p-aoe)", "open": WHITE}


def pill(s, x, y, text, size=9, weight=600, anchor="middle", pad=1.8, fill=WHITE, color=INK, border=None):
    """Label with white backing so it stays legible over a pattern. y = baseline."""
    w = tw(text, size, weight)
    if anchor == "middle":
        x0 = x - w / 2
    elif anchor == "end":
        x0 = x - w
    else:
        x0 = x
    s.rect(x0 - pad, y - size * 0.80 - pad * 0.4, w + 2 * pad, size * 1.05 + pad * 0.8, fill=fill, stroke=border, sw=0.5)
    s.text(x0, y, text, size, weight, "start", color)


def terrain(s, kind, x, y, w, h, label=None, label_dy=None, label_color=None, sw=0.9):
    s.rect(x, y, w, h, fill=PAT[kind], stroke=INK, sw=sw)
    if label:
        cx, cy = x + w / 2, y + h / 2 + 3.2
        if label_dy is not None:
            cy = y + label_dy
        if kind == "blocking":
            lines = label if isinstance(label, list) else [label]
            for i, ln in enumerate(lines):
                s.text(cx, cy + (i - (len(lines) - 1) / 2.0) * 10.5, ln, 9, 700, "middle", WHITE)
        else:
            lines = label if isinstance(label, list) else [label]
            for i, ln in enumerate(lines):
                pill(s, cx, cy + (i - (len(lines) - 1) / 2.0) * 11, ln)


def hexpts(cx, cy, r):
    return [(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i))) for i in range(6)]


def token(s, kind, cx, cy, r=7.0):
    """kind: 'A' Party A (black circle), 'B' Party B (white circle, outline, centre dot),
    'M' Monster (hatched hexagon), 'ML' large Monster (hatched square, r = half side)."""
    if kind == "A":
        s.circle(cx, cy, r, fill=INK, stroke=INK, sw=0.75)
    elif kind == "B":
        s.circle(cx, cy, r, fill=WHITE, stroke=INK, sw=1.4)
        s.circle(cx, cy, max(1.6, r * 0.28), fill=INK, stroke=None)
    elif kind == "M":
        s.polygon(hexpts(cx, cy, r * 1.08), fill=PAT["monster"], stroke=INK, sw=1.0)
    elif kind == "ML":
        s.rect(cx - r, cy - r, 2 * r, 2 * r, fill=PAT["monster"], stroke=INK, sw=1.4)
    elif kind == "obj":   # objective marker: diamond, white with black outline and cross
        s.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=WHITE, stroke=INK, sw=1.2)
        s.line(cx - r * 0.5, cy, cx + r * 0.5, cy, sw=1.0)
        s.line(cx, cy - r * 0.5, cx, cy + r * 0.5, sw=1.0)
    elif kind == "chest":  # small square with a bar
        s.rect(cx - r * 0.85, cy - r * 0.65, r * 1.7, r * 1.3, fill=LIGHT, stroke=INK, sw=1.0)
        s.line(cx - r * 0.85, cy - r * 0.1, cx + r * 0.85, cy - r * 0.1, sw=0.8)
    else:
        raise ValueError(kind)


def ghost(s, cx, cy, r=7.0):
    """Dotted outline = starting position (not a combatant on the board any more)."""
    s.circle(cx, cy, r, fill="none", stroke=INK, sw=1.0, dash="1.6 2")


def callout(s, cx, cy, n, r=6.6):
    s.circle(cx, cy, r, fill=INK, stroke=INK, sw=0.5)
    s.text(cx, cy + 3.3, str(n), 9, 700, "middle", WHITE)


def xmark(s, cx, cy, d=5.0, sw=1.8, color=INK, halo=True):
    if halo:
        s.circle(cx, cy, d + 2.2, fill=WHITE, stroke=None)
    s.line(cx - d, cy - d, cx + d, cy + d, color, sw, cap="round")
    s.line(cx - d, cy + d, cx + d, cy - d, color, sw, cap="round")


def _headpts(x1, y1, x2, y2, L=7.0, W=3.4):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - L * math.cos(ang), y2 - L * math.sin(ang)
    px, py = -math.sin(ang) * W, math.cos(ang) * W
    return [(x2, y2), (bx + px, by + py), (bx - px, by - py)], (bx, by)


def arrow(s, x1, y1, x2, y2, kind="move", forbidden=False, sw=None):
    """kind: move (solid, permitted), los (dashed, no head, end dots), forced (dotted + head)."""
    if kind == "move":
        w = sw or 1.6
        head, (bx, by) = _headpts(x1, y1, x2, y2)
        if forbidden:
            s.line(x1, y1, x2, y2, INK, w)
            xmark(s, x2, y2)
        else:
            s.line(x1, y1, bx, by, INK, w)
            s.polygon(head, INK)
    elif kind == "forced":
        w = sw or 1.9
        head, (bx, by) = _headpts(x1, y1, x2, y2, 7.5, 3.8)
        if forbidden:
            s.line(x1, y1, x2, y2, INK, w, dash="0.1 3.4", cap="round")
            xmark(s, x2, y2)
        else:
            s.line(x1, y1, bx, by, INK, w, dash="0.1 3.4", cap="round")
            s.polygon(head, INK)
    elif kind == "los":
        w = sw or 1.1
        s.line(x1, y1, x2, y2, INK, w, dash="4.5 2.8")
        s.circle(x1, y1, 1.9, fill=INK, stroke=None)
        if forbidden:
            xmark(s, x2, y2)
        else:
            s.circle(x2, y2, 1.9, fill=INK, stroke=None)
    else:
        raise ValueError(kind)


def poly_arrow(s, pts, kind="move", forbidden=False):
    """Multi-segment movement arrow; arrowhead on the last segment."""
    w = 1.6 if kind == "move" else 1.9
    dash = None if kind == "move" else "0.1 3.4"
    cap = "butt" if kind == "move" else "round"
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    L = 7.0
    head, (bx, by) = _headpts(x1, y1, x2, y2, L, 3.4)
    if forbidden:
        s.polyline(pts, INK, w, dash=dash, cap=cap)
        xmark(s, x2, y2)
    else:
        s.polyline(pts[:-1] + [(bx, by)], INK, w, dash=dash, cap=cap)
        s.polygon(head, INK)


def grid(s, x, y, cols, rows, cell, stroke="#a6a6a6", sw=0.5, fill=None):
    if fill:
        s.rect(x, y, cols * cell, rows * cell, fill=fill, stroke=None)
    for i in range(cols + 1):
        s.line(x + i * cell, y, x + i * cell, y + rows * cell, stroke, sw)
    for j in range(rows + 1):
        s.line(x, y + j * cell, x + cols * cell, y + j * cell, stroke, sw)
    s.rect(x, y, cols * cell, rows * cell, fill="none", stroke=INK, sw=0.9)


def cellrect(s, x0, y0, cell, i, j, kind, label=None, sw=0.6):
    """Fill grid cell (i=col,j=row) with a terrain pattern."""
    terrain(s, kind, x0 + i * cell, y0 + j * cell, cell, cell, label, sw=sw)


def dim(s, x1, y1, x2, y2, label, size=9, off=0, side="above", tick=3.0, weight=600):
    """Dimension line with end ticks and centred label (stated source distances only)."""
    s.line(x1, y1, x2, y2, INK, 0.8)
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    for (px, py) in ((x1, y1), (x2, y2)):
        s.line(px - nx * tick, py - ny * tick, px + nx * tick, py + ny * tick, INK, 0.8)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    sgn = -1 if side == "above" else 1
    lx, ly = mx + nx * (off + 7) * sgn, my + ny * (off + 7) * sgn
    pill(s, lx, ly + 3, label, size, weight)


def schematic(s, x, y, anchor="end", text="Schematic — not to scale"):
    s.text(x, y, text, 9, 600, anchor, "#333")


# --- Legend ----------------------------------------------------------
LEG_W = 22


def _swatch(s, kind, x, y):
    """Draw legend swatch centred vertically at y (row centre), starting at x; width LEG_W."""
    if kind in ("A", "B", "M"):
        token(s, kind, x + 9, y, 6.0)
    elif kind == "ML":
        token(s, "ML", x + 9, y, 6.0)
    elif kind == "obj":
        token(s, "obj", x + 9, y, 6.0)
    elif kind == "chest":
        token(s, "chest", x + 9, y, 6.5)
    elif kind in PAT:
        terrain(s, kind, x + 2, y - 5.5, 16, 11, None, sw=0.8)
    elif kind == "move":
        arrow(s, x, y, x + 20, y, "move")
    elif kind == "los":
        arrow(s, x + 1, y, x + 19, y, "los")
    elif kind == "forced":
        arrow(s, x, y, x + 20, y, "forced")
    elif kind == "forbidden":
        arrow(s, x, y, x + 15, y, "move", forbidden=True)
    elif kind == "step":
        callout(s, x + 9, y, "1", 6.2)
    elif kind == "zone":
        s.rect(x + 1, y - 5.5, 17, 11, fill=PALE, stroke=INK, sw=0.8, dash="3 2")
    elif kind == "aoe":
        s.rect(x + 2, y - 5.5, 16, 11, fill=PAT["aoe"], stroke=INK, sw=0.8)
    elif kind == "square":
        s.rect(x + 3, y - 6, 12, 12, fill=WHITE, stroke=INK, sw=0.6)
    elif kind == "ghost":
        ghost(s, x + 9, y, 6.0)
    elif kind == "blockx":
        xmark(s, x + 9, y, 4.2, 1.6, halo=False)
    elif kind == "hazard":
        s.rect(x + 2, y - 5.5, 16, 11, fill="#c4c4c4", stroke=INK, sw=0.8)
        s.text(x + 10, y + 3.6, "!", 9, 700, "middle")
    elif kind == "lowfill":
        s.rect(x + 2, y - 5.5, 16, 11, fill=LIGHT, stroke=INK, sw=0.8)
    elif kind == "palefill":
        s.rect(x + 2, y - 5.5, 16, 11, fill=PALE, stroke=INK, sw=0.8)
    else:
        raise ValueError(kind)


def legend(s, items, x, y, width, size=9, row_h=15, title="Key"):
    """items: list of (kind, label). Wraps in rows. Returns y below legend."""
    cy = y
    if title:
        s.text(x, cy + 8, title, 9, 700)
        cx = x + tw(title, 9, 700) + 8
    else:
        cx = x
    rowy = cy + 5
    for kind, label in items:
        w = LEG_W + 4 + tw(label, size, 400) + 10
        if cx + w - 10 > x + width and cx > x + 0.1:
            cx = x
            rowy += row_h
        _swatch(s, kind, cx, rowy + 3)
        s.text(cx + LEG_W + 4, rowy + 6, label, size, 400)
        cx += w
    return rowy + row_h


def step_list(s, x, y, steps, width, size=9, lead=10.5, gap=4, num_r=6.6):
    """Numbered steps with callout circles. steps: list of strings. Returns y after."""
    for i, st in enumerate(steps, 1):
        lines = wrap(st, width - 2 * num_r - 6, size)
        callout(s, x + num_r, y + num_r - 1.6, i, num_r)
        for k, ln in enumerate(lines):
            s.text(x + 2 * num_r + 6, y + 6 + k * lead, ln, size)
        y += max(2 * num_r, len(lines) * lead) + gap
    return y


def box(s, x, y, w, lines, size=9, weight=400, fill=WHITE, stroke=INK, sw=0.9, pad=4, lead=10.8, rx=2.5,
        anchor="middle", head=None, head_fill=None):
    """Rounded text box; lines is a string or list of strings (each wrapped to the box width).
    Returns box height."""
    if isinstance(lines, str):
        lines = [lines]
    wrapped = []
    for ln in lines:
        wrapped += wrap(ln, w - 2 * pad, size, weight)
    h = len(wrapped) * lead + 2 * pad - 1.5
    if head:
        h += lead + 1
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)
    ty = y + pad + size * 0.82
    if head:
        s.text(x + w / 2 if anchor == "middle" else x + pad, ty, head, size, 700, anchor)
        ty += lead + 1
    for ln in wrapped:
        s.text(x + w / 2 if anchor == "middle" else x + pad, ty, ln, size, weight, anchor)
        ty += lead
    return h


def vflow_arrow(s, x, y1, y2):
    """Short downward flow arrow (sequence flow)."""
    s.line(x, y1, x, y2 - 6, INK, 1.2)
    s.polygon([(x, y2), (x - 3.2, y2 - 7), (x + 3.2, y2 - 7)], INK)


def hflow_arrow(s, x1, x2, y):
    s.line(x1, y, x2 - 6, y, INK, 1.2)
    s.polygon([(x2, y), (x2 - 7, y - 3.2), (x2 - 7, y + 3.2)], INK)


def panel_title(s, x, y, letter, title, width=None):
    """Panel heading: bold letter in a square + title."""
    s.rect(x, y, 13, 13, fill=INK, stroke=None)
    s.text(x + 6.5, y + 10.4, letter, 9, 700, "middle", WHITE)
    s.text(x + 18, y + 10.4, title, 9.5, 700)


class Grid:
    """Square-grid helper: columns/rows count from 0 at top-left."""

    def __init__(self, s, ox, oy, cols, rows, cell, draw=True, fill=WHITE):
        self.s, self.ox, self.oy, self.cols, self.rows, self.cell = s, ox, oy, cols, rows, cell
        if draw:
            grid(s, ox, oy, cols, rows, cell, fill=fill)

    def c(self, col, row):
        return (self.ox + (col + 0.5) * self.cell, self.oy + (row + 0.5) * self.cell)

    def pt(self, x, y):
        """Point at grid-corner coordinates (x cells from left, y cells from top)."""
        return (self.ox + x * self.cell, self.oy + y * self.cell)

    def fillcell(self, col, row, kind, label=None):
        terrain(self.s, kind, self.ox + col * self.cell, self.oy + row * self.cell, self.cell, self.cell, label, sw=0.6)

    def block(self, col, row, w, h, kind, label=None, sw=0.9):
        terrain(self.s, kind, self.ox + col * self.cell, self.oy + row * self.cell, w * self.cell, h * self.cell, label, sw=sw)

    def token(self, col, row, kind, r=None, span=1):
        x, y = self.c(col + (span - 1) / 2.0, row + (span - 1) / 2.0)
        if kind == "ML":
            token(self.s, "ML", x, y, span * self.cell / 2.0 - 2)
        else:
            token(self.s, kind, x, y, r or self.cell * 0.38)

    def height(self):
        return self.rows * self.cell
