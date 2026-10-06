# Second-pass deployment review

Review date: 5 October 2026. This records a separate self-review of the completed prompt/configuration package. It is not an independent external audit, a rules audit of the full manuscript, or validation of a future rendered book.

## Findings addressed in the final package

| Potential failure | Resolution |
|---|---|
| A generic prompt fails to reflect the source scale | Actual manuscript counts, constructs, 11 chapters/three appendices, and widest tables are recorded; semantic parsing must recalculate acceptance counts. |
| LLM conversion silently changes the finalized rules | Immutable supplied source, checksum, separate patches, block coverage, cell hashes, and output mappings are mandatory. |
| Design polish consumes the budget before the book is converted | A small stress specimen is followed by a complete book build before optional embellishment. |
| Everything defaults to costly Opus | Full 5.5 IDs, ready Sonnet agent files, effort controls, explicit roles, and verification of actual model resolution. |
| Cheap models are given unsupported controls or consequential reviews | Haiku gets no effort field and only mechanical tasks; semantic/source/diagram QA uses Sonnet high. |
| Parallel agents overwrite shared styles | Two-worker limit, disjoint ownership, single shared-template owner, orchestrator integration. |
| Subtasks silently use a separately billed API | Native cloud subagents preferred; nested CLI/API sessions are explicitly discouraged. |
| A textual budget is presented as a hard cap | $80 target/$20 reserve, actual vs estimated accounting, account controls, and checkpoint-on-exhaustion are distinguished. |
| Image APIs consume unintended funds | Default external budget zero; explicit authorization flag; credentials alone are not authorization. |
| Claude is assumed to generate raster illustrations natively | Separate configured/supplied/fallback art routes, supported image-service requirement, and honest art completion state. |
| ChatGPT Plus is mistaken for image API credit | Manual transfer explained; API billing separate; no speculative Plus bridge promised. |
| Procedural ornaments masquerade as final illustrations | Atmosphere and vector diagrams have separate definitions and acceptance states. |
| Assets lose style consistency or lack print detail | Style anchor, repeated attributes/reference mechanism, contact sheets, native/effective resolution, bounded retries, final-size inspection. |
| Tall/wide tables clip or become microscopic | Content-based widths; full-page, continuation, faithful cards, or justified landscape; 9 pt essential-text minimum; all-cell reconciliation. |
| Random-table row relationships are damaged | Range/order checks, repeated keys on split representations, explicit transformed-field mapping. |
| Diagrams change the game | Source-linked geometry, timing/AP checks, verified examples, all distinct deployment coverage, independent review. |
| TOC/index look finished but contain stale page numbers | Stable tagged targets, final locator validation, rebuild-to-convergence, page labels/bookmarks. |
| The index is only an alphabetical TOC | Curated subjects/subentries/synonyms and authoritative definitions/significant uses. |
| Missing metadata becomes fabricated credits/legal claims | Unknown author/publisher/ISBN/legal data remain null in production configuration. |
| Generic PDF export is falsely called printer-certified | Typst PDF/A vs PDF/X distinction, suitable export/validation path, post-conversion inspection, printer-specific states. |
| Spine width is guessed | Actual stock/binding/page-count template required; panels and parametric candidate delivered otherwise. |
| Automated geometry checks are equated with visual review | All-page render/contact-sheet inspection, detailed flagged/exceptional page review, actual viewed-file ledger. |
| “Never stop” becomes infinite retries or false completion | Bounded repairs, persistent state, continued independent work, honest runtime/budget/external blockers. |
| A prototype is returned as the whole result | Full reading PDF, print status, cover, editable sources, manifests, QA evidence, archive required. |

## Remaining dependencies at deployment

- The cloud account must actually expose the selected models, effort fields, runtime, credit balance, and network paths. The prompt verifies these; it does not grant access.
- The requested fully illustrated edition requires supplied assets or an already configured and authorized image service. Defaults do not spend external funds.
- Printer-specific submission readiness needs an actual printer profile and cover template matching binding, stock, and final page count.
- A $100 limit and a request for exhaustive perfection can conflict. The prompt prioritises a complete reproducible book and reserves repair credit, but no fixed-cost guarantee is made.

## Package checks performed before delivery

The local validation checks parse production/settings JSON; parse agent YAML; verify source bytes/hash against the attachment; confirm model/effort selections, budgets, and cross-file dependencies; check presence of every required prompt topic; inspect archive integrity; and verify that no credentials or generated-book claims were bundled. These validate the launch kit, not execution inside the user's Claude account.

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
- No reference PDF upload is required. Original illustration assets, printer inputs, and live account/model/credit access remain external inputs.
- Scope: prepared assignment readiness; no generated publication, cloud dependency installation, or live account operation is certified.
- Preflight validation passed on the pristine kit; deliberate manuscript mutation, budget mismatch, and baseline tampering were rejected. A legitimate state update passed the resume check.
