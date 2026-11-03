#!/usr/bin/env bash
# SessionStart hook, Claude Code cloud sessions only (local sessions exit at once). A fresh cloud checkout has
# neither the locked Python packages nor the Hero portraits (Git LFS pointers), so the test suite fails there.
#   1. Installs requirements.lock into .venv (ignored by Git; tools/dev.py already prefers it), skipped when the
#      lock and this script are unchanged since the last good install.
#   2. Puts .venv first on PATH for the session's Bash commands, so python, python3, and make find the packages.
#   3. Fetches the 24 Hero portraits named in typst/heroes/basic-heroes.json (about 8 MB), the same list
#      .github/workflows/repository-checks.yml pulls; files already fetched are skipped.
# A failure ends the hook with an error the session shows; the next session retries.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}"

hashes=.venv/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"   # removed first, so a failed install runs again next time
  python3 -m venv .venv
  .venv/bin/python -m pip install -q --disable-pip-version-check -r requirements.lock >&2
  sha256sum .claude/hooks/session-start.sh requirements.lock > "$hashes"
fi

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  printf 'export VIRTUAL_ENV="%s/.venv"\nexport PATH="%s/.venv/bin:$PATH"\n' "$PWD" "$PWD" >> "$CLAUDE_ENV_FILE"
fi

portraits=$(.venv/bin/python -c "import json; d=json.load(open('typst/heroes/basic-heroes.json')); h=d if isinstance(d, list) else d.get('heroes', d); print(','.join(sorted({'assets/art/ink/' + x['art'] + '.png' for x in h if x.get('art')})))")
git lfs pull --include="$portraits" --exclude="" >&2

echo "Cloud setup: requirements.lock is installed in .venv (first on PATH), and the Hero portraits are fetched."
