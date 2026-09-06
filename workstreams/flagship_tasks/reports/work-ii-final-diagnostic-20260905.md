# Work II final B3 diagnostic

Phase: formal. Status: terminal. Scheduled: 120; counts: {"completed": 117, "failed": 3}.

| Model | Tool | Complete / scheduled | Joint recovery | Mean regret | Top-1 |
| --- | --- | --- | --- | --- | --- |
| gpt | off | 29/30 | 6/30 | 0.72821 | 0/30 |
| gpt | on | 30/30 | 7/30 | 0.66820 | 1/30 |
| deepseek | off | 29/30 | 2/30 | 0.60352 | 0/30 |
| deepseek | on | 29/30 | 2/30 | 0.63760 | 0/30 |

Tool-on minus off joint recovery: +0.01667; approximate world-bootstrap 95% interval: [-0.08333333333333333, 0.1].

5 reused world(s); no additional independent worlds or physics. Only two selected model configurations. Aligned priors already contain the correct exponent: retention is distinct from discovery. Minimal-schema history comparisons do not identify a randomized schema effect. Public numerics is a system intervention; the old privileged simulator qualification does not prove public-only identifiability.

## Resources

Token totals are reported CLI usage. Missing usage or interrupted/recovered requests may leave unreported consumption; these totals are lower bounds in affected groups.

```json
[
  {
    "model": "gpt",
    "tool": "off",
    "attempted_sessions": 30,
    "turns": 60,
    "usage_available_turns": 59,
    "usage_missing_turns": 1,
    "provider_error_turns": 1,
    "usage_potentially_incomplete_turns": 1,
    "input_tokens": 1025098,
    "output_tokens": 161123,
    "cached_input_tokens": 139520,
    "reasoning_output_tokens_reported": 125738,
    "reasoning_usage_available_turns": 59,
    "wall_seconds": 3085.9519999998156,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "gpt",
    "tool": "on",
    "attempted_sessions": 30,
    "turns": 60,
    "usage_available_turns": 60,
    "usage_missing_turns": 0,
    "provider_error_turns": 0,
    "usage_potentially_incomplete_turns": 0,
    "input_tokens": 1055087,
    "output_tokens": 185753,
    "cached_input_tokens": 115840,
    "reasoning_output_tokens_reported": 149858,
    "reasoning_usage_available_turns": 60,
    "wall_seconds": 3517.2320000000764,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "deepseek",
    "tool": "off",
    "attempted_sessions": 30,
    "turns": 60,
    "usage_available_turns": 59,
    "usage_missing_turns": 1,
    "provider_error_turns": 1,
    "usage_potentially_incomplete_turns": 1,
    "input_tokens": 2202939,
    "output_tokens": 2375119,
    "cached_input_tokens": 1245568,
    "reasoning_output_tokens_reported": 2335480,
    "reasoning_usage_available_turns": 59,
    "wall_seconds": 13379.733999999473,
    "tool_attempts": 0,
    "tool_compute_seconds": 0,
    "tool_rejections": 0
  },
  {
    "model": "deepseek",
    "tool": "on",
    "attempted_sessions": 30,
    "turns": 60,
    "usage_available_turns": 60,
    "usage_missing_turns": 0,
    "provider_error_turns": 0,
    "usage_potentially_incomplete_turns": 0,
    "input_tokens": 3968044,
    "output_tokens": 2430203,
    "cached_input_tokens": 2901376,
    "reasoning_output_tokens_reported": 2380394,
    "reasoning_usage_available_turns": 60,
    "wall_seconds": 13636.250999999233,
    "tool_attempts": 63,
    "tool_compute_seconds": 0.0266784003470093,
    "tool_rejections": 9
  }
]
```

## All failures / unstarted units

- A_S_B3--partition-discovery--seed650846081--opaque--r1--deepseek--on: failed / participant_schema_post
- A_S_B3--partition-discovery--seed110564668--opaque--r1--gpt--off: failed / provider_failure
- A_S_B3--partition-discovery--seed110564668--aligned_nominal--r1--deepseek--off: failed / provider_failure
