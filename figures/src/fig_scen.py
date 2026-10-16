"""FIG-13 .. FIG-16: deployment configurations, scenario objective placement, PvPvE interaction.

Every symbol is drawn by the shared glyph functions of scenkit.py (the same ones that draw FIG-20 and the 36 Core Scenario maps);
each figure carries a compact key strip with the glyphs it uses and refers to the full key, FIG-20.
"""
import math
import scenkit as K
from scenkit import MapSvg
from svgkit import FULL_W, INK, PALE, WHITE, MID, wrap, tw, f1, panel_title

K_ = 4.0           # pt per inch for 36" boards in the deployment figures
BS = 36 * K_       # board side (144 pt)


def rot_text(s, x, y, deg, text, size=9, weight=600, anchor="middle", fill=INK):
    s.raw('<g transform="rotate(%s %s %s)">' % (f1(deg), f1(x), f1(y)))
    s.htext(x, y, text, size, weight, anchor, fill)
    s.raw("</g>")


def board(s, ox, oy, side=None, frame=False):
    """The battlefield (or, with frame=True, a detail of it: thin grey frame)."""
    side = side or BS
    s.rect(ox, oy, side, side, fill=WHITE, stroke=MID if frame else INK, sw=0.8 if frame else 1.1)


def zone(s, ox, oy, k, x, y, w, h, party, n=36):
    """Deployment zone in battlefield inches (x right, y down) drawn by the shared zone glyph."""
    sides = [b[0] for b in K.band_sides((x, y, x + w, y + h), n)]
    K.zone(s, ox + x * k, oy + y * k, w * k, h * k, party, sides)


def toks(s, ox, oy, k, kind, pts, r=3.8):
    for (x, y) in pts:
        K.hero(s, kind, ox + x * k, oy + y * k, r)


def deploy_panel(idx, s, letter, title, caption, draw, cols=3, row_pitch=262, pitch_x=168, cap_w=160, frame=False):
    col, row = idx % cols, idx // cols
    ox = col * pitch_x
    py = row * row_pitch
    panel_title(s, ox, py, letter, title)
    bx, by = ox + 4, py + 22
    board(s, bx, by, frame=frame)
    draw(s, bx, by)
    return s.para(ox, by + BS + 11, caption, cap_w, 9, lead=10.4)


def set_scale(k):
    global K_, BS
    K_ = k
    BS = 36 * k


def _dimv(s, x, y1, y2, label):
    K.dim_labeled(s, x, y1, x, y2, label, 2.5)


def _dimh(s, x1, x2, y, label):
    K.dim_labeled(s, x1, y, x2, y, label, 2.5)


GEOM14 = {}   # FIG-14 separation dimensions in battlefield inches, recorded when drawn (checked by make_figures.selfcheck)


# ---------------------------------------------------------------- panels
def d_long(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 6, 36, "A")
    zone(s, bx, by, K_, 30, 0, 6, 36, "B")
    toks(s, bx, by, K_, "A", [(3, 10), (3, 16), (3, 22)])
    toks(s, bx, by, K_, "B", [(33, 10), (33, 16), (33, 22)])
    _dimh(s, bx, bx + 6 * K_, by + 3.5 * K_, "6\"")
    _dimh(s, bx + 30 * K_, bx + 36 * K_, by + 3.5 * K_, "6\"")
    rot_text(s, bx + 3 * K_ + 3.2, by + 31 * K_, -90, "long edge")
    rot_text(s, bx + 33 * K_ + 3.2, by + 31 * K_, -90, "long edge")


def d_short(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 36, 6, "A")
    zone(s, bx, by, K_, 0, 30, 36, 6, "B")
    toks(s, bx, by, K_, "A", [(14, 3), (20, 3), (26, 3)])
    toks(s, bx, by, K_, "B", [(14, 33), (20, 33), (26, 33)])
    _dimv(s, bx + 32 * K_, by, by + 6 * K_, "6\"")
    _dimv(s, bx + 32 * K_, by + 30 * K_, by + 36 * K_, "6\"")
    s.htext(bx + 3, by + 3 * K_ + 3.2, "short edge", 9, 600)
    s.htext(bx + 3, by + 33 * K_ + 3.2, "short edge", 9, 600)


def d_choose(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 6, 36, "A")
    zone(s, bx, by, K_, 30, 0, 6, 36, "B")
    toks(s, bx, by, K_, "A", [(3, 9), (3, 14), (3, 19)])
    toks(s, bx, by, K_, "B", [(33, 9), (33, 14), (33, 19)])
    K.step(s, bx + 3 * K_, by + 3.5 * K_, 1, 6.0)
    K.step(s, bx + 33 * K_, by + 3.5 * K_, 2, 6.0)
    _dimh(s, bx + 30 * K_, bx + 36 * K_, by + 23 * K_, "6\"")
    rot_text(s, bx + 3 * K_ + 3.2, by + 31.5 * K_, -90, "chosen")
    rot_text(s, bx + 33 * K_ + 3.2, by + 31.5 * K_, -90, "opposite")


def d_corner_choose(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 8, 8, "A")
    zone(s, bx, by, K_, 28, 28, 8, 8, "B")
    toks(s, bx, by, K_, "A", [(2.6, 2.6), (5.4, 5.4)], 3.4)
    toks(s, bx, by, K_, "B", [(30.6, 33.4), (33.4, 30.6)], 3.4)
    K.step(s, bx + 17 * K_, by + 4 * K_, 1, 6.0)
    K.step(s, bx + 22 * K_, by + 32 * K_, 2, 6.0)
    _dimh(s, bx + 28 * K_, bx + 36 * K_, by + 26 * K_, "8\"")
    _dimv(s, bx + 10 * K_ + 4, by, by + 8 * K_, "8\"")


def d_corner_alt(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 8, 8, "B")
    zone(s, bx, by, K_, 28, 28, 8, 8, "A")
    toks(s, bx, by, K_, "B", [(2.6, 2.6), (5.4, 5.4)], 3.4)
    toks(s, bx, by, K_, "A", [(30.6, 33.4), (33.4, 30.6)], 3.4)
    _dimh(s, bx + 28 * K_, bx + 36 * K_, by + 26 * K_, "8\"")
    _dimv(s, bx + 10 * K_ + 4, by, by + 8 * K_, "8\"")


def d_trail(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 36, 6, "A")
    zone(s, bx, by, K_, 0, 30, 36, 6, "B")
    # Trail 3-4" wide, full length between the short edges (3.5" drawn, centred for illustration)
    K.terrain_shape(s, "gap", "rect", (bx + 16.25 * K_, by, 3.5 * K_, BS), False, 1.3)
    toks(s, bx, by, K_, "A", [(18, 2.6), (18, 5.0), (8, 3.6)], 3.0)
    toks(s, bx, by, K_, "B", [(18, 33.4), (18, 31.0), (28, 32.4)], 3.0)
    K.pill_label(s, bx + 29 * K_, by + 18 * K_ + 3, "Trail", 9, 700)


def d_chasm(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 36, 8, "AB")
    K.terrain_shape(s, "chasm", "rect", (bx, by + 14 * K_, BS, 8 * K_), False, 0.9)
    K.pill_label(s, bx + BS / 2, by + 18 * K_ + 3.4, "Chasm 8\" wide", 9, 700)
    r = 3.0                                # enlarged Hero marker radius (pt)
    ri = r / K_                            # marker radius in drawn inches
    ay = 5.0
    toks(s, bx, by, K_, "A", [(6, ay), (12, ay)], r)
    # nearest opposing Hero: drawn marker edges are 7" apart (more than the 6" limit)
    bxn = 12 + 2 * ri + 7.0
    toks(s, bx, by, K_, "B", [(bxn, ay), (27, ay)], r)
    # ring = 6" from the Party A Hero's marker edge (clipped to the board's top edge)
    R = 6.0 + ri
    x_top = 12 + math.sqrt(R * R - ay * ay)
    K.ring_path(s, "M %s %s A %s %s 0 0 1 %s %s" % (f1(bx + x_top * K_), f1(by), f1(R * K_), f1(R * K_), f1(bx + 12 * K_), f1(by + (ay + R) * K_)))
    # 6" limit (radial, down from the Party A Hero) and the actual gap to the nearest Party B Hero
    K.dim_labeled(s, bx + 12 * K_, by + (ay + ri) * K_, bx + 12 * K_, by + (ay + R) * K_, "6\"", 2.5, off=-9)
    K.dim_labeled(s, bx + (12 + ri) * K_, by + ay * K_, bx + (bxn - ri) * K_, by + ay * K_, "7\"", 2.5, off=-8)
    GEOM14["B"] = dict(a=(12.0, ay), b=(bxn, ay), r=ri, limit=6.0, dim=((12 + ri, ay), (bxn - ri, ay)))
    _dimv(s, bx + 33 * K_, by, by + 8 * K_, "8\"")


def d_quake(s, bx, by):
    """Detail of the centre of the battlefield at 6.6 pt per inch (not the full 36\" board).
    Hero markers are drawn at their true 1\" footprint at this scale (r = 0.5\")."""
    k = BS / 18.0
    x0, y0 = 9.0, 9.0                      # inches shown from the board's north-west corner
    ox = bx - x0 * k
    oy = by - y0 * k
    r = 0.5 * k
    s.raw('<g clip-path="url(#qclip)">')
    zone(s, ox, oy, k, 14, 14, 8, 8, "AB")
    a1, a2 = (15.5, 16.8), (15.5, 21.2)
    b1, b2 = (20.5, 16.8), (20.5, 21.2)    # nearest opposing pair: footprint edges 4" apart (limit 3")
    # ring = 3" from the Party A Hero's footprint edge
    K.ring(s, ox + a1[0] * k, oy + a1[1] * k, (0.5 + 3.0) * k, clip="qclip")
    toks(s, ox, oy, k, "A", [a1, a2], r)
    toks(s, ox, oy, k, "B", [b1, b2], r)
    s.raw("</g>")
    # 3" limit (radial, to the left of the Party A Hero) and the actual gap A edge -> nearest B edge
    K.dim_labeled(s, ox + (a1[0] - 0.5) * k, oy + a1[1] * k, ox + (a1[0] - 3.5) * k, oy + a1[1] * k, "3\"", 2.5, off=-8)
    K.dim_labeled(s, ox + (a1[0] + 0.5) * k, oy + a1[1] * k, ox + (b1[0] - 0.5) * k, oy + b1[1] * k, "4\"", 2.5, off=-8)
    GEOM14["C"] = dict(a=a1, b=b1, r=0.5, limit=3.0, dim=((a1[0] + 0.5, a1[1]), (b1[0] - 0.5, b1[1])),
                       others=[a2, b2], zone=(14, 14, 22, 22))
    s.htext(bx + BS / 2, by + BS - 4, "centre detail", 9, 600, "middle", "#333")
    _dimh(s, ox + 14 * k, ox + 22 * k, oy + 12.2 * k, "8\"")
    K.pill_label(s, ox + 18 * k, oy + 24.4 * k, "Safe Zone", 9, 700)


def d_ravine(s, bx, by):
    zone(s, bx, by, K_, 0, 0, 36, 6, "A")
    zone(s, bx, by, K_, 0, 30, 36, 6, "B")
    K.terrain_shape(s, "difficult", "rect", (bx, by + 14.5 * K_, BS, 7 * K_), False, 0.9)
    K.pill_label(s, bx + BS / 2, by + 18 * K_ + 3.4, "Ravine 6–8\" wide", 9, 700)
    toks(s, bx, by, K_, "A", [(10, 3), (18, 3), (26, 3)])
    toks(s, bx, by, K_, "B", [(10, 33), (18, 33), (26, 33)])
    _dimv(s, bx + 32 * K_, by, by + 6 * K_, "6\"")
    _dimv(s, bx + 32 * K_, by + 30 * K_, by + 36 * K_, "6\"")


def fig13():
    s = MapSvg(FULL_W)
    set_scale(4.0)
    P = 228
    ys = []
    ys.append(deploy_panel(0, s, "A", "Opposite long edges", "Each party deploys within 6\" of its own long battlefield edge (6\" is the 10.1 step 11 default where the scenario gives no depth).", d_long, row_pitch=P))
    ys.append(deploy_panel(1, s, "B", "Opposite short edges", "Each party deploys within 6\" of its own short battlefield edge (6\" is the 10.1 step 11 default where the scenario gives no depth).", d_short, row_pitch=P))
    ys.append(deploy_panel(2, s, "C", "Roll-off winner chooses the edge", "(1) The Setup Roll-off winner chooses the edge (a long edge, or any battlefield edge, as the scenario states; the 10.1 step 11 default where it is silent). (2) The other party takes the opposite edge. Both are within 6\" of it.", d_choose, row_pitch=P))
    ys.append(deploy_panel(3, s, "D", "Roll-off winner chooses a corner", "(1) The Setup Roll-off winner chooses an 8\"×8\" corner zone (as the scenario states; also the 10.1 step 11 default). (2) The other party deploys in the diagonally opposite corner.", d_corner_choose, row_pitch=P))
    ys.append(deploy_panel(4, s, "E", "Opposite corners, alternate placing", "Opposite 8\"×8\" corner zones. Parties alternate placing Heroes within their zone, starting with the party that lost the Setup Roll-off (stated, or the 10.1 step 11 default).", d_corner_alt, row_pitch=P))
    lx, ly = 2 * 168 + 4, P + 22
    yk = K.strip_for(s, lx, ly, 160, {"hero-A": "Party A Heroes (enlarged)", "hero-B": "Party B Heroes (enlarged)", "zone-A": "Party A zone", "zone-B": "Party B zone"}, title="Key (full key: FIG-20)")
    y = max(ys[3], ys[4], yk) + 6
    yl = s.para(0, y, "Zones and bands are drawn to scale on a 36\"\u00d736\" battlefield (4 pt per inch); Hero markers are enlarged. North and South are the short edges and East and West the long edges, even on a square battlefield (10.1). Each party may field 1\u20134 Heroes; two or three are shown. Where a scenario states no depth or zone size (Sun-Drowned 2 and 3, The Mire 3, 5 and 6), the 10.1 step 11 default applies: 6\" from the edge, 8\"\u00d78\" corners. Where it states no placing order (these, Pale City 1 and most edge scenarios), Heroes are placed alternately from the Roll-off loser. Where only \"opposite battlefield edges\" are named, the Roll-off winner chooses the edge.", FULL_W, 9, lead=10.4)
    return s, yl + 2


def fig14():
    s = MapSvg(FULL_W)
    set_scale(3.3)
    s.add_def('<clipPath id="qclip"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (f1(2 * 126 + 4), f1(22), f1(BS), f1(BS)))
    ys = []
    kw = dict(cols=4, row_pitch=0, pitch_x=126, cap_w=119)
    ys.append(deploy_panel(0, s, "A", "Trail", "The Setup Roll-off winner chooses the short edge where the Trail enters and deploys within 6\" of it with at least two Heroes, or its only Hero, on the Trail. The other party does the same at the opposite short edge. The Trail is 3–4\" wide and runs the full length.", d_trail, **kw))
    ys.append(deploy_panel(1, s, "B", "One shared edge", "Both parties deploy along the same short edge (the start side of the Chasm) within 8\" of it, placing Heroes alternately starting with the party that lost the Setup Roll-off. No Hero is placed within 6\" of an opposing Hero.", d_chasm, **kw))
    ys.append(deploy_panel(2, s, "C", "Central Safe Zone", "Both parties deploy inside a central 8\"×8\" Safe Zone (shown enlarged: detail of the centre, 6.6 pt per inch), placing Heroes alternately starting with the party that lost the Setup Roll-off. No Hero is placed within 3\" of an opposing Hero.", d_quake, frame=True, **kw))
    ys.append(deploy_panel(3, s, "D", "Across a Ravine", "Opposite short edges, within 6\" of the edge, on higher ground outside the Ravine (6–8\" wide, perpendicular to the long edges).", d_ravine, **kw))
    y = max(ys) + 6
    y = K.strip_for(s, 0, y, FULL_W, {"hero-A": "Party A Heroes (enlarged)", "hero-B": "Party B Heroes (enlarged)", "ter-chasm": "Chasm", "ter-difficult": "Ravine floor (Difficult Terrain)"}, title="Key (full key: FIG-20)")
    yy = s.para(0, y + 4, "Zones, the Trail, the Chasm and the Ravine are drawn to scale on a 36\"×36\" battlefield (3.3 pt per inch); Hero markers are enlarged. Zone-depth dimensions show the stated limits. In panels B and C no Hero is placed within the stated distance of an opposing Hero: the ring (B, 6\", from a Party A Hero's edge; C, 3\") marks that distance, and the dimension line between the nearest opposing Heroes runs between their closest edges (2.6), 7\" in B and 4\" in C, both outside the limit. Panel B is measured between drawn marker edges; panel C markers are drawn at their true 1\" size. Where the source gives a range (Trail 3–4\", Ravine 6–8\"), a value inside the range is drawn and its position is schematic.", FULL_W, 9, lead=10.4)
    return s, yy + 2


# ---------------------------------------------------------------------------
# FIG-15  Chasm Crossing: ledges and objective placement
# ---------------------------------------------------------------------------
def fig15():
    s = MapSvg(FULL_W)
    k = 4.3
    side = 36 * k
    panel_title(s, 0, 0, "A", "The Chasm Crossing")
    bx, by = 4, 26
    board(s, bx, by, side)
    # start-side deployment zone (8" from the short edge), shared by both parties
    zone(s, bx, by, k, 0, 0, 36, 8, "AB")
    # chasm 14..22 inches from the start edge
    K.terrain_shape(s, "chasm", "rect", (bx, by + 14 * k, side, 8 * k), False, 0.9)
    # path of ledges: 4 narrow platforms bridging the chasm along the middle (schematic proportions)
    lx = bx + side * 0.5
    ledge_w, ledge_l, gap = 7.0, 5.0, 4.6
    top = by + 14 * k + 0.3
    for i in range(4):
        y0 = top + i * (ledge_l + gap)
        K.terrain_shape(s, "crumbling" if i == 1 else "ledge", "rect", (lx - ledge_w / 2, y0, ledge_w, ledge_l), False, 1.3)
    K.pill_label(s, lx + 11, top + 17, "Path of Ledges", 9, 700, "start")
    K.pill_label(s, bx + 5, by + 18 * k + 3.4, "Chasm 8\" wide", 9, 700, "start")
    # start-side tokens
    toks(s, bx, by, k, "A", [(5, 3), (9.5, 3)], 3.8)
    toks(s, bx, by, k, "B", [(24.5, 3), (29, 3)], 3.8)
    # objectives
    mx, my = lx, by + 11 * k
    K.marker(s, "obj", mx, my, False, 5.0)
    sx_, sy_ = lx, by + 25 * k
    K.marker(s, "obj", sx_, sy_, False, 5.0)
    K.pill_label(s, mx + 9, my + 3.4, "Survey Map", 9, 700, "start")
    K.pill_label(s, sx_ + 9, sy_ - 1.0, "Cartographer's", 9, 700, "start")
    K.pill_label(s, sx_ + 9, sy_ + 9.4, "Stone", 9, 700, "start")
    # 3" dimensions: Map to the first ledge, last ledge to the Stone (marker centres to the Chasm edges)
    K.dim_labeled(s, lx - 14, my, lx - 14, by + 14 * k, "3\"", 2.5, off=9)
    K.dim_labeled(s, lx - 14, by + 22 * k, lx - 14, sy_, "3\"", 2.5, off=9)
    K.pill_label(s, bx + side - 4, by + 6.3 * k + 6, "start side", 9, 600, "end")
    K.pill_label(s, bx + side - 4, by + 31 * k, "delivery side", 9, 600, "end")
    s.htext(bx + side, by + side + 12, "Schematic - not to scale", 9, 600, "end", "#333")
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
    y = K.step_list(s, rx, y, notes, rw, gap=5)
    y += 2
    y = K.strip_for(s, rx, y, rw, {"hero-A": "Party A", "hero-B": "Party B", "zone-AB": "Zone both use", "ter-chasm": "Chasm", "obj": "Objective",
                                  "ledge": "Ledge", "ledge-crumbling": "Crumbling Ledge"}, title="Key (FIG-20)")
    # ---------------- bottom: Chasm Fall, with the Fly/Climb exceptions ----------------
    y = max(y, by + side + 18) + 1
    panel_title(s, 0, y, "C", "Chasm Fall (Undermarches 2 Special Rules)")
    y += 22
    falls = [
        "**Chasm Fall:** a combatant Pushed off a Ledge into the Chasm, or that fails a Crumbling Ledge Check and falls, is immediately removed from play. A Hero is Defeated and makes a normal Injuries Roll. A non-Hero is resolved as though reduced to 0 HP. This replaces the normal Falling rule. Any carried items, including the Survey Map, fall into the Chasm and are lost.",
        "**Hero or Hireling with a Fly or Climb Speed** that would fall may immediately spend 1 unspent AP, including AP reserved for Reactions, to catch itself. Place it Prone in the nearest legal space on a Ledge, and end its current movement. If it cannot spend the AP, resolve the Chasm Fall normally.",
        "**Monster with a Fly or Climb Speed** that would fall is placed Prone in the nearest legal space on a Ledge, and its activation ends.",
    ]
    for i, st in enumerate(falls, 6):
        lines = wrap(st, FULL_W - 2 * 6.6 - 6, 9)
        K.step(s, 6.6, y + 6.6 - 1.6, i, 6.6)
        for kk, ln in enumerate(lines):
            s.text(2 * 6.6 + 6, y + 6 + kk * 10.5, ln, 9)
        y += max(13.2, len(lines) * 10.5) + 4
    return s, y - 3


# ---------------------------------------------------------------------------
# FIG-16  PvPvE interaction: Whispering Grove
# ---------------------------------------------------------------------------
def fig16():
    s = MapSvg(FULL_W)
    k = 10.0
    panel_title(s, 0, 0, "A", "The Whispering Grove (10.4, Greenmark 2)")
    bx, by, side = 4, 26, 196
    board(s, bx, by, side, frame=True)
    cx, cy = bx + side / 2, by + side / 2 - 2
    K.terrain_shape(s, "open", "circle", (cx, cy, 6.75 * k), False, 1.2)
    R = 4.04
    stones = [(cx, cy - R * k), (cx - 3.5 * k, cy + 2.02 * k), (cx + 3.5 * k, cy + 2.02 * k)]
    for (x, y) in stones:
        K.marker(s, "obj", x, y, False, 5.5)
    K.dim_labeled(s, stones[1][0], stones[1][1] + 17, stones[2][0], stones[1][1] + 17, "6–8\"", 2.5)
    ha = (stones[0][0] + 13, stones[0][1] - 3.6)
    hb = (stones[1][0] - 14, stones[1][1] - 2)
    K.hero(s, "A", ha[0], ha[1], 5.5)
    K.hero(s, "B", hb[0], hb[1], 5.5)
    # Antlered Warden (Large, 2" square) adjacent to the first Stone a Hero Interacts with (here the Stone the Party A Hero uses)
    wx, wy = stones[0][0], stones[0][1] + 16.5
    K.monster(s, "L", wx, wy, False, k)
    # Random Monster Group 2: inside the Clearing, 4" from its edge (radius 6.75" - 4" = 2.75" from the Clearing centre)
    ang = math.radians(30)
    gx, gy = cx + 2.75 * k * math.cos(ang), cy - 2.75 * k * math.sin(ang)
    ex_, ey_ = cx + 6.75 * k * math.cos(ang), cy - 6.75 * k * math.sin(ang)
    assert abs(math.hypot(ex_ - gx, ey_ - gy) - 4.0 * k) < 1e-9
    assert all(math.hypot(gx - sx, gy - sy) > 6.5 + 5.5 for (sx, sy) in stones) and math.hypot(gx - wx, gy - wy) > 17
    K.dim_labeled(s, gx, gy, ex_, ey_, "4\"", 2.5, off=11)      # from the group's marker centre to the Clearing edge
    K.monster(s, "M", gx, gy, False)                              # marker drawn over the dimension's start
    K.step(s, ha[0] + 12, ha[1] - 10, 1, 6.0)
    K.step(s, hb[0], hb[1] - 13, 2, 6.0)
    K.step(s, wx - 19, wy - 8, 3, 6.0)
    K.step(s, gx + 12, gy + 8, 6, 6.0)
    K.target_line(s, wx - 11, wy + 2, hb[0] + 7, hb[1] - 4)
    K.pill_label(s, cx, by + side - 8, "Central Clearing: about 12–15\" across", 9, 600)
    ycap = s.para(bx, by + side + 11, "Detail of the centre of the battlefield (10 pt per inch; Clearing drawn 13.5\" across; positions schematic).", 190, 9, 600, lead=10.4, fill="#333")
    # ---------------- right: sequence ----------------
    rx = side + 26
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Two parties, one Monster (PvPvE)")
    y = 24
    notes = [
        "**Activate a Stone (10.4):** a Hero adjacent to a Standing Stone uses Interact [2 AP] and makes a SPI Check. A stone is claimed by only one party. Here a Party A Hero Interacts with a Stone first.",
        "**Rival attempt:** a Party B Hero later attempts to activate another Stone.",
        "**Antlered Warden:** not placed at setup. When a Hero first Interacts with a Standing Stone, it is placed adjacent to that Stone (here, the Party A Hero's Stone) and is Awake when placed.",
        "**Monster Phase:** the Warden's Target Priority is the valid Hero who most recently activated or attempted to activate a Standing Stone, here the Party B Hero. If no listed target is valid, the normal Monster target priorities apply (9.5 E).",
        "**AI Step 1, Entangling Roots:** if the Primary Target is within 8\" and not Immobilized, it must pass a DEX Check or become Immobilized. The activation then ends.",
        "**Random Monster Group 2:** placed inside the Central Clearing, 4\" from its edge, Resting. Groups 1 and 3 (near a Stone and a Treasure Chest) are not drawn.",
    ]
    y = K.step_list(s, rx, y, notes, rw, gap=5)
    yk = K.strip_for(s, 0, max(y, ycap) + 4, FULL_W, {"hero-A": "Party A Hero", "hero-B": "Party B Hero", "mon-L": "Antlered Warden (2\"\u00d72\")", "mon": "Monster Group 2",
                                                      "obj": "Standing Stone", "los": "Warden's target", "ter-open": "Central Clearing"}, title="Key (full key: FIG-20)")
    H = yk
    return s, H + 2
