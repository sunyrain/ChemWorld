# Work I Task Claim

```yaml
task_id: W1-L01
title: "Correct and re-freeze latent-terminal estimands and entry rules"
status: DONE

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T14:11:23Z
lease_expires_at_utc: 2026-08-05T14:11:23Z
heartbeat_at_utc: 2026-08-03T14:11:23Z

base_commit: "2ba42613cb8a575e47adaa4227dde8846a4ac68c"
branch: work1/w1-l01-contract-correction
worktree: "D:/Projects/ChemWorld-W1-L01-Correction"
supersedes: "workstreams/arxiv_v1/claims/W1-L01--codex-2.md"

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L01--codex-1.md
  - src/chemworld/eval/latent_terminal_contract.py
  - scripts/freeze_work_i_latent_terminal_contract.py
  - configs/benchmark/work_i_latent_terminal_contract_v0.1.json
  - tests/test_latent_terminal_contract.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-contract-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "Pre-outcome rule for campaign_oracle_regret when a frozen campaign has no discard opportunity"
  - "Standalone validator that exact-binds estimands, denominators, missingness, entry, and censoring rules"
  - "Complete mandatory censoring/unresolved-outcome sensitivity surface for every estimand"
  - "Regenerated machine/human contracts without accessing hidden states or latent outcomes"
validation:
  - "uv run python scripts/freeze_work_i_latent_terminal_contract.py"
  - "uv run python scripts/freeze_work_i_latent_terminal_contract.py --check"
  - "uv run pytest -q tests/test_latent_terminal_contract.py"
  - "uv run ruff check src/chemworld/eval/latent_terminal_contract.py scripts/freeze_work_i_latent_terminal_contract.py tests/test_latent_terminal_contract.py"
  - "uv run mypy src/chemworld/eval/latent_terminal_contract.py scripts/freeze_work_i_latent_terminal_contract.py"
  - "git diff --check"

completed_since_last_heartbeat:
  - "Defined campaign_oracle_regret over the 9 frozen discard-opportunity cells and retained cell-02 as a null no-opportunity census row"
  - "Exact-bound estimands, denominators, aggregation, missingness, censoring sensitivity, and evidence-entry rules in the standalone validator"
  - "Defined mandatory unresolved-outcome bounds and censoring rows for all eight estimands"
  - "Regenerated the machine and human contracts without shadow execution or latent-outcome access"
current_validation: "PASS: deterministic generation/check; 8 focused tests; Ruff; Mypy; git diff --check. Contract SHA-256 55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30; population SHA-256 unchanged at ab35b3214c4cdf9003afff3f0d6b9205e615b5c76afa4664677bc9b95c19a9ae."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L01--codex-1.md
  - src/chemworld/eval/latent_terminal_contract.py
  - scripts/freeze_work_i_latent_terminal_contract.py
  - tests/test_latent_terminal_contract.py
  - configs/benchmark/work_i_latent_terminal_contract_v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-contract-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:11:23Z
next_24h: "Await independent review when the coordinator permits a reviewer; L02 may proceed because its dependency is none"
handoff_eta: 2026-08-03T14:15:00Z

final_commit: "4a0aaa62b5c854ae6e2489f636b3029ac546db46"
reviewer: null
review_result: null
notes: "Coordinator takeover after an independent CHANGES_REQUESTED verdict and the user's single-agent directive. No formal shadow execution, hidden-state read, or latent-outcome read is authorized."
```
