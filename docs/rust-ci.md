# WrightKit Rust CI standard

This document defines the preferred Rust CI composition for WrightKit repositories. It keeps toolchain provisioning and Cargo cache ownership as separate, visible workflow responsibilities.

Repository-local workflows own their commands, evidence, and release behavior. This document is a pattern, not a shared workflow or a requirement to migrate every repository immediately.

## Responsibilities

Each Rust job should make these decisions explicit:

1. Select the exact Rust toolchain and install only the required components and targets.
2. Use the committed `Cargo.lock` for dependency-resolving commands with `--locked`.
3. Let `Swatinem/rust-cache` own the Cargo registry, Git dependency, and, where justified, target cache.
4. Allow only a successful `main` job to save a persistent cache. Pull requests and secondary jobs restore only.
5. Disable Rust caching for release and tag jobs unless a measured release benefit justifies a separate cache family.

The toolchain action must not also be the cache owner. Keeping the two steps adjacent makes the cache policy visible in the workflow and independently reviewable.

## Preferred CI composition

Use a dedicated toolchain step followed by one explicit cache step:

```yaml
- name: Install Rust toolchain
  uses: dtolnay/rust-toolchain@master
  with:
    toolchain: 1.85.0
    components: clippy, rustfmt

- name: Restore Rust cache
  uses: Swatinem/rust-cache@v2
  with:
    # One stable logical family for compatible Linux CI jobs.
    shared-key: linux-ci
    # Target artifacts are allowed only for compile-heavy jobs with evidence.
    cache-targets: true
    cache-all-crates: false
    cache-workspace-crates: false
    # Cargo-installed binaries are not part of the default CI cache contract.
    cache-bin: false
    cache-on-failure: false
    # Main seeds the family; all other refs restore without writing.
    save-if: ${{ github.ref == 'refs/heads/main' }}
```

`Swatinem/rust-cache` automatically includes the Cargo registry and Git dependency cache. `cache-targets: true` also includes dependency build artifacts; set it to `false` when a job has no demonstrated target-cache benefit. Do not add `github.sha`, run IDs, or branch names to `shared-key`: those create unbounded cache families.

For a pull-request or secondary job, use the same compatible `shared-key` and set `save-if: false`. For release and tag jobs, omit the cache step entirely:

```yaml
- name: Install Rust toolchain
  uses: dtolnay/rust-toolchain@master
  with:
    toolchain: stable
```

The toolchain reference and version must follow the repository's existing reproducibility policy. A repository may use a checked-in `rust-toolchain.toml`; the workflow still needs to show which components and targets are required.

## Cargo locking

Commit the root `Cargo.lock` when the repository builds executables, runs CI tooling, or otherwise requires reproducible CI dependencies. Use `--locked` on every dependency-resolving CI command, including `cargo build`, `cargo check`, `cargo clippy`, `cargo test`, `cargo run`, and `cargo metadata`.

Commands such as `cargo fmt --all -- --check` do not resolve dependencies and do not need `--locked`.

## Cache ownership rules

- Keep one logical cache family per compatible CI environment. The Rust environment and lockfile hashes provide the normal invalidation boundary.
- A matrix or secondary job may restore the family but must not save another persistent entry unless it is deliberately the sole `main` writer.
- Set `cache-on-failure: false`; failed jobs must not persist incomplete artifacts.
- Keep `cache-all-crates` and `cache-workspace-crates` false unless a measured case requires them.
- Add a new family only for a real incompatibility such as a different operating system or materially different build environment, and record the evidence in the repository's CI documentation or PR.
- Do not use a cache to hide release reproducibility problems. Release/tag jobs must remain independently buildable from the lockfile.

The expected bounded pattern is therefore:

| Job | Restore | Save | Typical configuration |
| --- | --- | --- | --- |
| `main` quality/build writer | yes | yes, on success only | `save-if: github.ref == 'refs/heads/main'` |
| pull request | yes | no | `save-if: false` |
| secondary/conformance job | yes | no | same `shared-key`, `save-if: false` |
| release/tag | no | no | no Rust cache step |

## Pilot and migration gate

`language-provider-protocol#8` is the first pilot for the bounded shared-cache policy. Its merge commit is [`05ce40a`](https://github.com/wrightkit/language-provider-protocol/commit/05ce40ad5b67b9f9aad584768e966ea0b4470040). The corresponding `main` CI run [32022937163](https://github.com/wrightkit/language-provider-protocol/actions/runs/32022937163) succeeded for both `rust` and `conformance` and created one `linux-ci` cache entry.

The first `main` run recorded `No cache found` in both jobs, so it proves a successful seed but not a subsequent restore. The pilot is not yet accepted as the reference pattern. Before migrating another repository, a later `main` run must show an actual restore or exact cache hit, and the repository should record:

- the run and commit that seeded the cache;
- the later run and job that restored it;
- whether target caching reduced meaningful build work;
- the resulting cache-family and writer count.

The requested repo-local migrations are now prepared in `language-provider-protocol`, `wright`, `opy-rs`, `del-rs`, and `workshop-rs` branches. They use the explicit composition above while preserving each repository's existing gates and release behavior. The migrations remain rollout candidates until remote CI records a later cache restore; this evidence gate must be satisfied before treating the pattern as an accepted reference or migrating additional repositories merely for consistency.

## References

- [Swatinem/rust-cache](https://github.com/Swatinem/rust-cache)
- [dtolnay/rust-toolchain](https://github.com/dtolnay/rust-toolchain)
- [WrightKit issue #3](https://github.com/wrightkit/.github/issues/3)
