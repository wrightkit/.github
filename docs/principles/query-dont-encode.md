# query-dont-encode

**Applies when:** durable guidance, docs, or tests are about to record counts, versions, issue state, current priorities, or member lists.

**Principle:** Query mutable reality from its source of truth. Write down only facts that are themselves stable contracts.

**Changes the choice between:** hard-coding the current value where it is convenient, and linking to or deriving it from the owning source.

**Enforced by:** partly: generated docs and tests that derive values catch drift. Judgment decides whether a fact is a contract.

**Why:** a recorded snapshot starts drifting at once, and stale guidance misleads more than silence.

**Detail:** [agent-guidance.md](../agent-guidance.md#keep-durable-guidance-stable); [documentation.md](../documentation.md)
