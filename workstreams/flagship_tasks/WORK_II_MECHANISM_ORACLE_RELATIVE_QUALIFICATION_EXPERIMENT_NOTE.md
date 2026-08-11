# Work II mechanism-oracle relative qualification

Date: 2026-08-11
Status: frozen before execution

## Question and units

Does a fixed ChemWorld task expose, in every preregistered world, a safe and reproducible
oracle-relative high-quality basin with identifiable local laws, even when its historical leaderboard
threshold is not calibrated to the attainable score range?

- Candidate order: `reaction-safety-constrained`, then `electrochemical-conversion`.
- Worlds: complete public-test cohort `world_seed=0,1,2,3,4`; no seed selection.
- Independent qualification unit: one task × world.
- Provider calls: zero. Participant outcomes and provider trajectories are not read.
- The completed reaction-safety Q1-v0.2 rejection remains immutable. This is a new qualification
  question and cannot overwrite or reinterpret that result.

## Frozen mechanism-oracle search

Each evaluation resets the same world and executes one valid complete recipe. The optimizer reads
only evaluator-owned noiseless mechanism truth after the terminal state: metric values, exact ledger
cost and risk, and the task scoring contract. It never receives or exports hidden species IDs, rate
constants, world parameters or private mechanism names.

For each world:

1. build a deterministic 128-member initial population spanning the full frozen recipe contract and
   all categorical combinations;
2. run bounded differential evolution for 20 generations with seed derived from task ID and world
   seed, mutation `(0.5,1.0)`, recombination `0.7`, no polishing and one worker;
3. optimize the lexicographic objective: invalid recipe, then safety violation above the task limit,
   then negative noiseless task score; retain every unique evaluated recipe and all failures;
4. around the best safe oracle point, execute an `9 × 9` target-coordinate grid over normalized
   offsets `[-0.16,0.16]` and 64 deterministic full-dimensional perturbations within `±0.08`;
5. independently execute the oracle optimum and the seven best separated safe candidates with three
   keyed-noise final-assay replicates each, with exact replay. Optimizer truth never enters these
   observed validation scores.

Reaction safety uses the already frozen eight-coordinate full-envelope contract. Electrochemistry
uses its current nine-coordinate autonomous-open recipe contract. Target coordinates remain
temperature/duration and controlled potential/current respectively.

## Measurements and pass rules

Historical task-threshold reachability is reported but is not a pass gate. For each world, define
`S*` as the best safe noiseless oracle score, `sigma_obs` from the 24 observed validation executions,
and relative high quality as safe score at least `S* - max(0.05, 6 sigma_obs)`.

Every world must pass all of the following:

- all 128 initial-population members and 20 optimizer generations are attempted; at least 99.5% of
  unique mechanism evaluations and all 24 observed validation executions complete;
- all 24 observed validation executions exact-replay, with at least 7/8 candidate recipes completing
  all three replicates;
- a finite safe oracle optimum exists and the median observed score of its three replicates is within
  `max(0.05, 6 sigma_obs)` of its noiseless score;
- safe mechanism samples have `P90(score)-P10(score) >= max(0.10, 6 sigma_obs)`, and at least one
  primary metric spans `>= 0.10`;
- the local target grid contains at least five relative-high-quality points, spans at least `0.05` on
  both target coordinates, and includes an interior point;
- the local grid exposes at least one evaluator-identifiable law above `max(0.03, 6 sigma_obs)`:
  a directional slope, curvature, target interaction or safety-frontier crossing. Sign reversal is
  not mandatory;
- reaction safety additionally has at least 5% of retained mechanism evaluations in risk
  `[0.30,0.40]`, while `S*` remains below the `0.35` safety limit;
- all five worlds pass separately. Means cannot mask a failed world.

The composite-score floor fraction, historical threshold and exact optimum location are diagnostics,
not hard gates. Q2 may use only compressed local-law summaries and disagreement regions; it may not
copy the exact oracle optimum or hidden mechanism payload into a participant prompt.

## Failure and outputs

A platform defect restarts the affected task from world 0 with the same search and gates. A scientific
failure is retained and rejects that task before Q2; gates are not changed from its outcome. Expected
outputs are an ignored raw optimizer root, one tracked machine summary per task with exact evaluation
and failure denominators, and a go/no-go decision. No provider or D1 execution is authorized.
