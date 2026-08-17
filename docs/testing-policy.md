# WrightKit Testing Policy

This document defines organization-wide testing principles for WrightKit repositories.

The policy exists to make tests independent correctness constraints rather than snapshots of the implementation that happens to exist today. This is especially important in AI-assisted development, where production code and tests may be authored together and a green test suite can otherwise drift away from the intended semantic contract.

Repository-local guidance may add stricter or domain-specific requirements, but it must not weaken this policy.

## Applicability

This policy applies to changes involving:

- tests and test infrastructure;
- fixtures, snapshots, and corpora;
- expected results and compatibility baselines;
- regression and conformance evidence;
- fuzzing, property testing, and robustness testing;
- changes that add, remove, weaken, quarantine, or reclassify test coverage or support states.

Workspace and repository guidance should route agents and contributors to this policy when these concerns are affected. It does not need to be loaded for work that does not affect them.

## 1. Evidence before expectations

A correctness expectation must have an identifiable source of truth independent from the implementation under test.

Acceptable evidence includes, as appropriate:

- reproducible Overwatch Workshop client behavior;
- a pinned upstream compatibility oracle;
- an accepted semantic or public API contract;
- a provenance-linked real-world project regression;
- a deliberately specified invariant or property.

Changing production behavior and changing its correctness expectation in the same change is not sufficient evidence by itself. When an expected result changes, the change must identify what external evidence or accepted contract changed.

Changing a case between match, gap, expected failure, unsupported, inconclusive, or an equivalent support state is also a correctness expectation change and requires the same independent evidence.

Fixed expected values are valid when they encode independently established observable behavior. They are not valid merely because they match the current implementation.

## 2. Test counts are not correctness claims

Counts such as `26/26 fixtures passed`, `124 tests passed`, or similar totals are useful execution summaries, but they are not compatibility or correctness evidence on their own.

Compatibility and conformance reporting should be organized around semantic capabilities and evidence states rather than testcase quantity.

Reports should distinguish, where applicable:

- matched behavior;
- known gaps;
- unsupported or out-of-scope behavior;
- unexpected regressions or divergences;
- inconclusive evidence.

A known reference or contract mismatch must not be reported as a successful compatibility match simply because the current implementation reproduces the previously recorded failure.

## 3. Positive and negative behavior are both first-class

Important behavior should be tested across both successful and failing paths.

Depending on the component, tests should cover relevant cases such as:

- valid input;
- invalid input;
- incomplete or truncated input;
- malformed input;
- ambiguous input;
- unsupported input;
- boundary values and nesting limits;
- cross-file or project-graph failures;
- missing catalog or locale data;
- dependency, runtime, or process failures.

A test that only proves "the operation did not fail" is insufficient when the semantic result, diagnostic, emitted artifact, mutation, or refusal is part of the contract.

## 4. Errors must remain observable

WrightKit components must not turn failures into silent success.

Tests for important failure paths should verify propagation through the layers that expose the behavior, for example library, driver, CLI, provider, protocol, or tooling boundaries.

Tests should detect regressions such as:

- dropping or ignoring an error;
- converting failure into an empty or default result;
- returning success with missing diagnostics;
- emitting a partial artifact after a failed operation;
- losing the original source path, span, or provenance;
- accepting an unsupported construct without an explicit support contract.

For public command or protocol surfaces, failure tests should validate the externally visible contract: status/result kind, structured diagnostic or refusal, source attribution, and absence of misleading success output.

## 5. Real projects are permanent evidence

Synthetic unit tests are necessary but are not sufficient for compatibility work.

When a defect is discovered in a real project, preserve a minimized reproduction as a permanent regression fixture whenever practical. The minimized case should retain enough provenance to identify the original repository, immutable revision, and source path or equivalent origin.

Keep project-level corpus coverage where it provides additional evidence for behavior that a minimized fixture cannot exercise, including:

- imports and includes;
- project graphs;
- macros or preprocessing interactions;
- cross-file symbol and type relationships;
- settings and catalog interactions;
- unusual combinations of otherwise supported features.

Minimized regressions and full-project corpus tests are complementary; neither replaces the other.

Third-party fixture inclusion must follow the owning repository's licensing and provenance rules.

## 6. Prefer invariants over duplicated bookkeeping

Derived data should normally be checked through invariants instead of duplicated hard-coded totals that must be manually updated with the implementation.

For example, a support-state summary should be verified against the entries from which it is computed rather than by maintaining a second expected count beside the same data source.

Property and invariant tests are preferred where they can protect a broader contract, including examples such as:

- parse -> emit -> parse preserving declared semantics;
- locale conversion preserving canonical identities;
- diagnostics retaining valid source provenance;
- validated source edits remaining atomic;
- malformed input producing a structured failure rather than a panic or silent success.

## 7. Robustness must be tested adversarially

Parsers, compilers, analyzers, language services, protocol handlers, and agent-facing tools should be tested against hostile or pathological input where relevant.

Useful robustness classes include:

- deep nesting;
- unexpected EOF at syntax boundaries;
- recursive or cyclic imports/includes;
- recursive macro expansion;
- large arrays or strings;
- extreme numeric literals;
- Unicode and encoding boundaries;
- duplicate declarations or identities;
- missing mappings or catalog entries;
- malformed external/process responses;
- resource limits and interruption behavior.

User-controlled input should not cause an uncontrolled panic, abort, hang, or fabricated success result. Explicitly documented resource exhaustion or unsupported behavior is acceptable when surfaced deterministically.

Fuzzing is encouraged for parsers, serializers, protocol boundaries, and other high-input-space components when it adds meaningful coverage beyond hand-written fixtures.

## 8. Tests should resist plausible implementation faults

A green suite is stronger when it can demonstrate that plausible incorrect implementations would fail.

For high-risk code, maintainers should consider mutation-style checks or equivalent adversarial review, such as verifying that tests fail when:

- a validation condition is inverted or removed;
- an error path is converted to a default value;
- a required diagnostic is dropped;
- a semantic branch returns the wrong identity or result;
- a known gap is reclassified as passing without the implementation actually matching the contract.

Mutation testing does not need to be a per-PR mandatory gate in every repository. It is a QA technique for evaluating whether important tests are capable of detecting meaningful faults.

## 9. Independent verification

AI-generated tests are subject to the same evidence requirements as human-written tests.

For material semantic, compatibility, compiler, parser, source-edit, or protocol changes, acceptance should include an independent attempt to falsify the implementation rather than relying only on tests authored alongside it.

Independent verification may be performed by a separate reviewer, QA agent, review pass, or another repository-appropriate mechanism. The testing policy defines the required verification property, not a specific agent-team topology.

Appropriate verification work includes:

- checking expectations against the original evidence source;
- adding missing negative and boundary cases;
- exercising failure propagation through public surfaces;
- testing real-project regressions;
- checking that known gaps remain explicit;
- considering whether a simple incorrect mutation would escape the suite.

Independent verification is not satisfied by only rerunning the existing test command and observing that it is green.

When a new class of development failure escapes existing tests, add a regression that makes that failure mode observable where practical.

## 10. Compatibility tests preserve the contract, not the implementation

For OPY, DEL/OSTW-compatible, raw Workshop, locale, and interoperability testing, observable semantic compatibility is the default correctness target.

Do not require identity of:

- generated formatting;
- temporary variables;
- optimizer choices;
- internal IR;
- other implementation details that do not affect a declared observable contract.

Conversely, normalized output comparison is evidence only when the normalization preserves the semantics being claimed. It must not erase the difference that the test is supposed to detect.

If an upstream oracle accepts a case and WrightKit does not, preserve the expected accepted behavior and record the WrightKit result as a gap, unsupported boundary, or divergence as appropriate. Do not rewrite the expected result to the current failure merely to make the suite pass.

## 11. Test layers should remain complementary

Repositories should use the smallest useful combination of test layers for their responsibilities. Typical layers include:

1. focused unit and semantic tests;
2. negative and error-propagation tests;
3. property and invariant tests;
4. minimized provenance-linked regressions;
5. complete real-world corpus cases;
6. differential/oracle tests;
7. fuzz or robustness tests;
8. cross-component or end-to-end conformance tests.

A large corpus does not replace focused diagnostics. Hundreds of unit tests do not replace real-project evidence. A full-feature census does not replace malformed-input and failure-path testing.

## 12. Pull request expectations

A PR that changes observable behavior should make the evidence for that behavior reviewable.

When applicable, the PR should identify:

- the contract or evidence that defines the expected behavior;
- the regression or capability being protected;
- relevant positive and negative coverage;
- known limitations or gaps that remain;
- why any changed expected result or support classification is correct.

Tests must not be weakened, removed, broadly ignored, or reclassified solely to obtain a green CI result.

Temporary quarantines or expected-failure classifications are acceptable only when the gap remains visible, the intended behavior remains preserved, and the owning repository has a clear way to track the limitation.

## 13. Repository responsibilities

This policy defines WrightKit-wide testing governance. Each repository remains responsible for documenting and implementing its own evidence sources, fixture layouts, validation commands, and CI gates.

In particular:

- canonical Workshop conformance and client-observable Workshop evidence belong with the repository that owns canonical Workshop semantics;
- source-language compatibility evidence belongs with the corresponding source-language repository;
- protocol conformance belongs with the protocol repository;
- Wright-owned tooling, orchestration, lint, source-edit, and integration behavior is tested in Wright.

Cross-repository tests must respect these ownership boundaries rather than duplicating authoritative semantic data for convenience.

## Non-goals

This policy does not mandate a single Rust test framework, fixture schema, fuzzing library, mutation-testing tool, coverage percentage, agent topology, or CI topology for every repository.

It also does not require maximum testcase quantity. The objective is stronger evidence, meaningful failure detection, and durable semantic protection.
