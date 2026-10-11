# Heraldry Skirmish Classic Ink Art Skill v6.0 - Release verification

## Outcome

**Offline release candidate validated.** This result is deliberately distinct from a production-tested Work deployment or any claim of guaranteed high-quality generative art.

## Audit input and scope

- Baseline: `Heraldry_Classic_Ink_Art_Skill_v5_0.zip`.
- Audit: v5 runner, image QA, work preflight, delivery guard, ZIP validator, manifest, documentation, original reference assets and the existing test suite.
- Upstream contract retained: GitHub Heraldry queue schema 2, exact queued prompts, no added lore, at most three item-specific references, unchanged native artwork, limited retries, producer versus independent reviewer roles.
- The 275-item illustration catalogue's individual prompts are **not** packaged.

## Improvements validated offline

1. Native-image SHA checks at the delivery boundary: altered art after QA cannot be pushed through the guard using an old receipt.
2. Current prompt SHA and ordered reference SHA checks: stale or changed inputs block image delivery.
3. Ten individual QA decisions, complete evidence, print-size attestation and comparison register required.
4. Clean Git staging index required; direct-to-main flow refuses divergence and never uses force push or automatic rebase.
5. Four-edge diagnostic measurements and same-register batch reports highlight possible vignette and tonal drift. These are *advisory*, never proxies for a human/visual decision.
6. Install-version check via preflight prevents confusing an old live repository helper with v6.
7. ZIP is root-installable, manifest-hashed, safely extracted, and contains identical owner reference artwork.

## Tests

- Clean extracted archive: `python -m unittest discover -s tests -v` - **25 tests passed**.
- Clean extracted archive: `python scripts/validate_skill.py` - **PASS**.
- Packed ZIP: validator - **PASS**; CRC check no corruption; no duplicate members; all 28 entries present before adding this report.
- Source reference images: all 4 original JPEG SHA-256 values exactly match v5.
- Python script syntax checked by package validator.

## Known unverified external integration

The following tests require an actual configured **ChatGPT Work** cloud computer and authenticated repository access, and are not represented by the offline tests:

- Reference-attachment success in the live image-generation UI/model.
- Exact native file download and access to the Work local Python runtime.
- Authenticated `git lfs` staging, upload, push and remote blob retrieval.
- Actual GitHub review-intake automation and independent Claude Code/owner approval.
- Empirical aesthetic and style consistency across Bastions, climates, portraits, monsters, and spot art.
- Robustness over many sessions, quota boundaries and concurrent reviewer edits.

## Deployment acceptance plan

1. Repository maintainer installs all v6 source, references, helpers, tests, and standing instructions as a coordinated change, keeping prompts/queue untouched.
2. Pass repo-native CI and the full art skill test suite; validate rebuilt installable ZIP against deployed source.
3. Work performs `work_preflight.py --repo . --require-installed` and the *real* image/reference/native-file smoke test.
4. Generate ONE existing calibration anchor; verify prompt/reference SHA, QA evidence, exact asset bytes, and print-size appearance.
5. Deliver via guarded Git LFS push; confirm remote hash and an independent reviewer intake result.
6. Complete the other four anchors; obtain independent approval before unlocking the batch queue.

**Release status: Offline-validated candidate, not yet production-proven.**
