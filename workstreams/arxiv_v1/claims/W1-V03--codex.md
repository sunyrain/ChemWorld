# Work I Task Claim

```yaml
task_id: W1-V03
title: "Qualify and freeze the known-policy threshold on disjoint worlds"
status: DONE

owner: codex
collaborators: []
claimed_at_utc: 2026-08-03T06:17:59Z
lease_expires_at_utc: 2026-08-05T06:17:59Z
heartbeat_at_utc: 2026-08-03T06:43:56Z

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

completed_since_last_heartbeat:
  - "Executed five disjoint qualification worlds in both information arms plus exact replays: 20 campaigns, 120 signals, and 720 committed actions."
  - "Selected conversion threshold 0.007984561379998922 by the frozen midpoint-nearest-median rule, yielding 15/15 qualification branches per arm."
  - "Passed nine provenance, exclusion, finite-signal, closure, action, replay, matched-arm, routing, and zero-provider gates."
  - "Materialized an immutable source-bound machine binding and human-readable qualification report."
  - "Canonicalized audit-only state/resource evidence to 12 significant digits and zeroed sub-1e-15 solver residuals while preserving raw diagnostic values for threshold selection."
  - "Confirmed byte-identical report and binding reconstruction under Python 3.11.15 and Python 3.12.10."
current_validation: "Byte-exact execution rebuild under Python 3.11 and 3.12, six focused tests, ruff, mypy, source-manifest validation, and git diff check passed."
files_touched:
  - src/chemworld/eval/known_policy_threshold.py
  - scripts/qualify_work_i_known_policy_threshold.py
  - configs/benchmark/work_i_known_policy_threshold_v0.1.json
  - tests/test_known_policy_threshold.py
  - workstreams/arxiv_v1/reports/work-i-known-policy-threshold-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-known-policy-threshold-qualification-v0.1.md
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: 2026-08-03T18:17:59Z
next_24h: "Release the frozen binding to V04 deterministic policy implementation."
handoff_eta: 2026-08-03T06:43:56Z

final_commit: "bb2031c0e77aacb428996e239e4da484e51cac26"
reviewer: "coordinator"
review_result: "APPROVED: all nine gates pass; both supported Python runtimes reconstruct the exact frozen report and binding."
notes: "Qualification uses no provider calls and cannot inspect or retune against formal world seeds 0-4. Frozen report SHA-256: 9a928c28862099049c560b7135067ea86dc6535a7077926b66f39221abbe924e. Frozen binding SHA-256: 8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a."
```
