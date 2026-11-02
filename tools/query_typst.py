#!/usr/bin/env python3
"""Print the exact PDF-bound QA locations; never independently lay out the book.

Positions are serialized inside the PDF export, then captured by typst_run.py.
Calling Compiler.query also recompiles, even on the same compiler instance.
"""
import hashlib
import json

from manuscript import ROOT, version
from pdf_positions import validate_sidecar

SELECTORS = ("<tblpos>", "<ixpos>", "<hpos>", "<um-pos>")


def compiled_positions(root=ROOT):
    path = root / "build/query.json"
    q = json.loads(path.read_text(encoding="utf-8"))
    pdf = root / "build/book-cream.pdf"
    content = root / "typst/content.typ"
    if q.get("substrate") != "cream" or q.get("edition") != "interior":
        raise ValueError("Positions are not from the compiled interior")
    if q.get("content_sha256") != hashlib.sha256(content.read_bytes()).hexdigest():
        raise ValueError("Stale Typst source hash; rebuild")
    if q.get("pdf_sha256") != hashlib.sha256(pdf.read_bytes()).hexdigest():
        raise ValueError("Stale PDF hash; rebuild")
    positions = q.get("positions")
    if not isinstance(positions, dict) or any(not isinstance(positions.get(s), list) for s in SELECTORS):
        raise ValueError("Missing compile-bound position selectors; rebuild")
    try:
        return validate_sidecar(positions, pdf, root=root)
    except Exception as exc:
        raise ValueError("Missing or stale serialized PDF position evidence: " + str(exc)) from exc


if __name__ == "__main__":
    print(json.dumps(compiled_positions()))
