# ChemWorld collaboration contract

## Start here

Before changing the first paper or its evidence programme, read:

1. `workstreams/arxiv_v1/FIRST_PAPER_EVIDENCE_PLAN.md`
2. The relevant frozen protocol and current artifact bindings under `configs/current.json`

`WORK_I_TODOLIST.md` and its claim directory are retained as historical coordination records;
they are no longer the execution authority and must not receive new task rows after W1-R01.
Work II remains separate and is governed by `workstreams/flagship_tasks/WORK_II_TODOLIST.md`.

## Evidence before expansion

- Before a new data-producing experiment, commit a standalone protocol that states the research
  question, intervention, independent unit, inclusion and censoring rules, estimand, thresholds,
  seeds, expected outputs, failure policy, owner, and write set.
- Organize new work by claim-to-evidence need in `FIRST_PAPER_EVIDENCE_PLAN.md`, not by reviving the
  retired task matrix.
- Manuscript integration on `main` is coordinator-owned. Parallel workers, when explicitly used,
  must use isolated branches or worktrees and stay within their protocol write sets.
- Internal hashes, manifests, run identifiers, and repository filenames belong in evidence records
  and release metadata, not in reader-facing manuscript prose or figures.

## Isolation and integration

- Stay inside the protocol or coordinator-declared write set. Request a reservation before editing a
  shared manuscript, figure, derived-data, or release surface.
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
