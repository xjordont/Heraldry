"""Exercise ZIP creation and readback with a small isolated publication fixture."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import package


class PackagePaths(unittest.TestCase):
    def test_zip_members_and_checksums_are_portable_and_match_source_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            dist = root / "dist"
            dist.mkdir()
            for name, data in {"source/fixture.txt": b"source fixture\n",
                               "docs/proof-\u00e9.txt": b"print fixture\n"}.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            provenance = {"fixture": "current"}
            qa = root / "production/qa"
            qa.mkdir(parents=True)
            (qa / "STATUS.json").write_text(
                json.dumps({"release_gate": "PASS", "provenance": provenance}), encoding="utf-8")
            with patch.object(package, "ROOT", root), patch.object(package, "DIST", dist), \
                    patch.object(package, "check"), patch.object(package, "check_build", return_value=provenance), \
                    patch.object(package, "version", return_value="RC999"), contextlib.redirect_stdout(io.StringIO()):
                package.main()
            with zipfile.ZipFile(dist / "Heraldry_RC999_release.zip") as archive:
                names = archive.namelist()
                self.assertTrue(all("\\" not in name for name in names))
                self.assertIn("Heraldry_RC999/SHA256SUMS.txt", names)
                sums = archive.read("Heraldry_RC999/SHA256SUMS.txt").decode("utf-8")
                self.assertEqual(sums, (dist / "SHA256SUMS.txt").read_text(encoding="utf-8"))
                self.assertNotIn("\\", sums)
                for line in sums.splitlines():
                    digest, name = line.split("  ", 1)
                    data = archive.read("Heraldry_RC999/" + name)
                    self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
                    self.assertEqual(data, (root / name).read_bytes())
                self.assertIn("Heraldry_RC999/docs/proof-\u00e9.txt", names)
            report = json.loads((qa / "package-audit.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["checksums_verified"], len(names) - 1)


if __name__ == "__main__":
    unittest.main()
