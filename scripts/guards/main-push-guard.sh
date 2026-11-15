#!/bin/sh
# Default-branch gate. Reads git's pre-push lines on stdin and judges every
# update of main or master:
#   - it is not a deletion and not a non-fast-forward update;
#   - the pushed commit is the checked-out HEAD with no tracked changes, so the
#     gate tests exactly what is pushed;
#   - the repository's own gate, .githooks-local/pre-push-main, passes.
# A repository without that gate accepts changes only through a pull request.
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
    fail "the commit pushed to $branch is not the checked-out HEAD, so the gate cannot test it. Check it out, or push a task branch and open a PR."
  git diff --quiet HEAD -- ||
    fail "tracked files differ from HEAD, so the gate would not test the pushed commit. Commit or stash them first."

  gate="$root/.githooks-local/pre-push-main"
  [ -x "$gate" ] ||
    fail "this repository declares no $branch gate (.githooks-local/pre-push-main). Push a task branch and open a PR."
  (cd "$root" && "$gate" </dev/null) ||
    fail "the $branch gate failed. Fix the cause, or push a task branch and open a PR."
done
exit 0
