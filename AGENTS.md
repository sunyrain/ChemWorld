# ChemWorld collaboration contract

## Start here

Before changing the first paper or its evidence programme, read:

1. `workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md`
2. The relevant experiment note, when the task produces new data
3. Current artifact bindings under `configs/current.json` only when existing generated evidence is used

The retired task matrix and superseded evidence plan are stored under
`workstreams/arxiv_v1/archive/coordination/`. The old claim, integration, story and review directories
are historical or machine-bound records; they do not authorize new work or define the current story.
Work II remains separate and is governed by `workstreams/flagship_tasks/WORK_II_TODOLIST.md`.

## Lightweight execution

- Run Python, pytest, Ruff, and experiment entry points through the repository's locked environment:
  `uv run --no-sync ...`. Do not invoke the system Python directly or use its dependency state as
  diagnostic evidence for this repository.
- New work is tracked directly in `FIRST_PAPER_TODOLIST.md`; do not create new claim files, leases,
  review queues or per-task worktrees for the first paper.
- Before a new data-producing experiment, write one concise experiment note for the whole experiment
  block. It must state the question, tested units or coverage design, measurements, pass/failure rules
  and expected outputs. Keep it short and do not create a separate audit package.
- The first paper is venue-neutral. Do not invoke Nature-specific skills or impose Nature-specific
  style unless the user explicitly re-enables them.
- The coordinator works on `main`. Use a single executor unless the user explicitly requests parallel
  work.
- Any command expected to run longer than 60 seconds must expose progress at least once per minute.
  Report the current stage, completed/total units, throughput, and ETA when the denominator is known;
  otherwise report a concrete liveness counter. Prefer native progress output, or use
  `scripts/run_with_progress.py`. Keep wrapper logs and probes outside the repository so clean-worktree
  preflights are not invalidated.
- Internal hashes, manifests, run identifiers, and repository filenames belong in evidence records
  and release metadata, not in reader-facing manuscript prose or figures.

## Development-first, freeze-once workflow

This is the default workflow for every ChemWorld workstream, including Work II.  Treat it as a
project invariant, not as an optional optimization.

- **Development mode is the default.** While platform functions, experiment runners, candidate
  mechanisms, measurements, or the experiment matrix are still changing, optimize for correct
  behavior and scientific validity.  Do not require a globally clean worktree, a repository-wide
  source-tree hash, a current release certificate, or regenerated preregistration/readiness/audit
  artifacts merely to implement, test, benchmark, or run a clearly labelled development experiment.
- **Do not let historical evidence govern new design.** A stale hash, old audit, superseded
  certificate, or previous freeze may describe historical evidence, but it must not block a
  scientifically justified platform or design change.  Mark the old artifact stale/historical and
  rebuild it at the next release freeze; do not repeatedly repair the old evidence chain during
  feature development.
- **Preserve the scientific invariants during development.** Every data-producing block still needs
  its concise experiment note before execution.  Once that block starts, its question, tested units,
  coverage, measurements, denominators, pass/failure rules, and stop rules are fixed.  Keep all
  failures, exact replay, resource accounting, and readable machine summaries.  Never overwrite an
  unfavorable result or change a running block in response to its outcomes.
- **Development evidence is labelled, not discarded.** Development runs may guide debugging and
  design, but they do not automatically become formal or publication evidence.  A platform fix
  requires the affected formal qualification block to rerun from its first unit.  Raw provider data,
  credentials, and ignored run directories remain outside Git.
- **Freeze once, late.** Enter `release-freeze` mode only after the relevant functions and experiment
  matrix are stable and the user has authorized formal evidence production or release.  At that
  point create one clean source commit, bind the smallest execution-relevant surface, generate the
  required preregistration/release checks once, and execute the formal block without changing its
  design.  Tests, prose, unrelated configs, and historical reports should not be included in a
  runtime source hash unless they can actually change the execution or evaluator semantics.
- **No audit treadmill.** Do not regenerate global preflight, readiness, evidence-graph, SHA inventory,
  or release audit after each development edit.  Run focused functional/scientific tests while
  developing, one integrated acceptance pass before freeze, and the release audit once after the
  final execution surface is committed.

## Isolation and integration

- Keep implementation, generated results and manuscript integration distinguishable in commits when
  practical. Raw provider responses and local credentials never enter Git.
- Once a qualification experiment starts, do not change its coverage selection or pass/failure rules
  in response to the result. Fixing a platform defect is allowed, but the affected qualification block
  must then be rerun from the start.
- Preserve exact replay and resource-ledger semantics. Do not replace a completed result merely because
  a later run is more favorable.

## Repository hygiene

- Resolve current artifacts through `configs/current.json`; do not select files by version-looking names.
- Git history is the archive for superseded plans and smoke notes. Do not restore historical documents
  as competing current entry points.
- Run focused task-local validation while implementing, then one integrated acceptance pass before the
  paper is exported. Do not repeat broad audits after every small edit.
- Data-producing tasks require a readable machine-generated summary with exact denominators and all
  failures. Manual hash inventories and duplicate manifests are not required unless release tooling
  already generates them automatically.
- Do not add `api.md`, `key2.md`, `.env`, private seeds, `runs/`, caches, generated site output, or raw
  provider payloads.
