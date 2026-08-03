# ChemWorld collaboration contract

## Start here

Before changing Work I, read:

1. `workstreams/arxiv_v1/WORK_I_TODOLIST.md`
2. `workstreams/arxiv_v1/claims/README.md`
3. `workstreams/arxiv_v1/claims/TEMPLATE.md`

`WORK_I_TODOLIST.md` is the execution authority. The deeper scientific specification is
`workstreams/arxiv_v1/EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md`. Work II is separate and is
governed by `workstreams/flagship_tasks/WORK_II_TODOLIST.md`.

## Claim before writing

- Every Work I implementation, experiment, analysis, figure, manuscript, or release task requires a
  committed claim at `workstreams/arxiv_v1/claims/<TASK-ID>--<owner>.md` before substantive writes.
- One task has one accountable owner. Collaborators may be listed in the claim.
- Use branch `work1/<task-id>-<slug>` and a dedicated worktree unless the coordinator explicitly
  assigns an integration task on `main`.
- Declare the write set, deliverables, validation, shared-hot-file requests, UTC lease, and handoff ETA.
- The default lease is 48 hours. Update the heartbeat at least every 24 hours.
- Workers update only their own claim file. The coordinator owns the master status table.

## Isolation and integration

- Stay inside the declared write set. Request a reservation before editing a shared hot file listed in
  the Work I TODO.
- Do not regenerate the global evidence DAG, experiment ledger, manuscript, figure manifest, or release
  manifest from a task branch unless the task owns that integration surface.
- Keep code, raw runs, derived data, and reports in separate commits. Raw provider responses and local
  credentials never enter Git.
- Formal protocols, inclusion rules, seeds, thresholds, and estimands are immutable after freeze.
- Preserve evidence identity, source hashes, resource ledgers, and exact replay. Never replace a frozen
  result merely because a later run is more favorable.

## Repository hygiene

- Resolve current artifacts through `configs/current.json`; do not select files by version-looking names.
- Git history is the archive for superseded plans and smoke notes. Do not restore historical documents
  as competing current entry points.
- Run task-local validation and `git diff --check` before handoff. Data-producing tasks also require an
  immutable manifest, hashes, and explicit counting rules.
- Do not add `api.md`, `key2.md`, `.env`, private seeds, `runs/`, caches, generated site output, or raw
  provider payloads.
