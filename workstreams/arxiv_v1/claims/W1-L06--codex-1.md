# Work I Task Claim

```yaml
task_id: W1-L06
title: "Publish the frozen latent-terminal primary and threshold/censoring analysis"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T18:07:33Z
lease_expires_at_utc: 2026-08-05T18:07:33Z
heartbeat_at_utc: 2026-08-03T18:07:33Z

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

completed_since_last_heartbeat: []
current_validation: "L05 is integrated as a complete bounded FAIL report with 6 resolved and 30 unresolved receipts; L04 explicitly qualifies the registered unresolved-bound surface."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L06--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T20:07:33Z
next_24h: "Run the already-qualified analyzer once on the immutable L05 receipts and publish the complete bounded report without a complete-case primary substitute."
handoff_eta: 2026-08-03T19:07:33Z

final_commit: null
reviewer: null
review_result: null
notes: "The analyzer may read the six retained formal scores only to construct the registered observed-only diagnostics and sharp bounds. It must not promote those six scores to a primary complete-case terminal-quality claim."
```
