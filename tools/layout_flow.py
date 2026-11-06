#!/usr/bin/env python3
"""Column-flow measures for every page (rulebook-layout review, 2026-11-06).

Advisory except for one defect. A column left more than FOOT_GAP_PT short is classified by what follows it,
so reviewers and layout trials can tell apart:
  - section_end: the next page opens a heading at its top (the owner's fresh-page rule, DESIGN 13 rule 8);
  - keep_gap: the next page opens with a figure, table, or art kept whole;
  - interior: the text simply continues overleaf (DESIGN 8.5: an unexplained interior void needs repair).
It also lists low right-column section starts that turn the page, uneven chapter last pages, and chapter
spans. The defect, a horizontal rule drawn through a line of text, is returned for layout_qa to flag.

    python tools/layout_flow.py BASE.pdf [TRIAL.pdf]    # summary, or the change from BASE to TRIAL
"""
import argparse, json, statistics
import pymupdf
from layout_profile import PAGE_WIDTH_PT, PAGE_HEIGHT_PT, MARGIN_TOP_PT, MARGIN_BOTTOM_PT, MARGIN_OUTSIDE_PT, TOKENS

W, H = PAGE_WIDTH_PT, PAGE_HEIGHT_PT
TOP, BOT = MARGIN_TOP_PT, H - MARGIN_BOTTOM_PT
TAB = MARGIN_OUTSIDE_PT + TOKENS["ornament"].get("tab_halo_pt", 0)
MID = W / 2
FOOT_GAP_PT = 60            # bare column foot worth a look (the skill's 46-60 pt)
LOW_START_PT = 230          # a right-column section start this close to the foot that turns the page
UNEVEN_LAST_PT = 24         # chapter last page: column feet further apart than this


def body_boxes(page, text_dict=None, drawings=None):
    """Text lines, images, and drawings inside the body frame, as (rect, kind). Running furniture (the head,
    the folio, the thumb tab) lies outside it and is not counted."""
    out = []
    for block in (text_dict if text_dict is not None else page.get_text("dict"))["blocks"]:
        for line in block.get("lines", []):
            if abs(line["dir"][0]) < 0.5 or not "".join(s["text"] for s in line["spans"]).strip():
                continue
            r = pymupdf.Rect(line["bbox"])
            if r.y0 >= TOP - 2 and r.y1 <= BOT + 2 and r.x1 > TAB and r.x0 < W - TAB:
                out.append((r, "text"))
    for image in page.get_image_info():
        r = pymupdf.Rect(image["bbox"])
        if r.y1 > TOP and r.y0 < BOT and r.x1 > TAB and r.x0 < W - TAB and r.height > 8:
            out.append((r & pymupdf.Rect(0, TOP, W, BOT), "image"))
    for drawing in (drawings if drawings is not None else page.get_drawings()):
        r = drawing["rect"]
        if r.y0 >= TOP and r.y1 <= BOT and r.x0 > TAB - 4 and r.x1 < W - TAB + 4 and r.width > 4:
            out.append((pymupdf.Rect(r), "drawing"))
    return out


def column_feet(boxes):
    """Lowest content in each column; an element across the gutter counts for both."""
    feet = {"left": None, "right": None}
    for r, _ in boxes:
        for side, inside in (("left", r.x0 < MID - 4), ("right", r.x1 > MID + 4)):
            if inside:
                feet[side] = r.y1 if feet[side] is None else max(feet[side], r.y1)
    return feet


def rule_strikes(text_dict, drawings):
    """Page-composition rules (hairlines up to 0.8 pt, over 150 pt long: band rules, separators, table rules)
    through the core of a text line. Figures draw heavier strokes and label their own lines by design
    (FIG-11, FIG-18, the Chapter 11 cycle), so they are not tested."""
    rules = [d["rect"] for d in drawings if d["rect"].height < 1.5 and d["rect"].width > 150
             and (d.get("width") or 0) <= 0.8 and TOP < d["rect"].y0 < BOT]
    hits = []
    for block in text_dict["blocks"]:
        for line in block.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"]).strip()
            if not txt or abs(line["dir"][0]) < 0.5:
                continue
            x0, y0, x1, y1 = line["bbox"]
            core = (y0 + 0.3 * (y1 - y0), y1 - 0.3 * (y1 - y0))
            for r in rules:
                if core[0] < (r.y0 + r.y1) / 2 < core[1] and min(x1, r.x1) - max(x0, r.x0) > 10:
                    hits.append({"text": txt[:50], "rule_y": round(r.y0, 1)})
                    break
    return hits


def opens_with_kept_block(boxes):
    """The page's first body element is a figure, table band, or art (a whole unit kept for this page)."""
    if not boxes:
        return False
    first = min(boxes, key=lambda b: b[0].y0)
    top_band = [b for b in boxes if b[0].y0 < first[0].y0 + 30]
    return any(kind != "text" and b.width > 120 for b, kind in top_band)


def classify(page_no, heads_at_top, kept_next, chapter_last):
    """Geometry-only fallback, for a PDF without the build's embedded positions."""
    if chapter_last or (page_no + 1) in heads_at_top:
        return "section_end"
    return "keep_gap" if kept_next else "interior"


def column_starts(doc):
    """What the build placed at the top of each column, from the positions it embeds in the PDF:
    {(page, side): kind}. "section" is a numbered section (level 2 or above), a fresh start; "heading",
    "figure", "table", or "piece" was carried whole to that column. None without the record."""
    try:
        record = json.loads(doc.embfile_get("heraldry-positions.json"))["positions"]
    except Exception:
        return None
    rank = {"section": 0, "heading": 1, "figure": 2, "table": 3, "piece": 4}
    starts = {}
    def mark(page, x, y, kind):
        if y < TOP + 40:
            key = (page, "left" if x < MID else "right")
            if rank[kind] < rank.get(starts.get(key), 9):
                starts[key] = kind
    for h in (record.get("<hpos>") or [[]])[0]:
        mark(h["page"], h.get("x", 0), h["y"], "section" if h.get("level", 9) <= 2 else "heading")
    for t in record.get("<tblpos>", []):
        if t.get("edge") == "s":
            mark(t["page"], t.get("x", 0), t["y"], "figure" if str(t.get("id", "")).startswith("FIG") else "table")
    for m in record.get("<pm>", []):
        if m.get("edge") == "s":
            mark(m["page"], m.get("x", 0), m["y"], "piece")
    return starts


def classify_by_record(page_no, side, starts, chapter_last):
    """(class, what was carried). A short left column ends at what tops the right column; a short right
    column at what tops the next page."""
    if chapter_last:
        return "section_end", None
    following = [(page_no, "right"), (page_no + 1, "left")] if side == "left" else [(page_no + 1, "left")]
    for key in following:
        if key in starts:
            return ("section_end", None) if starts[key] == "section" else ("keep_gap", starts[key])
    return "interior", None


def page_measures(page, text_dict=None, drawings=None):
    """One page's column feet, whether it opens with a kept block, and any rule through text. A caller that
    has already extracted the page's text and drawings passes them in."""
    text_dict = text_dict if text_dict is not None else page.get_text("dict")
    drawings = drawings if drawings is not None else page.get_drawings()
    boxes = body_boxes(page, text_dict, drawings)
    return {"feet": column_feet(boxes), "kept": opens_with_kept_block(boxes), "strikes": rule_strikes(text_dict, drawings)}


def analyse(doc, measures=None, first_body_page=None):
    """measures: optional {page_no: page_measures(...)} gathered by the caller."""
    toc = doc.get_toc(simple=False)
    chapters = [t[2] for t in toc if t[0] == 1 and t[2] > 0]
    first = first_body_page or min(chapters, default=1)
    heads_at_top = {t[2] for t in toc if t[0] <= 3 and t[3].get("to") is not None and t[3]["to"].y < TOP + 40}
    chapter_last = {p - 1 for p in chapters[1:]} | {len(doc)}
    measures = measures or {i + 1: page_measures(page) for i, page in enumerate(doc)}
    feet = {n: m["feet"] for n, m in measures.items()}
    kept = {n: m["kept"] for n, m in measures.items()}
    strikes = {n: m["strikes"] for n, m in measures.items() if m["strikes"]}
    starts = column_starts(doc)
    short = []
    for n in range(first, len(doc) + 1):
        if n in chapters:
            continue                               # an opener's frame and lead are composed, not flowed
        for side in ("left", "right"):
            y = feet[n][side]
            if y is None:
                continue
            gap = BOT - y
            if gap > FOOT_GAP_PT:
                cls, carried = (classify_by_record(n, side, starts, n in chapter_last) if starts is not None
                                else (classify(n, heads_at_top, kept.get(n + 1, False), n in chapter_last), None))
                short.append({"page": n, "column": side, "bare_pt": round(gap), "class": cls, "carried": carried})
    low = []
    for k, t in enumerate(toc):
        if t[0] not in (2, 3) or t[3].get("to") is None:
            continue
        to, page = t[3]["to"], t[2]
        nxt = next((u for u in toc[k + 1:] if u[0] <= t[0]), None)
        if to.x > MID and BOT - to.y < LOW_START_PT and nxt is not None and nxt[2] > page:
            low.append({"page": page, "heading": t[1][:60], "from_foot_pt": round(BOT - to.y)})
    uneven = []
    for n in sorted(chapter_last):
        f = feet.get(n, {})
        if f.get("left") and f.get("right") and abs(f["left"] - f["right"]) > UNEVEN_LAST_PT:
            uneven.append({"page": n, "difference_pt": round(abs(f["left"] - f["right"]))})
    spans = []
    for k, start in enumerate(chapters):
        end = (chapters[k + 1] - 1) if k + 1 < len(chapters) else len(doc)
        title = next(t[1] for t in toc if t[0] == 1 and t[2] == start)
        spans.append({"chapter": title[:50], "first": start, "last": end, "pages": end - start + 1})
    by_class, by_carried = {}, {}
    for s in short:
        for table, key in ((by_class, s["class"]), (by_carried, s["carried"])):
            if key is None:
                continue
            c = table.setdefault(key, {"columns": 0, "bare_pt": 0})
            c["columns"] += 1
            c["bare_pt"] += s["bare_pt"]
    return {"pages": len(doc), "short_columns": by_class, "keep_gaps_by_carried": by_carried,
            "interior_pages": sorted({s["page"] for s in short if s["class"] == "interior"}),
            "keep_gap_pages": sorted({s["page"] for s in short if s["class"] == "keep_gap"}),
            "low_right_starts": low, "uneven_chapter_ends": uneven, "chapter_spans": spans,
            "rule_strikes": strikes, "short_detail": short,
            "method": f"column foot more than {FOOT_GAP_PT} pt above the frame foot; classified by what tops the next "
                      "column (a numbered section: section_end; a heading, figure, table, or flow piece carried whole: "
                      "keep_gap; nothing: interior), from the build's embedded positions where present",
            "classified_from": "embedded positions" if starts is not None else "page geometry"}


def summary(rep):
    sc = rep["short_columns"]
    return {"pages": rep["pages"],
            **{f"{c}_columns": sc.get(c, {}).get("columns", 0) for c in ("interior", "keep_gap", "section_end")},
            **{f"{c}_bare_pt": sc.get(c, {}).get("bare_pt", 0) for c in ("interior", "keep_gap", "section_end")},
            **{f"keep_gap_{k}_pt": rep.get("keep_gaps_by_carried", {}).get(k, {}).get("bare_pt", 0)
               for k in ("figure", "table", "heading", "piece")},
            "low_right_starts": len(rep["low_right_starts"]), "uneven_chapter_ends": len(rep["uneven_chapter_ends"]),
            "rule_strikes": sum(len(v) for v in rep["rule_strikes"].values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("base")
    ap.add_argument("trial", nargs="?")
    ap.add_argument("--json", help="write the full report (of TRIAL if given, else BASE) here")
    a = ap.parse_args()
    reps = [analyse(pymupdf.open(p)) for p in [a.base] + ([a.trial] if a.trial else [])]
    sums = [summary(r) for r in reps]
    if a.json:
        open(a.json, "w").write(json.dumps(reps[-1], indent=1, ensure_ascii=False, default=str))
    if len(reps) == 1:
        print(json.dumps(sums[0], indent=1))
        return
    print(f"{'measure':28} {'base':>9} {'trial':>9} {'change':>9}")
    for k in sums[0]:
        print(f"{k:28} {sums[0][k]:>9} {sums[1][k]:>9} {sums[1][k] - sums[0][k]:>+9}")
    a_sp = {s["chapter"]: s["pages"] for s in reps[0]["chapter_spans"]}
    for s in reps[1]["chapter_spans"]:
        if a_sp.get(s["chapter"]) != s["pages"]:
            print(f"  chapter {s['chapter']!r}: {a_sp.get(s['chapter'])} -> {s['pages']} pages")


if __name__ == "__main__":
    main()
