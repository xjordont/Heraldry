# Heraldry Skirmish publication project

[source/versions.json](source/versions.json) identifies the active manuscript. [RC485](source/Heraldry_RC485.md) was created to contain the seven approved clarifications previously applied during the RC484 build. The [original RC484](source/Heraldry_RC484.md) remains unchanged. All snapshots and their exact approved patch evidence remain available.

All future iterations use **main** unless the owner explicitly decides otherwise. Manuscript text-patch batches advance the RC number once; artwork, figure and layout changes use ordinary Git commits. Read [WORKFLOW.md](docs/WORKFLOW.md) for the exact revision command and review requirements.

## Continue with Claude Code

Select this repository and main, then provide your requested change with:

> Read CLAUDE.md, docs/WORKFLOW.md and production/STATE.md. Implement the requested iteration on main using the active manuscript in source/versions.json. Preserve earlier snapshots. Advance the RC number once if manuscript text changes. Follow MASTER_PROMPT.md, rebuild, verify, inspect and package the result, update the ledgers, and push verified work to main. Do not create a branch unless I explicitly decide to use one.

The project already has a working Typst build, 57 editable rules figures and twelve ChatGPT-generated atmospheric masters. [MASTER_PROMPT.md](MASTER_PROMPT.md) is its standing design/production contract. Resume the existing work; do not restart it.

## Build

```sh
python3 -m pip install -r requirements.lock
make test
make clean all verify package
```

See [BUILD.md](BUILD.md) for commands and [RELEASE_STATUS.md](production/RELEASE_STATUS.md) for actual evidence and limitations. Built PDFs are published as GitHub Releases, not committed ([docs/LARGE_FILES.md](docs/LARGE_FILES.md)); the RC492 PDFs built before that policy are in Git history (the link is in that document). The prior release ZIP is withheld during this artwork/design iteration; rebuild and review before creating a new release archive. Automated checks bind results to current source, code, assets and PDF hashes; visual review and physical printing remain separate.

## Design and components

- [Design specification](docs/DESIGN_SPEC.md), [art direction](docs/ART_DIRECTION.md), [visual QA](docs/VISUAL_QA.md) and [inkjet profile](docs/INKJET_PRINT.md).
- Manuscript snapshots and approved patch history: `source/` and `editorial/history/`.
- Original atmospheric assets and prompts: `assets/art/incoming/` and `production/art/`.
- Rules figure sources, SVGs and reviewed placement: `figures/`.
- Typesetting and build tools: `typst/`, `tools/` and `config/`.
- [Native Claude agents](.claude/agents/) and [reference analysis](docs/REFERENCE_ANALYSIS.md).

The design is clean dark fantasy on cream or white, borderless portrait US Letter, with essential content protected inside the printer overscan area. Reference books provide visual inspiration only; the active Heraldry manuscript is the rules authority. Commercial PDFs are not bundled. The twelve native atmospheric masters are supplied in assets/art/incoming/; read [artwork handoff](production/art/HANDOFF.md) for exact prompts, native placement limits and the required integration/review pass. InDesign export is on hold. Physical printer proof remains NOT TESTED.
