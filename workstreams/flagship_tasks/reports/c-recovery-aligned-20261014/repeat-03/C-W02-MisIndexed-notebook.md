# repeat-03 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:50:57.313268+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the anonymous-material scope, catalyst C1 and solvent S2 are initial leaders: C1 has the highest nominal activity geomean, while S2 combines low solubility, strong growth, low nucleation, and low occlusion. A sufficiently hot reaction followed by slow seeded cooling in S2 should therefore improve overall crystal recovery while keeping purity above 0.80 and fines below 0.50.

**Prediction before batch 1:** A 0.04 mol reagent / 0.005 mol C1 / 0.08 L S2 batch reacted near 360 K, then gently cooled, seeded, held, and filtered should achieve detectable seed-excluded crystals and plausibly exceed the 0.10 feasibility target.

Alternatives: hidden world residuals may reverse catalyst or solvent rankings; too-low S2 solubility may limit reaction or create fines. Initial batches will separate upstream conversion/selectivity from downstream recovery using HPLC/particle-size selectively.

## Revision 2

Recorded: 2026-10-14T11:52:57.746286+00:00; available public operations: 57; reviewed through: runner-operation-0057.

# Hypothesis notebook

## H1 [revised; supported in tested scope]
Solvent S2 remains an effective crystallization medium: batches 1–4 all gave high crystal purity and feasible seed-excluded recovery. The nominal catalyst ranking was misleading. At comparable 340 K/1 h reaction and 14,400 s cooling, C0 (batch 2, event runner-operation-0024) gave the largest observed recovery (0.503) among C0/C2/C3, while C2 and C3 were materially lower (events runner-operation-0035 and -0046). C1 at 360 K was competitive but lower (batch 1, -0013); catalyst and temperature are confounded there.

## H2 [tentative]
For C0/S2, a roughly 340 K, 1 h reaction is preferable to a longer 330 K hold. The 330 K/2 h trial (batch 5, -0057) had lower recovery and a fines fraction reported at 1.0, opposing the idea that lower severity automatically improves quality. This is only one trial and the unexpectedly severe fines response may reflect thermal-history sensitivity or run variability.

## H3 [tentative]
Cooling/seed history controls the fines constraint strongly. Batch 2 passed only narrowly (fines 0.491), whereas the ambient-warmed hold in batch 1 ended at lower fines (0.399) but also lower recovery. Next tests will use C0/S2 at 340 K and deliberately vary solvent, seed dose/timing, endpoint, and thermal cycling. A useful change must retain purity >=0.80 and fines <=0.50 while improving recovery beyond about 0.50; differences near assay noise will be treated as unresolved.

## Revision 3

Recorded: 2026-10-14T11:54:26.586103+00:00; available public operations: 135; reviewed through: runner-operation-0135.

# Hypothesis notebook

## H1 [supported in tested scope]
The best constraint-feasible region tested uses catalyst C0 with solvent S2, a 340 K reaction target for 3,600 s, 0.05 g seed, and a 14,400 s cool toward 260 K followed by immediate filtration. Batch 2 first identified this region (event runner-operation-0024), and batch 12 repeated it with the campaign's highest observed qualifying recovery, 0.524, purity 0.993, and fines 0.489 (runner-operation-0135).

## H2 [supported qualitatively; magnitude uncertain]
Solvent materially changes the recovery–fines tradeoff. S0 and S1 produced higher upstream yield and crystal recovery near 0.56–0.58 in batches 7–10, but their fines fractions near 0.70–0.75 violated the <=0.50 constraint (runner-operation-0079 through -0114). S2 sacrifices some upstream yield but suppresses fines sufficiently in the high-seed recipe. S3 was inferior and noncompliant (runner-operation-0068).

## H3 [supported in this tested range]
Reducing seed from 0.05 g to 0.005 g did not suppress fines; it coincided with severe fines in both S1 and S2 (batches 8, 9, 11; runner-operation-0090, -0103, -0125). A tested reheat/recool cycle also failed to rescue S1 fines (batch 9). Thus high seed dose is retained despite seed-excluded yield accounting.

## Decision and uncertainty
Recommend batch 12 because it has the greatest observed recovery among batches satisfying both explicit quality constraints. Batch 2 is a near replicate and also qualified, supporting the recipe region. The fines values of both are close to 0.50 relative to the stated assay noise (0.018), so robustness at the boundary is unresolved; batch 1 offers a lower-recovery but larger observed fines margin. Future confirmation should prioritize replicated fines measurements and a narrow S2 cooling/seed study rather than extrapolating from the noncompliant higher-yield solvents.
