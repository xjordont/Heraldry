# Heraldry Skirmish

The publication repository for the Heraldry Skirmish rulebook. It holds the manuscript, the Typst book build, editable rules figures, and the pen-and-ink illustration pipeline that produces a digital US Letter PDF edition in a clean dark-fantasy style.

## Agent workflows

Claude Code, Codex, and ChatGPT Work share the same repository workflows and six specialist roles. Start with [shared agent operations](docs/AGENT_OPERATIONS.md), `python tools/dev.py agent list`, and `python tools/dev.py agent check`. Platform tools and credentials must be available in the current session.

## Current state

<!-- BEGIN AUTO:status -->

- **Manuscript:** [RC528](source/Heraldry_RC528.md) (`source/versions.json`). Earlier snapshots are immutable.
- **Last recorded delivery:** [RC528-build-43](https://github.com/xjordont/Heraldry/releases/tag/RC528-build-43), 628 pages. Newer source/tooling changes may await a separately requested build. [Evidence and limits](production/STATE.md).
- **Last release workflow result:** RELEASED. This records that run, not verification of newer inputs.
- **Illustration records:** 346 approved of 346; 0 generation-queue items.
- **Rules figures:** 77; 77/77 current source/SVG/caption review bindings; 0 open findings. [Review ledger](production/qa/figure-semantic-review.json).

<!-- END AUTO:status -->

Running log: [production/STATE.md](production/STATE.md); entries before 2026-11-01 are in [production/history/STATE-2026-10.md](production/history/STATE-2026-10.md).

The status block refreshes automatically after pushes to `main` and after workflows that commit to it; `python tools/dev.py check` also refreshes it locally. Edit the surrounding guidance normally, but never the generated block. [Maintenance details](docs/README_AUTOMATION.md).

Editorial, reader, and accessibility checks follow the [publication protocol](docs/PUBLICATION_CHECKS.md). They are separate from the last release's scoped PASS evidence.

## How the project runs

| Track | Where | Rule |
|---|---|---|
| Manuscript | `source/`, `editorial/history/` | Each approved text-patch batch creates exactly one new RC with `tools/revise_manuscript.py`. Snapshots are never edited. Prose is never regenerated |
| Illustrations | `production/art/`, `assets/art/` | Prompts and queue come from the manuscript (`tools/art_gpt_pack.py`). Codex generates within the owner's ChatGPT plan and delivers each image. Whoever looks at an image may approve it, the generating client included. Only approved art is placed. Art changes never change the RC |
| Rules figures | `figures/src/`, `figures/out/` | Source-faithful vector diagrams with a semantic review ledger |
| Layout | `typst/`, `config/design_tokens.json` | Whole sections stay on one page when they fit (the keep rule in [docs/PROJECT_CONTRACT.md](docs/PROJECT_CONTRACT.md), checked by a mandatory audit) |
| Player aids and Hero records | `typst/aids/`, `assets/hero-record/` | Companion PDFs built with every release; they never change the RC |

- `main` is the only branch.
- Large build outputs (PDFs, ZIP packages) are never committed. Each requested build is published as a GitHub Release. See [docs/LARGE_FILES.md](docs/LARGE_FILES.md).

## Working on it

**With Codex, Claude Code, or ChatGPT Work:** select this repository on `main` and describe the change. All three have equal authority under [AGENTS.md](AGENTS.md), the shared agent contract; it points to `production/STATE.md` and the task docs. Product requirements are in [docs/PROJECT_CONTRACT.md](docs/PROJECT_CONTRACT.md) and the design system in [docs/DESIGN.md](docs/DESIGN.md).

**New manuscript:** supply the complete updated UTF-8 Markdown file. Run `python tools/dev.py manuscript prepare --input "path/to/update.md"`, review its exact diff and affected figures, then explicitly approve its `apply` command. It creates one next RC while retaining every prior version. See [the manuscript update guide](docs/MANUSCRIPT_UPDATES.md). PDF builds remain a separate owner request.

**Layout iteration:** `python tools/dev.py layout plan` previews the stages; `layout check` runs focused checks. For an explicitly requested local PDF proof, `layout run` records timings and evidence, reuses only verified measurements, and stops failed core checks before generating variants and review images. See [the layout workflow](docs/LAYOUT_WORKFLOW.md).

**Illustrations with Codex** (on the owner's PC): give Codex the line in [production/art/codex/CODEX_PROMPT.md](production/art/codex/CODEX_PROMPT.md). Its one-page contract is [BATCH_CARD.md](production/art/codex/BATCH_CARD.md); setup is in [CODEX_RUNBOOK.md](production/art/codex/CODEX_RUNBOOK.md). The pipeline is described in [docs/ART_AUTOMATION.md](docs/ART_AUTOMATION.md).

**Checks:** docs and art changes need none; for code changes run the tests that cover them, and CI runs the full suite on most pushes to `main` (AGENTS.md lists the exceptions). The full local check is:

```sh
python tools/dev.py check
```

**Build** (only when the owner asks for a PDF): in Claude Code the owner types `/build-release`; any client can follow [docs/BUILD_CARD.md](docs/BUILD_CARD.md). GitHub Actions builds the candidate and the release ([docs/BUILD_AUTOMATION.md](docs/BUILD_AUTOMATION.md)). `make` targets and outputs are in [BUILD.md](BUILD.md); a local `make` run is a proof for requested layout work and never publishes anything.

**On request:** `make art-packages`, or the `Build art packages` workflow, builds the installable art skill ZIP.

## Design

- [Design](docs/DESIGN.md): page grammar, type, components, art placement, and the typesetting policy. Its template specimens are in `typst/templates/` (render with `python3 tools/render_template_specimens.py --sheet`; PNG only, never a book PDF).
- [Art direction](docs/ART_DIRECTION.md) and [visual QA](docs/VISUAL_QA.md).
- Retired briefs, studies, and dated decisions are kept in [docs/history/](docs/history/).

The owner's reference books are background inspiration only; the active manuscript is the rules authority.

## Environment notes

- Cloud settings and network policies apply regardless of repository instructions. If the platform blocks a write, a model, or a dependency, record the actual restriction; never claim a push that did not happen.
- Never print or commit credentials.
- `.claude/settings.json` runs the main Claude Code session on the configured Opus model at medium effort. The native agents in `.claude/agents/` use Sonnet, except `mechanical-assistant` (Haiku) and `blind-editorial-reviewer` (Opus); `config/production.json` allows at most two at a time.
