# Codex Cloud workspace bootstrap

WrightKit keeps shared agent guidance outside individual product repositories. A Codex Cloud environment that checks out only one task repository must reconstruct that shared context before the agent starts work.

The canonical bootstrap is [`scripts/codex-cloud-bootstrap.sh`](../scripts/codex-cloud-bootstrap.sh). It prepares:

- `~/.wrightkit/.github`: workspace `AGENTS.md`, `GOAL.md`, and routed durable policy;
- `~/.wrightkit/.agents`: reusable WrightKit skills;
- `$CODEX_HOME/AGENTS.md` (or `~/.codex/AGENTS.md`): a small cloud entry point that routes Codex to the canonical shared context before repository-local guidance.

The task repository itself is not modified by bootstrap.

## Codex Cloud setup

Use this version-controlled bootstrap as the environment setup command:

```sh
printf 'wrightkit bootstrap: downloading setup\n'
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 30 \
  https://raw.githubusercontent.com/wrightkit/.github/main/scripts/codex-cloud-bootstrap.sh \
  | bash
```

Keep durable engineering rules, testing policy, skills, and repository ownership guidance in GitHub. Do not duplicate them in the Codex Cloud environment instructions.

### Private shared context

`wrightkit/.agents` is private. Configure `WRIGHTKIT_GITHUB_TOKEN` as a Codex Cloud environment secret with read-only access to that repository before using the bootstrap.

Prefer a fine-grained GitHub token scoped to the `wrightkit` organization, the `.agents` repository, and read-only repository contents. The bootstrap uses the token only while Git performs the private clone/fetch. Interactive Git prompting is disabled, the token is not placed in a clone URL or Git remote/config, and the generated Codex routing file does not contain it.

If the required token is missing, bootstrap exits immediately with an actionable error rather than waiting for Git authentication.

The setup is intentionally idempotent: re-running it updates the shared context to the current `main` revision and rewrites only the generated Codex routing entry. Cached environments may retain shared context for the cache lifetime; no separate policy copy should be maintained in the environment configuration.

## Repository scope

A normal environment should contain only the repository selected for the Codex task plus the shared context prepared above. The bootstrap does not clone unrelated WrightKit product repositories.

When a task genuinely requires another repository, make that dependency explicit in the environment/task setup rather than turning every environment into a full organization checkout. The workspace routing rules still determine semantic ownership even when the current environment cannot modify the owning repository.

## Overrides

The bootstrap accepts these environment variables for controlled testing or alternate layouts:

- `WRIGHTKIT_CONTEXT_ROOT`: shared context root; defaults to `~/.wrightkit`;
- `CODEX_HOME`: Codex home; defaults to `~/.codex`;
- `WRIGHTKIT_GITHUB_REPO`: source URL for the shared `.github` repository;
- `WRIGHTKIT_AGENTS_REPO`: source URL for the shared `.agents` repository;
- `WRIGHTKIT_GITHUB_TOKEN`: setup-only GitHub credential used for the default private `.agents` repository.

When `WRIGHTKIT_AGENTS_REPO` is overridden, the bootstrap treats the alternate source as independently accessible and does not require `WRIGHTKIT_GITHUB_TOKEN`. This keeps local fixture/testing workflows independent from Cloud credentials.

Required shared guidance is fail-closed: if the workspace router, product goal, routed docs, or shared skills cannot be prepared, setup exits with an error rather than allowing a task to proceed with incomplete WrightKit policy.
