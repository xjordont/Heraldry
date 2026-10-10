# Heraldry Skirmish illustration runner: v4.0

A skill for ChatGPT Work that produces the book's pen-and-ink illustrations from the GitHub repo `xjordont/heraldry`. It does not plan scenes or write prompts. Claude Code prepares and audits those in the repo; this skill runs the queue, checks each image and hands the results back.

## Install and start

1. Upload `Heraldry_Classic_Ink_Art_Skill_v4_0.zip` as a skill (it replaces v3.1; the name is the same).
2. Paste a start prompt from `OPERATOR_CARD.md`.
3. After the five anchors are pushed, tell Claude Code to review them and publish the batch queue.

`python production/art/skill/heraldry-classic-ink-art/scripts/validate_skill.py --zip production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip` (run from the repo root) confirms the zip is intact and still agrees with the repo: reference images, families table, queue, prompt hashes.

## What changed from v3.1, and why

v3.1 is a careful, honest skill for making one illustration per conversation. v4 keeps its best ideas and changes what did not fit the plan of running the whole book from the repo. Each row below was checked against the repo.

| Area | v3.1 | Problem | v4 |
|---|---|---|---|
| Source of the brief | The model plans each scene from pasted flavour text. Nothing mentions the queue, prompts, receipts, `assets/art/incoming` or the repo. | The repo already holds 274 audited briefs and 275 prompts with a uniqueness check and the rulebook fixes in the must-lists (the Undead Champion's maul, the Orc's shield, the Basilisk now Large). Re-planning at run time bypasses all of it. | The prompt file is used verbatim. No planning step. |
| Sizes | Cover 4:3, chapter 16:9 at 5.8 in, ancestry and class 3:4, tradition 1:1, boss 4:3. | The layout slots are 3:2 (cover 4.8 in, chapter 4.5 in), 2:3 (ancestry, class), 3:2 (tradition, boss). The queue and intake use three sizes. The presets would have produced images the slots reject. | The size comes from the queue item. |
| Style reference | Greythorn for every family. | Its dense texture is the wrong target for figures that print 1.6–1.9 in wide; the owner's figure sample is bold contour on white. Greythorn and the owner's scene sample both contain oaks, standing stones and a palisade gate, which leak into unrelated images. | Three registers. Each item has at most three references chosen for its register. Reference bleed is a hard fail. |
| Reference count | (The old queue said: attach every reference, up to nine images, to every item.) | Scene images attached to a figure prompt invite scenery in the figure. | Per-item reference sets in `QUEUE.json`. |
| Acceptance | A weighted self-score, target 9.0 out of 10. | A score the model assigns itself is not a measurement. | Ten binary hard fails. `check` repeats the item's must-show and do-not-draw lists, and `save` will not write the receipt until you state what you counted for each must-show line and confirm the do-not-draw items are absent. A script of tripwires, calibrated on real and synthetic images, catches the gross failures. |
| Retries | Repair until acceptable. | Costs subscription usage; later edits often regress. | A budget from the queue (3; cover and chapters 5), counted by the helper (each distinct image checked is one attempt), stop at the first clean attempt, at most two correction sentences per retry. |
| Print preparation | 4× Lanczos masters, 300 ppi proofs, a zip per image. | The intake already inks at native size and never upscales. Enlarged or re-encoded files break "unmodified", and 275 enlarged PNGs would add gigabytes to the repo. | Removed. Save the tool's file untouched. |
| Replay registry | `approved_assets.json` and copy scripts. | Duplicates `SELECTIONS.json`. Its Greythorn JPEG is the same render as the repo's copy but different bytes. | Removed. The repo says what is done. |
| Ink wording | Allows faint grey; says avoid a yellow cast. | The intake converts to pure ink on transparent, so grey wash is lost. The owner's prompts say warm ivory-white and the approved Greythorn paper is (248, 245, 237). | Ink marks only on flat near-white paper; warm ivory is fine. |
| Process | One image, no gates. | No anchor gate, resume, commit protocol, receipts or failure handling. | `doctor`, `status`, the anchors stop, 5–10 image batches with receipts, and paths for refusal, quota and no git. |
| Size | 8,971 words in 25 markdown files. | The rules were spread across many files. | About 7,100 words in 8 markdown files: a fifth fewer words and two-thirds fewer files. `SKILL.md` is about 2,200 words against v3.1's 1,865. It is longer because it is the whole procedure, including the rules the dry runs showed were needed; the other files are reference. |

## Kept from v3.1

The honest statement of limits; the ink vocabulary (now in `references/STYLE.md` and the prompts); the idea of narrow, composition-preserving repairs, including reverting to the better earlier image; separate gates before and after generation (now `doctor` and `show` before, `check` and the checklist after); the category guidance, condensed into `references/FAMILIES.md`; and hash-checked package integrity (`manifest.json`, `validate_skill.py`).

## How it was tested

- `tests/test_art_skill.py` runs in `make test`. It covers the tripwire classification on synthetic defects (grey wash, frame, crop, tint, blur, blank, tiny), parity of the colour, mid-tone and border measures with `tools/art_ink.py`, receipts, attempt rounds and the budget, the `--accept-flags` rule, look-alike detection, the push cadence, the no-git fallback, a real git state machine with a remote (pending, saved, pushed, redo, refused), and a contract test that the helper's files and receipts are accepted by the real intake tool without warnings. It also fails if the zip is older than its sources or the repo's reference images.
- An independent agent followed the documents literally, with no other knowledge, in a sandbox clone with a local remote and git-lfs: a full anchors session with a retry, an exhausted budget and a refusal. It found 13 document problems and 8 command problems. After the fixes the same agent re-checked its 27 findings (17 resolved, 9 partly, 1 not) and found 9 problems the fixes had introduced, such as `--accept-flags` working at attempt 1 and a save resetting the attempt count. Those are fixed too. A fresh agent then ran two sessions against a 269-item batch queue. Its stand-in images were byte copies of an anchor, so most checks failed, which exercised duplicate detection and the fallback paths and left the statement paths to the unit tests. Among other things it found that a redo stayed listed after the new image was pushed, that each retry overwrote the previous preview, that there was no path for an unsatisfiable prompt, and that the reviewer's reason for a redo never reached the operator. All are fixed.
- Nothing has been run against the real image tool yet. The first anchors run is the real test.

## Limits

- The tripwires are calibrated on the approved Greythorn render, the three owner samples and 13 synthetic defects. They catch gross problems. They cannot tell a good drawing from a mediocre one; the checklist and Claude Code's review do.
- This package cannot confirm that the image tool honours attached references, or that it passes your prompt through unchanged.
- It cannot confirm that ChatGPT Work has git, git-lfs or Python. `doctor` checks, and `bundle` is the fallback.
- During the anchors phase the figure anchors have one reference (the owner's figure sample). The batch has up to three.
- `save` insists on one real-looking statement per must-show line and an avoid-clear attestation, and records them. It cannot check that they are true. Claude Code's review is the check, and a receipt that claims a count the image does not show is itself a finding.
- The helper cannot stop an operator from rewording a prompt the image tool refused, or from attaching other references. The rules forbid both.

## Layout

```
SKILL.md                 the operating procedure
OPERATOR_CARD.md         start prompts
references/              STYLE, QA_CHECKLIST, REPAIR, FAMILIES (generated), AD_HOC, images/
scripts/heraldry_art.py  doctor, status, next, show, check, save, refuse, sheet, bundle
scripts/validate_skill.py
manifest.json
```
