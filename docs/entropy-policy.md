# WrightKit Code Entropy Policy

This document defines organization-wide rules for simplifying WrightKit code without deleting behavior that is still part of a product, compatibility, or ecosystem contract.

The objective is not to minimize line count. The objective is to reduce accidental maintenance obligations: duplicated truths, abandoned surfaces, speculative abstractions, redundant lifecycle state, obsolete compatibility machinery, and layers that no longer justify their cost.

Repository-local guidance may add stricter or domain-specific requirements, but it must not weaken this policy.

## Applicability

Use this policy when work includes any of the following:

- dead-code, redundancy, or over-engineering cleanup;
- removal or consolidation of APIs, traits, events, configuration, state, adapters, packages, or commands;
- replacement of custom infrastructure with the Rust standard library, platform facilities, or dependencies;
- removal of tests, fixtures, snapshots, documentation, compatibility paths, or generated artifacts because their owning implementation changed;
- architectural simplification after migrations, rewrites, milestone completion, or repeated AI-assisted changes.

Do not load or run an entropy audit for every ordinary feature change. Prefer deliberate audits at useful boundaries such as the end of a milestone or minor-version cycle, after a migration or large refactor, or when duplicated state and compatibility layers are visibly accumulating.

## 1. Simplification removes obligations, not merely lines

A simplification is valuable when it reduces the number of concepts, states, contracts, dependencies, or representations that contributors and agents must keep coherent.

A diff with fewer lines is not sufficient evidence. Moving the same complexity behind another wrapper, compatibility shim, helper, or abstraction is not entropy reclamation.

Prefer, in order:

1. removing an unnecessary contract or representation;
2. using an existing canonical representation;
3. using an appropriate Rust or platform primitive;
4. reusing an already justified dependency;
5. adding a new dependency only when its total maintenance cost is lower than the implementation it replaces.

## 2. Establish the contract before proposing deletion

Before classifying a surface as removable, identify whether it participates in any current contract.

Contract-sensitive surfaces include, where applicable:

- public Rust APIs and published crates;
- CLI commands, flags, exit behavior, diagnostics, and machine-readable output;
- configuration keys and schemas;
- serialized, persisted, cached, or migration-sensitive data;
- wire, protocol, MCP, LSP, RPC, or agent-tool interfaces;
- generated artifacts consumed outside the producing module;
- compatibility with OverPy, DEL/OSTW, raw Overwatch Workshop, locale data, or other declared ecosystem targets;
- documented behavior that users are reasonably expected to depend on;
- licensing or repository boundaries intentionally used to isolate implementations.

Repository-local architecture and compatibility documents define additional contracts.

A pre-1.0 version number is not blanket permission to remove a public surface. A repository may explicitly define some pre-1.0 APIs as unstable and allow breaking changes; when such a versioning policy exists, those surfaces may be treated as review-required rather than product-stable. Without that explicit policy, public surfaces remain contract-sensitive.

## 3. Repository search is evidence, not proof of no consumers

`rg`, compiler warnings, dead-code tools, dependency analyzers, and similar scanners are candidate generators.

For each candidate, inspect actual call sites and dynamic entrypoints. Search symbols, strings, paths, configuration names, registry keys, protocol fields, feature flags, generated references, and alternate invocation forms.

Classify consumers as:

- **production** — shipped runtime code, operational scripts, real configuration, migrations, generated/runtime registries, or other execution paths;
- **non-production** — tests, docs, comments, snapshots, and support-only expected output;
- **ambiguous/external** — examples, plugins, reflection, dynamic loading, published APIs, downstream crates, user scripts, or cross-repository consumers.

A public item with no in-repository caller is not automatically dead. Published crates and stable CLI or protocol surfaces must be treated as externally consumable unless compatibility evidence shows otherwise.

## 4. Compatibility removal is a product decision

Removing reachable compatibility is not cleanup merely because the implementation looks redundant.

Changes that alter declared OPY, DEL/OSTW, raw Workshop, locale, file-format, CLI, protocol, or public-crate compatibility require explicit ownership and review. The change must state:

- what observable capability is removed or changed;
- whether migration, deprecation, or a version boundary is required;
- which repository or component owns the decision;
- how downstream users or repositories are affected.

An entropy audit may identify such a surface, but it must classify it as a product/architecture decision rather than silently deleting it.

## 5. Cross-repository consumers are first-class

WrightKit is a multi-repository ecosystem. A surface may be unused locally while still being required by another WrightKit component.

Before removing a shared crate API, schema, generated artifact, compatibility hook, CLI contract, or tool interface, inspect known ecosystem consumers and the owning documentation. If cross-repository evidence cannot be obtained, record the uncertainty and downgrade the candidate rather than assuming it is safe.

Do not introduce duplicate implementations across repositories merely to make one repository locally simpler. Simplification should reduce ecosystem-wide obligations, not relocate them.

## 6. Tests are evidence, not an untouchable implementation snapshot

Follow the [WrightKit Testing Policy](testing-policy.md).

Tests that exist only to preserve an obsolete internal mechanism may be removed with that mechanism. Tests that protect surviving observable behavior, compatibility, negative behavior, provenance, or independent correctness evidence must remain or be replaced with an equivalent or stronger check.

Do not weaken or rewrite a meaningful expectation simply to make a deletion pass. A green suite alone does not prove that a candidate was non-load-bearing.

## 7. Consolidate duplicated state only after mapping ownership

Stateful and asynchronous code often contains multiple flags, sentinels, channels, guards, promises/futures, cancellation paths, or cleanup mechanisms that appear to describe the same lifecycle.

Before collapsing them, identify the owner and transition protected by each mechanism. Preserve independent machinery when it protects genuinely different concerns such as:

- publication versus rollback;
- cancellation versus terminal-result arbitration;
- process/task ownership versus user-visible completion;
- flush/commit completion versus resource quiescence;
- trust-boundary validation versus internal typed handoff.

Collapse state only when two mechanisms truly encode the same fact and can share one canonical owner.

## 8. Rust dependency changes require ecosystem accounting

Replacing custom Rust code with a dependency can be a simplification, but line deletion alone is not sufficient justification.

Evaluate at least:

- MSRV and toolchain compatibility;
- target and feature compatibility, including WASM or other constrained targets where relevant;
- transitive dependency and feature-graph growth;
- compile-time and binary-size impact when material;
- maintenance health and supply-chain/security exposure;
- whether a wrapper and dedicated tests would recreate most of the removed complexity;
- licensing compatibility with the owning repository.

Prefer the standard library or already-justified dependencies when they cover the required semantics cleanly.

## 9. Security, trust, durability, and failure visibility are protected boundaries

Do not reclaim apparent entropy by removing:

- authorization or permission checks;
- validation at real trust boundaries;
- data-loss or corruption prevention;
- persistence compatibility that remains supported;
- cleanup required to stop tasks, processes, workers, or other owned resources;
- diagnostics or error propagation required to keep failures observable;
- accessibility or safety behavior that is part of a user-facing contract.

If one of these looks redundant, treat it as a high-risk architecture/security candidate and require stronger evidence and explicit review.

## 10. AI-assisted simplification requires independent judgment

AI agents are particularly prone to preserving every existing abstraction while adding another layer, or to deleting a surface after inspecting only local callers.

For material simplifications:

- the auditing agent must provide consumer and contract evidence, not aesthetic claims;
- an agent that proposes a compatibility/public-contract change must not self-authorize that decision when the repository's role model assigns it to an Architect, maintainer, or product owner;
- cheap/subordinate agents may perform broad discovery, history search, call-site tracing, and mechanical implementation, but final acceptance remains with the role responsible for the contract;
- final review should inspect the relevant diff and decisive evidence directly, not only a worker-agent summary.

## 11. Risk classes

Classify each candidate before implementation.

### A — high-confidence internal simplification

Typical examples:

- private code with no production or dynamic consumer;
- duplicated internal representation with one clear canonical owner;
- obsolete support artifact whose owning behavior is already absent;
- forwarding-only internal layer with no independent contract.

These may be implemented in a focused simplification change after normal verification.

### B — review-required simplification

Typical examples:

- crate-visible or shared internal APIs;
- an explicitly unstable pre-1.0 public surface when the repository's accepted versioning policy permits breaking changes;
- lifecycle consolidation in concurrent/stateful code;
- dependency replacement;
- cross-repository surfaces with verified consumers that must migrate together;
- removal that changes substantial test or generated-artifact structure.

Require explicit review of the evidence and migration scope before acceptance.

### C — product/architecture decision

Typical examples:

- public published APIs unless an accepted repository versioning policy explicitly classifies the surface as unstable;
- stable CLI or protocol behavior;
- persisted or migration-sensitive formats;
- declared compatibility surfaces;
- security/trust/durability boundaries;
- licensing-boundary changes.

An audit may recommend the change, but implementation requires the repository's normal architecture/product decision path or an already explicit user decision.

## 12. Audit evidence format

A useful candidate should be reportable in this compact form:

```text
[confidence | risk class] candidate
obligation: concept/state/API/compatibility surface currently maintained
evidence: production consumers; dynamic/external checks; history/decision owner
cut: exact declarations, implementations, artifacts, tests/docs, or dependencies removed
tradeoff: observable capability, compatibility, or future extension lost
verify: smallest decisive check plus broader required gates
net effect: concepts/contracts/dependencies removed; replacement cost introduced
```

Candidates without enough evidence should be recorded as uncertain or rejected, not inflated into a cleanup backlog.

## 13. Implementation discipline

Implement one ownership boundary at a time unless the contract itself requires an atomic cross-repository migration.

A complete cut should remove obsolete declarations and their owned implementation, branches, tests that exist only for the removed behavior, exports, configuration, documentation, examples, snapshots, generated inventories, and dependencies where applicable.

After each non-trivial batch:

1. search again for stale symbols, strings, paths, docs, and configuration;
2. run the narrowest decisive test first;
3. run the repository's relevant formatting, lint, test, build, codegen, compatibility, and smoke checks;
4. inspect the complete diff for accidental scope growth;
5. verify public, persisted, protocol, compatibility, and user-visible boundaries explicitly when they are in scope.

Keep changes reviewable and reversible. Do not mix opportunistic entropy cleanup into unrelated feature work unless the simplification is necessary for that feature.

## 14. Recommended cadence

Entropy reclamation is a maintenance phase, not a permanent tax on every task.

Good trigger points include:

- completion of a milestone or minor-version objective;
- after a migration, repository split, or architectural replacement settles;
- after a sustained AI-agent implementation wave;
- before stabilizing a public API or compatibility surface;
- when duplicated abstractions, states, fallbacks, or wrappers start recurring in reviews.

Prefer audit first, then approve and implement a small number of high-confidence cuts in separate reviewable changes.

## Upstream inspiration

This policy is independently written for WrightKit. Its evidence-first approach is informed by [DeepSeek Harness's simplification practice](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-find-simplifications/SKILL.md) and the generalized [`reclaim-code-entropy`](https://github.com/Yevanchen/reclaim-code-entropy) agent skill. Their guidance is useful input, but WrightKit's repository, compatibility, testing, Rust, licensing, and role constraints take precedence.
