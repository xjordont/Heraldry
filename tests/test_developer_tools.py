"""Developer checks select the intended runtime and reject incomplete dependency locks."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_dependencies import locked_packages
from dev import select_python


class DeveloperTools(unittest.TestCase):
    def test_explicit_python_command_resolves_through_path(self):
        with patch("dev.shutil.which", return_value=sys.executable):
            self.assertEqual(select_python(override="fixture-python"), str(Path(sys.executable).resolve()))

    def test_lock_requires_unique_exact_pins(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "requirements.lock"
            for text in ("", "pillow>=12\n", "pillow==1\nPillow==2\n", "numpy==\n"):
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        locked_packages(path)
            path.write_text("# pinned\npillow==12.3.0\n", encoding="utf-8")
            self.assertEqual(locked_packages(path), {"pillow": "12.3.0"})

    def test_prefers_checkout_environment_and_honours_explicit_override(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "repo"
            shared = root.parent / "art-venv/Scripts/python.exe"
            shared.parent.mkdir(parents=True)
            shared.touch()
            self.assertEqual(Path(select_python(root)), shared)
            local = root / ".venv/Scripts/python.exe"
            local.parent.mkdir(parents=True)
            local.touch()
            self.assertEqual(Path(select_python(root)), local)
            self.assertEqual(Path(select_python(root, str(shared))), shared.resolve())
            with self.assertRaises(ValueError):
                select_python(root, str(root / "missing.exe"))


if __name__ == "__main__":
    unittest.main()
