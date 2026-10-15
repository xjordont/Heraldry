# Codex build card (primary developer, build orchestrator, and reviewer)

Owner decisions 2026-10-14: Codex orchestrates the whole build and release overnight, and Codex performs the all-page visual review
that gates the release. The owner's 2026-10-15 handoff makes Codex the primary developer. Read `CLAUDE.md`, `AGENTS.md`,
`production/STATE.md`, `docs/WORKFLOW.md`, and `docs/BUILD_AUTOMATION.md`. Work in PowerShell from `C:\Heraldry\art-producer` on `main`, with
`$env:PYTHONUTF8 = "1"` and `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"`. `PY` means `C:\Heraldry\art-venv\Scripts\python.exe`.
Use this card only for an owner-requested build. The standard route builds on GitHub. Codex may repair code, layout, or tooling and
re-dispatch the already requested build when necessary; manuscript text still requires an approved batch through the revision tool.
Never create a live branch, force-push, rewrite history, print credentials, or bypass review. Ordinary checks use `PY tools/dev.py check`;
local reports stay in ignored `build/checks/`. Before any main push, let the active publishing run finish and inspect its result.

## 1. Request the candidate build
1. `git status --short` must be empty. Finish or preserve existing work before continuing.
   `git pull --ff-only origin main`. Inspect divergence; never reset, rebase, or force-push to make it disappear.
2. `PY tools/build_request.py check`. Resolve reported readiness problems within the governing contract; preserve unrelated work.
3. `PY tools/build_request.py request`. Note the request id. This push starts the GitHub workflow "Build candidate".
4. `PY tools/build_request.py wait --id <id>` (polls every 4 minutes, up to 100). `CANDIDATE_READY`: continue. `FAILED`: print the JSON
   (`note`, `failed_checks`, `run_url`), inspect the job log, and repair the cause within this requested build. Test and push the repair,
   then request a fresh candidate. Timed out: inspect run status before deciding whether to wait longer; do not submit duplicate requests blindly.

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
   - `REVIEW FAILED` (major findings): retain the findings; release stays blocked. Codex repairs authorized layout/tooling defects,
     requests a fresh candidate, and reviews that exact candidate. Ask the owner only for a substantive unresolved design/rules decision.
   - Success: it commits and pushes `production/qa/visual-review.json` and prints the ledger commit SHA. That push starts the release workflow.

## 3. Wait for the release
9. `PY tools/build_request.py release-wait --ledger-commit <SHA>` (every 4 minutes, up to 60). `RELEASED`: print the JSON. `FAILED`: print the
   JSON (`note`, `run_url`), inspect the job log, repair the cause, test, and re-dispatch this requested delivery. A changed PDF requires a
   fresh candidate review. Both publishing helpers test before committing and refuse a concurrent main update; inspect preserved local
   work after refusal instead of automatically rebasing it.

## Final report
Request id and commit, candidate result, number of sheets/details reviewed and any minor notes, ledger commit SHA, release result,
`release_url` and tag, and "Physical print: NOT TESTED. Review was a contact-sheet and detail inspection by Codex, not glyph-level proofreading
and not an independent second review."
