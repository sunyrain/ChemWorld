# Work I Task Claim

```yaml
task_id: W1-M05
title: "Establish the Work I integration staging and hot-file queue"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T01:45:27Z
lease_expires_at_utc: 2026-08-06T01:45:27Z
heartbeat_at_utc: 2026-08-04T01:45:27Z

base_commit: "178c6357317867c2b278343368649b85c7206571"
branch: work1/w1-m05-integration-queue-codex-1
worktree: ../ChemWorld-W1-M05-C1
supersedes: "workstreams/arxiv_v1/claims/W1-M05--Yijun.md"

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-M05--codex-1.md
  - workstreams/arxiv_v1/integration/README.md
  - workstreams/arxiv_v1/integration/work-i-integration-queue-v0.1.json
  - scripts/audit_work_i_integration_queue.py
  - tests/test_work_i_integration_queue.py
shared_hot_file_requests: []

deliverables:
  - "Versioned machine-readable staging queue for all remaining Work I branches with source and handoff-head bindings"
  - "Explicit hot-file, dependency, conflict, reservation, review, and coordinator-only integration rules"
  - "Provider-free deterministic validator and focused tests"
validation:
  - "Validate the queue against the current Work I TODO, claims, and fetched origin/work1 heads"
  - "Run the task-local validator, focused tests, Ruff, Mypy, and git diff --check once"

completed_since_last_heartbeat: []
current_validation: "Coordinator-authorized takeover registered after the original branch produced no substantive files by its handoff ETA."
files_touched:
  - workstreams/arxiv_v1/claims/W1-M05--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T02:15:27Z
next_24h: "Build, validate, merge, and coordinator-accept the integration queue."
handoff_eta: 2026-08-04T02:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The project owner explicitly reassigned all remaining first-paper work to codex-1. The original claim is retained unchanged as history."
```
