# Quality-gate and CI design

Design owner: **Codex `/root` — 清衡**
Design batch: **QH-02**
Measured: **2026-08-12**
Mode: **design only; no pytest marker, workflow, dependency, script, or test was changed**

## Current feedback problem

The checkout currently collects **2,629 tests**. The central taxonomy selects:

| Selection | Tests selected |
| --- | ---: |
| `fast and current` | 2,491 |
| `slow and current` | 105 |
| `history` | 33 |
| `rl` | 55 |
| `reference` | 48 |

`fast and current` therefore selects about **94.8%** of the full suite. It is a currency filter with
a small slow exclusion, not a fast development loop. Collection alone takes roughly three seconds,
and a quiet run can provide no useful progress for minutes.

The test tree has about 47 Work II files, 32 Work I/paper files, 28 readily identifiable core
runtime/world files, 6 RL files, 5 reference files, and a large mixed remainder. File-name inference
cannot express risk, provider access, release mutation, or subsystem ownership reliably.

## Required orthogonal dimensions

Every test should receive one value in each mandatory dimension:

| Dimension | Values | Meaning |
| --- | --- | --- |
| duration | `smoke`, `core`, `extended`, `long` | expected feedback cost |
| currency | `current`, `history` | current contract versus compatibility reader |
| subsystem | `runtime`, `world`, `physchem`, `agent`, `data`, `work_i`, `work_ii`, `paper`, `docs`, `packaging` | change routing |
| externality | `offline`, `optional_backend`, `provider` | dependency/network/paid boundary |
| mutation | `read_only`, `local_output`, `release_build` | filesystem/release effects |

`rl` and `reference` can remain additional capability labels. Provider tests must use stubs by
default; a real-provider label is never part of ordinary CI.

## Target local commands

### Smoke — target under 60 seconds

Purpose: prove install/import, one environment lifecycle, one invalid-action rollback, one replay,
one task registry read, and one packaged-resource lookup.

It should not traverse publication artifacts, full registries, notebooks, optional reference
backends, RL training, Work I/II matrices, or provider clients.

### Core — target a few minutes with visible progress

Purpose: deterministic portable platform confidence:

- world/runtime transactions and constitution;
- public/private boundary;
- resource accounting;
- representative task families and composition compiler;
- trajectory schema, replay, score recomputation;
- CLI and wheel/package behavior.

Core remains offline and does not rebuild formal evidence.

### Research-focused

Use explicit rosters for Work I, Work II, paper/release, docs, RL, and reference validation. A change
map selects relevant rosters based on touched paths. Research-focused jobs may be longer, but every
job must expose a denominator and progress.

### Full

Nightly or manually dispatched. Includes all offline current/history tests and optional extras on
declared jobs. It must not call paid providers, unseal private data, or refresh committed evidence.

## CI matrix

Do not create the workflow until the active Work II branch is integrated and the smoke/core rosters
pass locally.

| Job | Platform/Python | Checks | External access |
| --- | --- | --- | --- |
| lint-type | Linux / 3.11 | Ruff, Mypy, diff hygiene | none |
| smoke-py311 | Linux / 3.11 | install + smoke roster | package download during setup only |
| smoke-py312-win | Windows / 3.12 | install + smoke roster, path/process portability | package download during setup only |
| core | Linux / 3.12 | offline core roster with coverage artifact | none after setup |
| docs | Linux / 3.12 + docs extra | public-doc audit and MkDocs strict build | none after setup |
| packaging | Linux / 3.11 | wheel build and outside-checkout smoke | none after setup |
| research-work-i | manual/path-selected | Work I focused non-data-producing tests | none |
| research-work-ii | manual/path-selected | Work II focused provider-free tests | none |
| full-offline | nightly/manual | complete offline suite | none after setup |

CI must never contain provider credentials, private seeds, raw runs, or maintainer-only release
authorization. Release evidence generation remains a separately authorized workflow and is not a PR
gate.

## Marker migration without losing coverage

1. Add new marker declarations and a validation test while preserving the current markers.
2. Create explicit smoke and core node rosters from already passing representative tests.
3. Require every test to have mandatory dimensions; initially report missing labels without failing.
4. Label one subsystem at a time and publish selection counts.
5. Switch missing-label validation to fail closed after the tree reaches 100%.
6. Retire filename/token inference only after old/new selection comparison proves no unintended loss.
7. Add a change-to-roster map and test that every protected path maps to at least one focused gate.

## Progress contract

For any job expected to exceed 60 seconds, output at least once per minute:

- stage;
- completed/total tests or experiment units;
- elapsed time and throughput;
- ETA when the denominator is stable;
- last completed node or active unit.

Use pytest progress reporting for ordinary tests and `scripts/run_with_progress.py` or a purpose-built
provider-free wrapper for long qualification jobs. Logs and probes remain outside the repository.

## Admission criteria for enabling CI

- active Work II write set is integrated or paused on a stable commit;
- Ruff and Mypy pass on the target baseline;
- smoke and core rosters are explicit and green locally on Windows;
- Linux/Windows path behavior is covered without changing scientific semantics;
- no workflow command regenerates `configs/current.json`, evidence graphs, release receipts, paper
  outputs, or formal reports;
- secrets and private artifacts are absent from job inputs and uploaded artifacts.

This design advances `CL-QA-01` through `CL-QA-06` but leaves them TODO. Implementation would touch
the protected `tests/`, workflow, and possibly script surfaces and must wait for a quiet main process.
