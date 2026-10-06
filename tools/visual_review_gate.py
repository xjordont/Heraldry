"""Require an honest visual ledger bound to this exact PDF and all its pages."""
import json
from manuscript import ROOT, sha256


def check(pdf, pages, root=ROOT):
    r = json.loads((root / "production/qa/visual-review.json").read_text())
    if r.get("sha256") != sha256(pdf) or r.get("pages") != pages:
        raise ValueError("Visual review belongs to a different PDF; inspect this build")
    if not str(r.get("status", "")).startswith("PASS"):
        raise ValueError("Visual review is not passing")
    if set(r.get("pages_reviewed", [])) != set(range(1, pages + 1)):
        raise ValueError("Visual review has incomplete all-page coverage")
    if not r.get("reviewer") or not r.get("reviewed_at"):
        raise ValueError("Visual review needs reviewer and date")
    return r
