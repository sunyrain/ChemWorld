# Work I Task Claim

```yaml
task_id: W1-F04
title: "Define the expected physical and observation divergence oracle"
status: REVIEW

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:42:33Z
lease_expires_at_utc: 2026-08-05T04:42:33Z
heartbeat_at_utc: 2026-08-03T04:48:37Z

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

completed_since_last_heartbeat:
  - Defined content-addressed divergence oracles for both Work I intervention classes.
  - Required paired physical-state and public-observation expectations at aligned checkpoints.
  - Implemented absolute, relative, and directional tolerance evaluation with deterministic failures.
  - Added frozen definition fixtures, reports, and missing/nonfinite/wrong-direction tests.
current_validation: "9/9 focused tests passed; 96/96 combined fork and mechanism regression tests passed; ruff, mypy, format check, and git diff check passed."
files_touched:
  - src/chemworld/foundation/world_fork_divergence.py
  - configs/benchmark/work_i_world_fork_divergence_v0.1.json
  - tests/test_world_fork_divergence.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-divergence-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:48:37Z
next_24h: "Coordinator review and merge; F05 can then feed actual aligned runtime checkpoints into the frozen oracle."
handoff_eta: 2026-08-03T05:48:37Z

final_commit: "e1951a26ee31566aab4d3da8ee138508bafd1cee"
reviewer: coordinator
review_result: pending
notes: "F04 defines expected response evidence only; actual runtime traces and replay are F05-F06."
```
