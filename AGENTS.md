# Agents working in this repository (Codex and others)

`CLAUDE.md` is the governing contract for every agent. Read it, `production/STATE.md`, `docs/WORKFLOW.md`, and `docs/BUILD_AUTOMATION.md` before continuing work.

## Codex role (owner handoff, 2026-10-15)

Codex is the primary developer and integration owner across manuscript tooling, artwork, figures, layout, tests, documentation, and releases. This supersedes the former art-worker-only role and restricted build-orchestrator carve-out. Continue authorized work and repair build failures within the governing contract; substantive rules ambiguities still require an owner decision.

## Required safeguards

- Work on `main` only. Preserve unrelated changes. Sync a clean checkout with `git pull --ff-only origin main`. Never force-push or rewrite history.
- Manuscript snapshots in `source/` are immutable. Apply approved text changes only through `tools/revise_manuscript.py`, with exactly one new RC per approved batch. Never regenerate manuscript prose with an LLM. Read the current RC from `source/versions.json` and keep `config/production.json` consistent.
- Build only on owner request. Use the GitHub candidate, image-review, and release chain in `docs/BUILD_AUTOMATION.md`; do not treat a documentation or tooling change as a build request.
- Keep the hash-bound review gate real. Inspect the required images, record actual observations and limits, and bind only the exact reviewed PDF. Automated checks do not replace visual review or a physical proof.
- Never commit built PDFs or ZIPs. Publish requested deliveries through GitHub Releases. Keep physical print status **NOT TESTED** until actual sheets are examined.
- Before every push, run `make test`. When touching contracts, also run `python3 tools/preflight.py --baseline`. Run track-specific checks and update the state and release status at milestones.
- Before pushing during a build, wait for its final result: the publish step aborts if main advances. Check `production/RELEASE_RESULT.json` and `dist/RELEASE.json` on main after release.
- Never print, log, or commit secrets. Use the owner's existing Git login. Artwork generation uses the owner's ChatGPT plan; do not use a paid image API without an explicit owner instruction.

## Track-specific instructions

For artwork generation and guarded delivery, follow the live `production/art/codex/BATCH_CARD.md`, `production/art/codex/CODEX_RUNBOOK.md`, and `production/art/skill/heraldry-classic-ink-art/SKILL.md`. Delivery is not approval; record an actual visual review before approving artwork. Old worker allowlists apply to that delivery procedure, not to Codex's overall developer role.

The build cards and historical prompts describe their scoped runs. Where they retain the former role restriction or require stopping at a repairable build failure, this owner handoff supersedes those restrictions. Preserve all manuscript, review, release, credential, and physical-proof safeguards.
