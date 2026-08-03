# Work I Task Claim

```yaml
task_id: W1-V09
title: "Report known-policy profile recovery, discriminant validity, and test-retest reliability"
status: CHANGES_REQUESTED

owner: codex-1
collaborators:
  - "agent:/root/w1_v09"
claimed_at_utc: 2026-08-03T08:32:31Z
lease_expires_at_utc: 2026-08-05T08:32:31Z
heartbeat_at_utc: 2026-08-03T10:48:37Z

base_commit: "4fb789ba76550bd0b30510123181bb5394a14d0b"
branch: work1/w1-v09-policy-validity-report
worktree: ../ChemWorld-W1-V09
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V09--codex-1.md
  - src/chemworld/eval/policy_validity_report.py
  - scripts/report_work_i_policy_control_validity.py
  - tests/test_policy_validity_report.py
  - workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.manifest.json
shared_hot_file_requests: []

deliverables:
  - Read-only deterministic analysis of only the V08 immutable formal manifest and its bound bundles; no world, controller, provider, or V08 artifact is executed or mutated.
  - Self-hashed machine and human reports covering all 30 primary campaign profiles, 180 primary closed lifecycles, frozen V01 metrics/nulls, V02 exact signatures/orderings/non-orderings, matched-arm checks, resource gates, and 30 same-identity retest pairs.
  - Campaign-level equal-weight policy summaries across ten world-arm cells per policy; lifecycle rows are never pooled before profile construction, and retest campaigns/lifecycles are excluded from the primary estimand.
  - Separate evidence-validity and scientific-status fields publishing every frozen gate and failure, including explicit threshold assay/discard counts and the frozen non-degeneracy state.
  - Exact bindings to the V08 DONE claim/final commit and immutable manifest, the V07 receipt, protocol/source/schedule/resource/dependency identities, every bundle hash/byte count, V01-V03 contracts, the V06 audit receipt, analyzer source identity, and counting rules.
  - Independent self-hashed delivery manifest binding the machine report, Markdown report, both immutable V08 inputs, and analyzer source hashes without creating a self-reference cycle.
  - A bounded known-policy construct/discriminant-validity and deterministic reliability conclusion, with no endpoint ranking, causal-null, model/provider-capability, scalar-intelligence, or real-laboratory claim.
validation:
  - uv run --isolated --frozen --python 3.11.15 pytest -q tests/test_policy_validity_report.py tests/test_policy_validity_audit.py
  - uv run --isolated --frozen --python 3.11.15 ruff check src/chemworld/eval/policy_validity_report.py scripts/report_work_i_policy_control_validity.py tests/test_policy_validity_report.py
  - uv run --isolated --frozen --python 3.11.15 mypy src/chemworld/eval/policy_validity_report.py scripts/report_work_i_policy_control_validity.py
  - Generate and byte-exact --check the reports and independent delivery manifest against both immutable V08 formal matrix manifest and V06 audit receipt recorded at unblock.
  - Negative tests cover non-degeneracy, ordering, signature, null, stale receipt/manifest/bundle hash, retest mismatch, and explicit non-orderings that must not become gates.
  - git diff --check
  - git diff --check 4fb789ba76550bd0b30510123181bb5394a14d0b...HEAD

completed_since_last_heartbeat:
  - "W1-V08 is DONE on pushed main 4fb789ba after independent acceptance; its immutable manifest, progress chain, audit, and execution handoff are available."
  - "The formal manifest self-hash is d15c7af5084a96d579fa87de55e0177d3eb2026dc5cb651042c516251751cdcc and the V06 audit self-hash is 661d42ec74993200750f040bb4d12f4403fbc9c2c4b78aed5a9e6cc2b0c6be95."
current_validation: "CHANGES_REQUESTED: current 12/12 gates and positive_control_established result are correct, but a valid self-hashed failed audit receipt would still produce hard-coded success assertions for retest/profile/resource reliability. Drive every JSON/Markdown reliability assertion from its corresponding frozen gate and add one self-consistent gate-failure test before regenerating report hashes."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T11:15:00Z
next_24h: "Apply the single fail-honest reporting correction, regenerate the report chain once, complete independent review, integrate, then stop V implementation and run the requested V-series audit."
handoff_eta: 2026-08-03T12:00:00Z

final_commit: null
reviewer: "/root/w1_v07_review"
review_result: "CHANGES_REQUESTED: all current-data bindings, counts, summaries, gates, hashes, and bounded conclusions pass, but the supported positive_control_unestablished path must not retain hard-coded success claims for retest/profile/resource reliability."
notes: "Formal outcome access is authorized only for deterministic read-only reporting from the pushed V08 DONE baseline. The reporter consumes both work-i-policy-control-formal-v0.1/matrix_manifest.json and work-i-policy-control-formal-audit-v0.1.json and executes no world, controller, provider, or formal cell. A scientific gate failure still yields the complete frozen report with status positive_control_unestablished; invalid evidence bindings yield invalid_evidence and no unsupported summary. Global ledger, evidence DAG, manuscript, figure/release manifests, configs/current.json, and every V08 artifact are excluded from the write set."
```
