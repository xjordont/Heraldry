# Work operations and handoff

## Capabilities

The repository holds the prompts, queue, references, and selection state; the worker generates, checks, records receipts, and delivers by Git push. The GitHub plugin alone does not provide a local shell, file bytes or Git LFS: confirm each capability rather than assuming it.

## Capability check

1. Use an authenticated checkout of `main` with Git, Git LFS, and Python. Git push is the only delivery: without it, nothing you generate can be delivered, so stop and report to the owner.
2. Run `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed`. It must say READY with `delivery: git_lfs`; BLOCKED means stop and report.
3. The image tool must actually accept the item's listed reference images and give you the native file. The preflight cannot see the image tool: if the references cannot be attached on the first item, stop and report. No separate smoke-test record is needed.
4. Per item: `check`, `qa` (complete the draft), `save`. Then deliver with `delivery_guard.py ship --execute --repo .`, which validates before it commits. If it blocks, stop and report that no push occurred; the saved images and receipts stay in the clone for a later `ship`.

Report authenticated Git LFS delivery only after a real `delivery_guard.py ship --execute` succeeds.

## QA record protocol

`qa ID FILE` writes the draft for the exact file you will save, with the image, prompt and reference hashes filled in. After reviewing the native image and its print-size preview, set `prompt_unchanged`, `references_attached` and `visual_review_at_print_size` to true, `register_compared`, and each `checks.<criterion>` to pass true or false with at least 15 characters of specific visible evidence. Do not mark failures passed. `save` finds the draft and refuses a missing, changed, incomplete or contradictory one; an exhausted budget uses `--accept-flags` with the failures recorded. The receipt embeds the ten checks. Keep the draft in the scratch folder, never in the repository.

## Delivery safety

Current live repository contract is direct-to-main, not branch/PR. The guard uses exact allowed paths, queue ID validation, SHA-bound receipts and LFS filter checks. It fast-forwards over intake commits that touch none of the delivered files, recovers an unpushed delivery commit, and never rebases, merges or force-pushes; divergence or an overlap stops it. Do not switch to branches or PRs. If several workers run at once, partition the queue by ID.

## After delivery

The intake workflow inks every delivered image; approval follows with `tools/art_intake.py` (`SKILL.md`, hard rule 7). A rejected image comes back as a `redo` (listed first by `next`) with its reason.

## Stopping conditions

Stop on a source or hash mismatch, an unfetched LFS pointer, missing image-tool references, unexpected repository changes, an authentication or push failure, or a blocked `ship`. Keep the saved images and receipts, report the blocker, and never claim a push that did not happen.
