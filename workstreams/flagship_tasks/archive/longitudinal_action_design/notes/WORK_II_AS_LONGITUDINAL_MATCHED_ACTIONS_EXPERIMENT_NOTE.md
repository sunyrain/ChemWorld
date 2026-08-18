# Archived: Work II A-S longitudinal matched-action qualification and canary

Status: terminal development qualification, scientifically rejected before provider execution.
It is not formal evidence and does not consume or inspect the fresh W2-40 worlds.

## Question

After one persistent agent autonomously completes twelve partition experiments and commits its
final typed mechanism checkpoint, can it choose between held-out action tradeoffs whose correct
ordering depends specifically on whether the partition-coefficient exponent is linear (`1.0`) or
power-response (`1.75`)?

## Units and coverage design

- Candidate construction uses development worlds `0..4`. Prospective validation uses only the
  already exposed world `368103785`; validation outcomes cannot change the roster or gates.
- Start from the 64 actions in the existing 128 grid with the short fixed process condition
  (`mix=180 s`, `settle=600 s`, `450 rpm`). Thus process conditions never vary within the roster.
- Build four disjoint matched contrasts, eight actions total. Within each contrast, reference
  partition coefficient and phase-volume leverage move in opposite directions. The two actions
  must have opposite score preferences under exponent `1.0` and `1.75` in every construction
  world, with at least `0.005` score separation under each law.
- The roster must use eight distinct solvent-extractant pairs and at least two volume settings.
  Selection is deterministic from construction worlds only: eligible contrasts are ordered by
  worst-case law-separation margin, then by query ID; the first disjoint four-contrast roster
  passing the frozen roster gates is selected.
- Roster gates in every construction world and the prospective validation world are: different
  linear and power Top-1 actions, at least `0.005` Top-1 margin under each law, at least `0.03`
  score range under each law, and Kendall tau no greater than `0.5` between the two eight-action
  rankings.
- Provider-free truth executes all 64 pool actions under both laws in five construction worlds,
  then the frozen eight-action roster under both laws in the exposed validation world. All truth
  executions require tolerance-zero exact replay. The power-law validation world also executes the
  16 frozen checkpoint queries plus exact replay before any provider call.
- Only if every qualification gate passes, run three new persistent sessions in the exposed
  validation world: `opaque`, `aligned_nominal`, and `misindexed_nominal`. Each autonomously runs
  twelve experiments, submits checkpoints at `0/3/6/9/12`, sees the eight candidates only after
  the final checkpoint, and returns a ranking-only terminal recommendation.

## Measurements

- Qualification: complete truth and replay denominators, eligible contrast count, selected four
  contrasts, unique pair/volume coverage, per-law score gaps, Top-1 identities and margins, score
  ranges, Kendall tau, checkpoint-query collisions, and public-packet leakage checks.
- Provider canary: lifecycle completion, same-thread continuity, all 36 physical experiments, all
  15 checkpoints, final-checkpoint-before-reveal, complete eight-action ranking, selected power-law
  rank, Top-1, raw and normalized regret, candidate collision, final-law normalized MAE, and complete
  experiment trajectories.
- The primary diagnostic is whether action success tracks the pre-reveal final mechanism law on a
  roster constructed to distinguish exponent `1.0` from `1.75`. Ranking-only mode has no terminal
  numeric-prediction MAE.

## Pass, failure, and stop rules

- Stop without provider calls if any construction truth, validation truth, exact replay, contrast,
  roster, leakage, or collision gate fails. Do not relax thresholds or replace validation outcomes
  inside this block.
- If qualification passes, retain all three scheduled provider sessions and every scientific,
  schema, provider, or platform failure. No outcome-based replacement or rerun is allowed.
- Any platform fix after the first provider operation requires all three canary sessions to restart
  from their first unit; scientific results are never overwritten.
- Passing this single-world canary supports operational feasibility and mechanism-targeted action
  diagnosis only. It does not establish an arm effect or authorize W2-40 formal execution.

## Expected outputs

Frozen protocol, provider-free truth and exact replay, selected matched roster with contrast
bindings, validation qualification, three twelve-round campaign records when qualified, readable
machine summary, complete rankings and trajectories, and a concise Chinese report.

## Closeout

- Construction truth completed `640/640` actions with `640/640` tolerance-zero exact replays,
  zero failures, and zero provider calls.
- The 64-action fixed-process pool contained only one stable cross-world exponent-sensitive
  contrast; the frozen requirement was four disjoint contrasts using eight distinct pairs.
- The block therefore stopped at construction qualification. No validation truth, participant
  session, or provider call was launched, and the threshold was not relaxed.
