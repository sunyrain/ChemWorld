# Work I Task Claim

```yaml
task_id: W1-V08
title: "Execute the frozen 30-campaign / 180-lifecycle known-policy matrix"
status: CLAIMED

owner: codex-1
collaborators:
  - "agent:/root/w1_v08"
claimed_at_utc: 2026-08-03T08:31:36Z
lease_expires_at_utc: 2026-08-05T08:31:36Z
heartbeat_at_utc: 2026-08-03T08:31:36Z

base_commit: "dc636000d0914977191b8a9a02ff683ec33a8cc6"
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
  - uv run python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --execute --allow-formal-execution --qualification-receipt configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json --output-root workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1
  - uv run python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json
  - uv run python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json --check
  - Verify immutable manifest hashes, file hashes, byte counts, 30/180 primary counts, retest exclusion, zero provider calls, and a completed-output --resume refusal/no-op from a clean checkout.
  - git diff --check
  - git diff --check dc636000d0914977191b8a9a02ff683ec33a8cc6...HEAD

completed_since_last_heartbeat: []
current_validation: "Read-only planning only; formal execution is prohibited until W1-V07 is DONE and its frozen receipt is present on main."
files_touched: []
blockers:
  - "W1-V07 qualification, protocol freeze, receipt merge, and independent acceptance are not complete."
blocked_by: W1-V07
unblock_condition: "W1-V07 is DONE on main and the exact V05 validator accepts its merged self-hashed qualification receipt."
next_check_at_utc: 2026-08-03T10:31:36Z
next_24h: "Remain read-only until V07 acceptance; then create the dedicated branch/worktree from updated main and execute the frozen matrix exactly once."
handoff_eta: 2026-08-04T08:31:36Z

final_commit: null
reviewer: null
review_result: null
notes: "This advance claim reserves V08 without authorizing early formal execution. No source, frozen config, current pointer, evidence DAG, experiment ledger, manuscript, figure manifest, release manifest, raw provider payload, or global hot file is in scope. An interrupted formal run may resume only with the identical frozen inputs and the runner's fail-closed --resume path."
```
