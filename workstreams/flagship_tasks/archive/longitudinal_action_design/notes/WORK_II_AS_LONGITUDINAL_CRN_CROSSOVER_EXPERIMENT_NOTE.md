# Archived: Work II A-S corrected-volume common-noise crossover qualification and canary

Status: terminal development qualification, scientifically rejected before provider execution.
The corrected-volume and common-noise construction did not pass the frozen cross-world gates.

## Question

Can a twelve-round agent apply its learned partition exponent to action choices when the candidate
tradeoffs are balanced using the runtime's actual total organic volume and evaluator comparisons use
common keyed observation noise rather than independent query noise?

## Units and frozen coverage

- Correct the physical balance term to use
  `V_organic = solvent_volume_L + extractant_volume_L`; the runtime fixes solvent volume at
  `0.020 L`. Set aqueous volume to `0.060 L` and each low-coefficient action's extractant volume to
  `0.060 L`, giving total low-action organic volume `0.080 L`.
- Sort the 16 reference coefficients. For each of the four lowest coefficients, choose the largest
  unused higher coefficient whose analytically balanced high-action extractant volume lies in
  `[0.002, 0.015] L`. The balance formula is
  `Vorg_high = Vorg_low * (K_low/K_high)^1.375`, followed by
  `Vextractant_high = Vorg_high - 0.020`.
- Freeze all process conditions at `mix=180 s`, `settle=600 s`, and `450 rpm`. The resulting eight
  actions use eight distinct material pairs.
- Evaluator truth uses one common keyed observation seed within each world, shared by all eight
  candidates and both exponent laws. This is a common-random-number comparison: it removes
  query-identity noise from relative rankings while preserving the observation kernel. Participant
  campaign observations retain the normal keyed-noise contract and are not paired or denoised.
- Provider-free construction uses worlds `0..4`; prospective validation uses only the already
  exposed world `368103785`. Every contrast must reverse between exponent `1.0` and `1.75` with at
  least `0.005` score gap in every world. Each roster must also have different law-specific Top-1
  actions, Top-1 margins at least `0.005`, score ranges at least `0.03`, and linear-power Kendall tau
  no greater than `0.5`.
- All 80 construction truth executions, 16 validation truth executions, and 16 checkpoint truth
  executions require tolerance-zero exact replay.
- Only after all gates pass, run three new persistent sessions (`opaque`, `aligned_nominal`, and
  `misindexed_nominal`) in the exposed validation world. Each autonomously completes twelve
  experiments, commits checkpoints at `0/3/6/9/12`, sees candidates only after the final checkpoint,
  and submits a ranking-only recommendation.

## Measurements

- Provider-free: exact denominators and failures, corrected total-volume bindings, common-noise
  provenance, four contrast reversals and gaps, law-specific rankings, Top-1 margins, score ranges,
  Kendall tau, candidate-checkpoint collisions, and public-packet leakage.
- Provider canary: complete 36-experiment and 15-checkpoint denominators, same-thread continuity,
  final-before-reveal, selected power-law rank, Top-1, normalized regret, final-law normalized MAE,
  contrast-side choices, candidate collision, and complete trajectories.

## Pass, failure, and stop rules

- Stop without provider calls if any truth, replay, corrected-volume, common-noise, contrast, roster,
  leakage, or collision gate fails. Do not modify pairs, volumes, noise pairing, thresholds, or the
  validation world inside this block.
- If qualification passes, retain all three provider sessions and all failures. No outcome-based
  replacement or favorable rerun is allowed.
- This single exposed-world development canary diagnoses mechanism application only; it does not
  estimate arm effects or authorize formal W2-40.

## Expected outputs

Frozen protocol, corrected analytic roster, paired-noise truth and exact replay, qualification,
campaign config, three twelve-round records when qualified, complete rankings and trajectories,
machine summary, and concise Chinese report.

## Closeout

- Construction truth completed `80/80` actions with `80/80` tolerance-zero exact replays, zero
  failures, and zero provider calls.
- Correcting total organic volume and sharing one observation seed across candidates and laws did
  not recover a stable roster: only `2/20` contrast-by-world checks passed, and all five world-level
  roster checks failed.
- This is the terminal negative design outcome for the strict partition-exponent-to-action branch.
  No fourth near-duplicate crossover construction or provider canary is authorized by this block.
