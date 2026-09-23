# Documentation management

WrightKit documentation uses progressive disclosure so humans and agents can load the smallest
current context needed for a task.

## Layout

Durable project documentation belongs under `docs/`.

Repository-root documentation is limited to entry points or files whose location is required by
tooling or ecosystem conventions, such as:

- `README.md` — concise project overview and documentation router;
- `AGENTS.md` — agent routing and repository constraints;
- `LICENSE` and other legal files;
- tool-required standard files that must remain colocated.

A subtree may keep a local `README.md` when it is an index for that subtree rather than a second
standalone documentation authority. Skill files and generated/release-managed files remain where
their owning tool requires them.

Each repository with durable documentation should provide `docs/README.md` as its documentation
index.

## Progressive disclosure

Keep each document focused on one responsibility.

Higher-level documents should contain:

1. the purpose and boundary of the area;
2. a concise summary of the current contract;
3. links to narrower documents for details.

Do not grow a single architecture, compatibility, testing, release, or contributor document into a
general knowledge dump. Split a document when it contains independently loadable responsibilities
or readers routinely need only one part of it. Prefer semantic/domain boundaries over arbitrary
line-count or file-count thresholds.

Do not duplicate the same contract across multiple documents merely to improve discoverability.
Route to the owning document instead.

## Authority and history

Keep these concerns separate:

- current durable contracts and invariants;
- ADR / decision history;
- current implementation and executable tests;
- mutable execution state in Issues, PRs, CI, releases, and project tooling.

Current documentation describes the current contract. Git history and ADRs preserve history.
Do not keep stale prose merely as an archive.

## Change synchronization

A change that materially changes supported behavior, a public contract, architecture, ownership,
user-facing workflow, contributor workflow, or operational procedure must update the corresponding
durable documentation in the same change when applicable.

Implementation and review must explicitly check whether documentation is affected. Do not create a
documentation edit for incidental implementation details that do not change a durable contract.

Repository-local `AGENTS.md` files should route contributors to `docs/README.md` and enforce this
synchronization rule.

## Drift audits

Rules reduce omissions but do not prove documentation remains current.

Periodically compare durable documentation with current contracts and implementation reality,
especially:

- after major implementation waves or migrations;
- after architecture or ownership changes;
- before major releases or stability milestones;
- when a stale or contradictory document is discovered.

An audit should classify findings as:

- aligned;
- stale or contradicted;
- duplicated authority;
- oversized/mixed responsibility;
- missing routing/index;
- undocumented durable contract.

Fix the owning document rather than copying current status into multiple places.

## Review rule

Documentation-only restructuring must preserve meaning unless the task explicitly changes the
contract. Moving or splitting a document is not authorization to redesign architecture, compatibility,
or product behavior.
