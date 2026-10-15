"""Release completion and race-safe result publication, without network access."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import release_result  # noqa: E402


class ReleaseResultStatus(unittest.TestCase):
    def test_success_requires_matching_release_and_successful_job(self):
        release = {"source_commit": "reviewed"}
        self.assertEqual(release_result.evaluate(release, "reviewed", "success")[0], "RELEASED")
        for status in ("failure", "cancelled", "skipped"):
            with self.subTest(status=status):
                result, note = release_result.evaluate(release, "reviewed", status)
                self.assertEqual(result, "FAILED")
                self.assertIn(status, note)
        self.assertEqual(release_result.evaluate(release, "new", "success")[0], "FAILED")
        self.assertEqual(release_result.evaluate({}, "reviewed", "success")[0], "FAILED")

    def test_ledger_failure_cannot_be_reported_as_released(self):
        result, note = release_result.evaluate({"source_commit": "reviewed"}, "reviewed", "failure", "commit verification ledgers")
        self.assertEqual(result, "FAILED")
        self.assertIn("commit verification ledgers", note)

    def test_workflow_passes_job_status_and_ledger_failure(self):
        workflow = (ROOT / ".github/workflows/rebuild-delivery.yml").read_text(encoding="utf-8")
        self.assertIn("id: ledgers", workflow)
        self.assertIn('--job-status "${{ job.status }}"', workflow)
        self.assertIn("steps.ledgers.outcome", workflow)
        result_step = workflow.split("- name: Record the release result on main", 1)[1]
        self.assertIn("--push", result_step)
        self.assertNotIn("--rebase", result_step)
        self.assertNotIn("git commit", result_step)


class ReleaseResultPublication(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="heraldry-release-result-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.origin = self.base / "origin.git"
        self.runner = self.base / "runner"
        self.peer = self.base / "peer"
        self.git(self.base, "init", "--bare", "--initial-branch=main", str(self.origin))
        self.git(self.base, "clone", str(self.origin), str(self.runner))
        self.configure(self.runner)
        (self.runner / "production").mkdir()
        (self.runner / "dist").mkdir()
        (self.runner / release_result.RESULT).write_text('{"result": "previous"}\n', encoding="utf-8")
        (self.runner / "dist/RELEASE.json").write_text('{"tag": "previous"}\n', encoding="utf-8")
        self.git(self.runner, "add", ".")
        self.git(self.runner, "commit", "-m", "initial main")
        self.git(self.runner, "push", "origin", "main")
        self.initial = self.git(self.runner, "rev-parse", "HEAD")
        self.git(self.base, "clone", str(self.origin), str(self.peer))
        self.configure(self.peer)

    def git(self, cwd, *args):
        result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def configure(self, repo):
        self.git(repo, "config", "user.name", "Release result tests")
        self.git(repo, "config", "user.email", "release-result@example.invalid")
        self.git(repo, "config", "core.autocrlf", "false")
        self.git(repo, "config", "commit.gpgsign", "false")

    def remote(self, *args):
        return self.git(self.base, f"--git-dir={self.origin}", *args)

    def write_result(self):
        payload = json.dumps({"result": "FAILED", "note": "commit verification ledgers failed"}) + "\n"
        (self.runner / release_result.RESULT).write_text(payload, encoding="utf-8")
        return payload

    def test_advanced_main_does_not_receive_pending_verification_commit(self):
        # The release runner committed rebuilt ledgers, but its push lost to another writer.
        (self.runner / "dist/RELEASE.json").write_text('{"tag": "stale pending release"}\n', encoding="utf-8")
        self.git(self.runner, "add", "dist/RELEASE.json")
        self.git(self.runner, "commit", "-m", "pending verification ledgers")
        pending = self.git(self.runner, "rev-parse", "HEAD")
        (self.peer / "new-tool.txt").write_text("new main input\n", encoding="utf-8")
        self.git(self.peer, "add", "new-tool.txt")
        self.git(self.peer, "commit", "-m", "new owner change")
        self.git(self.peer, "push", "origin", "main")
        advanced = self.git(self.peer, "rev-parse", "HEAD")
        # The normal index and worktree may also contain build output and unrelated edits.
        (self.runner / "dirty.txt").write_text("staged\n", encoding="utf-8")
        self.git(self.runner, "add", "dirty.txt")
        (self.runner / "dirty.txt").write_text("unstaged\n", encoding="utf-8")
        payload = self.write_result()
        status = self.git(self.runner, "status", "--porcelain")
        index = (self.runner / ".git/index").read_bytes()

        published = release_result.publish_result(self.runner, retry_delay=0)

        self.assertEqual(self.remote("rev-parse", "main"), published)
        self.assertEqual(self.remote("rev-parse", "main^"), advanced)
        self.assertEqual(self.remote("diff-tree", "--no-commit-id", "--name-only", "-r", published), release_result.RESULT)
        self.assertEqual(self.remote("show", "main:dist/RELEASE.json"), '{"tag": "previous"}')
        self.assertEqual(self.remote("show", "main:new-tool.txt"), "new main input")
        self.assertEqual(self.remote("show", f"main:{release_result.RESULT}"), payload.strip())
        self.assertEqual(self.git(self.runner, "rev-parse", "HEAD"), pending)
        self.assertEqual((self.runner / ".git/index").read_bytes(), index)
        self.assertEqual(self.git(self.runner, "status", "--porcelain"), status)
        self.assertEqual((self.runner / "dirty.txt").read_text(encoding="utf-8"), "unstaged\n")

    def test_push_race_retries_from_the_new_parent(self):
        self.write_result()
        real_run = subprocess.run
        pushes = []
        advance = []

        def race(args, **kwargs):
            if args[:3] == ["git", "push", "origin"]:
                pushes.append(args)
                if len(pushes) == 1:
                    (self.peer / "racing.txt").write_text("racing main input\n", encoding="utf-8")
                    for command in (["git", "add", "racing.txt"], ["git", "commit", "-m", "race winner"], ["git", "push", "origin", "main"]):
                        result = real_run(command, cwd=self.peer, capture_output=True)
                        self.assertEqual(result.returncode, 0, result.stderr)
                    advance.append(real_run(["git", "rev-parse", "HEAD"], cwd=self.peer, capture_output=True, text=True).stdout.strip())
            return real_run(args, **kwargs)

        with patch.object(release_result.subprocess, "run", side_effect=race):
            published = release_result.publish_result(self.runner, retry_delay=0)

        self.assertEqual(len(pushes), 2)
        self.assertEqual(self.remote("rev-parse", "main"), published)
        self.assertEqual(self.remote("rev-parse", "main^"), advance[0])
        self.assertEqual(self.remote("show", "main:racing.txt"), "racing main input")
        self.assertEqual(self.remote("diff-tree", "--no-commit-id", "--name-only", "-r", published), release_result.RESULT)

    def test_non_race_push_error_is_not_retried(self):
        self.write_result()
        real_run = subprocess.run
        pushes = []

        def denied(args, **kwargs):
            if args[:3] == ["git", "push", "origin"]:
                pushes.append(args)
                return subprocess.CompletedProcess(args, 128, stdout=b"", stderr=b"permission denied")
            return real_run(args, **kwargs)

        with patch.object(release_result.subprocess, "run", side_effect=denied):
            with self.assertRaisesRegex(RuntimeError, "not a main-update race"):
                release_result.publish_result(self.runner, retry_delay=0)
        self.assertEqual(len(pushes), 1)
        self.assertEqual(self.remote("rev-parse", "main"), self.initial)

    def test_identical_result_is_a_no_op(self):
        self.assertEqual(release_result.publish_result(self.runner, retry_delay=0), self.initial)
        self.assertEqual(self.remote("rev-parse", "main"), self.initial)
        self.assertEqual(self.git(self.runner, "status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
