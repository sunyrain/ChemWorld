# Work I Task Claim

```yaml
task_id: W1-F08
title: "Complete the world-authoring contract, examples, and validator documentation"
status: CLAIMED

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:37:40Z
lease_expires_at_utc: 2026-08-05T17:37:40Z
heartbeat_at_utc: 2026-08-03T17:37:40Z

base_commit: "027db9cc798f8b01fa1c6c269483a0ed9b087f56"
branch: work1/w1-f08-world-authoring-docs
worktree: ../ChemWorld-W1-F08
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-F08--codex-1.md
  - docs/world-authoring-contract.md
  - examples/world-authoring/mechanism-fork-v0.1.json
  - examples/world-authoring/material-law-fork-v0.1.json
  - scripts/validate_work_i_world_authoring_examples.py
  - tests/test_work_i_world_authoring_examples.py
  - workstreams/arxiv_v1/reports/work-i-world-authoring-examples-v0.1.json
shared_hot_file_requests: []

deliverables:
  - "Author-facing contract distinguishing registered world components, private intervention targets, invariant public surfaces, lineage, divergence, and replay"
  - "One valid mechanism-law fork and one valid material-law counterfactual fork example bound to the frozen F01 inventory"
  - "Provider-free validator wrapper with a self-hashed validation receipt"
  - "Failure-mode documentation showing how undeclared, multi-component, public-contract, digest, lineage, and replay violations fail closed"
validation:
  - "Validate both examples through the frozen inventory and WorldForkSpec implementation"
  - "Verify the examples change exactly one declared private component and preserve every invariant component"
  - "Run focused Ruff, Mypy, pytest, deterministic receipt rebuild, and git diff --check once at handoff"

completed_since_last_heartbeat: []
current_validation: "Claim prepared on synchronized origin/main; frozen F01--F07 implementation and reports remain read-only."
files_touched:
  - workstreams/arxiv_v1/claims/W1-F08--codex-1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T19:37:40Z
next_24h: "Publish validated examples and the fail-closed authoring contract without changing frozen fork semantics."
handoff_eta: 2026-08-03T19:37:40Z

final_commit: null
reviewer: null
review_result: null
notes: "F08 is documentation and example hardening only; it does not extend the registered component inventory or modify F01--F07 protocols, source, qualification traces, or certificates."
```
