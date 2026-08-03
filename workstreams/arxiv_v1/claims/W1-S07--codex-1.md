# Work I Task Claim

```yaml
task_id: W1-S07
title: "Enforce figure first-reference, closure-count, sensitivity, and terminology locks"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:27:55Z
lease_expires_at_utc: 2026-08-05T17:27:55Z
heartbeat_at_utc: 2026-08-03T17:27:55Z

base_commit: "4568040a5ec74b4f70c6eb495611bebf39b778f2"
branch: work1/w1-s07-language-lock-audit
worktree: ../ChemWorld-W1-S07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-S07--codex-1.md
  - scripts/audit_work_i_manuscript_language_locks.py
  - tests/test_work_i_manuscript_language_locks.py
  - workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.json
  - workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Machine-readable audit of the current manuscript's first textual references to Figures 1--6"
  - "Exact counting lock distinguishing 120 closed lifecycles from 84 performed assays and 36 assay discards"
  - "Language lock retaining 2/8 as an endpoint diagnostic and 6/8 only as threshold-sensitive supporting evidence"
  - "Terminology residual scan and line-addressed integration proposals without editing the manuscript hot file"
validation:
  - "Fail closed on missing, duplicated, out-of-order, or semantically invalid figure/count/sensitivity locks"
  - "Cross-check the S02 story architecture, frozen G2 report, Figure 6 source manifest, and current manuscript"
  - "Run focused Ruff, Mypy, pytest, deterministic report rebuild, and git diff --check once at handoff"

completed_since_last_heartbeat: []
current_validation: "Claim prepared on synchronized origin/main; no manuscript or shared hot file modified."
files_touched:
  - workstreams/arxiv_v1/claims/W1-S07--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T19:27:55Z
next_24h: "Implement the isolated manuscript language-lock audit and hand off exact integration proposals."
handoff_eta: 2026-08-03T19:27:55Z

final_commit: null
reviewer: null
review_result: null
notes: "W1-S07 does not edit paper/experimental_intelligence_v1_manuscript.md, paper/arxiv/main.tex, display items, figures, or evidence/release hot files."
```
