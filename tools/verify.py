#!/usr/bin/env python3
"""Release verification gate. Runs every deterministic check on the final files in dist/
and writes production/qa/*.json plus production/qa/STATUS.json. Exits non-zero when a
mandatory check fails, so a failed build cannot be labelled an unconditional release."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "production/qa"
DIST = ROOT / "dist"
PY = sys.executable
from manuscript import version
from provenance import check as check_provenance
QUERY_CACHE = None


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError, TypeError):
        return default


def ensure_build_artifacts(*paths):
    missing = [str(p) for p in paths if not Path(p).exists()]
    if missing:
        raise FileNotFoundError("Build artifacts missing; generate the publication first: " + ", ".join(missing))


def run(args, report=None):
    if report:
        Path(report).unlink(missing_ok=True)
    r = subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True)
    status = "PASS" if r.returncode == 0 else "FAIL"
    if report:
        if not Path(report).exists():
            status = "FAIL"
        else:
            payload = load_json(report)
            if not isinstance(payload, dict) or payload.get("status") != "PASS":
                status = "FAIL"
    return status, (r.stdout + r.stderr)[-600:]


def tquery(sel):
    global QUERY_CACHE
    if QUERY_CACHE is None:
        cmd = [PY, "tools/query_typst.py"]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("Typst query failed: " + (r.stderr or r.stdout or "unknown error"))
        QUERY_CACHE = json.loads(r.stdout)
    return QUERY_CACHE[sel]


def main():
    QA.mkdir(parents=True, exist_ok=True)
    cream = DIST / f"Heraldry_{version()}_inkjet-borderless.pdf"
    white = DIST / f"Heraldry_{version()}_inkjet-borderless-white.pdf"
    digital = DIST / f"Heraldry_{version()}_digital.pdf"
    ensure_build_artifacts(cream, white, digital)
    st = {}
    provenance = check_provenance()
    st["build_provenance"] = "PASS"
    st["source_preflight"], _ = run(["tools/preflight.py", "--report", "production/preflight.json"])
    pf = load_json(ROOT / "production/preflight.json") or {}
    src_ok = "FAIL"
    for c in pf.get("checks", []):
        if c.get("check") == "source_integrity":
            src_ok = c.get("status", "FAIL")
            break
    st["source_integrity"] = src_ok
    st["reconciliation"], _ = run(["tools/reconcile.py", str(cream), "--report", str(QA / "reconciliation.json")], QA / "reconciliation.json")
    st["reconciliation_digital"], _ = run(["tools/reconcile.py", str(digital), "--skip-covers", "--report", str(QA / "reconciliation-digital.json")], QA / "reconciliation-digital.json")
    lay, _ = run(["tools/layout_qa.py", str(cream), "--report", str(QA / "layout.json")])
    lj = load_json(QA / "layout.json") or {}
    st["layout_detectors"] = "PASS" if lay == "PASS" and not lj.get("counts") else "FAIL"
    st["inkjet_checker_cream"], _ = run(["tools/verify_inkjet_pdf.py", str(cream), "--report", str(QA / "inkjet-preflight.json")], QA / "inkjet-preflight.json")
    st["inkjet_checker_white"], _ = run(["tools/verify_inkjet_pdf.py", str(white), "--report", str(QA / "inkjet-preflight-white.json")], QA / "inkjet-preflight-white.json")
    st["print_supplementary"], _ = run(["tools/print_checks.py", "--cream", str(cream), "--white", str(white), "--report", str(QA / "print-checks.json")], QA / "print-checks.json")
    st["xref_audit"], _ = run(["tools/xref_audit.py"])
    xr = load_json(QA / "xref-audit.json") or {}
    st["xref_audit"] = "PASS" if st["xref_audit"] == "PASS" and not xr.get("unresolved") and not xr.get("duplicate_heading_numbers") else "FAIL"

    st["monster_references"], _ = run(["tools/rules_consistency.py"], QA / "rules-consistency.json")

    try:
        from visual_review_gate import check as check_visual
        rec = load_json(QA / "reconciliation.json") or {}
        if isinstance(rec, dict):
            check_visual(cream, rec.get("pdf_pages", []))
        else:
            raise ValueError("visual review input missing")
        st["visual_review_currency"] = "PASS"
    except (ValueError, OSError, TypeError) as exc:
        st["visual_review_currency"] = "FAIL"
        print(str(exc), file=sys.stderr)

    # ---- all-table audit: source id → output pages → representation → reconciliation
    rec = load_json(QA / "reconciliation.json") or {}
    bad_tables = {t["id"] for t in rec.get("table_cells_missing", [])} if isinstance(rec, dict) else set()
    inv = load_json(ROOT / "production/inventory/tables.json") or []
    reps = {t["id"]: t for t in (load_json(ROOT / "production/mappings/tables.json") or [])}
    pos = {}
    allpos = tquery("<tblpos>")
    for m in allpos:
        pos.setdefault(m["id"], []).append(m)
    starts = {}
    for m in allpos:
        if m["edge"] == "s":
            starts[m["id"]] = starts.get(m["id"], 0) + 1
    dup = {k: v for k, v in starts.items() if v != 1}
    st["no_duplicate_tables_figures"] = "PASS" if not dup else "FAIL"
    rows = []
    for t in inv:
        ps = pos.get(t["id"], [])
        folios = sorted({m["folio"] for m in ps}, key=lambda f: int(f) if f.isdigit() else 0)
        pages = sorted({m["page"] for m in ps})
        r = reps.get(t["id"], {})
        rows.append({"id": t["id"], "src_lines": t["src"], "heading": t["heading_title"], "columns": t["columns"],
                     "rows": t["rows"], "cells": t["cells"], "cell_sha256": t["cell_sha256"],
                     "representation": r.get("rep"), "scope": r.get("scope"), "family": r.get("family"),
                     "field_map": r.get("field_map"), "pdf_pages": [pages[0], pages[-1]] if pages else None,
                     "folios": [folios[0], folios[-1]] if folios else None,
                     "multipage": len(pages) > 1 and pages[0] != pages[-1],
                     "reconciliation": "FAIL" if t["id"] in bad_tables or not pages else "PASS"})
    ta = {"tables": len(rows), "pass": sum(r["reconciliation"] == "PASS" for r in rows),
          "multipage": [r["id"] for r in rows if r["multipage"]], "rows": rows,
          "note": "Cell-level check: every normalised source cell appears in the PDF text layer within the table's local window (tools/reconcile.py). Repeated headers and card field labels are treated as expected duplicates; the gate reports only unresolved or missing cell matches.",
          "status": "PASS"}
    ta["status"] = "PASS" if ta["pass"] == ta["tables"] else "FAIL"
    (QA / "table-audit.json").write_text(json.dumps(ta, indent=1, ensure_ascii=False))
    st["table_audit"] = ta["status"]

    # ---- index audit
    idx = load_json(ROOT / "build/index.json") or {}
    loc = {}
    for m in tquery("<ixpos>"):
        loc.setdefault(m["k"], set()).add(m["folio"])
    hpos_result = tquery("<hpos>")
    hpos = {h["id"]: h for h in (hpos_result[0] if isinstance(hpos_result, list) and hpos_result and isinstance(hpos_result[0], list) else [])}
    for k, hids in idx.get("heads", {}).items():
        for hid in hids:
            if hid in hpos:
                loc.setdefault(k, set()).add(str(hpos[hid]["folio"]))
    keys = [k for e in idx.get("entries", []) for k in e.get("keys", [])] + [k for e in idx.get("entries", []) for s in e.get("sub", []) for k in s.get("keys", [])]
    missing = [k for k in keys if k not in loc]
    entries = idx.get("entries", [])
    see_bad = [e["term"] for e in entries if e.get("see") and e["see"].lower() not in {x["term"].lower() for x in entries}]
    ia = {"entries": len(entries), "locator_keys": len(keys), "keys_without_page": missing, "see_targets_missing": see_bad,
          "term_pages": {k: sorted(v, key=lambda f: int(f) if f.isdigit() else 0) for k, v in loc.items()}}
    ia["status"] = "PASS" if not missing and not see_bad else "FAIL"
    (QA / "index-audit.json").write_text(json.dumps(ia, indent=1, ensure_ascii=False))
    st["index_audit"] = ia["status"]

    # ---- figures
    man = ROOT / "figures/manifest.json"
    if man.exists():
        figs = json.loads(man.read_text())
        figs = figs["figures"] if isinstance(figs, dict) else figs
        placed = {m["id"]: m for m in tquery("<tblpos>") if str(m["id"]).startswith("FIG")}
        fa = [{"id": f["id"], "placed": f["id"] in placed, "folio": placed.get(f["id"], {}).get("folio"),
               "semantic_status": f.get("status")} for f in figs]
        st["figures_placed"] = "PASS" if all(x["placed"] for x in fa) else "FAIL"
        (QA / "figure-audit.json").write_text(json.dumps(fa, indent=1))
    else:
        st["figures_placed"] = "NOT TESTED"
    # figure semantic review must be current (hash-bound to the SVG and caption) and free of open majors
    st["figure_semantic_review"], _ = run(["tools/figure_review_gate.py", "--report", str(QA / "figure-review-gate.json")], QA / "figure-review-gate.json")

    declared = [x["id"] for x in json.loads((ROOT / "editorial/patches.json").read_text())["patches"] if x.get("status") == "applied"]
    applied = load_json(ROOT / "build/blocks.json") or {}
    st["editorial_patches"] = "PASS" if declared == applied.get("patches_applied", []) else "FAIL"

    mandatory = ["visual_review_currency", "monster_references", "build_provenance", "editorial_patches", "source_preflight", "source_integrity", "reconciliation", "reconciliation_digital",
                 "layout_detectors", "inkjet_checker_cream", "inkjet_checker_white", "print_supplementary", "no_duplicate_tables_figures", "xref_audit", "table_audit", "index_audit", "figures_placed",
                 "figure_semantic_review"]
    failed = [k for k in mandatory if st.get(k) != "PASS"]
    out = {"provenance": provenance, "checks": st, "mandatory_failed": failed, "release_gate": "PASS" if not failed else "FAIL",
           "not_covered_here": ["all-page visual inspection (production/qa/visual-review.json)",
                               "diagram semantic correctness beyond the hash-bound review record (production/qa/figure-semantic-review.json)",
                               "physical inkjet proof: NOT TESTED"]}
    (QA / "STATUS.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "provenance"}, indent=1))
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        QA.mkdir(parents=True, exist_ok=True)
        (QA / "STATUS.json").write_text(json.dumps({"release_gate": "FAIL", "mandatory_failed": ["verification_execution"], "error": str(exc)}, indent=2) + "\n")
        raise
