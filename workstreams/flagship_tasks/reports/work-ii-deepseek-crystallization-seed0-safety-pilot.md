# Work II DeepSeek crystallization seed-0 safety pilot

Date: 2026-08-10
Status: passed as development operational calibration; not a formal or scientific result

## Scope

- Task: `reaction-to-crystallization`.
- Units: world seed 0 × `opaque` / `aligned_nominal` / `misindexed_nominal`.
- Execution: one persistent DeepSeek `deepseek-v4-flash` Codex session per cell, four complete
  experiments per session, with the three prior arms run concurrently.
- Source: `runs/development/work-ii-deepseek-crystallization-seed0-pilot-detached-7236def5`.

## Exact result

| Prior arm | Cells | Experiments | Committed operations | Resource rejections | Exact replay | Process time | Cumulative input | Cached input | Uncached input | Output | Cell wall time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opaque | 1/1 | 4/4 | 46/46 | 0 | 46/46 | 77,520 s | 4,581,360 | 4,448,256 | 133,104 | 29,484 | 297.8 s |
| aligned nominal | 1/1 | 4/4 | 46/46 | 0 | 46/46 | 117,120 s | 5,033,061 | 4,899,328 | 133,733 | 39,700 | 385.3 s |
| misindexed nominal | 1/1 | 4/4 | 40/40 | 0 | 40/40 | 117,120 s | 4,410,197 | 4,291,456 | 118,741 | 50,876 | 461.7 s |
| **Total** | **3/3** | **12/12** | **132/132** | **0** | **132/132** | — | **14,024,618** | **13,639,040** | **385,578** | **120,060** | **462.8 s matrix wall** |

All three cell qualifications and current-code physical replay/execution audits passed. The run
had no terminal cell failure and no provider error event. It retained two recovered MCP validation
failures: one `commit_belief_snapshot` `ValueError` in the opaque arm and one in the aligned arm.
The misindexed arm had none. These are included in the operational denominator and are not counted
as scientific operations.

Approximately 97.3% of cumulative input was served from cache. This reflects context reuse in each
persistent session, not repeated model output; output tokens were 120,060 across all three cells.

## Expansion guardrail decision

The maximum observed cell stayed within the frozen 20% pilot-headroom thresholds used for a later
five-seed readiness decision: 5.6M cumulative input, 800k uncached input, 80k output and 1,440 s
elapsed. The recovered-MCP ceiling is one per cell and the provider-error ceiling is zero.

The runtime now also freezes a 1,800 s total session wall limit, at most one recovered MCP tool
failure and zero provider error events. Crossing any live limit interrupts the session before the
next physical operation and retains an interruption receipt. Missing operational receipt fields
fail qualification instead of defaulting to zero.

Exact token usage is emitted only when the provider turn completes, so exact in-flight token
termination is not available on this Responses event stream. Token risk is therefore bounded by
the seed-0 headroom gate and fail-closed post-session accounting, while wall time, MCP failures and
provider errors are bounded live.

No five-seed provider run is authorized by this report alone. Expansion requires a clean committed
worktree and a passing readiness receipt that hash-binds this pilot and replays its trajectories
with current code.

## Artifact bindings

- `matrix_report.json`: `33d038e60a1fa1d2250f9aa668274b723ffacb89c47888660f5ed8b7e35fd29d`
- opaque `summary.json`: `21dc562bf674360cc7f0858698dbb49e3260483441e5e8175df6773c58752dc4`
- opaque `trajectory.jsonl`: `8ac86c46266ac5881477ac8cad98b6779738f6d3669a0cd2a66542163966029c`
- aligned `summary.json`: `17fe666db2ac7b4f15f9edd96cba1c1ad93d1b6ee769f4571cc6ef8dbb45fdf5`
- aligned `trajectory.jsonl`: `b87b0b0be75db71327378df96d263efbf2259b535499ad9a25cfee120017f1d7`
- misindexed `summary.json`: `742c6afc9dbd378480b87cc3d08a6689c200d08d090ab31ea23c49f984c3cffc`
- misindexed `trajectory.jsonl`: `b009f9a07f3ebb074ead1cab289224388410b8d1bb34e5e1ae48e2deac11c201`

The matrix metadata records source commit `7236def515ace368cdfa9748821ff360dbc3ac78`. The pilot is
used as a hash-bound observed-resource calibration and current-code replay input; it is not evidence
that the subsequently added live interruption fields were present during that provider execution.
