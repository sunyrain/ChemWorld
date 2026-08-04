# Work I Task Claim

```yaml
task_id: W1-D08
title: "Verify full tests, clean wheel, independent checkout, and final claims"
status: ACTIVE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:48:49Z
lease_expires_at_utc: 2026-08-06T02:48:49Z
heartbeat_at_utc: 2026-08-04T03:41:09Z

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
shared_hot_file_requests:
  - "Exclusive D08 reservation: release verification attestation and verification gates."
  - "Coordinator-approved narrow release blocker fix: treat only the downstream append-only experiment-ledger byte binding as refreshable while preserving every frozen L01 scientific field and all other source bindings."
  - "Coordinator-approved documentation consistency fix: remove one maintainer-only command from the public world-authoring page and register that page in the public reference catalog."

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
current_validation: "Shard 0 passed 375/375. Shard 1 passed 226 with one skip before four L01 validation failures; the narrow fix then passed its 13-test affected suite. Shard 2 passed 258 before two public-doc audit failures caused by the new world-authoring page carrying one maintainer command and missing the reference catalog. The runner remains fail-fast; both release blockers have narrow, non-scientific corrections."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T04:30:00Z
next_24h: "Run the release verification gates once against the rebuilt candidate, bind the exact results, and hand off."
handoff_eta: 2026-08-04T05:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Claim remains reserved by codex-1 while blocked, preventing duplicate ownership. External archive publication and corresponding-author metadata remain separate D02/D06 gates."
```
