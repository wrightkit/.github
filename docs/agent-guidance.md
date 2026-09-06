# WrightKit Agent Guidance Principles

This document defines how durable agent-facing guidance should be written across WrightKit.

The goal is to improve agent judgment, not to simulate a program with a growing list of instructions. Agents already have general reasoning ability; durable guidance should focus it on WrightKit's contracts, priorities, and failure modes.

## Guide reasoning, not execution by checklist

Prefer principles and decision criteria over exhaustive lists of cases. Describe what matters, what tradeoff is being protected, and how to recognize an exception.

Why: detailed rule inventories are brittle. They tend to turn examples, current repository shapes, and reviewer preferences into accidental contracts. Principles transfer better to new code and new failure modes.

Use hard rules only when the boundary itself is non-negotiable, such as repository ownership, security, licensing, compatibility, branch safety, public contracts, or role authorization.

## Explain why

Important guidance should explain the reason behind the rule: correctness, ownership, maintainability, reviewability, provenance, compatibility, or another concrete project goal.

Why: a reason lets the agent distinguish the intended invariant from the wording used to express it. This reduces mechanical compliance that produces the wrong result in an unfamiliar case.

## Separate contracts from heuristics

A contract defines behavior or authority that must be preserved. A heuristic helps make a good engineering choice when several correct implementations are available.

Do not present heuristics as eligibility tests. For example, AHA and the Rule of Three can help judge whether an abstraction is demonstrated, but the number of textual repetitions does not itself decide whether an abstraction is correct.

Why: engineering quality depends on domain shape, ownership, consumers, and maintenance cost, not arbitrary thresholds.

## Use examples to illustrate judgment

Examples should clarify a principle or failure mode. They should not silently become a complete list of supported cases, forbidden constructs, preferred APIs, or required implementation shapes.

Why: agents often generalize strongly from examples. A representative example is useful; an accidental pseudo-specification is not.

## Route instead of repeat

Stable organization policy belongs in `wrightkit/.github`; reusable procedures belong in `wrightkit/.agents`; repository-specific architecture and contracts belong in the owning repository.

Skills should link to canonical policy rather than copying it. Repository guidance should specialize shared policy only where local ownership requires it.

Why: duplicate instructions drift, consume context, and can disagree about which copy is authoritative.

## Make context acquisition a routing responsibility

Normal implementation prompts should be able to remain short, for example `implement #123` or `fix #123`. Durable guidance should make the agent responsible for resolving the smallest relevant context: Issue, owning repository, repository guidance, current architecture/contract, current implementation reality, and specialized policy or skills when their risk surface applies.

Do not require users or Issue bodies to repeat every relevant document path, architecture summary, or skill invocation. Instead, provide stable routing from always-read guidance to the current owner-side contract. When no trustworthy current contract can be resolved, or when the Issue, documented contract, and implementation disagree materially, guidance should make the stop condition explicit rather than inviting an Engineer to infer a new design.

Why: context routing is part of the project harness. If correct implementation depends on a user remembering which documents an agent should read, or on an agent first recognizing a missing concept before it can discover the guidance for that concept, the routing layer is not doing its job.

## Design skill metadata for discovery

Treat a skill's discovery metadata as an activation surface, not merely a summary of what the full skill contains. Before the skill body is loaded, the agent should be able to recognize relevant task shapes, changed artifacts, and failure signals from the metadata alone.

Front-load the concepts that should trigger the skill, including important indirect contexts. A task can materially touch testing, architecture, compatibility, verification, cleanup, semantic placement, or responsibility growth even when its headline is a dependency bump, parser feature, lowering change, refactor, CI fix, or migration. Prefer semantic trigger vocabulary that generalizes to new cases rather than exhaustive keyword lists or duplicated routing rules.

When a skill is added or its activation surface changes, check its description against representative trigger and non-trigger prompts. A normal relevant prompt should discover the skill without explicit naming, while routine unrelated work should not activate it unnecessarily.

Why: policy and procedures are ineffective when discovery depends on the agent first classifying the task using the same missing concept the skill was meant to supply.

## Keep durable guidance stable

Do not encode current issue state, release versions, counts, temporary gaps, current priorities, or other mutable reality into durable agent guidance unless the fact itself is a stable contract.

Why: current reality should be queried from its source of truth. Stable guidance remains useful across releases and is safer for prompt/document caching.

## Make authority and stop conditions clear

Tell the agent when it does not have authority to continue. Unresolved product, architecture, compatibility, public-contract, licensing, or cross-repository ownership decisions should be routed to the appropriate owner instead of decided through implementation convenience.

Why: an agent can often produce a plausible implementation for an undecided question. That does not make the decision authorized.

## Prefer concise procedures

A reusable skill should normally contain only the context needed to perform its task: purpose, relevant principles, hard boundaries, a broad workflow, stop conditions, and the evidence or output that completes the task.

This is guidance, not a required section template. Omit structure that does not help the task.

Why: procedural detail is valuable when ordering matters, but excessive instructions compete with the actual repository evidence the agent needs to reason about.
