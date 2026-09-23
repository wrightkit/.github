# WrightKit shared GitHub guidance

This repository contains organization-wide product intent, engineering policy, CI/release standards, and workspace agent routing.

Reusable WrightKit agent skills are owned by the sibling [`wrightkit/.agents`](https://github.com/wrightkit/.agents) repository and are expected at `.agents/skills` in the WrightKit workspace.

## Organization guidance

- [WrightKit goal](docs/goal.md): durable product intent, priorities, success outcomes, and deliberate non-goals. Read this first when a product or implementation tradeoff is unclear.
- [Workspace agent routing](AGENTS.md): organization-level routing entry point; routes agents to the right policy, skill, or repository-local guidance.

## Documentation

- [Documentation index](docs/README.md)
- [Documentation management](docs/documentation.md)

## Policies and standards

- [Engineering quality policy](docs/engineering-quality.md)
- [Issue readiness and PR audit](docs/issue-readiness-and-pr-audit.md)
- [Rust CI standard](docs/rust-ci.md)
- [Testing policy](docs/testing-policy.md)
- [Code entropy policy](docs/entropy-policy.md)
- [Release engineering](docs/release-engineering.md)
