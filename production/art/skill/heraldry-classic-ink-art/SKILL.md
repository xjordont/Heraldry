---
name: heraldry-classic-ink-art
description: Runs the Heraldry Skirmish illustration queue from the GitHub repo xjordont/heraldry. For each queued item it generates one black pen-and-ink illustration from the repo's prepared prompt and that item's own short reference set, checks it against the prompt's must-show and do-not-draw lists, saves it unmodified to assets/art/incoming/<ID>.png, logs a receipt and commits in small batches. Use when asked to generate, resume, redo or review Heraldry artwork. Never writes or edits prompts, the manuscript or tools.
---

# Heraldry Skirmish illustration runner (v4)

## Who does what

The repo is the single source of truth. Claude Code, a separate agent, writes every prompt, queue, reference set and review. You generate images and deliver them. `production/art/gpt/QUEUE.json` says what to draw, `production/art/gpt/prompts/<ID>.txt` is the exact prompt for each item, and `production/art/ILLUSTRATION_LIST.md` (the owner's "illustrations.md") is the human-readable catalogue of the same prompts. If the list and a prompt file ever differ, the prompt file wins. Never run from the list.

You do not plan scenes or write prompts. The planning was done and audited for uniqueness before the queue was published. Improvising at run time is where drift, duplicates and contradictions of the rulebook come from.

## Hard rules

1. Use each prompt file verbatim as the image prompt. Do not shorten, paraphrase, translate or "improve" it. The only permitted addition is one correction sentence on a retry (`references/REPAIR.md`), which you record in the receipt notes.
2. Attach only the images in that item's `references` (at most three). Attach nothing else. Never attach the whole reference folder.
3. Generate only IDs listed in `QUEUE.json`. Never regenerate a delivered image unless `status` shows it as `redo` or the owner asks.
4. Request the item's `size` exactly: 1536x1024 (wide 3:2), 1024x1536 (tall 2:3) or 1024x1024 (square), at the highest quality the tool offers. No upscaling and no print preparation: the repo's intake does that.
5. Save the image exactly as the tool delivered it. No crop, resize, sharpen, retouch or format conversion.
6. Change no file except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`. Do not edit the manuscript, queue, prompts, tools or this skill. No branches. No force-push.
7. Never call the images hand-drawn and never mark one approved. Claude Code reviews and approves.
8. Work without asking for confirmation between items. Stop only at the stop conditions below.

## Session start

First time only: clone `xjordont/heraldry` (a private repo; use the access the owner gave you) with `GIT_LFS_SKIP_SMUDGE=1` set, so the private reference PDFs are not downloaded, then run `git lfs install --local` inside it.

Every session, from the repo root:

```
git pull --rebase origin main
git lfs pull --include="assets/art/incoming/*.png"
python scripts/heraldry_art.py doctor
python scripts/heraldry_art.py status
```

(`scripts/` is this skill's folder; give the full path if the skill is installed elsewhere.) `doctor` must say READY, or READY TO GENERATE (see the no-git stop condition below). `status` prints the single next action. Obey it.

## Phases

- `anchors` (currently 5 images). Generate them, push, then stop. Tell the owner: "Anchors pushed. Ask Claude Code to review them and publish the batch queue." Do not start the batch.
- `batch`. Work through the queue in order. Anchor images are already approved and appear in the items' references.

## For each item

1. `python scripts/heraldry_art.py show ID` prints the item's references, size, size class, MUST BE SHOWN list, DO NOT DRAW list and the verbatim prompt. Read the lists before generating.
2. Attach the listed references. Paste the whole prompt. Request the size.
3. When the image arrives, save the tool's file to a scratch path, then run `python scripts/heraldry_art.py check ID <file>`. It writes a print-size preview. Look at the image itself and at the preview, and answer the ten questions below. The numbers are tripwires, not a quality score.
4. No hard fail: `python scripts/heraldry_art.py save ID <file> --attempts N --model "<image model if shown>" --notes "<anything unusual>"`. It re-checks, copies the bytes untouched to `assets/art/incoming/` with the true extension and appends the receipt. Add `--redo` only when the owner asked you to replace an image that was already delivered; items that `status` lists as `redo` do not need it.
5. Any hard fail: retry using `references/REPAIR.md`, up to the item's `max_attempts` (usually 3; cover and chapters 5). Stop at the first attempt with no hard fail. After the last allowed attempt, save the best one with `--accept-flags --notes "<what is still wrong>"`. Do not keep trying.

## Hard fails: reject the variant if any is true

1. Wrong subject, or anything contradicts SOURCE TEXT.
2. A "Must be shown exactly" item is missing or miscounted. Count limbs, eyes, heads and weapons.
3. A "Do not draw" item is present.
4. Any lettering, runes, signature, watermark, caption or pseudo-writing.
5. Colour, grey wash, gradients or paper texture. Ink marks only, on flat near-white paper.
6. A frame, box or hard crop. A figure or still life that is not isolated on white with about 8% margin and nothing cropped. A scene that does not fade to white on all four sides.
7. Subject bleed from a reference (oaks, standing stones, a palisade gate, a timber bridge, a skeleton with a shield) that the prompt did not ask for.
8. Broken anatomy or construction: wrong limb counts, unheld weapons, floating parts, impossible architecture, cloned elements.
9. A human scale figure the prompt did not ask for, or a requested one missing. The prompt's `Size:` line is canonical.
10. The subject is not unmistakable in the print-size preview.

Details, soft style checks and the batch drift review: `references/QA_CHECKLIST.md`. Style and the two registers: `references/STYLE.md`. Per-family expectations: `references/FAMILIES.md`.

## After each batch of 5–10 saved items (and at session end)

1. `python scripts/heraldry_art.py sheet --refs` writes a contact sheet of the saved items beside the first item's references. Look for drift (thicker or thinner line, grey tone, different finish), repeated poses or compositions, and scenery behind figures. Redo the one or two worst if attempts remain.
2. Commit and push:

```
git add assets/art/incoming production/art/gpt/RECEIPTS.jsonl
git commit -m "art(gpt): <first id> .. <last id>"
git pull --rebase origin main
git push origin main
```

If the push is rejected, pull with rebase and push again. `git lfs ls-files` must list each new PNG. If it does not, stop: git-lfs is not active and the PNGs would be committed as ordinary files.

3. Style drift is a known risk in very long image threads. After about 20 items, suggest the owner start a fresh conversation and paste the resume prompt from `OPERATOR_CARD.md`.

## Stop conditions

- Anchors pushed (above), or the queue is empty.
- The image tool refuses an item. Do not reword the prompt to get around it. Record it with `python scripts/heraldry_art.py refuse ID --reason "<the tool's message>"` (commit RECEIPTS.jsonl with the next batch), list it in your report, and continue with the next item.
- Quota or rate limit. Commit what is saved, report the counts and the next ID, and stop.
- `doctor` says NOT READY (broken queue, prompts or references, or a branch other than main), a prompt does not match its queue hash after a pull, or the queue is schema 1. Report it and stop.
- `doctor` says delivery by git is blocked (no git or git-lfs): keep generating and saving, and finish each batch with `python scripts/heraldry_art.py bundle --out batch.zip`; hand the zip to the owner. If you cannot run Python either, do the same steps by hand and deliver the images, named `<ID>.png`, with one receipt line each (`references/QA_CHECKLIST.md` shows the format).

## Report at the end of every session

IDs saved and pushed, attempts used, items saved with tripwires or `--accept-flags`, items skipped and why, the next ID. State plainly what you could not verify.

## Not in the queue

Do not generate it. Ask the owner to have Claude Code add it to the catalogue. For an explicit one-off outside the book, see `references/AD_HOC.md`.
