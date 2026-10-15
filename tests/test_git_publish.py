"""Publication helpers preserve local work and never rebase a rejected push."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_request
import git_publish as publish


class GitPublication(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.remote = self.directory / "origin.git"
        self.root = self.directory / "checkout"
        self.remote.mkdir()
        self.root.mkdir()
        self.git("init", "--bare", "--initial-branch=main", cwd=self.remote)
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Fixture publisher")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        self.git("remote", "add", "origin", str(self.remote))
        (self.root / "production").mkdir()
        (self.root / "production/build-request.json").write_text('{"old": true}\n', encoding="utf-8")
        (self.root / "other.txt").write_text("unrelated existing file\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "fixture base")
        self.git("push", "origin", "main")
        self.base = self.git("rev-parse", "HEAD")
        self.tests_run = []

    def git(self, *args, cwd=None):
        result = subprocess.run(["git", *args], cwd=cwd or self.root, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def run_tests(self, root):
        self.tests_run.append(root)

    def write_payload(self):
        (self.root / "production/build-request.json").write_text('{"new": true}\n', encoding="utf-8")

    def publish_payload(self, test_runner=None):
        return publish.publish_files(self.root, ["production/build-request.json"], "fixture publication", self.base,
                                     test_runner=test_runner or self.run_tests)

    def advance_remote(self):
        """Advance only the bare fixture repository, simulating a competing writer."""
        tree = self.git("rev-parse", self.base + "^{tree}")
        commit = self.git("-c", "user.name=Fixture writer", "-c", "user.email=fixture@example.invalid",
                          "commit-tree", tree, "-p", self.base, "-m", "concurrent remote change", cwd=self.remote)
        self.git("update-ref", "refs/heads/main", commit, self.base, cwd=self.remote)
        return commit

    def test_publication_runs_tests_then_pushes_only_its_file(self):
        self.assertEqual(publish.require_clean_main(self.root), self.base)
        self.write_payload()
        commit = self.publish_payload()
        self.assertEqual(self.tests_run, [self.root])
        self.assertEqual(self.git("rev-parse", "main", cwd=self.remote), commit)
        self.assertEqual(self.git("show", "--format=", "--name-only", commit), "production/build-request.json")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_clean_check_refuses_untracked_unstaged_and_staged_changes(self):
        for kind in ("untracked", "unstaged", "staged"):
            with self.subTest(kind=kind):
                target = self.root / ("new file.txt" if kind == "untracked" else "other.txt")
                before = target.read_bytes() if target.exists() else None
                target.write_text("must be preserved\n", encoding="utf-8")
                if kind == "staged":
                    self.git("add", "other.txt")
                status = self.git("status", "--porcelain")
                with self.assertRaises(publish.PublishError):
                    publish.require_clean_main(self.root)
                self.assertEqual(self.git("status", "--porcelain"), status)
                self.assertEqual(target.read_text(encoding="utf-8"), "must be preserved\n")
                # Clean only this test's known fixture changes between subtests.
                if kind == "staged":
                    self.git("restore", "--staged", "other.txt")
                if before is None:
                    target.unlink()
                else:
                    target.write_bytes(before)

    def test_clean_check_refuses_wrong_branch_and_ahead_or_behind_main(self):
        self.git("checkout", "-b", "fixture-other")
        with self.assertRaises(publish.PublishError):
            publish.require_clean_main(self.root)
        self.git("checkout", "main")
        self.advance_remote()
        with self.assertRaises(publish.PublishError):
            publish.require_clean_main(self.root)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_local_ahead_commit_is_preserved_and_not_pushed(self):
        self.git("commit", "--allow-empty", "-m", "unsent owner work")
        local = self.git("rev-parse", "HEAD")
        with self.assertRaises(publish.PublishError):
            publish.require_clean_main(self.root)
        self.assertEqual(self.git("rev-parse", "HEAD"), local)
        self.assertEqual(self.git("rev-parse", "main", cwd=self.remote), self.base)

    def test_unrelated_staging_is_not_committed_or_pushed(self):
        self.write_payload()
        (self.root / "other.txt").write_text("owner edit\n", encoding="utf-8")
        self.git("add", "other.txt")
        before = self.git("status", "--porcelain")
        with self.assertRaises(publish.PublishError):
            self.publish_payload()
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertFalse(self.tests_run)

    def test_failed_tests_preserve_payload_without_commit(self):
        self.write_payload()

        def failed(_):
            raise publish.PublishError("fixture test failure")

        with self.assertRaises(publish.PublishError):
            self.publish_payload(failed)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertIn('"new": true', (self.root / "production/build-request.json").read_text(encoding="utf-8"))

    def test_rechecks_remote_and_unrelated_changes_after_tests(self):
        self.write_payload()

        def tests_with_edit(_):
            (self.root / "other.txt").write_text("concurrent owner work\n", encoding="utf-8")
            self.git("add", "other.txt")

        with self.assertRaises(publish.PublishError):
            self.publish_payload(tests_with_edit)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "other.txt")
        # Restore only the simulated concurrent edit, then simulate remote movement.
        self.git("restore", "--staged", "other.txt")
        (self.root / "other.txt").write_text("unrelated existing file\n", encoding="utf-8")
        with self.assertRaises(publish.PublishError):
            self.publish_payload(lambda _: self.advance_remote())
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_payload_changed_by_tests_requires_retesting(self):
        self.write_payload()

        def mutating_tests(_):
            (self.root / "production/build-request.json").write_text('{"untested": true}\n', encoding="utf-8")

        with self.assertRaises(publish.PublishError):
            self.publish_payload(mutating_tests)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)

    def test_rejected_push_preserves_commit_and_does_not_rebase(self):
        self.write_payload()
        real_git = publish._git
        calls = []
        remote_commit = None

        def race(root, *args):
            nonlocal remote_commit
            calls.append(args)
            if args[0] == "push":
                remote_commit = self.advance_remote()
            return real_git(root, *args)

        with patch.object(publish, "_git", side_effect=race):
            with self.assertRaisesRegex(publish.PublishError, "local commit .* preserved"):
                self.publish_payload()
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.base)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("rev-parse", "main", cwd=self.remote), remote_commit)
        self.assertFalse(any(args[0] in {"pull", "rebase", "reset"} for args in calls))

    def test_request_preflight_rechecks_clean_main_before_writing(self):
        target = self.root / "production/build-request.json"
        before = target.read_bytes()
        (self.root / "other.txt").write_text("owner work\n", encoding="utf-8")
        with patch.object(build_request, "ROOT", self.root), patch.object(build_request, "problems", return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(build_request.cmd_request(None), 2)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)


class TestCommand(unittest.TestCase):
    def test_make_uses_current_python_with_spaces_and_utf8(self):
        root = Path(tempfile.gettempdir())
        python = str(root / "Python with spaces/python.exe")
        with patch.object(publish, "find_make", return_value="fixture-make"), \
                patch.object(publish.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            publish.run_tests(root, python)
        args, kwargs = run.call_args
        self.assertEqual(args[0], ["fixture-make", "test", f'PY="{str(Path(python).resolve()).replace(chr(92), "/")}"'])
        self.assertEqual(kwargs["env"]["PYTHONUTF8"], "1")

    def test_missing_make_or_failed_tests_refuses_publication(self):
        with patch.object(publish.shutil, "which", return_value=None), \
                patch.object(Path, "is_file", return_value=False):
            with self.assertRaises(publish.PublishError):
                publish.find_make(Path(tempfile.gettempdir()))
        with patch.object(publish, "find_make", return_value="fixture-make"), \
                patch.object(publish.subprocess, "run", return_value=subprocess.CompletedProcess([], 2)):
            with self.assertRaises(publish.PublishError):
                publish.run_tests(Path(tempfile.gettempdir()))


if __name__ == "__main__":
    unittest.main()
