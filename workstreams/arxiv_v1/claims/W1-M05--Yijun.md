# Work I Task Claim

```yaml
task_id: W1-M05
title: "Establish the Work I integration staging and hot-file queue"
status: ACTIVE

owner: Yijun
collaborators: []
claimed_at_utc: 2026-08-03T16:32:50Z
lease_expires_at_utc: 2026-08-05T16:37:50Z
heartbeat_at_utc: 2026-08-03T16:37:50Z

base_commit: "628478aa3f01023c249f08fddb8a35ecd6429803"
branch: work1/w1-m05-integration-queue-yijun
worktree: ../ChemWorld-W1-M05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-M05--Yijun.md
  - workstreams/arxiv_v1/integration/README.md
  - workstreams/arxiv_v1/integration/work-i-integration-queue-v0.1.json
  - scripts/audit_work_i_integration_queue.py
  - tests/test_work_i_integration_queue.py
shared_hot_file_requests: []

deliverables:
  - "Versioned machine-readable staging queue for claimed, active, review, blocked, and integration-ready Work I branches, with source commit and immutable handoff-head bindings"
  - "Explicit shared hot-file catalog, reservation ownership/lease rules, conflict detection, dependency ordering, independent-review gates, and coordinator-only merge/update protocol"
  - "Provider-free deterministic validator and focused tests that fail closed on undeclared tasks, duplicate ownership, write-set collisions, stale handoff identities, invalid transitions, or unauthorized hot-file use"
validation:
  - "Cross-check the queue snapshot against WORK_I_TODOLIST, every claim on the source commit, and fetched origin/work1 branch heads"
  - "Run the task-local validator in --check mode and its focused pytest suite"
  - "Run Ruff and Mypy on task-local Python files"
  - "Confirm no shared hot file, TODO, manuscript, global evidence, ledger, figure, release, or existing claim is modified"
  - "git diff --check"

completed_since_last_heartbeat:
  - "Verified that the W1-M05 claim is present on origin/main at b9755201cb860aca4718b8887ee25d567c71f5d0"
  - "Fast-forwarded the isolated branch to current origin/main and pushed it before implementation"
current_validation: "Enumerating source-commit claims, fetched work1 heads, review gates, dependencies, and coordinator-only hot-file constraints for a fail-closed snapshot"
files_touched:
  - workstreams/arxiv_v1/claims/W1-M05--Yijun.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T04:37:50Z
next_24h: "Build and validate the isolated staging/hot-file queue, then hand it to the coordinator without changing coordinator-owned state."
handoff_eta: 2026-08-04T00:32:50Z

final_commit: null
reviewer: null
review_result: null
notes: "M05 defines integration control infrastructure only. It does not merge review branches, edit the master TODO, grant reservations, or mutate manuscript/evidence/release hot files."
```
