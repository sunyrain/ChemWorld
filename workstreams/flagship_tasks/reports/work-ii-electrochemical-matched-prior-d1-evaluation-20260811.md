# Work II parametric initial-world-model pilot evaluation

Development evidence only; no formal inference or private-transfer claim.

## Exact denominators

- Participant scientific trajectories: **2/3** terminal; operationally qualified cells: **0/3**.
- Participant experiments: **20/30** complete; belief checkpoints: **8/15**.
- Held-out truth queries: **16/16** complete and **16/16** exact replay.
- Blind replays: **0/18** complete and exact replay.
- Evaluator provider calls: **0**; participant trajectories rerun: **0**.

## Arm-level results

| Arm | Best score | Pre error | Final error | Improvement | Law error | Direction | Unique/repeats | Unsafe/physical | Submitted→rationale | Blind gain |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| opaque | 0.7301 | 0.2907 | 0.2907 | 0.0000 | NA | NA | 8/2 | 0/0 | None→None | NA |
| aligned_nominal | 0.7739 | 0.2503 | 0.2503 | 0.0000 | NA | NA | 8/2 | 0/0 | None→None | NA |
| misindexed_nominal | NA | NA | NA | 0.0000 | NA | NA | 0/0 | 0/0 | None→None | NA |

## Operational profile

The three persistent sessions recorded 180 operation attempts and 3 logical Codex turns. Provider accounting was 3,154,356 input tokens (2,892,544 cached; 261,812 uncached), 38,699 output tokens, 18 recovered MCP failures, 0 provider-error events and a maximum session time of 673.1 s.
Participant safety outcomes were 0 public unsafe operations and 0 dynamic physical failures, with 0 resource rejections and 0 platform failures. Unsafe or physically infeasible model-selected operations remain scientific outcomes rather than platform failures.

## Development interpretation

In the misspecified arm, stated prior reliability was unavailable; the trajectory challenged no registered fields. Held-out prediction was unchanged while its best observed endpoint was unavailable. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction was unchanged, aligned prediction was unchanged, and misspecified prediction was unchanged. The descriptive complete-case H3 contrast was NA; the frozen missing-checkpoint failure penalty gives 0.0000. Neither is an inferential result.

Only 0/3 cells committed a final recommendation. Missing recommendations are retained as method failures; the evaluator neither reconstructs nor substitutes them, and their blind replays remain scheduled but unexecuted.

Machine report SHA-256: `5884d5ca7b615d9f6e8ec86e3925da85aff8430c8129f67ab365f1768affc0dd`.
