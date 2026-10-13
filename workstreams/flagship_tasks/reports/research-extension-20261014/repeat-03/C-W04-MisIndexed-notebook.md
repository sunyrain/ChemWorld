# repeat-03 / C-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:20:39.421817+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the nominal dossier, solvent S2 should favor the objective because its lower solubility and nucleation tendency plus higher growth and lower impurity occlusion should improve recovery, size, fines, and purity relative to S0. This may be overturned by fixed-world residuals.

## H2 [tentative]
Moderate seeding followed by controlled cooling and a low-temperature growth hold should reduce spontaneous fines versus unseeded/rapid cooling, while extending the cold hold should raise crystal recovery. Excess seed may inflate number-weighted fines and is seed-excluded from yield.

## H3 [tentative]
A high-activity catalyst at sufficient reaction temperature/time should raise target loading before crystallization, but overheating/overholding may create degradation and lower crystal purity. Initial scouting will test C1/S2 under moderate thermal conditions; subsequent batches will vary reaction and crystallization history.

Predicted first-batch outcome: measurable crystallization recovery above the 0.10 feasibility target, purity at least 0.80, and fines at or below 0.50 if crystals form. A failure would trigger solvent/catalyst and supersaturation-history screening.

## Revision 2

Recorded: 2026-10-13T18:22:23.686946+00:00; available public operations: 52; reviewed through: runner-operation-0052.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 is preferred over S3 for crystallization under 0.05 g seeding and long staged cooling. S2 batches 2–3 gave final crystal recovery about 0.419–0.429 with fines about 0.388–0.396, whereas S3 batch 4 gave lower recovery about 0.398 and fines about 0.557 (events runner-operation-0026, -0039, -0052). The comparison is confounded by catalyst/temperature, so it supports process selection rather than a pure solvent causal effect.

## H2 [supported in tested scope]
Relative to batch 1 (0.02 g seed, interrupted cold history), 0.05 g seed plus continuous long staged cooling produced markedly lower observed fines and somewhat higher recovery in batches 2–3 (events runner-operation-0014, -0026, -0039). Seed dose and thermal history are confounded. Prediction: retaining 0.05 g seed and avoiding ambient warming should usually satisfy fines <=0.50 in S2.

## H3 [unresolved]
Catalyst and reaction conditions change reaction selectivity/yield, but crystallization recovery is denominator-normalized and S2 products remain very pure. C1/S2 at 345 K is the current upstream baseline. Later tests should vary loading and catalyst while retaining downstream history to establish robustness.

## Decision
Optimize within S2 using slower/staged cooling, cold aging, and seed-dose/thermal-history perturbations; retain batch 3 as current best feasible recovery. A reproducibly higher recovery with acceptable fines will replace it.

## Revision 3

Recorded: 2026-10-13T18:23:44.093507+00:00; available public operations: 114; reviewed through: runner-operation-0114.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 remains the preferred solvent; S3 gave both lower recovery and excessive fines under its tested condition (events runner-operation-0039, -0052).

## H2 [revised: nonmonotone history]
Slow staged cooling with 0.05 g seed can satisfy fines, but more thermal processing is not uniformly beneficial. A four-stage 300→285→270→250 K schedule at 0.08 L gave recovery ~0.445/fines ~0.378 (event runner-operation-0066). At 0.05 L with one extra 250 K stage recovery rose to ~0.463 with fines ~0.459 (event -0081). Reheat/recool at 0.04 L produced nearly all fines (~0.987; event -0098), and excessive cold aging at 0.06 L also failed fines (~0.596; event -0114). Reheat and concentration/history are confounded in batch 7.

## H3 [supported as design tradeoff]
Higher product loading (less S2 solvent at fixed 0.04 mol reagent) tends to raise fractional recovery, but risks secondary nucleation and fines. Current feasible optimum is batch 6 (0.05 L S2, recovery ~0.463, purity 1.0, fines ~0.459). Prediction: 0.045–0.055 L S2 with four stages and no reheat may retain recovery near 0.46 while restoring a wider fines margin.

## Decision
Test the concentration window and stopping time without reheat. Prefer the highest observed recovery whose final assay meets purity >=0.80 and fines <=0.50; particle-size scouting alone is not the final constraint result.

## Revision 4

Recorded: 2026-10-13T18:24:48.741163+00:00; available public operations: 171; reviewed through: runner-operation-0171.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 is the preferred tested crystallization solvent. S3 did not improve recovery and failed the fines constraint under its tested condition (events runner-operation-0039, -0052). Material effects outside the tested histories remain unresolved because the comparison is partly confounded.

## H2 [supported in tested scope]
For S2, 0.05 g seed and slow staged cooling without ambient interruption or reheat gives feasible crystal populations. Reheat/recool at high loading was strongly associated with excessive fines (event -0098), while four- or five-stage monotone schedules at 0.05 L S2 repeatedly met the fines limit (events -0081, -0157, -0171). The reheat result is confounded with 0.04 L solvent and should not be generalized beyond this scope.

## H3 [supported as a nonmonotone tradeoff]
Fixed 0.04 mol reagent with reduced S2 volume increased recovery into the ~0.46–0.47 range, but volumes 0.045, 0.055, and 0.060 L under their tested histories generated excessive fines (events -0128, -0142, -0114). The 0.050 L condition formed a reproducible feasible window: recovery ~0.463/fines ~0.459 in batch 6 and ~0.457/fines ~0.434 in batch 11 (events -0081, -0157). Batch 12 stopped after one fewer 250 K stage and gave ~0.460 recovery with ~0.442 fines (event -0171), showing no clear benefit from the extra cold hold relative to batch variability.

## Final decision
Recommend completed batch 6 because it has the highest final-assay crystal recovery among batches satisfying purity >=0.80 and fines <=0.50: recovery ~0.4633, purity 1.000, fines ~0.4591 (event runner-operation-0081). Batches 11 and 12 provide nearby feasible corroboration. The selection optimizes observed recovery, while acknowledging measurement noise and a modest rather than large fines margin.
