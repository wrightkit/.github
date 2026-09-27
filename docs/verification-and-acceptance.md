# Verification and acceptance

This document defines how WrightKit decides that substantive behavior work is
accepted: the verification boundary established before implementation,
merge-time CI acceptance, independent falsification of material changes, and
what a behavior-changing pull request makes reviewable. Load it when
establishing the checks that decide completion, verifying a material change,
or preparing or reviewing such a pull request.

It is part of the [testing policy](testing-policy.md), whose core principles
also apply.

## Establish the verification boundary before implementation

For machine-verifiable behavior, the executable checks that decide completion
should exist, or have a defined place in the owning repository's test harness,
before implementation capacity for that behavior is expanded. Task admission,
missing harnesses, and the rationale are in
[`issue-readiness.md`](issue-readiness.md#verifiable-outcomes).

- Existing coverage is the boundary when it would already fail on a plausible
  wrong implementation of the requested behavior. Pure refactors, mechanical
  migrations, removals, and changes already protected by existing tests rely
  on that coverage; do not author a duplicate failing test only to satisfy
  this rule.
- New feature-specific cases belong in the owning repository's existing
  harness and may land in the same change as the implementation. Strict
  test-first ordering is not required.
- The tests and checks that constitute merge-time acceptance should run in the
  repository's CI. A check that can only run locally or by hand is reported in
  the PR as such and is not a merge gate. Each repository chooses its own CI
  topology under [`ci-platform.md`](ci-platform.md).
- Green CI establishes acceptance only as far as the boundary reaches. When
  the checks do not cover an acceptance criterion or important failure path,
  report that gap instead of treating the passing run as proof.

## Independently verify material changes

For material semantic, compatibility, compiler, parser, source-edit, or
protocol changes, acceptance should include an independent attempt to falsify
the implementation rather than only rerunning tests authored with it.

State a concrete claim, identify the contract or reference that defines the
expected behavior, and choose the narrowest check that would fail if the claim
were false. Where meaningful, compare pre-change and post-change behavior under
equivalent conditions and compare the result with the independent reference.

Independence comes from the reference, not from who runs the check. Rerunning
the same green command, or having another agent re-read the change, is not an
independent check. The Engineer performs this falsification as part of normal
verification and reports the reference used; PR review or an assigned QA role
provides the second pass, not an ad-hoc verifier agent.

When a new development failure escapes existing tests, add a regression in the
owning feature's established test structure where practical.

## Pull request expectations

A PR that changes observable behavior should make the following reviewable when
applicable:

- the contract, expected output, or reference comparison defining the behavior;
- the regression or capability being protected;
- relevant positive and negative coverage;
- known limitations or remaining gaps;
- the reason for any changed expected result or support classification;
- the required local, CI, runtime, or workflow validation.

Tests must not be weakened, removed, broadly ignored, or reclassified solely to
obtain a green CI result. Temporary command output, screenshots, benchmark
dumps, and one-off reports are not durable tests and should not be committed.
