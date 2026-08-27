# WrightKit CI platform

WrightKit uses small, versioned reusable workflows for repeated organization
contracts. Repository workflows remain the owners of triggers, path routing,
matrices, job dependencies, and domain-specific evidence.

## Workflow boundaries

- A **reusable workflow** owns a repeated job graph and its typed organization
  contract. `rust-quality.yml` owns the fundamental Rust quality gate;
  `release-plz-crates.yml` owns release-plz crate publication and release-tag
  creation.
- A **repository workflow** owns the repository's event triggers, native
  `strategy.matrix`, caller-level concurrency and `needs`, and semantic,
  compatibility, corpus, conformance, packaging, or product-release jobs.
- A **composite action** owns a repeated multi-step procedure only after
  repeated evidence justifies extracting that procedure. No composite action
  is required by the v1 contracts.

Callers must reference a stable v1 tag or an explicitly pinned compatible SHA.
They pass only declared inputs and explicitly named secrets; they must not use
arbitrary command hooks or `secrets: inherit` for the crate release workflow.

The shared quality workflow is the prerequisite for repository-owned Rust
validation where the same failure would otherwise be repeated. Repository
specific validation stays in its owner: Workshop catalog/scenario evidence,
OPY and DEL compatibility/corpus evidence, LPP conformance, and Wright
integration/distribution behavior.

Release ownership is similarly split: release-plz maintains Release PRs,
publishes crates, and creates canonical tags; each repository retains its own
tag-triggered binary, checksum, catalog, GitHub Release, and package-manager
workflow. The shared publication job uses one stable group and
`cancel-in-progress: false` with `queue: max`, so publication is never
cancelled while running and pending publication runs are retained in the
platform queue. GitHub permits up to 100 pending runs per concurrency group;
runs beyond that limit are cancelled.

Rust quality cache policy follows `docs/rust-ci.md`: compatible jobs restore one
stable family, only successful `main` quality runs save it, failed jobs do not
save it, and release/tag workflows do not use the quality cache.
