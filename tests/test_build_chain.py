import json, sys, tempfile, unittest
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_status  # noqa: E402
from qa_contract import MANDATORY_CHECKS  # noqa: E402


def verification_status(*failed):
    return {
        "checks": {name: "FAIL" if name in failed else "PASS" for name in MANDATORY_CHECKS},
        "mandatory_failed": list(failed),
        "release_gate": "FAIL" if failed else "PASS",
    }


def workflow(name):
    return (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")


def step_with_id(text, step_id):
    for step in re.split(r"(?m)^      - ", text)[1:]:
        if re.search(rf"(?m)^        id: {re.escape(step_id)}$", step):
            return step
    raise AssertionError(f"workflow step {step_id!r} not found")


class BuildChain(unittest.TestCase):
    def test_visual_review_alone_makes_a_candidate(self):
        r, failed, _ = build_status.evaluate(verification_status("visual_review_currency"), "")
        self.assertEqual((r, failed), ("CANDIDATE_READY", ["visual_review_currency"]))

    def test_any_other_failure_or_failed_step_fails(self):
        self.assertEqual(build_status.evaluate(verification_status("visual_review_currency", "one_page_keeps"), "")[0], "FAILED")
        self.assertEqual(build_status.evaluate(verification_status(), "tests and clean build")[0], "FAILED")
        self.assertEqual(build_status.evaluate(None, "")[0], "FAILED")

    def test_workflows_wired(self):
        cand = workflow("build-candidate.yml")
        rel = workflow("rebuild-delivery.yml")
        self.assertIn("production/build-request.json", cand)
        self.assertIn("--prerelease", cand)
        self.assertIn("production/qa/visual-review.json", rel)
        self.assertIn("tools/review_aids.py", cand)
        self.assertIn("tools/release_result.py", rel)
        for wf in (cand, rel):
            self.assertIn("assets/art/cover/front.png", wf, "the cover is an LFS file the build places")

    def test_candidate_publication_requires_fresh_automated_verification(self):
        cand = workflow("build-candidate.yml")
        verify = step_with_id(cand, "verify")
        self.assertLess(verify.index("rm -f production/qa/STATUS.json"), verify.index("python tools/verify.py"))
        self.assertIn("continue-on-error: true", verify, "pending visual review may fail verify")
        gate = step_with_id(cand, "gate")
        self.assertIn("python tools/build_status.py --check-candidate", gate)
        self.assertNotIn("continue-on-error", gate)
        for step_id in ("aids", "release"):
            self.assertIn("if: steps.gate.outcome == 'success'", step_with_id(cand, step_id))
        self.assertLess(cand.index("id: verify"), cand.index("id: gate"))
        self.assertLess(cand.index("id: gate"), cand.index("id: release"))
        self.assertIn("steps.gate.outcome != 'success'", cand, "failure/skipping cannot record READY")
        self.assertIn("steps.release.outcome != 'success'", cand, "missing candidate publication is a failure")

    def test_repository_checks_cover_windows_and_linux_without_building(self):
        checks = workflow("repository-checks.yml")
        self.assertIn("os: [ubuntu-latest, windows-latest]", checks)
        self.assertIn("runs-on: ${{ matrix.os }}", checks)
        self.assertIn("fail-fast: false", checks)
        self.assertIn("python tools/check_dependencies.py --ci", checks)
        self.assertIn("python tools/run_tests.py", checks)
        self.assertNotRegex(checks, r"(?m)^\s+run:.*\b(make|build_book\.py|verify\.py)\b")
        for name in ("repository-checks.yml", "build-candidate.yml", "rebuild-delivery.yml"):
            text = workflow(name)
            self.assertIn("cache: pip", text)
            self.assertIn("cache-dependency-path: requirements.lock", text)
            self.assertIn("PYTHONUTF8: '1'", text)
        for name in ("build-candidate.yml", "rebuild-delivery.yml"):
            self.assertIn("make PY=python test clean all", workflow(name))
            self.assertIn("python tools/check_dependencies.py --publish", workflow(name))

    def test_only_superseded_checks_are_cancelled_and_publication_is_serialized(self):
        groups = []
        for name in ("build-candidate.yml", "rebuild-delivery.yml"):
            text = workflow(name)
            concurrency = re.search(r"(?m)^concurrency:\n  group: ([^\n]+)\n  cancel-in-progress: ([^\n]+)", text)
            self.assertIsNotNone(concurrency, name)
            groups.append(concurrency.group(1))
            self.assertEqual(concurrency.group(2), "false", name)
        self.assertEqual(groups[0], groups[1], "candidate and release both write publication ledgers")
        checks = workflow("repository-checks.yml")
        self.assertIn("cancel-in-progress: true", checks)
        self.assertIn("github.event.pull_request.number || github.ref", checks)

    def test_publication_diagnostics_are_always_preserved_and_explicitly_scoped(self):
        for name, expected in (("build-candidate.yml", "production/BUILD_STATUS.json"),
                               ("rebuild-delivery.yml", "production/RELEASE_RESULT.json")):
            with self.subTest(workflow=name):
                text = workflow(name)
                steps = [step for step in re.split(r"(?m)^      - ", text)[1:]
                         if "uses: actions/upload-artifact@v4" in step]
                self.assertEqual(len(steps), 1)
                artifact = steps[0]
                self.assertIn("if: always()", artifact)
                self.assertIn("retention-days: 14", artifact)
                paths = re.search(r"(?ms)^          path: \|\n(.*)", artifact).group(1).splitlines()
                paths = [path.strip() for path in paths if path.strip()]
                self.assertIn(expected, paths)
                self.assertIn("production/qa/STATUS.json", paths)
                for path in paths:
                    self.assertRegex(path, r"^(production|dist)/[A-Za-z0-9_./-]+\.json$")
                    self.assertNotIn("..", Path(path).parts)
                    self.assertNotIn("references", Path(path).parts)

    def test_workflows_have_no_duplicate_keys(self):
        """GitHub rejects a workflow with a duplicated mapping key (PyYAML silently keeps the last), so no run ever starts.
        Standard library only: a small indentation-aware scan of the mapping keys, skipping block scalars (run: |)."""
        import re
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            with self.subTest(wf=wf.name):
                stack = []          # (indent, set of keys seen at that indent)
                block_indent = None
                for n, raw in enumerate(wf.read_text(encoding="utf-8").splitlines(), 1):
                    if not raw.strip() or raw.lstrip().startswith("#"):
                        continue
                    ind = len(raw) - len(raw.lstrip())
                    if block_indent is not None:
                        if ind > block_indent:
                            continue
                        block_indent = None
                    line = raw.lstrip()
                    new_item = line.startswith("- ")
                    if new_item:
                        ind += 2
                        line = line[2:].lstrip()
                    while stack and stack[-1][0] > ind:
                        stack.pop()
                    if new_item:
                        while stack and stack[-1][0] >= ind:
                            stack.pop()
                    m = re.match(r"([A-Za-z_][\w.-]*|'[^']*'|\"[^\"]*\"):(\s|$)", line)
                    if not m:
                        continue
                    if not stack or stack[-1][0] < ind:
                        stack.append((ind, set()))
                    key = m.group(1)
                    self.assertNotIn(key, stack[-1][1], f"{wf.name}:{n}: duplicate key {key!r}")
                    stack[-1][1].add(key)
                    if re.search(r":\s*[|>][+-]?\s*$", line):
                        block_indent = ind - (2 if new_item else 0)

    def test_request_tool_is_stdlib_only(self):
        import ast
        mods = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse((ROOT / "tools/build_request.py").read_text())) if isinstance(n, ast.Import)}
        self.assertLessEqual(mods, set(sys.stdlib_module_names))

    def test_workflow_reruns_use_distinct_release_tags(self):
        bash = shutil.which("bash")
        if not bash and os.name == "nt":
            candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
            bash = str(candidate) if candidate.is_file() else None
        if not bash:
            self.skipTest("Bash is needed to exercise the workflows' release tag commands")
        for filename, kind in (("build-candidate.yml", "candidate"), ("rebuild-delivery.yml", "build")):
            workflow = (ROOT / ".github/workflows" / filename).read_text(encoding="utf-8")
            script = re.search(r"(?ms)^          (TAG=.*?)^          shopt", workflow).group(1)
            tags = []
            for attempt in (1, 2, 3):
                with self.subTest(workflow=filename, attempt=attempt):
                    env = dict(os.environ, VERSION="RC492", GITHUB_RUN_NUMBER="37", GITHUB_RUN_ATTEMPT=str(attempt))
                    result = subprocess.run([bash, "-c", 'set -eu\n' + script + '\nprintf "%s" "$TAG"'],
                                            env=env, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    tags.append(result.stdout)
            self.assertEqual(tags[0], f"RC492-{kind}-37")
            self.assertEqual(tags[1:], [f"RC492-{kind}-37-attempt-2", f"RC492-{kind}-37-attempt-3"])
            self.assertEqual(len(set(tags)), 3)


class BuildReadiness(unittest.TestCase):
    def test_a_stale_art_binding_blocks_the_request_before_any_ci_run(self):
        import build_request
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "production/art/gpt").mkdir(parents=True)
            (root / "production/art/SPOT_CATALOG.json").write_text(json.dumps({"entries": [
                {"id": "ART-A", "spec_sha256": "new"}, {"id": "ART-B", "spec_sha256": "same"}]}))
            (root / "production/art/gpt/QUEUE.json").write_text(json.dumps({"items": []}))
            sels = {"ART-A": {"status": "approved", "spec_sha256": "old"}, "ART-B": {"status": "approved", "spec_sha256": "same"}}
            ok = subprocess.CompletedProcess([], 0, "", "")
            with patch.object(build_request, "ROOT", root), patch.object(build_request, "require_clean_main", return_value="a" * 40), \
                    patch.object(build_request.subprocess, "run", return_value=ok):
                (root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
                found = build_request.problems()
                self.assertEqual(len(found), 1)
                self.assertIn("outdated catalogue spec", found[0])
                self.assertIn("ART-A", found[0])
                sels["ART-A"]["spec_sha256"] = "new"
                (root / "production/art/SELECTIONS.json").write_text(json.dumps(sels))
                self.assertEqual(build_request.problems(), [])


if __name__ == "__main__":
    unittest.main()
