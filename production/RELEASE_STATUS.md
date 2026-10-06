# Release status — HERALDRY SKIRMISH RC484 (art-light edition)

Evidence: `production/qa/STATUS.json` (release gate), plus the files cited below. PASS/FAIL/BLOCKED/NOT TESTED/NOT APPLICABLE.

| Area | Status | Evidence |
|---|---|---|
| Source integrity | PASS | SHA-256 2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3 verified by preflight and every parse |
| Content integrity | PASS | `qa/reconciliation.json`: 8,426 blocks found in source order, 0 missing, 0 duplicated; 332/332 tables, 10,341 cells; 22,796 bold + 449 italic runs in bold/italic faces; only bundled fonts |
| Table audit | PASS | `qa/table-audit.json`: every table → representation → pages; 18 card tables and 34 stat cards carry field maps |
| Editorial issues | PASS WITH QUALIFICATION | no source patches; 633 section citations resolve; 1,898 Monster mentions in random tables match bestiary entries; 5 ambiguities found in figure work reported in `editorial/LEDGER.md`; full semantic contradiction audit of the manuscript NOT TESTED |
| Visual QA | PASS (scoped) | `qa/visual-review.json`: all 435 interior pages inspected on contact sheets, detailed sample pages, covers, calibration, overscan renders; layout detectors 0 flags (`qa/layout.json`) |
| Navigation | PASS | generated contents, 551 bookmarks (3 levels), 1,262 internal links resolve, page labels i–v / 1–429; index 228 entries, every locator resolves (`qa/index-audit.json`) |
| Instructional figures | PASS WITH NOTES | 19 vector figures placed once each; independent audit found 2 major defects, both fixed; minor residual: FIG-14 dimension label (see visual review) |
| Atmospheric art | BLOCKED | no authorised image service (external spend 0) and no supplied art; 12-asset manifest and prompts in `production/art/ART_MANIFEST.json`; fully illustrated edition incomplete |
| Inkjet file preflight | PASS | supplied checker PASS on cream and white (`qa/inkjet-preflight*.json`); edge-to-edge substrate, identical cream/white page maps, no rasters (`qa/print-checks.json`) |
| Physical inkjet proof | NOT TESTED | no printed sheets examined |
| Commercial wrap / PDF-X | NOT APPLICABLE | not requested |
| Budget telemetry | NOT AVAILABLE | estimates only (`budget.json`, ~$52) |

Missing commercial metadata (not placed in the book): author credit, publisher, ISBN, copyright holder — none supplied in `config/production.json`.
