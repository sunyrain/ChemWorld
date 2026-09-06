# Kimi / Qwen transport and development qualification

Development evidence. Codex: codex-cli 0.145.0.

| Model | Check | Status | Actual MCP calls | Seconds |
| --- | --- | --- | ---: | ---: |
| Pro/moonshotai/Kimi-K2.6 | native_responses | failed | n/a | 0.12 |
| Pro/moonshotai/Kimi-K2.6 | chat_tool_call | passed | n/a | 3.48 |
| Pro/moonshotai/Kimi-K2.6 | chat_tool_return | passed | n/a | 1.47 |
| Qwen/Qwen3.5-397B-A17B | native_responses | failed | n/a | 0.12 |
| Qwen/Qwen3.5-397B-A17B | chat_tool_call | failed | n/a | 0.16 |
| Qwen/Qwen3.5-397B-A17B | chat_tool_return | unstarted | n/a | -- |
| Pro/moonshotai/Kimi-K2.6 | Codex json_schema | failed | 0 | 14.86 |
| Pro/moonshotai/Kimi-K2.6 | Codex prompt_schema | passed | 2 | 17.08 |
| Qwen/Qwen3.5-397B-A17B | Codex json_schema | failed | 0 | 9.66 |
| Qwen/Qwen3.5-397B-A17B | Codex prompt_schema | failed | 0 | 0.81 |

Selected candidate: `{'label': 'kimi', 'model': 'Pro/moonshotai/Kimi-K2.6', 'schema_mode': 'prompt_schema'}`.
Third model adopted (development-qualified): **False**.
Calibration: 0/6 completed; 1 failed; 1 interrupted; 4 unstarted. Attempted turns: 2/12.

Selection follows the fixed Kimi then Qwen order, using protocol checks only.
Native API probes use forced tool selection; real Codex sessions use auto selection.
prompt_schema omits upstream response_format and validates answers on the host; it is not server-enforced strict decoding.
Provider-default reasoning is not equated to Codex medium effort. Output-item SSE events are emitted after buffering upstream output.
Failures and missing usage are retained in the paired JSON. No existing formal evidence or scientific denominators are replaced.

[Design and stopping rules](../WORK_II_PROVIDER_SELECTION_NOTE.md)

## Platform interruption

- The first Kimi calibration pre-turn reached Codex SSE idle timeout at 180.406 s.
- The upstream request remained unfinished when a second session was started.
- The configured socket timeout did not enforce a total upstream request deadline.
- The owned process tree was stopped; unfinished responses and usage are unknown.
- Raw partial stream chunks were not durable in the interrupted implementation.
- Deadline, cancellation, single-request isolation and incremental journaling were fixed and tested offline afterwards; this live block was not rerun.

## Reported resources

Direct API opportunities: 5/6 attempted, 1 unstarted. Codex smoke turns: 7/8 attempted.
Known input tokens: 32,173; known output tokens: 917; requests without usage: 6.
These token totals cover reported usage only; interrupted provider work has unknown cost.
Six-session throughput and formal-session ETA remain unknown until calibration completes.
