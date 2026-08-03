# Work I Task Claim

```yaml
task_id: W1-V08
title: "Execute the frozen 30-campaign / 180-lifecycle known-policy matrix"
status: ACTIVE

owner: codex-1
collaborators:
  - "agent:/root/w1_v08"
claimed_at_utc: 2026-08-03T08:31:36Z
lease_expires_at_utc: 2026-08-05T08:31:36Z
heartbeat_at_utc: 2026-08-03T09:57:32Z

base_commit: "f1452b5c5904c4b2cc6fabb2cd0387c43feb1d46"
branch: work1/w1-v08-formal-policy-controls
worktree: ../ChemWorld-W1-V08
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V08--codex-1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/**
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-execution-v0.1.md
shared_hot_file_requests: []

deliverables:
  - One immutable formal execution of the V07-frozen V05 runner over the unique 5 x 2 x 3 primary matrix: 30 campaigns and 180 closed primary lifecycles.
  - Same-identity deterministic retest evidence kept outside the primary estimand, with exactly 30 retest campaigns and 180 retest lifecycles when required by the frozen protocol.
  - Complete native bundles, terminal matrix manifest, semantic and file hashes, byte counts, source bindings, resource ledgers, zero-provider proof, and explicit counting rules.
  - Fail-closed resume evidence that accepts only a canonical validated prefix and never overwrites or replaces an accepted or failed frozen result.
  - V06 audit output and a concise execution handoff recording every failed cell or gate without retuning seeds, thresholds, protocol, estimand, stopping rules, or acceptance rules.
validation:
  - uv run --isolated --frozen --python 3.11.15 python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --execute --allow-formal-execution --qualification-receipt configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json --output-root workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1
  - uv run --isolated --frozen --python 3.11.15 python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json
  - uv run --isolated --frozen --python 3.11.15 python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json --check
  - Verify immutable manifest hashes, file hashes, byte counts, 30/180 primary counts, 30/180 retest exclusion, zero provider calls, and a completed-output --resume validated no-op from a clean checkout.
  - Verify matrix_progress.json independently closes its self-hash, accepted-bundle count/list, and canonical prefix before relying on the terminal manifest.
  - Hard-stop before commit if any single generated file is at least 50 MiB or total output size is abnormal relative to the approximately 40 MiB plan.
  - git diff --check
  - git diff --check dc636000d0914977191b8a9a02ff683ec33a8cc6...HEAD

completed_since_last_heartbeat:
  - "W1-V07 is DONE on pushed main f1452b5c; its receipt, apparatus, preflight, qualification report, and independent APPROVE are available."
  - "V08 execution plan is locked to the original CPython 3.11.15/NumPy 2.2.6/SciPy 1.17.1 apparatus and receipt bb3b6170e654cd74122ff719ac9a01d55bc163e8f2ca57046245139d9d3c60fa."
current_validation: "ACTIVE: create the dedicated worktree from f1452b5c, verify the frozen apparatus before output/world construction, execute the formal matrix exactly once, then audit and publish immutable evidence without retuning."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T10:30:00Z
next_24h: "Execute the frozen matrix exactly once, audit it, push immutable evidence by layer, and hand off without changing any frozen input or rule."
handoff_eta: 2026-08-03T11:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Formal execution is now authorized only from the pushed V07 DONE baseline and only under the exact frozen apparatus. No source, frozen config, current pointer, evidence DAG, experiment ledger, manuscript, figure manifest, release manifest, raw provider payload, or global hot file is in scope. An interrupted formal run may resume only with identical frozen inputs through the fail-closed --resume path. A completed --resume is a fully validated no-op, not permission to overwrite or replace accepted evidence."
```
