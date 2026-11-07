# Build card (owner-requested build and release)

Use this card only when the owner asks for a build. Any client may run it and review the pages; in Claude Code the owner starts it with `/build-release`. The chain and its tools are described in [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md).

`PY` means the project Python. On the owner's Windows PC, work in PowerShell from `C:\Heraldry\art-producer` on `main`, with `$env:PYTHONUTF8 = "1"` and `$env:HERALDRY_SCRATCH = "C:\Heraldry\art-scratch"`; `PY` is `C:\Heraldry\art-venv\Scripts\python.exe`. Elsewhere, `PY` is `python3` and the scratch folder is any folder outside the checkout.

You may repair code, layout, or tooling and re-dispatch the requested build. Manuscript text changes still need an approved batch through the revision tool. Don't push to `main` while a publishing run is queued or running: let it finish first.

Git follows `AGENTS.md`: sync with `git pull --ff-only origin main`. If a push (yours or a helper's) is refused because `main` moved, replay your unpushed commits with `git pull --rebase origin main` and push again. Never force-push, rewrite pushed history, or create a branch.

## 1. Request the candidate build
0. After layout, tooling, or Typst changes since the last release, prove them locally first (see [LAYOUT_WORKFLOW.md](LAYOUT_WORKFLOW.md)):
   - run one full build (`make clean all`, then `PY tools/verify.py`);
   - check that `production/qa/layout.json` has no flags;
   - compare the digital PDF with the last release using `PY tools/layout_flow.py LAST.pdf NEW.pdf`;
   - look at every page that changed.

   A compile peaks at about 7.5 GB, so run one build at a time on a 15 GB machine.
1. Start from a clean tree (`git status --short` is empty), then run `git pull --ff-only origin main`.
2. Run `PY tools/build_request.py check` and fix whatever readiness problem it reports.
3. Run `PY tools/build_request.py request` and note the request id. This push starts the GitHub workflow "Build candidate".
4. Run `PY tools/build_request.py wait --id <id>`. It polls every 120 seconds for up to 100 minutes; a candidate takes about 15 minutes.
   - `CANDIDATE_READY`: continue.
   - `FAILED`: read `note`, `failed_checks`, and `run_url`, fix the cause, push the fix, and request a fresh candidate.
   - Timed out: check the run's status before waiting longer. Don't submit duplicate requests.

## 2. Review every page (the release gate)
5. Run `git pull --ff-only origin main`, then `git lfs pull --include="production/qa/review/*"`. `production/qa/review/manifest.json` lists, all from the digital PDF:
   - every contact sheet (`sheet-NN.jpg`, 24 pages each, covering all pages);
   - the detail pages (`page-NNNN.jpg` at 100 dpi: the first and last page, every chapter opener, and every 50th page);
   - the two covers (`cover-front.jpg` and `cover-back.jpg`): page 1 is the front cover and the last page is the back cover.
6. Look at every listed image. Things to look for:
   - an unintended blank page (page 2, the inside front cover, and the verso just before Chapter 1 are deliberate blanks);
   - overlapping or clipped text;
   - text or art outside the safe edge;
   - missing or wrong art (an empty slot, a stub, or a white rectangle on the cream);
   - a table or figure broken or stranded from its heading;
   - wrong page order;
   - a heading, or an entry name, alone at the bottom of a column with its content on the next page;
   - an item's label and name line at a column or page foot without its text;
   - a column left empty in the middle of a section while the text simply continues overleaf (an interior void). Space left before a unit carried whole to the next column or page is a keep gap under the one-page keep rule (`docs/PROJECT_CONTRACT.md`): a minor note, unless the unit would have fitted where it started;
   - stacked column bands that read as one column, or a hairline through text (the layout gate also fails on the latter);
   - a heading printed twice (a table title repeating the heading above it);
   - a single table row or card entry alone overleaf;
   - a running-head shield cropped;
   - a page of art with no text where text is expected.

   Start with the pages `production/qa/layout.json` points to under `flow`: interior voids, the largest keep gaps, low right-column starts, uneven chapter ends, and numbered sections that start mid-column (each must start a page or a column; the only accepted one is the Appendix C run-on).

   `cover-front.jpg` must be the owner-supplied picture (HERALDRY, the skull-and-thorn frame, and the dragon skeleton), and `cover-back.jpg` must be the back cover with the castle logo. Anything else is a major finding.
7. Write the review record to a file in the scratch folder, such as `$env:HERALDRY_SCRATCH\review.json` (the schema is in the `tools/visual_review_bind.py` docstring):
   - one `sheets` entry per sheet, one `details` entry per detail page, and one `covers` entry per cover, each with a short note of what you saw and any `findings` (`page`, `severity` = `minor` or `major`, and `text`);
   - your `reviewer` name and a short `summary`.

   `major` means anything a reader would call a defect. Don't mark a real defect minor to get a release.

   **Splitting the review.** Three reviewers work well: sheets 1 to 14, sheets 15 to 27, and the detail pages with the covers. Give each the layout intent and the defect list above, and have each write its part in this schema; a finding's note goes in `text`. The lead looks at the covers and at every page with a major finding before binding.

   **Later candidates.** If a candidate was rebuilt after an earlier review, compare `manifest.json` hashes with that candidate's. An image whose hash is unchanged may carry its review forward, noted as such. Every changed image, and every changed page at full size, gets a fresh look.
8. Run `PY tools/visual_review_bind.py bind --review <review file> --push`.
   - `REFUSED`: fix the record (missing entries or LFS stubs) and run it again.
   - `REVIEW FAILED` (major findings): the release stays blocked. Fix the defect, request a fresh candidate, and review that one. Ask the owner only about a real design or rules decision.
   - Success: it commits and pushes `production/qa/visual-review.json` and prints the ledger commit SHA. That push starts the release workflow. If you had to rebase before the push landed, the ledger commit is the new `HEAD` (`git rev-parse HEAD`).

## 3. Wait for the release
9. Run `PY tools/build_request.py release-wait --ledger-commit <SHA>`. It polls every 120 seconds for up to 60 minutes; a release takes about 10 minutes.
   - `RELEASED`: print the JSON, and check that the digital PDF's SHA-256 in `dist/RELEASE.json` equals the reviewed one in `production/BUILD_STATUS.json`.
   - `FAILED`: read `note` and `run_url`, fix the cause, and re-dispatch the delivery. A changed PDF needs a fresh candidate review.

## Final report
Request id and commit, candidate result, the sheets and detail pages reviewed with any minor notes, ledger commit SHA, release result, `release_url`, tag, and whether the shipped PDF hash equals the reviewed one. Add a short entry to the top of `production/STATE.md` once nothing is running.

## Prompt to paste into Codex

```text
You are building and releasing Heraldry in C:\Heraldry\art-producer (xjordont/Heraldry, branch main). Read AGENTS.md, the newest entries of production/STATE.md, and docs/BUILD_CARD.md, then follow the card. Use C:\Heraldry\art-venv\Scripts\python.exe with PYTHONUTF8=1 and HERALDRY_SCRATCH=C:\Heraldry\art-scratch.

This prompt is an explicit request for the whole GitHub build and release, including the all-page visual review that gates it. A real defect is a major finding. Fix code or layout failures and retry; a changed PDF needs a fresh candidate and review. Never create a branch, force-push, rewrite pushed history, edit source/ snapshots, or touch credentials. Rules or design decisions belong to the owner.

Final report: the card's final report.
```
