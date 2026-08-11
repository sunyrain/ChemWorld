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
| opaque | 0.4922 | 0.1958 | 0.0559 | 0.1399 | 0.0568 | not scored | 8/2 | 0/0 | 7→7 | 0.0000 |
| aligned_nominal | 0.4801 | 0.2288 | 0.0486 | 0.1803 | 0.3816 | not scored | 10/0 | 0/0 | 2→2 | 0.0000 |
| misindexed_nominal | 0.4900 | 0.1298 | 0.0532 | 0.0765 | 0.5054 | not scored | 8/2 | 0/0 | 8→None | 0.0000 |

## Operational profile

The three persistent sessions recorded 210 operation attempts and 3 logical Codex turns. Provider accounting was 2,527,792 input tokens (2,213,376 cached; 314,416 uncached), 39,585 output tokens, 0 recovered MCP failures, 0 provider-error events and a maximum session time of 542.9 s.
Participant safety outcomes were 0 public unsafe operations and 0 dynamic physical failures, with 0 resource rejections and 0 platform failures. Unsafe or physically infeasible model-selected operations remain scientific outcomes rather than platform failures.

The frozen registered temperature direction and the 16-query empirical truth direction disagree in this world. Binary direction recovery is therefore not scored; held-out prediction error and executable-law error remain valid because both are evaluated directly against exact query truths.

## Development interpretation

In the misspecified arm, stated prior reliability changed from 0.70 to 0.35; the trajectory challenged reaction_temperature_K. Held-out prediction improved by 0.0765 while its best observed endpoint trailed the opaque endpoint by 0.0023. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction improved by 0.1399, aligned prediction improved by 0.1803, and misspecified prediction improved by 0.0765. The descriptive H3 contrast was -0.1037; it is not an inferential result.

3/3 final recommendations selected their own observed incumbent. Paired blind replay checks reproducibility and action commitment.

Machine report SHA-256: `7e671cf1f1cec2f3f58b84a0ae6970aa5623156acef40ef605d5d4b629f775a8`.
