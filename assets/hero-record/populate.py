#!/usr/bin/env python3
"""Populate the illustrated Hero Record for the 24 Basic Mode Heroes.

  python3 assets/hero-record/populate.py [--out build/hero-records] [--only NAME] [--pdf FILE]

Reads typst/heroes/basic-heroes.json (the B.4 profiles) and the finalized blank sides in this
folder, and writes one front and one reverse HTML page per Hero, plus 300 dpi PNG renders.
With --pdf, also writes all Heroes as one duplex-ready PDF (front, reverse, front, ...).
Output is a build product (docs/LARGE_FILES.md): it is never committed.

Every word of each Hero's ancestry traits, senses reminder, background rule, talents, Powers and
special rules is printed. Weapon trait rules are printed where room remains on the reverse; the
front's Weapons table always names every trait. The script fails if a Hero's rules cannot fit.
"""
import argparse
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

# ---------------------------------------------------------------- finalized blank geometry (CSS px, 96/in)
FRAME_IN_BOTTOM = 37.81 + 980.38 - 2
X0 = 50.87
# front
NAME_BOX = (92.0, 161.0, 340.0, 196.0)
ROW2_Y = (211.0, 241.0)
_cw = (585.0 - 92.0 - 20.0) / 3
ID_BOXES = {"class": (92.0, 92.0 + _cw), "ancestry": (92.0 + _cw + 10, 92.0 + 2 * _cw + 10),
            "background": (92.0 + 2 * _cw + 20, 585.0)}
LEVEL_C = (708.8 + 34, 184.7 + 34)
SHIELD = (587.63, 44.49, 185.31, 197.38)
STAT_X = {"STR": 97.02, "DEX": 200.86, "INT": 303.81, "SPI": 405.87, "INIT": 508.11, "SPD": 612.84, "SIZE": 715.78}
STAT_CY = 327.0
RES_CX = {"HP": (122.94, 259.61), "NRG": (384.21, 491.78), "Luck": (603.61, 710.82)}
RES_CY = 419.0
ARM_RULE, ARM_PITCH = 467.65 + 57.15, 35.0
ARM_EDGES = [50.87, 94.87, 206.37, 240.37, 274.37, 334.37, 394.37, 503.85]
WPN_RULE = (723.25 + 524.8 + 70.0 - 57.15 - 3 * 18.4) / 2 + 57.15
WPN_PITCH = 18.4
WPN_EDGES = [50.87, 94.87, 274.87, 320.87, 470.87, 550.87, 763.71]
INV_RULE = 723.25 + 57.15
INV_ROWS = 14
INV_PITCH = (FRAME_IN_BOTTOM - INV_RULE) / INV_ROWS
INV_EDGES = [50.87, 94.87, 274.87, 533.31, 593.31]
# reverse
BACK_PITCH = 25.15
POW_RULE = 161.1 + 71.45
POW_EDGES = [50.87, 225.87, 271.87, 331.87, 401.87, 763.71]
TAL_RULE = POW_RULE + 14 * BACK_PITCH + 8.05 + 71.45
TAL_EDGES = [50.87, 225.87, 335.87, 401.87, 763.71]
BACK_ROWS = 14

# ---------------------------------------------------------------- type for filled values
PAD = 5.0             # horizontal padding inside a ledger cell
BODY_PX = 12.0        # 9 pt: the repository minimum for printed type
BACK_LEAD = 13.0      # dense rules text, two lines per ruled row
BACK_VPAD = 3.0
R = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
esc = html.escape


# ================================================================ profile parsing
def runs_html(runs):
    out = []
    for t, b in runs:
        t = esc(t)
        out.append(f"<b>{t}</b>" if b else t)
    return "".join(out)


def flat(runs):
    return "".join(t for t, _ in runs)


def split_head(runs):
    """Split '**Name [cost]:** rest' into (name, cost, rest_runs). Items without a colon are name-only."""
    text = flat(runs)
    # the head is the leading bold text up to and including the first ':'
    head, i, pos = "", 0, 0
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
        head = ""
        pos = 0
    rest = runs[pos:]
    # a head like '**Name:** **[1 AP]**' never occurs; costs sit inside the bold head
    name = head.rstrip().rstrip(":").strip()
    cost = ""
    m = re.search(r"\s*\[([^\]]+)\]\s*$", name)
    if m:
        cost, name = m.group(1), name[:m.start()].strip()
    # trim leading space of the rest
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
            value, tail = m.group(1).strip(), m.group(2)
            new = ([(tail, False)] if tail else []) + rest[2:]
            return value, new
    return None, rest


def section(h, title):
    for s in h["sections"]:
        if s["title"] == title:
            return s["items"]
    return []


DAMAGE = re.compile(r"^\d*d\d+")


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
            chest = armour_row(name, rest, text)
        elif re.match(r"\s*Shield\b", text):
            shield = armour_row(name, rest, text, shield=True)
        elif not cost and any(DAMAGE.match(b) for b in bolds):
            weapons.append(weapon_row(name, qty, rest, text))
        else:
            inventory.append({"qty": qty, "name": name + (f" [{cost}]" if cost else ""), "runs": rest})
    return chest, shield, weapons, inventory


def armour_row(name, rest, text, shield=False):
    ad = re.search(r"AD (d\d+)", text).group(1)
    pen = re.search(r"DEX Pen (-?\d+)", text)
    spd = re.search(r'Max Speed (\d+")', text)
    traits = []
    if shield and "when using Block" in text:
        traits.append("Block only")
    if "add **+1**" in "".join((f"**{t}**" if b else t) for t, b in rest) and "Targe" in name:
        traits.append("+1 AD vs melee")
    if "does not count as metal" in text:
        traits.append("Non-metal")
    return {"name": name, "ad": ad, "av": "—", "pen": pen.group(1) if pen else "0",
            "spd": spd.group(1) if spd else "—", "traits": ", ".join(traits)}


def weapon_row(name, qty, rest, text):
    bolds = [t.strip() for t, b in rest if b]
    dmg = [b for b in bolds if DAMAGE.match(b)]
    if len(dmg) == 2:   # Versatile: one-handed and two-handed dice of the same type
        a = re.match(r"(\S+) \+ (\w+) (\w+) damage", dmg[0])
        b = re.match(r"(\S+) \+ (\w+) (\w+) damage", dmg[1])
        damage = f"{a.group(1)}/{b.group(1)} + {a.group(2)} {a.group(3)}"
    else:
        damage = dmg[0].replace(" damage", "")
    if "one-handed or" in text:
        hands = "1/2"
    elif "two-handed" in text:
        hands = "2"
    else:
        hands = "1"
    rng = "Melee"
    ranged = next((b for b in bolds if b.startswith("Ranged ")), None)
    thrown = next((b for b in bolds if b.startswith("Thrown ")), None)
    if ranged:
        rng = ranged.split(" ", 1)[1]
    elif thrown:
        rng = thrown.split(" ", 1)[1] if text.strip().startswith("Thrown weapon") else "Melee / " + thrown.split(" ", 1)[1]
    traits = [b for b in bolds if b not in dmg and not b.startswith("Ranged ")
              and not re.fullmatch(r"\d+(\.\d+)*", b)]          # drop rule cross-references such as 8.2
    traits = ["Thrown" if t.startswith("Thrown ") else t for t in traits]
    if "two-handed" in text and "one-handed or" not in text:
        traits = [t for t in traits]
    return {"name": name + (f" ({qty})" if qty > 1 else ""), "hands": hands, "damage": damage,
            "range": rng, "traits": ", ".join(dict.fromkeys(traits)), "two": hands == "2", "kind": text.split(",")[0].strip()}


def natural_weapons(h):
    """Ancestry natural weapons (Ratkin Teeth) belong in the Weapons table too."""
    out = []
    for it in section(h, "Ancestry Traits"):
        name, cost, rest = split_head(it["runs"])
        text = flat(rest)
        m = re.search(r"natural melee weapon occupying \*?\*?0 Hands", "".join((f"**{t}**" if b else t) for t, b in rest))
        if name == "Teeth" or m:
            dm = re.search(r"(\d*d\d+) (\w+) damage", text)
            traits = [t.strip().rstrip(".") for t, b in rest if b and t.strip() in ("Finesse", "Light", "Agile")]
            out.append({"name": name, "hands": "0", "damage": f"{dm.group(1)} + DEX {dm.group(2)}", "range": "Melee",
                        "traits": ", ".join(traits), "two": False, "kind": "Natural"})
    return out


CARD_POINTER = "Form Rules and the Novice Beast Forms"
TIER0 = re.compile(r"Cantrips|Orisons|Minor Rituals|Techniques|Tier 0")


def parse_rules(h):
    powers, talents = [], []
    for it in section(h, "Ancestry Traits"):
        name, cost, rest = split_head(it["runs"])
        talents.append(entry(name, "Ancestry", cost, rest, it["sub"]))
    sense = h["stats"].get("Senses")
    if sense:
        r = DATA["reminders"]["Superior Darkvision" if sense.startswith("Superior") else "Darkvision"]
        e = entry(sense, "Senses", "", r["runs"], [])
        e["reminder"] = True      # rulebook reminder, not profile text: shortened to its name if room is short
        talents.append(e)
    for it in section(h, "Background Rule"):
        name, cost, rest = split_head(it["runs"])
        talents.append(entry(name, "Background", cost, rest, it["sub"]))
    for it in section(h, "Talents, Powers, and Special Rules"):
        name, cost, rest = split_head(it["runs"])
        if "NRG" in cost:
            rng, rest2 = take_prefix(rest, "Range")
            tier = "0" if TIER0.search(name) else ("1" if rng else "—")
            if rng is None and TIER0.search(name):
                rng = "Varies"
            powers.append({"name": name, "tier": tier, "cost": cost, "range": rng or "—",
                           "html": para(rest2, it["sub"]), "text": flat(rest2)})
        else:
            e = entry(name, f"Class / {h['level']}", cost, rest, [])
            if it["sub"]:
                e["html"] += f"<br>See the {esc(name)} card for {CARD_POINTER}."
            talents.append(e)
    traits = []
    for it in section(h, "Weapon Trait Rules"):
        name, cost, rest = split_head(it["runs"])
        traits.append(entry(name, "Weapon trait", cost, rest, it["sub"]))
    return powers, talents, traits


def para(rest, subs):
    out = runs_html(rest)
    for s in subs:
        out += "<br>" + runs_html(s)
    return out


def entry(name, kind, cost, rest, subs):
    return {"name": name, "type": kind, "cost": cost or "—", "html": para(rest, []), "text": flat(rest),
            "span": "<br>".join(runs_html(x) for x in subs)}


# ================================================================ text measurement (real fonts, Chromium)
class Measurer:
    def __init__(self, page, font_css, out_dir):
        self.page = page
        # a file page, so the file:// fonts load (an about:blank page silently falls back to another font)
        f = out_dir / "_measure.html"
        f.write_text(f"<html><head><style>{font_css}"
                     "body{margin:0} .m{position:absolute;left:0;top:0;font-family:'Source Sans 3';font-weight:400;"
                     "white-space:normal;overflow-wrap:break-word} .m b{font-weight:600}</style></head><body>"
                     "<span style=\"font-family:'Source Sans 3';font-weight:400\">a</span><b style=\"font-family:'Source Sans 3'\">a</b>"
                     "<span style=\"font-family:'Grenze Gotisch';font-weight:700\">a</span>"
                     "<span style=\"font-family:'Source Serif 4';font-weight:700\">a</span></body></html>")
        page.goto(f.as_uri())
        page.evaluate("document.fonts.ready")
        ok = page.evaluate("""() => ["400 12px 'Source Sans 3'", "600 12px 'Source Sans 3'", "700 12px 'Grenze Gotisch'",
                                     "700 12px 'Source Serif 4'"].map(f => document.fonts.check(f))""")
        loaded = page.evaluate("() => [...document.fonts].filter(f => f.status === 'loaded').length")
        if loaded < 4:
            raise SystemExit(f"measurement fonts did not load ({loaded} loaded, checks {ok})")

    def lines(self, items):
        """items: list of (html, width, px, lead, weight). Returns line counts."""
        js = """(items) => items.map(([h, w, px, lead, wt]) => {
            const d = document.createElement('div'); d.className = 'm';
            d.style.width = w + 'px'; d.style.fontSize = px + 'px'; d.style.lineHeight = lead + 'px';
            d.style.fontWeight = wt; d.innerHTML = h; document.body.appendChild(d);
            const n = Math.round(d.getBoundingClientRect().height / lead); d.remove(); return n; })"""
        return self.page.evaluate(js, items)

    def width(self, items):
        js = """(items) => items.map(([h, px, wt, fam]) => {
            const d = document.createElement('span'); d.className = 'm'; d.style.whiteSpace = 'nowrap';
            d.style.fontSize = px + 'px'; d.style.fontWeight = wt; d.style.fontFamily = fam; d.innerHTML = h;
            document.body.appendChild(d); const w = d.getBoundingClientRect().width; d.remove(); return w; })"""
        return self.page.evaluate(js, items)


# ================================================================ HTML pieces
def div(cls, x, y, w, inner, style="", lines=None):
    wpart = f" width: {R(w)}px;" if w is not None else ""
    data = f' data-lines="{lines}"' if lines is not None else ""
    return f'<div class="{cls}"{data} style="left: {R(x)}px; top: {R(y)}px;{wpart}{style}">{inner}</div>'


# Source Sans 3 at 12 px on a 13 px line: baseline sits 10.2 px below the line-box top.
BASE_OFF = 10.2


ASC, DESC = 1.024, 0.400   # Source Sans 3 hhea metrics (em): Chromium places the baseline from these
TEXT_GAP = 6.05            # printed labels (13 px, line-height 1, 16.6 px above a rule) sit this far above it


def baseline_in_box(px, lead):
    return (lead - (ASC + DESC) * px) / 2 + ASC * px


def on_rule(cls, x0, x1, rule_y, inner, center=False, px=BODY_PX, lead=13.0, gap=TEXT_GAP, nowrap=True):
    """One line of text whose baseline sits `gap` above a rule, between two column edges."""
    base = baseline_in_box(px, lead)
    style = f" font-size: {R(px)}px; line-height: {R(lead)}px;" + (" text-align: center;" if center else "")
    return div(cls, x0 + PAD, rule_y - gap - base, x1 - x0 - 2 * PAD, inner, style)


def ledger_svg(x0, x1, top_rule, pitch, rows, edges, rule_rows, bar_to=None, end_bar=False, spans=(), full_rules=()):
    """Column bars over all rows; horizontal rules only at the given row boundaries (0 = header rule)."""
    GAP = 2.6
    bars = edges[1:-1] + ([x1] if end_bar else [])
    top = top_rule - 14.0
    bottom = bar_to if bar_to is not None else top_rule + pitch * rows
    ox, oy = x0 - 4, top - 2
    w, h = (x1 + 4) - ox, bottom + 2 - oy
    segs = []
    for k in rule_rows:
        y = top_rule + pitch * k
        if k in full_rules:     # the edge of a full-width block: one unbroken rule
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
        runs.append((y, top_rule + pitch * r0)); y = top_rule + pitch * r1
    runs.append((y, bottom))
    barpath = "".join(f"M{R(b-ox)} {R(a-oy)}V{R(c-oy)}" for b in bars for a, c in runs if c > a)
    return (f'<svg aria-hidden="true" width="{R(w)}" height="{R(h)}" viewBox="0 0 {R(w)} {R(h)}" '
            f'style="position: absolute; left: {R(ox)}px; top: {R(oy)}px; overflow: visible">'
            f'<path d="{"".join(segs)}" fill="none" stroke="#000000" stroke-width="1"></path>'
            f'<path d="{barpath}" fill="none" stroke="#000000" stroke-width="2.5"></path></svg>')


def block_rows(lines):
    """Ruled rows a reverse entry needs for `lines` text lines at the dense leading."""
    n = 1
    while math.floor((n * BACK_PITCH - 2 * BACK_VPAD) / BACK_LEAD) < lines:
        n += 1
    return n


# ================================================================ pages
FILL_CSS = """
.hf{position:absolute;margin:0;font-family:'Source Sans 3',sans-serif;font-weight:400;color:#000;white-space:nowrap}
.hf b{font-weight:600}
.hf.wrap{white-space:normal;overflow-wrap:break-word}
.hf.nm{font-weight:600}
.hv{position:absolute;margin:0;font-family:'Source Serif 4',serif;font-weight:700;color:#000;text-align:center;white-space:nowrap;line-height:1}
.hname{position:absolute;margin:0;font-family:'Grenze Gotisch',serif;font-weight:700;color:#000;white-space:nowrap;line-height:1}
.hid{position:absolute;margin:0;font-family:'Source Serif 4',serif;font-weight:700;color:#000;white-space:nowrap;line-height:1}
"""


def fonts_css(rel_fonts):
    faces = [("Grenze Gotisch", "100 900", "GrenzeGotisch[wght].ttf"),
             ("Source Sans 3", "400", "SourceSans3-Regular.ttf"),
             ("Source Sans 3", "600", "SourceSans3-Semibold.ttf"),
             ("Source Sans 3", "700", "SourceSans3-Bold.ttf"),
             ("Source Serif 4", "700", "SourceSerif4-Bold.ttf")]
    return "\n".join(f"@font-face{{font-family:'{f}';font-weight:{w};src:url('{rel_fonts}/{p}') format('truetype')}}"
                     for f, w, p in faces)


def retarget(template, out_dir, title):
    """Rewrite a blank side's relative paths for a page written into out_dir."""
    rel_art = os.path.relpath(HERE / "art", out_dir)
    rel_fonts = os.path.relpath(ROOT / "fonts/static", out_dir)
    s = template.replace('src="art/', f'src="{rel_art}/')
    s = re.sub(r"@font-face\{[^}]*\}\n?", "", s)
    s = s.replace("<style>\n@page{size:8.5in 11in;margin:0}\n",
                  "<style>\n@page{size:8.5in 11in;margin:0}\n" + fonts_css(rel_fonts) + "\n" + FILL_CSS, 1)
    s = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", s)
    return s


def build_front(h, m, out_dir):
    s = retarget((HERE / "hero-record-front.html").read_text(), out_dir, f"{h['name']}, Hero Record front")
    add = []
    # identity
    x0, y0, x1, y1 = NAME_BOX
    name_px = 27.0
    w = m.width([(esc(h["name"]), name_px, 700, "Grenze Gotisch")])[0]
    room = x1 - x0 - 30
    if w > room:
        name_px *= room / w
    add.append(div("hname", x0 + 15, (y0 + y1) / 2 - name_px * 0.52, None, esc(h["name"]), f" font-size: {R(name_px)}px;"))
    for key in ("class", "ancestry", "background"):
        a, b = ID_BOXES[key]
        px = 15.0
        cw = m.width([(esc(h[key]), px, 700, "Source Serif 4")])[0]
        if cw > b - a - 26:
            px *= (b - a - 26) / cw
        add.append(div("hid", a + 13, (ROW2_Y[0] + ROW2_Y[1]) / 2 - px * 0.47, None, esc(h[key]), f" font-size: {R(px)}px;"))
    add.append(div("hv", LEVEL_C[0] - 20, LEVEL_C[1] - 4, 40, esc(h["level"]), " font-size: 22px;"))
    # attribute shields
    sc = h["scores"]
    init = int(sc["INT"]) + int(sc["SPI"])
    vals = {**sc, "INIT": f"{init:+d}" if init else "+0", "SPD": h["stats"]["SPD"], "SIZE": h["stats"]["Sz"]}
    for k, cx in STAT_X.items():
        add.append(div("hv", cx - 40, STAT_CY - 15, 80, esc(vals[k]), " font-size: 31px;"))
    # resources: maximums printed, current left for play
    for k, (cur, mx) in RES_CX.items():
        add.append(div("hv", mx - 40, RES_CY - 14, 80, esc(h["stats"][k]), " font-size: 28px;"))
    # armour
    chest, shield, weapons, inventory = parse_equipment(h)
    weapons = natural_weapons(h) + weapons if False else weapons + natural_weapons(h)
    for i, row in enumerate((chest, shield)):
        if not row:
            continue
        y = ARM_RULE + ARM_PITCH * (i + 1)
        e = ARM_EDGES
        add.append(on_rule("hf nm", e[1], e[2], y, esc(row["name"])))
        add.append(on_rule("hf", e[2], e[3], y, esc(row["ad"]), center=True))
        add.append(on_rule("hf", e[3], e[4], y, esc(row["av"]), center=True))
        add.append(on_rule("hf", e[4], e[5], y, esc(row["pen"]), center=True))
        add.append(on_rule("hf", e[5], e[6], y, esc(row["spd"]), center=True))
        # Traits may take two lines; the last one sits on the row's rule like every other value
        n = m.lines([(esc(row["traits"]), e[7] - e[6] - 2 * PAD, BODY_PX, 13.0, 400)])[0] if row["traits"] else 1
        if n > 2:
            raise SystemExit(f"{h['name']}: {row['name']} traits need {n} lines")
        cell = on_rule("hf wrap", e[6], e[7], y, esc(row["traits"]))
        add.append(cell.replace("top: ", "top: ", 1) if n == 1 else
                   re.sub(r"top: ([\d.]+)px", lambda mm: f"top: {R(float(mm.group(1)) - 13.0 * (n - 1))}px", cell, count=1)
                   .replace('class="hf wrap"', f'class="hf wrap" data-lines="{n}"', 1))
    # weapons: the first is Primary; a second one-handed melee weapon is Off-Hand only with no shield
    if len(weapons) > 3:
        raise SystemExit(f"{h['name']}: {len(weapons)} weapons do not fit the 3 weapon rows")
    for i, wp in enumerate(weapons):
        po = ""
        if i == 0 and wp["hands"] != "0":
            po = "P"
        elif (i == 1 and not shield and not weapons[0]["two"] and wp["hands"] == "1"
              and wp["kind"].startswith("Melee") and weapons[0]["hands"] != "0"):
            po = "O"
        y = WPN_RULE + WPN_PITCH * (i + 1)
        e = WPN_EDGES
        cells = [(po, True), (wp["name"], False), (wp["hands"], True), (wp["damage"], False), (wp["range"], True), (wp["traits"], False)]
        for j, (t, c) in enumerate(cells):
            add.append(on_rule("hf nm" if j == 1 else "hf", e[j], e[j + 1], y, esc(t), center=c)) 
    # inventory: effect text runs line by line on the ledger rules
    e = INV_EDGES
    eff_w = e[3] - e[2] - 2 * PAD
    counts = m.lines([(runs_html(it["runs"]), eff_w, BODY_PX, INV_PITCH, 400) for it in inventory])
    name_counts = m.lines([(esc(it["name"]), e[2] - e[1] - 2 * PAD, BODY_PX, INV_PITCH, 600) for it in inventory])
    row = 0
    for it, n, nn in zip(inventory, counts, name_counts):
        n = max(n, nn)
        top_rule = INV_RULE + INV_PITCH * row      # the rule above this entry's first line
        first = top_rule + INV_PITCH
        add.append(on_rule("hf", e[0], e[1], first, str(it["qty"]), center=True))
        add.append(block_div("hf wrap nm", e[1], e[2], first, esc(it["name"]), INV_PITCH, lines=n))
        add.append(block_div("hf wrap", e[2], e[3], first, runs_html(it["runs"]), INV_PITCH, lines=n))
        add.append(on_rule("hf", e[3], e[4], first, "Carried", center=True))
        row += n
    if row > INV_ROWS:
        raise SystemExit(f"{h['name']}: inventory needs {row} rows, the sheet has {INV_ROWS}")
    block = "\n".join(["<!-- populated: " + esc(h["name"]) + " -->", *add])
    # portrait inside the shield's inner rule
    rel_ink = os.path.relpath(ROOT / "assets/art/ink", out_dir)
    import base64
    mask = "data:image/png;base64," + base64.b64encode((HERE / "art/hr-shield5-mask.png").read_bytes()).decode()
    rel_art = os.path.relpath(HERE / "art", out_dir)
    sx, sy, sw, sh = SHIELD
    portrait = (f'<div role="img" aria-label="{esc(h["name"])} portrait" style="position: absolute; left: {R(sx)}px; top: {R(sy)}px; '
                f'width: {R(sw)}px; height: {R(sh)}px; overflow: hidden; -webkit-mask-image: url({mask}); '
                f'mask-image: url({mask}); -webkit-mask-size: 100% 100%; mask-size: 100% 100%">'
                f'<img src="{rel_ink}/{h["art"]}.png" alt="" style="position: absolute; left: 50%; top: 13px; height: 235px; '
                f'transform: translateX(-50%)"></div>\n')
    # the shield's traced art has an opaque white field, so the masked portrait goes just above it
    s = re.sub(r'(<img src="[^"]*/hr-shield5\.svg"[^>]*>\n)', lambda mm: mm.group(1) + portrait, s, count=1)
    return s.replace("\n</body>", "\n" + block + "\n</body>", 1)


def block_div(cls, x0, x1, first_rule, inner, lead, lines=None):
    """Wrapped text whose first baseline sits on `first_rule` and each later line on the next rule."""
    base = baseline_in_box(BODY_PX, lead)
    gap = TEXT_GAP - 1.5    # inventory rows are 16.84 px: sit a little lower to clear the rule above
    return div(cls, x0 + PAD, first_rule - gap - base, x1 - x0 - 2 * PAD, inner,
               f" font-size: {R(BODY_PX)}px; line-height: {R(lead)}px;", lines=lines)


def layout_back(entries, cols, m):
    """entries: list of dict cells {col_index: (html, weight, center)}. Returns rows per entry."""
    items, idx = [], []
    for k, e in enumerate(entries):
        for c, (inner, wt, _center) in ((k, v) for k, v in e.items() if k != "_span"):
            w = cols[c + 1] - cols[c] - 2 * PAD
            items.append((inner, w, BODY_PX, BACK_LEAD, wt))
            idx.append(k)
    counts = m.lines(items)
    need = [1] * len(entries)
    for k, n in zip(idx, counts):
        need[k] = max(need[k], n)
    rows = [block_rows(n) for n in need]
    spans = [e.get("_span") for e in entries]
    sp = [(k, h) for k, h in enumerate(spans) if h]
    if sp:
        w = cols[-1] - cols[0] - 2 * PAD
        for (k, h), n in zip(sp, m.lines([(h, w, BODY_PX, BACK_LEAD, 400) for _, h in sp])):
            need[k] = (need[k], n)
            rows[k] = rows[k] + block_rows(n)
    return need, rows


def place_back(entries, need, rows, cols, rule0):
    out, row, bounds, spans = [], 0, [0], []
    for e, n_lines, n_rows in zip(entries, need, rows):
        if isinstance(n_lines, tuple):          # main row(s), then a full-width block for the sub-items
            n_main, n_span = n_lines
            r_main = block_rows(n_main)
            out += place_back([{k: v for k, v in e.items() if k != "_span"}], [n_main], [r_main], cols,
                              rule0 + BACK_PITCH * row)[0]
            top = rule0 + BACK_PITCH * (row + r_main)
            height = BACK_PITCH * (n_rows - r_main)
            y = top + (height - n_span * BACK_LEAD) / 2 - 0.4
            out.append(div("hf wrap", cols[0] + PAD, y, cols[-1] - cols[0] - 2 * PAD, e["_span"],
                           f" font-size: {R(BODY_PX)}px; line-height: {R(BACK_LEAD)}px;", lines=n_span))
            spans.append((row + r_main, row + n_rows))
            bounds.append(row + r_main)
            row += n_rows
            bounds.append(row)
            continue
        top = rule0 + BACK_PITCH * row
        height = BACK_PITCH * n_rows
        text_h = n_lines * BACK_LEAD
        y = top + (height - text_h) / 2 - 0.4
        for c, (inner, wt, center) in ((k, v) for k, v in e.items() if k != "_span"):
            cls = "hf wrap nm" if wt == 600 else "hf wrap"
            style = f" font-size: {R(BODY_PX)}px; line-height: {R(BACK_LEAD)}px;" + (" text-align: center;" if center else "")
            out.append(div(cls, cols[c] + PAD, y, cols[c + 1] - cols[c] - 2 * PAD, inner, style, lines=n_lines))
        row += n_rows
        bounds.append(row)
    return out, row, bounds, spans


def build_reverse(h, m, out_dir):
    s = retarget((HERE / "hero-record-reverse.html").read_text(), out_dir, f"{h['name']}, Hero Record reverse")
    powers, talents, traits = parse_rules(h)

    def pcell(p):
        return {0: (esc(p["name"]), 600, False), 1: (esc(p["tier"]), 400, True), 2: ("<br>".join(esc(x.strip()) for x in p["cost"].split(",")), 400, True),
                3: (esc(p["range"]), 400, True), 4: (p["html"], 400, False)}

    def tcell(t):
        c = {0: (esc(t["name"]), 600, False), 1: (esc(t["type"]), 400, True), 2: (esc(t["cost"]), 400, True),
             3: (t["html"], 400, False)}
        if t.get("span"):
            c["_span"] = t["span"]
        return c

    p_entries = [pcell(p) for p in powers]
    t_entries = [tcell(t) for t in talents]
    p_need, p_rows = layout_back(p_entries, POW_EDGES, m) if p_entries else ([], [])
    t_need, t_rows = layout_back(t_entries, TAL_EDGES, m) if t_entries else ([], [])
    if sum(t_rows) > BACK_ROWS:
        # Talents overflow, first remedy: a Senses reminder keeps its name and drops the rulebook text.
        for k, t in enumerate(talents):
            if t.get("reminder") and sum(t_rows) > BACK_ROWS:
                t["html"] = ""
                t_entries[k] = tcell(t)
                t_need[k], t_rows[k] = 1, 1
    if sum(t_rows) > BACK_ROWS:
        # Talents overflow: move action abilities (an AP cost) into spare Powers rows, largest first.
        movable = sorted([k for k, t in enumerate(talents) if "AP" in t["cost"]], key=lambda k: -t_rows[k])
        for k in movable:
            if sum(t_rows) <= BACK_ROWS:
                break
            if sum(p_rows) + t_rows[k] <= BACK_ROWS:
                t = talents[k]
                moved = {0: (esc(t["name"]), 600, False), 1: ("—", 400, True), 2: (esc(t["cost"]), 400, True),
                         3: ("—", 400, True), 4: (t["html"], 400, False)}
                if t.get("span"):
                    moved["_span"] = t["span"]
                p_entries.append(moved)
                t_entries[k] = None
                t_rows[k] = 0
                p_need, p_rows = layout_back(p_entries, POW_EDGES, m)
        keep = [i for i, e in enumerate(t_entries) if e is not None]
        t_entries = [t_entries[i] for i in keep]
        t_need = [t_need[i] for i in keep]
        t_rows = [t_rows[i] for i in keep]
    if sum(p_rows) > BACK_ROWS or sum(t_rows) > BACK_ROWS:
        raise SystemExit(f"{h['name']}: Powers need {sum(p_rows)} rows and Talents {sum(t_rows)}; each table has {BACK_ROWS}")
    # weapon trait rules where room remains (talents table first, then powers table)
    printed_traits = []
    for t in traits:
        cell = tcell(t)
        need, rws = layout_back([cell], TAL_EDGES, m)
        if sum(t_rows) + rws[0] <= BACK_ROWS:
            t_entries.append(cell); t_need += need; t_rows += rws; printed_traits.append(t["name"])
    add = []
    for entries, need, rws, cols, rule0, marker, svg_top in (
            (p_entries, p_need, p_rows, POW_EDGES, POW_RULE, "<!-- powers -->", POW_RULE),
            (t_entries, t_need, t_rows, TAL_EDGES, TAL_RULE, "<!-- talents -->", TAL_RULE)):
        cells, used, bounds, spans = place_back(entries, need, rws, cols, rule0)
        full = {r for sp in spans for r in sp}
        add += cells
        rule_rows = [0] + bounds[1:] + list(range(used + 1, BACK_ROWS + 1))
        if marker == "<!-- talents -->":
            rule_rows = [r for r in rule_rows if r < BACK_ROWS]   # the page frame closes the last row
            svg = ledger_svg(cols[0], cols[-1], rule0, BACK_PITCH, BACK_ROWS, cols, sorted(set(rule_rows)),
                             bar_to=FRAME_IN_BOTTOM + 1, spans=spans, full_rules=full)
        else:
            svg = ledger_svg(cols[0], cols[-1], rule0, BACK_PITCH, BACK_ROWS, cols, sorted(set(rule_rows)),
                             spans=spans, full_rules=full)
        s = re.sub(re.escape(marker) + r"\n<svg[^\n]*</svg>", lambda _m: marker + "\n" + svg, s, count=1)
    block = "\n".join(["<!-- populated: " + esc(h["name"]) + " -->", *add])
    s = s.replace("\n</body>", "\n" + block + "\n</body>", 1)
    return s, printed_traits, [t["name"] for t in traits]


def card_items(h):
    """Talent entries whose sub-items print on a separate reference card."""
    out = []
    for it in section(h, "Talents, Powers, and Special Rules"):
        if it["sub"]:
            name, cost, rest = split_head(it["runs"])
            subs = []
            for sub in it["sub"]:
                sn, _c, srest = split_head(sub)
                subs.append((sn, runs_html(srest)))
            out.append((name, cost, subs))
    return out


def build_card(h, name, cost, subs, out_dir):
    """A one-third-page reference card in the sheet's grammar: frame, brushed band, ruled text."""
    rel_art = os.path.relpath(HERE / "art", out_dir)
    rel_fonts = os.path.relpath(ROOT / "fonts/static", out_dir)
    rules = [x for x in subs if x[0] == "Form Rules"]
    forms = [x for x in subs if x[0] != "Form Rules"]
    X0c, X1c, TOP = 34.61, 780.33, 37.81
    body = []
    y = TOP + 74
    for sn, sh in rules:
        body.append(div("hf wrap", X0c + 18, y, X1c - X0c - 36, f"<b>{esc(sn)}:</b> {sh}",
                        f" font-size: {R(BODY_PX)}px; line-height: 13.5px;"))
    grid = []
    for i, (sn, sh) in enumerate(forms):
        col, row = i % 2, i // 2
        gx = X0c + 18 + col * ((X1c - X0c - 36) / 2 + 9)
        grid.append((gx, row, sn, sh))
    card = f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<title>{esc(h['name'])}, {esc(name)} card</title>
<style>
@page{{size:8.5in 11in;margin:0}}
{fonts_css(rel_fonts)}
{FILL_CSS}
body{{margin:0;background:#fff}}
.cf{{position:absolute;margin:0;font-family:'Source Serif 4',serif;font-weight:700;font-size:15px;line-height:1;color:#000;white-space:nowrap}}
.cb{{position:absolute;margin:0;font-family:'Grenze Gotisch',serif;font-weight:700;line-height:1;white-space:nowrap;color:#fff}}
.cs{{position:absolute;margin:0;font-family:'Source Sans 3',sans-serif;font-weight:700;font-size:12px;line-height:1;letter-spacing:0.16em;text-transform:uppercase;color:#fff;white-space:nowrap}}
.cut{{position:absolute;border-top:1px dashed #000}}
</style>
</head>
<body>
<div id="card" style="position: relative; width: 816px; height: 1056px; overflow: hidden; background: #ffffff">
<div aria-hidden="true" style="position: absolute; left: {R(X0c)}px; top: {R(TOP)}px; width: {R(X1c-X0c)}px; height: CARD_Hpx; box-sizing: border-box; border: 2px solid #000000"></div>
<img src="{rel_art}/hr-tbandB4.svg" alt="" aria-hidden="true" style="position: absolute; left: 39.87px; top: {R(TOP+8)}px; width: 733.44px; height: 49.77px">
<h1 class="cb" style="left: 65px; top: {R(TOP+14)}px; font-size: 34px">{esc(name)}</h1>
<div class="cs" style="left: 470px; top: {R(TOP+27)}px; width: 280px; text-align: right">{esc(h['name'])} · {esc(h['class'])} · {esc(cost)}</div>
{chr(10).join(body)}
FORMS
</div>
</body>
</html>
"""
    return card, grid


def finish_card(card, grid, m):
    """Measure the Form Rules paragraph and the form blocks, then place the forms in a 2 x 2 grid."""
    X0c, X1c, TOP = 34.61, 780.33, 37.81
    full_w = X1c - X0c - 36
    col_w = full_w / 2 - 9
    rules_html = re.search(r'<div class="hf wrap"[^>]*>(.*?)</div>', card, re.S)
    y = TOP + 74
    if rules_html:
        n = m.lines([(rules_html.group(1), full_w, BODY_PX, 13.5, 400)])[0]
        y += n * 13.5 + 14
    rows = {}
    for gx, row, sn, sh in grid:
        n = m.lines([(sh, col_w, BODY_PX, 13.5, 400)])[0]
        rows[row] = max(rows.get(row, 0), n)
    parts, yy = [], y
    for r in sorted(rows):
        parts.append(f'<div class="hr-rule" style="position: absolute; height: 0; border-top: 1px solid #000; left: {R(X0c + 18)}px; top: {R(yy - 7)}px; width: {R(full_w)}px"></div>')
        for gx, row, sn, sh in grid:
            if row != r:
                continue
            parts.append(div("cf", gx, yy, None, esc(sn)))
            parts.append(div("hf wrap", gx, yy + 20, col_w, sh, f" font-size: {R(BODY_PX)}px; line-height: 13.5px;"))
        yy += 20 + rows[r] * 13.5 + 14
    if len(rows) and grid:
        x_mid = X0c + 18 + full_w / 2
        parts.append(f'<div aria-hidden="true" style="position: absolute; left: {R(x_mid - 1.25)}px; top: {R(y - 7)}px; width: 2.5px; height: {R(yy - y - 7)}px; background: #000"></div>')
    h_card = yy - TOP + 6
    return card.replace("FORMS", "\n".join(parts)).replace("CARD_H", R(h_card)), h_card


def page_text(*files):
    """Visible text of generated pages, one string per element, entities decoded."""
    out = []
    for f in files:
        t = f.read_text()
        t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
        t = re.sub(r"<br>", " ", t)
        out += [html.unescape(re.sub(r"<[^>]+>", "", seg)) for seg in re.findall(r"<(?:div|h1|h2)[^>]*>(.*?)</(?:div|h1|h2)>", t, re.S)]
    return out


def fidelity(h, files, printed_traits):
    """Every word of the Hero's own rules and items must appear verbatim somewhere on its pages."""
    texts = page_text(*files)
    blob = "\n".join(re.sub(r"\s+", " ", x) for x in texts)
    missing = []

    def need(label, text):
        t = re.sub(r"\s+", " ", text).strip()
        if t and t not in blob:
            missing.append(f"{label}: {t[:60]}")

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
    for it in section(h, "Weapon Trait Rules"):
        name, cost, rest = split_head(it["runs"])
        if name in printed_traits:
            need("trait " + name, flat(rest))
    return missing


def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


def ensure_mask():
    """Interior of the portrait shield as a mask (opaque inside the inner rule)."""
    out = HERE / "art/hr-shield5-mask.png"
    if out.exists():
        return
    from PIL import Image, ImageDraw, ImageFilter
    from playwright.sync_api import sync_playwright
    scale = 4
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": int(SHIELD[2] * scale), "height": int(SHIELD[3] * scale)})
        import base64
        svg = base64.b64encode((HERE / "art/hr-shield5.svg").read_bytes()).decode()
        pg.set_content(f'<body style="margin:0;background:#fff"><img src="data:image/svg+xml;base64,{svg}" '
                       f'style="width:{SHIELD[2]*scale}px;height:{SHIELD[3]*scale}px;display:block"></body>')
        pg.wait_for_timeout(300)
        png = pg.screenshot()
        b.close()
    import io
    im = Image.open(io.BytesIO(png)).convert("L").point(lambda v: 255 if v > 128 else 0)
    w, hgt = im.size
    if im.getextrema() == (255, 255):
        raise SystemExit("shield outline did not render; cannot build the portrait mask")
    ImageDraw.floodfill(im, (w // 2, hgt // 2), 128)
    mask = im.point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.MinFilter(9))   # keep ink 1 px clear of the rule
    a = Image.new("LA", im.size, 0)
    a.putalpha(mask)
    a.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "build/hero-records")
    ap.add_argument("--only")
    ap.add_argument("--pdf", type=pathlib.Path)
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    ensure_mask()
    from playwright.sync_api import sync_playwright
    heroes = [h for h in DATA["heroes"] if not args.only or h["name"].lower() == args.only.lower()]
    report = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        mp = b.new_page()
        m = Measurer(mp, fonts_css((ROOT / "fonts/static").as_uri()), out_dir)
        pages, cards = [], []
        for h in heroes:
            front = build_front(h, m, out_dir)
            rev, printed, all_traits = build_reverse(h, m, out_dir)
            sl = slug(h["name"])
            (out_dir / f"{sl}-front.html").write_text(front)
            (out_dir / f"{sl}-reverse.html").write_text(rev)
            pages += [out_dir / f"{sl}-front.html", out_dir / f"{sl}-reverse.html"]
            for cname, ccost, subs in card_items(h):
                card, grid = build_card(h, cname, ccost, subs, out_dir)
                card, ch = finish_card(card, grid, m)
                cf = out_dir / f"{sl}-{slug(cname)}-card.html"
                cf.write_text(card)
                cards.append(cf)
                print(f"{h['name']:12} {cname} card {ch:.0f} px tall", file=sys.stderr)
            files = [out_dir / f"{sl}-front.html", out_dir / f"{sl}-reverse.html"] + \
                [out_dir / f"{sl}-{slug(c[0])}-card.html" for c in card_items(h)]
            miss = fidelity(h, files, printed)
            if miss:
                raise SystemExit(f"{h['name']}: text missing from the sheet:\n  " + "\n  ".join(miss))
            omitted = [t for t in all_traits if t not in printed]
            report.append({"hero": h["name"], "weapon_trait_rules_printed": printed, "weapon_trait_rules_by_name_only": omitted})
            print(f"{h['name']:12} traits printed {len(printed)}/{len(all_traits)}", file=sys.stderr)
        pdfs, problems = [], {}
        for f in pages + cards:   # cards follow every sheet so duplex front/back pairs stay aligned
            pg = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2550 / 816)
            pg.goto(f.as_uri())
            pg.wait_for_timeout(250)
            pg.evaluate("document.fonts.ready")
            bad = pg.evaluate("""() => [...document.querySelectorAll('.hf, .hv, .hid, .hname')].flatMap(d => {
                const cs = getComputedStyle(d), lead = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize);
                const out = [];
                if (d.dataset.lines) {
                    const n = Math.round(d.getBoundingClientRect().height / lead);
                    if (n > +d.dataset.lines) out.push(`${n} lines > ${d.dataset.lines}: ${d.textContent.slice(0, 50)}`);
                }
                if (cs.whiteSpace === 'nowrap' && d.style.width && d.scrollWidth > d.clientWidth + 0.5)
                    out.push(`too wide (${d.scrollWidth} > ${d.clientWidth}): ${d.textContent.slice(0, 50)}`);
                if (parseFloat(cs.fontSize) < 12) out.push(`below 9 pt: ${d.textContent.slice(0, 40)}`);
                return out; })""")
            if bad:
                problems[f.name] = bad
            if not args.no_png:
                pg.screenshot(path=str(f.with_suffix(".png")))
            if args.pdf:
                out = f.with_suffix(".pdf")
                pg.pdf(path=str(out), width="8.5in", height="11in", print_background=True, page_ranges="1")
                pdfs.append(out)
            pg.close()
        b.close()
    (out_dir / "report.json").write_text(json.dumps({"heroes": report, "fit_problems": problems}, indent=1) + "\n")
    (out_dir / "_measure.html").unlink(missing_ok=True)
    if problems:
        for k, v in problems.items():
            print(k, *v, sep="\n  ", file=sys.stderr)
        raise SystemExit(f"{len(problems)} page(s) have text that does not fit")
    if args.pdf:
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter()
        for f in pdfs:
            w.add_page(PdfReader(str(f)).pages[0])
        w.write(str(args.pdf))
        for f in pdfs:
            f.unlink()


if __name__ == "__main__":
    main()
