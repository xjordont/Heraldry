"""Explain sparse pages and paragraph tails without pretending whitespace is a bug."""
import statistics


def interval_summary(intervals, top, bottom):
    merged = []
    for lo, hi in sorted((max(top, a), min(bottom, b)) for a, b in intervals if b > top and a < bottom):
        if hi <= lo:
            continue
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(hi, merged[-1][1])
        else:
            merged.append([lo, hi])
    gaps, previous = [], top
    for lo, hi in merged:
        if lo > previous:
            gaps.append((previous, lo))
        previous = hi
    if previous < bottom:
        gaps.append((previous, bottom))
    return {"vertical_union_fraction": round(sum(b - a for a, b in merged) / (bottom - top), 4),
            "largest_empty_band_pt": round(max((b - a for a, b in gaps), default=0), 2),
            "bottom_empty_band_pt": round(bottom - merged[-1][1], 2) if merged else round(bottom - top, 2)}


def page_diagnostics(page, number, *, top, bottom, tab):
    width = page.rect.width
    text, intervals, short, baselines = [], [], [], []
    for block in page.get_text("dict")["blocks"]:
        body_lines = []
        for line in block.get("lines", []):
            spans = line["spans"]
            if not spans:
                continue
            x0, y0, x1, y1 = line["bbox"]
            if y0 < top - 2 or y1 > bottom + 2 or x1 <= tab or x0 >= width - tab:
                continue
            text.append((x0, y0, x1, y1))
            intervals.append((y0, y1))
            body_lines.append(line)
            baselines.append((round(x0, 1), float(spans[0]["origin"][1]), round(spans[0]["size"], 1)))
        if 0 < len(body_lines) <= 2:
            excerpt = " ".join(s["text"] for line in body_lines for s in line["spans"])
            short.append({"lines": len(body_lines), "text": excerpt[:100], "y_pt": round(body_lines[0]["bbox"][1], 2)})
    for image in page.get_image_info():
        x0, y0, x1, y1 = image["bbox"]
        if x1 > tab and x0 < width - tab:
            intervals.append((y0, y1))
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        # Full-sheet substrate and running furniture are not body occupancy. A drawing counts only when
        # at least half of its width lies inside the body frame: the thumb-tab pennant and the opener
        # frame straddle the outer strip and used to be read as content, which capped the foot-void
        # measure at the tab's own position (design audit 2026-11-01, P-04).
        overlap = min(rect.x1, width - tab) - max(rect.x0, tab)
        if rect.y0 >= top and rect.y1 <= bottom and overlap > 0 and overlap >= 0.5 * max(rect.width, 0.01):
            intervals.append((rect.y0, rect.y1))
    pitches = []
    for (xa, ya, sa), (xb, yb, sb) in zip(baselines, baselines[1:]):
        if abs(xa - xb) < 1 and sa == sb and 0 < yb - ya < sa * 2:
            pitches.append(yb - ya)
    left = sum(x1 <= width / 2 + 5 for x0, y0, x1, y1 in text)
    right = sum(x0 >= width / 2 - 5 for x0, y0, x1, y1 in text)
    summary = interval_summary(intervals, top, bottom)
    # A sparse page: under 55% of the frame height occupied and fewer than 50 text lines. The flag is a
    # review pointer, not a defect: deliberate section starts, tailpiece pages and art pages qualify.
    sparse = summary["vertical_union_fraction"] < 0.55 and len(text) < 50
    return {"page": number, **summary, "sparse": sparse, "body_lines": len(text),
            "column_lines": {"left": left, "right": right, "spanning": len(text) - left - right},
            "median_neighbouring_baseline_pt": round(statistics.median(pitches), 3) if pitches else None,
            "short_text_blocks": short[:20],
            "interpretation": "review context: complete-unit keep, fresh start, artwork, content end or excess composition gap"}
