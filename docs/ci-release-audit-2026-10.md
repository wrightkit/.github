# CI work reuse and release publication audit (October 2026)

Point-in-time audit of CI work reuse and release publication ordering across
WrightKit's actively developed Rust repositories, per `wrightkit/.github#49`.

Evidence was recorded on 2026-10-25 from each repository's `main` HEAD:

- `wright` @ `5449213d` — `.github/workflows/ci.yml` (724 lines),
  `release.yml` (645), `release-please.yml` (53); `release-please-config.json`;
  workspace `rust-version 1.97.1`, `rust-toolchain.toml channel 1.97.1`,
  version `0.38.1`.
- `workshop-rs` @ `660b365` — `ci.yml` (170), `release.yml` (124),
  `release-plz.yml` (18); `release-plz.toml`; `rust-version 1.88.0`, version
  `1.25.3`.
- `opy-rs` @ `67b7815` — `ci.yml` (157), `release-plz.yml` (308);
  `release-plz.toml`; `rust-toolchain.toml channel stable`,
  `rust-version 1.88.0`, version `0.3.25`.
- `athena` @ `40d450d` — `ci.yml` (41), `release-please.yml` (57);
  `release-please-config.json` publishing `athena-sim` `0.2.0` as tag + draft
  GitHub Release only (`publish = false` on all crates).
- `wrightkit/.github` @ `af134bf` — shared `rust-quality.yml`,
  `release-plz-crates.yml`, `setup-rust` composite action.

`deltin-rs` is excluded by owner direction (2026-10-20 comment on
`wrightkit/.github#49`: paused until it resumes). `athena` is included per the
same direction.

## Contracts recorded

These restate or sharpen the existing rules in [`rust-ci.md`](rust-ci.md) and
[`release-engineering.md`](release-engineering.md) so each finding names the
contract it violates or satisfies.

### Build identity

Two cargo invocations share a build identity only when all of these match:

- revision and source inputs (checkout SHA, feature flags, `cfg`-relevant env);
- dependency lock state (`Cargo.lock`, `--locked`);
- Rust toolchain/compiler identity (channel + version);
- target triple;
- cargo profile (dev/test/release/custom such as `dist`);
- feature set (`--all-features`, `--features`, `--no-default-features`);
- other material inputs (RUSTFLAGS, linker config, workspace members selected).

Different toolchains, targets, profiles, or feature sets are never
interchangeable merely because they share a commit.

### Reuse within one workflow run

- Same build identity: one producer builds the output; downstream consumers
  reuse the producer's current-run artifact or job result (`needs:` + artifact
  download). `rust-ci.md` already states this for runtime-bound gates; this
  audit applies it to build outputs generally.
- A consumer may rebuild only when its build identity differs, or when a
  documented failure mode (process boundary, runner OS, artifact unavailability)
  requires independence.
- A shared dependency/build cache is a reconstruction accelerator across runs
  and jobs. It is not evidence that the current revision's output was produced
  once — cache hits still re-link and re-test locally.

### Cross-run cache policy

- One stable logical family per compatible environment; keys cover toolchain,
  lockfile, and inputs that change the build (`shared-key` + `rust-cache`'s own
  inputs). No `github.sha`/run id in keys.
- Writer ownership: only a successful `main` job saves a persistent family;
  PR and secondary jobs restore only. Prevents untrusted or partial PR work
  from becoming an authoritative shared baseline.
- `cache-targets` only for compile-heavy jobs with a measured benefit; release
  and tag jobs omit the cache step entirely.
- Cargo registry/git dependencies are cached by `rust-cache` in every in-scope
  job — no job re-downloads dependencies when a compatible cache can satisfy it.
- Whole `target/` caching and workspace incremental state are not the default:
  restore/save cost on hosted runners must be shown to beat reconstruction.

### Release publication ordering

`release-engineering.md` requires: canonical tag triggers binary
distribution, one owner per external transition, GitHub Release created once
after the complete artifact set, downstream channels only after public
assets. This audit adds two rules there:

- *Gate publication on the release revision's verified CI result* —
  publication must not run ahead of the revision's authoritative CI result;
  an encoded required-checks gate is preferred over the implicit Release-PR
  merge gate.
- *`latest` pointers never regress* — mutable `latest` promotion is
  serialized per repository or version-guarded; per-tag concurrency groups
  alone do not provide this.

## Findings by repository

### Shared reusable layer (`wrightkit/.github`)

- `rust-quality.yml` produces no current-run artifact. Consumers that need a
  binary either rebuild (the `rust-ci.md` aspiration has no mechanism) or add
  their own producer job (wright's `wright-cli-build` does exactly this).
- `release-plz-crates.yml` `release` needs only `package-preflight`
  (`release-plz-crates.yml:41`) — no edge to the caller's CI gate, so crates.io
  publication and tag creation do not encode any same-revision CI dependency.
  Mitigation today is Release-PR CI + branch protection, which is not visible
  in the workflow.
- `package-preflight` runs `cargo publish --workspace --locked --dry-run`
  (line 36) and `release-plz release` then re-packages the same crates —
  two package builds of one revision per run, inherent to verify-then-publish.
  Accepted; recorded, not a follow-up.
- `release` and `release-pr` jobs lack `timeout-minutes`
  (`release-plz-crates.yml:45–53,72–97`) — violates `rust-ci.md` rule 7.
- `setup-rust` and shared workflows are compliant on caching: `save-if` writes
  only on `main`, `cache-on-failure: false`, no workspace-crate caching
  (`setup-rust/action.yml:63–74`).
- Third-party actions are tag-pinned in repo-local workflows while
  `ci-platform.md:25` mandates full-SHA pins for third-party actions:
  `dorny/paths-filter@v4`, `pnpm/action-setup@v6`,
  `obi1kenobi/cargo-semver-checks-action@v2`,
  `googleapis/release-please-action@v5`. `actions/*` tag pins are ambiguous
  under the current wording — resolved as covered, since the mandate's purpose
  (unreviewed upstream movement) applies equally.
- No `actionlint` job exists anywhere, though three repository release docs
  name it as the expected release-change check (`workshop-rs/docs/release.md`,
  `opy-rs/docs/release.md`, `deltin-rs/docs/release.md`).

### `wright`

Duplicated or reusable work in `ci.yml`:

- `wright-cli-build` (ci.yml:110–145) is the designated producer: debug,
  default features, `cargo build --locked -p wright-cli`, uploads
  `wright-cli-linux-stable-debug`. Consumers `workshop-integration`,
  `opy-integration` (partially), `cli-behavior`, `metrics-shard`, and
  `metrics-latency` download it — the producer/consumer contract is mostly
  realized. (`metrics-drift` consumes only `metrics-shard-*` JSON artifacts,
  not the CLI binary.)
- `benchmark` (ci.yml:353–382) runs `cargo build --locked -p wright-bench`
  with the same build identity (ubuntu, 1.97.1, dev profile, default features)
  but does not consume the producer. One producer building
  `-p wright-cli -p wright-bench` satisfies both — reuse candidate.
- `opy-integration` (ci.yml:242–285) re-executes `cargo test` subsets under
  default features where `rust-quality` already ran them under
  `--all-features`. Different feature set → different build identity →
  recorded as complementary coverage, retained.
- `cli-behavior` (ci.yml:336–351) installs Rust it never invokes — dead step.
- `lpp-integration` (ci.yml:312–314) builds `lpp-mock-provider` in a second
  workspace outside the `workspaces:` cache input → uncached dependency builds
  each run; small but real. Recorded; a cache-input widening is a valid
  follow-up only if measured worthwhile.
- Path-filter outputs `opy`, `lpp`, `cli` are all wired to `rust_core`
  (ci.yml:18–21); the `||` at ci.yml:113 is dead disjunction. Cosmetic.
- `wasm-core` restores cache family `linux-wasm-stable-release` that no job
  ever writes (ci.yml:665) — dead restore-only family, permanently cold.

Duplicated or reusable work in `release.yml`:

- `build` (x4 targets, release.yml:153–248) compiles `wright-cli`/`wright-lsp`
  per target; `core-package` (250–306) builds `wright-wasm` for
  `wasm32-unknown-unknown`; `release-metrics` (406–439) builds
  `--release -p wright-cli` with no `--target` and no `ui` feature — a third,
  genuinely distinct identity from `build`'s linux leg (no ui feature vs ui).
  The rebuild is justified by identity — but `release-metrics` is a candidate
  for co-location inside `build`'s linux leg since it shares the toolchain and
  profile.
- Cache steps exist on release/tag jobs contrary to "omit the cache step
  entirely" (`rust-ci.md:20,92`). Families `release-<target>-stable-release`
  and `release-wasm-core` are written by every **nightly** `workflow_run` and
  main-branch dispatch (`cache-save: github.ref == 'refs/heads/main'`,
  release.yml:195–202, 272–279) but never on the tag-push releases that are
  their stated purpose — the cache accelerates a run class that does not need
  it, while the release-class runs always restore cold. `release-metrics`'s
  `release-metrics-stable` family (420–424) is never written at all.

Release ordering (`release.yml`):

- Correct where ordering exists: `publish-r2` verifies immutable R2 objects
  publicly before `publish-release` flips the draft to public
  (needs chain 477–482), and `advance-latest` follows `publish-release`
  (619–645). Mutable `latest` cannot expose a partial release.
- `release-identity` verifies tag↔commit↔version (34–151) but asserts nothing
  about the revision's CI result; only the nightly path is CI-gated via
  `workflow_run` success (36–39). Stable publication encodes no same-revision
  CI dependency — it relies on Release-PR merge protection, invisible here.
- Per-tag concurrency groups (`wright-<tag>`, 29–31) do not serialize across
  different tags: two stable runs can interleave `publish-r2`,
  `publish-release --latest`, and `advance-latest`, allowing an older tag to
  regress `latest`. No monotonic guard exists.
- `publish-r2`, `advance-latest`, `publish-tap` hold R2/`GH_TOKEN` secrets
  without `environment: release` (575–645, 441–473); only `publish-release`
  and `publish-npm` use it (485, 553).
- `gh release` path edge: if a Release already exists as *public* (not draft),
  `publish-release` logs and uploads nothing (534–543) — a silently empty
  release is possible if the draft contract is ever bypassed upstream.
- `release-assets` downloads `pattern: wright-*` (322) which also matches the
  `wright-core-package` artifact — harmless but imprecise.
- `scripts/package-release.py:97` hardcodes `"toolchain": "stable"` in
  `.build.json`; builds actually use pinned `1.97.1`. The verify step asserts
  the static label, so provenance records fiction.
- `release-please.yml` syncs `Cargo.lock` under `stable` (38–46:
  `setup-rust` with no toolchain input → `RUSTUP_TOOLCHAIN=stable`), not the
  pinned 1.97.1 — lock resolution could drift from the CI toolchain.
- No `timeout-minutes` on any job in `release.yml` or `release-please.yml`
  — violates `rust-ci.md` rule 7.

### `workshop-rs`

Duplicated or reusable work in `ci.yml`:

- `check` is a matrix `[stable, 1.88.0]` of the shared `rust-quality` job
  (19–28): two full fmt+clippy+`test --workspace --all-targets` runs per
  revision. The MSRV leg is justified (`rust-ci.md:68`, published library).
- `catalog-check` (58–71) runs `workshop-catalog-gen -- check` under `1.88.0`
  — same toolchain/profile/features as `check`'s MSRV leg, but the quality job
  uploads nothing to consume, so it recompiles the workspace. Reuse blocked by
  the shared layer's missing producer output.
- `real-project-scenarios` (89–170) re-executes test filters
  (`tests::{parser,emitter,locale}::pinned_real_projects`) that already ran
  inside `check`'s stable `cargo test --workspace` for the same revision and
  identity. The job exists for per-scenario logs and artifact upload
  (165–170) — a real justification, but the re-execution should be recorded as
  deliberate rather than accidental.
- PR `types: [opened, synchronize, reopened, edited, labeled, unlabeled]`
  (ci.yml:10) exist to serve `semver-check`'s title/label-derived release
  type (36–51) — but every label edit re-runs the entire workflow, including
  the two `rust-quality` legs and scenario jobs, for the same revision.

Release ordering (`release.yml`, `release-plz.yml`):

- `release-plz` publishes crates and creates the `vX.Y.Z` tag (no GitHub
  Release; `release-plz.toml` disables it) — publication needs only
  `package-preflight` inside the reusable workflow; same same-revision CI gap
  as the shared layer.
- `release.yml` ordering is correct internally: `github-release` needs
  `[build, catalog-identity]` and creates the Release once with the complete
  artifact set (105–124).
- `github-release` has no `environment: release` — binary publication is
  unprotected while the reusable crates publish runs inside the environment.
- `gh release create` defaults to marking the release "latest"; per-tag
  concurrency (`release-${{ github.ref }}`, 11–13) does not serialize across
  tags — older tag finishing later can regress GitHub-latest.
- Release jobs configure cache families that are never written
  (`release-<target>`, `release-catalog`; release.yml:36–41, 88–92) and keep
  cache steps on a tag/release job contrary to the omit-cache rule.
- Tag pattern `v[0-9]+.[0-9]+.[0-9]+*` (line 6) fires on any `vX.Y.Z-*` tag,
  broader than the canonical `vX.Y.Z` contract.
- No `timeout-minutes` on any `release.yml` job.

### `opy-rs`

Duplicated or reusable work in `ci.yml`:

- `compiler-compatibility` (34–100) builds `opy-cli` debug and `opy-compat`
  `--release --features compatibility` in one job — two distinct identities,
  both needed by the harnesses. Compliant producer.
- `reconstruction-corpus` (102–119) runs `cargo test -p opy-rs --test
  reconstruction_corpus` under default features — the same test binary already
  ran under `--all-features` in `rust-quality`. The feature identity differs
  on paper, but the corpus suite compiles identically either way; the
  re-execution buys a separate pass/fail line at the cost of a second build.
- `macro-runtime-ports` (121–146) is a legitimately distinct identity
  (macOS+Windows runners, JS runtime port coverage).
- `release-order` (148–157) runs on every CI run regardless of changed files —
  cheap, acceptable.

Release ordering (`release-plz.yml`):

- Ordering is correct and machine-asserted: draft release → provider builds at
  the tag → checksum-verified immutable R2 + public verification →
  `promote-release` (environment: release) → `advance-latest` pointer, with
  `tools/verify-release-order.py` asserting the needs graph in CI
  (ci.yml:148–157). This is the reference shape for the other repositories.
- The tail jobs (`provider`…`advance-latest`) have no concurrency group;
  only the reusable `release` job serializes. Two main-push runs can overlap
  after publication, so `opy-rs/latest/version` can regress the same way as
  wright's pointer — and unlike wright there is no per-tag group at all.
- `publish-provider-r2` and `advance-latest` hold R2 secrets without
  `environment` (155–252, 278–308).
- `opy-provider`'s publication status is ambiguous: the crate lacks
  `publish = false` and any `release = false` in `release-plz.toml`, its
  changelog shows release-plz-managed entries, yet `docs/release.md:8` names
  only `opy-rs` and `opy-cli` as publishable. `cargo publish --workspace
  --dry-run` in the shared preflight will attempt it.
- `aarch64-apple-darwin` builds on `macos-14` (release-plz.yml:58) while
  wright uses `macos-15` and workshop-rs uses `macos-latest`/`macos-15-intel`
  — matrix drift, not a contract issue.
- No `timeout-minutes` on any repo-owned job in `ci.yml` or `release-plz.yml`.

### `athena`

- `ci.yml` is minimal and compliant: `rust-quality` (1.88.0, `linux-ci`
  family, sole writer on main) plus `wasm-check` — a legitimately distinct
  identity (`wasm32-unknown-unknown` target, `cargo check`) with restore-only
  caching and `timeout-minutes: 15`. No duplicated cargo work.
- `release-please.yml`: release-please creates the `vX.Y.Z` tag and a **draft**
  GitHub Release for `athena-sim` (`publish = false`; no crates.io, no binary
  assets). The draft boundary keeps public visibility behind an owner action —
  compliant with the publication-ordering contract.
- `release-please` job has no `timeout-minutes`, tag-pins
  `googleapis/release-please-action@v5`, and the `Cargo.lock` sync runs under
  `stable` (setup-rust default) while CI pins 1.88.0 — same toolchain drift as
  wright's equivalent step.
- Publication has no same-revision CI edge beyond Release-PR CI — same class
  of gap, lowest exposure (draft release, no artifacts).

## Decisions

- **Producer/consumer reuse:** adopt the contract as stated. Concrete
  single-producer consolidations are filed per repository below. The shared
  `rust-quality.yml` gains no artifact output in this audit; whether it should
  is a shared-workflow design question filed as a `.github` follow-up rather
  than decided here.
- **Cross-run caching:** current policy is sound and mostly implemented.
  Registry/git dependency caching exists in every in-scope job (satisfies the
  no-repeated-downloads criterion). Findings are dead families and cache steps
  on release jobs — hygiene follow-ups, not contract changes.
- **Workspace incremental/`target/` caching:** deliberately omitted.
  `rust-cache` already restores compiled *dependency* artifacts for
  compile-heavy jobs (`cache-targets` selectively enabled); workspace-crate
  incremental state is explicitly excluded everywhere
  (`cache-workspace-crates: false`). The measured-benefit bar
  (`rust-ci.md`) is unmet: no evidence shows hosted-runner restore+save of
  workspace intermediate state beats rebuilding workspaces that finish
  compile in tens of seconds on cache hits. A measurement follow-up is
  unnecessary unless a job's own timing changes that calculus.
- **Same-revision CI gating for publication:** now a written rule in
  `release-engineering.md`. Today it is enforced only implicitly through
  Release-PR merge protection; the reusable `release-plz-crates.yml` is the
  right place to encode it for crate-publishers (CI-P2), and
  `wright/release.yml` needs its own gate because it predates that workflow
  (W-P2).
- **Release ordering gaps (latest regression, unprotected publication,
  timeouts, dead caches):** repository-local follow-ups; none weakens gates.

## Follow-up issues

Repository-owned, evidence-backed implementation items (issue numbers as
filed):

- `wrightkit/.github`
  - CI-P1 → `wrightkit/.github#124`: `timeout-minutes` on
    `release`/`release-pr` in `release-plz-crates.yml`; adopt `actionlint` as
    the shared workflow-change check (three repo release docs already name
    it); clarify that `actions/*` falls under the third-party SHA-pin mandate
    and migrate tag-pinned third-party actions to SHAs.
  - CI-P2 → `wrightkit/.github#125`: encode the same-revision CI gate in
    `release-plz-crates.yml` (e.g. a `required-check-runs` input asserted
    against the release revision's check suite before crates
    publication/tagging).
  - CI-P3 → `wrightkit/.github#126` (`needs-decision`): decide whether
    `rust-quality.yml` offers an optional producer-artifact output for
    downstream consumers, or the policy documents consumer-side producer jobs
    as the contract.
- `wrightkit/wright`
  - W-P1 → `wrightkit/wright#984`: merge `benchmark`'s `wright-bench` build
    into the `wright-cli-build` producer (identical build identity) and
    consume one artifact set.
  - W-P2 → `wrightkit/wright#985`: `release.yml` ordering — same-revision CI
    gate in `release-identity`; `timeout-minutes` on all jobs;
    `environment: release` on `publish-r2`/`advance-latest`/`publish-tap`;
    monotonic guard or serialized promotion for `latest`.
  - W-P3 → `wrightkit/wright#986`: hygiene — remove `cli-behavior`'s unused
    Rust setup; drop the `linux-wasm-stable-release` and `release-*` cache
    steps/families (release jobs must omit caching; the families only ever
    populate on nightly/dispatch runs, never on tag releases); pin
    `release-please.yml` lock sync to 1.97.1; record the real toolchain in
    `package-release.py`; tighten the `release-assets` glob; collapse the
    dead `opy`/`lpp`/`cli` filter aliases.
- `wrightkit/workshop-rs`
  - S-P1 → `wrightkit/workshop-rs#574`: decide and document whether
    `real-project-scenarios` deliberately re-executes tests covered by
    `check` (per-scenario artifacts) or merges; route `catalog-check` to a
    producer artifact if CI-P3 adopts one.
  - S-P2 → `wrightkit/workshop-rs#575`: `release.yml` conformance —
    `timeout-minutes`; `environment: release` on `github-release`; remove
    dead release cache families; tighten the tag pattern to canonical
    `vX.Y.Z`; same-revision CI gate (via CI-P2); scope PR trigger types so
    label edits don't re-run the full suite for `semver-check`.
- `wrightkit/opy-rs`
  - O-P1 → `wrightkit/opy-rs#644`: serialize the release tail (concurrency
    group spanning `provider`→`advance-latest`, or per-version monotonic
    guard on `latest`); `environment: release` on R2/pointer jobs;
    `timeout-minutes` on repo jobs.
  - O-P2 → `wrightkit/opy-rs#645` (`needs-decision`): resolve `opy-provider`
    publication intent (`publish = false`, `release = false`, or documented
    as publishable) so the shared `cargo publish --workspace --dry-run`
    preflight is unambiguous.
  - O-P3 → `wrightkit/opy-rs#646`: record whether `reconstruction-corpus`'s
    default-features re-run is deliberate; align the
    `aarch64-apple-darwin` runner pin.
- `wrightkit/athena`
  - A-P1 → `wrightkit/athena#36`: `release-please.yml` — `timeout-minutes`;
    pin the `Cargo.lock` sync toolchain to 1.88.0; SHA-pin
    `release-please-action`.

No follow-up is filed for `deltin-rs` (paused by owner direction) or for the
`package-preflight` dry-run/publish double build (inherent verify-then-publish
cost).
