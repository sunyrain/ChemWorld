# Work I Task Claim

```yaml
task_id: W1-V07
title: "Qualify the known-policy matrix runner and freeze the formal protocol"
status: ACTIVE

owner: codex-1
collaborators:
  - "agent:/root/w1_v07"
claimed_at_utc: 2026-08-03T08:24:08Z
lease_expires_at_utc: 2026-08-05T08:24:08Z
heartbeat_at_utc: 2026-08-03T08:25:41Z

base_commit: "53e30431fde9cd15c4f3a632e9a7214b8ac2c79d"
branch: work1/w1-v07-runner-qualification-freeze
worktree: ../ChemWorld-W1-V07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V07--codex-1.md
  - src/chemworld/eval/policy_validity_qualification.py
  - scripts/qualify_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json
  - tests/test_policy_validity_qualification.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1/**
shared_hot_file_requests: []

deliverables:
  - Outcome-free qualification of the exact V05 runner through an injected synthetic 5 x 2 x 3 matrix with identities explicitly distinct from formal chemical worlds.
  - V06 audit PASS over the native immutable V05 qualification manifest, including construct, resource, replay/retest, arm-invariance, null, ordering, and non-degeneracy gates.
  - Live controller/interface smoke on fixed nonformal seed 20000 for both arms and all three policies, with original/retest identity and zero-provider verification.
  - Immutable qualification manifests, hashes, byte counts, source bindings, and explicit exclusion from the 30-campaign/180-lifecycle formal estimand.
  - Self-hashed V05-compatible W1-V07 receipt freezing formal protocol, preflight, source, controller, auditor, and qualification-evidence bindings.
  - Fail-closed W1-V08 entry gates with no seed, threshold, estimand, stopping-rule, or acceptance-rule retuning after qualification.
validation:
  - uv run python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --preflight --check
  - uv run python scripts/qualify_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - uv run python scripts/qualify_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_qualification_v0.1.json --check
  - uv run pytest -q tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_known_policy_agents.py tests/test_policy_validity_matrix.py tests/test_policy_validity_audit.py tests/test_policy_validity_qualification.py
  - uv run ruff check src/chemworld/eval/policy_validity_qualification.py scripts/qualify_work_i_policy_controls.py tests/test_policy_validity_qualification.py
  - uv run mypy src/chemworld/eval/policy_validity_qualification.py scripts/qualify_work_i_policy_controls.py
  - git diff --check
  - git diff --check 53e30431fde9cd15c4f3a632e9a7214b8ac2c79d...HEAD

completed_since_last_heartbeat:
  - "Confirmed the V06 DONE dependency, dedicated branch/worktree, clean starting state, and coordinator-pushed codex-1 claim."
current_validation: "Implementation has not started; claim activation checkpoint only."
files_touched:
  - workstreams/arxiv_v1/claims/W1-V07--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T12:24:08Z
next_24h: "Qualify synthetic and fixed nonformal execution paths, freeze the receipt, and stop before any formal execution."
handoff_eta: 2026-08-03T16:24:08Z

final_commit: null
reviewer: null
review_result: null
notes: "Formal seeds 0-4 may appear only as frozen schedule coordinates in injected synthetic artifacts; no formal environment, controller execution, or outcome may be accessed. Synthetic physical/world/noise identities must be visibly qualification-only. Any failed gate is reported without changing seeds, threshold, protocol, or acceptance rules."
```
