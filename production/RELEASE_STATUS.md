# Release status — Heraldry Skirmish RC486, illustrated edition

Evidence: production/qa/STATUS.json and production/build-provenance.json. Active revision: source/versions.json. Original RC484 remains unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| Manuscript workflow | PASS | RC486 contains P-01–P-12 (P-08..P-12 resolve the four unplaced scenario elements); approved patch archive, immutable parent/hash chain and exact snapshot reconstruction; future batches increment once |
| Repository workflow | PASS | Main policy consistent across brief, agents and setup; 12 regression tests; GitHub preflight/tests and append-only history checks added |
| Automated release gate | PASS | 19 checks bound to current source/code/assets/generated files and six PDF hashes; crashes/stale reports cannot pass |
| Content integrity | PASS (automated scope) | 8,426 text blocks in order, none missing/out of order/duplicated; 332 tables, 10,341 cells, 22,800 strong and 449 italic runs; bundled fonts only |
| One-page keeps | PASS | Mandatory hash-bound audit `qa/keep-audit.json`: 1833 units measured from rendered height, 1538 fit-capable, 0 split across pages, 0 missing coverage; 295 over-height units continue with intact children |
| Navigation | PASS | 228 index entries; 551 bookmarks and 1,259 internal links resolve in each print interior |
| Instructional figures | PASS (review scope) | 57 figures: 19 rules diagrams + FIG-20 legend, 36 scenario deployment maps (FIG-21..56), 10.1 template (FIG-57); independent hash-bound review, 0 open critical/major, gate PASS. Scenario coverage `qa/scenario-coverage.json`: 36/36 mapped, all elements placed (RC486); 0 open majors and 0 open minors (4 minors accepted with reasons) |
| Visual QA | PASS (scoped) | All 596 interior pages of the current clean-build cream PDF on contact sheets; covers, art crop, scenario openings, index; ledger bound to PDF hash |
| Inkjet files | PASS | Cream/white exact portrait Letter with identical pagination, edge-to-edge substrate, safe essential text and embedded fonts; calibration repaired/reviewed |
| Prior build reproducibility | PASS (historical) | Repeated clean builds give identical interior/digital/cover bytes; fixed revision timestamp; prior archive had unique verified entries/checksums; current archive withheld until rebuild |
| Atmospheric artwork | PASS (scoped) | Cover and eleven chapter masters placed at native 300 ppi and reviewed on the built pages |
| Physical printer proof | NOT TESTED | No actual printer/paper sheets examined |
| Complete rules contradiction audit | NOT TESTED | Existing triage and figure reviews do not cover every possible manuscript inconsistency |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |

Digital: 599 pages. Interiors: 596 each. Specimen: 13 pages. Visual review is not glyph-level proofreading; normalized table-cell/mapping checks do not prove every rule's meaning. Missing author, publisher, ISBN and copyright-holder metadata stays unset.

## Owner-requested design refinement — 2026-10-07

IMPLEMENTED IN THE RC486 BUILD: twelve ChatGPT Work masters placed, mandatory one-page keeps enforced, scenario diagrams unified with a shared key, and all 596 pages visually inspected. docs/DESIGN_REFINEMENT.md and production/art/HANDOFF.md record the requirements. Appendix A–C openers have no illustration. InDesign export is on hold.
