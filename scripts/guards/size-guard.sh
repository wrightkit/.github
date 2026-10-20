#!/bin/sh
# Context-size guard. A file may not exceed its line or token limit
# (tokens ~ bytes / 4). A file already over a limit may shrink but not grow
# compared with HEAD, so legacy files do not block unrelated work.
#
# Usage: size-guard.sh --index              check files staged for commit
#        size-guard.sh --worktree PATH...   check working-tree files
set -eu

SRC_LINES=800
SRC_TOKENS=10000
GUIDE_LINES=200
GUIDE_TOKENS=4000

mode="${1:-}"
[ -n "$mode" ] && shift

is_checked() {
  case "$1" in
    *.rs|*.py|*.ts|*.tsx|*.js|*.jsx|*.mjs|*.vue|*.sh|*.md) ;;
    *) return 1 ;;
  esac
  case "$1" in
    CHANGELOG.md|*/CHANGELOG.md|*.snap) return 1 ;;
    target/*|*/target/*|node_modules/*|*/node_modules/*) return 1 ;;
    .cache/*|*/.cache/*|fixtures/*|*/fixtures/*|snapshots/*|*/snapshots/*) return 1 ;;
    vendor/*|*/vendor/*|dist/*|*/dist/*|generated/*|*/generated/*) return 1 ;;
  esac
}

# Prints "lines tokens" for the content on stdin.
measure() {
  wc -lc | awk '{ printf "%d %d\n", $1, int($2 / 4) }'
}

failures=0

check() { # new_path old_path
  new="$1"; old="$2"
  is_checked "$new" || return 0

  case "$mode" in
    --index) content_cmd="git show :$new" ;;
    *) content_cmd="cat $new" ;;
  esac
  set -- $($content_cmd | measure)
  lines="$1"; tokens="$2"

  case "${new##*/}" in
    AGENTS.md|CLAUDE.md|LESSONS.md) max_l=$GUIDE_LINES; max_t=$GUIDE_TOKENS ;;
    *) max_l=$SRC_LINES; max_t=$SRC_TOKENS ;;
  esac

  [ "$lines" -le "$max_l" ] && [ "$tokens" -le "$max_t" ] && return 0

  if git cat-file -e "HEAD:$old" 2>/dev/null; then
    set -- $(git show "HEAD:$old" | measure)
    old_l="$1"; old_t="$2"
    # Over a limit is allowed only while not larger than HEAD.
    if { [ "$lines" -le "$max_l" ] || [ "$lines" -le "$old_l" ]; } &&
       { [ "$tokens" -le "$max_t" ] || [ "$tokens" -le "$old_t" ]; }; then
      return 0
    fi
    printf 'size-guard: %s grew while over limit (%s lines, ~%s tokens; HEAD %s lines, ~%s tokens; limit %s lines / %s tokens).\n' \
      "$new" "$lines" "$tokens" "$old_l" "$old_t" "$max_l" "$max_t" >&2
  else
    printf 'size-guard: new file %s is over limit (%s lines, ~%s tokens; limit %s lines / %s tokens).\n' \
      "$new" "$lines" "$tokens" "$max_l" "$max_t" >&2
  fi
  printf '  Split it by responsibility so each part is under the limit.\n' >&2
  failures=$((failures + 1))
}

case "$mode" in
  --index)
    tab="$(printf '\t')"
    pairs="$(git diff --cached --name-status -M --diff-filter=AMR |
      awk -F '\t' '{ print ($1 ~ /^R/) ? $3 "\t" $2 : $2 "\t" $2 }')"
    while IFS="$tab" read -r new old; do
      [ -n "$new" ] && check "$new" "$old"
    done <<PAIRS
$pairs
PAIRS
    ;;
  --worktree)
    for p in "$@"; do
      [ -f "$p" ] && check "$p" "$p"
    done
    ;;
  *)
    echo 'usage: size-guard.sh --index | --worktree PATH...' >&2
    exit 2
    ;;
esac

[ "$failures" -eq 0 ]
