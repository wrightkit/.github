---
name: wrightkit-reclaim-entropy
description: Audit or safely simplify WrightKit repositories by finding accidental maintenance surface, proving real consumers and contracts, ranking deletion/consolidation candidates, and applying only evidence-backed cuts. Use for entropy reclamation, code simplification, dead or redundant abstractions, duplicate state/APIs, obsolete fallbacks, compatibility residue, or post-milestone cleanup across WrightKit repositories. Treat public crates, CLI/protocol behavior, persisted formats, OPY/DEL/OSTW/raw Workshop compatibility, security boundaries, and licensing boundaries as protected contract surfaces unless explicitly approved for change.
---

# WrightKit Reclaim Entropy

Use this skill to reduce maintenance obligations without treating line count as the objective.

The authoritative WrightKit rules are in the organization-wide Code Entropy Policy and Testing Policy. Repository-local `AGENTS.md`, architecture documents, ADRs/specs, compatibility documents, and contribution rules may add stricter constraints. They take precedence over generic simplification heuristics.

Core rule: scanners create candidates; consumer, contract, ownership, history, and verification evidence justify a cut.

## Select a mode

Choose one mode from the user's request:

- **Audit** — inspect and rank candidates; do not edit files.
- **Apply** — implement only approved or clearly Risk A simplifications, one ownership boundary at a time, and verify them.
- **Focused investigation** — determine whether a named abstraction, lifecycle mechanism, compatibility path, dependency, or state representation is accidental or load-bearing.

If the request only says to review, audit, find, inspect, or report, default to Audit. Do not turn an audit into an implementation pass without an explicit instruction to change the repository.

## Establish WrightKit context first

Before judging code:

1. Read the nearest `AGENTS.md` and follow its routing instructions.
2. Read relevant architecture/spec/compatibility documents and repository contribution/testing guidance.
3. Identify whether the repository publishes a crate, CLI, protocol/tool interface, generated artifact, or compatibility layer consumed elsewhere.
4. Inspect repository status and preserve unrelated work.
5. Identify generated, vendored, fixture, migration, corpus, and public-package paths.
6. In Apply mode, discover the repository's actual narrow and broad validation commands and record a baseline when practical.

Do not infer that a local repository is the complete consumer universe. WrightKit is a multi-repository ecosystem.

## Protected contract surfaces

Treat the following as contract-sensitive by default:

- public APIs of published Rust crates;
- stable CLI commands, flags, exit behavior, diagnostics, and machine-readable output;
- configuration and schema keys;
- serialized, persisted, migration-sensitive, cached, or wire data;
- MCP, LSP, RPC, agent-tool, or other protocol surfaces;
- generated artifacts consumed by another component;
- declared compatibility with OverPy, DEL/OSTW, raw Overwatch Workshop, locale/catalog data, or other ecosystem targets;
- repository/license boundaries that intentionally isolate implementations;
- security, authorization, trust-boundary validation, data-integrity, failure-observability, and resource-quiescence behavior.

Removing or changing these is Risk C unless the user or owning architecture/product decision has already explicitly approved the change.

## Survey for entropy

Start with central production surfaces and recent architectural growth, not only compiler warnings.

Look for:

1. **Unconsumed surface** — internal APIs, traits, hooks, events, config, registries, helpers, packages, or feature flags with no real consumer.
2. **Duplicate truth** — multiple states, caches, summaries, registries, events, or representations that encode one fact and require synchronization.
3. **Speculative generality** — one-implementation traits, permanently fixed switches, unused fallback chains, abandoned extension points, or future-proof abstractions with no current owner.
4. **Extra route/layer** — pass-through wrappers, duplicate front doors, adapters with no independent contract, or helpers that obscure a single caller.
5. **Lifecycle duplication** — multiple flags, guards, channels, sentinels, futures, cancellation paths, or cleanup mechanisms representing one transition.
6. **Misplaced defense** — defensive copying, validation, rollback, or hostile-object machinery protecting a same-process typed handoff rather than a real trust/ownership boundary.
7. **Hand-rolled infrastructure** — local implementations already cleanly provided by `std`, the platform, or an already justified dependency.
8. **Support residue** — tests, docs, snapshots, fixtures, generated inventories, examples, or package structure that survive only for behavior that no longer exists.
9. **Added-then-abandoned residue** — an implementation was removed or superseded but config, schemas, compatibility branches, tests, docs, or decision records still imply that it exists.
10. **Cross-repository duplication** — two WrightKit repositories maintain equivalent logic or facts that should have one owner, provided consolidation does not violate licensing or product boundaries.

Do not treat deliberate independent adapters/backends or compatibility implementations as duplication until their separate ownership has been disproved.

## Prove or reject each candidate

For every exact candidate:

1. Search the symbol, path, package/crate name, CLI/config key, feature, event/wire string, generated reference, and alternate invocation syntax.
2. Inspect callers and callees instead of relying on hit counts.
3. Check dynamic loading, registries, reflection/string dispatch, code generation, macros, build scripts, feature-gated paths, examples, and operational scripts.
4. Classify consumers as production, non-production, or ambiguous/external.
5. For public/shared surfaces, inspect known downstream WrightKit consumers and published/documented contracts. If this cannot be established, downgrade confidence.
6. Read history and decision records. Identify what problem created the surface and whether that reason still exists.
7. For stateful/concurrent code, map each state mechanism to an owner and lifecycle transition before consolidating it.
8. State what observable capability or future extension is lost by the cut, even if the answer is none.
9. Estimate net maintenance reduction: concepts, contracts, code, tests owned only by the removed behavior, docs/config/generated artifacts, and dependencies removed minus migration/glue/dependency cost added.
10. Name the smallest decisive check that would fail if the cut were wrong.

Reject or downgrade a candidate when:

- a production or external consumer exists;
- dynamic reachability cannot be ruled out;
- a current architecture/compatibility decision justifies it;
- the change is actually a feature, compatibility, licensing, or public-API decision;
- complexity is merely moved to another wrapper or repository;
- a new dependency introduces comparable or greater maintenance cost;
- the candidate is tiny, speculative, or outside the requested scope.

## WrightKit risk classes

### Risk A — high-confidence internal cut

Examples:

- private unreachable implementation with no dynamic consumer;
- one of two internal representations where one canonical owner is clearly load-bearing;
- obsolete internal support artifacts after their owner is gone;
- pass-through internal layers with no contract or independent ownership.

May be implemented in Apply mode with normal verification.

### Risk B — review-required simplification

Examples:

- shared internal or crate-visible APIs;
- concurrent/lifecycle consolidation;
- dependency replacement;
- cross-repository migration with identified consumers;
- changes that substantially reshape tests, generated artifacts, or build structure.

Implementation is allowed only when the task already authorizes it; make the evidence and tradeoff explicit for review.

### Risk C — product/architecture decision

Examples:

- public published APIs;
- stable CLI/protocol/tool contracts;
- persisted or migration-sensitive formats;
- declared OPY, DEL/OSTW, raw Workshop, locale, or other compatibility surfaces;
- security/trust/data-loss/resource-ownership boundaries;
- licensing-boundary changes.

Do not self-authorize these. In Audit mode, report them separately. In Apply mode, implement only if the user or an already accepted architecture/product decision explicitly approves the change.

## Rust dependency rule

For a proposal to replace code with a crate, do not use deleted LOC as the deciding metric.

Check:

- whether `std` or an already-used dependency is sufficient first;
- MSRV/toolchain fit;
- platform and feature compatibility, including WASM or constrained targets where relevant;
- transitive dependencies and feature graph;
- compile-time/binary-size impact when material;
- maintenance health and supply-chain/security exposure;
- licensing compatibility;
- wrapper/glue and dedicated-test burden that remains.

A dependency is a simplification only if the ecosystem-wide maintenance obligation is lower.

## Testing rule

Tests are evidence, not automatically immutable implementation snapshots and not disposable line count.

Follow the WrightKit Testing Policy:

- keep tests that protect surviving observable behavior, compatibility, error propagation, provenance, or independent correctness evidence;
- remove tests that exist only to exercise a fully removed internal mechanism;
- do not change an expectation merely because the simplified implementation now produces something else;
- add or preserve a decisive regression when it makes the risk boundary observable.

Green tests alone do not prove deletion safety.

## Apply a proven cut

When applying:

1. Work in one ownership boundary unless an atomic cross-repository migration is required.
2. Remove the obsolete contract end to end: declaration, implementation, branches, owned tests, exports, config, docs, examples, snapshots, generated inventories, and dependencies where appropriate.
3. Collapse duplicate truth onto one canonical owner; do not add synchronization glue between two representations that should no longer coexist.
4. Avoid compatibility shims when no compatibility obligation exists. When one does exist, preserve it or use an explicit migration/deprecation plan.
5. Do not mix unrelated cleanup into the same change.
6. Follow repository branch/PR rules; never bypass role or main-branch protections to land a simplification.

## Validate

After each non-trivial cut:

1. search again for stale symbols, strings, paths, configuration, docs, generated references, and feature flags;
2. run the smallest decisive check first;
3. run relevant formatting, lint, test, build, codegen, compatibility, and smoke gates defined by the repository;
4. inspect the complete diff for scope growth and accidental expectation weakening;
5. explicitly verify any public, persisted, protocol, compatibility, cross-repository, or user-visible boundary touched.

If validation fails, determine whether the candidate was load-bearing, the implementation was incomplete, or the baseline was already red. Do not weaken a meaningful check to force the simplification through.

## Audit output

Rank only meaningful candidates. Prefer a few well-supported cuts to a long cleanup wishlist.

Use this format:

```text
[confidence | Risk A/B/C] candidate
obligation: concept/state/API/compatibility surface currently maintained
evidence: consumers; dynamic/external checks; history/decision owner
cut: exact declarations, implementation, artifacts, tests/docs, dependencies, or concepts removed
tradeoff: observable capability/compatibility/future extension lost
verify: smallest decisive check plus broader gates
net effect: maintenance obligations removed minus replacement/migration cost
```

Also list high-value candidates intentionally rejected or downgraded when the missing evidence is important for future work.

Finding no safe cut is a valid audit result.

## Agent-team use

Broad discovery may be delegated to cheaper/subordinate agents, including repository search, history inspection, caller tracing, test classification, and mechanical implementation.

The delegating/reviewing agent remains responsible for epistemic ownership:

- require workers to return concrete evidence, not only conclusions;
- directly inspect critical contract evidence and the final diff;
- do not allow the same role to self-authorize a Risk C decision when WrightKit's role model assigns that authority elsewhere;
- use an independent QA/review pass for material simplifications rather than accepting the implementing agent's green-test summary as sufficient proof.

## Recommended cadence

Do not run this skill automatically on every task.

Use it deliberately:

- after a milestone or minor-version objective;
- after a repository split, migration, replacement, or architectural wave settles;
- after sustained AI-agent implementation where abstractions have accumulated;
- before stabilizing a public API or compatibility surface;
- when reviews repeatedly encounter wrappers, fallbacks, duplicate state, or speculative interfaces.

Prefer Audit first. Approve a small number of candidates, then Apply them in separate reviewable changes.