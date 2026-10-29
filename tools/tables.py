"""Table measurement, classification and column-width allocation (deterministic)."""
from __future__ import annotations
import math, re
from metrics import width

from layout_profile import (TABLE_SIZE_PT, TABLE_LEADING_PT,
    TABLE_HORIZONTAL_PADDING_PT, TABLE_VERTICAL_PADDING_PT,
    COLUMN_WIDTH_PT, FRAME_WIDTH_PT, BODY_HEIGHT_PT)

# Width allocation is advisory; final keep decisions use real Typst measurements.
PT = TABLE_SIZE_PT
LEAD = PT * 1.05 + TABLE_LEADING_PT  # renderer's 0.8em top and -0.25em bottom edges
PAD = TABLE_HORIZONTAL_PADDING_PT
VPAD = TABLE_VERTICAL_PADDING_PT
COL_W = COLUMN_WIDTH_PT
FULL_W = FRAME_WIDTH_PT
BODY_H = BODY_HEIGHT_PT


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
    w = "Bold" if header else "Semibold" if bold else "Regular"
    if ital:
        w = w + "Italic" if w != "Regular" else "Italic"
    return width(s, size, "SourceSans3", w)


# Units that should not break internally in tables; measured as one "word".
NOBREAK = re.compile(r"\d+d\d+(?: ?[+×x−-] ?(?:APL/\d|\d+))?|\[\d+ AP\]|\d+ AP|\d+\"|\d+–\d+|\w+ \(c\)")


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


def cell_segments(nodes, header=False):
    """Explicit-break segments of one cell, each a list of (word width, following space width)."""
    segments = [[]]
    for s, b, i in runs(nodes):
        if s == "\n":
            segments.append([])
            continue
        protected = NOBREAK.sub(lambda m: m.group(0).replace(" ", "\u00a0"), s)
        space = seg_width(" ", b, i, header=header)
        for part in re.split(r"( )", protected):
            if part == " ":
                if segments[-1]:
                    word, _ = segments[-1][-1]
                    segments[-1][-1] = (word, space)
            elif part:
                width_ = seg_width(part.replace("\u00a0", " "), b, i, header=header)
                if segments[-1] and segments[-1][-1][1] == 0.0 and not part.startswith(" "):
                    word, _ = segments[-1][-1]
                    segments[-1][-1] = (word + width_, 0.0)   # style change inside one word
                else:
                    segments[-1].append((width_, 0.0))
    return segments


def wrapped_lines(segments, inner):
    """First-fit word wrapping (unjustified table cells); an over-long word takes its own line."""
    total = 0
    for words in segments:
        lines, used = 1, 0.0
        for k, (word, space) in enumerate(words):
            gap = words[k - 1][1] if k else 0.0
            if used and used + gap + word > inner:
                lines += 1
                used = word
            else:
                used += (gap if used else 0.0) + word
        total += lines
    return max(1, total)


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


def _proportional(w, maxs, total):
    """Water-fill the remaining slack proportionally to each column's unmet want."""
    n = len(w)
    slack = total - sum(w)
    want = [mx - x for x, mx in zip(w, maxs)]
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
    return w


def _cell_grid(tables):
    """Word segments of every cell, header rows included."""
    return [[cell_segments(cell, header=(r == 0)) for cell in row]
            for tb in tables for r, row in enumerate([tb["header"]] + tb["rows"])]


def _lines(segments, width, memo):
    key = (id(segments), round(width, 2))
    if key not in memo:
        memo[key] = wrapped_lines(segments, max(10.0, width - 2 * PAD) / 1.01)
    return memo[key]


def _break_width(segments, lines_now, width, limit):
    """Smallest width (to 0.25 pt) above `width` that sets the cell in fewer lines, or None."""
    lo, hi = width, limit
    if wrapped_lines(segments, max(10.0, hi - 2 * PAD) / 1.01) >= lines_now:
        return None
    while hi - lo > 0.25:
        mid = (lo + hi) / 2
        if wrapped_lines(segments, max(10.0, mid - 2 * PAD) / 1.01) < lines_now:
            hi = mid
        else:
            lo = mid
    return round(hi + 0.01, 2)


def allocate(mins, maxs, total, tables=None):
    """Column widths for a table (or a family sharing widths).

    Every column first receives its longest unbreakable word. With the source
    cells available, remaining width goes where it removes the most wrapped
    lines per point (a greedy minimisation of the estimated table height, after
    Anderson and Sobti's "tighter tables"), so a short name column is not left
    wrapping onto three lines beside a generous prose column. Any width still
    unused is shared in proportion to each column's unmet natural width.
    Without cells this is the classic proportional auto-table allocation.
    """
    n = len(mins)
    mins = [m + 2 * PAD + 0.5 for m in mins]
    maxs = [max(a, m + 2 * PAD + 0.5) for a, m in zip(mins, maxs)]
    if sum(maxs) <= total:
        return maxs, True
    if sum(mins) > total:
        return None, False
    w = list(mins)
    if tables:
        grid = [row for row in _cell_grid(tables) if len(row) == n]
        memo = {}
        lines = [[_lines(seg, w[c], memo) for c, seg in enumerate(row)] for row in grid]
        while total - sum(w) > 0.01:
            slack = total - sum(w)
            best = None
            for c in range(n):
                limit = min(maxs[c], w[c] + slack)
                if limit <= w[c] + 0.01:
                    continue
                steps = set()
                for r, row in enumerate(grid):
                    if lines[r][c] > 1:
                        need = _break_width(row[c], lines[r][c], w[c], limit)
                        if need is not None:
                            steps.add(need)
                for need in sorted(steps)[:12]:
                    gain = 0
                    for r, row in enumerate(grid):
                        new = _lines(row[c], need, memo)
                        if new < lines[r][c]:
                            others = max((lines[r][k] for k in range(n) if k != c), default=1)
                            gain += max(lines[r][c], others) - max(new, others)
                    if gain > 0:
                        score = (gain / (need - w[c]), -(need - w[c]), maxs[c])
                        if best is None or score > best[0]:
                            best = (score, c, need)
            if best is None:
                break
            _, c, need = best
            w[c] = need
            for r, row in enumerate(grid):
                lines[r][c] = _lines(row[c], w[c], memo)
    return _proportional(w, maxs, total), False


def est_height(tb, widths):
    """Estimated rendered height (pt) given column widths."""
    total = 0.0
    rows_h = []
    for r, row in enumerate([tb["header"]] + tb["rows"]):
        h = 1
        for c, cell in enumerate(row):
            inner = max(10.0, widths[c] - 2 * PAD) / 1.01
            h = max(h, wrapped_lines(cell_segments(cell, header=(r == 0)), inner))
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
    # The scope decision keeps the reviewed proportional rule; widths then use the cell-aware fill.
    wp, natural = allocate(mins, maxs, COL_W)
    if wp:
        skinny = any(w < 70 and maxs[i] > w * 2.2 for i, w in enumerate(wp))
        if not skinny:
            wc, _ = allocate(mins, maxs, COL_W, [tb])
            h, _ = est_height(tb, wc)
            out.update(rep="stat" if is_stat else "table", scope="column", widths=[round(x, 2) for x in wc], est_h=round(h))
            return out
    wf, natural = allocate(mins, maxs, FULL_W, [tb])
    if wf:
        h, rows_h = est_height(tb, wf)
        out.update(rep="table", scope="full", widths=[round(x, 2) for x in wf], est_h=round(h),
                   max_row_h=round(max(rows_h)))
        return out
    out.update(rep="cards", desc_cols=long_desc or [ncol - 1], scope="column")
    return out
