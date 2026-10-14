# Unattended build and release chain (owner decisions 2026-10-14)

Codex orchestrates the whole build and release overnight, including the all-page visual review that gates it ("Hand it all over to codex";
"I want Codex to have full rights to release like you do"). GitHub is the only channel: no token, no API call, no local PDF build. Codex uses
the Git login it already has.

```
Codex (Windows PC)                       GitHub Actions
build_request.py request  --push-->      Build candidate (build-candidate.yml)
                                           make test clean all; verify; review aids; pre-release
build_request.py wait     <--git---      commits production/BUILD_STATUS.json + production/qa/review/ (LFS)
git lfs pull; view every image
visual_review_bind.py bind --push -->    Rebuild verified delivery (rebuild-delivery.yml), started by the ledger push
                                           make test clean all verify package; GitHub Release; ledgers on main
build_request.py release-wait <--git--   commits production/RELEASE_RESULT.json
```

## The review gate stays real

`tools/verify.py` still requires `production/qa/visual-review.json` bound to the SHA-256 of the exact cream PDF with every page recorded.
The review is now by Codex, from images, and the ledger says so (reviewer name, `limits`: not glyph-level proofreading, not an independent second review,
not a physical proof). `tools/visual_review_bind.py` keeps it honest: it refuses unless the candidate is `CANDIDATE_READY` and matches the manifest
PDF hash, every contact sheet, detail page and the calibration sheet has real observations (60+ characters), the image files on disk match the manifest
hashes (no LFS stubs), a reviewer is named, and no finding is `major`. A major finding blocks the release and is reported. The release workflow
rebuilds the PDF from scratch and `verify` checks the ledger hash again, so a ledger for a different PDF fails the release. A clean build is
reproducible (proved on RC492).

## Pieces

| File | Role |
|---|---|
| `tools/build_request.py` | stdlib only. `check`, `request`, `wait`, `release-wait` |
| `production/build-request.json` | the trigger: `request_id`, time, base commit |
| `.github/workflows/build-candidate.yml` | starts on a push of the request file (or by hand); builds, verifies, makes the review aids, publishes the pre-release, commits `BUILD_STATUS.json` (also on failure) and `production/qa/review/` |
| `tools/build_status.py` | `CANDIDATE_READY` (only `visual_review_currency` failing) or `FAILED`; PDF hashes |
| `tools/review_aids.py` | 24-page contact sheets (all pages), 100 dpi detail pages (covers, chapter openers, every 50th page), calibration, `manifest.json` |
| `tools/visual_review_bind.py` | validates Codex's review record and writes the ledger (`--push` commits and pushes it) |
| `.github/workflows/rebuild-delivery.yml` | the release; also starts when `production/qa/visual-review.json` is pushed to main; writes `RELEASE_RESULT.json` |
| `tools/release_result.py` | `RELEASED` or `FAILED` for a ledger commit |
| `production/codex-build/CODEX_BUILD_CARD.md`, `CODEX_BUILD_PROMPT.md` | Codex's contract and the prompt to paste |

`build_request.py check` refuses unless: on main, tree clean, local main equals origin/main, every illustration approved, art queue empty, and
`tools/preflight.py` passes. Codex never fixes a failing build; it reports the failed step and stops.

Rules kept: PDFs and ZIPs are never committed (releases only; review images are JPEGs in LFS, replaced each build); ledgers on main describe the last
verified release; physical printing stays NOT TESTED.
