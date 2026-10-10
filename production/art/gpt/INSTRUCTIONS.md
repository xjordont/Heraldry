# ChatGPT Work: standing instructions for Heraldry illustrations

You generate the book's pen-and-ink illustrations with ChatGPT's image generation. Claude Code, in the same repository, prepares the prompts and checks your images; you only generate and commit images.

## Each session

1. Pull `main` with Git LFS so the reference images are real files, not pointers:
   - `git lfs install`
   - `git pull --rebase origin main`
   - `git lfs pull --include="assets/art/incoming/*.png,assets/art/style/*" --exclude=""`

   Then read `production/art/gpt/QUEUE.json`, or `QUEUE.md` for the same list as a table.
2. Work through the items in order. For each item:
   1. Open its prompt file, for example `production/art/gpt/prompts/ART-MON-GOBLIN.txt`, and use the whole text unchanged as the image prompt.
   2. Attach every image listed under `references` in the queue as a style reference.
   3. Generate at the item's `size` (1536x1024, 1024x1536 or 1024x1024) at the highest quality setting. If the tool cannot set exact pixels, ask for the aspect in words (wide 3:2, tall 2:3 or square). Keep the closest of those three sizes.
   4. Generate up to three variants. Keep the one that best meets the check below.
   5. Save it unmodified, with no crop, resize, sharpening or format conversion, as the item's `save_as` path, for example `assets/art/incoming/ART-MON-GOBLIN.png`.
      - If the tool delivers JPEG or WebP rather than PNG, keep the true extension (`.jpg` or `.webp`) with the same ID. The intake accepts all three.
      - PNG files are stored with Git LFS, so commit them from a git client with git-lfs installed. `git lfs ls-files` must list each new PNG.
   6. Append one line to `production/art/gpt/RECEIPTS.jsonl`: `{"id": "...", "prompt_sha256": "<from the queue>", "surface": "ChatGPT Work", "model": "<image model name if shown>", "date_utc": "YYYY-MM-DD", "variants_tried": N, "notes": "<anything unusual>"}`
3. Commit and push to `main` after every 5–10 images, with the message `art(gpt): <first id> .. <last id>`.
   - Before each push, run `git pull --rebase origin main`. The intake workflow commits to `main` after every push of yours. If a push is rejected, pull with rebase again and retry.
   - Never force-push and never create branches.

## Check each variant before keeping it

- The image is pure black ink on white or ivory paper. It has no colour, no grey wash, and no lettering, signature, watermark, border or frame.
- The subject matches the prompt's SOURCE TEXT and SUBJECT DETAILS, with the right number of limbs, eyes and heads, and the weapons it names.
- Scenes fade into white paper at all four edges. Figures stand isolated on white with nothing cropped by the image edge.
- Anatomy, hands, weapon grips and architecture are coherent.
- The line, hatching and finish match the reference images, so the book looks drawn by one hand.

If no variant passes, save the best one and say so in `notes`.

## Rules

- Change no file except `assets/art/incoming/<ID>.png` (or `.jpg`/`.webp`) and `production/art/gpt/RECEIPTS.jsonl`.
- Never edit the manuscript, prompts, queue or tools.
- Never describe these images as hand-drawn.
- The anchors phase comes first. After you push the anchors, stop and wait: Claude Code reviews them and publishes the batch queue with the approved anchors as references.
- When you push images, a GitHub workflow converts them to print ink and posts a review sheet automatically.
