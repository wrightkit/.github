# Issue Readiness and One-Pass PR Audit

This document defines the WrightKit-wide workflow for deciding whether an issue is ready for implementation and for auditing the resulting PR. It makes the PM/Architect/Engineer/QA boundary explicit without requiring every task to use all four roles or creating an autonomous issue-to-PR system.

The intended model is agent-compatible, not agent-autonomous: humans or Architects decide unresolved product and architecture questions; Engineer agents implement a settled contract; reviewers verify the complete result against that contract.

## Issue readiness

Readiness describes the state of the issue's contract, not the confidence of an agent or the presence of a particular GitHub label. A repository may represent these states with labels, fields, issue sections, or another explicit mechanism as long as the meaning remains discoverable.

Use the following semantic states:

- **`needs-design`** — an architectural, ownership, public-contract, or compatibility decision is unresolved. An Engineer should not choose the design by implementation convenience; route the question to the appropriate Architect or owning repository.
- **`needs-decision`** — a product, user-visible behavior, priority, or other non-architectural choice is unresolved. An Engineer should not select a behavior and present it as implementation of the issue.
- **`blocked`** — the contract is sufficiently decided, but an external dependency, owner, access requirement, or prerequisite prevents the work. Record the dependency and the condition that will unblock it.
- **`ready-for-implementation`** — the issue contains enough settled scope and contract information for an Engineer to implement it without inventing a product or architecture decision. Implementation details may remain open.

An issue can move back from `ready-for-implementation` when new evidence, architecture drift, current-code reality, or a scope change reopens a design, product, or dependency question. `ready-for-implementation` is not a permanent assertion that the Issue still matches the repository when implementation begins. Do not hide an unresolved decision inside an apparently ready issue; name the decision and route it to its owner first.

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

Tests, fixtures, or evidence exercising only retired, private, hidden, or compatibility-only paths are insufficient to prove that a replacement boundary is complete. Passing legacy or compatibility suites does not compensate for missing capabilities on the claimed canonical contract.

Why: migrating a boundary can leave legacy or compatibility adapters green while the new canonical entry point silently drops existing capabilities. Contract continuity ensures that replacements are verified at the surface where future consumers and tools will actually interact with the capability.

## Engineer preflight and defaults

A short request such as `implement #123` or `fix #123` is sufficient. Before changing code, the Engineer is responsible for resolving the relevant current context rather than expecting the prompt to repeat repository documents or skill names.

For substantive implementation work, an Engineer should:

1. Read the linked Issue and nearest repository guidance.
2. Identify the affected domain and owning repository before choosing the implementation location.
3. Resolve the current architecture or contract relevant to that domain through repository guidance and durable documentation. Treat ADRs as decision records; verify current implementation reality separately.
4. Inspect the current implementation, affected consumers, tests/evidence, and dependency boundaries far enough to establish current reality.
5. Compare the Issue contract, current architecture/contract, and current code reality. When replacing, hiding, or retiring a public or canonical boundary, verify that surviving accepted capabilities are accounted for on the replacement boundary, explicitly approved for removal/change, or transferred to another owner. If they are materially inconsistent, stop and report the mismatch to the appropriate Architect/owner; do not self-authorize a replacement design.
6. If they are aligned, load specialized policy or skills for the actual risk surface and make the smallest complete coherent change that satisfies the issue and current architecture.
7. Keep unrelated cleanup, renaming, broad refactoring, and speculative extensibility out of the change. A bounded structural extraction needed to keep the changed behavior in its coherent owning responsibility is part of the implementation scope, not unrelated cleanup.
8. Temporarily remove newly added explanatory comments and file/module headers, then read the changed implementation as code. If an experienced maintainer can no longer determine the unit's responsibility, feature placement, major relationships, or control flow from names, types, modules, APIs, and implementation structure, treat that as a readability/maintainability defect and improve the code first. Restore only irreducible external contracts, invariants, compatibility/safety rationale, provenance, or consumer-facing API documentation.
9. Verify the behavior at the narrowest decisive surface first, then run the broader gates required by the repository or risk surface. For boundary migrations, verify surviving contracts through the replacement boundary itself rather than relying only on legacy or compatibility paths.
10. Report material assumptions, limitations, and remaining gaps against the acceptance criteria. A green build does not resolve an undecided or inconsistent contract.

These defaults complement [`docs/engineering-quality.md`](engineering-quality.md) and do not replace repository-local architecture or contribution guidance.

## PR review is verification, not design

A reviewer verifies whether the PR correctly and completely implements its approved issue, current architecture, and contracts. Review is not an opportunity to redesign the system, revisit accepted architecture preferences, or expand the issue into cleanup and future work.

Why: architecture and product decisions have their own owners and decision process. Reopening them during PR review creates scope drift and repeated implementation cycles without new evidence.

The reviewer should inspect the full applicable PR scope in the initial pass. Finding one blocker does not end the review; continue through the remaining changed behavior and report all currently discoverable actionable findings together.

Review, as applicable:

- the linked issue scope, non-goals, and acceptance criteria;
- correctness, regressions, failure and unsupported paths;
- compliance with the current approved architecture, ownership, dependency, compatibility, API/protocol, and security contracts;
- contract continuity when replacing, hiding, or retiring a public or canonical boundary: confirm that surviving accepted capabilities are verified through the replacement boundary itself, that removals/changes have explicit contract approval, that ownership transfers explicitly declare the new authoritative owner and handoff boundary, and that tests exercising only retired or compatibility paths are not treated as proving replacement completeness;
- test coverage when it is materially relevant to a current failure mode or contract;
- newly added or materially affected explanatory comments and file/module headers, including whether the prose is functioning as a README for code whose responsibility, ownership, pipeline, or internal relationships are otherwise not self-explanatory;
- changes outside the approved scope that affect correctness or maintenance obligations.

Architecture is a compliance boundary during review. Do not propose an alternative architecture when the PR follows the current approved one. If new evidence shows that the Issue, documented contract, and current implementation disagree materially, identify the decision mismatch and route it to the appropriate owner rather than asking the Engineer to redesign it inside the PR.

A comment is not independently authoritative evidence that a placement or behavior is intentional. Do not treat an accurate explanatory header as sufficient evidence of readability. If removing the prose makes a changed feature/module/file materially difficult to understand, require the smallest code-level correction needed to make the responsibility and behavior discoverable. Require comment removal when the prose merely restates implementation; retain only information that cannot reasonably be expressed by code structure and belongs with the source.

## Findings and output

Report only actionable defects that should be corrected in the current PR.

A useful finding identifies:

- the concrete location or behavior;
- what is wrong;
- why it affects the current issue, contract, correctness, or regression risk;
- the required correction, at the smallest useful level.

Keep the explanation only as long as needed to establish the defect. Do not add review summaries, praise, architecture essays, speculative concerns, nits, future improvements, or optional suggestions by default.

If there are no actionable findings, reply `LGTM` and approve the PR. Do not add a checklist or summary of categories inspected.

## Follow-up review

After the Engineer addresses findings, review only:

1. the previously reported findings;
2. regressions introduced by those fixes;
3. materially new code or behavior added since the previous review.

Do not reopen previously reviewed areas or add preference-based concerns without new evidence. If the prior findings are fixed and no new defect was introduced, reply `LGTM` and approve.

Why: follow-up review verifies the correction. Re-running a fresh architectural audit after every fix creates avoidable review loops and makes the effective PR scope unstable.

## Specialist routing

Specialist policy and skills are demand-driven, not mandatory review stages:

- Route material test-quality or agent-generated-test questions to `.agents/skills/wrightkit-test-design-review/SKILL.md` and the canonical testing policy.
- Route material Rust ownership, API, error, async/concurrency, abstraction, semantic-placement, responsibility-growth, feature-locality, or metadata-driven behavior risk to `.agents/skills/wrightkit-rust-engineering-review/SKILL.md`.
- Route substantial simplification, deletion, duplication, or post-migration entropy work to [`docs/entropy-policy.md`](entropy-policy.md) and `.agents/skills/wrightkit-reclaim-entropy/SKILL.md` when that work is inside the approved scope.
- Route material changes requiring independent falsification or public boundary contract continuity verification to `.agents/skills/wrightkit-verify-change/SKILL.md` and the canonical testing policy.

Do not load every specialist route because a PR contains Rust, tests, or abstractions. The linked issue and the actual risk surface determine what is applicable.
