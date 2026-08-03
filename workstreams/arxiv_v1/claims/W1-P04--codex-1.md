# Work I Task Claim

```yaml
task_id: W1-P04
title: "Render Figure 3: same completion, different terminal policy"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:01:14Z
lease_expires_at_utc: 2026-08-05T16:01:14Z
heartbeat_at_utc: 2026-08-03T16:12:55Z

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

completed_since_last_heartbeat:
  - "Rendered the 120-lifecycle census as 84 assays plus 36 explicit discards, with system-specific 60/0 and 24/36 terminal profiles"
  - "Rendered all ten matched world-by-arm cells from the outcome-blind L01 population contract"
  - "Preserved all 36 registered discard identities, nine campaign-oracle opportunity cells, and the cell-02 structural null in fixed pending panels C--D"
  - "Published deterministic editable SVG, embedded-font PDF, 300 dpi PNG, and a self-hashed task manifest"
current_validation: "PASS: Ruff, formatting, mypy, 4 focused tests, deterministic byte rebuild, one visual inspection, and git diff --check"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P04--codex-1.md
  - scripts/render_work_i_figure_3.py
  - tests/test_work_i_figure_3.py
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.png
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T16:12:55Z
next_24h: "Await independent review; panels C--D remain fixed for qualified W1-L05/L06 result insertion."
handoff_eta: 2026-08-03T16:12:55Z

final_commit: "0b04ed255fd64844eff905eacfc4cc50da5854fb"
reviewer: null
review_result: null
notes: "Panels C and D are frozen structural slots. Until W1-L05/L06 publish qualified results, they remain visibly pending and cannot imply discard quality."
```
