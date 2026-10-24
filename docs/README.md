# WrightKit shared documentation

This directory is the progressive-disclosure entry point for WrightKit-wide durable documentation.
The repository root [README](../README.md) stays concise and routes here; load only the policy or
contract relevant to the task.

## Product direction

- [WrightKit goal](goal.md) — durable product intent, priorities, success outcomes, and deliberate non-goals.

## Engineering policy

- [Coding standards (reviewer entry point)](../CODING_STANDARDS.md) — routes reviewers to the owning policy and lists the recurring judgment criteria.
- [Documentation management](documentation.md) — documentation layout, progressive disclosure, synchronization, and drift audits.
- [Engineering quality](engineering-quality.md) — implementation quality, simplicity, locality, readability, and durable-vs-dynamic knowledge.
- [Issue readiness and implementation preflight](issue-readiness.md) — task readiness, verifiable outcomes, public-boundary continuity, and the issue closing boundary.
- [PR review and review-fix handoff](pr-review.md) — one-pass review, findings, thread handling, and re-review.
- [Testing policy](testing-policy.md) — testing entry point: core test principles, test organization, fixtures, and routing to the narrower testing documents.
  - [Compatibility and reference testing](compatibility-testing.md) — upstream-compiler structural convergence, raw Workshop/locale semantic compatibility, oracle gaps, and real-project regressions and corpora.
  - [Robustness testing](robustness-testing.md) — adversarial input and fuzzing.
  - [Verification and acceptance](verification-and-acceptance.md) — verification boundaries, merge-time CI acceptance, independent verification, and PR expectations.
- [Entropy policy](entropy-policy.md) — removal, consolidation, and post-wave cleanup.

## CI and release

- [CI platform](ci-platform.md) — shared CI platform boundaries.
- [Rust CI](rust-ci.md) — Rust job composition, caching, toolchains, and runtime-bound gates.
- [Rust build artifacts](rust-build-artifacts.md) — local/worktree build storage.
- [Release engineering](release-engineering.md) — tagging, packaging, and publication.
- [CI/release reuse audit, October 2026](ci-release-audit-2026-10.md) — point-in-time evidence and follow-up routing for `wrightkit/.github#49`; contracts remain in the documents above.

## Agents and cloud execution

- [Agent guidance](agent-guidance.md) — durable agent-instruction design.
- [Mechanical guards](mechanical-guards.md) — git hooks, agent tool-call hook, and file size limits.
- [Engineering principles](principles/README.md) — index of named engineering judgments, how to name them in work, and when a constraint belongs in code instead.
- [Codex Cloud](codex-cloud.md) — WrightKit shared-context bootstrap and cloud workspace routing.

Repository-local documentation remains authoritative for repository-specific contracts. ADRs preserve
decision history; source, tests, CI, releases, Issues, and PRs establish current execution reality.
