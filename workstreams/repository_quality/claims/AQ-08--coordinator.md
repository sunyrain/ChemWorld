# Repository quality task claim

```yaml
task_id: AQ-08
title: "Integrate claimed fixes and verify all repository quality gates"
status: CLAIMED
owner: coordinator
claimed_at_utc: 2026-08-03T14:44:01Z
base_commit: "183fd22415ed5067bbb6911708a8c0403a9f871b"
branch: agent/restore-main-quality-gates
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-08--coordinator.md
  - workstreams/repository_quality/MAIN_QUALITY_TODOLIST.md
  - configs/current.json
  - workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json
  - workstreams/world_foundation/reports/wf-110-runtime-integration.json
  - workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-public-matrix.json
  - workstreams/world_foundation/reports/public-boundary-security-vnext.json
  - workstreams/world_foundation/reports/runtime-reachability-vnext.json
  - workstreams/world_foundation/reports/state-transition-invariants.json
  - workstreams/world_foundation/reports/maturity-truth-vnext.json
  - workstreams/world_foundation/reports/backend-v0.5.json
  - workstreams/flagship_tasks/reports/task-design-matrix-v1.json
  - workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-preflight.json
deliverables:
  - "Reviewed integration of AQ-01 through AQ-07 and AQ-09"
  - "Truthfully refreshed generated current-evidence nodes after executable-source changes"
  - "Complete default-dev and optional-backend quality-gate evidence"
validation:
  - "uv run --frozen --extra dev python scripts/evidence_pipeline.py --refresh"
  - "uv run --frozen --extra dev python scripts/evidence_pipeline.py --check"
  - "uv run --frozen --extra dev pytest -m 'fast and current'"
  - "uv run --frozen --extra dev pytest"
  - "uv run --frozen --extra dev ruff check src tests scripts"
  - "uv run --frozen --extra dev mypy src/chemworld"
  - "uv run --frozen --extra dev python scripts/audit_public_docs.py"
  - "git diff --check"
completed:
  - "Integrated all worker claim, implementation, review-correction, and handoff commits"
  - "Mypy passes on 324 source files"
  - "Ruff, public-doc audit, and diff check pass before evidence refresh"
files_touched:
  - workstreams/repository_quality/claims/AQ-08--coordinator.md
final_commit: null
reviewer: null
review_result: null
notes: "The refresh is limited to generated DAG nodes; immutable evidence remains read-only. AQ-08 does not authorize new scientific results or stronger claims."
```
