"""AGENTS.md "Files": built PDFs, ZIPs, and secrets are never committed.

CI runs this on every push, so it also covers commits from clients without the Claude Code hook
(.claude/hooks/git-guard.sh). There are no exceptions: the owner's reference books stay local in
references/private/ and were purged from history on 2026-11-02.
"""
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
        bad = sorted(p for p in files if FORBIDDEN.search(p) and not p.endswith(".env.example"))
        self.assertEqual(bad, [], "PDFs, ZIPs, and secrets must not be committed (AGENTS.md, docs/LARGE_FILES.md)")

    def test_pattern(self):
        for path in ("dist/Heraldry_RC528_digital.pdf", "build/x.ZIP", ".env", "config/.env.local", "a/id_rsa", "k.pem"):
            self.assertTrue(FORBIDDEN.search(path), path)
        for path in (".env.example", "docs/pdf-notes.md", "tools/package.py", "assets/x.png", "environment.md"):
            self.assertFalse(FORBIDDEN.search(path) and not path.endswith(".env.example"), path)


if __name__ == "__main__":
    unittest.main()
