---
name: wrightkit-test-design-review
description: Review proposed or newly added WrightKit tests for contract value, stability, coverage duplication, fixture cost, and production pollution. Return keep, consolidate, rewrite, or delete with a concise rationale; use when deciding whether a code change needs a test or whether an agent-generated test should remain.
---

# WrightKit Test Design Review

Use this skill to decide whether a test protects a meaningful contract, regression, or stable invariant. A code change does not automatically require a new test, and fewer tests is a valid result.

The authoritative rules are the [Testing Policy](../../docs/testing-policy.md) and [Engineering Quality Policy](../../docs/engineering-quality.md). Repository-local guidance may add stricter requirements. This skill reviews test design; it does not replace repository-specific conformance, corpus, or compatibility strategy.

## Review procedure

Follow these checks in order:

1. **State the claim.** Identify the behavior the test is meant to protect, its observable surface, and the independent contract, regression, or invariant that makes it worth preserving. If there is no durable claim, recommend `delete` or `rewrite`.
2. **Find existing coverage.** Search focused unit, negative/error, property/invariant, integration, corpus, oracle, and end-to-end tests. Identify the nearest higher-level coverage and ask whether the proposed test detects a distinct failure mode. Do not recommend a new test before this check.
3. **Choose the smallest useful layer.** Prefer this order of responsibility: real failure-class regression, public contract, representative user-facing integration, property/invariant, then isolated stable unit logic. Keep a lower-level test when it isolates a failure that higher layers cannot detect; otherwise consolidate toward the higher useful surface.
4. **Check stability.** Prefer assertions about stable observable semantics and invariants that survive a correct internal rewrite. Treat current corpus/test counts, upstream membership or names, documentation prose, incidental formatting, private structure, helper call counts, and current enum/domain cardinality as dynamic or incidental unless an independent contract explicitly makes them observable.
5. **Check coupling and cost.** Reject tests whose primary value is locking implementation details or duplicating higher-level behavior. Prefer minimal representative inputs inline. A fixture needs a reason to exist: it is shared, large, provenance-relevant, or owned by an established canonical corpus location.
6. **Check production pollution.** A test should not normally require new `pub`/`pub(crate)` APIs, test-only hooks, configuration surfaces, visibility changes, or architectural indirection solely for test access. If observing internals needs production changes, first test an existing boundary or rewrite the test around the contract.
7. **Return one decision.** Use exactly one of `keep`, `consolidate`, `rewrite`, or `delete`, with a rationale tied to the claim, existing coverage, and failure mode. Do not manufacture a test merely because code changed.

## Decision meanings

- `keep` — the test protects a stable contract or distinct failure mode and is not redundant or unnecessarily coupled.
- `consolidate` — equivalent tests can be reduced or moved to the smallest useful higher-level surface without losing a distinct guard.
- `rewrite` — the intent is valuable, but assertions, inputs, fixtures, or test surface should target the contract rather than mutable facts or internals.
- `delete` — the test has no durable claim, only repeats existing coverage, or would shape production solely for test convenience.

## Output

Return a concise review in this form:

```text
Recommendation: keep | consolidate | rewrite | delete
Rationale: <why this decision follows from the protected behavior>
Claim/contract: <observable behavior, regression, or stable invariant>
Layer: <test layer and why it is the smallest useful one>
Existing coverage: <relevant tests and any distinct failure mode>
Stability/coupling: <stable assertion or dynamic/incidental dependency>
Fixture cost: <inline input or justified canonical fixture>
Production pollution: <none, or the test-only production change it would require>
```

## Evidence admission

This skill does not define an evidence lifecycle, promote artifacts, or create ad-hoc evidence directories. Route fixture, snapshot, report, corpus, and other repository-admission questions to the existing #9 evidence-lifecycle rules in the [Testing Policy §15](../../docs/testing-policy.md#15-verification-evidence-lifecycle-and-repository-admission). Apply that policy's admission criteria; keep single-task proof ephemeral unless the owning maintainer or QA role authorizes canonical integration.
