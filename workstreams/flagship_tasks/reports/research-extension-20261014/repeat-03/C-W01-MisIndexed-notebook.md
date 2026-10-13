# repeat-03 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:52:40.496210+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## Pre-experiment expectations

**H1 [tentative].** Solvent S2 should favor high crystallization recovery with acceptable purity and few fines because its dossier combines low relative solubility (0.7), strong growth (1.3), low nucleation (0.65), and low impurity occlusion (0.65). S3 is the conservative comparator; S0 is expected to produce more fines/occlusion.

**H2 [tentative].** Catalyst C1 at moderate-to-high temperature should give strong reaction conversion, but the fixed-world residual may reorder catalysts. Initial tests will compare catalyst/solvent choices before narrowing thermal and seed conditions.

**H3 [tentative].** A small seed dose followed by controlled, slower cooling and a cold hold should increase crystal size and reduce fines relative to abrupt cooling; excessive seed may reduce seed-excluded recovery or size. Reheating/recooling may ripen particles but could sacrifice recovery.

Decision rule: prioritize final-assay crystal_yield only among batches with crystal_purity >=0.80 and crystal_fines_fraction <=0.50; particle-size readings will guide cooling/hold adaptation, while final assays remain decisive.

## Revision 2

Recorded: 2026-10-13T17:54:48.819876+00:00; available public operations: 91; reviewed through: runner-operation-0091.

# Hypothesis notebook

## Current interpretations after batches 1–8

**H1 [supported in tested scope].** S2 is the best solvent for meeting both crystallization constraints under 14,400 s cooling to 250 K with 0.02 g seed. Batch 2 gave crystal_yield 0.512, purity 0.987 and fines 0.266 (event runner-operation-0025). S3 and S1 had lower recovery and failed the fines constraint in their single trials (events runner-operation-0036 and -0047). S0 gave a numerically higher recovery (0.573) but clearly failed fines (0.695; event -0058). These are single comparisons, so solvent effects are not claimed beyond this recipe.

**H2 [revised, unresolved catalyst ranking].** Catalyst C0/S2 produced the highest observed valid recovery so far (0.552, purity 1.000, fines 0.301; event runner-operation-0069). C3/S2 was also strong (0.532, 0.980, 0.265; event -0091), while C2 was lower (event -0080). The differences are numerical, confounded with stochastic process/instrument variation, and lack replication; C0 is selected provisionally for concentration studies.

**H3 [supported directionally].** Relative to batch 1, extending cooling to 250 K over 14,400 s and filtering immediately increased observed recovery and reduced fines (batch 2 event -0025 versus batch 1 event -0014). Batch 1 also included an uncontrolled hold that warmed the slurry, so the causal contribution of endpoint, duration, and immediate filtration is unresolved.

**H4 [prospective].** Lowering S2 volume at fixed reagent charge should raise supersaturation and seed-excluded recovery, but may increase fines or impurity occlusion. Test 0.04 and 0.06 L against the prior 0.08 L scope, with the same C0/thermal history. A result above the current best recovery while maintaining purity >=0.80 and fines <=0.50 would change the recommended loading.

Decision rule remains: maximize final-assay crystal_yield only among constraint-passing batches.

## Revision 3

Recorded: 2026-10-13T17:55:40.560406+00:00; available public operations: 124; reviewed through: runner-operation-0124.

# Hypothesis notebook

## Current interpretations after batches 1–11

**H1 [supported in tested scope].** S2 is the only solvent tested that repeatedly combines strong recovery with constraint compliance under the long 250 K cooling program. S0 can raise recovery but its tested recipe produced excessive fines; S1 and S3 also failed fines in single trials.

**H2 [provisional].** C0 is the working catalyst for the final loading study. Its observed valid recoveries in S2 include 0.552 at 0.08 L (runner-operation-0069), 0.566 at 0.04 L (runner-operation-0102), and 0.561 at 0.03 L with higher seed (runner-operation-0124). C3 was competitive but not replicated.

**H3 [supported directionally].** Long cooling to 250 K with immediate filtration is preferable to the warmer-ended batch-1 history. The endpoint/duration effects remain confounded.

**H4 [narrowed].** At fixed 0.04 mol reagent, lowering S2 from 0.08 to 0.04 L gave a modest numerical recovery increase while retaining low fines (event -0102). At 0.02 L with 0.02 g seed, recovery rose to 0.575 but fines reached 1.0 (event -0113), so concentration-driven nucleation creates a sharp quality risk. At 0.03 L with 0.05 g seed, fines were only 0.281 and recovery 0.561 (event -0124), suggesting—without an isolated seed-dose comparison—that greater seeding may suppress uncontrolled nucleation enough to recover quality.

**Final prospective test.** Repeat the 0.02 L high-loading recipe using 0.05 g seed. If its final assay has fines <=0.50 and purity >=0.80, it can supersede batch 9 only if its observed recovery exceeds 0.566; otherwise batch 9 remains the leading recommendation. Instrument uncertainty and lack of replication limit close rankings.

## Revision 4

Recorded: 2026-10-13T17:56:10.653960+00:00; available public operations: 134; reviewed through: runner-operation-0134.

# Hypothesis notebook

## Final source-stage interpretation

**H1 [supported in tested scope].** S2 was the most robust solvent for the quality-constrained objective under the long 250 K cooling program. Single S1, S3, and S0 trials did not meet the fines constraint, whereas multiple S2 trials did.

**H2 [provisional].** C0/S2 is the preferred material combination. C0 generated several constraint-passing batches; catalyst comparisons were unreplicated and therefore do not establish a general catalyst ranking.

**H3 [supported directionally, confounded].** Cooling to 250 K over 14,400 s and filtering immediately outperformed the warmer-ended batch-1 sequence. Endpoint, duration, and avoidance of warm hold changed together.

**H4 [supported nonlinear loading effect].** At fixed 0.04 mol reagent, 0.04 L S2 provided the highest observed constraint-passing crystal_yield: 0.566 with purity 0.987 and fines 0.249 (batch 9, runner-operation-0102). Lowering solvent to 0.02 L increased observed recovery slightly but caused fines=1.0 with both 0.02 and 0.05 g seed (batches 10 and 12; events -0113 and -0134). Thus extra seed did not rescue the excessive-nucleation regime, disconfirming the final prospective rescue hypothesis. The 0.03 L/0.05 g recipe passed (batch 11, event -0124) but its observed recovery 0.561 did not exceed batch 9; the small difference is not evidence of a true effect given assay noise and no replication.

## Decision
Recommend completed batch 9 because it has the largest observed final-assay crystal_yield among all batches satisfying purity >=0.80 and fines <=0.50. Its recipe scope is S2 0.04 L, reagent 0.04 mol, C0 0.005 mol, 365 K reaction for 3,600 s, 0.02 g seed, cooling to 250 K over 14,400 s, immediate filtration. Close alternatives are batches 6, 8, and 11; replication would be required before claiming fine distinctions.
