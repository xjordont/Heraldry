#!/usr/bin/env python3
"""Write production/RELEASE_RESULT.json after the release workflow ran for a visual-ledger push (called by rebuild-delivery.yml)."""
import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = "production/RELEASE_RESULT.json"


def evaluate(release, ledger_commit, job_status, failed_step=""):
    """A published release is complete only when all preceding workflow steps passed."""
    ok = job_status == "success" and not failed_step and release.get("source_commit") == ledger_commit
    if ok:
        return "RELEASED", "released and verified"
    if failed_step:
        return "FAILED", f"step failed: {failed_step}"
    if job_status != "success":
        return "FAILED", f"workflow did not complete successfully: {job_status}"
    return "FAILED", "no release was published for this commit"


def publish_result(root=ROOT, attempts=4, retry_delay=5):
    """Push a result-only commit, preserving the checkout and all newer main changes.

    A failed verification-ledger push can leave a local commit based on stale main.
    Never rebase or push that commit: construct the result atop freshly fetched main
    using a temporary index, and retry from a new parent if another writer wins.
    """
    root = Path(root)
    payload = (root / RESULT).read_bytes()

    def git(*args, env=None, data=None):
        r = subprocess.run(["git", *args], cwd=root, env=env, input=data, capture_output=True)
        if r.returncode:
            raise RuntimeError(f"git {args[0]} failed while recording the release result")
        return r.stdout.decode("utf-8").strip()

    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(attempts):
        git("fetch", "origin", "main")
        parent = git("rev-parse", "refs/remotes/origin/main")
        with tempfile.TemporaryDirectory(prefix="heraldry-release-result-") as tmp:
            env = os.environ.copy()
            env["GIT_INDEX_FILE"] = str(Path(tmp) / "index")
            git("read-tree", parent, env=env)
            blob = git("hash-object", "-w", "--stdin", data=payload)
            git("update-index", "--add", "--cacheinfo", f"100644,{blob},{RESULT}", env=env)
            tree = git("write-tree", env=env)
        if tree == git("rev-parse", f"{parent}^{{tree}}"):
            return parent
        commit = git("commit-tree", tree, "-p", parent, data=b"Record release workflow result\n")
        pushed = subprocess.run(["git", "push", "origin", f"{commit}:refs/heads/main"], cwd=root, capture_output=True)
        if pushed.returncode == 0:
            return commit
        error = pushed.stderr.decode("utf-8", errors="replace").lower()
        if not any(reason in error for reason in ("non-fast-forward", "fetch first", "failed to update ref")):
            raise RuntimeError("git push failed while recording the release result; not a main-update race")
        git("fetch", "origin", "main")
        if git("rev-parse", "refs/remotes/origin/main") == parent:
            raise RuntimeError("git push rejected the release result, but remote main did not advance")
        if attempt + 1 == attempts:
            raise RuntimeError(f"could not record the release result after {attempts} main-update races")
        time.sleep(retry_delay * (attempt + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger-commit", required=True)
    ap.add_argument("--job-status", required=True, choices=("success", "failure", "cancelled", "skipped"))
    ap.add_argument("--failed-step", default="")
    ap.add_argument("--run-url", default="")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    rel = ROOT / "dist/RELEASE.json"
    r = json.loads(rel.read_text()) if rel.is_file() else {}
    result, note = evaluate(r, a.ledger_commit, a.job_status, a.failed_step)
    ok = result == "RELEASED"
    out = {"ledger_commit": a.ledger_commit, "result": result, "note": note,
           "release_url": r.get("url", "") if ok else "", "tag": r.get("tag", "") if ok else "", "run_url": a.run_url,
           "physical_print": "NOT TESTED"}
    (ROOT / RESULT).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("result", "note")}))
    if a.push:
        print("result recorded at " + publish_result())


if __name__ == "__main__":
    main()
