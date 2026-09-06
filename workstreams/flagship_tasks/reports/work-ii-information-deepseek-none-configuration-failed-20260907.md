# W2-87 information completeness

deepseek / development: stopped_by_user; 6 scheduled.

| Information | Analysis | Recovery / scheduled | Status counts |
| --- | --- | --- | --- |
| original | recovery | 0/2 | {"failed": 1, "unstarted": 1} |
| original | retention | 0/1 | {"unstarted": 1} |
| complete | recovery | 0/2 | {"unstarted": 2} |
| complete | retention | 0/1 | {"unstarted": 1} |

Primary: {"contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors", "mean": null, "approximate_world_bootstrap_95": null, "bootstrap_seed": 90870, "bootstrap_draws": 20000}

Aligned-prior retention is separate from recovery. Units are worlds, not queries, priors or models. Information length is part of the disclosure treatment. Current-v3 data are not a reanalysis of historical B3 runtime semantics. This block was stopped by the user for a configuration change; all attempted, interrupted and unstarted units are retained. It is excluded from the new block.

Resources:
```json
{
  "attempted_sessions": 1,
  "turns": 2,
  "scheduled_turns": 12,
  "usage_available_turns": 1,
  "usage_missing_turns": 1,
  "provider_error_turns": 0,
  "wall_seconds": 363.82800000021234,
  "wall_seconds_incomplete_sessions": 1,
  "tool_attempts": 0,
  "tool_rejections": 0,
  "tool_compute_seconds": 0,
  "input_tokens": 7695,
  "output_tokens": 44351,
  "cached_input_tokens": 256,
  "reasoning_output_tokens": 43979
}
```

All failures / unstarted:
- W2-87-development-1--opaque--deepseek--original: failed / interrupted_attempt_not_reissued
- W2-87-development-1--opaque--deepseek--complete: unstarted / None
- W2-87-development-1--aligned_nominal--deepseek--complete: unstarted / None
- W2-87-development-1--aligned_nominal--deepseek--original: unstarted / None
- W2-87-development-1--misindexed_nominal--deepseek--original: unstarted / None
- W2-87-development-1--misindexed_nominal--deepseek--complete: unstarted / None
