#!/usr/bin/env python3
"""Run the test suites one module per process, in parallel.

The same tests and the same pass/fail result as `python -m unittest discover` on each directory, in a fraction of
the time: the heavy modules (Typst compiles, whole-manuscript revisions) run side by side instead of one after another.
Every test writes only to its own temporary folder, so modules cannot interfere.

    python tools/run_tests.py [--jobs N] [DIR ...]      (default: tests/ and the art skill's tests/)
"""
import argparse
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = ("tests", "production/art/skill/heraldry-classic-ink-art/tests")
# Start the slowest modules first so they do not finish last (seconds measured 2026-11-02).
HEAVY = ("test_workflow", "test_art_skill", "test_delivery_sync", "test_update_manuscript", "test_text_encoding")


def run_module(directory, path):
    started = time.monotonic()
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", directory, "-p", path.name],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            env=dict(os.environ, PYTHONUTF8="1"))
    output = result.stdout + result.stderr
    ran = re.search(r"^Ran (\d+) tests?", output, re.M)
    count = int(ran.group(1)) if ran else 0
    ok = result.returncode == 0 and ran is not None and count > 0
    return {"name": f"{directory}/{path.stem}", "ok": ok, "tests": count,
            "skipped": sum(int(n) for n in re.findall(r"skipped=(\d+)", output)),
            "seconds": time.monotonic() - started, "output": output}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dirs", nargs="*", default=list(DIRS))
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    args = parser.parse_args(argv)
    modules = [(d, p) for d in args.dirs for p in sorted((ROOT / d).glob("test_*.py"))]
    if not modules:
        print("no test modules found in " + ", ".join(args.dirs))
        return 1
    rank = {name: i for i, name in enumerate(HEAVY)}
    modules.sort(key=lambda m: rank.get(m[1].stem, len(HEAVY)))
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(lambda m: run_module(*m), modules))
    failed = [r for r in results if not r["ok"]]
    for r in sorted(results, key=lambda r: r["name"]):
        print(f"{'ok  ' if r['ok'] else 'FAIL'} {r['tests']:4d} tests {r['seconds']:6.1f}s  {r['name']}"
              + (f"  (skipped {r['skipped']})" if r["skipped"] else ""))
    for r in failed:
        print(f"\n===== {r['name']} =====\n{r['output'].rstrip()}")
    total, skipped = sum(r["tests"] for r in results), sum(r["skipped"] for r in results)
    print(f"\nRan {total} tests in {len(results)} modules in {time.monotonic() - started:.1f}s")
    print(("OK" + (f" (skipped={skipped})" if skipped else "")) if not failed
          else "FAILED: " + ", ".join(r["name"] for r in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
