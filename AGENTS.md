# Agents working in this repository (Codex and others)

`CLAUDE.md` is the governing contract for this repository and applies to every agent, not only Claude. Read it first.

Codex's role (owner decision 2026-10-11): **art worker**. Generate the queued illustrations on the owner's PC and deliver them; see `production/art/codex/CODEX_RUNBOOK.md` and the v6 skill `production/art/skill/heraldry-classic-ink-art/SKILL.md`.

Hard limits for Codex:

- Write only `assets/art/incoming/ART-*.{png,jpg,webp}` and `production/art/gpt/RECEIPTS.jsonl`, and deliver them only with `delivery_guard.py ship --execute`.
- Never edit prompts, the queue, the manuscript (`source/`, `editorial/`), tools, config, figures, layout or the skill. Claude Code owns those and publishes changes.
- Never approve art (`tools/art_intake.py approve*`), build PDFs (`make all`, `make package`) or dispatch workflows.
- Work on `main` only. No branches, no force-push, no history rewriting.
- Never print, log or commit a credential. Use the owner's existing Git login.
- Do not use a paid image API; generate within the owner's ChatGPT plan.
