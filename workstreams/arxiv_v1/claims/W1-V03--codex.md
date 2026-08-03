# Work I Task Claim

```yaml
task_id: W1-V03
title: "Qualify and freeze the known-policy threshold on disjoint worlds"
status: CLAIMED

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:17:59Z
lease_expires_at_utc: 2026-08-05T06:17:59Z
heartbeat_at_utc: 2026-08-03T06:17:59Z

base_commit: "acf89124715577ea743beb15731891bfb411fe73"
branch: work1/w1-v03-threshold-qualification
worktree: ../ChemWorld-W1-V03
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V03--codex.md
  - src/chemworld/eval/known_policy_threshold.py
  - scripts/qualify_work_i_known_policy_threshold.py
  - configs/benchmark/work_i_known_policy_threshold_v0.1.json
  - tests/test_known_policy_threshold.py
  - workstreams/arxiv_v1/reports/work-i-known-policy-threshold-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-known-policy-threshold-qualification-v0.1.md
shared_hot_file_requests: []

deliverables:
  - Deterministic qualification execution on worlds disjoint from formal seeds 0-4.
  - Threshold selected exactly by the frozen V02 candidate and tie-breaking rules.
  - Immutable source manifest, formal-world exclusion audit, matched-arm identity audit, and replay evidence.
  - Machine-readable threshold binding and human qualification report.
validation:
  - uv run python scripts/qualify_work_i_known_policy_threshold.py
  - uv run python scripts/qualify_work_i_known_policy_threshold.py --check
  - uv run pytest -q tests/test_known_policy_threshold.py
  - uv run ruff check src/chemworld/eval/known_policy_threshold.py scripts/qualify_work_i_known_policy_threshold.py tests/test_known_policy_threshold.py
  - uv run mypy src/chemworld/eval/known_policy_threshold.py
  - git diff --check

completed_since_last_heartbeat: []
current_validation: "V03 scope is bound to the V02 threshold firewall and excludes formal worlds by construction."
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T18:17:59Z
next_24h: "Execute disjoint qualification worlds, freeze the unique threshold and manifest hash, then hand off for independent rebuild."
handoff_eta: 2026-08-03T09:30:00Z

final_commit: null
reviewer: null
review_result: null
notes: "Qualification uses no provider calls and cannot inspect or retune against formal world seeds 0-4."
```
