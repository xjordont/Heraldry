# Heraldry Skirmish art runner v8: operator card

## Before generation

Work in the `xjordont/Heraldry` repository on `main`, following `SKILL.md`. On Codex, `production/art/codex/BATCH_CARD.md` is the one-page contract. Generate, check and deliver unchanged native image files. Never modify the prompts, manuscript or queue while running it.

```
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

No authenticated Git? Use the offline Work input package (`tools/art_work_package.py`):
1. Unzip it into an empty folder and follow its `START_HERE.md`.
2. Add `--offline-package` to the preflight. It must report READY, `delivery: bundle` and `remote_access: NOT_ATTEMPTED`.
3. Deliver with `bundle --evidence ...` and say that nothing was pushed.

On the first item, confirm that the image tool accepts the listed references and that you can save the native file; if either fails, stop and report. Repository access alone does not prove either.

## Per item

1. `show ID`. Paste the exact prompt and attach **only** the listed references, all of them. Look at a reference set's images once, the first time its `ref_set` appears in the session.
2. Target the maximum output resolution: the largest size and highest quality offered at the listed aspect, never the default (owner 2026-10-12). Keep the original bytes in the scratch folder.
3. `check ID FILE`. Inspect the original and the print-size preview beside the references, including whether the image is as gritty and bold as they are.
4. `qa ID FILE`: complete the ten criteria with visible evidence. Then `save ID FILE --must ... --avoid-clear --model "..."`. Never invent a pass.
5. One generation per item, in a fresh context; never retry. A hard fail is saved with `--accept-flags --notes "<what is wrong>"`; a rejection brings it back as a redo with its own single generation with correction sentences (`references/REPAIR.md`).

## Delivery and stopping

- **DELIVER** (after every save): `delivery_guard.py ship --execute --repo .`. It runs every delivery check itself; `audit` is the same check without the push, for diagnosis only.
- **DRIFT REVIEW** (every tenth save):
  1. Run `sheet --recent 10 --refs` and `style_audit.py --repo . --recent 10` (both write to the scratch folder).
  2. Look at the sheet once, then deliver in every case.
  3. If two or more images of the same register share a drift, report it and continue.
- If `ship` says BLOCKED: run `bundle`, report it, and stop. Never pull, rebase or force.
- Resume from `status`. Never regenerate a delivered item unless it is listed as a `redo`.
- Approval comes after the intake inks the images: look at each, then `tools/art_intake.py approve` or `reject` (`SKILL.md`, hard rule 7). You may approve your own images.

## Session prompt

Codex uses `production/art/codex/CODEX_PROMPT.md`. For ChatGPT Work:

> Use the Heraldry Skirmish Classic Ink Art v8 skill on xjordont/Heraldry, main. Run the preflight, doctor and status, then generate the queued illustrations in order using the exact repository prompts and each item's listed references. For each native image run check, inspect the image and its print-size preview, complete the ten-criterion QA record, and save. Deliver each image through the guarded process (or a labelled bundle), with a drift review every ten images. Generate once per item, and stop at NOTHING LEFT or any hard blocker. Report completed IDs, failures, commits or bundles, and the next ID. Never edit the queue, prompts, manuscript or code.
