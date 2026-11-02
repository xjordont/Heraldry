# Heraldry publication contract

Product and design requirements for the book, player aids, and Hero records. Agent rules and checks are in `AGENTS.md`; commands are in `docs/AGENT_OPERATIONS.md`. Paths are relative to the repository root.

`MASTER_PROMPT.md` is the standing production and design brief. Resume the project from `production/STATE.md` rather than restarting completed work.

## Source fidelity

- Preserve every source rule, exception, number, and table cell. Conversion is deterministic; never regenerate prose with an LLM.
- Only an approved manuscript text batch creates a new RC (`docs/WORKFLOW.md`). Artwork, figures, layout, tooling, and docs never change the RC number.
- `docs/CANON_AUTHORITY.md` records the owner's 2026-10-15 conventions, which override older imported briefs on those points. Never treat a historical review's RC number as the active version.

## Work tracks

| Track | Authoritative files | Versioning |
|---|---|---|
| Manuscript text | `source/versions.json`, immutable `source/Heraldry_RC###.md`, `editorial/history/RC###.json` | One new RC per approved text batch |
| Atmospheric artwork | `production/art/ART_MANIFEST.json`, `assets/art/incoming/`, `production/art/` | Git commits; fit and repagination at the next requested build |
| Rules figures | `figures/src/`, `figures/out/`, their manifests and review ledger, `config/figure_dependencies.json` | Git commits; a changed figure, caption, or dependent rules section needs a fresh look |
| Layout and publishing | `typst/`, `config/design_tokens.json`, `tools/`, `editorial/how_to_use.json` | Git commits; PDF review at the next requested build |

## Design

- Apply `docs/DESIGN_SPEC.md`, `docs/ART_DIRECTION.md`, `docs/INKJET_PRINT.md`, `docs/VISUAL_QA.md`, and `config/design_tokens.json`. `docs/DESIGN_REFINEMENT.md` holds the owner's latest design and pagination decisions.
- Clean dark fantasy, borderless portrait US Letter, a near-white cream edition and a white companion, with essential content at least 0.375 in inside the edges.
- Pagination: any complete scenario, section, subsection, table, procedure, or reference entry that fits on one empty usable page stays on one physical page with its heading, diagram, caption, and notes. Move it whole when the remaining space is too small. The keep audit fails the build on an avoidable split. Never shrink type or drop content to make something fit.
- Layout iteration follows `docs/LAYOUT_WORKFLOW.md`.

## Artwork

Only approved art is placed (`tools/build_book.py`). Owner-authored prompts in `production/art/OWNER_PROMPTS.json` are used verbatim. Routes are in `docs/ART_AUTOMATION.md`. The Gemini pipeline (`tools/art_generate.py`) is retired; use it only on the owner's instruction.

## References

Use only the ten owner-selected titles in `references/sample_pdfs.json` (Git LFS under `references/private/pdfs/`; see `references/README.md`), as visual inspiration for layout and art. Add no other books without the owner's instruction. Keep their bytes out of every publication package, and keep the repository private.

## Releases

Each requested build is published as a GitHub Release (`docs/BUILD_AUTOMATION.md`). `dist/` and its ledgers describe the last requested build, so never present them as current once the source has moved on. `production/RELEASE_STATUS.md` records release status, including missing art and physical print status. The optional InDesign export (`docs/INDESIGN_EXPORT.md`) runs only when the owner asks.
