#!/usr/bin/env python3
"""Request and follow an unattended candidate build (standard library only; runs on the owner's Windows PC under Codex).

The build itself runs on GitHub Actions (.github/workflows/build-candidate.yml), which starts when this tool pushes
production/build-request.json to main. No GitHub token, API call or local PDF build is involved: git is the only channel.
The workflow answers by committing production/BUILD_STATUS.json, which `wait` reads.

    python tools/build_request.py check                    # is main ready to build? (read-only)
    python tools/build_request.py request                  # check, write and push the request; prints the request id
    python tools/build_request.py wait --id ID [--timeout-min 100] [--interval-sec 240]
    python tools/build_request.py release-wait --ledger-commit SHA [--timeout-min 60] [--interval-sec 240]   # after the review is bound and pushed

Exit codes: 0 ok / candidate ready, 2 not ready or build failed, 3 timed out.
"""
import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = "production/build-request.json"
STATUS = "production/BUILD_STATUS.json"


def git(*a, check=True):
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(a)} failed: {(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


def problems():
    """Reasons main is not ready for a candidate build (empty list when ready)."""
    out = []
    if git("rev-parse", "--abbrev-ref", "HEAD") != "main":
        out.append("not on main")
    if git("status", "--porcelain"):
        out.append("working tree is not clean")
    git("fetch", "origin", "main")
    if git("rev-parse", "HEAD") != git("rev-parse", "origin/main"):
        out.append("local main differs from origin/main (pull --ff-only first, or ship unsent work)")
    sels = json.loads((ROOT / "production/art/SELECTIONS.json").read_text(encoding="utf-8"))
    not_ok = sorted(k for k, v in sels.items() if v.get("status") not in ("approved", "anchor-approved"))
    if not_ok:
        out.append(f"{len(not_ok)} illustrations are not approved: {', '.join(not_ok[:6])}")
    queue = json.loads((ROOT / "production/art/gpt/QUEUE.json").read_text(encoding="utf-8"))
    if queue.get("count"):
        out.append(f"the art queue still holds {queue['count']} items")
    r = subprocess.run([sys.executable, "tools/preflight.py"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        out.append("tools/preflight.py failed: " + (r.stdout + r.stderr).strip().splitlines()[-1][:200])
    return out


def cmd_check(_):
    p = problems()
    print("READY: main can be built" if not p else "NOT READY:\n- " + "\n- ".join(p))
    return 0 if not p else 2


def cmd_request(a):
    p = problems()
    if p:
        print("NOT READY:\n- " + "\n- ".join(p))
        return 2
    now = datetime.datetime.now(datetime.timezone.utc)
    rid = now.strftime("%Y%m%dT%H%M%SZ")
    (ROOT / REQUEST).write_text(json.dumps({"request_id": rid, "requested_at": now.isoformat(timespec="seconds"),
                                            "requested_by": "codex", "base_commit": git("rev-parse", "HEAD")}, indent=1) + "\n")
    git("add", REQUEST)
    git("commit", "-m", f"build: request candidate build {rid}")
    for wait in (0, 3, 6, 12):
        time.sleep(wait)
        r = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"request {rid} pushed at {git('rev-parse', 'HEAD')}")
            return 0
        git("pull", "--rebase", "origin", "main", check=False)
    print("push failed: " + r.stderr.strip())
    return 2


def read_status():
    r = subprocess.run(["git", "show", f"origin/main:{STATUS}"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def cmd_wait(a):
    end = time.time() + a.timeout_min * 60
    while time.time() < end:
        git("fetch", "origin", "main")
        s = read_status()
        if s and s.get("request_id") == a.id:
            print(json.dumps(s, indent=1))
            return 0 if s.get("result") == "CANDIDATE_READY" else 2
        print(f"waiting for the build of request {a.id} ...", flush=True)
        time.sleep(a.interval_sec)
    print(f"timed out after {a.timeout_min} minutes without a status for request {a.id}")
    return 3


def cmd_release_wait(a):
    end = time.time() + a.timeout_min * 60
    while time.time() < end:
        git("fetch", "origin", "main")
        r = subprocess.run(["git", "show", "origin/main:production/RELEASE_RESULT.json"], cwd=ROOT, capture_output=True, text=True)
        s = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
        if s and s.get("ledger_commit") == a.ledger_commit:
            print(json.dumps(s, indent=1))
            return 0 if s.get("result") == "RELEASED" else 2
        print(f"waiting for the release of ledger commit {a.ledger_commit[:10]} ...", flush=True)
        time.sleep(a.interval_sec)
    print("timed out without a release result")
    return 3


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(f=cmd_check)
    sub.add_parser("request").set_defaults(f=cmd_request)
    w = sub.add_parser("wait")
    w.add_argument("--id", required=True)
    w.add_argument("--timeout-min", type=int, default=100)
    w.add_argument("--interval-sec", type=int, default=240)
    w.set_defaults(f=cmd_wait)
    rw = sub.add_parser("release-wait")
    rw.add_argument("--ledger-commit", required=True)
    rw.add_argument("--timeout-min", type=int, default=60)
    rw.add_argument("--interval-sec", type=int, default=240)
    rw.set_defaults(f=cmd_release_wait)
    a = ap.parse_args()
    sys.exit(a.f(a))


if __name__ == "__main__":
    main()
