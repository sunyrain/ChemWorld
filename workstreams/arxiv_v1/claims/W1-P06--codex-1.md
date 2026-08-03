# Work I Task Claim

```yaml
task_id: W1-P06
title: "Render Figure 5: autonomous lifecycle and process profile"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:26:33Z
lease_expires_at_utc: 2026-08-05T16:26:33Z
heartbeat_at_utc: 2026-08-03T16:34:38Z

base_commit: "9fd601e9d000c4e50c2de14f3a15f823fe66fbd7"
branch: work1/w1-p06-figure-5
worktree: ../ChemWorld-W1-P06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P06--codex-1.md
  - scripts/render_work_i_figure_5.py
  - tests/test_work_i_figure_5.py
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.png
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.manifest.json
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

completed_since_last_heartbeat:
  - "Rendered the frozen seven-operation cell-01 lifecycle with observation entering public state before the next decision"
  - "Rendered the verified campaign receipt with closure, action, stock, cost, time, and sample units"
  - "Separated identity, resource authority, trajectory-receipt alignment, and exact replay controls from the prompt surface"
  - "Accounted for 60/60 closed lifecycles, 60 assays, 815 accepted operations, 164 non-final measurements, and zero invalid or right-censored units"
  - "Published deterministic editable SVG, embedded-font PDF, 300 dpi PNG, and a self-hashed task manifest"
current_validation: "PASS: Ruff, formatting, mypy, 4 focused tests, deterministic byte rebuild, one visual inspection, and git diff --check"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P06--codex-1.md
  - scripts/render_work_i_figure_5.py
  - tests/test_work_i_figure_5.py
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.png
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T16:34:38Z
next_24h: "Await independent review; preserve the descriptive-example and repeated-event counting boundaries."
handoff_eta: 2026-08-03T16:34:38Z

final_commit: "c8870e9bad5dc9f5b13838224dbb58a40c7d869e"
reviewer: null
review_result: null
notes: "The example lifecycle is descriptive and excluded from prior-effect inference; primitive operations are repeated events, not independent samples."
```
