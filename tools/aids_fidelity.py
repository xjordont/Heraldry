#!/usr/bin/env python3
"""Bind each player-aid sheet to the manuscript sections it condenses.

`record` hashes those sections in the current manuscript and writes
production/aids/fidelity.json. `check` (the default) reports every sheet whose
sections changed since it was recorded, so a new RC shows which sheets need a
fresh wording review. A hash records what was reviewed; it is not a review.

usage: python tools/aids_fidelity.py [check|record] [--reviewer TEXT]
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "production" / "aids" / "fidelity.json"

# Sheet -> manuscript sections (heading numbers, or a heading title for unnumbered headings).
SHEETS = {
    "pa01": ["2.3", "2.4", "2.10", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "4.2", "4.3", "C.1", "C.4", "10.5.4"],
    "pa02": ["3.4", "9.1", "9.3", "9.4", "9.5", "Bosses", "C.3", "C.8"],
    "pa03": ["2.4", "4.5", "5.1", "5.2", "5.3", "5.4", "5.5", "5.7", "C.5", "C.6"],
    "pa04": ["5.8", "5.9", "11.1.5", "11.2.4", "C.10"],
    "pa05": ["2.8.5", "5.9", "C.3"],
    "pa06": ["2.6", "2.9.9", "4.4", "5.1", "5.5.4", "5.6"],
    "pa07": ["2.7", "2.8", "2.9", "4.3", "5.9"],
    "pa08": ["11.1.5", "11.2", "11.3", "C.10"],
    "pa09": ["11.2.4", "11.2.5", "11.2.6", "11.3", "C.10"],
    "pa10": ["10.1", "10.5"],
}


def current_source():
    v = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    rev = next(r for r in v["revisions"] if r["number"] == v["current"])
    return v["current"], rev["sha256"], (ROOT / rev["path"]).read_text(encoding="utf-8").split("\n")


def section_text(lines, ref):
    pat = re.compile(r"^(#{2,6}) " + re.escape(ref) + r"(\s|$)")
    for i, line in enumerate(lines):
        m = pat.match(line)
        if m:
            level = len(m.group(1))
            j = i + 1
            while j < len(lines):
                h = re.match(r"^(#{1,6}) ", lines[j])
                if h and len(h.group(1)) <= level:
                    break
                j += 1
            return "\n".join(lines[i:j])
    raise KeyError(f"section {ref} not found")


def hashes(lines):
    return {sheet: {ref: hashlib.sha256(section_text(lines, ref).encode("utf-8")).hexdigest() for ref in refs}
            for sheet, refs in SHEETS.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", choices=["check", "record"], default="check")
    ap.add_argument("--reviewer", default="")
    a = ap.parse_args()
    rc, sha, lines = current_source()
    now = hashes(lines)
    if a.action == "record":
        if not a.reviewer:
            sys.exit("record needs --reviewer describing who checked the wording and how")
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps({
            "rc": rc, "source_sha256": sha, "recorded_at": datetime.date.today().isoformat(),
            "reviewer": a.reviewer, "sheets": now}, indent=1) + "\n", encoding="utf-8")
        print(f"recorded {len(now)} sheets against RC{rc}")
        return
    rec = json.loads(LEDGER.read_text(encoding="utf-8"))
    stale = {s: [r for r, h in refs.items() if rec["sheets"].get(s, {}).get(r) != h] for s, refs in now.items()}
    stale = {s: r for s, r in stale.items() if r}
    if stale:
        for s, refs in stale.items():
            print(f"STALE {s}: sections changed since RC{rec['rc']}: {', '.join(refs)}")
        sys.exit(1)
    print(f"PASS: all {len(now)} sheets match the sections reviewed at RC{rec['rc']}")


if __name__ == "__main__":
    main()
