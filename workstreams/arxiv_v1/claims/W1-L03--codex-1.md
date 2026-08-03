# Work I Task Claim

```yaml
task_id: W1-L03
title: "Implement prefix-identity replay and terminal branch replacement"
status: CLAIMED

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T14:06:52Z
lease_expires_at_utc: 2026-08-05T14:06:52Z
heartbeat_at_utc: 2026-08-03T14:06:52Z

base_commit: "bc6c02ac089acb088a3c60af171913776c397b50"
branch: work1/w1-l03-prefix-replay
worktree: "D:/Projects/ChemWorld-W1-L03"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-L03--codex-1.md
  - src/chemworld/eval/latent_terminal_replay.py
  - scripts/qualify_work_i_latent_terminal_replay.py
  - tests/test_latent_terminal_replay.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-replay-qualification-v0.1.json
shared_hot_file_requests: []

deliverables:
  - "Fail-closed exact-prefix replay primitive bound to the frozen L01 unit identities"
  - "Evaluator-only replacement of discard_batch by one final_assay terminal branch without chemistry/resource mutation"
  - "Synthetic qualification receipts covering identity, ordinal, keyed-noise, resource, mutation, and provider-zero gates"
validation:
  - "uv run python scripts/qualify_work_i_latent_terminal_replay.py"
  - "uv run python scripts/qualify_work_i_latent_terminal_replay.py --check"
  - "uv run pytest -q tests/test_latent_terminal_replay.py"
  - "uv run ruff check src/chemworld/eval/latent_terminal_replay.py scripts/qualify_work_i_latent_terminal_replay.py tests/test_latent_terminal_replay.py"
  - "uv run mypy src/chemworld/eval/latent_terminal_replay.py scripts/qualify_work_i_latent_terminal_replay.py"
  - "git diff --check"

completed_since_last_heartbeat: []
current_validation: "Claim registered on main before implementation"
files_touched:
  - workstreams/arxiv_v1/claims/W1-L03--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T16:06:52Z
next_24h: "Implement and synthetically qualify replay/branch replacement without formal shadow execution"
handoff_eta: 2026-08-04T04:06:52Z

final_commit: null
reviewer: null
review_result: null
notes: "L03 may use the frozen L01 contract but may not execute the 36 formal shadow assays or read their latent outcomes; L05 owns formal qualification/freeze/execution."
```
