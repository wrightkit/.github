#!/bin/sh
# Merged-branch guard. Refuse to push a branch whose pull request is already
# merged: such commits reach neither the PR nor the default branch.
# A branch with an open pull request passes. Fails open when `gh` is missing
# or cannot reach GitHub, so offline work is not blocked.
#
# Usage: merged-branch-guard.sh [BRANCH]   (default: the current branch)
set -u

branch="${1:-$(git branch --show-current 2>/dev/null)}"
case "$branch" in '' | main | master) exit 0 ;; esac
command -v gh >/dev/null 2>&1 || exit 0

open="$(gh pr list --head "$branch" --state open --json number --jq length 2>/dev/null)" || exit 0
[ "${open:-0}" = 0 ] || exit 0
merged="$(gh pr list --head "$branch" --state merged --json number --jq '.[0].number // empty' 2>/dev/null)" || exit 0
[ -n "$merged" ] || exit 0

printf 'merged-branch-guard: PR #%s for branch %s is already merged.\n' "$merged" "$branch" >&2
printf 'Create a new branch from origin/main, cherry-pick the new commits, and push that branch.\n' >&2
exit 1
