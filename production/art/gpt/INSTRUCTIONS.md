# ChatGPT Work: standing instructions for Heraldry illustrations (v6 proposed)

The GitHub repository is the source of truth. Claude Code prepares prompts, queue, reference sets and review decisions. ChatGPT Work generates native images and returns exact bytes, receipts, and QA evidence. Work never edits prompts, queue, source rules, or other code while processing illustration batches.

Use the installed `heraldry-classic-ink-art` v6 skill (source in `production/art/skill/heraldry-classic-ink-art/`). If not installed, read `SKILL.md` from the checked-out repository. The queue remains `production/art/gpt/QUEUE.json`, schema 2; prompts and prompt_sha256 are immutable per item; each item lists its own references (at most 3), must-show and do-not-draw clauses, native size, and attempt budget.

## Session start

1. Obtain a clean local checkout of `main` with only queue-listed LFS references fetched. Never download the private PDFs by default.
2. Run `scripts/work_preflight.py --repo . --require-installed`; if authentication/Git LFS is unavailable, choose bundle handoff.
3. Run the queue runner `scripts/heraldry_art.py doctor`, `status` and `show ID`.
4. Establish with a real smoke test that the image tool accepts the intended reference set and produces native image bytes accessible to Python. Do not assume @GitHub alone provides these capabilities.

Commands use the full path `python production/art/skill/heraldry-classic-ink-art/scripts/<script>.py` from the repo root.

## Per-item contract

- Use the exact queued prompt without paraphrasing, inserting new lore, or reconstructing prompts from the illustration list. Up to two targeted correction sentences may be added on a retry; record them.
- Attach only the item references in order. If references are missing, stop; do not quietly generate an unanchored replacement. This is stricter than the v4 degraded-reference fallback and prevents art-style drift.
- Generate at the exact requested size where supported. The v6 mechanical gate reports any pixel-size mismatch; only documented tool limitations permit a non-exact image to proceed to independent review.
- Save the original native image to a scratch file; keep it byte-identical. Never alter or upscale it for delivery.
- Run `heraldry_art.py check ID SCRATCH_IMAGE` and inspect its actual print-size preview and referenced images. The tripwires cannot judge artistic excellence.
- Create a scratch QA JSON using `fidelity_gate.py create`, fill all ten visual checks with genuine image-specific evidence, and ensure image/reference/prompt hashes match. For a passing candidate, run `heraldry_art.py save ID IMAGE --qa-file /scratch/ID.qa.json [--must ...] [--avoid-clear]`. No QA report means no save.
- Stop at the first clearly passing candidate, within the queue's `max_attempts`. At exhaustion only, the existing `--accept-flags` route may hand off a flagged result, with explicit unresolved issues. Work never approves publication art.
- Record one `production/art/gpt/RECEIPTS.jsonl` line per save, preserving existing fields; the v6 helper embeds the ten evidence-backed QA decisions and adds native-image SHA metadata.

## Batches and safe delivery

After 5 images, or at session end, view a contact sheet alongside references. Compare like registers only; look for progressive greying, altered hatching, repeated posing, missing vignettes and reference subject bleed.

Run `delivery_guard.py audit --repo .`, then `delivery_guard.py ship --execute --repo .` only if the audit passes and Git LFS and remote authentication are available. The guard stages ONLY queued incoming images and receipts, refuses unrelated worktree changes, checks LFS pointers, requires local HEAD equal origin/main, and never force-pushes or automatically merges a concurrent reviewer commit. If it stops or a tool is unavailable, run `heraldry_art.py bundle` outside the clone; deliver the ZIP without claiming a Git push.

The first queue phase (`anchors`) ends after delivery of its five items, until Claude Code reviews them and publishes a new queue. On rejection, use the recorded review reason and another attempt budget as permitted by the queue. Do not start a batch without an updated queue.

## Authority and limitations

1. Item prompt + must/avoid clauses govern depicted facts.
2. `QUEUE.json` governs IDs, formats, reference sets, budgets and workflow.
3. The v6 skill governs production and QA steps without overriding canonical subject facts.
4. The manuscript and lore remain untouched by Work.

This process improves consistency but cannot guarantee visually identical generation across all subjects. Exact replay of an already approved asset requires copying the approved bytes rather than regenerating it. Automated tests verify package integrity and mechanical gates, not final artistic quality. Claude Code/owner makes the final publishing decision.
