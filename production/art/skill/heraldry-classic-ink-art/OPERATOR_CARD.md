# Heraldry Skirmish art runner v7: operator card

## Before generation

Work in the `xjordont/Heraldry` repository on `main`, following `SKILL.md`. On Codex, `production/art/codex/BATCH_CARD.md` is the one-page contract. Claude Code owns the prompts, queue, references and approvals. You generate, check and deliver unchanged native image files. Never modify the prompts, manuscript or queue.

```
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

No authenticated Git? Use the offline Work input package (`tools/art_work_package.py`):
1. Unzip it into an empty folder and follow its `START_HERE.md`.
2. Add `--offline-package` to the preflight. It must report READY, `delivery: bundle` and `remote_access: NOT_ATTEMPTED`.
3. Deliver with `bundle --evidence ...` and say that nothing was pushed.

Confirm with a real smoke test that the image tool accepts the queue's references and that the native image file is accessible. Repository access alone does not prove either.

## Per item

1. `show ID`. Paste the exact prompt and attach **only** the listed references, all of them. Look at a reference set's images once, the first time its `ref_set` appears in the session.
2. Request the largest size and best quality offered at the listed aspect. Keep the original bytes in the scratch folder.
3. `check ID FILE`. Inspect the original and the print-size preview beside the references, including whether the image is as gritty and bold as they are.
4. `qa ID FILE`: complete the ten criteria with visible evidence. Then `save ID FILE --must ... --avoid-clear --model "..."`. Never invent a pass.
5. Retry narrowly within the item's budget (`references/REPAIR.md`). When the budget runs out, save the best attempt with `--accept-flags` and record what is still wrong. That is never an approval.

## Delivery and stopping

- **DELIVER** (after every save): `delivery_guard.py audit --repo .`, then `delivery_guard.py ship --execute --repo .`.
- **DRIFT REVIEW** (every tenth save):
  1. Run `sheet --recent 10 --refs` and `style_audit.py --repo . --recent 10 --out <scratch>/style.json`.
  2. Look at the sheet once. Stop if two or more images of the same register share a drift.
  3. Deliver.
- If `ship` says BLOCKED: run `bundle`, report it, and stop. Never pull, rebase or force.
- Resume from `status`. Never regenerate a delivered item unless it is listed as a `redo`.

## Session prompt

Codex uses `production/art/codex/CODEX_PROMPT.md`. For ChatGPT Work:

> Use the Heraldry Skirmish Classic Ink Art v7 skill on xjordont/Heraldry, main. Run the preflight, doctor and status, then generate the queued illustrations in order using the exact repository prompts and each item's listed references. For each native image run check, inspect the image and its print-size preview, complete the ten-criterion QA record, and save. Deliver each image through the guarded process (or a labelled bundle), with a drift review every ten images. Retry only within each item's budget, never self-approve, and stop at NOTHING LEFT or any hard blocker. Report completed IDs, failures, commits or bundles, and the next ID. Never edit the queue, prompts, manuscript or code.
