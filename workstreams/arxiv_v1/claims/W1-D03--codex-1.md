# Work I Task Claim

```yaml
task_id: W1-D03
title: "Build the single frozen F/V/L-derived data layer"
status: READY_FOR_REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:26:52Z
lease_expires_at_utc: 2026-08-05T18:26:52Z
heartbeat_at_utc: 2026-08-03T18:38:39Z

base_commit: "d587c12c17bfce932d05de6ece69ab13e40b0bb4"
branch: work1/w1-d03-frozen-derived-data
worktree: ../ChemWorld-W1-D03
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D03--codex-1.md
  - src/chemworld/eval/arxiv_v1_derived_data.py
  - scripts/build_arxiv_v1_derived_data.py
  - tests/test_arxiv_v1_derived_data.py
  - benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json
  - benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.manifest.json
  - benchmark/releases/chemworld-serious-v1/figure-manifest.json
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-pairs.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-expectations.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-traces.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-campaign-profiles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-lifecycles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-retests.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-terminal-lifecycles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-latent-discard-units.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-campaign-cells.csv
  - workstreams/arxiv_v1/reports/work-i-fvl-derived-data-layer-v0.1.md
shared_hot_file_requests:
  - "Reserved for W1-D03: benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"
  - "Reserved for mechanical derived-data hash rebind only: benchmark/releases/chemworld-serious-v1/figure-manifest.json"

deliverables:
  - "Backward-compatible additive extension of the existing sole arXiv derived JSON, bound to the frozen D01 contract and immutable F/V/L reports"
  - "Normalized source-bound F pair/expectation/trace, V campaign/lifecycle/retest, and L cell/lifecycle/discard records with exact registered counts and roles"
  - "Nine deterministic CSV views and a self-hashed immutable file manifest with byte counts, hashes, counting rules, and no raw hidden/provider payloads"
  - "Human-readable handoff disclosing the L05/L06 6-resolved/30-unresolved boundary and all primary/reliability/audit counting separation"
validation:
  - "Preserve the complete legacy G0/G2 derived subtrees byte-for-byte at canonical JSON value level while adding F/V/L"
  - "Validate D01 contract SHA-256, every source file and embedded identity, common fields, unique primary keys, exact row counts, nullability, and no nonfinite values"
  - "Run focused Ruff, Mypy, pytest, deterministic rebuild/check, output-manifest audit, and git diff --check once at handoff"

completed_since_last_heartbeat:
  - "Extended the sole arXiv derived JSON additively with D01-bound normalized F/V/L records and exact registered counts."
  - "Generated nine deterministic CSV views, immutable file/count manifest, and concise scientific-boundary handoff."
  - "Mechanically rebound the existing rendered-figure manifest to derived-data SHA-256 1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4."
current_validation: "PASS: deterministic --check; 9 focused pytest cases; Ruff; Mypy for both source files; git diff --check. No provider/world/shadow execution."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D03--codex-1.md
  - src/chemworld/eval/arxiv_v1_derived_data.py
  - scripts/build_arxiv_v1_derived_data.py
  - tests/test_arxiv_v1_derived_data.py
  - benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json
  - benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.manifest.json
  - benchmark/releases/chemworld-serious-v1/figure-manifest.json
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-pairs.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-expectations.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-f-world-fork-traces.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-campaign-profiles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-lifecycles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-v-policy-retests.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-terminal-lifecycles.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-latent-discard-units.csv
  - benchmark/releases/chemworld-serious-v1/tables/work-i-l-campaign-cells.csv
  - workstreams/arxiv_v1/reports/work-i-fvl-derived-data-layer-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator integration and downstream W1-D04 evidence-DAG binding."
handoff_eta: 2026-08-03T18:40:00Z

final_commit: null
reviewer: null
review_result: null
notes: "D03 does not update the evidence DAG, experiment ledger, release manifest, data card, manuscript, paper figure manifest, or rendered figure files; D04/D05/P09 own those downstream surfaces."
```
