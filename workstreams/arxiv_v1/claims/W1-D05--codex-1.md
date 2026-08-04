# Work I Task Claim

```yaml
task_id: W1-D05
title: "Update the Work I experiment ledger, release manifest, and data card"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:52:17Z
lease_expires_at_utc: 2026-08-05T18:52:17Z
heartbeat_at_utc: 2026-08-03T18:56:16Z

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

completed_since_last_heartbeat:
  - "Added one source-bound F/V/L section to the experiment ledger without changing historical G0/G2 physical-experiment totals."
  - "Updated the release manifest to the D03 derived/manifest hashes and D04 68-node graph, while preserving archive and author gates as open."
  - "Added data-card disclosure for F/V/L units, zero provider calls, and the retained 6-resolved/30-unresolved latent limitation."
current_validation: "PASS: JSON parse; Ruff; 18 focused ledger/release pytest cases; git diff --check."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D05--codex-1.md
  - workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
  - tests/test_arxiv_v1_experiment_ledger.py
  - tests/test_arxiv_release_artifacts.py
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator integration and the next unlocked manuscript/figure/QA task."
handoff_eta: 2026-08-03T18:57:00Z

final_commit: 659cd323
reviewer: null
review_result: null
notes: "D05 does not generate experiments, derived data, evidence DAGs, figures, manuscript text, author metadata, or external archive deposits."
```
