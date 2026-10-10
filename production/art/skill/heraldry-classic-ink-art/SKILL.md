---
name: heraldry-classic-ink-art
description: Runs the Heraldry Skirmish illustration queue from the GitHub repo xjordont/heraldry. For each queued item it generates one black pen-and-ink illustration from the repo's prepared prompt and that item's own short reference set, checks it against the prompt's must-show and do-not-draw lists, saves it unmodified to assets/art/incoming/<ID>.png, logs a receipt and commits in small batches. Use when asked to generate, resume, redo or review Heraldry artwork. Never writes or edits prompts, the manuscript or tools.
---

# Heraldry Skirmish illustration runner (v4)

## Who does what

The repo is the single source of truth. Claude Code, a separate agent, writes every prompt, queue, reference set and review. You generate images and deliver them. `production/art/gpt/QUEUE.json` says what to draw, `production/art/gpt/prompts/<ID>.txt` is the exact prompt for each item, and `production/art/ILLUSTRATION_LIST.md` (the owner's "illustrations.md") is the human-readable catalogue of the same prompts. If the list and a prompt file ever differ, the prompt file wins. Never run from the list.

You do not plan scenes or write prompts. The planning was done and audited for uniqueness before the queue was published. Improvising at run time is where drift, duplicates and contradictions of the rulebook come from.

**Precedence.** An item's own prompt, must list and do-not-draw list override every general note in this skill, including the family notes and the style page. If the repo's `production/art/gpt/INSTRUCTIONS.md` or the queue differs from this skill on a repo mechanic (paths, queue fields, receipt fields, commit message), follow the repo and say so in your report. The hard rules below never relax.

## Hard rules

1. Use each prompt file verbatim as the image prompt. Do not shorten, paraphrase, translate or "improve" it. The only permitted addition is a correction sentence on a retry (`references/REPAIR.md`), which you record in the receipt notes.
2. Attach only the images in that item's `references` (at most three). Attach nothing else. Never attach the whole reference folder.
3. Generate only IDs listed in `QUEUE.json`. An image is delivered once it is pushed. Never regenerate a delivered image unless `status` lists it as `redo` or the owner asks. Before the push you may regenerate freely, inside the item's attempt budget.
4. Request the item's `size` exactly: 1536x1024 (wide 3:2), 1024x1536 (tall 2:3) or 1024x1024 (square), at the highest quality the tool offers. No upscaling and no print preparation: the repo's intake does that.
5. Save the image exactly as the tool delivered it. No crop, resize, sharpen, retouch or format conversion.
6. Change no file in the clone except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`. Keep everything else you create (downloaded images, previews, contact sheets, bundles) in the scratch folder, outside the clone. `doctor` prints its location and the helper uses it by default. Do not edit the manuscript, queue, prompts, tools or this skill. No branches. No force-push.
7. Never call the images hand-drawn and never mark one approved. Claude Code reviews and approves.
8. Work without asking for confirmation between items. Stop only at the stop conditions below.

## The helper

The helper lives in the repo, so this path is always right and always matches the queue. Run it from the repo root and write the full command each time:

```
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py <command>
```

| Command | Use |
|---|---|
| `doctor` | environment, repo, queue and reference checks; prints the scratch folder |
| `status [--end]` | queue state and the single next action; `--end` at session end |
| `next` | the next items to generate |
| `show ID` | references, size, size class, MUST BE SHOWN and DO NOT DRAW lists, verbatim prompt |
| `check ID FILE` | tripwires for one generated image; counts it as an attempt; writes a print-size preview |
| `save ID FILE ...` | check again, copy the bytes untouched, write the receipt |
| `refuse ID --reason "..."` | record that the image tool refused an item |
| `sheet [ID ...] [--refs]` | contact sheet of saved images; `--refs` adds their references |
| `bundle` | hand-off zip when git cannot push |

## Session start

First time only: clone `xjordont/heraldry` (a private repo; use the access the owner gave you) with `GIT_LFS_SKIP_SMUDGE=1` set, then run `git lfs install --local --skip-smudge` inside it. That keeps the private reference PDFs, and every other large file you do not need, from being downloaded now or by later pulls.

Every session, from the repo root:

```
git pull --rebase origin main
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

If `doctor` lists reference images that are LFS pointers, run the single `git lfs pull --include="..."` command it prints, then run `doctor` again. `doctor` must say READY, or READY TO GENERATE (see the no-git stop condition). `status` prints the single next action. Obey it.

## Phases

- `anchors` (currently 5 images). Generate them, push, then stop. Tell the owner: "Anchors done. Ask Claude Code to review them and publish the batch queue." Do not start the batch. If an anchor was refused, say so; Claude Code decides what that means for the batch.
- `batch`. Work through the queue in order. Anchor images are already approved and appear in the items' references.

## For each item

1. `show ID`. Read the MUST BE SHOWN and DO NOT DRAW lists before generating.
2. Attach the listed references. Paste the whole prompt. Request the size. If the image tool cannot take reference images, or takes fewer than are listed, attach what it takes in the listed order, write `references attached: N of M` in `--notes` and in your report, and never imply references were used when they were not. If the tool shows you a revised prompt or shortens yours, note that too.
3. Save the tool's image into the scratch folder, never inside the clone. Run `check ID FILE`. It counts the attempt, prints the tripwires, writes a print-size preview and lists the MUST and DO NOT DRAW lines again. Look at the image and at the preview and answer the ten questions below. Count the must-show items yourself: the tripwires cannot.
4. No hard fail: `save ID FILE --must "<what you counted or found>" --avoid-clear --model "<image model if shown>" --notes "<anything unusual, including any correction sentence you added>"`. Give one `--must` for each MUST line (none if the list is empty). `--avoid-clear` states that you looked and none of the DO NOT DRAW items is present. `save` checks again, copies the bytes untouched with the true extension, and appends the receipt with the attempts the helper counted, your statements and the attestation. Add `--redo` only when the owner asked you to replace an image that was already delivered; items that `status` lists as `redo` need no flag.
5. Any hard fail: retry using `references/REPAIR.md`, up to the item's `max_attempts` (usually 3; cover and chapters 5). Stop at the first attempt with no hard fail. After the last allowed attempt, or whenever you cannot truthfully give the statements in step 4, save the best attempt with `save ID FILE --accept-flags --notes "<what is still wrong>"`. `--accept-flags` needs the notes and is for nothing else. Then move on.

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

A must-show item and a do-not-draw line that look opposed are almost always about scale or focus. A required grove circle beside "do not repeat the grove scenario" means: draw the circle small, in the middle distance as the composition says, and do not make it the subject. Satisfy both the narrowest way and carry on. Only a prompt that cannot be satisfied at all is a problem to report (`references/REPAIR.md`).

Details, soft style checks and the batch drift review: `references/QA_CHECKLIST.md`. Style and the registers: `references/STYLE.md`. Family defaults: `references/FAMILIES.md`.

## Batches and pushes

`status` asks for a push when 5 images are saved and unsent, when nothing is left to generate, and at session end if you run `status --end`. Never hold more than 10 unsent.

1. Drift review first: `sheet --refs` puts the saved, unpushed images beside the references of every item on the sheet. Look for drift (thicker or thinner line, grey tone, different finish), repeated poses or compositions, and scenery behind figures. Redo the one or two worst before you push; the attempt budget still counts every attempt.
2. Commit and push:

```
git add assets/art/incoming production/art/gpt/RECEIPTS.jsonl
git lfs ls-files
git commit -m "art(gpt): <first saved id> .. <last saved id>"
git pull --rebase origin main
git push origin main
```

`git lfs ls-files` lists staged PNGs, so run it before the commit: every new PNG must appear. If one does not, stop: git-lfs is not active and the PNG would be committed as an ordinary file. JPEG and WebP images are not stored with LFS. Refused IDs are not part of the message's range; their receipt lines go in with the batch. If the push is rejected, pull with rebase and push again.

3. Style drift is a known risk in very long image threads. After about 20 items, suggest the owner start a fresh conversation and paste the resume prompt from `OPERATOR_CARD.md`.

## Stop conditions

- The anchors are done, or the queue is empty.
- The image tool refuses an item. Do not reword the prompt to get around it. Record it with `refuse ID --reason "<the tool's message>"` (its receipt line goes in with the next batch), list it in your report, and continue with the next item.
- Quota or rate limit. Push what is saved, report the counts and the next ID, and stop.
- `doctor` says NOT READY (broken queue, prompts or references, or a branch other than main), a prompt does not match its queue hash after a pull, or the queue is schema 1. Report it and stop.
- `doctor` says delivery by git is blocked (no git or git-lfs): keep generating and saving, and finish each batch with `bundle`; hand the zip to the owner. If you cannot run Python either, do the same steps by hand and deliver the images, named `<ID>.<ext>` with their true extension, with one receipt line each (`references/QA_CHECKLIST.md` shows the format).

## Report at the end of every session

IDs saved and pushed, attempts used, items saved with `--accept-flags`, items refused, differences you found between the repo and this skill, the next ID. State plainly what you could not verify.

## Not in the queue

Do not generate it. Ask the owner to have Claude Code add it to the catalogue. For an explicit one-off outside the book, see `references/AD_HOC.md`.
