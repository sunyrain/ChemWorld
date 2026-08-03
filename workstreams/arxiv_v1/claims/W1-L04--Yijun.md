# Work I Task Claim

```yaml
task_id: W1-L04
title: "Implement latent-terminal quality, regret, selection, and missingness audits"
status: ACTIVE

owner: Yijun
collaborators: []
claimed_at_utc: 2026-08-03T14:53:36Z
lease_expires_at_utc: 2026-08-05T14:53:36Z
heartbeat_at_utc: 2026-08-03T14:59:44Z

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
current_validation: "ACTIVE on d2a4fda2ee2089a6b7606a9e9b0109012ed6f681; clean declared write set; no formal shadow outcomes accessed or executed."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L04--Yijun.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T02:53:36Z
next_24h: "Implement and synthetically qualify all eight frozen estimands, selection/sensitivity surfaces, and registered fail-closed bounds without formal execution."
handoff_eta: 2026-08-04T08:53:36Z

final_commit: null
reviewer: null
review_result: null
notes: "L04 may use synthetic fixtures only. It must not execute the 36 formal shadow assays, access their outcomes, or overlap L03 replay implementation files."
```
