# Launch readiness and visual references

This repository is a prepared production assignment, not an already built publishing application. The parser, layouts, fonts, diagrams, PDF build commands, and publication QA are work Claude performs during the run. No preflight result certifies an unseen book.

## Inspiration inputs

The written design specification is sufficient to start. For visual calibration, the best additional input is the 14 selected PDF viewer pages across six primary books in `references/reference_manifest.json`. Use the other five selected pages only for a specific AI, grid-diagram, or index problem.

Do not make all 32 supplied PDFs mandatory input. Reference access does not itself force Claude to read every page, but repeatedly assigning broad reference inspection would spend time and context without establishing clearer design decisions. Read the relevant sample once, record an abstract principle, and freeze the Heraldry component system after specimen repair.

Whole commercial PDFs are not needed in the repository. If you have permission to supply selected visual evidence to the cloud project, place it in a dedicated reference directory separate from original Heraldry assets. The local extraction tool defaults to an ignored `references/private/` directory: those files do not arrive in a cloud clone unless deliberately supplied through an authorised channel. A private repository does not itself grant redistribution rights. Use the written specification whenever optional excerpts are unavailable.

## Initial run

1. Select this repository and the current `main` branch in Claude Code cloud. Work on the cloud task branch after launch.
2. Select the configured Opus model and medium effort; check actual access and credit/paid-overage settings in the account.
3. Use the available cloud execution mode, without assuming a Bypass option exists. Keep dependency registries reachable. The repository cannot grant model access, modify billing, or alter the network policy.
4. Send: `Read MASTER_PROMPT.md and execute it completely.`
5. Claude runs `python3 tools/preflight.py --baseline --report production/preflight.json` before any project edits. Failed kit checks require repair; missing optional references and uninstalled tools do not indicate a corrupt kit.
6. Claude provisions only necessary dependencies, records versions, builds the actual-content specimen, and advances through the complete production sequence.

Cloud setup scripts are configured in the Claude environment dialog; merely adding a file named setup.sh does not register one. A setup script is optional here because the production brief authorises capability discovery and dependency setup during execution.

GitHub API/release downloads from unrelated repositories can be blocked by the cloud GitHub proxy. If a tool download fails there, prefer a supported package-registry distribution, available system package, or documented alternative installation path. Do not add credentials or change repository access as an improvised workaround. Lock actual successful tool versions and record any engine substitution required by a tested blocker.

## Resume

Read `production/STATE.md` and update it at every milestone. On resume, run `python3 tools/preflight.py --report production/preflight.json` without `--baseline`: production code and setup may legitimately change, but the protected source must still match. Use the full baseline again only when auditing an untouched checkout of this launch-kit revision. Never recompute the canonical source hash to disguise a changed manuscript.

The preflight does not enforce the paid-service budget. The account's controls enforce billing; configuration and the production ledger guide the agent.

## Output expectations

With no supplied original illustrations or configured authorised image service, the run completes an art-light edition and an asset-generation plan. The fully illustrated target remains incomplete until the planned original assets are integrated and pagination is rechecked. Inspiration art is never used as replacement artwork.

With no printer selected, the run creates a complete digital edition, a generic print candidate, and cover panels/candidate. Submission-ready print files still require the printer's specification, binding/paper decisions, final page count, and cover template. Check the estimated full page count early: do not shrink type, omit rules, or silently split volumes to satisfy an unknown binding limit.

The required final checks remain complete source/table reconciliation, precise diagram semantics, stable TOC/index links, all-page visual coverage, and truthful separate readiness statuses. One passing launch check is not a substitute for those production gates.

Official capability references checked 2026-10-06:

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/claude-code-on-the-web
- https://code.claude.com/docs/en/cloud-environments
