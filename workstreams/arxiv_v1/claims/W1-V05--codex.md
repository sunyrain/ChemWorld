# Work I Task Claim

```yaml
task_id: W1-V05
title: "Implement the 5x2x3 known-policy matrix runner, immutable manifest, and resume policy"
status: DONE

owner: codex
collaborators:
  - "agent:/root/w1_v05"
claimed_at_utc: 2026-08-03T06:54:12Z
lease_expires_at_utc: 2026-08-05T06:54:12Z
heartbeat_at_utc: 2026-08-03T07:46:53Z

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
  - git diff --check 1831d56f1f1ecfb83abab944f8548cd62b0dfcc6...HEAD

completed_since_last_heartbeat:
  - "Implemented the canonical world-major 5 x 2 x 3 schedule with exactly 30 primary campaigns and 180 primary closed lifecycles."
  - "Integrated the frozen V04 controllers for primary and same-identity deterministic retest execution with complete event, state, resource, terminal, profile, endpoint, and decision-audit evidence."
  - "Added content-addressed immutable cell bundles, a self-hashed terminal manifest, and fail-closed canonical-prefix resume with atomic publication and exact-next orphan adoption."
  - "Recorded an outcome-blind preflight bound to the merged V01-V04 contracts and source identities; no formal outcome was read and no provider call or formal execution occurred."
  - "Addressed review by requiring an explicit self-hashed W1-V07 receipt with true runner-qualified/protocol-frozen gates and current matrix-protocol, source-manifest, preflight, and controller bindings before any formal executor call."
  - "Removed the test-file EOF blank line and added an explicit base-commit-to-HEAD whitespace validation command."
current_validation: "Coordinator rerun on main passed deterministic preflight generation and exact --check (formal_result=false; SHA-256 58dc11556051faf44e495b6709dc91f5d04e47ca96399ccf7f65bed6660afdb0), all 46 related tests, ruff, mypy, working-tree diff check, and base-to-HEAD whitespace validation."
files_touched:
  - src/chemworld/eval/policy_validity_matrix.py
  - scripts/run_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_matrix_v0.1.json
  - tests/test_policy_validity_matrix.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
  - workstreams/arxiv_v1/claims/W1-V05--codex.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T08:54:12Z
next_24h: "Coordinator review and integration; formal qualification/execution remain with W1-V07/W1-V08."
handoff_eta: 2026-08-03T07:39:53Z

final_commit: "8b15b31f1d29678f614bfbf8f2bd223a63be41c5"
reviewer: "codex-1"
review_result: "APPROVED after changes: exact preflight reconstruction and 46 tests pass; formal execution fails closed before executor invocation unless a self-hashed W1-V07 qualification/freeze receipt matches the current protocol, source, preflight, and controller bindings."
notes: "Merged W1-V04 controller surface is bound in the preflight. Formal execution requires explicit opt-in plus a valid W1-V07 qualification receipt and was not invoked. Retest and replay evidence never count toward the frozen 30-campaign/180-lifecycle primary estimand."
```
