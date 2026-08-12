# Changelog

This file records user-visible software, contract, and migration changes from the next ChemWorld
release onward. Historical development activity remains in Git history and immutable research
evidence; it is not reconstructed here as a retrospective changelog.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases use
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the installable software package.
Research protocols, trajectory schemas, task contracts, and evidence artifacts retain their own
explicit version identifiers and must not be inferred solely from the package version.

## [Unreleased]

### Added

- Repository contribution and security policies.
- A repository cleanup and closeout programme with explicit development/release boundaries.
- Repository guards for tracked credentials, package-to-research path dependencies, and upward
  package imports.

### Changed

- Nothing yet.

### Deprecated

- Nothing yet.

### Removed

- Nothing yet.

### Fixed

- Closed the existing static type-checking backlog without changing Work II experiment semantics.

### Security

- Documented private vulnerability reporting, credential handling, third-party execution, and
  scientific-safety boundaries.

## Release-entry rules

- Add only user-visible behavior, API/schema/contract changes, migration requirements, and material
  security fixes.
- Do not copy commit logs, experiment diaries, run identifiers, hashes, internal filenames, or
  provider payloads into this file.
- Keep development-only scientific results in their governed workstream; add a changelog entry only
  when a public software or data release changes.
- Link each released heading to its tag or release page when the release is published.
- Move relevant `Unreleased` entries into one dated release heading without rewriting earlier
  entries.
