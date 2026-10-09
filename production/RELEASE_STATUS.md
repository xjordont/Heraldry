# Release status — Heraldry Skirmish RC486, illustrated edition

Evidence: production/qa/STATUS.json and production/build-provenance.json. Active revision: source/versions.json. Original RC484 remains unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| Manuscript workflow | PASS | RC486 contains P-01–P-12 (P-08..P-12 resolve the four unplaced scenario elements); approved patch archive, immutable parent/hash chain and exact snapshot reconstruction; future batches increment once |
| Repository workflow | PASS (2026-10-09 scope) | 15 regression tests and 8 preflight baseline checks pass; immutable history reconstructed; dependency installation fixed before CI tests |
| Automated release gate | PASS (recorded build scope) | Historical 19-check build evidence remains bound to its recorded input/PDF hashes; no full release rebuild or gate reapproval during this audit |
| Content integrity | PASS (automated scope) | 8,426 text blocks in order, none missing/out of order/duplicated; 332 tables, 10,341 cells, 22,800 strong and 449 italic runs; bundled fonts only |
| One-page keeps | PASS | Mandatory hash-bound audit `qa/keep-audit.json`: 1833 units measured from rendered height, 1538 fit-capable, 0 split across pages, 0 missing coverage; 295 over-height units continue with intact children |
| Navigation | PASS | 228 index entries; 551 bookmarks and 1,259 internal links resolve in each print interior |
| Instructional figures | PASS (review scope) | 57 figures: 19 rules diagrams + FIG-20 legend, 36 scenario deployment maps (FIG-21..56), 10.1 template (FIG-57); independent hash-bound review, 0 open critical/major, gate PASS. Scenario coverage `qa/scenario-coverage.json`: 36/36 mapped, all elements placed (RC486); 0 open majors and 0 open minors (4 minors accepted with reasons) |
| Visual QA | PASS (scoped) | All 596 interior pages of the current clean-build cream PDF on contact sheets; covers, art crop, scenario openings, index; ledger bound to PDF hash |
| Inkjet files | PASS | Cream/white exact portrait Letter with identical pagination, edge-to-edge substrate, safe essential text and embedded fonts; calibration repaired/reviewed |
| Prior build reproducibility | PASS (historical) | Repeated clean builds give identical interior/digital/cover bytes; fixed revision timestamp; prior archive had unique verified entries/checksums; current archive withheld until rebuild |
| Atmospheric artwork | PASS (scoped) | Cover and eleven chapter masters placed at native 300 ppi and reviewed on the built pages |
| Physical printer proof | NOT TESTED | No actual printer/paper sheets examined |
| Complete rules contradiction audit | COMPLETE — OPEN FINDINGS | [2026-10-09 audit](qa/manuscript-contradiction-audit.md): 21 open findings and 6 isolated uncertainties; exact candidates are proposed, source unchanged |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |

Digital: 599 pages. Interiors: 596 each. Specimen: 13 pages. Visual review is not glyph-level proofreading; normalized table-cell/mapping checks do not prove every rule's meaning. Missing author, publisher, ISBN and copyright-holder metadata stays unset.

## Owner-requested design refinement — 2026-10-07

IMPLEMENTED IN THE RC486 BUILD: twelve ChatGPT Work masters placed, mandatory one-page keeps enforced, scenario diagrams unified with a shared key, and all 596 pages visually inspected. docs/DESIGN_REFINEMENT.md and production/art/HANDOFF.md record the requirements. Appendix A–C openers have no illustration. InDesign export is on hold.

## Manuscript audit checkpoint — 2026-10-09

Active RC486 SHA-256: `5da05cec6153ac11865874a0da416c002ce90b2dc4936fc9ce50abca9d3dbbe5`. All chapters and Appendices A–C received a mechanical contradiction review. This completed audit does not clear the manuscript: unresolved rules procedures, scenario instructions and teaching-example errors remain. [Findings JSON](qa/manuscript-contradiction-audit.json) retains exact evidence lines and limits; [verification JSON](qa/manuscript-contradiction-verification.json) records reproducible bounded checks. [Candidate RC487 batch](../editorial/proposals/rc487-contradiction-audit.json) has 13 proposed exact replacements; it supplies no new mechanics or unseen example dice.

No manuscript snapshot, revision registry, history archive, or PDF changed. Historical visual, figure, layout and artwork PASS entries above remain limited to their recorded evidence; they are not current semantic approval. Next manuscript repair requires approved exact patches, one new RC revision, recalculated examples, and affected figure/PDF reconciliation.
