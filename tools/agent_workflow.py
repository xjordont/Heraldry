#!/usr/bin/env python3
"""Shared workflow discovery and execution for Claude Code, Codex, and ChatGPT Work.

This front door delegates to existing tools without changing their checks, scope,
credentials, approval requirements, or exit codes. It grants no platform access.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = {"claude-code", "codex", "chatgpt-work"}


def repository_file(root, value, prefixes):
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Workflow paths must be repository-relative")
    resolved = (root / path).resolve()
    relative = resolved.relative_to(root.resolve()).as_posix()
    if not any(relative.startswith(prefix) for prefix in prefixes) or not resolved.is_file():
        raise ValueError("Missing or unsupported workflow path: " + value)
    return resolved


def catalog(root=ROOT):
    data = json.loads((root / "config/agent_workflows.json").read_text(encoding="utf-8"))
    if data.get("schema") != 1 or set(data.get("clients", [])) != CLIENTS:
        raise ValueError("Shared workflows must support all three clients")
    roles = data["roles"]
    if len(roles) != 5 or len({role["name"] for role in roles}) != len(roles):
        raise ValueError("Expected five distinct shared specialist roles")
    for role in roles:
        repository_file(root, role["instructions"], ("docs/agents/",))
        adapter = repository_file(root, role["claude_adapter"], (".claude/agents/",))
        if role["instructions"] not in adapter.read_text(encoding="utf-8"):
            raise ValueError("Claude adapter does not load the shared role: " + role["name"])
    if not data["workflows"]:
        raise ValueError("Shared workflow catalog is empty")
    for name, workflow in data["workflows"].items():
        script = repository_file(root, workflow["script"], ("tools/", "figures/src/", "production/art/skill/heraldry-classic-ink-art/scripts/"))
        if script.suffix != ".py" or not workflow.get("description", "").strip():
            raise ValueError("Invalid workflow definition: " + name)
    return data


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="show shared roles and workflow commands")
    sub.add_parser("check", help="validate shared role and workflow wiring, without mutation")
    role = sub.add_parser("role", help="read a portable specialist role")
    role.add_argument("name")
    run = sub.add_parser("run", help="delegate to an existing workflow using this Python environment")
    run.add_argument("workflow")
    run.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        data = catalog(root)
        if args.command == "check":
            print(f"PASS: {len(data['roles'])} shared roles and {len(data['workflows'])} workflows; identical access for all three clients.")
            print("Runtime tools, native delegation, image generation, network, and Git credentials require availability in the current session.")
        elif args.command == "list":
            print("Clients: " + ", ".join(data["clients"]))
            print("Roles: " + ", ".join(role["name"] for role in data["roles"]))
            for name, workflow in data["workflows"].items():
                print(f"{name}: {workflow['description']} [{workflow['script']}]")
        elif args.command == "role":
            match = next((role for role in data["roles"] if role["name"] == args.name), None)
            if match is None:
                raise ValueError("Unknown specialist role: " + args.name)
            print((root / match["instructions"]).read_text(encoding="utf-8"), end="")
        else:
            workflow = data["workflows"].get(args.workflow)
            if workflow is None:
                raise ValueError("Unknown workflow: " + args.workflow)
            forwarded = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
            return subprocess.run([sys.executable, str(root / workflow["script"]), *forwarded],
                                  cwd=root, env=dict(os.environ, PYTHONUTF8="1")).returncode
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print("FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
