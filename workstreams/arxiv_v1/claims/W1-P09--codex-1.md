# Work I Task Claim

```yaml
task_id: W1-P09
title: "Refine and synchronize the six canonical publication figures"
status: ACTIVE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:22:11Z
lease_expires_at_utc: 2026-08-06T03:16:09Z
heartbeat_at_utc: 2026-08-04T03:16:09Z

base_commit: "e82b60df744493c2f31f848328ad42c26b08344d"
branch: work1/w1-p09-nature-figure-refinement-codex-1
worktree: ../ChemWorld-W1-P09-Nature-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
  - scripts/render_work_i_figure_1.py
  - tests/test_work_i_figure_1.py
  - scripts/render_work_i_figure_2.py
  - tests/test_work_i_figure_2.py
  - scripts/render_work_i_figure_3.py
  - tests/test_work_i_figure_3.py
  - scripts/render_work_i_figure_4.py
  - tests/test_work_i_figure_4.py
  - scripts/render_work_i_figure_5.py
  - tests/test_work_i_figure_5.py
  - scripts/render_work_i_figure_6.py
  - tests/test_work_i_figure_6.py
  - scripts/audit_work_i_publication_figures.py
  - tests/test_work_i_publication_figure_audit.py
  - scripts/audit_work_i_figure_integration.py
  - tests/test_work_i_figure_integration.py
  - paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.*
  - paper/figures/experimental-intelligence-v1/publication/figure-2-known-policy-validity.*
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.*
  - paper/figures/experimental-intelligence-v1/publication/figure-4-compiled-controls.*
  - paper/figures/experimental-intelligence-v1/publication/figure-5-complete-lifecycles.*
  - paper/figures/experimental-intelligence-v1/publication/figure-6-fresh-trajectories.*
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.json
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.md
  - paper/figures/experimental-intelligence-v1/work-i-publication-figure-manifest-v0.1.json
shared_hot_file_requests:
  - "Exclusive P09 reservation: paper/figures/experimental-intelligence-v1/ and canonical figure-integration outputs."
  - "The frozen paper/arxiv/figure-manifest.json remains a superseded migration input and will not be rewritten."

deliverables:
  - "Six refined canonical figures with a restrained semantic palette, lowercase panel labels, clearer evidence hierarchy, and readable final-size typography."
  - "Editable SVG and TrueType PDF exports plus 300 dpi PNG previews for all six figures."
  - "No change to frozen evidence, statistics, counting rules, exclusions, or manuscript claim boundaries."
  - "Updated per-figure manifests, publication audit, and canonical self-hashed 18-asset inventory."
validation:
  - "Run the six deterministic renderers once and their focused tests once."
  - "Run nature-figure static preflight once over all six plotting sources."
  - "Run publication/integration audits, Ruff, Mypy, and git diff --check once."
  - "Inspect all six final PNG previews once at publication size."

completed_since_last_heartbeat: []
current_validation: "nature-figure workflow loaded; one baseline visual inspection completed; substantive refinement has not started."
files_touched:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Refine all six renderers, rebuild the canonical assets once, run one focused QA pass, and hand off for centralized acceptance."
handoff_eta: 2026-08-04T06:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "The original P09 delivery was accepted on main at 410a4aab after final commit e940c765. This explicit project-owner-requested revision preserves that history in Git while reopening the same reserved figure-integration surface. No experiment, protocol, derived result, or frozen analysis will be regenerated."
```
