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
import subprocess
import sys

GUARDS = os.path.dirname(os.path.abspath(__file__))
READ_MAX_BYTES = 40_000  # ~10k tokens at bytes / 4
SKIP_READ_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ipynb"}

BASH = {"bash", "shell", "run_terminal_command", "execute_bash", "local_shell"}
READ = {"read", "read_file"}
WRITE = {"edit", "write", "multiedit", "search_replace", "notebookedit"}
PATCH = {"apply_patch"}

CMD_START = r"(?:^|[;&|(]\s*|\bsudo\s+|\bxargs\s+|\bexec\s+)"
COMMAND_RULES = [
    (re.compile(CMD_START + r"rm\b"), "Never use `rm`. Move files to the Trash with `trash <path>`."),
    (re.compile(CMD_START + r"unlink\b|\bfind\b[^;&|]*-delete\b|\bgit\s+clean\b"),
     "Permanent deletion is not allowed. Use `trash <path>`."),
    (re.compile(r"\bgit\s+(?:commit|push)\b[^;&|]*(?:--no-verify\b|\s-n\b)"),
     "Do not bypass git hooks (`--no-verify`). Fix the reported problem instead."),
    (re.compile(r"\bgit\s+push\b[^;&|]*(?:--force\b|--force-with-lease\b|\s-f\b|\s\+\S)"),
     "Do not force-push unless the user explicitly asked for it."),
    (re.compile(r"\bgit\s+push\b[^;&|]*\s(?:\S+:)?(?:main|master)\b"),
     "Do not push to the default branch. Push a task branch and open a PR."),
]


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


def check_command(command):
    for pattern, message in COMMAND_RULES:
        if pattern.search(command):
            deny(f"blocked: {message}")


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
            check_command(str(pick(tool_input, "command", "cmd") or ""))
        elif tool in READ:
            check_read(tool_input, cwd)
    elif name == "PostToolUse":
        if tool in WRITE:
            path = pick(tool_input, "file_path", "filePath", "path", "notebook_path")
            check_written([path] if path else [], cwd)
        elif tool in PATCH:
            patch = pick(tool_input, "patch", "input", "command")
            check_written(patch_paths(patch) if isinstance(patch, str) else [], cwd)


if __name__ == "__main__":
    main()
