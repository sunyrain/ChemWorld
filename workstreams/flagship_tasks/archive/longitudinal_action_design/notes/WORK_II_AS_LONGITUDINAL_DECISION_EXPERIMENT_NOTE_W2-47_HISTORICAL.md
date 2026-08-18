# Work II A-S twelve-round comprehensive decision matrix

Status: historical protocol diagnostic only; superseded by W2-48. The feature-only terminal packet
did not disclose the complete executable candidate plans and must not be restored as a current
action-quality design.

## Question

After one persistent agent autonomously completes twelve partition experiments, how well can it
rank and select among eight newly revealed realistic actions, and do action quality, mechanism
accuracy, and exploration breadth change together across initial-model arms and independent worlds?

## Units and coverage design

- Five fresh partition worlds, each containing matched `opaque`, `aligned_nominal`, and
  `misindexed_nominal` arms: 5 independent clusters, 15 persistent sessions, and 180 autonomous
  participant experiments.
- Every session uses one unchanged thread, twelve participant-chosen experiments, and typed belief
  checkpoints at `0/3/6/9/12`. No protocol-owned experiment or evidence packet enters the campaign.
- The final checkpoint commits before candidate reveal. The agent then receives eight feasible,
  multidimensional actions and returns one complete ranking plus a Top-1 selection. Per-candidate
  numeric predictions are not requested.
- Candidate packets are outcome-blind. For each world, an independent public packet seed hashes the
  16 nominal solvent-extractant pairs; the first eight pairs are assigned a balanced schedule that
  uses all four volume regimes twice and both mixing regimes four times. Hidden truth, hidden rank,
  checkpoint outcomes, and participant outcomes cannot affect candidate selection.
- The same packet is shown to all three arms within a world. Exact candidate execution during the
  campaign is retained and labelled as direct support; it is not replaced. Overall decision quality
  remains in the primary denominator, while unseen-action generalization is reported separately.

## Experiment matrix

| Item | Frozen denominator |
|---|---:|
| Independent world clusters | 5 |
| Prior arms per world | 3 |
| Persistent sessions | 15 |
| Autonomous experiments per session | 12 |
| Participant experiments | 180 |
| Checkpoints per session | 5 |
| Candidate actions per world | 8 |
| Candidate truth executions | 40 |
| Checkpoint truth executions | 80 |
| Provider-free truth and exact replay | 120 + 120 |

## Measurements

- Primary action endpoint: within-world raw regret of the selected action. Primary paired contrasts
  are `misindexed - aligned` and `opaque - aligned`; all five clusters remain in the denominator.
- Secondary action endpoints: selected rank, Top-1, normalized regret, selected-minus-candidate-mean
  score, complete-ranking Kendall tau, candidate score range, and exact candidate overlap.
- Mechanism is measured separately from action: checkpoint held-out prediction error, final mechanism
  family, exponent error, executable-law normalized MAE, and calibration on the 16 frozen queries.
- Exploration diagnostics include unique recipe count, solvent-extractant pair coverage, intervention
  axis coverage, exact repeats, selected-action pair support, and candidate-neighbourhood support.
  Cross-cell mechanism-regret and exploration-regret associations are descriptive, not causal
  mediation claims.
- Five independent clusters can distinguish a one-world accident from a repeated directional
  pattern, but they do not support a high-powered population claim. Report all five paired effects
  and direction consistency rather than treating nested experiments as independent samples.

## Pass, failure, and stop rules

- Before provider calls, all 40 candidate and 80 checkpoint truth queries must complete with
  tolerance-zero exact replay. Candidate packets must satisfy their public coverage contract and
  contain no truth-derived field or checkpoint-query collision.
- Low candidate score range is measured and retained; it does not trigger seed or candidate
  replacement. Participant, schema, provider, and scientific failures remain in the scheduled
  denominator.
- W2-43 already validates the twelve-round same-thread, checkpoint-before-reveal, and ranking-only
  provider interface. The new packet generator requires provider-free semantic validation, not a
  new paid schema canary.
- Changing worlds, packet seeds, rounds, arms, candidate generation, reveal timing, primary endpoint,
  or failure rules after the first provider operation requires a new block. This note alone never
  authorizes provider execution or paper-level claims.

## Expected outputs

One machine-readable protocol, deterministic outcome-blind candidate packets, provider-free truth
and replay, 15 retained cell records when separately authorized, a machine summary with exact
denominators and failures, a Chinese analysis report, and bounded Paper 2 claim updates.
