import json, sys, tempfile, unittest
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_status  # noqa: E402


class BuildChain(unittest.TestCase):
    def test_visual_review_alone_makes_a_candidate(self):
        r, failed, _ = build_status.evaluate({"mandatory_failed": ["visual_review_currency"]}, "")
        self.assertEqual((r, failed), ("CANDIDATE_READY", ["visual_review_currency"]))

    def test_any_other_failure_or_failed_step_fails(self):
        self.assertEqual(build_status.evaluate({"mandatory_failed": ["visual_review_currency", "one_page_keeps"]}, "")[0], "FAILED")
        self.assertEqual(build_status.evaluate({"mandatory_failed": []}, "tests and clean build")[0], "FAILED")
        self.assertEqual(build_status.evaluate(None, "")[0], "FAILED")

    def test_workflows_wired(self):
        cand = (ROOT / ".github/workflows/build-candidate.yml").read_text()
        rel = (ROOT / ".github/workflows/rebuild-delivery.yml").read_text()
        self.assertIn("production/build-request.json", cand)
        self.assertIn("--prerelease", cand)
        self.assertIn("production/qa/visual-review.json", rel)
        self.assertIn("tools/review_aids.py", cand)
        self.assertIn("tools/release_result.py", rel)
        for wf in (cand, rel):
            self.assertIn("assets/art/cover/front.png", wf, "the cover is an LFS file the build places")

    def test_workflows_have_no_duplicate_keys(self):
        """GitHub rejects a workflow with a duplicated mapping key (PyYAML silently keeps the last), so no run ever starts.
        Standard library only: a small indentation-aware scan of the mapping keys, skipping block scalars (run: |)."""
        import re
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            with self.subTest(wf=wf.name):
                stack = []          # (indent, set of keys seen at that indent)
                block_indent = None
                for n, raw in enumerate(wf.read_text().splitlines(), 1):
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


if __name__ == "__main__":
    unittest.main()
