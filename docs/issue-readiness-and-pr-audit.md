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

An issue can move back from `ready-for-implementation` when new evidence or a scope change reopens a design, product, or dependency question. Do not hide an unresolved decision inside an apparently ready issue; name the decision and route it to its owner first.

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

## Engineer defaults

For implementation work, an Engineer should:

1. Read the linked issue and nearest repository guidance before changing code. Load specialized policy or skills only when the change touches their concern.
2. Check that the issue is `ready-for-implementation` in substance. Do not self-authorize an unresolved design or product decision.
3. Inspect the existing implementation, tests, consumers, and ownership boundaries before adding a new path or abstraction.
4. Make the smallest complete change that satisfies the issue and existing architecture.
5. Keep unrelated cleanup, refactoring, renaming, and speculative extensibility out of the change.
6. Verify the behavior at the narrowest decisive surface first, then run the broader gates required by the repository or risk surface.
7. Report material assumptions, limitations, and remaining gaps against the acceptance criteria. A green build does not resolve an undecided contract.

These defaults complement [`docs/engineering-quality.md`](engineering-quality.md) and do not replace repository-local architecture or contribution guidance.

## PR review is verification, not design

A reviewer verifies whether the PR correctly and completely implements its approved issue, architecture, and contracts. Review is not an opportunity to redesign the system, revisit accepted architecture preferences, or expand the issue into cleanup and future work.

Why: architecture and product decisions have their own owners and decision process. Reopening them during PR review creates scope drift and repeated implementation cycles without new evidence.

The reviewer should inspect the full applicable PR scope in the initial pass. Finding one blocker does not end the review; continue through the remaining changed behavior and report all currently discoverable actionable findings together.

Review, as applicable:

- the linked issue scope, non-goals, and acceptance criteria;
- correctness, regressions, failure and unsupported paths;
- compliance with already-approved architecture, ownership, dependency, compatibility, API/protocol, and security contracts;
- test coverage when it is materially relevant to a current failure mode or contract;
- changes outside the approved scope that affect correctness or maintenance obligations.

Architecture is a compliance boundary during review. Do not propose an alternative architecture when the PR follows the approved one. If new evidence shows the approved contract itself is wrong, identify the decision mismatch and route it to the appropriate owner rather than asking the Engineer to redesign it inside the PR.

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
- Route genuinely material Rust ownership, API, error, async/concurrency, or structural risk to `.agents/skills/wrightkit-rust-engineering-review/SKILL.md`.
- Route substantial simplification, deletion, duplication, or post-migration entropy work to [`docs/entropy-policy.md`](entropy-policy.md) and `.agents/skills/wrightkit-reclaim-entropy/SKILL.md` when that work is inside the approved scope.
- Route material changes requiring independent falsification to `.agents/skills/wrightkit-verify-change/SKILL.md` and the canonical testing policy.

Do not load every specialist route because a PR contains Rust, tests, or abstractions. The linked issue and the actual risk surface determine what is applicable.