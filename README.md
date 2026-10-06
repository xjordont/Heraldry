# Heraldry Skirmish publication project

This repository contains the canonical RC484 manuscript and the reference-informed Claude Code publication kit.

## Launch

Connect this repository to Claude Code cloud, verify available models and spending controls, then use:

> Read MASTER_PROMPT.md and execute it completely.

The kit requests Opus orchestration and Sonnet implementation, with a $100 maximum Claude-credit budget and $20 reserved for final repairs. Model availability and permissions are checked at execution.

## Project files

- [MASTER_PROMPT.md](MASTER_PROMPT.md): complete production brief and acceptance criteria.
- [README_SETUP.md](README_SETUP.md): setup, budget, artwork routes, and execution guidance.
- [docs/DESIGN_SPEC.md](docs/DESIGN_SPEC.md): typesetting, page layout, table components, diagrams, and navigation.
- [docs/REFERENCE_ANALYSIS.md](docs/REFERENCE_ANALYSIS.md): design lessons from 29 unique supplied reference books.
- [docs/ART_DIRECTION.md](docs/ART_DIRECTION.md): original monochrome fantasy illustration direction.
- [source/Heraldry_RC484.md](source/Heraldry_RC484.md): preserved canonical rules manuscript.
- [references/README.md](references/README.md): optional selected-page visual calibration.
- [.claude/agents/](.claude/agents/): five configured production roles.

The manuscript is the only authority for rules. Reference books supply visual inspiration only. Full commercial reference PDFs and page images are not included. Their absence does not block the build.

## Verify the uploaded kit

Run `python3 tools/preflight.py --baseline` from the repository root. The check uses only the Python standard library, verifies the source and all shipped checksums, and reports runtime capabilities. Read [docs/LAUNCH_CHECKLIST.md](docs/LAUNCH_CHECKLIST.md) for optional visual references and remaining account/art/printer inputs. These checks cover the launch kit, not a future generated book.

The publication PDFs, original art, final pagination, and inkjet file preflight are production tasks to be completed during execution.

## Primary output and visual contract

Borderless portrait US Letter inkjet sheets, light cream/parchment tone with clean black ink, and a paper-white companion. Every page remains portrait; backgrounds extend to edges while essential content stays safe. Read [DESIGN_SPEC.md](docs/DESIGN_SPEC.md), [VISUAL_QA.md](docs/VISUAL_QA.md), [INKJET_PRINT.md](docs/INKJET_PRINT.md), and [design_tokens.json](config/design_tokens.json). The final book checker is `tools/verify_inkjet_pdf.py`; run it on final book PDFs during production. Physical printing is a separate proof step. Commercial wraps are optional additional work.
