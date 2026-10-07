# Second-pass deployment review

Review date: 5 October 2026. This records a separate self-review of the completed prompt/configuration package. It is not an independent external audit, a rules audit of the full manuscript, or validation of a future rendered book.

## Findings addressed in the final package

| Potential failure | Resolution |
|---|---|
| A generic prompt fails to reflect the source scale | Actual manuscript counts, constructs, 11 chapters/three appendices, and widest tables are recorded; semantic parsing must recalculate acceptance counts. |
| LLM conversion silently changes the finalized rules | Immutable supplied source, checksum, separate patches, block coverage, cell hashes, and output mappings are mandatory. |
| Everything defaults to one model | Full 5.5 IDs, ready Sonnet agent files, effort controls, explicit roles, and verification of actual model resolution. |
| Cheap models are given unsupported controls or consequential reviews | Haiku gets no effort field and only mechanical tasks; semantic/source/diagram QA uses Sonnet high. |
| Parallel agents overwrite shared styles | Two-worker limit, disjoint ownership, single shared-template owner, orchestrator integration. |
| Subtasks silently use independent API sessions | Native cloud subagents preferred; nested CLI/API sessions are explicitly discouraged. |
| Claude is assumed to generate raster illustrations natively | Separate configured/supplied/fallback art routes, supported image-service requirement, and honest art completion state. |
| Procedural ornaments masquerade as final illustrations | Atmosphere and vector diagrams have separate definitions and acceptance states. |
| Assets lose style consistency or lack print detail | Style anchor, repeated attributes/reference mechanism, contact sheets, native/effective resolution, bounded retries, final-size inspection. |
| Tall/wide tables clip or become microscopic | Content-based widths; full-page, keyed portrait continuation, or faithful cards; 9 pt essential-text minimum; all-cell reconciliation. |
| Random-table row relationships are damaged | Range/order checks, repeated keys on split representations, explicit transformed-field mapping. |
| Diagrams change the game | Source-linked geometry, timing/AP checks, verified examples, all distinct deployment coverage, independent review. |
| TOC/index look finished but contain stale page numbers | Stable tagged targets, final locator validation, rebuild-to-convergence, page labels/bookmarks. |
| The index is only an alphabetical TOC | Curated subjects/subentries/synonyms and authoritative definitions/significant uses. |
| Missing metadata becomes fabricated credits/legal claims | Unknown author/publisher/ISBN/legal data remain null in production configuration. |
| Generic PDF export is falsely called printer-certified | Typst PDF/A vs PDF/X distinction, suitable export/validation path, post-conversion inspection, printer-specific states. |
| Spine width is guessed | Actual stock/binding/page-count template required; panels and parametric candidate delivered otherwise. |
| Automated geometry checks are equated with visual review | All-page render/contact-sheet inspection, detailed flagged/exceptional page review, actual viewed-file ledger. |
| “Never stop” becomes infinite retries or false completion | Bounded repairs, persistent state, continued independent work, honest runtime/external blockers. |
| A prototype is returned as the whole result | Full reading PDF, print status, cover, editable sources, manifests, QA evidence, archive required. |

## Remaining dependencies at deployment

- The cloud account must actually expose the selected models, effort fields, runtime and network paths. The prompt verifies these; it does not grant access.
- The fully illustrated edition requires the ChatGPT Work originals to be integrated and reviewed.
- Physical home-inkjet proof needs the actual device/media; the specified borderless file can be completed independently. Commercial submission/wrap requirements apply only to a separately requested edition.

## Package checks performed before delivery

The local validation checks parse production/settings JSON; parse agent YAML; verify source bytes/hash against the attachment; confirm model/effort selections, and cross-file dependencies; check presence of every required prompt topic; inspect archive integrity; and verify that no credentials or generated-book claims were bundled. These validate the launch kit, not execution inside the user's Claude account.

## Version 2 reference integration review

- Design roles assigned explicitly; visual references never become mechanics authorities.
- Mandatory design specification; optional hash-verified image evidence; missing references do not halt production.
- Six primary books / 14 PDF pages; three optional secondary books / five additional pages.
- All 32 supplied PDF copies represented in inspection inventory; 29 unique SHA-256 hashes.
- No commercial PDFs or page images in the kit. Local reference renders ignored by Git and excluded from final publication/release assets.
- Source manuscript bytes unchanged; typography and all-table fidelity contracts retained.
- Reference extraction tested with the supplied editions; specimen and future book completion remain execution work.

## Final launch audit, 2026-10-06

- Added runnable standard-library preflight with source/hash, config, five-agent, manifest, required-file, and script-syntax checks.
- Added explicit initial/resumed-run contracts so legitimate production edits do not falsely invalidate baseline checks.
- Added launch checklist and initial NOT STARTED state.
- Removed speculative cloud Bypass-permission guidance; documented the cloud GitHub-proxy restriction affecting unrelated release downloads.
- No reference PDF upload is required. Original illustration assets, printer inputs, and live account/model access remain external inputs.
- Scope: prepared assignment readiness; no generated publication, cloud dependency installation, or live account operation is certified.
- Preflight validation passed on the pristine kit; deliberate manuscript mutation, and baseline tampering were rejected. A legitimate state update passed the resume check.

## Borderless/light-style and single-prompt review, 2026-10-06

- User-specified borderless portrait Letter replaces the earlier generic non-bleed profile throughout config, master prompt, design guide, agents and setup instructions.
- Cream/white companion files have identical content/pagination. All essential text/furniture remain safe despite edge-to-edge backgrounds; no landscape fallback or oversized bleed sheet.
- Added concrete design tokens and visible-quality acceptance rubric covering generic ornament, typography, tables, artwork construction/matting, and reader flow.
- Re-inspected attached reference compositions/details; recorded exact viewer pages and abstract adaptations without bundling source artwork.
- Added an actual PDF file checker and required inkjet calibration proof/instructions. Physical proof and commercial conformance are distinct from file readiness.
- Clarified single-repository cloud loading, supported dependency recovery, committed/pushed checkpoints, and resumable page-review batches.
- No book build or actual inkjet print has run. Live model access, network and optional image service still require capability discovery in Claude.
- File checker tests passed for valid embedded-font Letter output and rejected A4, landscape, unsafe edge text, undersized type, unembedded fonts, rotated/cropped pages and non-searchable output. Launch preflight rejected landscape/token mismatches and source mutation while permitting a legitimate state update.
