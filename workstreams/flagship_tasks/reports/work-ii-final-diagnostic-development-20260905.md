# Work II final B3 diagnostic

Phase: development. Status: terminal. Scheduled: 12; counts: {"completed": 10, "failed": 2}.

| Model | Tool | Complete / scheduled | Joint recovery | Mean regret | Top-1 |
| --- | --- | --- | --- | --- | --- |
| gpt | off | 3/3 | 1/3 | 0.42201 | 1/3 |
| gpt | on | 3/3 | 0/3 | 1.00000 | 0/3 |
| deepseek | off | 2/3 | 0/3 | 0.98086 | 0/3 |
| deepseek | on | 2/3 | 0/3 | 0.98086 | 0/3 |

Tool-on minus off joint recovery: -0.16667; approximate world-bootstrap 95% interval: None.

1 reused world(s); no additional independent worlds or physics. Only two selected model configurations. Aligned priors already contain the correct exponent: retention is distinct from discovery. Minimal-schema history comparisons do not identify a randomized schema effect. Public numerics is a system intervention; the old privileged simulator qualification does not prove public-only identifiability.

## Resources

Token totals are reported CLI usage. Missing usage or interrupted/recovered requests may leave unreported consumption; these totals are lower bounds in affected groups.

```json
[
  {
    "model": "gpt",
    "tool": "off",
    "attempted_sessions": 3,
    "turns": 6,
    "usage_available_turns": 6,
    "usage_missing_turns": 0,
    "provider_error_turns": 0,
    "usage_potentially_incomplete_turns": 0,
    "input_tokens": 102374,
    "output_tokens": 12804,
    "cached_input_tokens": 0,
    "reasoning_output_tokens_reported": 9239,
    "reasoning_usage_available_turns": 6,
    "wall_seconds": 223.56299999984913,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "gpt",
    "tool": "on",
    "attempted_sessions": 3,
    "turns": 6,
    "usage_available_turns": 6,
    "usage_missing_turns": 0,
    "provider_error_turns": 0,
    "usage_potentially_incomplete_turns": 0,
    "input_tokens": 105076,
    "output_tokens": 15613,
    "cached_input_tokens": 0,
    "reasoning_output_tokens_reported": 12042,
    "reasoning_usage_available_turns": 6,
    "wall_seconds": 310.1099999996368,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "deepseek",
    "tool": "off",
    "attempted_sessions": 3,
    "turns": 6,
    "usage_available_turns": 6,
    "usage_missing_turns": 0,
    "provider_error_turns": 1,
    "usage_potentially_incomplete_turns": 1,
    "input_tokens": 643900,
    "output_tokens": 174190,
    "cached_input_tokens": 569600,
    "reasoning_output_tokens_reported": 168989,
    "reasoning_usage_available_turns": 6,
    "wall_seconds": 1321.5470000000205,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "deepseek",
    "tool": "on",
    "attempted_sessions": 3,
    "turns": 6,
    "usage_available_turns": 6,
    "usage_missing_turns": 0,
    "provider_error_turns": 1,
    "usage_potentially_incomplete_turns": 1,
    "input_tokens": 386783,
    "output_tokens": 214815,
    "cached_input_tokens": 265472,
    "reasoning_output_tokens_reported": 210060,
    "reasoning_usage_available_turns": 6,
    "wall_seconds": 1646.5160000000615,
    "tool_attempts": 3,
    "tool_compute_seconds": 0.002425899961963296,
    "tool_rejections": 0
  }
]
```

## All failures / unstarted units

- A_S_B3--partition-discovery--seed0--aligned_nominal--r1--deepseek--off: failed / provider_failure
- A_S_B3--partition-discovery--seed0--aligned_nominal--r1--deepseek--on: failed / provider_failure
