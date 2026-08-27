# Issue Readiness and One-Pass PR Audit

This document defines the WrightKit-wide workflow for deciding whether an issue
is ready for implementation and for auditing the resulting PR. It makes the
PM/Architect/Engineer/QA boundary explicit without requiring every task to use
all four roles or creating an autonomous issue-to-PR system.

The intended model is agent-compatible, not agent-autonomous: humans or
Architects decide unresolved product and architecture questions; Engineer
agents implement a settled contract; reviewers audit the complete result.

## Issue readiness

Readiness describes the state of the issue's contract, not the confidence of an
agent or the presence of a particular GitHub label. A repository may represent
these states with labels, fields, issue sections, or another explicit mechanism
as long as the meaning remains discoverable.

Use the following semantic states:

- **`needs-design`** — an architectural, ownership, public-contract, or
  compatibility decision is unresolved. An Engineer should not choose the
  design by implementation convenience; route the question to the appropriate
  Architect or owning repository.
- **`needs-decision`** — a product, user-visible behavior, priority, or other
  non-architectural choice is unresolved. An Engineer should not select a
  behavior and present it as implementation of the issue.
- **`blocked`** — the contract is sufficiently decided, but an external
  dependency, owner, access requirement, or prerequisite prevents the work.
  Record the dependency and the condition that will unblock it.
- **`ready-for-implementation`** — the issue contains enough settled scope and
  contract information for an Engineer to implement it without inventing a
  product or architecture decision. Implementation details may remain open.

An issue can move back from `ready-for-implementation` when new evidence or a
scope change reopens a design, product, or dependency question. Do not hide an
unresolved decision inside an apparently ready issue; name the decision and
route it to its owner first.

## Minimum implementation contract

An issue marked `ready-for-implementation` should make the following
discoverable when applicable:

- **Problem / desired behavior** — what is wrong or what user/operator outcome
  is wanted.
- **Scope** — the behavior, surfaces, repositories, or workflows included.
- **Non-goals** — nearby work intentionally excluded from this issue.
- **Constraints** — relevant architecture, ownership, compatibility, security,
  or public-contract boundaries. Link to stable policy instead of copying it.
- **Acceptance criteria** — observable conditions that determine whether the
  issue is complete, including important failure or unsupported paths.
- **Dependencies / ownership boundaries** — prerequisites, owning components,
  and any required cross-repository coordination.

This is a discoverability contract, not an implementation specification. An
issue should not prescribe code structure, helper names, file layout, or a
future abstraction unless that detail is itself an accepted contract. Existing
repository guidance remains authoritative for stable engineering, testing,
entropy, CI, release, and compatibility rules.

If one of these sections is not applicable, the issue need not manufacture
content for it. If it is material but unknown, the issue is not ready and
should identify whether it needs design, a product decision, or an external
dependency.

## Engineer defaults

For implementation work, an Engineer should:

1. Read the linked issue, this workflow, and the nearest repository guidance
   before changing code. Load specialized policy or skills only when the change
   touches their concern.
2. Check that the issue is `ready-for-implementation` in substance. Do not
   self-authorize an unresolved design or product decision; stop and route it
   to the responsible owner.
3. Inspect the existing implementation, abstractions, tests, and ownership
   boundaries before adding a new path or abstraction.
4. Make the smallest complete change that satisfies the issue and its existing
   architecture.
5. Keep unrelated cleanup, refactoring, renaming, and speculative
   extensibility out of the change. If useful follow-up work is discovered,
   record it separately rather than expanding the issue.
6. Start with narrow, decisive local verification. Route deeper testing,
   compatibility, entropy, Rust-architecture, or falsifiable-verification
   work to the canonical policy or specialist workflow when applicable.
7. Report material assumptions, limitations, and remaining gaps against the
   acceptance criteria. A green build or test command does not resolve an
   undecided contract.

These defaults complement [`docs/engineering-quality.md`](engineering-quality.md)
and do not replace repository-local architecture or contribution guidance.

## One-pass PR audit

A reviewer or QA agent audits the entire issue and PR scope in one pass before
reporting the review result. Finding a blocker in one area does not end the
audit: continue through the remaining applicable areas and report all currently
discoverable blockers together. Do not use blocker-by-blocker “toothpaste”
review, where each fix reveals a basic review category that could have been
checked in the original pass.

The audit covers, as applicable:

1. **Issue contract** — scope, non-goals, readiness state, and every acceptance
   criterion.
2. **Correctness and regressions** — intended behavior, error and unsupported
   paths, and regressions at the user-facing or contract boundary.
3. **Architecture and public contracts** — ownership, dependency direction,
   compatibility, API/protocol/schema, security, and repository-local rules.
4. **Test design** — whether coverage protects a meaningful contract or failure
   mode, whether negative paths are covered where material, and whether tests
   are redundant or coupled to implementation details.
5. **Complexity and entropy** — unnecessary abstractions, duplicate truth,
   compatibility residue, unrelated cleanup, and maintenance cost.
6. **Repository hygiene** — generated artifacts, temporary evidence, stale
   references, scope creep, and accidental changes outside the owning surface.
7. **CI, release, and compatibility impact** — affected gates, downstream
   consumers, release behavior, and evidence required beyond local execution.

Only applicable categories need findings. Group findings by severity or action,
for example:

- **Blockers / required changes** — acceptance, correctness, contract, safety,
  ownership, or verification failures that prevent acceptance.
- **Important non-blocking findings** — material risks or maintainability issues
  that should be addressed or explicitly accepted.
- **Suggestions** — optional improvements that do not block the issue.

State the categories checked and the evidence used when the result is clean.
Do not manufacture stylistic findings, and do not approve or merge outside the
repository's normal authorization rules.

## Specialist routing

This document coordinates review; it does not duplicate specialist policy.
Invoke a route only when its trigger is present:

- Route material test-quality or agent-generated-test questions to
  `.agents/skills/wrightkit-test-design-review/SKILL.md` and the canonical
  testing policy. Do not add tests merely because code changed.
- Route high-risk Rust ownership, API, error, async/concurrency, or structural
  questions to `.agents/skills/wrightkit-rust-engineering-review/SKILL.md`.
- Route substantial simplification, deletion, duplication, or abstraction-cost
  questions to [`docs/entropy-policy.md`](entropy-policy.md) and
  `.agents/skills/wrightkit-reclaim-entropy/SKILL.md`.
- Route material changes requiring a falsifiable independent verification to
  `.agents/skills/wrightkit-verify-change/SKILL.md` and the canonical testing
  policy.

Do not load every specialist route for a trivial change. The issue contract and
the nearest repository guidance remain the starting point; specialist review
is demand-driven by the actual risk surface.
