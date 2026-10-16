# All-figure review and repairs - RC493

Completed 2026-10-16 under the owner's instruction to review and apply figure fixes for readability, clarity, accuracy, and design. All **57 figures** received a fresh comparison with the active rules and actual rendered inspection. **25 SVGs and 9 captions changed.** The four previously open figure-copy findings are resolved.

The manuscript remains RC493, SHA-256 `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`. Figure work did not change mechanics or create a new manuscript revision.

## What changed

- Instructional diagrams now retain the existing activation exceptions, flat mitigation and damage-type order, Cover and visibility exceptions, Aura source/footprint distinction, and the party's only-Hero Trail exception. AI text and captions retain explicit continuation and this-activation targeting conditions. The teaching Dodge declaration now precedes damage. All original worked dice, AP, HP, and scoring results remain intact.
- Diagram typography follows the manuscript's character lock. Local keys explain Awake/Resting suffixes. The shared key separates Large/Huge swatches and explains group and arrival labels. Regeneration removes duplicated phase-badge overdraw from the checked-in FIG-01 SVG.
- Crowded labels, overlapping Tarantulas, a platform ruler, an Unstable-area label, and the Vault's door markers are clearer. The Command Tent entrance now reads as Open. The variable Pressure Plate setup is explicitly identified as undrawn. An unsupported G2 patrol position was removed from FIG-51; its required Resting/patrol instruction remains in a note without inventing a water boundary.
- Raised islands and hummocks now interrupt surrounding water hatching. FIG-53 distinguishes Difficult deep mud from illustrative Shallow Water pools instead of depicting the whole Fen as water. FIG-55's final caption no longer strands a short reference fragment.
- The shared key distinguishes Tabletop closest-point measurement from Grid measurement. The setup template identifies its rounded exclusions as Tabletop geometry, gives the Grid procedure, separates edge and zone clearances, and keeps exclusion hatching visible inside deployment zones.

## Review evidence

| Coverage | Inspection and record |
| --- | --- |
| FIG-01 to FIG-19 | Every final SVG and caption directly viewed at 504 pt/200 ppi; source comparison, per-figure observations and exact bindings in [core review](figure-review-core-rc493.md) and [JSON evidence](figure-review-core-rc493.json). |
| FIG-20 and FIG-57 | Final diagrams and captions directly viewed at 504 pt/200 ppi after repairs; [key/template review](figure-review-key-template-rc493.md). |
| FIG-21 to FIG-56 | All 36 final maps directly viewed individually at 243 pt/144 ppi, with active scenario and shared-rule comparison; [map review](figure-review-maps-rc493.md). |
| All 36 map captions | Integration owner additionally viewed every complete map-plus-caption specimen at 243 pt/200 ppi; [caption review](figure-review-map-captions-rc493.md). |

The Codex integration owner and two delegated reviewers performed the work. The reviewers also made repairs; this is not an independent human proof. Historical findings and actual source limitations remain recorded. These include schematic proportions, representative terrain/counts, unfixed placement choices, and source ambiguities the figures expressly qualify. They are not silently converted into new rules.

The previews use native SVG widths of 504 pt and 243 pt. Current v4 template frames are 518.4 pt full width and 250.56 pt per column, so normal 100% placement enlarges these diagrams slightly. Native-width inspection is conservative for label size. Caption text was reviewed at the production 9 pt size. These source dimensions do not constitute final PDF-placement evidence.

`figure-semantic-review.json` binds all 57 current SVG, caption, and dependent-rule hashes to actual observations and viewed PNG hashes. A separate reproduction check compiled each current SVG through its inspection wrapper and reproduced all 57 inspected images byte-for-byte. The additional 36 caption specimens have their own recorded hashes.

## Validation and delivery limits

The figure generator's geometry/arithmetic assertions, glyph registry, source-distance citations, label/terrain checks, placement/caption checks, and visible-typography validation pass. Essential text remains at least 9 pt at the intended width. A font-metric scan found no text outside any figure canvas. Automated checks support the image review; they do not replace it.

Dependency coverage now includes the activation, mitigation, measurement, and terrain passages these figures explain. Source-bound scenario coverage metadata identifies RC493 and its hash. SVG/JSON generation uses explicit LF line endings, and subset generation initializes the geometry needed by its checks.

Baseline and final `python tools/dev.py check` both pass: 190 tests run each time with 3 expected empty-art-queue skips, plus exact dependency checks, baseline contracts, immutable source/history protection, and whitespace. Fresh scratch generation reproduces all 57 SVGs and both metadata files byte-for-byte. The final figure gate passes 57/57 with no stale entries, missing reviews, open major findings, or open minors. Original source snapshots and the previous release's PDF, visual, package, and gate records remain unchanged.

No book PDF was built or released. Last delivery remains **RC492-build-37**. Final figure placement, downstream pagination, PDF accessibility, and physical reproduction require their own review at the next requested build. Physical print: **NOT TESTED**.
