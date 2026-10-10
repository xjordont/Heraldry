#!/usr/bin/env python3
"""Remap manuscript line citations in figure sources after an RC promotion.

  python3 tools/remap_figure_lines.py --old source/Heraldry_RC488.md --new source/Heraldry_RC489.md

Builds an exact old->new line map from a diff of the two immutable snapshots (equal and
same-length replaced runs only) and applies it to every line citation in
figures/src/scenario_specs.json (keys lines, shared, spans, insert_after_line, board_line) and
to 4-5 digit line numbers in figures/src/*.py. A citation whose line was deleted is a hard
error: re-cite it by hand. Run `make figures` afterwards; its selfcheck verifies the cited text."""
import argparse, difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def line_map(old, new):
    a, b = old.read_text().split("\n"), new.read_text().split("\n")
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                m[i1 + k + 1] = j1 + k + 1
    return m, len(a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True, type=Path)
    ap.add_argument("--new", required=True, type=Path)
    a = ap.parse_args()
    m, n_old = line_map(a.old, a.new)
    lost = []

    def mp(x, where):
        if x not in m:
            lost.append((where, x))
            return x
        return m[x]

    def fix(o, where="spec"):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k in ("lines", "shared") and isinstance(v, list):
                    o[k] = [mp(x, where) for x in v]
                elif k == "spans" and isinstance(v, list):
                    o[k] = [[mp(x, where) for x in pr] for pr in v]
                elif k in ("insert_after_line", "board_line") and isinstance(v, int):
                    o[k] = mp(v, where)
                else:
                    fix(v, o.get("id", where) if isinstance(o.get("id"), str) else where)
        elif isinstance(o, list):
            for x in o:
                fix(x, where)

    spec = ROOT / "figures/src/scenario_specs.json"
    s = json.loads(spec.read_text())
    fix(s)
    changed = 0
    for f in sorted((ROOT / "figures/src").glob("*.py")):
        t = f.read_text()

        def r(mo):
            nonlocal changed
            v = int(mo.group(0))
            if 1000 <= v <= n_old and m.get(v, v) != v:
                changed += 1
                return str(m[v])
            return mo.group(0)
        t2 = re.sub(r"\b\d{4,5}\b", r, t)
        if t2 != t:
            f.write_text(t2)
    if lost:
        raise SystemExit(f"citations to deleted lines; re-cite by hand: {lost}")
    spec.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"python_refs_changed": changed}))


if __name__ == "__main__":
    main()
