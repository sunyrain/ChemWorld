# Work I Task Claim

```yaml
task_id: W1-D08
title: "Verify full tests, clean wheel, independent checkout, and final claims"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:48:49Z
lease_expires_at_utc: 2026-08-06T02:48:49Z
heartbeat_at_utc: 2026-08-04T02:48:49Z

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

completed_since_last_heartbeat: []
current_validation: "Claim registered on main after W1-D07 acceptance; validation commands have not started."
files_touched:
  - workstreams/arxiv_v1/claims/W1-D08--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T03:48:49Z
next_24h: "Run the four verification gates once, bind the exact results, merge, and push."
handoff_eta: 2026-08-04T05:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Verification is scoped to the current internally complete candidate. External archive publication and corresponding-author metadata remain separate D02/D06 gates."
```
