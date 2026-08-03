# Work I Task Claim

```yaml
task_id: W1-F05
title: "Implement the world-fork builder, deterministic runner, and integrated audit"
status: REVIEW

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:50:02Z
lease_expires_at_utc: 2026-08-05T04:50:02Z
heartbeat_at_utc: 2026-08-03T05:04:19Z

base_commit: "fb36f7bfe71c6351c4e15956364aaffea278c39b"
branch: work1/w1-f05-world-fork-runtime
worktree: ../ChemWorld-W1-F05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F05--codex.md
  - src/chemworld/foundation/world_fork_runtime.py
  - src/chemworld/eval/world_fork_audit.py
  - scripts/run_work_i_world_fork.py
  - configs/benchmark/work_i_world_fork_qualification_v0.1.json
  - tests/test_world_fork_runtime.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json
shared_hot_file_requests: []

deliverables:
  - Runtime extraction of all F01 component payloads from real ScenarioInstance and task contracts.
  - Deterministic base/fork execution of an identical typed action sequence with aligned checkpoints.
  - Integrated lineage, public-contract, divergence, executability, and exact-replay audit.
validation:
  - uv run pytest -q tests/test_world_fork_runtime.py
  - uv run ruff check src/chemworld/foundation/world_fork_runtime.py src/chemworld/eval/world_fork_audit.py scripts/run_work_i_world_fork.py tests/test_world_fork_runtime.py
  - uv run mypy src/chemworld/foundation/world_fork_runtime.py src/chemworld/eval/world_fork_audit.py
  - git diff --check

completed_since_last_heartbeat:
  - "Bound all 15 non-identity F01 components to live ChemWorld runtime payloads."
  - "Implemented identical typed-action execution on parent and child worlds with aligned terminal checkpoints."
  - "Integrated lineage, nine-component public invariance, divergence, execution, replay, and zero-provider-call gates."
  - "Generated a passing two-case seed-0 deterministic preflight report."
current_validation: "40 focused F01-F05 tests passed; ruff, mypy, deterministic report rebuild, and git diff --check passed."
files_touched:
  - src/chemworld/foundation/world_fork_runtime.py
  - src/chemworld/eval/world_fork_audit.py
  - scripts/run_work_i_world_fork.py
  - configs/benchmark/work_i_world_fork_qualification_v0.1.json
  - tests/test_world_fork_runtime.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:50:02Z
next_24h: "Coordinator review and merge; then execute the frozen 24-trace F06 matrix without protocol changes."
handoff_eta: 2026-08-03T05:15:00Z

final_commit: null
reviewer: coordinator
review_result: "pending"
notes: "F05 preflight covers one seed for each frozen intervention class (8 traces including exact replays). The full 24-trace evidence matrix remains W1-F06."
```
