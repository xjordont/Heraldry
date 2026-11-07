#!/usr/bin/env python3
"""Geometry detectors for every page: text overlap, text outside the body frame
(other than running furniture), unsafe edges, tiny type, near-empty pages, and a composition rule drawn
through text. Detectors flag pages for visual review; they do not prove good layout. The report also
carries the advisory column-flow measures of tools/layout_flow.py (short columns by cause, low
right-column starts, uneven chapter ends, chapter spans), which are not flags."""
import argparse, json
from pathlib import Path
import pymupdf
from layout_profile import PAGE_WIDTH_PT, PAGE_HEIGHT_PT, MARGIN_TOP_PT, MARGIN_BOTTOM_PT, MARGIN_OUTSIDE_PT, TOKENS
from layout_diagnostics import page_diagnostics
import layout_flow

W, H = PAGE_WIDTH_PT, PAGE_HEIGHT_PT
SAFE = TOKENS["page"]["essential_edge_safe_pt"]
TOP, BOT = MARGIN_TOP_PT, H - MARGIN_BOTTOM_PT
# The thumb-tab strip: the outer margin plus the pennant's paper halo. The old 0.42 in strip was
# narrower than the pennant, so its drawing counted as body content on every recto and the
# near-empty detector never fired there (design audit 2026-11-01).
TAB = MARGIN_OUTSIDE_PT + TOKENS["ornament"].get("tab_halo_pt", 0)


def page_text(page):
    """The page's text twice: with font metric boxes, and with glyph-ink boxes. Rotated navigation keywords are
    measured by their ink, not the font's tall metric box. Extracted once per page and shared by every detector."""
    return (page.get_text("dict"),
            page.get_text("dict", flags=pymupdf.TEXTFLAGS_DICT | pymupdf.TEXT_ACCURATE_BBOXES))


def lines_of(page, fonts=False, text=None):
    out = []
    flat, ink = text if text is not None else page_text(page)
    lines = [l for b in flat["blocks"] for l in b.get("lines", []) if abs(l["dir"][0]) >= 0.5]
    lines += [l for b in ink["blocks"] for l in b.get("lines", []) if abs(l["dir"][0]) < 0.5]
    for l in lines:
        txt = "".join(s["text"] for s in l["spans"]).strip()
        if not txt:
            continue
        size = max(s["size"] for s in l["spans"])
        out.append((pymupdf.Rect(l["bbox"]), txt, size) + ((l["spans"][0]["font"],) if fonts else ()))
    return out


def stranded_headings(page, text=None):
    """Heading-styled line in the last 60 pt of a column with < 2 lines after it in that column."""
    ls = lines_of(page, fonts=True, text=text)
    hits = []
    for r, t, sz, f in ls:
        is_head = ("Grenze" in f and sz > 12) or ("Serif4-Semibold" in f and sz > 12) or ("Serif4-Bold" in f and sz > 10.8)
        if is_head and r.y1 > BOT - 60 and r.y0 > 200:
            below = [x for x in ls if x[0].y0 > r.y1 and abs(x[0].x0 - r.x0) < 60]
            if len(below) < 2:
                hits.append(t[:50])
    return hits


def head_alone(body_lines, heads):
    """True when a page's body text is only the headings the outline lists for it: a head stranded on a page of
    its own while its content went overleaf (candidate 24, p. 100: 6.7 Human Trinket Table). Its rule and band
    are drawings, so near_empty does not see it."""
    if not heads:
        return False
    other = [t for t in body_lines if t.strip() and not any(t.strip() in h for h in heads)]
    return len(other) < 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--report", required=True)
    ap.add_argument("--first-body-page", type=int)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    body_starts = [page for level, _, page in doc.get_toc(simple=True) if level == 1 and page > 0]
    first_body_page = a.first_body_page if a.first_body_page is not None else min(body_starts, default=1)
    flags, diagnostics, measures = [], [], {}
    outline = doc.get_toc(simple=True)
    opener_pages = {page for level, _, page in outline if level == 1 and page > 0}
    for i, page in enumerate(doc):
        n = i + 1
        text, drawings = page_text(page), page.get_drawings()
        diagnostics.append(page_diagnostics(page, n, top=TOP, bottom=BOT, tab=TAB, text_dict=text[0], drawings=drawings))
        measures[n] = layout_flow.page_measures(page, text[0], drawings)
        for hit in measures[n]["strikes"]:
            flags.append({"page": n, "code": "rule_through_text", "text": hit["text"], "rule_y": hit["rule_y"]})
        ls = lines_of(page, text=text)
        # overlap: shrink boxes slightly (ascender/descender overlap is normal)
        boxes = [(pymupdf.Rect(r.x0 + 1, r.y0 + r.height * 0.3, r.x1 - 1, r.y1 - r.height * 0.3), t, s) for r, t, s in ls]
        for x in range(len(boxes)):
            for y in range(x + 1, len(boxes)):
                r1, r2 = boxes[x][0], boxes[y][0]
                if r1.intersects(r2):
                    inter = r1 & r2
                    if inter.get_area() > 6:
                        flags.append({"page": n, "code": "text_overlap", "a": boxes[x][1][:50], "b": boxes[y][1][:50]})
        for r, t, s in ls:
            if r.x1 < TAB or r.x0 > W - TAB:
                continue   # thumb tab: rotated chapter keyword in the outer strip (navigation furniture, bleeds by design)
            if min(r.x0, r.y0, W - r.x1, H - r.y1) < SAFE - 0.1:
                flags.append({"page": n, "code": "unsafe_edge", "text": t[:50]})
            if s < 8.9:
                flags.append({"page": n, "code": "small_type", "size": round(s, 2), "text": t[:50]})
            furniture = s <= 9.6 and (r.y1 < TOP or r.y0 > BOT - 2)
            if not furniture and (r.y1 > BOT + 2 or r.y0 < TOP - 14):
                flags.append({"page": n, "code": "outside_body_frame", "text": t[:50], "bbox": [round(v) for v in r]})
        if n >= first_body_page:
            for t in stranded_headings(page, text=text):
                flags.append({"page": n, "code": "stranded_heading", "text": t})
        # a body line overlaps the frame: left-column lines start exactly at the margin, so an open test
        # on x0 would drop them and the page would read as empty (local build 2026-11-01)
        body = [r for r, t, s in ls if TOP - 2 < r.y0 and r.y1 < BOT + 2 and r.x1 > TAB and r.x0 < W - TAB]
        # furniture (running-head rules, folio shield, tab) draws on every page, so only art or drawings
        # inside the body frame count as content
        body_art = [im for im in page.get_image_info() if im["bbox"][1] > TOP and im["bbox"][3] - im["bbox"][1] > 40]
        body_drw = [dr for dr in drawings if dr["rect"].y0 > TOP + 4 and dr["rect"].y1 < BOT - 4
                    and dr["rect"].x0 < W - TAB and dr["rect"].x1 > TAB and dr["rect"].width > 4]
        # a deliberate blank verso before a chapter opener (Chapter 1 starts on a recto) is book convention
        blank_verso = not body and n % 2 == 0 and n < len(doc) and "Chapter " in doc[n].get_text()[:400]
        if n >= first_body_page and len(body) < 6 and not body_art and not body_drw and not blank_verso:
            flags.append({"page": n, "code": "near_empty", "lines": len(body)})
        heads = [title for level, title, page in outline if page == n and level >= 2]
        body_text = [t for r, t, s in ls if TOP - 2 < r.y0 and r.y1 < BOT + 2 and r.x1 > TAB and r.x0 < W - TAB]
        if n >= first_body_page and n not in opener_pages and not body_art and head_alone(body_text, heads):
            flags.append({"page": n, "code": "head_alone", "text": heads[0][:50]})
    codes = {}
    for f in flags:
        codes[f["code"]] = codes.get(f["code"], 0) + 1
    # Sparse pages by chapter (outline level 1): a review list for the white-space programme.
    chapters = [(page, title) for level, title, page in doc.get_toc(simple=True) if level == 1 and page > 0]
    def chapter_of(n):
        current = "front matter"
        for page, title in chapters:
            if page <= n:
                current = title
        return current
    sparse_pages = [d["page"] for d in diagnostics if d.get("sparse") and d["page"] not in opener_pages]
    by_chapter = {}
    for n in sparse_pages:
        by_chapter.setdefault(chapter_of(n), []).append(n)
    flow = layout_flow.analyse(doc, measures, first_body_page)
    flow.pop("rule_strikes")                         # already flagged above
    rep = {"pdf": a.pdf, "pages": len(doc), "counts": codes, "flagged_pages": sorted({f["page"] for f in flags}), "flags": flags[:400],
           "flow": flow, "flow_summary": layout_flow.summary({**flow, "rule_strikes": {}}),
           "sparse_pages": {"count": len(sparse_pages), "pages": sparse_pages, "by_chapter": by_chapter,
                            "method": "vertical fill under 55% and fewer than 50 text lines, chapter openers excluded; page-background furniture (thumb tab, opener frame) is not counted as content"},
           "density_triage": diagnostics,
           "density_method": "Diagnostic only: vertical union of text, raster and vector bounds clipped to body; bounding boxes overestimate occupied ink. Sparse pages, column imbalance and short paragraphs require visual inspection; deliberate starts, blank verso and artwork are not automatic failures."}
    doc.close()
    Path(a.report).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    print(json.dumps({"pages": rep["pages"], "counts": codes, "flagged_pages": rep["flagged_pages"][:60],
                      "sparse_pages": len(sparse_pages), "flow": rep["flow_summary"]}))


if __name__ == "__main__":
    main()
