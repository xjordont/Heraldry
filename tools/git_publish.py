#!/usr/bin/env python3
"""Publish a narrowly scoped change on current, clean main without rewriting history.

Call require_clean_main before writing the publication files. Pass its returned
commit to publish_files afterwards. A refused publication keeps the files, index,
and any new local commit available for inspection and recovery.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


class PublishError(RuntimeError):
    """A required check failed; no automatic reset, pull, or rebase is attempted."""


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise PublishError(f"git {args[0]} failed: {detail}")
    return result.stdout.rstrip("\r\n")


def _changed_paths(root: Path) -> set[str]:
    paths = set()
    for args in (("diff", "--name-only", "--no-renames", "-z"),
                 ("diff", "--cached", "--name-only", "--no-renames", "-z"),
                 ("ls-files", "--others", "--exclude-standard", "-z")):
        paths.update(p for p in _git(root, *args).split("\0") if p)
    return paths


def _main_commit(root: Path) -> str:
    if _git(root, "symbolic-ref", "--quiet", "--short", "HEAD") != "main":
        raise PublishError("publication requires branch main")
    _git(root, "fetch", "origin", "refs/heads/main:refs/remotes/origin/main")
    head = _git(root, "rev-parse", "HEAD")
    if head != _git(root, "rev-parse", "refs/remotes/origin/main"):
        raise PublishError("local main differs from origin/main; inspect and sync with --ff-only before publication")
    return head


def require_clean_main(root: Path) -> str:
    """Refuse before file mutation unless main is clean and equals fetched origin/main."""
    root = Path(root).resolve()
    head = _main_commit(root)
    if _changed_paths(root):
        raise PublishError("publication requires a clean working tree and index; preserve or finish existing work first")
    return head


def find_make(root: Path) -> str:
    """Find GNU Make on PATH or the documented adjacent Windows tool installation."""
    executable = shutil.which("make")
    if executable:
        return executable
    windows_make = Path(root).resolve().parent / "tools/gnuwin32/bin/make.exe"
    if windows_make.is_file():
        return str(windows_make)
    raise PublishError("make is unavailable; install GNU Make or use the documented Windows tool path")


def run_tests(root: Path, python: str = sys.executable) -> None:
    """Run the required make test with this interpreter; raise PublishError on failure."""
    executable = str(Path(python).resolve()).replace("\\", "/")
    # Keep the interpreter quoted in the recipe, including Windows paths with spaces.
    command = [find_make(root), "test", f'PY="{executable.replace("$", "$$")}"']
    env = dict(os.environ, PYTHONUTF8="1")
    result = subprocess.run(command, cwd=root, env=env)
    if result.returncode:
        raise PublishError(f"make test failed (exit {result.returncode}); publication files are preserved")


def publish_files(root: Path, paths: list[str], message: str, base_commit: str,
                  test_runner=None) -> str:
    """Test, commit only paths, and normally push main once.

    test_runner(root) is injectable for isolated tests; production callers leave it
    unset to execute make test. Concurrent changes or a rejected push stop safely
    and retain the local work. The caller must first use require_clean_main.
    """
    root = Path(root).resolve()
    allowed = set(paths)
    if not allowed or any(not p or Path(p).is_absolute() or ".." in Path(p).parts
                          or p != Path(p).as_posix() for p in allowed):
        raise PublishError("publication paths must be explicit repository-relative file paths")

    def check_scope():
        if _main_commit(root) != base_commit:
            raise PublishError("main changed since publication started; generated files are preserved for inspection")
        unrelated = _changed_paths(root) - allowed
        if unrelated:
            raise PublishError("unrelated working or staged changes appeared; publication refused and all work is preserved")

    check_scope()
    if not _changed_paths(root):
        raise PublishError("no publication changes to commit")
    before = {p: (root / p).read_bytes() if (root / p).is_file() else None for p in allowed}
    (test_runner or run_tests)(root)
    check_scope()
    if before != {p: (root / p).read_bytes() if (root / p).is_file() else None for p in allowed}:
        raise PublishError("publication files changed during make test; inspect them and rerun publication")
    _git(root, "add", "--", *sorted(allowed))
    # --only makes the commit scope explicit even if another process stages a file.
    _git(root, "commit", "--only", "-m", message, "--", *sorted(allowed))
    commit = _git(root, "rev-parse", "HEAD")
    try:
        _git(root, "push", "origin", "HEAD:refs/heads/main")
    except PublishError as exc:
        raise PublishError(f"push refused; local commit {commit} and all files are preserved. "
                           "Inspect remote main before retrying; no pull or rebase was attempted. " + str(exc)) from exc
    return commit
