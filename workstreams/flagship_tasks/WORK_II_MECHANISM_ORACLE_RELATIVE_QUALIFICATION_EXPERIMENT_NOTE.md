# Work II mechanism-oracle relative qualification

Date: 2026-08-11
Status: frozen after executable-envelope correction and before execution

## Question and units

Does a fixed ChemWorld task expose, in every preregistered world, a safe and reproducible
oracle-relative high-quality basin with identifiable local laws, even when its historical leaderboard
threshold is not calibrated to the attainable score range?

- Candidate order: `reaction-safety-constrained`, then `electrochemical-conversion`.
- Worlds: complete public-test cohort `world_seed=0,1,2,3,4`; no seed selection.
- Independent qualification unit: one task × world.
- Provider calls: zero. Participant outcomes and provider trajectories are not read.
- The completed reaction-safety Q1-v0.2 artifact is retained, but a post-run audit found that
  `403/2,560` recipes contained a rejected heat operation because the screen used the generic
  `520 K` field ceiling instead of this task's executable `470 K` vessel ceiling. Exact replay had
  reproduced those invalid actions rather than proving recipe validity. Q1-v0.2 is therefore an
  inconclusive platform-defect audit, not a scientific task-design rejection. The present block
  starts again from world 0 with every operation required to commit.

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

Reaction safety uses the corrected eight-coordinate executable-envelope contract, including
temperature `250--470 K` and duration `1--14,400 s`. Electrochemistry
uses its current nine-coordinate autonomous-open recipe contract. Target coordinates remain
temperature/duration and controlled potential/current respectively.

## Measurements and pass rules

Historical task-threshold reachability is reported but is not a pass gate. For each world, define
`S*` as the best safe noiseless oracle score, `sigma_obs` from the 24 observed validation executions,
and relative high quality as safe score at least `S* - max(0.05, 6 sigma_obs)`.

Every world must pass all of the following:

- all 128 initial-population members and 20 optimizer generations are attempted; every operation in
  a completed recipe must commit; at least 99.5% of unique mechanism evaluations and all 24
  observed validation executions complete;
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

A schema-valid public recipe that reaches a dynamic constitution boundary is retained as an
evaluator-owned physical failure, ranked behind completed safe and unsafe outcomes, and counted
against the 0.5% incomplete allowance. It is not a platform defect by itself. A rejected public
payload, compiler/runtime mismatch, missing optimizer generation, observation failure or replay
failure is a platform defect and restarts the task from world 0.

The composite-score floor fraction, historical threshold and exact optimum location are diagnostics,
not hard gates. Q2 may use only compressed local-law summaries and disagreement regions; it may not
copy the exact oracle optimum or hidden mechanism payload into a participant prompt.

## Failure and outputs

A platform defect restarts the affected task from world 0 with the same search and gates. A scientific
failure is retained and rejects that task before Q2; gates are not changed from its outcome. Expected
outputs are an ignored raw optimizer root, one tracked machine summary per task with exact evaluation
and failure denominators, and a go/no-go decision. No provider or D1 execution is authorized.

## Phase conclusion — reaction-safety v0.1

The five-world block completed in `1,800.599 s` with zero provider calls, zero platform-failure
worlds and `120/120` observed validations exact-replayed. It classified all `14,121` unique mechanism
evaluations: `13,878` reached a committed physical endpoint and `243` reached a schema-valid dynamic
constitution boundary. The frozen v0.1 decision is `1/5` worlds pass and therefore rejects Q2.

The result isolates one gate-definition problem rather than an absent scientific surface. In every
world, the safe oracle optimum, observed-optimum agreement, dynamic range, primary-metric range,
relative basin, local-law and safety-frontier gates passed. Oracle scores were `0.4008--0.4882` at
risks `0.1031--0.1504`; no point reached the historical `0.70` threshold. Relative basins contained
`38--64` grid points, safe score ranges were `0.3207--0.3727`, primary-metric ranges were
`0.6309--0.7944`, and safety-frontier counts were `273--462` per world.

World 1 passed v0.1 because its 13 physical failures left a `99.541%` committed-endpoint fraction.
Worlds 0, 2, 3 and 4 failed only `mechanism_completion_fraction`, with committed-endpoint fractions
`96.846%`, `98.052%`, `99.435%` and `97.513%`. Because every request was successfully classified and
the physical failures are part of the safety landscape, this gate conflates evaluator reliability
with physical feasibility. v0.1 remains an immutable rejection. A separately frozen v0.2 must change
only this classification gate, retain every scientific threshold, and rerun from world 0 before any
Q2 authorization.
