"""FIG-10 .. FIG-12: Monster states, Standard Monster AI Script, target priorities."""
import math
from svgkit import *


def fig10():
    s = Svg(FULL_W)
    aw = 236
    panel_title(s, 0, 0, "A", "Monster Group states (9.3, 9.4)")
    y = 22
    h = box(s, 0, y, aw, "**Setup (9.3):** a Monster Group begins **Resting** unless the scenario says otherwise, has a Guard Point, and each Monster begins within 3\" of the group's starting point.",
            anchor="start", fill=PALE, sw=0.7, pad=5)
    y += h + 10
    # state boxes
    bw = 84
    s.rect(0, y, bw, 22, fill=WHITE, stroke=INK, sw=1.0, rx=2.5)
    s.text(bw / 2, y + 15, "RESTING", 9.5, 700, "middle")
    s.rect(aw - bw, y, bw, 22, fill=INK, stroke=INK, sw=1.0, rx=2.5)
    s.text(aw - bw / 2, y + 15, "AWAKE", 9.5, 700, "middle", WHITE)
    hflow_arrow(s, bw + 3, aw - bw - 3, y + 11)
    s.text((aw) / 2, y + 34, "any wake-up trigger", 9, 600, "middle")
    # one-way note
    y += 44
    yy = s.para(0, y + 8, "**Resting:** does not activate; wakes only when a wake-up rule is met. **Awake:** activates in the Monster Phase and stays Awake for the rest of the adventure.", aw, 9, lead=10.6)
    y = yy + 4
    s.text(0, y + 8, "Wake-up triggers (unless a scenario or stat block says otherwise)", 9, 700)
    y += 14
    trig = [
        "An enemy moves within 6\". No LOS needed.",
        "A visible enemy enters the group's LOS within 12\".",
        "The group suffers damage.",
        "An Explosion, collapsing terrain or a loud effect occurs within 6\".",
        "A scenario rule wakes it.",
    ]
    y = step_list(s, 0, y, trig, aw, gap=3.5)
    h = box(s, 0, y + 2, aw, "A **Hidden** enemy trips the 6\" trigger only within its Hide distance (normally 2\") and remains Hidden unless revealed. Hidden or Invisible enemies do not wake a Resting group through the 12\" LOS trigger unless a rule makes them visible to the group.",
            anchor="start", fill=PALE, sw=0.7, pad=5)
    ya = y + 2 + h
    # ---------------- Panel B: spatial ----------------
    bx = 262
    panel_title(s, bx, 0, "B", "Wake-up by distance and LOS (9.4)")
    cx, cy = bx + 124, 24 + 106
    R6, R12 = 46, 92
    s.circle(cx, cy, R12, fill="none", stroke=INK, sw=1.0, dash="5 3")
    s.circle(cx, cy, R6, fill=PALE, stroke=INK, sw=1.4)
    # monsters
    for dx, dy in ((-7, -5), (7, -4), (0, 7)):
        token(s, "M", cx + dx, cy + dy, 5.8)
    pill(s, cx + 24, cy - R6 + 11, "6\"", 9, 700)
    pill(s, cx - 63, cy - R12 + 20, "12\"", 9, 700)
    # (a) visible enemy within 12" with LOS -> trigger 2
    ax_, ay_ = cx + 70 * math.cos(math.radians(-35)), cy + 70 * math.sin(math.radians(-35))
    arrow(s, ax_, ay_, cx + 8, cy - 4, "los")
    token(s, "A", ax_, ay_, 6.5)
    callout(s, ax_ - 4, ay_ - 15, 2, 6.0)
    # (b) enemy moves within 6" though a Blocking wall is between
    wall_x = cx - 28
    terrain(s, "blocking", wall_x - 3, cy - 20, 6, 40, None)
    bx0, by0 = cx - 88, cy + 10
    bx1, by1 = cx - 40, cy + 10
    token(s, "B", bx0, by0, 6.5)
    arrow(s, bx0 + 8, by0, bx1 - 8, by1, "move")
    ghost(s, bx0, by0, 6.5) if False else None
    token(s, "B", bx1, by1, 6.5)
    callout(s, bx1 - 3, by1 + 16, 1, 6.0)
    # (c) enemy beyond 6", LOS blocked
    wy = cy + 62
    terrain(s, "blocking", cx - 22, wy - 3, 44, 6, None)
    ex_, ey_ = cx, cy + 82
    token(s, "A", ex_, ey_, 6.5)
    arrow(s, ex_, ey_ - 7, cx, cy + 14, "los", forbidden=False)
    xmark(s, cx, wy, 4.2, 1.6)
    s.text(ex_ + 12, ey_ + 3.2, "no wake-up", 9, 700)
    yb = cy + R12 + 8
    # legend / explanation
    ytext = yb + 2
    lines = [("1", "moves within 6\": wakes, although Blocking Terrain stands between"),
             ("2", "visible, within 12\" with LOS: wakes"),
             ("", "outside 6\" with LOS blocked: no wake-up trigger")]
    for n, t in lines[:2]:
        callout(s, bx + 7, ytext + 6, n, 6.0)
        ytext = s.para(bx + 18, ytext + 9, t, FULL_W - bx - 18, 9, lead=10.6) + 3
    s.text(bx, ytext + 7, "× on a sight line: LOS blocked. Third enemy: outside 6\", no LOS.", 9)
    s.text(bx, ytext + 19, "Schematic - not to scale", 9, 600, "start", "#333")
    yb = ytext + 22
    y = max(ya, yb) + 6
    y = legend(s, [("M", "Monster Group"), ("A", "Party A enemy"), ("B", "Party B enemy"), ("blocking", "Blocking Terrain"), ("los", "sight line"), ("move", "enemy movement")], 0, y, FULL_W)
    return s, y + 2


def fig11():
    s = Svg(FULL_W)
    lw, rw = 196, 262
    gap = 46
    rx = lw + gap
    h0 = box(s, 0, 0, FULL_W, "**Before the steps:** determine the Primary Target, applying any Target Priority printed in a Scenario-Specific Monster's AI Steps first; otherwise it is the nearest visible enemy (9.5 E). Re-determine it if it ceases to be legal. The Monster executes the **first valid instruction** and ignores the rest unless a rule says it continues. Monsters do not use AP.",
             anchor="start", fill=PALE, sw=0.7, pad=5)
    y = h0 + 12
    rows = [
        ("AI Step Abilities", "Does the Monster have a listed AI Step ability whose trigger is met?",
         "Resolve the first valid AI Step, in ascending order. A step marked d6 N+ is valid only on a roll of N or higher. The activation ends unless the ability says it continues (9.5 D)."),
        ("Engaged", "Is the Monster Engaged?",
         "Attack the enemy it is Engaged with; if more than one, the one with the lowest current HP (ties: Most Recent Attacker, then Random Determination). Use Multi-Attack if listed; otherwise a legal melee attack, or a legal ranged attack if none is legal. Choose randomly among legal attacks of the required type."),
        ("Visible Target", "Not Engaged, but is an enemy visible?",
         "Move toward the Primary Target and attack if Engaged. For a Knocked Out target, stop within melee distance and attack despite no Engagement. If ranged fire is possible without Engagement, move to the nearest legal firing position and attack; use legal ranged Multi-Attack, otherwise choose randomly among legal ranged attacks."),
        ("Search", "No enemy visible, but is a Hidden enemy within 12\" and LOS?",
         "That enemy's controller makes a DEX Check; on a failure that enemy loses Hidden. If several, choose the nearest, using 9.5 E for ties. The activation then ends."),
        ("No Visible Target", "None of the above applies.",
         "Move toward the Guard Point, objective, patrol route or scenario-directed destination by Movement Priorities (9.5 F)."),
    ]
    for i, (name, cond, out) in enumerate(rows, 1):
        lh = len(wrap(cond, lw - 30, 9)) * 10.6 + 22
        rh = len(wrap(out, rw - 10, 9)) * 10.6 + 8
        H = max(lh, rh, 36)
        # condition box
        s.rect(0, y, lw, H, fill=WHITE, stroke=INK, sw=1.0, rx=2.5)
        callout(s, 13, y + 13, i)
        s.text(26, y + 15, name, 9.5, 700)
        yy = y + 27
        for ln in wrap(cond, lw - 10, 9):
            s.text(5, yy, ln, 9)
            yy += 10.6
        # outcome box
        s.rect(rx, y, rw, H, fill=PALE, stroke=INK, sw=0.8, rx=2.5)
        yy = y + 12
        for ln in wrap(out, rw - 10, 9):
            s.text(rx + 5, yy, ln, 9)
            yy += 10.6
        if i < len(rows):
            hflow_arrow(s, lw + 2, rx - 2, y + H / 2) if False else None
            s.line(lw + 2, y + 13, rx - 7, y + 13, INK, 1.2)
            s.polygon([(rx - 1, y + 13), (rx - 8, y + 9.8), (rx - 8, y + 16.2)], INK)
            s.text(lw + gap / 2 + 1, y + 10, "yes", 9, 700, "middle")
            # no arrow down
            vflow_arrow(s, 30, y + H, y + H + 14)
            s.text(36, y + H + 11, "no", 9, 700)
            y += H + 14
        else:
            hflow_arrow(s, lw + 2, rx - 2, y + 13)
            y += H
    return s, y + 4


def fig12():
    s = Svg(FULL_W)
    PW, gap = 160, 12
    # ---------------- Panel A: primary target ----------------
    panel_title(s, 0, 0, "A", "Primary Target (9.5 E)")
    ox, oy = 0, 22
    s.rect(ox, oy, PW, 112, fill=WHITE, stroke=INK, sw=0.9)
    M = (22, oy + 58)
    E1 = (78, oy + 32)
    E3 = (62, oy + 92)
    E2 = (132, oy + 62)
    token(s, "M", *M, 7)
    arrow(s, M[0] + 6, M[1] - 2, E1[0] - 6, E1[1] + 1, "los")
    arrow(s, M[0] + 8, M[1] + 2, E2[0] - 6, E2[1] - 1, "los")
    token(s, "A", *E1, 6.5)
    token(s, "B", *E2, 6.5)
    # hidden enemy: dotted ring
    s.circle(E3[0], E3[1], 9.5, fill="none", stroke=INK, sw=1.0, dash="1.6 2")
    token(s, "A", *E3, 6.0)
    pill(s, E3[0] + 38, E3[1] + 3.5, "Hidden", 9, 600)
    callout(s, E1[0] + 13, E1[1] - 9, 1, 6.0)
    pill(s, E2[0], E2[1] + 17, "farther", 9, 600)
    yy = s.para(0, oy + 126, "**1 Primary Target:** the nearest visible enemy. The Hidden enemy is nearer but is not a visible enemy, so it is not chosen. Monsters follow priority alone and never favour one player over another (9.5 A).", PW, 9, lead=10.6)
    s.text(0, yy + 4, "Schematic - not to scale", 9, 600, "start", "#333")
    ya = yy + 6
    # ---------------- Panel B: ties ----------------
    bx = PW + gap
    panel_title(s, bx, 0, "B", "Ties (9.5 E)")
    s.rect(bx, oy, PW, 104, fill=WHITE, stroke=INK, sw=0.9)
    Mc = (bx + 24, oy + 52)
    r = 66
    e1 = (Mc[0] + r * math.cos(math.radians(-32)), Mc[1] + r * math.sin(math.radians(-32)))
    e2 = (Mc[0] + r * math.cos(math.radians(32)), Mc[1] + r * math.sin(math.radians(32)))
    s.path("M %s %s A %s %s 0 0 1 %s %s" % (f1(e1[0]), f1(e1[1]), r, r, f1(e2[0]), f1(e2[1])), stroke=INK, sw=0.9, dash="2 2.5")
    token(s, "M", *Mc, 7)
    token(s, "A", *e1, 6.5)
    token(s, "B", *e2, 6.5)
    pill(s, e1[0] + 6, e1[1] + 18, "HP 4", 9, 700)
    pill(s, e2[0] + 6, e2[1] - 12, "HP 7", 9, 700)
    pill(s, bx + 70, oy + 55, "equal distance", 9, 600)
    yy = oy + 104 + 11
    s.text(bx, yy, "Example HP values.", 9, 400)
    yy += 6
    lad = [("1", "Lowest current HP", "HP 4 is chosen"),
           ("2", "Most Recent Attacker", "the tied enemy that most recently caused HP damage or HP loss to this Monster"),
           ("3", "Random Determination", "among the tied targets (2.6.3)")]
    for i, (n, t, d) in enumerate(lad):
        hh = box(s, bx, yy, PW, [d], anchor="start", fill=WHITE, sw=0.9, pad=4, head=None) if False else 0
        lines = wrap("**%s** %s" % (t, "- " + d), PW - 24, 9)
        hh = len(lines) * 10.6 + 6
        s.rect(bx, yy, PW, hh, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
        callout(s, bx + 11, yy + hh / 2, n, 6.0)
        for k, ln in enumerate(lines):
            s.text(bx + 22, yy + 10 + k * 10.6, ln, 9)
        yy += hh
        if i < 2:
            vflow_arrow(s, bx + 11, yy, yy + 11)
            s.text(bx + 20, yy + 8.5, "still tied", 9, 600)
            yy += 11
    yb = yy + 4
    # ---------------- Panel C: blocked route ----------------
    cx0 = 2 * (PW + gap) + 4
    panel_title(s, cx0 - 4, 0, "C", "Blocked Route (9.5 F)")
    K = 18
    g = Grid(s, cx0 - 4, 22, 8, 5, K)
    ring = [(3, 1), (4, 1), (5, 1), (3, 2), (5, 2), (3, 3), (4, 3), (5, 3)]
    for (c, rr) in ring:
        g.fillcell(c, rr, "impassable")
    g.token(0, 2, "M", r=6.5)
    g.token(4, 2, "A", r=6.5)
    g.token(7, 4, "B", r=6.5)
    arrow(s, *g.c(0, 2), *g.c(4, 2), "los")
    # route to E2 around the ring (below)
    pts = [(g.c(0, 2)[0] + 7, g.c(0, 2)[1] + 5), g.c(1, 3), g.c(2, 4), g.c(6, 4)]
    pts = [g.c(0, 2), g.c(1, 3), g.c(2, 4), g.c(6, 4)]
    poly_arrow(s, [(pts[0][0] + 4, pts[0][1] + 4), pts[1], pts[2], (pts[3][0] - 2, pts[3][1])], "move")
    callout(s, g.c(4, 2)[0] + 13, g.c(4, 2)[1] - 12, 1, 6.0)
    callout(s, g.c(7, 4)[0] - 4, g.c(7, 4)[1] - 14, 2, 6.0)
    yy = g.oy + 5 * K + 12
    yy = s.para(cx0 - 4, yy, "**1** The nearest visible enemy cannot be attacked this activation: Impassable Terrain does not block LOS, but closes every route to it this activation for this melee Monster, including Climb and Jump. **2** A legal route reaches another visible enemy, which becomes the new Primary Target.", PW, 9, lead=10.6)
    yc = yy
    y = max(ya, yb, yc) + 6
    s.line(0, y, FULL_W, y, MID, 0.6)
    yy = s.para(0, y + 15, "**Movement Priorities (9.5 F):** (1) shortest legal route; (2) among equally short routes, avoid hazardous terrain if possible; (3) end in the nearest legal position from which the Monster can attack or threaten the target.", FULL_W, 9, lead=10.6)
    y = yy
    y = legend(s, [("M", "Monster"), ("A", "Party A"), ("B", "Party B"), ("impassable", "Impassable Terrain"), ("los", "sight line"), ("move", "movement"), ("step", "step")], 0, y, FULL_W)
    return s, y + 2
