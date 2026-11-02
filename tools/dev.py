#!/usr/bin/env python3
"""Local checks, status, reviewed manuscript updates, layout proofs, and shared agent workflows."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def select_python(root=ROOT, override=None):
    if override:
        candidate = Path(shutil.which(override) or override).expanduser().resolve()
        if not candidate.is_file():
            raise ValueError("The selected Python executable does not exist")
        return str(candidate)
    candidates = [root / ".venv/Scripts/python.exe", root / ".venv/bin/python", root.parent / "art-venv/Scripts/python.exe"]
    return str(next((p for p in candidates if p.is_file()), Path(sys.executable)))


def run(python, *args):
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([python, *args], cwd=ROOT, env=env).returncode


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise ValueError(f"git {args[0]} failed")
    return result.stdout.strip()


def status():
    """Report local state and last-release evidence without implying it is rebuilt."""
    print("Branch: " + git("branch", "--show-current"))
    print("HEAD: " + git("rev-parse", "--short", "HEAD"))
    print("Local/remote differences (local tracking ref): " + git("rev-list", "--left-right", "--count", "HEAD...origin/main"))
    changes = git("status", "--short")
    print("Working tree: " + ("clean" if not changes else "modified\n" + changes))
    versions = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    print(f"Manuscript: RC{versions['current']}")
    result = json.loads((ROOT / "production/RELEASE_RESULT.json").read_text(encoding="utf-8"))
    print(f"Last requested release: {result.get('tag', '(none)')} ({result.get('result', 'unknown')})")
    print("Release source: " + result.get("ledger_commit", "unknown"))
    print("Build evidence describes that release; this command does not certify current input/PDF equivalence.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("doctor", "check", "status", "manuscript", "layout", "agent"))
    parser.add_argument("--python", help="override automatic .venv / Heraldry environment selection")
    parser.add_argument("--base", default="origin/main", help="snapshot history reference for check (local tracking ref)")
    # Delegate optional commands' help/options to their selected-runtime tools.
    argv = sys.argv[1:]
    delegated = next((name for name in argv if name in {"manuscript", "layout", "agent"}), None)
    if delegated:
        position = argv.index(delegated)
        args = parser.parse_args(argv[:position + 1])
        delegated_args = argv[position + 1:]
    else:
        args = parser.parse_args(argv)
    try:
        python = select_python(override=args.python)
        print("Python: " + python, flush=True)
        if args.command in {"manuscript", "layout", "agent"}:
            script = {"manuscript": "tools/update_manuscript.py", "layout": "tools/layout_workflow.py",
                      "agent": "tools/agent_workflow.py"}[args.command]
            return run(python, script, *delegated_args)
        if args.command == "status":
            return status()
        report = ROOT / "build/checks"
        if run(python, "tools/check_dependencies.py", "--report", str(report / "dependencies.json")):
            return 1
        if args.command == "doctor":
            return 0
        if run(python, "tools/update_readme.py", "--write"):
            return 1
        if run(python, "tools/preflight.py", "--baseline", "--report", str(report / "preflight.json")):
            return 1
        if run(python, "tools/check_history.py", "--base", args.base):
            return 1
        if git("diff", "--check"):
            return 1
        from git_publish import PublishError, run_tests
        try:
            run_tests(ROOT, python=python)
        except PublishError as exc:
            print("FAILED: " + str(exc), file=sys.stderr)
            return 1
        print("PASS: README refreshed; dependencies, contracts, snapshot history, whitespace, and make test. No publication build.")
        return 0
    except (ValueError, OSError) as exc:
        print("FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
