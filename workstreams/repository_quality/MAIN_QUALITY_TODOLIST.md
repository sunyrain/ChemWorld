# Main quality-gate audit and TODO

Last updated: 2026-08-03

Status: `ACTIVE / CLAIM-DRIVEN`

This audit is limited to reproducible repository quality gates on `main`. It does not change frozen
Work I/II protocols, evidence, reports, or scientific claims.

## Evaluation

ChemWorld is already a substantial research-software system rather than a small prototype. It has a
clear package boundary, a locked Python 3.11/3.12 environment, extensive tests, typed agent and
evaluation interfaces, replay/evidence tooling, bilingual documentation, and explicit scientific
claim boundaries. The public documentation audit passes all checks across 64 files.

The current checkout nevertheless fails three development gates promised by `DEVELOPMENT.md`:

- `pytest -m "fast and current"` stops during collection because two RL test modules import optional
  `torch`/`stable_baselines3` dependencies in the default `dev` environment;
- the complete default-dev suite also assumes the optional `paper` Markdown backend is installed in
  one release-finalizer preflight assertion;
- Ruff reports one overlong assertion;
- Mypy reports 45 errors across 20 source files, including platform guards, mutable value schemas,
  NumPy shapes, mapping variance, optional values, and narrowed collection types.

The immediate goal is to restore these gates without changing runtime behavior, dependency policy,
frozen evidence, or benchmark semantics.

## Claim workflow

1. A worker creates `claims/<TASK-ID>--<owner>.md` from `claims/TEMPLATE.md` on its task branch.
2. The claim is committed before substantive implementation work.
3. The worker stays inside the declared write set, runs task-local validation, and changes its claim
   status to `REVIEW` with the final commit and evidence.
4. The coordinator reviews and integrates the branch, reruns repository-level gates, then changes the
   task and claim to `DONE`.

## Task matrix

| ID | Status | Scope | Validation |
| --- | --- | --- | --- |
| AQ-01 | OPEN | Make optional RL tests collect safely in default `dev`; fix the Ruff failure | focused pytest; Ruff on touched tests |
| AQ-02 | OPEN | Type-safe provider and cross-platform process guards | focused tests; Ruff; Mypy on touched files |
| AQ-03 | OPEN | Type world-understanding, single-stage, predictive, and electrochemical service paths | focused tests; Ruff; Mypy on touched files |
| AQ-04 | OPEN | Type live-LLM and static-optimization agent paths | focused tests; Ruff; Mypy on touched files |
| AQ-05 | OPEN | Type static campaign, baseline, and material-information evaluators | focused tests; Ruff; Mypy on touched files |
| AQ-06 | OPEN | Type replication audit, arXiv derived data, and participant qualification | focused tests; Ruff; Mypy on touched files |
| AQ-07 | OPEN | Type mechanism-adaptation execution | focused tests; Ruff; Mypy on touched files |
| AQ-08 | OPEN | Coordinator integration and full quality-gate verification | default-dev tests; Ruff; Mypy; docs audit; diff check |
| AQ-09 | OPEN | Make the release-finalizer test honor the optional `paper` dependency contract | focused/default-dev pytest; Ruff on touched tests |

## Completion criteria

- `uv run --frozen --extra dev pytest -m "fast and current"` collects without RL extras and passes;
- the relevant complete default-dev test suite passes, with optional RL tests skipped only when their
  declared backend is absent;
- `uv run --frozen --extra dev ruff check src tests scripts` passes;
- `uv run --frozen --extra dev mypy src/chemworld` passes;
- `uv run --frozen --extra dev python scripts/audit_public_docs.py` still passes;
- `git diff --check` passes;
- no frozen protocol, result, evidence identity, or public scientific claim changes.
