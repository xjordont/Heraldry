# Work operations and handoff

## Capabilities

The repository holds the prompts, queue, references and selection state; the worker generates, checks, records receipts and delivers. The GitHub plugin alone does not provide a local shell, file bytes or Git LFS: confirm each capability rather than assuming it.

## Capability check

1. Use an authenticated checkout with Git, Git LFS and Python, or, without Git authentication, the offline input package (next section).
2. Run `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed` (add `--offline-package` for the package). If LFS or authentication is unavailable, delivery is by `bundle`, never a claimed push.
3. The image tool must actually accept the item's listed reference images and give you the native file. The preflight cannot see the image tool: if the references cannot be attached on the first item, stop and report. No separate smoke-test record is needed.
4. Per item: `check`, `qa` (complete the draft), `save`. Then deliver with `delivery_guard.py ship --execute --repo .`, which validates before it commits; if it blocks, `bundle` and say no push occurred.

## Offline input package route (no authenticated Git)

When shell git cannot authenticate, or the GitHub connector cannot fetch binary references, use a Work input ZIP built by `tools/art_work_package.py build` from a named commit. It holds only: the queue and its prompt files, every queue-listed reference as real image bytes, this complete skill (source folder and installable ZIP), `RECEIPTS.jsonl`, `SELECTIONS.json`, `config/art_style.json`, `START_HERE.md` and `WORK_PACKAGE.json` (source commit, every path with SHA-256 and size, prompt hashes, decoded reference formats and sizes). No other art and no private reference PDFs.

1. Unzip into an empty folder; run every command from it. No `git init`, clone or pull.
2. `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --offline-package --require-installed`. READY requires every packaged file to match its hash (receipts may only grow), every prompt to match `QUEUE.json`, and every queue reference to decode as an image. It never runs git, reports `remote_access: NOT_ATTEMPTED` and `delivery: bundle`.
3. The capability check above still applies: the package cannot prove the image tool's reference attachment or native-file access.
4. `check`, `qa`, `save` exactly as in a checkout. `save` keeps a copy of each QA report in the scratch folder.
5. When `status` asks (every tenth image without Git): `sheet --recent 10 --refs`, `style_audit.py --recent 10`, then `heraldry_art.py bundle --evidence SHEET --evidence STYLE_JSON`. Before writing, `bundle` applies the same receipt gate as `delivery_guard.py` (native SHA, prompt SHA, reference SHAs, ten QA criteria) and requires each saved QA report unchanged. The ZIP holds the native images, `receipts_append.jsonl`, `review_evidence/qa/<ID>.qa.json`, the extra evidence and `BUNDLE_MANIFEST.json` (`pushed_to_github: false`, not approved). `delivery_guard.py` refuses in a package folder: there is nothing to push with.
6. Hand the bundle over as a downloadable file, say that nothing was pushed, and continue with the next items. The `Import Work review bundle` workflow checks it with `tools/art_work_package.py verify-bundle` before the intake.

Authenticated Git/LFS delivery stays a separate capability: report it only after a real `delivery_guard.py ship --execute` succeeds from a real checkout.

## QA record protocol

`qa ID FILE` writes the draft for the exact file you will save, with the image, prompt and reference hashes filled in. After reviewing the native image and its print-size preview, set `prompt_unchanged`, `references_attached` and `visual_review_at_print_size` to true, `register_compared`, and each `checks.<criterion>` to pass true or false with at least 15 characters of specific visible evidence. Do not mark failures passed. `save` finds the draft and refuses a missing, changed, incomplete or contradictory one; an exhausted budget uses `--accept-flags` with the failures recorded. The receipt embeds the ten checks. Keep the draft in the scratch folder, never in the repository.

## Delivery safety

Current live repository contract is direct-to-main, not branch/PR. The guard uses exact allowed paths, queue ID validation, SHA-bound receipts and LFS filter checks. It fast-forwards over intake commits that touch none of the delivered files, recovers an unpushed delivery commit, and never rebases, merges or force-pushes; divergence or an overlap stops it. Do not switch to branches or PRs. If several workers run at once, partition the queue by ID.

## After delivery

The intake workflow inks every delivered image; approval follows with `tools/art_intake.py` (`SKILL.md`, hard rule 7). A rejected image comes back as a `redo` (listed first by `next`) with its reason.

## Stopping conditions

Stop on source/hash mismatch, unfetched LFS pointer, missing image-tool references, exhausted budget, unhandled image-tool refusal, unexpected repository changes, authentication failure, or QA failure that cannot be fixed within the allowed budget. The fallback is always an explicitly labelled ZIP containing original bytes and receipts, not a falsely claimed Git push.
