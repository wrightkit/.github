#!/usr/bin/env python3
"""Report the merge-gate facts of one PR in a single call.

Usage: pr-gate.py OWNER/REPO PR_NUMBER

Prints JSON with the head commit, the required-check summary, whether the
latest LGTM comment or review is newer than the head commit, the changed paths
that CODEOWNERS assigns, and whether the PR is a release PR. It decides
nothing: the orchestrator applies the gate in the orchestrate-issues skill.
"""
import base64
import fnmatch
import json
import subprocess
import sys


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def codeowners(repo, ref):
    for path in (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"):
        out = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}?ref={ref}", "--jq", ".content"],
                             capture_output=True, text=True)
        if out.returncode == 0:
            text = base64.b64decode(out.stdout).decode()
            rules = [line.split() for line in text.splitlines() if line.strip() and not line.startswith("#")]
            return [r for r in rules if len(r) >= 2]
    return []


def owners_of(path, rules):
    """The last matching rule wins, as in GitHub. Glob matching is approximate."""
    hit = []
    for pattern, *who in rules:
        p = pattern.lstrip("/")
        if fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path, p.rstrip("/") + "/*") or path.startswith(p.rstrip("/") + "/"):
            hit = who
    return hit


def main():
    repo, number = sys.argv[1], sys.argv[2]
    pr = json.loads(gh("pr", "view", number, "--repo", repo, "--json",
                       "state,isDraft,mergeable,headRefName,headRefOid,baseRefName,title,files,comments,reviews,commits"))
    head_date = pr["commits"][-1]["committedDate"]
    verdicts = [(c["createdAt"], c["author"]["login"], "comment") for c in pr["comments"] if "LGTM" in c["body"]]
    verdicts += [(r["submittedAt"], r["author"]["login"], r["state"]) for r in pr["reviews"] if "LGTM" in r["body"]]
    latest = max(verdicts, default=None)

    # `gh pr checks` exits 1 for a failed check and 8 for a pending one; the JSON is still valid.
    done = subprocess.run(["gh", "pr", "checks", number, "--repo", repo, "--required", "--json", "name,bucket"],
                          capture_output=True, text=True)
    if done.returncode not in (0, 1, 8):
        sys.exit(f"gh pr checks failed: {done.stderr.strip()}")
    checks = json.loads(done.stdout or "[]")
    buckets = {}
    for c in checks:
        buckets.setdefault(c["bucket"], []).append(c["name"])

    rules = codeowners(repo, pr["baseRefName"])
    owned = {f["path"]: owners_of(f["path"], rules) for f in pr["files"]}
    owned = {path: who for path, who in owned.items() if who}

    print(json.dumps({
        "state": pr["state"], "draft": pr["isDraft"], "mergeable": pr["mergeable"],
        "head": pr["headRefOid"], "head_committed_at": head_date,
        "latest_lgtm": {"at": latest[0], "by": latest[1], "kind": latest[2], "after_head": latest[0] > head_date} if latest else None,
        "required_checks": buckets,
        "codeowner_paths": owned,
        "release_pr": pr["headRefName"].startswith("release-please--") or pr["title"].startswith("chore(main): release"),
    }, indent=2))


if __name__ == "__main__":
    main()
