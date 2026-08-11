# Work II parametric initial-world-model pilot evaluation

Development evidence only; no formal inference or private-transfer claim.

## Exact denominators

- Participant cells: **3/3** completed and qualified.
- Participant experiments: **12/12** complete; belief checkpoints: **12/12**.
- Held-out truth queries: **4/4** complete and **4/4** exact replay.
- Blind replays: **18/18** complete and exact replay.
- Evaluator provider calls: **0**; participant trajectories rerun: **0**.

## Arm-level results

| Arm | Best observed score | Pre prediction error | Final error | Improvement | Final prior reliability | Law error | Blind gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| opaque | 0.5876 | 0.3375 | 0.0997 | 0.2378 | NA | 0.1198 | 0.0000 |
| aligned_nominal | 0.8109 | 0.3512 | 0.3621 | -0.0108 | 0.8000 | 0.3126 | 0.0000 |
| misindexed_nominal | 0.8307 | 0.4162 | 0.4296 | -0.0134 | 0.4000 | 0.5448 | 0.0000 |

## Operational profile

The three persistent sessions recorded 74 operation attempts and 3 logical Codex turns. Provider accounting was 6,707,104 input tokens (6,473,984 cached; 233,120 uncached), 134,330 output tokens, 3 recovered MCP failures, 0 provider-error events and a maximum session time of 398.8 s.

## Development interpretation

In the misspecified arm, stated prior reliability changed from 0.70 to 0.40; the trajectory challenged current_mA, potential_V. Held-out prediction worsened by 0.0134 while its best observed endpoint exceeded the opaque endpoint by 0.2431. This separates endpoint search, prior self-report and held-out predictive correction rather than treating them as one outcome.

Across this single development world, opaque prediction improved by 0.2378, aligned prediction worsened by 0.0108, and misspecified prediction worsened by 0.0134. The descriptive H3 contrast was -0.0025; it is not an inferential result.

3/3 final recommendations selected their own observed incumbent. Paired blind replay therefore checks reproducibility and action commitment but cannot show an additional recommendation-over-incumbent gain when the two targets are identical.

Machine report SHA-256: `eb0ad71478a4980dc289ccc49d2290e88b038b82c8d62382cab8a6feb3cc6e48`.
