"""FIG-18 and FIG-19: the Appendix A (Learn to Play) and Appendix B (Basic Mode) setup diagrams.

The board panels are drawn by the same map renderer, spec system and glyph functions (scenkit) as the 36 Core Scenario maps
(figures/src/scenario_specs.json, section "appendix"); only Appendix A and B rules are used.  Each figure carries a compact key
strip with exactly the glyphs it uses, because Appendix readers may not have seen the key in 10.4 (FIG-20).
"""
import scenkit as K
from scenkit import MapSvg
from svgkit import FULL_W, INK, PALE, WHITE, wrap, tw, panel_title, box
import fig_scenmaps as M
from fig_seq import _pip

LEFT_W = 210


def fig18():
    sp = M.spec()["appendix"]["A"]
    s = MapSvg(FULL_W)
    panel_title(s, 0, 0, "A", "Setup and positions (A.4, A.11)")
    c, h = M.embed_map(s, sp, 0, 18, LEFT_W, bx=15, by=14)
    y = 18 + h + 4
    # A.11 relative layout of the Satchel and the four Dire Wolves (side of the ruin not stated, so shown apart from the board)
    s.text(0, y + 8, "A.11 relative layout (not a position on the board)", 9, 700)
    y += 12
    ix, iy = 46, y + 26
    k = 10.0
    K.marker(s, "obj", ix, iy, False, 4.8)
    for n, (dx, dy) in enumerate(((0, 2), (2, 0), (-2, 0), (0, -2)), 1):
        K.monster(s, "M", ix + dx * k, iy + dy * k, False)
        s.htext(ix + dx * k + (8 if dx >= 0 else -8), iy + dy * k + 3.2, "W%d" % n, 9, 600, "start" if dx >= 0 else "end")
    K.dim_labeled(s, ix, iy + 32, ix + 2 * k, iy + 32, '2"', 2.6, off=9)
    yt = s.para(ix + 54, iy - 22, "W1 to W4 are Dire Wolves 1 to 4: 2\" south, east, west and north of the Satchel (A.11). On the board, the ruin leaves no space for W3 and W4 beside Edric.", LEFT_W - ix - 54, 9, lead=10.4)
    y = max(iy + 46, yt) + 2
    labels18 = {"hero-A": "Road Wardens (Party A)", "hero-B": "Black Briar Raiders (Party B)", "mon": "Dire Wolf (A = Awake)", "obj": "Dispatch Satchel",
              "zone-A": "Party A zone", "zone-B": "Party B zone", "ter-impassable": "Low wall", "ter-blocking": "Centre ruin",
              "ter-coverdiff": "Rubble", "ter-cover": "Cover piece", "range": "Range", "dim": "Distance"}
    yl = y
    # ---------------- right: round 1 ----------------
    rx = 218
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Round 1 as played in A.11 (fixed rolls)")
    y = 22
    hh = box(s, rx, y, rw, "**Initiative:** Road Wardens 1d20 = 13, +0 INT, +1 SPI = **14**. Black Briar Raiders 1d20 = 10, +0, +0 = **10**. The Road Wardens win and choose to act first. All Heroes refresh to 3 AP.", anchor="start", fill=PALE, sw=0.7, pad=4)
    y += hh + 5
    rows = [
        ("1 Edric", (False, False, False), "Move, Move, Interact: picks up the Dispatch Satchel. With 0 AP left it cannot take Reactions this round."),
        ("2 Varek", (False, False, False), "Move, Move (Engaged with Edric), Attack with Battleaxe: 1d8 = 6, +3 STR = 9. Edric's Brigandine AD d8 = 4, so Edric takes 9 - 4 = 5 (16 → 11 HP)."),
        ("3 Mara", (False, False, True), "Move, Attack with Shortbow: 1d6 = 4, +3 DEX = 7. Dire Wolf 3 has AV 1: 7 - 1 = 6 (15 → 9 HP). Keeps 1 AP."),
        ("4 Senna", (False, False, True), "Move, then declare Shortbow Attack. Mara declares Dodge [1 AP] before damage is rolled. Senna: 1d6 = 5, +3 DEX = 8. Mara's DEX Check: 1d20 = 11, +3 = 14, a success. Mara takes 0 damage and has spent its 3 AP. Senna keeps 1 AP."),
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
    yk = K.strip_for(s, 0, max(y, yl) + 6, FULL_W, labels18)
    return s, yk + 2


def fig19():
    sp = M.spec()["appendix"]["B"]
    s = MapSvg(FULL_W)
    panel_title(s, 0, 0, "A", "The Courier's Strongbox (B.6)")
    c, h = M.embed_map(s, sp, 0, 18, LEFT_W, bx=15, by=14)
    y = 18 + h + 4
    labels19 = {"hero-A": "One side's Heroes", "hero-B": "Other side's Heroes", "zone-A": "Zone, 4\" deep", "zone-B": "Zone, 4\" deep",
              "mon": "Monster group (R = Resting)", "chest": "Strongbox", "obj": "Satchel", "mk": "Monster Entry marker",
              "ter-blocking": "Ruin: Blocking", "ter-impassable": "Cart or low wall: Impassable", "ter-cover": "Other piece: Cover",
              "ter-open": "Road", "range": "Range", "dim": "Distance"}
    yl = y
    # ---------------- right ----------------
    rx = 218
    rw = FULL_W - rx
    panel_title(s, rx, 0, "B", "Placement rules and an example score")
    y = 22
    notes = [
        "**Terrain:** a road across the centre; 2 ruins, carts or low walls within 4\" of the centre; 4 more 3\"×3\" pieces, one in each quarter. Ruins are Blocking, carts and low walls Impassable, other pieces Cover.",
        "**Deployment:** each side deploys within 4\" of opposite battlefield edges.",
        "**Monster Entry markers:** 3 markers around the centre, each 5–7\" from it, at least 4\" from each other and outside both deployment zones. The 3 groups (4 Goblins, 4 Skeleton Warriors, 4 Bandits) are assigned to the markers at random, one complete group per marker, with 1 Satchel on each marker. Every group begins Resting.",
        "**Treasure:** the Strongbox (12c) at the centre; 3 Satchels (4c each). A carrier of the Strongbox has -2\" Speed, to a minimum of 1\".",
        "**Extraction:** leave the battlefield through your own deployment edge; remove the carrier from play and add the carried treasure's Coin Value to your score.",
    ]
    for n_ in notes:
        y = s.para(rx, y + 7, n_, rw, 9, lead=10.5) + 2
    y += 2
    y = s.para(rx, y + 8, "**Example (assumed): Ironscar, SPD 4\", carries the Strongbox from the centre**", rw, 9, lead=10.5) - 4
    ex_rows = [("Speed carrying the Strongbox", "4\" - 2\" = 2\" per Move"),
               ("Centre to an edge, open ground", "12\"; 12\" ÷ 2\" = at least 6 Moves"),
               ("Score: Strongbox + 1 Satchel + 2 Goblins + 1 Bandit", "12 + 4 + 2 + 3 = 21c")]
    for a_, b_ in ex_rows:
        s.rect(rx, y, rw, 16, fill=WHITE, stroke=INK, sw=0.7)
        s.text(rx + 4, y + 11.4, a_, 9)
        s.text(rx + rw - 4, y + 11.4, b_, 9, 700, "end")
        y += 16
    y += 4
    yy = s.para(rx, y + 8, "An adjacent, unengaged combatant picks up the Strongbox or a Satchel with Interact [1 AP]. Coin Values: Goblin 1c, Skeleton Warrior 1c, Bandit 3c (B.5). The game ends after Round 6; the higher score wins. Ties: the Strongbox-extracting side wins; otherwise draw (B.6).", rw, 9, lead=10.6)
    yk = K.strip_for(s, 0, max(yl, yy) + 6, FULL_W, labels19)
    return s, yk + 2
