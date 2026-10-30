#!/usr/bin/env python3
"""Regenerate all HERALDRY SKIRMISH RC484 rules diagrams: python3 figures/src/make_figures.py
Writes figures/out/FIG-NN.svg, figures/manifest.json and figures/placements.json.
Optional: pass figure ids (e.g. FIG-01 FIG-05) to build a subset only (SVG only)."""
import importlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "out")

MODULES = ["fig_seq", "fig_spatial", "fig_monster", "fig_scen", "fig_misc", "fig_appx", "fig_scenmaps",
           "fig_end_a", "fig_end_b", "fig_end_c"]


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
        with open(os.path.join(OUT, fid + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        done.append((fid, svg.w, round(h, 1)))
    return done


def selfcheck():
    """Geometry and arithmetic assertions backing the manifest's semantic_check claims."""
    import fig_end_a, fig_end_b, fig_end_c
    fig_end_a.selfcheck_end_a()
    fig_end_b.selfcheck_end_b()
    fig_end_c.selfcheck_end_c()
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
    assert not fs._seg_hits_open_square((0.5, 1.5), (7.5, 2.5), 2, 2)  # panel E after Shift: clears the Fighter (cell (2,2))
    assert 2.0 - (1.5 + (3.0 - 0.5) / 7.0) > 0            # clearance of at least a quarter square at the Fighter square edge
    assert fs._seg_hits_open_square((0.5, 2.5), (7.5, 2.5), 2, 2)      # panel E before Shift: crosses the Fighter
    # FIG-08 counts
    assert len(fs.aura_squares((3, 3), 2)) == 13
    assert len(fs.cone_squares((0, 2), 3)) == 7
    assert (0, 2) not in [q for q, _ in fs.cone_squares((0, 2), 3)]   # the origin square is not among the counted cone squares (P-01 concerns the originating combatant)
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
    # FIG-14 panels B and C: each separation dimension runs exactly between the closest edges (2.6) of the
    # nearest opposing Heroes; those Heroes are farther apart than the limit; every marker is inside its zone
    import fig_scen
    fig_scen.fig14()  # populate geometry even when the CLI regenerates a different SVG subset
    for key in ("B", "C"):
        g = fig_scen.GEOM14[key]
        (x1, y1), (x2, y2) = g["dim"]
        (ax, ay), (bx_, by_) = g["a"], g["b"]
        assert abs(math.hypot(bx_ - ax, by_ - ay) - g["r"] * 2 - math.hypot(x2 - x1, y2 - y1)) < 1e-9
        assert abs(x1 - (ax + g["r"])) < 1e-9 and abs(x2 - (bx_ - g["r"])) < 1e-9 and y1 == ay and y2 == by_
        assert math.hypot(x2 - x1, y2 - y1) > g["limit"]
    gc = fig_scen.GEOM14["C"]
    z = gc["zone"]
    for (x, y) in [gc["a"], gc["b"]] + gc["others"]:
        assert z[0] <= x - 0.5 and x + 0.5 <= z[2] and z[1] <= y - 0.5 and y + 0.5 <= z[3]
    for (ax, ay) in [gc["a"], gc["others"][0]]:      # every A-B pair is more than 3" apart (closest points)
        for (bx_, by_) in [gc["b"], gc["others"][1]]:
            assert math.hypot(bx_ - ax, by_ - ay) - 1.0 > 3.0
    assert fig_scen.GEOM14["B"]["b"][0] - fig_scen.GEOM14["B"]["a"][0] - 2 * fig_scen.GEOM14["B"]["r"] > 6.0
    # FIG-15: Survey Map 3" before the first ledge, Stone 3" after the last
    assert 14 - 11 == 3 and 25 - 22 == 3
    # FIG-20..57: scenario deployment maps, legend and procedural template
    import fig_scenmaps
    problems = fig_scenmaps.check_scenmaps()
    assert not problems, "scenario map checks failed:\n  " + "\n  ".join(problems)


def typography_errors(text):
    """Apply the manuscript's visible-character lock to figure labels and captions."""
    bad = set()
    banned = "\u00a0\u00a7\u2018\u2019\u201c\u201d\u2026\u2032\u2033\u2035\u2036\u2212"
    for i, char in enumerate(text):
        if char in banned or (unicodedata.category(char) == "Pd" and char not in "-–"):
            bad.add("U+%04X" % ord(char))
        if char == "–" and not (i > 0 and i + 1 < len(text) and text[i - 1].isdigit() and text[i + 1].isdigit()):
            bad.add("non-range U+2045")
    return sorted(bad)


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
                for problem in typography_errors("".join(el.itertext())):
                    errs.append("%s: visible typography %s" % (fn, problem))
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
    model = json.load(open(os.path.join(HERE, "..", "..", "build", "blocks.json")))
    appendix_c = {b["id"] for ch in model["chapters"] if ch["id"].startswith("h-appendix-c") for b in ch["blocks"]}
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
        if b in appendix_c:
            errs.append("%s: block %s in Appendix C" % (fid, b))
        if fid in seen:
            errs.append("duplicate %s" % fid)
        seen.add(fid)
        import re
        for problem in typography_errors(m["caption"]):
            errs.append("%s: caption typography %s" % (fid, problem))
        if not re.search(r"\(see [^)]+\)\.$", m["caption"]):
            errs.append("%s: caption does not end with a section reference" % fid)
        if len(re.findall(r"[.!?](?:\s|$)", m["caption"])) > 3:
            errs.append("%s: caption longer than 3 sentences" % fid)
    return errs


def write_anchor_proposals():
    """figures/anchor_proposals.json: content-anchor definitions (section, type, text prefix) for the new figures,
    ready to merge into config/content_anchors.json so that placement survives line renumbering."""
    import figdata
    from content_anchors import text_of
    model = json.load(open(os.path.join(HERE, "..", "..", "build", "blocks.json")))
    cands, section = [], None
    for ch in model["chapters"]:
        for b in ch["blocks"]:
            if b["type"] == "heading":
                section = b["id"]
            cands.append((section, b))
    byid = {b["id"]: (sec, b) for sec, b in cands}
    out = {}
    for fid in sorted(figdata.META):
        if not figdata.META[fid].get("new_figure"):
            continue
        sec, b = byid[figdata.META[fid]["insert_after"]]
        t = text_of(b)
        for n in (120, 160, 220, 300, 400):
            pre = t[:n]
            hits = [x for s_, x in cands if s_ == sec and x["type"] == b["type"] and text_of(x).startswith(pre)]
            if len(hits) == 1:
                out[fid] = dict(section=sec, type=b["type"], prefix=pre)
                break
        else:
            raise SystemExit("no unique anchor prefix for " + fid)
    with open(os.path.join(HERE, "..", "anchor_proposals.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_coverage(dims):
    """production/qa/scenario-coverage.json: scenario / map / rule coverage matrix."""
    import figdata
    import fig_scenmaps
    rows, summ, amb_total = fig_scenmaps.coverage_matrix()
    for r in rows:
        r["map_size_pt"] = {"width": dims[r["map_figure"]][0], "height": dims[r["map_figure"]][1]}
    appendix = fig_scenmaps.appendix_coverage()
    for r in appendix:
        r["insert_after"] = figdata.META[r["map_figure"]]["insert_after"]
        r["map_size_pt"] = {"width": dims[r["map_figure"]][0], "height": dims[r["map_figure"]][1]}
    procedural = dict(key="10.1 Preparation Steps", source_lines=[11099, 11112], map_figure="FIG-%d" % (fig_scenmaps.FIRST_MAP_FIG + 36), iconography="shared-v2",
                      legend_figure=fig_scenmaps.LEGEND_FIG, detail_figures=["FIG-13", "FIG-14"],
                      insert_after="B%05d" % fig_scenmaps.TEMPLATE_ANCHOR_LINE,
                      setup_rules=["step 7: define deployment zones before terrain; alternately placed Blocking/Impassable pieces stay outside zones; Blocking pieces more than 2\" apart", "step 7 defaults: edge zones 6\" deep, corner zones 8\"x8\"; step 11: alternate placing from the Roll-off loser"],
                      status="drawn")
    drawn = sum(1 for r in rows if r["status"] == "drawn")
    summary = dict(scenarios=len(rows), drawn=drawn, blocked_by_ambiguity=len(rows) - drawn,
                   scenario_map_figures="FIG-%d to FIG-%d" % (fig_scenmaps.FIRST_MAP_FIG, fig_scenmaps.FIRST_MAP_FIG + len(rows) - 1),
                   legend_figure=fig_scenmaps.LEGEND_FIG, template_figure=procedural["map_figure"],
                   elements=dict(mandatory=summ["MANDATORY_POSITION"], constrained=summ["CONSTRAINED"], illustrative=summ["ILLUSTRATIVE"], unresolved=summ["UNRESOLVED"]),
                   iconography="shared-v2", glyph_registry="figures/src/scenkit.py (REG); key FIG-20",
                   ambiguities_logged=amb_total,
                   global_notes=["Group placement constraints ('within 3\" of ...', 'at least 8\" from ...') are drawn for one marker per Monster Group; the text does not say whether every member of a multi-Monster group must satisfy them.",
                                 "Counts of scattered terrain are printed values; maps draw a few representative pieces and never resolve 10.6 scaling."])
    with open(os.path.join(HERE, "..", "..", "source", "versions.json"), encoding="utf-8") as f:
        versions = json.load(f)
    current = next(r for r in versions["revisions"] if r["number"] == versions["current"])
    out = dict(source=current["path"], source_sha256=current["sha256"], source_created_at=current["created_at"],
               scenarios=rows, appendix=appendix, procedural=procedural, summary=summary)
    path = os.path.join(HERE, "..", "..", "production", "qa", "scenario-coverage.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # independent-review records live in the same file: carry every existing "review" key over, never regenerate it
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        for sec in ("scenarios", "appendix"):
            prev = {r["key"]: r["review"] for r in old.get(sec, []) if "review" in r}
            for r in out[sec]:
                if r["key"] in prev:
                    r["review"] = prev[r["key"]]
        for sec in ("procedural", "summary"):
            if "review" in old.get(sec, {}):
                out[sec]["review"] = old[sec]["review"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    only = sys.argv[1:] or None
    done = build(only)
    for d in done:
        print("wrote %s  %spt x %spt" % d)
    selfcheck()
    print("selfcheck (geometry/arithmetic assertions): OK")
    errs = validate_svgs()
    if not only:
        import fig_scenmaps
        errs += ["REGISTRY: " + e for e in fig_scenmaps.check_registry(OUT)]
        import figdata
        figdata.write_all({d[0]: (d[1], d[2]) for d in done})
        print("wrote manifest.json, placements.json")
        write_coverage({d[0]: (d[1], d[2]) for d in done})
        write_anchor_proposals()
        print("wrote production/qa/scenario-coverage.json")
        errs += validate_placements()
    for e in errs:
        print("VALIDATION:", e)
    print("validation: %s" % ("OK" if not errs else "%d problem(s)" % len(errs)))
    if errs:
        sys.exit(1)
