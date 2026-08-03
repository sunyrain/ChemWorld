# Work I Task Claim

```yaml
task_id: W1-V08
title: "Execute the frozen 30-campaign / 180-lifecycle known-policy matrix"
status: DONE

owner: codex-1
collaborators:
  - "agent:/root/w1_v08"
claimed_at_utc: 2026-08-03T08:31:36Z
lease_expires_at_utc: 2026-08-05T08:31:36Z
heartbeat_at_utc: 2026-08-03T10:15:38Z

base_commit: "716ee1ff6a5c32d987ae7cdcc6dfda9606ef5b8c"
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
  - git diff --check 716ee1ff6a5c32d987ae7cdcc6dfda9606ef5b8c...HEAD

completed_since_last_heartbeat:
  - "Verified the V07 receipt and exact CPython 3.11.15/NumPy 2.2.6/SciPy 1.17.1 apparatus before output construction."
  - "Executed the frozen formal matrix exactly once: 30 primary campaigns/180 closed primary lifecycles plus 30 same-identity retest campaigns/180 retest lifecycles excluded from the primary estimand, with zero provider calls."
  - "Validated every bundle and the manifest/progress hashes, bytes, canonical 30-cell prefix, counts, bindings, retest identity, matched arms, and 40,045,374-byte output size."
  - "Generated and byte-checked the V06 audit; all 12 gates passed, including the non-degenerate 28-assay/32-discard threshold branches."
  - "Validated completed --resume as a no-op: 32 files and all per-file SHA-256/byte counts were unchanged."
  - "Pushed raw evidence 55b7b3c1908a6bec8ee3dbc4b5e3efcbd3599ab6, audit 7e3337b7cbcb83248a88dceef31bcb635468d680, and execution handoff 75c9fcd831b7a3af4cdb24e551a8f3b367cbc251."
current_validation: "DONE: all claim-listed formal execution, immutable evidence, progress, size, provider-zero, retest-exclusion, V06 audit/check, completed-resume no-op, diff, and independent-review gates passed. Manifest SHA256 d15c7af5084a96d579fa87de55e0177d3eb2026dc5cb651042c516251751cdcc; progress SHA256 b3c4f143139041dd5c70e7d24441f46712caa7b136da9084178beb6ee93db906; audit SHA256 661d42ec74993200750f040bb4d12f4403fbc9c2c4b78aed5a9e6cc2b0c6be95."
files_touched:
  - workstreams/arxiv_v1/claims/W1-V08--codex-1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_progress.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/bundles/*.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-formal-execution-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Handoff complete; V09 may activate from the pushed V08 DONE baseline and must treat all formal evidence as immutable."
handoff_eta: 2026-08-03T10:12:04Z

final_commit: "75c9fcd831b7a3af4cdb24e551a8f3b367cbc251"
reviewer: "/root/w1_v07_review"
review_result: "APPROVE: one concentrated read-only review closed the V07 apparatus/receipt chain, 30/180 primary and excluded 30/180 retest counts, provider-zero proof, all 32 evidence files, progress/manifest hashes, 12/12 V06 audit gates, size gates, resume byte invariance, and no-retuning boundary."
notes: "Formal execution is now authorized only from the pushed V07 DONE baseline and only under the exact frozen apparatus. No source, frozen config, current pointer, evidence DAG, experiment ledger, manuscript, figure manifest, release manifest, raw provider payload, or global hot file is in scope. An interrupted formal run may resume only with identical frozen inputs through the fail-closed --resume path. A completed --resume is a fully validated no-op, not permission to overwrite or replace accepted evidence."
```
