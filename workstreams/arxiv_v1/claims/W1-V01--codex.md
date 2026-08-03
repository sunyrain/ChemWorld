# Work I Task Claim

```yaml
task_id: W1-V01
title: "Freeze the experimental-agency construct and profile schema"
status: REVIEW

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:25:00Z
lease_expires_at_utc: 2026-08-05T06:25:00Z
heartbeat_at_utc: 2026-08-03T06:45:00Z

base_commit: "cd35fffbd907b0ddd57acc45ee296c3f1af91798"
branch: work1/w1-v01-profile-contract
worktree: ../ChemWorld-W1-V01
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V01--codex.md
  - src/chemworld/eval/policy_validity_contract.py
  - scripts/freeze_work_i_policy_profile.py
  - configs/benchmark/work_i_policy_profile_contract_v0.1.json
  - tests/test_policy_validity_contract.py
  - workstreams/arxiv_v1/reports/work-i-policy-profile-contract-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Operational definition and explicit non-claims for experimental agency.
  - Versioned multidimensional profile schema with denominators, null rules, invariants, and aggregation units.
  - Deterministic machine/human contract artifacts and executable validation tests.
validation:
  - uv run python scripts/freeze_work_i_policy_profile.py
  - uv run python scripts/freeze_work_i_policy_profile.py --check
  - uv run pytest -q tests/test_policy_validity_contract.py
  - uv run ruff check src/chemworld/eval/policy_validity_contract.py scripts/freeze_work_i_policy_profile.py tests/test_policy_validity_contract.py
  - uv run mypy src/chemworld/eval/policy_validity_contract.py
  - git diff --check

completed_since_last_heartbeat:
  - "Defined experimental agency as a multidimensional observable policy construct rather than a scalar intelligence or endpoint score."
  - "Frozen five construct axes, 19 construct metrics, two separate endpoint-context metrics, exact denominators, null rules, invariants, and campaign-level aggregation."
  - "Bound the trajectory axis to the existing G2 discovery, retention, drawdown, recovery, and terminal-retention definitions."
  - "Implemented a defensive profile-record validator and deterministic machine/human contract renderer."
current_validation: "Deterministic artifact rebuild, five contract tests, ruff, mypy, and git diff --check passed."
files_touched:
  - src/chemworld/eval/policy_validity_contract.py
  - scripts/freeze_work_i_policy_profile.py
  - configs/benchmark/work_i_policy_profile_contract_v0.1.json
  - tests/test_policy_validity_contract.py
  - workstreams/arxiv_v1/reports/work-i-policy-profile-contract-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T18:25:00Z
next_24h: "Coordinator review, independent deterministic rebuild on main, and merge; V02 can then bind preregistered policy orderings to this contract hash."
handoff_eta: 2026-08-03T07:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Frozen contract SHA-256: 01e3cb3ff5c7b2455fd998fb5eebdd1932931c6fef2d5125632b103d79a34262. The contract is intentionally multidimensional and outcome-independent: it does not introduce a composite intelligence score or encode endpoint quality as experimental agency."
```
