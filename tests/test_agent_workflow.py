"""Cross-client workflow access preserves the existing tools and their failure gates."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import agent_workflow as agent
import build_request
import dev
import package


class SharedAgentWorkflows(unittest.TestCase):
    def fixture(self, root):
        for name in ["config/agent_workflows.json", *[
                value for role in agent.catalog()["roles"]
                for key, value in role.items() if key != "name"],
                *[flow["script"] for flow in agent.catalog()["workflows"].values()]]:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(agent.ROOT / name, target)

    def test_all_clients_share_roles_and_workflows_without_native_model_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            data = agent.catalog(root)
            self.assertEqual(set(data["clients"]), agent.CLIENTS)
            self.assertEqual(len(data["roles"]), 6)
            self.assertIn("art-intake", data["workflows"])
            self.assertIn("build", data["workflows"])
            self.assertIn("visual-review", data["workflows"])
            # No Claude settings, installation, account, or native worker runtime in this fixture.
            self.assertFalse((root / ".claude/settings.json").exists())

    def test_catalog_rejects_client_exclusion_missing_tools_and_adapter_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            path = root / "config/agent_workflows.json"
            original = path.read_bytes()
            data = json.loads(original)
            data["clients"].remove("chatgpt-work")
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "all three"):
                agent.catalog(root)
            path.write_bytes(original)
            (root / "tools/art_intake.py").unlink()
            with self.assertRaisesRegex(ValueError, "Missing"):
                agent.catalog(root)
            shutil.copyfile(agent.ROOT / "tools/art_intake.py", root / "tools/art_intake.py")
            adapter = root / agent.catalog(root)["roles"][0]["claude_adapter"]
            adapter.write_text("stale native-only role", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "shared role"):
                agent.catalog(root)

    def test_workflow_paths_cannot_escape_repository_or_select_unrelated_files(self):
        for value in ("../external.py", str(agent.ROOT / "tools/dev.py"), "source/Heraldry_RC513.md"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                agent.repository_file(agent.ROOT, value, ("tools/",))

    def test_read_commands_do_not_execute_workflows(self):
        for args in (["list"], ["check"], ["role", "publication-engineer"]):
            with patch.object(agent.subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(agent.main(args), 0)
                self.assertTrue(output.getvalue())
                run.assert_not_called()

    def test_dispatch_preserves_arguments_environment_and_underlying_failure(self):
        forwarded = ["bind", "--review", "a path with spaces/review.json", "--push", "$(not-a-shell)"]
        with patch.object(agent.subprocess, "run", return_value=subprocess.CompletedProcess([], 2)) as run:
            self.assertEqual(agent.main(["run", "visual-review", "--", *forwarded]), 2)
            command = run.call_args.args[0]
            self.assertEqual(command, [sys.executable, str(agent.ROOT / "tools/visual_review_bind.py"), *forwarded])
            self.assertEqual(run.call_args.kwargs["cwd"], agent.ROOT)
            self.assertEqual(run.call_args.kwargs["env"]["PYTHONUTF8"], "1")
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_real_script_execution_returns_failure_without_shell_interpolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            script = root / "tools/art_intake.py"
            script.write_text("import sys\nfrom pathlib import Path\nPath('args.txt').write_text(repr(sys.argv[1:]))\nraise SystemExit(7)\n", encoding="utf-8")
            literal = "$(must-stay-literal)"
            self.assertEqual(agent.main(["run", "art-intake", "--", "reject", literal], root), 7)
            self.assertEqual((root / "args.txt").read_text(), repr(["reject", literal]))

    def test_unknown_role_or_workflow_does_not_run_anything(self):
        for args in (["role", "invented"], ["run", "invented"]):
            with patch.object(agent.subprocess, "run") as run, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(agent.main(args), 1)
                run.assert_not_called()

    def test_dev_launcher_delegates_using_selected_environment(self):
        argv = ["tools/dev.py", "agent", "run", "layout", "--", "check"]
        with patch.object(sys, "argv", argv), patch.object(dev, "select_python", return_value="chosen-python"), \
                patch.object(dev, "run", return_value=2) as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(dev.main(), 2)
            run.assert_called_once_with("chosen-python", "tools/agent_workflow.py", "run", "layout", "--", "check")

    def test_release_package_includes_generic_agent_entry_point_and_shared_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ["AGENTS.md", "CLAUDE.md", "docs/PROJECT_CONTRACT.md", "config/agent_workflows.json"]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture", encoding="utf-8")
            with patch.object(package, "ROOT", root):
                paths = {path.relative_to(root).as_posix() for path in package.files()}
            self.assertTrue({"AGENTS.md", "CLAUDE.md", "docs/PROJECT_CONTRACT.md", "config/agent_workflows.json"} <= paths)

    def test_build_requests_record_actual_client_and_retain_guarded_publishing(self):
        for client in sorted(agent.CLIENTS):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "production").mkdir()
                with patch.object(build_request, "ROOT", root), patch.object(build_request, "problems", return_value=[]), \
                        patch.object(build_request, "require_clean_main", return_value="a" * 40), \
                        patch.object(build_request, "publish_files", return_value="b" * 40) as publish, \
                        contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(build_request.cmd_request(argparse.Namespace(requested_by=client)), 0)
                record = json.loads((root / build_request.REQUEST).read_text(encoding="utf-8"))
                self.assertEqual(record["requested_by"], client)
                self.assertEqual(record["base_commit"], "a" * 40)
                self.assertEqual(publish.call_args.args[1], [build_request.REQUEST])


if __name__ == "__main__":
    unittest.main()
