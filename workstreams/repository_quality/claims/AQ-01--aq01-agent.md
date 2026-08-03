# Repository quality task claim

```yaml
task_id: AQ-01
title: "Collect optional RL tests safely and fix touched-test Ruff failure"
status: DONE
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
  - "Optional RL tests skip clearly at module or test scope when their backend is unavailable"
  - "Optional RL tests retain existing coverage when the backend is installed"
  - "Ruff E501 failure in the experiment-ledger test is fixed"
validation:
  - "uv run --frozen --extra dev pytest -q tests/test_rl_replay_evaluation.py tests/test_rl_training_accounting.py tests/test_arxiv_v1_experiment_ledger.py --no-cov"
  - "uv run --frozen --extra dev pytest -q -m 'fast and current' --no-cov"
  - "uv run --frozen --extra dev ruff check tests/test_rl_replay_evaluation.py tests/test_rl_training_accounting.py tests/test_arxiv_v1_experiment_ledger.py"
  - "git diff --check"
completed:
  - "Default dev focused tests: 17 passed, 4 skipped"
  - "RL-present replay tests: 9 passed with torch 2.11.0+cu130 and stable-baselines3 2.9.0"
  - "RL-present training-accounting tests: 4 passed with torch 2.11.0+cu130 and stable-baselines3 2.9.0"
  - "Ruff passed on all three touched test files"
  - "git diff --check passed"
files_touched:
  - tests/test_rl_replay_evaluation.py
  - tests/test_rl_training_accounting.py
  - tests/test_arxiv_v1_experiment_ledger.py
final_commit: "38f3edd8ec025ca40ff795a7ac1f02992d2b100c"
reviewer: "coordinator"
review_result: "PASS: integrated; default-dev and locked RL-present coverage reviewed."
notes: >-
  Ready for review at 2026-08-03T14:30:53Z. The default-dev fast/current gate now collects the RL
  tests safely. Its first unrelated failure is
  tests/test_arxiv_release_artifacts.py::test_release_manifest_records_completed_p0_gates because
  the default dev environment lacks the optional paper dependency markdown; AQ-08 owns the complete
  repository gate. Replay tests that do not need an RL backend remain active in default dev, while
  only the three policy-backend tests skip. The RL-present validation used an existing local Python
  3.12 torch installation plus stable-baselines3 2.9.0 in temporary, untracked paths.
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
