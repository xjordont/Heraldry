# Heraldry Skirmish: Classic Ink Art Skill v7.0

**A source-faithful, queue-driven image-generation skill. The Heraldry GitHub repository is the source of truth; Claude Code and the owner approve the artwork independently.**

The skill runs on Codex on the owner's PC (the current route), or in ChatGPT Work with the offline input package as the fallback. It does not claim to guarantee identical generated images or a successful run of an untested image tool. Unit tests and image diagnostics never measure artistic quality.

## Changes since v6

| Area | v7 |
|---|---|
| Art direction | Gritty old-school black-and-white ink (owner, 2026-10-11): bold rough contours, heavy solid blacks, scratchy hatching and dry-brush, high contrast. Still pure black ink: no grey wash, no stipple fields, no clean vector-like line |
| References | Owner samples plus four public-domain prints (Callot, Piranesi, Haden) chosen for the same look. Sets are chosen per family and per monster kind (undead, beast, vermin, humanoid, magical), at most three per item. Each queue item names its `ref_set` |
| Queue order | The first ten items cover one of each reference set, so the first drift review tests every set |
| Cadence | Each image is delivered as soon as it is saved (`push_every: 1`), with a drift review every tenth image (`review_every: 10`, `sheet --recent`, `style_audit --recent`) |
| Delivery | `delivery_guard ship` fast-forwards safely over the intake bot's commits and retries a lost push; divergence or overlap still stops |
| Docs | Reference documents have version-free names (`STYLE_CONSISTENCY.md`, `VISUAL_ACCEPTANCE.md`, `WORK_OPERATIONS.md`). The v6 deployment folder is retired because v6 and v7 are installed in the repository |

The v6 integrity guarantees carry over unchanged:
- byte-bound QA records, with ten criteria that each need visual evidence;
- native-hash receipts;
- prompt and reference hash checks at delivery;
- a clean index and no force-push.

## Production boundary

- **Claude Code and the repository** own the prompts, queue, references, approval decisions, the print intake and publication.
- **The art worker** (Codex, or ChatGPT Work as the fallback):
  - follows each item's exact prompt and attaches only the listed references;
  - generates, checks the native file and print-size preview, and records evidence;
  - delivers through the guard.
- **GitHub** stores the queue, receipts and the delivered image bytes through Git LFS.

## Run

```sh
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

On Codex, `production/art/codex/BATCH_CARD.md` is the whole working contract on one page. The image tool must actually accept the listed reference images: the scripts cannot prove that.

## Offline input package

Where the worker cannot authenticate git, Claude Code builds a self-contained input ZIP with `tools/art_work_package.py build`. It holds the queue, prompts, reference bytes, this skill, receipts, selections, a hash manifest and the source commit.
- `work_preflight.py --offline-package` verifies it without Git.
- Delivery is by `bundle` only.
- `tools/art_work_package.py verify-bundle` checks the returned ZIP.

## Offline verification

```sh
python -m unittest discover -s tests -v
python scripts/validate_skill.py --zip /path/to/Heraldry_Classic_Ink_Art_Skill_v7_0.zip --repo /path/to/repo
```

## Included files

- `SKILL.md`, `OPERATOR_CARD.md`: the full procedure and a short starting card.
- `references/`:
  - `STYLE.md`, `STYLE_CONSISTENCY.md`, `VISUAL_ACCEPTANCE.md`: art direction.
  - `QA_CHECKLIST.md`: checks.
  - `REPAIR.md`: retry corrections.
  - `FAMILIES.md`: family defaults.
  - `WORK_OPERATIONS.md`: operations.
  - `AD_HOC.md`: one-off requests.
- `references/images/`: byte-identical copies of every reference image any queue item can attach, plus the approved Greythorn render, with a SHA inventory. The queue's own reference paths are authoritative.
- `scripts/`: `heraldry_art.py`, `fidelity_gate.py`, `style_audit.py`, `work_preflight.py`, `delivery_guard.py`, `validate_skill.py`, `build_release.py`.
- `tests/`: offline regression tests. The `test_v5_regression.py` and `test_v6.py` file names are historical.

The skill package does not contain the 270 queued prompts; they live in the repository queue.
