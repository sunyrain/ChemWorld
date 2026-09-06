# W2-87 information completeness

gpt / formal: terminal; 60 scheduled.

| Information | Analysis | Recovery / scheduled | Status counts |
| --- | --- | --- | --- |
| original | recovery | 6/20 | {"completed": 20} |
| original | retention | 8/10 | {"completed": 10} |
| complete | recovery | 20/20 | {"completed": 20} |
| complete | retention | 10/10 | {"completed": 10} |

Primary: {"contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors", "mean": 0.7, "approximate_world_bootstrap_95": [0.45, 0.95], "bootstrap_seed": 90870, "bootstrap_draws": 20000}

Aligned-prior retention is separate from recovery. Units are worlds, not queries, priors or models. Information length is part of the disclosure treatment. Current-v3 data are not a reanalysis of historical B3 runtime semantics.

Resources:
```json
{
  "attempted_sessions": 60,
  "turns": 120,
  "scheduled_turns": 120,
  "usage_available_turns": 120,
  "usage_missing_turns": 0,
  "provider_error_turns": 0,
  "wall_seconds": 8355.718000001041,
  "tool_attempts": 0,
  "tool_rejections": 0,
  "tool_compute_seconds": 0,
  "input_tokens": 2148201,
  "output_tokens": 395748,
  "cached_input_tokens": 472320,
  "reasoning_output_tokens": 323219
}
```

All failures / unstarted:
