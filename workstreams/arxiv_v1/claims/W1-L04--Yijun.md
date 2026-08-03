# Work I Task Claim

```yaml
task_id: W1-L04
title: "Implement latent-terminal quality, regret, selection, and missingness audits"
status: REVIEW

owner: Yijun
collaborators: []
claimed_at_utc: 2026-08-03T14:53:36Z
lease_expires_at_utc: 2026-08-05T14:53:36Z
heartbeat_at_utc: 2026-08-03T15:24:41Z

base_commit: "b4c643dbd65af934b40678e5c82f63fdcdefeef8"
branch: work1/w1-l04-latent-terminal-analysis
worktree: ../ChemWorld-W1-L04
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L04--Yijun.md
  - src/chemworld/eval/latent_terminal_analysis.py
  - scripts/qualify_work_i_latent_terminal_analysis.py
  - tests/test_latent_terminal_analysis.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Deterministic analyzer implementing all eight L01-frozen estimands without changing their definitions, denominators, or entry rules"
  - "Selection-table, threshold-sensitivity, finite-population aggregation, decision-time, censoring, and unresolved-outcome bound calculations"
  - "Synthetic outcome-independent qualification proving fail-closed behavior and exact deterministic report regeneration"
  - "Focused positive and negative tests for denominators, null cells, missing scores, non-finite values, threshold equality, and forbidden complete-case substitution"
validation:
  - "uv run python scripts/qualify_work_i_latent_terminal_analysis.py"
  - "uv run python scripts/qualify_work_i_latent_terminal_analysis.py --check"
  - "uv run pytest -q tests/test_latent_terminal_analysis.py"
  - "uv run ruff check src/chemworld/eval/latent_terminal_analysis.py scripts/qualify_work_i_latent_terminal_analysis.py tests/test_latent_terminal_analysis.py"
  - "uv run mypy src/chemworld/eval/latent_terminal_analysis.py scripts/qualify_work_i_latent_terminal_analysis.py"
  - "git diff --check"

completed_since_last_heartbeat:
  - "Read the collaboration contract, Work I authority and master plan, L01-L03 claims, frozen machine/human latent-terminal contract, and L02 reconstructability evidence before implementation"
  - "Implemented the eight L01-frozen estimands, registered selection and threshold tables, 36/24/60 finite-population aggregation, decision-time null handling, the nine-cell campaign oracle, and registered missingness/censoring bounds"
  - "Added exact receipt/contract binding, fail-closed non-finite and unresolved handling, deterministic self-hashes, and explicit rejection of complete-case or imputed substitutions"
  - "Qualified seven deterministic synthetic cases and 20 focused tests without executing or accessing any formal shadow outcome"
current_validation: "PASS: synthetic qualifier generation/check (7/7, report SHA f2113e77d8b3bca66f80ddd1e88d48c87bc25443ab52c29129f4aca4271747be); pytest 20 passed; Ruff passed; changed-file mypy with --follow-imports=skip passed; git diff --check passed. The required dependency-following mypy invocation also surfaced six errors exclusively outside this claim's write set (electrochemical_services.py: 3, live_llm.py: 2, training.py: 1); no out-of-scope fixes were made."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L04--Yijun.md
  - src/chemworld/eval/latent_terminal_analysis.py
  - scripts/qualify_work_i_latent_terminal_analysis.py
  - tests/test_latent_terminal_analysis.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T03:24:41Z
next_24h: "Await independent review; address only in-scope review findings without accessing formal outcomes or overlapping L03 replay files."
handoff_eta: 2026-08-03T15:24:41Z

final_commit: "9044f8b61ccdce0d1f9e04c63d018326bf798f9a"
reviewer: null
review_result: null
notes: "Ready for review. L04 used synthetic fixtures only: formal_shadow_evaluations_executed=0, formal_shadow_outcomes_accessed=false, and provider_calls=0. No L03 replay implementation file was read as an outcome source or modified. uv environment acquisition stalled on unavailable downloads, so validations ran against the repository's existing pinned virtual environment with PYTHONPATH=src:."
```
