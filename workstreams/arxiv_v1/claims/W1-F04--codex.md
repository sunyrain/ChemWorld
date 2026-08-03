# Work I Task Claim

```yaml
task_id: W1-F04
title: "Define the expected physical and observation divergence oracle"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:42:33Z
lease_expires_at_utc: 2026-08-05T04:42:33Z
heartbeat_at_utc: 2026-08-03T04:42:33Z

base_commit: "e44e996e440248f282268ed0016be7365855eecb"
branch: work1/w1-f04-divergence-oracle
worktree: ../ChemWorld-W1-F04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F04--codex.md
  - src/chemworld/foundation/world_fork_divergence.py
  - configs/benchmark/work_i_world_fork_divergence_v0.1.json
  - tests/test_world_fork_divergence.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-divergence-v0.1.json
shared_hot_file_requests: []

deliverables:
  - A preregistered divergence oracle bound to intervention class and target component.
  - Paired physical-state and public-observation expectations at aligned checkpoints.
  - Absolute, relative, and directional tolerances with deterministic failure semantics.
validation:
  - uv run pytest -q tests/test_world_fork_divergence.py
  - uv run ruff check src/chemworld/foundation/world_fork_divergence.py tests/test_world_fork_divergence.py
  - uv run mypy src/chemworld/foundation/world_fork_divergence.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registration only; implementation has not started."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:42:33Z
next_24h: "Freeze paired checkpoint semantics and tolerance evaluation for both Work I intervention classes."
handoff_eta: 2026-08-04T04:42:33Z

final_commit: null
reviewer: null
review_result: null
notes: "F04 defines expected response evidence only; actual runtime traces and replay are F05-F06."
```
