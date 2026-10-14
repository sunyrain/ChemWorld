# repeat-02 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:01:43.591870+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative, pre-experiment]
Solvent S2 should favor larger, cleaner crystals and fewer fines because its nominal growth is highest and nucleation/occlusion are lowest, while its lower solubility may improve recovery. Against this, S1 has the strongest nominal reaction activity and could produce more target upstream. Initial solvent screen will test the tradeoff at a common C1 reaction condition.

H2 [tentative, pre-experiment]
C1 is the best initial catalyst choice from nominal activity; adequate high-temperature residence should increase conversion, but excessive temperature/time may increase degradation. I will begin near 360 K and use HPLC selectively to distinguish reaction-limited from crystallization-limited outcomes.

H3 [tentative, pre-experiment]
Moderate seeding followed by slow cooling and a cold hold should reduce spontaneous fines while maintaining recovery. If recovery is low despite good conversion, colder/longer aging or lower-solubility solvent will be prioritized; if purity/fines fail, slower cooling, less supersaturation, or a growth hold will be tested.

## Revision 2

Recorded: 2026-10-14T11:03:54.761620+00:00; available public operations: 46; reviewed through: runner-operation-0046.

# Working hypotheses

H1 [supported in screened scope]
At C1, 360 K/1800 s, 0.05 g seed and two 7200 s cool/hold segments to 275 K, S2 is the only screened solvent meeting both quality constraints and also gives the highest observed recovery: final yield 0.557, purity 0.990, fines 0.423 (event runner-operation-0035). S1 gave 0.531 recovery but fines 0.557 (runner-operation-0024); S0 and S3 had lower recovery and much higher fines (runner-operation-0013, -0046). This agrees with nominal low nucleation/occlusion for S2, but solvent identity is confounded with reaction response and there are no replicates.

H2 [unresolved]
C1 may be best catalyst, but only C1 has been tested. Under S2, screen C0/C2/C3 at the same thermal/crystallization history. A catalyst that raises upstream target without unacceptable degradation should raise crystal recovery.

H3 [supported in current S2 recipe, optimization unresolved]
Moderate seeding plus slow cold processing can meet fines <=0.50 in S2 (particle measurement runner-operation-0032 and final assay -0035). Further cold duration, temperature, seed dose, and reaction loading may alter recovery/fines. Next prioritize catalyst identity, then thermal and seed optimization around S2.

## Revision 3

Recorded: 2026-10-14T11:04:47.636660+00:00; available public operations: 79; reviewed through: runner-operation-0079.

# Working hypotheses

H1 [supported in screened scope]
S2 is the only screened solvent meeting both quality constraints at the common recipe and also gave the highest screened-solvent recovery (runner-operation-0035). The solvent result is not replicated, but is directionally consistent with its nominal crystallization properties.

H2 [supported for catalyst ranking at this recipe, close alternatives unresolved]
With S2 and a common 360 K/1800 s reaction and cooling history, C3 gave the highest observed recovery (0.577) with purity 0.981 and fines 0.392 (runner-operation-0079). C0 was close at 0.568/0.978/0.439 (runner-operation-0057), C1 0.557/0.990/0.423 (-0035), and C2 lower at 0.481 (-0068). Single runs and assay noise mean the small C3-C0 difference is unresolved; C2 is clearly less promising numerically.

H3 [optimization hypothesis]
C3 reaches essentially complete conversion at 360 K/1800 s but shows nontrivial byproduct/degradation signals (runner-operation-0079). A milder/shorter reaction may improve selectivity enough to raise recoverable target even with slightly less conversion. Separately, cooling to 260 K should increase recovery but may increase nucleation/fines; lower seed dose may reduce number counts but risks uncontrolled nucleation. Test these factors around S2/C3 while retaining slow cooling and cold hold.

## Revision 4

Recorded: 2026-10-14T11:06:07.062750+00:00; available public operations: 133; reviewed through: runner-operation-0133.

# Final source-stage hypotheses

H1 [supported in tested domain]
S2 strongly outperformed the other solvents for the joint recovery/purity/fines objective under the common initial recipe. Its nominal low solubility, low nucleation tendency, high growth, and low occlusion are a coherent explanation, but reaction-solvent effects remain confounded and no solvent condition was replicated.

H2 [supported at tested recipe; close ranking uncertain]
C3 was the best observed catalyst in the common S2 screen (runner-operation-0079), although C0 was close (runner-operation-0057) and the gap is not established beyond single noisy assays.

H3 [supported locally]
Shortening the C3 reaction from 1800 s to 900 s at 360 K raised observed upstream yield/selectivity and crystal recovery while lowering degradation (compare runner-operation-0079 with -0101). Further shortening to 600 s reduced conversion but produced nearly the same final recovery at the colder crystallization condition (runner-operation-0133), suggesting a broad local optimum governed by a conversion/degradation tradeoff.

H4 [supported numerically; small differences unresolved]
With S2/C3 and short reaction, lowering crystallization target from 275 K to 260-250 K increased observed recovery while retaining purity >0.97 and fines <0.50 (runner-operation-0101, -0112, -0123). Batch 11 at 250 K/900 s has the highest measured qualifying recovery, 0.662, purity 0.994, fines 0.441 (runner-operation-0123); batch 12 at 600 s is essentially tied at 0.661/0.995/0.461 (runner-operation-0133). The 0.001 recovery difference is far below the declared assay noise and is not evidence that 900 s is truly superior. Batch 11 is preferred because its pre-filtration particle measurement also indicated passing fines (runner-operation-0120) and its conversion was higher.

Decision
Recommend completed batch 11. Scope: 0.04 mol reagent, 0.08 L S2, 0.005 mol C3; 360 K for 900 s at 400 rpm; 0.05 g seed; two 7200 s stages at 250 K; filter, terminate, assay. Confidence would change with replication showing batch 12 or another nearby residence time has materially higher recovery, or if fines reproducibility near the 0.50 limit is poor.
