"""Contract and revision checks must read UTF-8 regardless of the host locale."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TextEncoding(unittest.TestCase):
    def run_strict(self, *args):
        env = dict(os.environ, PYTHONUTF8="0")
        result = subprocess.run(
            [sys.executable, "-X", "warn_default_encoding", "-W", "error::EncodingWarning", *args],
            cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_preflight_checks_real_utf8_evidence_without_a_locale_override(self):
        with tempfile.TemporaryDirectory() as d:
            report = Path(d) / "preflight.json"
            self.run_strict("tools/preflight.py", "--report", str(report))
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result["kit_status"], "PASS")
            self.assertTrue(all(c["status"] == "PASS" for c in result["checks"]))

    def test_revision_round_trip_reads_utf8_registry_config_and_patch_history(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ("source", "config", "editorial"):
                shutil.copytree(ROOT / name, root / name)
            proposal = root / "proposal.json"
            proposal.write_text(json.dumps({"patches": [{
                "id": "ENCODING-TEST", "status": "approved",
                "find": "A competitive GM-less PvPvE fantasy tabletop miniature skirmish game",
                "replace": "A competitive GM-less PvPvE fantasy tabletop miniature skirmish game for testing",
                "expected_count": 1,
            }]}, ensure_ascii=False), encoding="utf-8")
            code = (
                "import sys; from pathlib import Path; "
                "sys.path.insert(0, str(Path('tools').resolve())); "
                "from revise_manuscript import revise; "
                "from manuscript import check; "
                "root=Path(sys.argv[1]); "
                "revise(root, root/'proposal.json', 'UTF-8 test', 'Test fixture only'); "
                "check(root)"
            )
            self.run_strict("-c", code, str(root))


if __name__ == "__main__":
    unittest.main()
