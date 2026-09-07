# W2-87 information completeness

deepseek / formal: terminal; 60 scheduled.

| Information | Analysis | Recovery / scheduled | Status counts |
| --- | --- | --- | --- |
| original | recovery | 3/20 | {"failed": 2, "completed": 18} |
| original | retention | 6/10 | {"failed": 3, "completed": 7} |
| complete | recovery | 17/20 | {"completed": 17, "failed": 3} |
| complete | retention | 10/10 | {"completed": 10} |

Primary: {"contrast": "complete_minus_original_joint_recovery_unknown_and_wrong_priors", "mean": 0.7, "approximate_world_bootstrap_95": [0.55, 0.85], "bootstrap_seed": 90870, "bootstrap_draws": 20000}

Aligned-prior retention is separate from recovery. Units are worlds, not queries, priors or models. Information length is part of the disclosure treatment. Current-v3 data are not a reanalysis of historical B3 runtime semantics. The user authorized resuming the original configuration and calendar deadline. Only previously unattempted units resumed; all failures and interruptions remain. The user subsequently removed the block calendar deadline. This is a disclosed scheduling amendment, not an unchanged original block stopping rule. Turn/session timeouts, tool limits, coverage, failure rules and all earlier outcomes were retained. The user also authorized up to 3 concurrent independent sessions for the remaining queue. Dispatch followed original indices; completion order could differ. Rate-limit events and concurrency changes are retained.

Effective budgets: {"block_timeout_s": null, "provider_retries": 0, "session_timeout_s": 1200, "turn_timeout_s": 600}

Resources:
```json
{
  "attempted_sessions": 60,
  "turns": 119,
  "scheduled_turns": 120,
  "usage_available_turns": 114,
  "usage_missing_turns": 5,
  "provider_error_turns": 1,
  "wall_seconds": 26198.56399999908,
  "wall_seconds_incomplete_sessions": 1,
  "tool_attempts": 296,
  "tool_rejections": 88,
  "tool_compute_seconds": 0.11439270223490894,
  "input_tokens": 15067287,
  "output_tokens": 3470258,
  "cached_input_tokens": 13120384,
  "reasoning_output_tokens": 3356264
}
```

All failures / unstarted:
- W2-87-world-01--opaque--deepseek--original: failed / tool_budget_exceeded
- W2-87-world-01--aligned_nominal--deepseek--original: failed / interrupted_attempt_not_reissued
- W2-87-world-02--opaque--deepseek--original: failed / provider_failure
- W2-87-world-04--misindexed_nominal--deepseek--complete: failed / participant_schema_post
- W2-87-world-06--misindexed_nominal--deepseek--complete: failed / participant_schema_post
- W2-87-world-08--aligned_nominal--deepseek--original: failed / participant_schema_post
- W2-87-world-09--aligned_nominal--deepseek--original: failed / turn_timeout
- W2-87-world-09--misindexed_nominal--deepseek--complete: failed / tool_budget_exceeded
