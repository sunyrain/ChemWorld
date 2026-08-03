# Work I Task Claim

```yaml
task_id: W1-M04
title: "Archive the scope-stopped G2 v0.6 multiworld extension"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:07:21Z
lease_expires_at_utc: 2026-08-05T17:07:21Z
heartbeat_at_utc: 2026-08-03T17:13:27Z

base_commit: "ce62904362d61d6023bccb2810787953812bab71"
branch: work1/w1-m04-v06-scope-stop
worktree: ../ChemWorld-W1-M04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-M04--codex-1.md
  - scripts/archive_work_i_v06_scope_stop.py
  - tests/test_work_i_v06_scope_stop.py
  - workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.json
  - workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Self-hashed scope-stop receipt binding the frozen v0.6 design and the retained local matrix manifest without publishing provider responses"
  - "Administrative-only census of 160 planned cells, 7 completed cells, 1 right-censored cell, 152 pending cells, and 3 complete pairs"
  - "Explicit first-paper exclusion rule: no v0.6 outcome, score, contrast, estimand, figure, or inferential language is promoted"
  - "Human-readable handoff distinguishing the historical run manifest status from the owner scope-stop decision"
validation:
  - "Fail-closed validation of protocol, schedule, analysis, power, qualification, raw-manifest hashes, schedule identity, cell identity, and administrative state counts"
  - "Tests prove no score or outcome fields enter the tracked receipt and that tampering fails the receipt self-hash"
  - "ruff, mypy, pytest, deterministic report rebuild, and git diff --check"

completed_since_last_heartbeat:
  - "Bound all five prospective v0.6 design artifacts plus the archiver to immutable tracked hashes."
  - "Verified the retained local matrix manifest self-hash, protocol identity, reconstructed 160-cell schedule, source revision, and administrative states."
  - "Archived 7 completed cells, 1 right-censored cell, 152 pending cells, 3 complete pairs, and one right-censored pair without copying score or provider-response fields."
  - "Recorded the owner scope decision as superseding the historical raw run_status=running for Work I scope only, while preserving the raw manifest unchanged."
  - "Froze the first-paper exclusion: no v0.6 outcome, contrast, estimand, figure, or population claim is allowed."
current_validation: "PASS: receipt ce5ebbf5c52597f067c5ceda254668ede00d829efa09778344833fb7cf6bcc24; Ruff and format; mypy; 4 focused pytest cases; real local-manifest deterministic rebuild; tracked source hashes; raw self-hash; git diff --check."
files_touched:
  - workstreams/arxiv_v1/claims/W1-M04--codex-1.md
  - scripts/archive_work_i_v06_scope_stop.py
  - tests/test_work_i_v06_scope_stop.py
  - workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.json
  - workstreams/arxiv_v1/reports/g2-v0.6-scope-stop-receipt-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review; no v0.6 execution will resume inside Work I."
handoff_eta: 2026-08-03T17:13:27Z

final_commit: "252485b0ed5ff1f3be42de27fb541a7550fb91e2"
reviewer: null
review_result: null
notes: "The local runs/ manifest remains untracked by repository policy. The receipt binds its SHA-256 and byte count and extracts only lifecycle state and identity fields; it does not copy raw provider responses or outcome values."
```
