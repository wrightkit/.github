---
name: wrightkit-rust-engineering-review
description: Review non-trivial WrightKit Rust changes for architectural and maintainability risks in ownership/state, public APIs, errors, async/concurrency, abstraction cost, dependencies, and entropy. Use for Rust architecture, API, concurrency, or large-refactor review; not for trivial edits or routine mechanical checks.
---

# WrightKit Rust Engineering Review

Use this skill when a change needs engineering judgment beyond syntax and
mechanical correctness: Rust architecture or API review, concurrency design,
large refactors, or agent-generated code whose structure may have grown more
complex than the task requires. Do not load it for a small local edit, or just
because a Rust file changed.

The compiler and ordinary gates prove important things, but compile-clean code
can still be architecturally wrong, unnecessarily coupled, or over-engineered.
Review the design against the repository's actual contracts and consumers.

## Authority and boundary

- Read the nearest `AGENTS.md`, repository-local architecture/contracts, and
  the changed code's owner and consumers first.
- Route general simplicity, DRY, demonstrated-abstraction, and maintenance
  decisions to [Issue #14](https://github.com/wrightkit/.github/issues/14) and
  the [Code Entropy Policy](../../docs/entropy-policy.md). Do not duplicate
  those policies or impose universal Rust patterns.
- Treat existing public, protocol, persisted, compatibility, security, and
  cross-repository contracts as evidence, not obstacles to be redesigned for
  convenience.
- Do not treat `rustc`, `cargo check`, Clippy, rustfmt, or tests as a
  substitute for this structural review. This skill does not prescribe or
  repeat those routine procedures; use repository CI/local validation as
  supporting evidence and focus here on design.

## Review dimensions

Inspect the delta and trace the relevant callers, boundaries, and lifecycle.
Raise a concern only when there is concrete evidence of a contract, ownership,
correctness, resource, or maintenance problem.

- **Ownership and state:** Look for cloning or ownership transfer used to avoid
  defining a clearer boundary; `Arc`, locks, interior mutability, or shared
  state without a demonstrated concurrency or lifetime need; and state whose
  owner, transition, cleanup, or mutation authority is unclear.
- **Visibility and public API:** Look for widened visibility, leaked
  implementation state, or traits/generics/enums/configuration added without a
  real caller or stable contract. Check whether the API forces needless
  lifetime, error, feature, or conversion complexity on consumers.
- **Errors:** Check that reusable/library boundaries retain meaningful domain
  and context information. Flag premature generic erasure, duplicate
  translation layers, or `panic`/`unwrap`/`expect` where failure is part of a
  recoverable contract; accept an operation-specific invariant when it is
  explicit and actually enforced.
- **Async and concurrency:** Check for blocking work in async paths, guards or
  resources held across `.await` without a reason, unnecessary spawning,
  channels, or parallelism, and unclear task ownership, cancellation, shutdown,
  or result arbitration.
- **Abstraction, dependency, and feature cost:** Check one-use helpers and
  manager/service/context/adapter chains, speculative extension points, and
  dependencies or feature flags added without a demonstrated requirement.
  Consider the whole cost—ownership, callers, MSRV/targets, feature graph,
  compile/binary impact, maintenance, and security—not just deleted lines.
- **Entropy:** Look for duplicate truths, redundant lifecycle mechanisms,
  compatibility residue, dead support surfaces, and layers that merely move
  complexity. Prefer a justified deletion or simpler canonical owner when it
  preserves the actual contract.

Keep a real architectural concern separate from style preference. A different
formatting choice, familiar idiom, or reviewer taste is not a finding unless it
causes a concrete effect on a named contract, consumer, lifecycle, failure
mode, or maintenance obligation. If evidence is missing, label the item as a
question or hypothesis rather than asserting a defect.

## Severity and output

Report findings in severity order:

- **P0 / blocker:** concrete contract or correctness risk, unsoundness,
  recoverability/data-integrity failure, security boundary violation, or
  uncontrolled resource/task lifecycle.
- **P1 / significant:** demonstrated ownership/API boundary failure or
  substantial unnecessary state, concurrency, dependency, or abstraction cost
  with a simpler viable design.
- **P2 / local:** evidence-backed, localized simplification or maintainability
  issue that does not currently break a contract.
- **Preference / hypothesis:** not a finding; record only if useful and state
  what evidence would resolve it.

For each finding, use:

```text
[P0|P1|P2] <short title>
Concern: <specific design problem>
Evidence: <owner, consumer, contract, lifecycle, or diff evidence>
Impact: <observable risk or maintenance cost>
Recommendation: <smallest appropriate correction>
```

Then report simplification opportunities separately, including what can be
deleted, merged, or returned to its canonical owner; the evidence that it is
not load-bearing; the net maintenance reduction; any lost capability or
trade-off; and the smallest decisive validation. End with either
`No architectural findings` or the remaining findings, and state unresolved
evidence instead of inferring safety from a green compile.
