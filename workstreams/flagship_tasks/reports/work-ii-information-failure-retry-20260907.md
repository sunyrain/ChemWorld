# Information intervention: one retry of eight failures

All eight failed/interrupted original sessions were selected after their outcomes were known and received at most one fresh full-session attempt. This is a selected-failure reliability sensitivity check, not independent replication. The original 120-session primary, all failures and original resources remain unchanged. The virtual one-retry sensitivity is descriptive; it is not a replacement primary. No extra retry is triggered by another failure or an unfavorable scientific answer.

Status: terminal; {'completed': 8}; 8 scheduled additional sessions.

| Original session | Original failure | Retry status | Recovery / retention | Top-1 |
| --- | --- | --- | --- | --- |
| 1 | tool_budget_exceeded | completed / None | 1 | 0 |
| 4 | interrupted_attempt_not_reissued | completed / None | 1 | 0 |
| 8 | provider_failure | completed / None | 1 | 1 |
| 23 | participant_schema_post | completed / None | 1 | 1 |
| 35 | participant_schema_post | completed / None | 1 | 0 |
| 45 | participant_schema_post | completed / None | 0 | 0 |
| 52 | turn_timeout | completed / None | 1 | 0 |
| 54 | tool_budget_exceeded | completed / None | 1 | 0 |

Descriptive one-retry sensitivity (original denominator retained):

| Information | Population | Recovery / scheduled | Mean normalized regret |
| --- | --- | --- | --- |
| original | recovery | 5/20 | 0.055513 |
| original | retention | 8/10 | 0.065827 |
| complete | recovery | 20/20 | 0.095970 |
| complete | retention | 10/10 | 0.082974 |

Additional resources (missing usage is a lower bound):
```json
{
  "attempted_sessions": 8,
  "turns": 16,
  "scheduled_turns": 16,
  "usage_available_turns": 16,
  "usage_missing_turns": 0,
  "provider_error_turns": 0,
  "wall_seconds": 3404.030000000028,
  "wall_seconds_incomplete_sessions": 0,
  "tool_attempts": 35,
  "tool_rejections": 11,
  "tool_compute_seconds": 0.014796600211411715,
  "input_tokens": 2255824,
  "output_tokens": 450242,
  "cached_input_tokens": 1979776,
  "reasoning_output_tokens": 433005
}
```
