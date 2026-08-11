# Work II Q0–Q2 five-world oracle qualification

Date: 2026-08-11
Status: reaction-safety Q1-v0.2 invalidated by a platform defect; corrected Q1-v0.3 rerun pending

## Question and units

Can the reaction-safety and electrochemical parametric loci produce five fixed-law worlds with a
reachable, non-saturated, internally supported two-dimensional response surface from which matched,
credible and falsifiable aligned/misspecified initial models can be constructed?

- Tasks: first `reaction-safety-constrained`, then `electrochemical-conversion`.
- Worlds: the complete preregistered public-test cohort `world_seed=0,1,2,3,4`; no seed selection.
- Independent qualification unit: one task × world response surface.
- Per world: 512 provider-free recipes; none enters a participant denominator.
- Target coordinates:
  - reaction safety: reaction temperature and reaction duration;
  - electrochemistry: controlled-stage potential and current deltas, conditional on a frozen probe and
    material/formulation context selected before Q2.

## Frozen coverage design

Each world uses a deterministic scrambled Sobol design whose seed is derived from task ID and world
seed. The first 384 points of a 512-point design are the broad full-space sample. Categorical
coordinates are compiled by the existing task-recipe contract; no numeric ordering is inferred.

The remaining 128 executions are selected only from broad oracle outcomes by a frozen lexicographic
algorithm:

1. choose seven unique interior anchors from each of four strata: highest feasible score, closest to
   the task threshold, closest to the safety frontier, and largest local target-space score variation;
2. around each of the 28 anchors, execute four target-coordinate corner perturbations at normalized
   offsets `±0.04`, reflecting at `[0.02,0.98]` while leaving every non-target coordinate fixed;
3. select eight deterministic anchors spanning high-quality and frontier strata and execute two
   independent keyed-noise repeats of each, giving 16 repeat executions for noise estimation.

Thus every world contains exactly `384 broad + 112 local refinement + 16 noise repeats = 512`
executions. Raw trajectories and per-recipe rows remain under ignored `runs/`; the tracked summary
contains exact denominators, every failure, aggregate response-surface statistics and raw-report
bindings.

For reaction safety, “full-space” means the dedicated executable Q1 recipe contract rather than the
historical static-optimization pilot window. Its corrected eight coordinates are temperature
`250–470 K`, duration
`1–14,400 s`, reagent amount `0.003–0.030 mol`, stirring `100–1,200 rpm`, four unordered catalysts,
catalyst amount `0.00008–0.00055 mol`, four unordered solvents and solvent volume `0.005–0.050 L`.
The first attempted runner incorrectly inherited the old `333.15–423.15 K` and `900–7,200 s` task
recipe bounds. It was stopped on August 11, 2026 after 831/2,560 provider-free executions, before a
task summary was created. Those ignored trajectories are retained as an aborted platform-defect
attempt and never enter a Q1 denominator. The corrected reaction-safety block restarts from recipe 1
with the original Sobol namespace, adaptive algorithm and gates unchanged.

A second Q1-v0.2 run then used the generic public field ceiling `520 K`, but the task's active vessel
advertised and enforced a state-dependent `470 K` ceiling. A post-run operation audit found 403
recipes with a rejected heat action: 357 broad and 46 adaptive, distributed as 79, 73, 81, 84 and 86
across worlds 0--4. The executor had required a committed final assay but had not rejected an earlier
noncommitted operation, so exact replay reproduced the invalid actions. Q1-v0.2 is retained only as a
platform-defect audit. Q1-v0.3 restarts at world 0 with the corrected executable envelope and requires
every operation in every completed recipe to commit.

## Measurements and gates

Q0 records that the target and coverage coordinates exist in the dedicated Q1 recipe schema, their
physical bounds match the frozen contract, they compile into permitted operations, affect a measured
endpoint, and have a finite task threshold and safety contract.

Q1 records score and primary-metric distributions, safety risk, floor/ceiling fractions, target and
full-space coordinates, exact replay, threshold reachability, top-region boundary location, connected
high-quality basin size, local target gradients/interactions, repeat-derived noise and cross-world
heterogeneity. Frozen pass rules are:

- 512/512 recipes with every operation committed, 512/512 completed final assays and 512/512 exact
  replay in every world;
- safe score-threshold recipes are at least 1% of valid recipes and at least five in absolute count;
- feasible `P90(score)-P10(score) >= 0.15`;
- at least one primary-metric range is `>= max(0.10, 3 sigma_noise)`;
- score floor (`<=1e-9`) and ceiling (`>=1-1e-9`) fractions are each at most 20%;
- the top 5% contains a point interior on both target coordinates (`0.10–0.90` normalized);
- threshold-reaching feasible recipes contain a connected full-space component of at least five
  points at normalized Euclidean distance `<=0.15`;
- at least two local anchor families exceed the score effect gate and show either a target-gradient
  sign reversal across condition slices or a repeatable interaction contrast;
- reaction safety additionally has at least 5% of valid recipes in safety risk `[0.30,0.40]` and a
  non-isolated score-threshold region below the `0.35` safety limit;
- all five worlds pass separately; averages cannot mask a failed world.

Q2 runs only after Q1 passes. It must select a reference context lexicographically from qualified
interior basins, construct word-count/schema/confidence-matched aligned and misspecified laws, keep
baseline predicted utility within `0.05`, create disagreement on at least 25% held-out queries, expose
at least two separated falsification regions requiring different interventions, and pass a blind
label/leakage audit. Q2 does not use participant outcomes.

## Failure and outputs

Any failure rejects the complete task cohort at the failed gate. Platform defects require the entire
affected Q1 task block to restart from recipe 1 with the same design and thresholds. Scientific
failures are retained and are not repaired by changing seeds, surfaces or gates.

Expected outputs are one raw five-world response-surface root, one readable tracked JSON summary per
task, a Q0/Q1 go/no-go decision, and—only after 5/5 Q1 pass—a separately frozen Q2 prior-pair artifact
and D1 config. No provider call is authorized by this note.

## Phase conclusion — reaction safety Q1-v0.2

No scientific phase conclusion is authorized. Although Q1-v0.2 reported `2,560/2,560` final assays
and exact replays, 403 recipes contained a rejected heat operation. That defect contaminated broad
coverage, adaptive-anchor selection, floor fractions, local families and the `0/5` decision. The
artifact remains immutable as a development audit, but none of those outcome statistics may support
a task-design rejection. The corrected Q1-v0.3 block must rerun from world 0 before these gates can
be interpreted. The separately frozen mechanism-oracle relative qualification does not overwrite or
retroactively repair Q1-v0.2.
