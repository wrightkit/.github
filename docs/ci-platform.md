# WrightKit CI platform

WrightKit uses small reusable workflows for repeated organization
contracts. Repository workflows remain the owners of triggers, path routing,
matrices, job dependencies, and domain-specific validation.

## Workflow boundaries

- A **reusable workflow** owns a repeated job graph and its typed organization
  contract. `rust-quality.yml` owns the fundamental Rust quality gate;
  `release-plz-crates.yml` owns release-plz crate publication and release-tag
  creation.
- A **repository workflow** owns the repository's event triggers, native
  `strategy.matrix`, caller-level concurrency and `needs`, and semantic,
  compatibility, corpus, conformance, packaging, or product-release jobs.
- A **composite action** owns a repeated multi-step procedure only after the
  same stable procedure is used across repositories and extracting it removes
  duplicated workflow steps. `.github/actions/setup-rust` owns installing a
  toolchain and restoring the bounded Cargo cache, which every Rust repository
  repeats before running its own commands.

Callers of WrightKit's own reusable workflows may track `@main`, so a contract
change reaches every repository without a pin bump; the workflow's inputs and
outputs are the compatibility surface, and a breaking change updates its callers
in the same rollout. Every third-party action is pinned to a full commit SHA,
because it runs with the caller's credentials and a moved tag or branch would
change what executes without a review. GitHub-owned `actions/*` actions count
as third-party for this mandate: their tags move the same way.

Callers pass only declared inputs and explicitly named secrets; they must not use
arbitrary command hooks or `secrets: inherit` for the crate release workflow.

The shared quality workflow is the prerequisite for repository-owned Rust
validation where the same failure would otherwise be repeated. Repository
specific validation stays in its owner: Workshop catalog/scenario checks,
OPY and DEL compatibility/corpus checks, LPP conformance, and Wright
integration/distribution behavior.

Release ownership is similarly split: release-plz maintains Release PRs,
publishes crates, and creates canonical tags; each repository retains its own
tag-triggered binary, checksum, catalog, GitHub Release, and package-manager
workflow. Before the publication job starts, the reusable workflow runs
`cargo publish --workspace --locked --dry-run` so every publishable package is
packaged and verified from its artifact while grouped workspace versions are
checked together. The shared publication job uses one stable group and
`cancel-in-progress: false` with `queue: max`, so publication is never
cancelled while running and pending publication runs are retained in the
platform queue. GitHub permits up to 100 pending runs per concurrency group;
runs beyond that limit are cancelled.

The `release-plz-crates.yml` workflow exposes `releases_created` and `releases`
from its `release` job to callers. `releases_created` is the string `true` or
`false`; `releases` is the JSON release metadata emitted by release-plz. A
caller can gate a repository-owned follow-up job with
`needs.<release-job>.outputs.releases_created == 'true'` and pass the matching
`needs.<release-job>.outputs.releases` value without rediscovering the tag or
release.

Rust quality cache policy follows `docs/rust-ci.md`: compatible jobs restore one
stable family, only successful `main` quality runs save it, failed jobs do not
save it, and release/tag workflows do not use the quality cache.

## Run speed

These rules keep a CI run short without removing a check.

- **Cancel superseded pull request runs only.** Give the CI workflow
  `concurrency.group: ci-${{ github.event.pull_request.number || github.sha }}`
  and `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`. A push
  to `main` gets a unique group, so every `main` commit keeps a complete run;
  the release gate depends on that. A workflow that also reacts to title or
  label events adds a separate group suffix for them, so they cannot cancel a
  running suite.
- **Filter documentation-only changes inside the workflow, not with `on.paths`.**
  A workflow skipped by `paths` or `paths-ignore` never reports its checks, and
  a required check that never reports blocks the merge. A `changes` job built on
  `dorny/paths-filter` with `predicate-quantifier: every` computes `code`;
  callers pass `skip: ${{ needs.changes.outputs.code != 'true' }}` to
  `rust-quality.yml` or put `if: needs.changes.outputs.code == 'true'` on their
  own jobs. A skipped job reports its check name as skipped, which counts as
  passing for a required check. The release gate accepts only `success`, so it
  must never depend on a check that a release commit can skip: a release commit
  changes `Cargo.toml`, which is code. A repository with no required check may
  filter with `paths-ignore` instead.
- **Do not chain jobs that exchange no data.** Drop a `needs` that only orders
  jobs. Keep `needs` for artifacts and outputs, and for the aggregate job.
- **Count jobs.** A free organization runs 20 jobs at once, and 5 of them on
  macOS. A run that starts more jobs than that queues the rest, so merge many
  small jobs into one job with a loop, or into a few shards.
- **Put checks that do not depend on the operating system on Ubuntu.** Use macOS
  and Windows only for installers, packaging, and platform runtime behavior.
- **Prefer prebuilt tools.** Download a checksum-pinned release binary, or use an
  install action that downloads one. Do not run `cargo install` or `go install`
  in a job. `actionlint.yml` installs the release binary and verifies its
  SHA-256.
- **Keep `cargo test`.** `cargo nextest` was measured on the hosted runners and
  was slower for opy-rs (52 s to 149 s) and athena (40 s to 65 s), because it
  starts one process per test.
- **Optimize a dependency that dominates a debug test.** A
  `[profile.dev.package.<crate>]` `opt-level` entry costs one cached compile and
  can remove minutes of test time; Wright sets one for `workshop-rs`.
