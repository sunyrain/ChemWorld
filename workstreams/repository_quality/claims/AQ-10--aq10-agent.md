# Repository quality task claim

```yaml
task_id: AQ-10
title: "Make trajectory-launcher path assertions platform-neutral"
status: REVIEW
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
completed:
  - Replaced Windows-only separator expectations with exact native Path string expectations.
  - Confirmed the launcher already preserves native config and output path semantics without production changes.
  - "PASS: uv run --frozen --extra dev pytest tests/test_g2_trajectory_replication_launcher.py (5 passed)"
  - "PASS: uv run --frozen --extra dev ruff check tests/test_g2_trajectory_replication_launcher.py scripts/launch_g2_trajectory_replication.py"
  - "PASS: git diff --check"
files_touched:
  - tests/test_g2_trajectory_replication_launcher.py
final_commit: "065367fad53301d194a288a2d0fd0cf415dbf375"
reviewer: null
review_result: null
notes: "The Linux failure was a platform-specific test expectation, not a production path bug. Path.__str__ supplies the native representation consumed by subprocess on each platform."
```
