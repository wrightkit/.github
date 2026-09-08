# WrightKit Engineering Quality Policy

This policy defines organization-wide defaults for agent-assisted engineering work. Implementation decisions must remain grounded in correctness, existing architecture, coherent responsibility, locality, and low maintenance cost.

Repository-local guidance may add stricter requirements, but it must not weaken this policy or replace repository-specific architecture and compatibility contracts.

## Decision priority

When choosing between valid implementations, follow these priorities in order:

1. Correctness against the explicit issue or public contract
2. Existing architecture, ownership, and dependency boundaries
3. The simplest complete change that satisfies the contract while keeping the changed behavior in a coherent responsibility
4. Locality of the change and ease of review
5. Clear, readable code and documentation
6. DRY, when a demonstrated abstraction reduces total maintenance cost
7. Speculative extensibility, only when current evidence justifies it

The default is the smallest complete coherent change that satisfies the issue and existing architecture. Complexity needs a current reason. Existing placement is not evidence that new behavior belongs there.

## Preserve domain locality and responsibility

Organize implementation so a maintainer can find the behavior through the domain responsibility it implements rather than reconstructing unrelated compiler phases, registries, or framework machinery first.

When a parser, lowerer, compiler, checker, registry, catalog, service, or other implementation unit already carries several unrelated responsibilities, do not use adjacency alone to justify putting another behavior there. Ask which domain contract owns the behavior and whether the proposed placement makes that ownership easier or harder to discover.

A local structural extraction needed to keep the changed behavior cohesive is part of the feature change, not unrelated cleanup. Keep that extraction bounded to the responsibility the issue actually touches; do not turn a feature into a repository-wide reorganization or speculative architecture rewrite.

Prefer typed code for behavior, invariants, context-sensitive semantics, and control flow. Large mechanical inventories such as names, aliases, localization, enum membership, or other genuinely declarative facts may remain validated or generated data. If generic code interprets metadata fields to decide program semantics, treat that as a semantic abstraction that needs a concrete current justification rather than assuming a data-driven representation is automatically simpler.

Why: repeated locally minimal additions can make every individual PR easy to review while steadily increasing navigation distance, mixed responsibility, and the number of concepts required to understand one feature. WrightKit optimizes total maintenance cost, not only the size of the current diff.

## Prefer demonstrated abstractions

Use AHA and the Rule of Three as reasoning heuristics, not eligibility tests. Keep behavior local until repeated real cases reveal a stable common contract and an abstraction would reduce total conceptual and maintenance cost.

Why: premature abstraction couples cases before their common shape is understood. Small duplication is usually cheaper than the wrong helper, trait, adapter, or wrapper layer.

Do not add an extension point for a hypothetical consumer. When a new layer is proposed, identify the current owner, real consumer, and independently observable benefit. If those are unclear, keep the behavior local until evidence establishes the boundary.

## Prefer simple, idiomatic Rust

Use Rust's ownership model, enums, newtypes, `Result`/`Option`, traits, and type system when they express real domain distinctions, make ownership explicit, or prevent concrete classes of errors. Simplicity does not mean avoiding useful Rust features or writing Rust as if it were another language.

More advanced type machinery, generics, synchronization, concurrency, macros, unsafe code, or abstraction layers should solve a concrete current problem. They should not exist primarily for theoretical generality, language cleverness, zero-cost-at-any-cost optimization, or hypothetical future flexibility.

Why: WrightKit values correctness, reviewability, and maintainability over demonstrating language sophistication. Complexity should come from the domain when necessary, not from the implementation technique.

This is not a ban on advanced Rust. A complex ownership model, trait boundary, async design, or low-level optimization is appropriate when the domain or measured constraints require it and the implementation makes that reason discoverable.

## Prefer code over commentary

Code should express structure, behavior, ownership, and intent through names, types, modules, APIs, and control flow. Comments are exceptional: keep them only when they carry durable information that cannot be expressed clearly and reliably in code.

A feature, module, crate, or file is not considered readable merely because an explanatory header makes it understandable. A maintainer should normally be able to identify what it owns, how its major pieces relate, and where behavior lives from the path/module structure, names, types, public API, and implementation itself. Long `//!` or `//` preambles that explain why a file exists, enumerate its responsibilities, narrate a pipeline, describe which neighboring modules do what, or provide a prose walkthrough of the implementation are readability-failure signals even when factually accurate.

Do not add comments that:

- narrate implementation steps or restate names and obvious control flow;
- duplicate module structure, ownership, or behavior that the code already makes discoverable;
- act as a file/module/crate README for responsibilities or execution flow that should be evident from the implementation structure;
- preserve transient project state, migration progress, issue status, or speculative future work;
- compensate for unclear naming, mixed responsibility, weak decomposition, poor feature locality, or an implementation whose purpose is otherwise difficult to infer.

When explanatory prose appears necessary to understand changed code, first improve the code itself: rename, narrow the API, expose the domain distinction through types, simplify control flow, or perform the bounded structural extraction needed to keep the behavior in its coherent owning responsibility. If removing a file or module header leaves an experienced maintainer unable to determine why the unit exists or how to work on its feature, treat that as evidence to improve the implementation structure rather than evidence that the header should be retained.

Comments remain appropriate for durable information that code cannot encode cleanly, including non-obvious invariants, external compatibility constraints and quirks, correctness or safety rationale, provenance/evidence, and public API contracts that consumers need. These exceptions must explain information outside the implementation's ordinary structural meaning; they do not justify a prose description of the implementation itself. Rustdoc should document real consumer-facing contracts; do not mechanically restate a symbol's name or type merely to increase documentation coverage.

Comment ablation is therefore a readability test, not only a comment-retention test. For substantive code, temporarily remove explanatory file/module headers and local narration, then judge the source on its own. If responsibility, feature placement, or control flow becomes materially harder to understand, correct the names/types/modules/APIs/decomposition first. Restore only irreducible external constraints, invariants, rationale, provenance, or consumer contracts.

Source comments are not architecture contracts or independent evidence of current behavior. A comment that says a design is intentional does not waive the requirement to check the current architecture contract and implementation reality.

Why: explanatory comments are an unvalidated natural-language cache. They can become stale while still looking authoritative to humans and coding agents, and extensive explanatory prose can hide a codebase whose structure is not self-explanatory. WrightKit therefore treats the need for implementation-explaining prose as a maintenance signal and admits prose only when removing it would lose durable information that cannot be recovered reliably from the code.

## Keep issue work focused

An issue implementation should touch only what the issue owns and what is clearly necessary to fulfill its contract. Keep unrelated cleanup, renaming, refactoring, and formatting separate unless the issue explicitly includes them, correctness requires them, or a bounded structural extraction is needed to keep the changed behavior in its coherent owning responsibility.

Why: a focused change is easier to reason about, verify, review, and revert. It also prevents an implementation agent from turning a local task into an unauthorized architecture change. Focus does not mean preserving a bad placement merely because it minimizes the diff.

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
