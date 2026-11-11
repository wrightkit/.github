#!/usr/bin/env python3
"""Tool-call guard shared by every coding agent that speaks Claude-style hooks.

Claude Code, Codex, Grok, and Devin send a JSON event on stdin and treat
exit code 2 as "block, show stderr to the model". Tool and field names differ
between agents, so this script normalizes them. Decidable rules only; judgment
rules stay in review.
"""
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

GUARDS = os.path.dirname(os.path.abspath(__file__))
READ_MAX_BYTES = 40_000  # ~10k tokens at bytes / 4
SKIP_READ_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ipynb"}

BASH = {"bash", "shell", "exec", "run_terminal_command", "execute_bash", "local_shell"}
READ = {"read", "read_file"}
WRITE = {"edit", "write", "multiedit", "search_replace", "notebookedit"}
PATCH = {"apply_patch"}
DEFAULT_BRANCHES = {"main", "master"}
GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
PUSH_VALUE_OPTIONS = {"--repo", "-o", "--push-option", "--receive-pack", "--exec"}
COMMIT_VALUE_OPTIONS = {"-m", "--message", "-F", "--file", "-C", "-c", "--author", "--date"}

WRAPPERS = {"sudo", "xargs", "exec", "env", "command", "nohup", "time"}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?^\s*\2$", re.M | re.S)


def pick(d, *keys):
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return None


def deny(message, post=False):
    sys.stderr.write(message + "\n")
    if post:
        sys.stdout.write(json.dumps({"decision": "block", "reason": message}))
    sys.exit(2)


def repo_relative(path, cwd):
    path = path if os.path.isabs(path) else os.path.join(cwd, path)
    directory = os.path.dirname(path) or "."
    if not os.path.isdir(directory):
        return None, None
    top = subprocess.run(
        ["git", "-C", directory, "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if top.returncode != 0:
        return None, None
    root = top.stdout.strip()
    return root, os.path.relpath(os.path.realpath(path), os.path.realpath(root))


def shell_segments(command):
    """Split a shell command into argv lists, one per simple command.

    Heredoc bodies and quoted strings are data, so only real command words
    reach the rules below.
    """
    lexer = shlex.shlex(HEREDOC.sub("", command), posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace_split = True
    lexer.whitespace = " \t\r"
    try:
        tokens = list(lexer)
    except ValueError:
        return []
    segments, current = [], []
    for token in tokens:
        if set(token) <= set(";&|()\n"):
            segments.append(current)
            current = []
        else:
            current.append(token)
    segments.append(current)
    return segments


def deletion_message(seg):
    i = 0
    while i < len(seg) and (seg[i] in WRAPPERS or re.fullmatch(r"\w+=.*", seg[i])):
        i += 1
    if i >= len(seg):
        return None
    word, rest = os.path.basename(seg[i]), seg[i + 1:]
    if word == "rm":
        return "Never use `rm`. Move files to the Trash with `trash <path>`."
    if word == "unlink" or (word == "find" and "-delete" in rest) or (word == "git" and "clean" in rest):
        return "Permanent deletion is not allowed. Use `trash <path>`."
    return None


def git_commands(command):
    """Yield (subcommand, args, directory) for each git call in a shell command."""
    for seg in shell_segments(command):
        if "git" not in seg:
            continue
        i, directory = seg.index("git") + 1, None
        while i < len(seg) and seg[i].startswith("-"):
            if seg[i] == "-C" and i + 1 < len(seg):
                directory = seg[i + 1]
            i += 2 if seg[i] in GIT_VALUE_OPTIONS else 1
        if i < len(seg):
            yield seg[i], seg[i + 1:], directory


def current_branch(cwd, directory):
    where = os.path.join(cwd, directory) if directory else cwd
    result = subprocess.run(["git", "-C", where, "branch", "--show-current"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def push_targets(args, cwd, directory):
    positional, skip = [], False
    for arg in args:
        if skip:
            skip = False
        elif arg in PUSH_VALUE_OPTIONS:
            skip = True
        elif not arg.startswith("-"):
            positional.append(arg)
    refspecs = positional[1:]  # first positional is the remote
    names = []
    for refspec in refspecs:
        name = refspec.lstrip("+").split(":")[-1]
        names.append(name.removeprefix("refs/heads/"))
    if not refspecs:
        names.append(current_branch(cwd, directory))
    return [current_branch(cwd, directory) if n == "HEAD" else n for n in names]


def is_force(args):
    for arg in args:
        if arg.startswith(("--force", "+")) or arg == "--mirror":
            return True
        if arg.startswith("-") and not arg.startswith("--") and "f" in arg:
            return True
    return False


def commit_skips_hooks(args):
    skip = False
    for arg in args:
        if skip:
            skip = False
        elif arg in COMMIT_VALUE_OPTIONS:
            skip = True
        elif arg == "--no-verify" or (arg.startswith("-") and not arg.startswith("--") and "n" in arg):
            return True
    return False


def check_git(command, cwd):
    for sub, args, directory in git_commands(command):
        if sub == "commit" and commit_skips_hooks(args):
            deny("blocked: Do not bypass git hooks (`--no-verify`). Fix the reported problem instead.")
        if sub == "push":
            if "--no-verify" in args:
                deny("blocked: Do not bypass git hooks (`--no-verify`). Fix the reported problem instead.")
            on_default = DEFAULT_BRANCHES & set(push_targets(args, cwd, directory))
            if on_default and is_force(args):
                deny(f"blocked: Do not force-push {', '.join(sorted(on_default))}.")
            if on_default or "--mirror" in args:
                deny("blocked: Do not push to the default branch. Push a task branch and open a PR.")
            for branch in push_targets(args, cwd, directory):
                where = os.path.join(cwd, directory) if directory else cwd
                guard = subprocess.run([os.path.join(GUARDS, "merged-branch-guard.sh"), branch or ""],
                                       cwd=where, capture_output=True, text=True)
                if guard.returncode != 0:
                    deny(f"blocked: {guard.stderr.strip()}")


def check_command(command, cwd="."):
    for seg in shell_segments(command):
        message = deletion_message(seg)
        if message:
            deny(f"blocked: {message}")
    check_git(command, cwd)


def check_read(tool_input, cwd):
    path = pick(tool_input, "file_path", "filePath", "path")
    if not path or pick(tool_input, "offset", "limit", "pages", "start_line", "end_line") is not None:
        return
    full = path if os.path.isabs(path) else os.path.join(cwd, path)
    if os.path.splitext(full)[1].lower() in SKIP_READ_EXT or not os.path.isfile(full):
        return
    size = os.path.getsize(full)
    if size <= READ_MAX_BYTES:
        return
    with open(full, "rb") as f:
        if b"\0" in f.read(8192):
            return
    deny(
        f"blocked: {path} is ~{size // 4} tokens. Search it with grep first, "
        "then read only the needed range with offset and limit."
    )


def patch_paths(patch):
    return re.findall(r"^\*\*\* (?:Add|Update) File: (.+)$", patch, re.M)


def check_written(paths, cwd):
    for path in paths:
        root, rel = repo_relative(path, cwd)
        if root is None:
            continue
        result = subprocess.run(
            [os.path.join(GUARDS, "size-guard.sh"), "--worktree", rel],
            cwd=root, capture_output=True, text=True,
        )
        if result.returncode != 0:
            deny(result.stderr.strip() or f"size-guard failed for {rel}", post=True)


DOCS = os.path.normpath(os.path.join(GUARDS, "..", "..", "docs"))
POLICY_FOR_PATH = [
    ("agent-guidance.md", lambda p: os.path.basename(p) in {"AGENTS.md", "CLAUDE.md", "SKILL.md"}),
    ("testing-policy.md", lambda p: bool({"tests", "fixtures"} & set(p.split("/"))) or p.endswith(".snap")),
    ("rust-ci.md", lambda p: "/.github/workflows/" in p),
    ("mechanical-guards.md", lambda p: "/scripts/guards/" in p or "/.git-hooks/" in p),
]
POLICY_FOR_COMMAND = [
    ("pr-review.md", lambda a: a[:3] in (["gh", "pr", "review"], ["gh", "pr", "comment"])),
    ("release-engineering.md", lambda a: a[:2] in (["git", "tag"], ["gh", "release"])),
]


def policies_for_paths(paths, cwd):
    full = [os.path.abspath(os.path.join(cwd, p)) for p in paths if p]
    return [doc for doc, match in POLICY_FOR_PATH if any(match(p) for p in full)]


def policies_for_command(command):
    docs = []
    for seg in shell_segments(command):
        while seg and (seg[0] in WRAPPERS | {"rtk"} or re.fullmatch(r"\w+=.*", seg[0])):
            seg = seg[1:]
        docs += [doc for doc, match in POLICY_FOR_COMMAND if seg and match([os.path.basename(seg[0])] + seg[1:])]
    return docs


def inject(docs, event):
    """Add each policy document to the agent's context once per session."""
    session = re.sub(r"\W", "_", str(pick(event, "session_id", "sessionId") or ""))
    state = os.path.join(tempfile.gettempdir(), "wrightkit-agent-hook", session) if session else None
    seen = set(open(state).read().split()) if state and os.path.exists(state) else set()
    new = [d for d in dict.fromkeys(docs) if d not in seen and os.path.isfile(os.path.join(DOCS, d))]
    if not new:
        return
    parts = []
    for doc in new:
        with open(os.path.join(DOCS, doc), encoding="utf-8") as f:
            parts.append(f"WrightKit policy for this action: .github/docs/{doc} (added once per session)\n\n{f.read()}")
    sys.stdout.write(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "additionalContext": "\n\n".join(parts)}}))
    if state:
        os.makedirs(os.path.dirname(state), exist_ok=True)
        with open(state, "a") as f:
            f.write("".join(d + "\n" for d in new))


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    name = str(pick(event, "hook_event_name", "hookEventName") or "")
    tool = str(pick(event, "tool_name", "toolName") or "").lower()
    tool_input = pick(event, "tool_input", "toolInput") or {}
    cwd = pick(event, "cwd") or os.getcwd()

    if name == "PreToolUse":
        if tool in BASH:
            command = str(pick(tool_input, "command", "cmd") or "")
            check_command(command, cwd)
            inject(policies_for_command(command), event)
        elif tool in READ:
            check_read(tool_input, cwd)
        elif tool in WRITE:
            path = pick(tool_input, "file_path", "filePath", "path", "notebook_path")
            inject(policies_for_paths([path], cwd), event)
        elif tool in PATCH:
            patch = pick(tool_input, "patch", "input", "command")
            inject(policies_for_paths(patch_paths(patch) if isinstance(patch, str) else [], cwd), event)
    elif name == "PostToolUse":
        if tool in WRITE:
            path = pick(tool_input, "file_path", "filePath", "path", "notebook_path")
            check_written([path] if path else [], cwd)
        elif tool in PATCH:
            patch = pick(tool_input, "patch", "input", "command")
            check_written(patch_paths(patch) if isinstance(patch, str) else [], cwd)


if __name__ == "__main__":
    main()
