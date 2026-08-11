# Work II mechanism-oracle classified-outcome qualification

Date: 2026-08-11
Status: frozen before execution

## Question and units

After separating evaluator reliability from dynamic physical feasibility, does
`reaction-safety-constrained` expose in every preregistered world a safe, reproducible
oracle-relative high-quality basin with identifiable local laws?

- Worlds: complete public-test cohort `world_seed=0,1,2,3,4`; no seed selection.
- Independent unit: one task × world.
- Provider calls: zero; participant/provider trajectories are not read.
- The v0.1 `1/5` rejection remains immutable. Existing raw outcomes are development evidence only;
  v0.2 reruns the complete block from world 0.

## Frozen classification-only correction

Search, recipe contract, seeds, optimizer, local grid, perturbations, validation candidates, observed
replicates and every scientific threshold are identical to v0.1. The only changed gate is outcome
classification:

1. `completed`: every recipe operation commits and evaluator-owned noiseless metrics are returned;
2. `physical_failure`: the public recipe is schema-valid, runtime execution reaches a dynamic
   constitution boundary, and the failed operation/check is recorded;
3. `platform_failure`: payload/compiler mismatch, unclassified exception, missing optimizer request
   or generation, observation failure, or replay failure.

Every unique mechanism request must end in class 1 or 2. Class 2 is ranked as physically infeasible,
excluded from score/metric distributions, retained in the machine summary, and never retried or
replaced. Any class-3 outcome invalidates the task block and requires restart from world 0.
Committed-endpoint fraction and physical-failure fraction are diagnostics, not pass gates.

## Unchanged scientific gates

For every world:

- 128 deterministic balanced initial members and all 20 differential-evolution generations;
- 24/24 independent noisy validation executions and exact replay, with at least 7/8 complete
  candidate groups;
- finite safe oracle optimum and observed median within `max(0.05, 6 sigma_obs)`;
- safe `P90(score)-P10(score) >= max(0.10, 6 sigma_obs)` and primary-metric range `>= 0.10`;
- at least five relative-high-quality local points spanning `>=0.05` on both target coordinates and
  containing an interior point;
- identifiable slope, curvature, interaction or safety crossing above `max(0.03, 6 sigma_obs)`;
- at least 5% retained completed mechanism evaluations in risk `[0.30,0.40]`, with the oracle optimum
  below the `0.35` limit;
- all five worlds pass separately. Historical threshold reachability remains diagnostic only.

## Failure and outputs

Expected outputs are an ignored raw root, a tracked machine summary with exact classified,
physical-failure, platform-failure, validation and replay denominators, and a Q2 go/no-go decision.
No provider, prior construction or D1 run is authorized unless all five worlds pass v0.2.
