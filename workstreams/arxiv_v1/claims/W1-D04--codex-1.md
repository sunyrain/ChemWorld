# Work I Task Claim

```yaml
task_id: W1-D04
title: "Register frozen F/V/L evidence DAG nodes and source bindings"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:41:41Z
lease_expires_at_utc: 2026-08-05T18:41:41Z
heartbeat_at_utc: 2026-08-03T18:41:41Z

base_commit: "730d53532443809703c95bcb93a4b9cae926d9cb"
branch: work1/w1-d04-fvl-evidence-dag
worktree: ../ChemWorld-W1-D04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D04--codex-1.md
  - scripts/evidence_pipeline.py
  - tests/test_evidence_pipeline.py
  - tests/test_repository_current_registry.py
  - configs/current.json
  - workstreams/arxiv_v1/reports/work-i-fvl-evidence-binding-v0.1.md
shared_hot_file_requests:
  - "Reserved for W1-D04: scripts/evidence_pipeline.py"
  - "Reserved for W1-D04 evidence-DAG refresh only: configs/current.json"

deliverables:
  - "Acyclic evidence-DAG nodes for the frozen D01 contract, F/V/L immutable reports, D03 derived data, and immutable D03 manifest"
  - "Explicit content/result/manifest source-binding checks that fail closed on stale embedded hashes, derived-data hashes, counts, or latent missingness boundaries"
  - "Refreshed current registry with all new paths, roles, dependencies, hashes, freshness, and gate states visible on main"
  - "Concise handoff documenting registered nodes and the intentional separation from D05 ledger/release/data-card work"
validation:
  - "Run the D04 DAG/source-binding tests and evidence pipeline --check once after a clean deterministic refresh"
  - "Confirm new nodes are current, existing intentionally stale mechanism bindings are neither hidden nor rewritten, and git diff --check passes"

completed_since_last_heartbeat: []
current_validation: "D03 is integrated at main 730d5353 with derived-data SHA-256 1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D04--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T20:41:41Z
next_24h: "Register, refresh, validate, and publish F/V/L evidence bindings without modifying frozen source artifacts."
handoff_eta: 2026-08-03T20:41:41Z

final_commit: null
reviewer: null
review_result: null
notes: "D04 owns the global evidence-DAG integration window only. It does not update the experiment ledger, release manifest, data card, manuscript, figures, or frozen F/V/L inputs; D05/P09 own those surfaces."
```
