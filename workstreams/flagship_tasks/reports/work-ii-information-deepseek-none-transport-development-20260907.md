# W2-87 information completeness

deepseek / development: terminal; 6 scheduled.

| Information | Analysis | Recovery / scheduled | Status counts |
| --- | --- | --- | --- |
| original | recovery | 0/2 | {"failed": 2} |
| original | retention | 0/1 | {"failed": 1} |
| complete | recovery | 0/2 | {"failed": 2} |
| complete | retention | 0/1 | {"failed": 1} |

Primary: {"contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors", "mean": 0.0, "approximate_world_bootstrap_95": null, "bootstrap_seed": 90870, "bootstrap_draws": 20000}

Aligned-prior retention is separate from recovery. Units are worlds, not queries, priors or models. Information length is part of the disclosure treatment. Current-v3 data are not a reanalysis of historical B3 runtime semantics.

Resources:
```json
{
  "attempted_sessions": 6,
  "turns": 10,
  "scheduled_turns": 12,
  "usage_available_turns": 7,
  "usage_missing_turns": 3,
  "provider_error_turns": 3,
  "wall_seconds": 377.3279999999795,
  "wall_seconds_incomplete_sessions": 0,
  "tool_attempts": 15,
  "tool_rejections": 4,
  "tool_compute_seconds": 0.004169499734416604,
  "input_tokens": 206789,
  "output_tokens": 22146,
  "cached_input_tokens": 164096,
  "reasoning_output_tokens": 0
}
```

All failures / unstarted:
- W2-87-development-1--opaque--deepseek--original: failed / participant_schema_pre
- W2-87-development-1--opaque--deepseek--complete: failed / provider_failure
- W2-87-development-1--aligned_nominal--deepseek--complete: failed / provider_failure
- W2-87-development-1--aligned_nominal--deepseek--original: failed / participant_schema_post
- W2-87-development-1--misindexed_nominal--deepseek--original: failed / participant_schema_post
- W2-87-development-1--misindexed_nominal--deepseek--complete: failed / provider_failure
