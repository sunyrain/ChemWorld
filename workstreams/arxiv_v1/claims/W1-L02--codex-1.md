# Work I Task Claim

```yaml
task_id: W1-L02
title: "Audit reconstructability of all 36 pre-discard states"
status: ACTIVE

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T14:06:52Z
lease_expires_at_utc: 2026-08-05T14:06:52Z
heartbeat_at_utc: 2026-08-03T14:06:52Z

base_commit: "bc6c02ac089acb088a3c60af171913776c397b50"
branch: work1/w1-l02-discard-reconstructability
worktree: "D:/Projects/ChemWorld-W1-L02"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L02--codex-1.md
  - src/chemworld/eval/latent_terminal_reconstructability.py
  - scripts/audit_work_i_latent_terminal_reconstructability.py
  - tests/test_latent_terminal_reconstructability.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.md
shared_hot_file_requests: []

deliverables:
  - "A census audit proving or rejecting exact pre-discard state reconstruction for each of the 36 frozen discard units"
  - "Per-unit prefix/action/source/resource identity gates and fail-closed unresolved receipts"
  - "Machine-readable and human-readable reports that do not execute shadow assays or access latent outcomes"
validation:
  - "uv run python scripts/audit_work_i_latent_terminal_reconstructability.py"
  - "uv run python scripts/audit_work_i_latent_terminal_reconstructability.py --check"
  - "uv run pytest -q tests/test_latent_terminal_reconstructability.py"
  - "uv run ruff check src/chemworld/eval/latent_terminal_reconstructability.py scripts/audit_work_i_latent_terminal_reconstructability.py tests/test_latent_terminal_reconstructability.py"
  - "uv run mypy src/chemworld/eval/latent_terminal_reconstructability.py scripts/audit_work_i_latent_terminal_reconstructability.py"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Single-agent implementation started after corrected L01 contract integration"
files_touched:
  - workstreams/arxiv_v1/claims/W1-L02--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:06:52Z
next_24h: "Implement the outcome-blind 36-unit reconstructability audit and hand it to independent review"
handoff_eta: 2026-08-04T02:06:52Z

final_commit: null
reviewer: null
review_result: null
notes: "No provider calls, shadow terminal evaluations, latent scores, manuscript edits, or global evidence regeneration are authorized. Harvey was stopped before handoff when the coordinator switched the project to single-agent execution; codex-1 will continue sequentially."
```
