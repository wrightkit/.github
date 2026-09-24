# Issue readiness and implementation preflight

This policy defines the minimum task contract, boundary-migration continuity,
and Engineer preflight required before implementation.

WrightKit separates PM/Architect/Engineer/QA authority without requiring every
task to use all four roles. The workflow is agent-compatible, not
autonomous: humans or Architects resolve product and architecture decisions;
Engineer agents implement settled contracts; reviewers verify the complete
result against those contracts.

## Issue readiness

Readiness describes the state of the issue's contract, not the confidence of an agent or the presence of a particular GitHub label. A repository may represent these states with labels, fields, issue sections, or another explicit mechanism as long as the meaning remains discoverable.

Use the following semantic states:

- **`needs-design`** — an architectural, ownership, public-contract, or compatibility decision is unresolved. An Engineer should not choose the design by implementation convenience; route the question to the appropriate Architect or owning repository.
- **`needs-decision`** — a product, user-visible behavior, priority, or other non-architectural choice is unresolved. An Engineer should not select a behavior and present it as implementation of the issue.
- **`blocked`** — the contract is sufficiently decided, but an external dependency, owner, access requirement, or prerequisite prevents the work. Record the dependency and the condition that will unblock it.
- **`ready-for-implementation`** — the issue contains enough settled scope and contract information for an Engineer to implement it without inventing a product or architecture decision. Implementation details may remain open.

An issue can move back from `ready-for-implementation` when new contract information, architecture drift, current-code reality, or a scope change reopens a design, product, or dependency question. `ready-for-implementation` is not a permanent assertion that the Issue still matches the repository when implementation begins. It settles the contract, not whether a new persistent mechanism is necessary: establish its current requirement and apply the single independent simplification review in [`docs/engineering-quality.md`](engineering-quality.md) once proposed or added mechanisms are concrete enough to assess. Do not hide an unresolved decision inside an apparently ready issue; name the decision and route it to its owner first.

## Minimum implementation contract

An issue marked `ready-for-implementation` should make the following discoverable when applicable:

- **Problem / desired behavior** — what is wrong or what user/operator outcome is wanted.
- **Scope** — the behavior, surfaces, repositories, or workflows included.
- **Non-goals** — nearby work intentionally excluded from this issue.
- **Constraints** — relevant architecture, ownership, compatibility, security, or public-contract boundaries. Link to stable policy instead of copying it.
- **Acceptance criteria** — observable conditions that determine whether the issue is complete, including important failure or unsupported paths.
- **Dependencies / ownership boundaries** — prerequisites, owning components, and any required cross-repository coordination.

This is a discoverability contract, not an implementation specification. An issue should not prescribe code structure, helper names, file layout, or a future abstraction unless that detail is itself an accepted contract.

If a section is not applicable, do not manufacture content for it. If material information is unknown, the issue is not ready and should identify whether it needs design, a product decision, or an external dependency.

## Contract continuity for boundary migrations

When an issue or change replaces, hides, or retires a public or canonical boundary (such as a public API, semantic model, AST/IR, wire/provider protocol, or canonical engine representation), the change must verify the continuity of surviving accepted contracts through the replacement boundary itself.

Every capability under the previous accepted contract must fall into one of three explicit categories:

1. **Preserved contracts** — capabilities that remain supported must be verified directly against the replacement boundary.
2. **Approved removals or changes** — intentional deprecations, breaking changes, or behavioral modifications must be backed by an approved architecture or contract decision; they must not be dropped silently as an implementation convenience or incidental side effect of the migration.
3. **Ownership transfers** — capabilities moved to another layer, crate, or repository must explicitly declare the new authoritative owner and handoff boundary.

Tests or checks exercising only retired, private, hidden, or compatibility-only paths are insufficient to prove that a replacement boundary is complete. Passing legacy or compatibility suites does not compensate for missing capabilities on the claimed canonical contract.

Why: migrating a boundary can leave legacy or compatibility adapters green while the new canonical entry point silently drops existing capabilities. Contract continuity ensures that replacements are verified at the surface where future consumers and tools will actually interact with the capability.

## Engineer preflight and defaults

A short request such as `implement #123` or `fix #123` is sufficient. Before changing code, the Engineer is responsible for resolving the relevant current context rather than expecting the prompt to repeat repository documents or skill names.

For substantive implementation work, an Engineer should:

1. Read the linked Issue and nearest repository guidance.
2. Identify the affected domain and owning repository before choosing the implementation location.
3. Resolve the current architecture or contract relevant to that domain through repository guidance and durable documentation. Treat ADRs as decision records; verify current implementation reality separately.
4. Inspect the current implementation, affected consumers, tests, and dependency boundaries far enough to establish current reality.
5. Compare the Issue contract, current architecture/contract, and current code reality. When replacing, hiding, or retiring a public or canonical boundary, verify that surviving accepted capabilities are accounted for on the replacement boundary, explicitly approved for removal/change, or transferred to another owner. If they are materially inconsistent, stop and report the mismatch to the appropriate Architect/owner; do not self-authorize a replacement design.
6. If they are aligned and the proposed design introduces a material persistent mechanism, establish its current requirement as described in [`docs/engineering-quality.md`](engineering-quality.md). The single independent simplification review should happen once proposed or added mechanisms are concrete enough to assess; implementation readiness does not depend on completing it before coding. Do not treat a small diff, few files, or few lines as proof that the mechanism is simple or necessary.
7. If they are aligned, load specialized policy or skills for the actual risk surface and make the smallest complete coherent change that satisfies the issue and current architecture.
8. Keep unrelated cleanup, renaming, broad refactoring, and speculative extensibility out of the change. A bounded structural extraction needed to keep the changed behavior in its coherent owning responsibility is part of the implementation scope, not unrelated cleanup.
9. Temporarily remove newly added explanatory comments and file/module headers, then read the changed implementation as code. If an experienced maintainer can no longer determine the unit's responsibility, feature placement, major relationships, or control flow from names, types, modules, APIs, and implementation structure, treat that as a readability/maintainability defect and improve the code first. Restore only irreducible external contracts, invariants, compatibility/safety rationale, source mapping or attribution, or consumer-facing API documentation.
10. Verify the behavior at the narrowest decisive surface first, then run the broader gates required by the repository or risk surface. For boundary migrations, verify surviving contracts through the replacement boundary itself rather than relying only on legacy or compatibility paths.
11. Report material assumptions, limitations, and remaining gaps against the acceptance criteria. A green build does not resolve an undecided or inconsistent contract.

These defaults complement [`docs/engineering-quality.md`](engineering-quality.md) and do not replace repository-local architecture or contribution guidance.
