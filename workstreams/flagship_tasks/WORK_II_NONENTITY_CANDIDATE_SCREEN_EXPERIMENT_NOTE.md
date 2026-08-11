# Work II non-entity candidate screens

Date: 2026-08-11
Status: frozen before deterministic execution

## Question and tested units

Which additional structural and parametric initial-model interventions are sufficiently identifiable
in the executable world to justify a DeepSeek D1 participant triplet?

All screens are provider-free development diagnostics at `public-test`, `world_seed=0`, excluded from
formal and participant denominators. The candidate roster and settings below are fixed before seeing
their outcomes.

1. **Crystallization structural candidate** — reaction versus crystallization dominance.
   - Reaction mild: `340 K`, `900 s`; reaction strong: `410 K`, `7200 s`.
   - Crystallization mild: `285 K`, `900 s`; crystallization strong: `270 K`, `7200 s`.
   - Fixed catalyst `0`, solvent `0`, reagent `0.01 mol`, seed `0.005 g`.
2. **Partition structural candidate** — contact/mass-transfer versus settling/separation dominance.
   - Contact mild: mix `60 s`, `300 rpm`; contact strong: mix `600 s`, `1100 rpm`.
   - Settling mild: `120 s`; settling strong: `1200 s`.
   - Fixed solvent `0`, aqueous phase `0.015 L`, extractant `0`, extractant `0.018 L`.
3. **Reaction-safety parametric candidate** — local temperature-duration operating window.
   - Temperatures: `340, 360, 390, 420 K`.
   - Durations: `900, 1800, 3600, 7200 s`.
   - Fixed catalyst `0`, solvent `0`, reagent `0.01 mol`, catalyst `0.0003 mol`.

## Measurements

- Every recipe's final task metrics, leaderboard score, failure, trajectory hash and exact replay.
- Structural candidates: mean absolute score influence of each module and their absolute influence gap.
- Parametric candidate: highest-score and lowest-score grid cells and their score gap.
- Generated three-arm pilot config only when the frozen gate passes.

## Pass and failure rules

- Structural: 4/4 recipes complete, 4/4 exact replay and module-influence gap `>= 0.10`.
- Parametric: 16/16 recipes complete, 16/16 exact replay, distinct best/worst cells and score gap
  `>= 0.10`.
- Ties are resolved deterministically by lower temperature/duration or the declared module order.
- A failed candidate is retained as an intervention-identifiability result and receives no provider call.
- Fixing a platform defect requires the affected screen to restart from its first recipe under a new
  output identity; settings and thresholds do not change after outcomes are observed.

## Expected outputs

- one tracked machine-readable summary per candidate, with exact denominators and all failures;
- one provider-neutral three-arm pilot config for each passing candidate;
- DeepSeek-derived configs and one-world D1 triplets only for candidates that pass this screen;
- a matrix-level go/no-go summary without agent-capability claims from environment failures.
