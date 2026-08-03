# Repository quality task claim

```yaml
task_id: AQ-02
title: "Type-safe provider and cross-platform process guards"
status: CLAIMED
owner: "aq02-agent"
claimed_at_utc: 2026-08-03T14:14:23Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq02-platform-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ02"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-02--aq02-agent.md
  - src/chemworld/providers/wellau.py
  - src/chemworld/providers/codex_subscription.py
  - src/chemworld/agents/interactive_codex_experiment.py
  - src/chemworld/rl/training.py
deliverables:
  - "Narrow WellAU request parameters to their declared Literal types"
  - "Guard Windows-only subprocess and ctypes attributes without changing cross-platform runtime semantics"
validation:
  - "Mypy on all touched source files"
  - "Ruff on all touched source files"
  - "Relevant existing provider, interactive Codex, and RL training tests"
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
