# Work I Task Claim

```yaml
task_id: W1-P03
title: "Render Figure 2: known policies validate the experimental-agency profile"
status: DONE

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T15:46:20Z
lease_expires_at_utc: 2026-08-05T15:46:20Z
heartbeat_at_utc: 2026-08-03T15:57:28Z

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

completed_since_last_heartbeat:
  - "Rendered all four frozen P01 panels for policy definitions, terminal signatures, separate profile axes, and retest reliability"
  - "Bound V02 policy definitions and V09 formal evidence through the self-hashed D01 contract and report dependency hash"
  - "Kept 30 retest campaigns separate from the 30 primary campaigns and 180 primary lifecycles"
  - "Produced deterministic editable SVG, embedded-font PDF, 300 dpi PNG, and a self-hashed seven-source manifest"
current_validation: "PASS: 4 focused tests, deterministic byte rebuild, Ruff, mypy, SVG editability, PDF font embedding, 2124x1560 PNG, visual inspection, and git diff --check"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P03--codex-1.md
  - scripts/render_work_i_figure_2.py
  - tests/test_work_i_figure_2.py
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.png
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.manifest.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T15:57:28Z
next_24h: "Await independent review and later P08/P09 manifest/caption integration"
handoff_eta: 2026-08-03T16:01:00Z

final_commit: "4ad107456b5b8b4d4785a55b3572a9687d3932b5"
reviewer: null
review_result: null
notes: "Retest campaigns are deterministic reliability evidence only and remain excluded from the 30-campaign primary estimand. The figure makes no model/provider capability, endpoint ranking, causal information-effect, scalar-intelligence, or real-laboratory claim."
```
