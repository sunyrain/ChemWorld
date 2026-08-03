# Work I Task Claim

```yaml
task_id: W1-S01
title: "Build the Work I claim-evidence-figure map"
status: REVIEW

owner: Yijun
collaborators: []
claimed_at_utc: 2026-08-03T14:53:36Z
lease_expires_at_utc: 2026-08-05T14:53:36Z
heartbeat_at_utc: 2026-08-03T15:13:22Z

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

completed_since_last_heartbeat:
  - "Built a 37-claim map spanning the center thesis, apparatus, programmability, measurement validity, complete-system terminal policy, compiled controls, process profiles, latent pending work, and scope/release boundaries."
  - "Bound every claim to exact allowed wording, forbidden overclaim, evidence path/hash/status, analysis unit, manuscript section, figure/panel, and completion state in synchronized JSON and Markdown outputs."
  - "Verified all 15 registered source paths and file SHA-256 values, all declared artifact content hashes, JSON parsing/counts/unique IDs, human/machine coverage, and pending/development-only publication guardrails."
current_validation: "PASS: 37 unique claims in 9 categories; 15/15 source paths and file SHA-256 values verified; all artifact content hashes embedded or canonically reproduced; JSON/Markdown coverage synchronized; no REVIEW/CLAIMED latent or development-only evidence promoted; python3 -m json.tool PASS; git diff --check PASS."
files_touched:
  - workstreams/arxiv_v1/claims/W1-S01--Yijun.md
  - workstreams/arxiv_v1/story/work-i-claim-evidence-figure-map-v0.1.json
  - workstreams/arxiv_v1/story/work-i-claim-evidence-figure-map-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await independent review; downstream S02-S10 and D03-D05 may consume the isolated map without treating it as a manuscript, figure-manifest, DAG, ledger, or release-manifest edit."
handoff_eta: 2026-08-03T15:13:22Z

final_commit: "fd12304c5592694e17a98b6ba230f213d101ba24"
reviewer: null
review_result: null
notes: "The story inputs preserve the current integration boundary: the legacy derived-data/figure layer predates Work I, L01-L02 remain REVIEW, L03-L04 remain CLAIMED, L05-L06 remain incomplete, and publication readiness remains false. No manuscript, figure, global evidence DAG, ledger, or release-manifest file was edited."
```
