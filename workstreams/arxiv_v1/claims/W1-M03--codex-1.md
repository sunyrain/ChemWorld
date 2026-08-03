# Work I Task Claim

```yaml
task_id: W1-M03
title: "Align historical generated reports with the current evidence binding"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:18:20Z
lease_expires_at_utc: 2026-08-05T17:18:20Z
heartbeat_at_utc: 2026-08-03T17:18:20Z

base_commit: "068b1964f622c129fe0fdde8255562a3a0900c7d"
branch: work1/w1-m03-report-alignment
worktree: ../ChemWorld-W1-M03
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-M03--codex-1.md
  - scripts/audit_work_i_historical_report_alignment.py
  - tests/test_work_i_historical_report_alignment.py
  - workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Self-hashed receipt binding both historical generated reports to their tracked bytes and current evidence-DAG nodes"
  - "Explicit acceptance evidence for 237 candidates, 235 committed executions, zero findings, 35 public-boundary probes, and 12 semantic-invariance paired runs"
  - "Fail-closed distinction between historical report source commits and current content-hash bindings"
  - "Human-readable handoff confirming whether any unexplained generated-artifact drift remains"
validation:
  - "Validate target paths, Git tracking, file SHA-256 values, configs/current.json node paths and hashes, freshness, artifact state, and gate state"
  - "Validate report status, checks, dependency bindings, core counts, and receipt self-hash"
  - "Run focused lint, type checking, tests, deterministic receipt rebuild, evidence-pipeline check, and git diff --check once at handoff"

completed_since_last_heartbeat: []
current_validation: "Pre-claim inspection: both reports are tracked and clean; their file hashes match current evidence-DAG nodes; core acceptance counts are present."
files_touched:
  - workstreams/arxiv_v1/claims/W1-M03--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T19:18:20Z
next_24h: "Implement the fail-closed alignment receipt and complete one focused validation pass."
handoff_eta: 2026-08-03T19:18:20Z

final_commit: null
reviewer: null
review_result: null
notes: "This task will not rewrite either historical report, configs/current.json, the global evidence DAG, or release manifests."
```
