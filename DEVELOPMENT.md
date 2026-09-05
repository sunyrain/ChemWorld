# ChemWorld development guide

ChemWorld keeps one current entry point per workstream. Git history stores superseded plans,
editorial snapshots and retired producer code. Frozen experiment notes, inputs, results, failures
and release artifacts remain available wherever evidence or replay consumers require them.

## Repository boundaries

- `src/chemworld/` contains the installable environment, agent interfaces, and evaluation runtime.
- `configs/current.json` resolves current evidence and distinguishes development state from frozen releases.
- `configs/` contains current protocols/templates and frozen inputs required to interpret retained evidence.
- `scripts/` contains current commands and retained reconstruction tools; its guide identifies their scope.
- `workstreams/` contains one tracker per workstream, experiment notes and retained evidence records.
- `runs/`, `site/`, caches, credentials, and provider responses are local artifacts and remain ignored.

The environment provides physical-chemistry worlds, interventions, observations, budgets, scoring,
and replay. Evaluation campaigns may update an Agent's context, memory, and actions, but ChemWorld
does not retrain hosted models or modify their weights.

## Locked contributor environment

The public README documents a general editable `pip` install for users. Repository development uses
the committed `uv.lock` so validation does not silently inherit or mutate the system Python
environment. On a fresh checkout, install once with:

```bash
uv sync --extra dev
```

After setup, run all repository tools with `uv run --no-sync ...`. Add optional extras to the
one-time sync command when the task requires them; do not let a validation command perform an
implicit dependency sync.

## Change workflow

1. Resolve active paths from `configs/current.json`; do not select files by largest version suffix.
2. Trace consumers before removing superseded code or configuration. Migrate active callers together;
   preserve frozen inputs and results at their bound paths without refreshing historical hashes.
3. Add or update focused tests for the affected contracts. Avoid a full test run unless the change
   genuinely spans the whole repository.
4. Run Ruff and mypy on the changed Python modules, plus their focused tests. Run package-wide
   mypy only for cross-package changes or the integrated acceptance pass; run wheel smoke when
   packaging or resource lookup changes.
5. Keep raw runs outside Git. Commit readable machine summaries with exact denominators and all
   failures; retain the records needed by current evidence, replay and frozen release consumers.
6. Check `git status --short` before committing; never add `api.md`, `key2.md`, `.env`, private seeds,
   or raw provider responses.

For a quick development smoke, run these six existing behavior tests (normally under 10 seconds):

```bash
uv run --no-sync pytest -q \
  tests/test_env.py::test_env_registers_and_steps \
  tests/test_invalid_action_atomicity.py::test_state_precondition_rollback_only_penalizes_process_ledger \
  tests/test_score_replay.py::test_result_rejects_metric_binding_and_source_byte_tampering \
  tests/test_tasks_and_wrappers.py::test_builtin_tasks_are_instantiable \
  tests/test_resource_accounting.py::test_resource_ledger_tracks_checkpoints_and_fails_closed \
  tests/test_mechanism_library.py::test_mechanism_schema_contract_is_loadable_and_matches_runtime_constant
```

This is a liveness smoke, not acceptance evidence for every subsystem. Run the owning focused tests
for changed behavior; run RL, reference-data, notebook, wheel, or release checks only when those
surfaces change.

Coverage is an explicit diagnostic, not a default gate on every focused test. When coverage is the
question being investigated, opt in for the relevant surface:

```bash
uv run --no-sync pytest --cov=chemworld --cov-report=term-missing tests/<relevant-test-file>.py
```

The repository does not use a global coverage percentage as acceptance evidence. Prefer missing
behavior and failure-path analysis over increasing a percentage with self-referential tests.

Generated evidence must distinguish environment validation from Agent performance. A passing backend
check does not imply a method result, benchmark ranking, or publication claim.

## Local generated files

Use a task-specific directory under the system temporary directory for pytest `--basetemp`, PDF
renders and diagnostic logs. Disposable `.pytest-tmp-*`, tool caches and generated `site/` output
can be removed when no job uses them. Keep `.venv/`, credentials, user-supplied assets and `runs/`
separate from that cleanup; an old run may still be the only source of a failure or replay record.

Repository cleanup is tracked in
[the engineering TODO](workstreams/repository_quality/CLEANUP_CLOSEOUT_TODOLIST.md).
Development checks do not require an evidence-pipeline refresh. Release checks belong to the
single authorized freeze after the execution surface is stable, as specified in [AGENTS.md](AGENTS.md).
