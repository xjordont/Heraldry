# Heraldry publication contract

Product and design requirements for the book, player aids, and Hero records. Everything ships as digital PDFs. Agent rules and checks are in `AGENTS.md`; commands are in `docs/AGENT_OPERATIONS.md`. Paths are relative to the repository root. Resume from `production/STATE.md` rather than restarting completed work.

The design document is `docs/DESIGN.md` (page grammar, type, components, art placement, and the typesetting policy), with `docs/ART_DIRECTION.md`, `docs/VISUAL_QA.md`, and `config/design_tokens.json`. Apply the established system consistently; don't redesign it piecemeal or produce galleries of unrelated alternatives.

## Source fidelity

- The active manuscript is the newest immutable snapshot in `source/versions.json`; `config/production.json` must agree. RC484 is the preserved original, not the authority after a revision. Restore a missing snapshot only from its recorded hash. Never use a historical manuscript or simulator as an alternative authority.
- Preserve every rule, qualifier, exception, number, table cell, named entry, scenario, appendix, and intentional reference summary. Don't shorten or rebalance the game to fit the book. Keep the source's section numbering and exact game terms, and never double-number a heading the source already numbers. Keep emphasis that carries game meaning. Don't invent mechanics or import rules from other games.
- Conversion is deterministic: Markdown, a semantic model from a real Markdown parser, custom Typst components, PDF. Never regenerate prose or retype tables with an LLM. Layout decisions live in templates and sidecar metadata, never in rewritten text. An unsupported Markdown construct fails the build; nothing is silently dropped.
- Layout, front matter, navigation, original illustrations, rules-faithful worked examples, and diagrams are authorized additions. Text changes, including mechanical copyedits, go only through an approved RC (`docs/WORKFLOW.md`); hidden publication-only text patches are prohibited (`editorial/patches.json` stays empty).
- Only an approved manuscript text batch creates a new RC. Artwork, figures, layout, tooling, and docs never change the RC number.
- When the source genuinely contradicts itself, keep the text, record the evidence, ask the owner, and carry on with other work. Never settle it by choosing an interpretation. An unresolved material contradiction blocks an unconditional content PASS.
- `docs/CANON_AUTHORITY.md` records the owner's 2026-10-15 conventions, which override older imported briefs on those points. Never treat a historical review's RC number as the active version.
- The owner's reference books are background inspiration only. Never take their mechanics, terminology, art, fonts, layouts, or icon systems.

## Work tracks

| Track | Authoritative files | Versioning |
|---|---|---|
| Manuscript text | `source/versions.json`, immutable `source/Heraldry_RC###.md`, `editorial/history/RC###.json` | One new RC per approved text batch |
| Atmospheric artwork | `production/art/ART_MANIFEST.json`, `production/art/SELECTIONS.json`, `assets/art/`, `production/art/` | Git commits; fit and repagination at the next requested build |
| Rules figures | `figures/src/`, `figures/out/`, their manifests and review ledger, `config/figure_dependencies.json` | Git commits; a changed figure, caption, or dependent rules section needs a fresh look |
| Layout and publishing | `typst/`, `config/design_tokens.json`, `tools/`, `editorial/how_to_use.json` | Git commits; PDF review at the next requested build |

Layout iteration follows `docs/LAYOUT_WORKFLOW.md`.

## Format

- Portrait US Letter pages (612 × 792 pt) throughout, in a warm cream page colour that reaches every edge. Text, folios, and figure geometry stay at least 0.375 in inside every edge. No landscape pages or spreads.
- The digital edition carries its own covers: the front cover is page 1 and the back cover the last page. Cover lettering is live vector type over the art, never lettering drawn by an image model.
- Searchable vector text with embedded fonts. Never rasterize the book. Don't claim PDF/A or PDF/UA conformance without real validation.
- Fonts are the bundled open-licence files in `fonts/`, with their licences; system fonts are never used. Essential text is at least 9 pt (`type_pt.minimum_essential`). Never fix overflow by shrinking type, tightening tracking, or switching to a condensed face.

## Pagination: the one-page keep rule

This is the full statement of the owner's mandatory rule (2026-10-07); other documents point here. It overrides any softer "where practical" keep wording.

Every complete scenario, section or subsection, table, example, procedure, stat profile, or reference entry that fits within one empty usable page at its approved layout width must occupy exactly one page. Its measured group includes its heading, all nested content, caption, legend or deployment diagram, and necessary notes. If the remaining space is too small, move the whole unit to the next page; never split it to fill space or balance columns. A column limit is not proof that a unit cannot fit: use the approved full-width layout where appropriate. Keep type legible and all content present.

- Measure rendered height, not manuscript length. A section runs from its heading to the next heading of equal or higher rank; a scenario runs to the next scenario or enclosing-section boundary. Fit uses the empty usable frame after margins, running furniture, and required spacing, with a small conservative tolerance.
- Fit-capable children stay intact inside a longer parent. Only a genuinely over-height unit may continue, with repeated table headers or an identifying continuation, and its source ID, measured size, and reason are recorded.
- Artwork never displaces or fragments a fit-capable rules unit; move the art instead. Never shrink type, omit notes or maps, clip content, or pad a unit to evade the rule. White space left by moving a whole unit is acceptable.
- The build's keep audit is bound to the exact inputs and PDF hash. It covers every applicable unit with its measured height, fit class, and actual pages. A fit-capable unit on more than one page, or missing audit coverage, fails the build.

## Tables

- Treat every table as structured data with a stable ID, source span, heading context, headers, alignment, and cell hashes, rendered through one coherent family of components. Every table has the black header band (owner, 2026-10-12; `docs/DESIGN.md` 6.10); never rely on tint or colour alone to show grouping.
- Size columns from content roles and rendered measurements: long rules prose gets most of the width, and dice notation, short values with units, and modifiers stay together. Respect explicit `<br>` lines. Keep footnotes, lead-ins, and the rules below a table with it.
- For a difficult table use, in order: rebalance widths and padding; go full width; split at natural row groups with repeated headers and a continued marker; recast rows as labelled cards with every header mapped to a field; then keyed portrait continuation panels with all columns. Never split column groups without repeated unique row keys. Keep every column meaning and row relationship in a machine-readable mapping.
- Keep ordinary rows intact. Preserve row order and range coverage in random tables. No ellipses, cropped columns, missing rows, duplicated entries, shifted cells, or unlabelled continuations.
- Reconcile every source cell against the render input and the published representation, including cards; repeated headers and row keys are layout duplication, distinct from duplicated data. Keep an all-table audit (source ID, output pages, representation, status), and look at every table family, every exceptional table, and every page transition of a multipage table.

## Rules figures

- Editable SVG or native vector diagrams, generated from code, never by an image model, in one grayscale-safe grammar: combatant and base symbols, allegiance shapes and hatching, terrain patterns, line types, arrows, dimensions, numbered steps, and legends. No colour-dependent meaning. Labels are at least 9 pt at final size. Mark schematic diagrams as such; never draw false scaled dimensions.
- Each figure has an ID, source references, an instructional purpose, a geometry or data specification, an editable file, a caption, an insertion target, and a semantic review status (`figures/README.md`).
- Use actual rule terms and source values. A worked example shows its assumptions, legal actions, arithmetic, timing, and outcome, with every number verified. A figure or caption never creates a rule, reveals hidden information, changes random determination, or drops an exception. Where the source is ambiguous, draw only the uncontested part and log the point.
- Coverage follows the mechanics the source provides, including every distinct deployment configuration; similar scenarios may share a validated diagram. Appendix A and B figures show only their own rules, never advanced rules.

## Artwork

- Only approved art is placed (`tools/build_book.py`). Owner-authored prompts in `production/art/OWNER_PROMPTS.json` are used verbatim. Art is generated through the owner's ChatGPT plan with no paid image API; the route is in `docs/ART_AUTOMATION.md`.
- Preserve native masters unchanged and make derivatives separately. Placed rasters are at least 300 ppi at placed size (`tools/check_art_ppi.py` checks every release PDF); changing a DPI tag or resampling does not add real detail, so place a small image smaller.
- Never fill a missing or failed image with commercial reference art or procedural silhouettes. Record the exact asset that needs repair and continue the rest of the work.
- Generated images are recorded as AI-generated in the intake records, never described as hand-drawn; the book carries no illustration credit (owner, 2026-10-29). Make no invented licence or exclusivity claims. Atmospheric art never establishes rules or deployment geometry.

## Front matter, navigation, index, and covers

- A designed title page, a restrained colophon using only verified information, version identification, a short "How to use this book" drawn from the book's structure (`editorial/how_to_use.json`), and an automatically paginated, linked contents. Never invent an ISBN, publisher, contributor, endorsement, copyright holder, or licence, and never print placeholder legal text.
- The active RC is explicit in the PDF metadata, covers, and filenames.
- The manual Markdown contents is replaced only through a documented navigation substitution. Internal anchors use stable source IDs, including duplicate and unnumbered headings. Bookmarks are hierarchical, never every heading in one flat list. Folios, page labels, links, and section references stay coherent.
- The index is a curated subject index (game terms, conditions, actions, terrain, classes, ancestries, equipment, Powers, Monster rules, scenarios, and campaign concepts, with subentries and see or see-also references), not a word list. Locators come from tagged targets in the final layout, with the term-to-source-to-page mapping kept for audit.
- Back-cover copy is accurate and short (`editorial/back_cover.json`).

## Verification

A successful compile proves only that a file exists. Use deterministic checks plus looking at the pages.

- **Content:** the source hash, complete block and heading coverage, exact numbers and rule tokens, every table cell and transformed field, special characters and inline emphasis, and links and section references. Use source-ordered block mapping, not word counts or spot searches; PDF text extraction is a cross-check only. Document every normalisation (whitespace, discretionary hyphens, running furniture, repeated headers, the replaced contents).
- **Layout:** no content outside the safe area, clipping, overlap, missing glyphs, undersized essential text, detached headings or captions, unexpected blank pages, split profiles, failed table continuations, or overset text. Geometry scripts are detectors, not proof. Look at every review image (`docs/BUILD_AUTOMATION.md`), then every flagged, dense, or exceptional page, every figure, and both covers, and recheck changed and repaginated pages after a repair.
- **Figures:** check every geometry or data specification and caption against its source slice: distances, timing, eligibility, allegiance, AP costs, resolution order, and arithmetic.
- **Navigation:** every contents entry, bookmark, link, index locator, and cross-reference resolves to the right place in the digital PDF and its screen companion. Rebuild to a stable page map; never deliver stale or oscillating locators.
- **PDF:** every page is 612 × 792 pt portrait with the page colour to every edge, fonts are embedded, essential text meets the minimum, and placed art meets its resolution.

Failed mandatory verification fails the verify command and blocks the release. Blocked external inputs stay visible as blocked, never as passing.

## Releases

- Each requested build is published as a GitHub Release (`docs/BUILD_AUTOMATION.md`): the digital PDF with its covers, linked contents, bookmarks, index, figures, and approved art; its screen companion (150 ppi rasters, same pages and links); the player aids; the blank Hero record and the 24 Basic Mode Heroes; the specimen; the release ZIP; and `SHA256SUMS.txt`. Never truncate or silently omit a deliverable.
- The release ZIP is the rebuildable source package: instructions, pinned dependencies, sources, fonts and licences, figures, ink art, manifests, and evidence ledgers. It excludes credentials, caches, raw generated art, style references, and review images.
- `dist/` and its ledgers describe the last requested build, so never present them as current once the source has moved on. Record release status, including missing art, in `production/STATE.md`, keeping PASS, FAIL, BLOCKED, NOT TESTED, and NOT APPLICABLE distinct. Never claim "perfect", "fully illustrated", or "certified" beyond the evidence.
