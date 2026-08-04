# Work I Task Claim

```yaml
task_id: W1-D08
title: "Verify full tests, clean wheel, independent checkout, and final claims"
status: BLOCKED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:48:49Z
lease_expires_at_utc: 2026-08-06T02:48:49Z
heartbeat_at_utc: 2026-08-04T03:16:09Z

base_commit: "69061d60"
branch: work1/w1-d08-release-verification-codex-1
worktree: ../ChemWorld-W1-D08-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
  - benchmark/releases/chemworld-serious-v1/verification-attestation.json
  - benchmark/releases/chemworld-serious-v1/manifest.json
  - benchmark/releases/chemworld-serious-v1/DATA_CARD.md
shared_hot_file_requests:
  - "Exclusive D08 reservation: release verification attestation and verification gates."

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
current_validation: "BLOCKED before attestation: the accepted publication figures and D07 arXiv package are being revised, so D08 must verify the rebuilt candidate rather than the superseded package."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
blockers:
  - "W1-P09 has been reopened for project-owner-requested Nature-style refinement of all six canonical figures."
  - "W1-D07 must rebuild the arXiv/proof package after the refined figure assets are accepted."
blocked_by: "W1-P09 visual refinement and downstream W1-D07 package rebuild"
unblock_condition: "Refined P09 assets are accepted on main and D07 rebuilds the publication package against their new hashes."
next_check_at_utc: 2026-08-04T06:00:00Z
next_24h: "Resume the four verification gates once against the rebuilt release candidate."
handoff_eta: null

final_commit: null
reviewer: null
review_result: null
notes: "Claim remains reserved by codex-1 while blocked, preventing duplicate ownership. External archive publication and corresponding-author metadata remain separate D02/D06 gates."
```
