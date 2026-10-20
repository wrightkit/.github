import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent-hook.py")


def run(event):
    return subprocess.run([sys.executable, "-I", HOOK], input=json.dumps(event), capture_output=True, text=True)


def claude(tool, tool_input, event="PreToolUse", cwd="."):
    return {"hook_event_name": event, "tool_name": tool, "tool_input": tool_input, "cwd": cwd}


class CommandRules(unittest.TestCase):
    def blocked(self, command, tool="Bash", event=None):
        result = run(event or claude(tool, {"command": command}))
        self.assertEqual(result.returncode, 2, command)
        self.assertTrue(result.stderr.startswith("blocked:"), result.stderr)

    def allowed(self, command):
        self.assertEqual(run(claude("Bash", {"command": command})).returncode, 0, command)

    def test_blocks_permanent_deletion(self):
        for c in ["rm -rf build", "ls && rm x", "sudo rm x", "find . -name '*.o' -delete", "git clean -fd", "unlink x"]:
            self.blocked(c)

    def test_allows_trash_and_git_rm(self):
        for c in ["trash build", "git rm old.rs", "echo rmdir", "cargo fmt --all"]:
            self.allowed(c)

    def test_blocks_hook_bypass_and_unsafe_push(self):
        for c in ["git commit -n -m x", "git commit --no-verify -m x", "git push --force", "git push origin +topic",
                  "git push -f origin x", "git push origin main", "git push origin HEAD:master"]:
            self.blocked(c)

    def test_allows_task_branch_push(self):
        self.allowed("git push -u origin feat/commit-guards")

    def test_other_agent_schemas(self):
        grok = {"hook_event_name": "PreToolUse", "toolName": "run_terminal_command", "toolInput": {"command": "rm -rf x"}}
        self.blocked("", event=grok)
        codex = claude("shell", {"command": "rm x"})
        self.blocked("", event=codex)


class ReadAndSize(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory(dir=os.getcwd())
        self.addCleanup(self.dir.cleanup)
        subprocess.run(["git", "init", "-q", self.dir.name], check=True)

    def write(self, name, lines):
        path = os.path.join(self.dir.name, name)
        with open(path, "w") as f:
            f.write("".join(f"line {i}\n" for i in range(lines)))
        return path

    def test_read_big_file_requires_range(self):
        path = self.write("big.rs", 6000)
        self.assertEqual(run(claude("Read", {"file_path": path})).returncode, 2)
        self.assertEqual(run(claude("Read", {"file_path": path, "limit": 200})).returncode, 0)

    def test_read_small_file_allowed(self):
        path = self.write("small.rs", 50)
        self.assertEqual(run(claude("Read", {"file_path": path})).returncode, 0)

    def test_oversized_write_blocks_with_feedback(self):
        path = self.write("new.rs", 900)
        result = run(claude("Write", {"file_path": path}, event="PostToolUse"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("over limit", result.stderr)
        self.assertEqual(json.loads(result.stdout)["decision"], "block")

    def test_normal_write_allowed(self):
        path = self.write("ok.rs", 100)
        self.assertEqual(run(claude("Edit", {"file_path": path}, event="PostToolUse")).returncode, 0)

    def test_codex_apply_patch(self):
        path = self.write("p.rs", 900)
        patch = f"*** Begin Patch\n*** Add File: {path}\n+x\n*** End Patch"
        self.assertEqual(run(claude("apply_patch", {"patch": patch}, event="PostToolUse")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
