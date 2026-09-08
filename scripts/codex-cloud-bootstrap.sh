#!/usr/bin/env bash
set -euo pipefail

context_root="${WRIGHTKIT_CONTEXT_ROOT:-$HOME/.wrightkit}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
github_repo="${WRIGHTKIT_GITHUB_REPO:-https://github.com/wrightkit/.github.git}"
agents_repo="${WRIGHTKIT_AGENTS_REPO:-https://github.com/wrightkit/.agents.git}"

sync_repo() {
  local url="$1"
  local dest="$2"

  if [[ -d "$dest/.git" ]]; then
    git -C "$dest" fetch origin main
    git -C "$dest" merge --ff-only origin/main
  else
    [[ ! -e "$dest" ]] || {
      echo "wrightkit bootstrap: refusing to replace existing $dest" >&2
      exit 1
    }
    git clone "$url" "$dest"
  fi
}

mkdir -p "$context_root" "$codex_home"

sync_repo "$github_repo" "$context_root/.github"
sync_repo "$agents_repo" "$context_root/.agents"

workspace_agents="$context_root/.github/AGENTS.md"
workspace_goal="$context_root/.github/GOAL.md"

[[ -f "$workspace_agents" ]] || {
  echo "wrightkit bootstrap: missing $workspace_agents" >&2
  exit 1
}

[[ -f "$workspace_goal" ]] || {
  echo "wrightkit bootstrap: missing $workspace_goal" >&2
  exit 1
}

[[ -d "$context_root/.github/docs" ]] || {
  echo "wrightkit bootstrap: missing shared docs" >&2
  exit 1
}

[[ -d "$context_root/.agents/skills" ]] || {
  echo "wrightkit bootstrap: missing shared skills" >&2
  exit 1
}

cat >"$codex_home/AGENTS.md" <<EOF
# WrightKit Cloud Workspace Routing

This Codex environment is executing one repository from the WrightKit multi-repository workspace.

Before applying repository-local guidance, read and apply the canonical shared workspace context from:

- $workspace_goal
- $workspace_agents

Shared routed policy lives under:

- $context_root/.github/docs/

Reusable WrightKit skills live under:

- $context_root/.agents/skills/

The checked-out repository's nearest AGENTS.md then specializes these shared rules. Do not treat repository-local guidance as a standalone replacement for the WrightKit workspace contract.

If any required shared context above is unavailable, stop rather than silently continuing with incomplete WrightKit policy.
EOF

printf 'WrightKit agent context ready at %s\n' "$context_root"
