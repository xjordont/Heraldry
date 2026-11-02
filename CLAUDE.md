# Claude Code entry point

Read and follow `AGENTS.md`, `docs/PROJECT_CONTRACT.md`, and `docs/AGENT_OPERATIONS.md`, then `docs/WORKFLOW.md`, `docs/BUILD_AUTOMATION.md`, and the newest entries of `production/STATE.md`. STATE.md is a long newest-first log: read from the top through at least the latest release entry and anything still pending, and search older sections by keyword rather than reading the whole file.

The shared project contract governs Claude Code, Codex, and ChatGPT Work equally. `.claude/settings.json` and `.claude/agents/` are Claude-native adapters; portable specialist role instructions live in `docs/agents/`. Preserve all manuscript, review, publishing, credential, and physical-proof safeguards.

## Hard rules (kept here so they survive context compaction)

- Build, regenerate PDFs, or dispatch release workflows only when the owner asks in this conversation.
- `source/` snapshots are immutable; text changes go only through `tools/revise_manuscript.py`, one new RC per approved batch. Never regenerate manuscript prose with an LLM.
- Run `make test` before every push (`python tools/dev.py check` for ordinary iterations). Never commit PDFs or ZIPs.
- Physical print stays **NOT TESTED** until real sheets are examined; automated checks never replace visual review.
- Use the Oxford comma in everything you write.

## Branches and pull requests

Owner, 2026-10-31: "From now on commit straight to main, no PRs." Commit and push every verified change directly to `main` (`docs/PROJECT_CONTRACT.md`, `docs/WORKFLOW.md`). Do not create a session or feature branch and do not open a pull request, even when a cloud session assigns a working branch or asks for one. If the platform refuses a push to `main`, report the exact refusal and keep the work; do not fall back to a branch or PR without asking the owner.
