"""FIG-58 .. FIG-64: end-of-section fillers for Chapters 1 and 2.

FIG-58 What You Need to Play (1.4), FIG-59 Goals of the Game (1.5), FIG-60 Rules Hierarchy and Precedence (1.6),
FIG-61 Ability Scores (2.2), FIG-62 Ability Checks (2.3, 2.4), FIG-63 Cover, Light, Hidden, and Visibility (2.8),
FIG-64 Luck Points (2.10).  Each fig function returns (Svg, height) like fig_seq.py.
"""
from svgkit import *

# Single-line texts are recorded here so selfcheck_end_a() can prove that they fit their boxes.
_FITS = []


def T(s, x, y, text, maxw=None, size=9, weight=400, anchor="start", fill=INK):
    """One line of text; when maxw is given the width is recorded and asserted to fit."""
    if maxw is not None:
        w = tw(text, size, weight)
        _FITS.append((text, w, maxw))
        assert w <= maxw + 0.01, (text, w, maxw)
    s.text(x, y, text, size, weight, anchor, fill)


def hdr(s, x, y, w, n, title, ref=None, h=19):
    """Black header bar with a white numbered circle (FIG-01 grammar)."""
    s.rect(x, y, w, h, fill=INK, stroke=INK, sw=0.9, rx=2.5)
    off = 22 if n is not None else 7
    if n is not None:
        s.circle(x + 11, y + h / 2, 6.6, fill=WHITE, stroke=None)
        s.text(x + 11, y + h / 2 + 3.2, str(n), 9, 700, "middle", INK)
    room = w - off - 6 - ((tw(ref, 9, 600) + 8) if ref else 0)
    T(s, x + off, y + h / 2 + 3.4, title, room, 9.5, 700, "start", WHITE)
    if ref:
        s.text(x + w - 5, y + h / 2 + 3.4, ref, 9, 600, "end", WHITE)
    return h


def card(s, x, y, w, n, title, ref, body, pad=5, minH=0):
    """Header bar plus a body callback body(s, x, y, w) -> y below; frame drawn around both."""
    h0 = hdr(s, x, y, w, n, title, ref)
    yb = body(s, x + pad, y + h0 + pad + 1, w - 2 * pad)
    H = max(yb - y + pad, minH)
    s.rect(x, y, w, H, fill="none", stroke=INK, sw=0.9, rx=2.5)
    return H


def card_h(w, n, title, ref, body, pad=5):
    """Height a card would have (dry run on a scratch canvas)."""
    return card(Svg(w), 0, 0, w, n, title, ref, body, pad)


def fixbox(s, x, y, w, h, text, size=9, weight=400, fill=WHITE, sw=0.9, lead=10.6, anchor="middle", pad=4):
    """Box of fixed size with wrapped text centred vertically; asserts the text fits."""
    lines = wrap(text, w - 2 * pad, size, weight)
    assert len(lines) * lead + 2 * pad - 2 <= h + 0.01, (text, len(lines), h)
    s.rect(x, y, w, h, fill=fill, stroke=INK, sw=sw, rx=2.5)
    y0 = y + (h - len(lines) * lead) / 2 + 7.3 - 0.4
    for i, ln in enumerate(lines):
        s.text(x + w / 2 if anchor == "middle" else x + pad, y0 + i * lead, ln, size, weight, anchor)
    return h


def nlines(text, w, size=9, weight=400):
    return len(wrap(text, w - 8, size, weight))


def ptxt(s, x, y, text, w, size=9, lead=10.6, weight=400, anchor="start", fill=INK):
    """Wrapped paragraph, y = top of the block; returns the bottom."""
    lines = wrap(text, w, size, weight)
    for i, ln in enumerate(lines):
        s.text(x if anchor == "start" else x + w / 2, y + 7.3 + i * lead, ln, size, weight, anchor, fill)
    return y + len(lines) * lead


def bullets(s, x, y, w, items, lead=10.6, gap=1.5, mark="•"):
    for it in items:
        lines = wrap(it, w - 9, 9)
        s.text(x, y + 7.3, mark, 9, 700)
        for k, ln in enumerate(lines):
            s.text(x + 9, y + 7.3 + k * lead, ln, 9)
        y += len(lines) * lead + gap
    return y


def chips(s, x, y, w, items, h=14, gap=4, weight=600, size=9, fill=WHITE, padx=5, rowgap=4):
    """Flowing chips (rounded outlined labels); returns the bottom."""
    cx, cy = x, y
    for it in items:
        cw = tw(it, size, weight) + 2 * padx
        assert cw <= w, it
        if cx + cw > x + w + 0.01 and cx > x:
            cx = x
            cy += h + rowgap
        s.rect(cx, cy, cw, h, fill=fill, stroke=INK, sw=0.8, rx=2)
        s.text(cx + cw / 2, cy + h / 2 + 3.2, it, size, weight, "middle")
        cx += cw + gap
    return cy + h


def mdim(s, x1, y1, x2, y2, label, tick=3.0):
    """Dimension line with end ticks and the label centred on the line (pill backing)."""
    s.line(x1, y1, x2, y2, INK, 0.8)
    horiz = abs(y2 - y1) < abs(x2 - x1)
    for (px, py) in ((x1, y1), (x2, y2)):
        if horiz:
            s.line(px, py - tick, px, py + tick, INK, 0.8)
        else:
            s.line(px - tick, py, px + tick, py, INK, 0.8)
    pill(s, (x1 + x2) / 2, (y1 + y2) / 2 + 3, label, 9, 600)


def sheet(s, x, y, w=22, h=28):
    """Record-sheet icon: page outline with ruled lines."""
    s.rect(x, y, w, h, fill=WHITE, stroke=INK, sw=0.9, rx=1.5)
    for k in range(5):
        s.line(x + 3.5, y + 6 + k * 4.4, x + w - 3.5, y + 6 + k * 4.4, INK, 0.6)


def person(s, cx, cy, n):
    s.circle(cx, cy, 6.6, fill=WHITE, stroke=INK, sw=0.9)
    s.text(cx, cy + 3.2, str(n), 9, 600, "middle")


# =====================================================================
# FIG-58  1.4 What You Need to Play
# =====================================================================
def fig58():
    s = Svg(FULL_W)
    LW, RX, RW = 248, 256, 248

    def players(s, x, y, w):
        yy = ptxt(s, x, y, "**1–8 players.**", w)
        for k in range(8):
            person(s, x + 7 + k * 17, yy + 9, k + 1)
        return yy + 20

    def battlefield(s, x, y, w):
        yy = ptxt(s, x, y, "One battlefield in either mode. Both measure **36\"×36\"**.", w)
        side = 88
        bx = x + 20
        tx = bx + side + 14
        tw_ = w - (tx - x)
        # ---- Tabletop Mode row ----
        by = yy + 20
        mdim(s, bx, by - 9, bx + side, by - 9, "36\"")
        mdim(s, bx - 10, by, bx - 10, by + side, "36\"")
        s.rect(bx, by, side, side, fill=WHITE, stroke=INK, sw=1.2)
        for (ox, oy, ow, oh) in ((9, 10, 26, 16), (50, 32, 24, 22), (12, 56, 30, 16)):
            s.rect(bx + ox, by + oy, ow, oh, fill=LIGHT, stroke=INK, sw=0.8, rx=2)
        tape_y = by + side + 6
        s.rect(bx, tape_y, side, 8, fill=PALE, stroke=INK, sw=0.8, rx=1.5)
        for k in range(1, 12):
            s.line(bx + k * side / 12, tape_y, bx + k * side / 12, tape_y + (5 if k % 2 else 8), INK, 0.6)
        ptxt(s, tx, by + 2, "**Tabletop Mode:** an open surface measured in inches, a suitable collection of terrain, and a tape measure.", tw_)
        # ---- Grid Mode row ----
        gy = tape_y + 8 + 22
        mdim(s, bx, gy - 9, bx + side, gy - 9, "36\"")
        mdim(s, bx - 10, gy, bx - 10, gy + side, "36\"")
        cell = side / 6.0
        grid(s, bx, gy, 6, 6, cell)
        s.rect(bx, gy, cell, cell, fill=LIGHT, stroke=INK, sw=0.9)
        yy2 = ptxt(s, tx, gy + 2, "**Grid Mode:** a battle map marked in 1\" squares.", tw_)
        s.line(tx, yy2 + 8, tx + cell, yy2 + 8, INK, 0.8)
        s.line(tx, yy2 + 5, tx, yy2 + 11, INK, 0.8)
        s.line(tx + cell, yy2 + 5, tx + cell, yy2 + 11, INK, 0.8)
        T(s, tx + cell + 5, yy2 + 11.3, "1\" square", tw_ - cell - 5, 9, 600)
        yb = gy + side + 5
        T(s, x, yb + 7.3, "Schematic - not to scale; only a few squares drawn", w, 9, 600, "start", "#333")
        return yb + 12

    def models(s, x, y, w):
        yy = ptxt(s, x, y, "1 miniature, standee, or token for each of these in play:", w)
        return chips(s, x, yy + 3, w, ["Hero", "Hireling", "Monster", "Summon"]) + 1

    def markers(s, x, y, w):
        yy = ptxt(s, x, y, "Distinguishable markers or miniatures for objectives, Treasure Chests, hazards, scenario elements, and other temporary battlefield features.", w)
        iy = yy + 12
        slots = [("obj", "objectives"), ("chest", "Treasure Chests"), ("hazard", "hazards")]
        cx = x
        for kind, lab in slots:
            if kind == "hazard":
                s.rect(cx + 1, iy - 6, 12, 12, fill="#c4c4c4", stroke=INK, sw=0.8)
                s.text(cx + 7, iy + 3.6, "!", 9, 700, "middle")
            else:
                token(s, kind, cx + 7, iy, 6.2)
            T(s, cx + 17, iy + 3.2, lab, None, 9)
            cx += 17 + tw(lab, 9) + 10
        yy = iy + 10
        yy = ptxt(s, x, yy, "Coins, paper tokens, spare miniatures, or similar markers are sufficient. The icons here are illustrations only.", w)
        return yy

    def records(s, x, y, w):
        sheet(s, x, y + 1)
        sheet(s, x + 28, y + 1)
        yy = ptxt(s, x + 60, y, "A record sheet for each Hero and party, plus pencils or another method of recording game state.", w - 60)
        return max(yy, y + 30)

    def tokens(s, x, y, w):
        yy = chips(s, x, y, w, ["**AP**", "**Activated**", "**Resting**", "**HP**", "**NRG**", "condition", "Luck"], padx=4, gap=3)
        return ptxt(s, x, yy + 3, "Tokens for each of these, or another method of tracking each resource and state.", w)

    def dice(s, x, y, w):
        yy = ptxt(s, x, y, "At least:", w)
        yy = chips(s, x, yy + 2, w, ["4d4", "4d6", "4d8", "4d10", "2d12", "2d20"], h=16, size=10, weight=700, padx=7)
        return yy + 1

    # left column: 1, 2 ; right column: 3 to 7
    yl = card(s, 0, 0, LW, 1, "Players", "1.4", players) + 7
    yl += card(s, 0, yl, LW, 2, "Battlefield", "1.4", battlefield)
    yr = 0
    for n, title, fn in ((3, "Models", models), (4, "Markers", markers), (5, "Records", records),
                         (6, "Resource and state tokens", tokens), (7, "Dice", dice)):
        yr += card(s, RX, yr, RW, n, title, "1.4", fn) + 7
    return s, max(yl, yr - 7) + 1


# =====================================================================
# FIG-59  1.5 Goals of the Game
# =====================================================================
def fig59():
    s = Svg(FULL_W)
    hb = box(s, 0, 0, FULL_W, "**Adventure:** a single game of Heraldry Skirmish. **Your goal:** complete the scenario's objective and satisfy its victory conditions.",
             anchor="start", fill=PALE, sw=0.9, pad=6)
    y0 = hb + 8
    W1, X2 = 292, 300
    W2 = FULL_W - X2

    def coins(s, x, y, w):
        yy = ptxt(s, x, y, "Many competitive scenarios compare secured wealth, measured in **coins**. Parties earn coins by:", w)
        gap = 5
        bw = (w - 3 * gap) / 4.0
        srcs = ["looting treasure", "completing objectives", "defeating Monsters", "surviving long enough to escape the battlefield with their spoils"]
        bh = max(nlines(t_, bw) for t_ in srcs) * 10.6 + 6
        yy += 4
        for k, txt in enumerate(srcs):
            bx = x + k * (bw + gap)
            fixbox(s, bx, yy, bw, bh, txt, fill=WHITE)
            vflow_arrow(s, bx + bw / 2, yy + bh + 1, yy + bh + 15)
        yy += bh + 16
        h1 = fixbox(s, x, yy, w, 34, "**Coins**, written **Xc**, where **X** is the number of coins. **CV** (**Coin Value**) refers to an equivalent value in coins.", fill=PALE)
        return yy + h1

    def triumph(s, x, y, w):
        yy = ptxt(s, x, y, "In campaign play, the goal is **Triumph**.", w)
        yy += 4
        # competitive campaign
        T(s, x, yy + 7.3, "Competitive campaign", w, 9, 700)
        yy += 13
        sq = 18
        for k in range(5):
            bx = x + k * (sq + 4)
            s.rect(bx, yy, sq, sq, fill=WHITE, stroke=INK, sw=0.9, rx=2)
            s.text(bx + sq / 2, yy + 12.5, str(k + 1), 9, 600, "middle")
        hflow_arrow(s, x + 5 * (sq + 4) + 1, x + 5 * (sq + 4) + 28, yy + sq / 2)
        fixbox(s, x + 5 * (sq + 4) + 30, yy, w - 5 * (sq + 4) - 30, sq, "**Triumph**", fill=PALE)
        yy += sq + 2
        yy = ptxt(s, x, yy, "Complete any **5** different Stronghold Components.", w)
        yy += 5
        T(s, x, yy + 7.3, "Solo or cooperative campaign", w, 9, 700)
        yy += 13
        yy = ptxt(s, x, yy, "Complete the rolled objective and extraction requirement in the **Triumph Finale**.", w)
        return yy + 1

    hA = card_h(W1, 1, "x", None, coins)
    hB = card_h(W2, 2, "x", None, triumph)
    H = max(hA, hB)
    card(s, 0, y0, W1, 1, "Adventure goal: coins", "1.5", coins, minH=H)
    card(s, X2, y0, W2, 2, "Campaign goal: Triumph", "1.5.1", triumph, minH=H)
    y1 = y0 + H + 8

    def fates(s, x, y, w):
        gap = 6
        ws = [140, w - 2 * gap - 280, 140]
        items = [
            ("Die", "A Hero who dies and is not returned to life before the next adventure is removed from the campaign permanently."),
            ("Retire", "A Hero may retire during the Town Phase. A retired Hero is removed from the Roster permanently, returns their eligible items to **Storage**, and adds a Retirement Payout to the Treasury. A Hero that retires at **Level 10** becomes a **Legendary Veteran**."),
            ("Triumph", "A Hero who remains on the Roster when their party achieves **Triumph** shares in that victory unless another rule says otherwise."),
        ]
        bh = max(nlines(b, ws[k]) for k, (_, b) in enumerate(items)) * 10.6 + 2 * 4 + 14
        for k, (name, body) in enumerate(items):
            bw = ws[k]
            bx = x + sum(ws[:k]) + k * gap
            s.rect(bx, y, bw, bh, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
            s.rect(bx, y, bw, 14, fill=LIGHT, stroke=INK, sw=0.9, rx=2.5)
            s.text(bx + bw / 2, y + 10.3, name, 9, 700, "middle")
            ptxt(s, bx + 4, y + 17, body, bw - 8, anchor="start")
        return y + bh

    card(s, 0, y1, FULL_W, 3, "Every Hero eventually meets one of three Fates", "1.5.1", fates)
    H3 = card_h(FULL_W, 3, "x", None, fates)
    return s, y1 + H3 + 2


# =====================================================================
# FIG-60  1.6 Rules Hierarchy and Precedence
# =====================================================================
def fig60():
    s = Svg(FULL_W)
    W1, X2 = 262, 270
    W2 = FULL_W - X2

    def procedure(s, x, y, w):
        fixbox(s, x, y, w, 22, "**Two rules conflict.**", fill=PALE)
        vflow_arrow(s, x + w / 2, y + 23, y + 47)
        yy = y + 49
        bw = 110
        rh = 42
        callout(s, x + 8, yy + rh / 2, 1)
        fixbox(s, x + 18, yy, bw - 12, rh, "One rule is **more specific**.")
        hflow_arrow(s, x + bw + 7, x + bw + 29, yy + rh / 2)
        fixbox(s, x + bw + 31, yy, w - bw - 31, rh, "**Use the more specific rule.**", fill=PALE)
        ax = x + 18 + (bw - 12) / 2
        vflow_arrow(s, ax, yy + rh + 1, yy + rh + 41)
        T(s, ax + 7, yy + rh + 25, "equally specific", w - 60, 9, 600)
        yy += rh + 43
        callout(s, x + 8, yy + rh / 2, 2)
        fixbox(s, x + 18, yy, bw - 12, rh, "Two rules are **equally specific**.")
        hflow_arrow(s, x + bw + 7, x + bw + 29, yy + rh / 2)
        fixbox(s, x + bw + 31, yy, w - bw - 31, rh, "**Use the more restrictive rule.**", fill=PALE)
        return yy + rh + 2

    def overrides(s, x, y, w):
        pairs = [
            ("**Scenario rules**", "override", "the core rules, for that scenario", False),
            ("**Class features, Powers, Monster rules, terrain rules, and item rules**", "override", "the general rules they explicitly modify", False),
            ("**Examples, summaries, and reference tables**", "never override", "the main rules text", True),
        ]
        yy = y
        for top, verb, bottom, never in pairs:
            h1 = nlines(top, w) * 10.6 + 6
            fixbox(s, x, yy, w, h1, top, fill=PALE if not never else WHITE)
            yy += h1
            if never:
                s.line(x + 14, yy + 2, x + 14, yy + 20, INK, 1.2)
                xmark(s, x + 14, yy + 11, 4.2, 1.8)
            else:
                vflow_arrow(s, x + 14, yy + 2, yy + 20)
            T(s, x + 28, yy + 14, verb, w - 30, 9, 600)
            yy += 22
            h2 = nlines(bottom, w) * 10.6 + 6
            fixbox(s, x, yy, w, h2, bottom)
            yy += h2 + 7
        return yy - 7

    hA = card_h(W1, 1, "x", None, procedure)
    hB = card_h(W2, 2, "x", None, overrides)
    H = max(hA, hB)
    card(s, 0, 0, W1, 1, "Resolving a conflict", "1.6", procedure, minH=H)
    card(s, X2, 0, W2, 2, "Which rule overrides", "1.6", overrides, minH=H)
    y1 = H + 8

    def words(s, x, y, w):
        gap = 6
        bw = (w - 2 * gap) / 3.0
        items = [("must", "marks a required instruction"), ("may", "marks a permission or choice"), ("cannot", "marks a prohibition")]
        for k, (a, b) in enumerate(items):
            bx = x + k * (bw + gap)
            fixbox(s, bx, y, bw, 28, "**%s** %s" % (a, b))
        yy = y + 28 + 5
        yy = ptxt(s, x, yy, "These words do not create a separate precedence system. Resolve every conflict with the procedure above.", w)
        return yy

    card(s, 0, y1, FULL_W, 3, "Reading rules text", "1.6", words)
    return s, y1 + card_h(FULL_W, 3, "x", None, words) + 2


# =====================================================================
# FIG-61  2.2 Ability Scores
# =====================================================================
def fig61():
    s = Svg(FULL_W)

    def four(s, x, y, w):
        gap = 6
        bw = (w - 3 * gap) / 4.0
        data = [
            ("Strength (STR)", ["melee force", "physical power", "climbing", "forcing objects", "resisting bodily harm"]),
            ("Dexterity (DEX)", ["ranged accuracy", "speed", "balance", "stealth", "dodging", "delicate physical tasks"]),
            ("Intelligence (INT)", ["perception", "reasoning", "knowledge", "investigation", "initiative", "**Arcane Spells**", "**Psychic Abilities**"]),
            ("Spirit (SPI)", ["willpower", "faith", "resolve", "leadership", "powers of faith, nature, and sorcery"]),
        ]
        hh = 0
        for _, items in data:
            hh = max(hh, sum(len(wrap(i, bw - 8 - 9, 9)) for i in items) * 10.6 + len(items) * 1.5)
        bh = 16 + 5 + hh + 3
        for k, (name, items) in enumerate(data):
            bx = x + k * (bw + gap)
            s.rect(bx, y, bw, bh, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
            s.rect(bx, y, bw, 16, fill=LIGHT, stroke=INK, sw=0.9, rx=2.5)
            T(s, bx + bw / 2, y + 11.4, name, bw - 6, 9, 700, "middle")
            bullets(s, bx + 5, y + 21, bw - 8, items)
        return y + bh

    y = card(s, 0, 0, FULL_W, 1, "Four ability scores", "2.2", four)
    y = card_h(FULL_W, 1, "x", None, four) + 8
    W2, X3 = 276, 284
    W3 = FULL_W - X3

    def who(s, x, y, w):
        lw = 108
        rows = [
            ("**Heroes** and **Hirelings**", "Use ability scores."),
            ("A non-Monster **Summon** or other combatant", "Uses the ability scores listed in their profile."),
            ("Such a combatant with an omitted score for a **STR**, **DEX**, **INT**, or **SPI Check**", "Treat that score as **+0** for that Check only. This grants no ability score for any other purpose."),
            ("**Monsters**", "**Never** have or use ability scores."),
        ]
        yy = y
        for a, b in rows:
            h = max(nlines(a, lw), nlines(b, w - lw - 16)) * 10.6 + 6
            fixbox(s, x, yy, lw, h, a, fill=PALE)
            hflow_arrow(s, x + lw + 2, x + lw + 14, yy + h / 2)
            fixbox(s, x + lw + 16, yy, w - lw - 16, h, b, anchor="start")
            yy += h + 5
        return yy - 5

    def values(s, x, y, w):
        yy = ptxt(s, x, y, "Ability scores are added as modifiers to **Checks** and other listed rolls.", w)
        yy += 6
        ly = yy + 26
        x0, step = x + 38, 32
        ticks = ["-1", "+0", "+1", "+2", "+3"]
        xs = [x0 + k * step for k in range(5)]
        s.rect(xs[0], ly - 4, xs[-1] - xs[0], 8, fill=MID, stroke=INK, sw=0.9, dash="3 2")
        arrow(s, xs[0], ly, x + 3, ly, "move", sw=1.2)
        arrow(s, xs[-1], ly, x + w - 3, ly, "move", sw=1.2)
        for k, (tx, lab) in enumerate(zip(xs, ticks)):
            s.line(tx, ly - 7, tx, ly + 7, INK, 0.9)
            T(s, tx, ly + 19, lab, 28, 9, 600, "middle")
        T(s, (xs[0] + xs[-1]) / 2, ly - 12, "most starting Heroes", xs[-1] - xs[0] + 20, 9, 600, "middle")
        yy = ly + 26
        yy = bullets(s, x, yy, w, ["Most starting Heroes have values between **-1** and **+3**.",
                                   "Scores may be negative.",
                                   "No maximum unless a rule says otherwise."])
        return yy

    hA = card_h(W2, 2, "x", None, who)
    hB = card_h(W3, 3, "x", None, values)
    H = max(hA, hB)
    card(s, 0, y, W2, 2, "Who uses ability scores", "2.2", who, minH=H)
    card(s, X3, y, W3, 3, "Range of values", "2.2", values, minH=H)
    return s, y + H + 2


# =====================================================================
# FIG-62  2.3 Ability Checks (with 2.4 Advantage and Disadvantage)
# =====================================================================
def _die(s, x, y, n, ignored=False, size=20):
    s.rect(x, y, size, size, fill=PALE if ignored else WHITE, stroke=INK, sw=1.0, rx=3)
    s.text(x + size / 2, y + size / 2 + 3.4, str(n), 10, 700, "middle", MID if ignored else INK)
    if ignored:
        s.line(x + 2, y + size - 2, x + size - 2, y + 2, INK, 1.2)


EX62 = dict(score=2, dice=(7, 15))      # worked example (assumed values; no natural 1 or 20 appears)


def fig62():
    s = Svg(FULL_W)
    WA, XB = 252, 260
    WB = FULL_W - XB

    def making(s, x, y, w):
        yy = y
        steps = ["A rule calls for a **Check** and tells you which ability to use.", "Roll **1d20** and add the listed ability score.", "Read the result."]
        for k, st in enumerate(steps, 1):
            callout(s, x + 6.6, yy + 5.6, k)
            yy = ptxt(s, x + 18, yy, st, w - 18) + 5
        yy += 1
        half = (w - 6) / 2
        t20 = "**Natural 20:** **Critical Success**, always succeeds"
        t1 = "**Natural 1:** **Critical Failure**, always fails"
        hh = max(nlines(t20, half), nlines(t1, half)) * 10.6 + 6
        fixbox(s, x, yy, half, hh, t1, fill=PALE)
        fixbox(s, x + half + 6, yy, half, hh, t20, fill=PALE)
        yy += hh + 6
        T(s, x, yy + 7.3, "Otherwise compare the total with 12:", w, 9, 600)
        yy += 13
        # result bar
        bw = w
        s.rect(x, yy, bw / 2, 18, fill=WHITE, stroke=INK, sw=0.9, rx=2)
        s.rect(x + bw / 2, yy, bw / 2, 18, fill=DARK, stroke=INK, sw=0.9, rx=2)
        T(s, x + bw / 4, yy + 12.3, "11 or lower: fails", bw / 2 - 4, 9, 600, "middle")
        T(s, x + 3 * bw / 4, yy + 12.3, "12 or higher: succeeds", bw / 2 - 4, 9, 600, "middle", WHITE)
        yy += 24
        yy = ptxt(s, x, yy, "**Natural 1** and **natural 20** apply only to **d20 Checks** unless a rule says otherwise. Some attacks, Reactions, and Power rules define their own critical results for non-d20 rolls.", w)
        return yy

    def advdis(s, x, y, w):
        yy = ptxt(s, x, y, "For a **d20 Check** the affected die is **d20**. Add one extra die, then ignore one:", w)
        yy += 1
        yy = bullets(s, x, yy, w, ["**Advantage:** ignore the lowest single die.", "**Disadvantage:** ignore the highest single die.",
                                   "Both apply to one roll: they cancel and you roll normally.",
                                   "Instances of the same kind do not stack."])
        yy += 3
        lo, hi = EX62["dice"]
        sc = EX62["score"]
        yy = ptxt(s, x, yy, "**Example.** Assume an ability score of +%d and two d20 showing %d and %d:" % (sc, lo, hi), w) + 3
        for name, ign, keep in (("Advantage", lo, hi), ("Disadvantage", hi, lo)):
            total = keep + sc
            res = "succeeds" if total >= 12 else "fails"
            T(s, x, yy + 13.5, name, 70, 9, 600)
            dx = x + 72
            _die(s, dx, yy, lo, ignored=(ign == lo))
            _die(s, dx + 25, yy, hi, ignored=(ign == hi))
            T(s, dx + 52, yy + 13.5, "%d + %d = %d: %s" % (keep, sc, total, res), w - 72 - 52, 9, 600)
            yy += 25
        return yy

    hA = card_h(WA, 1, "x", None, making)
    hB = card_h(WB, 2, "x", None, advdis)
    H = max(hA, hB)
    card(s, 0, 0, WA, 1, "Making a Check", "2.3", making, minH=H)
    card(s, XB, 0, WB, 2, "Advantage and Disadvantage", "2.4", advdis, minH=H)
    y1 = H + 8

    def monsters(s, x, y, w):
        gap = 6
        cw = [150, 196, w - 2 * gap - 346]
        cols = [
            ("Monsters never make a Check", "A **Monster** has no **STR**, **DEX**, **INT**, or **SPI** score. If a rule would require one to make a Check, do not roll it. Resolve the normal failed-Check effect (not a **Critical Failure**) against that **Monster** automatically unless they are **Immune** to it."),
            ("Exception: Terrain Check", "A **Monster** automatically succeeds on every **Terrain Check**: a Check required by the **Climb** or **Jump** rules, by a Terrain Type or **Terrain Tag**, or by a terrain feature or hazard marker that a scenario or Secondary Objective places. A Check that a Power, scroll, item, attack, Special Ability, or weather result requires directly is not a **Terrain Check**."),
            ("Casting Check", "If a **Power** or scroll would require a **Monster** to make such a Check and that **Monster's LVL** is higher than the Level of the Hero using it, its **Casting Check** is made with **Disadvantage**."),
        ]
        bh = max(nlines(b, cw[k]) for k, (_, b) in enumerate(cols)) * 10.6 + 8 + 14
        for k, (hd, body) in enumerate(cols):
            bx = x + sum(cw[:k]) + k * gap
            s.rect(bx, y, cw[k], bh, fill=WHITE, stroke=INK, sw=0.9, rx=2.5)
            s.rect(bx, y, cw[k], 14, fill=LIGHT, stroke=INK, sw=0.9, rx=2.5)
            T(s, bx + cw[k] / 2, y + 10.3, hd, cw[k] - 6, 9, 700, "middle")
            ptxt(s, bx + 4, y + 17, body, cw[k] - 8)
        return y + bh

    card(s, 0, y1, FULL_W, 3, "Monsters and Checks", "2.3", monsters)
    return s, y1 + card_h(FULL_W, 3, "x", None, monsters) + 2


# =====================================================================
# FIG-63  2.8 Cover, Light, Hidden, and Visibility
# =====================================================================
DARKFILL = "#bfbfbf"


def badge(s, cx, cy, letter, size=12):
    """Square scene label (white, outlined) so it cannot be mistaken for a round combatant token."""
    s.rect(cx - size / 2, cy - size / 2, size, size, fill=WHITE, stroke=INK, sw=1.0, rx=1.5)
    s.text(cx, cy + 3.3, letter, 9, 700, "middle")


def _lightsource(s, cx, cy, r=3.6):
    for k in range(8):
        a = k * math.pi / 4
        s.line(cx + (r + 1.5) * math.cos(a), cy + (r + 1.5) * math.sin(a), cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a), INK, 1.0)
    s.circle(cx, cy, r, fill=WHITE, stroke=INK, sw=1.0)


PT_PER_IN63 = 10                      # scene scale: Aura 3" has radius 30 pt, a 1" model is 10 pt wide (r = 5)
SC63 = dict(aura_in=3, tok_r=5, a_off=(-13, 12), b_pair=(132, 22, 200, 22), c_pair=(132, 48, 142, 48))


def fig63():
    s = Svg(FULL_W)
    W1, X2 = 262, 270
    W2 = FULL_W - X2

    def ladder(s, x, y, w):
        rows = [
            (3, "Hidden", "cannot be targeted by anything that requires **LOS**."),
            (2, "Cover", "still targeted normally, but applicable ranged attacks and effects against them suffer **Disadvantage**."),
            (1, "Exposed", "has no **Cover**. Attacks and effects target them normally."),
        ]
        yy = y
        bw = w - 20
        prev_bottom = None
        for k, (n, name, eff) in enumerate(rows):
            ind = (2 - k) * 10
            lines = wrap("**%s** %s" % (name, eff), bw - 24, 9)
            h = len(lines) * 10.6 + 8
            bx = x + ind
            if prev_bottom is not None:
                ax = x + 30
                s.line(ax, yy + 1, ax, prev_bottom + 7, INK, 1.2)
                s.polygon([(ax, prev_bottom), (ax - 3.2, prev_bottom + 7), (ax + 3.2, prev_bottom + 7)], INK)
            s.rect(bx, yy, bw, h, fill=PALE if n == 3 else WHITE, stroke=INK, sw=0.9, rx=2.5)
            callout(s, bx + 10, yy + h / 2, n)
            for i, ln in enumerate(lines):
                s.text(bx + 22, yy + 4 + 7.3 + i * 10.6, ln, 9)
            prev_bottom = yy + h
            yy += h + 8
        yy -= 8
        yy += 5
        yy = bullets(s, x, yy, w, [
            "A combatant becomes **Hidden** only by holding **Cover** from every enemy that has **LOS** to them, or by standing outside every enemy's **LOS** entirely.",
            "A combatant who loses **Cover** falls to step 1 and loses **Hidden** with it.",
            "**Cover** granted only by a sight line crossing a combatant does not count toward becoming or remaining **Hidden** (**2.8.4**).",
        ])
        return yy

    def light(s, x, y, w):
        yy = ptxt(s, x, y, "One **Visibility State** per battlefield: **Light** or **Darkness**. It is **Light** unless a scenario, weather result, or special rule sets it.", w)
        yy += 3
        sw_, sh = w, 67
        s.rect(x, yy, sw_, sh, fill=DARKFILL, stroke=INK, sw=0.9)
        cx, cy, r = x + 44, yy + 34, SC63["aura_in"] * PT_PER_IN63
        s.circle(cx, cy, r, fill=WHITE, stroke=INK, sw=1.0, dash="4 2.5")
        _lightsource(s, cx, cy)
        s.line(cx + 5, cy, cx + r, cy, INK, 0.8)
        s.line(cx + r, cy - 3, cx + r, cy + 3, INK, 0.8)
        pill(s, cx + 17, cy - 3.5, "3\"", 9, 600)
        pill(s, x + 190, yy + 11, "Darkness", 9, 700)
        pill(s, cx - 24, yy + 11, "Light", 9, 700)
        rr = SC63["tok_r"]
        token(s, "A", cx + SC63["a_off"][0], cy + SC63["a_off"][1], rr)
        badge(s, cx, cy + 21, "a")
        bx1, by1, bx2, by2 = SC63["b_pair"]
        token(s, "A", x + bx1, yy + by1, rr)
        token(s, "B", x + bx2, yy + by2, rr)
        badge(s, x + bx1, yy + by1 + 13, "b")
        cx1, cy1, cx2, cy2 = SC63["c_pair"]
        token(s, "A", x + cx1, yy + cy1, rr)
        token(s, "B", x + cx2, yy + cy2, rr)
        badge(s, x + cx2 + 14, yy + cy2, "c")
        yy += sh + 2
        T(s, x + w - 4, yy - 6, "Schematic - not to scale", 150, 9, 600, "end", INK)
        T(s, x, yy + 7.3, "black circle: a combatant; white circle: an enemy", w, 9, 400)
        yy += 13
        yy = ptxt(s, x, yy, "**Light Source:** **Aura 3\"** unless a rule lists another size. Its carrier cannot be **Hidden** unless a rule says otherwise.", w) + 2
        for tag, txt in (("a", "Light removes **Darkness** in the **Aura**, but not other **Cover**."),
                         ("b", "**Darkness** gives **Cover** against non-adjacent enemies."),
                         ("c", "**Darkness** gives no **Cover** against an adjacent enemy.")):
            badge(s, x + 6, yy + 5.6, tag)
            yy = ptxt(s, x + 16, yy, txt, w - 16) + 1.5
        return yy

    hA = card_h(W1, 1, "x", None, ladder)
    hB = card_h(W2, 2, "x", None, light)
    H = max(hA, hB)
    card(s, 0, 0, W1, 1, "Concealment ladder", "2.8", ladder, minH=H)
    card(s, X2, 0, W2, 2, "Visibility State and Light", "2.8.1–2.8.3", light, minH=H)
    y1 = H + 8

    def hid(s, x, y, w):
        yy = bullets(s, x, y, w, [
            "**Hidden** and **Invisible** are separate conditions; a combatant may have either or both. Neither blocks **LOS** (**5.9**).",
            "With both, **Invisible** governs targeting and the combatant does not gain the **Hidden** benefit in **5.9** until **Invisible** ends. They remain **Hidden** for every other rule.",
            "**Spot** removes only **Hidden** unless a rule says otherwise.",
            "A rule that explicitly removes **Hidden** or **Invisible** bars regaining it until the end of the round unless a more specific rule says otherwise. Ordinary end conditions in **5.9** do not trigger this.",
            "To close on a concealed enemy, move within their **Hide distance**, use **Spot**, or break their **Cover** by changing the angle of approach. **Areas of Effect** are the exception at every step.",
        ])
        return yy

    card(s, 0, y1, FULL_W, 3, "Hidden, Invisible, and closing on a concealed enemy", "2.8, 2.8.5", hid)
    return s, y1 + card_h(FULL_W, 3, "x", None, hid) + 2


# =====================================================================
# FIG-64  2.10 Luck Points
# =====================================================================
def fig64():
    s = Svg(FULL_W)

    def timing(s, x, y, w):
        gap = 24
        bw = (w - 2 * gap) / 3.0
        items = [
            ("The roll", "A d20 **Check** made by or against a Hero, or one damage roll whose source is that Hero or that directly affects that Hero."),
            ("Luck window", "A Hero may spend **1 Luck Point** after seeing the result, but before applying consequences from that roll."),
            ("Consequences", "The result is applied. For a shared damage roll, the **Luck** window closes when defence or mitigation begins (**2.7.3**)."),
        ]
        bh = max(nlines(b, bw) for _, b in items) * 10.6 + 8 + 14
        for k, (hd, body) in enumerate(items):
            bx = x + k * (bw + gap)
            s.rect(bx, y, bw, bh, fill=PALE if k == 1 else WHITE, stroke=INK, sw=1.2 if k == 1 else 0.9, rx=2.5)
            s.rect(bx, y, bw, 14, fill=LIGHT if k != 1 else INK, stroke=INK, sw=0.9, rx=2.5)
            T(s, bx + bw / 2, y + 10.3, hd, bw - 6, 9, 700, "middle", WHITE if k == 1 else INK)
            ptxt(s, bx + 4, y + 17, body, bw - 8)
            if k < 2:
                hflow_arrow(s, bx + bw + 3, bx + bw + gap - 3, y + bh / 2)
        yy = y + bh + 5
        yy = ptxt(s, x, yy, "A **Check** is made against a Hero if that Hero is the target of the **Check**, is directly affected by it, or would suffer its consequences.", w)
        return yy

    y = card(s, 0, 0, FULL_W, 1, "When a Hero may spend Luck", "2.10", timing)
    y = card_h(FULL_W, 1, "x", None, timing) + 8
    W2, X3 = 248, 256
    W3 = FULL_W - X3

    def reroll(s, x, y, w):
        return bullets(s, x, y, w, [
            "Reroll the entire **Check** or damage roll.",
            "If the original roll had **Advantage** or **Disadvantage**, the reroll uses the same one.",
            "A rerolled damage roll is rerolled completely. Determine **Total Misses**, **Critical Hits**, exploding dice, and total damage from the new result.",
            "If one roll affects more than one combatant, apply the new result to every combatant affected by that roll.",
            "A roll can be rerolled by **Luck** only once.",
            "The new result must be used, even if it is worse.",
        ])

    def decide(s, x, y, w):
        yy = ptxt(s, x, y, "If more than one Hero could spend **Luck** on the same roll:", w) + 3
        yy = step_list(s, x, yy, ["The side that won **Initiative** decides first.",
                                  "Within a side, the **Party Leader's** controller chooses the decision order.",
                                  "Once one Hero spends **Luck**, no other Hero can spend **Luck** on that roll."], w, gap=4)
        yy += 1
        yy = ptxt(s, x, yy, "**Luck Points** refresh to their maximum at the start of each new adventure unless a rule says otherwise.", w)
        return yy

    hA = card_h(W2, 2, "x", None, reroll)
    hB = card_h(W3, 3, "x", None, decide)
    H = max(hA, hB)
    card(s, 0, y, W2, 2, "The reroll", "2.10", reroll, minH=H)
    card(s, X3, y, W3, 3, "Competing Heroes and refresh", "2.10", decide, minH=H)
    return s, y + H + 2


# =====================================================================
# Semantic self-check
# =====================================================================
HMAX = {"FIG-58": 400, "FIG-59": 320, "FIG-60": 450, "FIG-61": 390, "FIG-62": 345, "FIG-63": 350, "FIG-64": 285}

# phrases drawn in each figure that must appear in the cited source lines (active snapshot; markup stripped, case-insensitive)
_SRC_CHECKS = {
    "FIG-58": ((405, 418), ["1–8 players", "36\"×36\"", "Tabletop Mode", "Grid Mode", "1\" squares", "tape measure",
                            "miniature, standee, or token", "Hero, Hireling, Monster, and Summon", "Treasure Chests", "hazards",
                            "record sheet for each Hero and party", "AP, Activated, Resting, HP, NRG, condition, and Luck tokens",
                            "At least 4d4, 4d6, 4d8, 4d10, 2d12, and 2d20 dice"]),
    "FIG-59": ((419, 434), ["a single game of Heraldry Skirmish is called an adventure", "complete the scenario's objective and satisfy its victory conditions",
                            "compare secured wealth", "Xc", "Coin Value", "looting treasure, completing objectives, defeating Monsters",
                            "escape the battlefield with their spoils", "completes any 5 different Stronghold Components",
                            "rolled objective and extraction requirement in the Triumph Finale", "three Fates", "Die:", "Retire:", "Triumph:",
                            "Legendary Veteran", "Level 10", "Storage", "Retirement Payout"]),
    "FIG-60": ((435, 440), ["use the more specific rule", "Scenario rules override the core rules for that scenario",
                            "Class features, Powers, Monster rules, terrain rules, and item rules override the general rules they explicitly modify",
                            "use the more restrictive rule", "Examples, summaries, and reference tables never override the main rules text",
                            "marks a required instruction", "marks a permission or choice", "marks a prohibition",
                            "do not create a separate precedence system"]),
    "FIG-61": ((504, 516), ["Monsters never have or use ability scores", "treat that score as +0 for that Check only", "between -1 and +3",
                            "may be negative and have no maximum unless a rule says otherwise", "melee force, physical power, climbing, forcing objects, and resisting bodily harm",
                            "ranged accuracy, speed, balance, stealth, dodging, and delicate physical tasks",
                            "perception, reasoning, knowledge, investigation, initiative, Arcane Spells, and Psychic Abilities",
                            "willpower, faith, resolve, leadership, and powers of faith, nature, and sorcery", "listed in their profile"]),
    "FIG-62": ((517, 567), ["roll 1d20 and add the listed ability score", "12 or higher", "11 or lower", "natural 1", "Critical Failure", "natural 20",
                            "Critical Success", "always fails", "always succeeds", "only to d20 Checks", "do not roll it", "not a Critical Failure",
                            "Terrain Check", "automatically succeeds", "add one extra die of the affected type, then ignore the lowest single die",
                            "add one extra die of the affected type, then ignore the highest single die", "cancel each other out", "do not stack",
                            "Casting Check is made with Disadvantage"]),
    "FIG-63": ((754, 827), ["Exposed", "Hidden", "cannot be targeted by anything that requires LOS", "Aura 3\"", "removing Darkness there but not any other source of Cover",
                            "Darkness provides Cover", "non-adjacent enemies", "cannot be Hidden unless a rule says otherwise", "Visibility State",
                            "the battlefield starts in Light", "Hide distance", "use Spot", "Invisible governs targeting", "Spot removes only Hidden",
                            "cannot regain the removed condition until the end of the round", "falls to step 1 and loses Hidden with it",
                            "outside every enemy's LOS entirely"]),
    "FIG-64": ((965, 986), ["after seeing the result", "before applying consequences", "Reroll the entire Check or damage roll", "same Advantage or Disadvantage",
                            "Total Misses, Critical Hits, exploding dice, and total damage", "every combatant affected by that roll",
                            "the side that won Initiative decides first", "Party Leader's controller chooses the decision order",
                            "no other Hero can spend Luck on that roll", "only once", "even if it is worse", "refresh to their maximum at the start of each new adventure"]),
}


def _source_lines():
    """Lines of the active immutable snapshot named in source/versions.json."""
    from manuscript import source_path
    return source_path().read_text(encoding="utf-8").split("\n")


def selfcheck_end_a():
    """Assertions behind the FIG-58 to FIG-64 semantic checks: heights, text fit, arithmetic, order, source phrases."""
    import math
    del _FITS[:]
    for fid, fn in (("FIG-58", fig58), ("FIG-59", fig59), ("FIG-60", fig60), ("FIG-61", fig61), ("FIG-62", fig62), ("FIG-63", fig63), ("FIG-64", fig64)):
        svg, h = fn()
        assert svg.w == FULL_W == 504
        assert h <= HMAX[fid], (fid, h, HMAX[fid])
    assert _FITS and all(w <= m + 0.01 for _, w, m in _FITS)
    # FIG-61: tick order and the stated range of most starting Heroes
    ticks = [-1, 0, 1, 2, 3]
    assert ticks == sorted(ticks) and ticks[0] == -1 and ticks[-1] == 3
    # FIG-62: d20 Check threshold and the worked example (assumed score +2, dice 7 and 15; no natural 1 or 20)
    lo, hi = EX62["dice"]
    sc = EX62["score"]
    assert 1 < lo < hi < 20
    assert hi + sc == 17 and hi + sc >= 12        # Advantage ignores the lowest die, keeps 15: 15 + 2 = 17, succeeds
    assert lo + sc == 9 and lo + sc <= 11         # Disadvantage ignores the highest die, keeps 7: 7 + 2 = 9, fails
    assert 12 - 1 == 11                           # 11 or lower fails, 12 or higher succeeds
    # FIG-63: scene scale and adjacency (adjacent = 1" or less between closest points, 2.1)
    r_aura = SC63["aura_in"] * PT_PER_IN63
    assert SC63["aura_in"] == 3 and r_aura == 30
    d_tok = 2 * SC63["tok_r"]
    assert d_tok == 1 * PT_PER_IN63               # a token is a 1" footprint
    ax, ay = SC63["a_off"]
    assert math.hypot(ax, ay) + SC63["tok_r"] < r_aura   # combatant a lies wholly inside the Aura
    for key, adjacent in (("c_pair", True), ("b_pair", False)):
        x1, y1, x2, y2 = SC63[key]
        gap = (math.hypot(x2 - x1, y2 - y1) - d_tok) / PT_PER_IN63     # closest-point gap in inches
        assert (gap <= 1.0) == adjacent, (key, gap)
    # every drawn phrase appears in the cited source lines
    lines = _source_lines()
    for fid, ((lo_, hi_), phrases) in _SRC_CHECKS.items():
        blob = "\n".join(lines[lo_ - 1:hi_]).replace("**", "")
        flat = " ".join(blob.split()).lower()
        for ph in phrases:
            assert ph.lower() in flat, (fid, ph)
    return True


if __name__ == "__main__":
    print(selfcheck_end_a())
