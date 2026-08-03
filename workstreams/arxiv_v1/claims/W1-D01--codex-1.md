# Work I Task Claim

```yaml
task_id: W1-D01
title: "Freeze schemas, units, and counting rules for new Work I experiments"
status: CLAIMED

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T15:02:45Z
lease_expires_at_utc: 2026-08-05T15:02:45Z
heartbeat_at_utc: 2026-08-03T15:02:45Z

base_commit: "8822f2a1c84ba99aa3c64ea88f9937c4c949c5da"
branch: work1/w1-d01-data-contract
worktree: "D:/Projects/ChemWorld-W1-D01"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D01--codex-1.md
  - configs/benchmark/work_i_incremental_data_contract_v0.1.json
  - src/chemworld/eval/work_i_data_contract.py
  - scripts/build_work_i_data_contract.py
  - tests/test_work_i_data_contract.py
  - workstreams/arxiv_v1/reports/work-i-incremental-data-contract-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Self-hashed cross-track contract for F/V/L record identities, dimensions, units, nullability, source hashes, and artifact roles"
  - "Explicit primary, replay/retest, qualification, shadow, and diagnostic counting rules that prevent double counting"
  - "Fail-closed validator and concise human report bound to the current immutable F/V/L protocol/report inputs"
validation:
  - "uv run python scripts/build_work_i_data_contract.py"
  - "uv run python scripts/build_work_i_data_contract.py --check"
  - "uv run pytest -q --no-cov tests/test_work_i_data_contract.py"
  - "uv run ruff check src/chemworld/eval/work_i_data_contract.py scripts/build_work_i_data_contract.py tests/test_work_i_data_contract.py"
  - "uv run mypy src/chemworld/eval/work_i_data_contract.py scripts/build_work_i_data_contract.py"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim prepared for main registration before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-D01--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:02:45Z
next_24h: "Implement and freeze the cross-track incremental data contract without regenerating global derived data"
handoff_eta: 2026-08-04T03:02:45Z

final_commit: null
reviewer: null
review_result: null
notes: "D01 freezes interfaces and counting semantics only. It does not regenerate the global derived-data layer, evidence DAG, experiment ledger, manuscript, figure manifest, or release manifest; those remain D03-D05/M06 surfaces."
```
