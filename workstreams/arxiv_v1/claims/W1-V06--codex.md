# Work I Task Claim

```yaml
task_id: W1-V06
title: "Implement construct-validity, resource, and exact-replay audit"
status: CLAIMED

owner: codex
collaborators:
  - "agent:/root/w1_v06"
claimed_at_utc: 2026-08-03T06:54:12Z
lease_expires_at_utc: 2026-08-05T06:54:12Z
heartbeat_at_utc: 2026-08-03T06:54:12Z

base_commit: "1831d56f1f1ecfb83abab944f8548cd62b0dfcc6"
branch: work1/w1-v06-policy-validity-audit
worktree: ../ChemWorld-W1-V06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V06--codex.md
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/audit_work_i_policy_validity.py
  - tests/test_policy_validity_audit.py
shared_hot_file_requests: []

deliverables:
  - Fail-closed audit library that independently rebuilds the frozen profile and verifies construct-validity identities, partial orderings, conditional null rules, and the threshold non-degeneracy gate.
  - Exact campaign resource reconciliation and zero-provider verification from immutable matrix records.
  - Event, state, resource, terminal, profile, and endpoint exact-replay and same-identity test-retest verification.
  - Matched-arm identity/action invariance checks that preserve the boundary between interface validation and a material-information null claim.
  - Deterministic, source-bound audit receipt and read-only CLI suitable for V07 qualification and V09 reporting without freezing a protocol or consuming formal outcomes during this task.
validation:
  - uv run pytest -q tests/test_policy_validity_audit.py
  - uv run pytest -q tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_campaign_resources.py tests/test_policy_validity_audit.py
  - uv run ruff check src/chemworld/eval/policy_validity_audit.py scripts/audit_work_i_policy_validity.py tests/test_policy_validity_audit.py
  - uv run mypy src/chemworld/eval/policy_validity_audit.py scripts/audit_work_i_policy_validity.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: ""
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T08:54:12Z
next_24h: "Implement and validate audit gates against synthetic immutable records without reading formal outcomes."
handoff_eta: 2026-08-03T12:54:12Z

final_commit: null
reviewer: null
review_result: null
notes: "W1-V06 owns audit mechanics only. W1-V07 owns runner qualification and protocol freeze; W1-V09 owns the formal profile-recovery report."
```
