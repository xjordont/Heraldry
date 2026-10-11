#!/usr/bin/env python3
"""Geometry detectors for every page: text overlap, text outside the body frame
(other than running furniture), unsafe edges, tiny type, near-empty pages.
Detectors flag pages for visual review; they do not prove good layout."""
import argparse, json
from pathlib import Path
import pymupdf

W, H = 612, 792
SAFE = 27
TOP, BOT = 0.65 * 72, 792 - 0.7 * 72


def lines_of(page, fonts=False):
    out = []
    d = page.get_text("dict")
    for b in d["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"]).strip()
            if not txt:
                continue
            size = max(s["size"] for s in l["spans"])
            out.append((pymupdf.Rect(l["bbox"]), txt, size) + ((l["spans"][0]["font"],) if fonts else ()))
    return out


def stranded_headings(page):
    """Heading-styled line in the last 60 pt of a column with < 2 lines after it in that column."""
    ls = lines_of(page, fonts=True)
    hits = []
    for r, t, sz, f in ls:
        is_head = ("Cinzel" in f and sz > 12) or ("Serif4-Semibold" in f and sz > 12) or ("Serif4-Bold" in f and sz > 10.8)
        if is_head and r.y1 > BOT - 60 and r.y0 > 200:
            below = [x for x in ls if x[0].y0 > r.y1 and abs(x[0].x0 - r.x0) < 60]
            if len(below) < 2:
                hits.append(t[:50])
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--report", required=True)
    ap.add_argument("--first-body-page", type=int, default=1)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    flags = []
    for i, page in enumerate(doc):
        n = i + 1
        ls = lines_of(page)
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
            if min(r.x0, r.y0, W - r.x1, H - r.y1) < SAFE - 0.1:
                flags.append({"page": n, "code": "unsafe_edge", "text": t[:50]})
            if s < 8.9:
                flags.append({"page": n, "code": "small_type", "size": round(s, 2), "text": t[:50]})
            furniture = s <= 9.6 and (r.y1 < TOP or r.y0 > BOT - 2)
            if not furniture and (r.y1 > BOT + 2 or r.y0 < TOP - 14):
                flags.append({"page": n, "code": "outside_body_frame", "text": t[:50], "bbox": [round(v) for v in r]})
        for t in stranded_headings(page):
            flags.append({"page": n, "code": "stranded_heading", "text": t})
        body = [r for r, t, s in ls if TOP - 2 < r.y0 and r.y1 < BOT + 2]
        if n >= a.first_body_page and len(body) < 6 and not page.get_images() and not page.get_drawings():
            flags.append({"page": n, "code": "near_empty", "lines": len(body)})
    codes = {}
    for f in flags:
        codes[f["code"]] = codes.get(f["code"], 0) + 1
    rep = {"pdf": a.pdf, "pages": len(doc), "counts": codes, "flagged_pages": sorted({f["page"] for f in flags}), "flags": flags[:400]}
    Path(a.report).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    print(json.dumps({"pages": len(doc), "counts": codes, "flagged_pages": rep["flagged_pages"][:60]}))


if __name__ == "__main__":
    main()
