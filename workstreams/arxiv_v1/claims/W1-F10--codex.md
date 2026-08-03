# Work I Task Claim

```yaml
task_id: W1-F10
title: "Qualify transaction, resource, failure, and instrument semantics"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:26:00Z
lease_expires_at_utc: 2026-08-05T05:26:00Z
heartbeat_at_utc: 2026-08-03T06:20:00Z

base_commit: "e36293e7964a09b1129a49fca00f7ed3d580acb4"
branch: work1/w1-f10-semantic-qualification
worktree: ../ChemWorld-W1-F10
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F10--codex.md
  - scripts/qualify_work_i_experiment_semantics.py
  - tests/test_work_i_experiment_semantics.py
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.md
  - src/chemworld/foundation/world_fork_runtime.py
  - tests/test_world_fork_runtime.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md
  - scripts/summarize_work_i_world_fork.py
  - workstreams/arxiv_v1/claims/W1-F05--codex.md
  - workstreams/arxiv_v1/claims/W1-F06--codex.md
  - workstreams/arxiv_v1/claims/W1-F07--codex.md
shared_hot_file_requests:
  - "Correct the F05 reconstructed public failure-contract status vocabulary, remove trailing-whitespace generation in the F07 certificate renderer, and deterministically reissue the affected F06/F07 artifacts."

deliverables:
  - Per-operation transaction, precondition, failure, and runtime-route qualification table.
  - Per-instrument cost, latency, sample consumption, destructiveness, and terminal-state table.
  - Campaign resource hard-limit and replay semantics summary bound to executable probes.
validation:
  - uv run python scripts/qualify_work_i_experiment_semantics.py
  - uv run python scripts/qualify_work_i_experiment_semantics.py --check
  - uv run pytest -q tests/test_work_i_experiment_semantics.py
  - uv run ruff check scripts/qualify_work_i_experiment_semantics.py tests/test_work_i_experiment_semantics.py
  - git diff --check

completed_since_last_heartbeat:
  - "Bound every one of the 28 typed operations to its declared contract, runtime kernel, domain service, affected ledgers, a valid commit probe, and an invalid-action state-preservation probe."
  - "Qualified all five instrument contracts against observed cost, sample consumption, destructiveness, and terminal-state behavior."
  - "Executed the four distinct public transaction outcomes and qualified constitution rollback plus campaign hard-limit, attempt-charging, committed-only debit, and snapshot-replay semantics."
  - "Corrected the F05 reconstructed public failure vocabulary and deterministically reissued F05-F07 evidence without altering protocols, traces, gates, or conclusions."
current_validation: "F10 deterministic machine/human rebuild passed; 28/28 valid operation commits, 28/28 invalid probes with physical-state preservation, 5/5 instrument probes, four runtime statuses, resource replay, and all gates passed. Nine focused tests passed; ruff and mypy passed."
files_touched:
  - scripts/qualify_work_i_experiment_semantics.py
  - tests/test_work_i_experiment_semantics.py
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.md
  - src/chemworld/foundation/world_fork_runtime.py
  - tests/test_world_fork_runtime.py
  - scripts/summarize_work_i_world_fork.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md
  - workstreams/arxiv_v1/claims/W1-F05--codex.md
  - workstreams/arxiv_v1/claims/W1-F06--codex.md
  - workstreams/arxiv_v1/claims/W1-F07--codex.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:26:00Z
next_24h: "Coordinator review, independent rebuild on main, and merge."
handoff_eta: 2026-08-03T06:30:00Z

final_commit: "af6a21651ed7808ffce96c302ce93852d564eb42"
reviewer: coordinator
review_result: "accepted after independent Python 3.12 rebuild on main, nine focused regression tests, ruff, mypy, and deterministic reconstruction of F05-F07 derived evidence"
notes: "Qualification SHA-256: 91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3. Corrected F06 report SHA-256: 62684d414e9f9037b70d170abc6b29b442a928cf76df900a6bb53a3d60f2ee02. Corrected F07 certificate SHA-256: 5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78. Instrument latency is reported as declared scheduling semantics; the executable probe separately verifies immediate state effects, cost, sample debit, destructiveness, and terminal preconditions."
```
