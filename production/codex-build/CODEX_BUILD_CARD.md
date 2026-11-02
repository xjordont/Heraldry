# Build card (owner-requested build and release)

Use this card only when the owner asks for a build. Any client may run it and review the pages. The chain and its tools are described in `docs/BUILD_AUTOMATION.md`.

On the Windows PC, work in PowerShell from `C:\Heraldry\art-producer` on `main`, with `$env:PYTHONUTF8 = "1"` and `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"`. `PY` means `C:\Heraldry\art-venv\Scripts\python.exe`. You may repair code, layout, or tooling and re-dispatch the requested build. Manuscript text changes still need an approved batch through the revision tool. Don't push to main while a publishing run is active: let it finish first.

## 1. Request the candidate build
1. Start from a clean tree: `git status --short` is empty, then run `git pull --ff-only origin main`. Never reset, rebase, or force-push to get rid of a divergence.
2. Run `PY tools/build_request.py check` and fix whatever readiness problem it reports.
3. Run `PY tools/build_request.py request` and note the request id. This push starts the GitHub workflow "Build candidate".
4. Run `PY tools/build_request.py wait --id <id>` (it polls every 4 minutes, up to 100 times).
   - `CANDIDATE_READY`: continue.
   - `FAILED`: read `note`, `failed_checks`, and `run_url`, fix the cause, push the fix, and request a fresh candidate.
   - Timed out: check the run's status before waiting longer. Don't submit duplicate requests.

## 2. Review every page (the release gate)
5. Run `git pull --ff-only origin main`, then `git lfs pull --include="production/qa/review/*"`. `production/qa/review/manifest.json` lists, all from the digital PDF:
   - every contact sheet (`sheet-NN.jpg`, 24 pages each, covering all pages)
   - the detail pages (`page-NNNN.jpg` at 100 dpi: the first and last page, every chapter opener, and every 50th page)
   - the two covers (`cover-front.jpg` and `cover-back.jpg`): page 1 is the front cover and the last page is the back cover
6. Look at every listed image. Things to look for:
   - an unintended blank page (page 2, the inside front cover, and the verso just before Chapter 1 are deliberate blanks)
   - overlapping or clipped text
   - text or art outside the safe edge
   - missing or wrong art (an empty slot, a stub, or a white rectangle on the cream)
   - a table or figure broken or stranded from its heading
   - wrong page order
   - a heading, or an entry name, alone at the bottom of a column with its content on the next page
   - a page of art with no text where text is expected

   `cover-front.jpg` must be the owner-supplied picture (HERALDRY, the skull-and-thorn frame, and the dragon skeleton), and `cover-back.jpg` must be the back cover with the castle logo. Anything else is a major finding.
7. Write the review record to `$env:HERALDRY_SCRATCH\review.json` (the schema is in the `tools/visual_review_bind.py` docstring):
   - one `sheets` entry per sheet, one `details` entry per detail page, and one `covers` entry per cover, each with a short note of what you saw and any `findings` (`page`, `severity` = `minor` or `major`, and `text`)
   - your `reviewer` name and a short `summary`

   `major` means anything a reader would call a defect. Don't mark a real defect minor to get a release.
8. Run `PY tools/visual_review_bind.py bind --review $env:HERALDRY_SCRATCH\review.json --push`.
   - `REFUSED`: fix the record (missing entries or LFS stubs) and run it again.
   - `REVIEW FAILED` (major findings): the release stays blocked. Fix the defect, request a fresh candidate, and review that one. Ask the owner only about a real design or rules decision.
   - Success: it commits and pushes `production/qa/visual-review.json` and prints the ledger commit SHA. That push starts the release workflow.

## 3. Wait for the release
9. Run `PY tools/build_request.py release-wait --ledger-commit <SHA>` (every 4 minutes, up to 60 times).
   - `RELEASED`: print the JSON.
   - `FAILED`: read `note` and `run_url`, fix the cause, and re-dispatch the delivery. A changed PDF needs a fresh candidate review.

   If a helper refuses a push because main moved, look at the preserved local work rather than rebasing it automatically.

## Final report
Request id and commit, candidate result, the sheets and detail pages reviewed with any minor notes, ledger commit SHA, release result, `release_url`, and tag.
