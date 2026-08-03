# Work I Task Claim

```yaml
task_id: W1-P08
title: "Audit publication figure editability, resolution, fonts, and final dimensions"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T16:51:32Z
lease_expires_at_utc: 2026-08-05T16:51:32Z
heartbeat_at_utc: 2026-08-03T17:02:24Z

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

completed_since_last_heartbeat:
  - "Resolved exactly six canonical figures and 18 bound outputs from the frozen P01 figure system and per-figure manifests."
  - "Verified editable SVG text with zero embedded rasters, 2124x1560 PNGs with 300 dpi declarations, and single-page 7.08x5.2 inch PDFs with embedded TrueType fonts."
  - "Excluded 12 legacy unmanifested SVG/PNG assets from the canonical inventory."
  - "Detected a Figure 3 PDF serialization mismatch; corrected it within the still-valid W1-P04 write set, then rebuilt this audit against the corrected manifest."
  - "Preserved the explicit P01 status that Figure 3 panels C/D remain pending W1-L05/L06 results."
current_validation: "PASS: audit a585f6407c2bb92f3e8567154263b0b2a09cc7b79db999349a017631eea7316e; 6/6 figures and 18/18 assets; all six task-local renderer checks; Ruff and format; mypy; 4 focused pytest cases including tamper failure; deterministic report rebuild; git diff --check."
files_touched:
  - workstreams/arxiv_v1/claims/W1-P08--codex-1.md
  - scripts/audit_work_i_publication_figures.py
  - tests/test_work_i_publication_figure_audit.py
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.json
  - paper/figures/experimental-intelligence-v1/publication/figure-publication-audit-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review; Figure 3 scientific pending panels remain owned by L05/L06."
handoff_eta: 2026-08-03T17:02:24Z

final_commit: "4049d662fdf0bcbc7f40d96d06bb90d8c7427760"
reviewer: null
review_result: null
notes: "This is an audit-only task. It resolves the six canonical figures through the frozen P01 figure system and their manifests; legacy unmanifested publication-directory files are not promoted or rewritten. Asset PASS does not promote Figure 3 C/D from their explicit pending scientific status."
```
