# Work II parametric initial-world-model pilot evaluation

Development evidence only; no formal inference or private-transfer claim.

## Exact denominators

- Participant scientific trajectories: **3/3** terminal; operationally qualified cells: **2/3**.
- Participant experiments: **12/12** complete; belief checkpoints: **12/12**.
- Held-out truth queries: **4/4** complete and **4/4** exact replay.
- Blind replays: **18/18** complete and exact replay.
- Evaluator provider calls: **0**; participant trajectories rerun: **0**.

## Arm-level results

| Arm | Best observed score | Pre prediction error | Final error | Improvement | Final prior reliability | Law error | Blind gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| opaque | 0.0552 | 0.3594 | 0.1224 | 0.2370 | NA | 0.1976 | 0.0000 |
| aligned_nominal | 0.1822 | 0.3344 | 0.0271 | 0.3074 | 0.4000 | 0.2827 | 0.0000 |
| misindexed_nominal | 0.1270 | 0.4263 | 0.0184 | 0.4079 | 0.7500 | 0.0183 | 0.0000 |

## Operational profile

The three persistent sessions recorded 87 operation attempts and 3 logical Codex turns. Provider accounting was 7,797,205 input tokens (7,507,072 cached; 290,133 uncached), 121,605 output tokens, 4 recovered MCP failures, 0 provider-error events and a maximum session time of 378.1 s.

## Development interpretation

In the misspecified arm, stated prior reliability changed from 0.70 to 0.75; the trajectory challenged reaction_duration_s, reaction_temperature_K. Held-out prediction improved by 0.4079 while its best observed endpoint exceeded the opaque endpoint by 0.0718. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction improved by 0.2370, aligned prediction improved by 0.3074, and misspecified prediction improved by 0.4079. The descriptive H3 contrast was 0.1005; it is not an inferential result.

3/3 final recommendations selected their own observed incumbent. Paired blind replay therefore checks reproducibility and action commitment but cannot show an additional recommendation-over-incumbent gain when the two targets are identical.

Machine report SHA-256: `44938f46c61a1acf3e43146bd808e2a8757ac36fbc113907fde76f4eaf8808a0`.
