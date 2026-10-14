import json, sys, tempfile, unittest
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

    def test_request_tool_is_stdlib_only(self):
        import ast
        mods = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse((ROOT / "tools/build_request.py").read_text())) if isinstance(n, ast.Import)}
        self.assertLessEqual(mods, set(sys.stdlib_module_names))


if __name__ == "__main__":
    unittest.main()
