# repeat-02 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:12:44.739705+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Within the nominal dossier's scope, solvent S2 should favor larger, purer crystals with fewer fines because it combines high relative growth (1.3), low nucleation (0.65), and low impurity occlusion (0.65), while its low solubility may improve recovery. A seeded, slow-cooling process after a high-conversion reaction should therefore be the initial baseline. This expectation would weaken if the first batch fails purity/fines constraints or if later controlled solvent comparisons favor S3/S1.

## H2 [tentative; pre-experiment]
Catalyst C1 is the first reaction baseline because its nominal panel activity is highest. Reaction conditions and catalyst identity remain uncertain; an HPLC reading after reaction will guide later batches.

## Planned first test
Use full reagent/solvent/catalyst loading in S2, heat under inert atmosphere, quench, seed modestly, cool slowly, hold, filter, and assay. Particle sizing before filtration is predicted to show fines <=0.50. Later batches will vary catalyst, thermal duration, seed dose, and cooling history while keeping single-batch stock use within the 12-batch equal-share budget.

## Revision 2

Recorded: 2026-10-13T17:17:31.022071+00:00; available public operations: 140; reviewed through: runner-operation-0140.

# Hypothesis notebook

## H1 [supported only for purity/recovery; rejected for fines at high loading]
S2 gives high crystal purity and useful recovery, but at 0.04 mol reagent in 0.08 L it produced essentially all fines despite slow cooling, added seed, long holds, and one thermal cycle (final assays in runner-operation-0015, -0040, and -0103). Thus the original expectation that S2 plus slow seeded cooling alone would satisfy fines is rejected in the high-loading scope. S3 and S1 did not solve the high-loading fines problem (runner-operation-0074 and -0122).

## H2 [supported in tested scope]
Upstream loading is the dominant control found so far. Reducing reagent from 0.04 to 0.01 mol at otherwise similar S2 conditions changed final fines from near 1 to 0.450 while retaining purity 1.00 and crystallization recovery 0.390 (runner-operation-0140). The comparison is confounded by concentration-dependent reaction behavior, but the magnitude relative to instrument noise is large. Testable consequence: a modest loading increase should raise recovery and may approach/cross the 0.50 fines constraint, defining a useful boundary.

## H3 [unresolved]
Seed dose and thermal cycling caused only small numerical size/fines changes among overloaded batches, with multiple process differences and no replication. Do not claim a seed-dose effect. Once loading is controlled near 0.01 mol/0.08 L, test loading increments and then modest changes in final temperature or seed dose.

## Decision
Use batch 6 as the current feasible benchmark. Next test 0.0125 mol reagent with the same S2 staged cooling and slightly more seed. If fines exceed 0.50, return toward 0.01 and improve recovery by deeper final cooling or holding rather than further loading.

## Revision 3

Recorded: 2026-10-13T17:19:17.370934+00:00; available public operations: 253; reviewed through: runner-operation-0253.

# Hypothesis notebook

## H1 [supported in low-loading S2 scope]
S2 can deliver high-purity, constraint-compliant crystals when upstream loading is sufficiently low. High-loading trials (0.04 mol reagent/0.08 L) gave near-unity fines despite seed, long holds, alternative solvents, and a thermal cycle (runner-operation-0015 through -0122). Reducing loading to 0.01 mol/0.08 L moved the process into a distinct low-fines regime (runner-operation-0140).

## H2 [supported; boundary is sharp over tested range]
At 0.01 mol reagent, staged slow cooling in S2 with 0.10 g seed produced compliant fines and high purity. Raising loading to 0.0125 mol caused fines near 0.99 (runner-operation-0159), whereas 0.011 mol remained compliant at 0.408 (runner-operation-0235). Because these are single batches and other small process differences exist, the precise loading boundary is unresolved; a conservative recommendation retains 0.01 mol.

## H3 [supported in tested 0.01-mol recipe]
Lowering the second-stage endpoint from 280 K to 270, 260, and 250 K increased measured crystal recovery from 0.390 to 0.480, 0.532, and 0.579 while final fines stayed below 0.50 (runner-operation-0140, -0178, -0197, -0216). This monotone recovery pattern across the staged series is stronger evidence than any one numerical difference, although batches were not formal replicates.

## Reproducibility and final decision
The batch-10 recipe (0.01 mol reagent, 0.08 L S2, 0.005 mol C1; reaction at 350 K for 3600 s; quench; 0.10 g seed; staged slow cooling/holds at 300 K then 250 K; filter) gave crystal recovery 0.579, purity 0.981, and fines 0.291 (runner-operation-0216). A repeat recipe in batch 12 gave recovery 0.573, purity 0.997, and fines 0.281 (runner-operation-0253), supporting robustness within unknown process/instrument variability. Batch 10 is selected because it has the highest observed compliant crystal recovery; batch 12 is corroborating evidence. Seed-dose effects remain unresolved because seed changes were confounded with thermal and loading changes.
