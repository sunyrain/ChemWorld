# Work I Task Claim

```yaml
task_id: W1-F08
title: "Complete the world-authoring contract, examples, and validator documentation"
status: REVIEW

owner: codex-1
collaborators: []
claimed_at_utc: 2026-08-03T17:37:40Z
lease_expires_at_utc: 2026-08-05T17:37:40Z
heartbeat_at_utc: 2026-08-03T17:44:05Z

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

completed_since_last_heartbeat:
  - "Published an author-facing contract for the 17-component frozen inventory, three private intervention targets, nine invariant public-contract components, lineage, divergence, execution, replay, and claim ceilings."
  - "Added compact mechanism/constitutive-law and material-law authoring examples covering both frozen intervention classes."
  - "Validated both requests through the production WorldForkSpec builder using deterministic content-addressed parent and child snapshots."
  - "Verified that each example changes exactly one target, preserves 14 other non-identity components and all nine public-contract components, and makes no execution, divergence, or performance claim."
  - "Documented ten validator stages, nine common failure modes, and the complete evidence-bundle handoff."
current_validation: "PASS: receipt f6e7076cc40c513c151604fc0bde9562953001ca41c8fb2aa9e6e9fc575896b6; inventory 654b710fcfb0a66232e4a3c6e14f1abb1dd6c24357e7eac995d23d11f64ee6da; Ruff and format; Mypy; 4 focused pytest cases; production WorldForkSpec validation; deterministic receipt rebuild; cached git diff --check."
files_touched:
  - workstreams/arxiv_v1/claims/W1-F08--codex-1.md
  - docs/world-authoring-contract.md
  - examples/world-authoring/mechanism-fork-v0.1.json
  - examples/world-authoring/material-law-fork-v0.1.json
  - scripts/validate_work_i_world_authoring_examples.py
  - tests/test_work_i_world_authoring_examples.py
  - workstreams/arxiv_v1/reports/work-i-world-authoring-examples-v0.1.json
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Await coordinator review; frozen F01--F07 implementation and evidence remain unchanged."
handoff_eta: 2026-08-03T17:44:05Z

final_commit: "859b79667ff9d5b75bdc398d51319add5677e1c2"
reviewer: null
review_result: null
notes: "F08 is documentation and example hardening only. It did not extend the registered component inventory or modify F01--F07 protocols, source, qualification traces, or certificates; synthetic example snapshots make no runtime claim."
```
