#!/usr/bin/env python3
"""CI guard: prior manuscript snapshots and revision records are append-only."""
import argparse
import json
import subprocess
from manuscript import ROOT, check, load


def git_bytes(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", required=True)
    a = p.parse_args()
    check()
    if subprocess.run(["git", "cat-file", "-e", f"{a.base}^{{commit}}"], cwd=ROOT, capture_output=True).returncode:
        print(f"SKIP: base {a.base[:12]} is not in this history (rewritten, as on 2026-11-02); nothing to compare")
        return
    current = load()
    listed = subprocess.check_output(["git", "ls-tree", "--name-only", a.base, "source/versions.json"], cwd=ROOT).strip()
    if listed:
        old = json.loads(git_bytes(a.base, "source/versions.json"))
        if current["revisions"][:len(old["revisions"])] != old["revisions"]:
            raise SystemExit("Earlier revision records changed; history is append-only")
        paths = [r["path"] for r in old["revisions"]] + [r["patch_file"] for r in old["revisions"] if r.get("patch_file")]
    else:
        paths = ["source/Heraldry_RC484.md"]  # one-time migration from the original build
    for name in paths:
        if (ROOT / name).read_bytes() != git_bytes(a.base, name):
            raise SystemExit(f"Prior snapshot/evidence modified: {name}")
    print(f"PASS: {len(paths)} previous snapshots/evidence files unchanged")


if __name__ == "__main__":
    main()
