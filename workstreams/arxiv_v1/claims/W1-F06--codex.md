# Work I Task Claim

```yaml
task_id: W1-F06
title: "Execute and freeze the 24-trace world-fork qualification matrix"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:12:38Z
lease_expires_at_utc: 2026-08-05T05:12:38Z
heartbeat_at_utc: 2026-08-03T05:12:38Z

base_commit: "854e97931a2a7ce3d0dd03868513b07c96b77671"
branch: work1/w1-f06-world-fork-qualification
worktree: ../ChemWorld-W1-F06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F06--codex.md
  - workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
shared_hot_file_requests: []

deliverables:
  - Frozen 2 intervention classes x 3 seeds x 2 world variants x original/replay matrix.
  - Immutable report hash, trace count, provider-call count, and all-gate aggregate.
validation:
  - uv run python scripts/run_work_i_world_fork.py --seeds all --output workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
  - uv run python scripts/run_work_i_world_fork.py --seeds all --output workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json --check
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "F05 runtime and protocol accepted; formal outcome remains unread."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:12:38Z
next_24h: "Execute the frozen matrix exactly once, rebuild independently, and hand off the immutable artifact."
handoff_eta: 2026-08-03T06:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "No protocol, world, seed, threshold, oracle, or main-figure rule may change after this claim."
```
