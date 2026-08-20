# WrightKit release engineering standard

This document defines the preferred release-engineering principles for WrightKit repositories. It is intentionally tool-agnostic: repositories may use release-plz, release-please, hand-written GitHub Actions, generated workflows, or other tooling when the resulting release topology remains explicit and maintainable.

Repository-local documentation owns the exact commands, package names, targets, credentials, and recovery procedure. This document owns the cross-repository engineering rules.

## Core principles

### Keep the release topology simpler than the product

Release automation is reliability infrastructure. Prefer the smallest workflow that clearly expresses the required external state transitions.

Do not add a release tool merely because it is common in the ecosystem. A generator or release framework is justified only when it removes more project-owned complexity than it introduces.

For a small fixed distribution matrix, a readable hand-written workflow can be preferable to a generated workflow with its own configuration, compatibility constraints, and integrity checks.

### Give every external state transition one owner

Make ownership explicit for at least:

- version selection and changelog / Release PR maintenance;
- registry publication;
- canonical Git tag creation;
- binary builds and checksums;
- GitHub Release creation;
- downstream package-manager publication.

Do not create overlapping fallback owners for the same transition. In particular, avoid combining a release manager with repository shell logic that independently creates or repairs the same tag or GitHub Release during the normal path.

### Prefer the canonical tag as the binary-distribution trigger

When a repository publishes versioned binaries, the canonical version tag should normally be the release identity and the trigger for binary distribution.

Prefer:

```text
version / Release PR
  -> registry publication as applicable
  -> canonical vX.Y.Z tag
  -> binary build workflow
  -> GitHub Release
```

Avoid indirect release triggers such as `pull_request.closed`, detached merge commits, synthetic branches, or reconstructed version state unless the repository has a demonstrated requirement that cannot be expressed from the canonical tag.

### Create the GitHub Release after the complete artifact set exists

GitHub Release publication should normally be the completion boundary for primary downloadable artifacts.

Prefer:

```text
build all required targets
  -> package archives
  -> generate checksums / manifests / project-specific artifacts
  -> collect workflow artifacts
  -> create the GitHub Release once with the complete set
```

Do not introduce a draft/published state machine unless the repository actually needs a staged public-release contract. Building into temporary GitHub Actions artifacts and creating the Release only after all required builds pass is usually simpler.

Downstream distribution channels such as Homebrew, npm, Scoop, WinGet, or other package registries should not point users at assets that are not yet publicly available.

### Generated workflows have exclusive ownership

If a tool generates a workflow and verifies that generated file against its configuration, choose one ownership model:

1. **Generator-owned:** keep the workflow generated and change it only through the generator/configuration; or
2. **Repository-owned:** remove the generator contract and maintain the workflow directly.

Do not treat a generated workflow as hand-maintained source while still running generator integrity checks. If maintainers need routine edits that the generator does not support cleanly, that is evidence that the generator may be the wrong abstraction for the repository.

### Keep the happy path small; recover rare partial states explicitly

crates.io, Git tags, GitHub Releases, and downstream package managers are separate external systems. They do not form one atomic transaction.

Do not turn the normal release workflow into a transaction coordinator for every theoretically possible partial state.

Simple idempotency is valuable when it falls naturally out of the tools. Rare states that require reconstructing external history, moving published releases backwards, or inferring release identity from inconsistent systems should normally use an explicit maintainer recovery procedure instead of adding branches to every future release.

Do not manufacture a replacement version solely to hide a recoverable distribution failure unless the published version itself is semantically invalid.

## Credentials and event propagation

Use the narrowest credential that satisfies the required event semantics.

- Use the repository-provided `GITHUB_TOKEN` / `${{ github.token }}` for same-repository API operations when no downstream workflow event must be triggered.
- Use a dedicated GitHub App token or appropriately scoped secret when an automated Git operation must trigger another workflow and GitHub's `GITHUB_TOKEN` event-recursion protection would suppress that event.
- Do not replace all repository operations with one broad long-lived token for convenience.
- Keep registry authentication separate from release orchestration changes. Migrating to Trusted Publishing / OIDC is valuable, but it should be verified independently rather than bundled into an unrelated release-topology rewrite.

Document why a dedicated token exists whenever its purpose is event propagation rather than ordinary repository access.

## Concurrency and cancellation

Publication jobs must not race each other.

Use a stable concurrency group for release publication and set `cancel-in-progress: false` unless the repository has a specific safe cancellation contract. A newer commit arriving on `main` must not cancel a crates.io publication or a tag-triggered release already in progress.

Do not allow duplicate jobs for the same canonical tag.

## Validation standard

Release validation has multiple evidence levels. Keep them distinct.

### Static / pre-publication evidence

Useful checks include:

- YAML / actionlint validation;
- Cargo package/build checks;
- target matrix validation;
- generated-plan validation when a generator owns the workflow;
- archive/checksum generation tests;
- repository CI and release-specific unit/integration checks.

These prove only the paths they actually execute.

### Production release evidence

A release-system migration is not proven solely because its PR CI is green.

Before calling a new release topology established, observe at least one real release completing the declared external contract, for example:

```text
Release PR/version
  -> registry publication
  -> canonical tag
  -> all required binaries
  -> GitHub Release
  -> downstream channels, if declared part of the release
```

Record failures by the boundary that actually failed rather than describing the whole release system as successful because an earlier stage passed.

## Review checklist

When reviewing release changes, verify:

- Is each external state transition owned exactly once?
- Is the canonical release identity obvious?
- Does binary distribution start from that identity rather than reconstructed PR state?
- Are all required primary artifacts complete before the GitHub Release becomes public?
- Are downstream channels ordered after the assets they reference are public?
- Is a generated workflow either fully generator-owned or fully repository-owned?
- Is the normal path free from recovery logic for rare hypothetical states?
- Are credential choices explained by permission and event-propagation needs?
- Can concurrent main pushes or repeated tag events race publication?
- Does the validation evidence include a real release before the migration is declared proven?

## Repository-local documentation

Each releasing repository should document only its concrete release contract:

- release manager and versioning behavior;
- canonical tag format;
- registry publication order;
- binary targets and archive formats;
- project-specific release artifacts;
- token / environment requirements;
- normal maintainer procedure;
- explicit recovery steps for known partial states.

Do not copy this policy verbatim into every repository. Link to it and keep repo-local docs focused on current reality.

## Evidence behind this standard

This standard incorporates lessons from the `workshop-rs` release-pipeline rework in August 2026. The repository accumulated failures while combining release-plz, repository-owned recovery logic, detached merge-commit execution, and generated `dist` workflow behavior. The stable direction reduced the topology to release-plz for version/registry/tag responsibilities and a small tag-triggered repository workflow for fixed-platform binary builds and GitHub Release creation.

The durable lesson is not that WrightKit should always hand-write release workflows. It is that release tooling must reduce ownership and state complexity; when the abstraction becomes harder to reason about than the release contract, simplify or remove it.
