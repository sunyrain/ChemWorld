# Work I Task Claim

```yaml
task_id: W1-F02
title: "Define WorldForkSpec, parent-child lineage, and component diffs"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:12:02Z
lease_expires_at_utc: 2026-08-05T04:12:02Z
heartbeat_at_utc: 2026-08-03T04:12:02Z

base_commit: "765afacbff1b77450db6daf51d766a89054e53b3"
branch: work1/w1-f02-world-fork-spec
worktree: ../ChemWorld-W1-F02
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F02--codex.md
  - src/chemworld/foundation/world_fork_spec.py
  - configs/benchmark/work_i_world_fork_spec_v0.1.json
  - tests/test_world_fork_spec.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-spec-v0.1.json
shared_hot_file_requests: []

deliverables:
  - A typed, versioned WorldForkSpec bound to the frozen F01 inventory hash.
  - Content-addressed parent-child lineage and an exact declared component diff.
  - Semantic guards for one compatible private-physics target and immutable invariants.
validation:
  - uv run pytest -q tests/test_world_fork_spec.py
  - uv run ruff check src/chemworld/foundation/world_fork_spec.py tests/test_world_fork_spec.py
  - uv run mypy src/chemworld/foundation/world_fork_spec.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registration only; implementation has not started."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:12:02Z
next_24h: "Freeze lineage identities, component-digest maps, and single-target diff semantics against the F01 inventory."
handoff_eta: 2026-08-04T04:12:02Z

final_commit: null
reviewer: null
review_result: null
notes: "F02 defines fork identity and admissible diffs only; F03 certifies public-contract invariance, F04 defines divergence, and F05 implements execution."
```
