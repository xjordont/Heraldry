# Heraldry publication repository

Execute `MASTER_PROMPT.md` as the production brief. Canonical source: `source/Heraldry_RC484.md`; preserve bytes and record hash. Layout, assets, metadata, and explicit authorized editorial patches live separately.

Primary model: Opus 5.5, medium effort for ordinary orchestration; Sonnet 5.5 does bulk implementation. Native project agents are in `.claude/agents/`. At most two workers concurrently; assign disjoint output ownership. Do not use paid nested API/CLI workers as a substitute for native cloud subagents.

Read `config/production.json`, `docs/ART_DIRECTION.md`, and `docs/DESIGN_SPEC.md`. Use `docs/REFERENCE_ANALYSIS.md` once for design rationale; optional visual pages are in `references/reference_manifest.json`. Reference books are visual inspiration only. Their mechanics never supersede Heraldry. Missing references do not block production. Claude cloud budget is $100; target $80 with $20 reserved for final repairs. No external paid image generation is authorized unless its configuration explicitly grants a separate budget. Keys are not authorization to spend. Do not print secrets.

Use deterministic scripts for conversion/inventory; never regenerate all source prose or tables with an LLM. Maintain complete source/table/output mappings. Build a real stress specimen, then the complete book, diagrams/assets, navigation, and verified deliverables. The specimen is not completion.

Track state/next commands in `production/STATE.md`; record costs, editorial changes, asset status, QA and print blockers in on-disk ledgers. Continue authorized work without design approval pauses. Preserve checkpoints under resource limits. Report actual results; no unsupported claims of full illustration, PDF/X certification, perfect visual inspection, or printer-specific readiness.

Before first execution, read `docs/LAUNCH_CHECKLIST.md` and run `python3 tools/preflight.py --baseline --report production/preflight.json`. On resume after production changes, omit `--baseline` while retaining source integrity. `production/STATE.md` is initialised as NOT STARTED; update it with evidence at each milestone.

Primary output: borderless portrait US Letter home-inkjet sheets (612 × 792 pt), light cream background to all edges, plus a paper-white companion. Read `docs/INKJET_PRINT.md`, `docs/VISUAL_QA.md` and `config/design_tokens.json`. No landscape inserts, external bleed canvas, crop marks or default commercial wrap. Essential text/folios/geometry remain at least 0.375 inch from edges. Run the supplied inkjet PDF checker on final book variants. File readiness and physical proof are separate; physical proof is NOT TESTED until actual output is examined. Push buildable task-branch checkpoints at milestones; retain resumable QA batches.
