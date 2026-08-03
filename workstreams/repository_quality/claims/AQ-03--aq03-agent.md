# Repository quality task claim

```yaml
task_id: AQ-03
title: "Type world-understanding, single-stage, predictive, and electrochemical service paths"
status: CLAIMED
owner: aq03-agent
claimed_at_utc: 2026-08-03T14:14:34Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq03-core-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ03"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-03--aq03-agent.md
  - src/chemworld/eval/world_understanding.py
  - src/chemworld/agents/electrochemical_single_stage.py
  - src/chemworld/agents/crystallization_single_stage.py
  - src/chemworld/eval/electrochemical_predictive.py
  - src/chemworld/eval/crystallization_predictive.py
  - src/chemworld/runtime/electrochemical_services.py
deliverables:
  - "Resolve current Mypy errors in the declared source files without changing runtime or scientific behavior"
validation:
  - "Mypy on all declared source files"
  - "Ruff on all declared source files"
  - "Focused tests covering the touched paths"
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
