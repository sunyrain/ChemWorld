# Work I Task Claim

```yaml
task_id: W1-P06
title: "Render Figure 5: autonomous lifecycle and process profile"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:26:33Z
lease_expires_at_utc: 2026-08-05T16:26:33Z
heartbeat_at_utc: 2026-08-03T16:26:33Z

base_commit: "9fd601e9d000c4e50c2de14f3a15f823fe66fbd7"
branch: work1/w1-p06-figure-5
worktree: ../ChemWorld-W1-P06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P06--codex-1.md
  - scripts/render_work_i_figure_5.py
  - tests/test_work_i_figure_5.py
  - paper/figures/experimental-intelligence-v1/publication/figure-5-autonomous-lifecycle.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-5-autonomous-lifecycle.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-5-autonomous-lifecycle.png
  - paper/figures/experimental-intelligence-v1/publication/figure-5-autonomous-lifecycle.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Publication Figure 5 in editable SVG, font-embedded PDF, and 300 dpi review PNG"
  - "Panels A--D show one seven-operation lifecycle, campaign receipt, identity/replay controls, and failure/closure accounting"
  - "Task-local deterministic manifest binding the current frozen G2 v0.4 derived evidence and output hashes"
validation:
  - "Focused source and renderer tests for 7-operation ordering, 60/60 closure, 815 operations, 164 non-final measurements, identity, replay, and zero-invalid accounting"
  - "Deterministic byte rebuild check"
  - "SVG editability, embedded PDF fonts, final dimensions, and PNG resolution checks"
  - "One final visual inspection"
  - "ruff, mypy, pytest for task-local files, and git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim registered before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P06--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T22:26:33Z
next_24h: "Bind the current frozen G2 v0.4 lifecycle evidence, render Figure 5, and hand off the task-local publication bundle."
handoff_eta: 2026-08-03T22:26:33Z

final_commit: null
reviewer: null
review_result: null
notes: "The example lifecycle is descriptive and excluded from prior-effect inference; primitive operations are repeated events, not independent samples."
```
