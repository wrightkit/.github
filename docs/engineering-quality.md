# WrightKit Engineering Quality Policy

This policy defines organization-wide defaults for agent-assisted engineering work. Implementation decisions must remain grounded in correctness, existing architecture, locality, and low maintenance cost.

Repository-local guidance may add stricter requirements, but it must not weaken this policy or replace repository-specific architecture and compatibility contracts.

## Decision priority

When choosing between valid implementations, follow these priorities in order:

1. Correctness against the explicit issue or public contract
2. Existing architecture, ownership, and dependency boundaries
3. The simplest complete change that satisfies the contract
4. Locality of the change and ease of review
5. Clear, readable code and documentation
6. DRY, when a demonstrated abstraction reduces total maintenance cost
7. Speculative extensibility, only when current evidence justifies it

The default is the smallest complete change that satisfies the issue and existing architecture. Complexity needs a current reason.

## Prefer demonstrated abstractions

Use AHA and the Rule of Three as reasoning heuristics, not eligibility tests. Keep behavior local until repeated real cases reveal a stable common contract and an abstraction would reduce total conceptual and maintenance cost.

Why: premature abstraction couples cases before their common shape is understood. Small duplication is usually cheaper than the wrong helper, trait, adapter, or wrapper layer.

Do not add an extension point for a hypothetical consumer. When a new layer is proposed, identify the current owner, real consumer, and independently observable benefit. If those are unclear, keep the behavior local until evidence establishes the boundary.

## Prefer simple, idiomatic Rust

Use Rust's ownership model, enums, newtypes, `Result`/`Option`, traits, and type system when they express real domain distinctions, make ownership explicit, or prevent concrete classes of errors. Simplicity does not mean avoiding useful Rust features or writing Rust as if it were another language.

More advanced type machinery, generics, synchronization, concurrency, macros, unsafe code, or abstraction layers should solve a concrete current problem. They should not exist primarily for theoretical generality, language cleverness, zero-cost-at-any-cost optimization, or hypothetical future flexibility.

Why: WrightKit values correctness, reviewability, and maintainability over demonstrating language sophistication. Complexity should come from the domain when necessary, not from the implementation technique.

This is not a ban on advanced Rust. A complex ownership model, trait boundary, async design, or low-level optimization is appropriate when the domain or measured constraints require it and the implementation makes that reason discoverable.

## Keep issue work focused

An issue implementation should touch only what the issue owns and what is clearly necessary to fulfill its contract. Keep unrelated cleanup, renaming, refactoring, and formatting separate unless the issue explicitly includes them or correctness requires them.

Why: a focused change is easier to reason about, verify, review, and revert. It also prevents an implementation agent from turning a local task into an unauthorized architecture change.

When removing behavior, remove obsolete code paths with it unless a compatibility contract requires a transition. Do not preserve fallback layers merely because deletion feels risky; establish whether a real consumer or contract still requires them.

## Keep durable knowledge stable

Durable policy and architecture documentation belongs to stable knowledge: invariants, ownership and routing, contracts, architecture principles, and engineering methods. Fast-changing facts such as current counts, versions, gap inventories, roadmap state, and issue status belong in issues, PRs, generated outputs, or other dynamic surfaces that refresh directly from their source of truth.

Why: stable documents remain reliable context for humans and agents and improve prompt/document caching. Cache performance is never a correctness requirement and must not justify stale or misleading guidance.

## Route specialized guidance

This policy sets baseline defaults. Refer to specialized policies for domain-specific requirements:

- [Agent Guidance Principles](agent-guidance.md) for writing durable agent-facing policy and skills.
- [Testing Policy](testing-policy.md) for tests, fixtures, compatibility evidence, robustness, and independent verification.
- [Code Entropy Policy](entropy-policy.md) for deletion, consolidation, and evidence-backed simplification.
- [Rust CI standard](rust-ci.md) for Rust toolchain and cache composition.
- [Release engineering standard](release-engineering.md) for release ownership, publication, and recovery.

Do not duplicate those policies here or dilute them with general implementation preferences.