# ChemWorld development guide

ChemWorld keeps one active implementation and one active configuration surface. Git history is the
archive for superseded protocols, reports, experiments, and maintenance decisions; historical copies
do not remain in the main tree merely for replay convenience.

## Repository boundaries

- `src/chemworld/` contains the installable environment, agent interfaces, and evaluation runtime.
- `configs/current.json` identifies the active backend and mechanism-adaptation contracts.
- `configs/` contains only active protocols or templates required by a current command.
- `scripts/` contains current maintenance and experiment entry points.
- `workstreams/` contains current, compact evidence summaries—not raw campaigns or version history.
- `runs/`, `site/`, caches, credentials, and provider responses are local artifacts and remain ignored.

The environment provides physical-chemistry worlds, interventions, observations, budgets, scoring,
and replay. Evaluation campaigns may update an Agent's context, memory, and actions, but ChemWorld
does not retrain hosted models or modify their weights.

## Change workflow

1. Resolve active paths from `configs/current.json`; do not select files by largest version suffix.
2. Remove superseded code and configuration in the same change that migrates its remaining callers.
3. Add or update focused tests for the affected contracts. Avoid a full test run unless the change
   genuinely spans the whole repository.
4. Run Ruff on changed Python files, `mypy src/chemworld`, the focused tests, and wheel smoke when
   packaging or resource lookup changes.
5. Keep raw runs outside Git. Commit only a compact result when it is required to support a current
   repository statement.
6. Check `git status --short` before committing; never add `api.md`, `.env`, private seeds, or raw
   provider responses.

For selective validation, use the centrally assigned pytest taxonomy, for example
`pytest -m "fast and current"`, `pytest -m rl`, or `pytest -m reference`. Compatibility-boundary
tests use `history`; integration, notebook, wheel, and exhaustive audit tests use `slow`.

Generated evidence must distinguish environment validation from Agent performance. A passing backend
check does not imply a method result, benchmark ranking, or publication claim.
