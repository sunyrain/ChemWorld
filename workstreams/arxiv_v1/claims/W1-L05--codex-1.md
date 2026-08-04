# Work I Task Claim

```yaml
task_id: W1-L05
title: "Qualify, freeze, and execute the 36 evaluator-only latent-terminal shadow assays"
status: DONE

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:48:56Z
lease_expires_at_utc: 2026-08-05T17:48:56Z
heartbeat_at_utc: 2026-08-03T18:05:22Z

base_commit: "eeb13513e92fb001ef5e48a56ad316a951400bbb"
branch: work1/w1-l05-shadow-assays
worktree: ../ChemWorld-W1-L05
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L05--codex-1.md
  - configs/benchmark/work_i_latent_terminal_shadow_assays_v0.1.json
  - scripts/run_work_i_latent_terminal_shadow_assays.py
  - tests/test_work_i_latent_terminal_shadow_assays.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assay-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Outcome-blind formal protocol binding the L01 entry rules, L02 reconstructability census, L03 replay implementation, and L04 analysis input contract"
  - "36/36 preflight proving unique registered discard identities and exact reconstructability before the first shadow score is read"
  - "Immutable self-hashed formal result with all 36 evaluator-only shadow assay receipts, original/replay identity checks, and exact counting rules"
  - "Human-readable execution handoff that publishes success or bounded failure for the full registered population"
validation:
  - "Commit and push the protocol, runner, tests, and preflight before formal execution"
  - "Require 36/36 exact prefix reconstructions, 36/36 terminal replacements, 36/36 same-identity replays, zero agent/provider calls, and no original artifact mutation"
  - "Fail closed without replacing, filtering, retry-selecting, or partially publishing outcomes"
  - "Run focused Ruff, Mypy, pytest, deterministic result check, source/hash audit, and git diff --check once at handoff"

completed_since_last_heartbeat:
  - "Pushed prospective protocol and 36/36 outcome-blind preflight at freeze commit ddc55253 before the first formal score was read."
  - "Executed the frozen two-pass population once and published all 36 receipts: 6 resolved, 30 bounded unresolved, zero provider calls, and unchanged raw source files."
  - "Located the fail-closed cause without rerunning: L03 resource preflight mutates the in-memory ledger before its mutation baseline, invalidating downstream lifecycle prefixes."
current_validation: "Focused Ruff, Mypy with imports skipped, four pytest cases, deterministic result check, terminal-index audit, and git diff --check passed. Formal report status is FAIL by construction: 6/36 resolved and 30/36 unresolved; all 36 registered receipts are present."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L05--codex-1.md
  - configs/benchmark/work_i_latent_terminal_shadow_assays_v0.1.json
  - scripts/run_work_i_latent_terminal_shadow_assays.py
  - tests/test_work_i_latent_terminal_shadow_assays.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assay-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.md
blockers:
  - "L03's evaluator-only resource preflight records a shadow event in the live in-memory ledger before the advertised mutation baseline; a future protocol version must preflight a copied ledger. Frozen v0.1 results must not be replaced."
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Coordinator review and L06 bounded-analysis handoff; do not rerun or replace frozen v0.1 outcomes."
handoff_eta: 2026-08-03T18:15:00Z

final_commit: "1c4328328b22488762abbef43a0e3772294f8c59"
reviewer: null
review_result: null
notes: "The only formal run is retained exactly. It made no provider call and changed no on-disk trajectory or ledger. The 6 resolved receipts and 30 registered unresolved receipts are execution evidence, not L06 inferential summaries."
```
