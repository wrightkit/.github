# WrightKit Workspace Agent Routing

This file is the workspace-level agent routing entry point for the WrightKit organization.

This file carries durable organization constraints and routing; it is not a technical manual or a second copy of the product goal.

Repository-local `AGENTS.md` files specialize contracts for their own repository. They must not duplicate shared policy, but they may add stricter or domain-specific requirements that take precedence locally.

The user request and linked Issue, when present, set task scope. [`docs/goal.md`](docs/goal.md) resolves project-direction tradeoffs. Identify the owning repository, read its linked Issue and nearest `AGENTS.md` when present, then load only relevant policy or skills. Before editing, also read the Issue's comments, its parent Issue, and linked or referenced Issues and PRs, even when the request does not mention them; decisions and corrections often live there rather than in the Issue body. A short request such as `implement #123` is sufficient when the Issue and repository provide the needed context. Continue authorized reversible work without routine confirmation. Ask or stop only when missing information could materially change the outcome, an owner decision is unresolved, the Issue, documented contract, and current implementation materially conflict, or an external or irreversible action is not authorized.

No proprietary include syntax is required.

## Repository routing

Use this map to identify the likely owner, then confirm current ownership and read its `AGENTS.md` before substantial work.

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

For cross-repository work, read each affected repository's guidance, change the authoritative contract in its owning repository, integrate consumers separately, and verify the contract across the boundary.

## Policy routing

Load policy documents only when their concern is relevant. Do not preload all of them.

| Task concern | Load |
| --- | --- |
| Writing or revising durable agent guidance, AGENTS content, or reusable skills | [`docs/agent-guidance.md`](docs/agent-guidance.md) |
| Durable documentation layout, progressive disclosure, documentation synchronization, or drift audits | [`docs/documentation.md`](docs/documentation.md) |
| Implementation design, scope discipline, demonstrated abstractions, simple/idiomatic Rust, responsibility locality, and stable-vs-dynamic documentation | [`docs/engineering-quality.md`](docs/engineering-quality.md) |
| Issue readiness, implementation preflight, and public/canonical boundary migration continuity | [`docs/issue-readiness.md`](docs/issue-readiness.md) |
| One-pass PR review, review findings, review-fix thread handling, and follow-up review | [`docs/pr-review.md`](docs/pr-review.md) |
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

- Use [`docs/goal.md`](docs/goal.md) to resolve product-direction tradeoffs; do not duplicate or silently redefine its intent in repository-local guidance.
- Respect repository ownership boundaries: modify authoritative contracts in their owning repository, integrate cross-repository changes separately in consumers, and never bypass ownership for implementation convenience.
- Durable documentation belongs under `docs/` and follows [`docs/documentation.md`](docs/documentation.md). When supported behavior, a public contract, architecture, ownership, workflow, or operational procedure changes, update the owning documentation in the same change when applicable; review must check this explicitly.
- Do not introduce complex abstractions only for hypothetical future needs.
- Keep source attribution, pinned reference identity, and related decision history where a semantic, compatibility, or regression workflow requires them.
- Do not silently weaken diagnostics, tests, compatibility expectations, validation, or error handling to make CI pass.
- When replacing, hiding, or retiring a public or canonical boundary (API, model, IR, or protocol), verify continuity of surviving accepted contracts through the replacement boundary itself. Tests or checks exercising only retired, private, or compatibility-only paths do not prove replacement completeness.
- Source-language compilation converges structurally on the established upstream compiler output ([`docs/goal.md`](docs/goal.md) principle 7). Do not deviate from it, including for an apparent upstream bug, without a recorded exception approved by the owner.
- Do not invent WrightKit-only OPY or OSTW syntax unless explicitly approved as a language-level design.
- Do not create GitHub cross-references to repositories outside WrightKit from issues, PRs, comments, or commit messages unless notifying that thread is intended. Cite external issues and PRs inside a code span, such as `owner/repo#123`, or by pinned version or commit. Why: a linked reference adds a backlink to the external thread, notifying its maintainers and exposing WrightKit planning there; a bare `#123` after an external reference also silently links to the local repository instead.

## Role and self-authorization

WrightKit uses role separation to prevent an agent from self-authorizing decisions owned by another role:

- **PM** owns scope and execution planning.
- **Architect** owns significant architecture and contract decisions.
- **Engineer** implements approved work.
- **QA** independently attempts to falsify the implementation and verifies acceptance criteria.

An agent that proposes a compatibility, public-contract, or architecture change must not self-authorize that decision when the repository's role model assigns it to an Architect, maintainer, or product owner.

## Delivery is part of completion

Implementation requests are complete after relevant verification, a commit on a non-default branch, a push, and an open or updated PR. Never push implementation commits directly to the default branch unless the user explicitly authorizes that exception. Review-fix work also requires affected threads to be handled and follow-up review to be signaled as described in [`docs/pr-review.md`](docs/pr-review.md). Stop before delivery only for a local-only request or a concrete blocker; report the PR and handoff state, or the blocker and local state.

Why: the PR, not an agent worktree, is the shared review surface. Leaving verified changes in local state, or pushing fixes without thread handling and re-review handoff, stalls the review lifecycle and leaves reviewers unaware that verification is needed.

Do not end a turn while owed work remains by writing a summary that announces the next step without taking it, offering to continue unless told otherwise, listing decisions that by your own account block nothing, or stopping because a milestone is done or the turn has been long. Put status notes and recommendations in the same message as the next action and continue with whatever does not depend on an answer. Stop only under the ask-or-stop conditions above or for a concrete blocker.

Why: a text-only turn ends the work until someone replies. In unattended worktree runs, a mid-task report silently becomes an unfinished delivery.

## Tests and verification artifacts

One-off command output, reports, screenshots, and temporary reproducers are not repository state merely because they helped with one task. Test data belongs in an existing feature-owned location only when it protects a durable contract or regression under [`docs/testing-policy.md`](docs/testing-policy.md).

Verify material changes against an authority independent of the implementation, such as an accepted contract, a pinned upstream oracle, or a real project, not only against tests written with the change. Independence comes from that authority, not from another agent: do not spawn a verifier or reviewer agent to re-check your own work. The independent second pass is PR review or an assigned QA role, which may use `.agents/skills/wrightkit-verify-change/SKILL.md`.

Why: a same-model agent re-reading the same change shares its blind spots and adds cost; a check against an outside authority catches a wrong expectation that both the implementation and its tests agree on.

## Simplification review

Substantive design or implementation work applies one ablation pass, as described in [`docs/engineering-quality.md`](docs/engineering-quality.md): the Engineer asks whether newly added mechanisms can be removed or simplified while the approved requirement and contract still hold, and PR review checks the result independently. Ablation reviews necessity, not correctness.
