# Claude Code setup and continuation

This is an existing, built publication project. Select `xjordont/Heraldry` and `main` in Claude Code cloud; read `CLAUDE.md`, `docs/WORKFLOW.md`, `production/STATE.md` and the requested change. Do not recreate the initial kit or start a task branch. The old Claude build branch is a historical checkpoint.

The active manuscript comes from `source/versions.json`. Every approved manuscript text-patch batch creates the next RC snapshot using `tools/revise_manuscript.py`. Earlier snapshots are immutable; artwork, figures and layout do not increment RC. `MASTER_PROMPT.md` supplies the standing production/design contract.

Start with `python3 tools/preflight.py --baseline --report production/preflight.json` and `make test`. Install pinned dependencies if needed, then use `make clean all verify package`. Read `BUILD.md` for outputs and the workflow for exact patch promotion. Do not claim completion until current evidence and the visual review support it.

Verify runtime model availability. `.claude/settings.json` selects configured Opus/medium; native agent definitions select configured Sonnet for substantive work, with at most two workers concurrently. Report any runtime model substitution. Use native workers.

Atmospheric artwork is generated in ChatGPT Work and supplied in `assets/art/incoming/` using the manifest IDs. Claude integrates and reviews those original masters; no external image API runner is part of this project. Continue independent work if a particular asset needs repair.

Optional visual evidence is limited to the selected reference pages in `references/reference_manifest.json`; written specifications are sufficient to continue. Keep commercial PDFs separate from publication assets and releases. Read `references/README.md` for optional local extraction.

The printing target is borderless portrait US Letter inkjet: cream and white variants with identical pagination, finished cover sheets, calibration page and instructions. File checks cannot prove the user's actual printer, driver, paper or binding. Physical proof remains NOT TESTED until actual printed sheets are inspected. Commercial cover wraps and PDF/X are additional scope.

Cloud settings and network policies apply independently of repository instructions. If the platform blocks main writes, model access or a dependency source, record the actual restriction and preserve work; do not override it or invent a successful push. Prefer a permitted package registry for blocked dependency downloads. Never expose credentials.
