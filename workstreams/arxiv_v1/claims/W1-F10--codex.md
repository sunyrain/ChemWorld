# Work I Task Claim

```yaml
task_id: W1-F10
title: "Qualify transaction, resource, failure, and instrument semantics"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:26:00Z
lease_expires_at_utc: 2026-08-05T05:26:00Z
heartbeat_at_utc: 2026-08-03T05:26:00Z

base_commit: "e36293e7964a09b1129a49fca00f7ed3d580acb4"
branch: work1/w1-f10-semantic-qualification
worktree: ../ChemWorld-W1-F10
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F10--codex.md
  - scripts/qualify_work_i_experiment_semantics.py
  - tests/test_work_i_experiment_semantics.py
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.md
  - src/chemworld/foundation/world_fork_runtime.py
  - tests/test_world_fork_runtime.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md
  - workstreams/arxiv_v1/claims/W1-F05--codex.md
  - workstreams/arxiv_v1/claims/W1-F06--codex.md
  - workstreams/arxiv_v1/claims/W1-F07--codex.md
shared_hot_file_requests:
  - "Correct the F05 reconstructed public failure-contract status vocabulary and deterministically reissue its F06/F07 derived artifacts."

deliverables:
  - Per-operation transaction, precondition, failure, and runtime-route qualification table.
  - Per-instrument cost, latency, sample consumption, destructiveness, and terminal-state table.
  - Campaign resource hard-limit and replay semantics summary bound to executable probes.
validation:
  - uv run python scripts/qualify_work_i_experiment_semantics.py
  - uv run python scripts/qualify_work_i_experiment_semantics.py --check
  - uv run pytest -q tests/test_work_i_experiment_semantics.py
  - uv run ruff check scripts/qualify_work_i_experiment_semantics.py tests/test_work_i_experiment_semantics.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registered; semantic probes have not run."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:26:00Z
next_24h: "Bind declared semantics to runtime routes and executable commit/reject probes, then freeze the table."
handoff_eta: 2026-08-03T07:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The table must distinguish declared contracts from behavior exercised by an executable probe. Initial read-only probing found the F05 reconstructed failure-status vocabulary omitted validation_failed, rolled_back, and campaign_resource_rejected; coordinator reserved the affected derived artifacts for correction in this task."
```
