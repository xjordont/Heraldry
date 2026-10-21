#!/usr/bin/env python3
"""Measure units once; consume the data serialized by that warning-aware compile."""
import hashlib
import io
import json
import math
import re
import time
from collections import Counter
from pathlib import Path

import pypdf
import typst

from manuscript import pdf_epoch
from pdf_positions import compilation_identity

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = "heraldry-unit-measurements.json"


def expected_unit_ids(source):
    # These are generated #munit calls, not a parser for arbitrary manuscript
    # prose. Full independent source-unit coverage is enforced by keep_audit.
    return [json.loads(m) for m in re.findall(r'#munit\(("(?:[^"\\]|\\.)*")', source)]


def measurement_rows(pdf, expected):
    reader = pypdf.PdfReader(io.BytesIO(pdf))
    attachments = list(reader.attachments.get(ATTACHMENT, []))
    if len(attachments) != 1:
        raise ValueError("Measurement compile must serialize exactly one unit-measurement attachment")
    rows = json.loads(attachments[0])
    if not isinstance(rows, list) or not rows:
        raise ValueError("Empty or malformed serialized unit measurements")
    if any(not isinstance(r, dict) or not isinstance(r.get("id"), str) for r in rows):
        raise ValueError("Malformed serialized unit ID")
    got, wanted = Counter(r["id"] for r in rows), Counter(expected)
    if not wanted or got != wanted or any(n != 1 for n in got.values()):
        raise ValueError("Missing, duplicate or unexpected serialized unit measurements")
    output = {}
    for row in rows:
        if any(type(row.get(k)) not in (float, int) or not math.isfinite(row[k]) or row[k] < 0 for k in ("h1", "h2")):
            raise ValueError("Invalid measured height: " + row["id"])
        output[row["id"]] = {"h1": round(row["h1"], 1), "h2": round(row["h2"], 1)}
    return output


def measure(source, root=ROOT):
    source, root = Path(source), Path(root)
    expected = expected_unit_ids(source.read_text(encoding="utf-8"))
    identity = compilation_identity(root, "cream", "print", source)
    compiler = typst.Compiler(str(source), root=str(root), font_paths=[str(root / "fonts/static")],
                              ignore_system_fonts=True, sys_inputs={"substrate": "cream", "edition": "print", "index": "off"})
    start = time.monotonic()
    pdf, warnings = compiler.compile_with_warnings(timestamp=pdf_epoch(root))
    elapsed = time.monotonic() - start
    diagnostics = [str(w) for w in warnings]
    if any(any(word in d.lower() for word in ("converg", "introspection", "stabiliz", "stabilis")) for d in diagnostics):
        raise ValueError("Unit measurement did not converge: " + "\n".join(diagnostics))
    if compilation_identity(root, "cream", "print", source) != identity:
        raise ValueError("Publication inputs changed during unit measurement; rerun")
    output = measurement_rows(pdf, expected)
    return output, {"origin": "measurement-pdf-attachment", "identity": identity,
                    "measurement_pdf_sha256": hashlib.sha256(pdf).hexdigest(),
                    "measurements_sha256": hashlib.sha256(json.dumps(output, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                    "units": len(output), "warnings": diagnostics, "seconds": round(elapsed, 3)}


def main():
    output = ROOT / "build/unit_measure.json"
    binding = ROOT / "build/unit_measure.binding.json"
    output.unlink(missing_ok=True)
    binding.unlink(missing_ok=True)
    rows, evidence = measure(ROOT / "typst/measure.typ")
    output.write_bytes(json.dumps(rows).encode("utf-8"))
    binding.write_bytes((json.dumps(evidence, indent=2) + "\n").encode("utf-8"))
    print(f"{len(rows)} units measured in {evidence['seconds']:.1f}s")


if __name__ == "__main__":
    main()
