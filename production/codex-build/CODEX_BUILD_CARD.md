# Codex build card (orchestrator and reviewer, not art worker)

Owner decisions 2026-10-14: Codex orchestrates the whole build and release overnight, and Codex performs the all-page visual review
that gates the release. Read this and `AGENTS.md` only. Work in PowerShell from `C:\Heraldry\art-producer` on `main`, with
`$env:PYTHONUTF8 = "1"` and `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"`. `PY` means `C:\Heraldry\art-venv\Scripts\python.exe`.
You never build PDFs locally, generate art, edit tools, config, source, art or other ledgers, dispatch workflows, create branches,
force-push, or touch credentials. The only files you write are your review record (in the scratch folder) and, through the bind tool,
`production/qa/visual-review.json`.

## 1. Request the candidate build
1. `git status --short` must be empty (or only your own unsent art files: then run the art `delivery_guard.py ship --execute --repo .` first).
   `git pull --ff-only origin main`. Never resolve git by hand.
2. `PY tools/build_request.py check`. NOT READY: quote every line and stop.
3. `PY tools/build_request.py request`. Note the request id. This push starts the GitHub workflow "Build candidate".
4. `PY tools/build_request.py wait --id <id>` (polls every 4 minutes, up to 100). `CANDIDATE_READY`: continue. `FAILED`: print the JSON
   (`note`, `failed_checks`, `run_url`) and stop; do not retry or edit. Timed out: wait once more with `--timeout-min 60`, then stop and report.

## 2. Review every page (this is the release gate: do it honestly)
5. `git pull --ff-only origin main` then `git lfs pull --include="production/qa/review/*"`. Read `production/qa/review/manifest.json`:
   it lists every contact sheet (`sheet-NN.jpg`, 24 pages each, all pages covered), the detail pages (`page-NNNN.jpg`, 100 dpi: first and last page,
   every chapter opener, every 50th page), the two covers (`cover-front.jpg`, `cover-back.jpg`, from the separate covers PDF) and `calibration.jpg`.
   The inkjet book itself has no covers inside it: its page 1 is the title page and its last page is the end of the index. That is correct, not a defect.
6. Open and look at EVERY image listed, one at a time, in order. For each, write what you actually saw. Look for: an unintended blank page
   (page 6 is a deliberate blank verso before Chapter 1), overlapping or clipped text, text or art outside the safe edge, missing or wrong
   art (an empty slot, a stub, a white rectangle on the cream), a table or figure broken or stranded from its heading, wrong page order,
   a heading alone at the bottom of a column, an entry name alone at the bottom of a column with its fields on the next page, a page of art with
   no text where text is expected. In `cover-front.jpg` the front cover must be the owner-supplied picture (HERALDRY, skull-and-thorn frame,
   dragon skeleton); `cover-back.jpg` must be the back cover with the castle logo. If either is not, that is a major finding.
7. Write the review record to `$env:HERALDRY_SCRATCH\review.json` (schema: `tools/visual_review_bind.py` docstring): one `sheets` entry per
   sheet (observations of at least 60 characters, and `findings` with `page`, `severity` = `minor` or `major`, `text`), one `details` entry per
   detail page, one `covers` entry per cover image, `calibration.observations`, your `reviewer` name ("Codex (OpenAI model, image inspection)") and a short `summary`.
   Severity `major` = anything a reader would call a defect. Never mark a real defect minor to get a release; never invent observations.
8. `PY tools/visual_review_bind.py bind --review $env:HERALDRY_SCRATCH\review.json --push`.
   - `REFUSED`: fix the record (missing entries, short observations, LFS stubs) and run it again; do not weaken the check.
   - `REVIEW FAILED` (major findings): print the findings and STOP. The book is not released; Claude Code decides the repair.
   - Success: it commits and pushes `production/qa/visual-review.json` and prints the ledger commit SHA. That push starts the release workflow.

## 3. Wait for the release
9. `PY tools/build_request.py release-wait --ledger-commit <SHA>` (every 4 minutes, up to 60). `RELEASED`: print the JSON. `FAILED`: print the
   JSON (`note`, `run_url`) and stop; do not retry.

## Final report
Request id and commit, candidate result, number of sheets/details reviewed and any minor notes, ledger commit SHA, release result,
`release_url` and tag, and "Physical print: NOT TESTED. Review was a contact-sheet and detail inspection by Codex, not glyph-level proofreading
and not an independent second review."
