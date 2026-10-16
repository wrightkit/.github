# upstream-is-the-spec

**Applies when:** an OPY or DEL/OSTW construct could be made cheaper, cleaner, or more permissive than the upstream compiler produces or accepts.

**Principle:** For a language with an established upstream compiler, its output and its accepted input are the specification. Convergence is structural, measured on canonical Workshop programs, never on text.

**Changes the choice between:** an apparent improvement or bug fix in our output, and the upstream shape plus a recorded, approved exception.

**Enforced by:** differential and corpus comparison under the compatibility tests. Judgment decides whether a difference is a deviation or an unsupported construct.

**Why:** users adopt WrightKit because it behaves like the compiler they already trust. A silent rewrite breaks that, even when it is behaviorally equivalent.

**Detail:** [goal.md](../goal.md) principle 7; [compatibility-testing.md](../compatibility-testing.md)
