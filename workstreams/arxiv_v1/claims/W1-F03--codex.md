# Work I Task Claim

```yaml
task_id: W1-F03
title: "Define the public-contract invariance certificate"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:34:14Z
lease_expires_at_utc: 2026-08-05T04:34:14Z
heartbeat_at_utc: 2026-08-03T04:34:14Z

base_commit: "16d5fe7c23fd82737de762b039f26ba55720699a"
branch: work1/w1-f03-public-contract-certificate
worktree: ../ChemWorld-W1-F03
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F03--codex.md
  - src/chemworld/foundation/world_fork_public_contract.py
  - configs/benchmark/work_i_world_fork_public_contract_v0.1.json
  - tests/test_world_fork_public_contract.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-public-contract-v0.1.json
shared_hot_file_requests: []

deliverables:
  - Canonical payload and digest extraction for all nine F01 public-contract components.
  - A parent-child invariance certificate bound to a validated WorldForkSpec.
  - Explicit proof that audit-only fork identity is absent from the certified public payload.
validation:
  - uv run pytest -q tests/test_world_fork_public_contract.py
  - uv run ruff check src/chemworld/foundation/world_fork_public_contract.py tests/test_world_fork_public_contract.py
  - uv run mypy src/chemworld/foundation/world_fork_public_contract.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "Claim registration only; implementation has not started."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:34:14Z
next_24h: "Freeze public payload extraction, compare parent and child digests, and reject any fork identity or contract mutation."
handoff_eta: 2026-08-04T04:34:14Z

final_commit: null
reviewer: null
review_result: null
notes: "F03 certifies interface equality only; it does not establish physical divergence, replay, or agent performance."
```
