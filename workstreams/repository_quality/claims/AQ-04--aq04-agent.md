# Repository quality task claim

```yaml
task_id: AQ-04
title: "Type live-LLM and static-optimization agent paths"
status: REVIEW
owner: aq04-agent
claimed_at_utc: 2026-08-03T14:14:40Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq04-agent-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ04"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-04--aq04-agent.md
  - src/chemworld/agents/live_llm.py
  - src/chemworld/agents/static_optimization.py
deliverables:
  - "Resolve current Mypy errors in the live-LLM and static-optimization agent paths without changing runtime behavior"
validation:
  - "Mypy on touched source files"
  - "Ruff on touched source files"
  - "Relevant existing tests"
  - "git diff --check"
completed:
  - "Mypy passed on both touched source files"
  - "Ruff passed on both touched source files"
  - "Relevant existing test selection passed (173 AQ-04 tests; 81 focused static/predictive tests after shared query Protocol integration)"
  - "git diff --check passed"
files_touched:
  - src/chemworld/agents/live_llm.py
  - src/chemworld/agents/static_optimization.py
final_commit: "a187c99002d1ecbafdd3bedb7f8dac8157323a86"
reviewer: null
review_result: null
notes: "Implementation preserves provider-cost accounting and prompt mapping field order while expressing callable and container invariants through control flow and concrete types. Cleanup a187c99002d1ecbafdd3bedb7f8dac8157323a86 uses the native read-only predictive query Protocol from AQ-03 integration basis 69141912, removing the temporary runtime query copies."
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
