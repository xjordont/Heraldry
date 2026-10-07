# Launch readiness and visual references

This repository contains the current publication build. Resume production/STATE.md and follow docs/WORKFLOW.md. Preflight checks repository contracts and manuscript history; PDF and visual evidence require separate checks.

## Inspiration inputs

The written design specification is sufficient to start. For visual calibration, the best additional input is the selected PDF viewer pages across the ten owner-selected books in `references/reference_manifest.json`. Use additional selected pages only for a specific AI, grid-diagram, or index problem.

Do not make entire reference PDFs a repeated reading prerequisite. Reference access does not itself force Claude to read every page, but repeatedly assigning broad reference inspection would consume time and context without establishing clearer design decisions. Read the relevant sample once, record an abstract principle, and freeze the Heraldry component system after specimen repair.

Whole commercial PDFs are not needed in the repository. If you have permission to supply selected visual evidence to the cloud project, place it in a dedicated reference directory separate from original Heraldry assets. The local extraction tool defaults to an ignored `references/private/` directory: those files do not arrive in a cloud clone unless deliberately supplied through an authorised channel. A private repository does not itself grant redistribution rights. Use the written specification whenever optional excerpts are unavailable.

## Initial run

1. Select only this repository and the current `main` branch in Claude Code cloud. Continue on main; another branch requires an explicit owner decision. A multi-repository project may start above the clones and not load nested agent/settings files; if using that mode, explicitly verify configuration discovery.
2. Select the configured Opus model and medium effort; check actual runtime model access.
3. Use the available cloud execution mode, without assuming a Bypass option exists. Keep dependency registries reachable. The repository cannot grant model access, alter the network policy.
4. Send: `Read MASTER_PROMPT.md and execute it completely.`
5. Claude runs `python3 tools/preflight.py --baseline --report production/preflight.json` before any project edits. Failed kit checks require repair; missing optional references and uninstalled tools do not indicate a corrupt kit.
6. Claude provisions only necessary dependencies, records versions, builds the actual-content specimen, and advances through the complete production sequence.

Cloud setup scripts are configured in the Claude environment dialog; merely adding a file named setup.sh does not register one. A setup script is optional here because the production brief authorises capability discovery and dependency setup during execution.

GitHub API/release downloads from unrelated repositories can be blocked by the cloud GitHub proxy. If a tool download fails there, prefer a supported package-registry distribution, available system package, or documented alternative installation path. Do not add credentials or change repository access as an improvised workaround. Lock actual successful tool versions and record any engine substitution required by a tested blocker.

## Resume

Read `production/STATE.md` and update it at every milestone. On resume, run `python3 tools/preflight.py --report production/preflight.json` without `--baseline`: production code and setup may legitimately change, but the protected source must still match. The baseline option checks the archived RC484 original. Never alter a snapshot hash to disguise a manuscript edit; promote an approved batch to the next RC revision.


## Output expectations

Twelve native atmospheric masters are supplied by ChatGPT Work. Read production/art/HANDOFF.md and verify the original PNGs with tools/check_art.py. The fully illustrated target remains incomplete until the planned original assets are integrated and pagination is rechecked. Inspiration art is never used as replacement artwork.

The specified target is borderless portrait US Letter home inkjet printing. The run completes cream and white interior PDFs with identical pagination, finished Letter cover sheets, a calibration PDF and print instructions. Run the inkjet file checker and inspect the visual stress specimen. Physical device/media proof is NOT TESTED until actual sheets are examined; it does not block completion of the files. Commercial wraps, spine templates and PDF/X are NOT APPLICABLE unless separately requested. Check page count early for handling/binding; do not shrink type, omit rules or silently split volumes.

The required final checks remain complete source/table reconciliation, precise diagram semantics, stable TOC/index links, all-page visual coverage, and truthful separate readiness statuses. One passing launch check is not a substitute for those production gates.

Official capability references checked 2026-10-06:

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/claude-code-on-the-web
- https://code.claude.com/docs/en/cloud-environments

Read `docs/INKJET_PRINT.md`, `docs/VISUAL_QA.md` and `config/design_tokens.json` alongside the design specification. Commit and push verified main checkpoints at each milestone. Render/review contact sheets in resumable batches to control disk/memory; preserve exact inspected-page coverage. Neither automatic preflight nor this launch checklist certifies the current PDFs.
