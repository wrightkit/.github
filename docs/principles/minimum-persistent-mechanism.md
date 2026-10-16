# minimum-persistent-mechanism

**Applies when:** a design adds state, indirection, configuration, a dependency, a schema, a protocol, a fallback, or a new layer.

**Principle:** Start from what existing mechanisms already do, name the exact gap, and add only the smallest thing that closes it. Judge by persistent concepts and maintenance obligations, not by diff size.

**Changes the choice between:** a new mechanism justified by future usefulness, and the direct or existing path that satisfies the current contract.

**Enforced by:** judgment only; PR review checks the ablation pass.

**Why:** a persistent mechanism is paid for by every later reader. Future usefulness and internal coherence are not a present requirement.

**Detail:** [engineering-quality.md](../engineering-quality.md#admit-the-minimum-persistent-mechanism)
