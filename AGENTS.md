# WrightKit Workspace Agent Routing

This file is the workspace-level agent routing entry point for the WrightKit organization.

Read [`GOAL.md`](GOAL.md) first for durable product intent. This file explains how work is routed and governed; it is not a technical manual or a second copy of the product goal.

Repository-local `AGENTS.md` files specialize contracts for their own repository. They must not duplicate shared policy, but they may add stricter or domain-specific requirements that take precedence locally.

To apply this routing from a local workspace:

1. Read [`GOAL.md`](GOAL.md).
2. Read this file.
3. Read the nearest repository-local `AGENTS.md`.
4. Load routed policy or skills only when the task touches their concern.

No proprietary include syntax is required.

## Repository routing

Before substantial work, identify the affected repository and read its `AGENTS.md`.

| Concern | Primary repository |
| --- | --- |
| Canonical Workshop semantics, catalog, locales, parsing, validation, Workshop representation and emission | `workshop-rs` |
| OverPy-compatible language implementation | `opy-rs` |
| DeltinScript / OSTW-compatible language implementation | `del-rs` |
| Provider process/data protocol | `language-provider-protocol` |
| User-facing tooling, orchestration, integration, analysis, and agent surfaces | `wright` |
| Product website | `wrightkit.dev` |
| Distribution, packaging, and release-artifact ownership | `wright` (`dist/`, `.github/workflows/release.yml`) for build/package/publish; `homebrew-tap` for the published Homebrew formula only |
| Organization-wide shared policy, CI patterns, and GitHub governance | `wrightkit/.github` |
| WrightKit-wide reusable agent skills and procedures | `wrightkit/.agents` |

Confirm current reality before making architectural assumptions. Repository ownership may evolve.

For cross-repository work:

1. Identify the semantic or product owner.
2. Read every affected repository's `AGENTS.md`.
3. Change the authoritative contract in the owning repository.
4. Implement consumer integration separately.
5. Verify the cross-repository contract explicitly.

## Policy routing

Load policy documents only when their concern is relevant. Do not preload all of them.

| Task concern | Load |
| --- | --- |
| Writing or revising durable agent guidance, AGENTS content, or reusable skills | [`docs/agent-guidance.md`](docs/agent-guidance.md) |
| Implementation design, scope discipline, demonstrated abstractions, simple/idiomatic Rust, responsibility locality, and stable-vs-dynamic documentation | [`docs/engineering-quality.md`](docs/engineering-quality.md) |
| Public or canonical boundary migrations (API, model, IR, protocol), contract continuity, issue readiness, one-pass implementation/PR review, and review-fix handoff | [`docs/issue-readiness-and-pr-audit.md`](docs/issue-readiness-and-pr-audit.md) |
| Tests, fixtures, corpora, snapshots, expected results, compatibility tests, fuzzing, independent verification | [`docs/testing-policy.md`](docs/testing-policy.md) |
| Code entropy, dead code, redundancy, over-engineering, mutable-inventory documentation | [`docs/entropy-policy.md`](docs/entropy-policy.md) |
| CI failure triage across job surfaces (Rust quality vs. LPP integration vs. differential/compatibility vs. dist/release) | Classify by surface: local/quality gates fix in place; LPP integration check protocol commit first; differential/compatibility triage under testing policy |
| Rust CI toolchain, caching, and job composition | [`docs/rust-ci.md`](docs/rust-ci.md) |
| Rust build artifact growth, dev/test profile configuration, ephemeral worktree lifecycle, and local storage management | [`docs/rust-build-artifacts.md`](docs/rust-build-artifacts.md) |
| Release engineering, tagging, and artifact publication | [`docs/release-engineering.md`](docs/release-engineering.md) |
| Entropy reclamation workflow | `.agents/skills/wrightkit-reclaim-entropy/SKILL.md` |
| Rust architecture/API/concurrency/responsibility review | `.agents/skills/wrightkit-rust-engineering-review/SKILL.md` |
| Test necessity/stability/duplication review | `.agents/skills/wrightkit-test-design-review/SKILL.md` |
| Independent change verification | `.agents/skills/wrightkit-verify-change/SKILL.md` |

## Global invariants

These rules always apply regardless of repository:

- Use [`GOAL.md`](GOAL.md) to resolve product-direction tradeoffs; do not duplicate or silently redefine its intent in repository-local guidance.
- Respect repository ownership boundaries: modify authoritative contracts in their owning repository, integrate cross-repository changes separately in consumers, and never bypass ownership for implementation convenience.
- Do not introduce complex abstractions only for hypothetical future needs.
- Keep source attribution, pinned reference identity, and related decision history where a semantic, compatibility, or regression workflow requires them.
- Do not silently weaken diagnostics, tests, compatibility expectations, validation, or error handling to make CI pass.
- When replacing, hiding, or retiring a public or canonical boundary (API, model, IR, or protocol), verify continuity of surviving accepted contracts through the replacement boundary itself. Tests or checks exercising only retired, private, or compatibility-only paths do not prove replacement completeness.
- Do not treat upstream bugs or implementation details as ideal WrightKit semantics without an accepted contract or reference comparison.
- Do not invent WrightKit-only OPY or OSTW syntax unless explicitly approved as a language-level design.

## Role and self-authorization

WrightKit uses role separation to prevent an agent from self-authorizing decisions owned by another role:

- **PM** owns scope and execution planning.
- **Architect** owns significant architecture and contract decisions.
- **Engineer** implements approved work.
- **QA** independently attempts to falsify the implementation and verifies acceptance criteria.

An agent that proposes a compatibility, public-contract, or architecture change must not self-authorize that decision when the repository's role model assigns it to an Architect, maintainer, or product owner.

## Implementation context preflight

A short request such as `implement #123` or `fix #123` is sufficient instruction for normal implementation work. The agent is responsible for resolving the relevant project context before editing code; the user should not have to repeat repository guidance, architecture links, or skill names in every prompt.

Before substantive implementation:

1. Read the linked Issue and nearest repository `AGENTS.md`.
2. Identify the affected domain and owning repository before choosing an implementation location.
3. Resolve the current architecture or contract relevant to that domain through repository guidance and durable documentation. Treat ADRs as decision records; verify current implementation reality separately.
4. Inspect the current implementation, affected consumers, tests, and dependency boundaries far enough to establish current reality.
5. Compare the Issue contract, current architecture/contract, and current code reality. When replacing, hiding, or retiring a public or canonical boundary, verify that surviving accepted capabilities are accounted for on the replacement boundary, explicitly approved for removal/change, or transferred to another owner. `ready-for-implementation` does not waive this consistency check.
6. If they are materially inconsistent, stop as Engineer and report the mismatch to the appropriate Architect/owner instead of choosing a new architecture by implementation convenience.
7. If they are aligned, load the specialized policy or skills indicated by the actual risk surface and implement the smallest complete coherent change.

Do not preload every architecture document or specialist skill. The preflight exists to find the smallest relevant context, not to turn each implementation into a repository-wide audit.

## Delivery is part of completion

For repository work, a locally correct implementation is not delivered until the remote review surface reflects it.

- For `implement #123`, `fix #123`, or equivalent implementation requests: complete verification, commit on a non-default branch, push, and open or update a PR.
- For requests to address PR review findings:
  - keep changes strictly focused on actionable review findings without unrelated cleanup, redesign, or scope expansion;
  - commit verified corrections and push to the existing PR head branch (do not stop after local commit);
  - review-fix work is complete only when the PR is handed back to review: handle affected review threads without hiding unresolved findings, and re-request review or signal handoff per [`docs/issue-readiness-and-pr-audit.md`](docs/issue-readiness-and-pr-audit.md);
  - the final report must identify the updated PR, pushed commits, thread status, and review handoff state.
- Never push implementation commits directly to the default branch unless the user explicitly authorizes that exception.
- Stop before push/PR or review handoff only when local-only work was requested or a concrete blocker prevents delivery/handoff (e.g. missing permissions, auth failure, branch conflict); report the blocker and exact local state.
- A final report for implementation or review-fix work should identify the PR containing the delivered change and its review handoff state, or the concrete blocker that prevented completing it.

Why: the PR, not an agent worktree, is the shared review surface. Leaving verified changes in local state, or pushing fixes without thread handling and re-review handoff, stalls the review lifecycle and leaves reviewers unaware that verification is needed.

## Tests and verification artifacts

One-off command output, reports, screenshots, and temporary reproducers are not repository state merely because they helped with one task.

Before committing a test, fixture, snapshot, corpus case, or other test data, load [`docs/testing-policy.md`](docs/testing-policy.md) and confirm that it protects a durable contract or regression in an existing feature-owned location. For material changes, use `.agents/skills/wrightkit-verify-change/SKILL.md` to attempt independent falsification.

## Independent ablation

After completing design or implementation work, do not declare it complete until an independent agent/reviewer who did not author it has run an ablation pass.

- For design, remove, defer, or replace each new abstraction, dependency, state mechanism, public API, protocol boundary, or cross-repository contract. Keep it only when its absence demonstrably breaks an approved requirement, invariant, ownership boundary, acceptance criterion, or known real workflow. Hypothetical future flexibility is not enough.
- For implementation, use a temporary patch/worktree to remove, disable, or simplify the key new behavior and rerun the relevant regression, contract, corpus/fixture, or real-project checks. The check supporting the change should fail again under the relevant ablation; otherwise investigate ineffective code or insufficient coverage.
- Ablation is not merely rerunning the normal test suite or mechanically mutation-testing every line. Do not add production APIs or permanent scaffolding solely for ablation. Keep ablation artifacts temporary unless they independently deserve durable regression/contract status.
