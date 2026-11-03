# Build and release chain

Builds happen only when the owner asks. GitHub Actions builds the candidate and the release; the agent requests the build, looks at the candidate's review images, and binds the review. The step-by-step procedure is [BUILD_CARD.md](BUILD_CARD.md). Local proofs during requested layout work ([LAYOUT_WORKFLOW.md](LAYOUT_WORKFLOW.md)) never start this chain, and they share its verified measurement cache.

```
Agent                                    GitHub Actions
build_request.py request  --push-->      Build candidate (build-candidate.yml)
                                           make test clean all; verify; review aids; pre-release
build_request.py wait     <--git---      commits production/BUILD_STATUS.json + production/qa/review/ (LFS)
git lfs pull; view every image
visual_review_bind.py bind --push -->    Rebuild verified delivery (rebuild-delivery.yml), started by the ledger push
                                           history check; make test clean all verify package;
                                           Hero records; player aids; 300 ppi check; GitHub Release; ledgers on main
build_request.py release-wait <--git--   commits production/RELEASE_RESULT.json
```

## Review

The review covers the digital PDF. Look at every contact sheet (all pages), the detail pages (the first and last page, chapter openers, and every 50th page), and both covers (its first and last pages). Write the review JSON outside the checkout with a short note per image and any findings marked `minor` or `major`. A major finding is an unintended blank page, overlapping or clipped text, missing or wrong art, a broken table, content past the safe edge, or wrong page order; it blocks the release. `tools/visual_review_bind.py` checks that the review covers every image in the manifest, that the images on disk are real (not LFS stubs), and that the reviewer is named. `tools/verify.py` then requires the ledger to match the exact PDF hash, so a review of a different PDF fails the release.

## The release run

`rebuild-delivery.yml` does more than the candidate. It:

1. on a push, checks that no earlier manuscript snapshot or evidence changed since the previous head (`tools/check_history.py`);
2. checks the artwork masters (`tools/check_art.py`) and rebuilds from the ledger commit with `make test clean all verify package`, which must reproduce the reviewed PDF;
3. builds the Hero records with `assets/hero-record/sheet.py` (the blank, which must match the committed blank sides, and the 24 Basic Mode Heroes);
4. checks the player aids against the manuscript (`tools/aids_fidelity.py`) and renders them (`tools/render_aids.py`);
5. checks that every placed raster in every release PDF is at least 300 ppi (`tools/check_art_ppi.py`);
6. refuses to publish if `main` moved during the run, then publishes the GitHub Release, commits the ledgers and `dist/RELEASE.json`, and records `production/RELEASE_RESULT.json`.

The candidate skips steps 1, 3, 4, and 5, so a candidate can pass and its release still fail on them.

## Pieces

| File | Role |
|---|---|
| `tools/build_request.py` | Standard library only: `check`, `request`, `wait`, `release-wait` |
| `production/build-request.json` | The trigger: `request_id`, time, and base commit |
| `.github/workflows/build-candidate.yml` | Runs on a push of the request file (or by hand); builds, verifies, makes the review aids, publishes the pre-release, and commits `BUILD_STATUS.json` (also on failure) and `production/qa/review/` |
| `tools/build_status.py` | `CANDIDATE_READY` (only `visual_review_currency` failing) or `FAILED`, with PDF hashes |
| `tools/review_aids.py` | 24-page contact sheets of the digital PDF, 100 dpi detail pages, both covers, and `manifest.json` |
| `tools/visual_review_bind.py` | Validates the review and writes the ledger (`--push` commits and pushes it) |
| `.github/workflows/rebuild-delivery.yml` | The release; also starts when `production/qa/visual-review.json` is pushed to main, and writes `RELEASE_RESULT.json` |
| `tools/release_result.py` | `RELEASED` or `FAILED` for a ledger commit |
| `docs/BUILD_CARD.md` | The step-by-step card, with the prompt to paste into Codex |
| `.claude/skills/build-release/SKILL.md` | `/build-release` in Claude Code (owner only): runs the card |

`build_request.py check` refuses unless you are on a clean `main` equal to `origin/main`, every illustration is approved, no approval is bound to an outdated catalogue spec, the art queue holds no required item (optional section-end tailpieces may stay queued), and `tools/preflight.py` passes. If a build fails, read the job log, fix the cause, push to `main`, and re-dispatch the requested workflow; a new, unrelated build still needs an owner request.

## Notes

- Don't push to `main` while a build runs: the publish step aborts if `main` advances. Claude Code's push guard (`.claude/hooks/git-guard.sh`) refuses a push while "Build candidate" or "Rebuild verified delivery" is requested, pending, waiting, queued, or running. After a release, check `production/RELEASE_RESULT.json` and `dist/RELEASE.json` on `main`.
- Candidate, delivery, and README jobs share the `publication-main` queue, so they never write `main` at the same time.
- Each candidate commits its review JPEGs (about 57 images, about 19 MB) to `production/qa/review/` through Git LFS, replacing the previous set in the tree; earlier sets stay in LFS storage and history. PDFs and ZIPs go only to Releases; ledgers on `main` describe the last release.
- Tags are `<RC>-candidate-<run>` and `<RC>-build-<run>`; reruns append `-attempt-<attempt>`.
