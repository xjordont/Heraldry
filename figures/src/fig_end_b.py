"""FIG-65 .. FIG-71: end-of-section diagrams for Chapters 3 to 5 (Initiative Phase, End of Round, Timing Rules,
Reactions, Illegal Actions, Push and Trip, Multiple Attacks).  Every rule shown is stated in the active manuscript snapshot (source/versions.json)
(active snapshot per source/versions.json); line numbers are recorded in figdata_end_b.py.  Same visual grammar as fig_seq.py / fig_spatial.py."""
import re
from svgkit import *

MAXH = {65: 320, 66: 440, 67: 250, 68: 345, 69: 380, 70: 235, 71: 290}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def mh(text, w, size=9, lead=10.8, pad=4, head=False):
    """Height that svgkit.box would return for text at width w."""
    lines = [text] if isinstance(text, str) else text
    n = sum(len(wrap(t, w - 2 * pad, size)) for t in lines)
    return n * lead + 2 * pad - 1.5 + ((lead + 1) if head else 0)


def card(s, x, y, w, text, fill=WHITE, sw=0.9, pad=4, minh=0, anchor="start", head=None):
    h = max(mh(text, w, pad=pad, head=bool(head)), minh)
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=sw, rx=2.5)
    lines = [text] if isinstance(text, str) else text
    wrapped = []
    for t in lines:
        wrapped += wrap(t, w - 2 * pad)
    ty = y + pad + 7.4
    tx = x + pad if anchor == "start" else x + w / 2
    if head:
        s.text(tx, ty, head, 9, 700, anchor)
        ty += 11.8
    for ln in wrapped:
        s.text(tx, ty, ln, 9, 400, anchor)
        ty += 10.8
    return h


def stepcard(s, x, y, w, n, text, fill=WHITE, minh=0):
    """Card with a numbered black circle at the left."""
    lines = wrap(text, w - 30)
    h = max(len(lines) * 10.8 + 6, 24, minh)
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=0.9, rx=2.5)
    callout(s, x + 12, y + 12, n)
    ty = y + 10.5
    for ln in lines:
        s.text(x + 25, ty + 2, ln, 9)
        ty += 10.8
    return h


def hbar(s, x, y, w, title, num=None, ref=None, h=18, rtitle=None):
    s.rect(x, y, w, h, fill=INK, stroke=INK, sw=0.9, rx=2.5)
    tx = x + 6
    if num is not None:
        s.circle(x + 11, y + h / 2, 6.6, fill=WHITE, stroke=None)
        s.text(x + 11, y + h / 2 + 3.2, str(num), 9, 700, "middle", INK)
        tx = x + 22
    s.text(tx, y + h / 2 + 3.3, title, 9.5, 700, "start", WHITE)
    if ref:
        s.text(x + w - 5, y + h / 2 + 3.3, ref, 9, 600, "end", WHITE)


def chip(s, x, y, text, h=14, weight=600, fill=WHITE, color=INK, pad=5, stroke=INK, dash=None, sw=0.8):
    w = tw(text, 9, weight) + 2 * pad
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=2.5, dash=dash)
    s.text(x + w / 2, y + h / 2 + 3.2, text, 9, weight, "middle", color)
    return w


def pip(s, x, y, filled, size=9):
    if filled:
        s.rect(x, y, size, size, fill=INK, stroke=INK, sw=0.8)
    else:
        s.rect(x, y, size, size, fill=WHITE, stroke=INK, sw=1.0)
        s.line(x + 2, y + 2, x + size - 2, y + size - 2, INK, 0.9)
        s.line(x + 2, y + size - 2, x + size - 2, y + 2, INK, 0.9)


def check(s, cx, cy, d=4.2):
    s.polyline([(cx - d, cy), (cx - d * 0.3, cy + d * 0.8), (cx + d, cy - d * 0.8)], INK, 1.8, cap="round")


def ordinal(s, x, y, text, w=22, h=14):
    s.rect(x, y, w, h, fill=PALE, stroke=INK, sw=0.8, rx=2.5)
    s.text(x + w / 2, y + h / 2 + 3.2, text, 9, 700, "middle")


def hline(s, y, x1=0, x2=FULL_W):
    s.line(x1, y, x2, y, MID, 0.6)


# ---------------------------------------------------------------------------
# FIG-65  Initiative Phase (3.2)
# ---------------------------------------------------------------------------
TIE_BREAKERS = [
    "Highest **DEX** among the Heroes used for the Initiative roll, if each side used a Hero.",
    "Starting in Round 2, the side that won Initiative in the previous round.",
    "Roll off again.",
]
EX65 = dict(wardens=17, other=14)


def fig65():
    s = Svg(FULL_W)
    LW = 254
    panel_title(s, 0, 0, "A", "Initiative Phase in order (3.2)")
    steps = [
        "**Refresh AP.** Each combatant on the battlefield with an AP maximum refreshes AP to their normal maximum unless a rule says otherwise.",
        "**Roll.** Competitive play: each side rolls 1d20 and adds its Party Leader's INT and SPI (panel B).",
        "**Compare.** The higher total wins Initiative for the round. A tie goes to the tie-breakers (panel C).",
        "**Choose.** The side that wins Initiative chooses which side takes the first Party Phase activation. Sides then alternate, beginning with that side (3.3).",
        "**Start of round.** Resolve effects that occur at the start of the round. If 2 or more would resolve at the same time, use 3.6 Timing Rules.",
    ]
    y = 20
    for i, t in enumerate(steps, 1):
        h = stepcard(s, 0, y, LW, i, t)
        y += h
        if i < len(steps):
            vflow_arrow(s, 12, y + 0.5, y + 8.5)
            y += 8
    ya = y
    # ---- panel E: source example (left, under the steps)
    y += 7
    panel_title(s, 0, y, "E", "Source example: start of Round 3 (3.2)")
    y += 18
    scale = 7.5
    for name, val, fill in (("Road Wardens", EX65["wardens"], INK), ("Opposing side", EX65["other"], LIGHT)):
        s.text(0, y + 9, name, 9, 600)
        s.rect(84, y, val * scale, 12, fill=fill, stroke=INK, sw=0.8)
        s.text(84 + val * scale + 4, y + 9.4, "total %d" % val, 9, 700)
        y += 14.5
    y = s.para(0, y + 8, "Both sides refresh AP. The Road Wardens win Initiative and choose to act second. A Power that lasts until the start of Round 3 ends after Initiative is determined.", LW, 9, lead=10.6)
    ye = y
    # ---- right column
    RX, RW = 268, FULL_W - 268
    panel_title(s, RX, 0, "B", "Whose modifier is used (competitive)")
    y = 20
    rows = [
        "**Party Leader on the battlefield:** the side adds that Party Leader's INT and SPI.",
        "**Party Leader not on the battlefield:** the side chooses one allied Hero on the battlefield to provide the modifier instead.",
        "**No allied Hero on the battlefield:** the side rolls 1d20 with no ability modifiers.",
    ]
    for i, t in enumerate(rows):
        h = card(s, RX, y, RW, t)
        y += h
        if i < len(rows) - 1:
            vflow_arrow(s, RX + 12, y + 1, y + 10)
            s.text(RX + 22, y + 8.2, "otherwise", 9, 400, "start", "#333")
            y += 10.5
    y += 6
    panel_title(s, RX, y, "C", "Tied Initiative: use the first that resolves it")
    y += 18
    for i, t in enumerate(TIE_BREAKERS):
        lines = wrap(t, RW - 32)
        h = max(len(lines) * 10.6 + 5, 16)
        ordinal(s, RX, y + 1, "%d%s" % (i + 1, ("st", "nd", "rd")[i]), 24, 14)
        for k, ln in enumerate(lines):
            s.text(RX + 30, y + 10.8 + k * 10.6, ln, 9)
        y += h + 2
    y += 4
    panel_title(s, RX, y, "D", "Solo and cooperative play (10.5.4)")
    y += 18
    h = card(s, RX, y, RW, "One allied player rolls 1d20 and adds bonuses granted to the party's Initiative roll, not a Party Leader's INT or SPI. **12 or higher:** Party Phase, then Monster Phase. **11 or lower:** Monster Phase, then Party Phase. This roll replaces competitive side-based Initiative.", fill=PALE, sw=0.7)
    y += h
    yb = y
    return s, max(ya, ye, yb) + 2


# ---------------------------------------------------------------------------
# FIG-66  End of Round (3.5)
# ---------------------------------------------------------------------------
EOR_STEPS = [
    "Resolve ongoing damage, conditions, terrain, weather, Power effects, item effects, Monster effects, and scenario effects that occur at the end of the round",
    "End effects that last until the end of the round, and remove any remaining Temporary HP",
    "Remove any unspent AP",
    "Resolve scenario scoring, extraction, round limits, and victory conditions",
]
EX66 = dict(temp=4, dmg=2, ap=1)


def fig66():
    s = Svg(FULL_W)
    # --- when it begins
    panel_title(s, 0, 0, "A", "When End of Round begins (3.5)")
    x, y = 0, 20
    for t in ("Initiative Phase", "Party Phase", "Monster Phase"):
        w = chip(s, x, y, t, h=16)
        x += w
        hflow_arrow(s, x + 2, x + 14, y + 8)
        x += 16
    chip(s, x, y, "End of Round", h=16, fill=INK, color=WHITE)
    x2 = x + tw("End of Round", 9, 600) + 10
    s.text(x2 + 6, y + 11.4, "Default order shown (3.1).", 9, 400)
    y += 22
    y = s.para(0, y + 7, "The **End of Round** begins after both the **Party Phase** and **Monster Phase** have resolved, including when a specific rule places the Monster Phase first (3.1, 3.4.3). Resolve it in the order below unless a more specific rule says otherwise.", FULL_W, 9, lead=10.6)
    y += 3
    # --- four steps
    LW = 130
    heads = ["End-of-round effects", "End effects, remove Temporary HP", "Remove unspent AP", "Scoring and victory"]
    bodies = [
        None,
        "Effects that last **until the end of the round** end. Any remaining **Temporary HP** is removed (5.4.2). A combatant loses all Temporary HP earlier if reduced to 0 HP, Knocked Out, or removed from the battlefield (5.4.2).",
        "Any unspent AP is removed. Until then it is kept, and Heroes and Hirelings may spend it on Reactions (3.3.2, 3.3.3). It never carries into the following round (3.3.2).",
        "Resolve **scenario scoring, extraction, round limits, and victory conditions**.",
    ]
    RX = LW + 8
    RW = FULL_W - RX
    cats = ["ongoing damage", "conditions", "terrain", "weather", "Power effects", "item effects", "Monster effects", "scenario effects"]
    row1_text = wrap("that occur at the end of the round. If 2 or more resolve at the same time, use 3.6 Timing Rules.", RW - 12)
    for i in range(4):
        if i == 0:
            cx, rows = RX + 5, 1
            for c in cats:
                w = tw(c, 9, 600) + 10
                if cx + w > RX + RW - 4:
                    cx = RX + 5
                    rows += 1
                cx += w + 4
            bh = 5 + rows * 18 + 3 + len(row1_text) * 10.8
        elif i == 3:
            bh = 24
        else:
            bh = len(wrap(bodies[i], RW - 12)) * 10.8 + 8
        h = max(bh, 24)
        s.rect(0, y, LW, h, fill=INK, stroke=INK, sw=0.9, rx=2.5)
        s.circle(12, y + 12, 6.6, fill=WHITE, stroke=None)
        s.text(12, y + 15.2, str(i + 1), 9, 700, "middle", INK)
        for k, ln in enumerate(wrap(heads[i], LW - 30, 9, 700)):
            s.text(24, y + 14.4 + k * 10.8, ln, 9, 700, "start", WHITE)
        s.rect(RX, y, RW, h, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
        if i == 0:
            cx, cy = RX + 5, y + 5
            for c in cats:
                w = tw(c, 9, 600) + 10
                if cx + w > RX + RW - 4:
                    cx = RX + 5
                    cy += 18
                chip(s, cx, cy, c, h=14, fill=PALE, sw=0.7)
                cx += w + 4
            ty = cy + 18 + 8.5
            for k, ln in enumerate(row1_text):
                s.text(RX + 6, ty + k * 10.8, ln, 9)
        elif i == 3:
            s.text(RX + 6, y + 15.4, bodies[3], 9)
        else:
            for k, ln in enumerate(wrap(bodies[i], RW - 12)):
                s.text(RX + 6, y + 14 + k * 10.8, ln, 9)
        y += h
        if i < 3:
            vflow_arrow(s, LW / 2, y + 0.5, y + 8.5)
            y += 8
    # --- outcome
    y += 1
    vflow_arrow(s, LW / 2, y + 0.5, y + 10.5)
    y += 10
    bw = (FULL_W - 12) / 2
    t1 = "**The scenario has ended:** no new round begins."
    t2 = "**The scenario has not ended:** a new round begins with the **Initiative Phase** (3.1, 3.2)."
    hh = max(mh(t1, bw), mh(t2, bw))
    card(s, 0, y, bw, t1, fill=PALE, sw=0.7, minh=hh)
    card(s, bw + 12, y, bw, t2, fill=PALE, sw=0.7, minh=hh)
    y += hh + 7
    hline(s, y)
    y += 5
    # --- example
    panel_title(s, 0, y, "B", "Example (assumed values): one Hero through the End of Round")
    y += 17
    y = s.para(0, y + 7, "Assumes the Hero starts with %d Temporary HP, %d unspent AP, and an effect that lasts until the end of the round, and that an ongoing effect deals %d damage after mitigation at the end of the round." % (EX66["temp"], EX66["ap"], EX66["dmg"]), FULL_W, 9, lead=10.6) + 1
    cw = 70
    cols = [150 + k * cw for k in range(5)]
    ty = y
    s.rect(0, ty, FULL_W, 15, fill=INK, stroke=INK, sw=0.8, rx=2)
    s.text(5, ty + 10.8, "Hero's state", 9, 700, "start", WHITE)
    for k, lab in enumerate(["Start", "After step 1", "After step 2", "After step 3", "After step 4"]):
        s.text(cols[k] + 5, ty + 10.8, lab, 9, 700, "start", WHITE)
    ty += 15
    t_after = EX66["temp"] - EX66["dmg"]
    rows = [
        ("Temporary HP", [str(EX66["temp"]), str(t_after), "0", "0", "0"]),
        ("Until-end-of-round effect", ["active", "active", "ended", "ended", "ended"]),
        ("Unspent AP", [str(EX66["ap"]), str(EX66["ap"]), str(EX66["ap"]), "0", "0"]),
    ]
    for ri, (lab, vals) in enumerate(rows):
        s.rect(0, ty, FULL_W, 15, fill=WHITE if ri % 2 == 0 else PALE, stroke=INK, sw=0.6)
        s.text(5, ty + 10.8, lab, 9, 600)
        for k, v in enumerate(vals):
            s.text(cols[k] + 5, ty + 10.8, v, 9)
        ty += 15
    ty = s.para(0, ty + 11, "Damage at step 1 is subtracted from Temporary HP first (5.4.2), so the Hero loses no HP.", FULL_W, 9, lead=10.6)
    return s, ty + 1


# ---------------------------------------------------------------------------
# FIG-67  Timing Rules (3.6)
# ---------------------------------------------------------------------------
PRIORITY = [
    "Initiative winner's side effects.",
    "Non-Initiative side effects.",
    "Monster Group effects in ascending Monster Group number.",
    "Terrain, weather, hazard, and scenario effects in the order listed by the relevant rule.",
]


def fig67():
    s = Svg(FULL_W)
    LW = 264
    panel_title(s, 0, 0, "A", "Five timing terms, default phase order (3.1, 3.6)")
    bandw = 64
    tx = bandw + 6
    tw_ = LW - tx
    terms = [
        (1, "**At the start of the round:** after AP is refreshed and Initiative is determined, but before the first activation of the round."),
        (2, "**At the start of an activation:** after a combatant is chosen to activate and before they perform actions. Occurs each time a combatant activates."),
        (3, "**During an activation:** while that combatant is spending AP and resolving actions during that activation."),
        (4, "**At the end of an activation:** after that combatant finishes acting during that activation. Occurs each time a combatant activates."),
        (5, "**At the end of the round:** during the distinct End of Round phase, after both the Party Phase and Monster Phase are complete."),
    ]
    y = 20
    ys = {}
    for n, t in terms:
        lines = wrap(t, tw_ - 22)
        h = len(lines) * 10.4 + 4
        callout(s, tx + 8, y + 8.5, n, 6.6)
        for k, ln in enumerate(lines):
            s.text(tx + 20, y + 11.5 + k * 10.4, ln, 9)
        ys[n] = (y, h)
        y += h + 1.5
        if n == 4:
            ys["M"] = (y, 14)
            s.text(tx + 20, y + 10.2, "Monster Phase: not drawn against the terms.", 9, 400, "start", "#333")
            y += 14 + 1.5
    yend = y

    def band(y1, y2, label, fill, dash=None):
        s.rect(0, y1, bandw, y2 - y1 - 1, fill=fill, stroke=INK, sw=0.9, rx=2.5, dash=dash)
        lab = wrap(label, bandw - 4, 9, 600)
        base = (y1 + y2 - 1) / 2 - (len(lab) * 10 - 10) / 2 + 3
        col = WHITE if fill == INK else INK
        for k, ln in enumerate(lab):
            s.text(bandw / 2, base + k * 10, ln, 9, 600, "middle", col)
    band(ys[1][0], ys[1][0] + ys[1][1] + 1.5, "Initiative Phase", PALE)
    band(ys[2][0], ys[4][0] + ys[4][1] + 1.5, "Party Phase: each activation", LIGHT)
    band(ys["M"][0], ys["M"][0] + ys["M"][1] + 1.5, "Monster Phase", WHITE, dash="3 2")
    band(ys[5][0], ys[5][0] + ys[5][1] + 1.5, "End of Round", INK)
    ya = yend
    # ---- right: simultaneous effects
    RX = LW + 14
    RW = FULL_W - RX
    panel_title(s, RX, 0, "B", "Two or more effects at the same time (3.6)")
    y = 20
    y = s.para(RX, y + 7, "**A more specific rule takes priority.** If none is more specific, resolve in this order:", RW, 9, lead=10.4)
    y += 1
    for i, t in enumerate(PRIORITY, 1):
        lines = wrap(t, RW - 24)
        h = len(lines) * 10.4 + 3
        callout(s, RX + 8, y + 7.5, i, 6.6)
        for k, ln in enumerate(lines):
            s.text(RX + 20, y + 10.6 + k * 10.4, ln, 9)
        y += h + 1
    y += 2
    h = card(s, RX, y, RW, "**Solo and cooperative play:** the round's resolved phase order replaces steps 1 and 2. Party Phase first: allied-side effects, then Monster Group effects. Monster Phase first: Monster Group effects, then allied-side effects. Monster Group effects stay in ascending number; terrain, weather, hazard, and scenario effects stay last.", fill=PALE, sw=0.7, pad=3.5)
    y += h + 2
    y = s.para(RX, y + 8, "**Same side, same time:** the Party Leader's controller chooses the order. **Still tied:** use Random Determination to choose the next effect, then repeat until none are tied.", RW, 9, lead=10.4)
    return s, max(ya, y) + 2


# ---------------------------------------------------------------------------
# FIG-68  Reactions (4.5)
# ---------------------------------------------------------------------------
def fig68():
    s = Svg(FULL_W)
    panel_title(s, 0, 0, "A", "The declaration window for one attack or damaging effect (4.5)")
    boxes = [
        (140, "Identify", "If the source has no declaration step, pause before its first damage die, or before applying fixed damage or HP loss, and identify who would be affected."),
        (72, "Redirect", "Resolve target redirection first."),
        (122, "Declare", "Confirm the final targets, then declare all remaining Reactions before any of the source's damage dice are rolled."),
        (154, "Roll and resolve", "Roll damage. A damage roll, Total Miss, Critical Hit, damage application, or Luck reroll never opens a new declaration window for that source."),
    ]
    gap = (FULL_W - sum(b[0] for b in boxes)) / 3.0
    y0 = 31
    H = max(len(wrap(b[2], b[0] - 10)) for b in boxes) * 10.6 + 25
    x = 0
    xs = []
    for i, (w, hd, tx) in enumerate(boxes):
        s.rect(x, y0, w, H, fill=WHITE if i < 3 else PALE, stroke=INK, sw=0.9, rx=2.5)
        callout(s, x + 11, y0 + 11, i + 1)
        s.text(x + 22, y0 + 14, hd, 9.5, 700)
        yy = y0 + 26
        for ln in wrap(tx, w - 10):
            s.text(x + 5, yy, ln, 9)
            yy += 10.6
        xs.append((x, w))
        if i < 3:
            hflow_arrow(s, x + w + 1.5, x + w + gap - 1.5, y0 + 11)
        x += w + gap
    # brackets over the boxes
    yb = y0 - 7
    x1, x2 = xs[0][0], xs[2][0] + xs[2][1]
    for (a, b, lab) in ((x1, x2, "Declaration window open"), (xs[3][0], xs[3][0] + xs[3][1], "Window closed")):
        s.line(a, yb, b, yb, INK, 0.9)
        s.line(a, yb, a, yb + 4, INK, 0.9)
        s.line(b, yb, b, yb + 4, INK, 0.9)
        pill(s, (a + b) / 2, yb + 3.2, lab, 9, 600)
    y = y0 + H + 7
    hline(s, y - 3.5)
    # ---------------- row 2 ----------------
    BX, BW = 0, 140
    CX, CW = 152, 148
    DX, DW = 308, FULL_W - 308
    # ---- B: who may react
    panel_title(s, BX, y, "B", "Who may react, and cost")
    yy = y + 18
    items = [
        "**Heroes and Hirelings:** whenever a rule allows one.",
        "**Allied Summons:** only if a rule explicitly grants them Reactions.",
        "**Monsters:** only if a rule explicitly allows it.",
        "A Reaction needs enough unspent AP to pay its cost. Taking one does not begin or end an activation.",
        "**Block, Dodge, Parry,** and ranged-triggered **Reflex Attack** pay their costs immediately, even if the source later deals no damage or is cancelled.",
        "A Reaction the source's controller uses on the source's own roll does not count against an affected combatant's limit (panel C).",
    ]
    for t in items:
        lines = wrap(t, BW - 10)
        s.text(BX + 1, yy + 7, "•", 9, 700)
        for k, ln in enumerate(lines):
            s.text(BX + 9, yy + 7 + k * 10.6, ln, 9)
        yy += len(lines) * 10.6 + 3
    yB = yy
    # ---- C: one per affected combatant
    panel_title(s, CX, y, "C", "Limit per affected combatant")
    yy = y + 18
    yy = s.para(CX, yy + 7, "Only 1 Reaction may modify how a single action or effect resolves against each affected combatant. A combatant also takes only 1 Reaction in response to the same action or effect, including one that grants a separate action.", CW, 9, lead=10.6)
    yy += 2
    cy = yy + 8
    token(s, "M", CX + 7, cy, 6)
    arrow(s, CX + 15, cy, CX + 28, cy, "los")
    token(s, "A", CX + 37, cy, 6)
    s.text(CX + 48, cy + 3.2, "Source: Ogre attacks Cleric", 9, 600)
    yy = cy + 13
    w1 = chip(s, CX, yy, "Dodge [1 AP]", h=15)
    check(s, CX + w1 + 10, yy + 7.5)
    s.text(CX + w1 + 18, yy + 11, "declared", 9)
    yy += 18
    w2 = chip(s, CX, yy, "Any other modifying Reaction", h=15, dash="3 2")
    xmark(s, CX + w2 + 10, yy + 7.5, 4.2, 1.6, halo=False)
    yy += 18
    yy = s.para(CX, yy + 7, "The Cleric may still react to a different attack later in the round. If 2 or more legal Reactions would modify the same effect, the affected combatant's controller chooses which is declared; the others cost nothing.", CW, 9, lead=10.6)
    yC = yy
    # ---- D: roll-dependent Reactions
    panel_title(s, DX, y, "D", "Reactions that depend on the roll")
    yy = y + 18
    h = card(s, DX, yy, DW, "**Declare in advance.** Choose its target and commit its calculated AP and NRG costs, any consumable, and any limited use. Committed resources cannot be voluntarily spent or committed elsewhere; AP and NRG stay unspent and are still subject to forced loss. Declaring it uses the one-Reaction limit for that source at once.", pad=4)
    yy += h
    half = (DW - 10) / 2.0
    vflow_arrow(s, DX + DW / 4, yy + 0.5, yy + 10.5)
    vflow_arrow(s, DX + 3 * DW / 4, yy + 0.5, yy + 10.5)
    yy += 11
    t1 = "**Trigger occurs,** still legal and affordable: spend the committed costs and resolve it."
    t2 = "**Source ends first:** release the commitments, spending nothing."
    hh = max(mh(t1, half), mh(t2, half))
    card(s, DX, yy, half, t1, minh=hh, fill=PALE, sw=0.7)
    card(s, DX + half + 10, yy, half, t2, minh=hh, fill=PALE, sw=0.7)
    yy += hh + 4
    yy = s.para(DX, yy + 7, "**Source example:** a Hero declares Conviction and commits 1 AP. If a retained base die shows 1, spend it and resolve the printed reroll; if none does, release it.", DW, 9, lead=10.6)
    yD = yy
    return s, max(yB, yC, yD) + 2


# ---------------------------------------------------------------------------
# FIG-69  Illegal Actions (4.6)
# ---------------------------------------------------------------------------
LEGAL_TARGET_TESTS = [
    "matches the rule's target description and count",
    "is within the required distance or range",
    "meets any required LOS or visibility",
    "satisfies every other restriction in that rule",
]


def _numbered(s, x, y, w, n, head, bullets=(), tail=None, minh=0, fill=WHITE, extra=0):
    """Numbered card: head paragraph, optional bullet list, optional tail paragraph; returns height."""
    tw_ = w - 30
    hl = wrap(head, tw_)
    bl = [wrap(b, tw_ - 10) for b in bullets]
    tl = wrap(tail, tw_) if tail else []
    nlines = len(hl) + sum(len(b) for b in bl) + len(tl)
    h = max(nlines * 10.6 + 8 + extra, 24, minh)
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=0.9, rx=2.5)
    callout(s, x + 12, y + 12, n)
    ty = y + 12.5
    for ln in hl:
        s.text(x + 25, ty, ln, 9)
        ty += 10.6
    for b in bl:
        s.text(x + 27, ty, "•", 9, 700)
        for k, ln in enumerate(b):
            s.text(x + 36, ty + k * 10.6, ln, 9)
        ty += len(b) * 10.6
    for ln in tl:
        s.text(x + 25, ty, ln, 9)
        ty += 10.6
    return h


def fig69():
    s = Svg(FULL_W)
    LW = 250
    panel_title(s, 0, 0, "A", "At declaration (4.6)")
    y = 20
    h = _numbered(s, 0, y, LW, 1, "**Target legal?** If the action requires a target, it must be legal when the action is declared and when it resolves. A target is legal only if it:", LEGAL_TARGET_TESTS, "This procedure adds no LOS or visibility requirement to a rule that has none.")
    y += h
    vflow_arrow(s, 12, y + 0.5, y + 8.5)
    y += 8
    h = _numbered(s, 0, y, LW, 2, "**Climb or Jump:** a legal destination must be declared before the **Check** is rolled. If it cannot be, the combatant cannot attempt it.")
    y += h + 5
    h = card(s, 0, y, LW, "If a failed **Check** forces the action to choose another target, the rejected target remains ineligible for that action.", fill=PALE, sw=0.7)
    y += h
    ya = y
    RX = LW + 14
    RW = FULL_W - RX
    panel_title(s, RX, 0, "B", "After declaration: three cases (4.6, 2.6.1)")
    y = 20
    h = _numbered(s, RX, y, RW, 3, "**Illegal before it resolves?** The action fails and has no effect unless a rule says otherwise. Its AP remains spent unless the action was abandoned during Declared State verification (2.6.1).")
    y += h + 5
    h = _numbered(s, RX, y, RW, 4, "**Movement interrupted by a Reaction?** Resolve the interruption under 2.6.1.")
    y += h + 5
    dh = 50
    h = _numbered(s, RX, y, RW, 5, "**Path cannot be completed legally?** If movement has otherwise begun, the combatant stops at the last legal position.", extra=dh)
    # mini strip: six squares, declared path stops where the path becomes illegal
    K = 20
    gx, gy = RX + 28, y + h - dh + 2
    g = Grid(s, gx, gy, 7, 1, K)
    ghost(s, *g.c(0, 0), 6.0)
    cy = g.c(0, 0)[1]
    arrow(s, g.c(0, 0)[0] + 7, cy, g.c(3, 0)[0] - 8, cy, "move")
    g.token(3, 0, "A", r=6.0)
    arrow(s, g.c(3, 0)[0] + 7, cy, g.c(5, 0)[0], cy, "move", forbidden=True)
    s.text(gx + 3.5 * K, gy + K + 10, "stops here", 9, 600, "middle")
    schematic(s, gx, gy + K + 21, "start")
    y += h
    yb = y
    # ---- bottom: AP outcomes
    y = max(ya, yb) + 7
    hline(s, y - 3)
    panel_title(s, 0, y + 1, "C", "What happens to the AP")
    y += 20
    cols = [0, 252, 456]
    s.rect(0, y, FULL_W, 15, fill=INK, stroke=INK, sw=0.8, rx=2)
    for c, hd in zip(cols, ("Situation", "AP outcome", "Source")):
        s.text(c + 5, y + 10.8, hd, 9, 700, "start", WHITE)
    y += 15
    rows = [
        ("Declared movement is illegal and the declaration is abandoned", "No AP is spent", "2.6.1"),
        ("An action becomes illegal before it resolves", "AP remains spent, unless abandoned during Declared State verification", "4.6"),
        ("An effect interrupts movement and the remaining path is illegal", "No AP is refunded", "2.6.1"),
    ]
    for ri, r in enumerate(rows):
        nl = max(len(wrap(v, w_ - 8)) for v, w_ in zip(r, (cols[1] - cols[0], cols[2] - cols[1], 48)))
        rh = nl * 10.6 + 5.4
        s.rect(0, y, FULL_W, rh, fill=WHITE if ri % 2 == 0 else PALE, stroke=INK, sw=0.6)
        for c, v, w_ in zip(cols, r, (cols[1] - cols[0], cols[2] - cols[1], 48)):
            for k, ln in enumerate(wrap(v, w_ - 8)):
                s.text(c + 5, y + 11.5 + k * 10.6, ln, 9)
        y += rh
    y += 3
    y = s.para(0, y + 8, "Combat attacks and combat manoeuvres are resolved in Section 5. Powers are resolved in Section 8.", FULL_W, 9, lead=10.6)
    return s, y + 1


# ---------------------------------------------------------------------------
# FIG-70  Push and Trip (5.6)
# ---------------------------------------------------------------------------
SZ_ORDER = ["S", "M", "L", "H"]


def trip_legal_sizes(actor):
    """Sz values that are 'your Sz or smaller' for an actor of size `actor` (S < M < L < H, the order listed in 2.6)."""
    return [z for z in SZ_ORDER if SZ_ORDER.index(z) <= SZ_ORDER.index(actor)]


def _facts(s, x, y, w, rows, lbl=46):
    for ri, (lab, txt) in enumerate(rows):
        lines = wrap(txt, w - lbl - 6)
        h = len(lines) * 10.6 + 4
        s.rect(x, y, w, h, fill=WHITE if ri % 2 == 0 else PALE, stroke=INK, sw=0.6)
        s.text(x + 4, y + 10.8, lab, 9, 700)
        for k, ln in enumerate(lines):
            s.text(x + lbl, y + 10.8 + k * 10.6, ln, 9)
        y += h
    return y


def fig70():
    s = Svg(FULL_W)
    CW = 246
    X2 = FULL_W - CW
    hbar(s, 0, 0, CW, "Push [1 AP]", ref="5.6.1")
    hbar(s, X2, 0, CW, "Trip [1 AP]", ref="5.6.2")
    # ---- Push diagram (schematic)
    dy = 44
    token(s, "A", 14, dy, 7)
    hp = hexpts(34, dy, 6.5 * 1.08)
    s.polyline(hp + [hp[0]], INK, 1.0, dash="1.6 2")
    token(s, "M", 34 + 50, dy, 6.5)
    arrow(s, 34 + 9, dy, 34 + 50 - 9, dy, "forced")
    dim(s, 34, dy + 14, 34 + 50, dy + 14, "2\"", off=-2, side="below")
    s.text(14, dy - 11, "you", 9, 600, "middle")
    s.text(34, dy - 11, "start", 9, 600, "middle")
    s.text(34 + 50, dy - 11, "end", 9, 600, "middle")
    schematic(s, 0, dy + 34, "start")
    nx = 112
    yy = s.para(nx, dy - 16, "Over an edge or into hazardous terrain: resolve that terrain or **Falling** after the forced movement ends. **Push** never triggers **Reflex Attack**.", CW - nx, 9, lead=10.4)
    ypd = max(yy, dy + 40)
    # ---- Trip diagram
    tx0 = X2
    s.text(tx0, 30, "Example: you are Sz M", 9, 600)
    s.text(tx0, dy + 37, "Sizes listed S, M, L, H (2.6)", 9, 400, "start", "#333")
    token(s, "A", tx0 + 10, dy + 6, 7)
    legal = trip_legal_sizes("M")
    cx = tx0 + 34
    for z in SZ_ORDER:
        s.rect(cx, dy - 3, 20, 18, fill=WHITE if z in legal else PALE, stroke=INK, sw=0.9, rx=2.5)
        s.text(cx + 10, dy + 9.4, z, 9, 700, "middle")
        if z in legal:
            check(s, cx + 10, dy + 24)
        else:
            xmark(s, cx + 10, dy + 24, 3.6, 1.5, halo=False)
        cx += 24
    nx2 = tx0 + 34 + 4 * 24 + 6
    yy2 = s.para(nx2, dy - 16, "Already **Prone**: no additional effect unless a rule says otherwise. A rule may make a target fixed, anchored, or immune to **Trip**.", FULL_W - nx2, 9, lead=10.4)
    ytd = max(yy2, dy + 40)
    # ---- facts
    y = max(ypd, ytd) + 4
    ya = _facts(s, 0, y, CW, [
        ("Target", "One legal combatant, adjacent to you unless a rule says otherwise."),
        ("Check", "**STR Check** with **Disadvantage**."),
        ("Success", "**Push** the target 2\" directly away from you."),
        ("Failure", "Nothing happens."),
    ])
    yb = _facts(s, X2, y, CW, [
        ("Weapon", "You must wield a weapon with the **Trip** trait."),
        ("Target", "Unless a rule says otherwise, a combatant of your **Sz** or smaller within that weapon's **Range** or melee distance."),
        ("Check", "**STR or DEX Check** with **Disadvantage**."),
        ("Result", "On a success the target becomes **Prone**; on a failure nothing happens."),
    ])
    y = max(ya, yb) + 6
    h = card(s, 0, y, FULL_W, "**Both actions:** not an Attack action or weapon attack, no damage dice, and not part of the multi-attack Disadvantage chain. Take them only during your own activation. They do not trigger **Block**, **Dodge**, **Parry**, or rules that trigger when an attack targets a combatant. Each is a hostile action: a **Hidden** actor loses **Hidden** after it resolves. A **Monster** uses them only if its profile, AI rule, scenario rule, or Special Ability says so.", fill=PALE, sw=0.7)
    return s, y + h + 1


# ---------------------------------------------------------------------------
# FIG-71  Multiple Attacks (5.7)
# ---------------------------------------------------------------------------
def chain_status(actions):
    """5.7: weapon attacks count toward the multi-attack Disadvantage chain; Push and Trip do not.
    The second and each later counted attack rolls base damage dice with Disadvantage (no exempting rule assumed).
    Returns (position or None, Disadvantage?) per action."""
    out, n = [], 0
    for a in actions:
        if a in ("Push", "Trip"):
            out.append((None, False))
        else:
            n += 1
            out.append((n, n >= 2))
    return out


EX71 = [
    ("Example 1", ["Attack", "Attack", "Attack"]),
    ("Example 2", ["Attack", "Push", "Attack"]),
]
HERO_AP = 3


def fig71():
    s = Svg(FULL_W)
    AW = 262
    panel_title(s, 0, 0, "A", "The chain in one activation (5.7)")
    y = 20
    y = s.para(0, y + 7, "The second and each later weapon attack a Hero or Hireling makes during one activation rolls its base damage dice with **Disadvantage** unless a rule says otherwise. The chain resets at the start of each of that combatant's activations.", AW, 9, lead=10.6)
    y += 3
    y = s.para(0, y + 7, "Examples (assumed): a Hero with %d AP (2.5). Attack and Push cost 1 AP each (4.2), so each example spends all %d AP. No rule exempts an attack." % (HERO_AP, HERO_AP), AW, 9, lead=10.6) * 1.0
    y += 2
    cw, cg = 82, 8
    for label, acts in EX71:
        s.text(0, y + 8, "**%s:** %s" % (label, ", ".join(acts)), 9)
        y += 12
        status = chain_status(acts)
        for k, (a, (pos, dis)) in enumerate(zip(acts, status)):
            x = k * (cw + cg)
            nochain = pos is None
            s.rect(x, y, cw, 41, fill=PALE if nochain else (LIGHT if dis else WHITE), stroke=INK, sw=0.9 if not nochain else 0.8, rx=2.5, dash="3 2" if nochain else None)
            s.text(x + 5, y + 11.5, "%s [1 AP]" % a, 9, 700)
            s.text(x + 5, y + 23, "not in the chain" if nochain else "chain position %d" % pos, 9)
            s.text(x + 5, y + 34.5, "no damage dice" if nochain else ("**Disadvantage**" if dis else "no Disadvantage"), 9)
            if k < 2:
                hflow_arrow(s, x + cw + 0.5, x + cw + cg - 0.5, y + 26)
        y += 41 + 6
    ya = y
    # ---- panel B
    BX = AW + 14
    BW = FULL_W - BX
    panel_title(s, BX, 0, "B", "What counts toward the chain")
    y = 20
    blocks = [
        ("Counts", "Any attack, unless a rule says it does not.", WHITE),
        ("Counts as one attack", "An attack made with two **Light** weapons. A **Sweep** attack (7.7).", WHITE),
        ("Does not count", "**Push** and **Trip**, which roll no damage dice (5.6). Attacks granted by a **Reaction**, such as **Reflex Attack**, **Counter Attack**, **No Escape**, and **Duelist's Riposte**. A **Riposte** (5.5.3). Any attack whose own rule says it does not count.", PALE),
    ]
    for hd, tx, fill in blocks:
        h = card(s, BX, y, BW, tx, head=hd, fill=fill)
        y += h + 4
    h = card(s, BX, y, BW, "Monsters and Summons do not use this rule. A Summon may make each weapon attack its AP allows unless its own entry limits it. A Monster with **Multi-Attack** makes the attacks that ability lists (9.6).", head="Not used by", fill=WHITE, sw=0.7)
    y += h
    yb = y
    # ---- bottom strip
    y = max(ya, yb) + 4
    hline(s, y - 2)
    y += 4
    t1 = "**Exemptions** lift the Disadvantage but leave the attack in the chain. **Agile** exempts the second weapon attack made with that weapon. **Combat Mastery** exempts a Hero's second weapon attack. **War Master** exempts all of that Hero's melee weapon attacks. Later attacks resolve normally unless another rule applies."
    hh = mh(t1, FULL_W)
    card(s, 0, y, FULL_W, t1, minh=hh, fill=PALE, sw=0.7)
    return s, y + hh + 1


# ---------------------------------------------------------------------------
# self check
# ---------------------------------------------------------------------------
def _source_text():
    """Lines of the active immutable snapshot named in source/versions.json."""
    from manuscript import source_path
    return source_path().read_text(encoding="utf-8").split("\n")


def _svg_texts(svg):
    """(x, y, size, weight, anchor, visible text) for every <text> element of an Svg body."""
    out = []
    for raw in svg.body:
        if not raw.startswith("<text "):
            continue
        m = re.match(r'<text x="([-\d.]+)" y="([-\d.]+)"(.*?)>(.*)</text>$', raw, re.S)
        attrs = m.group(3)
        size = float(re.search(r'font-size="([\d.]+)"', attrs).group(1))
        anchor = (re.search(r'text-anchor="(\w+)"', attrs) or [None, "start"])[1]
        body = m.group(4)
        def unesc(z):
            return z.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if "<tspan" in body:
            parts = [(int(a), unesc(b)) for a, b in re.findall(r'<tspan font-weight="(\d+)">(.*?)</tspan>', body, re.S)]
            width = sum(tw(b, size, a) for a, b in parts)
            txt = "".join(b for _, b in parts)
        else:
            wt = int(re.search(r'font-weight="(\d+)"', raw).group(1))
            txt = unesc(re.sub(r"<[^>]+>", "", body))
            width = tw(txt, size, wt)
        out.append((float(m.group(1)), float(m.group(2)), size, width, anchor, txt))
    return out


def selfcheck_end_b():
    """Geometry, arithmetic, ordering, source-phrase and typography assertions for FIG-65 to FIG-71."""
    import figdata_end_b
    src = _source_text()

    def has(lo, hi, *phrases):
        block = " ".join(src[lo - 1:hi]).replace("**", "").replace("*", "")
        for p in phrases:
            assert p in block, "source lines %d-%d lack %r" % (lo, hi, p)

    # ---- every drawn rule appears in its cited lines of the active snapshot
    has(1025, 1025, "refreshes AP to their normal maximum")
    has(1027, 1027, "1d20", "Party Leader's INT and SPI", "higher total wins Initiative", "10.5.4 PvE Initiative")
    has(1029, 1029, "chooses one allied Hero on the battlefield", "rolls 1d20 with no ability modifiers")
    has(1031, 1035, "Highest DEX among the Heroes used for the Initiative roll, if each side used a Hero",
        "Starting in Round 2, the side that won Initiative in the previous round", "Roll off again")
    has(1037, 1039, "chooses which side takes the first Party Phase activation", "start of the round", "3.6 Timing Rules")
    has(1041, 1041, "17", "14", "act second", "until the start of Round 3 ends after Initiative is determined")
    has(14751, 14756, "Do not add a Party Leader's INT or SPI", "Total 12 or higher", "Party Phase, then the Monster Phase",
        "Total 11 or lower", "Monster Phase, then the Party Phase", "replaces competitive side-based Initiative")
    has(1130, 1137, "begins after both the Party Phase and Monster Phase have resolved", "more specific rule says otherwise",
        "ongoing damage, conditions, terrain, weather, Power effects, item effects, Monster effects, and scenario effects",
        "until the end of the round", "remove any remaining Temporary HP", "Remove any unspent AP",
        "scenario scoring, extraction, round limits, and victory conditions")
    has(1019, 1021, "unless the scenario ends first", "Monster Phase before the Party Phase")
    has(1124, 1126, "If a specific rule placed the Monster Phase before the Party Phase")
    has(1082, 1086, "Unspent AP may be spent later in the same round on Reactions", "never carries into the following round")
    has(1094, 1094, "retained until the end of the round and may still be spent on Reactions")
    has(1584, 1588, "subtract the damage or HP loss from their Temporary HP first", "always expires during step 2",
        "reduced to 0 HP, become Knocked Out, or leave the battlefield")
    has(1143, 1147, "After AP is refreshed and Initiative is determined, but before the first activation of the round",
        "After a combatant is chosen to activate and before they perform actions", "This timing occurs each time a combatant activates",
        "While that combatant is spending AP and resolving actions during that activation",
        "After that combatant finishes acting during that activation",
        "During the distinct End of Round phase, after both the Party Phase and Monster Phase are complete")
    has(1149, 1160, "the more specific rule takes priority", "Initiative winner's side effects", "Non-Initiative side effects",
        "Monster Group effects in ascending Monster Group number", "Terrain, weather, hazard, and scenario effects in the order listed by the relevant rule",
        "replaces steps 1 and 2", "allied-side effects resolve before Monster Group effects",
        "Monster Group effects resolve before allied-side effects", "remain last", "Party Leader's controller chooses the order",
        "use Random Determination to choose the next effect to resolve, then repeat until no tied effects remain")
    has(1427, 1429, "Taking a Reaction does not begin or end an activation", "enough unspent AP to pay its cost")
    has(1431, 1431, "before any of that source's damage dice are rolled", "Resolve target redirection first",
        "confirm the final targets and declare the remaining Reactions", "pause before its first damage die, or before applying fixed damage or HP loss")
    has(1433, 1433, "calculated AP and NRG costs, any consumable, and any limited use", "cannot be voluntarily spent or committed elsewhere",
        "AP and NRG remain unspent and are still subject to forced loss", "release the commitments without spending them")
    has(1435, 1435, "Block, Dodge, Parry, and ranged-triggered Reflex Attack", "pay their costs immediately", "deals no damage, or is cancelled")
    has(1437, 1437, "never opens a new declaration window for that source")
    has(1441, 1441, "Conviction", "1 AP", "retained base die shows 1", "release the AP commitment")
    has(1443, 1443, "Each allied Summon may spend unspent AP on Reactions only if a rule explicitly grants",
        "Monsters do not take Reactions unless a rule explicitly allows it")
    has(1445, 1445, "only one Reaction in response to the same action or effect", "Reactions that grant a separate action")
    has(1433, 1433, "immediately uses the normal one-Reaction limits for that source")
    has(1447, 1447, "An Ogre attacks a Cleric", "1 AP to Dodge", "only 1 Reaction may modify a single action or effect against each affected combatant",
        "different attack later in the round")
    has(1449, 1449, "the affected combatant's controller chooses which one is declared", "do not spend the costs of the others",
        "source's controller to modify the source's own roll does not count")
    has(1457, 1463, "legal when the action is declared and when it resolves", "rejected target remains ineligible",
        "matches the rule's target description and count", "within the required distance or range", "required LOS or visibility",
        "does not add an LOS or visibility requirement", "cannot attempt it", "it fails and has no effect unless a rule says otherwise",
        "AP remains spent unless the action was abandoned during Declared State verification")
    has(1465, 1467, "interrupted by a Reaction, resolve that interruption under 2.6.1", "stops at the last legal position",
        "resolved in Section 5", "resolved in Section 8")
    has(644, 650, "An abandoned declaration costs no AP", "Do not refund any AP spent on that movement")
    has(1719, 1727, "Neither action is an Attack action or weapon attack", "neither rolls damage dice", "multi-attack Disadvantage chain",
        "only during their own activation", "do not trigger Block, Dodge, Parry", "hostile action", "lose Hidden after the action resolves",
        "Push target must be adjacent", "Range or melee distance", "profile, AI rule, scenario rule, or Special Ability")
    has(1731, 1735, "STR Check with Disadvantage", "2\" directly away", "nothing happens", "over an edge or into hazardous terrain",
        "Falling after the forced movement ends", "never triggers Reflex Attack")
    has(1739, 1745, "Trip trait", "Sz or smaller", "STR or DEX Check with Disadvantage", "becomes Prone", "fixed, anchored, or otherwise immune to Trip",
        "already Prone, Trip has no additional effect")
    has(1749, 1766, "costs 1 AP unless a rule says otherwise", "Hero or Hireling may make more than one weapon attack",
        "second and each later weapon attack", "rolls its base damage dice with Disadvantage", "resets at the start of each of that combatant's activations",
        "Push and Trip", "Reflex Attack, Counter Attack, No Escape, and Duelist's Riposte", "a Riposte, which is not an attack (5.5.3)",
        "two Light weapons counts as a single attack", "Sweep attack (7.7)",
        "Agile exempts the second weapon attack made with that weapon", "Combat Mastery exempts a Hero's second weapon attack",
        "War Master exempts all of that Hero's melee weapon attacks", "Later attacks resolve normally unless another rule applies",
        "Monsters do not use AP", "Summons and Monsters do not use this rule", "Multi-Attack makes the attacks listed by that ability, as described in 9.6")
    has(572, 572, "Heroes begin each round with 3 AP")
    has(1216, 1217, "Push", "1 AP", "Trip", "1 AP")
    has(1215, 1215, "Attack", "1 AP")
    has(618, 625, "Small (S), Medium (M), Large (L), or Huge (H)")

    # ---- FIG-65
    assert len(TIE_BREAKERS) == 3 and "DEX" in TIE_BREAKERS[0] and "Round 2" in TIE_BREAKERS[1] and TIE_BREAKERS[2] == "Roll off again."
    assert EX65["wardens"] > EX65["other"] and (EX65["wardens"], EX65["other"]) == (17, 14)
    assert all((t >= 12) != (t <= 11) for t in range(-5, 40))          # 12 or higher / 11 or lower partition the totals
    # ---- FIG-66
    assert len(EOR_STEPS) == 4 and EOR_STEPS[2] == "Remove any unspent AP"
    assert EX66["dmg"] <= EX66["temp"] and EX66["temp"] - EX66["dmg"] == 2 and 2 - 2 == 0 and EX66["ap"] - 1 == 0
    # ---- FIG-67
    assert len(PRIORITY) == 4 and PRIORITY[0].startswith("Initiative winner") and PRIORITY[3].startswith("Terrain, weather")
    # ---- FIG-69
    assert len(LEGAL_TARGET_TESTS) == 4
    # ---- FIG-70
    assert trip_legal_sizes("M") == ["S", "M"] and trip_legal_sizes("S") == ["S"] and trip_legal_sizes("H") == SZ_ORDER
    assert trip_legal_sizes("L") == ["S", "M", "L"]
    # ---- FIG-71
    assert chain_status(EX71[0][1]) == [(1, False), (2, True), (3, True)]
    assert chain_status(EX71[1][1]) == [(1, False), (None, False), (2, True)]
    assert all(len(a) == HERO_AP for _, a in EX71) and HERO_AP == 3          # 3 AP at 1 AP per action
    assert chain_status(["Trip", "Attack"]) == [(None, False), (1, False)]

    # ---- rendered output: size, extent, typography
    from make_figures import typography_errors
    heights = {}
    for n in range(65, 72):
        fid = "FIG-%d" % n
        svg, h = globals()["fig%d" % n]()
        heights[fid] = h
        assert svg.w == FULL_W and h <= MAXH[n], "%s height %.1f exceeds %d" % (fid, h, MAXH[n])
        meta = figdata_end_b.META_END[fid]
        text = svg.render(h, title=meta["title"], desc=meta["purpose"])
        assert "href" not in text and "<image" not in text
        for col in re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"', text):
            c = col[1:]
            c = "".join(ch * 2 for ch in c) if len(c) == 3 else c
            assert c[0:2] == c[2:4] == c[4:6], "%s non-gray %s" % (fid, col)
        for sw in re.findall(r'stroke-width="([\d.]+)"', text):
            assert float(sw) >= 0.5, "%s stroke %s" % (fid, sw)
        for x, y, size, w, anchor, txt in _svg_texts(svg):
            assert size >= 9, (fid, txt)
            x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
            assert x0 >= -0.6 and x0 + w <= FULL_W + 0.6, "%s text outside width: %r (%.1f..%.1f)" % (fid, txt, x0, x0 + w)
            assert 0 <= y <= h + 0.5, (fid, txt, y, h)
            assert not typography_errors(txt), (fid, txt, typography_errors(txt))
            assert not re.search(r"\bhits?\b", txt.replace("Critical Hit", "").replace("Hit,", ""), re.I), (fid, txt)
            assert "--" not in txt and "..." not in txt, (fid, txt)
        # captions
        cap = meta["caption"]
        assert not typography_errors(cap) and not re.search(r"\bhits?\b", cap.replace("Critical Hit", ""), re.I)
        assert re.search(r"\(see [^)]+\)\.$", cap) and len(re.findall(r"[.!?](?:\s|$)", cap)) <= 3, fid
        assert meta["insert_after"].startswith("B0") and meta["scope"] == "full"
    return heights


