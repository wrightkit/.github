# demonstrated-abstraction

**Applies when:** repeated code, or a possible second consumer, suggests a helper, trait, adapter, or extension point.

**Principle:** Keep behavior local until real cases reveal a stable common contract. Small duplication is cheaper than the wrong abstraction.

**Changes the choice between:** extracting now for tidiness or hypothetical reuse, and leaving the cases separate until a current owner, real consumer, and observable benefit exist.

**Enforced by:** judgment only. The number of repetitions is a heuristic, not an eligibility test.

**Why:** an abstraction couples cases before their shared shape is understood, and undoing it costs more than the duplication did.

**Detail:** [engineering-quality.md](../engineering-quality.md#prefer-demonstrated-abstractions)
