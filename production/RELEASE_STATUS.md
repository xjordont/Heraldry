# Release status — Heraldry Skirmish RC485, art-light edition

Evidence: production/qa/STATUS.json and production/build-provenance.json. Active revision: source/versions.json. Original RC484 remains unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| Manuscript workflow | PASS | RC485 contains P-01–P-07; approved patch archive, immutable parent/hash chain and exact snapshot reconstruction; future batches increment once |
| Repository workflow | PASS | Main policy consistent across brief, agents and setup; 12 regression tests; GitHub preflight/tests and append-only history checks added |
| Automated release gate | PASS | 18 checks bound to current source/code/assets/generated files and six PDF hashes; crashes/stale reports cannot pass |
| Content integrity | PASS (automated scope) | 8,426 text blocks in order, none missing/out of order/duplicated; 332 tables, 10,341 cells, 22,800 strong and 449 italic runs; bundled fonts only |
| Navigation | PASS | 228 index entries; 551 bookmarks and 1,259 internal links resolve in each print interior |
| Instructional figures | PASS (review scope) | 57 figures: 19 rules diagrams + FIG-20 legend, 36 scenario deployment maps (FIG-21..56), 10.1 template (FIG-57); independent hash-bound review, 0 open critical/major, gate PASS. Scenario coverage `qa/scenario-coverage.json`: 36/36 mapped, 15 logged ambiguities, 4 maps with an undrawn element pending owner decision |
| Visual QA | PASS (scoped) | All 450 interior pages of the current cream PDF on contact sheets; detail pages of maps, template, legend, glossary and stat cards; ledger bound to PDF hash |
| Inkjet files | PASS | Cream/white exact portrait Letter with identical pagination, edge-to-edge substrate, safe essential text and embedded fonts; calibration repaired/reviewed |
| Prior build reproducibility | PASS (historical) | Repeated clean builds give identical interior/digital/cover bytes; fixed revision timestamp; prior archive had unique verified entries/checksums; current archive withheld until rebuild |
| Atmospheric artwork masters | READY; INTEGRATION PENDING | Cover and eleven chapter masters generated in ChatGPT Work; integration and final-size review required |
| Physical printer proof | NOT TESTED | No actual printer/paper sheets examined |
| Complete rules contradiction audit | NOT TESTED | Existing triage and figure reviews do not cover every possible manuscript inconsistency |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |

Digital: 453 pages. Interiors: 450 each. Specimen: 13 pages. Visual review is not glyph-level proofreading; normalized table-cell/mapping checks do not prove every rule's meaning. Missing author, publisher, ISBN and copyright-holder metadata stays unset.

## Owner-requested design refinement — 2026-10-07

PENDING IMPLEMENTATION AND VISUAL REVIEW. The owner requests a less plain illustrated design and better heading/table flow. docs/DESIGN_REFINEMENT.md records the actual-page/code findings and required next iteration; docs/ART_AUTOMATION.md records GPT routes. Historical PASS rows above retain their stated scope and do not certify these new requirements. The artwork checkpoint supplies twelve native masters and updated instructions; dist PDFs and RC485 are unchanged. Read production/art/HANDOFF.md. The new illustrated/design edition and its release package require a fresh build and visual review. Atmospheric artwork is generated in ChatGPT Work; InDesign export is on hold.
