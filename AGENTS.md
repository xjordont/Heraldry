# Agents working in this repository

This repository builds the Heraldry Skirmish rulebook, player aids, and Hero records as digital PDFs. Claude Code, Codex, and ChatGPT Work share these instructions and have equal authority: any of them may develop, generate, review, approve, integrate, and release work the owner has asked for. Keep going on authorized work without pausing for routine approvals.

## Start here

- `production/STATE.md` is a newest-first log. Read the top entries (at least back to the latest release and anything still pending) and search it by keyword when you need history; entries before 2026-11-01 are in `production/history/STATE-2026-10.md`.
- `source/versions.json` names the active manuscript; `config/production.json` must agree.
- Product requirements are in `docs/PROJECT_CONTRACT.md` and the design system in `docs/DESIGN.md`; commands are in `docs/AGENT_OPERATIONS.md`.

## Hard rules

- **Manuscript.** Snapshots in `source/` are immutable. Change manuscript text only with the owner's approval, through `tools/revise_manuscript.py` (exact patches) or `python tools/dev.py manuscript` (a full owner upload), one new RC per approved batch. Never regenerate manuscript prose with an LLM. Ask the owner about substantive rules ambiguities, and read `docs/CANON_AUTHORITY.md` before rules or editorial work.
- **Builds.** Build the book, regenerate PDFs, or release only when the owner asks. A doc, tooling, art, or manuscript change is not a build request; local proofs during requested layout work are fine.
- **Git.** Commit straight to `main`: no branches, pull requests, force-pushes, or rewrites of pushed history. Sync with `git pull --ff-only origin main` and keep unrelated local changes. If a push is refused because `main` moved (bots and other agents push to it too), replay your unpushed commits with `git pull --rebase origin main` and push again. While a build is running, wait for it to finish before pushing, because its publish step aborts if `main` moves.
- **Files.** Never commit built PDFs, ZIPs, or secrets. Deliveries go to GitHub Releases (`docs/LARGE_FILES.md`).
- **Art.** Only approved art is placed in the book. Whoever generates an image may review and approve it once they have looked at it. Use the owner's ChatGPT plan, and no paid image API without the owner's say-so.
- **Honesty.** Report what you actually did and checked.
- **Style.** Use the Oxford comma in everything you write: docs, player aids, commit messages, and replies.

## Checks

- Docs, `production/STATE.md`, editorial proposals, and art intake or approval need no test run.
- For code, config, or layout changes, run the tests that cover them (for example `python -m unittest discover -s tests -p 'test_hero_record.py'` with the project Python), or `make test` for broad changes (both suites, modules in parallel, under a minute).
- CI (`.github/workflows/repository-checks.yml`) runs the full suite on every push to `main` except one that changes only `production/STATE.md` or its archive, editorial proposals, an art delivery (incoming images and receipts), or the build request or review ledger (whose build runs the suite); if it goes red, fix it.
- `python tools/dev.py check` is the full local check (dependencies, preflight, snapshot history, whitespace, and every test). The build workflows run the suite again before building.

## By task

| Task | Read |
|---|---|
| Manuscript changes | `docs/WORKFLOW.md`, `docs/MANUSCRIPT_UPDATES.md` |
| Layout | `docs/DESIGN.md`, `docs/LAYOUT_WORKFLOW.md` |
| Builds and releases | `docs/BUILD_AUTOMATION.md`, `docs/BUILD_CARD.md` |
| Artwork | `production/art/codex/BATCH_CARD.md`, `production/art/skill/heraldry-classic-ink-art/SKILL.md`, `docs/ART_AUTOMATION.md` |
| Rules figures | `figures/README.md` |
| Player aids | `docs/PLAYER_AIDS.md` |
| Hero records | `assets/hero-record/README.md` |
| Editorial review | `editorial/proposals/README.md`, the `blind-editorial-reviewer` role (`docs/agents/`) |

Add a short entry to the top of `production/STATE.md` at each milestone.
