# WrightKit Rust Build Artifact Policy

This document defines organization-wide policy for controlling local Rust build
artifact growth across WrightKit repositories and agent-managed worktrees.

The policy distinguishes long-lived developer checkouts from ephemeral issue and
PR worktrees, because the cost-benefit tradeoff for large incremental caches
differs between them.

## Dev and test profile defaults

Every WrightKit Rust workspace sets the following profile defaults:

```toml
# Reduces dependency artifact volume; WrightKit code retains line-table
# diagnostics for backtraces and panic locations.
[profile.dev]
debug = 1

[profile.dev.package."*"]
debug = false

[profile.test]
debug = 1

[profile.test.package."*"]
debug = false
```

Why `debug = 1` for workspace code: full DWARF (`debug = 2`) is rarely needed
for everyday development; line tables (`debug = 1`) are sufficient for most
backtraces and panic messages. The reduction is significant because most of the
debug artifact volume comes from dependency crates, which carry no useful
user-facing diagnostics.

Setting `debug = false` for `"*"` (third-party dependencies) removes their
debug information entirely. This does not affect correctness or test coverage;
it only removes symbols that are not useful outside of deep upstream debugging
sessions. When investigating a specific upstream dependency, the developer can
temporarily override the profile locally.

These defaults do not affect CI, which is governed by
[`rust-ci.md`](rust-ci.md) and the `rust-quality.yml` reusable workflow.

## Ephemeral worktree policy

Ephemeral worktrees are Git worktrees created by agents or developers to work
on a specific issue or PR branch. They are identified by the naming convention
`<base-repo>-issue-<N>` or `<base-repo>-pr<N>` under the workspace root.

For ephemeral worktrees, incremental compilation provides little durable value:
the worktree is typically retired after the issue closes, and incremental caches
are not reused across sessions or worktrees.

**Build configuration for ephemeral worktrees:**

Disable incremental compilation by setting `CARGO_INCREMENTAL=0` in the shell
session or in a `.cargo/config.toml` local to the worktree:

```toml
# <worktree-root>/.cargo/config.toml
[build]
incremental = false
```

This prevents the `target/debug/incremental/` directory from growing across
sessions. The dev and test profile defaults above still apply and reduce
dependency artifact size.

**Lifecycle and cleanup:**

When retiring an ephemeral worktree, remove its `target/` directory before or
at the same time as the worktree itself:

```sh
# Remove the build artifacts, then remove the worktree
trash <worktree>/target
git -C <base-repo> worktree remove <worktree>
```

Agents that create ephemeral worktrees are responsible for removing the
worktree and its `target/` during retirement. Retired worktrees must not leave
`target/` directories behind as persistent project state.

## Isolation requirement

Concurrent worktrees must remain build-isolated. Do not configure a shared
`CARGO_TARGET_DIR` that points to a single mutable directory shared across
worktrees or repositories. Shared mutable target directories cause build
corruption when worktrees run `cargo` commands concurrently or use different
toolchain versions.

Each worktree or repository retains its own `target/`. The volume reduction
from profile defaults and incremental disabling removes the primary growth
driver without sacrificing isolation.

## Periodic cleanup

For long-lived repositories, the `target/debug/incremental/` directory grows
across sessions and compiler versions. Remove it when a clean rebuild is needed
or when storage pressure accumulates:

```sh
# Safe: removes only incremental state; deps/ and rlibs remain intact
trash <repo>/target/debug/incremental

# Full clean: removes all build artifacts; next build starts from zero
cargo clean --manifest-path <repo>/Cargo.toml
```

There is no mandatory pruning schedule. Remove incremental state when storage
pressure or incremental correctness concerns arise, not on a timer.

## What this policy does not address

- **CI artifact growth** is governed by [`rust-ci.md`](rust-ci.md) and the
  `Swatinem/rust-cache` configuration in `rust-quality.yml`.
- **Shared compiler caches** (`sccache`) were evaluated and deferred. They do
  not substitute for target lifecycle management and add operational complexity.
  Revisit only if build latency across independent worktrees becomes a measured
  bottleneck.
- **Age-based pruning** (`cargo-sweep`) is not required by this policy. The
  lifecycle model—profile defaults plus worktree retirement cleanup—is the
  primary mechanism. Add pruning only if that model proves insufficient.

## Acceptance evidence

Before declaring this policy applied to a repository:

1. The workspace `Cargo.toml` contains the `[profile.dev]` and `[profile.test]`
   blocks specified above.
2. Ephemeral worktrees created after this policy took effect do not retain
   `target/debug/incremental/` after retirement.
3. A representative local build shows reduced artifact size compared to the
   default configuration. Record the before and after `du -sh target/` readings
   and the date in the implementing PR or issue comment.
4. CI results remain green on the same commit; no test or lint regressions.
