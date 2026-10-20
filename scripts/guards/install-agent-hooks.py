#!/usr/bin/env python3
"""Register agent-hook.py in every installed agent's user-level hook config.

Claude Code, Codex, and Devin share one hook JSON shape. Grok reads
~/.claude/settings.json itself, so registering Claude also covers Grok.
Run with --dry-run to preview, --uninstall to remove. Idempotent.
"""
import argparse
import datetime
import json
import os
import shutil
import sys

HOME = os.path.expanduser("~")
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent-hook.py")
MARKER = "agent-hook.py"
MATCHER = "Bash|Read|Edit|Write|MultiEdit|NotebookEdit|apply_patch|shell|run_terminal_command|read_file|search_replace"
# A missing script must not block tool calls: python exits 2 on a missing file.
COMMAND = f"test -f '{SCRIPT}' || exit 0; exec python3 -I '{SCRIPT}'"
TARGETS = {
    "claude (also read by grok)": os.path.join(HOME, ".claude", "settings.json"),
    "codex": os.path.join(HOME, ".codex", "hooks.json"),
    "devin": os.path.join(HOME, ".config", "devin", "config.json"),
}
EVENTS = ("PreToolUse", "PostToolUse")


def is_ours(group):
    return any(MARKER in h.get("command", "") for h in group.get("hooks", []))


def update(config, install):
    hooks = config.setdefault("hooks", {})
    for event in EVENTS:
        groups = [g for g in hooks.get(event, []) if not is_ours(g)]
        if install:
            groups.append({"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND, "timeout": 20}]})
        if groups:
            hooks[event] = groups
        else:
            hooks.pop(event, None)
    if not hooks:
        config.pop("hooks")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()

    for name, path in TARGETS.items():
        if not os.path.isdir(os.path.dirname(path)):
            print(f"skip   {name}: {os.path.dirname(path)} not found")
            continue
        before = open(path).read() if os.path.exists(path) else "{}"
        config = json.loads(before)
        update(config, not args.uninstall)
        after = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
        if json.loads(before) == config:
            print(f"ok     {name}: already up to date")
            continue
        if args.dry_run:
            print(f"would  {name}: update {path}")
            continue
        if os.path.exists(path):
            shutil.copy2(path, f"{path}.bak-{datetime.date.today():%Y%m%d}")
        with open(path, "w") as f:
            f.write(after)
        print(f"wrote  {name}: {path}")


if __name__ == "__main__":
    sys.exit(main())
