# Team Project Management

ChemWorld should treat `TODO.md` as the strategic backlog, not as the daily
work tracker. Daily execution should happen through GitHub Issues, milestones,
projects, pull requests, and release artifacts.

## Operating Model

Use three levels:

1. Roadmap: `TODO.md`, `docs/roadmap.md`, and architecture docs.
2. Execution: GitHub Issues, Project board, milestones, and PRs.
3. Evidence: tests, benchmark reports, docs, notebooks, and release artifacts.

Every task should move from idea to merged code through:

```text
TODO.md item
  -> GitHub issue
  -> design note or acceptance criteria
  -> implementation branch
  -> PR with tests/docs
  -> review
  -> merge
  -> release artifact or benchmark report update
```

## Project Board

Recommended columns:

- `Inbox`: raw ideas, not yet scoped.
- `Ready`: scoped issue with owner, acceptance criteria, and priority.
- `In Progress`: actively worked this week.
- `Review`: PR open or design awaiting review.
- `Validation`: tests, benchmark runs, notebook smoke, docs build.
- `Done`: merged and documented.
- `Deferred`: valid but not in the current milestone.

Rules:

- An item cannot enter `Ready` without acceptance criteria.
- An item cannot enter `In Progress` without an owner.
- An item cannot enter `Done` without a linked PR or explicit decision record.
- Keep WIP small: each person should normally own at most two active issues.

## Milestones

Recommended milestones for the physchem-core push:

- `M0 Governance`: third-party audit, no-copy policy, project management.
- `M1 Reaction Network`: generic species, stoichiometry, mechanism loader.
- `M2 Property Core`: vapor pressure, Cp, density, enthalpy, units.
- `M3 Phase Equilibrium`: activity models, LLE, VLE, flash.
- `M4 Reactor Models`: batch, semi-batch, CSTR, PFR.
- `M5 Unit Operations`: extraction, distillation, crystallization, drying.
- `M6 Reference Validation`: optional comparisons to external packages.
- `M7 Benchmark Tasks`: new tasks, baselines, docs, artifacts.

Each milestone should have:

- scope;
- non-goals;
- owner;
- target date;
- risk list;
- required tests;
- release note.

## Labels

Use stable labels:

- `area:physchem-core`
- `area:reaction-network`
- `area:thermo`
- `area:eos`
- `area:phase-equilibrium`
- `area:reactor`
- `area:unit-operation`
- `area:instrumentation`
- `area:evaluation`
- `area:docs`
- `area:notebook`
- `kind:design`
- `kind:implementation`
- `kind:test`
- `kind:bug`
- `kind:refactor`
- `kind:research`
- `priority:P0`
- `priority:P1`
- `priority:P2`
- `status:blocked`
- `status:needs-decision`
- `good-first-issue`

## Issue Quality Bar

Every implementation issue should contain:

- problem statement;
- target module/files;
- desired public API;
- acceptance criteria;
- test plan;
- documentation update;
- risks or model limitations;
- reference links if relevant;
- non-goals.

Example:

```text
Title: Implement generic stoichiometric matrix builder

Acceptance criteria:
- Parses reversible and irreversible reaction equations.
- Builds species list and S matrix.
- Checks element conservation.
- Fails invalid reactions with clear errors.
- Includes tests for at least five mechanisms.
```

## PR Quality Bar

A PR should include:

- linked issue;
- short design summary;
- changed public API;
- tests run;
- docs updated;
- benchmark impact;
- known limitations.

Required local checks before review:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Additional checks for benchmark-affecting PRs:

```powershell
chemworld run --task reaction-to-assay --agent scripted_chemistry
chemworld verify --constitution --submission <trajectory.jsonl>
chemworld baselines report --tasks <task> --agents random scripted_chemistry --seeds 0
```

## Decision Records

Use a short Architecture Decision Record when a choice affects future work:

```text
docs/adr/0001-physchem-core-boundary.md
docs/adr/0002-reaction-network-schema.md
docs/adr/0003-property-correlation-source-policy.md
```

ADR format:

- Status: proposed, accepted, superseded.
- Context.
- Decision.
- Alternatives considered.
- Consequences.
- Follow-up tasks.

## Weekly Rhythm

Suggested team cadence:

- Monday: triage board, choose weekly P0/P1 issues.
- Wednesday: 20-minute technical sync, unblock decisions.
- Friday: demo merged work, update docs, close stale issues.
- End of milestone: run full validation and write release notes.

Daily async update format:

```text
Yesterday: ...
Today: ...
Blocked by: ...
PR/issue links: ...
```

## Ownership Model

Recommended roles:

- Maintainer: release gate, issue triage, final merge.
- Module owner: owns architecture and tests for one physchem area.
- Implementer: writes code and local docs.
- Reviewer: checks correctness, model limits, and maintainability.
- Benchmark steward: reruns baselines and watches score drift.
- Education steward: checks notebooks and teaching clarity.

Every high-impact PR should have at least:

- one implementation reviewer;
- one scientific/model reviewer;
- one benchmark or docs reviewer if the public API changes.

## Backlog Hygiene

Every two weeks:

- close duplicate issues;
- split issues larger than one week of work;
- move vague ideas back to `Inbox`;
- confirm P0/P1 priorities;
- update `TODO.md` only when the roadmap changes;
- update task cards when benchmark contracts change.

## Definition Of Done

A feature is done only when:

- code is merged;
- tests cover normal and failure paths;
- docs explain assumptions and limitations;
- public API or schema changes are documented;
- benchmark or notebook impact is checked;
- no hidden dependency on local reference repos exists.

## How To Use `TODO.md`

`TODO.md` is the north star. Use it to create scoped issues:

- one issue per coherent deliverable;
- one milestone per capability layer;
- one PR per issue where possible;
- update the checkbox only after the corresponding issue is merged.

Do not use one giant PR to complete a full milestone. Large scientific modules
should be merged as thin vertical slices:

```text
schema -> core math -> tests -> env integration -> docs -> benchmark task
```
