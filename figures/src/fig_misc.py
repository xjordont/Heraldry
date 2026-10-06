"""FIG-17 .. FIG-19: campaign sequence, Appendix A setup and opening, Appendix B Basic Mode."""
import math
from svgkit import *
from fig_seq import _pip
from fig_scen import _dimh, _dimv


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


def fig18():
    s = Svg(FULL_W)
    k = 7.0
    side = 24 * k
    panel_title(s, 0, 0, "A", "Setup and positions (A.4, A.11)")
    bx, by = 4, 24
    s.rect(bx, by, side, side, fill=WHITE, stroke=INK, sw=1.1)
    # deployment zones: within 4" of the two short edges
    s.rect(bx, by, side, 4 * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")
    s.rect(bx, by + side - 4 * k, side, 4 * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")
    cx, cy = bx + side / 2, by + side / 2

    def P(x, y):  # inches from NW corner
        return bx + x * k, by + y * k
    # centre cross-hairs
    s.line(cx - 4, cy, cx + 4, cy, MID, 0.6)
    s.line(cx, cy - 4, cx, cy + 4, MID, 0.6)
    # satchel at the centre, 4 wolves 2" N/S/E/W
    token(s, "obj", cx, cy, 4.8)
    for dx, dy in ((0, 2), (2, 0), (-2, 0), (0, -2)):
        token(s, "M", cx + dx * k, cy + dy * k, 5.0)
    # chest 5" east of centre
    token(s, "chest", cx + 5 * k, cy, 5.0)
    # heroes (A.11 table): Party A south edge, Party B north edge
    token(s, "A", *P(12, 20), 5.2)
    token(s, "A", *P(18, 20), 5.2)
    token(s, "B", *P(12, 4), 5.2)
    token(s, "B", *P(18, 4), 5.2)
    pill(s, *P(12, 22.3), "Edric", 9, 600)
    pill(s, *P(18, 22.3), "Mara", 9, 600)
    pill(s, *P(12, 1.7), "Varek", 9, 600)
    pill(s, *P(18, 1.7), "Senna", 9, 600)
    # dimensions stated in A.11
    _dimv(s, bx + 9.5 * k, by + 20 * k, by + side, "4\"") if False else None
    pill(s, cx + 5 * k + 4, cy + 17, "5\" east", 9, 600)
    pill(s, cx + 13, cy - 2 * k - 1 + 12, "wolves 2\"", 9, 600) if False else None
    yy = s.para(bx, by + side + 11, "24\"×24\" battlefield, 7 pt per inch; markers enlarged. Positions are those of the A.11 table. The terrain of A.2 is not drawn.", 190, 9, lead=10.4)
    yl = legend(s, [("A", "Road Wardens"), ("B", "Black Briar Raiders"), ("M", "Dire Wolf"), ("obj", "Dispatch Satchel"), ("chest", "Treasure Chest"), ("zone", "within 4\" of short edge")], 0, yy + 4, 190)
    # ---------------- right: round 1 ----------------
    rx = 200
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Round 1 as played in A.11 (fixed rolls)")
    y = 22
    # initiative
    hh = box(s, rx, y, rw, "**Initiative:** Road Wardens 1d20 = 13, +0 INT, +1 SPI = **14**. Black Briar Raiders 1d20 = 10, +0, +0 = **10**. The Road Wardens win and choose to act first. All Heroes refresh to 3 AP.", anchor="start", fill=PALE, sw=0.7, pad=4)
    y += hh + 5
    rows = [
        ("1 Edric", (False, False, False), "Move, Move, Interact: picks up the Dispatch Satchel. With 0 AP left he cannot take Reactions this round."),
        ("2 Varek", (False, False, False), "Move, Move (Engaged with Edric), Attack with Battleaxe: 1d8 = 6, +3 STR = 9. Edric's Brigandine AD d8 = 4, so Edric takes 9 − 4 = 5 (16 → 11 HP)."),
        ("3 Mara", (False, False, True), "Move, Attack with Shortbow: 1d6 = 4, +3 DEX = 7. Dire Wolf 3 has AV 1: 7 − 1 = 6 (15 → 9 HP). Keeps 1 AP."),
        ("4 Senna", (False, False, True), "Move, Attack with Shortbow: 1d6 = 5, +3 DEX = 8. Mara declares Dodge [1 AP]: 1d20 = 11, +3 DEX = 14. A Check of 12 or more succeeds: Mara takes 0 (her 3 AP are spent). Senna keeps 1 AP."),
    ]
    s.text(rx, y + 8, "Party Phase (activations alternate, Road Wardens first)", 9, 700)
    y += 13
    nm_w = 50
    for nm, pips, tx in rows:
        lines = wrap(tx, rw - nm_w - 44, 9)
        hh = max(len(lines) * 10.6 + 6, 18)
        s.rect(rx, y, rw, hh, fill=WHITE, stroke=INK, sw=0.8, rx=2)
        s.text(rx + 4, y + 11, nm, 9, 700)
        for i, ln in enumerate(lines):
            s.text(rx + nm_w, y + 10 + i * 10.6, ln, 9)
        for i, f in enumerate(pips):
            _pip(s, rx + rw - 40 + i * 12, y + 4, f, 9)
        y += hh + 2
    y += 3
    s.text(rx, y + 8, "Monster Phase (Dire Wolves 1 to 4 in order; Edric carries the Satchel)", 9, 700)
    y += 13
    mrows = [
        ("Wolf 1", "Moves into Engagement with Edric and Bites: 1d8 = 5, +1 = 6. AD d8 = 3: Edric takes 3 (11 → 8 HP). STR Check 9 + 3 = 12 succeeds."),
        ("Wolf 2", "Pack Tactics (Advantage): 4 and 7, keep 7, +1 = 8. AD d8 = 5: Edric takes 3 (8 → 5 HP). STR Check 6 + 3 = 9 fails: Edric is Prone."),
        ("Wolves 3, 4", "No open space from which to engage Edric: they end as close as possible and do not attack."),
    ]
    for nm, tx in mrows:
        lines = wrap(tx, rw - nm_w - 8 - 6, 9)
        hh = max(len(lines) * 10.6 + 6, 18)
        s.rect(rx, y, rw, hh, fill=WHITE, stroke=INK, sw=0.8, rx=2)
        s.text(rx + 4, y + 11, nm, 9, 700)
        for i, ln in enumerate(lines):
            s.text(rx + nm_w + 8, y + 10 + i * 10.6, ln, 9)
        y += hh + 2
    y += 2
    hh = box(s, rx, y, rw, "**End of Round:** Senna's 1 unspent AP is removed. Edric: 5 HP, Prone, carrying the Satchel, Engaged by Varek and Dire Wolves 1 and 2.", anchor="start", fill=PALE, sw=0.7, pad=4)
    y += hh + 4
    s.text(rx, y + 8, "AP squares:", 9, 700)
    _pip(s, rx + 56, y - 0.5, True, 9)
    s.text(rx + 68, y + 8, "unspent after activation", 9)
    _pip(s, rx + 170, y - 0.5, False, 9)
    s.text(rx + 182, y + 8, "spent", 9)
    y += 14
    return s, max(y, yl) + 2


def fig19():
    s = Svg(FULL_W)
    k = 7.0
    side = 24 * k
    panel_title(s, 0, 0, "A", "The Courier's Strongbox (B.6)")
    bx, by = 4, 24
    s.rect(bx, by, side, side, fill=WHITE, stroke=INK, sw=1.1)
    # deployment: each side within 4" of opposite edges (north/south drawn)
    s.rect(bx, by, side, 4 * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")
    s.rect(bx, by + side - 4 * k, side, 4 * k, fill=PALE, stroke=INK, sw=0.9, dash="3.5 2")
    cx, cy = bx + side / 2, by + side / 2

    def P(x, y):
        return bx + x * k, by + y * k
    # road across the centre (width not stated; schematic band)
    s.rect(bx, cy - 1.5 * k, side, 3 * k, fill=WHITE, stroke=None)
    s.line(bx, cy - 1.5 * k, bx + side, cy - 1.5 * k, MID, 0.7, dash="6 3")
    s.line(bx, cy + 1.5 * k, bx + side, cy + 1.5 * k, MID, 0.7, dash="6 3")
    s.line(bx, cy, bx + side, cy, MID, 0.8, dash="1 3")
    pill(s, bx + 20, cy - 2, "road", 9, 600)
    # 2 pieces within 4" of the centre: one ruin (Blocking), one low wall/cart (Impassable)
    x, y = P(13, 7.5)
    terrain(s, "blocking", x, y, 3 * k, 3 * k, ["Ruin"] if False else None)
    x, y = P(8, 13)
    terrain(s, "impassable", x, y, 3 * k, 3 * k, None)
    # four additional 3x3 pieces, one per quarter (Cover)
    for (px, py) in ((3, 6), (18, 5.5), (3, 15.5), (18, 15)):
        x, y = P(px, py)
        terrain(s, "cover", x, y, 3 * k, 3 * k, None)
    # Monster Entry markers must be 5-7" from the centre: draw the legal band, then three markers inside it
    s.circle(cx, cy, 5 * k, fill="none", stroke=MID, sw=0.8, dash="2 2.5")
    s.circle(cx, cy, 7 * k, fill="none", stroke=MID, sw=0.8, dash="2 2.5")
    ents = [(12 + 6 * math.cos(math.radians(a)), 12 - 6 * math.sin(math.radians(a))) for a in (0, 120, 240)]
    for (ex, ey) in ents:
        px, py = P(ex, ey)
        token(s, "M", px, py, 5.6)
        token(s, "obj", px + 11, py, 4.0)
    token(s, "chest", cx, cy, 7.0)
    # sides
    for i in range(3):
        token(s, "A", *P(7 + 5 * i, 2), 4.6)
        token(s, "B", *P(7 + 5 * i, 22), 4.6)
    yy = s.para(bx, by + side + 11, "24\"×24\" battlefield, 7 pt per inch. Dashed rings mark 5\" and 7\" from the centre, the band for Monster Entry markers (3 drawn, at least 4\" apart). Terrain positions and the road are schematic.", 190, 9, lead=10.4)
    yl = legend(s, [("A", "one side"), ("B", "other side"), ("M", "Monster group (Resting)"), ("chest", "Strongbox"), ("obj", "Satchel"), ("blocking", "ruin: Blocking"), ("impassable", "cart or low wall: Impassable"), ("cover", "other piece: Cover"), ("zone", "within 4\" of an edge")], 0, yy + 4, 190)
    # ---------------- right ----------------
    rx = 204
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Placement rules and an example score")
    y = 22
    notes = [
        "**Terrain:** a road across the centre; 2 ruins, carts or low walls within 4\" of the centre; 4 more 3\"×3\" pieces, one in each quarter. Ruins are Blocking, carts and low walls Impassable, other pieces Cover.",
        "**Deployment:** each side deploys within 4\" of opposite battlefield edges.",
        "**Monster Entry markers:** 3 markers around the centre, each 5–7\" from it, at least 4\" from each other and outside both deployment zones. One complete group (Goblins, Skeleton Warriors, Bandits) and 1 Satchel at each marker; every group begins Resting.",
        "**Treasure:** the Strongbox (12c) at the centre; 3 Satchels (4c each). A carrier of the Strongbox has −2\" Speed, to a minimum of 1\".",
        "**Extraction:** leave the battlefield through your own deployment edge; the carried treasure's Coin Value is added to your score.",
    ]
    y = step_list(s, rx, y, notes, rw, gap=4)
    y += 2
    s.text(rx, y + 8, "Example (assumed): Ironscar, SPD 4\", carries the Strongbox from the centre", 9, 700)
    y += 12
    ex_rows = [("Speed carrying the Strongbox", "4\" − 2\" = 2\" per Move"),
               ("Centre to an edge, open ground", "12\"; 12\" ÷ 2\" = at least 6 Moves"),
               ("Score: Strongbox + 1 Satchel + 2 Goblins + 1 Bandit", "12 + 4 + 2 + 3 = 21c")]
    for a_, b_ in ex_rows:
        s.rect(rx, y, rw, 16, fill=WHITE, stroke=INK, sw=0.7)
        s.text(rx + 4, y + 11.4, a_, 9)
        s.text(rx + rw - 4, y + 11.4, b_, 9, 700, "end")
        y += 16
    y += 4
    yy = s.para(rx, y + 8, "Picking up the Strongbox also costs Interact [1 AP]. Coin Values: Goblin 1c, Skeleton Warrior 1c, Bandit 3c (B.5). The game ends after Round 6; the higher score wins (B.6).", rw, 9, lead=10.6)
    return s, max(yl, yy) + 2
