# Heraldry Skirmish

The publication repository for the Heraldry Skirmish rulebook. It holds the manuscript, the Typst book build, editable rules figures, and the pen-and-ink illustration pipeline that produces a borderless US Letter PDF edition in a clean dark-fantasy style.

## Agent workflows

Claude Code, Codex, and ChatGPT Work share the same repository workflows and five specialist roles. Start with [shared agent operations](docs/AGENT_OPERATIONS.md), `python tools/dev.py agent list`, and `python tools/dev.py agent check`. Platform tools and credentials must be available in the current session.

## Current state

<!-- BEGIN AUTO:status -->

- **Manuscript:** [RC513](source/Heraldry_RC513.md) (`source/versions.json`). Earlier snapshots are immutable.
- **Last recorded delivery:** [RC492-build-37](https://github.com/xjordont/Heraldry/releases/tag/RC492-build-37), 672 interior pages. RC513 source changes await a separately requested PDF build. [Evidence and limits](production/RELEASE_STATUS.md).
- **Last release workflow result:** RELEASED. This records that run, not verification of newer inputs.
- **Illustration records:** 299 approved of 299; 24 generation-queue items.
- **Rules figures:** 57; 57/57 current source/SVG/caption review bindings; 0 open findings. [Review ledger](production/qa/figure-semantic-review.json).
- **Physical printing:** NOT TESTED. Automated checks do not replace examination of real sheets.

<!-- END AUTO:status -->

Running log: [production/STATE.md](production/STATE.md).

Targeted editorial, reader, accessibility, and physical-proof checks: [publication protocol](docs/PUBLICATION_CHECKS.md) and [current first-pass findings](production/qa/publication-first-pass.md). These are separate from the last release's scoped PASS evidence.

## Recent changes

<!-- BEGIN AUTO:recent -->

- [`8214f250`](https://github.com/xjordont/Heraldry/commit/8214f25006ed03c87814a90520296f96913782e7) hero record: populate the illustrated record for the 24 Basic Mode Heroes
- [`20cb13bc`](https://github.com/xjordont/Heraldry/commit/20cb13bc5787ec2402fa407a52923b1f7f5378cb) ci: fetch Hero portraits for card tests; skip Work package test without LFS images
- [`98ca8910`](https://github.com/xjordont/Heraldry/commit/98ca8910374392d874a5e1dde9794ab6e4df8255) hero record: add illustrated blank Hero Record, front and Powers & Talents reverse
- [`86ce6f1d`](https://github.com/xjordont/Heraldry/commit/86ce6f1d4eb729cf1f6f6305340b7ddf1d1b6c19) layout: restore black visual anchors on blank Hero record
- [`3006eb12`](https://github.com/xjordont/Heraldry/commit/3006eb124720854a231cb20276ec0830259d6215) layout: refine blank Hero record with book typography and open ledgers
- [`4293a055`](https://github.com/xjordont/Heraldry/commit/4293a055d7953d194bf8f3640e4e27ba2066ff93) layout: standardize expanded Hero records with attached field labels

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

**With Codex or Claude Code:** select this repository on `main` and describe the change. Codex is the primary developer and integration owner. [CLAUDE.md](CLAUDE.md) is the governing contract; read it with [docs/WORKFLOW.md](docs/WORKFLOW.md) and `production/STATE.md`, then resume the existing work. [MASTER_PROMPT.md](MASTER_PROMPT.md) is the standing design and production contract, not a restart instruction.

**New manuscript:** supply the complete updated UTF-8 Markdown file. Run `python tools/dev.py manuscript prepare --input "path/to/update.md"`, review its exact diff and affected figures, then explicitly approve its `apply` command. It creates one next RC while retaining every prior version. See [the manuscript update guide](docs/MANUSCRIPT_UPDATES.md). PDF builds remain a separate owner request.

**Layout iteration:** `python tools/dev.py layout plan` previews the stages; `layout check` runs focused checks. For an explicitly requested local PDF proof, `layout run` records timings and evidence, reuses only verified measurements, and stops failed core checks before generating variants and review images. See [the layout workflow](docs/LAYOUT_WORKFLOW.md).

**Optional InDesign project:** run `python tools/dev.py indesign export --output "C:/Heraldry/indesign/my-project"`. It creates editable IDML with native text/tables, threaded chapter stories, styles, masters, navigation, fonts/licences, approved art and editable linked SVG figures. Run its `Finish in InDesign.jsx` in installed InDesign to finish composition and save native INDD, or use `indesign compose --project <folder>` on Windows. See [the InDesign guide](docs/INDESIGN_EXPORT.md). Only explicit commands or its manual Actions workflow start this export; normal development and PDF builds do not.

**Illustrations with Codex** (on the owner's PC): give Codex the line in [production/art/codex/CODEX_PROMPT.md](production/art/codex/CODEX_PROMPT.md). Its one-page contract is [BATCH_CARD.md](production/art/codex/BATCH_CARD.md); setup is in [CODEX_RUNBOOK.md](production/art/codex/CODEX_RUNBOOK.md). The pipeline is described in [docs/ART_AUTOMATION.md](docs/ART_AUTOMATION.md).

**Checks** (every change):

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
- [Visual QA](docs/VISUAL_QA.md) and [inkjet print profile](docs/INKJET_PRINT.md).
- [Reference analysis](docs/REFERENCE_ANALYSIS.md).

The owner's ten reference books are private, kept in Git LFS under `references/private/`, and never packaged (see [references/README.md](references/README.md)). They are visual inspiration only; the active manuscript is the rules authority. InDesign is an optional export, separate from the PDF release pipeline.

## Environment notes

- Cloud settings and network policies apply regardless of repository instructions. If the platform blocks a write, a model or a dependency, record the actual restriction; never claim a push that did not happen.
- Never print or commit credentials.
- `.claude/settings.json` selects the configured Opus model for orchestration, and the native agents in `.claude/agents/` use the configured Sonnet model for bulk work, at most two at a time.
