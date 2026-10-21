#!/usr/bin/env python3
"""Corroborate Typst position queries against the serialized PDF's physical pages."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pymupdf
from pdf_positions import validate_sidecar

ROOT = Path(__file__).resolve().parents[1]
SELECTORS = ("<tblpos>", "<ixpos>", "<hpos>", "<um-pos>")


def normalized(title):
    return re.sub(r"\s+", " ", str(title)).strip().casefold()


def heading_positions(positions):
    rows = positions.get("<hpos>")
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], list):
        raise ValueError("Missing or malformed Typst heading-location query")
    if any(not isinstance(r, dict) or "id" not in r or "page" not in r for r in rows[0]):
        raise ValueError("Invalid heading-location record")
    return rows[0]


def analyze(pdf, headings, positions):
    """Compare unique source headings to physical PDF bookmark destinations.

    Ambiguous repeated titles are skipped, never arbitrarily assigned. Each
    position selector is additionally checked against the actual page count.
    """
    # PyMuPDF keeps a native handle open until the document is closed. On
    # Windows, that handle prevents temporary PDFs from being removed.
    with pymupdf.open(pdf) as doc:
        page_count = len(doc)
        if page_count < 1:
            raise ValueError("Empty publication PDF")
        toc = doc.get_toc(simple=True)
    hpos = heading_positions(positions)
    bad_bounds = []
    for selector in SELECTORS:
        records = hpos if selector == "<hpos>" else positions.get(selector)
        if not isinstance(records, list):
            raise ValueError("Missing or malformed Typst position query: " + selector)
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("page"), int) or not 1 <= record["page"] <= page_count:
                bad_bounds.append({"selector": selector,
                                   "id": record.get("id") if isinstance(record, dict) else None,
                                   "page": record.get("page") if isinstance(record, dict) else None})
    counts = Counter(normalized(h.get("title", "")) for h in headings)
    unique = {normalized(h["title"]): h["id"] for h in headings
              if isinstance(h, dict) and h.get("id") and h.get("title")
              and counts[normalized(h["title"])] == 1}
    qpos = {h["id"]: h["page"] for h in hpos}
    toc_counts = Counter(normalized(t[1]) for t in toc)
    matched, mismatches = [], []
    for _, title, actual_page in toc:
        key = normalized(title)
        if toc_counts[key] != 1 or key not in unique:
            continue
        hid = unique[key]
        if hid not in qpos:
            continue
        expected = qpos[hid]
        matched.append(hid)
        if expected != actual_page:
            mismatches.append({"id": hid, "title": title,
                               "query_page": expected, "pdf_bookmark_page": actual_page})
    coverage_floor = min(10, max(1, len(unique) // 10))
    good = not bad_bounds and not mismatches and len(matched) >= coverage_floor
    return {"status": "PASS" if good else "FAIL", "pdf_pages": page_count,
            "query_records": {key: len(hpos if key == "<hpos>" else positions[key])
                              for key in SELECTORS},
            "pdf_bookmarks": len(toc), "unique_source_headings": len(unique),
            "headings_corroborated": len(matched), "minimum_required": coverage_floor,
            "page_bounds_invalid": bad_bounds[:50],
            "bookmark_page_mismatches": mismatches[:100],
            "note": "Physical PDF bookmark destinations independently check unique heading pages; all query page numbers must also lie within the PDF."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--positions", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    pdf = Path(args.pdf)
    meta = json.loads((ROOT / "build/query.json").read_text())
    content = ROOT / "typst/content.typ"
    if meta.get("substrate") != "cream" or meta.get("edition") != "print":
        raise ValueError("Position query was not compiled as the cream print edition")
    if meta.get("pdf_sha256") != hashlib.sha256(pdf.read_bytes()).hexdigest():
        raise ValueError("Position query belongs to a different PDF; rebuild")
    if meta.get("content_sha256") != hashlib.sha256(content.read_bytes()).hexdigest():
        raise ValueError("Position query belongs to a different Typst source; rebuild")
    positions = json.loads(Path(args.positions).read_text())
    if positions != meta.get("positions"):
        raise ValueError("Position file differs from the compile-bound location query")
    binding = validate_sidecar(positions, pdf, root=ROOT)["binding"]
    headings = json.loads((ROOT / "production/inventory/headings.json").read_text())
    report = analyze(pdf, headings, positions)
    report["pdf_sha256"] = meta["pdf_sha256"]
    report["serialized_position_binding"] = binding
    Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("note", "pdf_sha256")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
