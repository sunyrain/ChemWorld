# First-paper complete-agent instrument use

Status: **FAILED**

## Complete census

| Quantity | Observed | Required |
| --- | ---: | ---: |
| Lifecycles | 1 | 1 |
| Submitted actions | 16 | 1--16 |
| Trajectory records | 16 | submitted actions |
| Committed actions | 15 | submitted actions |
| Rollbacks | 0 | 0 |
| Committed terminate | 1 | >=1 |
| Committed final assay | 0 | 1 |
| Provider sessions/model calls | 1/1 | 1/1 |
| MCP step calls | 16 | submitted actions |
| Public/private leakage findings | 0 | 0 |

All submitted actions are inspected; sampling is not used as a pass gate.

## Closure and replay

- Lifecycle closed: `false`.
- Environment resources reconciled: `true`.
- Declared process-time budget: `8435.453480088603` / `10440.0` s; passed `true`.
- Declared sample budget: `0.00055` / `0.001` L.
- Exact replay: `true`; max absolute error `0.0`.
- Input/output tokens: `514844` / `3070`.
- Per-run USD price: unavailable for cached ChatGPT subscription login; no measured zero is reported.

## Existing U04 evidence

- Current fork pairs/traces/provider calls: `6` / `24` / `0`.

## Failures

- `transaction_not_committed`: `{"class": "transaction_not_committed", "observed": "validation_failed", "rollback_reason": "validation_failed", "step": 16}`
- `world_event_propagation_failed`: `{"class": "world_event_propagation_failed", "step": 16}`
- `runner_or_provider_exception`: `{"class": "runner_or_provider_exception", "exception_type": "CompleteAgentQualificationError", "message_body_retained": false, "message_byte_count": 284, "message_sha256": "f945b1de76fab83cc07dee1d0931e94748c84996115d78773357764bc3127cbe"}`
- `provider_session_receipt_failed`: `{"checks": ["terminal_reason_complete", "final_payload_status_complete"], "class": "provider_session_receipt_failed"}`
- `lifecycle_closure_failed`: `{"checks": ["all_actions_committed", "exactly_one_final_assay", "complete_experiment_count_exact", "final_assay_terminated", "final_assay_not_truncated", "no_right_censoring"], "class": "lifecycle_closure_failed"}`
- `step_monitor_failed`: `{"action_count": 16, "class": "step_monitor_failed", "event_count": 16}`
- `missing_or_failed_receipt`: `{"class": "missing_or_failed_receipt", "requirement": "transaction_committed", "step": 16}`
- `missing_or_failed_receipt`: `{"class": "missing_or_failed_receipt", "requirement": "step_monitor"}`
- `missing_or_failed_receipt`: `{"class": "missing_or_failed_receipt", "requirement": "provider_accounting"}`
- `missing_or_failed_receipt`: `{"class": "missing_or_failed_receipt", "requirement": "lifecycle"}`

## Claim boundary

- One complete-agent virtual-instrument usability demonstration only.
- The endpoint score is descriptive and is not a performance threshold or ranking.
- No physical-laboratory validity or general-agent claim is made.
