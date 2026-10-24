# WrightKit coding standards — reviewer entry point

This file routes reviewers and implementers to the canonical policy for each
judgment area. It is an index, not a second authority: the linked document
owns the contract. When a repository-local `AGENTS.md` or owner contract is
stricter or more specific, it wins for that repository.

## Routing

Start from the concern, not from a document list.

| Concern | Canonical policy |
| --- | --- |
| Review workflow, finding quality, review-fix handoff | [PR review](docs/pr-review.md) |
| What a PR must make verifiable; when a check counts | [Verification and acceptance](docs/verification-and-acceptance.md) |
| Issue contract, readiness, closing, boundary continuity | [Issue readiness](docs/issue-readiness.md) |
| Test organization, fixtures, evidence boundaries | [Testing policy](docs/testing-policy.md) |
| Upstream/oracle comparison, real-project regressions | [Compatibility testing](docs/compatibility-testing.md) |
| Malformed/extreme input, fuzzing | [Robustness testing](docs/robustness-testing.md) |
| Design, scope, simplicity, ablation, comments | [Engineering quality](docs/engineering-quality.md) |
| Deletion, consolidation, stale-inventory cleanup | [Entropy policy](docs/entropy-policy.md) |
| Rust CI jobs, toolchains, caches, runtime gates | [Rust CI](docs/rust-ci.md) |
| Shared CI platform and reusable workflow boundaries | [CI platform](docs/ci-platform.md) |
| Tags, packaging, publication ordering | [Release engineering](docs/release-engineering.md) |
| Repository ownership and domain routing | [Workspace AGENTS.md](AGENTS.md) |

Domain-specific details stay with their owners: Workshop semantics and catalog
in `workshop-rs`, OPY in `opy-rs`, DEL/OSTW in `deltin-rs`, tooling surfaces in
`wright`, probes and simulation in `athena`. Route a conflict there instead of
resolving it in shared policy.

## Recurring judgment criteria

Each rule names the protected contract and a practical criterion; the owning
document holds the full wording.

### Verification scope

- **A tolerated residual validates only what was checked.** Accepting one
  difference, skipping one failure, or tolerating one residual does not
  validate unchecked siblings or descendants of that case. Criterion: name
  what the check still fails to cover, or the approval is over-broad.
  → [verification-and-acceptance.md](docs/verification-and-acceptance.md)
- **A source-dependent result is valid only in matching context.** A
  before/after, baseline, or fixture comparison counts only when the
  document, project, revision, and configuration match and the compared state
  is valid; after a failed refresh or reload, re-establish validity before
  trusting the comparison.
  → [verification-and-acceptance.md](docs/verification-and-acceptance.md)
- **A reference-backed verdict requires an executed comparison.** Recording
  reference metadata — version, path, checksum, expected block — is not
  evidence; the case must actually run and the expected data must influence
  the result. Criterion: a wrong implementation under the expected data must
  fail the check.
  → [verification-and-acceptance.md](docs/verification-and-acceptance.md)

### Boundary and compatibility

- **Boundary continuity covers every surviving surface.** Replacing or
  retiring a public boundary must account for public mutation and
  deserialization paths and the invariants construction establishes, diagnostic
  codes/severities/ordering, metrics and their meaning, source mappings, and
  refusal/typed-error behavior — not only the happy path.
  → [issue-readiness.md](docs/issue-readiness.md#contract-continuity-for-boundary-migrations)
- **An exception binds the approved behavior, not a path.** A recorded
  compatibility exception applies to the specific approved behavior and its
  authority; a new difference under the same path or failure category is not
  covered by it.
  → [compatibility-testing.md](docs/compatibility-testing.md)
- **Normalization preserves the declared property.** Ordinary compiler
  compatibility remains structural; a normalized comparison is valid only
  when the normalization does not erase the difference the test claims to
  detect.
  → [compatibility-testing.md](docs/compatibility-testing.md)

### Change completeness

- **An optimization preserves effective behavior.** A transform or folding
  pass keeps the effective source scope, evaluation count and order, and side
  effects of its input; a program-final optimization state must not change
  earlier scoped behavior.
  → [engineering-quality.md](docs/engineering-quality.md#hold-the-change-on-the-whole-path)
- **A measurement keeps its meaning.** A before/after metric comparison is
  valid only while the field measures the same quantity; repurposing an
  unchanged field name for a different measure invalidates the comparison.
  → [engineering-quality.md](docs/engineering-quality.md#hold-the-change-on-the-whole-path)

## What this file is not

Not a new policy authority, not a test taxonomy, and not a checklist of
mandatory stages. Repeated review findings enter policy through the recurring-
findings rule in [pr-review.md](docs/pr-review.md#recurring-findings), which
keeps the evidence in Issues and PR threads rather than here.
