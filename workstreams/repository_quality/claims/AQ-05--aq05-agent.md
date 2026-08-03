# Repository quality task claim

```yaml
task_id: AQ-05
title: "Type static campaign, baseline, and material-information evaluators"
status: CLAIMED
owner: aq05-agent
claimed_at_utc: 2026-08-03T14:14:47Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq05-static-eval-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ05"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-05--aq05-agent.md
  - src/chemworld/eval/static_optimization_campaign.py
  - src/chemworld/eval/static_optimization_baselines.py
  - src/chemworld/eval/static_material_information_campaign.py
  - src/chemworld/eval/static_material_information_triarm.py
deliverables:
  - Accurate typing for heterogeneous static-evaluator summaries, schemas, tuples, and metrics
  - No runtime algorithm or output changes
validation:
  - Mypy on all touched Python files
  - Ruff on all touched Python files
  - Relevant evaluator tests
  - git diff --check
completed: []
files_touched: []
final_commit: null
reviewer: null
review_result: null
notes: ""
```
