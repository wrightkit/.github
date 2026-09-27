# WrightKit for Claude Code

@docs/goal.md
@AGENTS.md

The two imported files are the shared contract for every agent. This file adds only what is specific to Claude Code and current Claude models, following [`docs/agent-guidance.md`](docs/agent-guidance.md). Where anything here seems to differ, `AGENTS.md` and the policy it routes to take precedence.

## Long runs

- The finish line is the Issue's acceptance criteria plus delivery as defined in `AGENTS.md`. Work to it without check-ins; stop only under [When to stop](AGENTS.md#when-to-stop).
- Gather starting context in one batch: the Issue with its comments, parent, and linked Issues and PRs, the nearest `AGENTS.md`, and the code the change touches. Make independent reads and searches as parallel tool calls.
- For work with more than a handful of steps, keep a checklist in a scratch file outside the repository. Tick items as they finish and add what you discover. After context compaction, re-read the file rather than relying on the summary. Never commit it.
- Commit messages, PR bodies, and review comments explain a decision in a few sentences when the reader needs it. They do not reproduce your reasoning process.

## Subagents

- Split broad read-only investigation across subagents when it divides cleanly by owner, such as an entropy or documentation drift audit across repositories or crates, or finding every consumer of a boundary across the workspace. Give each a self-contained prompt with the question, the scope, and the evidence to return: paths with line numbers or command output.
- Check a subagent's evidence before accepting its conclusion. A claim without evidence is a lead to check, not a finding.
- Search, log reading, and test-output summaries can run on a smaller model. Keep design decisions, code edits, and review judgment in the main session.
- Do not use a subagent to verify or review your own change; `AGENTS.md` explains why.
