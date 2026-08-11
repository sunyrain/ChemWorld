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
| opaque | 0.6703 | 0.3471 | 0.3202 | 0.0269 | NA | 0.4235 | 0.0000 |
| aligned_nominal | 0.5680 | 0.3592 | 0.1550 | 0.2042 | 0.7800 | 0.2377 | 0.0000 |
| misindexed_nominal | 0.2743 | 0.4200 | 0.1985 | 0.2215 | 0.0300 | 0.2421 | 0.0000 |

## Development interpretation

The misspecified arm sharply reduced its stated prior reliability after the first contradictory assay and explicitly flagged the potential field, demonstrating behavioral rejection of a wrong parametric model. It nevertheless remained below the opaque arm's best endpoint within four experiments, separating model rejection from finite-budget performance recovery.

All three final recommendations selected their own observed incumbent. Paired blind replay therefore checks reproducibility and action commitment but cannot show an additional recommendation-over-incumbent gain in this pilot.

Machine report SHA-256: `354407194068d23042bcaeb3dc76499a26609a140cd933ed4446a37df4deb9fb`.
