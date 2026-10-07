# Agent work loop

This policy defines how agents discover, propose, implement, and deliver WrightKit work without drifting from [`goal.md`](goal.md). It adds the loop around the rules in [issue readiness](issue-readiness.md), [PR review](pr-review.md), and [verification and acceptance](verification-and-acceptance.md); it does not restate them.

## The loop

```text
evidence -> proposed Issue (needs-*) -> owner promotes -> implementation PR -> CI + independent review -> owner merges
```

Each stage has one kind of actor. Discovery agents propose; the owner decides readiness; Engineer agents implement settled contracts; reviewers verify; the owner merges.

Why: [role separation](../AGENTS.md#role-and-self-authorization) keeps an agent from authorizing its own scope. An agent that discovers a problem, judges it ready, implements it, and approves it would be checking its own work against its own premises.

## Discovery proposes from evidence

An agent-proposed Issue starts from a concrete failure, not from a goal principle read in isolation. Acceptable evidence is something a reader can re-run or open: an agent-benchmark result, a differential or corpus failure, a CI failure that recurs, a real-project regression, an [entropy](entropy-policy.md) audit finding, or a drift between a documented contract and the code.

A proposed Issue must carry:

- the evidence, with a link or command that reproduces it;
- the [goal principle](goal.md#core-principles) it serves and where it falls in the [decision priorities](goal.md#decision-priorities);
- the owning repository, per [repository routing](../AGENTS.md#repository-routing);
- acceptance criteria that form a [verifiable outcome](issue-readiness.md#verifiable-outcomes), or the decision that must be made first.

Without evidence and a verifiable outcome, do not file it. Check for an existing Issue first and comment there instead of duplicating.

Why: [`goal.md`](goal.md) ranks reliability in real workflows over checklist coverage. An Issue derived from a principle alone is a roadmap guess, and an implementation of it has no independent check.

## Readiness is the owner's call

Discovery agents file Issues as `needs-design` or `needs-decision`, with the open question and a recommendation. Only the owner moves an Issue to `ready-for-implementation`. Use the semantic states in [issue readiness](issue-readiness.md#issue-readiness) as labels with those exact names in every repository, so a queue can be read mechanically.

An Engineer agent starts only from an Issue the owner has marked `ready-for-implementation` or from an explicit request that names one.

Why: the owner settles scope and contract; an agent-run pre-check shares the proposing agent's blind spots and is not independent authorization.

## Implementation boundaries

- One Issue per agent run, and one open implementation PR per repository from the loop at a time.
- Several agents of different kinds may work the same queue, so claim an Issue before substantive work: check that no open PR or branch references it, then open a draft PR that references it as soon as the first commit is pushed. An Issue with such a PR is taken; pick another or stop. The claim lives in GitHub, not in any one agent's session, so it must survive that agent stopping, and the owner may close a stale claim.
- Follow [Engineer preflight](issue-readiness.md#engineer-preflight) and [Delivery is part of completion](../AGENTS.md#delivery-is-part-of-completion). Verify against an authority independent of the change.
- Work stays inside the owning repository; cross-repository effects follow the contract-first order in [`AGENTS.md`](../AGENTS.md#repository-routing).
- CI failures on the loop's own PR are fixed in place under the surface triage in [`AGENTS.md`](../AGENTS.md#policy-routing). Do not weaken checks, diagnostics, or compatibility expectations to turn CI green.
- Release PRs, dependency-update PRs that change a public contract, and repositories the owner has marked paused are outside the loop. Read the pause from the current roadmap Issue rather than from this document.
- Merging, pushing to a default branch, and closing Issues stay with the owner.

Why: agents share one GitHub identity, so an assignee cannot tell them apart, while a draft PR is visible to all of them. A narrow, single-owner change is reviewable in one pass, and the loop stays safe to run unattended because the irreversible steps are not in it.

## Stop conditions

Stop and route to the owner under [When to stop](../AGENTS.md#when-to-stop). In the loop this most often means: the Issue, documented contract, and current code disagree; the acceptance criteria cannot be turned into a check that could fail; the fix belongs to a different repository; or the work would deviate from upstream compiler output without a recorded exception.

## Drift review

Periodically compare merged loop work with [`goal.md`](goal.md): which principle each change served, and whether work concentrated where real workflows are not failing. Record findings on the current roadmap Issue. This is a reading of outcomes, not a metric to optimize.

Why: individually correct PRs can still concentrate effort away from what the goal ranks first.
