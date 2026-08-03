# Work I Task Claim

```yaml
task_id: W1-V09
title: "Report known-policy profile recovery, discriminant validity, and test-retest reliability"
status: CLAIMED

owner: codex-1
collaborators:
  - "agent:/root/w1_v09"
claimed_at_utc: 2026-08-03T08:32:31Z
lease_expires_at_utc: 2026-08-05T08:32:31Z
heartbeat_at_utc: 2026-08-03T08:32:31Z

base_commit: "751f7526799e2920437ba3fbfb6802070c0484d0"
branch: work1/w1-v09-policy-validity-report
worktree: ../ChemWorld-W1-V09
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V09--codex-1.md
  - src/chemworld/eval/policy_validity_report.py
  - scripts/report_work_i_policy_validity.py
  - tests/test_policy_validity_report.py
  - workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Read-only deterministic analysis of only the V08 immutable formal manifest and its bound bundles; no world, controller, provider, or V08 artifact is executed or mutated.
  - Self-hashed machine and human reports covering all 30 primary campaign profiles, 180 primary closed lifecycles, frozen V01 metrics/nulls, V02 exact signatures/orderings/non-orderings, matched-arm checks, resource gates, and 30 same-identity retest pairs.
  - Campaign-level equal-weight policy summaries across ten world-arm cells per policy; lifecycle rows are never pooled before profile construction, and retest campaigns/lifecycles are excluded from the primary estimand.
  - Separate evidence-validity and scientific-status fields publishing every frozen gate and failure, including explicit threshold assay/discard counts and the frozen non-degeneracy state.
  - Exact bindings to the V08 DONE claim/final commit and immutable manifest, the V07 receipt, protocol/source/schedule/resource/dependency identities, every bundle hash/byte count, V01-V03 contracts, the V06 audit receipt, analyzer source identity, and counting rules.
  - A bounded known-policy construct/discriminant-validity and deterministic reliability conclusion, with no endpoint ranking, causal-null, model/provider-capability, scalar-intelligence, or real-laboratory claim.
validation:
  - uv run pytest -q tests/test_policy_validity_report.py tests/test_policy_validity_audit.py
  - uv run ruff check src/chemworld/eval/policy_validity_report.py scripts/report_work_i_policy_validity.py tests/test_policy_validity_report.py
  - uv run mypy src/chemworld/eval/policy_validity_report.py scripts/report_work_i_policy_validity.py
  - Generate and byte-exact --check the reports against the immutable V08 formal matrix manifest recorded at unblock.
  - Negative tests cover non-degeneracy, ordering, signature, null, stale receipt/manifest/bundle hash, retest mismatch, and explicit non-orderings that must not become gates.
  - git diff --check
  - git diff --check 751f7526799e2920437ba3fbfb6802070c0484d0...HEAD

completed_since_last_heartbeat: []
current_validation: "Read-only planning only; formal outcomes must not be read before W1-V08 is DONE and its immutable handoff is accepted."
files_touched: []
blockers:
  - "W1-V08 formal execution, immutable manifest/audit handoff, and independent acceptance are not complete."
blocked_by: W1-V08
unblock_condition: "W1-V08 is DONE on main with its final commit, immutable manifest path plus file/self hashes, audit path plus file/self hashes, V07 receipt hash, and counting rules recorded and independently accepted."
next_check_at_utc: 2026-08-03T12:32:31Z
next_24h: "Remain read-only until V08 acceptance; then create the dedicated branch/worktree from updated main and implement the reporter without changing any frozen rule."
handoff_eta: 2026-08-04T16:32:31Z

final_commit: null
reviewer: null
review_result: null
notes: "This advance claim reserves V09 without authorizing early access to formal outcomes. A scientific gate failure still yields the complete frozen report with status positive_control_unestablished; invalid evidence bindings yield invalid_evidence and no unsupported summary. Global ledger, evidence DAG, manuscript, figure/release manifests, configs/current.json, and every V08 artifact are excluded from the write set."
```
