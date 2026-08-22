---
name: wrightkit-verify-change
description: Evidence-first verification procedure for WrightKit changes. Use when acceptance of a material semantic, compatibility, parser, compiler, source-edit, or protocol change requires independent falsification rather than just rerunning existing tests. Produces a clear VERIFIED / NOT VERIFIED / INCONCLUSIVE verdict and classifies all evidence artifacts by lifecycle.
---

# WrightKit Verify Change

Use this skill to verify that a specific change achieves its claimed outcome by producing and comparing concrete evidence, then classifying that evidence by lifecycle so it does not accumulate in the repository by default.

The authoritative testing rules are in [`docs/testing-policy.md`](../../docs/testing-policy.md). Repository-local `AGENTS.md` files may add stricter constraints. Both take precedence over this skill's defaults.

Do not use this skill to authorize repository-resident proof artifacts. Evidence admission requires the criteria in `docs/testing-policy.md § Evidence admission`.

## When to use this skill

Use it for material changes where a green existing test suite is not independent proof:

- semantic, compatibility, parser, or compiler changes;
- source-edit, refactor, or protocol contract changes;
- changes whose tests were authored alongside the implementation;
- acceptance criteria that require an independent falsification attempt;
- any change where the requester explicitly asks for independent verification.

Do not use it merely to rerun an existing passing suite and summarize the output.

## Procedure

Follow these steps in order. Record decisions at each step before continuing.

### Step 1 — Restate the claim in falsifiable form

Write a single concrete, falsifiable claim: what the change is supposed to do differently from before.

Acceptable: "After this change, `wright check` reports a structured diagnostic (not a panic) when an OPY import cycle is detected."

Not acceptable: "The change improves cycle detection."

If the claim cannot be falsified with a concrete test or observation, stop and request clarification.

### Step 2 — Identify the authoritative source or contract

Identify the independent source that defines correct behavior. This must be external to the implementation under test.

Acceptable sources:

- reproducible Overwatch Workshop client behavior;
- a pinned upstream compatibility oracle;
- an accepted public API or semantic contract;
- a provenance-linked real-world project regression;
- a deliberately specified invariant or property;
- a prior accepted issue or architecture decision.

If no independent source exists, report the verification as `INCONCLUSIVE` and recommend establishing a contract before accepting the change.

### Step 3 — Choose the smallest decisive verification surface

Select the narrowest test or observation that would fail if the claim were false.

Prioritize, in order:

1. An existing focused test targeting the claimed behavior.
2. A targeted new invocation against a minimal input that exercises the claim.
3. A real-world corpus case that previously triggered the failure class.
4. A differential comparison against a pinned oracle.

Do not default to running the full test suite as the primary verification surface. The full suite is a supporting gate, not evidence that the specific claim is correct.

### Step 4 — Capture a baseline

Before the change is applied (or using the pre-change state), capture a concrete artifact:

- command output, exit code, and stderr;
- structured output or emitted artifact;
- observable behavior or client-reproducible state.

Record the exact command used and, if applicable, a commit or input hash.

If the change is already applied and the pre-change state is unavailable, note this explicitly. Proceeding without a baseline is acceptable for small, obviously scoped changes; record the omission.

### Step 5 — Capture treatment

With the change applied, capture the same artifact using the same conditions and command.

Record the exact command, commit, and any relevant environment differences.

### Step 6 — Compare and interpret

Compare baseline and treatment artifacts concretely. The comparison must be against the independent contract from Step 2, not only against each other.

Identify:

- whether the treatment artifact matches the claimed correct behavior;
- whether the treatment differs from baseline in only the claimed way, or also in unexpected ways;
- whether any existing test or known-gap expectation changed;
- whether a plausible incorrect mutation of the implementation would be detected by this evidence.

### Step 7 — Verdict

State one of:

- **`VERIFIED`** — the concrete treatment artifact matches the independent contract; the change does what it claims; a plausible incorrect implementation would have been detected.
- **`NOT VERIFIED`** — the treatment artifact does not match the contract, or the change introduces unexpected behavioral differences.
- **`INCONCLUSIVE`** — the evidence cannot distinguish correct from incorrect behavior (missing baseline, missing contract, indeterminate environment, insufficient surface).

Do not omit the verdict. Do not substitute a summary ("seems to work") for one of these three outcomes.

If the verdict is `NOT VERIFIED` or `INCONCLUSIVE`, describe what additional evidence or implementation change would change the verdict.

### Step 8 — Classify evidence artifacts

For every artifact produced during verification, assign one lifecycle class:

| Class | Meaning | Default location |
| --- | --- | --- |
| `ephemeral` | Useful for this task only; does not protect a durable contract | `$TMPDIR`, CI artifacts, or discard after task |
| `promotion-candidate` | Minimized, deterministic, and protects a reusable contract; warrants admission review | Report for integration into the repository's canonical test structure |
| `canonical` | Already owned by an accepted test location with established provenance | Integrated per the owning repository's layout |

Most verification artifacts produced by this skill are `ephemeral` by default. Report `promotion-candidate` artifacts explicitly without committing them; the owning maintainer or QA role decides whether and where to integrate them.

## Evidence admission (summary)

Before promoting any artifact from `ephemeral` to `promotion-candidate` or `canonical`, confirm all of the following:

- a durable observable contract, invariant, or regression is protected;
- a plausible incorrect implementation would be detected;
- value survives the current PR or task;
- the artifact is minimal and deterministic;
- an existing canonical test or corpus location can own it;
- it does not duplicate equivalent coverage;
- external or real-world inputs retain required provenance and licensing information.

If any criterion fails, the artifact stays `ephemeral`.

Full admission criteria are in [`docs/testing-policy.md`](../../docs/testing-policy.md).

## Constraints

- A green existing test suite is not independent proof. Do not report `VERIFIED` based solely on rerunning the suite without comparing against an independent contract.
- Do not scatter issue-specific test files, report files, benchmark dumps, or debug logs into the repository merely to demonstrate the claim. These are `ephemeral` by default.
- Do not self-authorize permanent repository artifacts. Promotion requires the admission criteria above and an explicit decision by the owning maintainer or QA role.
- If verification reveals that a reusable regression guard is warranted, report it as a `promotion-candidate` for integration, not a committed artifact.

## Output format

Summarize the verification with this structure:

```
Claim: <falsifiable statement from Step 1>
Contract: <independent source from Step 2>
Surface: <verification surface from Step 3>
Baseline: <artifact summary and command>
Treatment: <artifact summary and command>
Comparison: <concrete differences and contract match>
Verdict: VERIFIED | NOT VERIFIED | INCONCLUSIVE

Evidence artifacts:
  - <artifact description> [ephemeral | promotion-candidate | canonical]
  - ...

Promotion candidates (if any):
  <description of what the candidate protects, where it should integrate, and what admission criteria it meets>
```
