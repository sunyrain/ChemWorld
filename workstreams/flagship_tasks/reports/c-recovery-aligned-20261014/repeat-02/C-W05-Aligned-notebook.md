# repeat-02 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:17:04.467015+00:00; available public operations: 0; reviewed through: None.

# Campaign hypotheses

## H1 [tentative; pre-experiment]
Catalysts and solvents will materially affect reaction conversion/selectivity; the nominal dossier suggests C1 or C3 and S2/S3 as productive starting points, but fixed residuals could reverse this. A high-temperature reaction followed by quench will test feasibility. If HPLC shows poor conversion or selectivity, vary catalyst before crystallization refinements.

## H2 [tentative; pre-experiment]
For crystallization, S2 should favor growth, low impurity occlusion, and low nucleation, so modest seeding plus slow cooling and a cold hold should produce purity >=0.80 and fines <=0.50. Faster cooling or excess seed is expected to increase fines; insufficient supersaturation may lower recovery. Testable consequence: among otherwise similar runs, slow seeded cooling should improve size/fines, while deeper cold holds should increase recovery.

## Decision scope
First establish a productive upstream recipe and feasible crystallization. Thereafter use batches to separate catalyst, solvent, seed dose, cooling rate, cold endpoint/hold, and (if useful) reheat/recool effects. Final selection will prioritize measured crystal_yield only among batches satisfying both quality constraints.

## Revision 2

Recorded: 2026-10-14T11:19:15.057603+00:00; available public operations: 71; reviewed through: runner-operation-0071.

# Campaign hypotheses

## H1 [supported in tested scope]
At 390 K/3600 s in S2, C0 is the best tested catalyst for usable target formation. Final assays gave crystal_yield 0.452 for C0 (event runner-operation-0057), versus 0.409 C1 (0015), 0.419 C2 (0071), and 0.373 C3 (0043), with all comparable 270 K seeded crystallizations meeting purity/fines constraints except a separate colder run. HPLC directionally agreed that C0 had the highest yield/selectivity among the catalyst screen (0050 versus 0007, 0036, 0064). These are numerical differences under one run each, so catalyst-by-condition interaction and run variability remain unresolved.

## H2 [narrowed]
Seeded slow cooling to 270 K with S2 is repeatedly compatible with high purity and fines below 0.50 (0015, 0043, 0057, 0071). Cooling instead to 265 K produced fines_fraction 1.0 despite similar purity (0029), so deeper cooling can trigger excessive secondary nucleation; this is a large single-run contrast, not yet a repeatability estimate. Test 275 K and thermal-history/seed variants around C0/S2.

## H3 [tentative]
Solvent S2 nominally supports clean growth, but other solvents may improve reaction yield enough to offset crystallization disadvantages. Screen solvents with C0, holding reaction and 270 K crystallization broadly fixed.

## Decision
Use C0 at 390 K/3600 s as current upstream baseline. Prioritize solvent effects, then optimize endpoint/hold and seed strategy. Final selection remains highest measured crystal_yield among purity >=0.80 and fines <=0.50.

## Revision 3

Recorded: 2026-10-14T11:20:49.476301+00:00; available public operations: 161; reviewed through: runner-operation-0161.

# Campaign hypotheses

## H1 [supported in tested scope]
At 390 K/3600 s, C0 is the best tested catalyst with S2. The catalyst comparison and HPLC evidence are recorded in events 0015, 0043, 0050/0057, 0064/0071. Interaction outside this condition remains unresolved.

## H2 [supported for solvent quality tradeoff]
Solvent changes create a strong recovery–fines tradeoff. S0 and S1 increased crystal_yield to about 0.54 and 0.53 but failed fines (0.81 and 0.62; events 0113 and 0085). S3 also failed fines and had lower recovery (0099). Slow cooling, warmer endpoints, long holds, and 0.20 g seed did not rescue S0/S1 below the 0.50 fines limit (0130, 0147), suggesting a solvent-specific nucleation tendency rather than only cooling-rate control. S2 remains the reliable quality solvent.

## H3 [supported directionally; final test precommitted]
Within C0/S2, reducing solvent from 0.08 to 0.06 L raised measured crystal_yield from 0.452 (0057) to 0.467 (0161), but fines moved from 0.413 to 0.512, narrowly outside specification. Because these are single runs with assay noise, exact monotonicity is unresolved. Prediction before batch 12: an intermediate 0.065 L loading with the established 270 K slow cooling should preserve most recovery gain while bringing fines below 0.50. A failed fines result will leave batch 4 (event 0057) as the leading confirmed feasible process.

## Final decision rule
Select the completed batch with highest measured crystal_yield among those with crystal_purity >=0.80 and crystal_fines_fraction <=0.50; do not substitute native score for this rule.

## Revision 4

Recorded: 2026-10-14T11:21:13.418749+00:00; available public operations: 174; reviewed through: runner-operation-0174.

# Campaign hypotheses — final source-stage record

## H1 [supported in tested scope]
C0 at 390 K/3600 s was the best tested catalyst with S2 under the common seeded 270 K crystallization. Batch 4 (final assay event runner-operation-0057) gave crystal_yield 0.4525, purity 1.000, and fines 0.4130. Comparable C1, C2, and C3 batches had lower recovery (events 0015, 0071, 0043). Single-run comparisons leave repeatability and interactions unresolved.

## H2 [supported for solvent quality tradeoff]
S0 and S1 improved reaction/overall recovery but strongly worsened number-fines: final crystal_yield/fines were about 0.540/0.811 for S0 (0113) and 0.534/0.622 for S1 (0085). S3 also failed fines (0099). Warmer endpoints, slower cooling, longer holds, and 0.20 g seed did not rescue S0/S1 (0130, 0147). Thus S2 is the best-supported solvent for meeting the quality constraint, despite lower recovery.

## H3 [disconfirmed as a simple interpolation]
The precommitted expectation that intermediate 0.065 L S2 would retain recovery while restoring fines below 0.50 was not supported: batch 12 gave yield 0.4668 but fines 0.6013 (0174). The 0.06 L batch was only narrowly over the limit at 0.5123 (0161), but it is still infeasible by the stated point-estimate rule. These single results and instrument noise mean the loading response is not demonstrably monotone; repeatability would be needed before choosing a boundary recipe.

## Final selection
Recommend lifecycle batch 4. It has the highest measured crystal_yield among completed batches whose final assay satisfies purity >=0.80 and fines <=0.50. Batch 4 used 0.04 mol reagent, 0.08 L S2, 0.005 mol C0, nitrogen control, 390 K reaction for 3600 s, quench, 0.05 g seed, slow cooling to 270 K over 10800 s, a 7200 s cold hold at 200 rpm, then filtration. Higher-recovery S0/S1 and concentrated-S2 alternatives were rejected for excess fines.
