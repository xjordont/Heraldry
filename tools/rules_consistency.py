#!/usr/bin/env python3
"""Deterministic rules-consistency checks (no interpretation):
every Monster named in a random-monster table has a bestiary entry."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from parse_source import plain
h = json.loads((ROOT / "production/inventory/headings.json").read_text())
best = {re.sub(r"\s*\[[^\]]*\]$", "", x["title"]).strip() for x in h if x["level"] == 5 and "h-97-the-bestiary" in x["parents"]}
m = json.loads((ROOT / "build/blocks.json").read_text())
missing, checked = {}, 0
def walk(bs):
    global checked
    for b in bs:
        if b["type"] == "table" and plain(b["header"][0]) == "d10" and plain(b["header"][1]) == "1 Hero":
            for r in b["rows"]:
                for c in r[1:]:
                    for part in plain(c).split(","):
                        mm = re.match(r"\s*(\d+)\s+(.+?)\s*$", part)
                        if mm:
                            checked += 1
                            if mm.group(2) not in best:
                                missing.setdefault(mm.group(2), []).append(b["id"])
        walk(b.get("blocks", []))
for ch in m["chapters"]:
    walk(ch["blocks"])
out = {"bestiary_entries": len(best), "monster_group_mentions_checked": checked, "missing_bestiary_entries": missing,
       "status": "PASS" if not missing else "FAIL"}
(ROOT / "production/qa/rules-consistency.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
