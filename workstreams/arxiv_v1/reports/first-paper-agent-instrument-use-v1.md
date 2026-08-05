# First-paper complete-agent instrument use

Status: **FAILED**

## Complete census

| Quantity | Observed | Required |
| --- | ---: | ---: |
| Lifecycles | 1 | 1 |
| Submitted actions | 16 | 1--16 |
| Trajectory records | 16 | submitted actions |
| Committed actions | 16 | submitted actions |
| Rollbacks | 0 | 0 |
| Committed terminate | 1 | >=1 |
| Committed final assay | 1 | 1 |
| Provider sessions/model calls | 1/1 | 1/1 |
| MCP step calls | 16 | submitted actions |
| Public/private leakage findings | 0 | 0 |

All submitted actions are inspected; sampling is not used as a pass gate.

## Closure and replay

- Lifecycle closed: `true`.
- Environment resources reconciled: `true`.
- Exact replay: `true`; max absolute error `0.0`.
- Input/output tokens: `517000` / `2169`.
- Per-run USD price: unavailable for cached ChatGPT subscription login; no measured zero is reported.

## Existing U04 evidence

- Current fork pairs/traces/provider calls: `6` / `24` / `0`.

## Failures

- `runner_or_provider_exception`: `{"class": "runner_or_provider_exception", "exception_type": "MethodResourceLimitError", "message_body_retained": false, "message_byte_count": 49, "message_sha256": "ef30063599b4eade80cd20c06ed3df1f0ed34e32992bea2669f597829f1441b8"}`
- `provider_token_accounting_failed`: `{"checks": ["input_within_limit"], "class": "provider_token_accounting_failed"}`
- `missing_or_failed_receipt`: `{"class": "missing_or_failed_receipt", "requirement": "provider_accounting"}`

## Claim boundary

- One complete-agent virtual-instrument usability demonstration only.
- The endpoint score is descriptive and is not a performance threshold or ranking.
- No physical-laboratory validity or general-agent claim is made.
