#!/usr/bin/env python3
"""Supplementary file checks not covered by verify_inkjet_pdf.py:
substrate painted to every sheet edge, cream/white page-map identity,
raster inventory with effective ppi, internal link and bookmark resolution."""
import argparse, json
from pathlib import Path
import pymupdf

SUB = {"cream": (0xFC, 0xFA, 0xF5), "white": (0xFF, 0xFF, 0xFF)}


def edge_check(doc, rgb):
    bad = []
    for i, p in enumerate(doc):
        pix = p.get_pixmap(matrix=pymupdf.Matrix(12 / 72, 12 / 72), alpha=False)
        w, h = pix.width, pix.height
        pts = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
        off = [pt for pt in pts if max(abs(a - b) for a, b in zip(pix.pixel(*pt), rgb)) > 3]
        if len(off) > 0.02 * len(pts):
            bad.append({"page": i + 1, "off_edge_pixels": len(off)})
    return bad


def links_check(doc):
    n_links = n_bad = 0
    bad = []
    for i, p in enumerate(doc):
        for l in p.get_links():
            if l["kind"] in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED):
                n_links += 1
                tgt = l.get("page", -1)
                if tgt is None or tgt < 0 or tgt >= len(doc):
                    n_bad += 1
                    bad.append({"page": i + 1, "link": str(l)[:120]})
    toc = doc.get_toc(simple=True)
    bad_toc = [t for t in toc if not (1 <= t[2] <= len(doc))]
    levels = {}
    for t in toc:
        levels[t[0]] = levels.get(t[0], 0) + 1
    return {"internal_links": n_links, "unresolved_links": n_bad, "examples": bad[:10],
            "bookmarks": len(toc), "bookmark_levels": levels, "bookmarks_bad_target": len(bad_toc)}


def rasters(doc):
    out = []
    for i, p in enumerate(doc):
        for img in p.get_images(full=True):
            xref = img[0]
            for r in p.get_image_rects(xref):
                ppi = min(img[2] / (r.width / 72), img[3] / (r.height / 72)) if r.width and r.height else 0
                out.append({"page": i + 1, "xref": xref, "px": [img[2], img[3]], "placed_in": [round(r.width / 72, 2), round(r.height / 72, 2)], "effective_ppi": round(ppi)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cream", required=True)
    ap.add_argument("--white", required=True)
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    c, w = pymupdf.open(a.cream), pymupdf.open(a.white)
    res = {"pages": {"cream": len(c), "white": len(w)}}
    res["substrate_edges"] = {"cream": edge_check(c, SUB["cream"]), "white": edge_check(w, SUB["white"])}
    diffs = []
    if len(c) == len(w):
        for i in range(len(c)):
            if c[i].get_text("text") != w[i].get_text("text"):
                diffs.append(i + 1)
    res["page_map_identical"] = len(c) == len(w) and not diffs
    res["page_text_differences"] = diffs[:20]
    res["links"] = {"cream": links_check(c), "white": links_check(w)}
    res["rasters"] = rasters(c)
    res["page_labels_sample"] = [c[i].get_label() for i in (0, len(c) // 2, len(c) - 1)]
    ok = (not res["substrate_edges"]["cream"] and not res["substrate_edges"]["white"] and res["page_map_identical"]
          and res["links"]["cream"]["unresolved_links"] == 0 and res["links"]["white"]["unresolved_links"] == 0
          and res["links"]["cream"]["bookmarks_bad_target"] == 0 and res["links"]["white"]["bookmarks_bad_target"] == 0
          and all(r["effective_ppi"] >= 300 for r in res["rasters"]))
    res["status"] = "PASS" if ok else "FAIL"
    Path(a.report).write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("status", "pages", "page_map_identical")} | {"edges_bad": [len(res["substrate_edges"]["cream"]), len(res["substrate_edges"]["white"])], "links": res["links"]["cream"], "rasters": len(res["rasters"])}))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
