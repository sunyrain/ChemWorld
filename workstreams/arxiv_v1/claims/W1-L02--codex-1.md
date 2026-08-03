# Work I Task Claim

```yaml
task_id: W1-L02
title: "Audit reconstructability of all 36 pre-discard states"
status: REVIEW

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T14:06:52Z
lease_expires_at_utc: 2026-08-05T14:06:52Z
heartbeat_at_utc: 2026-08-03T14:38:35Z

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
  - "Verify two independent checkpoint captures per cell within the single full generation"
  - "uv run pytest -q tests/test_latent_terminal_reconstructability.py"
  - "uv run ruff check src/chemworld/eval/latent_terminal_reconstructability.py scripts/audit_work_i_latent_terminal_reconstructability.py tests/test_latent_terminal_reconstructability.py"
  - "uv run mypy src/chemworld/eval/latent_terminal_reconstructability.py scripts/audit_work_i_latent_terminal_reconstructability.py"
  - "git diff --check"

completed_since_last_heartbeat:
  - "Matched all 53 indexed raw files and 127883533 bytes to the frozen terminal index"
  - "Replayed all 10 source trajectories and reconstructed all 36 pre-discard checkpoints"
  - "Matched historical resource receipts/ledger hashes and independent hidden-state/resource checkpoint hashes"
  - "Published only checkpoint hashes and gates; executed zero shadow terminals, read zero latent discard scores, and made zero provider calls"
current_validation: "PASS: 36/36 reconstructable; report SHA-256 995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857; 4 focused tests; Ruff; Mypy; git diff --check. The single full generation already performs two independent checkpoint replays per cell; a duplicate 150-second full --check was intentionally not repeated."
files_touched:
  - workstreams/arxiv_v1/claims/W1-L02--codex-1.md
  - src/chemworld/eval/latent_terminal_reconstructability.py
  - scripts/audit_work_i_latent_terminal_reconstructability.py
  - tests/test_latent_terminal_reconstructability.py
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-04T14:38:35Z
next_24h: "Await independent review; continue sequentially to L03 without executing formal shadow assays"
handoff_eta: 2026-08-03T14:38:35Z

final_commit: "2d29d22f1ae4f68a6f30590b987597d909ec68f4"
reviewer: null
review_result: null
notes: "No provider calls, shadow terminal evaluations, latent scores, manuscript edits, or global evidence regeneration are authorized. Harvey was stopped before handoff when the coordinator switched the project to single-agent execution; codex-1 will continue sequentially."
```
