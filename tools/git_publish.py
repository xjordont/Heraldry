#!/usr/bin/env python3
"""Publish a narrowly scoped change on current, clean main without rewriting history.

Call require_clean_main before writing the publication files. Pass its returned
commit to publish_files afterwards. A refused publication keeps the files, index,
and any new local commit available for inspection and recovery.
"""
from __future__ import annotations

from pathlib import Path
import subprocess


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


def require_current_main(root: Path, allowed_changes=()) -> str:
    """Require fetched current main; optionally admit explicitly bound companion edits."""
    root = Path(root).resolve()
    head = _main_commit(root)
    if _changed_paths(root) - set(allowed_changes):
        raise PublishError("publication requires a clean working tree and index outside its allowed companion files; preserve or finish existing work first")
    return head


def require_clean_main(root: Path) -> str:
    """Refuse before file mutation unless main is clean and equals fetched origin/main."""
    return require_current_main(root)


def publish_files(root: Path, paths: list[str], message: str, base_commit: str,
                  test_runner=None) -> str:
    """Commit only paths, and normally push main once.

    The callers publish one JSON file (a build request or a review ledger) on a clean main
    that CI has already tested, and the build it starts runs the suite before building, so
    no local test run happens here unless test_runner(root) is given. Concurrent changes or a
    rejected push stop safely and retain the local work. The caller must first use
    require_clean_main.
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
    if test_runner:
        test_runner(root)
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
