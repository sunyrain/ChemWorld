# Work I Task Claim

```yaml
task_id: W1-V04
title: "Implement deterministic known-policy controllers"
status: REVIEW

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:45:52Z
lease_expires_at_utc: 2026-08-05T06:45:52Z
heartbeat_at_utc: 2026-08-03T07:00:19Z

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

completed_since_last_heartbeat:
  - "Implemented all three frozen policies as primitive-operation state machines over the six-card V02 schedule."
  - "Hard-bound construction to the exact V02 contract, V03 qualification report, V03 threshold binding, and current qualification source manifest."
  - "Made material information structurally unreadable by retaining only a narrow task-interface view; only measure_then_threshold reads public conversion after UV-vis."
  - "Added fail-closed transaction handling, structured per-decision audits, and threshold branch traces."
  - "Closed 6/6 lifecycles for every policy on nonformal smoke world 20000 with all operations committed and zero provider calls."
current_validation: "Python 3.12: 9/9 focused and environment-integration tests pass. Python 3.11: 6/6 non-environment focused tests pass. Ruff, mypy, and git diff check pass."
files_touched:
  - src/chemworld/agents/known_policy.py
  - tests/test_known_policy_agents.py
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T08:45:52Z
next_24h: "Coordinator integration review, then release the controllers to V05/V06."
handoff_eta: 2026-08-03T07:00:19Z

final_commit: "49dc6b75e8922df139b7557e9e1c389df68657d1"
reviewer: null
review_result: null
notes: "V04 implements frozen contracts only; formal execution belongs to V08."
```
