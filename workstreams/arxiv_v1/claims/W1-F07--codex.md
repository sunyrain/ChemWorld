# Work I Task Claim

```yaml
task_id: W1-F07
title: "Publish machine-readable and human-readable world-fork certificates"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T05:15:58Z
lease_expires_at_utc: 2026-08-05T05:15:58Z
heartbeat_at_utc: 2026-08-03T05:18:47Z

base_commit: "352678ef5f6b191f94bc0182accb026913c73b93"
branch: work1/w1-f07-world-fork-certificate
worktree: ../ChemWorld-W1-F07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F07--codex.md
  - scripts/summarize_work_i_world_fork.py
  - tests/test_world_fork_report.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Concise content-addressed machine certificate derived only from the frozen F06 artifact.
  - Human report stating the supported claim, design, counts, outcomes, and explicit claim boundary.
  - Deterministic rebuild test binding both reports to the formal report SHA-256.
validation:
  - uv run python scripts/summarize_work_i_world_fork.py
  - uv run python scripts/summarize_work_i_world_fork.py --check
  - uv run pytest -q tests/test_world_fork_report.py
  - uv run ruff check scripts/summarize_work_i_world_fork.py tests/test_world_fork_report.py
  - git diff --check

completed_since_last_heartbeat:
  - "Derived a 15 KB machine certificate with pair-level lineage, gate, and divergence bindings."
  - "Generated a publication-facing human certificate with design, outcome, and interpretation tables."
  - "Bound both outputs to the frozen F06 content and file SHA-256 digests."
current_validation: "Deterministic machine/human rebuild, two focused tests, ruff, and git diff --check passed."
files_touched:
  - scripts/summarize_work_i_world_fork.py
  - tests/test_world_fork_report.py
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T17:15:58Z
next_24h: "Coordinator independently rebuilds both report formats and merges the certificate."
handoff_eta: 2026-08-03T05:30:00Z

final_commit: "b43a77197197696a14c99e328316cd55b66c734e"
reviewer: coordinator
review_result: "accepted after independent machine/human certificate reconstruction"
notes: "Certificate SHA-256: c4c3bce535ce5eb5b8f189c57786f1551a54829261fe68833474cf81b4beb554. The reports summarize frozen evidence without changing any qualification input."
```
