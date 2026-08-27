# GOAL: what WrightKit is for

Context: for humans and agents working anywhere in WrightKit. Read this before `AGENTS.md`.

This document states what WrightKit is for. `AGENTS.md` covers workflow routing and repository policy. Architecture documents and ADRs define technical contracts; issues and pull requests track active work. When competing technical choices come up, use these goals to decide.

## Summary

WrightKit is a tooling-first development toolchain for the Overwatch Workshop. It helps developers and coding agents inspect, analyze, safely edit, and maintain real Workshop projects across raw Workshop script and its established source languages.

## Core principles

1. **Wright is the primary user product.** Developers interact with `wright`; `workshop-rs`, `opy-rs`, and `deltin-rs` are independently usable language and semantic engines. Users should not need to understand the repository layout, intermediate representations, or provider protocols to use the toolchain. Missing semantics belong in their owning implementation, not papered over inside `wright`.

2. **Tooling comes first; compilation supports it.** The primary value of WrightKit lies in diagnostics, static analysis, semantic navigation, validated edits, editor and CI integrations, and cost analysis. Compilation, conversion, and reconstruction exist to enable those workflows across languages, not to turn the project into a transpiler collection.

3. **Real workflows take priority over symmetric feature matrices.** Reliability in actual projects matters more than nominal parity between languages, raw feature counts, or test totals. Different languages can receive different levels of effort depending on real-world adoption. Compatibility suites and corpora exist to expose failures that affect users and tooling, not to check off inventory lists.

4. **Human developers and coding agents share the same core tooling.** Human-facing CLI and editor workflows must stay clear and usable. Coding agents also need structured, deterministic access to semantic analysis, diagnostics, AST queries, and validated edits without scraping terminal output or reimplementing language parsers. WrightKit gives coding agents Workshop-specific tooling; it does not try to be a generic agent framework.

5. **Enable intent-driven development for agents.** Over time, an agent should be able to take a high-level requirement for a project, use WrightKit to inspect the code and its dependencies, apply targeted edits, check diagnostics, evaluate server-load risks, and flag what it cannot statically verify. Developers can then focus on design requirements rather than Workshop syntax details.

6. **Workshop is the semantic and conversion hub.** `workshop-rs` owns canonical Workshop semantics and validated engine facts. Individual language crates own their respective syntax and semantics, and `wright` integrates them into cross-language tooling. Conversions between languages like OPY and DEL route through Workshop representation instead of bespoke direct bridges. When reconstructing source code from Workshop rules, the output should be idiomatic and maintainable while retaining any structure preserved by the Workshop format.

7. **Compatibility means matching semantics, not exact text.** Supported language constructs must preserve execution behavior, diagnostic contracts, and safe editing boundaries. Identical formatting, matching temporary variable names, optimizer choices, and byte-for-byte compiler output are not correctness criteria unless they alter behavior. Known upstream quirks can be preserved when projects depend on them, but upstream bugs should not be treated as intended language design. WrightKit cannot guarantee that generated code will execute without issues on a live game server.

8. **Support Workshop updates independently.** Official Workshop additions like new heroes, maps, actions, and settings should land without waiting on upstream OPY or OSTW releases. While an upstream language remains active, WrightKit follows its specification rather than inventing custom dialects. If an upstream compiler is abandoned, WrightKit will maintain compatibility and evolve the language when real user demand justifies it.

9. **Game knowledge supports tooling, not game design judgments.** WrightKit tracks verified technical facts about the Workshop environment: element catalogs, script resource limits, and static stability hazards. The toolchain reports risks and explains its static reasoning without claiming to guarantee runtime behavior. Its scope ends at technical tooling; WrightKit does not evaluate gameplay balance, fun, or game design quality.

10. **Keep the core small and predictable.** Built-in lints focus on high-confidence rules with minimal false positives; broader checks belong in optional or community rule sets. Stable integration points allow third-party tools and language providers to connect when needed, but the project does not build abstractions for hypothetical consumers. Default conventions handle standard workflows; platform-specific work requires backing evidence from real users.

## Decision priorities

When competing technical approaches are on the table, prefer in this order:

1. Unblock a real Workshop development workflow.
2. Improve semantic correctness, diagnostic accuracy, or static analysis.
3. Strengthen coding-agent workflows without degrading the human developer experience.
4. Enable safe, localized source edits.
5. Fix the issue in the repository that owns the underlying semantics.
6. Advance Workshop analysis, interoperability, compilation, or reconstruction in service of the priorities above.
7. Keep the implementation small, focused, and backed by concrete evidence.

Never trade these outcomes for feature-matrix symmetry, identical compiler output, roadmap checklists, architectural purism, or speculative extensibility.

## Measuring success

For human developers, Wright replaces manual guesswork with standard tooling: accurate diagnostics, dependency analysis, resource-cost estimates, static stability warnings, and automated safe fixes.

For agent-driven workflows, an agent can take a project requirement, use WrightKit to inspect and edit the codebase, validate changes, and clearly report any behavior the compiler cannot prove statically.

These outcomes matter far more than reaching arbitrary targets for supported languages, lint rules, corpus size, or test matrix completion.

## Non-goals

WrightKit is not intended to be:

- a generic compiler framework
- a full IDE or heavy UI product
- Workshop project hosting or a GitHub replacement
- a generic AI coding-agent framework
- a game runtime simulator
- a pure transpiler collection
- a platform that judges gameplay balance or game-design quality

Detailed engineering, testing, repository ownership, compatibility standards, and workflows are defined in `AGENTS.md`, organization policies, repository guides, and ADRs rather than repeated here.
