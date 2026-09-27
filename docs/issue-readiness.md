# Issue readiness and implementation preflight

This policy defines the minimum task contract, verifiable outcomes,
boundary-migration continuity, and Engineer preflight required before
implementation.

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
- **`ready-for-implementation`** — the issue contains enough settled scope and contract information for an Engineer to implement it without inventing a product or architecture decision, including acceptance criteria that form a [verifiable outcome](#verifiable-outcomes). Implementation details may remain open.

An issue can move back from `ready-for-implementation` when new contract information, architecture drift, current-code reality, or a scope change reopens a design, product, or dependency question. `ready-for-implementation` is not a permanent assertion that the Issue still matches the repository when implementation begins. It settles the contract, not whether a new persistent mechanism is necessary: establish its current requirement and apply the single simplification pass in [`docs/engineering-quality.md`](engineering-quality.md) once proposed or added mechanisms are concrete enough to assess. Do not hide an unresolved decision inside an apparently ready issue; name the decision and route it to its owner first.

## Minimum implementation contract

An issue marked `ready-for-implementation` should make the following discoverable when applicable:

- **Problem / desired behavior** — what is wrong or what user/operator outcome is wanted.
- **Scope** — the behavior, surfaces, repositories, or workflows included.
- **Non-goals** — nearby work intentionally excluded from this issue.
- **Constraints** — relevant architecture, ownership, compatibility, security, or public-contract boundaries. Link to stable policy instead of copying it.
- **Acceptance criteria** — observable conditions that determine whether the issue is complete, including important failure or unsupported paths. For substantive behavior work they must form a [verifiable outcome](#verifiable-outcomes).
- **Dependencies / ownership boundaries** — prerequisites, owning components, and any required cross-repository coordination.

This is a discoverability contract, not an implementation specification. An issue should not prescribe code structure, helper names, file layout, or a future abstraction unless that detail is itself an accepted contract.

If a section is not applicable, do not manufacture content for it. If material information is unknown, the issue is not ready and should identify whether it needs design, a product decision, or an external dependency.

## Verifiable outcomes

Substantive behavior work is ready for Engineer implementation only when its acceptance criteria form a practical executable verification boundary. For each machine-verifiable behavior the Issue requests, it should be possible to answer:

1. What behavior must be true when the task is complete?
2. What automated test or check would fail if that behavior were wrong?
3. Would that failure be attributable to this task rather than to unrelated work?

The Issue answers the first question directly. The second and third may be answered by an existing test or check, a reference or oracle comparison, or the owning repository's harness where the new cases belong; the Issue does not need to name test functions or files, and tests stay organized by feature under [`docs/testing-policy.md`](testing-policy.md). The Engineer may derive the concrete checks from clear acceptance criteria. When the criteria are too vague to derive a check that could fail, the Issue needs a decision; the Engineer does not invent the acceptance boundary. When the owning repository has no harness for the behavior class, building one is a prerequisite: mark the Issue `blocked` on it or split it into its own Issue rather than building verification infrastructure incidentally inside a feature task.

When existing coverage already fails on a plausible wrong implementation, as for most pure refactors, mechanical migrations, removals, and changes already protected by tests, that coverage is the boundary; name it rather than requiring a new failing test. Boundary migrations also follow [contract continuity](#contract-continuity-for-boundary-migrations). When the outcome is not machine-verifiable, such as documentation, guidance, or judgment-based presentation, the acceptance criteria name the review or reference check that decides completion instead of a manufactured automated test.

Why: agents can produce plausible changes faster than people can read them line by line. When completion is defined by checks that fail on wrong behavior, CI status and a look at which boundaries those checks cover carry most of the correctness signal, and review can focus on whether the checks themselves are right. Without that boundary, drift is found only by manual reading, at the reviewer's cost.

### Task granularity

Size a task by a meaningful, independently verifiable outcome, not by lines of code, files changed, or number of implementation steps.

- **Too broad** — no check can confirm completion short of the whole feature, and a failure cannot be localized. "Implement OPY imports" is too broad; "resolve relative imports across files" and "report an import cycle as a structured diagnostic instead of a panic" are separately verifiable outcomes.
- **Implementation-only fragments** — a task with no observable behavior of its own, such as "add the resolver type" or "wire the new helper", can only be verified by the task that uses it, so its checks are absent or mirror implementation structure. Fold such steps into the behavior they serve.
- **Meaningful** — the task delivers at least one behavior that its checks can confirm or refute on their own, and failures of those checks point back to it.

Splitting finer than the verifiable outcome adds review and coordination cost without adding signal; splitting coarser pushes the cost of drift onto review.

## Contract continuity for boundary migrations

When an issue or change replaces, hides, or retires a public or canonical boundary (such as a public API, semantic model, AST/IR, wire/provider protocol, or canonical engine representation), the change must verify the continuity of surviving accepted contracts through the replacement boundary itself.

Every capability under the previous accepted contract must fall into one of three explicit categories:

1. **Preserved contracts** — capabilities that remain supported must be verified directly against the replacement boundary.
2. **Approved removals or changes** — intentional deprecations, breaking changes, or behavioral modifications must be backed by an approved architecture or contract decision; they must not be dropped silently as an implementation convenience or incidental side effect of the migration.
3. **Ownership transfers** — capabilities moved to another layer, crate, or repository must explicitly declare the new authoritative owner and handoff boundary.

Tests or checks exercising only retired, private, hidden, or compatibility-only paths are insufficient to prove that a replacement boundary is complete. Passing legacy or compatibility suites does not compensate for missing capabilities on the claimed canonical contract.

Why: migrating a boundary can leave legacy or compatibility adapters green while the new canonical entry point silently drops existing capabilities. Contract continuity ensures that replacements are verified at the surface where future consumers and tools will actually interact with the capability.

## Engineer preflight

A short request such as `implement #123` or `fix #123` is sufficient; the Engineer resolves context through the routing in `AGENTS.md` rather than expecting the prompt to repeat documents or skill names.

Before changing code in substantive work, establish and compare three things:

- the Issue contract, including its discussion, parent, and linked work;
- the current architecture or contract for the affected domain, from repository guidance and durable documentation (ADRs are decision records, not proof of current behavior);
- current implementation reality: code, consumers, tests, and dependency boundaries, inspected far enough to be decisive.

If they materially disagree, including a boundary replacement that would drop surviving capabilities (see [Contract continuity](#contract-continuity-for-boundary-migrations)), stop and report the mismatch to the appropriate Architect or owner rather than choosing a design.

Why: an agent can produce a plausible implementation for an undecided or drifted contract; a green build does not make that decision authorized.

Also identify the checks that decide completion: the existing tests or checks the change relies on and, where new behavior needs new cases, the feature-owned location in the existing harness where they belong. If no such boundary can be established, the task is not ready; see [Verifiable outcomes](#verifiable-outcomes).

When the three align and the verification boundary is established, implement under [`docs/engineering-quality.md`](engineering-quality.md) and verify under [`docs/testing-policy.md`](testing-policy.md). Report material assumptions, the reference used for verification, and remaining gaps against the acceptance criteria. Repository-local guidance may add stricter requirements.
