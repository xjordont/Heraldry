#!/usr/bin/env python3
"""The illustrated Hero Record: one generator for the blank sheet and the 24 Basic Mode Heroes.

  python3 assets/hero-record/sheet.py blank [--png]           # rewrite hero-record-front/reverse.html
  python3 assets/hero-record/sheet.py heroes [--only NAME] [--pdf FILE] [--no-png]

Static artwork and lettering live in parts/front.html and parts/reverse.html; shared type and
fonts in sheet.css. Every ledger, field and filled value is built here from one geometry spec, so
the blank and the populated sheets cannot drift apart. Hero data comes from
typst/heroes/basic-heroes.json (B.4 of the active manuscript, via tools/hero_cards.py).

Populated output goes to build/hero-records/ and is never committed (docs/LARGE_FILES.md).
Builds fail on any text that overflows its cell, type below 9 pt, or B.4 rules or item text
missing from a Hero's pages.
"""
import argparse
import base64
import html
import json
import math
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = json.loads((ROOT / "typst/heroes/basic-heroes.json").read_text())
esc = html.escape
R = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")

# ================================================================ geometry (CSS px, 96 per inch, Letter)
FRAME_BOTTOM = 37.81 + 980.38 - 2          # inner edge of the 2 px page frame
X0, X1 = 50.87, 763.71                     # ledger edges shared by both sides
FIRST = 44.0                               # Type and Qty columns
HEAD_PX, HEAD_ABOVE, BAR_ABOVE, GAP = 13, 16.6, 14.0, 2.6
TEXT_GAP = 6.05                            # a value's baseline sits this far above its rule, like the labels

# identity cartouches
NAME_BOX = (92.0, 161.0, 340.0, 196.0)
ROW2_Y = (211.0, 241.0)
_cw = (585.0 - 92.0 - 20.0) / 3
ID_COLS = {"class": (92.0, 92.0 + _cw), "ancestry": (92.0 + _cw + 10, 92.0 + 2 * _cw + 10),
           "background": (92.0 + 2 * _cw + 20, 585.0)}
NOTCH, OUT_W, IN_W, INSET = 8.0, 2.6, 1.0, 3.6
LEVEL_C = (742.8, 218.7)
SHIELD = (587.63, 44.49, 185.31, 197.38)
SHIELD_FIELD = (598.6, 744.2, 59.0, 229.9)  # x0, x1, y0, y1 of the white field inside the inner rule

# attribute shields: field axis (measured from the art) and the optical centre of each white field
STAT_AXIS = {"STR": 97.12, "DEX": 200.80, "INT": 304.00, "SPI": 406.24, "INIT": 508.48, "SPD": 612.96, "SIZE": 716.32}
STAT_FIELD_TOP, STAT_CENTRE = 289.8, 319.5
STAT_PX = 28.0
CAP_H = 0.66                               # Source Sans 3 cap height (em)
ASC, DESC = 1.024, 0.400                   # Source Sans 3 hhea metrics (em)

RES_CX = {"HP": (122.94, 259.61), "NRG": (384.21, 491.78), "Luck": (603.61, 710.82)}
RES_CY = 419.0
COIN_C, COIN_R = (681.1, 844.6), 62.0       # inner circle of the Coins ring

# front ledgers
ARM_RULE, ARM_PITCH = 467.65 + 57.15, 35.0
ARM_COLS = [("Type", FIRST), ("Name", 111.5), ("AD", 34), ("AV", 34), ("DEX Pen", 60), ("Max SPD", 60), ("Traits", None)]
ARM_X1 = 503.85
WOUND_CX, WOUND_X0 = 552.0, 574.85
WPN_RULE, WPN_PITCH = 602.85 + 57.15, 18.4
WPN_COLS = [("Weapon", FIRST + 180), ("Hands", 46), ("Damage and Type", 150), ("Range", 80), ("Traits", None)]
INV_RULE, INV_ROWS = 723.25 + 57.15, 14
INV_PITCH = (FRAME_BOTTOM - INV_RULE) / INV_ROWS
INV_X1 = 593.31
INV_COLS = [("Qty", FIRST), ("Item", 180), ("Effect", None), ("Location", 60)]

# reverse
BAND = {"powers": ("hr-pbandB4.svg", 51.19, "Powers", 66.87, 6.36),
        "talents": ("hr-tbandB4.svg", 49.77, "Talents &amp; Special Abilities", 65.05, 6.11)}
BAND_X, BAND_W, BAND_PX = 39.87, 733.44, 34
BAND_TO_RULE, SECTION_GAP, BACK_ROWS, BACK_PITCH = 71.45, 8.05, 14, 25.15
POW_TOP = 161.1
POW_COLS = [("Name", 175), ("Tier", 46), ("Cost", 60), ("Range", 70), ("Effect", None)]
TAL_COLS = [("Name", 175), ("Type / Level", 110), ("Cost", 66), ("Effect", None)]

# filled text
PAD, BODY_PX, BACK_LEAD, BACK_VPAD = 5.0, 12.0, 13.0, 3.0


def edges(x0, x1, cols):
    fixed = sum(w for _, w in cols if w is not None)
    out = [x0]
    for _, w in cols:
        out.append(out[-1] + (w if w is not None else (x1 - x0) - fixed))
    return out


# ================================================================ drawing primitives
def div(cls, x, y, w, inner, style="", lines=None):
    wpart = f" width: {R(w)}px;" if w is not None else ""
    data = f' data-lines="{lines}"' if lines is not None else ""
    return f'<div class="{cls}"{data} style="left: {R(x)}px; top: {R(y)}px;{wpart}{style}">{inner}</div>'


def baseline_in_box(px, lead):
    return (lead - (ASC + DESC) * px) / 2 + ASC * px


def ledger(x0, x1, rule0, pitch, rows, cols, rule_rows=None, end_bar=False, bar_to=None, spans=(), full_rules=()):
    """Column bars and horizontal rules. rule_rows: row boundaries to rule (0 = header rule; default all).
    spans: (r0, r1) row ranges with no bars (a full-width block); full_rules: boundaries ruled unbroken."""
    e = edges(x0, x1, cols)
    bars = e[1:-1] + ([x1] if end_bar else [])
    rule_rows = range(rows + 1) if rule_rows is None else rule_rows
    top = rule0 - BAR_ABOVE
    bottom = bar_to if bar_to is not None else rule0 + pitch * rows
    ox, oy = x0 - 4, top - 2
    w, h = (x1 + 4) - ox, bottom + 2 - oy
    segs = []
    for k in rule_rows:
        y = rule0 + pitch * k
        if k in full_rules:
            segs.append(f"M{R(x0-ox)} {R(y-oy)}H{R(x1-ox)}")
            continue
        start = x0
        for b in bars:
            segs.append(f"M{R(start-ox)} {R(y-oy)}H{R(b-GAP-ox)}")
            start = b + GAP
        if not end_bar:
            segs.append(f"M{R(start-ox)} {R(y-oy)}H{R(x1-ox)}")
    runs, y = [], top
    for r0, r1 in sorted(spans):
        runs.append((y, rule0 + pitch * r0))
        y = rule0 + pitch * r1
    runs.append((y, bottom))
    barpath = "".join(f"M{R(b-ox)} {R(a-oy)}V{R(c-oy)}" for b in bars for a, c in runs if c > a)
    svg = (f'<svg aria-hidden="true" width="{R(w)}" height="{R(h)}" viewBox="0 0 {R(w)} {R(h)}" '
           f'style="position: absolute; left: {R(ox)}px; top: {R(oy)}px; overflow: visible">'
           f'<path d="{"".join(segs)}" fill="none" stroke="#000000" stroke-width="1"></path>'
           f'<path d="{barpath}" fill="none" stroke="#000000" stroke-width="2.5"></path></svg>')
    heads = [f'<div class="hr-l hr-c" style="left: {R(a)}px; top: {R(rule0-HEAD_ABOVE)}px; width: {R(b-a)}px; '
             f'font-size: {HEAD_PX}px">{label}</div>' for (label, _), a, b in zip(cols, e, e[1:]) if label]
    return [svg] + heads, e


def wrap_svg(parts, ax, ay, bx, by, attrs='aria-hidden="true"'):
    return (f'<svg {attrs} width="{R(bx-ax)}" height="{R(by-ay)}" viewBox="{R(ax)} {R(ay)} {R(bx-ax)} {R(by-ay)}" '
            f'style="position: absolute; left: {R(ax)}px; top: {R(ay)}px; overflow: visible">' + "".join(parts) + "</svg>")


def notch_path(x0, y0, x1, y1, r=NOTCH, i=0.0):
    """Cartouche with concave quarter-round corners; i insets it for the engraved inner rule."""
    rr = r + i
    k = math.sqrt(rr * rr - i * i)
    X0, Y0, X1, Y1 = x0 + i, y0 + i, x1 - i, y1 - i
    a = f"A{R(rr)} {R(rr)} 0 0 0 "
    return (f"M{R(x0+k)} {R(Y0)}H{R(x1-k)}{a}{R(X1)} {R(y0+k)}V{R(y1-k)}{a}{R(x1-k)} {R(Y1)}"
            f"H{R(x0+k)}{a}{R(X0)} {R(y1-k)}V{R(y0+k)}{a}{R(x0+k)} {R(Y0)}Z")


def cartouches():
    specs = [("Name", *NAME_BOX)] + [(k.title(), a, ROW2_Y[0], b, ROW2_Y[1]) for k, (a, b) in ID_COLS.items()]
    parts, out = [], []
    for label, x0, y0, x1, y1 in specs:
        parts.append(f'<path d="{notch_path(x0, y0, x1, y1)}" fill="#ffffff" stroke="#000000" stroke-width="{OUT_W}"></path>')
        parts.append(f'<path d="{notch_path(x0, y0, x1, y1, i=INSET)}" fill="none" stroke="#000000" stroke-width="{IN_W}"></path>')
        out.append(f'<div class="hr-legend" style="left: {R(x0 + NOTCH + 6)}px; top: {R(y0 - 6.5)}px">'
                   f'<span class="hr-lz"></span>{label}<span class="hr-lz hr-lz-r"></span></div>')
    xs = [s[1] for s in specs] + [s[3] for s in specs]
    ys = [s[2] for s in specs] + [s[4] for s in specs]
    return [wrap_svg(parts, min(xs) - 3, min(ys) - 3, max(xs) + 3, max(ys) + 3)] + out


def lozenges(bottoms, w=22, h=25, sw=3):
    cx = WOUND_CX
    parts = [f'<polygon points="{cx},{R(yb-h)} {R(cx+w/2)},{R(yb-h/2)} {cx},{R(yb)} {R(cx-w/2)},{R(yb-h/2)}" fill="#ffffff" '
             f'stroke="#000000" stroke-width="{sw}" stroke-linejoin="miter"></polygon>' for yb in bottoms]
    return wrap_svg(parts, cx - w / 2 - 3, min(bottoms) - h - 3, cx + w / 2 + 3, max(bottoms) + 3,
                    'role="img" aria-label="Three wound markers"')


def on_rule(cls, x0, x1, rule_y, inner, center=False, lead=13.0, gap=TEXT_GAP, lines=None):
    """One line of filled text whose baseline sits `gap` above a rule, between two column edges."""
    style = f" font-size: {R(BODY_PX)}px; line-height: {R(lead)}px;" + (" text-align: center;" if center else "")
    return div(cls, x0 + PAD, rule_y - gap - baseline_in_box(BODY_PX, lead) - (lead * (lines - 1) if lines else 0),
               x1 - x0 - 2 * PAD, inner, style, lines=lines)


def value_top(px, centre):
    """Top of a line-height-1 box whose capitals are centred on `centre`."""
    return centre - baseline_in_box(px, px) + CAP_H * px / 2


CAPTION = {"size": 12, "weight": 400, "fill": "#333333", "spacing": 0.4}   # secondary ink (design tokens: 0.2 grey)
STAT_ARCH_R = 104.0      # the white field's top edge is a gentle arch of about this radius
COIN_ARCH_R = COIN_R     # the Coins ring's inner circle


def curved_caption(ident, cx, cy, r, text, label):
    """Small, quiet text that follows a field's curved top: baseline on a circle of radius r about (cx, cy),
    centred on the axis. Used for the attribute fields' base and the Coins ring's starting coins."""
    path = f"M{R(cx-r)} {R(cy)} A{R(r)} {R(r)} 0 0 1 {R(cx+r)} {R(cy)}"
    c = CAPTION
    return (f'<svg role="img" aria-label="{label}" class="hr-arc" width="{R(2*r)}" height="{R(r)}" '
            f'viewBox="{R(cx-r)} {R(cy-r)} {R(2*r)} {R(r)}" style="position: absolute; left: {R(cx-r)}px; top: {R(cy-r)}px; '
            f'overflow: visible"><defs><path id="{ident}" d="{path}"></path></defs>'
            f'<text font-family="\'Source Sans 3\', sans-serif" font-weight="{c["weight"]}" font-size="{c["size"]}" '
            f'letter-spacing="{c["spacing"]}" text-anchor="middle" fill="{c["fill"]}">'
            f'<textPath href="#{ident}" startOffset="50%">{text}</textPath></text></svg>')


def field_caption(key, text):
    """Top of a DEX or SPD field: the base value, following the arched top edge."""
    r = STAT_ARCH_R
    return curved_caption(f"hr-cap-{key.lower()}", STAT_AXIS[key], STAT_FIELD_TOP + r, r - 13.0, text, f"{key} base")


def arc_caption(text):
    """Inside top of the Coins ring: the starting coins, like LEVEL in its circle."""
    return curved_caption("hr-coin-arc", COIN_C[0], COIN_C[1], COIN_ARCH_R - 12.5, text, "Starting coins")


# ================================================================ B.4 profile parsing
def runs_html(runs):
    return "".join(f"<b>{esc(t)}</b>" if b else esc(t) for t, b in runs)


def flat(runs):
    return "".join(t for t, _ in runs)


def split_head(runs):
    """Split '**Name [cost]:** rest' into (name, cost, rest_runs). Items without a colon are name-only."""
    text = flat(runs)
    head, pos = "", 0
    for i, (t, b) in enumerate(runs):
        if not b and t.strip():
            break
        head += t
        pos = i + 1
        if ":" in t:
            break
    if ":" not in head:
        if text.strip() and ":" not in text:
            return text.strip(), "", []
        head, pos = "", 0
    rest = runs[pos:]
    name = head.rstrip().rstrip(":").strip()
    cost = ""
    m = re.search(r"\s*\[([^\]]+)\]\s*$", name)
    if m:
        cost, name = m.group(1), name[:m.start()].strip()
    if rest and not rest[0][1]:
        rest = [(rest[0][0].lstrip(), False)] + rest[1:]
        if not rest[0][0]:
            rest = rest[1:]
    return name, cost, rest


def take_prefix(rest, label):
    """If rest starts with '**Label:** value. ', remove it and return (value, rest)."""
    if len(rest) >= 2 and rest[0][1] and rest[0][0].strip() == label + ":":
        m = re.match(r"\s*([^.]+?)\.\s*(.*)$", rest[1][0], re.S)
        if m and not rest[1][1]:
            return m.group(1).strip(), ([(m.group(2), False)] if m.group(2) else []) + rest[2:]
    return None, rest


def section(h, title):
    return next((s["items"] for s in h["sections"] if s["title"] == title), [])


DAMAGE = re.compile(r"^\d*d\d+")
WEAPON_KIND = re.compile(r"^(Melee|Ranged|Thrown) weapon\b")
CARRIED = re.compile(r"Carried only: this Hero does not meet its ([^.]+)\.")


def parse_equipment(h):
    chest = shield = None
    weapons, inventory = [], []
    for it in section(h, "Equipment and Items"):
        name, cost, rest = split_head(it["runs"])
        text = flat(rest)
        qty = 1
        m = re.match(r"^(\d+)\s+(.*)$", name)
        if m:
            qty, name = int(m.group(1)), m.group(2)
        bolds = [t.strip() for t, b in rest if b]
        if re.match(r"\s*Chest\b", text) and "AD d" in text:
            chest = armour_row(name, text)
        elif re.match(r"\s*Shield\b", text):
            shield = armour_row(name, text, shield=True)
        elif not cost and (WEAPON_KIND.match(text) or (bolds and DAMAGE.match(text.strip()))):
            weapons.append(weapon_row(name, qty, rest, text))
        else:
            inventory.append({"qty": qty, "name": name + (f" [{cost}]" if cost else ""), "runs": rest})
    return chest, shield, weapons, inventory


def armour_row(name, text, shield=False):
    pen = re.search(r"DEX Pen (-?\d+)", text)
    spd = re.search(r'Max Speed (\d+)"', text)
    traits = []
    if shield and "when using Block" in text:
        traits.append("Block only")
    if "add +1 to the Targe's AD roll" in text:
        traits.append("+1 AD vs melee")
    return {"name": name, "ad": re.search(r"AD (d\d+)", text).group(1), "av": "—",
            "pen": int(pen.group(1)) if pen else 0, "spd": int(spd.group(1)) if spd else None, "traits": ", ".join(traits)}


def weapon_row(name, qty, rest, text):
    bolds = [t.strip() for t, b in rest if b]
    dmg = [b for b in bolds if DAMAGE.match(b)]
    if len(dmg) == 2:   # Versatile: one-handed and two-handed dice of the same type
        a = re.match(r"(\S+) \+ (\w+) (\w+) damage", dmg[0])
        b = re.match(r"(\S+) \+ (\w+) (\w+) damage", dmg[1])
        damage = f"{a.group(1)}/{b.group(1)} + {a.group(2)} {a.group(3)}"
    else:
        damage = dmg[0].replace(" damage", "")
    hands = "1/2" if "one-handed or" in text else "2" if "two-handed" in text else "1"
    ranged = next((b for b in bolds if b.startswith("Ranged ")), None)
    thrown = next((b for b in bolds if b.startswith("Thrown ")), None)
    rng = "Melee"
    if ranged:
        rng = ranged.split(" ", 1)[1]
    elif thrown:
        rng = thrown.split(" ", 1)[1] if text.startswith("Thrown weapon") else "Melee / " + thrown.split(" ", 1)[1]
    traits = [("Thrown" if b.startswith("Thrown ") else b) for b in bolds
              if b not in dmg and not b.startswith("Ranged ") and not re.fullmatch(r"\d+(\.\d+)*", b)]
    carried = CARRIED.search(text)
    if carried:
        traits = ["Carried only: " + carried.group(1)]
    return {"name": name + (f" ({qty})" if qty > 1 else ""), "hands": hands, "damage": damage, "range": rng,
            "traits": ", ".join(dict.fromkeys(traits))}


def natural_weapons(h):
    """Ancestry natural weapons (Ratkin Teeth) belong in the Weapons table too."""
    out = []
    for it in section(h, "Ancestry Traits"):
        name, cost, rest = split_head(it["runs"])
        text = flat(rest)
        if "natural melee weapon occupying" in text:
            dm = re.search(r"(\d*d\d+) (\w+) damage", text)
            traits = [t.strip() for t, b in rest if b and t.strip() in ("Finesse", "Light", "Agile")]
            out.append({"name": name, "hands": "0", "damage": f"{dm.group(1)} + DEX {dm.group(2)}", "range": "Melee",
                        "traits": ", ".join(traits)})
    return out


TIER0 = re.compile(r"Cantrips|Orisons|Minor Rituals|Techniques|Tier 0")
# Senses restated briefly (owner request 2026-10-26); the full reminder is in B.4 and the rulebook.
SENSES = {"Darkvision": "Within {r}, ignore Cover and visual penalties from nonmagical Darkness. "
                        "Does not reveal Hidden or Invisible combatants; magical Darkness still applies."}
CARD_POINTER = "Form Rules and the Novice Beast Forms"


def entry(name, kind, cost, rest):
    return {"name": name, "type": kind, "cost": cost or "—", "html": runs_html(rest), "text": flat(rest)}


def parse_rules(h):
    """Powers (anything costing NRG) and Talents & Special Abilities. Weapon trait rules are universal
    rules and are not repeated here (owner decision 2026-10-26)."""
    powers, talents = [], []
    for it in section(h, "Ancestry Traits"):
        name, cost, rest = split_head(it["runs"])
        talents.append(entry(name, "Ancestry", cost, rest))
    sense = h["stats"].get("Senses")
    if sense:
        m = re.match(r"(.*?Darkvision) \((\d+\")\)", sense)
        talents.append({"name": sense, "type": "Senses", "cost": "—", "text": SENSES["Darkvision"].format(r=m.group(2)),
                        "html": esc(SENSES["Darkvision"].format(r=m.group(2)))})
    for it in section(h, "Background Rule"):
        name, cost, rest = split_head(it["runs"])
        talents.append(entry(name, "Background", cost, rest))
    for it in section(h, "Talents, Powers, and Special Rules"):
        name, cost, rest = split_head(it["runs"])
        if "NRG" in cost:
            rng, rest2 = take_prefix(rest, "Range")
            tier = "0" if TIER0.search(name) else ("1" if rng else "—")
            powers.append({"name": name, "tier": tier, "cost": cost, "range": rng or ("Varies" if TIER0.search(name) else "—"),
                           "html": runs_html(rest2), "text": flat(rest2)})
        else:
            e = entry(name, f"Class / {h['level']}", cost, rest)
            if it["sub"]:
                e["html"] += f"<br>See the {esc(name)} card for {CARD_POINTER}."
            talents.append(e)
    return powers, talents


def card_items(h):
    out = []
    for it in section(h, "Talents, Powers, and Special Rules"):
        if it["sub"]:
            name, cost, _rest = split_head(it["runs"])
            out.append((name, cost, [(split_head(s)[0], runs_html(split_head(s)[2])) for s in it["sub"]]))
    return out


def effective(h, chest, shield):
    """Effective DEX (printed DEX plus the worse equipped DEX Pen) and SPD (capped by every Max Speed)."""
    base_dex = int(h["scores"]["DEX"])
    pens = [a["pen"] for a in (chest, shield) if a]
    pen = min(pens) if pens else 0
    base_spd = int(h["stats"]["SPD"].rstrip('"'))
    caps = [a["spd"] for a in (chest, shield) if a and a["spd"] is not None]
    return base_dex, pen, base_dex + pen, base_spd, min([base_spd] + caps)


def signed(n):
    return f"+{n}" if n >= 0 else f"−{-n}"


# ================================================================ text measurement (real fonts, Chromium)
class Measurer:
    def __init__(self, page, out_dir):
        self.page = page
        f = out_dir / "_measure.html"
        f.write_text(page_html("measure", "", out_dir, extra_css=".m{position:absolute;left:0;top:0;font-family:'Source Sans 3';"
                                                                "font-weight:400;white-space:normal;overflow-wrap:break-word} .m b{font-weight:600}"))
        page.goto(f.as_uri())
        page.evaluate("""async () => { for (const f of ["400 12px 'Source Sans 3'", "600 12px 'Source Sans 3'",
            "700 12px 'Source Sans 3'", "700 12px 'Grenze Gotisch'", "700 12px 'Source Serif 4'"]) await document.fonts.load(f); }""")
        loaded = page.evaluate("() => [...document.fonts].filter(f => f.status === 'loaded').length")
        if loaded < 5:
            raise SystemExit(f"measurement fonts did not load ({loaded})")
        self.file = f

    def lines(self, items):
        """items: (html, width, px, lead, weight) -> line counts."""
        return self.page.evaluate("""(items) => items.map(([h, w, px, lead, wt]) => {
            const d = document.createElement('div'); d.className = 'm';
            Object.assign(d.style, {width: w + 'px', fontSize: px + 'px', lineHeight: lead + 'px', fontWeight: wt});
            d.innerHTML = h; document.body.appendChild(d);
            const n = Math.round(d.getBoundingClientRect().height / lead); d.remove(); return n; })""", items)

    def width(self, items):
        """items: (html, px, weight, family) -> widths."""
        return self.page.evaluate("""(items) => items.map(([h, px, wt, fam]) => {
            const d = document.createElement('span'); d.className = 'm';
            Object.assign(d.style, {whiteSpace: 'nowrap', fontSize: px + 'px', fontWeight: wt, fontFamily: fam});
            d.innerHTML = h; document.body.appendChild(d); const w = d.getBoundingClientRect().width; d.remove(); return w; })""", items)


# ================================================================ pages
def page_html(title, body, out_dir, extra_css=""):
    base = os.path.relpath(HERE, out_dir).replace(os.sep, "/") + "/"
    style = f"\n<style>{extra_css}</style>" if extra_css else ""
    return (f'<!doctype html>\n<html lang="en-CA">\n<head>\n<meta charset="utf-8">\n<title>{esc(title)}</title>\n'
            f'<base href="{base}">\n<link rel="stylesheet" href="sheet.css">{style}\n</head>\n<body>\n'
            f'<div style="position: relative; width: 816px; height: 1056px; overflow: hidden; background: #ffffff; '
            f"color: #000000; font-family: 'Source Sans 3', sans-serif\">\n{body}\n</div>\n</body>\n</html>\n")


def front_body(h=None, m=None):
    static = (HERE / "parts/front.html").read_text()
    out = cartouches()
    # attribute fields: DEX and SPD carry their base at the top; every value is centred in its field
    if h is None:
        for k in ("DEX", "SPD"):
            out.append(field_caption(k, "Base"))
    # armour + wounds
    arm, ae = ledger(X0, ARM_X1, ARM_RULE, ARM_PITCH, 2, ARM_COLS, end_bar=True)
    arm_ys = [ARM_RULE + ARM_PITCH * i for i in range(3)]
    out += arm
    for label, y in (("Chest", arm_ys[1]), ("Shield", arm_ys[2])):
        out.append(f'<div class="hr-l hr-c" style="left: {R(X0)}px; top: {R(y - HEAD_ABOVE)}px; width: {R(FIRST)}px; '
                   f'font-size: {HEAD_PX}px">{label}</div>')
    out.append(lozenges(arm_ys))
    out += [f'<div class="hr-rule" style="left: {R(WOUND_X0)}px; top: {R(y - 0.5)}px; width: {R(X1 - WOUND_X0)}px"></div>'
            for y in arm_ys]
    wpn, we = ledger(X0, X1, WPN_RULE, WPN_PITCH, 3, WPN_COLS)
    inv, ie = ledger(X0, INV_X1, INV_RULE, INV_PITCH, INV_ROWS, INV_COLS, rule_rows=range(INV_ROWS),
                     end_bar=True, bar_to=FRAME_BOTTOM + 1)
    out += wpn + inv
    out.append(arc_caption("Start" if h is None else f"Start {esc(h['stats']['Coins'])}"))
    portrait = ""
    if h is not None:
        fill, portrait = front_values(h, m, ae, we, ie)
        out += fill
    return static.replace("<!-- @portrait -->", portrait) + "\n".join(out)


def front_values(h, m, ae, we, ie):
    out = []
    # identity
    x0, y0, x1, y1 = NAME_BOX
    px = 27.0
    w = m.width([(esc(h["name"]), px, 700, "Grenze Gotisch")])[0]
    px *= min(1.0, (x1 - x0 - 30) / w)
    out.append(div("hname", x0 + 15, (y0 + y1) / 2 - px * 0.52, None, esc(h["name"]), f" font-size: {R(px)}px;"))
    for key, (a, b) in ID_COLS.items():
        px = 15.0
        w = m.width([(esc(h[key]), px, 700, "Source Serif 4")])[0]
        px *= min(1.0, (b - a - 26) / w)
        out.append(div("hid", a + 13, sum(ROW2_Y) / 2 - px * 0.47, None, esc(h[key]), f" font-size: {R(px)}px;"))
    out.append(div("hv", LEVEL_C[0] - 20, value_top(22, LEVEL_C[1] + 9), 40, esc(h["level"]), " font-size: 22px;"))
    # attributes
    chest, shield, weapons, inventory = parse_equipment(h)
    weapons += natural_weapons(h)
    base_dex, pen, eff_dex, base_spd, eff_spd = effective(h, chest, shield)
    sc = h["scores"]
    init = int(sc["INT"]) + int(sc["SPI"])
    vals = {"STR": signed(int(sc["STR"])), "DEX": signed(eff_dex), "INT": signed(int(sc["INT"])),
            "SPI": signed(int(sc["SPI"])), "INIT": signed(init), "SPD": f'{eff_spd}"', "SIZE": h["stats"]["Sz"]}
    for k, cx in STAT_AXIS.items():
        out.append(div("hv", cx - 40, value_top(STAT_PX, STAT_CENTRE), 80, esc(vals[k]), f" font-size: {R(STAT_PX)}px;"))
    # DEX: base and the worse equipped DEX Pen (just the base when nothing equipped imposes one)
    out.append(field_caption("DEX", f"{signed(base_dex)} \u2212 {-pen}" if pen < 0 else f"Base {signed(base_dex)}"))
    out.append(field_caption("SPD", f'Base {base_spd}"'))
    # resources: maximums printed, current left for play
    for k, (cur, mx) in RES_CX.items():
        out.append(div("hres", mx - 40, RES_CY - 14, 80, esc(h["stats"][k]), " font-size: 28px;"))
    # armour
    for i, row in enumerate((chest, shield)):
        if not row:
            continue
        y = ARM_RULE + ARM_PITCH * (i + 1)
        cells = [(row["name"], False, "hf nm"), (row["ad"], True, "hf"), (row["av"], True, "hf"),
                 (signed(row["pen"]) if row["pen"] else "0", True, "hf"), (f'{row["spd"]}"' if row["spd"] else "—", True, "hf")]
        for j, (t, c, cls) in enumerate(cells):
            out.append(on_rule(cls, ae[j + 1], ae[j + 2], y, esc(t), center=c))
        if row["traits"]:
            n = m.lines([(esc(row["traits"]), ae[7] - ae[6] - 2 * PAD, BODY_PX, 13.0, 400)])[0]
            out.append(on_rule("hf wrap", ae[6], ae[7], y, esc(row["traits"]), lines=n))
    # weapons
    if len(weapons) > 3:
        raise SystemExit(f"{h['name']}: {len(weapons)} weapons do not fit the 3 weapon rows")
    for i, wp in enumerate(weapons):
        y = WPN_RULE + WPN_PITCH * (i + 1)
        cells = [(wp["name"], False, "hf nm"), (wp["hands"], True, "hf"), (wp["damage"], False, "hf"),
                 (wp["range"], True, "hf"), (wp["traits"], False, "hf")]
        for j, (t, c, cls) in enumerate(cells):
            out.append(on_rule(cls, we[j], we[j + 1], y, esc(t), center=c))
    # inventory: every other item, its effect running line by line on the ledger rules
    eff_w = ie[3] - ie[2] - 2 * PAD
    counts = m.lines([(runs_html(it["runs"]), eff_w, BODY_PX, INV_PITCH, 400) for it in inventory])
    name_counts = m.lines([(esc(it["name"]), ie[2] - ie[1] - 2 * PAD, BODY_PX, INV_PITCH, 600) for it in inventory])
    row = 0
    for it, n, nn in zip(inventory, counts, name_counts):
        n = max(n, nn, 1)
        first = INV_RULE + INV_PITCH * (row + 1)
        gap = TEXT_GAP - 1.5     # 16.8 px rows: sit a little lower to clear the rule above
        out.append(on_rule("hf", ie[0], ie[1], first, str(it["qty"]), center=True, lead=INV_PITCH, gap=gap))
        for cls, a, b, inner in (("hf wrap nm", ie[1], ie[2], esc(it["name"])), ("hf wrap", ie[2], ie[3], runs_html(it["runs"]))):
            out.append(div(cls, a + PAD, first - gap - baseline_in_box(BODY_PX, INV_PITCH), b - a - 2 * PAD, inner,
                           f" font-size: {R(BODY_PX)}px; line-height: {R(INV_PITCH)}px;", lines=n))
        out.append(on_rule("hf", ie[3], ie[4], first, "Carried", center=True, lead=INV_PITCH, gap=gap))
        row += n
    if row > INV_ROWS:
        raise SystemExit(f"{h['name']}: inventory needs {row} rows; the sheet has {INV_ROWS}")
    return out, portrait_html(h)


def portrait_html(h):
    """The Hero's ink portrait, centred on its own ink in the shield field and masked to it."""
    from PIL import Image
    import numpy as np
    src = ROOT / "assets/art/ink" / f"{h['art']}.png"
    with Image.open(src) as im:
        a = np.array(im.convert("LA"))[:, :, 1] > 128
        W, H = im.size
    ys, xs = np.where(a)
    fx0, fx1, fy0, fy1 = SHIELD_FIELD
    height = (fy1 - fy0) * 1.12 * H / (ys.max() - ys.min())   # figure a little taller than the field
    k = height / H
    left = (fx0 + fx1) / 2 - k * (xs.min() + xs.max()) / 2
    top = fy0 + 7 - k * ys.min()
    mask = "data:image/png;base64," + base64.b64encode((HERE / "art/hr-shield5-mask.png").read_bytes()).decode()
    sx, sy, sw, sh = SHIELD
    return (f'<div role="img" aria-label="{esc(h["name"])} portrait" style="position: absolute; left: {R(sx)}px; top: {R(sy)}px; '
            f'width: {R(sw)}px; height: {R(sh)}px; overflow: hidden; -webkit-mask-image: url({mask}); mask-image: url({mask}); '
            f'-webkit-mask-size: 100% 100%; mask-size: 100% 100%"><img src="../art/ink/{h["art"]}.png" alt="" '
            f'style="position: absolute; left: {R(left - sx)}px; top: {R(top - sy)}px; height: {R(height)}px"></div>')


# ---------------------------------------------------------------- reverse
def band(kind, top):
    img, hgt, title, tx, ty = BAND[kind]
    return [f'<img src="art/{img}" alt="" aria-hidden="true" style="position: absolute; left: {R(BAND_X)}px; top: {R(top)}px; '
            f'width: {R(BAND_W)}px; height: {R(hgt)}px">',
            f'<h2 class="hr-band" style="left: {R(tx)}px; top: {R(top + ty)}px; font-size: {BAND_PX}px">{title}</h2>']


def block_rows(lines):
    n = 1
    while math.floor((n * BACK_PITCH - 2 * BACK_VPAD) / BACK_LEAD) < lines:
        n += 1
    return n


def back_layout(entries, cols, m, pitch):
    """Ruled rows each entry needs: its tallest cell, at the dense leading, rounded up to whole rows."""
    e = edges(X0, X1, cols)
    items, idx = [], []
    for k, ent in enumerate(entries):
        for c, (inner, wt, _center) in ent.items():
            items.append((inner, e[c + 1] - e[c] - 2 * PAD, BODY_PX, BACK_LEAD, wt))
            idx.append(k)
    need = [1] * len(entries)
    for k, n in zip(idx, m.lines(items)):
        need[k] = max(need[k], n)
    rows = []
    for n in need:
        r = 1
        while math.floor((r * pitch - 2 * BACK_VPAD) / BACK_LEAD) < n:
            r += 1
        rows.append(r)
    return need, rows


def back_table(entries, need, rows, cols, rule0, pitch, n_rows, close_on_frame):
    e = edges(X0, X1, cols)
    out, row, bounds = [], 0, [0]
    for ent, n_lines, n in zip(entries, need, rows):
        top = rule0 + pitch * row
        y = top + (pitch * n - n_lines * BACK_LEAD) / 2 - 0.4
        for c, (inner, wt, center) in ent.items():
            style = f" font-size: {R(BODY_PX)}px; line-height: {R(BACK_LEAD)}px;" + (" text-align: center;" if center else "")
            out.append(div("hf wrap nm" if wt == 600 else "hf wrap", e[c] + PAD, y, e[c + 1] - e[c] - 2 * PAD, inner, style, lines=n_lines))
        row += n
        bounds.append(row)
    rule_rows = sorted(set(bounds + list(range(row, n_rows + 1))))
    if close_on_frame:
        rule_rows = [r for r in rule_rows if r < n_rows]
    svg, _ = ledger(X0, X1, rule0, pitch, n_rows, cols, rule_rows=rule_rows,
                    bar_to=FRAME_BOTTOM + 1 if close_on_frame else None)
    return svg + out


TITLE = (114.99, 64.88, 59.8, 400.0)       # left, top, size, widest the title may run before the ruins


def title(text, m=None):
    x, y, px, room = TITLE
    if m is not None:
        w = m.width([(text, px, 700, "Grenze Gotisch")])[0]
        if w > room:
            y += (px - px * room / w) * 0.62   # keep the baseline where it was
            px *= room / w
    return f'<h1 class="hr-title" style="left: {R(x)}px; top: {R(y)}px; font-size: {R(px)}px">{text}</h1>'


def reverse_body(h=None, m=None):
    static = (HERE / "parts/reverse.html").read_text()
    powers, talents = parse_rules(h) if h is not None else (None, None)
    out = [title("Talents &amp; Abilities" if h is not None and not powers else "Powers &amp; Talents", m)]
    if h is not None and not powers:
        # purely martial Heroes: Talents & Special Abilities take the whole reverse
        rule0 = POW_TOP + BAND_TO_RULE
        n_rows = round((FRAME_BOTTOM - rule0) / BACK_PITCH)
        pitch = (FRAME_BOTTOM - rule0) / n_rows
        out += band("talents", POW_TOP)
        ents = [tcell(t) for t in talents]
        need, rows = back_layout(ents, TAL_COLS, m, pitch)
        if sum(rows) > n_rows:
            raise SystemExit(f"{h['name']}: Talents need {sum(rows)} rows; the page has {n_rows}")
        out += back_table(ents, need, rows, TAL_COLS, rule0, pitch, n_rows, True)
        return static + "\n".join(out)
    pow_rule = POW_TOP + BAND_TO_RULE
    if h is None:
        p_n = BACK_ROWS
    else:
        # The boundary between Powers and Talents moves per Hero: each table gets the rows its entries
        # need, and the spare rows are shared out for notes, so nothing has to move to the wrong table.
        p_ents, t_ents = [pcell(p) for p in powers], [tcell(t) for t in talents]
        p_need, p_rows = back_layout(p_ents, POW_COLS, m, BACK_PITCH)
        t_need, t_rows = back_layout(t_ents, TAL_COLS, m, BACK_PITCH)
        spare = 2 * BACK_ROWS - sum(p_rows) - sum(t_rows)
        if spare < 0:
            raise SystemExit(f"{h['name']}: Powers need {sum(p_rows)} rows and Talents {sum(t_rows)}; "
                             f"the reverse has {2 * BACK_ROWS}")
        p_n = sum(p_rows) + spare // 2
    t_n = 2 * BACK_ROWS - p_n
    tal_top = pow_rule + p_n * BACK_PITCH + SECTION_GAP
    tal_rule = tal_top + BAND_TO_RULE
    out += band("powers", POW_TOP) + band("talents", tal_top)
    if h is None:
        out += ledger(X0, X1, pow_rule, BACK_PITCH, BACK_ROWS, POW_COLS)[0]
        out += ledger(X0, X1, tal_rule, BACK_PITCH, BACK_ROWS, TAL_COLS, rule_rows=range(BACK_ROWS), bar_to=FRAME_BOTTOM + 1)[0]
        return static + "\n".join(out)
    out += back_table(p_ents, p_need, p_rows, POW_COLS, pow_rule, BACK_PITCH, p_n, False)
    out += back_table(t_ents, t_need, t_rows, TAL_COLS, tal_rule, BACK_PITCH, t_n, True)
    return static + "\n".join(out)


def cost_html(cost):
    return "<br>".join(esc(x.strip()) for x in cost.split(","))


def pcell(p):
    return {0: (esc(p["name"]), 600, False), 1: (esc(p["tier"]), 400, True), 2: (cost_html(p["cost"]), 400, True),
            3: (esc(p["range"]), 400, True), 4: (p["html"], 400, False)}


def tcell(t):
    return {0: (esc(t["name"]), 600, False), 1: (esc(t["type"]), 400, True), 2: (cost_html(t["cost"]), 400, True),
            3: (t["html"], 400, False)}


# ---------------------------------------------------------------- reference card (sub-items, e.g. Wild Shape)
def card_body(h, name, cost, subs, m):
    X0c, X1c, TOP = 34.61, 780.33, 37.81
    full_w = X1c - X0c - 36
    col_w = full_w / 2 - 9
    out = band("talents", TOP + 8)[:1]
    out.append(f'<h1 class="hr-band" style="left: 65px; top: {R(TOP + 14)}px; font-size: 34px">{esc(name)}</h1>')
    out.append(f'<div class="hr-cap" style="left: 470px; top: {R(TOP + 27)}px; width: 280px; font-size: 12px; '
               f'text-align: right; color: #fff; font-weight: 700">{esc(h["name"])} · {esc(h["class"])} · {esc(cost)}</div>')
    y = TOP + 74
    for sn, sh in [s for s in subs if s[0] == "Form Rules"]:
        inner = f"<b>{esc(sn)}:</b> {sh}"
        n = m.lines([(inner, full_w, BODY_PX, 13.5, 400)])[0]
        out.append(div("hf wrap", X0c + 18, y, full_w, inner, f" font-size: {R(BODY_PX)}px; line-height: 13.5px;", lines=n))
        y += n * 13.5 + 14
    forms = [s for s in subs if s[0] != "Form Rules"]
    yy = y
    for r in range(0, len(forms), 2):
        pair = forms[r:r + 2]
        n = max(m.lines([(sh, col_w, BODY_PX, 13.5, 400) for _, sh in pair]))
        out.append(f'<div class="hr-rule" style="left: {R(X0c + 18)}px; top: {R(yy - 7)}px; width: {R(full_w)}px"></div>')
        for c, (sn, sh) in enumerate(pair):
            gx = X0c + 18 + c * (full_w / 2 + 9)
            out.append(div("hid", gx, yy, None, esc(sn), " font-size: 15px;"))
            out.append(div("hf wrap", gx, yy + 20, col_w, sh, f" font-size: {R(BODY_PX)}px; line-height: 13.5px;", lines=n))
        yy += 20 + n * 13.5 + 14
    out.append(f'<div aria-hidden="true" style="position: absolute; left: {R(X0c + 18 + full_w / 2 - 1.25)}px; top: {R(y - 7)}px; '
               f'width: 2.5px; height: {R(yy - y - 7)}px; background: #000"></div>')
    frame = (f'<div aria-hidden="true" style="position: absolute; left: {R(X0c)}px; top: {R(TOP)}px; width: {R(X1c - X0c)}px; '
             f'height: {R(yy - TOP + 6)}px; box-sizing: border-box; border: 2px solid #000000"></div>')
    return "\n".join([frame] + out)


# ================================================================ checks
def page_text(*files):
    out = []
    for f in files:
        t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", f.read_text(), flags=re.S).replace("<br>", " ")
        out += [html.unescape(re.sub(r"<[^>]+>", "", seg)) for seg in re.findall(r"<(?:div|h1|h2|textPath)[^>]*>(.*?)</(?:div|h1|h2|textPath)>", t, re.S)]
    return "\n".join(re.sub(r"\s+", " ", x) for x in out)


def fidelity(h, files):
    """Every word of the Hero's own rules and items, and their coins, must appear on the Hero's pages."""
    blob = page_text(*files)
    missing = []

    def need(label, text):
        t = re.sub(r"\s+", " ", text).strip()
        if t and t not in blob:
            missing.append(f"{label}: {t[:70]}")

    for title in ("Ancestry Traits", "Background Rule", "Talents, Powers, and Special Rules"):
        for it in section(h, title):
            name, cost, rest = split_head(it["runs"])
            need(name, name)
            rng, rest2 = take_prefix(rest, "Range")
            need(name, flat(rest2 if "NRG" in cost else rest))
            if rng:
                need(name + " range", rng)
            for sub in it["sub"]:
                sn, _c, srest = split_head(sub)
                need(name + " / " + sn, flat(srest))
    for it in section(h, "Equipment and Items"):
        name, cost, rest = split_head(it["runs"])
        need("item", re.sub(r"^\d+\s+", "", name))
    need("coins", "Start " + h["stats"]["Coins"])
    return missing


FIT_JS = """() => [...document.querySelectorAll('.hf, .hv, .hres, .hid, .hname, .hr-arc text')].flatMap(d => {
    const cs = getComputedStyle(d), lead = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize), out = [];
    if (d.dataset.lines) {
        const n = Math.round(d.getBoundingClientRect().height / lead);
        if (n > +d.dataset.lines) out.push(`${n} lines > ${d.dataset.lines}: ${d.textContent.slice(0, 50)}`);
    }
    if (cs.whiteSpace === 'nowrap' && d.style.width && d.scrollWidth > d.clientWidth + 0.5)
        out.push(`too wide (${d.scrollWidth} > ${d.clientWidth}): ${d.textContent.slice(0, 50)}`);
    if (parseFloat(cs.fontSize) < 12) out.push(`below 9 pt: ${d.textContent.slice(0, 40)}`);
    return out; })"""


def render(browser, pages, png=True, pdf=None):
    """Render pages; return {file: problems}. With pdf, write all pages, in order, to one PDF."""
    problems, parts = {}, []
    for f in pages:
        pg = browser.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2550 / 816)
        pg.goto(f.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        bad = pg.evaluate(FIT_JS)
        if bad:
            problems[f.name] = bad
        if png:
            pg.screenshot(path=str(f.with_suffix(".png")))
        if pdf:
            out = f.with_suffix(".pdf")
            pg.pdf(path=str(out), width="8.5in", height="11in", print_background=True, page_ranges="1")
            parts.append(out)
        pg.close()
    if pdf:
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter()
        for f in parts:
            w.add_page(PdfReader(str(f)).pages[0])
        w.write(str(pdf))
        for f in parts:
            f.unlink()
    return problems


def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("what", choices=["blank", "heroes"])
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "build/hero-records")
    ap.add_argument("--only")
    ap.add_argument("--pdf", type=pathlib.Path)
    ap.add_argument("--png", action="store_true", help="blank: also render previews/")
    ap.add_argument("--no-png", action="store_true", help="heroes: skip the 300 dpi PNGs")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        if a.what == "blank":
            pages = [HERE / "hero-record-front.html", HERE / "hero-record-reverse.html"]
            pages[0].write_text(page_html("Hero Record, front", front_body(), HERE))
            pages[1].write_text(page_html("Hero Record, reverse", reverse_body(), HERE))
            problems = render(b, pages, png=False, pdf=a.pdf)
            if a.png:
                (HERE / "previews").mkdir(exist_ok=True)
                for f, name in zip(pages, ("Hero_Record_Front_2550x3300.png", "Hero_Record_Reverse_2550x3300.png")):
                    pg = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2550 / 816)
                    pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
                    pg.screenshot(path=str(HERE / "previews" / name)); pg.close()
        else:
            out_dir = a.out.resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            m = Measurer(b.new_page(), out_dir)
            heroes = [h for h in DATA["heroes"] if not a.only or h["name"].lower() == a.only.lower()]
            pages, cards = [], []
            for h in heroes:
                sl = slug(h["name"])
                files = [out_dir / f"{sl}-front.html", out_dir / f"{sl}-reverse.html"]
                files[0].write_text(page_html(f"{h['name']}, Hero Record front", front_body(h, m), out_dir))
                files[1].write_text(page_html(f"{h['name']}, Hero Record reverse", reverse_body(h, m), out_dir))
                for cname, ccost, subs in card_items(h):
                    cf = out_dir / f"{sl}-{slug(cname)}-card.html"
                    cf.write_text(page_html(f"{h['name']}, {cname} card", card_body(h, cname, ccost, subs, m), out_dir))
                    files.append(cf)
                    cards.append(cf)
                miss = fidelity(h, files)
                if miss:
                    raise SystemExit(f"{h['name']}: text missing from the sheet:\n  " + "\n  ".join(miss))
                pages += files[:2]
            m.file.unlink(missing_ok=True)
            # cards follow every sheet so duplex front/back pairs stay aligned
            problems = render(b, pages + cards, png=not a.no_png, pdf=a.pdf)
        b.close()
    if problems:
        for k, v in problems.items():
            print(k, *v, sep="\n  ", file=sys.stderr)
        raise SystemExit(f"{len(problems)} page(s) have text that does not fit")
    print("PASS: every value fits its cell at 9 pt or larger" + ("; every B.4 rule, item and coin value is printed" if a.what == "heroes" else ""))


if __name__ == "__main__":
    main()
