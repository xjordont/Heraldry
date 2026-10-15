"""Windows checkout settings cannot rewrite hash-bound source or patch evidence."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CheckoutBytes(unittest.TestCase):
    def test_autocrlf_checkout_preserves_immutable_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            author, clone = root / "author", root / "clone"
            author.mkdir()

            def git(cwd, *args):
                result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                                        encoding="utf-8", errors="replace")
                self.assertEqual(result.returncode, 0, result.stderr)

            git(author, "init", "--initial-branch=main")
            git(author, "config", "user.name", "Checkout test")
            git(author, "config", "user.email", "checkout@example.invalid")
            git(author, "config", "core.autocrlf", "false")
            git(author, "config", "commit.gpgsign", "false")
            (author / ".gitattributes").write_bytes((ROOT / ".gitattributes").read_bytes())
            originals = {"source/Heraldry_fixture.md": b"# Immutable\n\nOriginal bytes.\n",
                         "editorial/history/RCfixture.json": b'{\n "patches": []\n}\n'}
            for name, data in originals.items():
                path = author / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            git(author, "add", ".")
            git(author, "commit", "-m", "immutable fixtures")
            git(root, "-c", "core.autocrlf=true", "clone", "--no-local", str(author), str(clone))
            for name, data in originals.items():
                self.assertEqual((clone / name).read_bytes(), data, name)


if __name__ == "__main__":
    unittest.main()
