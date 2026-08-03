# Work I Task Claim

```yaml
task_id: W1-P07
title: "Render Figure 6: fresh-session trajectory variation"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:36:50Z
lease_expires_at_utc: 2026-08-05T16:36:50Z
heartbeat_at_utc: 2026-08-03T16:47:43Z

base_commit: "905d57c76dbf5b9ad24bb6f8e784df70afa07496"
branch: work1/w1-p07-figure-6
worktree: ../ChemWorld-W1-P07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P07--codex-1.md
  - scripts/render_work_i_figure_6.py
  - tests/test_work_i_figure_6.py
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.png
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Publication Figure 6 in editable SVG, font-embedded PDF, and 300 dpi review PNG"
  - "Panels A--D show the matched fresh-session design, 2/8 endpoint diagnostic, continuous process contrasts, and explicit censoring plus 6/8 threshold-sensitive classification"
  - "Task-local deterministic manifest binding the current frozen G2 v0.5 derived evidence and output hashes"
validation:
  - "Focused source and renderer tests for 2 selected worlds, 10 planned pairs, 8 complete pairs, 2 right-censored pairs, 2/8 endpoint diagnostic, and 6/8 supporting classification"
  - "Deterministic byte rebuild check"
  - "SVG editability, embedded PDF fonts, final dimensions, and PNG resolution checks"
  - "One final visual inspection"
  - "ruff, mypy, pytest for task-local files, and git diff --check"

completed_since_last_heartbeat:
  - "Rendered all four frozen Figure 6 panels and publication SVG/PDF/PNG assets."
  - "Bound the figure to current.json, the current release, frozen derived data, formal terminal audit, and outcome-blind interpretation policy."
  - "Preserved both right-censored pairs and the descriptive, selected-world claim boundary."
current_validation: "PASS: Ruff and format check; mypy; 4 focused pytest cases; deterministic byte rebuild; editable SVG; embedded PDF fonts; 2124x1560 300 dpi PNG; one visual inspection; git diff --check. Manifest c10eec4b5c56c3f5749e404002e3643be6bcc943e71ad0b1b31cb2227d5d475b."
files_touched:
  - workstreams/arxiv_v1/claims/W1-P07--codex-1.md
  - scripts/render_work_i_figure_6.py
  - tests/test_work_i_figure_6.py
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.png
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review."
handoff_eta: 2026-08-03T16:47:43Z

final_commit: "d068a6d8710b07d51b91594ef9180eed06699738"
reviewer: null
review_result: null
notes: "The selected worlds are development-selected and descriptive. The 2/8 best/raw-terminal discordance is an endpoint diagnostic; 6/8 mixed classifications are threshold-sensitive supporting evidence, not the primary conclusion."
```
