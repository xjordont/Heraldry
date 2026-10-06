#!/usr/bin/env python3
"""Regenerate all HERALDRY SKIRMISH RC484 rules diagrams: python3 figures/src/make_figures.py
Writes figures/out/FIG-NN.svg, figures/manifest.json and figures/placements.json.
Optional: pass figure ids (e.g. FIG-01 FIG-05) to build a subset only (SVG only)."""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "out")

MODULES = ["fig_seq", "fig_spatial", "fig_monster", "fig_scen", "fig_misc"]


def registry():
    reg = {}
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        for name in dir(mod):
            if name.startswith("fig") and name[3:].isdigit():
                reg["FIG-%02d" % int(name[3:])] = getattr(mod, name)
    return reg


def build(only=None):
    os.makedirs(OUT, exist_ok=True)
    reg = registry()
    done = []
    for fid in sorted(reg):
        if only and fid not in only:
            continue
        svg, h = reg[fid]()
        import figdata
        meta = figdata.META.get(fid, {})
        text = svg.render(h, title=meta.get("title", fid), desc=meta.get("purpose"))
        with open(os.path.join(OUT, fid + ".svg"), "w", encoding="utf-8") as f:
            f.write(text)
        done.append((fid, svg.w, round(h, 1)))
    return done


def selfcheck():
    """Geometry and arithmetic assertions backing the manifest's semantic_check claims."""
    import fig_spatial as fs
    import math
    # FIG-04: shortest Grid distance for dx=3, dy=2 with orth 1 and diagonal 1.5
    best = min(1.5 * k + ((3 - k) + (2 - k)) * 1.0 for k in range(0, 3))
    assert best == 4.0
    # FIG-05: Speed 5" example
    assert 1 + 1.5 + 1.5 == 4.0 and 5 - 4.0 == 1.0 and 1.5 > 1.0 and 4.0 + 1.5 == 5.5   # FIG-05 forbidden diagonal from the 4" cell
    # FIG-03 examples
    assert (6 - 5) + 4 == 5 and 9 - 3 == 6 and 3 + 2 == 5 and 9 - 5 == 4
    # FIG-07 sight-line geometry (grid-corner coordinates, row 0 at top)
    assert fs._los_blocked((2, 3), (5, 0), [(3, 1), (4, 2)])          # corner shared by 2 Blocking squares
    assert not fs._los_blocked((2, 3), (5, 0), [(3, 1)])              # one square alone: line misses its interior
    assert fs._los_blocked((0, 2), (7, 2), [(3, 2)])                  # interior crossing blocks
    assert not fs._seg_hits_open_square((2.5, 1.5), (5.5, 2.5), 3, 2)  # panel D: only touches a corner
    assert not fs._seg_hits_open_square((1.5, 1.5), (7.5, 2.5), 2, 2)  # panel E after Shift: clears the Fighter (cell (2,2))
    assert 2.0 - (1.5 + (3.0 - 1.5) / 6.0) >= 0.25            # clearance of at least a quarter square at the Fighter square edge
    assert fs._seg_hits_open_square((0.5, 2.5), (7.5, 2.5), 2, 2)      # panel E before Shift: crosses the Fighter
    # FIG-08 counts
    assert len(fs.aura_squares((3, 3), 2)) == 13
    assert len(fs.cone_squares((0, 2), 3)) == 7
    blk = fs.cone_squares((0, 2), 3, [(2, 3)])
    assert dict(blk)[(3, 3)] is True and dict(blk)[(3, 2)] is False
    # FIG-12 equal routes (not drawn) and FIG-18 arithmetic
    assert 16 - 5 == 11 and 11 - 3 == 8 and 8 - 3 == 5 and 13 + 0 + 1 == 14 and 10 + 0 + 0 == 10
    assert 6 + 3 == 9 and 9 - 4 == 5 and 4 + 3 == 7 and 7 - 1 == 6 and 15 - 6 == 9 and 11 + 3 == 14
    assert 5 + 1 == 6 and 6 - 3 == 3 and 9 + 3 == 12 and max(4, 7) + 1 == 8 and 8 - 5 == 3 and 6 + 3 == 9
    # FIG-19 arithmetic
    assert 4 - 2 == 2 and 24 / 2 == 12 and 12 / 2 == 6 and 12 + 4 + 2 * 1 + 3 == 21
    ents = [(12 + 6 * math.cos(math.radians(a)), 12 - 6 * math.sin(math.radians(a))) for a in (0, 120, 240)]
    for i in range(3):
        assert 5 <= math.hypot(ents[i][0] - 12, ents[i][1] - 12) <= 7
        for j in range(i + 1, 3):
            assert math.hypot(ents[i][0] - ents[j][0], ents[i][1] - ents[j][1]) >= 4
        assert 4 <= ents[i][1] <= 20
    # FIG-15: Survey Map 3" before the first ledge, Stone 3" after the last
    assert 14 - 11 == 3 and 25 - 22 == 3


def validate_svgs():
    import re
    import xml.etree.ElementTree as ET
    errs = []
    col = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    def gray(v):
        if v in ("none", "currentColor") or v.startswith("url(#"):
            return True
        m = col.match(v)
        if not m:
            return False
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return h[0:2] == h[2:4] == h[4:6]
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".svg") or not fn.startswith("FIG-"):
            continue
        root = ET.parse(os.path.join(OUT, fn)).getroot()
        w = root.get("width")
        if w not in ("243pt", "504pt"):
            errs.append("%s: width %s" % (fn, w))
        for el in root.iter():
            tag = el.tag.split("}")[-1]
            if tag in ("image", "foreignObject", "script", "style"):
                errs.append("%s: forbidden element %s" % (fn, tag))
            for k, v in el.attrib.items():
                if k.endswith("href"):
                    errs.append("%s: href %s" % (fn, v))
                if k in ("fill", "stroke") and not gray(v):
                    errs.append("%s: non-gray %s=%s" % (fn, k, v))
                if k == "stop-color":
                    errs.append("%s: stop-color" % fn)
            if tag == "text":
                fs_ = float(el.get("font-size", "0"))
                if fs_ < 9:
                    errs.append("%s: font-size %s < 9" % (fn, fs_))
                if "Source Sans 3" not in (el.get("font-family") or ""):
                    errs.append("%s: font-family" % fn)
            sw = el.get("stroke-width")
            if sw is not None and float(sw) < 0.5:
                errs.append("%s: stroke-width %s < 0.5" % (fn, sw))
    return errs


def validate_placements():
    import blockindex
    import figdata
    idx = blockindex.load()
    errs = []
    seen = set()
    for fid, m in figdata.META.items():
        b = m["insert_after"]
        if b not in idx:
            errs.append("%s: block %s not found" % (fid, b))
            continue
        if idx[b]["type"] not in ("para", "list"):
            errs.append("%s: block %s is %s" % (fid, b, idx[b]["type"]))
        if not idx[b]["top"]:
            errs.append("%s: block %s not top-level" % (fid, b))
        src = idx[b]["src"]
        if src and src[0] >= 17122:
            errs.append("%s: block %s in Appendix C" % (fid, b))
        if fid in seen:
            errs.append("duplicate %s" % fid)
        seen.add(fid)
        import re
        if not re.search(r"\(see [^)]+\)\.$", m["caption"]):
            errs.append("%s: caption does not end with a section reference" % fid)
        if len(re.findall(r"[.!?](?:\s|$)", m["caption"])) > 3:
            errs.append("%s: caption longer than 3 sentences" % fid)
    return errs


if __name__ == "__main__":
    only = sys.argv[1:] or None
    done = build(only)
    for d in done:
        print("wrote %s  %spt x %spt" % d)
    selfcheck()
    print("selfcheck (geometry/arithmetic assertions): OK")
    errs = validate_svgs()
    if not only:
        import figdata
        figdata.write_all({d[0]: (d[1], d[2]) for d in done})
        print("wrote manifest.json, placements.json")
        errs += validate_placements()
    for e in errs:
        print("VALIDATION:", e)
    print("validation: %s" % ("OK" if not errs else "%d problem(s)" % len(errs)))
    if errs:
        sys.exit(1)
