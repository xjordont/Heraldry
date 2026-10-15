"""Hash the current manuscript sections that each figure explains."""
import hashlib
import json
import re
from manuscript import ROOT, source_path


def hashes(root=ROOT):
    text = source_path(root).read_text(encoding="utf-8")
    deps = json.loads((root / "config/figure_dependencies.json").read_text(encoding="utf-8"))
    return hashes_for_text(text, deps)


def hashes_for_text(text, dependencies):
    """Hash figure evidence without writing a snapshot or build artifact."""
    lines = text.splitlines(keepends=True)
    headings = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,5})\s+(.+)", line)
        if not m:
            continue
        number = re.match(r"((?:\d+|[A-C])(?:\.\d+)+|\d+)\.?\s", m[2])
        appendix = re.match(r"Appendix ([A-C])\b", m[2])
        if number or appendix:
            headings.append((i, len(m[1]), (number or appendix)[1]))
    sections = {}
    for k, (start, level, number) in enumerate(headings):
        end = next((i for i, depth, _ in headings[k+1:] if depth <= level), len(lines))
        sections[number] = "".join(lines[start:end])
    result = {}
    for fid, numbers in dependencies.items():
        if not numbers or any(n not in sections for n in numbers):
            raise ValueError(f"{fid}: missing figure source dependency")
        result[fid] = hashlib.sha256(json.dumps({n: sections[n] for n in numbers}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return result
