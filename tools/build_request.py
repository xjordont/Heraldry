#!/usr/bin/env python3
"""Request and follow an unattended candidate build (standard library only; shared by all repository agents).

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

from git_publish import PublishError, publish_files, require_clean_main

ROOT = Path(__file__).resolve().parents[1]
REQUEST = "production/build-request.json"
STATUS = "production/BUILD_STATUS.json"


def git(*a, check=True):
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(a)} failed: {(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


def problems():
    """Reasons main is not ready for a candidate build (empty list when ready)."""
    out = []
    try:
        require_clean_main(ROOT)
    except PublishError as exc:
        out.append(str(exc))
    sels = json.loads((ROOT / "production/art/SELECTIONS.json").read_text(encoding="utf-8"))
    not_ok = sorted(k for k, v in sels.items() if v.get("status") not in ("approved", "anchor-approved"))
    if not_ok:
        out.append(f"{len(not_ok)} illustrations are not approved: {', '.join(not_ok[:6])}")
    catalogue = json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text(encoding="utf-8"))["entries"]
    # An approval bound to an older catalogue spec would be left out of the book, and the build's
    # artwork step (tools/check_art.py) fails on it: catch it here in seconds, not after a CI run.
    spec = {e["id"]: e["spec_sha256"] for e in catalogue}
    stale = sorted(k for k, v in sels.items() if v.get("status") in ("approved", "anchor-approved", "auto-selected")
                   and k in spec and v.get("spec_sha256") != spec[k])
    if stale:
        out.append(f"{len(stale)} approved illustrations are bound to an outdated catalogue spec "
                   f"(re-bind or redo them): {', '.join(stale[:6])}")
    queue = json.loads((ROOT / "production/art/gpt/QUEUE.json").read_text(encoding="utf-8"))
    # Section-end tailpieces are optional fill (owner 2026-10-30): the book leaves their space white
    # until each is approved, so a pending tailpiece never blocks a build. Every other item does.
    optional = {e["id"] for e in catalogue if e.get("end_art")}
    required = [i for i in queue.get("items", []) if i.get("id") not in optional]
    if required or (queue.get("count") and not queue.get("items")):
        out.append(f"the art queue still holds {len(required) or queue['count']} required items")
    r = subprocess.run([sys.executable, "tools/preflight.py"], cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
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
    try:
        base = require_clean_main(ROOT)
        now = datetime.datetime.now(datetime.timezone.utc)
        rid = now.strftime("%Y%m%dT%H%M%SZ")
        (ROOT / REQUEST).write_text(json.dumps({"request_id": rid, "requested_at": now.isoformat(timespec="seconds"),
                                                "requested_by": getattr(a, "requested_by", "repository operator"), "base_commit": base}, indent=1) + "\n",
                                    encoding="utf-8")
        commit = publish_files(ROOT, [REQUEST], f"build: request candidate build {rid}", base)
    except PublishError as exc:
        print("REFUSED: " + str(exc))
        return 2
    print(f"request {rid} pushed at {commit}")
    return 0


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
    request = sub.add_parser("request")
    request.add_argument("--requested-by", default="repository operator", help="actual requesting client or operator, recorded in provenance")
    request.set_defaults(f=cmd_request)
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
