"""Table measurement, classification and column-width allocation (deterministic)."""
from __future__ import annotations
import math, re
from metrics import width

# Must match typst/heraldry.typ's live table components, not retired v1 tokens.
PT = 9.3            # active table-size
LEAD = 12.0         # 9.3pt text plus 2.7pt line leading
PAD = 5.0           # active htable inset (each side)
VPAD = 4.0          # active htable inset (top and bottom)
COL_W = 250.5       # one text column (design v4: (7.2 in - 0.24 in) / 2)
FULL_W = 518.4      # full text frame (design v4: 8.5 in - 0.75 in - 0.55 in = 7.2 in)
BODY_H = 792 - 0.68 * 72 - 0.7 * 72   # 688.6 pt text frame height (design v4)


def runs(nodes, bold=False, ital=False):
    """Yield (text, bold, italic) segments; '\n' marks explicit line breaks."""
    for n in nodes:
        t = n["t"]
        if t in ("text", "code"):
            yield n["v"], bold, ital
        elif t in ("br", "soft"):
            yield "\n", bold, ital
        elif t == "strong":
            yield from runs(n["c"], True, ital)
        elif t == "em":
            yield from runs(n["c"], bold, True)
        elif t == "link":
            yield from runs(n["c"], bold, ital)


def seg_width(s, bold, ital, size=PT, header=False):
    w = "Semibold" if (bold or header) else "Regular"
    if ital:
        w = "SemiboldItalic" if w == "Semibold" else "Italic"
    return width(s, size, "SourceSans3", w)


# Units that should not break internally in tables; measured as one "word".
NOBREAK = re.compile(r"\d+d\d+(?: ?[+×x−-] ?(?:APL/\d|\d+))?|\[\d+ AP\]|\d+ AP|\d+\"|\d+–\d+")


def cell_metrics(nodes, header=False):
    """Return (min_content, max_content) widths in pt for one cell."""
    lines = [0.0]
    words = []
    cur_word = 0.0
    for s, b, i in runs(nodes):
        if s == "\n":
            lines.append(0.0)
            words.append(cur_word); cur_word = 0.0
            continue
        lines[-1] += seg_width(s, b, i, header=header)
        # split into words, keeping no-break units together
        protected = NOBREAK.sub(lambda m: m.group(0).replace(" ", " "), s)
        parts = re.split(r"( )", protected)
        for p in parts:
            if p == " ":
                words.append(cur_word); cur_word = 0.0
            elif p:
                cur_word += seg_width(p.replace(" ", " "), b, i, header=header)
    words.append(cur_word)
    return max(words) if words else 0.0, max(lines)


def cell_plain(nodes):
    return "".join(s for s, _, _ in runs(nodes))


def measure_table(tb):
    ncol = len(tb["header"])
    mins, maxs, sums = [0.0] * ncol, [0.0] * ncol, [0.0] * ncol
    for r, row in enumerate([tb["header"]] + tb["rows"]):
        for c, cell in enumerate(row):
            mn, mx = cell_metrics(cell, header=(r == 0))
            mins[c] = max(mins[c], mn)
            maxs[c] = max(maxs[c], mx)
            if r:
                sums[c] += mx
    avgs = [s / max(1, len(tb["rows"])) for s in sums]
    return mins, maxs, avgs


def allocate(mins, maxs, total):
    """Classic auto-table: give every column its minimum, then share the slack
    proportionally to (max-min) so that long prose columns receive most width."""
    n = len(mins)
    mins = [m + 2 * PAD + 0.5 for m in mins]
    maxs = [max(a, m + 2 * PAD + 0.5) for a, m in zip(mins, maxs)]
    if sum(maxs) <= total:
        return maxs, True
    if sum(mins) > total:
        return None, False
    w = list(mins)
    slack = total - sum(mins)
    want = [mx - mn for mn, mx in zip(mins, maxs)]
    # iterative water-filling so no column exceeds its max
    active = [i for i in range(n) if want[i] > 0]
    while slack > 0.01 and active:
        tot = sum(want[i] for i in active)
        done = []
        for i in active:
            give = slack * want[i] / tot
            room = maxs[i] - w[i]
            if give >= room:
                w[i] = maxs[i]; done.append(i)
            else:
                w[i] += give
        slack = total - sum(w)
        if not done:
            break
        active = [i for i in active if i not in done]
    return w, False


def est_height(tb, widths):
    """Estimated rendered height (pt) given column widths."""
    total = 0.0
    rows_h = []
    for r, row in enumerate([tb["header"]] + tb["rows"]):
        h = 1
        for c, cell in enumerate(row):
            _, mx = cell_metrics(cell, header=(r == 0))
            inner = max(10.0, widths[c] - 2 * PAD)
            nbr = sum(1 for s, _, _ in runs(cell) if s == "\n")
            lines = max(1, math.ceil(mx * 1.04 / inner)) + nbr
            h = max(h, lines)
        rh = h * LEAD + 2 * VPAD
        rows_h.append(rh)
        total += rh
    return total, rows_h


def classify(tb, meta):
    """Return a dict with representation, widths (pt) and diagnostics."""
    header = [cell_plain(h) for h in tb["header"]]
    mins, maxs, avgs = measure_table(tb)
    ncol = len(header)
    is_stat = header[:6] == ["HP", "AV", "SPD", "LVL", "CV", "Sz"]
    out = {"id": tb["id"], "columns": ncol, "rows": len(tb["rows"]), "header": header,
           "min_pt": [round(x, 1) for x in mins], "max_pt": [round(x, 1) for x in maxs]}
    long_desc = [i for i in range(ncol) if avgs[i] > 160]   # ≈ >30 words average
    # Prose-heavy many-column tables become labelled entries (cards)
    if ncol >= 6 and long_desc and not is_stat:
        out.update(rep="cards", desc_cols=long_desc, scope="column")
        return out
    wc, natural = allocate(mins, maxs, COL_W)
    if wc:
        skinny = any(w < 70 and maxs[i] > w * 2.2 for i, w in enumerate(wc))
        h, _ = est_height(tb, wc)
        if not skinny:
            out.update(rep="stat" if is_stat else "table", scope="column", widths=[round(x, 2) for x in wc], est_h=round(h))
            return out
    wf, natural = allocate(mins, maxs, FULL_W)
    if wf:
        h, rows_h = est_height(tb, wf)
        out.update(rep="table", scope="full", widths=[round(x, 2) for x in wf], est_h=round(h),
                   max_row_h=round(max(rows_h)))
        return out
    out.update(rep="cards", desc_cols=long_desc or [ncol - 1], scope="column")
    return out
