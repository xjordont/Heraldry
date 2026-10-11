# Agents working in this repository (Codex and others)

`CLAUDE.md` is the governing contract for this repository and applies to every agent. Codex's role (owner decision 2026-10-11) is **art worker**. Its complete working contract is `production/art/codex/BATCH_CARD.md`; read that, not the long docs. Background, only if needed: `production/art/codex/CODEX_RUNBOOK.md` and the v6 skill `production/art/skill/heraldry-classic-ink-art/SKILL.md`.

Hard limits:

- Write only `assets/art/incoming/ART-*.{png,jpg,webp}` and `production/art/gpt/RECEIPTS.jsonl`, through `heraldry_art.py save` and `delivery_guard.py ship --execute`.
- Never edit prompts, the queue, the manuscript (`source/`, `editorial/`), tools, config, figures, layout or the skill. Claude Code owns those.
- Never approve art, build PDFs or dispatch workflows. Work on `main` only: no branches, no force-push, no history rewriting.
- Never print, log or commit a credential. Use the owner's existing Git login. Never use a paid image API; generate within the owner's ChatGPT plan.
