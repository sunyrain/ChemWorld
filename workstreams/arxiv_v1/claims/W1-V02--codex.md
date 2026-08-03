# Work I Task Claim

```yaml
task_id: W1-V02
title: "Freeze three known policies and their expected agency-profile signatures"
status: ACTIVE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:04:22Z
lease_expires_at_utc: 2026-08-05T06:04:22Z
heartbeat_at_utc: 2026-08-03T06:04:22Z

base_commit: "7d41964cd1025c2831b35c172164a0156d3c51fe"
branch: work1/w1-v02-known-policy-contract
worktree: ../ChemWorld-W1-V02
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V02--codex.md
  - src/chemworld/eval/known_policy_contract.py
  - scripts/freeze_work_i_known_policies.py
  - configs/benchmark/work_i_known_policy_contract_v0.1.json
  - tests/test_known_policy_contract.py
  - workstreams/arxiv_v1/reports/work-i-known-policy-contract-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Three deterministic known-policy definitions sharing one six-probe physical schedule.
  - Preregistered profile signatures, exact identities, partial orderings, and explicit non-orderings.
  - Threshold-policy decision interface reserved for independent qualification worlds in W1-V03.
  - Deterministic machine/human contract artifacts and executable validation tests.
validation:
  - uv run python scripts/freeze_work_i_known_policies.py
  - uv run python scripts/freeze_work_i_known_policies.py --check
  - uv run pytest -q tests/test_known_policy_contract.py
  - uv run ruff check src/chemworld/eval/known_policy_contract.py scripts/freeze_work_i_known_policies.py tests/test_known_policy_contract.py
  - uv run mypy src/chemworld/eval/known_policy_contract.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Policy grammar, shared six-probe schedule, and outcome-independent expected signatures are being encoded."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T18:04:22Z
next_24h: "Freeze the policy action grammar and expected measurement signatures, then hand off V02 for independent rebuild and review."
handoff_eta: 2026-08-03T08:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "These policies are construct-validity positive controls, not endpoint-performance baselines. The threshold value itself is intentionally absent from V02 and must be frozen from disjoint qualification worlds in W1-V03."
```
