"""FIG-72 .. FIG-77: end-of-section fillers for Chapters 6 and 7 (character creation procedure, Hero attributes,
Average Party Level, party building guidelines, reading item entries, stacking and precedence).

Same visual grammar as FIG-01 to FIG-03 and FIG-17: black header bars with white numbered circles, 0.9 pt boxes
with rx 2.5, black numbered step circles, flow arrows.  Every figure returns (svg, height) like fig_seq.py."""
import re
from svgkit import *

LEAD = 10.6


# ---------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------
def _badge(s, x, y, letter):
    """Black square with a white letter (panel grammar of panel_title)."""
    s.rect(x, y, 13, 13, fill=INK, stroke=None)
    s.text(x + 6.5, y + 10.4, letter, 9, 700, "middle", WHITE)


def _bar(s, x, y, w, n, title, ref=None, h=19):
    """Black header bar with white numbered circle (FIG-01 grammar)."""
    s.rect(x, y, w, h, fill=INK, stroke=INK, sw=0.9, rx=2.5)
    tx = x + 6
    if n is not None:
        s.circle(x + 11, y + h / 2, 6.6, fill=WHITE, stroke=None)
        s.text(x + 11, y + h / 2 + 3.2, str(n), 9, 700, "middle", INK)
        tx = x + 22
    s.text(tx, y + h / 2 + 3.3, title, 9.5, 700, "start", WHITE)
    if ref:
        s.text(x + w - 5, y + h / 2 + 3.3, ref, 9, 600, "end", WHITE)
    return h


def _lines_h(lines):
    return len(lines) * LEAD


def _step_tile(s, x, y, w, n, text, badge=None, fill=WHITE, min_h=22):
    """Numbered step box: black step circle at left, wrapped text.  Returns box height."""
    tw_ = w - 30 - (17 if badge else 0)
    lines = wrap(text, tw_, 9)
    h = max(min_h, _lines_h(lines) + 9)
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=0.9, rx=2.5)
    callout(s, x + 13, y + h / 2, n)
    ty = y + (h - _lines_h(lines)) / 2 + 8.2
    for k, ln in enumerate(lines):
        s.text(x + 26, ty + k * LEAD, ln, 9)
    if badge:
        _badge(s, x + w - 18, y + 4, badge)
    return h


def _text_box(s, x, y, w, text, fill=PALE, pad=5, sw=0.7, head=None, min_h=0):
    """Rounded box with wrapped text (and an optional bold head line); returns height."""
    lines = wrap(text, w - 2 * pad, 9)
    h = max(min_h, _lines_h(lines) + 2 * pad - 1.5 + (LEAD if head else 0))
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=sw, rx=2.5)
    ty = y + pad + 7.4
    if head:
        s.text(x + pad, ty, head, 9, 700)
        ty += LEAD
    for k, ln in enumerate(lines):
        s.text(x + pad, ty + k * LEAD, ln, 9)
    return h


def _elbow_arrow(s, x1, y1, xmid, y2, x2):
    """Right, vertical, right connector ending in an arrowhead at (x2, y2)."""
    s.line(x1, y1, xmid, y1, INK, 1.2)
    s.line(xmid, y1, xmid, y2, INK, 1.2)
    hflow_arrow(s, xmid - 0.6, x2, y2)


# ---------------------------------------------------------------------
# FIG-72  6.2 Character Creation Procedure
# ---------------------------------------------------------------------
STEPS_72 = [
    "Select a miniature, standee, or token to represent the Hero.",
    "Select or roll the Hero's ancestry, background, and class, in that order.",
    "Calculate the Hero's final **STR**, **DEX**, **INT**, and **SPI** scores.",
    "Choose the Hero's starting known Powers, if any.",
    "Choose the **General Talent** and **Novice Class Talent** granted at Level 1.",
    "Select or roll the Hero's starting equipment package and determine which items are equipped or carried.",
    "Calculate **Max HP**, **SPD**, **Max NRG**, maximum **Luck**, and **Initiative Bonus**, including every applicable modifier.",
    "Record all abilities, Powers, Talents, and equipment.",
    "In campaign play, add starting coins to the **Treasury**. Record each starting item as equipped, assigned to that Hero to carry during the first adventure, or held in **Storage**.",
    "Set current HP, NRG, and Luck equal to their final maximum values.",
]
FORMULA_ABILITY = "Final Ability Score = Ancestry Base Score + ancestry trait modifiers + Background Bonus + Class Modifier + any Random Background Bonus"
FORMULA_HP = "Starting Max HP = Ancestry Base HP + Class Starting HP Bonus"


def fig72():
    s = Svg(FULL_W)
    colw, colw2, gap = 220, 264, 20
    x2 = colw + gap
    badges = {3: "A", 7: "B"}
    ys, hs = [], []
    # column 1: steps 1-5, column 2: steps 6-10, vertical flow arrows inside each column
    cols_end = []
    for col, (lo, hi, cx, cwid) in enumerate(((1, 5, 0, colw), (6, 10, x2, colw2))):
        y = 2
        for n in range(lo, hi + 1):
            h = _step_tile(s, cx, y, cwid, n, STEPS_72[n - 1], badge=badges.get(n))
            ys.append(y)
            hs.append(h)
            y += h
            if n < hi:
                vflow_arrow(s, cx + 13, y, y + 10)
                y += 10
        cols_end.append(y)
    # connector from step 5 to step 6 through the gap between the columns
    y5 = ys[4] + hs[4] / 2
    y6 = ys[5] + hs[5] / 2
    _elbow_arrow(s, colw, y5, colw + gap / 2, y6, x2)
    y = max(cols_end) + 8
    s.line(0, y, FULL_W, y, MID, 0.6)
    y += 7
    # formulas
    aw, bw = 300, 196
    xb = aw + 8
    ha = _text_box_formula(s, 0, y, aw, "A", "Final starting ability scores (step 3)", FORMULA_ABILITY)
    hb = _text_box_formula(s, xb, y, bw, "B", "Starting Max HP (step 7)", FORMULA_HP)
    y += max(ha, hb) + 6
    note = ("After calculating each base value, apply every applicable ancestry, background, class, Talent, item, and "
            "random-generation modifier. Use **6.4 Hero Attributes** for **Initiative Bonus** and **Max NRG**.")
    hn = _text_box(s, 0, y, FULL_W, note, fill=WHITE)
    y += hn
    return s, y + 3


def _text_box_formula(s, x, y, w, letter, head, formula):
    pad = 5
    lines = wrap("**%s**" % formula, w - 2 * pad, 9)
    h = 17 + _lines_h(lines) + pad
    s.rect(x, y, w, h, fill=PALE, stroke=INK, sw=0.7, rx=2.5)
    _badge(s, x + 4, y + 3, letter)
    s.text(x + 22, y + 13, head, 9, 700)
    for k, ln in enumerate(lines):
        s.text(x + pad, y + 17 + 8.4 + k * LEAD, ln, 9)
    return h


# ---------------------------------------------------------------------
# FIG-73  6.4 Hero Attributes
# ---------------------------------------------------------------------
RECORDS_73 = [
    "**Name**", "**Ancestry, Background,** and **Class**", "**Level**", "**STR, DEX, INT,** and **SPI**",
    "current and maximum **HP**", "current and maximum **NRG**", "**SPD**", "**Sz**",
    "current and maximum **Luck**", "**Wounds**", "**Initiative Bonus**", "**Known Powers**, if any",
    "**General Talents, Class Talents,** and **Special Abilities**",
    "**Inventory**, including equipped and carried items", "**Carried Coins**",
]


def _pips(s, x, y, cur, mx, size=6.5):
    """Row of mx squares, the first cur filled (current value), the rest empty (room up to the maximum)."""
    for i in range(mx):
        if i < cur:
            s.rect(x + i * (size + 1.6), y, size, size, fill=INK, stroke=INK, sw=0.6)
        else:
            s.rect(x + i * (size + 1.6), y, size, size, fill=WHITE, stroke=INK, sw=0.8)
    return mx * (size + 1.6) - 1.6


def fig73():
    s = Svg(FULL_W)
    gx = 12
    aw, bw, cw = 198, 156, 126
    bx = aw + gx
    cx = bx + bw + gx
    # ---- Panel A: the record list (single column, source order) ----
    panel_title(s, 0, 0, "A", "Every Hero records (6.4)")
    y = 17
    for item in RECORDS_73:
        lines = wrap(item, aw - 12, 9)
        h = max(11.2, _lines_h(lines) + 1.2)
        s.rect(0, y, aw, h, fill=WHITE, stroke=INK, sw=0.7)
        for k, ln in enumerate(lines):
            s.text(5, y + 8.8 + k * LEAD, ln, 9)
        y += h
    ya = y
    # ---- Panel B: derived values ----
    panel_title(s, bx, 0, "B", "Derived values")
    y = 17
    s.text(bx, y + 7.5, "Unless a rule says otherwise:", 9, 400)
    y += 11
    h = _text_box(s, bx, y, bw, "**Initiative Bonus = INT + SPI**", fill=WHITE, sw=0.9, pad=4)
    y += h + 3
    h = _text_box(s, bx, y, bw,
                  "**Base Max NRG = Level + (2 × Primary Casting Score), minimum 0** for non-Martial classes that cast Powers. "
                  "Then apply any background, ancestry, talent, item, or class feature that modifies **Max NRG**. "
                  "Recalculate **Max NRG** whenever the Hero's Level, Primary Casting Score, or a permanent Max NRG modifier changes.",
                  fill=WHITE, sw=0.9, pad=4)
    y += h + 3
    h = _text_box(s, bx, y, bw,
                  "Martial classes always have **Max NRG 0** and cannot gain **Max NRG** unless a rule explicitly grants a replacement benefit.",
                  fill=WHITE, sw=0.9, pad=4)
    y += h
    yb = y
    # ---- Panel C: maxima and current values ----
    panel_title(s, cx, 0, "C", "Current and maximum")
    y = 17
    s.text(cx, y + 7.5, "Example (HP, assumed values)", 9, 700)
    y += 12
    rows = [
        (7, 10, "HP 7 of 10."),
        (6, 6, "Max HP falls below current HP: reduce current HP to the new maximum."),
        (6, 10, "Max HP rises: current HP stays 6. An increase does not restore HP unless a rule says otherwise."),
    ]
    for ri, (cur, mx, cap) in enumerate(rows):
        pw = _pips(s, cx, y + 1, cur, mx, size=5.2)
        if ri == 0:
            s.text(cx + pw + 6, y + 7.2, cap, 9)
            y += 11 + 4
            continue
        y += 10
        lines = wrap(cap, cw, 9)
        for k, ln in enumerate(lines):
            s.text(cx, y + 8 + k * LEAD, ln, 9)
        y += _lines_h(lines) + 4
    lines = wrap("Unless a rule explicitly says otherwise, current **HP**, **NRG**, and **Luck** cannot exceed the maximum; excess gained or restored is lost. "
                 "**Temporary HP** is separate. **Max HP** cannot fall below **1**.", cw, 9)
    for k, ln in enumerate(lines):
        s.text(cx, y + 8 + k * LEAD, ln, 9)
    y += _lines_h(lines)
    yc = y
    # ---- Carried Coins note across the foot ----
    y = max(ya, yb, yc) + 4
    h = _text_box(s, 0, y, FULL_W,
                  "**Carried Coins** records only coins currently carried on the battlefield. In campaign play, secured coins belong to "
                  "the party's shared **Treasury**, not to an individual Hero. Record current HP, NRG, and Luck separately from their maximum values.",
                  fill=PALE, pad=4)
    y += h
    return s, y + 2


# ---------------------------------------------------------------------
# FIG-74  6.14 Average Party Level (APL)
# ---------------------------------------------------------------------
def _level_token(s, cx, cy, level, r=8.5):
    s.circle(cx, cy, r, fill=INK, stroke=INK, sw=0.75)
    s.text(cx, cy + 3.3, str(level), 9, 700, "middle", WHITE)


def _icon_box(s, x, y, w, icon, head, text, fill=WHITE, dash=None):
    """Box with a leading icon ('ok' = black Hero token, 'no' = X mark), bold head and wrapped text."""
    lines = wrap(text, w - 12, 9)
    h = 22 + _lines_h(lines) + 3
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=0.9, rx=2.5, dash=dash)
    if icon == "ok":
        token(s, "A", x + 12, y + 11, 6.0)
    else:
        xmark(s, x + 12, y + 11, 4.4, 1.7, halo=False)
    s.text(x + 24, y + 14.2, head, 9, 700)
    for k, ln in enumerate(lines):
        s.text(x + 6, y + 27 + k * LEAD, ln, 9)
    return h


APL_EX_LEVELS = (3, 3, 2, 2)
APL_BENCH_LEVEL = 5
APL_SWAP_OUT = 2


def fig74():
    s = Svg(FULL_W)
    aw, bx = 246, 258
    bw = FULL_W - bx
    # ---------------- Panel A: the rule ----------------
    panel_title(s, 0, 0, "A", "Calculating APL (6.14)")
    y = 19
    steps = ["Add together the Levels of all Heroes in the Active Party.",
             "Divide by the number of Heroes in the Active Party.",
             "**Round down.**"]
    for i, t in enumerate(steps, 1):
        h = _step_tile(s, 0, y, aw, i, t)
        y += h
        if i < len(steps):
            vflow_arrow(s, 13, y, y + 12)
            y += 12
    y += 8
    w2 = (aw - 6) / 2.0
    h1 = _icon_box(s, 0, y, w2, "ok", "Counts", "Heroes in the Active Party selected for that adventure.")
    h2 = _icon_box(s, w2 + 6, y, w2, "no", "Does not count", "Hirelings, Summons, and Heroes on the Bench.")
    y += max(h1, h2) + 8
    s.text(0, y + 7.5, "Which Active Party is used", 9, 700)
    y += 12
    for t in ("**Before the first adventure of a campaign:** use the starting Active Party.",
              "**During an adventure:** calculate APL using only the Heroes in the Active Party selected for that adventure.",
              "**During the following Town Phase:** continue using the APL of the Active Party that completed that adventure; do not recalculate it after swapping Heroes."):
        h = _text_box(s, 0, y, aw, t, fill=PALE)
        y += h + 3
    ya = y
    # ---------------- Panel B: worked example ----------------
    panel_title(s, bx, 0, "B", "Example (assumed values)")
    y = 19
    intro = ("Assumes a standard Active Party of 4 Heroes (11.1.2) and that no Hero changes Level during the example. "
             "The Level of each Hero is shown inside the token.")
    for k, ln in enumerate(wrap(intro, bw, 9)):
        s.text(bx, y + 8 + k * LEAD, ln, 9)
    y += len(wrap(intro, bw, 9)) * LEAD + 5
    # Active Party frame
    s.rect(bx, y, bw, 44, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
    s.text(bx + 6, y + 12, "Active Party", 9, 700)
    for i, lv in enumerate(APL_EX_LEVELS):
        _level_token(s, bx + 22 + i * 34, y + 30, lv)
    s.text(bx + 22 + 4 * 34 - 6, y + 33, "Levels 3, 3, 2, and 2", 9)
    y += 44 + 6
    # Not counted frame
    s.rect(bx, y, bw, 36, fill=PALE, stroke=INK, sw=0.9, rx=2.5, dash="3 2")
    s.text(bx + 6, y + 12, "Not counted", 9, 700)
    cxs = [bx + 14, bx + 100, bx + 176]
    xmark(s, cxs[0], y + 26, 4.4, 1.7, halo=False)
    _level_token(s, cxs[0] + 17, y + 26, APL_BENCH_LEVEL, 7.5)
    s.text(cxs[0] + 29, y + 29, "Bench Hero", 9)
    xmark(s, cxs[1] + 8, y + 26, 4.4, 1.7, halo=False)
    s.text(cxs[1] + 17, y + 29, "Hireling", 9)
    xmark(s, cxs[2] + 6, y + 26, 4.4, 1.7, halo=False)
    s.text(cxs[2] + 15, y + 29, "Summon", 9)
    y += 36 + 8
    total = sum(APL_EX_LEVELS)
    n = len(APL_EX_LEVELS)
    calc = ["Add: 3 + 3 + 2 + 2 = %d." % total,
            "Divide: %d ÷ %d = %s." % (total, n, ("%.2f" % (total / n)).rstrip("0")),
            "Round down: **APL %d**." % (total // n)]
    for i, t in enumerate(calc, 1):
        h = _step_tile(s, bx, y, bw, i, t, min_h=20)
        y += h
        if i < len(calc):
            vflow_arrow(s, bx + 13, y, y + 12)
            y += 12
    y += 8
    new_total = total - APL_SWAP_OUT + APL_BENCH_LEVEL
    town = ("**Town Phase:** the Level %d Bench Hero swaps in for a Level %d Hero. The Town Phase still uses APL %d; "
            "do not recalculate it. **Next adventure:** Levels 3, 3, 2, and %d give %d ÷ %d = %s, rounded down to **APL %d**."
            % (APL_BENCH_LEVEL, APL_SWAP_OUT, total // n, APL_BENCH_LEVEL, new_total, n,
               ("%.2f" % (new_total / n)).rstrip("0"), new_total // n))
    h = _text_box(s, bx, y, bw, town, fill=PALE)
    y += h
    return s, max(ya, y) + 3


# ---------------------------------------------------------------------
# FIG-75  6.17 Party Building Guidelines
# ---------------------------------------------------------------------
LEFT_75 = [
    "Both sides field the same number of Heroes unless the scenario says otherwise.",
    "**Before creating Heroes:** choose a Hero Level from **1–10**. Every Hero begins at that Level unless the scenario says otherwise.",
    "**Above Level 1:** first complete Hero creation at Level 1. Then resolve **Gaining a Level** once for each additional Level without paying Training Costs.",
    "**Before deployment:** pool all starting coins. Each party may spend those coins at list price on items or equipment normally available through **Buy and Sell Goods** in **11.2.4**. Assign purchased items to Hero inventories and equip them legally. Discard all unspent coins when the adventure begins.",
    "**After completing all creation, advancement, purchases, and equipment choices:** set each Hero's current HP, NRG, and Luck equal to their final maximum values.",
]
RIGHT_75 = [
    "Rules that resolve during a Town Phase, Aftermath Phase, or later adventure have no effect unless the scenario says otherwise.",
    "Matched one-off play does not use Hirelings unless the scenario explicitly allows them.",
    "Both sides use the same campaign restrictions, if any.",
    "Apply the rare ancestry limit in **6.9 Ancestries**: each party may field no more than **1 Hero** with a rare ancestry.",
    "If using random creation, apply the matched-play restrictions in **6.5**: matched competitive play ignores all Random Ancestry, Random Background, Random Class, and Random Starting Package Bonuses.",
]
LADDER_LEVEL = 4


def fig75():
    s = Svg(FULL_W)
    cw = 246
    rx = 258
    _bar(s, 0, 0, cw, 1, "Building each party")
    y = 24
    for t in LEFT_75:
        h = _text_box(s, 0, y, cw, t, fill=WHITE, sw=0.9)
        y += h + 4
    ya = y - 4
    _bar(s, rx, 0, cw, 2, "Limits that also apply")
    y = 24
    for t in RIGHT_75:
        h = _text_box(s, rx, y, cw, t, fill=WHITE, sw=0.9)
        y += h + 4
    y += 2
    # level ladder example
    s.text(rx, y + 7.5, "Example (assumed value): Hero Level %d chosen" % LADDER_LEVEL, 9, 700)
    y += 14
    bw_, gp = 46, 20
    for i in range(LADDER_LEVEL):
        x = rx + i * (bw_ + gp)
        s.rect(x, y, bw_, 17, fill=(PALE if i == 0 else WHITE), stroke=INK, sw=0.9, rx=2.5)
        s.text(x + bw_ / 2, y + 12, "Level %d" % (i + 1), 9, 700, "middle")
        if i < LADDER_LEVEL - 1:
            hflow_arrow(s, x + bw_ + 1.5, x + bw_ + gp - 1.5, y + 8.5)
    y += 17 + 4
    steps_n = LADDER_LEVEL - 1
    y = s.para(rx, y + 8, "Create at Level 1, then resolve **Gaining a Level** %d times (%d - 1), with no Training Costs." % (steps_n, LADDER_LEVEL), cw, 9, lead=LEAD) - 8
    return s, max(ya, y) + 3


# ---------------------------------------------------------------------
# FIG-76  7.3 Reading Item Entries
# ---------------------------------------------------------------------
ORDER_76 = ["action or cost", "range or target", "procedure", "effect", "duration", "restrictions or exceptions"]
# Table fields of the two quoted entries: (column header, cell value); the last column carries the rules text.
FIELDS_SHOVEL = [("Item", "Shovel"), ("Cost (c)", "1"), ("In-Game Effect", None)]
FIELDS_SPIDERMILK = [("d20", "4"), ("Item", "Spidermilk Venom"), ("Cost (c)", "2"), ("Effect", None)]
ARMOUR_HEAD = ["Armour", "Cost (c)", "AD", "STR Req", "DEX Pen", "Max Speed", "Rule"]
# Quoted text by element index (0-5) in the source order of 7.3; elements not listed are omitted by the entry.
SHOVEL = {
    0: "**Interact [2 AP]:**",
    1: "Choose an origin within **1\"** and **LOS**.",
    3: "Remove **Difficult Terrain** from the **Aura 1\"** area around that origin",
    4: "for the remainder of the adventure.",
    5: "This does not remove magical, hazardous, or scenario-locked terrain effects.",
}
SPIDERMILK = {
    3: "The weapon attack deals an additional **1d4 poison damage**; target's **Speed** is reduced by 2\"",
    4: "until the end of the round.",
}


def _fields_table(s, x, y, w, fields):
    """Two-row mini table: column headers (grey) over cell values; the rules-text column is black."""
    widths = [max(tw(h, 9, 600), tw('see below', 9, 600)) + 8 if v is None else max(tw(h, 9, 600), tw(v, 9, 400)) + 8 for h, v in fields]
    k = w / float(sum(widths))
    widths = [wd * k for wd in widths]
    cx = x
    for (head, val), wd in zip(fields, widths):
        s.rect(cx, y, wd, 14, fill=LIGHT, stroke=INK, sw=0.7)
        s.text(cx + wd / 2, y + 10.2, head, 9, 600, "middle")
        if val is None:
            s.rect(cx, y + 14, wd, 14, fill=INK, stroke=INK, sw=0.7)
            s.text(cx + wd / 2, y + 24.2, "see below", 9, 600, "middle", WHITE)
        else:
            s.rect(cx, y + 14, wd, 14, fill=WHITE, stroke=INK, sw=0.7)
            s.text(cx + wd / 2, y + 24.2, val, 9, 400, "middle")
        cx += wd
    return 28


def fig76():
    s = Svg(FULL_W)
    panel_title(s, 0, 0, "A", "Anatomy of two real item entries (quoted from 7.16 and 7.14)")
    y = 20
    lw, cw, gp = 128, 178, 6
    c1 = lw + gp
    c2 = c1 + cw + gp
    s.text(c1, y + 7.5, "**Shovel** (7.16)", 9)
    s.text(c2, y + 7.5, "**Spidermilk Venom** (7.14)", 9)
    y += 12
    _fields_table(s, c1, y, cw, FIELDS_SHOVEL)
    _fields_table(s, c2, y, cw, FIELDS_SPIDERMILK)
    s.text(0, y + 10.2, "Table fields", 9, 700)
    s.text(0, y + 24.2, "Entry values", 9, 700)
    y += 28 + 7
    s.text(0, y + 7.5, "Rules text, in the order 7.3 gives", 9, 700)
    y += 12
    ys = []
    for i in range(len(ORDER_76)):
        cells = [wrap(col[i], cw - 10, 9) if i in col else None for col in (SHOVEL, SPIDERMILK)]
        nl = max(len(c) if c else 1 for c in cells)
        h = max(16.5, nl * LEAD + 5)
        ys.append((y, h))
        for col_i, (cx, c) in enumerate(zip((c1, c2), cells)):
            if c:
                s.rect(cx, y, cw, h, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
                for k, ln in enumerate(c):
                    s.text(cx + 5, y + 10.4 + k * LEAD, ln, 9)
            else:
                s.rect(cx, y, cw, h, fill=PALE, stroke=INK, sw=0.7, rx=2.5, dash="3 2")
                note = "not in this entry"
                if i == 0 and col_i == 1:
                    note = "not in this entry; the cost is set by 7.14.1"
                s.text(cx + 5, y + 10.4, note, 9, 400, "start", "#555", italic=True)
        y += h + 3
    # order column: numbered circles joined by a line
    cxn = 10
    s.line(cxn, ys[0][0] + ys[0][1] / 2, cxn, ys[-1][0] + ys[-1][1] / 2, INK, 1.2)
    for i, (yy, hh) in enumerate(ys):
        callout(s, cxn, yy + hh / 2, i + 1)
        s.text(cxn + 12, yy + hh / 2 + 3.3, ORDER_76[i], 9, 600)
    s.line(0, y, FULL_W, y, MID, 0.6)
    y += 4
    # other categories use other fields
    s.text(0, y + 10.2, "Other tables use other fields, for example 7.10 Armour:", 9, 600)
    x = FULL_W - sum(tw(c, 9, 600) + 8 for c in ARMOUR_HEAD)
    for i, c in enumerate(ARMOUR_HEAD):
        w = tw(c, 9, 600) + 8
        dark = (i == len(ARMOUR_HEAD) - 1)
        s.rect(x, y, w, 14, fill=(INK if dark else LIGHT), stroke=INK, sw=0.7)
        s.text(x + w / 2, y + 10.2, c, 9, 600, "middle", WHITE if dark else INK)
        x += w
    y += 14 + 5
    note = ("Item entries use the core terminology and procedures in **Sections 2, 4, 5,** and **7.2**; apply those rules unless an entry gives a specific exception. "
            "Entries include enough operational information to resolve ordinary use without unnecessary reference chains.")
    h = _text_box(s, 0, y, FULL_W, note, fill=PALE)
    y += h
    return s, y + 3


# ---------------------------------------------------------------------
# FIG-77  7.4 Stacking and Precedence
# ---------------------------------------------------------------------
def _chip(s, x, y, text, weight=600, fill=WHITE, dash=None):
    w = tw(text, 9, weight) + 10
    s.rect(x, y, w, 15, fill=fill, stroke=INK, sw=0.9, rx=2.5, dash=dash)
    s.text(x + w / 2, y + 10.8, text, 9, weight, "middle")
    return w


def fig77():
    s = Svg(FULL_W)
    cw, rx = 246, 258
    # ---------------- left column ----------------
    panel_title(s, 0, 0, "A", "What stacks and what does not")
    y = 19
    h = _step_tile(s, 0, y, cw, 1,
                   "If 2 item effects would modify the same statistic, **Reaction**, **Check**, or non-damage roll, apply only the "
                   "**single highest bonus** and the **single worst penalty** unless a rule explicitly says the effects stack. "
                   "Damage dice and damage modifiers stack under **5.4**.", fill=WHITE)
    y += h
    ex = "Example (assumed values), same Check: two item bonuses, +1 and +2, apply +2. Two item penalties, -1 and -3, apply -3."
    h = _text_box(s, 12, y + 3, cw - 12, ex, fill=PALE)
    s.line(6.5, y + 0.5, 6.5, y + 3 + h / 2, INK, 1.0)
    s.line(6.5, y + 3 + h / 2, 12, y + 3 + h / 2, INK, 1.0)
    y += h + 7
    h = _step_tile(s, 0, y, cw, 4,
                   "**AV bonuses** from different equipped locations stack. Two effects from the **same named item** never stack.")
    y += h + 8
    panel_title(s, 0, y, "B", "Damage type and damage order")
    y += 19
    h = _step_tile(s, 0, y, cw, 2, "If two effects would change a weapon's damage type, the **most recent effect** applies.")
    y += h + 5
    h = _step_tile(s, 0, y, cw, 3,
                   "If a rule would both **replace** and **modify** damage, resolve the replacement first, then apply modifiers.")
    y += h
    ya = y
    # ---------------- right column ----------------
    panel_title(s, rx, 0, "C", "Cross-reference and overrides")
    y = 19
    h = _step_tile(s, rx, y, cw, 5, "If a combatant is both **Hidden** and **Invisible**, follow **2.8.5**.")
    y += h + 5
    lines = wrap("If a rule says a combatant **cannot be chosen as the target** of attacks, Powers, or Special Abilities", cw - 50, 9, 700)
    boxh = _lines_h(lines) + 10
    nun = len(wrap("Unless another rule explicitly says they can affect untargetable targets.", cw - 12, 9))
    cont_h = 5 + boxh + 21 + 19 + 19 + nun * LEAD + 3
    s.rect(rx, y, cw, cont_h, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
    callout(s, rx + 13, y + 13, 6)
    s.rect(rx + 26, y + 5, cw - 32, boxh, fill=INK, stroke=INK, sw=0.9, rx=2.5)
    for k, ln in enumerate(lines):
        s.text(rx + 31, y + 5 + 12 + k * LEAD, ln.replace("**", ""), 9, 700, "start", WHITE)
    ay = y + 5 + boxh
    cxm = rx + cw / 2
    vflow_arrow(s, cxm, ay + 1, ay + 17)
    s.text(cxm + 8, ay + 13, "overrides", 9, 700)
    cy = ay + 21
    x = rx + 6
    for c in ("Hidden", "Invisible", "LOS", "adjacency"):
        x += _chip(s, x, cy, c) + 4
    cy += 19
    _chip(s, rx + 6, cy, "rules that ignore targeting restrictions")
    cy += 19
    for k, ln in enumerate(wrap("Unless another rule explicitly says they can affect untargetable targets.", cw - 12, 9)):
        s.text(rx + 6, cy + 8 + k * LEAD, ln, 9)
    y = y + cont_h + 8
    panel_title(s, rx, y, "D", "Placement and Reactions")
    y += 19
    h = _step_tile(s, rx, y, cw, 7,
                   "If an effect places a combatant in an illegal space, place that combatant in the nearest legal space instead. Forced movement follows **4.4.6**.")
    y += h + 5
    h = _step_tile(s, rx, y, cw, 8,
                   "If an item duplicates a **Reaction** such as **Block** or **Parry**, follow the item text exactly. If an item does not change the normal **Reaction** timing or cost, use the core rule.")
    y += h
    yb = y
    s.text(0, ya + 6 + 7.5, "Circled numbers follow the bullet order of 7.4.", 9, 400, "start", "#333")
    ya += 6 + 11
    return s, max(ya, yb) + 3


# ---------------------------------------------------------------------
# self-check: arithmetic, ordering, height limits, and quotation against the active manuscript
# ---------------------------------------------------------------------
MAX_H = {"72": 310, "73": 245, "74": 330, "75": 305, "76": 285, "77": 285}

# (phrase, first source line, last source line): each phrase must occur verbatim (bold markup and case ignored)
# in that source range and in the figure's own text.
QUOTES = {
    "72": [(re.sub(r"\*\*", "", st), 2030, 2039) for st in STEPS_72] + [
        (FORMULA_ABILITY, 2041, 2043), (FORMULA_HP, 2045, 2047),
        ("After calculating each base value, apply every applicable ancestry, background, class, Talent, item, and random-generation modifier.", 2049, 2049),
        ("Use 6.4 Hero Attributes for Initiative Bonus and Max NRG.", 2049, 2049),
    ],
    "73": [(re.sub(r"\*\*", "", r), 2067, 2083) for r in RECORDS_73] + [
        ("Initiative Bonus = INT + SPI", 2087, 2087),
        ("Base Max NRG = Level + (2 × Primary Casting Score), minimum 0 for non-Martial classes that cast Powers.", 2088, 2088),
        ("Then apply any background, ancestry, talent, item, or class feature that modifies Max NRG.", 2088, 2088),
        ("Recalculate Max NRG whenever the Hero's Level, Primary Casting Score, or a permanent Max NRG modifier changes.", 2088, 2088),
        ("Martial classes always have Max NRG 0 and cannot gain Max NRG unless a rule explicitly grants a replacement benefit.", 2088, 2088),
        ("Unless a rule explicitly says otherwise", 2094, 2094),
        ("current HP, NRG, and Luck cannot exceed the", 2094, 2094),
        ("Unless a rule says otherwise:", 2085, 2085),
        ("excess gained or restored is lost", 2094, 2094), ("Temporary HP is separate.", 2094, 2094),
        ("Max HP cannot fall below 1.", 2092, 2092),
        ("Carried Coins records only coins currently carried on the battlefield.", 2096, 2096),
        ("In campaign play, secured coins belong to the party's shared Treasury, not to an individual Hero.", 2096, 2096),
        ("Record current HP, NRG, and Luck separately from their maximum values.", 2096, 2096),
    ],
    "74": [
        ("Add together the Levels of all Heroes in the Active Party.", 3240, 3240),
        ("Divide by the number of Heroes in the Active Party.", 3241, 3241),
        ("Round down.", 3242, 3242),
        ("Heroes in the Active Party selected for that adventure", 3236, 3236),
        ("Hirelings, Summons, and Heroes on the Bench", 3244, 3244),
        ("Before the first adventure of a campaign: use the starting Active Party.", 0, 0),
        ("calculate APL using only the Heroes in the Active Party selected for that adventure", 3236, 3236),
        ("continue using the APL of the Active Party that completed that adventure", 3236, 3236),
        ("do not recalculate it after swapping Heroes", 3236, 3236),
    ],
    "75": [(re.sub(r"\*\*", "", t_), 3329, 3338) for t_ in (LEFT_75[0], RIGHT_75[0], RIGHT_75[1], RIGHT_75[2])] + [
        ("choose a Hero Level from 1–10. Every Hero begins at that Level unless the scenario says otherwise.", 3330, 3330),
        ("first complete Hero creation at Level 1. Then resolve Gaining a Level once for each additional Level without paying Training Costs.", 3331, 3331),
        ("pool all starting coins. Each party may spend those coins at list price on items or equipment normally available through Buy and Sell Goods in 11.2.4. "
         "Assign purchased items to Hero inventories and equip them legally. Discard all unspent coins when the adventure begins.", 3332, 3332),
        ("After completing all creation, advancement, purchases, and equipment choices", 3333, 3333),
        ("set each Hero's current HP, NRG, and Luck equal to their final maximum values.", 3333, 3333),
        ("Apply the rare ancestry limit in 6.9 Ancestries", 3337, 3337),
        ("each party may field no more than 1 Hero with a rare ancestry", 2207, 2207),
        ("If using random creation, apply the matched-play restrictions in 6.5", 3338, 3338),
        ("matched competitive play ignores all Random Ancestry, Random Background, Random Class, and Random Starting Package Bonuses.", 0, 0),
    ],
    "76": [
        ("Interact [2 AP]:", 4656, 4656),
        ("Choose an origin within 1\" and LOS.", 4656, 4656),
        ("Remove Difficult Terrain from the Aura 1\" area around that origin", 4656, 4656),
        ("for the remainder of the adventure.", 4656, 4656),
        ("This does not remove magical, hazardous, or scenario-locked terrain effects.", 4656, 4656),
        ("The weapon attack deals an additional 1d4 poison damage; target's Speed is reduced by 2\"", 4329, 4329),
        ("until the end of the round.", 4329, 4329),
        ("action or cost", 3413, 3413), ("range or target", 3413, 3413), ("procedure", 3413, 3413),
        ("duration", 3413, 3413), ("restrictions or exceptions", 3413, 3413),
        ("Item entries use the core terminology and procedures in Sections 2, 4, 5, and 7.2", 3411, 3411),
        ("apply those rules unless an entry gives a specific exception", 3411, 3411),
        ("include enough operational information to resolve ordinary use without unnecessary reference chains", 3413, 3413),
        ("In-Game Effect", 4633, 4633), ("Effect", 4324, 4324), ("Spidermilk Venom", 4329, 4329),
        ("Armour", 3713, 3713), ("Max Speed", 3713, 3713),
    ],
    "77": [
        ("If 2 item effects would modify the same statistic, Reaction, Check, or non-damage roll, apply only the single highest bonus and the single worst penalty unless a rule explicitly says the effects stack. Damage dice and damage modifiers stack under 5.4.", 3417, 3417),
        ("AV bonuses from different equipped locations stack. Two effects from the same named item never stack.", 3420, 3420),
        ("If two effects would change a weapon's damage type, the most recent effect applies.", 3418, 3418),
        ("If a rule would both replace and modify damage, resolve the replacement first, then apply modifiers.", 3419, 3419),
        ("If a rule says a combatant cannot be chosen as the target of attacks, Powers, or Special Abilities", 3422, 3422),
        ("Hidden", 3422, 3422), ("Invisible", 3422, 3422), ("LOS", 3422, 3422), ("adjacency", 3422, 3422),
        ("rules that ignore targeting restrictions", 3422, 3422),
        ("unless another rule explicitly says they can affect untargetable targets", 3422, 3422),
        ("If a combatant is both Hidden and Invisible, follow 2.8.5.", 3421, 3421),
        ("If an effect places a combatant in an illegal space, place that combatant in the nearest legal space instead. Forced movement follows 4.4.6.", 3423, 3423),
        ("If an item duplicates a Reaction such as Block or Parry, follow the item text exactly. If an item does not change the normal Reaction timing or cost, use the core rule.", 3424, 3424),
    ],
}

def _norm(x):
    return re.sub(r"\s+", " ", re.sub(r"\*\*", "", x)).strip().lower()


def _svg_text(svg_obj, h):
    svg = svg_obj.render(h)
    parts = re.findall(r"<text[^>]*>(.*?)</text>", svg, flags=re.S)
    out = []
    for p in parts:
        p = re.sub(r"<[^>]+>", "", p)
        p = p.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        out.append(p)
    return _norm(" ".join(out))


def selfcheck_end_c():
    import os
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "source", "Heraldry_RC522.md")
    src = open(src_path, encoding="utf-8").read().split("\n")

    def src_range(lo, hi):
        return _norm(" ".join(src[lo - 1:hi]))

    # structure and ordering
    assert len(STEPS_72) == 10 and len(RECORDS_73) == 15
    assert len(LEFT_75) + len(RIGHT_75) == 10                      # the ten bullets of 6.17
    assert ORDER_76 == ["action or cost", "range or target", "procedure", "effect", "duration", "restrictions or exceptions"]
    assert ", ".join(ORDER_76[:-1]) + ", then " + ORDER_76[-1] in src_range(3413, 3413)
    assert set(SHOVEL) <= set(range(6)) and set(SPIDERMILK) <= set(range(6))
    assert 3 in SHOVEL and 3 in SPIDERMILK and 2 not in SHOVEL and 2 not in SPIDERMILK
    # FIG-73 example: a maximum that falls below current HP drags current HP down; a later increase restores nothing
    cur, mx = 7, 10
    assert cur <= mx
    mx = 6
    cur = min(cur, mx)
    assert (cur, mx) == (6, 6)
    mx = 10
    assert (cur, mx) == (6, 10) and mx >= 1
    # FIG-74 example (Levels 3, 3, 2, 2; Bench Hero Level 5 swapped in for a Level 2 Hero)
    lv = list(APL_EX_LEVELS)
    assert len(lv) == 4 and sum(lv) == 10 and sum(lv) / len(lv) == 2.5 and sum(lv) // len(lv) == 2
    lv2 = list(lv)
    lv2.remove(APL_SWAP_OUT)
    lv2.append(APL_BENCH_LEVEL)
    assert sorted(lv2) == [2, 3, 3, 5] and sum(lv2) == 13 and sum(lv2) / 4 == 3.25 and sum(lv2) // 4 == 3
    # FIG-75 example: Level 4 chosen (legal 1-10) needs 4 - 1 = 3 Gaining a Level resolutions
    assert 1 <= LADDER_LEVEL <= 10 and LADDER_LEVEL - 1 == 3
    # FIG-77 example values: highest bonus +2 of (+1, +2); worst penalty -3 of (-1, -3)
    assert max(1, 2) == 2 and min(-1, -3) == -3
    # heights and quotation
    for n, limit in MAX_H.items():
        svg_obj, h = globals()["fig" + n]()
        assert h <= limit, "FIG-%s height %.1f exceeds %s" % (n, h, limit)
        stream = _svg_text(svg_obj, h)
        for phrase, lo, hi in QUOTES[n]:
            ph = _norm(phrase)
            assert ph in stream, "FIG-%s: phrase missing from figure: %r" % (n, phrase)
            if lo:
                assert ph in src_range(lo, hi), "FIG-%s: phrase not in source lines %d-%d: %r" % (n, lo, hi, phrase)
    # the two figure-only merged phrases: both halves are in the source
    assert "before the first adventure of a campaign, use the starting active party." in src_range(3236, 3236)
    assert "matched competitive play may use the random creation tables, but ignores all random ancestry" in src_range(2138, 2138)
    assert "| item | cost (c) | in-game effect |" in src_range(4633, 4633)
    assert "| d20 | item | cost (c) | effect |" in src_range(4324, 4324) and "| 4 | spidermilk venom | 2 |" in src_range(4329, 4329)
    return True


if __name__ == "__main__":
    selfcheck_end_c()
    print("selfcheck_end_c ok")
