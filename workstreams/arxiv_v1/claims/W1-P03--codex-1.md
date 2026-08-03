# Work I Task Claim

```yaml
task_id: W1-P03
title: "Render Figure 2: known policies validate the experimental-agency profile"
status: CLAIMED

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T15:46:20Z
lease_expires_at_utc: 2026-08-05T15:46:20Z
heartbeat_at_utc: 2026-08-03T15:46:20Z

base_commit: "d259a0dd511acad46975d46730a8e3caa42af2a9"
branch: work1/w1-p03-figure-2
worktree: "D:/Projects/ChemWorld-W1-P03"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P03--codex-1.md
  - scripts/render_work_i_figure_2.py
  - tests/test_work_i_figure_2.py
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.png
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.manifest.json
shared_hot_file_requests: []

deliverables:
  - "Editable two-column Figure 2 implementing the frozen P01 A-D known-policy validity jobs"
  - "Primary 30-campaign profile recovery, discriminant axes, and same-identity retest reliability shown without denominator inflation"
  - "Deterministic SVG/PDF/PNG exports and self-hashed per-figure manifest"
validation:
  - "uv run python scripts/render_work_i_figure_2.py"
  - "uv run python scripts/render_work_i_figure_2.py --check"
  - "uv run pytest --no-cov -q tests/test_work_i_figure_2.py"
  - "uv run ruff check scripts/render_work_i_figure_2.py tests/test_work_i_figure_2.py"
  - "uv run mypy scripts/render_work_i_figure_2.py"
  - "Visual inspection of the final-size PNG"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim prepared for main registration before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P03--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:46:20Z
next_24h: "Render and validate Figure 2 without editing the manuscript, global figure manifest, or release outputs"
handoff_eta: 2026-08-03T21:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Retest campaigns are deterministic reliability evidence only and remain excluded from the 30-campaign primary estimand. The figure makes no model/provider capability, endpoint ranking, causal information-effect, scalar-intelligence, or real-laboratory claim."
```
