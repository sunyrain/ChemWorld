# Work I Task Claim

```yaml
task_id: W1-P08
title: "Audit publication figure editability, resolution, fonts, and final dimensions"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:51:32Z
lease_expires_at_utc: 2026-08-05T16:51:32Z
heartbeat_at_utc: 2026-08-03T16:51:32Z

base_commit: "b2f03bd647cee67e88e11f7fd620c864e511e2db"
branch: work1/w1-p08-publication-figure-audit
worktree: ../ChemWorld-W1-P08
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-P08--codex-1.md
  - scripts/audit_work_i_publication_figures.py
  - tests/test_work_i_publication_figure_audit.py
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.json
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Fail-closed inventory of the six P01-assigned publication figures and their task-local manifests"
  - "Machine-readable audit of SVG text editability, raster absence, PNG 300 dpi final dimensions, PDF page dimensions, embedded TrueType fonts, and source/output hashes"
  - "Concise human-readable audit report with per-figure findings and a global publication gate"
validation:
  - "Focused tests covering P01 inventory resolution, manifest self-hashes, source/output hashes, SVG/PDF/PNG properties, and tamper failure"
  - "Run all six task-local deterministic renderer checks without changing committed assets"
  - "ruff, mypy, pytest, report rebuild equality, and git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim registered before substantive writes"
files_touched:
  - workstreams/arxiv_v1/claims/W1-P08--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T20:51:32Z
next_24h: "Implement and publish the six-figure publication-asset audit without rewriting any figure output."
handoff_eta: 2026-08-03T20:51:32Z

final_commit: null
reviewer: null
review_result: null
notes: "This is an audit-only task. It resolves the six canonical figures through the frozen P01 figure system and their manifests; legacy unmanifested publication-directory files are not promoted or rewritten."
```
