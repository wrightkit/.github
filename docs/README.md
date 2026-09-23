# WrightKit shared documentation

This directory is the progressive-disclosure entry point for WrightKit-wide durable documentation.
The repository root [README](../README.md) stays concise and routes here; load only the policy or
contract relevant to the task.

## Product direction

- [WrightKit goal](goal.md) — durable product intent, priorities, success outcomes, and deliberate non-goals.

## Engineering policy

- [Documentation management](documentation.md) — documentation layout, progressive disclosure, synchronization, and drift audits.
- [Engineering quality](engineering-quality.md) — implementation quality, simplicity, locality, readability, and durable-vs-dynamic knowledge.
- [Issue readiness and PR audit](issue-readiness-and-pr-audit.md) — task readiness, public-boundary changes, and one-pass review.
- [Testing policy](testing-policy.md) — tests, fixtures, compatibility checks, and independent verification.
- [Entropy policy](entropy-policy.md) — removal, consolidation, and post-wave cleanup.

## CI and release

- [CI platform](ci-platform.md) — shared CI platform boundaries.
- [Rust CI](rust-ci.md) — Rust job composition, caching, and toolchains.
- [Rust build artifacts](rust-build-artifacts.md) — local/worktree build storage.
- [Release engineering](release-engineering.md) — tagging, packaging, and publication.

## Agents and cloud execution

- [Agent guidance](agent-guidance.md) — durable agent-instruction design.
- [Codex Cloud](codex-cloud.md) — WrightKit shared-context bootstrap and cloud workspace routing.

Repository-local documentation remains authoritative for repository-specific contracts. ADRs preserve
decision history; source, tests, CI, releases, Issues, and PRs establish current execution reality.
