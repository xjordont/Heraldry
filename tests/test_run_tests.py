"""The parallel test runner must report every failure; a runner that said OK too easily would hide them."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(files):
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as tmp:
        for name, body in files.items():
            (Path(tmp) / name).write_text(body)
        return subprocess.run([sys.executable, "tools/run_tests.py", Path(tmp).relative_to(ROOT).as_posix()],
                              cwd=ROOT, capture_output=True, text=True)


class ParallelRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / "build").mkdir(exist_ok=True)

    def test_counts_every_module_and_passes_only_when_all_pass(self):
        ok = "import unittest\nclass T(unittest.TestCase):\n    def test_a(self): pass\n    def test_b(self): pass\n"
        result = run({"test_one.py": ok, "test_two.py": ok})
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Ran 4 tests in 2 modules", result.stdout)

    def test_a_failure_an_error_or_an_import_problem_fails_the_run(self):
        ok = "import unittest\nclass T(unittest.TestCase):\n    def test_a(self): pass\n"
        for bad in ("import unittest\nclass T(unittest.TestCase):\n    def test_a(self): self.assertEqual(1, 2)\n",
                    "import unittest\nclass T(unittest.TestCase):\n    def test_a(self): raise RuntimeError('boom')\n",
                    "import unittest\nimport no_such_module_anywhere\n",
                    "import unittest\n"):                       # a module with no tests is a mistake, not a pass
            with self.subTest(bad=bad.splitlines()[-1]):
                result = run({"test_good.py": ok, "test_bad.py": bad})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("FAILED:", result.stdout)
                self.assertIn("test_bad", result.stdout.split("FAILED:", 1)[1])


if __name__ == "__main__":
    unittest.main()
