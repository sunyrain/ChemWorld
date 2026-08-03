# Repository quality task claim

```yaml
task_id: AQ-09
title: "Honor the optional paper dependency contract in the release-finalizer test"
status: CLAIMED
owner: aq09-agent
claimed_at_utc: 2026-08-03T14:19:09Z
base_commit: d07da8553a08220911bb3da4c98ed849bc12e948
branch: agent/aq09-paper-test
worktree: /home/chenhh/python_projects/chemworld/ChemWorld-AQ09
declared_write_set:
  - workstreams/repository_quality/claims/AQ-09--aq09-agent.md
  - tests/test_arxiv_release_artifacts.py
deliverables:
  - Release-finalizer test coverage that distinguishes default dev from the optional paper extra
validation:
  - Focused pytest in the default dev environment
  - Focused Markdown-present branch validation when feasible
  - Ruff on the touched test
  - git diff --check
completed: []
files_touched: []
final_commit: null
reviewer: null
review_result: null
notes: "Do not modify pyproject.toml or production finalizer behavior; do not mask unrelated blockers."
```
