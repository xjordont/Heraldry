#!/usr/bin/env bash
# PreToolUse hook: manuscript snapshots in source/ are immutable (AGENTS.md, "Hard rules").
# Blocks Edit, Write, MultiEdit, and NotebookEdit on source/Heraldry_RC*.md. New RCs come only
# from tools/revise_manuscript.py or `python tools/dev.py manuscript`, which run through Bash.
# Uses bash and grep only, so it also runs under Git Bash on Windows (no jq or Python needed).
input=$(cat)
if printf '%s' "$input" | grep -Eq '"(file_path|notebook_path)"[[:space:]]*:[[:space:]]*"([^"]*[/\\])?source[/\\]+Heraldry_RC[0-9]+\.md"'; then
  echo "Blocked: manuscript snapshots in source/ are immutable. Change manuscript text only with the owner's approval, through tools/revise_manuscript.py (exact patches) or 'python tools/dev.py manuscript' (a full owner upload); see docs/WORKFLOW.md." >&2
  exit 2
fi
exit 0
