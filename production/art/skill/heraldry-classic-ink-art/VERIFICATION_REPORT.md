# Heraldry Skirmish Classic Ink Art Skill v7.0: release verification

## Outcome

**Offline release validated (2026-10-11).** This is not a claim of production-tested image generation or guaranteed artistic quality.

## What changed from v6

1. **Art direction:** gritty old-school black-and-white ink. The prompts, `STYLE.md`, `STYLE_CONSISTENCY.md`, `VISUAL_ACCEPTANCE.md` and `REPAIR.md` were updated, including a new "too clean" correction.
2. **Reference mapping v7:** 17 sets, made of five monster kinds (by ID, with a coverage check) and one set per family. Each queue item records its `ref_set`, and `show` prints it. The ZIP carries every attachable reference, derived from `config/art_style.json`.
3. **Queue order:** ten lead items, one per set, come first, so the first drift review covers every set.
4. **Cadence:** each image is delivered when it is saved, with a drift review every tenth image (`sheet --recent`, `style_audit --recent`).
5. **Delivery guard:** a safe fast-forward over intake commits, a retry after a lost push, and a stop on divergence or overlap. This was carried from v6 fixes made the same day.
6. **Docs:** the reference docs have version-free names, the obsolete v6 `deployment/` folder is removed, and `work_preflight --require-installed` checks for v7.

## Tests

- Skill suite (`python -m unittest discover -s tests`, run from the skill folder): **39 tests passed**.
- `scripts/validate_skill.py --zip ... --repo .`: **PASS**. Package hashes, required files, reference images byte-identical to the repository, and FAMILIES.md current.
- Repository pipeline tests: the reference mapping, kind coverage (a missing or duplicate kind fails), the lead order, and that no isolated figure receives a scenic reference.
- Prompt audit across all 270 queue prompts: hashes, no placeholders, every must and avoid line present, vignettes on scenes, isolation on figures, source text, size class, and no stipple or detail-heavy wording in subject details. **0 issues.**

## Not verified offline

- Whether the worker's image tool accepts the listed reference images, and what model or size it offers.
- Real image quality and style consistency across families. The first drift review at image 10 is the first evidence.
- Git LFS delivery from the worker's machine over a long unattended run, and the ChatGPT plan's usage limits.
