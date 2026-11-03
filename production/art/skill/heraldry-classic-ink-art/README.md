# Heraldry Skirmish: Classic Ink Art Skill v8.0

**A source-faithful, queue-driven image-generation skill. The Heraldry GitHub repository is the source of truth.**

The skill runs on Codex on the owner's PC (the current route), or in any client with an authenticated Git checkout, Git LFS, and Python. Git push through `delivery_guard.py ship` is its only delivery.

## Changes since v7

| Area | v8 |
|---|---|
| Generation | **One generation per item** (`max_attempts` 1; owner 2026-10-12: first generations beat retries), in a fresh context. A defect is saved with `--accept-flags --notes`; a rejection brings it back as a redo, which is again a single generation with at most two correction sentences (`references/REPAIR.md`) |
| Edges | Only a cropped subject, or one touching an edge, is a hard fail; a narrow margin is advisory (the layout trims margins) |
| References | Mapping v8: up to five per item (the image tool's limit), 66 distinct images (owner samples, including STYLE-REF-45 to 74, plus four public-domain prints). Every figure set (monster kinds, classes and ancestries, backgrounds, items) uses images found in no other set; no scenery reaches an isolated figure except the owner-approved wolf pack |
| Fresh start | The owner cleared every earlier approval on 2026-10-12, so the whole catalogue was regenerated under v8. The queue records `receipts_base`, so drift reviews count only new receipts |
| Helper | `next` and `status` fast-forward a clean clone, so mid-session redos show at once; `check` and `save` report the saved attempt's own number; `save` keeps a local copy in `HERALDRY_ARCHIVE`; messages name the running interpreter |
| Delivery | Every incoming image format (PNG, JPEG, WebP) goes through Git LFS, enforced by `ship` and `doctor` |
| Packaging | The installable ZIP is built on request (`make art-packages` or the `Build art packages` workflow), never committed |

Carried over from v7: the gritty old-school direction, per-family and per-kind reference sets with `ref_set` on each item, redos first then one lead item per set, delivery after every image with a drift review every tenth, and the guarded fast-forwarding `ship`. Carried over from v6: byte-bound QA records with ten evidenced criteria, native-hash receipts, prompt and reference hash checks at delivery, a clean index, and no force-push.

## Production boundary

- **The repository** holds the prompts, queue, references, the print intake and approval (`tools/art_intake.py`).
- **The art worker** (Codex, or another client with authenticated Git) follows each item's exact prompt with only the listed references, checks the native file and print-size preview, records evidence, and delivers through the guard. Whoever looked at an image may approve it, the worker included.
- **GitHub** stores the queue, receipts and the delivered image bytes through Git LFS.

## Run

```sh
python production/art/skill/heraldry-classic-ink-art/scripts/work_preflight.py --repo . --require-installed
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py doctor
python production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py status
```

On Codex, `production/art/codex/BATCH_CARD.md` is the whole working contract on one page. The image tool must actually accept the listed reference images: the scripts cannot prove that.

## Without authenticated Git

A worker that cannot push cannot deliver. It stops, keeps any saved images and receipts, and reports to the owner.

## Verification (no network needed)

```sh
python -m unittest discover -s tests -v   # or, from the repository root, `make test` runs this suite too
python scripts/validate_skill.py --zip /path/to/Heraldry_Classic_Ink_Art_Skill_v8_0.zip --repo /path/to/repo
```

## Included files

- `SKILL.md`, `OPERATOR_CARD.md`: the full procedure and a short starting card.
- `references/`:
  - `STYLE.md`, `STYLE_CONSISTENCY.md`, `VISUAL_ACCEPTANCE.md`: art direction.
  - `QA_CHECKLIST.md`: checks.
  - `REPAIR.md`: correction sentences for redos (one generation per item).
  - `FAMILIES.md`: family defaults.
  - `WORK_OPERATIONS.md`: capabilities, the QA record, and delivery safety.
  - `AD_HOC.md`: one-off requests.
- `references/images/`: byte-identical copies of every reference image any queue item can attach, with a SHA inventory. The queue's own reference paths are authoritative.
- `scripts/`: `heraldry_art.py`, `fidelity_gate.py`, `style_audit.py`, `work_preflight.py`, `delivery_guard.py`, `validate_skill.py`. The ZIP is built by `tools/art_skill_build.py` in the repository.
- `tests/`: regression tests that need no network. The `test_v5_regression.py` and `test_v6.py` file names are historical.

The skill package does not contain the queued prompts; they live in the repository queue.
