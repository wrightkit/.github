#!/usr/bin/env bash
set -euo pipefail

context_root="${WRIGHTKIT_CONTEXT_ROOT:-$HOME/.wrightkit}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
github_repo="${WRIGHTKIT_GITHUB_REPO:-https://github.com/wrightkit/.github.git}"
agents_repo="${WRIGHTKIT_AGENTS_REPO:-https://github.com/wrightkit/.agents.git}"
github_token="${WRIGHTKIT_GITHUB_TOKEN:-}"

log() {
  printf 'wrightkit bootstrap: %s\n' "$*" >&2
}

fail() {
  log "$*"
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required"

export GIT_TERMINAL_PROMPT=0

askpass=""
cleanup() {
  if [[ -n "$askpass" ]]; then
    rm -f "$askpass"
  fi
}
trap cleanup EXIT

prepare_private_git_auth() {
  [[ -n "$github_token" ]] || fail "WRIGHTKIT_GITHUB_TOKEN is required to read private wrightkit/.agents context"

  askpass="$(mktemp)"
  chmod 700 "$askpass"
  cat >"$askpass" <<'EOF'
#!/bin/sh
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *Password*) printf '%s\n' "$WRIGHTKIT_GITHUB_TOKEN" ;;
  *) exit 1 ;;
esac
EOF
}

run_public_git() {
  git -c credential.helper= "$@"
}

run_private_git() {
  GIT_ASKPASS="$askpass" git -c credential.helper= "$@"
}

sync_repo() {
  local url="$1"
  local dest="$2"
  local label="$3"
  local auth="$4"

  log "syncing $label"

  if [[ -d "$dest/.git" ]]; then
    if [[ "$auth" == "private" ]]; then
      run_private_git -C "$dest" fetch origin main
      run_private_git -C "$dest" merge --ff-only origin/main
    else
      run_public_git -C "$dest" fetch origin main
      run_public_git -C "$dest" merge --ff-only origin/main
    fi
  else
    [[ ! -e "$dest" ]] || fail "refusing to replace existing $dest"

    if [[ "$auth" == "private" ]]; then
      run_private_git clone "$url" "$dest"
    else
      run_public_git clone "$url" "$dest"
    fi
  fi
}

mkdir -p "$context_root" "$codex_home"

agents_auth="public"
if [[ "$agents_repo" == "https://github.com/wrightkit/.agents.git" ]]; then
  agents_auth="private"
  prepare_private_git_auth
fi

sync_repo "$github_repo" "$context_root/.github" "shared policy (.github)" "public"
sync_repo "$agents_repo" "$context_root/.agents" "shared skills (.agents)" "$agents_auth"

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
