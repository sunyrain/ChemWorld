# Work I Task Claim

```yaml
task_id: W1-D05
title: "Update the Work I experiment ledger, release manifest, and data card"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:52:17Z
lease_expires_at_utc: 2026-08-05T18:52:17Z
heartbeat_at_utc: 2026-08-03T18:52:17Z

base_commit: "9ffb11c4c7c3da3337bf9401fe716e1aa31caa7c"
branch: work1/w1-d05-ledger-release-card
worktree: ../ChemWorld-W1-D05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D05--codex-1.md
  - workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
  - tests/test_arxiv_v1_experiment_ledger.py
  - tests/test_arxiv_release_artifacts.py
shared_hot_file_requests:
  - "Reserved for W1-D05: workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
  - "Reserved for W1-D05: benchmark/releases/chemworld-serious-v1/manifest.json"
  - "Reserved for W1-D05: benchmark/releases/chemworld-serious-v1/DATA_CARD.md"

deliverables:
  - "Ledger section binding F=6/12/24, V=30/180/30, and L=60/36/10 to D01/D03/D04 hashes and explicit analysis roles"
  - "Release manifest bindings for the D03 immutable manifest and D04 68-node evidence graph without declaring publication readiness"
  - "Data-card disclosure of the F/V/L measurement layers, zero provider calls in these frozen additions, and the L 6-resolved/30-unresolved limitation"
validation:
  - "Run focused experiment-ledger/release-artifact tests and git diff --check once"
  - "Confirm no scientific counts are folded into the historical physical-experiment total and the external archive/author metadata gates remain open"

completed_since_last_heartbeat: []
current_validation: "D03 and D04 are integrated; derived SHA-256 1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4 and evidence graph SHA-256 a7f7ef76e69fb9532197f8b7352da24ecd6103cdc1ced11f68f86bde5577a2af."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D05--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T20:52:17Z
next_24h: "Synchronize the three release-facing truth surfaces and publish their tests without recomputing any experiment."
handoff_eta: 2026-08-03T20:52:17Z

final_commit: null
reviewer: null
review_result: null
notes: "D05 does not generate experiments, derived data, evidence DAGs, figures, manuscript text, author metadata, or external archive deposits."
```
