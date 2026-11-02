# Unattended build and release chain (owner decisions 2026-10-14)

## Shared client authority

Owner instruction, 2026-10-22: Claude Code, Codex, and ChatGPT Work have equal authority under `docs/AGENT_OPERATIONS.md`, which defines worker and reviewer scope. Client names below identify the original route, not exclusive permissions. A generation-only worker never approves its own work; record the actual client and reviewer in provenance.


Local layout iteration uses [LAYOUT_WORKFLOW.md](LAYOUT_WORKFLOW.md). Candidate and delivery jobs share the verified measurement cache; restoring it does not skip fresh composition or any publication gate. Local proofs do not dispatch this release chain.

Codex orchestrates the whole build and release overnight, including the all-page visual review that gates it ("Hand it all over to codex";
"I want Codex to have full rights to release like you do"). GitHub is the delivery channel. Codex uses
the Git login it already has. The owner's 2026-10-15 primary-developer handoff and `docs/WORKFLOW.md`
allow local specimens and full-book diagnosis during an explicitly requested layout pass. Local output
does not constitute a published candidate or bypass the exact-PDF review and GitHub release chain below.

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
The review is by the assigned reviewer on any supported client, from images, and the ledger says so (reviewer name, `limits`: not glyph-level proofreading, not an independent second review,
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
| `tools/visual_review_bind.py` | validates the assigned reviewer's record and writes the ledger (`--push` commits and pushes it) |
| `.github/workflows/rebuild-delivery.yml` | the release; also starts when `production/qa/visual-review.json` is pushed to main; writes `RELEASE_RESULT.json` |
| `tools/release_result.py` | `RELEASED` or `FAILED` for a ledger commit |
| `production/codex-build/CODEX_BUILD_CARD.md`, `CODEX_BUILD_PROMPT.md` | Codex's contract and the prompt to paste |

`build_request.py check` refuses unless: on main, tree clean, local main equals origin/main, every illustration approved, art queue empty, and
`tools/preflight.py` passes. Under the owner's 2026-10-15 primary-developer handoff, Codex reads the failed job log, repairs the cause, runs the required tests, pushes to main, and re-dispatches the requested release workflow. This supersedes the former stop-only build-worker restriction; a new, unrelated build still requires an owner request.

Rules kept: PDFs and ZIPs are never committed (releases only; review images are JPEGs in LFS, replaced each build); ledgers on main describe the last
verified release; physical printing stays NOT TESTED.

## Failure and review safeguards

README maintenance shares `publication-main` with `queue: max` on all three workflows. It defers for queued publication work and refreshes after workflow completion. Ordinary checks refresh its generated blocks locally; no PDF build is involved. See [README automation](README_AUTOMATION.md).

Routine local checks use `python tools/dev.py check`; they do not request a build or overwrite release ledgers. Exact dependencies and required imports/tools are checked locally and in CI. Repository CI covers Ubuntu and Windows, caches downloads by `requirements.lock`, and cancels only superseded repository checks. Candidate and delivery jobs share the non-cancelling `publication-main` queue, preventing them from writing main concurrently.

Candidate verification deletes the prior STATUS report before running, then requires complete results for the shared mandatory-check list. Only a valid report with all nonvisual checks passing may produce review aids or a candidate pre-release. Missing or inconsistent summaries fail. Both publishing jobs retain explicitly listed JSON diagnostics as 14-day artifacts even on failure; early failure may leave older committed snapshots, so use the run's result/outcome to interpret them.

The visual-review binder requires contact-sheet ranges covering every PDF page exactly once, first/last detail images, both covers, and calibration. Major findings on any reviewed image block binding; unknown severities also refuse. Minor notes from every image are retained. Figure semantic reviews require a named reviewer, a review date, and current SVG, caption, and manuscript-dependency hashes.

The Windows request/review helpers require clean, fetched, current main before mutation. They run `make test`, recheck main and their exact file scope, then commit and push only their own file. Test failures preserve generated files; rejected pushes preserve the local commit and stop. They never automatically pull, reset, or rebase. Keep the review JSON in the external scratch folder.

The release workflow passes its preceding job status to `release_result.py --job-status`, including a failed verification-ledger commit or push. A published asset alone does not produce a RELEASED result. `release_result.py --push` appends only the result record to freshly fetched main using a temporary index. It retries a concurrent main update without rebasing a pending verification-ledger commit onto newer inputs. It preserves all other files on remote main and leaves the runner's dirty build checkout intact.

First-attempt tags retain `<RC>-candidate-<run>` and `<RC>-build-<run>`. Workflow reruns append `-attempt-<attempt>` so a successful earlier publication does not cause a tag collision or require overwriting a release.
