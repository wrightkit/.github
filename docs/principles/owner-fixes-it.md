# owner-fixes-it

**Applies when:** a consumer is missing semantics, data, or a contract that another repository owns.

**Principle:** Change the authoritative contract in the repository that owns it, then integrate consumers separately. Do not paper over a gap inside the consumer for convenience.

**Changes the choice between:** a local workaround in `wright` or a language crate, and a fix in the owning repository followed by a consumer update.

**Enforced by:** repository ownership map in [AGENTS.md](../../AGENTS.md#repository-routing); cross-repository CI where present. Judgment decides what a gap is.

**Why:** a workaround forks the truth. The next consumer meets the same gap and the owner never learns it exists.

**Detail:** [goal.md](../goal.md) principles 1 and 6
