#!/usr/bin/env python3
"""Print the exact PDF-bound QA locations; never independently lay out the book.

The compile-time query is captured by tools/typst_run.py when it writes the cream
print PDF. Re-querying the same source in a new compiler can produce locations
that do not correspond to the serialized PDF.
"""
import hashlib
import json

from manuscript import ROOT, version

SELECTORS = ("<tblpos>", "<ixpos>", "<hpos>", "<um-pos>")


def compiled_positions(root=ROOT):
    path = root / "build/query.json"
    q = json.loads(path.read_text(encoding="utf-8"))
    pdf = root / "dist" / f"Heraldry_{version(root)}_inkjet-borderless.pdf"
    content = root / "typst/content.typ"
    if q.get("substrate") != "cream" or q.get("edition") != "print":
        raise ValueError("Positions are not from the compiled cream print edition")
    if q.get("content_sha256") != hashlib.sha256(content.read_bytes()).hexdigest():
        raise ValueError("Stale Typst source hash; rebuild")
    if q.get("pdf_sha256") != hashlib.sha256(pdf.read_bytes()).hexdigest():
        raise ValueError("Stale PDF hash; rebuild")
    positions = q.get("positions")
    if not isinstance(positions, dict) or any(not isinstance(positions.get(s), list) for s in SELECTORS):
        raise ValueError("Missing compile-bound position selectors; rebuild")
    return {s: positions[s] for s in SELECTORS}


if __name__ == "__main__":
    print(json.dumps(compiled_positions()))
