# Heraldry Skirmish: Classic Fantasy Ink Art Skill v6.0

**A source-faithful, reviewable, queue-driven image-generation skill for ChatGPT Work, with the Heraldry GitHub repository as its source of truth and independent Claude Code/owner artwork approval.**

V6 strengthens v5's engineering quality and artistic-continuity audit. It **does not** claim to guarantee pixel-identical generated artwork, superior images from untested models, unattended orchestration of a separate Claude Code process, or Git LFS support merely because @GitHub is connected.

## Changes since v5

| System | V6 enhancement |
|---|---|
| Delivery provenance | `delivery_guard.py` verifies each *changed* incoming image's exact SHA-256 against its latest receipt, the queued prompt SHA, all reference SHA values, the native dimensions, and all ten visual QA decisions before staging |
| Concurrent writes | Enforces an initially clean Git index, checks `main` against the remote twice, and never rebases, force-pushes or silently overwrites other work; uses a bundle handoff if blocked |
| Style observability | `fidelity_gate.py` reports separate top/bottom/left/right outer ink fractions plus a central-to-edge ratio; checks remain advisory, not an artificial artistic score |
| Family drift | `style_audit.py` compares *same-register* saved images, detects exact cross-image copies and suspicious tonal and edge outliers; must accompany visual contact sheet inspection |
| QA evidence | A visual record must explicitly attest inspection at actual print width, identify the comparison register, bind every reference and the native bytes, and provide concrete evidence for each criterion |
| Deployment | `work_preflight.py --require-installed` blocks claiming the old repository skill as a v6 runtime; external image/reference and local-file smoke tests remain mandatory |
| Regression | Expanded offline unit suite tests altered images, altered reference assets, stale receipts, missing QA evidence, dimension exceptions, refusal records, incomplete style context, and fallback conditions |
| Package | Versioned manifest with SHA-256 of all files, safe ZIP checks and byte-verification of four unchanged approved style references |

## Production boundary

- **Claude Code and the repository**: own canonical prompts, queue, references, approval decisions, the final print intake and publication.
- **ChatGPT Work**: follows the exact item prompt, attaches only listed references, generates an image, checks the native file and print-size preview, records evidence, and delivers in guarded batches.
- **GitHub**: stores the queue, receipts and submitted image bytes via Git LFS when the *local Work environment* actually supports it. Otherwise a labelled handoff ZIP is required.

## Install

This ZIP is a **candidate release, not an installed repository upgrade**. Follow `deployment/REPOSITORY_UPGRADE.md` and reconcile `deployment/INSTRUCTIONS_V6_REPLACEMENT.md` with the repository's latest `production/art/gpt/INSTRUCTIONS.md` before allowing an autonomous Work run. Upgrade the repository helper, additional scripts, skill documents, tests and installable ZIP together. Do not mix a v6 `SKILL.md` with a v4/v5 repo helper.

The runtime must pass:

```sh
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

Complete a **real image-tool smoke test** with references and a native file on disk before accepting any image. The script alone cannot prove this.

## Before each batch delivery

1. Inspect image references, native assets and print-size previews and complete QA for every item.
2. Run `heraldry_art.py sheet --refs` and `style_audit.py` (report outside the repository).
3. Run `delivery_guard.py audit --repo .`; then `ship --execute` only if it passes.
4. If Git LFS or remote push fails, make a helper `bundle` and **do not claim delivery succeeded**.
5. **Stop after the five calibration anchors**, pending independent review and a new queue.

## Offline verification

```sh
python -m unittest discover -s tests -v
python scripts/validate_skill.py --zip /path/to/Heraldry_Classic_Ink_Art_Skill_v6_0.zip
```

Unit tests and image diagnostics do not measure artistic excellence. Real Work generation, native-file transfer, Git LFS upload, reviewer intake, and consistent style across multiple unillustrated subject families require a separate pilot.

## Included files

- `SKILL.md`, `OPERATOR_CARD.md`: full procedure and concise starting instructions.
- `references/STYLE.md`, `STYLE_CONSISTENCY_V6.md`, `VISUAL_ACCEPTANCE_V6.md`, `FAMILIES.md`, `QA_CHECKLIST.md`, `REPAIR.md`: art direction, QA, family framing and revision rules.
- `references/images/`: byte-preserved approved Greythorn and three owner-approved reference JPEGs, with a SHA inventory.
- `scripts/heraldry_art.py`, `fidelity_gate.py`, `style_audit.py`, `work_preflight.py`, `delivery_guard.py`, `validate_skill.py`, `build_release.py`.
- `tests/test_v5_regression.py`, `tests/test_v6.py`: offline regression tests.
- `deployment/`: maintainer-only repository upgrade plan and proposed v6 standing instructions.

The skill package does **not** incorporate the 275 individual prompts from the illustration catalogue.
