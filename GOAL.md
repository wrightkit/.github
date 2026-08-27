# GOAL — what WrightKit is for

Context: for humans and agents working anywhere in WrightKit. Read this before `AGENTS.md`.

This document is **what we want**. `AGENTS.md` explains **how work is routed and governed**. Architecture documents and ADRs define technical contracts; Issues and PRs define current work. When multiple reasonable choices compete, come back here and ask which option better serves the goal.

## The one sentence

**WrightKit is a modern, tooling-first development toolchain for Overwatch Workshop: it helps developers and coding agents understand, check, analyze, safely modify, and maintain real Workshop projects across raw Workshop and its established source languages.**

## What that means, unpacked

1. **Wright is the user product.** `wright` is the flagship user-facing product; `workshop-rs`, `opy-rs`, and `deltin-rs` are necessary independently usable implementations with clear semantic ownership. Users should not need to understand WrightKit's repository layout, IRs, or provider architecture to use the toolchain. Fix missing semantics in the implementation that owns them rather than hiding gaps in Wright.

2. **Tooling is the product; compilation enables it.** Diagnostics, lint/static analysis, semantic inspection, validated source edits, agent tooling, editor/CI integration, and Workshop cost/stability analysis are the center of the product. Compilation, conversion, and reconstruction matter because they enable those workflows and language independence; WrightKit must not become a collection whose primary value is transpilation.

3. **Real projects matter more than symmetric feature matrices.** Prefer making real development workflows reliable over maximizing feature counts, test counts, or parity between languages. Different languages may receive different investment when their real usage differs. Corpora and compatibility work exist to expose failures that matter to users and tooling, not to make an inventory reach 100% for its own sake.

4. **Humans come first; coding agents are a first-class outcome.** Human-facing CLI and editor workflows should stay understandable and useful. At the same time, coding agents should get structured, deterministic access to the same semantic understanding, diagnostics, queries, edits, and validation without scraping human output or reimplementing Workshop/OPY/DEL semantics. WrightKit provides professional Workshop tooling to coding agents; it does not become a generic or full coding-agent framework.

5. **The long-term agent outcome is development from intent.** A capable coding agent should increasingly be able to take a natural-language requirement for a real project, use WrightKit to understand the relevant source and relationships, make targeted edits, run diagnostics and analysis, inspect resource/stability risks, compile or validate the result, repair justified problems, and report what remains outside static proof. The user should be able to focus increasingly on requirements and outcomes rather than language mechanics.

6. **Workshop is the canonical semantic and conversion hub.** Canonical Workshop semantics and reviewed technical facts belong in `workshop-rs`; source-language implementations own their language semantics; Wright owns the cross-language product/tooling layer. OPY↔DEL conversion should normally pass through Workshop rather than creating a second direct semantic mapping. Workshop-to-source reconstruction should aim for useful, idiomatic, maintainable source and preserve information that survives the Workshop representation where practical.

7. **Compatibility is semantic, not textual.** Supported constructs should preserve source-language behavior and the contracts required for trustworthy diagnostics, analysis, provenance, reconstruction, and safe editing. Formatting, temporary variables, helper shape, optimizer decisions, or compiler-output identity are not correctness requirements unless they change those outcomes. Real upstream quirks may be preserved when projects depend on them, without treating upstream bugs as ideal language design. WrightKit does not promise that a generated program is guaranteed to run correctly on a live Overwatch server.

8. **WrightKit follows Workshop evolution independently.** New Workshop heroes, maps, actions, values, settings, and other canonical content should not wait for OPY/DEL upstream updates. While a source language remains maintained, follow its language definition rather than inventing a WrightKit-only dialect. If an upstream implementation is abandoned, WrightKit should be capable of continuing backward-compatible maintenance and normal language evolution when real users still justify it.

9. **Workshop knowledge serves development tooling.** WrightKit should maintain strong-evidence technical facts needed for Workshop development, including catalog/game facts, resource costs, and statically reasoned stability risks. Report risk and reasoning rather than claiming runtime certainty. The boundary is technical development tooling: WrightKit does not decide whether gameplay is balanced, fun, or well designed.

10. **Keep the trustworthy core small and the ecosystem open.** Built-in lint should favor high-confidence rules with low false-positive cost; optional official and community rule collections can cover broader needs. Stable integration contracts may allow third-party tooling and language providers where real demand exists, but WrightKit should not pre-design a generic compiler framework for hypothetical consumers. Convention should beat configuration for common workflows, and platform-specific investment should follow real user evidence.

## How to choose when good options compete

Prefer the choice that, in order:

1. unblocks a real Workshop development workflow;
2. improves semantic correctness, diagnostics, analysis, or trustworthy project understanding;
3. strengthens agent-driven development without degrading human developer experience;
4. enables safe, localized source modification;
5. fixes the missing capability in the repository that owns that semantics;
6. improves Workshop technical analysis, interoperability, compilation, or reconstruction in service of the above;
7. keeps the solution small, local, and evidence-backed.

Do not trade these outcomes for support-matrix symmetry, compiler-output identity, roadmap bookkeeping, architecture polish, or speculative extensibility.

## How we know we are succeeding

For existing developers, Wright should replace more manual searching and guesswork with normal development-tooling workflows: actionable diagnostics, semantic inspection, relationship analysis, resource-cost visibility, static stability-risk analysis, and safe fixes where the evidence is strong enough.

For AI-driven development, a capable coding agent should increasingly be able to take a real Workshop requirement, use WrightKit to understand and modify the project, validate the result, and clearly identify what the toolchain cannot prove.

Those outcomes matter more than any fixed count of languages, rules, corpus files, commands, or passing feature cells.

## What we deliberately do not optimize for

WrightKit is not trying to become:

- a generic compiler framework;
- a full IDE or heavy UI product;
- Workshop project hosting or a GitHub replacement;
- a generic AI coding-agent framework;
- a game runtime simulator;
- a pure transpiler collection;
- a platform that judges gameplay balance or game-design quality.

Detailed engineering, testing, ownership, compatibility, and execution rules belong in `AGENTS.md`, routed organization policy, repository documentation, and ADRs rather than being repeated here.
