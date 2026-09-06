# W2-87 information completeness

deepseek / formal: stopped_by_user; 60 scheduled.

| Information | Analysis | Recovery / scheduled | Status counts |
| --- | --- | --- | --- |
| original | recovery | 0/20 | {"failed": 1, "unstarted": 19} |
| original | retention | 0/10 | {"failed": 1, "unstarted": 9} |
| complete | recovery | 1/20 | {"completed": 1, "unstarted": 19} |
| complete | retention | 1/10 | {"completed": 1, "unstarted": 9} |

Primary: {"contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors", "mean": null, "approximate_world_bootstrap_95": null, "bootstrap_seed": 90870, "bootstrap_draws": 20000}

Aligned-prior retention is separate from recovery. Units are worlds, not queries, priors or models. Information length is part of the disclosure treatment. Current-v3 data are not a reanalysis of historical B3 runtime semantics. This block was stopped by the user for a configuration change; all attempted, interrupted and unstarted units are retained. It is excluded from the new block.

Resources:
```json
{
  "attempted_sessions": 4,
  "turns": 7,
  "scheduled_turns": 120,
  "usage_available_turns": 5,
  "usage_missing_turns": 2,
  "provider_error_turns": 0,
  "wall_seconds": 1258.3910000000615,
  "wall_seconds_incomplete_sessions": 1,
  "tool_attempts": 14,
  "tool_rejections": 9,
  "tool_compute_seconds": 0.004289999371394515,
  "input_tokens": 420813,
  "output_tokens": 146967,
  "cached_input_tokens": 334976,
  "reasoning_output_tokens": 143163
}
```

All failures / unstarted:
- W2-87-world-01--opaque--deepseek--original: failed / tool_budget_exceeded
- W2-87-world-01--aligned_nominal--deepseek--original: failed / interrupted_attempt_not_reissued
- W2-87-world-01--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-01--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-02--opaque--deepseek--complete: unstarted / None
- W2-87-world-02--opaque--deepseek--original: unstarted / None
- W2-87-world-02--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-02--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-02--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-02--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-03--opaque--deepseek--original: unstarted / None
- W2-87-world-03--opaque--deepseek--complete: unstarted / None
- W2-87-world-03--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-03--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-03--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-03--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-04--opaque--deepseek--complete: unstarted / None
- W2-87-world-04--opaque--deepseek--original: unstarted / None
- W2-87-world-04--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-04--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-04--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-04--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-05--opaque--deepseek--original: unstarted / None
- W2-87-world-05--opaque--deepseek--complete: unstarted / None
- W2-87-world-05--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-05--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-05--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-05--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-06--opaque--deepseek--complete: unstarted / None
- W2-87-world-06--opaque--deepseek--original: unstarted / None
- W2-87-world-06--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-06--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-06--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-06--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-07--opaque--deepseek--original: unstarted / None
- W2-87-world-07--opaque--deepseek--complete: unstarted / None
- W2-87-world-07--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-07--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-07--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-07--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-08--opaque--deepseek--complete: unstarted / None
- W2-87-world-08--opaque--deepseek--original: unstarted / None
- W2-87-world-08--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-08--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-08--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-08--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-09--opaque--deepseek--original: unstarted / None
- W2-87-world-09--opaque--deepseek--complete: unstarted / None
- W2-87-world-09--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-09--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-09--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-world-09--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-10--opaque--deepseek--complete: unstarted / None
- W2-87-world-10--opaque--deepseek--original: unstarted / None
- W2-87-world-10--aligned_nominal--deepseek--original: unstarted / None
- W2-87-world-10--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-world-10--misindexed_nominal--deepseek--complete: unstarted / None
- W2-87-world-10--misindexed_nominal--deepseek--original: unstarted / None
