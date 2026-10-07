"""FIG-17: campaign sequence and Town Phase (FIG-18 and FIG-19 live in fig_appx.py)."""
import math
from svgkit import *
from fig_seq import _pip


def fig17():
    s = Svg(FULL_W)
    bw, gap = 114, 16
    y0 = 4
    phases = [
        ("Expedition", "11.2.1", [
            "After selecting the Active Party, before generating the battlefield, each party rolls 1d10 on the Expedition Event Table.",
            "Apply the result immediately unless it specifies a later timing.",
        ]),
        ("Skirmish", "11.2.2", [
            "Generate the battlefield, deploy forces and resolve the adventure using the scenario rules in Section 10.",
        ]),
        ("Aftermath", "11.2.3", [
            "Step 1: secure Coins and loot.",
            "Step 2: resolve the Fallen.",
            "Step 3: Journey Home. Roll 1d20 on the completed Climate's Journey Table and apply it.",
        ]),
        ("Town", "11.2.4", [
            "The party receives 4 Town Action Points (TAP), or the amount a Journey result sets.",
            "Spend TAP on Town actions; unspent TAP are lost at the end of the phase unless a rule says otherwise.",
        ]),
    ]
    heights = []
    texts = []
    for i, (name, ref, items) in enumerate(phases):
        hs = 0
        for it in items:
            hs += len(wrap(it, bw - 15, 9)) * 10.6 + 3.5
        heights.append(hs + 10)
    H = max(heights)
    for i, (name, ref, items) in enumerate(phases):
        x = i * (bw + gap)
        s.rect(x, y0, bw, 22, fill=INK, stroke=INK, sw=0.9, rx=2.5)
        s.circle(x + 12, y0 + 11, 6.6, fill=WHITE, stroke=None)
        s.text(x + 12, y0 + 14.3, str(i + 1), 9, 700, "middle", INK)
        s.text(x + 22, y0 + 15, name, 9.5, 700, "start", WHITE)
        s.text(x + bw - 4, y0 + 15, ref, 9, 600, "end", WHITE)
        s.rect(x, y0 + 25, bw, H, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
        ty = y0 + 25 + 5
        for it in items:
            lines = wrap(it, bw - 15, 9)
            s.text(x + 5, ty + 7, "•", 9, 700)
            for k, ln in enumerate(lines):
                s.text(x + 12, ty + 7 + k * 10.6, ln, 9)
            ty += len(lines) * 10.6 + 3.5
        if i < 3:
            hflow_arrow(s, x + bw + 1.5, x + bw + gap - 1.5, y0 + 11)
    yb = y0 + 25 + H + 10
    x_end = 3 * (bw + gap) + bw / 2
    x_start = bw / 2
    s.line(x_end, y0 + 25 + H, x_end, yb, INK, 1.2)
    s.line(x_end, yb, x_start, yb, INK, 1.2)
    s.line(x_start, yb, x_start, y0 + 25 + H + 2, INK, 1.2)
    s.polygon([(x_start, y0 + 25 + H), (x_start - 3.4, y0 + 25 + H + 7), (x_start + 3.4, y0 + 25 + H + 7)], INK)
    pill(s, (x_start + x_end) / 2, yb + 3.2, "After every adventure, win or lose, resolve Aftermath and Town unless a rule says otherwise (11.2)", 9, 600)
    y = yb + 16
    s.line(0, y, FULL_W, y, MID, 0.6)
    panel_title(s, 0, y + 6, "A", "Town Phase checklist (11.2.4)")
    panel_title(s, 262, y + 6, "B", "Town locations")
    y += 26
    chk = [
        "Confirm current Storage, Treasury, roster status and any lingering injuries.",
        "Resolve start-of-Town effects, then gain 4 TAP (or the modified amount).",
        "Spend TAP on legal Town actions in any order.",
        "Pay all required coin costs as each Town action resolves.",
        "Update Hero sheets, known Powers, equipped items, pending commissions, Storage and Stronghold progress.",
        "Confirm the party's legal Roster and Active Party before the next adventure.",
    ]
    ya = step_list(s, 0, y, chk, 250, gap=3)
    locs = [("The Grand Hall", "trade, brokerage, commissions and fencing"),
            ("The Chapel", "restores the injured, removes afflictions, petitions for miracles"),
            ("The Arcane Spire", "researches Powers and copies scrolls"),
            ("The Training Grounds", "retrains veterans and sharpens technique"),
            ("The Ironworks", "improves gear and reforges prized equipment"),
            ("The Guild of Keys", "manages contracts, maps, logistics and black-market routes")]
    yy = y
    for nm, ds in locs:
        lines = wrap("**%s:** %s" % (nm, ds), 238, 9)
        h = len(lines) * 10.6 + 5
        s.rect(262, yy, 242, h, fill=PALE, stroke=INK, sw=0.7, rx=2)
        for k, ln in enumerate(lines):
            s.text(266, yy + 10 + k * 10.6, ln, 9)
        yy += h + 3
    return s, max(ya, yy) + 2
