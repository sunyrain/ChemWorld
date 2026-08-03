# Work I Task Claim

```yaml
task_id: W1-L01
title: "Freeze discarded-state latent-terminal estimands and evidence-entry rules"
status: CLAIMED

owner: codex-2
collaborators: []
claimed_at_utc: 2026-08-03T07:20:50Z
lease_expires_at_utc: 2026-08-05T07:20:50Z
heartbeat_at_utc: 2026-08-03T07:20:50Z

base_commit: "bce0855ef202f00bc01d30684366dfa626267e68"
branch: work1/w1-l01-latent-terminal-contract
worktree: ../ChemWorld-W1-L01
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L01--codex-2.md
  - src/chemworld/eval/latent_terminal_contract.py
  - scripts/freeze_work_i_latent_terminal_contract.py
  - configs/benchmark/work_i_latent_terminal_contract_v0.1.json
  - tests/test_latent_terminal_contract.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-contract-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Outcome-independent estimand contract for evaluator-only replacement of each observed discard by one final-assay terminal branch after an exactly matched prefix.
  - Frozen definitions for latent terminal score, discard regret, false-discard rate, assay commitment precision, censoring, denominators, aggregation, and sensitivity analyses.
  - Explicit evidence-entry rules separating the complete mandatory report from the narrower main-text result and forbidding outcome-driven threshold or inclusion changes.
  - Machine-readable validator, deterministic freeze command, human-readable protocol, and tests bound to the existing 36-discard evidence identity without reading latent outcomes.
validation:
  - uv run python scripts/freeze_work_i_latent_terminal_contract.py
  - uv run python scripts/freeze_work_i_latent_terminal_contract.py --check
  - uv run pytest -q tests/test_latent_terminal_contract.py
  - uv run ruff check src/chemworld/eval/latent_terminal_contract.py scripts/freeze_work_i_latent_terminal_contract.py tests/test_latent_terminal_contract.py
  - uv run mypy src/chemworld/eval/latent_terminal_contract.py scripts/freeze_work_i_latent_terminal_contract.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: ""
files_touched:
  - workstreams/arxiv_v1/claims/W1-L01--codex-2.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T09:20:50Z
next_24h: "Freeze and independently validate the outcome-blind latent-terminal estimand contract without executing shadow assays."
handoff_eta: 2026-08-03T15:20:50Z

final_commit: null
reviewer: null
review_result: null
notes: "L01 defines estimands and entry rules only. L02 owns discarded-state reconstructability; L03-L04 own execution and audit implementation; L05 alone may qualify, freeze, and execute the 36 evaluator-only shadow assays."
```
