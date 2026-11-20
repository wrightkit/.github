#!/bin/sh
# Default-branch gate. Reads git's pre-push lines on stdin and judges every
# update of main or master. The rules are the same in every repository:
#   - it is not a deletion and not a non-fast-forward update;
#   - the pushed commit is the checked-out HEAD with no tracked changes, so the
#     pushed commit is the state that was verified;
#   - the new commits hold no fixup!, squash!, amend!, or WIP commit;
#   - the repository's own gate, .githooks-local/pre-push-main, passes when the
#     repository declares one.
set -u

fail() {
  printf 'main-push-guard: %s\n' "$1" >&2
  exit 1
}

while read -r _ local_sha remote_ref remote_sha; do
  case "$remote_ref" in refs/heads/main | refs/heads/master) ;; *) continue ;; esac
  branch="${remote_ref#refs/heads/}"

  case "$local_sha" in *[!0]*) ;; *) fail "refusing to delete $branch." ;; esac
  case "$remote_sha" in
    *[!0]*)
      git merge-base --is-ancestor "$remote_sha" "$local_sha" 2>/dev/null ||
        fail "the push to $branch is not a fast-forward. Fetch, rebase onto origin/$branch, and push again. Do not force-push."
      ;;
  esac

  root="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "no working tree; the $branch gate cannot run."
  [ "$(git rev-parse HEAD)" = "$local_sha" ] ||
    fail "the commit pushed to $branch is not the checked-out HEAD, so it is not the state you verified. Check it out, or push a task branch and open a PR."
  git diff --quiet HEAD -- ||
    fail "tracked files differ from HEAD, so the pushed commit is not the state you verified. Commit or stash them first."

  case "$remote_sha" in
    *[!0]*)
      range="$remote_sha..$local_sha"
      unfinished="$(git log --format=%s "$range" | grep -iE '^(fixup!|squash!|amend!|wip([^[:alnum:]]|$))' | head -n 1)"
      [ -z "$unfinished" ] ||
        fail "the push to $branch holds an unfinished commit: \"$unfinished\". Squash or reword it first."
      ;;
  esac

  gate="$root/.githooks-local/pre-push-main"
  if [ -e "$gate" ]; then
    [ -x "$gate" ] || fail "$gate is not executable."
    (cd "$root" && "$gate" </dev/null) ||
      fail "the $branch gate failed. Fix the cause, or push a task branch and open a PR."
  fi
done
exit 0
