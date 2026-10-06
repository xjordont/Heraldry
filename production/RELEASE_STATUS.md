# Release status — HERALDRY SKIRMISH RC484 (art-light edition)

Evidence: `production/qa/STATUS.json` (release gate), plus the files cited below. PASS/FAIL/BLOCKED/NOT TESTED/NOT APPLICABLE.

| Area | Status | Evidence |
|---|---|---|
| Source integrity | PASS | SHA-256 2744833106569e6b20f6913340de5d80c7869782556e23b8f738a0407e4f16f3 verified by preflight and every parse |
| Content integrity | PASS | `qa/reconciliation.json`: 8,426 blocks found in source order, 0 missing, 0 duplicated; 332/332 tables, 10,341 cells; 22,796 bold + 449 italic runs in bold/italic faces; only bundled fonts |
| Table audit | PASS | `qa/table-audit.json`: every table → representation → pages; 18 card tables and 34 stat cards carry field maps |
| Editorial issues | PASS | 7 author-authorized patches (`editorial/patches.json`, gate check `editorial_patches`) close every triaged ambiguity (`qa/ambiguity-triage.json`, `closed_by`); A-10 settled by §1.6; canonical source unchanged and hash-verified; full semantic audit of the whole manuscript NOT TESTED |
| Visual QA | PASS (scoped) | `qa/visual-review.json`: all 436 interior pages (re-inspected after the correction pass) inspected on contact sheets, detailed sample pages, covers, calibration, overscan renders; layout detectors 0 flags (`qa/layout.json`) |
| Navigation | PASS | generated contents, 551 bookmarks (3 levels), 1,262 internal links resolve, page labels i–v / 1–430; index 228 entries, every locator resolves (`qa/index-audit.json`) |
| Instructional figures | PASS | 19 figures; independent hash-bound review: 0 open findings of any severity; gate `figure_semantic_review` PASS |
| Atmospheric art | BLOCKED | no authorised image service (external spend 0) and no supplied art; 12-asset manifest and prompts in `production/art/ART_MANIFEST.json`; fully illustrated edition incomplete |
| Inkjet file preflight | PASS | supplied checker PASS on cream and white (`qa/inkjet-preflight*.json`); edge-to-edge substrate, identical cream/white page maps, no rasters (`qa/print-checks.json`) |
| Physical inkjet proof | NOT TESTED | no printed sheets examined |
| Commercial wrap / PDF-X | NOT APPLICABLE | not requested |
| Budget telemetry | NOT AVAILABLE | estimates only (`budget.json`, ~$52) |

Missing commercial metadata (not placed in the book): author credit, publisher, ISBN, copyright holder — none supplied in `config/production.json`.
