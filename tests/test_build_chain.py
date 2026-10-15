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

    def test_workflows_have_no_duplicate_keys(self):
        """GitHub rejects a workflow with a duplicated mapping key (PyYAML silently keeps the last), so no run ever starts."""
        import yaml
        from yaml.constructor import ConstructorError

        class Strict(yaml.SafeLoader):
            pass

        def no_dup(loader, node, deep=False):
            seen = set()
            for k, _ in node.value:
                key = loader.construct_object(k, deep=deep)
                if key in seen:
                    raise ConstructorError(None, None, f"duplicate key {key!r}", k.start_mark)
                seen.add(key)
            return yaml.SafeLoader.construct_mapping(loader, node, deep)
        Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_dup)
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            with self.subTest(wf=wf.name):
                yaml.load(wf.read_text(), Loader=Strict)

    def test_request_tool_is_stdlib_only(self):
        import ast
        mods = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse((ROOT / "tools/build_request.py").read_text())) if isinstance(n, ast.Import)}
        self.assertLessEqual(mods, set(sys.stdlib_module_names))


if __name__ == "__main__":
    unittest.main()
