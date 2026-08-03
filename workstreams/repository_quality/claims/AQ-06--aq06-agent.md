# Repository quality task claim

```yaml
task_id: AQ-06
title: "Type replication audit, arXiv derived data, and participant qualification"
status: REVIEW
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
  - "PASS: uv run --frozen --extra dev mypy on all three touched source files"
  - "PASS: uv run --frozen --extra dev ruff check on all three touched source files"
  - "PASS: pytest --no-cov -q audit and derived-data tests (16 passed)"
  - "PASS: pytest -q participant prompt qualification test (1 passed)"
  - "PASS: git diff --check"
completed:
  - "Narrowed optional resource-replay payloads before mapping access and ledger calls"
  - "Validated final-score sequences before terminal indexing"
  - "Routed qualification campaign-state reads through the typed public interface"
files_touched:
  - workstreams/repository_quality/claims/AQ-06--aq06-agent.md
  - src/chemworld/eval/autonomous_material_replication_audit.py
  - src/chemworld/eval/arxiv_v1_derived_data.py
  - src/chemworld/eval/participant_prompt_qualification.py
final_commit: "9a1c66dbfd25011b15877a419121bea81965ac5d"
reviewer: null
review_result: null
notes: "No tests, frozen protocols, evidence, reports, dependencies, or scientific claims changed. Invalid audit payloads continue to fail closed."
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
