# Work I Task Claim

```yaml
task_id: W1-P02
title: "Render Figure 1: ChemWorld apparatus and controlled world forks"
status: CLAIMED

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T15:32:29Z
lease_expires_at_utc: 2026-08-05T15:32:29Z
heartbeat_at_utc: 2026-08-03T15:32:29Z

base_commit: "9548e0afb32e4b01064e0c6e7c8dffa8c54389fe"
branch: work1/w1-p02-figure-1
worktree: "D:/Projects/ChemWorld-W1-P02"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P02--codex-1.md
  - scripts/render_work_i_figure_1.py
  - tests/test_work_i_figure_1.py
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.png
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Editable two-column Figure 1 implementing the frozen P01 A-D panel jobs"
  - "Exact F certificate counts and qualification gates resolved through the frozen D01 source bindings"
  - "Deterministic SVG/PDF/PNG exports and self-hashed per-figure manifest"
validation:
  - "uv run python scripts/render_work_i_figure_1.py"
  - "uv run python scripts/render_work_i_figure_1.py --check"
  - "uv run pytest --no-cov -q tests/test_work_i_figure_1.py"
  - "uv run ruff check scripts/render_work_i_figure_1.py tests/test_work_i_figure_1.py"
  - "uv run mypy scripts/render_work_i_figure_1.py"
  - "Visual inspection of the final-size PNG"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim prepared for main registration before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P02--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:32:29Z
next_24h: "Render and validate Figure 1 without editing the manuscript, global figure manifest, or release outputs"
handoff_eta: 2026-08-03T20:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The figure proves apparatus programmability only. It does not depict agent performance, rule adaptation, arbitrary third-party DSL support, or physical-laboratory transfer."
```
