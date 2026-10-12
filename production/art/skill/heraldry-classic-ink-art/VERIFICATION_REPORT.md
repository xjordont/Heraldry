# Heraldry Skirmish Classic Ink Art Skill v8.0: release verification

## Outcome

**Offline release validated (2026-10-12).** This does not claim that image generation has been tested in production, or that artistic quality is guaranteed.

## What changed from v7

1. **One generation per item.** Owner decision, 2026-10-12, after the first eight batch images: "the first image generated for each prompt is far superior to any further attempts".
   - `max_attempts` is 1 for every item, generated in a fresh context.
   - A defect is saved with `--accept-flags --notes`, and Claude Code decides on a redo.
   - A redo is one fresh generation with at most two correction sentences. `REPAIR.md` now covers redos only.
2. **Edges.** Only a cropped subject, or one touching an edge, is a hard fail. A narrow margin is advisory, because the layout trims it; the old 8% rule had forced retries.
3. **Reference mapping v8.**
   - Up to six references per item (`max_refs` 6), drawn from 66 distinct images: the owner's samples, including STYLE-REF-45 to 74, plus four public-domain prints.
   - Every figure set (the five monster kinds, classes and ancestries, backgrounds, items) uses images found in no other set.
   - Scenery never reaches an isolated figure, except the owner-approved wolf pack in the beast set.
   - Two full reviews of every reference against every set are recorded in `docs/ART_DIRECTION.md`.
4. **Fresh start.**
   - The owner cleared all earlier approvals, so all 275 items are pending.
   - The queue records `receipts_base`, so drift reviews count only receipts written after publication.
   - The Giant Tarantula brief was recomposed: a view from above with the eight legs radiating evenly.
5. **Helper (`heraldry_art.py`).**
   - `next` and `status` fast-forward a clean clone first, so a mid-session redo shows at once.
   - `check` and `save` report the saved attempt's own number, and receipts record `saved_attempt`.
   - `save` keeps a local copy in `HERALDRY_ARCHIVE`.
   - Commands in messages name the running interpreter, and the retired smoke-file hints are gone.
6. **Delivery.** PNG, JPEG and WebP all go through Git LFS, enforced by `ship` and `doctor`.
7. **Packaging and intake.**
   - The installable ZIP and the offline package are built on request (`make art-packages`, or the `Build art packages` workflow), never committed.
   - The intake fetches non-PNG pointers too, names the recorded surface in provenance, and commits no contact sheets; the reviewer uses `art_intake.py pending --sheet`.

The v7 changes (gritty direction, per-family and per-kind sets, lead order, per-image cadence, guarded fast-forward `ship`) and the v6 integrity guarantees (byte-bound QA records with ten evidenced criteria, native-hash receipts, prompt and reference hash checks at delivery, a clean index, no force-push) carry over unchanged.

## Tests

- **Skill suite** (`python -m unittest discover -s tests`, run from the skill folder): passes. Real-git and LFS regressions cover:
  - unpushed-commit recovery, a landed push, a format replacement, a refused deletion and a failed-push rollback;
  - a refusal reopening after a prompt fix;
  - the monotonic drift count, and receipts before `receipts_base`;
  - the refresh with and without unsent work;
  - the saved attempt number;
  - the archive copy;
  - LFS pointers in `style_audit` and in the recent-image list.
- **Repository suite** (`make test`): passes. It builds a fresh skill ZIP and offline package, and checks:
  - that both builds are reproducible;
  - the validator and its tamper detection;
  - the reference mapping, kind coverage, the lead order, one generation per item, and that no isolated figure receives a scenic reference.
- **Fresh-clone rehearsal of Codex's routine:** a partial clone of `main` with LFS skip-smudge, then the preflight, `doctor`, `status`, `next` and one full delivery (check, qa, save, ship to a local remote). All passed. See `production/STATE.md`.

## Not verified offline

- What model and size the worker's image tool offers. The owner confirmed on 2026-10-12 that Codex accepts six reference images.
- Real image quality and style consistency across sets. The drift reviews at images 10 and 20 are the first evidence.
- Git LFS delivery from the worker's PC over a long unattended run. ChatGPT Plus usage resets every 5 hours; each session ends at the limit and the same prompt resumes.
