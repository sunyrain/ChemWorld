# Work I Task Claim

```yaml
task_id: W1-F01
title: "Freeze the world-component inventory and manifest schema"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T03:58:43Z
lease_expires_at_utc: 2026-08-05T03:58:43Z
heartbeat_at_utc: 2026-08-03T03:58:43Z

base_commit: "5d34fc891ef53b41d1d2e8b4b5edeeefa80ece69"
branch: work1/w1-f01-world-component-inventory
worktree: ../ChemWorld-W1-F01
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F01--codex.md
  - src/chemworld/foundation/world_fork_manifest.py
  - configs/benchmark/work_i_world_fork_component_inventory_v0.1.json
  - tests/test_world_fork_manifest.py
  - workstreams/arxiv_v1/reports/work-i-world-component-inventory-v0.1.json
shared_hot_file_requests: []

deliverables:
  - A versioned, machine-readable inventory of forkable and invariant world components.
  - A strict manifest schema and validator with semantic checks.
  - A frozen Work I v0.1 inventory report consumable by later world-fork tasks.
validation:
  - uv run pytest -q tests/test_world_fork_manifest.py
  - uv run ruff check src/chemworld/foundation/world_fork_manifest.py tests/test_world_fork_manifest.py
  - uv run mypy src/chemworld/foundation/world_fork_manifest.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registration only; implementation has not started."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T15:58:43Z
next_24h: "Audit the executable-world state surfaces, freeze component identities and mutation permissions, then implement and validate the v0.1 manifest."
handoff_eta: 2026-08-04T03:58:43Z

final_commit: null
reviewer: null
review_result: null
notes: "F01 establishes the vocabulary consumed by F02-F05; it does not implement world forking or claim behavioral results."
```
