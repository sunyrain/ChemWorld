# Work I Task Claim

```yaml
task_id: W1-L06
title: "Publish the frozen latent-terminal primary and threshold/censoring analysis"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:07:33Z
lease_expires_at_utc: 2026-08-05T18:07:33Z
heartbeat_at_utc: 2026-08-03T18:12:09Z

base_commit: "4d35a56839a133a935c9489c2bea6dff45ac4964"
branch: work1/w1-l06-latent-analysis
worktree: ../ChemWorld-W1-L06
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L06--codex-1.md
  - scripts/analyze_work_i_latent_terminal_shadow_assays.py
  - tests/test_work_i_latent_terminal_formal_analysis.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Self-hashed formal analysis bound to the frozen L01 contract and the only L05 full-population receipt report"
  - "All eight registered estimands, four threshold rows, 36 unit rows, missingness strata, and sharp fixed-denominator bounds"
  - "Human-readable handoff that withholds latent-dependent point estimates and reports only registered bounds when the 36-score gate fails"
validation:
  - "Require the exact L05 report and receipt identities; never execute a shadow assay or call an agent/provider"
  - "Validate all 36 registered rows, the fixed 60-lifecycle census, four threshold surfaces, eight estimands, source hashes, and analysis self-hash"
  - "Run focused Ruff, Mypy, pytest, deterministic rebuild check, and git diff --check once at handoff"

completed_since_last_heartbeat:
  - "Bound the analysis to the exact L01, L04, L05 preflight, and only L05 formal-result identities."
  - "Published all eight registered estimands, four threshold rows, 36 audit rows, registered missingness surfaces, and sharp fixed-denominator bounds."
  - "Withheld every latent-dependent primary point estimate, retained the exact observed-assay precision only as non-promotable, and marked main_text_eligible false."
current_validation: "Focused Ruff, Mypy with imports skipped, four pytest cases, deterministic rebuild check, seven-file source-manifest check, analysis self-hash, and git diff --check passed. Analysis status is incomplete_full_report_required with 6 resolved and 30 unresolved receipts."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L06--codex-1.md
  - scripts/analyze_work_i_latent_terminal_shadow_assays.py
  - tests/test_work_i_latent_terminal_formal_analysis.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.md
blockers:
  - "The frozen L05 execution gate failed, so terminal quality remains unresolved and the latent-terminal result is not main-text eligible; this is a scientific-entry limitation, not an incomplete L06 deliverable."
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator review and manuscript handoff: state unresolved terminal quality and use only the frozen failure status and registered bounds."
handoff_eta: 2026-08-03T18:20:00Z

final_commit: "2afd71d9c9cefc82798fbd2874cbc7a246aee79a"
reviewer: null
review_result: null
notes: "No shadow assay was rerun or replaced. The analyzer executed zero shadow evaluations and made zero provider calls. The six retained formal scores occur only in registered diagnostic/bound surfaces; no complete-case primary substitute is published."
```
