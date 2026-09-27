# WrightKit Testing Policy

This policy defines organization-wide testing principles for WrightKit
repositories.

Tests should protect contracts and failure behavior that matter to users and
maintainers. They should not merely mirror the implementation that happens to
exist today. Repository-local guidance may add stricter requirements, but it
must not weaken this policy or replace repository-specific contracts and test
commands.

This document is the testing entry point. It holds the principles that apply to
all test work and routes to narrower documents for concerns that only some
changes touch.

## Applicability

This policy applies to changes involving:

- tests and test infrastructure;
- the executable checks that decide completion of substantive behavior work;
- fixtures, snapshots, corpora, and other test data;
- expected outputs and compatibility baselines;
- regression, conformance, and integration checks;
- fuzzing, property testing, and robustness testing;
- public or canonical boundary migrations that replace, hide, or retire an
  accepted contract;
- changes that add, remove, weaken, quarantine, or reclassify test coverage or
  support states.

Workspace and repository guidance should route agents and contributors here
when these concerns are affected. It does not need to be loaded for work that
does not affect them.

## Narrower testing documents

Load these only when the change touches their concern. Each builds on the
principles in this document.

- [Compatibility and reference testing](compatibility-testing.md) — structural
  convergence with the upstream compiler, raw Workshop and locale semantic
  compatibility, oracle-accepted cases recorded as gaps, and real-project
  regressions and corpora.
- [Robustness testing](robustness-testing.md) — adversarial and pathological
  input, uncontrolled failure on user-controlled input, and fuzzing.
- [Verification and acceptance](verification-and-acceptance.md) — the
  verification boundary before implementation, merge-time CI acceptance,
  independent falsification, and pull request expectations.

When replacing, hiding, or retiring a public or canonical boundary, test
surviving accepted capabilities through the replacement boundary itself, as
defined in
[Contract continuity for boundary migrations](issue-readiness.md#contract-continuity-for-boundary-migrations).

## Start from the contract, not the implementation

Every expected result needs an independent source. Depending on the feature,
that source may be:

- reproducible Overwatch Workshop client behavior;
- a pinned upstream compatibility oracle;
- an accepted semantic or public API contract;
- a real-project regression tied to its source repository, revision, and path;
- a deliberately specified invariant or property.

When production behavior and an expected result change in the same change,
explain which contract, reference comparison, or runtime behavior justifies the
new result. A value is not a valid expectation merely because it matches the
current implementation.

Changing a case between match, gap, expected failure, unsupported, or
inconclusive is also a correctness change. Keep the intended behavior and the
reason for the classification visible in the test or its feature-owned data.

## Test counts are not correctness claims

Counts such as `26/26 fixtures passed` and `124 tests passed` are useful
execution summaries, but they do not establish compatibility or correctness by
themselves.

Compatibility and conformance reports should distinguish, where applicable:

- matched behavior;
- known gaps;
- unsupported or out-of-scope behavior;
- unexpected regressions or divergences;
- inconclusive results.

A known reference or contract mismatch must not be reported as a successful
match merely because the implementation reproduces an old failure.

## Test both successful and failing behavior

Important behavior should be tested across positive and negative paths. Select
the cases that matter to the component, such as:

- valid, invalid, incomplete, malformed, ambiguous, and unsupported input;
- boundary values and nesting limits;
- cross-file or project-graph failures;
- missing catalog or locale data;
- dependency, runtime, or process failures.

A test that only proves that an operation did not fail is insufficient when the
semantic result, diagnostic, emitted artifact, mutation, or refusal is part of
the contract.

## Keep failures observable

WrightKit components must not turn failures into silent success. Tests for
important failure paths should follow the behavior through the layer that
exposes it: library, driver, CLI, provider, protocol, or tooling.

Tests should detect regressions such as:

- dropping or ignoring an error;
- converting failure into an empty or default result;
- returning success with missing diagnostics;
- emitting a partial artifact after a failed operation;
- losing the original source path, span, or source mapping;
- accepting an unsupported construct without an explicit support contract.

For public command or protocol surfaces, failure tests should validate the
externally visible result kind, structured diagnostic or refusal, source mapping,
and absence of misleading success output.

## Prefer invariants over duplicated bookkeeping

Derived data should normally be checked through invariants instead of a second
hard-coded total that must be updated with the implementation.

Useful invariant tests include:

- parse -> emit -> parse preserving declared semantics;
- locale conversion preserving canonical identities;
- diagnostics retaining valid source mapping;
- validated source edits remaining atomic;
- malformed input producing a structured failure rather than a panic or silent
  success.

Property and invariant tests are valuable when they protect a broader contract
than a collection of examples. Dynamic facts such as current registry
membership, corpus size, or enum cardinality should not become durable
expectations merely because they are easy to enumerate.

## Make tests resist plausible wrong implementations

A green suite is stronger when a plausible incorrect implementation would fail.
For high-risk code, maintainers should consider mutation-style checks or
equivalent adversarial review, such as verifying that tests fail when:

- a validation condition is inverted or removed;
- an error path is converted to a default value;
- a required diagnostic is dropped;
- a semantic branch returns the wrong identity or result;
- a known gap is reclassified as passing without matching the contract.

Mutation testing is a QA technique, not a mandatory gate for every repository.
Use it when it adds meaningful information about the strength of the tests.

## Keep test layers complementary

Use the smallest useful combination of layers for the repository's
responsibilities. Typical layers include:

1. focused unit and semantic tests;
2. negative and error-propagation tests;
3. property and invariant tests;
4. minimized feature-owned regressions;
5. complete real-world project cases;
6. differential or oracle tests;
7. fuzz or robustness tests;
8. cross-component or end-to-end conformance tests.

A large corpus does not replace focused diagnostics. Hundreds of unit tests do
not replace real-project checks. A feature census does not replace malformed
input and failure-path tests.

## Organize tests by feature and behavior

Select durable tests by the behavior they protect, not mechanically from a code
diff. Prefer, in order:

1. regression tests for real failure classes;
2. public contract tests;
3. integration tests from representative user-facing entry points;
4. property or invariant tests;
5. unit tests for isolated stable logic where they add distinct value.

Every durable test belongs to a stable feature. Within that feature, it may
protect a public contract, invariant, regression, failure mode, or other
observable behavior. Issue, pull-request, and task identifiers are related
history, not test taxonomy: they must not define a test file, module, suite,
case name, or committed test directory. This includes real-project tests,
whose input metadata is defined in
[Compatibility and reference testing](compatibility-testing.md#preserve-real-project-regressions-and-test-data-carefully).

Code changing does not, by itself, require a new test. Add, consolidate, or
remove tests according to the contract and distinct failure mode they protect.
Do not lock current documentation prose, private implementation structure,
helper call counts, or dynamic inventory totals into tests.

## Avoid production pollution

Tests should not normally require new `pub` or `pub(crate)` APIs, test-only
hooks, configuration surfaces, visibility changes, or architectural indirection
solely to observe internals. Prefer an existing public or integration boundary.
If a proposed test needs production structure only for test access, first look
for an existing contract or rewrite the test.

Prefer minimal representative inputs inline. Add a fixture file when it is
shared, large, source-linked, or owned by an established canonical corpus
location. Keep licensing and source attribution with third-party or real-world
inputs, following the owning repository's licensing and attribution
requirements.

## Repository responsibilities

Each repository remains responsible for documenting and implementing its own
test commands, fixture layouts, expected-output format, and CI gates.

In particular:

- canonical Workshop conformance and client-observable behavior belong with the
  repository that owns canonical Workshop semantics;
- source-language compatibility tests belong with the corresponding
  source-language repository;
- protocol conformance belongs to the protocol repository;
- Wright-owned tooling, orchestration, lint, source-edit, and integration
  behavior is tested in Wright.

Cross-repository tests must respect these ownership boundaries rather than
duplicating authoritative semantic data for convenience.

## Non-goals

This policy does not mandate a single Rust test framework, fixture schema,
fuzzing library, mutation-testing tool, coverage percentage, agent topology, or
CI topology for every repository.

It also does not require maximum test quantity. The objective is durable tests,
meaningful failure detection, clear expected outputs, and protection of the
contracts that users and maintainers actually depend on.
