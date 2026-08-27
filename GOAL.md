# GOAL — what WrightKit is for

Context: for humans and agents working anywhere in WrightKit. Read this before `AGENTS.md`.

This document is **what we want**. `AGENTS.md` is **how work is routed and governed**. Architecture documents and ADRs define durable technical contracts; Issues and PRs define current work. When multiple technically reasonable choices compete, use this document to decide which one better serves WrightKit.

## The one sentence

**WrightKit is a modern, tooling-first development toolchain for Overwatch Workshop: it helps developers and coding agents understand, check, analyze, safely modify, and maintain real Workshop projects across raw Workshop and its established source languages.**

## What that means

### 1. Wright is the user product

`wright` is WrightKit's flagship user-facing product. A Workshop developer should be able to install Wright and use the toolchain without first learning WrightKit's repository layout, IRs, provider protocol, or internal architecture.

`workshop-rs`, `opy-rs`, and `deltin-rs` exist because reliable tooling requires reliable owning implementations. They should remain independently usable and maintain clear semantic ownership, but their purpose is not to create competing product surfaces. Missing language or Workshop semantics belong in the implementation that owns them, not in Wright as an integration workaround.

Common workflows should favor convention over configuration. WrightKit should work well in the environments Workshop developers actually use and should avoid unnecessary platform or shell assumptions; platform-specific investment should follow real user evidence.

### 2. Tooling is the product; compilation enables it

The product center is developer understanding and safe action:

- actionable correctness diagnostics;
- lint and static analysis;
- semantic inspection and query;
- project relationships and provenance;
- validated source edits and refactoring;
- agent-facing and embedding tools;
- editor and CI integration;
- Workshop resource-cost and static stability analysis.

Compilation and reconstruction are necessary capabilities, especially for language independence, migration, validation, and agent workflows. They are not the end state by themselves. WrightKit must not become a collection whose primary value is transpilation.

When compiler completeness competes with a real tooling workflow, prefer the work that unblocks real development unless the compiler gap prevents correct understanding, diagnostics, analysis, editing, or validation.

### 3. Real projects are the primary measure of usefulness

Breadth is useful only when it serves actual development. Do not optimize for symmetric support matrices, feature counts, test counts, or roadmap bookkeeping at the expense of making real projects reliable.

Different languages may receive different investment when their real usage and blockers differ. A less-used language does not need artificial feature parity with a more-used one. Compatibility corpora, fixtures, and conformance work exist to discover and prevent failures that matter to the toolchain; completing an inventory is not an end in itself.

### 4. Humans come first, and coding agents are a first-class outcome

Human developers remain the primary UX reference. Wright should have useful, understandable human-facing CLI and editor behavior rather than turning its normal interface into a machine protocol.

At the same time, agent-driven Workshop development is a first-class long-term outcome. WrightKit should give capable coding agents structured, deterministic access to the same semantic understanding, diagnostics, queries, edits, and validation that humans rely on. Agents should not need to scrape pretty terminal output or independently reimplement Workshop, OverPy, or DEL/OSTW semantics.

WrightKit does **not** aim to become a generic or full coding-agent framework. The toolchain provides the Workshop-specific capabilities; a coding agent supplies planning, repository exploration, product-context discovery, and general software-development orchestration.

WrightKit also does not invent project intent. If a project documents why an event or mechanic exists, an agent can discover that context in the project's source, comments, documentation, or agent guidance. Wright's responsibility is to make the code and Workshop semantics trustworthy and queryable, not to manufacture background knowledge that the project never recorded.

### 5. The long-term agent outcome is real-project maintenance from intent

A successful mature workflow is one where a developer can state a requirement in natural language and a capable coding agent can use WrightKit to:

1. understand the relevant source and semantic relationships;
2. locate the implementation that controls the behavior;
3. query canonical Workshop and language facts;
4. make targeted source changes while preserving unrelated source;
5. run diagnostics and static analysis;
6. inspect cost and static stability risks where applicable;
7. compile or otherwise validate the result;
8. repair problems it can justify repairing; and
9. report both the result and anything the toolchain cannot prove statically.

The user should be able to focus increasingly on requirements and outcomes rather than language mechanics. Reaching that outcome is more important than forcing equal feature breadth across every supported source language.

### 6. Workshop is the canonical semantic and conversion hub

Canonical Workshop semantics, catalog data, settings, validation, representation, emission, and reviewed gameplay facts belong in `workshop-rs`.

Source-language implementations own their own syntax, preprocessing/project loading, type and semantic models, diagnostics, provenance, and lowering/reconstruction behavior. Wright consumes those capabilities and adds cross-language product tooling.

Conversions between high-level languages should normally pass through Workshop rather than creating a second direct semantic mapping whose maintenance cost exceeds its value. Direct OPY↔DEL conversion is not a core product burden.

Workshop-to-source reconstruction should improve toward useful, idiomatic, human-maintainable source. Preserve information that survives the Workshop representation when practical, including comments that remain represented. Do not promise recovery of information that compilation discarded, such as original macros, helper abstractions, or source structure that no longer exists.

### 7. Compatibility is semantic, not textual

For supported constructs, WrightKit should preserve the behavior defined by the source language when lowering to Workshop and preserve the contracts required for trustworthy tooling.

Formatting differences, temporary variables, generated helper shape, optimizer decisions, rule layout, or compiler-output identity are not correctness requirements unless they affect observable semantics, diagnostics, provenance, analysis, reconstruction, or safe editing.

Real upstream quirks that existing projects depend on may need compatibility behavior. Preserve such behavior when evidence requires it, but do not confuse an upstream bug or implementation accident with ideal language semantics.

WrightKit does not promise that any generated Workshop program is guaranteed to run correctly on a live Overwatch server. WrightKit's responsibility is correct static understanding, transformation, validation, and clearly bounded analysis; server state and other external runtime failures are outside that guarantee.

### 8. WrightKit follows Workshop evolution independently

New Workshop heroes, maps, actions, values, enums, settings, and other canonical content should not wait for an OverPy or DEL/OSTW upstream release before WrightKit can understand them at the Workshop layer.

While an upstream source language remains maintained, WrightKit should follow its language definition rather than creating a WrightKit-only dialect. If an upstream implementation is abandoned, WrightKit should be capable of continuing the language as a backward-compatible maintained implementation, including normal language evolution needed to express new Workshop capabilities.

Historical project compatibility should be preserved where practical, but future investment in an inactive language may decrease when real usage no longer justifies equal support for new features.

### 9. Workshop knowledge exists to improve development tooling

WrightKit should maintain the canonical technical knowledge required to make Workshop development effective: language/catalog facts, settings, hero and ability facts where useful, element/resource costs, documented Workshop execution semantics, and other evidence-backed properties that tools can reason about.

The boundary is development tooling, not game design. WrightKit should not decide whether a hero is balanced, whether a mechanic is fun, or what a project ought to design.

Static stability analysis should explain risks and the reasoning behind them rather than claim certainty the toolchain cannot have. If code creates unusually high per-frame work or another evidence-backed risk pattern, report the risk and useful evidence; leave the final engineering decision to the developer or agent.

Canonical semantic facts require strong evidence. Uncertain community claims should not silently become canonical truth.

### 10. Core lint is small and trustworthy; the lint ecosystem can be broad

Built-in lint should favor a small set of high-confidence rules with stable meaning and low false-positive cost. WrightKit may maintain optional official rule collections outside the core.

The long-term lint model should allow community rules to be distributed through ordinary package/source mechanisms such as Git or GitHub. WrightKit does not need to operate a central marketplace merely to enable an ecosystem.

Official rules do not gain a hidden precedence mechanism over configured community rules. Configuration conflicts should be explicit and resolvable. A strong community rule may later be reviewed and adopted into WrightKit's built-in or official rule sets.

### 11. Safe source modification grows from evidence

The desired transformation path is:

**semantic understanding → validated source edits → original source**

Do not make full-file regeneration the default editing model merely because an IR exists. Preserve comments, trivia, formatting, and unrelated structure where practical.

Automatic fixes and semantic refactoring are a long-term product capability, but correctness comes before aggressiveness. Early implementations should be conservative. Expand automatic changes as the semantic model and validation evidence justify stronger guarantees.

### 12. Open integration does not mean generic-first design

Third-party tooling should be able to build on stable WrightKit capabilities where there is demonstrated value. `workshop-rs` in particular should be useful as a canonical Workshop library, and stable provider/integration contracts can allow additional language implementations to participate in Wright tooling.

Do not pre-design a generic compiler framework for hypothetical languages or consumers. A real third-party language with real users can justify integration work when it exists. Public and extensible does not mean speculative abstraction comes first.

Before 1.0, foundational APIs may still need breaking changes to reach the correct durable design. Existing real consumers deserve consideration, but hypothetical compatibility must not freeze known-bad architecture.

## How to choose when good options compete

Prefer the choice that, in order:

1. unblocks a real Workshop development workflow;
2. improves semantic correctness, diagnostics, analysis, or trustworthy project understanding;
3. strengthens agent-driven development without degrading the human developer experience;
4. enables safe, localized source modification;
5. fixes the missing capability in the repository that owns that semantics;
6. improves Workshop technical analysis, interoperability, compilation, or reconstruction in service of the above;
7. keeps the solution small, local, and evidence-backed.

Do not trade these outcomes for support-matrix symmetry, compiler-output identity, roadmap bookkeeping, architecture polish, or speculative extensibility.

## How we know WrightKit is succeeding

For an existing developer, Wright should increasingly replace manual searching and guesswork with normal development-tooling workflows: useful diagnostics, semantic inspection, relationship analysis, dead/unreachable-code detection, resource-cost visibility, static stability-risk analysis, and safe fixes where the evidence is strong enough.

For an AI-driven developer, a capable coding agent should increasingly be able to take a real Workshop requirement, use WrightKit to understand and modify the project, validate the result, and clearly identify what remains outside static proof.

Those outcomes matter more than any fixed count of languages, rules, corpus files, commands, or passing feature cells.

## What we deliberately do not optimize for

WrightKit is not trying to become:

- a generic compiler framework;
- a full IDE or heavy UI product;
- Workshop project hosting or a GitHub replacement;
- a generic AI coding-agent framework;
- a game runtime simulator;
- a pure transpiler collection;
- a platform that judges gameplay balance or game-design quality;
- a source of WrightKit-only OPY/OSTW syntax while those languages have an authoritative maintained definition.

When work starts drifting toward one of these outcomes, require a separate product decision rather than assuming it belongs in WrightKit.
