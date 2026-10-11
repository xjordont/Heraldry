# Prompt to paste into Codex

The same text works for every session. Codex reads the current queue from the repository.

```text
You are the art worker for the Heraldry Skirmish rulebook in this repository (xjordont/Heraldry, branch main). Read AGENTS.md, then production/art/codex/CODEX_RUNBOOK.md, and follow it exactly. It points to the v6 skill at production/art/skill/heraldry-classic-ink-art/SKILL.md, whose per-item contract you must follow.

1. Make sure the clone is set up as in the runbook (autocrlf false, LFS installed with skip-smudge), the working tree is clean, and `git pull --ff-only origin main` succeeds. Set HERALDRY_SCRATCH to a folder outside the repo.
2. Run work_preflight.py --require-installed, heraldry_art.py doctor and status. Show me the output. If anything says BLOCKED or NOT READY, stop and report it word for word.
3. Image generation: use the image generation included in my ChatGPT plan. Do not use a paid API key. Prefer GPT Image 2.5 Sunburst if available and tell me the exact model name. Before generating any queue item, confirm that you can attach the item's listed reference images and that the result is saved as a real file Python can open; if either fails, stop and tell me.
4. Generate only what status says, in queue order, following SKILL.md: verbatim prompt, only the listed references, largest size at the listed aspect, check, look at the image and print-size preview beside the references, ten-point QA file with real evidence, then save with --qa-file and --model. Art direction: hand-inked, confident contours, economy of line, hatching only for form and shadow, open white paper, like the owner's samples; no hyper-detail, stippling or noisy texture. Retry only within each item's attempt budget.
5. When status asks for delivery: contact sheet with --refs, style audit, then delivery_guard.py audit and, only if it passes, delivery_guard.py ship --execute. Never force-push, never create branches, never commit anything except the queued images and RECEIPTS.jsonl.
6. Stop when status says STOP (for the anchors phase: after delivering all five). Report each ID, the model name, the pixel size produced, attempts, any QA failures or accepted flags, and the commit SHA. Nothing you deliver is approved: Claude Code reviews it.
```
