# WrightKit shared GitHub guidance

This repository contains organization-wide product intent, engineering policy, CI/release standards, and workspace agent routing.

Reusable WrightKit agent skills are owned by the sibling [`wrightkit/.agents`](https://github.com/wrightkit/.agents) repository and are expected at `.agents/skills` in the WrightKit workspace.

## Organization guidance

- [WrightKit goal](docs/goal.md): durable product intent, priorities, success outcomes, and deliberate non-goals. Read this first when a product or implementation tradeoff is unclear.
- [Workspace agent routing](AGENTS.md): organization-level routing entry point; routes agents to the right policy, skill, or repository-local guidance.
- [Claude Code entry point](CLAUDE.md): loads the goal and `AGENTS.md`, then adds Claude-specific guidance for long runs and subagents. Claude Code reads `CLAUDE.md` rather than `AGENTS.md`, so the workspace root needs a `CLAUDE.md` that imports the local workspace `AGENTS.md` (if any) and `@.github/CLAUDE.md`. Imports resolve relative to the importing file, so the imports inside `.github/CLAUDE.md` keep resolving from `.github/`.

## Documentation

Engineering policy, CI, release, and agent documentation are indexed in [docs/README.md](docs/README.md).
