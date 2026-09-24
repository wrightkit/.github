# One-pass PR review and review-fix handoff

This policy defines WrightKit PR verification, finding quality, review-fix
thread handling, and follow-up review handoff.

## PR review is verification, not design

A reviewer verifies whether the PR correctly and completely implements its approved issue, current architecture, and contracts. Review is not an opportunity to redesign the system, revisit accepted architecture preferences, or expand the issue into cleanup and future work.

Why: architecture and product decisions have their own owners and decision process. Reopening them during PR review creates scope drift and repeated implementation cycles without new information.

The reviewer should inspect the full applicable PR scope in the initial pass. Finding one blocker does not end the review; continue through the remaining changed behavior and report all currently discoverable actionable findings together.

Review, as applicable:

- the linked issue scope, non-goals, and acceptance criteria;
- correctness, regressions, failure and unsupported paths;
- compliance with the current approved architecture, ownership, dependency, compatibility, API/protocol, and security contracts;
- contract continuity when replacing, hiding, or retiring a public or canonical boundary: confirm that surviving accepted capabilities are verified through the replacement boundary itself, that removals/changes have explicit contract approval, that ownership transfers explicitly declare the new authoritative owner and handoff boundary, and that tests exercising only retired or compatibility paths are not treated as proving replacement completeness;
- test coverage when it is materially relevant to a current failure mode or contract;
- newly added or materially affected explanatory comments and file/module headers, including whether the prose is functioning as a README for code whose responsibility, ownership, pipeline, or internal relationships are otherwise not self-explanatory;
- changes outside the approved scope that affect correctness or maintenance obligations.

Architecture is a compliance boundary during review. Do not propose an alternative architecture when the PR follows the current approved one. If the Issue, documented contract, and current implementation disagree materially, identify the decision mismatch and route it to the appropriate owner rather than asking the Engineer to redesign it inside the PR.

A comment is not independently authoritative proof that a placement or behavior is intentional. Do not treat an accurate explanatory header as sufficient proof of readability. If removing the prose makes a changed feature/module/file materially difficult to understand, require the smallest code-level correction needed to make the responsibility and behavior discoverable. Require comment removal when the prose merely restates implementation; retain only information that cannot reasonably be expressed by code structure and belongs with the source.

## Findings and output

Report only actionable defects that should be corrected in the current PR.

A useful finding identifies:

- the concrete location or behavior;
- what is wrong;
- why it affects the current issue, contract, correctness, or regression risk;
- the required correction, at the smallest useful level.

Keep the explanation only as long as needed to establish the defect. Do not add review summaries, praise, architecture essays, speculative concerns, nits, future improvements, or optional suggestions by default.

If there are no actionable findings, reply `LGTM` and approve the PR. Do not add a checklist or summary of categories inspected.

## Addressing review findings and handoff

When an Engineer agent addresses PR review findings, the work is governed by the same scope discipline and contract boundaries as the original implementation. Pushing code is necessary but not sufficient: review-fix work is complete only when verified corrections are pushed, affected review threads are handled, and the PR is explicitly handed back to follow-up review.

Repository guidance should specialize this shared policy only when local repository ownership or tooling requires it (such as a repository-specific re-review trigger); repositories must not duplicate or contradict this workflow.

### Scope discipline during review fixes

Addressing review findings is strictly verification and fix work. It addresses actionable defects reported in the review without expanding the PR:

- Correct only the actionable defects identified in the review and verify that no regressions were introduced.
- Do not add unrelated cleanup, renaming, broad refactoring, formatting churn, or speculative extensibility while fixing review findings.
- Do not redesign the feature, revisit settled architecture preferences, or expand the issue's scope.
- If a review finding suggests an architectural change, redesign, or scope expansion that contradicts the approved issue or current architecture, stop as Engineer and report the decision mismatch rather than self-authorizing an out-of-scope redesign.

### Review threads: reply and resolution

When review findings are reported as review threads on GitHub and client/API operations are available:

- **Reply to confirm fixes**: Once the correction is verified and pushed, reply to the thread concisely confirming the resolution, citing the fixing commit or explaining the change if non-obvious rationale was required.
- **Resolve addressed threads**: Mark threads as resolved only when the underlying finding has genuinely been corrected and verified in the pushed branch.
- **Never hide unresolved findings**: Do not resolve or clear threads for findings that are contested, deferred, unaddressed, or only partially addressed. If a finding cannot be resolved within the PR's scope or requires maintainer/Architect clarification, reply with the status, leave the thread open/unresolved, and surface the item in the handoff report.

### Handing back to follow-up review

A review-fix task is not complete solely because fixes were verified, committed, and pushed. The agent must hand the updated PR back to the review lifecycle:

- **Directly re-requestable reviewers**: When GitHub supports re-requesting the reviewer identity (e.g., human reviewers or GitHub users/teams where `gh pr review --re-request` or the review-request API succeeds), re-request review from the applicable reviewer who reported the findings.
- **Indirect / bot / external reviewers**: When the reviewer cannot be re-requested directly via GitHub's native review-request mechanism (such as certain bot accounts, GitHub Apps, external review tools, or missing API permissions):
  1. Check repository guidance for a documented re-review trigger (such as a bot mention or slash command) and invoke it if supported.
  2. If no documented trigger exists or automated re-request fails, post an explicit review-ready comment on the PR summarizing the addressed findings, pushed commits, and readiness for follow-up review.
  3. Report any remaining orchestration limitation (e.g., that follow-up review requires manual triggering or reviewer notification) in the final handoff.

### Review-fix completion criteria

A review-fix task is complete only when all of the following are satisfied:

1. **Corrections verified and pushed**: Fixes are verified at the narrowest decisive surface (including regression checks against previous findings and proportionate repository gates), committed on the PR branch, and pushed to the remote PR.
2. **Review threads handled**: Addressed review threads are replied to and/or resolved without concealing unresolved findings.
3. **Follow-up review signaled**: Follow-up review is explicitly triggered or re-requested via GitHub or the repository's documented mechanism, or an explicit review-ready handoff comment is left if direct re-request is unsupported.
4. **Handoff reported**: The final report identifies the PR URL, pushed commits, thread resolution status, and the review handoff state (reviewer re-requested or handoff signal used).

Why: committing and pushing code updates the branch, but without thread handling and an explicit handoff back to review, the reviewer is not informed that corrections are ready for verification, leaving PRs stalled in an ambiguous state.

## Follow-up review

After the Engineer addresses findings and hands the PR back, review only:

1. the previously reported findings;
2. regressions introduced by those fixes;
3. materially new code or behavior added since the previous review.

Do not reopen previously reviewed areas or add preference-based concerns without new information. If the prior findings are fixed and no new defect was introduced, reply `LGTM` and approve.

Why: follow-up review verifies the correction. Re-running a fresh architectural audit after every fix creates avoidable review loops and makes the effective PR scope unstable.

## Specialist routing

Specialist policy and skills are demand-driven, not mandatory review stages:

- Route material test-quality or agent-generated-test questions to `.agents/skills/wrightkit-test-design-review/SKILL.md` and the canonical testing policy.
- Route material Rust ownership, API, error, async/concurrency, abstraction, semantic-placement, responsibility-growth, feature-locality, or metadata-driven behavior risk to `.agents/skills/wrightkit-rust-engineering-review/SKILL.md`.
- Route substantial simplification, deletion, duplication, or post-migration entropy work to [`docs/entropy-policy.md`](entropy-policy.md) and `.agents/skills/wrightkit-reclaim-entropy/SKILL.md` when that work is inside the approved scope.
- Route material changes requiring independent falsification or public boundary contract continuity verification to `.agents/skills/wrightkit-verify-change/SKILL.md` and the canonical testing policy.

Do not load every specialist route because a PR contains Rust, tests, or abstractions. The linked issue and the actual risk surface determine what is applicable.
