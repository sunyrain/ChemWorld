# Work I Task Claim

```yaml
task_id: W1-S07
title: "Enforce figure first-reference, closure-count, sensitivity, and terminology locks"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:27:55Z
lease_expires_at_utc: 2026-08-05T17:27:55Z
heartbeat_at_utc: 2026-08-03T17:35:47Z

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

completed_since_last_heartbeat:
  - "Bound the current manuscript, frozen S02 story architecture, audited G2 comparison, six-figure system, and Figure 6 manifest by SHA-256."
  - "Verified the frozen 120 closed lifecycles = 84 final assays + 36 explicit discards partition across two distinct complete systems."
  - "Verified the current prose already treats 2/8 as the endpoint diagnostic and 6/8 as threshold-sensitive supporting evidence in deliberately selected worlds."
  - "Identified five final-integration blockers: Figure 2 absent and first references observed as [1,6,3,4,5], missing explicit 84-assay total at the first 120 mention, and three terminology residuals."
  - "Produced five line-addressed integration actions without modifying the manuscript or a shared hot file."
current_validation: "PASS: receipt 26ff46b73c8e584b65e18eff06f0440539f77a8e62a8a0e601c6aa41204e8969; Ruff and format; Mypy; 4 focused pytest cases; deterministic audit rebuild; frozen G2 and figure self-hashes; source SHA bindings; cached git diff --check."
files_touched:
  - workstreams/arxiv_v1/claims/W1-S07--codex-1.md
  - scripts/audit_work_i_manuscript_language_locks.py
  - tests/test_work_i_manuscript_language_locks.py
  - workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.json
  - workstreams/arxiv_v1/story/work-i-manuscript-language-lock-audit-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review; W1-S03/S09/S10 should consume the SHA-bound, line-addressed integration actions."
handoff_eta: 2026-08-03T17:35:47Z

final_commit: "3c2afd71489b30321da319bd6ee23dfc824a496a"
reviewer: null
review_result: null
notes: "W1-S07 did not edit paper/experimental_intelligence_v1_manuscript.md, paper/arxiv/main.tex, display items, figures, or evidence/release hot files. The audit status integration_changes_required describes the current manuscript snapshot, not task failure."
```
