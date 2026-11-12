# WrightKit Workspace Agent Routing

Repository-local `AGENTS.md` files specialize contracts for their own repository. They must not duplicate shared policy, but they may add stricter or domain-specific requirements that take precedence locally.

The user request and linked Issue, when present, set task scope. [`docs/goal.md`](docs/goal.md) resolves project-direction tradeoffs. Decisions and corrections often live in the Issue's comments, its parent Issue, and linked or referenced Issues and PRs rather than in the Issue body. A short request such as `implement #123` is sufficient when the Issue and repository provide the needed context. Substantive behavior work also needs a verifiable outcome: before editing, identify the tests or checks that will decide completion, as defined in [`docs/issue-readiness.md`](docs/issue-readiness.md#verifiable-outcomes). The Issue's acceptance criteria and [Delivery is part of completion](#delivery-is-part-of-completion) define when the work is done; [When to stop](#when-to-stop) defines when to ask before then.

Paths here assume the workspace root, the directory that holds the `.github` and `.agents` checkouts: `docs/` links resolve to `.github/docs/`, and `.agents/skills/` paths resolve from that root.

## Repository routing

Use this map to identify the likely owner, then confirm current ownership and read its `AGENTS.md` before substantial work.

| Concern | Primary repository |
| --- | --- |
| Canonical Workshop semantics, catalog, locales, parsing, validation, representation, emission | `workshop-rs` |
| OverPy-compatible language implementation | `opy-rs` |
| DeltinScript / OSTW-compatible language implementation | `deltin-rs` |
| Workshop runtime simulation (execution model, probe captures) | `athena` |
| Provider process/data protocol | `language-provider-protocol` |
| User-facing tooling, orchestration, integration, analysis, agent surfaces | `wright` |
| Product website | `wrightkit.dev` |
| Experimental web editor for native Workshop; owns no Workshop semantics | `editor` (planned) |
| GitHub Action that installs and caches the Wright CLI | `setup-wright` |
| Build, packaging, release artifacts | `wright` (`dist/`, `.github/workflows/release.yml`); `homebrew-tap` holds only the published Homebrew formula |
| Shared policy, CI patterns, GitHub governance | `wrightkit/.github` |
| Reusable agent skills and procedures for WrightKit work | `wrightkit/.agents` |
| Optional user-facing agent skills for Workshop projects, such as the vendored `wright` guide | `wrightkit/skills` |
| Workshop.code wiki to agent-friendly Markdown | `workshop-md-converter` |
| Agent benchmark harness, scenarios, published results (private) | `benchmark-suite` |

For cross-repository work, read each affected repository's guidance and verify the contract across the boundary.

## Policy routing

Load a document only when its concern is relevant. Do not preload them. Paths without a directory are under `docs/`.

| Task concern | Load |
| --- | --- |
| Product direction, scope, non-goals, or a choice between competing technical approaches | [`goal.md`](docs/goal.md) |
| PR review; which policy owns a coding-standards judgment | [`CODING_STANDARDS.md`](CODING_STANDARDS.md) (repository root) |
| Start of a multi-step task; naming the judgment behind a decision | [`principles/README.md`](docs/principles/README.md) |
| Agent guidance, `AGENTS.md` or `CLAUDE.md` content, skills | [`agent-guidance.md`](docs/agent-guidance.md) |
| Documentation layout, synchronization, drift audits | [`documentation.md`](docs/documentation.md) |
| Implementation design, scope discipline, abstractions, idiomatic Rust, responsibility locality | [`engineering-quality.md`](docs/engineering-quality.md) |
| Issue readiness, verifiable outcomes, preflight, closing boundary, boundary migration continuity | [`issue-readiness.md`](docs/issue-readiness.md) |
| PR review findings, review-fix threads, follow-up review | [`pr-review.md`](docs/pr-review.md) |
| Tests, fixtures, snapshots, expected results, support classifications (entry point for the three rows below) | [`testing-policy.md`](docs/testing-policy.md) |
| Upstream structural compatibility, raw Workshop/locale compatibility, oracle or differential comparisons, real-project regressions, corpora | [`compatibility-testing.md`](docs/compatibility-testing.md) |
| Malformed, extreme, or adversarial input; fuzzing | [`robustness-testing.md`](docs/robustness-testing.md) |
| Verification boundaries, merge-time CI acceptance, behavior-changing PR evidence | [`verification-and-acceptance.md`](docs/verification-and-acceptance.md) |
| Dead code, redundancy, over-engineering, mutable-inventory documentation | [`entropy-policy.md`](docs/entropy-policy.md) |
| CI failure triage | Classify by job surface: fix local/quality gates in place; for LPP integration, check the protocol commit first; triage differential/compatibility under [`compatibility-testing.md`](docs/compatibility-testing.md) |
| Rust CI toolchain, caching, job composition, runtime-bound gates | [`rust-ci.md`](docs/rust-ci.md) |
| Rust build artifact growth, dev/test profiles, worktree lifecycle, local storage | [`rust-build-artifacts.md`](docs/rust-build-artifacts.md) |
| Git hooks, the agent tool-call hook, file size limits | [`mechanical-guards.md`](docs/mechanical-guards.md) |
| Releases, tags, artifact publication | [`release-engineering.md`](docs/release-engineering.md) |
| Procedures: Issue orchestration, entropy reclamation, Rust engineering review, test design review, independent change verification | `.agents/skills/<name>/SKILL.md`: `orchestrate-issues`, `reclaim-entropy`, `rust-engineering-review`, `test-design-review`, `verify-change` |

## Global invariants

These rules always apply regardless of repository:

- Do not duplicate or silently redefine the intent of [`docs/goal.md`](docs/goal.md) in repository-local guidance.
- Respect repository ownership boundaries: modify authoritative contracts in their owning repository, integrate cross-repository changes separately in consumers, and never bypass ownership for implementation convenience.
- Durable documentation belongs under `docs/` and follows [`docs/documentation.md`](docs/documentation.md). When supported behavior, a public contract, architecture, ownership, workflow, or operational procedure changes, update the owning documentation in the same change when applicable; review must check this explicitly.
- Keep source attribution, pinned reference identity, and related decision history where a semantic, compatibility, or regression workflow requires them.
- Do not silently weaken diagnostics, tests, compatibility expectations, validation, or error handling to make CI pass.
- When replacing, hiding, or retiring a public or canonical boundary (API, model, IR, or protocol), verify surviving accepted contracts through the replacement boundary itself, as defined in [Contract continuity for boundary migrations](docs/issue-readiness.md#contract-continuity-for-boundary-migrations).
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

Implementation requests are complete after relevant verification, a commit on a non-default branch, a push, and an open or updated PR. Never push implementation commits directly to the default branch unless the user explicitly authorizes that exception. Review-fix work also requires affected threads to be handled and follow-up review to be signaled as described in [`docs/pr-review.md`](docs/pr-review.md). Stop before delivery only for a local-only request or a concrete blocker, then give the [final report](#final-report).

Why: the PR, not an agent worktree, is the shared review surface. Leaving verified changes in local state, or pushing fixes without thread handling and re-review handoff, stalls the review lifecycle and leaves reviewers unaware that verification is needed.

## When to stop

Continue authorized, reversible work without routine confirmation. Stop and ask only when:

- missing information could materially change the outcome;
- an owner decision is unresolved;
- the Issue, documented contract, and current implementation materially conflict;
- the next action is external or irreversible and the task did not authorize it, such as force-pushing, pushing to a default branch, deleting branches, tags, releases, or data, publishing a release or package, or closing or editing Issues and PRs outside the task; or
- a concrete blocker prevents progress.

Before stopping, finish whatever does not depend on the answer.

Do not end a turn while owed work remains by writing a summary that announces the next step without taking it, offering to continue unless told otherwise, listing decisions that by your own account block nothing, or stopping because a milestone is done or the turn has been long. Put status notes and recommendations in the same message as the next action.

Why: a text-only turn ends the work until someone replies. In unattended worktree runs, a mid-task report silently becomes an unfinished delivery.

## Final report

End a task with a report a reviewer can act on without reading the session. Lead with what needs the reader: an open decision, a blocker, or an action that needs their authority; say so when nothing does. Then give the delivered state (PR, pushed commits, review handoff) or the local state if delivery stopped, the independent reference used for verification, and anything you could not confirm, with where you looked. Leave out a step-by-step account of the session. For multi-step work, end with a `Principles Named or Used` section as defined in [`docs/principles/README.md`](docs/principles/README.md#using-principles).

Why: the reader's first job is to unblock the work, and an unconfirmed claim listed among verified ones tends to be accepted as verified.

## Tests and verification artifacts

One-off command output, reports, screenshots, and temporary reproducers are not repository state merely because they helped with one task. Test data belongs in an existing feature-owned location only when it protects a durable contract or regression under [`docs/testing-policy.md`](docs/testing-policy.md).

Verify material changes against an authority independent of the implementation, such as an accepted contract, a pinned upstream oracle, or a real project, not only against tests written with the change. Independence comes from that authority, not from another agent: do not spawn a verifier or reviewer agent to re-check your own work. The independent second pass is PR review or an assigned QA role, which may use `.agents/skills/verify-change/SKILL.md`.

Why: a same-model agent re-reading the same change shares its blind spots and adds cost; a check against an outside authority catches a wrong expectation that both the implementation and its tests agree on.

## Simplification review

Substantive design or implementation work applies one ablation pass, as described in [`docs/engineering-quality.md`](docs/engineering-quality.md): the Engineer asks whether newly added mechanisms can be removed or simplified while the approved requirement and contract still hold, and PR review checks the result independently. Ablation reviews necessity, not correctness.
