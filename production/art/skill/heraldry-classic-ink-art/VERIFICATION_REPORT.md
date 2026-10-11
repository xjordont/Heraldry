# Heraldry Skirmish Classic Ink Art Skill v7.0: release verification

## Outcome

**Offline release validated (2026-10-11).** This is not a claim of production-tested image generation or guaranteed artistic quality.

## What changed from v6

1. **Art direction:** gritty old-school black-and-white ink. The prompts, `STYLE.md`, `STYLE_CONSISTENCY.md`, `VISUAL_ACCEPTANCE.md` and `REPAIR.md` were updated, including a new "too clean" correction.
2. **Reference mapping v7:** 17 sets, made of five monster kinds (by ID, with a coverage check) and one set per family. Each queue item records its `ref_set`, and `show` prints it. The ZIP carries every attachable reference, derived from `config/art_style.json`.
3. **Queue order:** after any redos, seventeen lead items come first, one per set, so the first two drift reviews (images 10 and 20) cover every set.
4. **Cadence:** each image is delivered when it is saved, with a drift review every tenth image (`sheet --recent`, `style_audit --recent`).
5. **Delivery guard:** a safe fast-forward over intake commits, a retry after a lost push, and a stop on divergence or overlap. This was carried from v6 fixes made the same day.
6. **Docs:** the reference docs have version-free names, the obsolete v6 `deployment/` folder is removed, and `work_preflight --require-installed` checks for v7.

## Audit fixes (2026-10-11, second pass)

- **delivery_guard `ship`:**
  - A commit that was made but never pushed (timeout, killed session) is recovered on the next run instead of blocking forever.
  - Any failure between staging and pushing rolls back to a clean index.
  - Pushes cannot hang on a credential prompt.
  - Authentication and LFS failures report their real cause.
  - A push that timed out but landed is recognised and not delivered twice.
  - A redo saved in a different file format is delivered as a replacement.
- **Refusals:** a refusal now binds to the prompt it refused, so a republished prompt reopens the item.
- **Robustness:** UTF-8 reads throughout the worker scripts (Windows). `doctor` reports a clone without `git lfs install`. The dead 5% aspect check is removed. `check` caches image hashes in scratch, so it no longer re-decodes every delivered image on every call.
- **Workflows:**
  - Intake and bundle import start every attempt from the newest main. Concurrent deliveries can no longer conflict over `SELECTIONS.json`, and resets no longer download every LFS file.
  - The import has its own concurrency group.
  - Repository checks skip pure image deliveries.
- **Prompts:** a second, semantic audit of all 270 prompts fixed about 50 brief defects:
  - contradictions with the source text (the toll-road bandit captain's weapon, the snow goblin's sling);
  - internal contradictions (carcass, kneeling legionaries, stars on black, the spider sizes);
  - scale conflicts (Briarling, Executioner, Last Colossus);
  - near-duplicate poses (Harpy/Gargoyle, Gloom Hulk/Burrowmaw, Spectre/Lich/Ice Wraith, Fallen Paladin/Ashen Revenant, Undead Sentinel/Tomb Guardian, Wererat/Ratkin, Werebear/Gorebeak Bear);
  - glow, ray and tone wording;
  - garbled lines;
  - "Wide" compositions in square monster prompts.

## Prime-time pass (2026-10-11, third pass)

- `status` lists redos first, like `next`. The drift-review count is monotonic, so a rejection cannot repeat a review. The DRIFT REVIEW message prints the exact `style_audit` command and says to deliver in every case.
- Helper commands print the running interpreter, and receipts name the real surface.
- `sheet --out` inside the clone is refused, and `check` says when an attempt was the last allowed one.
- `style_audit` and the recent-image list skip LFS pointers. `style_audit` defaults its report to scratch and prints its advisories.
- `delivery_guard ship` fetches once per delivery, not twice.
- The stale smoke-file gate and `--out` wording were removed from every worker document.
- Re-checking an earlier attempt reports that attempt; receipts record `saved_attempt` beside `variants_tried`.
- `next` and `status` fast-forward a clean clone first, so a mid-session redo shows at once.
- Every incoming image format goes through Git LFS, enforced by `ship` and `doctor`.

## Tests

- Skill suite (`python -m unittest discover -s tests`, run from the skill folder): **49 tests passed**, including new real-git tests for unpushed-commit recovery, a landed push, a format replacement, a refused deletion, a failed-push rollback, and a refusal reopening after a prompt fix.
- `scripts/validate_skill.py --zip ... --repo .`: **PASS**. Package hashes, required files, reference images byte-identical to the repository, and FAMILIES.md current.
- Repository pipeline tests: the reference mapping, kind coverage (a missing or duplicate kind fails), the lead order, and that no isolated figure receives a scenic reference.
- Prompt audit across all 270 queue prompts: hashes, no placeholders, every must and avoid line present, vignettes on scenes, isolation on figures, source text, size class, and no stipple or detail-heavy wording in subject details. **0 issues.**

## Not verified offline

- Whether the worker's image tool accepts the listed reference images, and what model or size it offers.
- Real image quality and style consistency across families. The first drift review at image 10 is the first evidence.
- Git LFS delivery from the worker's machine over a long unattended run, and the ChatGPT plan's usage limits.
