# Mechanical guards

Context: for anyone changing the git hooks, the agent tool-call hook, or the size limits.

A rule that a script can decide belongs in a script, not in a prompt. Rules that need judgment stay in review.

## Layers

| Layer | Runs | Covers | Source |
| --- | --- | --- | --- |
| Global `pre-push` | every push, any repository on the machine | a branch whose PR is already merged and that has no open PR (needs `gh`; skipped offline); every update of `main` or `master` through the [default-branch gate](#default-branch-gate) | `~/.git-hooks/pre-push`; `~/.git-hooks/merged-branch-guard.sh` and `~/.git-hooks/main-push-guard.sh` are symlinks to the scripts of the same name in `scripts/guards/` |
| Global `pre-commit` | every commit, any repository on the machine | size limits, `git diff --cached --check` | `~/.git-hooks/pre-commit`; `~/.git-hooks/size-guard.sh` is a symlink to `scripts/guards/size-guard.sh` |
| Workspace `pre-commit` / `pre-push` | commits and pushes in repositories beside this checkout | scratch files; for Rust, `rustfmt --check`, `Cargo.lock` agreement with `Cargo.toml`, and a clippy compile check on the declared `rust-version` | `scripts/guards/pre-commit`, `scripts/guards/pre-push`; a repository adds its own checks in `.githooks-local/pre-commit` |
| Agent tool-call hook | before and after agent tool calls | `rm`, hook bypass, force-push to `main` or `master`, `git push --mirror`, push of a merged-PR branch, force-push to other branches is allowed, large reads, oversized writes; adds the owning policy document to the agent's context once per session when an edit or command needs it (agent guidance files, tests and fixtures, workflows, guards, PR review, tags and releases) | `scripts/guards/agent-hook.py` |

The git layer is the only one every agent and human passes through. The tool-call hook acts earlier and costs fewer tokens, but only for agents that support hooks. Register it with `scripts/guards/install-agent-hooks.py`; it covers Claude Code, Codex, and Devin, and Grok reads the Claude registration. Codex asks for hook trust on first start.

## Default-branch gate

`scripts/guards/main-push-guard.sh` judges every push that updates `main` or `master`. The push passes only when all of these hold:

- it is a fast-forward and not a deletion;
- the pushed commit is the checked-out `HEAD` and no tracked file differs from it;
- the repository's executable `.githooks-local/pre-push-main` exits 0.

`.githooks-local/pre-push-main` runs the repository's full local gate, the same checks that its CI requires. A repository without that file accepts changes only through a PR. A GitHub rule that requires a PR still rejects the push after the gate passes.

Why: a direct push skips PR CI and review, so the same checks must pass on the exact commit before it leaves the machine. Whether a change may skip review is a judgment, and stays in [`AGENTS.md`](../AGENTS.md#delivery-is-part-of-completion).

## Size limits

| File | Lines | Tokens (bytes / 4) |
| --- | --- | --- |
| Source, tests, other Markdown | 800 | 10,000 |
| `AGENTS.md`, `CLAUDE.md`, `LESSONS.md` | 200 | 4,000 |

A new file over a limit fails. A file already over a limit may shrink but not grow compared with HEAD. Generated files, `fixtures/`, `snapshots/`, `CHANGELOG.md`, and vendored or build directories are exempt.

Why: a large file costs tokens on every read and spreads the agent's attention. A no-growth rule stops further decay without blocking unrelated work on legacy files.

## Adding a rule

Add a rule only when a script can decide it with no false positives on correct work. Put the check in `scripts/guards/` and cover it in `test_agent_hook.py` or a script test. A lesson that stays judgment-based remains in `LESSONS.md` or review.
