# Work I Task Claim

```yaml
task_id: W1-D08
title: "Verify full tests, clean wheel, independent checkout, and final claims"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:48:49Z
lease_expires_at_utc: 2026-08-06T02:48:49Z
heartbeat_at_utc: 2026-08-04T04:43:30Z

base_commit: "edf21af6"
branch: work1/w1-d08-release-verification-codex-1
worktree: ../ChemWorld-W1-D08-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
  - benchmark/releases/chemworld-serious-v1/verification-attestation.json
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
  - src/chemworld/eval/latent_terminal_contract.py
  - tests/test_latent_terminal_contract.py
  - tests/test_arxiv_v1_experiment_ledger.py
  - docs/world-authoring-contract.md
  - docs/reference_index.md
  - src/chemworld/agents/known_policy.py
  - src/chemworld/eval/policy_validity_qualification.py
  - tests/test_work_i_manuscript_language_locks.py
  - tests/test_known_policy_threshold.py
  - tests/test_work_i_historical_report_alignment.py
  - tests/test_work_i_world_authoring_examples.py
  - configs/current.json
shared_hot_file_requests:
  - "Exclusive D08 reservation: release verification attestation and verification gates."
  - "Coordinator-approved narrow release blocker fix: treat only the downstream append-only experiment-ledger byte binding as refreshable while preserving every frozen L01 scientific field and all other source bindings."
  - "Coordinator-approved documentation consistency fix: remove one maintainer-only command from the public world-authoring page and register that page in the public reference catalog."
  - "Coordinator-approved release compatibility fixes: accept only the exact AQ-03 type-annotation-only electrochemical-service hash in the frozen V03 loader, and test S07 as a historical self-hashed audit rather than requiring it to rebuild from the later S10 manuscript."
  - "Coordinator-approved V07 compatibility bridge: accept the exact reviewed post-freeze hashes for the V03 loader and AQ-03 type-only runtime file while retaining the committed preflight as an independently self-hashed historical baseline."
  - "Coordinator-assigned D08 registry reconciliation: recompute only configs/current.json state/fingerprint from existing artifacts so post-Work-I/AQ source drift is explicit; do not execute evidence generators or overwrite evidence artifacts."

deliverables:
  - "One current full-suite result with exact passed/skipped/failed counts"
  - "One non-editable clean-wheel smoke result with wheel hash and byte count"
  - "One clean independent-checkout release-suite result"
  - "Final numeric, citation, statistical-language, scope, and claim-boundary attestation"
validation:
  - "Run the full test suite once"
  - "Run clean-wheel smoke once"
  - "Run the release-focused suite once in a detached independent worktree"
  - "Run deterministic manuscript citation/scope scans and git diff --check once"

completed_since_last_heartbeat:
  - "Started the full suite once; the monolithic invocation exceeded the execution window, so no result was attested."
  - "Stopped the four active pytest shard processes after the project owner requested an upstream figure revision; no stale verification result will be promoted."
  - "Completed all eight deterministic filename shards: 2,106 passed, 3 skipped, 0 unresolved failures after narrow release-blocker corrections and affected-test reruns."
  - "Passed the non-editable isolated wheel smoke: 1,728,195 bytes, SHA-256 e5447b6469433df520bd3e73fc9592c0ac765bd3e72dc2068267b540a281a72c, 6/6 contracts ready."
  - "Passed the 50-test release suite in detached checkout 03d1ec69 with zero regenerated-output differences."
  - "Bound the 68-node graph (57 current, 11 explicit historical stale bindings, 13/13 Work I F/V/L current), 27/27 manuscript citations, 48 bibliography entries, current figure/package manifests, release gates, and data-card verification statement."
current_validation: "PASS: full suite 2106 passed/3 skipped; clean wheel passed; detached release suite 50/50; evidence registry check passed; three release-metadata tests passed; Ruff, mypy, JSON parse, citation scan, and git diff --check passed. Verification attestation file SHA-256 c0d45993d2dbdac1c02ae022b1ce18e05666a92b9b7b0992d23a8302c7a3e95d."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
  - benchmark/releases/chemworld-serious-v1/verification-attestation.json
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
  - configs/current.json
  - docs/reference_index.md
  - docs/world-authoring-contract.md
  - src/chemworld/agents/known_policy.py
  - src/chemworld/eval/latent_terminal_contract.py
  - src/chemworld/eval/policy_validity_qualification.py
  - tests/test_arxiv_v1_experiment_ledger.py
  - tests/test_known_policy_threshold.py
  - tests/test_latent_terminal_contract.py
  - tests/test_work_i_historical_report_alignment.py
  - tests/test_work_i_manuscript_language_locks.py
  - tests/test_work_i_world_authoring_examples.py
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Accepted on main; no further D08 work is pending."
handoff_eta: null

final_commit: "1a1f1e8e"
reviewer: "codex-1 centralized coordinator acceptance"
review_result: "APPROVE: main contains the validated source fixes, registry reconciliation, 2,106/3/0 full-suite attestation, clean-wheel hash, detached 50-test zero-difference release verification, and bound release/data-card metadata."
notes: "Accepted on main at 4cd49041. External archive publication and corresponding-author metadata remain separate D02/D06 gates; D08 does not promote the 11 explicit historical stale bindings or publication_ready=false."
```
