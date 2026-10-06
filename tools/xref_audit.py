#!/usr/bin/env python3
"""Audit numbered section citations in the manuscript (e.g. 'see 7.6', '**10.5.7**')
against the numbered headings. Also checks heading-number sequence gaps/duplicates."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "source/Heraldry_RC484.md").read_text().split("\n")
heads = json.loads((ROOT / "production/inventory/headings.json").read_text())
nums = {}
for h in heads:
    m = re.match(r"^((?:\d+|[A-C])(?:\.\d+)+)\s", h["title"]) or re.match(r"^(\d+)\.\s", h["title"])
    if m:
        nums.setdefault(m.group(1), []).append(h["line"])
dups = {k: v for k, v in nums.items() if len(v) > 1}
cites = []
pat = re.compile(r"(\*\*|\b[Ss]ee |\b[Ss]ections? |\(|\bin |\bunder |\bper |\band |, )((?:\d{1,2}|[A-C])\.\d{1,2}(?:\.\d{1,2})?)(?=\*\*|\)|[ ,;:.]|$)")
for i, line in enumerate(src, 1):
    if line.startswith("#") or line.lstrip().startswith("- ["):
        continue
    for m in pat.finditer(line):
        ref = m.group(2)
        pre = line[:m.start(2)]
        if re.search(r"[×x]\s*(\*\*)?$", pre) or re.search(r"\d\s*$", pre):
            continue
        if m.group(1) == "(" and not re.match(r"^\d+\.\d+(\.\d+)?\)", line[m.start(2):]):
            continue
        cites.append({"line": i, "ref": ref, "resolved": ref in nums, "context": line[max(0, m.start() - 40):m.end() + 20]})
unres = [c for c in cites if not c["resolved"]]
out = {"numbered_headings": len(nums), "duplicate_heading_numbers": dups, "citations_checked": len(cites),
       "unresolved": unres}
(ROOT / "production/qa").mkdir(parents=True, exist_ok=True)
(ROOT / "production/qa/xref-audit.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(nums), "headings;", len(cites), "citations;", len(unres), "unresolved;", len(dups), "duplicate numbers")
for u in unres[:30]: print(u)
