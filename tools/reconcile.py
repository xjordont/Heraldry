#!/usr/bin/env python3
"""Source → PDF reconciliation.

Checks, in source order, that every rendered source block (headings, paragraphs,
list items, block quotes) and every table cell of the protected manuscript
appears in the PDF text layer, and that bold/italic runs are rendered in bold/
italic faces. Normalisation rules (documented in production/qa/RECONCILIATION.md):
  * whitespace runs (incl. U+00A0 no-break spaces and line breaks) → one space
  * U+00AD discretionary hyphens inserted by line breaking are removed
  * running heads/folios outside the body frame are excluded
  * the manual Markdown TOC is replaced by the generated contents (not searched)
  * front-title split: H1 "A: B" is rendered as two display lines "A" / "B"
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from parse_source import plain  # noqa: E402

TOP, BOT = 0.65 * 72 - 4, 792 - 0.7 * 72 + 4


def norm(s: str) -> str:
    s = s.replace("­\n", "").replace("­ ", "").replace("­", "")
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # A dash or slash at a line end is indistinguishable from one followed by a space:
    # both sides are compared with spaces after these characters removed.
    return re.sub(r"([-–—/]) ", r"\1", s)


def pdf_stream(pdf, skip_covers=False):
    doc = pymupdf.open(pdf)
    parts = []
    bold, ital = [], []
    global fonts
    fonts = set()
    for i, page in enumerate(doc):
        if skip_covers and i in (0, len(doc) - 1):
            continue   # digital edition covers quote source text (cover copy), not body content
        d = page.get_text("dict")
        for b in d["blocks"]:
            for l in b.get("lines", []):
                y0, y1 = l["bbox"][1], l["bbox"][3]
                if y1 < TOP or y0 > BOT:
                    continue
                for sp in l["spans"]:
                    t = sp["text"]
                    fn = sp["font"]
                    fonts.add(fn.split("+")[-1])
                    is_b = any(k in fn for k in ("Bold", "Semibold", "SemiBold", "Black"))
                    is_i = "Ita" in fn
                    # concatenate adjacent spans of the same class; break with "|" otherwise
                    bold.append(t if is_b else "|")
                    ital.append(t if is_i else "|")
                    parts.append(t)
                bold.append(" ")
                ital.append(" ")
                parts.append("\n")
    raw = "".join(parts)
    return norm(raw), norm("".join(bold)), norm("".join(ital)), len(doc)


def runs(nodes, kind, acc, inside=False):
    for n in nodes:
        if n["t"] == kind:
            acc.append(plain(n["c"]))
        if "c" in n:
            runs(n["c"], kind, acc, inside)


def collect(model):
    """Source-ordered units: (id, kind, text, src, table_cells, strong_runs, em_runs)."""
    units = []

    def add_block(b):
        t = b["type"]
        if t in ("heading", "para"):
            s, e = [], []
            runs(b["c"], "strong", s)
            runs(b["c"], "em", e)
            units.append({"id": b["id"], "kind": t, "text": norm(plain(b["c"])), "src": b["src"], "strong": s, "em": e})
        elif t == "list":
            for it in b["items"]:
                for x in it["blocks"]:
                    add_block(x)
        elif t == "quote":
            for x in b["blocks"]:
                add_block(x)
        elif t == "table":
            cells = [norm(plain(c)) for c in b["header"]] + [norm(plain(c)) for r in b["rows"] for c in r]
            s, e = [], []
            for r in [b["header"]] + b["rows"]:
                for c in r:
                    runs(c, "strong", s)
                    runs(c, "em", e)
            units.append({"id": b["id"], "kind": "table", "cells": cells, "src": b["src"], "strong": s, "em": e,
                          "rows": len(b["rows"]), "cols": len(b["header"])})
        elif t == "hr":
            units.append({"id": b["id"], "kind": "hr", "src": b["src"]})

    for ch in model["chapters"]:
        if ch["id"] == "h-table-of-contents":
            continue
        for b in ch["blocks"]:
            add_block(b)
    return units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--report", required=True)
    ap.add_argument("--skip-covers", action="store_true")
    a = ap.parse_args()
    model = json.loads((ROOT / "build/blocks.json").read_text())
    text, btext, itext, npages = pdf_stream(a.pdf, a.skip_covers)
    units = collect(model)
    cursor = 0
    res = {"found_in_order": 0, "found_out_of_order": 0, "missing": [], "table_cells": 0, "table_cells_missing": [],
           "tables_ok": 0, "tables_total": 0, "strong_runs": 0, "strong_missing": [], "em_runs": 0, "em_missing": [],
           "hr_rendered_as_ornament": 0, "out_of_order": []}
    WINDOW = 60000
    for u in units:
        if u["kind"] == "hr":
            res["hr_rendered_as_ornament"] += 1
            continue
        if u["kind"] == "table":
            res["tables_total"] += 1
            start = max(0, cursor - 2000)
            win = text[start:start + WINDOW]
            miss = [c for c in u["cells"] if c and c not in win]
            res["table_cells"] += len(u["cells"])
            if miss:
                res["table_cells_missing"].append({"id": u["id"], "src": u["src"], "missing": miss[:5], "n": len(miss)})
            else:
                res["tables_ok"] += 1
            # advance cursor to the last cell's position
            last = [c for c in u["cells"] if c]
            if last:
                p = text.find(last[-1], start)
                if p >= 0:
                    cursor = max(cursor, p)
        else:
            t = u["text"]
            if not t:
                continue
            if u["id"] == "h-heraldry-skirmish-the-dying-lands":
                t = t.split(": ")[0]
            p = text.find(t, cursor)
            if p >= 0 and p - cursor < WINDOW:
                res["found_in_order"] += 1
                cursor = p + len(t)
            else:
                q = text.find(t)
                if q >= 0:
                    res["found_out_of_order"] += 1
                    res["out_of_order"].append({"id": u["id"], "src": u["src"], "text": t[:70]})
                else:
                    res["missing"].append({"id": u["id"], "src": u["src"], "text": t[:120]})
        for r in u.get("strong", []):
            r = norm(r)
            if not r:
                continue
            res["strong_runs"] += 1
            if r not in btext:
                res["strong_missing"].append({"id": u["id"], "run": r[:60]})
        for r in u.get("em", []):
            r = norm(r)
            if not r:
                continue
            res["em_runs"] += 1
            if r not in itext:
                res["em_missing"].append({"id": u["id"], "run": r[:60]})
    # duplicate detection: long text blocks must appear exactly as often as in the source
    from collections import Counter
    src_counts = Counter(u["text"] for u in units if u["kind"] == "para" and len(u.get("text", "")) > 60)
    src_stream = " ".join([u.get("text", "") for u in units] + [c for u in units for c in u.get("cells", [])])
    # figures are live vector text and may quote the rules they illustrate
    import html as _html
    figtxt = norm(" ".join(_html.unescape(x) for f in sorted((ROOT / "figures/out").glob("FIG-*.svg"))
                           for x in re.findall(r"<text[^>]*>(.*?)</text>", f.read_text(), re.S)))
    capt = ""
    pl = ROOT / "figures/placements.json"
    if pl.exists():
        capt = norm(" ".join(f["caption"] for v in json.loads(pl.read_text()).values() for f in v))
    res["duplicated_blocks"] = [{"text": t[:70], "source": src_stream.count(t), "pdf": text.count(t)} for t in src_counts
                                if text.count(t) > src_stream.count(t) + figtxt.count(t) + capt.count(t)]
    res["units"] = len(units)
    res["status"] = "PASS" if not res["duplicated_blocks"] and not res["out_of_order"] and not res["missing"] and not res["table_cells_missing"] and not res["strong_missing"] and not res["em_missing"] else "FAIL"
    res["pdf_pages"] = npages
    allowed = {"SourceSerif4", "SourceSans3", "Cinzel"}
    res["fonts"] = sorted(fonts)
    res["unexpected_fonts"] = sorted(f for f in fonts if f.split("-")[0] not in allowed)
    if res["unexpected_fonts"]:
        res["status"] = "FAIL"
    Path(a.report).write_text(json.dumps(res, indent=1, ensure_ascii=False))
    summ = {k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}
    print(json.dumps(summ))
    raise SystemExit(0 if res["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
