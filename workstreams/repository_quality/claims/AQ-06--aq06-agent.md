# Repository quality task claim

```yaml
task_id: AQ-06
title: "Type replication audit, arXiv derived data, and participant qualification"
status: CLAIMED
owner: aq06-agent
claimed_at_utc: 2026-08-03T14:14:55Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq06-audit-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ06"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-06--aq06-agent.md
  - src/chemworld/eval/autonomous_material_replication_audit.py
  - src/chemworld/eval/arxiv_v1_derived_data.py
  - src/chemworld/eval/participant_prompt_qualification.py
deliverables:
  - "Fail-closed type narrowing for optional audit payloads and indexed data"
  - "Typed Gym environment campaign-state access without broad Any, cast, or ignore escapes"
validation:
  - "Mypy on touched source files"
  - "Ruff on touched source files"
  - "Related focused tests"
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
