# WrightKit shared GitHub guidance

This repository contains organization-wide engineering guidance and reusable agent skills.

## Agent routing

- [Workspace agent routing](AGENTS.md) — organization-level entry point; routes agents to the right policy, skill, or repository-local guidance.

## Policies and standards

- [Rust CI standard](docs/rust-ci.md)
- [Testing policy](docs/testing-policy.md)
- [Code entropy policy](docs/entropy-policy.md)
- [Release engineering](docs/release-engineering.md)

## Agent skills

- [`wrightkit-reclaim-entropy`](skills/wrightkit-reclaim-entropy/SKILL.md) — evidence-first simplification and entropy reclamation for WrightKit repositories.
- [`wrightkit-verify-change`](skills/wrightkit-verify-change/SKILL.md) — falsifiable claim verification with baseline/treatment comparison and evidence lifecycle classification.
