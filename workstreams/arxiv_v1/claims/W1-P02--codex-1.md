# Work I Task Claim

```yaml
task_id: W1-P02
title: "Render Figure 1: ChemWorld apparatus and controlled world forks"
status: REVIEW

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T15:32:29Z
lease_expires_at_utc: 2026-08-05T15:32:29Z
heartbeat_at_utc: 2026-08-03T15:43:58Z

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

completed_since_last_heartbeat:
  - "Rendered the frozen P01 A-D apparatus and controlled-world-fork information architecture"
  - "Resolved both F source artifacts through the self-hashed D01 contract and retained exact 6-pair/24-trace/zero-provider counts"
  - "Produced deterministic editable SVG, embedded-font PDF, 300 dpi PNG, and a self-hashed five-source manifest"
  - "Removed cross-panel overlap after final-size visual inspection without changing evidence or claims"
current_validation: "PASS: 4 focused tests, deterministic byte rebuild, Ruff, mypy, SVG editability, PDF font embedding, 2124x1560 PNG, visual inspection, and git diff --check"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P02--codex-1.md
  - scripts/render_work_i_figure_1.py
  - tests/test_work_i_figure_1.py
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.png
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T15:43:58Z
next_24h: "Await independent review and later P08/P09 manifest/caption integration"
handoff_eta: 2026-08-03T15:47:00Z

final_commit: "e0344545cc8fcae2e5663c31927be3bc1f8d13e2"
reviewer: null
review_result: null
notes: "The figure proves apparatus programmability only. It does not depict agent performance, rule adaptation, arbitrary third-party DSL support, or physical-laboratory transfer."
```
