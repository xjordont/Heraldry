---
name: heraldry-classic-ink-art
description: Runs the Heraldry Skirmish illustration queue from the GitHub repo xjordont/heraldry. For each queued item it generates one black pen-and-ink illustration from the repo's prepared prompt and that item's own short reference set, checks it against the prompt's must-show and do-not-draw lists, saves it unmodified to assets/art/incoming/<ID>.<ext>, logs a receipt and delivers each image to main with a guarded push. Use when asked to generate, resume, redo or review Heraldry artwork. Never writes or edits prompts, the manuscript or tools.
---

# Heraldry Skirmish illustration runner (v7)

## Who does what

The repo is the single source of truth. Claude Code, a separate agent, writes every prompt, queue, reference set and review. You generate images and deliver them. `production/art/gpt/QUEUE.json` says what to draw, `production/art/gpt/prompts/<ID>.txt` is the exact prompt for each item, and `production/art/ILLUSTRATION_LIST.md` (the owner's "illustrations.md") is the human-readable catalogue of the same prompts. If the list and a prompt file ever differ, the prompt file wins. Never run from the list.

You do not plan scenes or write prompts. The planning was done and audited for uniqueness before the queue was published. Improvising at run time is where drift, duplicates and contradictions of the rulebook come from.

**Precedence.** An item's own prompt, must list and do-not-draw list override every general note in this skill, including the family notes and the style page. The prompt's own wording wins over this skill's shorthand: its "warm ivory-white paper", for example, is the flat near-white paper the checks mean. If the repo's `production/art/gpt/INSTRUCTIONS.md` or the queue differs from this skill on a repo mechanic (paths, queue fields, receipt fields, commit message), follow the repo and say so in your report. The hard rules below never relax.

## Hard rules

1. Use each prompt file verbatim as the image prompt. Do not shorten, paraphrase, translate or "improve" it. The only permitted addition is up to two correction sentences on a retry (`references/REPAIR.md`), which you record in the receipt notes.
2. Attach only the images in that item's `references` (at most three). Attach nothing else. Never attach the whole reference folder.
3. Generate only IDs listed in `QUEUE.json`. An image is delivered once it is pushed. Never regenerate a delivered image unless `status` lists it as `redo` or the owner asks. A redo starts a fresh attempt budget, and `show` prints the reviewer's reason: base your correction sentence on it. If the reason conflicts with the prompt's must or do-not-draw lines, the prompt wins; say so in your report. Before the push you may regenerate freely, inside the item's attempt budget.
4. The item's `size` is the minimum and fixes the aspect: wide 3:2 (1536x1024), tall 2:3 (1024x1536) or square 1:1 (1024x1024). Request the largest size and highest quality the tool offers at that aspect; a larger native image at the same aspect passes. Use the GPT Image 2.5 Sunburst model if the tool offers it (owner request), otherwise the default image model, and record the exact model name shown with `save --model`. No upscaling and no print preparation: the repo's intake does that.
5. Save the image exactly as the tool delivered it. No crop, resize, sharpen, retouch or format conversion.
6. Change no file in the clone except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`. Keep everything else you create (downloaded images, previews, contact sheets, bundles) in the scratch folder, outside the clone. `doctor` prints its location and the helper uses it by default (set `HERALDRY_SCRATCH` to another folder outside the clone if the system temp folder is not available). Do not edit the manuscript, queue, prompts, tools or this skill. No branches. No force-push.
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
| `next [--n N]` | the next items to generate (8 unless `--n`) |
| `show ID` | references, size, size class, MUST BE SHOWN and DO NOT DRAW lists, verbatim prompt |
| `check ID FILE` | tripwires for one generated image; counts it as an attempt; writes a print-size preview |
| `save ID FILE ...` | check again, copy the bytes untouched, write the receipt |
| `refuse ID --reason "..."` | record that the image tool refused an item |
| `sheet [ID ...] [--refs]` | contact sheet of saved images; `--refs` adds their references |
| `bundle [--evidence FILE ...]` | review hand-off zip (native images, receipts, QA reports, hash manifest) when git cannot push |
| `work_preflight.py` | read-only Python, LFS, queue, references, remote auth and model-smoke status; `--offline-package` verifies a Work input package without Git |
| `fidelity_gate.py` | create/verify byte-bound QA JSON (all ten criteria require visual evidence) |
| `delivery_guard.py` | `audit`, `ship --execute`: verify native hashes, receipts, reference and prompt hashes, clean index, and Git LFS before delivery |
| `style_audit.py` | advisory four-edge and same-register style drift report (scratch only); supplements the contact sheet |

## Session start

**Two input routes.** (a) An authenticated Git checkout, below. (b) An **offline Work input package**: a ZIP that Claude Code builds with `tools/art_work_package.py` from a named commit, holding the exact queue, its prompt files, every queue-listed reference as real image bytes, this complete skill, receipts and selection state, each with SHA-256 in `WORK_PACKAGE.json`. Use (b) when shell git cannot authenticate or the GitHub connector cannot fetch the binary references. Unzip it into an empty folder, treat that folder as the clone, and follow its `START_HERE.md`: `work_preflight.py --repo . --offline-package --require-installed` must say READY with `delivery: bundle` and `remote_access: NOT_ATTEMPTED`. Never `git init`, clone or pull there. Everything else in this skill applies unchanged except delivery: `delivery_guard.py` needs Git and refuses, so every batch ends with `bundle` and an explicit statement that nothing was pushed. The package proves only its inputs; the image-reference and native-file smoke test is still yours to do.

Route (a), first time only: clone `xjordont/heraldry` (a private repo; use the access the owner gave you) with `GIT_LFS_SKIP_SMUDGE=1` set, then run `git lfs install --local --skip-smudge` inside it. That keeps the private reference PDFs, and every other large file you do not need, from being downloaded now or by later pulls.

Every session, from the repo root, first run `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed` and follow `references/WORK_OPERATIONS.md`. A GitHub connector without local Git LFS is not a substitute for a successful push. Then:

```
# Only pull while the checkout is clean. If prior images/receipts are unsent,
# use status and the guarded delivery/bundle procedure instead of rebasing.
git pull --ff-only origin main
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

If `doctor` says NOT READY YET, run the single `git lfs pull --include="..."` command it prints (reference images that are still LFS pointers), then run `doctor` again. `doctor` must say READY, or READY TO GENERATE (see the no-git stop condition). `status` prints the single next action. Obey it.

## Phases

- `anchors` (a short calibration set, when one is published). Generate them, push, then stop. Tell the owner: "Anchors done. Ask Claude Code to review them and publish the batch queue." Do not start the batch. If an anchor was refused, say so; Claude Code decides what that means for the batch.
- `batch`. Work through the queue in order and keep going between deliveries until `status` says NOTHING LEFT. The first ten items cover one of each reference set, so the first drift review tests every set. References are the owner's gritty ink samples and a few public-domain prints chosen for the same look; generated images are never references. Each item's `ref_set` names its set: look at a set's images once, the first time it appears in the session.

## For each item

1. `show ID`. Read the MUST BE SHOWN and DO NOT DRAW lists before generating.
2. Attach the listed references. Paste the whole prompt. Request the size. If the image tool cannot accept every required reference, STOP and report a capability blocker; do not silently proceed with an unanchored image. If the tool shows you a revised prompt or shortens yours, report the deviation and do not attest that the queued prompt was unchanged.
3. Save the tool's image into the scratch folder, never inside the clone. Run `check ID FILE`. It counts the attempt (every distinct image you check is one; the count carries on through a redo before the push and starts afresh only after the image has been delivered and sent back), prints the tripwires, writes a print-size preview and lists the MUST and DO NOT DRAW lines again. Look at the image and at the preview and check each of the ten hard fails below (each is true or false). Count the must-show items yourself: the tripwires cannot. Keep every attempt's file in the scratch folder until the item is saved, so you can go back to the best one; each attempt's preview is kept too. Some DO NOT DRAW lines name another entry ("Not the Undead Champion"): before you attest, open that entry's reference image if it is among your references, or its delivered image (`assets/art/incoming/<ID>.<ext>`); if neither exists, read what that entry's own prompt describes (`show` its ID) and make sure your attempt is not that.
4. No hard fail: first create and finish a scratch visual QA JSON following `references/STYLE_CONSISTENCY.md` and `references/WORK_OPERATIONS.md`, set `visual_review_at_print_size: true` and `register_compared` accurately, then run `save ID FILE --qa-file /scratch/ID.qa.json --must "<what you counted or found>" --avoid-clear --model "<image model if shown>" --notes "<anything unusual, including any correction sentence you added>"`. Give exactly one `--must` for each MUST line, in order, each a real statement such as `"counted 8 legs, 4 a side"`; give none if the list is empty. `--avoid-clear` states that you looked and none of the DO NOT DRAW items is present. `save` checks again, copies the bytes untouched with the true extension, and appends the receipt with the attempts the helper counted, your statements and the attestation. Add `--redo` only when the owner asked you to replace an image that was already delivered; items that `status` lists as `redo` need no flag. `--attempts N` can only raise the count the helper recorded, for images you generated but did not check.
5. Any hard fail: retry using `references/REPAIR.md`, up to the item's `max_attempts` (usually 3; cover and chapters 5). Stop at the first attempt with no hard fail. After the last allowed attempt, save the best attempt with `save ID FILE --qa-file /scratch/ID.qa.json --accept-flags --notes "<what is still wrong>"`. The best attempt is the one that breaks the fewest hard fails; if tied, the one whose subject is most accurate. It is never a byte copy of another image. The helper refuses `--accept-flags` until you have checked as many images as the budget allows, and it marks the receipt. It is for nothing else. If every attempt was a copy of a reference or of another image, save nothing: `refuse ID --reason "the tool keeps returning a copy of <path>"`. Then move on.

## Hard fails: reject the variant if any is true

1. Wrong subject, or anything contradicts SOURCE TEXT.
2. A "Must be shown exactly" item is missing or miscounted. Count limbs, eyes, heads and weapons.
3. A "Do not draw" item is present.
4. Any lettering, runes, signature, watermark, caption or pseudo-writing.
5. Colour, grey wash, gradients or paper texture. Ink marks only, on flat, even paper (the warm ivory-white the prompt asks for is fine).
6. A frame, box or hard crop. A figure or still life that is not isolated on white with about 8% margin and nothing cropped. A scene that does not fade to white on all four sides.
7. Subject bleed from a reference that the prompt did not ask for: anything on the bleed list in `references/STYLE.md` (a throne, a full moon, a crowd of skulls, period ruffs and breeches, a palisade gate with twin towers, a skeleton with a shield).
8. Broken anatomy or construction: wrong limb counts, unheld weapons, floating parts, impossible architecture, cloned elements.
9. A human scale figure the prompt did not ask for, or a requested one missing. Scale follows the prompt: a creature's `Size:` line, or the people a scene says it has.
10. The subject is not unmistakable in the print-size preview.

A must-show item and a do-not-draw line that look opposed are almost always about scale or focus. A required grove circle beside "do not repeat the grove scenario" means: draw the circle small, in the middle distance as the composition says, and do not make it the subject. Satisfy both the narrowest way and carry on. A prompt that cannot be satisfied at all is not for you to fix or to burn attempts on: `refuse ID --reason "prompt cannot be satisfied: <what clashes>"` and move on (`references/REPAIR.md`).

Details, soft style checks and the batch drift review: `references/QA_CHECKLIST.md`. Style and the registers: `references/STYLE.md`. Family defaults: `references/FAMILIES.md`.

## Delivery and drift review

The batch queue sets `push_every: 1` and `review_every: 10` (owner 2026-10-11): every image is delivered as soon as it is saved, so a usage limit never strands work, and every tenth image triggers a drift review. `status` says which.

1. **DELIVER** (after each save): run the guarded delivery below.
2. **DRIFT REVIEW** (every tenth save): first `sheet --recent 10 --refs` and `style_audit.py --repo . --recent 10 --out <scratch>/style.json`, and read `references/VISUAL_ACCEPTANCE.md`. Look for drift (thicker or thinner line, grey tone, a cleaner or softer finish than the references), repeated poses or compositions, and scenery behind figures. Redo the worst before delivering; the attempt budget still counts every attempt. Then deliver.

```
python production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .   # validates, then commits and pushes
```

`ship` fast-forwards over the intake bot's commits when they touch none of the delivered files, and retries a lost push once more. If the guard blocks (divergence, an overlap, an unknown local change, missing Git LFS, authentication), do **not** force-push, rebase or assume delivery. Use `bundle`, report that no push occurred, and stop. The guard commits only queue IDs under `assets/art/incoming` and the JSONL receipts. Claude Code controls review, inking, proofs and approval.

3. At the end of a session run `status --end`, do what it says, then write the report.
4. Style drift is a known risk in very long image threads. After about 20 items in one conversation, start a fresh one with the same session prompt; `status` resumes exactly where you stopped.

## Stop conditions

- The anchors are done, or the queue is empty.
- The whole batch has drifted: the drift review shows the same fault in most of the images, not in one or two. Push what is good, stop, and tell the owner.
- The image tool refuses an item. Do not reword the prompt to get around it. Record it with `refuse ID --reason "<the tool's message, or what happened if it gave none>"` (its receipt line goes in with the next batch), list it in your report, and continue with the next item.
- Quota or rate limit, or the tool stops returning images without refusing (two attempts in a row with no image). Push what is saved, report the counts and the next ID, and stop. Nothing is recorded for an item you did not finish.
- `doctor` says NOT READY (not "NOT READY YET", which has its own one-step fix): a broken queue, prompts or references, or a branch other than main. Also a prompt that does not match its queue hash after a pull, or a queue that is schema 1. Report it and stop.
- `doctor` says delivery by git is blocked (no git or git-lfs): keep generating and saving, and finish each batch with `bundle`; hand the zip to the owner. If you cannot run Python either, do the same steps by hand and deliver the images, named `<ID>.<ext>` with their true extension, with one receipt line each (`references/QA_CHECKLIST.md` shows the format).

## Report at the end of every session

IDs saved and pushed, attempts used, items saved with `--accept-flags`, items refused, differences you found between the repo and this skill, the next ID. State plainly what you could not verify.

## Not in the queue

Do not generate it. Ask the owner to have Claude Code add it to the catalogue. For an explicit one-off outside the book, see `references/AD_HOC.md`.


## Release gates (v7)

The exact queued prompt and its must and do-not-draw clauses remain authoritative. These gates add release-process requirements, not subject facts. No visual QA record overrides the prompt; if a prompt contradicts the rulebook, refuse and escalate for Claude Code to fix upstream.

- **Capability smoke test:** `references/WORK_OPERATIONS.md` and `scripts/work_preflight.py` check the environment, references and Git LFS. The image tool must actually accept the listed reference images; the script cannot discover that.
- **Image-bound visual QA:** `qa ID IMAGE` writes the `fidelity_gate.py` draft outside the clone. Complete all ten criteria with concrete evidence; `save` finds the draft. The helper refuses incomplete or stale reports, and a clean `check` never substitutes for looking. See `references/STYLE_CONSISTENCY.md`.
- **Native dimensions (owner 2026-10-11):** the queue size is the minimum at a fixed aspect. Request the largest size offered at that aspect. A smaller or off-aspect image is a recorded exception that needs reviewer approval.
- **Delivery:** only through `delivery_guard.py ship --execute`, which validates first (`audit` runs the same validation alone, for diagnosis). It verifies each image against its latest native-hash receipt, the prompt hash, unchanged references and all ten QA entries, and blocks on a dirty index, unexpected paths, missing LFS or divergence. Never bypass it with a direct `git add` or push.
- **Drift:** compare four-edge ink statistics with an actual look; a number never proves a vignette. When two sibling images share the same drift, stop and report it.
- **Independent review:** Claude Code reviews every delivered image. You never approve, and a numerical score is never approval.
- **Installed version:** `work_preflight.py --require-installed` confirms the clone carries this v7 skill before production.
