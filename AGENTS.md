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

- New work is tracked directly in `FIRST_PAPER_TODOLIST.md`; do not create new claim files, leases,
  review queues or per-task worktrees for the first paper.
- Before a new data-producing experiment, write one concise experiment note for the whole experiment
  block. It must state the question, tested units or coverage design, measurements, pass/failure rules
  and expected outputs. Keep it short and do not create a separate audit package.
- The first paper is venue-neutral. Do not invoke Nature-specific skills or impose Nature-specific
  style unless the user explicitly re-enables them.
- The coordinator works on `main`. Use a single executor unless the user explicitly requests parallel
  work.
- Internal hashes, manifests, run identifiers, and repository filenames belong in evidence records
  and release metadata, not in reader-facing manuscript prose or figures.

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
