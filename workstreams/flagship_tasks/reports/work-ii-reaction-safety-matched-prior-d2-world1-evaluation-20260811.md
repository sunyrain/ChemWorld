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
| opaque | 0.4045 | 0.1118 | 0.0351 | 0.0767 | 0.0351 | yes | 8/2 | 0/0 | 8→6 | -0.0003 |
| aligned_nominal | 0.3990 | 0.1213 | 0.0188 | 0.1025 | 0.0611 | yes | 8/2 | 4/0 | 10→10 | 0.0000 |
| misindexed_nominal | 0.4033 | 0.1386 | 0.0344 | 0.1041 | 0.0541 | yes | 10/0 | 0/0 | 2→2 | 0.0000 |

## Operational profile

The three persistent sessions recorded 210 operation attempts and 3 logical Codex turns. Provider accounting was 4,257,953 input tokens (3,738,624 cached; 519,329 uncached), 49,463 output tokens, 4 recovered MCP failures, 0 provider-error events and a maximum session time of 798.4 s.
Participant safety outcomes were 4 public unsafe operations and 0 dynamic physical failures, with 0 resource rejections and 0 platform failures. Unsafe or physically infeasible model-selected operations remain scientific outcomes rather than platform failures.

## Development interpretation

In the misspecified arm, stated prior reliability changed from 0.70 to 0.85; the trajectory challenged no registered fields. Held-out prediction improved by 0.1041 while its best observed endpoint trailed the opaque endpoint by 0.0012. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction improved by 0.0767, aligned prediction improved by 0.1025, and misspecified prediction improved by 0.1041. The descriptive H3 contrast was 0.0016; it is not an inferential result.

2/3 final recommendations selected their own observed incumbent. Paired blind replay checks reproducibility and action commitment.

Machine report SHA-256: `0d6ecb44de47f67d1e9dbd977c31d9551509194f001a73f13cbb4de170208979`.
