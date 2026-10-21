#!/usr/bin/env python3
"""Fail closed on avoidable splits, missing source units and invalid markers."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

from pdf_positions import validate_sidecar

ROOT = Path(__file__).resolve().parents[1]


def validate_measurement_binding(units, positions_binding, root=ROOT):
    """Require classification heights from the current warning-free compile."""
    root = Path(root)
    rows = json.loads((root / "build/unit_measure.json").read_text(encoding="utf-8"))
    binding = json.loads((root / "build/unit_measure.binding.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if binding.get("origin") != "measurement-pdf-attachment" or binding.get("measurements_sha256") != digest:
        raise ValueError("Unit heights differ from serialized measurement evidence; rebuild")
    identity = binding.get("identity", {})
    final = positions_binding["identity"]
    for key in ("input_sha256", "variant", "edition", "compiler", "timestamp"):
        if key not in identity or identity[key] != final.get(key):
            raise ValueError("Unit measurements do not describe the final PDF inputs: " + key)
    measure_sha = hashlib.sha256((root / "typst/measure.typ").read_bytes()).hexdigest()
    if identity.get("content_sha256") != measure_sha:
        raise ValueError("Stale generated unit measurement source; rebuild")
    if set(rows) != set(units.get("expected_unit_ids", [])):
        raise ValueError("Measurement coverage differs from expected source-unit inventory")
    for unit in units["units"]:
        actual = rows.get(unit["id"], {})
        if any(unit.get(k) != actual.get(k) for k in ("h1", "h2")):
            raise ValueError("Keep audit heights differ from measured heights: " + unit["id"])
    return binding


def analyze_units(units, positions, pdf_pages):
    """Audit independently enumerated source units against final PDF markers."""
    fit = units["frame_fit_pt"]
    measured = units["units"]
    expected = units.get("expected_unit_ids")
    manifest = units.get("source_unit_manifest")
    coverage_errors = []
    if not isinstance(expected, list) or not expected:
        coverage_errors.append({"reason": "missing independent expected source-unit inventory"})
        expected = []
    counts = Counter(x["id"] for x in measured)
    expected_counts = Counter(expected)
    for uid in sorted(set(counts) | set(expected_counts)):
        if counts[uid] != 1 or expected_counts[uid] != 1:
            coverage_errors.append({"id": uid, "source_count": expected_counts[uid], "measured_count": counts[uid]})
    if not isinstance(manifest, list) or Counter(x["id"] for x in manifest) != expected_counts:
        coverage_errors.append({"reason": "source-unit manifest is missing or disagrees with expected IDs"})
    markers = {}
    for m in positions["<um-pos>"]:
        markers.setdefault(m.get("id"), []).append(m)
    pos, marker_errors = {}, []
    for uid, found in markers.items():
        starts = [m for m in found if m.get("edge") == "s"]
        ends = [m for m in found if m.get("edge") == "e"]
        if uid not in expected_counts or len(starts) != 1 or len(ends) != 1 or len(found) != 2:
            marker_errors.append({"id": uid, "starts": len(starts), "ends": len(ends),
                                  "records": len(found), "unexpected": uid not in expected_counts})
            continue
        p1, p2 = starts[0].get("page"), ends[0].get("page")
        if type(p1) is not int or type(p2) is not int or not 1 <= p1 <= p2 <= pdf_pages:
            marker_errors.append({"id": uid, "start": p1, "end": p2, "invalid_page_order": True})
            continue
        pos[uid] = {"s": p1, "e": p2}
    rows, fails, over, measurement_errors = [], [], [], []
    missing = sorted(set(expected) - set(pos))
    for x in measured:
        h1, h2 = x.get("h1"), x.get("h2")
        heights = [h for h in (h1, h2) if type(h) in (int, float) and math.isfinite(h) and h >= 0]
        if len(heights) != 2:
            measurement_errors.append({"id": x["id"], "h1": h1, "h2": h2})
        fits = bool(heights) and min(heights) <= fit
        p = pos.get(x["id"])
        if p is None:
            continue
        pages = list(range(p["s"], p["e"] + 1))
        row = {"id": x["id"], "kind": x["kind"], "class": x["class"], "h1_pt": h1, "h2_pt": h2,
               "fit_capable": fits, "pages": pages}
        rows.append(row)
        if fits and len(pages) > 1:
            fails.append(row)
        if not fits and len(heights) == 2:
            over.append({"id": x["id"], "kind": x["kind"], "h2_pt": h2, "pages": pages,
                         "reason": "taller than one empty usable page at approved widths; child units audited separately"})
    return {"frame_fit_pt": fit, "units": len(measured), "expected_source_units": len(expected),
            "audited": len(rows), "fit_capable": sum(r["fit_capable"] for r in rows),
            "avoidable_splits": fails, "missing_coverage": missing, "malformed_markers": marker_errors,
            "source_coverage_errors": coverage_errors, "measurement_errors": measurement_errors,
            "over_height": over, "rows": rows,
            "status": "FAIL" if any((fails, missing, marker_errors, coverage_errors, measurement_errors)) else "PASS"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--positions", required=True, help="JSON extracted from exact serialized PDF")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    u = json.loads((ROOT / "build/units.json").read_text())
    content = hashlib.sha256((ROOT / "typst/content.typ").read_bytes()).hexdigest()
    if u.get("content_sha256") != content:
        raise ValueError("units.json does not describe current typst/content.typ; rebuild")
    positions = json.loads(Path(a.positions).read_text())
    bound = validate_sidecar(positions, a.pdf, root=ROOT)["binding"]
    measurement_binding = validate_measurement_binding(u, bound, ROOT)
    rep = analyze_units(u, positions, bound["pdf_pages"])
    rep.update({"content_sha256": content, "pdf": a.pdf, "pdf_sha256": bound["pdf_sha256"],
                "position_binding": bound, "measurement_binding": measurement_binding})
    Path(a.report).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()
                      if k not in ("rows", "position_binding", "measurement_binding")}))
    raise SystemExit(0 if rep["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
