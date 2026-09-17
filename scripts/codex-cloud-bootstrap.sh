#!/usr/bin/env bash
set -euo pipefail

context_root="${WRIGHTKIT_CONTEXT_ROOT:-$HOME/.wrightkit}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
github_repo="${WRIGHTKIT_GITHUB_REPO:-https://github.com/wrightkit/.github.git}"
agents_repo="${WRIGHTKIT_AGENTS_REPO:-https://github.com/wrightkit/.agents.git}"

log() {
  printf 'wrightkit bootstrap: %s\n' "$*" >&2
}

fail() {
  log "$*"
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required"

export GIT_TERMINAL_PROMPT=0

run_git() {
  git \
    -c credential.helper= \
    -c http.lowSpeedLimit=1 \
    -c http.lowSpeedTime=30 \
    "$@"
}

sync_repo() {
  local url="$1"
  local dest="$2"
  local label="$3"

  log "syncing $label"

  if [[ -d "$dest/.git" ]]; then
    run_git -C "$dest" fetch origin main
    run_git -C "$dest" merge --ff-only origin/main
  else
    [[ ! -e "$dest" ]] || fail "refusing to replace existing $dest"
    run_git clone --depth 1 --branch main --single-branch "$url" "$dest"
  fi
}

mkdir -p "$context_root" "$codex_home"

sync_repo "$github_repo" "$context_root/.github" "shared policy (.github)"
sync_repo "$agents_repo" "$context_root/.agents" "shared skills (.agents)"

workspace_agents="$context_root/.github/AGENTS.md"
workspace_goal="$context_root/.github/GOAL.md"

log "validating shared context"

[[ -f "$workspace_agents" ]] || fail "missing $workspace_agents"
[[ -f "$workspace_goal" ]] || fail "missing $workspace_goal"
[[ -d "$context_root/.github/docs" ]] || fail "missing shared docs"
[[ -d "$context_root/.agents/skills" ]] || fail "missing shared skills"

log "installing Codex workspace routing"

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

log "agent context ready at $context_root"
