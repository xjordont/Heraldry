"""FIG-01 .. FIG-03: round sequence, activation/AP/Reaction timing, attack sequence."""
from svgkit import *


def fig01():
    s = Svg(FULL_W)
    bw, gap = 114, 16
    y0 = 4
    phases = [
        ("Initiative Phase", "3.2", [
            "Refresh AP for each combatant that has an AP maximum.",
            "Each side rolls 1d20 + its Party Leader's INT and SPI. The higher total wins Initiative.",
            "The winner chooses which side takes the first Party Phase activation.",
            "Resolve start-of-round effects.",
        ]),
        ("Party Phase", "3.3", [
            "Sides alternate activating one eligible allied combatant at a time.",
            "Each combatant may activate once per round.",
            "A side must Pass when it has no eligible combatant.",
            "The phase ends when all sides have Passed.",
        ]),
        ("Monster Phase", "3.4", [
            "Resolve Monster waking rules (9.4).",
            "Activate each Awake Monster Group in ascending group number.",
            "Each Monster follows the Standard Monster AI Script (9.5); Monsters do not use AP.",
        ]),
        ("End of Round", "3.5", [
            "Resolve end-of-round effects.",
            "End effects that last until the end of the round.",
            "Remove unspent AP.",
            "Resolve scoring, extraction, round limits and victory conditions.",
        ]),
    ]
    heights = []
    for i, (name, ref, items) in enumerate(phases):
        x = i * (bw + gap)
        s.rect(x, y0, bw, 22, fill=INK, stroke=INK, sw=0.9, rx=2.5)
        callout(s, x + 12, y0 + 11, i + 1, 6.6)
        s.rect(x + 5.4, y0 + 4.4, 13.2, 13.2, fill=WHITE, stroke=None)  # white ring for numeral
        callout(s, x + 12, y0 + 11, i + 1, 6.6)
        s.text(x + 22, y0 + 15, name, 9.5, 700, "start", WHITE)
        yy = y0 + 22 + 3
        body_start = yy
        ty = yy + 4
        for it in items:
            lines = wrap(it, bw - 15, 9)
            s.text(x + 5, ty + 7, "•", 9, 700)
            for k, ln in enumerate(lines):
                s.text(x + 12, ty + 7 + k * 10.6, ln, 9)
            ty += len(lines) * 10.6 + 3.5
        h = ty - body_start + 4
        heights.append(h)
        s.text(x + bw - 4, y0 + 15, ref, 9, 600, "end", WHITE)
    H = max(heights)
    for i in range(4):
        x = i * (bw + gap)
        s.rect(x, y0 + 25, bw, H, fill="none", stroke=INK, sw=0.9, rx=2.5)
        if i < 3:
            hflow_arrow(s, x + bw + 1.5, x + bw + gap - 1.5, y0 + 11)
    # loop back arrow
    yb = y0 + 25 + H + 10
    x_end = 3 * (bw + gap) + bw / 2
    x_start = bw / 2
    s.line(x_end, y0 + 25 + H, x_end, yb, INK, 1.2)
    s.line(x_end, yb, x_start + 0, yb, INK, 1.2)
    head, _ = (None, None)
    s.line(x_start, yb, x_start, y0 + 25 + H + 2, INK, 1.2)
    s.polygon([(x_start, y0 + 25 + H), (x_start - 3.4, y0 + 25 + H + 7), (x_start + 3.4, y0 + 25 + H + 7)], INK)
    pill(s, (x_start + x_end) / 2, yb + 3.2, "Next round begins after End of Round, unless the scenario has ended", 9, 600, border=None)
    # exception strip
    ye = yb + 14
    s.rect(0, ye, FULL_W, 40, fill=PALE, stroke=INK, sw=0.7, rx=2.5)
    s.text(6, ye + 12, "Exception (3.1, 3.4.3):", 9, 700)
    s.text(6 + tw("Exception (3.1, 3.4.3):", 9, 700) + 4, ye + 12,
           "if a specific rule places the Monster Phase before the Party Phase, both phases", 9)
    s.text(6, ye + 23, "still resolve once each before End of Round. Order then: Initiative → Monster → Party → End of Round.", 9)
    # mini chips
    chips = ["Initiative", "Monster", "Party", "End of Round"]
    cx = 6
    cy = ye + 28
    for k, c in enumerate(chips):
        w = tw(c, 9, 600) + 8
        s.rect(cx, cy, w, 10.5, fill=WHITE, stroke=INK, sw=0.6, rx=2)
        s.text(cx + w / 2, cy + 8.2, c, 9, 600, "middle")
        cx += w
        if k < 3:
            s.text(cx + 5, cy + 8.6, "→", 9, 600, "middle")
            cx += 10
    H_total = ye + 44
    return s, H_total


def _pip(s, x, y, filled, size=11):
    if filled:
        s.rect(x, y, size, size, fill=INK, stroke=INK, sw=0.8)
    else:
        s.rect(x, y, size, size, fill=WHITE, stroke=INK, sw=1.0)
        s.line(x + 2, y + 2, x + size - 2, y + size - 2, INK, 0.9)
        s.line(x + 2, y + size - 2, x + size - 2, y + 2, INK, 0.9)


def fig02():
    s = Svg(FULL_W)
    # ---------------- Panel A: activation steps ----------------
    ax, aw = 0, 232
    panel_title(s, ax, 0, "A", "Activating a combatant (3.3.1)")
    y = 20
    s.text(ax, y + 7, "Eligible to activate (3.3):", 9, 700)
    y += 10
    elig = ["on the battlefield and belongs to the side", "at least 1 AP remaining",
            "has not already activated this round", "not prevented by another rule"]
    for e in elig:
        s.text(ax + 4, y + 9, "•", 9, 700)
        s.text(ax + 12, y + 9, e, 9)
        y += 10.6
    y += 7
    steps = ["Choose one eligible allied combatant.",
             "Resolve effects that occur at the start of that combatant's activation.",
             "Spend at least 1 AP on actions, in any order the rules allow. Further AP may be spent in the same activation.",
             "Resolve effects that occur at the end of that combatant's activation.",
             "Mark the combatant as having activated this round."]
    y = step_list(s, ax, y, steps, aw, gap=5)
    hh = box(s, ax, y + 1, aw, "**Reactions** (4.5): taken when a rule's trigger occurs, usually outside the reacting combatant's activation. Taking one does not begin or end an activation. Only 1 Reaction may modify the same action or effect against a given combatant.", anchor="start", fill=PALE, sw=0.7, pad=5)
    ya = y + 1 + hh
    # ---------------- Panel B: AP timeline ----------------
    bx = 250
    bwid = FULL_W - bx
    panel_title(s, bx, 0, "B", "One Hero's AP through a round (example)")
    y = 20
    y = s.para(bx, y + 7, "Assumes a Hero with an equipped shield. Heroes begin each round with 3 AP (2.5).", bwid, 9, lead=10.6) - 3
    s.text(bx, y + 7, "Heroes' AP is shown with squares:", 9)
    ox = bx + tw("Heroes' AP is shown with squares:", 9) + 6
    _pip(s, ox, y - 1.5, True, 9); s.text(ox + 12, y + 7, "unspent", 9)
    ox2 = ox + 12 + tw("unspent", 9) + 8
    _pip(s, ox2, y - 1.5, False, 9); s.text(ox2 + 12, y + 7, "spent", 9)
    y += 8
    rows = [
        ("Initiative Phase", 3, "Refresh to 3 AP.", "3.2"),
        ("Party Phase — this Hero's one activation", 1, None, "3.3"),
        ("Monster Phase", 0, "A Monster's slashing attack would damage the Hero: the Hero declares **Block** (Reaction, 1 AP). It is not an activation.", "5.5.1"),
        ("End of Round", 0, "Any unspent AP is removed.", "3.5"),
    ]
    ry = y + 6
    for idx, (title, left, note, ref) in enumerate(rows):
        s.rect(bx, ry, bwid, 14, fill=INK, stroke=INK, sw=0.8, rx=2)
        s.text(bx + 5, ry + 10.4, title, 9, 700, "start", WHITE)
        s.text(bx + bwid - 5, ry + 10.4, ref, 9, 600, "end", WHITE)
        ry += 19
        # pips
        if idx == 0:
            for k in range(3):
                _pip(s, bx + 4 + k * 14, ry, True)
            s.text(bx + 54, ry + 9, note, 9)
            ry += 17
        elif idx == 1:
            # action chips with pips
            cx = bx + 4
            for name in ("Move", "Attack"):
                w = tw(name + " – 1 AP", 9, 600) + 10
                s.rect(cx, ry - 2, w, 14, fill=WHITE, stroke=INK, sw=0.8, rx=2)
                s.text(cx + w / 2, ry + 8, name + " – 1 AP", 9, 600, "middle")
                cx += w + 6
            s.text(cx + 2, ry + 8, "→", 9, 600)
            cx += 14
            for k, f in enumerate((False, False, True)):
                _pip(s, cx + k * 14, ry - 0.5, f)
            ry += 16
            yy = s.para(bx + 4, ry + 7, "Move (4.2) and Attack (4.2, 5.1) cost 1 AP each. The activation ends with 1 AP unspent; unspent AP may be kept for Reactions (3.3.2).", bwid - 6, 9, lead=10.6)
            ry = yy - 3
        elif idx == 2:
            for k, f in enumerate((False, False, False)):
                _pip(s, bx + 4 + k * 14, ry, f)
            yy = s.para(bx + 54, ry + 8, note, bwid - 56, 9, lead=10.6)
            ry = max(yy, ry + 17) - 3
        else:
            s.text(bx + 4, ry + 8, "No AP is carried into the next round (3.3.2).", 9)
            ry += 14
        ry += 4
    hh = box(s, bx, ry, bwid, "If no Reaction is taken, the 1 unspent AP is simply removed at End of Round. A combatant reduced below 1 AP by Reactions is no longer eligible to activate (3.3.2).", anchor="start", fill=PALE, sw=0.7, pad=5)
    yb = ry + hh
    return s, max(ya, yb) + 4


def fig03():
    s = Svg(FULL_W)
    # ---------------- Panel A: attack sequence ----------------
    aw = 236
    panel_title(s, 0, 0, "A", "The attack sequence (5.2)")
    y = 21
    steps = [
        ("Declare and verify.", "Attacker, attack, target, primary damage type and any additional types. Confirm LOS, visibility, range, Cover and other targeting rules."),
        ("Resolve declaration Reactions.", "Redirection and similar Reactions first, then verify again. The defender may declare at most one Reaction that modifies the attack (4.5)."),
        ("Roll and build damage.", "Base dice with Advantage/Disadvantage, Total Miss and Critical Hit checks, exploding dice, modifiers by damage type. Any Luck reroll (2.10) happens before consequences."),
        ("Defend and mitigate.", "Resolve the chosen Reaction, then apply the Mitigation Order (5.1.1)."),
        ("Apply and finish.", "Reduce HP, then resolve remaining Critical Hit effects, damage-triggered effects and conditions."),
    ]
    for i, (hd, body) in enumerate(steps, 1):
        lines = wrap("**%s** %s" % (hd, body), aw - 32, 9)
        h = len(lines) * 10.6 + 6
        s.rect(0, y, aw, h, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
        callout(s, 13, y + 12, i)
        for k, ln in enumerate(lines):
            s.text(24, y + 10 + k * 10.6, ln, 9)
        y += h
        if i < len(steps):
            vflow_arrow(s, 13, y, y + 12)
            y += 12
        if i == 3:
            pass
    # total miss branch marker
    ya = y
    s.rect(0, ya + 5, aw, 28, fill=PALE, stroke=INK, sw=0.7, rx=2.5)
    for k, ln in enumerate(wrap("**Total Miss** (5.3): if every retained base damage die shows a natural 1, the attack deals no damage and ends at step 3.", aw - 10, 9)):
        s.text(5, ya + 16 + k * 10.6, ln, 9)
    ya += 33
    # ---------------- Panel B: mitigation + example ----------------
    bx = 252
    bw = FULL_W - bx
    panel_title(s, bx, 0, "B", "Mitigation Order and worked example (5.1.1)")
    y = 21
    mo = [
        "Keep each damage type separate. Apply AV once to blunt, piercing and slashing damage only; reduce each type to a minimum of 0.",
        "Apply Immune, Resistant and Vulnerable to each remaining type.",
        "Total the remaining damage and apply it.",
    ]
    y = step_list(s, bx, y, mo, bw, gap=4)
    y += 2
    s.text(bx, y + 8, "Example: a Fighter declares Block", 9, 700)
    y += 14
    # table
    cols = [bx, bx + 78, bx + 128, bx + 188]
    hdr = ["Damage type", "Rolled", "AV", "Suffered"]
    s.rect(bx, y, bw, 15, fill=INK, stroke=INK, sw=0.8)
    for c, hd in zip(cols, hdr):
        s.text(c + 5, y + 10.8, hd, 9, 700, "start", WHITE)
    y += 15
    rowsd = [("slashing", "6", "− 5", "1"), ("fire (ignores AV)", "4", "—", "4")]
    for r in rowsd:
        s.rect(bx, y, bw, 16, fill=WHITE, stroke=INK, sw=0.7)
        for c, val in zip(cols, r):
            s.text(c + 5, y + 11.5, val, 9, 400)
        y += 16
    s.rect(bx, y, bw, 16, fill=PALE, stroke=INK, sw=0.7)
    s.text(cols[0] + 5, y + 11.5, "Total damage", 9, 700)
    s.text(cols[3] + 5, y + 11.5, "1 + 4 = 5", 9, 700)
    y += 22
    yy = s.para(bx, y + 8, "The Fighter's 5 AV (armour AD plus shield AD) reduces the 6 slashing damage to 1. Fire damage ignores AV.", bw, 9, lead=10.6)
    y = yy + 4
    s.text(bx, y + 8, "Second example: Hero with d6 AD Chest armour (5.4.3)", 9, 700)
    y += 14
    s.rect(bx, y, bw, 15, fill=INK, stroke=INK, sw=0.8)
    for c, hd in zip((bx, bx + 126, bx + 190), ("Case", "AV", "Suffered")):
        s.text(c + 5, y + 10.8, hd, 9, 700, "start", WHITE)
    y += 15
    for case, av, res in (("9 slashing, no Block (d6 = 3)", "3", "9 − 3 = 6"),
                          ("same attack, Block (+2 AV)", "3 + 2 = 5", "9 − 5 = 4")):
        s.rect(bx, y, bw, 16, fill=WHITE, stroke=INK, sw=0.7)
        s.text(bx + 4, y + 11.5, case, 9)
        s.text(bx + 131, y + 11.5, av, 9)
        s.text(bx + 195, y + 11.5, res, 9)
        y += 16
    y += 8
    return s, max(ya, y) + 4
