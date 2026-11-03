# Standing instructions for Heraldry illustrations (skill v8)

The GitHub repository is the source of truth for prompts, queue and reference sets. The art worker (Codex on the owner's PC, or another client with an authenticated Git checkout) generates native images and returns exact bytes, receipts, and QA evidence, and never edits prompts, queue, source rules, or code while processing illustration batches.

Use the installed `heraldry-classic-ink-art` v8 skill (source in `production/art/skill/heraldry-classic-ink-art/`). If not installed, read `SKILL.md` from the checked-out repository. The queue remains `production/art/gpt/QUEUE.json`, schema 2; prompts and prompt_sha256 are immutable per item; each item lists its own references (at most five), must-show and do-not-draw clauses, native size, and attempt budget.

## Session start

1. Obtain a clean local checkout of `main` with only queue-listed LFS references fetched. Never ask for, accept, or paste a credential into a conversation (a token route was tried in ChatGPT Work on 2026-10-11 and withdrawn).
2. Run `scripts/work_preflight.py --repo . --require-installed`. If Git cannot authenticate or Git LFS is unavailable, stop and report it: Git push is the only delivery.
3. Run the queue runner `scripts/heraldry_art.py doctor`, `status` and `show ID`.
4. The first item is the capability check: the image tool must accept its listed references and produce native image bytes accessible to Python. If it cannot, stop and report. Do not assume @GitHub alone provides these capabilities.

Commands use the full path `python production/art/skill/heraldry-classic-ink-art/scripts/<script>.py` from the repo root.

## Per-item contract

- Use the exact queued prompt without paraphrasing, inserting new lore, or reconstructing prompts from the illustration list. Up to two targeted correction sentences may be added on a redo; record them.
- Attach only the item references in order. If references are missing, stop; do not quietly generate an unanchored replacement. This prevents art-style drift. An item whose reference set is `none` (owner 2026-10-31) has nothing to attach: generate it from the prompt alone.
- Use the GPT Image 2.5 Sunburst model if the image tool offers it (owner request 2026-10-11); otherwise the default model. Record the model name shown (`save --model`).
- The queue size is the minimum at a fixed aspect. Target the maximum output resolution (owner 2026-10-12): choose the largest size and highest quality the tool offers at that aspect, never the default. `check` warns below the queue's `target_pixels`; the gate fails only a smaller or off-aspect image.
- Art direction (owner 2026-10-11): gritty old-school black-and-white ink. Bold rough contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast, like the item's references. Pure black ink: no grey wash, stipple fields, machine-even texture or clean vector-like line.
- Save the original native image to a scratch file; keep it byte-identical. Never alter or upscale it for delivery.
- Run `heraldry_art.py check ID SCRATCH_IMAGE` and inspect its actual print-size preview and referenced images. The tripwires cannot judge artistic excellence.
- Run `heraldry_art.py qa ID IMAGE` to create the scratch QA JSON, fill all ten visual checks with genuine image-specific evidence, and ensure image/reference/prompt hashes match. For a passing candidate, run `heraldry_art.py save ID IMAGE [--must ...] [--avoid-clear]` (the draft is found automatically). No QA report means no save.
- Generate once per item (`max_attempts` is 1). An image with a hard fail is still saved, with `--accept-flags` and its failures listed as unresolved issues; a rejection brings it back as a redo. Approval follows the intake (`SKILL.md`, hard rule 7).
- Record one `production/art/gpt/RECEIPTS.jsonl` line per save, preserving existing fields; the helper embeds the ten evidence-backed QA decisions and adds native-image SHA metadata.

## Batches and safe delivery

Each image is delivered as soon as it is saved (`push_every: 1`); `status` says DELIVER. Every tenth image it says DRIFT REVIEW: first view `sheet --recent 10 --refs` and run `style_audit.py --recent 10`. Compare like registers only, and look for progressive greying, a cleaner or softer finish than the references, altered hatching, repeated posing, missing vignettes and reference subject bleed.

Run `delivery_guard.py ship --execute --repo .`; it validates everything first and needs Git LFS and remote authentication. The guard stages ONLY queued incoming images and receipts, refuses unrelated worktree changes, checks LFS pointers, fast-forwards over upstream commits only when they touch none of the delivered files, stops on divergence or overlap, and never force-pushes or merges. If it stops or a tool is unavailable, stop and report the reason; the saved images and receipts stay in the clone for a later `ship`. Never claim a push that did not happen.

An `anchors` phase, when one is published, ends after delivery of its items until they are approved. In the batch phase, a rejected image returns as a `redo` with the rejection reason and a fresh attempt budget; `status` puts redos first.

## Authority and limitations

1. Item prompt + must/avoid clauses govern depicted facts.
2. `QUEUE.json` governs IDs, formats, reference sets, budgets and workflow.
3. The v8 skill governs production and QA steps without overriding canonical subject facts.
4. The art worker never touches the manuscript or lore.

Exact replay of an already approved asset requires copying the approved bytes rather than regenerating it. The owner has the final say on what is published.
