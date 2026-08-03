# Work I Task Claim

```yaml
task_id: W1-V05
title: "Implement the 5x2x3 known-policy matrix runner, immutable manifest, and resume policy"
status: ACTIVE

owner: codex
collaborators:
  - "agent:/root/w1_v05"
claimed_at_utc: 2026-08-03T06:54:12Z
lease_expires_at_utc: 2026-08-05T06:54:12Z
heartbeat_at_utc: 2026-08-03T06:56:12Z

base_commit: "1831d56f1f1ecfb83abab944f8548cd62b0dfcc6"
branch: work1/w1-v05-policy-control-matrix
worktree: ../ChemWorld-W1-V05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V05--codex.md
  - src/chemworld/eval/policy_validity_matrix.py
  - scripts/run_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_matrix_v0.1.json
  - tests/test_policy_validity_matrix.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
shared_hot_file_requests: []

deliverables:
  - Canonical world-major 5-world x 2-arm x 3-policy schedule with six lifecycles per campaign, 30 primary campaigns, 180 primary closed lifecycles, and zero provider calls.
  - Controller-driven primary and same-identity deterministic retest execution with event, state, resource, terminal, and identity provenance.
  - Content-addressed immutable per-cell bundles and a self-hashed matrix manifest bound to frozen contracts, configuration, source identity, artifact bytes, and explicit counting rules.
  - Crash-safe fail-closed resume that accepts only a validated canonical prefix, never overwrites accepted bundles, and rejects holes, corruption, unexpected files, or identity drift.
  - Outcome-blind schedule-only preflight artifact; formal qualification and execution remain owned by W1-V07 and W1-V08.
validation:
  - uv run python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --preflight
  - uv run python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --preflight --check
  - uv run pytest -q tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_known_policy_agents.py tests/test_policy_validity_matrix.py
  - uv run ruff check src/chemworld/eval/policy_validity_matrix.py scripts/run_work_i_policy_controls.py tests/test_policy_validity_matrix.py
  - uv run mypy src/chemworld/eval/policy_validity_matrix.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: ""
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T08:54:12Z
next_24h: "Implement and validate the outcome-blind runner, manifest, resume policy, and preflight without executing the formal matrix."
handoff_eta: 2026-08-03T12:54:12Z

final_commit: null
reviewer: null
review_result: null
notes: "Runner plumbing may be developed with an injected fake executor, but final integration and REVIEW require the merged W1-V04 controller surface. Retest and replay evidence never count toward the frozen 30-campaign/180-lifecycle primary estimand."
```
