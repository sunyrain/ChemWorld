# Work I Task Claim

```yaml
task_id: W1-S01
title: "Build the Work I claim-evidence-figure map"
status: CLAIMED

owner: Yijun
collaborators: []
claimed_at_utc: 2026-08-03T14:53:36Z
lease_expires_at_utc: 2026-08-05T14:53:36Z
heartbeat_at_utc: 2026-08-03T14:53:36Z

base_commit: "b4c643dbd65af934b40678e5c82f63fdcdefeef8"
branch: work1/w1-s01-claim-evidence-map
worktree: ../ChemWorld-W1-S01
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-S01--Yijun.md
  - workstreams/arxiv_v1/story/work-i-claim-evidence-figure-map-v0.1.json
  - workstreams/arxiv_v1/story/work-i-claim-evidence-figure-map-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "A claim-by-claim map from the Work I center thesis through apparatus, programmability, measurement validity, complete-system policy, process profiles, and boundaries"
  - "Exact evidence artifact and source bindings, intended manuscript section, intended figure/panel, status, and allowed/forbidden wording for every mapped claim"
  - "Machine-readable and human-readable maps that distinguish frozen evidence, pending latent-terminal evidence, development-only results, and external-release blockers"
validation:
  - "Verify every cited local artifact exists and every recorded SHA-256 matches where an authoritative hash is available"
  - "Cross-check claim language against WORK_I_TODOLIST.md, the master plan, and frozen human-readable reports"
  - "Verify no pending or development-only evidence is promoted to a completed publication claim"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim prepared on the current origin/main baseline; no manuscript or hot-file edits performed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-S01--Yijun.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T02:53:36Z
next_24h: "Produce and validate the claim-evidence-figure map as an isolated story input."
handoff_eta: 2026-08-04T08:53:36Z

final_commit: null
reviewer: null
review_result: null
notes: "This task produces isolated story inputs only and does not edit the main manuscript, figures, global evidence DAG, ledger, or release manifest."
```
