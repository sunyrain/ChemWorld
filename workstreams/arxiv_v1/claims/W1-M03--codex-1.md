# Work I Task Claim

```yaml
task_id: W1-M03
title: "Align historical generated reports with the current evidence binding"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:18:20Z
lease_expires_at_utc: 2026-08-05T17:18:20Z
heartbeat_at_utc: 2026-08-03T17:25:37Z

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

completed_since_last_heartbeat:
  - "Bound both historical reports to their Git index blobs, working-tree SHA-256 values, and declared current evidence-DAG nodes without rewriting the reports."
  - "Verified the frozen acceptance evidence: 237 candidates, 235 validator-valid and runtime-committed executions, zero findings, 35/35 public-boundary probes, and 12/12 semantic-invariance paired runs."
  - "Separated the runtime report's historical source commit from the current path-plus-content-hash selector."
  - "Confirmed on the claimed main baseline that the repository-wide evidence checker already had an executable-source fingerprint mismatch; classified it as explained integration drift outside W1-M03 hot-file authority."
  - "Produced a self-hashed machine-readable receipt and concise human-readable handoff."
current_validation: "TASK-LOCAL PASS: receipt 301a3316654c38a3b273db57cdebb589026f90683a92b8e3da5632a5e0d3ced1; Ruff and format; Mypy; 4 focused pytest cases; deterministic receipt rebuild; target Git-index and SHA bindings; git diff --check. GLOBAL HANDOFF: evidence_pipeline --check fails on main baseline 143c83a7 because the repository executable fingerprint is stale and runtime_affordance registry freshness/gate plus stale-binding census await coordinator integration; no target report path or content mismatch was found."
files_touched:
  - workstreams/arxiv_v1/claims/W1-M03--codex-1.md
  - scripts/audit_work_i_historical_report_alignment.py
  - tests/test_work_i_historical_report_alignment.py
  - workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-historical-report-alignment-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review; route the explained repository-wide fingerprint refresh through W1-M05/W1-M06."
handoff_eta: 2026-08-03T17:25:37Z

final_commit: "6dca55b9c52ddd753ef306479e6921b06826ea49"
reviewer: null
review_result: null
notes: "Neither historical report, configs/current.json, the global evidence DAG, nor release manifests were rewritten. The target reports are aligned; the separately disclosed repository-level stale fingerprint predates W1-M03 implementation and requires coordinator-owned integration."
```
