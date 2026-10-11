# Installation into the existing Heraldry repository (manual / Claude Code step)

This ZIP is an updated skill, **not** an automatic change to GitHub. The live repository currently references v4; simply attaching v6 to ChatGPT Work will not replace its helper or standing instructions.

Stage these changes in a controlled repository upgrade performed by the repository maintainer:

1. Replace `production/art/skill/heraldry-classic-ink-art/SKILL.md`, the included references, and `scripts/heraldry_art.py` and `scripts/validate_skill.py` with v6 files.
2. Copy the new scripts `fidelity_gate.py`, `work_preflight.py`, and `delivery_guard.py`, and corresponding reference documents.
3. Rebuild the repository's installable ZIP and manifest with `tools/art_skill_build.py` (or the same deterministically hash-checked build process currently in the repo).
4. Update `production/art/gpt/INSTRUCTIONS.md` to v6's QA-file and delivery-guard contract; use `deployment/INSTRUCTIONS_V6_REPLACEMENT.md` as the proposed replacement, reconcile with any newer repo-side requirements.
5. Add v6 QA/delivery unit tests into the actual repo suite; run `python -m unittest discover -s tests -v` and the repo's CI checks.
6. Commit skill upgrade separately from illustration batches so the production image agent never edits protected prompts, manuscript or helper tools.
7. Confirm clone, Git LFS, image tool references, QA, ship, and intake on ONE anchor before starting batches.

Unchanged repo contracts: `QUEUE.json` schema 2, prompt hashes, source precedence, `assets/art/incoming/<ID>.<ext>`, receipts JSONL, and the separation of generator from reviewer. This package does NOT contain or import the individual catalogue prompts.

Note: the v6 release validator intentionally checks package integrity and assets without requiring the live repo to already be upgraded. Repo synchronization must be validated separately during deployment.

## V6 additional installation requirements

- Copy `scripts/style_audit.py` and `references/VISUAL_ACCEPTANCE_V6.md` as well as v6 QA and delivery scripts.
- Install the v6 regression tests (including `tests/test_v6.py`) and update the repository packaging procedure so the installable ZIP retains all v6 files; do not rely on an older v4 builder configuration that omits them.
- Replace repository standing instructions with the v6 candidate only after reconciling the current repo version and approved review contract.
- Run `work_preflight.py --repo . --require-installed` from the Work checkout. The preflight deliberately fails if a v6 `SKILL.md` is not present.
- Validate the exact versioned ZIP after building. Keep a known-good v4 checkout for rollback until the pilot passes; do not silently change the queue, prompts, image selection, or owner approvals.
- Test one image (prompt + references + native file + QA + audit + LFS push + independent reviewer intake) before the remaining anchors.
