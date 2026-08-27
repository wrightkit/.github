# WrightKit Engineering Quality Policy

This policy defines organization-wide defaults for agent-assisted engineering
work. Implementation decisions must remain grounded in correctness, existing
architecture, locality, and low maintenance cost.

Repository-local guidance may add stricter requirements, but it must not weaken
this policy or replace repository-specific architecture and compatibility
contracts.

## Decision priority

When choosing between valid implementations, follow these priorities in order:

1. Correctness against the explicit issue or public contract
2. Existing architecture, ownership, and dependency boundaries
3. The simplest complete change that satisfies the contract
4. Locality of the change and ease of review
5. Clear, readable code and documentation
6. DRY, but only when a demonstrated abstraction reduces total maintenance cost
7. Speculative extensibility, only when current evidence justifies it

The default rule is straightforward: make the smallest complete change that
satisfies the issue and existing architecture.

## Prefer demonstrated abstractions

Avoid hasty abstractions (AHA). Abstract repeated behavior only when the cases
share a stable contract and the abstraction makes the code easier to understand
or modify. The rule of three is a practical threshold: after one use, keep the
logic local; after two, compare callers and their ownership; abstract only when
a third real case confirms the common shape.

DRY comes after correctness, locality, and proven abstractions. Small duplication
is preferable to coupling unlike cases through the wrong helper, trait, adapter,
or wrapper layer. Never add an extension point for a hypothetical consumer.

## Keep issue work focused

An issue implementation should touch only what the issue owns and what is
clearly necessary to fulfill its contract. Keep unrelated cleanup, renaming,
refactoring, and formatting separate unless the issue explicitly includes them
or correctness requires them. When removing behavior, remove obsolete code
paths with it; do not preserve compatibility code or add fallback layers
without an explicit contract.

Before adding a layer, identify its current owner, consumer, and independently
observable benefit. If you cannot name all three, keep the behavior local and
log the future requirement in an issue or roadmap note instead of encoding a
hypothesis into production structure.

## Keep durable knowledge stable

Durable policy and architecture documentation belongs to stable knowledge:
invariants, ownership and routing, contracts, architecture principles, and
engineering methods. Fast-changing facts like current counts, versions, gap
inventories, roadmap state, and issue status belong in issues, PRs, generated
outputs, or other dynamic surfaces that refresh directly from their source of
truth.

Avoid unnecessary structural and phrasing churn in stable documents. Keeping
them steady helps agents and human readers reuse reliable context, and it allows
prompt and documentation caching to work efficiently. Still, cache performance is
never a correctness requirement and must never justify keeping stale or
misleading guidance.

## Route specialized guidance

This policy sets baseline defaults. Refer to specialized policies for
domain-specific requirements:

- [Testing Policy](testing-policy.md) for tests, fixtures, compatibility
  evidence, robustness, and independent verification.
- [Code Entropy Policy](entropy-policy.md) for deletion, consolidation, and
  evidence-backed simplification.
- [Rust CI standard](rust-ci.md) for Rust toolchain and cache composition.
- [Release engineering standard](release-engineering.md) for release
  ownership, publication, and recovery.

Do not duplicate those policies here or dilute them with general
implementation preferences.
