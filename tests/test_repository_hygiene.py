"""AGENTS.md "Files": built PDFs, ZIPs, and secrets are never committed.

CI runs this on every push, so it also covers commits from clients without the Claude Code hook
(.claude/hooks/git-guard.sh). The owner's reference books listed in references/sample_pdfs.json are the
one allowed set of tracked PDFs; any other PDF, ZIP, key, or .env file fails.
"""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(r"\.(pdf|zip|pem|key|p12|pfx)$|(^|/)\.env(\.[^/]*)?$|(^|/)id_(rsa|ed25519)$", re.IGNORECASE)


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [p for p in out.decode("utf-8").split("\0") if p]


class RepositoryHygieneTest(unittest.TestCase):
    def test_no_built_files_or_secrets_are_tracked(self):
        files = tracked_files()
        if files is None:
            self.skipTest("not a Git checkout")
        samples = json.loads((ROOT / "references/sample_pdfs.json").read_text(encoding="utf-8"))
        allowed = {entry["path"] for entry in samples["files"]
                   if isinstance(entry, dict) and "path" in entry}
        bad = sorted(p for p in files
                     if FORBIDDEN.search(p) and not p.endswith(".env.example") and p not in allowed)
        self.assertEqual(bad, [], "PDFs, ZIPs, and secrets must not be committed (AGENTS.md, docs/LARGE_FILES.md)")

    def test_pattern(self):
        for path in ("dist/Heraldry_RC528_digital.pdf", "build/x.ZIP", ".env", "config/.env.local", "a/id_rsa", "k.pem"):
            self.assertTrue(FORBIDDEN.search(path), path)
        for path in (".env.example", "docs/pdf-notes.md", "tools/package.py", "assets/x.png", "environment.md"):
            self.assertFalse(FORBIDDEN.search(path) and not path.endswith(".env.example"), path)


if __name__ == "__main__":
    unittest.main()
