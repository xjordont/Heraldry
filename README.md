# Heraldry Skirmish

The publication repository for the Heraldry Skirmish rulebook. It holds the manuscript, the Typst book build, 57 editable rules figures, and the pen-and-ink illustration pipeline that produces a borderless US Letter PDF edition in a clean dark-fantasy style.

## Current state

- **Manuscript:** RC492 (`source/versions.json`). Earlier snapshots, from the original RC484 onwards, are immutable.
- **Last requested build:** RC492, 598 interior pages, with the six anchor illustrations of that time placed (the Giant Tarantula has since been sent back for a redo). Evidence and limits are in [production/RELEASE_STATUS.md](production/RELEASE_STATUS.md). Builds happen only when the owner asks.
- **Illustrations:** 275 planned.
  - Approved: 1 (Deepwarden). All earlier images were cleared on 2026-10-12 so every illustration is made the same way.
  - Queued for generation: 274 remaining of 275, one generation per item (gritty old-school black ink; skill v8).
- **Physical printing:** NOT TESTED until real sheets are examined.

Running log: [production/STATE.md](production/STATE.md).

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

**With Claude Code:** select this repository on `main` and describe the change. [CLAUDE.md](CLAUDE.md) is the governing contract. Claude reads it with [docs/WORKFLOW.md](docs/WORKFLOW.md) and `production/STATE.md`, then resumes the existing work. [MASTER_PROMPT.md](MASTER_PROMPT.md) is the standing design and production contract, not a restart instruction.

**Illustrations with Codex** (on the owner's PC): give Codex the line in [production/art/codex/CODEX_PROMPT.md](production/art/codex/CODEX_PROMPT.md). Its one-page contract is [BATCH_CARD.md](production/art/codex/BATCH_CARD.md); setup is in [CODEX_RUNBOOK.md](production/art/codex/CODEX_RUNBOOK.md). The pipeline is described in [docs/ART_AUTOMATION.md](docs/ART_AUTOMATION.md).

**Checks** (every change):

```sh
python3 -m pip install -r requirements.lock
python3 tools/preflight.py --baseline --report production/preflight.json
make test
```

**Build** (only when the owner asks for a PDF):

```sh
make clean all verify package
```

Then inspect the pages and record the visual review, and run the `Rebuild verified delivery` workflow to publish the Release. Outputs and commands are in [BUILD.md](BUILD.md). Page contact sheets for review come from `tools/contact_sheet.py`.

**On request:** `make art-packages`, or the `Build art packages` workflow, builds the installable skill ZIP and the offline ChatGPT Work package.

## Design references

- [Design specification](docs/DESIGN_SPEC.md) and [design refinement](docs/DESIGN_REFINEMENT.md).
- [Art direction](docs/ART_DIRECTION.md).
- [Visual QA](docs/VISUAL_QA.md) and [inkjet print profile](docs/INKJET_PRINT.md).
- [Reference analysis](docs/REFERENCE_ANALYSIS.md).

The owner's ten reference books are private, kept in Git LFS under `references/private/`, and never packaged (see [references/README.md](references/README.md)). They are visual inspiration only; the active manuscript is the rules authority. InDesign export is on hold.

## Environment notes

- Cloud settings and network policies apply regardless of repository instructions. If the platform blocks a write, a model or a dependency, record the actual restriction; never claim a push that did not happen.
- Never print or commit credentials.
- `.claude/settings.json` selects the configured Opus model for orchestration, and the native agents in `.claude/agents/` use the configured Sonnet model for bulk work, at most two at a time.
