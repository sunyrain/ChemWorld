# Work I Task Claim

```yaml
task_id: W1-M05
title: "Establish the Work I integration staging and hot-file queue"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T01:45:27Z
lease_expires_at_utc: 2026-08-06T01:45:27Z
heartbeat_at_utc: 2026-08-04T02:00:21Z

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

completed_since_last_heartbeat:
  - "Froze the 14-task remaining-work snapshot against main commit 9e93316b, including explicit source and nullable handoff-head bindings."
  - "Recorded the single-agent execution order, task dependencies, four hot-file reservation classes, and prompt-push policy."
  - "Preserved D02 as owner-deferred and D06/D09 as external release blockers without reopening completed science."
  - "Added a provider-free validator and three focused fail-closed tests."
current_validation: "PASS: queue audit reports 14/14 remaining tasks, one active entry, and four reservation classes; focused tests 3 passed; Ruff passed; Mypy passed; git diff --check passed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-M05--codex-1.md
  - workstreams/arxiv_v1/integration/README.md
  - workstreams/arxiv_v1/integration/work-i-integration-queue-v0.1.json
  - scripts/audit_work_i_integration_queue.py
  - tests/test_work_i_integration_queue.py
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator acceptance, then advance the single active queue entry to W1-S03."
handoff_eta: 2026-08-04T02:00:21Z

final_commit: "f4605c0210b281714f98d1b5d7e3fb6dbb6725b7"
reviewer: "codex-1 coordinator"
review_result: "PASS"
notes: "The project owner explicitly reassigned all remaining first-paper work to codex-1. The original claim is retained unchanged as history. The queue is a staging snapshot; each later task still requires its own committed claim before substantive writes."
```
