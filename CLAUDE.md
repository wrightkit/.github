# WrightKit for Claude Code

@docs/goal.md
@AGENTS.md

## Long runs

- For work with more than a handful of steps, keep a checklist in a scratch file outside the repository. Tick items as they finish and add what you discover. After context compaction, re-read the file rather than relying on the summary. Never commit it.
- Commit messages, PR bodies, and review comments explain a decision in a few sentences when the reader needs it. They do not reproduce your reasoning process.

## Subagents

- Split broad read-only investigation across subagents when it divides cleanly by owner, such as an entropy or documentation drift audit across repositories or crates, or finding every consumer of a boundary across the workspace. Give each a self-contained prompt with the question, the scope, and the evidence to return: paths with line numbers or command output.
- Check a subagent's evidence before accepting its conclusion. A claim without evidence is a lead to check, not a finding.
- Search, log reading, and test-output summaries can run on a smaller model. Keep design decisions, code edits, and review judgment in the main session.
