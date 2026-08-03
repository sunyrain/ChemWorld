# Work I Task Claim

```yaml
task_id: W1-F09
title: "Audit the publication display scope for tasks, operations, instruments, and endpoints"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:20:41Z
lease_expires_at_utc: 2026-08-05T05:20:41Z
heartbeat_at_utc: 2026-08-03T05:20:41Z

base_commit: "1ea2c3102f48ec47b269ef06be174a1c66338001"
branch: work1/w1-f09-platform-surface-audit
worktree: ../ChemWorld-W1-F09
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F09--codex.md
  - scripts/audit_work_i_platform_surface.py
  - tests/test_work_i_platform_surface.py
  - workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Exact enumerations and counting rules behind the 15/28/5/62 display claim.
  - Cross-binding to live registries, evaluator endpoint contracts, and the frozen task-design matrix.
  - Human wording that distinguishes registered surface, executable reachability, and empirical coverage.
validation:
  - uv run python scripts/audit_work_i_platform_surface.py
  - uv run python scripts/audit_work_i_platform_surface.py --check
  - uv run pytest -q tests/test_work_i_platform_surface.py
  - uv run ruff check scripts/audit_work_i_platform_surface.py tests/test_work_i_platform_surface.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registered; source bindings have not yet been evaluated."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:20:41Z
next_24h: "Recompute each display count from live source objects and freeze the exact wording boundary."
handoff_eta: 2026-08-03T06:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Registered platform scope must not be described as complete empirical coverage of all tasks."
```
