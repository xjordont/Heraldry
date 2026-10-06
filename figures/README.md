# Rules diagrams (RC484)

Nineteen editable SVG diagrams for the Heraldry Skirmish rulebook, generated deterministically from code (stdlib only).

Regenerate everything (SVGs, `manifest.json`, `placements.json`) and run all checks:

    python3 figures/src/make_figures.py          # all figures
    python3 figures/src/make_figures.py FIG-07   # SVG subset only (no manifest rewrite)

Files

- `src/svgkit.py` shared visual grammar (tokens, terrain patterns, arrows, callouts, legend, grid helpers, text metrics from `src/fontmetrics.json`).
- `src/fig_seq.py`, `fig_spatial.py`, `fig_monster.py`, `fig_scen.py`, `fig_misc.py` figure drawings; `src/figdata.py` IDs, captions, insertion targets, source references, semantic checks.
- `out/FIG-NN.svg` outputs, 1 user unit = 1 pt, width 504 pt (all figures are `full` scope), Source Sans 3 text of 9 pt or more, grayscale only, no raster or external references.
- `manifest.json` one record per figure; `placements.json` maps block id to `[{id, caption, width, scope}]`, inserted immediately after that block.

Checks run by `make_figures.py`: geometry and arithmetic assertions behind the manifest's semantic checks, SVG validation (grayscale colours, font size >= 9, stroke >= 0.5, no images or hrefs, widths), and placement validation (block exists in `build/blocks.json`, is a top-level paragraph or list, is not in Appendix C, caption ends with a section reference and has at most 3 sentences).

Visual inspection: `python3 figures/src/test/render.py FIG-01 FIG-02 ...` renders PNGs through Typst into `figures/src/test/` (git-ignored; safe to delete).

Visual grammar: Party A = black circle; Party B = white circle with centre dot; Monster = hatched hexagon (hatched square for Large); Blocking = solid dark gray; Cover = cross-hatch; Difficult = dot stipple; Impassable = dense diagonal hatch; solid arrow = movement or permitted; dashed = line of sight; dotted = forced movement; arrow ending in X = not permitted; numbered black circles = steps. Diagrams that are not to scale carry "Schematic — not to scale"; inch values shown are only values the source states.
