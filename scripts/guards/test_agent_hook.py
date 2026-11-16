import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent-hook.py")


def run(event, gh_merged=False):
    """Run the hook with a stub `gh` so no test reaches GitHub."""
    with tempfile.TemporaryDirectory() as stub:
        gh = os.path.join(stub, "gh")
        with open(gh, "w") as f:
            f.write('#!/bin/sh\ncase "$*" in *"--state merged"*) [ "$MERGED" = 1 ] && echo 7;; *"--state open"*) echo 0;; esac\n')
        os.chmod(gh, 0o755)
        env = {**os.environ, "PATH": stub + os.pathsep + os.environ["PATH"], "MERGED": "1" if gh_merged else "0"}
        return subprocess.run([sys.executable, "-I", HOOK], input=json.dumps(event), capture_output=True, text=True, env=env)


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

    def test_blocks_deletion_after_newline_or_in_subshell(self):
        for c in ["echo a\nrm x", "(cd build; rm x)", "FOO=1 rm x", "xargs rm", "/bin/rm x"]:
            self.blocked(c)

    def test_allows_deletion_words_in_quotes_and_heredocs(self):
        for c in ["grep 'git clean' notes.md", 'python3 -c "import re; re.compile(\'rm -r\')"',
                  "cat <<'E'\nrm x\ngit clean -fd\nE", "echo unlink", "git log --grep=clean"]:
            self.allowed(c)

    def test_blocks_hook_bypass(self):
        for c in ["git commit -n -m x", "git commit --no-verify -m x", "git commit -anm x", "git push --no-verify"]:
            self.blocked(c)

    def test_blocks_force_push_to_default_branch(self):
        for c in ["git push --force origin main", "git push -f origin master", "git push --force-with-lease origin HEAD:main",
                  "git push origin +main", "git push origin +feat:refs/heads/main", "git push --mirror"]:
            self.blocked(c)

    def test_leaves_plain_push_to_default_branch_to_the_git_gate(self):
        for c in ["git push origin main", "git push origin HEAD:master", "git -C . push origin main"]:
            self.allowed(c)

    def test_allows_force_push_to_other_branches(self):
        for c in ["git push --force origin next", "git push -f origin next", "git push --force-with-lease -u origin feat/x",
                  "git push origin +next", "git push origin HEAD:next --force", "git push -u origin feat/commit-guards"]:
            self.allowed(c)

    def test_blocks_push_of_a_merged_pr_branch(self):
        event = claude("Bash", {"command": "git push -u origin feat/x"})
        result = run(event, gh_merged=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("already merged", result.stderr)
        self.assertEqual(run(event).returncode, 0)

    def test_does_not_mistake_arguments_for_flags(self):
        for c in ["git push -n origin next", "git push --dry-run origin next", 'git commit -m "fix -n handling"',
                  'git commit -m "force push main notes"', "git log --oneline && git status"]:
            self.allowed(c)

    def test_force_push_follows_the_current_branch(self):
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as repo:
            subprocess.run(["git", "init", "-q", "-b", "next", repo], check=True)
            self.assertEqual(run(claude("Bash", {"command": "git push --force"}, cwd=repo)).returncode, 0)
            self.assertEqual(run(claude("Bash", {"command": "git push --force origin HEAD"}, cwd=repo)).returncode, 0)
            subprocess.run(["git", "-C", repo, "checkout", "-q", "-b", "main"], check=True)
            self.assertEqual(run(claude("Bash", {"command": "git push --force"}, cwd=repo)).returncode, 2)
            self.assertEqual(run(claude("Bash", {"command": "git push --force origin HEAD"}, cwd=repo)).returncode, 2)

    def test_other_agent_schemas(self):
        grok = {"hook_event_name": "PreToolUse", "toolName": "run_terminal_command", "toolInput": {"command": "rm -rf x"}}
        self.blocked("", event=grok)
        for tool in ("shell", "exec"):
            self.blocked("", event=claude(tool, {"command": "rm x"}))


class MergedBranchGuard(unittest.TestCase):
    GUARD = os.path.join(os.path.dirname(HOOK), "merged-branch-guard.sh")

    def guard(self, open_prs, merged_pr, branch="feat/x", gh=True):
        with tempfile.TemporaryDirectory() as stub:
            if gh:
                path = os.path.join(stub, "gh")
                with open(path, "w") as f:
                    f.write(f'#!/bin/sh\ncase "$*" in *"--state merged"*) echo "{merged_pr}";; *"--state open"*) echo {open_prs};; esac\n')
                os.chmod(path, 0o755)
            env = {**os.environ, "PATH": stub + os.pathsep + "/usr/bin:/bin"}
            return subprocess.run([self.GUARD, branch], capture_output=True, text=True, env=env).returncode

    def test_blocks_only_merged_branch_without_open_pr(self):
        self.assertEqual(self.guard(0, 7), 1)
        self.assertEqual(self.guard(1, 7), 0)
        self.assertEqual(self.guard(0, ""), 0)
        for long_lived in ("main", "master", "next"):
            self.assertEqual(self.guard(0, 7, branch=long_lived), 0)

    def test_fails_open_without_gh(self):
        self.assertEqual(self.guard(0, 7, gh=False), 0)


class MainPushGuard(unittest.TestCase):
    GUARD = os.path.join(os.path.dirname(HOOK), "main-push-guard.sh")
    ZERO = "0" * 40

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.git("init", "-q", "-b", "main")
        self.base = self.commit("base")
        self.head = self.commit("head")

    def git(self, *args):
        config = ["-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "-c", "user.name=t", "-c", "user.email=t@example.com"]
        return subprocess.run(["git", "-C", self.dir.name, *config, *args], check=True, capture_output=True, text=True).stdout.strip()

    def commit(self, name):
        with open(os.path.join(self.dir.name, name), "w") as f:
            f.write(name + "\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", name)
        return self.git("rev-parse", "HEAD")

    def gate(self, status):
        path = os.path.join(self.dir.name, ".githooks-local", "pre-push-main")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(f"#!/bin/sh\nexit {status}\n")
        os.chmod(path, 0o755)
        self.head = self.commit(f"gate-{status}")

    def push(self, local=None, remote_ref="refs/heads/main", remote=None):
        line = f"refs/heads/main {local or self.head} {remote_ref} {remote or self.base}\n"
        return subprocess.run([self.GUARD], input=line, cwd=self.dir.name, capture_output=True, text=True)

    def test_ignores_other_branches(self):
        self.assertEqual(self.push(remote_ref="refs/heads/feat/x").returncode, 0)
        self.assertEqual(self.push(remote_ref="refs/heads/next").returncode, 0)

    def test_allows_a_repository_without_a_gate(self):
        self.assertEqual(self.push().returncode, 0)
        self.assertEqual(self.push(remote_ref="refs/heads/master").returncode, 0)

    def test_blocks_a_gate_that_cannot_run(self):
        self.gate(0)
        os.chmod(os.path.join(self.dir.name, ".githooks-local", "pre-push-main"), 0o644)
        self.head = self.commit("mode")
        self.assertIn("not executable", self.push().stderr)

    def test_blocks_a_merge_commit(self):
        self.git("checkout", "-q", "-b", "side", self.base)
        self.commit("side")
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", "merge side", "side")
        self.head = self.git("rev-parse", "HEAD")
        self.assertIn("merge commit", self.push().stderr)

    def test_blocks_unfinished_commits(self):
        for subject in ("fixup! base", "squash! base", "amend! base", "WIP", "wip: parser"):
            self.head = self.commit(subject)
            result = self.push()
            self.assertEqual(result.returncode, 1, subject)
            self.assertIn("unfinished commit", result.stderr)
            self.git("reset", "-q", "--hard", "HEAD~1")
        self.head = self.commit("wipe the cache")
        self.assertEqual(self.push().returncode, 0)

    def test_follows_the_repository_gate(self):
        self.gate(0)
        self.assertEqual(self.push().returncode, 0)
        self.assertEqual(self.push(remote=self.ZERO).returncode, 0)
        self.gate(1)
        self.assertEqual(self.push().returncode, 1)

    def test_blocks_deletion_and_non_fast_forward(self):
        self.assertEqual(self.push(local=self.ZERO).returncode, 1)
        self.git("checkout", "-q", "-b", "side", self.base)
        side = self.commit("side")
        self.git("checkout", "-q", "main")
        self.assertIn("fast-forward", self.push(remote=side).stderr)

    def test_blocks_a_commit_that_is_not_the_verified_state(self):
        self.assertIn("checked-out HEAD", self.push(local=self.git("rev-parse", "HEAD~1")).stderr)
        with open(os.path.join(self.dir.name, "base"), "w") as f:
            f.write("changed\n")
        self.assertIn("tracked files", self.push().stderr)


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


class PolicyInjection(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        old = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = tmp.name
        self.addCleanup(lambda: os.environ.__setitem__("TMPDIR", old) if old else os.environ.pop("TMPDIR"))

    def context(self, tool, tool_input, session="s1"):
        event = {**claude(tool, tool_input), "session_id": session}
        result = run(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"] if result.stdout else ""

    def test_edit_triggers_owning_policy(self):
        cases = [("/w/opy-rs/AGENTS.md", "agent-guidance.md"), ("/w/x/tests/a.rs", "testing-policy.md"),
                 ("/w/x/src/a.snap", "testing-policy.md"), ("/w/x/.github/workflows/ci.yml", "rust-ci.md"),
                 ("/w/.github/scripts/guards/pre-push", "mechanical-guards.md")]
        for i, (path, doc) in enumerate(cases):
            self.assertIn(f".github/docs/{doc}", self.context("Edit", {"file_path": path}, session=f"e{i}"), path)

    def test_command_triggers_owning_policy(self):
        cases = [("gh pr review 5 --approve", "pr-review.md"), ("rtk gh pr comment 5 -b x", "pr-review.md"),
                 ("git tag v1.0.0", "release-engineering.md"), ("gh release create v1", "release-engineering.md")]
        for i, (command, doc) in enumerate(cases):
            self.assertIn(f".github/docs/{doc}", self.context("Bash", {"command": command}, session=f"c{i}"), command)

    def test_unrelated_actions_inject_nothing(self):
        self.assertEqual(self.context("Edit", {"file_path": "/w/x/src/lib.rs"}), "")
        self.assertEqual(self.context("Bash", {"command": "echo 'gh pr review'"}), "")

    def test_injects_once_per_session(self):
        self.assertNotEqual(self.context("Edit", {"file_path": "/w/a/AGENTS.md"}), "")
        self.assertEqual(self.context("Edit", {"file_path": "/w/b/SKILL.md"}), "")
        self.assertNotEqual(self.context("Edit", {"file_path": "/w/b/SKILL.md"}, session="s2"), "")

    def test_codex_patch_triggers_policy(self):
        patch = "*** Begin Patch\n*** Update File: /w/x/tests/a.rs\n+x\n*** End Patch"
        self.assertIn("testing-policy.md", self.context("apply_patch", {"patch": patch}))


if __name__ == "__main__":
    unittest.main()
