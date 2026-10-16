# Engineering principles

A principle is a named, distilled piece of engineering judgment: a good practice that tells an agent which way to lean when valid options remain. It is not a procedure, a checklist, or a restatement of a policy. Each principle file is at most 30 lines.

Read this index before starting a multi-step task. Open a principle file only when its trigger matches the work. Policy documents keep the detailed rules; a principle links to them instead of copying them.

## Index

| Principle | Lean this way when |
| --- | --- |
| [minimum-persistent-mechanism](minimum-persistent-mechanism.md) | a design adds state, indirection, config, a dependency, or a layer |
| [demonstrated-abstraction](demonstrated-abstraction.md) | repeated code or a hypothetical consumer suggests a shared helper or trait |
| [owner-fixes-it](owner-fixes-it.md) | a missing semantic could be patched in a consumer instead of its owner |
| [upstream-is-the-spec](upstream-is-the-spec.md) | OPY or DEL behavior could be "improved" away from the upstream compiler |
| [independent-authority](independent-authority.md) | the evidence that a change works comes from tests written with the change |
| [query-dont-encode](query-dont-encode.md) | guidance or docs are about to record counts, versions, or current status |

## Repository-local principles

A judgment tied to one repository's domain lives in that repository's `docs/principles/`, in the same shape, and is routed from its `AGENTS.md`. This directory holds only judgment that applies across repositories. A repository principle is usually promoted from an entry in its `docs/LESSONS.md` whose prevention depends on a choice made while authoring; read the local index with this one.

## Using principles

- **Before a multi-step task:** read the index. Skip it for single-step answers.
- **While working:** name a principle only when it changed a choice, and say which choice it changed. A principle that merely agrees with what you were already doing is not named.
- **At the end of the reply:** for multi-step work, add a `Principles Named or Used` section listing `id — the choice it changed`, or `None`. Reviewers use it to see which judgments shaped the change; it is an audit trail, not a record of your reasoning.

Why: the index lets an agent recognize a relevant judgment without loading every policy. Requiring the decision a principle changed keeps naming honest, because a name without a changed choice is decoration.

## Adding a principle

Add one only for judgment that recurs and that no deterministic mechanism can carry. First ask whether a lint, type, schema, test, CI check, or API contract can express the constraint; if it can, build that and do not write the principle. When a check covers part of a principle, keep only the judgment part and name the check in `Enforced by`. Delete a principle once a deterministic check makes it redundant.

Write each file in this shape: `Applies when`, `Principle`, `Changes the choice between`, `Enforced by`, `Why`, `Detail`. Do not add steps, examples that read as a complete list, or mutable facts.
