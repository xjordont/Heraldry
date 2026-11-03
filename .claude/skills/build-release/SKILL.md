---
name: build-release
description: Run the owner-requested candidate build, all-page review, and GitHub release for the active RC. Only the owner starts it, because builds happen only on request.
disable-model-invocation: true
argument-hint: "[resume: candidate | review | release]"
---

# Build and release the active RC

The owner typed `/build-release`, which is the build request `AGENTS.md` requires. Follow `docs/BUILD_CARD.md` step by step; `docs/BUILD_AUTOMATION.md` explains the chain. If an argument names a stage, resume there after confirming the state in `production/BUILD_STATUS.json` or `production/RELEASE_RESULT.json`.

## On Linux, macOS, or a cloud session

Use `python3` wherever the card says `PY`, and a scratch directory outside the checkout instead of `$env:HERALDRY_SCRATCH`. Without `gh`, use the GitHub MCP tools (`actions_list`, `actions_get`, `actions_run_trigger`) to watch runs and read job logs.

## Rules that cost a release when skipped

- **No pushes while a publishing run is waiting or running.** That includes `.claude/`, docs, and `STATE.md` commits. Commit locally and push after `RELEASE_RESULT.json` lands. `.claude/hooks/git-guard.sh` refuses such a push (a requested, pending, waiting, queued, or running "Build candidate" or "Rebuild verified delivery"), but check before you start other work in the same session.
- **If the release run will fail because `main` moved:** cancel it, wait until no "Build candidate", "Rebuild verified delivery", or "Update GitHub README" run is queued or running, and then dispatch `rebuild-delivery.yml` on `main`. A rebuild from a commit that changes nothing in the book reproduces the reviewed PDF, so the existing review still binds.
- **Confirm what shipped:** the digital PDF's SHA-256 in `dist/RELEASE.json` must equal the one in `production/BUILD_STATUS.json` for the reviewed candidate.
- **A major finding blocks the release.** Fix it, request a fresh candidate, and review that one.

## Finish

Add a short entry to the top of `production/STATE.md` (request id, candidate tag, any minor review notes, release tag and link, and the PDF hash match), push it once nothing is running, and give the owner the card's final report.
