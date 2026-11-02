# Build and release chain

Builds happen only when the owner asks. GitHub Actions builds the candidate and the release; the agent requests the build, looks at the candidate's review images, and binds the review. Local proofs during requested layout work ([LAYOUT_WORKFLOW.md](LAYOUT_WORKFLOW.md)) never start this chain, and they share its verified measurement cache.

```
Agent                                    GitHub Actions
build_request.py request  --push-->      Build candidate (build-candidate.yml)
                                           make test clean all; verify; review aids; pre-release
build_request.py wait     <--git---      commits production/BUILD_STATUS.json + production/qa/review/ (LFS)
git lfs pull; view every image
visual_review_bind.py bind --push -->    Rebuild verified delivery (rebuild-delivery.yml), started by the ledger push
                                           make test clean all verify package; GitHub Release; ledgers on main
build_request.py release-wait <--git--   commits production/RELEASE_RESULT.json
```

## Review

Look at every contact sheet (all pages), the detail pages (chapter openers and every 50th page), both covers, and the calibration sheet. Write the review JSON outside the checkout with a short note per image and any findings marked `minor` or `major`. A major finding is an unintended blank page, overlapping or clipped text, missing or wrong art, a broken table, content past the safe edge, or wrong page order; it blocks the release. `tools/visual_review_bind.py` checks that the review covers every image in the manifest, that the images on disk are real (not LFS stubs), and that the reviewer is named. `tools/verify.py` then requires the ledger to match the exact PDF hash, so a review of a different PDF fails the release.

## Pieces

| File | Role |
|---|---|
| `tools/build_request.py` | Standard library only: `check`, `request`, `wait`, `release-wait` |
| `production/build-request.json` | The trigger: `request_id`, time, and base commit |
| `.github/workflows/build-candidate.yml` | Runs on a push of the request file (or by hand); builds, verifies, makes the review aids, publishes the pre-release, and commits `BUILD_STATUS.json` (also on failure) and `production/qa/review/` |
| `tools/build_status.py` | `CANDIDATE_READY` (only `visual_review_currency` failing) or `FAILED`, with PDF hashes |
| `tools/review_aids.py` | 24-page contact sheets, 100 dpi detail pages, calibration, and `manifest.json` |
| `tools/visual_review_bind.py` | Validates the review and writes the ledger (`--push` commits and pushes it) |
| `.github/workflows/rebuild-delivery.yml` | The release; also starts when `production/qa/visual-review.json` is pushed to main, and writes `RELEASE_RESULT.json` |
| `tools/release_result.py` | `RELEASED` or `FAILED` for a ledger commit |
| `production/codex-build/CODEX_BUILD_CARD.md`, `CODEX_BUILD_PROMPT.md` | The step-by-step card and the prompt to paste |

`build_request.py check` refuses unless you are on a clean `main` equal to `origin/main`, every illustration is approved, the art queue is empty, and `tools/preflight.py` passes. If a build fails, read the job log, fix the cause, push to `main`, and re-dispatch the requested workflow; a new, unrelated build still needs an owner request.

## Notes

- Don't push to `main` while a build runs: the publish step aborts if `main` advances. After a release, check `production/RELEASE_RESULT.json` and `dist/RELEASE.json` on `main`.
- Candidate, delivery, and README jobs share the `publication-main` queue, so they never write `main` at the same time.
- Review images are JPEGs in LFS, replaced each build. PDFs and ZIPs go only to Releases; ledgers on `main` describe the last release.
- Tags are `<RC>-candidate-<run>` and `<RC>-build-<run>`; reruns append `-attempt-<attempt>`.
