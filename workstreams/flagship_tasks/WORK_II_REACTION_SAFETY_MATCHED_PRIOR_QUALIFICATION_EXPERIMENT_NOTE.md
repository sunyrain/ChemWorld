# Work II reaction-safety matched-prior qualification

Date: 2026-08-11
Status: frozen before execution

## Question and units

Can the qualified reaction-safety worlds support two participant-facing local temperature-duration
models that are matched at baseline but make distinguishable, nontrivial predictions away from it?

- Worlds: the complete public-test cohort `world_seed=0,1,2,3,4`; no seed selection.
- Independent qualification unit: one task × world.
- Provider calls: zero; participant trajectories are not read.
- Source: only the completed mechanism-oracle classified-outcome qualification. All five source
  bindings must match their recorded hashes and authorize Q2.

## Frozen reference context and surface design

For each world, select the first validation candidate after rank 1 whose score is within `0.05` of
the safe oracle optimum and whose six non-target coordinates are at least `0.05` Euclidean distance
from the optimum context. Only its non-target context is retained. Continuous controls are rounded
before execution to public, participant-readable increments: reagent `0.001 mol`, stirring `50 rpm`,
catalyst amount `0.000025 mol`, and solvent volume `0.0025 L`; nominal catalyst and solvent choices
are unchanged. Failure to find such a candidate rejects the world without relaxing the rule.

At that rounded context, execute an `11 × 11` provider-free surface:

- temperature: `370,380,...,470 K`;
- duration: `300,900,...,6300 s`;
- the even/even checkerboard cells are the frozen fitting set; all remaining cells are held out;
- every query must be classified as a committed endpoint or a dynamic physical failure. A platform
  failure invalidates the whole block and requires restart from world 0.

Fit separate centered quadratic ridge models for score and safety risk using committed safe fitting
cells. The public reference region is `420 K, 3300 s`, with tolerances `10 K` and `600 s`; this is a
fixed coarse region, not an oracle optimum. Candidate misspecifications are frozen in this order:
temperature-axis reflection, then duration-axis reflection. A reflection is around the public
reference region and is clipped to the fitting-response range, so it remains numerically plausible.
Use the first candidate that passes every gate; do not choose by participant outcome.

## Measurements and pass rules

Each world must satisfy all of the following:

- `121/121` surface queries classified, zero platform failures, at least 24 safe fitting cells and
  40 safe held-out cells;
- aligned held-out normalized MAE no greater than `0.20` for score and `0.20` for safety risk;
- aligned and misspecified predicted score differ by at most `0.05` in the frozen baseline region;
- at least 25% of safe held-out queries show a score disagreement of
  `max(0.03, 6 sigma_obs)` or a different prediction relative to the `0.35` safety limit;
- blind-label evaluation assigns the lower joint held-out error to the aligned law by at least
  `0.05` normalized-error units;
- on both sides of the reflected axis, at least three held-out queries favor the aligned law by
  `0.05` normalized-error units, and the two retained representatives are separated by at least
  four grid steps. These are two distinct falsification interventions, not repeats;
- the supplied-prior objects have identical schemas, confidence, reference context, baseline region
  and word count. They differ only in the frozen directional claim. Neither contains an arm label,
  oracle score/vector, screening seed, hidden mechanism name, exact optimum, run path or source ID;
- a deterministic, spatially balanced set of 16 safe held-out queries is frozen for D1, independently
  of which queries most favor either law;
- all five worlds pass separately. Means cannot mask a failed world.

Dynamic temperature-bound rollback is a physical/safety outcome and remains in the denominator; it
is not a platform failure. Expected outputs are an ignored raw surface root, a tracked machine
summary with exact denominators and all failures, a five-world matched-prior package, and one frozen
world-0 D1 config. D1 is not executed by this qualification block.
