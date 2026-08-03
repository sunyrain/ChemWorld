# Work I Task Claim

```yaml
task_id: W1-P05
title: "Render Figure 4: compiled information controls"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:14:49Z
lease_expires_at_utc: 2026-08-05T16:14:49Z
heartbeat_at_utc: 2026-08-03T16:14:49Z

base_commit: "098ed1ef8ffc6bf6fc54657f78addb68ace3193d"
branch: work1/w1-p05-figure-4
worktree: ../ChemWorld-W1-P05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P05--codex-1.md
  - scripts/render_work_i_figure_4.py
  - tests/test_work_i_figure_4.py
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.png
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Publication Figure 4 in editable SVG, font-embedded PDF, and 300 dpi review PNG"
  - "Four panels separate frozen G0 outcome, prediction/calibration, epistemic, and non-composite profile readouts"
  - "Task-local deterministic manifest binding the current release entrypoint, frozen derived data, immutable sources, output hashes, and claim boundary"
validation:
  - "Focused source and renderer tests for task/arm counts, exact G0 readouts, and no-composite invariants"
  - "Deterministic byte rebuild check"
  - "SVG editability, embedded PDF fonts, final dimensions, and PNG resolution checks"
  - "One final visual inspection"
  - "ruff, mypy, pytest for task-local files, and git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim registered before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P05--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T22:14:49Z
next_24h: "Bind the current frozen derived-data release, render Figure 4, and hand off the task-local publication bundle."
handoff_eta: 2026-08-03T22:14:49Z

final_commit: null
reviewer: null
review_result: null
notes: "The figure is a bounded compiled-control decomposition, not an LLM-versus-optimizer contest and not a scalar experimental-intelligence score."
```
