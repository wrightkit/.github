# Lessons

Short review queue of reusable failure classes from merged .github work. Each entry names a prevention action and the evidence behind it. Promote an entry into a regression test, an owner contract, or an existing engineering standard, then remove it here. The procedure is the `merged-pr-retro` skill in `wrightkit/.agents`.

### A guard must parse the invocation it judges, not pattern-match raw text
- **Rule:** A hook or guard that inspects a command line must parse its arguments and accept every allowed form while rejecting only the target case; matching the raw string misfires on legitimate invocations.
- **Why:** The agent tool-call hook regex-matched the whole command, rejected every force-push including feature branches where it is normal workflow, and flagged `git push -n` and `-n` inside a commit message as hook bypasses.
- **Prevention home:** argument parsing plus the allow/reject unit tests landed in #113.
- **Incidents:** [#111](https://github.com/wrightkit/.github/pull/111) defect fixed by [#113](https://github.com/wrightkit/.github/pull/113) — observed 2026-10-20

### A job that provisions a toolchain asserts the toolchain that actually runs
- **Rule:** A CI job named for a toolchain or environment must assert that version is what executes; a committed `rust-toolchain.toml` can silently outrank the installed default.
- **Why:** The shared `Rust (1.85.0)` job ran stable for repositories carrying a pinned `rust-toolchain.toml`, so the declared-MSRV gate never exercised the minimum it was named for.
- **Prevention home:** the toolchain assertion landed in #109; the per-repo pins were then unified (`workshop-rs#529`, `opy-rs#625`, `wright#849`).
- **Incidents:** [#109](https://github.com/wrightkit/.github/pull/109) (fixes [#108](https://github.com/wrightkit/.github/issues/108)) — observed 2026-10-20
