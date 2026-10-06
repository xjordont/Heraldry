# Release status — Heraldry Skirmish RC485, art-light edition

Evidence: production/qa/STATUS.json and production/build-provenance.json. Active revision: source/versions.json. Original RC484 remains unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| Manuscript workflow | PASS | RC485 contains P-01–P-07; approved patch archive, immutable parent/hash chain and exact snapshot reconstruction; future batches increment once |
| Repository workflow | PASS | Main policy consistent across brief, agents and setup; 12 regression tests; GitHub preflight/tests and append-only history checks added |
| Automated release gate | PASS | 18 checks bound to current source/code/assets/generated files and six PDF hashes; crashes/stale reports cannot pass |
| Content integrity | PASS (automated scope) | 8,426 text blocks in order, none missing/out of order/duplicated; 332 tables, 10,341 cells, 22,800 strong and 449 italic runs; bundled fonts only |
| Navigation | PASS | 228 index entries; 551 bookmarks and 1,259 internal links resolve in each print interior |
| Instructional figures | PASS (review scope) | 19 figures; prior independent reviews carried forward because RC485 equals the reviewed publication text; hashes also bind dependent sections; 0 open findings |
| Visual QA | PASS (scoped) | All 436 interior pages on 24-dpi contact sheets; five detailed pages, covers/calibration and one overscan page; actual hash/coverage recorded |
| Inkjet files | PASS | Cream/white exact portrait Letter with identical pagination, edge-to-edge substrate, safe essential text and embedded fonts; calibration repaired/reviewed |
| Reproducibility/package | PASS | Repeated clean builds give identical interior/digital/cover bytes; fixed revision timestamp; complete archive with unique verified entries/checksums |
| Atmospheric artwork | BLOCKED | 12 planned assets; no approved art or authorized paid service |
| Physical printer proof | NOT TESTED | No actual printer/paper sheets examined |
| Complete rules contradiction audit | NOT TESTED | Existing triage and figure reviews do not cover every possible manuscript inconsistency |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |
| Claude credit telemetry | NOT AVAILABLE | Existing estimates retained; this audit did not reset budget authorization |

Digital: 439 pages. Interiors: 436 each. Specimen: 13 pages. Visual review is not glyph-level proofreading; normalized table-cell/mapping checks do not prove every rule's meaning. Missing author, publisher, ISBN and copyright-holder metadata stays unset.
