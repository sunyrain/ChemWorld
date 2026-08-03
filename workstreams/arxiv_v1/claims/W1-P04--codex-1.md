# Work I Task Claim

```yaml
task_id: W1-P04
title: "Render Figure 3: same completion, different terminal policy"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:01:14Z
lease_expires_at_utc: 2026-08-05T16:01:14Z
heartbeat_at_utc: 2026-08-03T16:01:14Z

base_commit: "b871c34221d5d96e77ba95fcecff662bcee6663d"
branch: work1/w1-p04-figure-3
worktree: ../ChemWorld-W1-P04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P04--codex-1.md
  - scripts/render_work_i_figure_3.py
  - tests/test_work_i_figure_3.py
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.png
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Publication Figure 3 in editable SVG, font-embedded PDF, and 300 dpi review PNG"
  - "Panels A--B bind the frozen 120-lifecycle census and complete-system terminal-action profiles to hashed source evidence"
  - "Panels C--D preserve explicit result-independent slots for W1-L05/L06 without fabricating latent-terminal results"
  - "Task-local deterministic manifest with output hashes, source hashes, counting rules, and pending-panel status"
validation:
  - "Focused renderer tests for source hashing, exact 84-assay/36-discard accounting, system/arm profiles, and pending-panel invariants"
  - "Deterministic byte rebuild check"
  - "SVG editability, embedded PDF fonts, final dimensions, and PNG resolution checks"
  - "One final visual inspection"
  - "ruff, mypy, pytest for task-local files, and git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim registered before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P04--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T22:01:14Z
next_24h: "Bind frozen complete-system evidence, render Figure 3, and hand off the task-local publication bundle."
handoff_eta: 2026-08-03T22:01:14Z

final_commit: null
reviewer: null
review_result: null
notes: "Panels C and D are frozen structural slots. Until W1-L05/L06 publish qualified results, they remain visibly pending and cannot imply discard quality."
```
