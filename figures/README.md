# Rules diagrams (RC485)

Fifty-seven editable SVG diagrams for the Heraldry Skirmish rulebook, generated deterministically from code (stdlib only): FIG-01 to FIG-19 rules diagrams, and FIG-20 to FIG-57 the scenario deployment maps (legend, 36 Core Scenario maps, 10.1 procedural template).

Regenerate everything (SVGs, `manifest.json`, `placements.json`, `anchor_proposals.json`, `production/qa/scenario-coverage.json`) and run all checks:

    python3 figures/src/make_figures.py          # all figures
    python3 figures/src/make_figures.py FIG-07   # SVG subset only (no manifest rewrite)

Files

- `src/svgkit.py` shared visual grammar (tokens, terrain patterns, arrows, callouts, legend, grid helpers, text metrics from `src/fontmetrics.json`).
- `src/fig_seq.py`, `fig_spatial.py`, `fig_monster.py`, `fig_scen.py`, `fig_misc.py` figure drawings; `src/figdata.py` IDs, captions, insertion targets, source references, semantic checks.
- `out/FIG-NN.svg` outputs, 1 user unit = 1 pt, Source Sans 3 text of 9 pt or more, grayscale only, no raster or external references. FIG-01 to FIG-19, FIG-20 (legend) and FIG-57 (template) are `full` scope (504 pt wide); FIG-21 to FIG-56 (the maps) are `column` scope (243 pt wide, height at most about 260 pt).
- `manifest.json` one record per figure; `placements.json` maps block id to `[{id, caption, width, scope}]`, inserted immediately after that block.

Checks run by `make_figures.py`: geometry and arithmetic assertions behind the manifest's semantic checks, SVG validation (grayscale colours, font size >= 9, stroke >= 0.5, no images or hrefs, widths), and placement validation (block exists in `build/blocks.json`, is a top-level paragraph or list, is not in Appendix C, caption ends with a section reference and has at most 3 sentences).

Visual inspection: `python3 figures/src/test/render.py FIG-01 FIG-02 ...` renders PNGs through Typst into `figures/src/test/` (git-ignored; safe to delete).

Visual grammar: Party A = black circle; Party B = white circle with centre dot; Monster = hatched hexagon (hatched square for Large); Blocking = solid dark gray; Cover = cross-hatch; Difficult = dot stipple; Impassable = dense diagonal hatch; solid arrow = movement or permitted; dashed = line of sight; dotted = forced movement; arrow ending in X = not permitted; numbered black circles = steps. Diagrams that are not to scale carry "Schematic — not to scale"; inch values shown are only values the source states.

## Scenario deployment maps (FIG-20 to FIG-57)

- `src/scenario_specs.json` one structured spec per Core Scenario (key such as `"Greenmark 1"`): `tag`, `insert_after_line` (source line of the paragraph the map follows, block id `B` plus 5 digits), `board_line`, `caption`, `detail_figures`, `setup_rules`, `foot` notes, `ambiguities`, `undrawn` (conditional placements deliberately not drawn) and `elements`. Every element has `id`, `kind` (zone, feature, marker, monster, edge), geometry in inches (origin top-left, North drawn at the top, short edges top and bottom), `status` and `lines` (source line numbers inside the scenario's span; `shared` lists 10.1 / 10.6 rule lines such as step 11 at line 11072). Statuses: `MANDATORY_POSITION` (the source fixes the location), `CONSTRAINED` (a range or relation, drawn solid with its dimension line or ring), `ILLUSTRATIVE` (location open: one legal arrangement drawn light grey dashed). Annotations (`anno`) draw and assert the stated distances: `rel` (within / at least / exactly, as ruler or ring), `ring`, `edgein`, `dim`, `pdim` (Hero-to-Hero), `inside`; `hide` asserts without drawing.
- `src/fig_scenmaps.py` the one renderer: board 36"x36" at 5.2 pt per inch (zones and stated distances to scale, markers enlarged, Large and Huge Monsters at footprint scale), 6" scale bar, N/E/S/W letters, automatic label placement with leader lines, standard note "Grey dashed = one legal arrangement; position not fixed by the rules", plus `fig20` (the shared legend, placed after the 10.4 introduction, which the maps rely on instead of a per-map legend) and `fig57` (10.1 Preparation Steps template, "Template - not a fixed battlefield", with the step 11 default zones and the step 7 exclusion distances 3" and 6").
- `check_scenmaps()` (run by `make_figures.py` selfcheck): exactly one map per 10.4 scenario heading and sequential figure ids in book order; every element cites lines inside its scenario's span; every inch value printed on a map appears in its cited source lines; every `rel`, `ring`, `edgein`, `dim`, `pdim` and `inside` annotation is asserted numerically (closest-point distances, 2.6); markers and Monsters stay out of the deployment zones (10.1 step 8) and Blocking, Impassable or obstacle pieces stay 3" from an edge and 6" from a zone (10.1 step 7) unless flagged `exempt` because the scenario says otherwise; the legend and template inch values are checked against their cited lines.
- `anchor_proposals.json` content-anchor definitions (section, type, text prefix) for FIG-20 to FIG-57, ready to merge into `config/content_anchors.json` so placement survives line renumbering.
- `production/qa/scenario-coverage.json` the coverage matrix: per scenario the map figure, detail figures, insertion block, shared setup rules, element counts by status, conditional placements not drawn, ambiguities logged for an owner decision, and status (`drawn` or `blocked-by-ambiguity` where one element cannot be drawn without inventing a rule).
- Visual grammar additions (maps only): water (waves), slippery (dashes) and a neutral grey "Impassable or Blocking, decided per piece" (2.9.1) swatch; hazard marker (grey square with "!"); other marker (white square with dot); Party A zone has a solid black edge band, Party B an open band, and a zone both parties share a black band with white dashes.
