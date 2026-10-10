# ChatGPT Work: standing instructions for Heraldry illustrations

You generate the book's pen-and-ink illustrations with ChatGPT's image generation. Claude Code, in the same repository, writes the prompts, queue, references and reviews. You generate and deliver. You never plan scenes, edit prompts or approve images.

The method is the skill `heraldry-classic-ink-art`, v4. Its source is in this repo at `production/art/skill/heraldry-classic-ink-art/` and the installable zip is `production/art/skill/Heraldry_Classic_Ink_Art_Skill_v4_0.zip`. If the skill is installed, follow it. If it is not, follow `production/art/skill/heraldry-classic-ink-art/SKILL.md` directly and run its helper from the clone:

```
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

This file is the repo-side contract and the skill is the procedure. They say the same thing.

## Contract

- The work list is `production/art/gpt/QUEUE.json` (schema 2; `QUEUE.md` shows it as a table). Each item has `id`, `size`, `references`, `max_attempts`, `must`, `avoid`, `prompt` and `prompt_sha256`.
- Use each prompt file unchanged as the image prompt. On a retry you may add one correction sentence (see the skill's `references/REPAIR.md`) and must record it in the receipt notes.
- Attach only the item's own `references` (at most three images). Do not attach the whole list.
- Generate at the item's `size`, 1536x1024, 1024x1536 or 1024x1024, at the highest quality available. Stop at the first attempt that passes the skill's checks, and never exceed `max_attempts`.
- Save the image unmodified, with no crop, resize, sharpening or format conversion, as `assets/art/incoming/<ID>.png`. If the tool delivers JPEG or WebP, keep the true extension (`.jpg` or `.webp`). The intake accepts all three, and there is one file per ID.
- Append one line per image to `production/art/gpt/RECEIPTS.jsonl`: `{"id": "...", "prompt_sha256": "<from the queue>", "surface": "ChatGPT Work", "model": "<image model if shown>", "date_utc": "YYYY-MM-DD", "variants_tried": N, "notes": "<anything unusual>"}`. The helper's `save` command writes it. A refusal by the image tool is recorded with the helper's `refuse` command.
- Change no other file. Never edit the manuscript, prompts, queue, tools or skill. No branches. No force-push.
- Commit and push to `main` after every 5–10 images with the message `art(gpt): <first id> .. <last id>`. Run `git pull --rebase origin main` before each push, because the intake workflow commits to `main` after every push of yours. If a push is rejected, pull with rebase again and retry.
- PNGs are stored with Git LFS: after `git add` and before `git commit`, `git lfs ls-files` must list each new PNG. Clone with `GIT_LFS_SKIP_SMUDGE=1`, run `git lfs install --local --skip-smudge`, and fetch only the reference images that `doctor` names. Do not download the private reference PDFs or every delivered PNG.
- If the image tool cannot take the listed references, or takes fewer, say so in the receipt notes (`references attached: N of M`) and in your report. If it shows a revised prompt, note that too.
- The anchors phase comes first. After you push the anchors, stop and wait: Claude Code reviews them and publishes the batch queue with the approved anchors in the reference sets.
- Never describe these images as hand-drawn, and never mark one approved.

## What happens next

A GitHub workflow converts each pushed image to print ink and posts a review sheet. Claude Code reviews it and approves or rejects each image. A rejected item returns to the queue and shows as `redo` in `status`.
