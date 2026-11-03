# Agent commands

All three clients use the same commands, catalogued in `config/agent_workflows.json`. Prefix each with `python tools/dev.py`, which picks the project Python on Windows or POSIX (on the configured PC, use `C:/Heraldry/art-venv/Scripts/python.exe` if bare Python finds another installation). A command never builds, approves, or publishes anything you did not ask for, and direct script calls still work. `agent list` shows every workflow.

| Work | Command |
|---|---|
| Environment and status | `doctor`, `agent check`, `status` |
| Full local check | `check` |
| Manuscript import | `agent run manuscript -- prepare --input FILE`, then apply with the owner's approval |
| Manuscript patch batch | `agent run revision -- --help` |
| Art briefs and queue | `agent run art-catalog`, `agent run art-queue -- --help` |
| Art generation | `agent run art-worker -- next --n 1` |
| Art delivery | `agent run art-delivery -- ship --execute --repo .` |
| Art review | `agent run art-intake -- pending --sheet`, then `approve --ids ... --by NAME` or `reject --ids ... --reason ...` |
| Offline art transport | `agent run art-package -- --help` |
| Rules figures | `agent run figure-generate`, `agent run figure-review` |
| Layout | `agent run layout -- plan`, then `check`; a full proof only in requested layout or build work |
| Candidate and release | `agent run build -- check`, only when the owner asks for a build |
| PDF review binding | `agent run visual-review -- bind --review FILE --push` |
| Verify and package | `agent run verify`, `agent run package` |

## Guards

`tests/test_repository_hygiene.py` fails CI if any PDF, ZIP, key, or `.env` file is tracked; the owner's reference books stay local in `references/private/`. Claude Code also loads `.claude/settings.json`, which refuses direct edits to manuscript snapshots (`.claude/hooks/protect-snapshots.sh`) and refuses a `git push` that carries such files, or that would land while "Build candidate" or "Rebuild verified delivery" is queued or running (`.claude/hooks/git-guard.sh`). In Claude Code cloud sessions, `.claude/hooks/session-start.sh` installs `requirements.lock` into `.venv` (first on PATH) and fetches the 24 Hero portraits from LFS, so the full suite runs there. Other clients follow the same rules by hand. For Claude, `/build-release` (owner-only) runs the build card.

## Specialist roles

Six role contracts live in `docs/agents/`: `publication-engineer`, `book-designer`, `publication-auditor`, `rules-illustrator`, `mechanical-assistant`, and `blind-editorial-reviewer`. The reviewer is read-only and rates proposed manuscript wording from current and proposed lines under shuffled keys, without the rationale, as in the RC528 humanizer review. Read one with `python tools/dev.py agent role NAME`; `.claude/agents/` loads the same files for Claude. Delegate to native workers when it helps, giving each its own files, or do the roles yourself in sequence.

## Missing capabilities

If a session lacks shell, Git or LFS access, or an image tool that accepts references, say exactly what is missing and use an existing route: the offline art bundle with the GitHub import workflow, or a local executor. Never paste credentials into a conversation.
