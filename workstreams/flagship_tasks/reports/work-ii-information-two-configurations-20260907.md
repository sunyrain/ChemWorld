# W2-87: information completeness in two configurations

Within-configuration disclosure effects under matched stimuli and task budgets. DeepSeek Flash/low and GPT/medium are distinct configurations, not equal-compute competitors. The two models share ten worlds, not twenty independent worlds. Retention is separate from recovery. Disclosure length and paired observation noise are part of the setting. Historical Flash/high and historical B3 runtime results are not pooled here. User-authorized calendar and concurrency amendments are retained alongside the original and effective budgets; execution scheduling was not identical throughout.

| Configuration | Information | Analysis | Joint recovery / scheduled | Prediction MAE (available n) | Regret |
| --- | --- | --- | --- | --- | --- |
| deepseek-v4-flash / low | original | recovery | 3/20 | 0.046537 (18) | 0.150898 |
| deepseek-v4-flash / low | original | retention | 6/10 | 0.035376 (7) | 0.343060 |
| deepseek-v4-flash / low | complete | recovery | 17/20 | 0.006081 (17) | 0.242629 |
| deepseek-v4-flash / low | complete | retention | 10/10 | 0.005853 (10) | 0.082974 |
| gpt-5.6-sol / medium | original | recovery | 6/20 | 0.038709 (20) | 0.070974 |
| gpt-5.6-sol / medium | original | retention | 8/10 | 0.038293 (10) | 0.077820 |
| gpt-5.6-sol / medium | complete | recovery | 20/20 | 0.006055 (20) | 0.007481 |
| gpt-5.6-sol / medium | complete | retention | 10/10 | 0.006131 (10) | 0.007481 |

Primary (80 recovery sessions; ten world clusters):
```json
{
  "contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors",
  "mean": 0.7,
  "approximate_world_bootstrap_95": [
    0.525,
    0.85
  ],
  "bootstrap_seed": 90870,
  "bootstrap_draws": 20000,
  "aggregation": "equal priors within model/world; equal configurations within world; equal worlds"
}
```

Effective budgets (original budgets and scheduling amendments retained in JSON):
```json
{
  "deepseek": {
    "block_timeout_s": null,
    "provider_retries": 0,
    "session_timeout_s": 1200,
    "turn_timeout_s": 600
  },
  "gpt": {
    "block_timeout_s": 14400,
    "provider_retries": 0,
    "session_timeout_s": 1200,
    "turn_timeout_s": 600
  }
}
```

Resources by configuration (CLI-reported usage; unavailable usage is a lower bound):
```json
{
  "deepseek": {
    "attempted_sessions": 60,
    "cached_input_tokens": 13120384,
    "input_tokens": 15067287,
    "output_tokens": 3470258,
    "provider_error_turns": 1,
    "reasoning_output_tokens": 3356264,
    "scheduled_turns": 120,
    "tool_attempts": 296,
    "tool_compute_seconds": 0.11439270223490894,
    "tool_rejections": 88,
    "turns": 119,
    "usage_available_turns": 114,
    "usage_missing_turns": 5,
    "wall_seconds": 26198.56399999908,
    "wall_seconds_incomplete_sessions": 1
  },
  "gpt": {
    "attempted_sessions": 60,
    "cached_input_tokens": 332544,
    "input_tokens": 1552862,
    "output_tokens": 327180,
    "provider_error_turns": 0,
    "reasoning_output_tokens": 278923,
    "scheduled_turns": 120,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0,
    "turns": 120,
    "usage_available_turns": 120,
    "usage_missing_turns": 0,
    "wall_seconds": 8355.718000001041,
    "wall_seconds_incomplete_sessions": 0
  }
}
```

All failed sessions:
- W2-87-world-01--opaque--deepseek--original: failed / tool_budget_exceeded
- W2-87-world-01--aligned_nominal--deepseek--original: failed / interrupted_attempt_not_reissued
- W2-87-world-02--opaque--deepseek--original: failed / provider_failure
- W2-87-world-04--misindexed_nominal--deepseek--complete: failed / participant_schema_post
- W2-87-world-06--misindexed_nominal--deepseek--complete: failed / participant_schema_post
- W2-87-world-08--aligned_nominal--deepseek--original: failed / participant_schema_post
- W2-87-world-09--aligned_nominal--deepseek--original: failed / turn_timeout
- W2-87-world-09--misindexed_nominal--deepseek--complete: failed / tool_budget_exceeded
