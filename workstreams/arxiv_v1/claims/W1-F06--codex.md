# Work I Task Claim

```yaml
task_id: W1-F06
title: "Execute and freeze the 24-trace world-fork qualification matrix"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:12:38Z
lease_expires_at_utc: 2026-08-05T05:12:38Z
heartbeat_at_utc: 2026-08-03T05:14:36Z

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

completed_since_last_heartbeat:
  - "Executed all six frozen parent-child pairs and their exact replays."
  - "Observed 24/24 deterministic traces, six passes for every audit gate, and zero provider calls."
  - "Rebuilt the complete 2.54 MB report byte-for-byte from the frozen protocol."
current_validation: "Formal rebuild, counting assertions, report hash, and git diff --check passed."
files_touched:
  - workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:12:38Z
next_24h: "Coordinator cross-runtime reconstruction and merge, followed by F07 report synthesis."
handoff_eta: 2026-08-03T05:25:00Z

final_commit: "06ea21a85224df8f48f214226a04b6118ecb2adb"
reviewer: coordinator
review_result: "accepted after independent Python 3.12 reconstruction matched the frozen Python 3.11 artifact"
notes: "Frozen report SHA-256: 97867c1c1bbadc2b00832c9609e920ed71656d04ed8ba3c193bd353ae1336bba. No protocol, world, seed, threshold, oracle, or main-figure rule changed after claim."
```
