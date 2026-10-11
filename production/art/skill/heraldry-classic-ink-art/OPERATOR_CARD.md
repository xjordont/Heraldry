# Heraldry Skirmish art runner v6: operator card

## Before generation

Work with the `xjordont/Heraldry` repository, `main`, following `SKILL.md`. Claude Code owns prompts, queue, references and approvals. Work generates, checks and delivers unchanged native image files; never modify prompts, manuscript or queue.

Run in the authenticated checkout:

```
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

If Git LFS/authentication is unavailable, use the bundle fallback. Confirm through a real smoke test that the image tool accepts the queue's references and that the native image file is accessible. Do not claim this was verified from repository access alone.

## Per item

1. `show ID`; paste the exact prompt and attach **only** the listed references (all of them).
2. Generate the requested native pixel dimensions at the highest quality offered; keep original bytes in scratch.
3. Run `check ID SCRATCH_IMAGE`; inspect original and print-size preview beside its references. Set `visual_review_at_print_size: true` and `register_compared` in the QA file **only after** this review.
4. Create the image-bound QA report with `fidelity_gate.py create ... --out /scratch/ID.qa.json`, complete ten criteria with visible evidence, and run `save ID FILE --qa-file /scratch/ID.qa.json` plus the existing `--must` and `--avoid-clear` assertions. Never invent a pass.
5. Retry narrowly within the queue budget; at exhaustion, use a flagged handoff with recorded failures, not a false approval.

## Batch and stopping rules

- Review each batch with `sheet --refs` and `style_audit.py --repo . --limit 10 --out /scratch/batch_style.json`. Stop if two or more same-register siblings exhibit a common style drift.
- After 5 images, or at session end, run `delivery_guard.py audit --repo .`; then `delivery_guard.py ship --execute --repo .` only when safe. Otherwise `bundle` and state delivery is pending.
- **Anchors phase: generate exactly 5, deliver, STOP.** Wait for independent Claude Code review and republished queue.
- Resume from `status`; never regenerate an approved/delivered item unless it is an explicit `redo`.
- An @GitHub connection does not automatically launch Claude Code, supply Git LFS, or approve artwork.

## Copy-and-use Work prompt

> Use the Heraldry Skirmish Classic Ink Art v6 skill on xjordont/Heraldry, main. Perform the Work environment and image-reference smoke tests, run the queue doctor and status, then generate the queued illustrations in order using the exact repository prompts and item-specific references. For each native image, run mechanical checks, inspect the image and print-size proof, and complete the ten-criterion, byte-bound style-fidelity QA report with explicit print-size review. Audit cross-image drift and verify current image/reference hashes before delivery. Retry only within each item's budget; do not self-approve. Review batch-level artistic drift and deliver every 5 images through the guarded Git LFS process, or provide a clearly labelled fallback bundle. Stop after the five anchors, or at any hard blocker; report completed IDs, failures, receipt hashes, commit or bundle, and the next action. Never edit the queue, prompts, manuscript or code during generation.
