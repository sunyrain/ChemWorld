# Archived: Work II A-S longitudinal analytic-crossover action qualification and canary

Status: terminal development qualification, scientifically rejected before provider execution.
It is not formal evidence and does not inspect the fresh W2-40 worlds.

## Question

After twelve autonomous experiments and a pre-reveal final mechanism checkpoint, can an agent choose
among held-out actions deliberately placed around the crossover between a linear partition law
(`p=1.0`) and the true power law (`p=1.75`)?

## Units and frozen coverage

- Use four analytic matched contrasts, eight actions total. Sort the 16 nominal solvent-extractant
  pairs by reference partition coefficient. Pair the four lowest coefficients with the four highest
  in reverse order, yielding eight distinct material pairs.
- Fix aqueous volume at `0.020 L`, the low-coefficient action's extractant volume at `0.030 L`, and
  all process settings at `mix=180 s`, `settle=600 s`, `450 rpm`.
- For each contrast, compute the high-coefficient action's extractant volume as
  `0.030 * (K_low / K_high)^1.375`. The balancing exponent `1.375` is the midpoint of `1.0` and
  `1.75` in log space. Thus the ideal coefficient-volume term is tied at `p=1.375`, the
  low-coefficient/high-volume action is favored at `p=1.0`, and the
  high-coefficient/low-volume action is favored at `p=1.75`.
- Candidate construction is analytic and outcome-independent. Provider-free construction checks use
  worlds `0..4`; prospective validation uses only the already exposed world `368103785`. Validation
  outcomes cannot change candidates or thresholds.
- Every contrast must reverse preference between the two laws in every construction and validation
  world with at least `0.005` score gap under each law. In every world the eight-action roster must
  have different linear and power Top-1 actions, Top-1 margins of at least `0.005`, score ranges of
  at least `0.03`, and linear-power Kendall tau no greater than `0.5`.
- All 80 construction truth executions, 16 validation truth executions, and 16 power-law checkpoint
  truth executions require tolerance-zero exact replay before provider calls.
- Only if all gates pass, run three new persistent sessions (`opaque`, `aligned_nominal`,
  `misindexed_nominal`) in the exposed validation world. Each session autonomously completes twelve
  experiments, commits checkpoints at `0/3/6/9/12`, receives the candidates only after the final
  checkpoint, and submits a ranking-only recommendation.

## Measurements

- Provider-free: exact denominators and failures, analytic contrast bindings, per-law preference and
  score gap, Top-1 identity and margin, score range, Kendall tau, checkpoint collision, and public
  packet leakage.
- Provider canary: `36/36` physical-experiment denominator, `15/15` checkpoint denominator,
  same-thread continuity, final-before-reveal, full ranking, selected true power rank, Top-1,
  normalized regret, candidate collision, final-law normalized MAE, and complete trajectories.
- The primary diagnostic is alignment between the pre-reveal final mechanism law and action choice
  on exponent-sensitive tradeoffs. No terminal numeric-prediction MAE is defined in ranking-only
  mode.

## Pass, failure, and stop rules

- Stop without provider calls if any truth, replay, contrast, roster, leakage, or collision gate
  fails. Do not alter the analytic formula, pairs, thresholds, or validation world within this block.
- If qualification passes, retain all three provider sessions and all failures; do not replace or
  rerun an unfavorable scientific outcome.
- A platform fix after the first provider operation requires all three sessions to restart from their
  first unit. This single exposed-world canary cannot establish arm effects or authorize formal W2-40.

## Expected outputs

Frozen protocol, analytic roster, provider-free truth and exact replay, qualification summary,
campaign config, three twelve-round cell records when qualified, complete rankings and trajectories,
machine summary, and concise Chinese report.

## Closeout

- Construction truth completed `80/80` actions with `80/80` tolerance-zero exact replays, zero
  failures, and zero provider calls.
- The analytic balance treated `extractant_volume` as the full organic volume, while the runtime
  also contains a fixed `0.020 L` solvent contribution. The intended crossover premise therefore
  did not describe the executed physical actions.
- None of the four contrasts reversed with the frozen gap across all five construction worlds, so
  the block stopped at construction qualification. No participant session was launched.
