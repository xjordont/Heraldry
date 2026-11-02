#!/usr/bin/env bash
# PreToolUse hook (Bash): enforces two AGENTS.md rules before Claude pushes to main.
#   1. Files: never commit built PDFs, ZIPs, or secrets. Every commit about to be pushed is checked, so a
#      file added by `git add -A`, `git commit -a`, or a force-add is caught before it leaves the machine.
#      No exceptions: the owner's reference books stay local in references/private/ (ignored by Git).
#   2. Builds: don't push while "Build candidate" or "Rebuild verified delivery" is queued or running,
#      because the release's publish step aborts if main moves.
# Bash, git, grep, and curl only, so it also runs under Git Bash on Windows. Network or API trouble never
# blocks a push (the build check is skipped with a note); set HERALDRY_ALLOW_PUSH_DURING_BUILD=1 to override it.
input=$(cat)
command=$(printf '%s' "$input" | grep -o '"command"[[:space:]]*:[[:space:]]*"\([^"\\]\|\\.\)*"' | head -n 1)
printf '%s' "$command" | grep -Eq 'git([[:space:]]+-[^[:space:]]+)*[[:space:]]+push' || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

# 1. Files in the outgoing commits (added, modified, or renamed in any of them, even if deleted later).
upstream=$(git rev-parse --verify -q origin/main) || upstream=""
if [ -n "$upstream" ]; then
  bad=$(git log --name-only --diff-filter=AMR --format= "$upstream..HEAD" 2>/dev/null | sort -u \
        | grep -Ei '\.(pdf|zip|pem|key|p12|pfx)$|(^|/)\.env(\.[^/]*)?$|(^|/)id_(rsa|ed25519)$' \
        | grep -Ev '(^|/)\.env\.example$')
  if [ -n "$bad" ]; then
    {
      echo "Blocked: the commits about to be pushed contain files that must never be committed (AGENTS.md, \"Files\"):"
      printf '%s\n' "$bad" | sed 's/^/  /'
      echo "Remove them from those unpushed commits (for example, git rm --cached and amend, or reset the unpushed commits and recommit), then push again. PDFs and ZIPs go to GitHub Releases (docs/LARGE_FILES.md)."
    } >&2
    exit 2
  fi
fi

# 2. A publishing build on GitHub.
[ "${HERALDRY_ALLOW_PUSH_DURING_BUILD:-}" = "1" ] && exit 0
printf '%s' "$command" | grep -q 'HERALDRY_ALLOW_PUSH_DURING_BUILD=1' && exit 0   # inline: VAR=1 git push ...
repo=$(git remote get-url origin 2>/dev/null | sed -E 's#\.git$##; s#^.*github\.com[:/]+##; s#^.*/git/##')
case "$repo" in */*) ;; *) exit 0 ;; esac
token="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
for status in in_progress queued waiting; do
  if [ -n "$token" ]; then
    body=$(curl -sS -m 8 -H "Authorization: Bearer $token" "https://api.github.com/repos/$repo/actions/runs?status=$status&branch=main&per_page=20" 2>/dev/null)
  else
    body=$(curl -sS -m 8 "https://api.github.com/repos/$repo/actions/runs?status=$status&branch=main&per_page=20" 2>/dev/null)
  fi
  if ! printf '%s' "$body" | grep -q '"total_count"'; then
    echo "Note: could not ask GitHub whether a build is running (private repository without GH_TOKEN, or no network); push allowed." >&2
    exit 0
  fi
  running=$(printf '%s' "$body" | grep -oE '"name"[[:space:]]*:[[:space:]]*"(Build candidate|Rebuild verified delivery)"' | sed 's/.*: *"//; s/"$//' | sort -u)
  if [ -n "$running" ]; then
    echo "Blocked: a publishing build is $status on main ($(printf '%s' "$running" | paste -sd, -)). AGENTS.md: wait for it to finish before pushing, because its publish step aborts if main moves. Commit locally and push afterwards; set HERALDRY_ALLOW_PUSH_DURING_BUILD=1 only if the owner says to push anyway." >&2
    exit 2
  fi
done
exit 0
