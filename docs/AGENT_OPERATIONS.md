# Shared agent operations

Owner instruction, 2026-10-22: ChatGPT Work and Codex may perform every repository task Claude Code may perform. All three clients have the same repository authority: orchestrate, implement, repair, review, integrate, and deliver authorized work. This supersedes client-specific role restrictions in older prompts and cards. Scope restrictions belong to a task, not a product name.

Read `AGENTS.md`, `docs/PROJECT_CONTRACT.md`, the current `production/STATE.md`, `docs/WORKFLOW.md`, and `docs/BUILD_AUTOMATION.md`. Resolve the active manuscript from `source/versions.json`. Native Claude settings in `config/production.json` and `.claude/` configure Claude only; other clients use their current supported model and tools. Do not require a Claude model, account, CLI, or worker launcher to do repository work.

## One command surface

Run `python tools/dev.py doctor` to check local dependencies, then `python tools/dev.py agent check` and `python tools/dev.py agent list`. The dev launcher selects the repository environment on Windows or POSIX, including the existing Heraldry Windows venv. On the configured PC, use `C:/Heraldry/art-venv/Scripts/python.exe` if bare Python selects another installation.

`config/agent_workflows.json` defines one shared workflow catalog. There are no client-specific capability lists. `python tools/dev.py agent run NAME -- ARGS` forwards the arguments, Python environment, and underlying exit status to the existing tool. It never builds, approves, publishes, or fixes anything implicitly. Existing direct script commands remain supported; the catalog is a front door, not an allowlist limiting authorized development.

| Work | Shared command | Authority and evidence |
|---|---|---|
| Manuscript import | `agent run manuscript -- prepare --input FILE` | Review exact candidate, then apply actual owner authorization; immutable snapshots |
| Manuscript patch batch | `agent run revision -- --help` | Approved exact replacements through the revision engine |
| Art briefs and queue | `agent run art-catalog`, `agent run art-queue -- --help` | Catalog regeneration writes derived files; use current source, owner prompts, and art direction |
| Art generation | `agent run art-worker -- next --n 1` | Live batch card, built-in plan image tool, all listed references, native files, actual QA |
| Art delivery | `agent run art-delivery -- ship --execute --repo .` | Existing narrow Git/LFS guard; generated delivery is never approval |
| Art review | `agent run art-intake -- pending --sheet` | Inspect delivered images; use `approve --ids ... --by ACTUAL_REVIEWER` or `reject --ids ... --reason ...` |
| Offline art transport | `agent run art-package -- --help` | Verified input/review bundles and GitHub import workflow |
| Rules figures | `agent run figure-generate`, `agent run figure-review` | Current source, actual semantic inspection, and exact hash bindings |
| Layout | `agent run layout -- plan`, then `check` | Full proof requires an owner-requested layout/build task |
| Candidate and release | `agent run build -- check` | Owner-requested candidate, exact-PDF review, GitHub delivery |
| PDF review binding | `agent run visual-review -- bind --review FILE --push` | Named actual reviewer, all required images inspected, no unresolved major finding |
| Editable InDesign | `agent run indesign -- --help` | Explicit invocation; native composition requires installed InDesign |
| Publication verification/package | `agent run verify`, `agent run package` | Existing matching build, provenance, visual-review, and release gates |

Prefix table commands with `python tools/dev.py`. For a new task, first run ordinary `python tools/dev.py check`. A command reference is not authorization to build or publish unrelated work.

## Portable specialist roles

The five role contracts live in `docs/agents/`. Read one with `python tools/dev.py agent role publication-engineer` (or `book-designer`, `publication-auditor`, `rules-illustrator`, or `mechanical-assistant`). Claude-native definitions load these same files. Codex and ChatGPT Work can apply a role directly or pass it to a supported native worker. Use at most two workers, with disjoint file ownership, only when delegation is authorized and available. Without native delegation, perform the roles sequentially in the current session. A sequential author/reviewer is not an independent review; name the actual reviewer and record that limit.

## Scope and transport

A generation-only worker still follows the image/receipt allowlist and cannot approve its own delivery in that worker task. A developer or orchestrator task can edit briefs, queues, tooling, layout, and review records across clients. The art delivery guard remains narrow; ordinary code changes use the checked development publishing workflow. Changing clients never grants a new manuscript decision or bypasses review.

Review ownership is client-neutral. The owner or assigned reviewer may review, approve, or reject art, request redos, repair a failed candidate, and bind a fresh review after actual inspection. A failed review remains failed until the defect is repaired and the changed artifact is reviewed. Do not relabel generated art or a mechanical check as approval.

Use the current authenticated local repository or the host's supported repository tools. Verify Git/LFS transport before binary delivery. If a Work session lacks shell, file access, Git authentication, LFS transport, native workers, or reference-capable image generation, report the exact missing capability and use the existing supported transport: an offline art bundle and GitHub import workflow, or an authorized local executor. Repository code cannot enable an unavailable product tool or override platform permissions. Never paste credentials into a conversation or use a paid image API without explicit authorization. Do not infer present limitations from an old session's product name.

No manuscript revision, artwork approval, PDF build, release, or physical proof follows from this parity change itself. Physical printing remains **NOT TESTED** until actual sheets are examined.
