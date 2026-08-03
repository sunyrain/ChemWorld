# Work I Task Claim

```yaml
task_id: W1-F03
title: "Define the public-contract invariance certificate"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T04:34:14Z
lease_expires_at_utc: 2026-08-05T04:34:14Z
heartbeat_at_utc: 2026-08-03T04:41:10Z

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

completed_since_last_heartbeat:
  - Canonicalized all nine public-contract component payloads and their digests.
  - Bound parent and child payload digests to the corresponding WorldForkSpec snapshots.
  - Added recursive identity-key and exact-identity-value leakage detection.
  - Added a definition fixture, deterministic certificate report, and mutation/leakage tests.
current_validation: "8/8 focused tests passed; 87/87 combined fork and mechanism regression tests passed; ruff, mypy, format check, and git diff check passed."
files_touched:
  - src/chemworld/foundation/world_fork_public_contract.py
  - configs/benchmark/work_i_world_fork_public_contract_v0.1.json
  - tests/test_world_fork_public_contract.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-public-contract-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:41:10Z
next_24h: "Coordinator review and merge; F05 can then bind actual runtime public payloads to this certificate."
handoff_eta: 2026-08-03T05:41:10Z

final_commit: "5718254cf1ceae8eb9aac964210c700ec16def3d"
reviewer: coordinator
review_result: PASS
notes: "Coordinator verified the declared write set, dependency boundary, nine-component binding, contract-mutation failure, and both identity-key and exact-value leakage rejection. F03 certifies interface equality only; it does not establish physical divergence, replay, or agent performance."
```
