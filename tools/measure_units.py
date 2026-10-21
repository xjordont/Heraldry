#!/usr/bin/env python3
"""Measure units once; consume the data serialized by that warning-aware compile."""
import argparse
import hashlib
import io
import json
import math
import re
import time
import tempfile
from collections import Counter
from pathlib import Path

import pypdf
import typst

from manuscript import pdf_epoch
from pdf_positions import compilation_identity

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = "heraldry-unit-measurements.json"
CACHE_SCHEMA = 1
CACHE_DIRECTORY = ".cache/layout-measurements"
# Include the export options in addition to compilation_identity. A cache entry
# can only stand in for this exact invocation, never for individual unit rows.
COMPILER_INPUTS = {"substrate": "cream", "edition": "print", "index": "off"}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def cache_key(source_bytes, identity, source_location):
    return hashlib.sha256(canonical({
        "schema": CACHE_SCHEMA,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "identity": identity,
        "source_location": source_location,
        "sys_inputs": COMPILER_INPUTS,
        "ignore_system_fonts": True,
        "font_paths": ["fonts/static"],
    })).hexdigest()


def load_cache(entry, key, identity, expected):
    """Read heights only from the hash-checked serialized PDF, never a row cache."""
    envelope = json.loads((entry / "evidence.json").read_bytes())
    if not isinstance(envelope, dict) or envelope.get("schema") != CACHE_SCHEMA or envelope.get("key") != key:
        raise ValueError("Invalid measurement cache envelope/key")
    evidence = envelope.get("evidence")
    if not isinstance(evidence, dict) or evidence.get("origin") != "measurement-pdf-attachment" or evidence.get("identity") != identity:
        raise ValueError("Measurement cache identity mismatch")
    if evidence.get("warnings") != []:
        raise ValueError("Warning-bearing measurement cache entry")
    elapsed = evidence.get("seconds")
    if type(elapsed) not in (float, int) or not math.isfinite(elapsed) or elapsed < 0:
        raise ValueError("Invalid measurement cache compile time")
    pdf = (entry / "measurement.pdf").read_bytes()
    if hashlib.sha256(pdf).hexdigest() != evidence.get("measurement_pdf_sha256"):
        raise ValueError("Measurement cache PDF SHA mismatch")
    rows = measurement_rows(pdf, expected)
    if hashlib.sha256(canonical(rows)).hexdigest() != evidence.get("measurements_sha256") or len(rows) != evidence.get("units"):
        raise ValueError("Measurement cache attachment differs from evidence")
    return rows, evidence


def save_cache(entry, key, pdf, evidence):
    """Publish the envelope last; interrupted or competing writes fail closed."""
    entry.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".write-", dir=entry.parent) as temporary:
        scratch = Path(temporary)
        (scratch / "measurement.pdf").write_bytes(pdf)
        (scratch / "evidence.json").write_bytes(canonical({
            "schema": CACHE_SCHEMA, "key": key, "evidence": evidence,
        }) + b"\n")
        entry.mkdir(exist_ok=True)
        (scratch / "measurement.pdf").replace(entry / "measurement.pdf")
        (scratch / "evidence.json").replace(entry / "evidence.json")


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


def measure(source, root=ROOT, *, use_cache=True):
    source, root = Path(source), Path(root)
    start = time.monotonic()
    source_bytes = source.read_bytes()
    expected = expected_unit_ids(source_bytes.decode("utf-8"))
    identity = compilation_identity(root, "cream", "print", source)
    try:
        source_location = source.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        source_location = source.resolve().as_posix()
    key = cache_key(source_bytes, identity, source_location)
    entry = root / CACHE_DIRECTORY / key
    cache = {"status": "miss" if use_cache else "bypass", "key": key,
             "path": entry.as_posix(), "reason": "entry absent" if use_cache else "disabled by caller",
             "stored": False}

    def require_current():
        if compilation_identity(root, "cream", "print", source) != identity or source.read_bytes() != source_bytes:
            raise ValueError("Publication inputs changed during unit measurement; rerun")

    if use_cache and entry.exists():
        try:
            output, evidence = load_cache(entry, key, identity, expected)
        except (OSError, ValueError, TypeError, KeyError, AttributeError, pypdf.errors.PyPdfError) as error:
            cache["reason"] = "rejected entry: " + str(error)
        else:
            require_current()
            cache.update(status="hit", reason="exact PDF and attachment validated")
            return output, evidence | {"cache": cache, "compile_seconds": 0.0,
                                       "cached_compile_seconds": evidence["seconds"],
                                       "seconds": round(time.monotonic() - start, 3)}

    compiler = typst.Compiler(str(source), root=str(root), font_paths=[str(root / "fonts/static")],
                              ignore_system_fonts=True, sys_inputs=COMPILER_INPUTS.copy())
    compile_start = time.monotonic()
    pdf, warnings = compiler.compile_with_warnings(timestamp=pdf_epoch(root))
    elapsed = time.monotonic() - compile_start
    diagnostics = [str(w) for w in warnings]
    if any(any(word in d.lower() for word in ("converg", "introspection", "stabiliz", "stabilis")) for d in diagnostics):
        raise ValueError("Unit measurement did not converge: " + "\n".join(diagnostics))
    require_current()
    output = measurement_rows(pdf, expected)
    evidence = {"origin": "measurement-pdf-attachment", "identity": identity,
                "measurement_pdf_sha256": hashlib.sha256(pdf).hexdigest(),
                "measurements_sha256": hashlib.sha256(canonical(output)).hexdigest(),
                "units": len(output), "warnings": diagnostics, "seconds": round(elapsed, 3)}
    # Existing warning handling remains authoritative. Only warning-free exports
    # are reusable; a failed or warning-bearing compile cannot populate a cache.
    if use_cache and not diagnostics:
        try:
            save_cache(entry, key, pdf, evidence)
        except OSError as error:
            cache["write_error"] = str(error)
        else:
            cache["stored"] = True
    elif diagnostics:
        cache["write_skipped"] = "compiler warnings"
    return output, evidence | {"cache": cache, "compile_seconds": round(elapsed, 3),
                               "seconds": round(time.monotonic() - start, 3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-cache", action="store_true", help="compile fresh without reading or writing the measurement cache")
    args = parser.parse_args()
    output = ROOT / "build/unit_measure.json"
    binding = ROOT / "build/unit_measure.binding.json"
    output.unlink(missing_ok=True)
    binding.unlink(missing_ok=True)
    rows, evidence = measure(ROOT / "typst/measure.typ", use_cache=not args.no_cache)
    output.write_bytes(json.dumps(rows).encode("utf-8"))
    binding.write_bytes((json.dumps(evidence, indent=2) + "\n").encode("utf-8"))
    print(f"{len(rows)} units measured in {evidence['seconds']:.1f}s "
          f"(cache {evidence['cache']['status']}, compile {evidence['compile_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
