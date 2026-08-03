# Work I Task Claim

```yaml
task_id: W1-V04
title: "Implement deterministic known-policy controllers"
status: ACTIVE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:45:52Z
lease_expires_at_utc: 2026-08-05T06:45:52Z
heartbeat_at_utc: 2026-08-03T06:52:02Z

base_commit: "e0ad2cbceef68e7eb764c7d0b88894d4bb09f63b"
branch: work1/w1-v04-known-policy-controllers
worktree: ../ChemWorld-W1-V04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V04--codex.md
  - src/chemworld/agents/known_policy.py
  - tests/test_known_policy_agents.py
shared_hot_file_requests: []

deliverables:
  - Deterministic implementations of assay_all, start_then_discard, and measure_then_threshold.
  - Fail-closed policy construction bound to the frozen V02 contract and V03 threshold binding.
  - Decision-audit metadata proving observation and material-information access boundaries.
  - Focused unit and environment-integration tests for all terminal branches.
validation:
  - uv run pytest -q tests/test_known_policy_agents.py
  - uv run ruff check src/chemworld/agents/known_policy.py tests/test_known_policy_agents.py
  - uv run mypy src/chemworld/agents/known_policy.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: ""
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T08:45:52Z
next_24h: "Implement and validate all three frozen controllers without consuming formal-world outcomes."
handoff_eta: 2026-08-03T09:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "V04 implements frozen contracts only; formal execution belongs to V08."
```
