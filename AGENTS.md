# WrightKit Workspace Agent Routing

This file is the workspace-level agent routing entry point for the WrightKit organization.

Its job is to route agents and contributors to the right authoritative source for each concern. It is not a technical manual.

Repository-local `AGENTS.md` files specialize contracts for their own repository. They must not duplicate shared policy, but they may add stricter or domain-specific requirements that take precedence locally.

To apply this routing from a local workspace:

1. Read this file.
2. Read the nearest repository-local `AGENTS.md`.
3. Load routed policy or skills only when the task touches their concern.

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
| Organization-wide shared policy, CI patterns, and reusable skills | `wrightkit/.github` |

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
| Implementation design, scope discipline, demonstrated abstractions, and stable-vs-dynamic documentation | [`docs/engineering-quality.md`](docs/engineering-quality.md) |
| Tests, fixtures, corpora, snapshots, expected results, compatibility evidence, fuzzing, verification artifacts | [`docs/testing-policy.md`](docs/testing-policy.md) |
| Durable documentation that summarizes mutable inventories or status | [`docs/entropy-policy.md`](docs/entropy-policy.md) |
| A CI job failed and the owning surface is unclear (Rust quality vs. LPP integration vs. differential/compatibility vs. dist/release) | Classify by job before fixing: `rust-quality`/local gates → fix in place; cross-repo integration (`lpp-client-integration`) → identify whether the failure is in `wright` or the pinned `language-provider-protocol` commit before changing either; differential/compatibility jobs → treat a new failure as a compatibility regression under `docs/testing-policy.md`, not a flaky test, unless proven otherwise |
| Dead-code, redundancy, over-engineering, post-migration simplification | [`docs/entropy-policy.md`](docs/entropy-policy.md) |
| Rust CI toolchain, caching, and job composition | [`docs/rust-ci.md`](docs/rust-ci.md) |
| Release engineering, tagging, and artifact publication | [`docs/release-engineering.md`](docs/release-engineering.md) |
| Entropy reclamation workflow | [`skills/wrightkit-reclaim-entropy/SKILL.md`](skills/wrightkit-reclaim-entropy/SKILL.md) |
| Evidence-first change verification | [`skills/wrightkit-verify-change/SKILL.md`](skills/wrightkit-verify-change/SKILL.md) |

## Global invariants

These rules always apply regardless of repository:

- Respect repository ownership boundaries. Modify authoritative contracts in their owning repository.
- Integrate cross-repository changes separately in consumers.
- Do not bypass ownership boundaries for implementation convenience.
- Do not introduce complex abstractions only for hypothetical future needs.
- Preserve provenance for semantic, compatibility, and regression evidence.
- Do not silently weaken diagnostics, tests, compatibility expectations, validation, or error handling to make CI pass.
- Do not treat upstream bugs or implementation details as ideal WrightKit semantics without evidence.
- Do not invent WrightKit-only OPY or OSTW syntax unless explicitly approved as a language-level design.

## Role and self-authorization

WrightKit uses role separation to prevent an agent from self-authorizing decisions owned by another role.

Typical separation:

- **PM** owns scope and execution planning.
- **Architect** owns significant architecture and contract decisions.
- **Engineer** implements approved work.
- **QA** independently attempts to falsify the implementation and verifies acceptance criteria.

An agent that proposes a compatibility, public-contract, or architecture change must not self-authorize that decision when the repository's role model assigns it to an Architect, maintainer, or product owner.

## Verification evidence

Verification evidence that is useful for a single task is not automatically repository state.

Before committing any test, fixture, report, log, benchmark output, screenshot, or other proof artifact to a repository, load [`docs/testing-policy.md`](docs/testing-policy.md) and apply its evidence admission criteria.

For focused change verification, use the [`wrightkit-verify-change`](skills/wrightkit-verify-change/SKILL.md) skill.

## Product direction

WrightKit is tooling-first. Prioritize capabilities that improve understanding, checking, analysis, modification, automation, interoperability, or reliability for real Workshop projects.

Compatibility targets observable semantics and declared contracts, not byte-identical output, temporary variables, optimizer behavior, formatting, or internal IR.
