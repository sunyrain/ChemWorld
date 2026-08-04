# Work I Task Claim

```yaml
task_id: W1-P09
title: "Synchronize final captions, display items, and publication figure manifests"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-04T02:22:11Z
lease_expires_at_utc: 2026-08-06T02:22:11Z
heartbeat_at_utc: 2026-08-04T02:22:11Z

base_commit: "c57c4e1240e2eb9589ace6444d6231dc11787103"
branch: work1/w1-p09-final-figure-integration-codex-1
worktree: ../ChemWorld-W1-P09-C1
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
  - scripts/render_work_i_figure_3.py
  - tests/test_work_i_figure_3.py
  - scripts/render_arxiv_v1_display_items.py
  - tests/test_arxiv_v1_display_items.py
  - scripts/audit_work_i_figure_integration.py
  - tests/test_work_i_figure_integration.py
  - paper/experimental_intelligence_v1_display_items.md
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.svg
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.pdf
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.png
  - paper/figures/experimental-intelligence-v1/publication/figure-3-terminal-policy.manifest.json
  - paper/figures/experimental-intelligence-v1/work-i-publication-figure-manifest-v0.1.json
shared_hot_file_requests:
  - "Exclusive P09 reservation: paper/experimental_intelligence_v1_display_items.md"
  - "The frozen paper/arxiv/figure-manifest.json is a P01-marked superseded migration input and will not be rewritten; P09 publishes a new canonical Work I inventory instead."

deliverables:
  - "Final Figure 3 panels C/D showing the frozen 6 resolved / 30 unresolved gate failure without complete-case estimates"
  - "Six final Figure 1–6 legends synchronized with the integrated manuscript and analysis units"
  - "Canonical self-hashed Work I publication-figure inventory over all 18 SVG/PDF/PNG assets"
  - "Provider-free deterministic integration audit binding captions, manuscript references, per-figure manifests, and output hashes"
validation:
  - "Run Figure 3 deterministic rebuild and focused tests once"
  - "Regenerate display items and validate all six caption titles/order/counting locks"
  - "Run the focused figure-integration audit, Ruff, Mypy, and git diff --check once"

completed_since_last_heartbeat: []
current_validation: "Claim registered on main after W1-S10 acceptance; no figure, caption, display, or manifest write has started."
files_touched:
  - workstreams/arxiv_v1/claims/W1-P09--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T03:22:11Z
next_24h: "Render the frozen Figure 3 disposition, synchronize all display items, validate once, merge, and push."
handoff_eta: 2026-08-04T04:00:00Z

final_commit: null
reviewer: null
review_result: null
notes: "No experiment, protocol, derived result, or frozen analysis is regenerated. The new Work I publication manifest supersedes the legacy arXiv inventory without mutating the P01-bound historical input."
```
