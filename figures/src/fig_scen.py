"""FIG-13 .. FIG-16: deployment configurations, scenario objective placement, PvPvE interaction."""
import math
from svgkit import *

K = 4.0           # pt per inch for 36" boards in the deployment figures
BS = 36 * K       # board side (144 pt)


def rot_text(s, x, y, deg, text, size=9, weight=600, anchor="middle", fill=INK):
    s.raw('<g transform="rotate(%s %s %s)">' % (f1(deg), f1(x), f1(y)))
    s.text(x, y, text, size, weight, anchor, fill)
    s.raw("</g>")


def board(s, ox, oy, side=None, dashed=False):
    side = side or BS
    s.rect(ox, oy, side, side, fill=WHITE, stroke=INK, sw=1.1, dash="7 3" if dashed else None)


def zone(s, ox, oy, k, x, y, w, h):
    """Deployment zone in battlefield inches (x right, y down), dashed outline, pale fill."""
    s.rect(ox + x * k, oy + y * k, w * k, h * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")


def toks(s, ox, oy, k, kind, pts, r=3.8):
    for (x, y) in pts:
        token(s, kind, ox + x * k, oy + y * k, r)


def deploy_panel(idx, s, letter, title, caption, draw, cols=3, row_pitch=262, pitch_x=168, cap_w=160, dashed=False):
    col, row = idx % cols, idx // cols
    ox = col * pitch_x
    py = row * row_pitch
    panel_title(s, ox, py, letter, title)
    bx, by = ox + 4, py + 22
    board(s, bx, by, dashed=dashed)
    draw(s, bx, by)
    return s.para(ox, by + BS + 11, caption, cap_w, 9, lead=10.4)


def set_scale(k):
    global K, BS
    K = k
    BS = 36 * k


def _dimv(s, x, y1, y2, label):
    s.line(x, y1, x, y2, INK, 0.8)
    s.line(x - 2.5, y1, x + 2.5, y1, INK, 0.8)
    s.line(x - 2.5, y2, x + 2.5, y2, INK, 0.8)
    pill(s, x, (y1 + y2) / 2 + 3.2, label, 9, 700)


def _dimh(s, x1, x2, y, label):
    s.line(x1, y, x2, y, INK, 0.8)
    s.line(x1, y - 2.5, x1, y + 2.5, INK, 0.8)
    s.line(x2, y - 2.5, x2, y + 2.5, INK, 0.8)
    pill(s, (x1 + x2) / 2, y + 3.2, label, 9, 700)


GEOM14 = {}   # FIG-14 separation dimensions in battlefield inches, recorded when drawn (checked by make_figures.selfcheck)


def _dimc(s, x1, y1, x2, y2, label, size=9, side=None, dy=0.0):
    """Dimension line between two measured points with an arrowhead and an end tick at both ends.
    The label sits on the line, so the line itself must be long enough to show beyond the label."""
    ang = math.atan2(y2 - y1, x2 - x1)
    L, W = 3.6, 1.6
    s.line(x1, y1, x2, y2, INK, 0.8)
    for (px, py, a) in ((x1, y1, ang + math.pi), (x2, y2, ang)):
        bx, by = px - L * math.cos(a), py - L * math.sin(a)
        nx, ny = -math.sin(a) * W, math.cos(a) * W
        s.polygon([(px, py), (bx + nx, by + ny), (bx - nx, by - ny)], INK)
        s.line(px - math.sin(a) * 2.8, py + math.cos(a) * 2.8, px + math.sin(a) * 2.8, py - math.cos(a) * 2.8, INK, 0.8)
    if side is None:                       # label centred above a horizontal line
        pill(s, (x1 + x2) / 2, (y1 + y2) / 2 - 4.2, label, size, 700)
    else:                                  # label beside a short line (side = signed x offset in pt)
        pill(s, (x1 + x2) / 2 + side, (y1 + y2) / 2 + 3.2 + dy, label, size, 700, anchor="end" if side < 0 else "start")


# ---------------------------------------------------------------- panels
def d_long(s, bx, by):
    zone(s, bx, by, K, 0, 0, 6, 36)
    zone(s, bx, by, K, 30, 0, 6, 36)
    toks(s, bx, by, K, "A", [(3, 10), (3, 16), (3, 22)])
    toks(s, bx, by, K, "B", [(33, 10), (33, 16), (33, 22)])
    _dimh(s, bx, bx + 6 * K, by + 3.5 * K, "6\"")
    _dimh(s, bx + 30 * K, bx + 36 * K, by + 3.5 * K, "6\"")
    rot_text(s, bx + 3 * K + 3.2, by + 31 * K, -90, "long edge")
    rot_text(s, bx + 33 * K + 3.2, by + 31 * K, -90, "long edge")


def d_short(s, bx, by):
    zone(s, bx, by, K, 0, 0, 36, 6)
    zone(s, bx, by, K, 0, 30, 36, 6)
    toks(s, bx, by, K, "A", [(14, 3), (20, 3), (26, 3)])
    toks(s, bx, by, K, "B", [(14, 33), (20, 33), (26, 33)])
    _dimv(s, bx + 32 * K, by, by + 6 * K, "6\"")
    _dimv(s, bx + 32 * K, by + 30 * K, by + 36 * K, "6\"")
    s.text(bx + 3, by + 3 * K + 3.2, "short edge", 9, 600)
    s.text(bx + 3, by + 33 * K + 3.2, "short edge", 9, 600)


def d_choose(s, bx, by):
    zone(s, bx, by, K, 0, 0, 6, 36)
    zone(s, bx, by, K, 30, 0, 6, 36)
    toks(s, bx, by, K, "A", [(3, 9), (3, 14), (3, 19)])
    toks(s, bx, by, K, "B", [(33, 9), (33, 14), (33, 19)])
    callout(s, bx + 3 * K, by + 3.5 * K, 1, 6.0)
    callout(s, bx + 33 * K, by + 3.5 * K, 2, 6.0)
    _dimh(s, bx + 30 * K, bx + 36 * K, by + 23 * K, "6\"")
    rot_text(s, bx + 3 * K + 3.2, by + 31.5 * K, -90, "chosen")
    rot_text(s, bx + 33 * K + 3.2, by + 31.5 * K, -90, "opposite")


def d_corner_choose(s, bx, by):
    zone(s, bx, by, K, 0, 0, 8, 8)
    zone(s, bx, by, K, 28, 28, 8, 8)
    toks(s, bx, by, K, "A", [(2.6, 2.6), (5.4, 5.4)], 3.4)
    toks(s, bx, by, K, "B", [(30.6, 33.4), (33.4, 30.6)], 3.4)
    callout(s, bx + 17 * K, by + 4 * K, 1, 6.0)
    callout(s, bx + 22 * K, by + 32 * K, 2, 6.0)
    _dimh(s, bx + 28 * K, bx + 36 * K, by + 26 * K, "8\"")
    _dimv(s, bx + 10 * K + 4, by, by + 8 * K, "8\"")


def d_corner_alt(s, bx, by):
    zone(s, bx, by, K, 0, 0, 8, 8)
    zone(s, bx, by, K, 28, 28, 8, 8)
    toks(s, bx, by, K, "B", [(2.6, 2.6), (5.4, 5.4)], 3.4)
    toks(s, bx, by, K, "A", [(30.6, 33.4), (33.4, 30.6)], 3.4)
    _dimh(s, bx + 28 * K, bx + 36 * K, by + 26 * K, "8\"")
    _dimv(s, bx + 10 * K + 4, by, by + 8 * K, "8\"")


def d_trail(s, bx, by):
    zone(s, bx, by, K, 0, 0, 36, 6)
    zone(s, bx, by, K, 0, 30, 36, 6)
    # Trail 3-4" wide, full length between the short edges (3.5" drawn, centred for illustration)
    s.rect(bx + 16.25 * K, by, 3.5 * K, BS, fill=WHITE, stroke=None)
    s.line(bx + 16.25 * K, by, bx + 16.25 * K, by + BS, INK, 1.3)
    s.line(bx + 19.75 * K, by, bx + 19.75 * K, by + BS, INK, 1.3)
    toks(s, bx, by, K, "A", [(18, 2.6), (18, 5.0), (8, 3.6)], 3.0)
    toks(s, bx, by, K, "B", [(18, 33.4), (18, 31.0), (28, 32.4)], 3.0)
    pill(s, bx + 29 * K, by + 18 * K + 3, "Trail", 9, 700)


def d_chasm(s, bx, by):
    zone(s, bx, by, K, 0, 0, 36, 8)
    terrain(s, "impassable", bx, by + 14 * K, BS, 8 * K, None, sw=0.9)
    pill(s, bx + BS / 2, by + 18 * K + 3.4, "Chasm 8\" wide", 9, 700)
    r = 3.0                                # enlarged Hero marker radius (pt)
    ri = r / K                             # marker radius in drawn inches
    ay = 5.0
    toks(s, bx, by, K, "A", [(6, ay), (12, ay)], r)
    # nearest opposing Hero: drawn marker edges are 7" apart (more than the 6" limit)
    bxn = 12 + 2 * ri + 7.0
    toks(s, bx, by, K, "B", [(bxn, ay), (27, ay)], r)
    # dashed arc = 6" from the Party A Hero's marker edge (clipped to the board's top edge)
    R = 6.0 + ri
    x_top = 12 + math.sqrt(R * R - ay * ay)
    s.path("M %s %s A %s %s 0 0 1 %s %s" % (f1(bx + x_top * K), f1(by), f1(R * K), f1(R * K), f1(bx + 12 * K), f1(by + (ay + R) * K)), stroke=INK, sw=0.9, dash="3 2")
    # 6" limit (radial, down from the Party A Hero) and the actual gap to the nearest Party B Hero
    _dimc(s, bx + 12 * K, by + (ay + ri) * K, bx + 12 * K, by + (ay + R) * K, "6\"", side=-3.5, dy=9)
    _dimc(s, bx + (12 + ri) * K, by + ay * K, bx + (bxn - ri) * K, by + ay * K, "7\"")
    GEOM14["B"] = dict(a=(12.0, ay), b=(bxn, ay), r=ri, limit=6.0, dim=((12 + ri, ay), (bxn - ri, ay)))
    _dimv(s, bx + 33 * K, by, by + 8 * K, "8\"")


def d_quake(s, bx, by):
    """Detail of the centre of the battlefield at 6.6 pt per inch (not the full 36\" board).
    Hero markers are drawn at their true 1\" footprint at this scale (r = 0.5\")."""
    k = BS / 18.0
    x0, y0 = 9.0, 9.0                      # inches shown from the board's north-west corner
    ox = bx - x0 * k
    oy = by - y0 * k
    r = 0.5 * k
    zone(s, ox, oy, k, 14, 14, 8, 8)
    a1, a2 = (15.5, 16.8), (15.5, 21.2)
    b1, b2 = (20.5, 16.8), (20.5, 21.2)    # nearest opposing pair: footprint edges 4" apart (limit 3")
    # dashed ring = 3" from the Party A Hero's footprint edge
    s.circle(ox + a1[0] * k, oy + a1[1] * k, (0.5 + 3.0) * k, fill="none", stroke=INK, sw=0.9, dash="3 2")
    toks(s, ox, oy, k, "A", [a1, a2], r)
    toks(s, ox, oy, k, "B", [b1, b2], r)
    # 3" limit (radial, to the left of the Party A Hero) and the actual gap A edge -> nearest B edge
    _dimc(s, ox + (a1[0] - 0.5) * k, oy + a1[1] * k, ox + (a1[0] - 3.5) * k, oy + a1[1] * k, "3\"")
    _dimc(s, ox + (a1[0] + 0.5) * k, oy + a1[1] * k, ox + (b1[0] - 0.5) * k, oy + b1[1] * k, "4\"")
    GEOM14["C"] = dict(a=a1, b=b1, r=0.5, limit=3.0, dim=((a1[0] + 0.5, a1[1]), (b1[0] - 0.5, b1[1])),
                       others=[a2, b2], zone=(14, 14, 22, 22))
    s.text(bx + BS / 2, by + BS - 4, "centre detail", 9, 600, "middle", "#333")
    _dimh(s, ox + 14 * k, ox + 22 * k, oy + 12.2 * k, "8\"")
    pill(s, ox + 18 * k, oy + 24.4 * k, "Safe Zone", 9, 700)


def d_ravine(s, bx, by):
    zone(s, bx, by, K, 0, 0, 36, 6)
    zone(s, bx, by, K, 0, 30, 36, 6)
    terrain(s, "difficult", bx, by + 14.5 * K, BS, 7 * K, None, sw=0.9)
    pill(s, bx + BS / 2, by + 18 * K + 3.4, "Ravine 6\u20138\" wide", 9, 700)
    toks(s, bx, by, K, "A", [(10, 3), (18, 3), (26, 3)])
    toks(s, bx, by, K, "B", [(10, 33), (18, 33), (26, 33)])
    _dimv(s, bx + 32 * K, by, by + 6 * K, "6\"")
    _dimv(s, bx + 32 * K, by + 30 * K, by + 36 * K, "6\"")


def _legend_block(s, lx, ly, items, text, tw_):
    from svgkit import _swatch
    s.text(lx, ly + 8, "Key", 9, 700)
    ly += 14
    for kind, lab in items:
        _swatch(s, kind, lx, ly + 8)
        s.text(lx + LEG_W + 4, ly + 11.2, lab, 9)
        ly += 15
    return s.para(lx, ly + 10, text, tw_, 9, lead=10.4)


def fig13():
    s = Svg(FULL_W)
    set_scale(4.0)
    P = 228
    ys = []
    ys.append(deploy_panel(0, s, "A", "Opposite long edges", "Each party deploys within 6\" of its own long battlefield edge.", d_long, row_pitch=P))
    ys.append(deploy_panel(1, s, "B", "Opposite short edges", "Each party deploys within 6\" of its own short battlefield edge.", d_short, row_pitch=P))
    ys.append(deploy_panel(2, s, "C", "Roll-off winner chooses the edge", "(1) The Setup Roll-off winner chooses the edge (a long edge, or any battlefield edge, as the scenario states). (2) The other party takes the opposite edge. Both are within 6\" of their edge.", d_choose, row_pitch=P))
    ys.append(deploy_panel(3, s, "D", "Roll-off winner chooses a corner", "(1) The Setup Roll-off winner chooses an 8\"\u00d78\" corner zone. (2) The other party deploys in the diagonally opposite corner.", d_corner_choose, row_pitch=P))
    ys.append(deploy_panel(4, s, "E", "Opposite corners, alternate placing", "Opposite 8\"\u00d78\" corner zones. Where the scenario says so, parties alternate placing Heroes within their zone, starting with the party that lost the Setup Roll-off.", d_corner_alt, row_pitch=P))
    yl = _legend_block(s, 2 * 168 + 4, P + 22, [("A", "Party A Heroes (enlarged)"), ("B", "Party B Heroes (enlarged)"), ("zone", "deployment zone")],
                       "Zones and bands are drawn to scale on a 36\"\u00d736\" battlefield (4 pt per inch); Hero markers are enlarged. North and South are the short edges and East and West the long edges, even on a square battlefield (10.1). Each party may field 1\u20134 Heroes; two or three are shown. Sun-Drowned 2, The Mire 5 and The Mire 6 state no band distance: the 6\" band is the general pattern there, not a stated value.", 160)
    return s, max(ys[3], ys[4], yl) + 4


def fig14():
    s = Svg(FULL_W)
    set_scale(3.3)
    ys = []
    kw = dict(cols=4, row_pitch=0, pitch_x=126, cap_w=119)
    ys.append(deploy_panel(0, s, "A", "Trail", "The Setup Roll-off winner chooses the short edge where the Trail enters and deploys within 6\" of it with at least two Heroes on the Trail. The other party does the same at the opposite short edge. The Trail is 3\u20134\" wide and runs the full length.", d_trail, **kw))
    ys.append(deploy_panel(1, s, "B", "One shared edge", "Both parties deploy along the same short edge (the start side of the Chasm) within 8\" of it, placing Heroes alternately starting with the party that lost the Setup Roll-off. No Hero is placed within 6\" of an opposing Hero.", d_chasm, **kw))
    ys.append(deploy_panel(2, s, "C", "Central Safe Zone", "Both parties deploy inside a central 8\"\u00d78\" Safe Zone (shown enlarged: detail of the centre, 6.6 pt per inch), placing Heroes alternately starting with the party that lost the Setup Roll-off. No Hero is placed within 3\" of an opposing Hero.", d_quake, dashed=True, **kw))
    ys.append(deploy_panel(3, s, "D", "Across a Ravine", "Opposite short edges, within 6\" of the edge, on higher ground outside the Ravine (6\u20138\" wide, perpendicular to the long edges).", d_ravine, **kw))
    y = max(ys) + 6
    from svgkit import legend
    y = legend(s, [("A", "Party A Heroes (enlarged)"), ("B", "Party B Heroes (enlarged)"), ("zone", "deployment zone"), ("impassable", "Chasm (Impassable Terrain)"), ("difficult", "Ravine floor (Difficult Terrain)")], 0, y, FULL_W)
    yy = s.para(0, y + 4, "Zones, the Trail, the Chasm and the Ravine are drawn to scale on a 36\"\u00d736\" battlefield (3.3 pt per inch); Hero markers are enlarged. Zone-depth dimensions show the stated limits. In panels B and C no Hero is placed within the stated distance of an opposing Hero: the dashed arc (B, 6\") or ring (C, 3\") marks that distance from a Party A Hero\u2019s edge, and the dimension line between the nearest opposing Heroes runs between their closest edges (2.6), 7\" in B and 4\" in C, both outside the limit. Panel B is measured between drawn marker edges; panel C markers are drawn at their true 1\" size. Where the source gives a range (Trail 3\u20134\", Ravine 6\u20138\"), a value inside the range is drawn and its position is schematic.", FULL_W, 9, lead=10.4)
    return s, yy + 2


# ---------------------------------------------------------------------------
# FIG-15  Chasm Crossing: ledges and objective placement
# ---------------------------------------------------------------------------
def fig15():
    s = Svg(FULL_W)
    k = 4.3
    side = 36 * k
    panel_title(s, 0, 0, "A", "The Chasm Crossing")
    bx, by = 4, 26
    board(s, bx, by, side)
    # start-side deployment zone (8" from the short edge)
    s.rect(bx, by, side, 8 * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")
    # chasm 14..22 inches from the start edge
    terrain(s, "impassable", bx, by + 14 * k, side, 8 * k, None, sw=0.9)
    # path of ledges: 4 narrow platforms bridging the chasm along the middle (schematic proportions)
    lx = bx + side * 0.5
    ledge_w, ledge_l, gap = 7.0, 5.0, 4.6
    top = by + 14 * k + 0.3
    for i in range(4):
        y0 = top + i * (ledge_l + gap)
        crumbling = i == 1
        s.rect(lx - ledge_w / 2, y0, ledge_w, ledge_l, fill=WHITE, stroke=INK, sw=1.3, dash="2.5 1.8" if crumbling else None)
    pill(s, lx + 11, top + 17, "Path of Ledges", 9, 700, anchor="start")
    pill(s, bx + 5, by + 18 * k + 3.4, "Chasm 8\" wide", 9, 700, anchor="start")
    # start-side tokens
    toks(s, bx, by, k, "A", [(5, 3), (9.5, 3)], 3.8)
    toks(s, bx, by, k, "B", [(24.5, 3), (29, 3)], 3.8)
    # objectives
    mx, my = lx, by + 11 * k
    token(s, "obj", mx, my, 5.0)
    sx_, sy_ = lx, by + 25 * k
    token(s, "obj", sx_, sy_, 5.0)
    pill(s, mx + 9, my + 3.4, "Survey Map", 9, 700, anchor="start")
    pill(s, sx_ + 9, sy_ - 1.0, "Cartographer's", 9, 700, anchor="start")
    pill(s, sx_ + 9, sy_ + 9.4, "Stone", 9, 700, anchor="start")
    # 3" dimensions: Map to the first ledge, last ledge to the Stone (marker centres to the Chasm edges)
    _dimc(s, lx - 14, my, lx - 14, by + 14 * k, "3\"", side=-4)
    _dimc(s, lx - 14, by + 22 * k, lx - 14, sy_, "3\"", side=-4)
    pill(s, bx + side - 4, by + 6.3 * k + 6, "start side", 9, 600, anchor="end")
    pill(s, bx + side - 4, by + 31 * k, "delivery side", 9, 600, anchor="end")
    schematic(s, bx + side, by + side + 12)
    # ---------------- right: placement notes ----------------
    rx = side + 26
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Reading the placement")
    y = 24
    notes = [
        "**Deployment:** both parties use the start-side short edge, within 8\" of it; no Hero within 6\" of an opposing Hero.",
        "**Survey Map:** a carried objective that starts on the start side, 3\" from the first ledge. Its carrier's Speed is reduced by 1\" while carrying it.",
        "**Path of Ledges:** 3–4 narrow (1\" wide) platform markers bridging the Chasm, with 1–2\" gaps that require a Jump. 1–2 ledges are marked Crumbling: a Hero ending an activation on one makes a DEX Check and falls on a failure.",
        "**Cartographer's Stone:** a 1\" marker on the delivery side, 3\" from the last ledge. The first party to place the Survey Map adjacent to it wins immediately.",
        "**Jumping the Gaps (4.4.9):** each 1\" jumped costs 2\" of movement; declare a landing point, then make a DEX Check. A failed Jump into the Chasm causes a Chasm Fall (panel C).",
    ]
    y = step_list(s, rx, y, notes, rw, gap=5)
    y += 2
    y = legend(s, [("A", "Party A"), ("B", "Party B"), ("zone", "deployment zone"), ("impassable", "Chasm"), ("obj", "objective"), ("square", "ledge (dashed = Crumbling)")], rx, y, rw)
    # ---------------- bottom: Chasm Fall, with the Fly/Climb exceptions ----------------
    y = max(y, by + side + 18) + 1
    panel_title(s, 0, y, "C", "Chasm Fall (Undermarches 2 Special Rules)")
    y += 22
    falls = [
        "**Chasm Fall:** a combatant Pushed off a Ledge into the Chasm, or that fails a Crumbling Ledge Check and falls, is immediately removed from play. A Hero is Defeated and makes a normal Injuries Roll. A non-Hero is resolved as though reduced to 0 HP. This replaces the normal Falling rule. Any carried items, including the Survey Map, fall into the Chasm and are lost.",
        "**Hero or Hireling with a Fly or Climb Speed** that would fall may immediately spend 1 unspent AP, including AP reserved for Reactions, to catch themselves. Place them Prone in the nearest legal space on a Ledge, and end their current movement. If they cannot spend the AP, resolve the Chasm Fall normally.",
        "**Monster with a Fly or Climb Speed** that would fall is placed Prone in the nearest legal space on a Ledge, and their activation ends.",
    ]
    for i, st in enumerate(falls, 6):
        lines = wrap(st, FULL_W - 2 * 6.6 - 6, 9)
        callout(s, 6.6, y + 6.6 - 1.6, i, 6.6)
        for kk, ln in enumerate(lines):
            s.text(2 * 6.6 + 6, y + 6 + kk * 10.5, ln, 9)
        y += max(13.2, len(lines) * 10.5) + 4
    return s, y - 3


# ---------------------------------------------------------------------------
# FIG-16  PvPvE interaction: Whispering Grove
# ---------------------------------------------------------------------------
def fig16():
    s = Svg(FULL_W)
    k = 10.0
    panel_title(s, 0, 0, "A", "The Whispering Grove (10.4, Greenmark 2)")
    bx, by, side = 4, 26, 196
    s.rect(bx, by, side, side, fill=WHITE, stroke=INK, sw=1.0, dash="6 3")
    cx, cy = bx + side / 2, by + side / 2 - 2
    s.circle(cx, cy, 6.75 * k, fill=WHITE, stroke=INK, sw=1.2, dash="5 3")
    R = 4.04
    stones = [(cx, cy - R * k), (cx - 3.5 * k, cy + 2.02 * k), (cx + 3.5 * k, cy + 2.02 * k)]
    for (x, y) in stones:
        token(s, "obj", x, y, 5.5)
    _dimh(s, stones[1][0], stones[2][0], stones[1][1] + 17, "6\u20138\"")
    ha = (stones[0][0] + 14, stones[0][1] + 2)
    hb = (stones[1][0] - 14, stones[1][1] - 2)
    token(s, "A", *ha, 5.5)
    token(s, "B", *hb, 5.5)
    wx, wy = cx + 3, cy + 2
    token(s, "ML", wx, wy, 10)
    callout(s, ha[0] + 12, ha[1] - 10, 1, 6.0)
    callout(s, hb[0] - 12, hb[1] - 10, 2, 6.0)
    callout(s, wx + 17, wy - 14, 3, 6.0)
    arrow(s, wx - 11, wy + 4, hb[0] + 7, hb[1] + 3, "los")
    pill(s, cx, by + side - 8, "Central Clearing: about 12\u201315\" across", 9, 600)
    s.text(bx, by + side + 12, "Detail of the centre of the battlefield", 9, 600, "start", "#333")
    s.text(bx, by + side + 23, "(10 pt per inch; positions schematic)", 9, 600, "start", "#333")
    # ---------------- right: sequence ----------------
    rx = side + 26
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Two parties, one Monster (PvPvE)")
    y = 24
    notes = [
        "**Activate a Stone (10.4):** a Hero adjacent to a Standing Stone uses Interact [2 AP] and makes a SPI Check. A stone is claimed by only one party. Here a Party A Hero activates a Stone first.",
        "**Rival attempt:** a Party B Hero later attempts to activate another Stone.",
        "**Antlered Warden:** not placed at setup. When the first Stone is Interacted with, it is placed adjacent to the central Standing Stone and is Awake when placed.",
        "**Monster Phase:** the Warden's Target Priority is the valid Hero who most recently activated or attempted to activate a Standing Stone, here the Party B Hero. If no listed target is valid, the normal Monster target priorities apply (9.5 E).",
        "**AI Step 1, Entangling Roots:** if the Primary Target is within 8\" and not Immobilized, it must pass a DEX Check or become Immobilized. The activation then ends.",
    ]
    y = step_list(s, rx, y, notes, rw, gap=5)
    y += 2
    y = legend(s, [("A", "Party A Hero"), ("B", "Party B Hero"), ("ML", "Antlered Warden"), ("obj", "Standing Stone"), ("los", "Warden's target")], rx, y, rw)
    H = max(y, by + side + 28)
    return s, H + 2
