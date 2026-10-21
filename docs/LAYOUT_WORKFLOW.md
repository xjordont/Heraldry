# Repeatable layout workflow

Use this workflow for an owner-requested layout pass. A tooling change alone does not authorize a full-book build. The local runner never publishes, approves a visual review, or edits release ledgers.

## Entry points

Run these commands from the repository root with the project's Python environment:

```text
python tools/dev.py layout plan
python tools/dev.py layout check
python tools/dev.py layout run
```

`plan` reads the active manuscript and prints the stages without generating PDFs. `check` runs dependency and baseline checks plus focused regression tests, including small compiler fixtures. `run` prepares the current manuscript, composes cream, runs core gates, then generates companion variants and review images only after those gates pass. Independent checks use at most two workers. Run the full `python tools/dev.py check` after changes are frozen and before pushing; focused checks do not replace it.

Each check/run writes commands, durations, logs, report hashes, and status to `build/checks/layout-runs/<run>/run.json`. A successful full local run ends at `LOCAL_QA_PASS_REVIEW_REQUIRED`. Inspect every manifest asset, covers, calibration, and any suspect pages before claiming visual review. Physical print remains NOT TESTED until physically tested. The archived cream PDF is the exact substrate used for the review images.

Do not run concurrent composition commands in the shared checkout. The runner holds `build/layout-workflow.lock`; after an interrupted process, inspect its receipt and confirm no process is running before removing a stale lock. Do not clean away proof evidence during iteration.

## Reuse measurements, never reuse approval

Verified unit measurements live in ignored `.cache/layout-measurements/`, outside `build/`, so `make clean` preserves them. The key includes the exact measurement source, full publication input identity, compiler identity, fonts, and compilation options. A hit requires matching evidence and the exact PDF hash, then extracts and validates the measurement rows from that PDF again. Corruption is a cache miss; warning-bearing exports are not stored. Input changes during measurement fail the run.

An updated manuscript or other bound input requires fresh measurements. There is no approximate per-unit height reuse across edited manuscripts. GitHub candidate and delivery jobs restore the same cache namespace, but internal identity verification remains mandatory. A restored cache never substitutes for source, keep, position, geometry, print-profile, or visual-review gates.

Converged column-balancing plans may be restored as starting hints from the same verified measurement entry. Segment signatures bind rendered content and layout settings, rather than only heading IDs and item counts. Every hint is followed by real composition, balancing, and convergence checks. Failed or uncompiled proposals cannot become converged cache entries. For a diagnostic fresh measurement, use `python tools/build_book.py --no-measurement-cache` after normal preparation; this bypasses measurement and persisted hint caches. To ignore local balancing hints as well, add `--no-balance` (this disables balancing, so it is a diagnostic comparison, not the production default).

## Manuscript changes and table widths

Always parse the active RC before composition. The runner verifies the parsed model against the current manuscript and freezes publication inputs after preparation. Changes during composition or validation stop the run. Start a new run after changing any bound input; old PDF approval does not carry forward.

Reviewed table-width preferences in `config/design_tokens.json` use normalized complete heading paths and exact plain header cells. They do not use sequential T-numbers. Renumbered sections and inserted tables therefore retain their intended selectors. A changed table is freshly measured and allocated, with changed-content diagnostics. Removed targets produce warnings and remain unapplied; ambiguous or overlapping selectors fail before compilation. Inspect `production/mappings/table_scope_policies.json` and the run's composition diagnostics whenever a manuscript changes.

## Lessons retained from the compact-layout pass

Keep the approved 10.5 pt body, 9 pt tables, narrow margins, two-column rules, and full-width introduction flavour in the shared layout profile. Improve components and flow rather than repeatedly shrinking text. Preserve source coverage, substantive heading keeps, fit-capable keep units, continuation identities, and physical page evidence. Cosmetic whitespace alone does not justify violating those constraints.

Use focused fixtures while editing, then freeze inputs and run the complete checks once. Stop failed cream proofs before paying for variants or all-page images. Local print instructions stay beside the run receipt, leaving last-delivered instructions intact. Use recorded timings to identify the next bottleneck instead of repeating expensive probes blindly.

The previous RC493 proof's 603 print pages and 606 digital pages are historical evidence for its exact inputs. Workflow changes do not certify a newly generated full book. The cache is covered by compiler fixtures and invalidation tests; no new full-book speed benchmark is implied. Published delivery still follows [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md).
