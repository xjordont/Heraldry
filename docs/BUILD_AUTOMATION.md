# Unattended build chain (owner request 2026-10-14)

Goal: a full build and release prepared overnight with Codex as orchestrator and GitHub as the only channel. No token, no
local PDF build, no API call: Codex uses the Git login it already has.

```
Codex (Windows PC)                      GitHub Actions                              Claude Code (next session)
tools/build_request.py request  --push-->  Build candidate (build-candidate.yml)
  writes production/build-request.json      make test clean all; verify; pre-release
tools/build_request.py wait     <--git---   commits production/BUILD_STATUS.json
  reports CANDIDATE_READY | FAILED                                                   reproduces the build (same PDF hashes),
                                                                                     reviews every page, binds
                                                                                     production/qa/visual-review.json, pushes
                                            Rebuild verified delivery (rebuild-delivery.yml)  <--push of that ledger--
                                              make test clean all verify package; GitHub Release; ledgers on main
```

## Why the last step needs Claude Code

`tools/verify.py` makes `visual_review_currency` a mandatory check: `production/qa/visual-review.json` must be bound to the
SHA-256 of the exact cream PDF and record that every page was inspected. That inspection is human/Claude work (docs/VISUAL_QA.md:
automated checks do not replace visual inspection), so an unattended run stops at a **pre-release candidate** named
`<RC>-candidate-<n>` ("visual review pending"). A clean build is reproducible, so Claude Code rebuilds the same PDF, reviews it,
and compares hashes with the candidate's `SHA256SUMS-candidate.txt` before binding the ledger.

## Pieces

| File | Role |
|---|---|
| `tools/build_request.py` | stdlib only. `check` (main ready?), `request` (writes and pushes the request), `wait` (polls `origin/main` for the status) |
| `production/build-request.json` | the trigger: `request_id`, time, base commit |
| `.github/workflows/build-candidate.yml` | starts on a push of the request file (or by hand); builds, verifies, publishes the pre-release, commits `production/BUILD_STATUS.json` (also on failure, with the failed step) |
| `tools/build_status.py` | decides `CANDIDATE_READY` (only `visual_review_currency` failing) or `FAILED`; records PDF hashes |
| `production/BUILD_STATUS.json` | the answer Codex reads |
| `.github/workflows/rebuild-delivery.yml` | the release; also starts when `production/qa/visual-review.json` is pushed to main |
| `production/build/CODEX_BUILD_CARD.md`, `CODEX_BUILD_PROMPT.md` | Codex's contract and the prompt to paste |

`build_request.py check` refuses to request unless: on main, tree clean, local main equals origin/main, every illustration
approved, art queue empty, and `tools/preflight.py` passes. Codex never edits tools, config, source, art or ledgers; it never
fixes a failing build: it reports the failed step and stops.

Rules kept: PDFs and ZIPs are never committed (releases only); the ledgers on main describe the last verified release;
physical printing stays NOT TESTED.
