# V6 Work operations and handoff

## Responsibility boundary

Repository/Claude Code owns canonical prose, prompt writing, uniqueness audit, queue, references, selection decisions, print intake and review. ChatGPT Work owns native image generation, checks, receipts, delivery. The actual GitHub plugin alone does not provide local shell, file bytes, Git LFS, or a long-running Claude Code process. Confirm each capability rather than assuming.

## Smoke-test gate

1. Obtain a clean authenticated checkout of the Heraldry repository; only checkout in an environment where Git, Git LFS and Python are available.
2. Run `python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed` and the existing helper's `doctor` and `status`. If LFS/auth are not available, select the `bundle` fallback instead of claiming a push.
3. Pick a single queued item, open its prompt and load only its queue-listed references. Generate the image through the available image tool.
4. Verify that the exact image bytes are accessible on the local filesystem, and that the listed visual references were actually attached. This is a manual tool-capability check; the preflight cannot inspect the image-tool UI.
5. Only if all three conditions hold may the operator write a scratch JSON smoke record with `image_generated`, `all_queue_references_attached`, and `native_file_accessible` set to true. Rerun `work_preflight.py --smoke-file /scratch/smoke.json`.
6. Run `check`, write a visual-QA JSON outside the clone, and `save` with `--qa-file`.
7. Run `delivery_guard.py audit --repo .` then `delivery_guard.py ship --execute --repo .` if it passes. If anything blocks, use the helper's `bundle` and hand that ZIP to the reviewer with a clear note that no Git push occurred.
8. Confirm the exact commit and its LFS content were received by GitHub and the intake; don't equate local `git commit` with delivery.

## QA record protocol

Create a draft file via `fidelity_gate.py create ID /scratch/IMG.png --prompt-sha <queue hash> --reference /path/to/ref1 ... --out /scratch/ID.qa.json`. The script fills nonsemantic style diagnostics. After personally reviewing both native image and print-size preview, write `prompt_unchanged: true`, `references_attached: true`, and each `checks.<criterion>.pass` true or false with at least 15 characters of specific visible evidence. Do not mark failures passed. `save` refuses a missing, changed, incomplete or contradictory QA record; exhausted budgets can use `--accept-flags` and documented failures. The helper embeds the ten QA checks and their evidence in the receipt. Keep the full file as a scratch artifact (do not modify the repository other than incoming art and receipts).

## Delivery safety

Current live repository contract is direct-to-main, not branch/PR. The v6 guard uses exact allowed paths, queue ID validation, SHA-bound receipts, LFS filter checks and main-head equality. It never performs automatic rebase, force push or overwrite on conflict; if the intake advanced main in the meantime it stops. This is intentionally narrower than a branch/PR redesign and preserves intake compatibility.

For a later branch/PR workflow, Claude Code would need to update its intake workflow, protected branch policy and review procedure first. Do not unilaterally switch to PRs in Work. A single producer should hold the writing lease; if multiple workers operate, partition the queue by unique ID and commit separately with coordination.

## Independent reviewer handshake

Delivery is not approval. After each batch: publish receipt hashes and Git commit ID (or fallback ZIP path), notify Claude Code/owner to run the actual repository intake and review, and stop at the anchors gate. On rejection, wait for updated `SELECTIONS.json` / queue status, then redo using the specified reason. No autonomous cross-agent trigger is assumed without configured automation.

## Stopping conditions

Stop on source/hash mismatch, unfetched LFS pointer, missing image-tool references, exhausted budget, unhandled image-tool refusal, unexpected repository changes, authentication failure, or QA failure that cannot be fixed within the allowed budget. The fallback is always an explicitly labelled ZIP containing original bytes and receipts, not a falsely claimed Git push.
