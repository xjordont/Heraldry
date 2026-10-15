#!/usr/bin/env python3
"""Check exact locked packages, imports, and tools without installing or building."""
import argparse
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"fonttools": "fontTools", "markdown-it-py": "markdown_it", "mdurl": "mdurl", "numpy": "numpy",
           "pillow": "PIL", "potracer": "potrace", "pymupdf": "pymupdf", "pypdf": "pypdf", "typst": "typst"}


def locked_packages(path):
    packages = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.count("==") != 1:
            raise ValueError("Every requirement must have one exact == version pin")
        name, version = line.split("==")
        key = name.lower().replace("_", "-")
        if not name or not version or key in packages:
            raise ValueError("Missing or duplicate dependency pin")
        packages[key] = version
    if not packages:
        raise ValueError("The dependency lock is empty")
    return packages


def command_path(name, root=ROOT):
    found = shutil.which(name)
    if found:
        return found
    if name == "make":
        candidate = root.parent / "tools/gnuwin32/bin/make.exe"
        if candidate.is_file():
            return str(candidate)
    if name == "bash" and os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
        if candidate.is_file():
            return str(candidate)
    return None


def inspect(root=ROOT, profile="local"):
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    add("python", sys.version_info >= (3, 12), sys.version.split()[0])
    try:
        locked = locked_packages(root / "requirements.lock")
    except (OSError, ValueError) as exc:
        add("lock", False, str(exc))
        locked = {}
    for name, expected in locked.items():
        try:
            actual = importlib.metadata.version(name)
            module = MODULES.get(name)
            if module is None:
                raise ValueError("Add this distribution's import name to MODULES")
            importlib.import_module(module)
            add(name, actual == expected, f"installed {actual}; required {expected}; import {module}")
        except (ImportError, ValueError, OSError) as exc:
            add(name, False, str(exc))
    pip = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    add("pip_check", pip.returncode == 0, (pip.stdout + pip.stderr).strip()[-1000:])
    names = ["git"]
    if profile == "local":
        names += ["make", "bash"]
    elif profile == "publish":
        names += ["make", "bash", "gh", "mkdir", "cp", "rm", "cut", "sort", "sha256sum"]
    for name in names:
        path = command_path(name, root)
        add("command_" + name, path is not None, path or "not found on PATH")
    git = command_path("git", root)
    if git:
        lfs = subprocess.run([git, "lfs", "version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        add("git_lfs", lfs.returncode == 0, lfs.stdout.strip() if lfs.returncode == 0 else "git lfs version failed")
    else:
        add("git_lfs", False, "Git is unavailable")
    return {"status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
            "profile": profile, "python": sys.executable, "checks": checks,
            "scope": "Installed dependencies and executable availability; no book build, credentials, or physical proof"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    profiles = parser.add_mutually_exclusive_group()
    profiles.add_argument("--ci", action="store_true", help="repository checks need Python, Git, and LFS")
    profiles.add_argument("--publish", action="store_true", help="also require the publishing runner's shell tools and gh")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = inspect(profile="publish" if args.publish else "ci" if args.ci else "local")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for check in result["checks"]:
        print(f"{check['status']}: {check['check']}: {check['detail']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
