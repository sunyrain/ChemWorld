# Repository quality task claim

```yaml
task_id: AQ-10
title: "Make trajectory-launcher path assertions platform-neutral"
status: CLAIMED
owner: aq10-agent
claimed_at_utc: 2026-08-03T14:52:20Z
base_commit: "cbcf2f77696a399b081ef23c7590d16cb3fb1f2d"
branch: agent/aq10-launcher-path
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ10"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-10--aq10-agent.md
  - tests/test_g2_trajectory_replication_launcher.py
  - scripts/launch_g2_trajectory_replication.py
deliverables:
  - Platform-neutral trajectory-launcher command path assertions that retain exact config, output, and resume binding coverage.
validation:
  - uv run --frozen --extra dev pytest tests/test_g2_trajectory_replication_launcher.py
  - uv run --frozen --extra dev ruff check tests/test_g2_trajectory_replication_launcher.py scripts/launch_g2_trajectory_replication.py
  - git diff --check
completed: []
files_touched: []
final_commit: null
reviewer: null
review_result: null
notes: ""
```
