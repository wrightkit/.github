# Compatibility and reference testing

This document defines how WrightKit tests compatibility with an upstream
compiler, raw Workshop and locale semantic compatibility, and behavior found in
real projects. Load it when a change adds or changes a compatibility
expectation, an oracle or differential comparison, a real-project regression,
or a corpus case.

It is part of the [testing policy](testing-policy.md), whose core principles
also apply, including independent sources for expected results and the
distinction between matches, gaps, and divergences in reports.

## Compatibility tests protect structure, not formatting

For OPY and DEL/OSTW-compatible compilation, the correctness target is
structural convergence with the established upstream compiler, as defined in
[`goal.md`](goal.md) principle 7. Compare the upstream and WrightKit outputs as
canonical Workshop programs parsed by `workshop-rs`; never compare text diffs,
line counts, or text-pattern counts. Formatting, whitespace, and comments are
not criteria. A structural difference fails unless it is a recorded, approved
exception in the owning repository.

For raw Workshop, locale, and interoperability testing without an upstream
compiler oracle, observable semantic compatibility remains the correctness
target. Do not require identity of formatting or internal IR there. Normalized
output comparison is valid only when the normalization preserves the property
being claimed and does not erase the difference the test is meant to detect.

If an upstream oracle accepts a case and WrightKit does not, preserve the
accepted expected behavior and record the WrightKit result as a gap,
unsupported boundary, or divergence as appropriate. Do not rewrite the
expected result to the current failure merely to make the suite pass.

## Preserve real-project regressions and test data carefully

Synthetic unit tests are necessary but are not sufficient for compatibility or
project-graph work.

When a defect is found in a real project, preserve a minimized reproduction as
a feature-owned regression test whenever practical. Its metadata should retain
the source repository, immutable revision, and source path. Any real-project
test may retain those details in comments or test-data metadata; they identify
the input. Related Issue or PR history belongs in GitHub or Git history rather
than committed test metadata, and it does not determine test organization.

Keep project-level corpus coverage when it tests imports, includes, macros,
project graphs, cross-file symbols and types, settings/catalog interactions, or
combinations that a minimized case cannot exercise.

Minimized regressions and complete project cases are complementary. Neither
replaces focused diagnostics or failure-path tests. Licensing and attribution
for third-party inputs follow
[Avoid production pollution](testing-policy.md#avoid-production-pollution).
