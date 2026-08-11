# Work II parametric initial-world-model pilot evaluation

Development evidence only; no formal inference or private-transfer claim.

## Exact denominators

- Participant scientific trajectories: **3/3** terminal; operationally qualified cells: **3/3**.
- Participant experiments: **30/30** complete; belief checkpoints: **15/15**.
- Held-out truth queries: **16/16** complete and **16/16** exact replay.
- Blind replays: **18/18** complete and exact replay.
- Evaluator provider calls: **0**; participant trajectories rerun: **0**.

## Arm-level results

| Arm | Best score | Pre error | Final error | Improvement | Law error | Direction | Unique/repeats | Unsafe/physical | Submitted→rationale | Blind gain |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| opaque | 0.4192 | 0.1088 | 0.0589 | 0.0499 | 0.0589 | no | 8/2 | 5/0 | 9→10 | 0.0000 |
| aligned_nominal | 0.4182 | 0.1052 | 0.1107 | -0.0055 | 0.3036 | no | 8/2 | 1/0 | 4→5 | -0.0448 |
| misindexed_nominal | 0.4163 | 0.1785 | 0.1361 | 0.0424 | 0.0639 | no | 8/2 | 1/0 | 6→7 | -0.0347 |

## Operational profile

The three persistent sessions recorded 210 operation attempts and 3 logical Codex turns. Provider accounting was 4,332,263 input tokens (3,910,144 cached; 422,119 uncached), 47,505 output tokens, 1 recovered MCP failures, 0 provider-error events and a maximum session time of 1003.8 s.
Participant safety outcomes were 7 public unsafe operations and 0 dynamic physical failures, with 0 resource rejections and 0 platform failures. Unsafe or physically infeasible model-selected operations remain scientific outcomes rather than platform failures.

## Development interpretation

In the misspecified arm, stated prior reliability changed from 0.70 to 0.20; the trajectory challenged reaction_temperature_K. Held-out prediction improved by 0.0424 while its best observed endpoint trailed the opaque endpoint by 0.0029. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction improved by 0.0499, aligned prediction worsened by 0.0055, and misspecified prediction improved by 0.0424. The descriptive H3 contrast was 0.0479; it is not an inferential result.

All submitted recommendation indices are retained unchanged, but the action layer is platform-confounded: each rationale's first uniquely matched score identifies the 1-based observed incumbent while the submitted index is one smaller. Blind replay uses the actual submitted index; rationale-matched indices are diagnostic only, so the blind gap must not be attributed to participant action quality.

Machine report SHA-256: `b6417882a1286a3e6f3b79f705af3386f4e7fca0dbf0556bedbd5336d41ef31b`.
