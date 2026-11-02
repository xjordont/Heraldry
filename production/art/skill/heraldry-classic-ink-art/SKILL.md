---
name: heraldry-classic-ink-art
description: Runs the Heraldry Skirmish illustration queue from the GitHub repo xjordont/heraldry. For each queued item it generates one black pen-and-ink illustration from the repo's prepared prompt and that item's own short reference set, checks it against the prompt's must-show and do-not-draw lists, saves it unmodified to assets/art/incoming/<ID>.<ext>, logs a receipt and delivers each image to main with a guarded push. Use when asked to generate, resume, redo or review Heraldry artwork. Never writes or edits prompts, the manuscript or tools.
---

# Heraldry Skirmish illustration runner (v8)

## The queue is the source of truth

`production/art/gpt/QUEUE.json` says what to draw, `production/art/gpt/prompts/<ID>.txt` is the exact prompt for each item, and `production/art/ILLUSTRATION_LIST.md` (the owner's "illustrations.md") is the human-readable catalogue of the same prompts. If the list and a prompt file ever differ, the prompt file wins. Never run from the list.

While running the queue you do not plan scenes or write prompts. The planning was done and audited for uniqueness before the queue was published. Improvising at run time is where drift, duplicates and contradictions of the rulebook come from.

**Precedence.** An item's own prompt, must list and do-not-draw list override every general note in this skill, including the family notes and the style page. The prompt's own wording wins over this skill's shorthand: its "warm ivory-white paper", for example, is the flat near-white paper the checks mean. If the repo's `production/art/gpt/INSTRUCTIONS.md` or the queue differs from this skill on a repo mechanic (paths, queue fields, receipt fields, commit message), follow the repo and say so in your report. The hard rules below never relax.

## Hard rules

1. Use each prompt file verbatim as the image prompt. Do not shorten, paraphrase, translate or "improve" it. The only permitted addition is up to two correction sentences on a redo (`references/REPAIR.md`), which you record in the receipt notes.
2. Attach only the images in that item's `references` (at most six). Attach nothing else. Never attach the whole reference folder.
3. Generate only IDs listed in `QUEUE.json`. An image is delivered once it is pushed. Never regenerate a delivered image unless `status` lists it as `redo` or the owner asks. A redo starts a fresh attempt budget, and `show` prints the rejection reason: base your correction sentence on it. If the reason conflicts with the prompt's must or do-not-draw lines, the prompt wins; say so in your report. Before the push you may regenerate freely, inside the item's attempt budget.
4. The item's `size` is the minimum and fixes the aspect: wide 3:2 (1536x1024), tall 2:3 (1024x1536) or square 1:1 (1024x1024). Target the maximum output resolution (owner 2026-10-12): choose the tool's largest size at that aspect and its highest quality, never the default, or ask for the maximum resolution when there is no setting. A larger native image at the same aspect passes; `check` warns below the queue's `target_pixels` (the largest pixel count the tool has delivered, 1.57 MP), and `save` records `native_px` in the receipt. Use the GPT Image 2.5 Sunburst model if the tool offers it (owner request), otherwise the default image model, and record the exact model name shown with `save --model`. No upscaling and no print preparation: the repo's intake does that.
5. Save the image exactly as the tool delivered it. No crop, resize, sharpen, retouch or format conversion.
6. While generating, change no file in the clone except `assets/art/incoming/<ID>.<ext>` and `production/art/gpt/RECEIPTS.jsonl`. Keep everything else you create (downloaded images, previews, contact sheets, bundles) in the scratch folder, outside the clone. `doctor` prints its location and the helper uses it by default (set `HERALDRY_SCRATCH` to another folder outside the clone if the system temp folder is not available). Do not edit the manuscript, queue, prompts, tools or this skill. No branches. No force-push.
7. Never call the images hand-drawn. Approval is a separate repo step once the intake has inked the delivered images: look at each, then `python tools/art_intake.py approve --ids ...` or `reject --ids ... --reason "..."` (`docs/ART_AUTOMATION.md`). You may approve your own images after the run if you have the repo tools.
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
| `work_preflight.py` | read-only Python, LFS, queue, references, and remote auth status; `--offline-package` verifies a Work input package without Git |
| `fidelity_gate.py` | create/verify byte-bound QA JSON (all ten criteria require visual evidence) |
| `delivery_guard.py` | `audit`, `ship --execute`: verify native hashes, receipts, reference and prompt hashes, clean index, and Git LFS before delivery |
| `style_audit.py` | advisory four-edge and same-register style drift report (scratch only); supplements the contact sheet |

## Session start

**Two input routes.** (a) An authenticated Git checkout, below. (b) An **offline Work input package**: a ZIP built with `tools/art_work_package.py` from a named commit, holding the exact queue, its prompt files, every queue-listed reference as real image bytes, this complete skill, receipts and selection state, each with SHA-256 in `WORK_PACKAGE.json`. Use (b) when shell git cannot authenticate or the GitHub connector cannot fetch the binary references. Unzip it into an empty folder, treat that folder as the clone, and follow its `START_HERE.md`: `work_preflight.py --repo . --offline-package --require-installed` must say READY with `delivery: bundle` and `remote_access: NOT_ATTEMPTED`. Never `git init`, clone or pull there. Everything else in this skill applies unchanged except delivery: `delivery_guard.py` needs Git and refuses, so every batch ends with `bundle` and an explicit statement that nothing was pushed. The package proves only its inputs; the first item is still your proof that the image tool accepts the references and gives you the native file.

Route (a), first time only: clone `xjordont/heraldry` (a private repo; use the access the owner gave you) with `GIT_LFS_SKIP_SMUDGE=1` set, then run `git lfs install --local --skip-smudge` inside it. That keeps the private reference PDFs, and every other large file you do not need, from being downloaded now or by later pulls.

Every session, from the repo root, first run `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed` (`references/WORK_OPERATIONS.md` covers the offline package route). A GitHub connector without local Git LFS is not a substitute for a successful push. Then:

```
# Only pull while the checkout is clean. If prior images/receipts are unsent,
# use status and the guarded delivery/bundle procedure instead of rebasing.
git pull --ff-only origin main
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

If `doctor` says NOT READY YET, run the single `git lfs pull --include="..."` command it prints (reference images that are still LFS pointers), then run `doctor` again. `doctor` must say READY, or READY TO GENERATE (see the no-git stop condition). `status` prints the single next action. Obey it.

## Phases

- `anchors` (only if a calibration set is published; the current queue is `batch`). Generate them, push, then stop. The batch starts once the anchors are approved (`tools/art_intake.py approve-anchors`, after looking at them) and the batch queue is published (`tools/art_gpt_pack.py`): do that yourself if you have the repo tools, otherwise tell the owner. Report any refused anchor.
- `batch`. Work through the queue in order and keep going between deliveries until `status` says NOTHING LEFT. The lead items, after any redo, cover one of each reference set. `next` puts redos first; it and `status` first fast-forward a clean clone, so a redo sent back mid-session shows at once. References are the owner's gritty ink samples and a few public-domain prints chosen for the same look; generated images are never references. Each item's `ref_set` names its set: look at a set's images once, the first time it appears in the session.

## For each item

1. `show ID`. Read the MUST BE SHOWN and DO NOT DRAW lists before generating.
2. Attach the listed references. Paste the whole prompt. Request the size. Generate in a fresh image request: no earlier image, attempt or item in the context (owner 2026-10-12: first generations are far better than retries). If the image tool cannot accept every required reference, STOP and report a capability blocker; do not silently proceed with an unanchored image. If the tool shows you a revised prompt or shortens yours, report the deviation and do not attest that the queued prompt was unchanged. If an image call shows no image, take the file the tool saved (newest in its generated-images folder); if none exists, call once more, and if that also returns nothing, `refuse` the item and continue.
3. Save the tool's image into the scratch folder, never inside the clone. Run `check ID FILE`. It counts the attempt (every distinct image you check is one; the count carries on through a redo before the push and starts afresh only after the image has been delivered and sent back), prints the tripwires, writes a print-size preview and lists the MUST and DO NOT DRAW lines again. Look at the image and at the preview and check each of the ten hard fails below (each is true or false). Count the must-show items yourself: the tripwires cannot. Some DO NOT DRAW lines name another entry ("Not the Undead Sentinel (shieldless, with a halberd)"): make sure your image does not show the traits in the brackets. You do not need to open the other entry.
4. Run `qa ID FILE` on the exact file you will save and complete the JSON draft it names (the attestations `references_attached`, `prompt_unchanged`, `visual_review_at_print_size` true; `register_compared`; ten `checks` with `pass` and 15+ characters of evidence; `unresolved_issues` empty when nothing failed), then run `save ID FILE --must "<what you counted or found>" --avoid-clear --model "<image model if shown>" --notes "<anything unusual, including any correction sentence you added>"`. Give exactly one `--must` for each MUST line, in order, each a real statement such as `"counted 8 legs, 4 a side"`; give none if the list is empty. `--avoid-clear` states that you looked and none of the DO NOT DRAW items is present. `save` checks again, copies the bytes untouched with the true extension, and appends the receipt with the saved attempt's number, how many images the helper counted, your statements and the attestation. Add `--redo` only when the owner asked you to replace an image that was already delivered; items that `status` lists as `redo` need no flag. `--attempts N` can only raise the count the helper recorded, for images you generated but did not check.
5. **One generation per item** (`max_attempts` is 1; owner 2026-10-12). Never generate a second image for the item in the same round, and never retry. If the image has a hard fail, still save it: mark those checks false in the `qa` draft, list the defects in `unresolved_issues`, and run `save ID FILE --accept-flags --notes "<what is wrong>"`. A rejection brings it back as a redo: a fresh round with its own single generation, the verbatim prompt plus at most two correction sentences based on the rejection reason (`references/REPAIR.md`). If the image is a byte copy of a reference or of another image, save nothing: `refuse ID --reason "the tool returned a copy of <path>"`. Then move on. If the image tool refuses the item itself (a safety or content refusal), save nothing: `refuse ID --reason "<what it said>"`, deliver, and continue with the next item; the prompt is then rewritten in the catalogue.

## Hard fails: reject the variant if any is true

1. Wrong subject, or anything contradicts SOURCE TEXT.
2. A "Must be shown exactly" item is missing or miscounted. Count limbs, eyes, heads and weapons.
3. A "Do not draw" item is present.
4. Any lettering, runes, signature, watermark, caption or pseudo-writing.
5. Colour, grey wash, gradients or paper texture. Ink marks only, on flat, even paper (the warm ivory-white the prompt asks for is fine).
6. A frame, box or hard crop. A figure or still life that is not isolated on white, or that is cropped or touches an image edge (a narrow but complete margin is fine: the layout trims it). A scene that does not fade to white on all four sides.
7. Subject bleed from a reference that the prompt did not ask for: anything on the bleed list in `references/STYLE.md` (a throne, a full moon, a crowd of skulls, period ruffs and breeches, a palisade gate with twin towers, a skeleton with a shield).
8. Broken anatomy or construction: wrong limb counts, unheld weapons, floating parts, impossible architecture, cloned elements.
9. A human scale figure the prompt did not ask for, or a requested one missing. Scale follows the prompt: a creature's `Size:` line, or the people a scene says it has.
10. The subject is not unmistakable in the print-size preview.

A must-show item and a do-not-draw line that look opposed are almost always about scale or focus. A required grove circle beside "do not repeat the grove scenario" means: draw the circle small, in the middle distance as the composition says, and do not make it the subject. Satisfy both the narrowest way and carry on. A prompt that cannot be satisfied at all is not for you to fix or to burn attempts on: `refuse ID --reason "prompt cannot be satisfied: <what clashes>"` and move on (`references/REPAIR.md`).

Details, soft style checks and the batch drift review: `references/QA_CHECKLIST.md`. Style and the registers: `references/STYLE.md`. Family defaults: `references/FAMILIES.md`.

## Delivery and drift review

The batch queue sets `push_every: 1` and `review_every: 10` (owner 2026-10-11): every image is delivered as soon as it is saved, so a usage limit never strands work, and every tenth image triggers a drift review. `status` says which.

1. **DELIVER** (after each save): run the guarded delivery below.
2. **DRIFT REVIEW** (every tenth save): first `sheet --recent 10 --refs` and `style_audit.py --repo . --recent 10` (both write to the scratch folder), and read `references/VISUAL_ACCEPTANCE.md`. Look for drift (thicker or thinner line, grey tone, a cleaner or softer finish than the references), repeated poses or compositions, and scenery behind figures. The statistics are advisory: a number never proves a vignette. Deliver in every case and keep going (owner 2026-10-12: run the whole list): name any drifting image, and any fault shared by two or more same-register images, in your report so it can be sent back as a redo. Nothing drifted: say so.

```
python production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .   # validates, then commits and pushes
```

`ship` verifies each image against its latest native-hash receipt, the prompt hash, unchanged references and all ten QA entries, fast-forwards over the intake bot's commits when they touch none of the delivered files, and retries a lost push once more. `audit` runs the same validation without pushing, for diagnosis. A ship with nothing unsent and the clone level with `origin/main` reports `UP-TO-DATE` (exit 0), so a repeat after a lost-output timeout is harmless. Never bypass it with a direct `git add` or push. If the guard blocks (divergence, an overlap, an unknown local change, missing Git LFS, authentication), do **not** force-push, rebase or assume delivery. Use `bundle`, report that no push occurred, and stop. The guard commits only queue IDs under `assets/art/incoming` and the JSONL receipts.

3. At the end of a session run `status --end`, do what it says, then write the report.
4. In ChatGPT Work, style drift is a risk in very long image threads: after about 20 items, start a fresh conversation with the same session prompt. Codex continues in one session; either way `next` resumes exactly where you stopped.

## Stop conditions

- The queue is empty (or, in an `anchors` phase, the anchors are done).
- The image tool refuses an item. Do not reword the prompt to get around it. Record it with `refuse ID --reason "<the tool's message, or what happened if it gave none>"` (its receipt line is delivered by the next ship), list it in your report, and continue with the next item.
- Usage limit (ChatGPT Plus resets every 5 hours), rate limit, or the tool stops returning images without refusing (two requests in a row with no image). Everything saved is already delivered; report the counts and the next ID, and stop. The owner restarts the same prompt after the reset, and `next` resumes. Nothing is recorded for an item you did not finish.
- `doctor` says NOT READY (not "NOT READY YET", which has its own one-step fix): a broken queue, prompts or references, or a branch other than main. Also a prompt that does not match its queue hash after a pull, or a queue that is schema 1. Report it and stop.
- `doctor` says delivery by git is blocked (no git or git-lfs): keep generating and saving, and finish each batch with `bundle`; hand the zip to the owner. If you cannot run Python either, do the same steps by hand and deliver the images, named `<ID>.<ext>` with their true extension, with one receipt line each (`references/QA_CHECKLIST.md` shows the format).

## Report at the end of every session

IDs saved and pushed, attempts used, items saved with `--accept-flags`, items refused, differences you found between the repo and this skill, the next ID. State plainly what you could not verify.

## Not in the queue

Do not generate it: a book illustration needs a catalogue entry first. For an explicit one-off outside the book, see `references/AD_HOC.md`.
