# Claude Code setup and continuation

This is an existing, built publication project. Select `xjordont/Heraldry` and `main` in Claude Code cloud; read `CLAUDE.md`, `docs/WORKFLOW.md`, `production/STATE.md` and the requested change. Do not recreate the initial kit or start a task branch. The old Claude build branch is a historical checkpoint.

The active manuscript comes from `source/versions.json`. Every approved manuscript text-patch batch creates the next RC snapshot using `tools/revise_manuscript.py`. Earlier snapshots are immutable; artwork, figures and layout do not increment RC. `MASTER_PROMPT.md` supplies the standing production/design contract.

Start with `python3 tools/preflight.py --baseline --report production/preflight.json` and `make test`. Install pinned dependencies if needed, then use `make clean all verify package`. Read `BUILD.md` for outputs and the workflow for exact patch promotion. Do not claim completion until current evidence and the visual review support it.

Verify the live account's model availability, remaining Claude credit, expiry and paid-overage controls. The configured $100 ceiling is the project boundary; do not assume each new iteration renews it. `.claude/settings.json` selects configured Opus/medium, native agent definitions select configured Sonnet for substantive work, and at most two workers run concurrently. Report any runtime model substitution. Do not launch separately billed nested model workers.

No external paid image calls are authorized by default. Supply original approved assets in `assets/art/incoming/` using the IDs in `production/art/ART_MANIFEST.json`, or explicitly authorize/configure a service and budget. Credentials alone do not authorize spend. Atmospheric art remains BLOCKED until supplied; continue independent work and preserve the art-light edition.

Optional visual evidence is limited to the selected reference pages in `references/reference_manifest.json`; written specifications are sufficient to continue. Keep commercial PDFs separate from publication assets and releases. Read `references/README.md` for optional local extraction.

The printing target is borderless portrait US Letter inkjet: cream and white variants with identical pagination, finished cover sheets, calibration page and instructions. File checks cannot prove the user's actual printer, driver, paper or binding. Physical proof remains NOT TESTED until actual printed sheets are inspected. Commercial cover wraps and PDF/X are additional scope.

Cloud settings and network policies apply independently of repository instructions. If the platform blocks main writes, model access or a dependency source, record the actual restriction and preserve work; do not override it or invent a successful push. Prefer a permitted package registry for blocked dependency downloads. Never expose credentials.
