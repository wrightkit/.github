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
change what executes without a review.

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
