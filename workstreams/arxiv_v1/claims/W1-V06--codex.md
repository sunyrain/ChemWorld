# Work I Task Claim

```yaml
task_id: W1-V06
title: "Implement construct-validity, resource, and exact-replay audit"
status: DONE

owner: codex
collaborators:
  - "agent:/root/w1_v06"
claimed_at_utc: 2026-08-03T06:54:12Z
lease_expires_at_utc: 2026-08-05T06:54:12Z
heartbeat_at_utc: 2026-08-03T08:23:11Z

base_commit: "1831d56f1f1ecfb83abab944f8548cd62b0dfcc6"
branch: work1/w1-v06-policy-validity-audit
worktree: ../ChemWorld-W1-V06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V06--codex.md
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/audit_work_i_policy_validity.py
  - tests/test_policy_validity_audit.py
shared_hot_file_requests: []

deliverables:
  - Fail-closed audit library that independently rebuilds the frozen profile and verifies construct-validity identities, partial orderings, conditional null rules, and the threshold non-degeneracy gate.
  - Exact campaign resource reconciliation and zero-provider verification from immutable matrix records.
  - Event, state, resource, terminal, profile, and endpoint exact-replay and same-identity test-retest verification.
  - Matched-arm identity/action invariance checks that preserve the boundary between interface validation and a material-information null claim.
  - Deterministic, source-bound audit receipt and read-only CLI suitable for V07 qualification and V09 reporting without freezing a protocol or consuming formal outcomes during this task.
validation:
  - uv run pytest -q tests/test_policy_validity_audit.py::test_v05_run_matrix_manifest_passes_all_v06_audit_gates --no-cov
  - uv run pytest -q tests/test_policy_validity_audit.py
  - uv run pytest -q tests/test_policy_validity_matrix.py tests/test_policy_validity_audit.py tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_campaign_resources.py
  - uv run pytest -q tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_campaign_resources.py tests/test_policy_validity_audit.py
  - uv run ruff check src/chemworld/eval/policy_validity_audit.py scripts/audit_work_i_policy_validity.py tests/test_policy_validity_audit.py
  - uv run mypy src/chemworld/eval/policy_validity_audit.py scripts/audit_work_i_policy_validity.py
  - git diff --check

completed_since_last_heartbeat:
  - "Completed read-only contract, dependency, repository, and write-set reconnaissance."
  - "Implemented a fail-closed, source-bound audit over the exact 30-cell factorial matrix and all 180 closed lifecycles."
  - "Added independent V01 profile reconstruction, V02 contract checks, full resource-ledger prefix reconciliation, replay/retest component verification, matched-arm invariance checks, and a read-only CLI."
  - "Added 13 synthetic immutable-record tests covering the valid matrix, tampering, conditional nulls, threshold degeneracy, replay/retest mismatches, arm drift, endpoint non-ordering, manifest bindings, and CLI behavior."
  - "Added strict native V05 manifest, bundle, execution, stable-numeric hash, controller-decision, and retest normalization into the existing independent V06 gates."
  - "Qualified the real V05 run_matrix producer API with an injected synthetic executor over all 30 cells and 180 primary lifecycles without executing or reading formal-world outcomes."
current_validation: "Coordinator rerun on main passed all 14 V06 tests and 72 V01-V06 contract/controller/matrix/resource/audit regressions without coverage; ruff, mypy, working-tree diff check, and base-to-HEAD whitespace validation also pass."
files_touched:
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/audit_work_i_policy_validity.py
  - tests/test_policy_validity_audit.py
  - workstreams/arxiv_v1/claims/W1-V06--codex.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator review of the native V05 compatibility checkpoint and downstream W1-V07 receipt binding; no formal execution is authorized by this claim."
handoff_eta: 2026-08-03T08:07:28Z

final_commit: "76716adc453e6efb488b18c640409e8659b3aaee"
reviewer: "codex-1"
review_result: "APPROVED after native-producer compatibility review: the V06 consumer strictly validates and audits V05 immutable artifacts, reconstructs profiles/resources/replay/retest evidence, and passes the complete injected 30-cell/180-lifecycle all-gates path without formal execution."
notes: "W1-V06 owns audit mechanics only. W1-V07 owns runner qualification and protocol freeze; W1-V09 owns the formal profile-recovery report. The compatibility acceptance used V05 execution_mode=injected_test with synthetic immutable evidence and formal_result=false; no chemical world, live controller, provider, or formal outcome was invoked or read."
```
