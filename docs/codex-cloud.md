# Codex Cloud workspace bootstrap

WrightKit keeps shared agent guidance outside individual product repositories. A Codex Cloud environment that checks out only one task repository must reconstruct that shared context before the agent starts work.

The canonical bootstrap is [`scripts/codex-cloud-bootstrap.sh`](../scripts/codex-cloud-bootstrap.sh). It prepares:

- `~/.wrightkit/.github`: workspace `AGENTS.md`, `GOAL.md`, and routed durable policy;
- `~/.wrightkit/.agents`: reusable WrightKit skills;
- `$CODEX_HOME/AGENTS.md` (or `~/.codex/AGENTS.md`): a small cloud entry point that routes Codex to the canonical shared context before repository-local guidance.

The task repository itself is not modified by bootstrap.

## Codex Cloud setup

Use a minimal environment setup command that executes the version-controlled bootstrap:

```sh
curl -fsSL https://raw.githubusercontent.com/wrightkit/.github/main/scripts/codex-cloud-bootstrap.sh | bash
```

Keep durable engineering rules, testing policy, skills, and repository ownership guidance in GitHub. Do not duplicate them in the Codex Cloud environment instructions.

The setup is intentionally idempotent. Re-running it updates the shared context to the current `main` revision and rewrites only the generated Codex routing entry.

## Repository scope

A normal environment should contain only the repository selected for the Codex task plus the shared context prepared above. The bootstrap does not clone unrelated WrightKit product repositories.

When a task genuinely requires another repository, make that dependency explicit in the environment/task setup rather than turning every environment into a full organization checkout. The workspace routing rules still determine semantic ownership even when the current environment cannot modify the owning repository.

## Overrides

The bootstrap accepts these environment variables for controlled testing or alternate layouts:

- `WRIGHTKIT_CONTEXT_ROOT`: shared context root; defaults to `~/.wrightkit`;
- `CODEX_HOME`: Codex home; defaults to `~/.codex`;
- `WRIGHTKIT_GITHUB_REPO`: source URL for the shared `.github` repository;
- `WRIGHTKIT_AGENTS_REPO`: source URL for the shared `.agents` repository.

Required shared guidance is fail-closed: if the workspace router, product goal, routed docs, or shared skills cannot be prepared, setup exits with an error rather than allowing a task to proceed with incomplete WrightKit policy.
