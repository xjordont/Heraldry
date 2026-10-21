#!/usr/bin/env python3
"""Supplementary file checks not covered by verify_inkjet_pdf.py:
substrate painted to every sheet edge, cream/white page-map and geometry identity,
raster inventory with effective ppi, internal link and bookmark resolution."""
import argparse, json
from pathlib import Path
import pymupdf
from pypdf import PdfReader

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


def _rect(rect):
    """Compare geometry, not substrate-dependent colour or PDF object numbers."""
    return tuple(round(float(v), 2) for v in rect)


def _geometry(value):
    """Preserve path/control-point/transform geometry, omitting colour only."""
    if isinstance(value, (tuple, list, pymupdf.Rect, pymupdf.Point, pymupdf.Quad, pymupdf.Matrix)):
        return tuple(_geometry(v) for v in value)
    if isinstance(value, float):
        return round(value, 3)
    return value


def _near(a, b, tolerance=0.02):
    if isinstance(a, (float, int)) and isinstance(b, (float, int)):
        return abs(a - b) <= tolerance
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(_near(x, y, tolerance) for x, y in zip(a, b))
    return a == b


def _link_signature(link):
    dest = link.get("to")
    if dest is None:
        target = None
    elif hasattr(dest, "x"):
        target = (round(float(dest.x), 2), round(float(dest.y), 2))
    else:
        target = str(dest)
    return (link.get("kind"), link.get("page"), link.get("uri"),
            link.get("nameddest"), _rect(link["from"]), target)


def compare_geometry(cream_page, white_page):
    """Find content-position differences even when extracted page text is equal.

    Text words, raster placements, vector drawing geometry, and link targets
    must agree; colours are deliberately excluded because substrate changes.
    """
    def glyphs(page):
        return [(s["font"], s["size"], s.get("flags"), c["c"], tuple(c["origin"]), tuple(c["bbox"]))
                for b in page.get_text("rawdict")["blocks"] for l in b.get("lines", [])
                for s in l["spans"] for c in s["chars"]]
    text_ok = _near(glyphs(cream_page), glyphs(white_page))
    def images(page):
        return sorted([(tuple(i["bbox"]), tuple(i["transform"]), i["width"], i["height"], i.get("digest"))
                       for i in page.get_image_info(hashes=True, xrefs=False)], key=str)
    raster_ok = _near(images(cream_page), images(white_page))
    def strokes(page):
        return sorted([(d["type"], _geometry(d["rect"]), _geometry(d["items"]),
                        d.get("width"), d.get("dashes"), _geometry(d.get("lineCap")),
                        d.get("lineJoin"), d.get("closePath"), d.get("even_odd"))
                       for d in page.get_drawings()], key=str)
    vector_ok = _near(strokes(cream_page), strokes(white_page))
    cl = sorted((_link_signature(l) for l in cream_page.get_links()), key=str)
    wl = sorted((_link_signature(l) for l in white_page.get_links()), key=str)
    links_ok = _near(cl, wl)
    return {"text": text_ok, "raster": raster_ok, "vector": vector_ok, "links": links_ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cream", required=True)
    ap.add_argument("--white", required=True)
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    # Explicit closure is required on Windows, where native PDF handles lock files.
    with pymupdf.open(a.cream) as c, pymupdf.open(a.white) as w:
        res = {"pages": {"cream": len(c), "white": len(w)}}
        res["substrate_edges"] = {"cream": edge_check(c, SUB["cream"]), "white": edge_check(w, SUB["white"])}
        differences = {"page_text": [], "text_geometry": [], "raster_geometry": [],
                       "vector_geometry": [], "navigation_geometry": []}
        res["toc_identical"] = c.get_toc(simple=True) == w.get_toc(simple=True)
        if len(c) == len(w):
            for i in range(len(c)):
                if c[i].get_text("text") != w[i].get_text("text"):
                    differences["page_text"].append(i + 1)
                geometry = compare_geometry(c[i], w[i])
                for key, field in (("text", "text_geometry"), ("raster", "raster_geometry"),
                                   ("vector", "vector_geometry"), ("links", "navigation_geometry")):
                    if not geometry[key]:
                        differences[field].append(i + 1)
        res["page_map_identical"] = len(c) == len(w) and not differences["page_text"]
        res["page_text_differences"] = differences["page_text"][:20]
        res["geometry_identical"] = len(c) == len(w) and res["toc_identical"] and all(
            not vals for key, vals in differences.items() if key != "page_text"
        )
        res["geometry_differences"] = {key: vals[:20] for key, vals in differences.items() if key != "page_text"}
        res["links"] = {"cream": links_check(c), "white": links_check(w)}
        res["rasters"] = rasters(c)
        # Parse /PageLabels with pypdf. Older PyMuPDF releases can misread the
        # catalog entry and report spurious label differences.
        labels = PdfReader(a.cream).page_labels
        res["page_labels_sample"] = [labels[i] for i in (0, len(c) // 2, len(c) - 1)]
        res["geometry_tolerance_pt"] = 0.02
        res["geometry_method"] = "glyph/font/origin/bbox; raster bytes/transform; vector paths/strokes; links; colours excluded"
    ok = (not res["substrate_edges"]["cream"] and not res["substrate_edges"]["white"]
          and res["page_map_identical"] and res["geometry_identical"]
          and res["links"]["cream"]["unresolved_links"] == 0 and res["links"]["white"]["unresolved_links"] == 0
          and res["links"]["cream"]["bookmarks_bad_target"] == 0 and res["links"]["white"]["bookmarks_bad_target"] == 0
          and all(r["effective_ppi"] >= 300 for r in res["rasters"]))
    res["status"] = "PASS" if ok else "FAIL"
    Path(a.report).write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("status", "pages", "page_map_identical", "geometry_identical")}
                     | {"edges_bad": [len(res["substrate_edges"]["cream"]), len(res["substrate_edges"]["white"])],
                        "links": res["links"]["cream"], "rasters": len(res["rasters"])}))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
