"""FIG-04 .. FIG-09: measurement, grid movement, engagement/reach, LOS/Cover, areas of effect, forced movement."""
import math
from svgkit import *


def _flow_boxes(s, x0, y, boxes, total_w, gap=14, size=9):
    """Row of numbered boxes joined by arrows. boxes = [(heading, text)]. Returns bottom y."""
    n = len(boxes)
    bw = (total_w - gap * (n - 1)) / n
    hs = []
    for i, (hd, tx) in enumerate(boxes):
        lines = wrap(tx, bw - 10, size)
        hs.append(len(lines) * 10.6 + 24)
    H = max(hs)
    for i, (hd, tx) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        s.rect(x, y, bw, H, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
        callout(s, x + 11, y + 11, i + 1)
        s.text(x + 22, y + 14, hd, 9.5, 700)
        yy = y + 26
        for ln in wrap(tx, bw - 10, size):
            s.text(x + 5, yy, ln, size)
            yy += 10.6
        if i < n - 1:
            hflow_arrow(s, x + bw + 1.5, x + bw + gap - 1.5, y + 11)
    return y + H


def fig04():
    s = Svg(FULL_W)
    C = 16.0  # scale used in panels A and C : 1 inch = 16 pt (schematic)
    # ---------------- Panel A: Tabletop ----------------
    panel_title(s, 0, 0, "A", "Tabletop Mode (2.6)")
    ax, ay = 4, 30
    s.rect(ax, ay + 6, C, C, fill=WHITE, stroke=INK, sw=0.9)
    token(s, "A", ax + C / 2, ay + 6 + C / 2, 5.5)
    s.rect(ax + 84, ay + 30, 2 * C, 2 * C, fill=PAT["monster"], stroke=INK, sw=1.2)
    p1 = (ax + C, ay + 6 + C)
    p2 = (ax + 84, ay + 30)
    s.line(p1[0], p1[1], p2[0], p2[1], INK, 1.2)
    s.circle(p1[0], p1[1], 2.2, fill=INK, stroke=None)
    s.circle(p2[0], p2[1], 2.2, fill=INK, stroke=None)
    pill(s, (p1[0] + p2[0]) / 2 - 4, p1[1] + 18, "distance", 9, 600)
    s.text(ax, ay + 70, "Measured between the closest points", 9)
    s.text(ax, ay + 81, "of the source and target spaces.", 9)
    yy = s.para(0, ay + 100, "Rules footprints are used, not the miniature's base. Rules that measure from a point use that point.", 150, 9, lead=10.6)
    s.text(0, yy + 6, "Schematic \u2014 not to scale", 9, 600, "start", "#333")
    ya = yy + 8
    # ---------------- Panel B: Grid range ----------------
    bx = 170
    panel_title(s, bx, 0, "B", "Grid Mode: range / distance (2.6)")
    K = 22
    g = Grid(s, bx + 4, 24, 7, 4, K)
    src, tgt = (1, 3), (4, 1)
    pts = [g.c(*src), g.c(2, 2), g.c(3, 1), g.c(*tgt)]
    s.polyline(pts, INK, 1.1)
    g.token(*src, "A", r=7)
    g.token(*tgt, "M", r=6.5)
    for (a_, b_), lab in zip(zip(pts[:-1], pts[1:]), ["1.5", "1.5", "1"]):
        mx, my = (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2
        pill(s, mx + (8 if lab != "1" else 0), my + (8 if lab != "1" else -5), lab, 9, 700)
    s.text(g.c(1, 3)[0], g.oy + 4 * K + 11, "source square", 9, 400, "middle")
    s.text(bx + 4, g.oy + g.height() + 25, "1.5\" + 1.5\" + 1\" = 4\"", 9, 700)
    yy = s.para(bx + 4, g.oy + g.height() + 37, "Orthogonal square = 1\", diagonal square = 1.5\". Count the shortest grid distance without the source square. Obstacles do not change it; check LOS, Cover and terrain separately.", 162, 9, lead=10.6)
    yb = yy
    # ---------------- Panel C: footprints ----------------
    cx0 = 350
    panel_title(s, cx0, 0, "C", "Grid Mode: footprints (2.6)")
    x = cx0 + 2
    y0 = 24
    base = y0 + 3 * C + 14
    items = [("S", 1, "A"), ("M", 1, "A"), ("L", 2, "M"), ("H", 3, "M")]
    xx = x
    for lab, n, kind in items:
        w = n * C
        grid(s, xx, base - w, n, n, C, fill=WHITE)
        if kind == "A":
            token(s, "A", xx + w / 2, base - w / 2, 5.5)
        else:
            s.rect(xx + 2, base - w + 2, w - 4, w - 4, fill=PAT["monster"], stroke=INK, sw=1.2)
        s.text(xx + w / 2, base + 11, lab, 9, 700, "middle")
        s.text(xx + w / 2, base + 21, "%d×%d" % (n, n), 9, 400, "middle")
        xx += w + 9
    yy = s.para(cx0, base + 36, "A combatant occupies the squares of their Sz footprint (S and M 1×1, L 2×2, H 3×3). Their whole footprint must fit in every legal final position.", 152, 9, lead=10.6)
    yc = yy
    # ---------------- Row 2: Declared State ----------------
    y = max(ya, yb, yc) + 10
    s.line(0, y, FULL_W, y, MID, 0.6)
    panel_title(s, 0, y + 6, "D", "Declared movement and positional state (2.6.1)")
    y += 26
    boxes = [
        ("Declare", "Before voluntary or forced movement, declare the intended path and final position (for placement, the final position)."),
        ("Verify", "An opposing player may measure and verify it. If illegal, amend it or choose another action; an abandoned declaration costs no AP."),
        ("Move", "Once movement begins, or a Reaction is declared against it, the declaration cannot be amended or abandoned. A triggered Reaction resolves at the first point on the path where its trigger occurs."),
        ("Declared State", "The actual path and final position become the Declared State until the combatant moves or is moved. If a miniature is moved accidentally, restore it."),
    ]
    yb2 = _flow_boxes(s, 0, y, boxes, FULL_W)
    return s, yb2 + 4


def _centre_label(s, x, y, text, size=9):
    pill(s, x, y, text, size, 600)


def fig05():
    s = Svg(FULL_W)
    C = 20.0
    # ---------------- Panel A: Speed 5" example ----------------
    panel_title(s, 0, 0, "A", "Grid Mode Move, Speed 5\" (4.4.3)")
    g = Grid(s, 4, 24, 7, 5, C)
    start = (0, 4)
    g.token(*start, "A", r=7)
    P = [g.c(0, 4), g.c(1, 4), g.c(2, 3), g.c(3, 2)]
    s.polyline(P, INK, 1.6)
    for q in P[1:]:
        s.circle(q[0], q[1], 2.6, fill=INK, stroke=None)
    x3, y3 = g.c(3, 2)
    x4, y4 = g.c(4, 2)
    arrow(s, x3, y3, x4, y4, "move")
    x5, y5 = g.c(4, 1)
    arrow(s, x3 + 3, y3 - 3, x5 - 2, y5 + 2, "move", forbidden=True)
    for (cx_, cy_), lab, dx, dy in [((1, 4), "1", 0, -4), ((2, 3), "2.5", 13, 17), ((3, 2), "4", -13, 4), ((4, 2), "5", 0, 18)]:
        pill(s, g.ox + cx_ * C + C / 2 + dx, g.oy + cy_ * C + dy, lab, 9, 700)
    pill(s, g.ox + 5 * C + 6, g.oy + 1 * C + 14, "5.5", 9, 700)
    gy = g.oy + g.height()
    s.text(4, gy + 12, "Running total of movement spent (inches).", 9)
    yy = s.para(4, gy + 24, "Speed 5\": one orthogonal square (1\"), two diagonal squares (1.5\" each) = 4\". One more orthogonal square (1\") is allowed; another diagonal (1.5\") would exceed the 1\" remaining.", 235, 9, lead=10.6)
    ya = yy
    # ---------------- Panel B: costs per step ----------------
    bx = 262
    panel_title(s, bx, 0, "B", "Cost of one step into a square (2.6, 2.9.3)")
    gx = bx + 4
    g1 = Grid(s, gx, 26, 3, 3, C)
    g1.token(1, 1, "A")
    for (c, r) in [(1, 0), (0, 1), (2, 1), (1, 2)]:
        pill(s, g1.ox + c * C + 10, g1.oy + r * C + 13.5, "1", 9, 700)
    for (c, r) in [(0, 0), (2, 0), (0, 2), (2, 2)]:
        pill(s, g1.ox + c * C + 10, g1.oy + r * C + 13.5, "1.5", 9, 700)
    s.text(gx + 30, 26 + 3 * C + 12, "Open Terrain", 9, 600, "middle")
    gx2 = gx + 3 * C + 28
    g2 = Grid(s, gx2, 26, 3, 3, C)
    for r in range(3):
        for c in range(3):
            if (c, r) != (1, 1):
                g2.fillcell(c, r, "difficult")
    g2.token(1, 1, "A")
    for (c, r) in [(1, 0), (0, 1), (2, 1), (1, 2)]:
        pill(s, g2.ox + c * C + 10, g2.oy + r * C + 13.5, "2", 9, 700)
    for (c, r) in [(0, 0), (2, 0), (0, 2), (2, 2)]:
        pill(s, g2.ox + c * C + 10, g2.oy + r * C + 13.5, "3", 9, 700)
    s.text(gx2 + 30, 26 + 3 * C + 12, "Difficult Terrain", 9, 600, "middle")
    yy = s.para(bx, 26 + 3 * C + 26, "Numbers are the movement spent to enter that square from the centre square. Difficult Terrain: 2\" orthogonal, 3\" diagonal. If Difficult Terrain, Climb or Jump each apply to the same 1\", use only the single highest cost (4.4.7).", 240, 9, lead=10.6)
    yb = yy
    # ---------------- Row 2 ----------------
    y = max(ya, yb) + 10
    s.line(0, y, FULL_W, y, MID, 0.6)
    y += 6
    # ---------------- Panel C: multi-square ----------------
    panel_title(s, 0, y, "C", "Multi-square footprint (4.4.3)")
    gy0 = y + 24
    g = Grid(s, 4, gy0, 6, 4, C)
    g.block(2, 1, 1, 1, "difficult")
    g.fillcell(2, 1, "difficult")
    g.token(0, 1, "ML", span=2)
    s.rect(g.ox + 1 * C + 1, g.oy + 1 * C + 1, 2 * C - 2, 2 * C - 2, fill="none", stroke=INK, sw=1.2, dash="4 2.5")
    arrow(s, g.pt(1.3, 3.5)[0], g.pt(1.3, 3.5)[1], g.pt(2.5, 3.5)[0], g.pt(2.5, 3.5)[1], "move")
    pill(s, g.pt(4.3, 1.5)[0], g.pt(4.3, 1.5)[1] + 3, "cost 2\"", 9, 700)
    s.text(g.ox + 3 * C + 2, g.oy + 4 * C + 12, "", 9)
    yy = s.para(4, gy0 + 4 * C + 12, "A Large combatant stepping east would occupy a Difficult Terrain square. For each step, use the highest movement cost that applies to any square occupied after the step: this orthogonal step costs 2\".", 235, 9, lead=10.6)
    yc = yy
    # ---------------- Panel D: diagonal corner rule ----------------
    bx = 262
    panel_title(s, bx, y, "D", "Diagonal steps around corners (4.4.3)")
    gx = bx + 4
    cell = 24
    for k in range(2):
        gg = Grid(s, gx + k * 120, gy0, 2, 2, cell)
        if k == 0:
            gg.fillcell(0, 0, "blocking")
            gg.fillcell(1, 1, "blocking")
        else:
            gg.fillcell(0, 0, "blocking")
        gg.token(0, 1, "A")
        a = gg.c(0, 1)
        b = gg.c(1, 0)
        if k == 0:
            arrow(s, a[0] + 4, a[1] - 4, b[0] - 1, b[1] + 1, "move", forbidden=True)
        else:
            arrow(s, a[0] + 4, a[1] - 4, b[0] - 1, b[1] + 1, "move")
        s.text(gg.ox + cell, gy0 + 2 * cell + 12, ["Not allowed", "Allowed"][k], 9, 700, "middle")
    yy = s.para(bx, gy0 + 2 * cell + 24, "A diagonal step needs at least one of the 2 orthogonal intermediate positions to be one the combatant could legally enter. If both are closed, no diagonal step is possible.", 240, 9, lead=10.6)
    yd = yy
    # legend
    y = max(yc, yd) + 6
    y = legend(s, [("A", "Combatant"), ("M", "Large Monster footprint 2×2" if False else "Monster"), ("difficult", "Difficult Terrain"), ("blocking", "Blocking Terrain"), ("move", "Move (permitted)"), ("forbidden", "Not permitted")], 0, y, FULL_W)
    return s, y + 2


# ---------------------------------------------------------------------------
# FIG-06  Engagement, Reach, Reflex Attack
# ---------------------------------------------------------------------------
def fig06():
    s = Svg(FULL_W)
    K = 22
    panel_title(s, 0, 0, "A", "Grid Mode melee bands (5.1)")
    g = Grid(s, 4, 24, 5, 5, K)
    for r in range(5):
        for c in range(5):
            if (c, r) == (2, 2):
                continue
            ring = max(abs(c - 2), abs(r - 2))
            s.rect(g.ox + c * K + 0.4, g.oy + r * K + 0.4, K - 0.8, K - 0.8, fill=LIGHT if ring == 1 else PALE, stroke=None)
    grid(s, g.ox, g.oy, 5, 5, K, fill=None)
    for r in range(5):
        for c in range(5):
            if (c, r) in ((2, 2), (3, 1), (0, 4)):
                continue
            ring = max(abs(c - 2), abs(r - 2))
            s.text(g.ox + c * K + K / 2, g.oy + r * K + K / 2 + 3.2, str(ring), 9, 600, "middle", "#444")
    g.token(2, 2, "A", r=7)
    g.token(3, 1, "B", r=7)
    g.token(0, 4, "M", r=6.5)
    g.token(4, 2, "M", r=6.5) if False else None
    # labels
    s.text(g.ox + 5 * K + 8, g.oy + 12, "Adjacent: the 8 surrounding", 9, 600)
    s.text(g.ox + 5 * K + 8, g.oy + 23, "squares. A melee attack", 9)
    s.text(g.ox + 5 * K + 8, g.oy + 34, "normally targets these.", 9)
    s.rect(g.ox + 5 * K + 8, g.oy + 46, 12, 9, fill=LIGHT, stroke=INK, sw=0.6)
    s.text(g.ox + 5 * K + 24, g.oy + 54, "adjacent (1 square)", 9)
    s.rect(g.ox + 5 * K + 8, g.oy + 60, 12, 9, fill=PALE, stroke=INK, sw=0.6)
    s.text(g.ox + 5 * K + 24, g.oy + 68, "within Reach (2 squares)", 9)
    yy = g.oy + 5 * K + 12
    yy = s.para(4, yy, "**Engaged** = adjacent to at least one enemy: the Party B combatant is adjacent, so both are Engaged. The Monster is within Reach distance but not adjacent, so it does not Engage. Digits give the distance in squares. Tabletop Mode: melee 1\", Reach 2\". Reach does not change Engagement.", 236, 9, lead=10.6)
    ya = yy
    # ---------------- Panel B ----------------
    bx = 262
    panel_title(s, bx, 0, "B", "Leaving melee distance (4.4.4, 5.5.4)")
    K2 = 22
    for k, (ttl, endcol) in enumerate((("Move [1 AP]", 4), ("Shift [1 AP]", 3))):
        gx = bx + 2 + k * 122
        gg = Grid(s, gx, 26, 5, 3, K2)
        for r in range(3):
            for c in range(0, 3):
                if (c, r) != (1, 1):
                    s.rect(gg.ox + c * K2 + 0.4, gg.oy + r * K2 + 0.4, K2 - 0.8, K2 - 0.8, fill=LIGHT, stroke=None)
        grid(s, gg.ox, gg.oy, 5, 3, K2, fill=None)
        gg.token(1, 1, "B", r=5.4)
        ghost(s, *gg.c(2, 1), 5.4)
        a = gg.c(2, 1)
        b = gg.c(endcol, 1)
        arrow(s, a[0] + 6, a[1], b[0] - 6, b[1], "move")
        gg.token(endcol, 1, "A", r=5.4)
        s.text(gg.ox + 2.5 * K2, gg.oy + 3 * K2 + 11, ttl, 9, 700, "middle")
        s.text(gg.ox + 2.5 * K2, gg.oy + 3 * K2 + 22, ["Reflex Attack triggers", "No Reflex Attack"][k], 9, 600, "middle")
        if k == 0:
            callout(s, a[0] + 6, a[1] - 11, 1, 5.6)
    yy = 26 + 3 * K2 + 36
    yy = s.para(bx, yy, "**Move** away from the Party B combatant's melee distance: that combatant may spend 1 AP on a Reflex Attack (base damage dice with Disadvantage). It resolves at the trigger point (1), before the mover leaves. **Shift** (1\", 1 AP) and forced movement do not trigger it.", 242, 9, lead=10.6)
    yb = yy
    y = max(ya, yb) + 6
    y = legend(s, [("A", "Party A"), ("B", "Party B"), ("M", "Monster"), ("lowfill", "adjacent / enemy melee band"), ("palefill", "Reach band"), ("ghost", "starting position"), ("move", "Move / Shift path"), ("step", "step")], 0, y, FULL_W)
    return s, y + 2


# ---------------------------------------------------------------------------
# FIG-07  LOS, Cover, Blocking Terrain, intervening combatants
# ---------------------------------------------------------------------------
def fig07():
    s = Svg(FULL_W)
    K = 20
    PW = 160
    gapx = 12
    rows = 4
    cols = 8
    panels = []

    def base(idx, letter, title):
        col = idx % 3
        row = idx // 3
        ox = col * (PW + gapx)
        oy = row * 178
        panel_title(s, ox, oy, letter, title)
        g = Grid(s, ox, oy + 20, cols, rows, K)
        return g, ox, oy

    # P1 Blocking
    g, ox, oy = base(0, "A", "Blocking Terrain")
    g.block(3, 1, 1, 3, "blocking")
    arrow(s, *g.c(0, 2), *g.c(7, 2), "los")
    xmark(s, g.pt(3, 2.5)[0], g.pt(3, 2.5)[1] , 4.5)
    g.token(0, 2, "A"); g.token(7, 2, "M")
    texts = {0: ("LOS blocked", "The sight line crosses Blocking Terrain (2.7.2).")}
    # P2 corner of two Blocking squares
    g2, ox2, oy2 = base(1, "B", "Corner of 2 Blocking squares")
    g2.fillcell(3, 1, "blocking"); g2.fillcell(4, 2, "blocking")
    arrow(s, *g2.c(2, 3), *g2.c(5, 0), "los")
    xmark(s, g2.pt(4, 2)[0], g2.pt(4, 2)[1], 4.5)
    g2.token(2, 3, "A"); g2.token(5, 0, "M")
    # P3 Cover Terrain across its depth
    g3, ox3, oy3 = base(2, "C", "Across Cover Terrain")
    g3.block(3, 1, 1, 3, "cover")
    arrow(s, *g3.c(0, 2), *g3.c(7, 2), "los")
    xmark(s, g3.pt(3, 2.5)[0], g3.pt(3, 2.5)[1], 4.5)
    g3.token(0, 2, "A"); g3.token(7, 2, "M")
    # P4 grazing
    g4, ox4, oy4 = base(3, "D", "Touching only a corner")
    g4.block(3, 2, 1, 2, "cover")
    arrow(s, *g4.c(2, 1), *g4.c(5, 2), "los")
    s.circle(g4.pt(4, 1.0)[0] if False else g4.pt(4, 2)[0], g4.pt(4, 2)[1], 3.6, fill=WHITE, stroke=INK, sw=1.0)
    g4.token(2, 1, "A"); g4.token(5, 2, "M")
    # P5 intervening combatant + Shift
    g5, ox5, oy5 = base(4, "E", "Intervening combatant")
    g5.token(2, 2, "A")
    ghost(s, *g5.c(0, 2))
    arrow(s, *g5.c(0, 2), *g5.c(7, 2), "los") if False else None
    # first sight line (from ghost position) crossing the Fighter
    a = g5.c(0, 2); b = g5.c(7, 2)
    s.line(a[0], a[1], b[0], b[1], INK, 1.0, dash="4.5 2.8")
    # shift
    arrow(s, a[0] + 5, a[1] - 5, g5.c(1, 1)[0] - 6, g5.c(1, 1)[1] + 5, "move")
    a2 = g5.c(1, 1)
    s.line(a2[0], a2[1], b[0], b[1], INK, 1.0, dash="4.5 2.8")
    g5.token(1, 1, "A"); g5.token(7, 2, "M")
    callout(s, g5.pt(3.8, 3.2)[0], g5.pt(3.8, 3.2)[1], 1, 6.0)
    callout(s, g5.pt(0.35, 1.15)[0], g5.pt(0.35, 1.15)[1], 2, 6.0)
    callout(s, g5.pt(4.6, 1.45)[0], g5.pt(4.6, 1.45)[1], 3, 6.0)
    # P6 Impassable
    g6, ox6, oy6 = base(5, "F", "Impassable Terrain")
    g6.block(3, 1, 1, 3, "impassable")
    arrow(s, *g6.c(0, 2), *g6.c(7, 2), "los")
    g6.token(0, 2, "A"); g6.token(7, 2, "M")
    # texts below
    caps = [
        (g, ox, oy, "LOS blocked.", "The sight line crosses Blocking Terrain (2.7.2)."),
        (g2, ox2, oy2, "LOS blocked.", "Grid Mode: the line touches a corner shared by 2 Blocking squares (2.7.2)."),
        (g3, ox3, oy3, "LOS blocked.", "Grid Mode: the line passes through the interior of a Cover Terrain square that neither occupies (2.7.2)."),
        (g4, ox4, oy4, "LOS clear; target has Cover.", "The line only touches the corner of a non-Open feature, which still grants Cover (2.7.2, 2.8.4)."),
        (g5, ox5, oy5, "Cover at 1; none at 3.", "1 The line crosses an ally that is not Prone or Knocked Out and is the same Sz or larger than the target: Cover. 2 Shift 1 AP clear of the line. 3 No Cover (2.8.4)."),
        (g6, ox6, oy6, "LOS clear; Cover by default.", "A generic Impassable feature provides Cover unless its terrain entry says otherwise (chasms and pits provide none), and does not block LOS (2.9.1, 2.8.4)."),
    ]
    maxy = [0, 0]
    for gg, ox_, oy_, hd, tx in caps:
        yy = gg.oy + rows * K + 12
        s.text(ox_, yy, hd, 9, 700)
        yy2 = s.para(ox_, yy + 10.8, tx, PW, 9, lead=10.4)
        r = 0 if oy_ < 100 else 1
        maxy[r] = max(maxy[r], yy2)
    # since rows are fixed at 178 pitch, make sure captions fit
    assert maxy[0] < 178 - 4, maxy
    y = maxy[1] + 4
    s.line(0, y, FULL_W, y, MID, 0.6)
    y += 4
    yy = s.para(0, y + 8, "**Cover** is binary and does not stack. Against a target with Cover, ranged weapon and thrown attacks roll their base damage dice with Disadvantage. Cover never applies to melee attacks, and Areas of Effect and hazards ignore Cover (2.8.4). Tabletop Mode: the sight line runs centre to centre, and 1\" or more of continuous Cover Terrain between the spaces blocks LOS (2.7.2).", FULL_W, 9, lead=10.6)
    y = legend(s, [("A", "Party A"), ("M", "Monster"), ("blocking", "Blocking"), ("cover", "Cover Terrain"), ("impassable", "Impassable"), ("los", "sight line"), ("blockx", "where LOS is blocked"), ("move", "Shift"), ("ghost", "starting position")], 0, yy + 2, FULL_W)
    return s, y + 2


# ---------------------------------------------------------------------------
# FIG-08  Areas of Effect
# ---------------------------------------------------------------------------
def _seg_hits_open_square(p, q, col, row):
    """True if open segment pq passes through the open interior of grid cell (col,row).
    Coordinates are in cell units (x right, y down)."""
    x0, y0 = p
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    eps = 1e-9
    for (pp, d, lo, hi) in ((x0, dx, col, col + 1), (y0, dy, row, row + 1)):
        if abs(d) < eps:
            if not (lo + eps < pp < hi - eps):
                return False
        else:
            ta, tb = (lo - pp) / d, (hi - pp) / d
            if ta > tb:
                ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
            if t0 >= t1 - eps:
                return False
    return t1 - t0 > eps


def _los_blocked(origin, target, blocking):
    """Grid Mode (2.7.2): blocked if the line crosses a Blocking square's interior or touches a corner shared by 2 Blocking squares."""
    p = (origin[0] + 0.5, origin[1] + 0.5)
    q = (target[0] + 0.5, target[1] + 0.5)
    for (c, r) in blocking:
        if _seg_hits_open_square(p, q, c, r):
            return True
    # corner rule
    for (c, r) in blocking:
        for (c2, r2) in blocking:
            if (c2, r2) <= (c, r):
                continue
            if abs(c - c2) <= 1 and abs(r - r2) <= 1:
                # shared corner points
                xs = set([c, c + 1]) & set([c2, c2 + 1])
                ys = set([r, r + 1]) & set([r2, r2 + 1])
                for x in xs:
                    for y in ys:
                        # does segment pass through the point (x, y)?
                        dx, dy = q[0] - p[0], q[1] - p[1]
                        cross = (x - p[0]) * dy - (y - p[1]) * dx
                        if abs(cross) < 1e-9:
                            t = ((x - p[0]) * dx + (y - p[1]) * dy) / (dx * dx + dy * dy)
                            if 0 <= t <= 1:
                                return True
    return False


def aura_squares(src, radius, blocking=()):
    """Grid Mode Aura: squares whose centre lies within radius of the source square centre (ties included)."""
    out = []
    n = int(math.ceil(radius))
    for dc in range(-n, n + 1):
        for dr in range(-n, n + 1):
            if dc * dc + dr * dr <= radius * radius + 1e-9:
                sq = (src[0] + dc, src[1] + dr)
                if sq in blocking:
                    continue
                out.append((sq, _los_blocked(src, sq, blocking) if (dc or dr) else False))
    return out


def cone_squares(src, length, blocking=()):
    """Cone along +x: apex at origin square centre, far edge `length` wide at distance `length` (ties included)."""
    out = []
    for dx in range(1, length + 1):
        for dy in range(-length, length + 1):
            if abs(dy) <= dx * 0.5 + 1e-9:
                sq = (src[0] + dx, src[1] + dy)
                if sq in blocking:
                    continue
                out.append((sq, _los_blocked(src, sq, blocking)))
    return out


def fig08():
    s = Svg(FULL_W)
    PW, gp = 120, 8
    K = 16
    X = [i * (PW + gp) for i in range(4)]
    # ------------- Panel A: template shapes -------------
    panel_title(s, X[0], 0, "A", "Templates (2.7.3)")
    L = 50
    ox, oy = X[0] + 8, 58
    s.polygon([(ox, oy), (ox + L, oy - L / 2), (ox + L, oy + L / 2)], fill=PAT["aoe"], stroke=INK, sw=1.0)
    token(s, "A", ox, oy, 5.5)
    s.text(ox + 4, oy - L / 2 - 4, "Cone X\"", 9, 700)
    pill(s, ox + L - 8, oy + 3.4, "X\"", 9, 600)
    ox2, oy2 = X[0] + 8, 112
    s.rect(ox2, oy2 - 6, L, 12, fill=PAT["aoe"], stroke=INK, sw=1.0)
    token(s, "A", ox2, oy2, 5.5)
    s.text(ox2 + 4, oy2 - 12, "Line X\"", 9, 700)
    pill(s, ox2 + L - 8, oy2 + 3.4, "X\"", 9, 600)
    ox3, oy3 = X[0] + 36, 164
    s.circle(ox3, oy3, 24, fill=PAT["aoe"], stroke=INK, sw=1.0)
    token(s, "A", ox3, oy3, 5.5)
    s.line(ox3, oy3, ox3 + 24, oy3, INK, 1.0)
    pill(s, ox3 + 13, oy3 - 3, "X\"", 9, 600)
    s.text(ox3 + 28, oy3 - 20, "Aura X\"", 9, 700)
    yy = s.para(X[0], 200, "Line width is 1\" unless listed. A Cone or Line does not affect the combatant it originates from. Tabletop: affected if any part of the footprint is within or touches the boundary.", PW, 9, lead=10.4)
    s.text(X[0], yy + 3, "Schematic \u2014 not to scale", 9, 600, "start", "#333")
    ya = yy + 5
    # ------------- Panel B: aura grid -------------
    panel_title(s, X[1], 0, "B", "Grid: Aura 2\"")
    g = Grid(s, X[1] + 4, 24, 7, 7, K)
    src = (3, 3)
    sq = aura_squares(src, 2)
    for (c, r), _ in sq:
        s.rect(g.ox + c * K + 0.5, g.oy + r * K + 0.5, K - 1, K - 1, fill=PAT["aoe"], stroke=None)
    grid(s, g.ox, g.oy, 7, 7, K, fill=None)
    g.token(3, 3, "A", r=5.5)
    n_sq = len(sq)
    yb = s.para(X[1], g.oy + 7 * K + 12, "Squares whose centre lies within 2\" of the source square's centre (a tie at exactly 2\" is included), including the source square: **%d squares**." % n_sq, PW, 9, lead=10.4)
    # ------------- Panel C: cone grid -------------
    panel_title(s, X[2], 0, "C", "Grid: Cone 3\"")
    g = Grid(s, X[2] + 4, 24, 6, 5, K)
    src = (0, 2)
    cs = cone_squares(src, 3)
    for (c, r), blk in cs:
        s.rect(g.ox + c * K + 0.5, g.oy + r * K + 0.5, K - 1, K - 1, fill=PAT["aoe"], stroke=None)
    grid(s, g.ox, g.oy, 6, 5, K, fill=None)
    ox_, oy_ = g.c(*src)
    s.polygon([(ox_, oy_), (ox_ + 3 * K, oy_ - 1.5 * K), (ox_ + 3 * K, oy_ + 1.5 * K)], fill="none", stroke=INK, sw=1.1)
    g.token(0, 2, "A", r=5.5)
    yc = s.para(X[2], g.oy + 5 * K + 12, "Squares whose centre lies within the cone (ties rounded outward): **%d squares** beyond the origin square. The origin square (the source) is not affected." % len(cs), PW, 9, lead=10.4)
    # ------------- Panel D: blocked -------------
    panel_title(s, X[3], 0, "D", "Blocked by terrain")
    g = Grid(s, X[3] + 4, 24, 6, 5, K)
    blocking = [(2, 3)]
    cs2 = cone_squares(src, 3, blocking)
    for (c, r), blk in cs2:
        if not blk:
            s.rect(g.ox + c * K + 0.5, g.oy + r * K + 0.5, K - 1, K - 1, fill=PAT["aoe"], stroke=None)
    grid(s, g.ox, g.oy, 6, 5, K, fill=None)
    ox_, oy_ = g.c(*src)
    s.polygon([(ox_, oy_), (ox_ + 3 * K, oy_ - 1.5 * K), (ox_ + 3 * K, oy_ + 1.5 * K)], fill="none", stroke=INK, sw=1.1)
    for (c, r) in blocking:
        g.fillcell(c, r, "blocking")
    for (c, r), blk in cs2:
        if blk:
            xmark(s, *g.c(c, r), 4.0, 1.5, halo=True)
    g.token(0, 2, "A", r=5.5)
    yd = s.para(X[3], g.oy + 5 * K + 12, "A square is unaffected if the sight line from the origin to it is blocked by Blocking Terrain, even though the cone covers it.", PW, 9, lead=10.4)
    y = max(ya, yb, yc, yd) + 6
    s.line(0, y, FULL_W, y, MID, 0.6)
    panel_title(s, 0, y + 6, "E", "When one damage roll is shared by several combatants (2.7.3)")
    y += 26
    boxes = [
        ("Declare", "Each affected combatant that can take a legal Reaction may declare at most one (4.5)."),
        ("Roll once", "Roll the shared damage once, unless the effect says otherwise."),
        ("Luck", "Resolve any Luck reroll (2.10) before defence or mitigation begins."),
        ("Resolve", "Using the final roll, each affected combatant separately resolves their Reaction, then applies AD, AV, Resistance, Vulnerability, Immunity and other mitigation (5.1.1)."),
    ]
    y = _flow_boxes(s, 0, y, boxes, FULL_W)
    y += 8
    y = legend(s, [("A", "Source / origin"), ("aoe", "affected square / area"), ("blocking", "Blocking Terrain"), ("blockx", "covered but unaffected (sight line blocked)")], 0, y, FULL_W)
    return s, y + 2


# ---------------------------------------------------------------------------
# FIG-09  Forced movement
# ---------------------------------------------------------------------------
def fig09():
    s = Svg(FULL_W)
    K = 20
    PW = 164
    gap = 6
    # ---------------- Panel A: Push / Pull / Slide ----------------
    panel_title(s, 0, 0, "A", "Push, Pull, Slide (4.4.6)")
    y = 24
    strips = [
        ("Push X\": directly away from the source", "push"),
        ("Pull X\": directly toward the source", "pull"),
        ("Slide X\": in the direction the effect names", "slide"),
    ]
    for ttl, kind in strips:
        s.text(0, y + 8, ttl, 9, 600)
        g = Grid(s, 0, y + 13, 7, 1, K)
        cy = g.c(0, 0)[1]
        if kind == "push":
            g.token(0, 0, "A", r=6.5)
            g.token(1, 0, "M", r=6)
            arrow(s, g.c(1, 0)[0] + 8, cy, g.c(4, 0)[0], cy, "forced")
        elif kind == "pull":
            g.token(6, 0, "A", r=6.5)
            g.token(2, 0, "M", r=6)
            arrow(s, g.c(2, 0)[0] + 8, cy, g.c(5, 0)[0] - 8, cy, "forced")
        else:
            g.token(1, 0, "M", r=6)
            arrow(s, g.c(1, 0)[0] + 8, cy, g.c(5, 0)[0], cy, "forced")
            s.text(g.ox + 6 * K, cy + 3.2, "", 9)
        y += 13 + K + 11
    yy = s.para(0, y + 4, "Forced movement never triggers Reflex Attack. Terrain movement costs count against the listed distance (4.4.7).", PW - 4, 9, lead=10.6)
    ya = yy
    # ---------------- Panel B: Collision ----------------
    bx = PW + gap + 6
    panel_title(s, bx, 0, "B", "Collision (4.4.6)")
    y = 24
    s.text(bx, y + 8, "Impassable Terrain in the path", 9, 600)
    g = Grid(s, bx, y + 13, 7, 1, K)
    cy = g.c(0, 0)[1]
    g.fillcell(4, 0, "impassable")
    g.token(0, 0, "A", r=6.5)
    g.token(1, 0, "M", r=6)
    arrow(s, g.c(1, 0)[0] + 8, cy, g.c(3, 0)[0] - 1, cy, "forced")
    s.line(g.c(3, 0)[0] + 5, cy - 7, g.c(3, 0)[0] + 5, cy + 7, INK, 2.0)
    y2 = y + 13 + K + 11
    s.text(bx, y2 + 8, "Another combatant in the path", 9, 600)
    g = Grid(s, bx, y2 + 13, 7, 1, K)
    cy = g.c(0, 0)[1]
    g.token(0, 0, "A", r=6.5)
    g.token(1, 0, "M", r=6)
    g.token(4, 0, "B", r=6.5)
    arrow(s, g.c(1, 0)[0] + 8, cy, g.c(3, 0)[0] - 1, cy, "forced")
    s.line(g.c(3, 0)[0] + 5, cy - 7, g.c(3, 0)[0] + 5, cy + 7, INK, 2.0)
    y3 = y2 + 13 + K + 11
    yy = s.para(bx, y3 + 4, "The target stops at the last legal position and suffers a Collision. A Collision deals no damage by itself; a rule that deals Collision damage says so.", PW - 4, 9, lead=10.6)
    yb = yy
    # ---------------- Panel C: ledge ----------------
    cx = 2 * (PW + gap) + 12
    cw = FULL_W - cx
    panel_title(s, cx, 0, "C", "Ledge example (4.4.6)")
    y = 38
    K2 = 22
    g = Grid(s, cx, y, 7, 3, K2)
    cyy = g.c(0, 1)[1]
    g.token(0, 1, "A", r=6.5)
    sx = g.c(1, 1)[0]
    ex = sx + 2 * K2
    terrain(s, "impassable", ex, g.oy, g.ox + 7 * K2 - ex, 3 * K2, None)
    s.rect(g.ox, g.oy, 7 * K2, 3 * K2, fill="none", stroke=INK, sw=0.9)
    ghost(s, sx, cyy, 6.5)
    arrow(s, sx + 8, cyy, ex - 7, cyy, "forced")
    token(s, "M", ex, cyy, 6.0)
    s.line(ex, g.oy, ex, g.oy + 3 * K2, INK, 1.6)
    pill(s, ex + (g.ox + 7 * K2 - ex) / 2 + 2, g.oy + 2.3 * K2 + 3.5, "no surface", 9, 600)
    pill(s, ex + (g.ox + 7 * K2 - ex) / 2, g.oy + 2.5 * K2 + 3.5, "edge point \u2190", 9, 600) if False else None
    dim(s, sx, g.oy + 3 * K2 + 8, ex, g.oy + 3 * K2 + 8, "2\"", off=-1, side="below")
    dim(s, sx, g.oy - 8, sx + 3 * K2, g.oy - 8, "Push 3\"", off=-1, side="above")
    callout(s, ex - 13, g.oy + 8, 1, 5.8)
    callout(s, ex + 13, g.oy + 8, 2, 5.8)
    y = g.oy + 3 * K2 + 22
    yy = s.para(cx, y + 4, "Push 3\" toward a ledge 2\" along the path (Skeleton). (1) The missing surface does not stop the push: the Skeleton moves 2\" to the edge point and the forced movement ends. (2) Falling is then resolved from that point. This is not a Collision.", cw, 9, lead=10.6)
    yc = yy
    y = max(ya, yb, yc) + 6
    y = legend(s, [("A", "Pushing source"), ("M", "Target (Skeleton)"), ("B", "Another combatant"), ("impassable", "Impassable Terrain / missing surface"), ("forced", "Forced movement"), ("ghost", "starting position")], 0, y, FULL_W)
    return s, y + 2
