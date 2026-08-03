# Repository quality task claim

```yaml
task_id: AQ-01
title: "Collect optional RL tests safely and fix touched-test Ruff failure"
status: CLAIMED
owner: "aq01-agent"
claimed_at_utc: 2026-08-03T14:14:09Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq01-optional-rl-tests
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ01"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-01--aq01-agent.md
  - tests/test_rl_replay_evaluation.py
  - tests/test_rl_training_accounting.py
  - tests/test_arxiv_v1_experiment_ledger.py
deliverables:
  - "Optional RL tests skip clearly at module level when their backend is unavailable"
  - "Optional RL tests retain existing coverage when the backend is installed"
  - "Ruff E501 failure in the experiment-ledger test is fixed"
validation:
  - "uv run --frozen --extra dev pytest -q tests/test_rl_replay_evaluation.py tests/test_rl_training_accounting.py tests/test_arxiv_v1_experiment_ledger.py --no-cov"
  - "uv run --frozen --extra dev pytest -q -m 'fast and current' --no-cov"
  - "uv run --frozen --extra dev ruff check tests/test_rl_replay_evaluation.py tests/test_rl_training_accounting.py tests/test_arxiv_v1_experiment_ledger.py"
  - "git diff --check"
completed: []
files_touched: []
final_commit: null
reviewer: null
review_result: null
notes: ""
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
