"""Pipe sample hook-input JSON into each hook script and check the decision."""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

HOOKS = pathlib.Path(__file__).resolve().parent.parent / "hooks"


def run(script, payload, project, env=None):
    e = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "DELIVERY_ALLOW_GIT")}
    e["CLAUDE_PROJECT_DIR"] = str(project)
    e.update(env or {})
    return subprocess.run([sys.executable, str(HOOKS / script)], input=json.dumps(payload),
                          capture_output=True, text=True, env=e, timeout=20)


def bash(cmd):
    return {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}}


def write(path):
    return {"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": path, "content": "x"}}


class HookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        (self.root / ".delivery").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def guards(self, cfg):
        (self.root / ".delivery" / "guards.json").write_text(json.dumps(cfg))

    # git guard
    def test_commit_blocked_without_approval(self):
        r = run("guard_git.py", bash('git commit -m "x"'), self.root)
        self.assertEqual(r.returncode, 2)
        self.assertIn("blocked until the owner approves", r.stderr)

    def test_push_and_variants_blocked(self):
        for cmd in ("git push origin main", "git -C repo commit -am x", "cd a && git push",
                    "git --no-pager commit -m y"):
            self.assertEqual(run("guard_git.py", bash(cmd), self.root).returncode, 2, cmd)

    def test_other_git_allowed(self):
        for cmd in ("git status", "git diff --staged", "git log -1", "echo commit", "git add -A"):
            self.assertEqual(run("guard_git.py", bash(cmd), self.root).returncode, 0, cmd)

    def test_commit_allowed_with_approval_file(self):
        (self.root / ".delivery" / "APPROVED").write_text("owner\n")
        self.assertEqual(run("guard_git.py", bash("git commit -m x"), self.root).returncode, 0)

    def test_approval_file_expires(self):
        f = self.root / ".delivery" / "APPROVED"
        f.write_text("owner\n")
        os.utime(f, (0, 0))
        self.assertEqual(run("guard_git.py", bash("git commit -m x"), self.root).returncode, 2)

    def test_commit_allowed_with_env_flag(self):
        r = run("guard_git.py", bash("git push"), self.root, {"DELIVERY_ALLOW_GIT": "1"})
        self.assertEqual(r.returncode, 0)

    def test_no_op_outside_delivery_projects(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(run("guard_git.py", bash("git commit -m x"), other).returncode, 0)

    def test_disabled_in_config(self):
        self.guards({"git_guard": {"enabled": False}})
        self.assertEqual(run("guard_git.py", bash("git commit -m x"), self.root).returncode, 0)

    # secrets guard
    def test_env_write_blocked(self):
        for path in (".env", "/x/y/.env", "app/.env.local", ".env.production"):
            r = run("guard_secrets.py", write(path), self.root)
            self.assertEqual(r.returncode, 2, path)
        self.assertEqual(run("guard_secrets.py", write(".env.example"), self.root).returncode, 0)
        self.assertEqual(run("guard_secrets.py", write("src/env.py"), self.root).returncode, 0)

    def test_env_shell_write_blocked(self):
        for cmd in ("echo X=1 > .env", "echo X >> .env.local", "cp a .env", "printf x | tee .env"):
            self.assertEqual(run("guard_secrets.py", bash(cmd), self.root).returncode, 2, cmd)

    def test_agent_cannot_approve_itself(self):
        self.assertEqual(run("guard_secrets.py", write(".delivery/APPROVED"), self.root).returncode, 2)
        self.assertEqual(run("guard_secrets.py", bash("touch .delivery/APPROVED"), self.root).returncode, 2)

    def test_cat_env_asks(self):
        r = run("guard_secrets.py", bash("cat .env"), self.root)
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")
        r = run("guard_secrets.py", bash("echo $JIRA_TOKEN"), self.root)
        self.assertEqual(json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_cat_env_warn_mode(self):
        self.guards({"secrets_guard": {"read_mode": "warn"}})
        r = run("guard_secrets.py", bash("cat .env"), self.root)
        self.assertIn("systemMessage", json.loads(r.stdout))

    def test_harmless_commands_pass(self):
        for cmd in ("cat README.md", "grep '^JIRA_SITE=' .env.example", "ls -la", "echo hello"):
            r = run("guard_secrets.py", bash(cmd), self.root)
            self.assertEqual((r.returncode, r.stdout), (0, ""), cmd)

    # prod guard
    def test_prod_guard_off_by_default(self):
        self.assertEqual(run("guard_prod.py", bash("flutter run --flavor=prod"), self.root).stdout, "")

    def test_prod_guard_patterns(self):
        self.guards({"prod_guard": {"enabled": True, "patterns": ["--flavor[= ]prod\\b"], "mode": "block"}})
        self.assertEqual(run("guard_prod.py", bash("flutter run --flavor=prod"), self.root).returncode, 2)
        self.assertEqual(run("guard_prod.py", bash("flutter run --flavor=staging"), self.root).returncode, 0)

    # session start
    def test_session_start_prints_restart_doc_and_graph(self):
        (self.root / "ARCHITECTURE-PROMPT.md").write_text("Read ARCHITECTURE.md first.\n")
        r = run("session_start.py", {"hook_event_name": "SessionStart", "source": "startup"}, self.root)
        self.assertEqual(r.returncode, 0)
        self.assertIn("Read ARCHITECTURE.md first.", r.stdout)
        self.assertIn("Code graph: none", r.stdout)

    def test_session_start_silent_outside_delivery_projects(self):
        with tempfile.TemporaryDirectory() as other:
            r = run("session_start.py", {"hook_event_name": "SessionStart"}, other)
            self.assertEqual(r.stdout, "")


if __name__ == "__main__":
    unittest.main()
