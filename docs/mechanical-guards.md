# Mechanical guards

Context: for anyone changing the git hooks, the agent tool-call hook, or the size limits.

A rule that a script can decide belongs in a script, not in a prompt. Rules that need judgment stay in review.

## Layers

| Layer | Runs | Covers | Source |
| --- | --- | --- | --- |
| Global `pre-commit` | every commit, any repository on the machine | size limits, `git diff --cached --check` | `~/.git-hooks/pre-commit`; `~/.git-hooks/size-guard.sh` is a symlink to `scripts/guards/size-guard.sh` |
| Workspace `pre-commit` / `pre-push` | commits and pushes in repositories beside this checkout | scratch files, compile check on the declared `rust-version` | `scripts/guards/pre-commit`, `scripts/guards/pre-push` |
| Agent tool-call hook | before and after agent tool calls | `rm`, hook bypass, force or default-branch push, large reads, oversized writes | `scripts/guards/agent-hook.py` |

The git layer is the only one every agent and human passes through. The tool-call hook acts earlier and costs fewer tokens, but only for agents that support hooks. Register it with `scripts/guards/install-agent-hooks.py`; it covers Claude Code, Codex, and Devin, and Grok reads the Claude registration. Codex asks for hook trust on first start.

## Size limits

| File | Lines | Tokens (bytes / 4) |
| --- | --- | --- |
| Source, tests, other Markdown | 800 | 10,000 |
| `AGENTS.md`, `CLAUDE.md`, `LESSONS.md` | 200 | 4,000 |

A new file over a limit fails. A file already over a limit may shrink but not grow compared with HEAD. Generated files, `fixtures/`, `snapshots/`, `CHANGELOG.md`, and vendored or build directories are exempt.

Why: a large file costs tokens on every read and spreads the agent's attention. A no-growth rule stops further decay without blocking unrelated work on legacy files.

## Adding a rule

Add a rule only when a script can decide it with no false positives on correct work. Put the check in `scripts/guards/` and cover it in `test_agent_hook.py` or a script test. A lesson that stays judgment-based remains in `LESSONS.md` or review.
