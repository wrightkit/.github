# independent-authority

**Applies when:** deciding that a material change is correct, or choosing what evidence to cite.

**Principle:** Verify against an authority the implementation did not produce: an accepted contract, a pinned upstream oracle, or a real project. Tests written with the change confirm intent, not correctness.

**Changes the choice between:** reporting green self-written tests as verification, and naming the independent reference used and what it could not confirm.

**Enforced by:** CI gates cover what they encode. Judgment picks the reference and states what is unconfirmed.

**Why:** the implementation and its tests can share one wrong expectation. An outside authority is what exposes it.

**Detail:** [verification-and-acceptance.md](../verification-and-acceptance.md); [AGENTS.md](../../AGENTS.md#tests-and-verification-artifacts)
