# Work I Task Claim

```yaml
task_id: W1-V07
title: "Qualify the known-policy matrix runner and freeze the formal protocol"
status: REVIEW

owner: codex-1
collaborators:
  - "agent:/root/w1_v07"
claimed_at_utc: 2026-08-03T08:24:08Z
lease_expires_at_utc: 2026-08-05T08:24:08Z
heartbeat_at_utc: 2026-08-03T09:05:04Z

base_commit: "53e30431fde9cd15c4f3a632e9a7214b8ac2c79d"
branch: work1/w1-v07-runner-qualification-freeze
worktree: ../ChemWorld-W1-V07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V07--codex-1.md
  - src/chemworld/eval/policy_validity_qualification.py
  - src/chemworld/eval/policy_validity_matrix.py
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/qualify_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json
  - tests/test_policy_validity_qualification.py
  - tests/test_policy_validity_matrix.py
  - tests/test_policy_validity_audit.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1/**
shared_hot_file_requests:
  - "GRANTED by coordinator at 2026-08-03T08:42:54Z: src/chemworld/eval/policy_validity_matrix.py and its task-local test/preflight, solely to correct the qualification-discovered native material-information identity binding before protocol freeze."
  - "GRANTED by coordinator at 2026-08-03T08:47:00Z: src/chemworld/eval/policy_validity_audit.py and its task-local tests, solely to make the independent native adapter bind that corrected digest to the frozen bundle cell descriptor before its SHA is frozen in the V07 receipt."

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
  - Verify native live executions bind material_information_sha256 to the frozen canonical arm descriptor and reject a null, stale, or cross-arm digest.
  - Verify the independent V06 native adapter rejects null, stale, and cross-arm-swapped material-information digests even after all producer self-hashes are recomputed.
  - git diff --check
  - git diff --check 53e30431fde9cd15c4f3a632e9a7214b8ac2c79d...HEAD

completed_since_last_heartbeat:
  - "Qualification discovery fail-closed exposed and corrected the pre-freeze V05 producer/V06 adapter material-information identity binding under coordinator reservations; null, stale, and cross-arm-swapped rehashed evidence is rejected."
  - "Pushed implementation hardening 9a65b0c8, deterministic preflight 5361cf7b, immutable artifacts/delivery manifest 1e09cb48, report/Markdown bfb16215, and formal receipt 7021e407."
  - "Complete injected synthetic V05 matrix passed every V06 gate: 30 campaigns, 180 closed lifecycles, 30 threshold assays, 30 threshold discards, and zero provider calls."
  - "Fixed seed-20000 nonformal smoke passed all gates: 6 original plus 6 exact retest campaigns, 36 plus 36 closed lifecycles, matched-arm invariance, and zero provider calls."
  - "Exact preflight and qualification byte rebuilds passed; full V01-V07 task-local suite passed 79 tests in 134.51s; ruff, mypy, both diff checks, and clean/upstream parity passed."
  - "Independent reviewer /root/w1_v07_review returned APPROVE and independently confirmed the frozen report, receipt, and delivery bindings."
current_validation: "REVIEW: all declared validations pass; qualification report c3f3985784187dbd77c9ef5f08744646bf79c052be5f1112e8daea016ec69b51, receipt 7cde7677d28943d50c6ddf12540513b91f3e88ec55b39d69a3caf50d646ad305, delivery manifest 7e97061bcbcc7708618153014b08c5218ea2fd544213c9498bf8494ca6f41661; formal environment executions/outcome reads remain 0/0."
files_touched:
  - src/chemworld/eval/policy_validity_qualification.py
  - src/chemworld/eval/policy_validity_matrix.py
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/qualify_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - tests/test_policy_validity_qualification.py
  - tests/test_policy_validity_matrix.py
  - tests/test_policy_validity_audit.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
  - configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1/**
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T09:20:00Z
next_24h: "Await coordinator integration/DONE bookkeeping; do not execute W1-V08 from this branch."
handoff_eta: 2026-08-03T09:10:00Z

final_commit: "7021e4076f3fcfa67c5374f593c7b0aa0d151143"
reviewer: "/root/w1_v07_review"
review_result: "APPROVED"
notes: "Formal seeds 0-4 may appear only as frozen schedule coordinates in injected synthetic artifacts; no formal environment, controller execution, or outcome may be accessed. To exercise the exact V05/V06 contracts, synthetic cell/campaign/profile IDs remain the canonical schedule coordinates; injected_test mode, formal_result=false, explicit qualification-only role/namespace fields, and qualification-only world/noise/physical identities distinguish the evidence from V08. Noise identity remains paired across information arms. The native producer and independent auditor bind material_information_sha256 to semantic_sha256(cell.material_information), matching the frozen arm descriptor; null, stale, or swapped values remain invalid after rehashing. This changes no world, seed, controller, threshold, estimand, stopping rule, or acceptance rule. Any failed gate is reported without retuning."
```
