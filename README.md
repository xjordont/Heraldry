# Heraldry Skirmish

The publication repository for the Heraldry Skirmish rulebook. It holds the manuscript, the Typst book build, editable rules figures, and the pen-and-ink illustration pipeline that produces a digital US Letter PDF edition in a clean dark-fantasy style.

## Agent workflows

Claude Code, Codex, and ChatGPT Work share the same repository workflows and five specialist roles. Start with [shared agent operations](docs/AGENT_OPERATIONS.md), `python tools/dev.py agent list`, and `python tools/dev.py agent check`. Platform tools and credentials must be available in the current session.

## Current state

<!-- BEGIN AUTO:status -->

- **Manuscript:** [RC528](source/Heraldry_RC528.md) (`source/versions.json`). Earlier snapshots are immutable.
- **Last recorded delivery:** [RC527-build-41](https://github.com/xjordont/Heraldry/releases/tag/RC527-build-41). RC528 source changes await a separately requested PDF build. [Evidence and limits](production/RELEASE_STATUS.md).
- **Last release workflow result:** RELEASED. This records that run, not verification of newer inputs.
- **Illustration records:** 346 approved of 346; 0 generation-queue items.
- **Rules figures:** 77; 77/77 current source/SVG/caption review bindings; 0 open findings. [Review ledger](production/qa/figure-semantic-review.json).

<!-- END AUTO:status -->

Running log: [production/STATE.md](production/STATE.md).

Targeted editorial, reader, and accessibility checks: [publication protocol](docs/PUBLICATION_CHECKS.md) and [current first-pass findings](production/qa/publication-first-pass.md). These are separate from the last release's scoped PASS evidence.

## Recent changes

<!-- BEGIN AUTO:recent -->

- [`4d7d8aa2`](https://github.com/xjordont/Heraldry/commit/4d7d8aa2b9c7f240ba559664e2495321cfe56735) RC528: humanizer revision applied (131 approved exact replacements)
- [`b3150f5a`](https://github.com/xjordont/Heraldry/commit/b3150f5ac4b5822d5aad1acb6a9215f2e348f77f) build: finish digital-only cleanup after the local proof
- [`e8da035d`](https://github.com/xjordont/Heraldry/commit/e8da035d724ae31d5e695082e5d8376ed05b2ce8) editorial: third humanizer pass rewrites the rejected patches (131 proposed)
- [`8330e00a`](https://github.com/xjordont/Heraldry/commit/8330e00ae4c8c6bdc93c6ef024ef4763f1d5967e) docs: remove physical-printing references from the design, QA, and role docs
- [`446e2ede`](https://github.com/xjordont/Heraldry/commit/446e2ede6c1184e674c5b0f2a9f834ae82700280) build: go digital-only and remove the InDesign export
- [`82b33d52`](https://github.com/xjordont/Heraldry/commit/82b33d520e05fab6db26ca0f0d831625711bb667) editorial: quality-review the RC528 humanizer proposal (64 kept, 76 withdrawn)

<!-- END AUTO:recent -->

Status and recent changes refresh automatically after pushes to `main` and completed repository workflows, including bot updates. `python tools/dev.py check` also refreshes them locally. Edit the surrounding guidance normally; the marked blocks come from repository records and Git history. [Maintenance details](docs/README_AUTOMATION.md).

## How the project runs

| Track | Where | Rule |
|---|---|---|
| Manuscript | `source/`, `editorial/history/` | Each approved text-patch batch creates exactly one new RC with `tools/revise_manuscript.py`. Snapshots are never edited. Prose is never regenerated |
| Illustrations | `production/art/`, `assets/art/` | Prompts and queue come from the manuscript (`tools/art_gpt_pack.py`). Codex generates within the owner's ChatGPT plan and delivers each image. Claude Code reviews and approves. Only approved art is placed. Art changes never change the RC |
| Rules figures | `figures/src/`, `figures/out/` | Source-faithful vector diagrams with a semantic review ledger |
| Layout | `typst/`, `config/design_tokens.json` | Whole sections stay on one page when they fit (mandatory pagination audit) |

- `main` is the only branch.
- Large build outputs (PDFs, ZIP packages) are never committed. Each requested build is published as a GitHub Release. See [docs/LARGE_FILES.md](docs/LARGE_FILES.md).

## Working on it

**With Codex, Claude Code, or ChatGPT Work:** select this repository on `main` and describe the change. All three have equal authority under [AGENTS.md](AGENTS.md), the shared agent contract; it points to `production/STATE.md` and the task docs. [MASTER_PROMPT.md](MASTER_PROMPT.md) is the standing design and production contract, not a restart instruction.

**New manuscript:** supply the complete updated UTF-8 Markdown file. Run `python tools/dev.py manuscript prepare --input "path/to/update.md"`, review its exact diff and affected figures, then explicitly approve its `apply` command. It creates one next RC while retaining every prior version. See [the manuscript update guide](docs/MANUSCRIPT_UPDATES.md). PDF builds remain a separate owner request.

**Layout iteration:** `python tools/dev.py layout plan` previews the stages; `layout check` runs focused checks. For an explicitly requested local PDF proof, `layout run` records timings and evidence, reuses only verified measurements, and stops failed core checks before generating variants and review images. See [the layout workflow](docs/LAYOUT_WORKFLOW.md).

**Illustrations with Codex** (on the owner's PC): give Codex the line in [production/art/codex/CODEX_PROMPT.md](production/art/codex/CODEX_PROMPT.md). Its one-page contract is [BATCH_CARD.md](production/art/codex/BATCH_CARD.md); setup is in [CODEX_RUNBOOK.md](production/art/codex/CODEX_RUNBOOK.md). The pipeline is described in [docs/ART_AUTOMATION.md](docs/ART_AUTOMATION.md).

**Checks:** docs and art changes need none; for code changes run the tests that cover them, and CI runs the full suite on every push. The full local check is:

```sh
python tools/dev.py check
```

**Build** (only when the owner asks for a PDF):

```sh
make clean all verify package
```

Then inspect the pages and record the visual review, and run the `Rebuild verified delivery` workflow to publish the Release. Outputs and commands are in [BUILD.md](BUILD.md). Page contact sheets for review come from `tools/contact_sheet.py`.

**On request:** `make art-packages`, or the `Build art packages` workflow, builds the installable skill ZIP and the offline ChatGPT Work package.

## Design references

- [PDF layout and density review](reports/Rulebook%20layout%20and%20density%20review.md): current pipeline/PDF audit, reference-book lessons, and proposed layout trials.
- [Book design plan](docs/BOOK_DESIGN_PLAN.md): design system v2, a template for every page type. Its specimens are in `typst/templates/` (render with `python3 tools/render_template_specimens.py --sheet`; PNG only, never a book PDF). The evidence is in the [reference study](docs/design/REFERENCE_STUDY.md).
- [Design specification](docs/DESIGN_SPEC.md) and [design refinement](docs/DESIGN_REFINEMENT.md) (pagination policy).
- [Art direction](docs/ART_DIRECTION.md).
- [Visual QA](docs/VISUAL_QA.md).
- [Reference analysis](docs/REFERENCE_ANALYSIS.md).

The owner's ten reference books are private, kept in Git LFS under `references/private/`, and never packaged (see [references/README.md](references/README.md)). They are visual inspiration only; the active manuscript is the rules authority.

## Environment notes

- Cloud settings and network policies apply regardless of repository instructions. If the platform blocks a write, a model or a dependency, record the actual restriction; never claim a push that did not happen.
- Never print or commit credentials.
- `.claude/settings.json` selects the configured Opus model for orchestration, and the native agents in `.claude/agents/` use the configured Sonnet model for bulk work, at most two at a time.
