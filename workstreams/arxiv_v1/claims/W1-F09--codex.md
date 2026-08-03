# Work I Task Claim

```yaml
task_id: W1-F09
title: "Audit the publication display scope for tasks, operations, instruments, and endpoints"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:20:41Z
lease_expires_at_utc: 2026-08-05T05:20:41Z
heartbeat_at_utc: 2026-08-03T05:24:30Z

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

completed_since_last_heartbeat:
  - "Recomputed 15 task contracts, 28 operation kinds, five instruments, and 62 task-metric bindings from live registries."
  - "Bound live counts to the 415-case frozen task-design matrix and verified all endpoints executable."
  - "Separated the 62 task-specific bindings from the 43 unique metric identifiers and froze approved publication wording."
current_validation: "Deterministic JSON/Markdown rebuild, two focused tests, ruff, and git diff --check passed."
files_touched:
  - scripts/audit_work_i_platform_surface.py
  - tests/test_work_i_platform_surface.py
  - workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:20:41Z
next_24h: "Coordinator rebuild and merge, then F10 semantic qualification."
handoff_eta: 2026-08-03T05:35:00Z

final_commit: "96f35a70888cce2b24a26b8f8f2434b403be3463"
reviewer: coordinator
review_result: "accepted after independent live-registry and frozen-matrix reconstruction"
notes: "Audit SHA-256: 941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77. Registered platform scope is explicitly distinguished from empirical agent coverage."
```
