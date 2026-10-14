# repeat-01 / C-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:52:41.300352+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative, pre-experiment].** Solvent S2 should favor acceptable crystal purity and coarser particles because its dossier reports lower impurity occlusion/nucleation and higher growth, while its lower solubility may improve recovery. This may trade against reaction performance; observations override the dossier.

**H2 [tentative, pre-experiment].** Catalyst C1 is the first reaction-screen choice because its nominal panel activity is highest, but fixed-world residuals could reorder catalysts. At equal 0.04 mol reagent, 0.005 mol catalyst, and thermal history, HPLC conversion/selectivity will guide catalyst choice.

**H3 [tentative, pre-experiment].** Slow cooling plus modest seeding and a growth hold should reduce fines relative to rapid/unseeded crystallization. A seed-dose series and thermal-history tests will distinguish nucleation from growth effects.

Initial plan: establish feasibility with C1/S2, then screen catalyst/solvent and crystallization history. Quality constraints are purity >=0.80 and fines <=0.50; prioritize maximum final crystal yield among qualifying batches.

## Revision 2

Recorded: 2026-10-14T10:56:08.995636+00:00; available public operations: 144; reviewed through: runner-operation-0144.

# Final hypothesis synthesis

**H1 [supported in tested scope].** S2 is the preferred crystallization solvent among the focused tests. With C1 and a 0.04 mol charge, S2 produced multiple qualifying batches; S3 gave numerically high recovery (~0.456) but fines above 0.55 in both tested histories (final assays at runner-operation-0109 and runner-operation-0120). Thus S3's recovery advantage is unusable under the fines constraint in this campaign.

**H2 [supported in tested scope].** C1 is the preferred catalyst. At the common 350 K / 3600 s reaction and S2 crystallization history, the C1 batch gave crystal yield ~0.437 with purity ~0.992 and fines ~0.367 (runner-operation-0036), versus lower qualifying recovery for C0, C2, and C3 comparisons (runner-operation-0024, -0048, -0060). The catalyst screen is single-run per catalyst, so small differences are not established as precise effect sizes.

**H3 [supported with qualification].** A 0.05 g seed dose, long cooling to 250 K, and growth hold can satisfy fines <=0.50, whereas the initial 0.02 g/shorter cooling batch was slightly above the limit (runner-operation-0012). Morphology varied substantially with upstream temperature and between histories, so the seed effect is not isolated cleanly; reaction loading/thermal state is a confound.

**H4 [supported in local temperature range].** For C1/S2, the best observed compromise occurred near 345–347.5 K reaction temperature for 3600 s. At 345 K, recovery ~0.446, purity ~0.996, fines ~0.398 (runner-operation-0132). At 347.5 K, recovery ~0.454, purity ~0.997, fines ~0.378 (runner-operation-0144). Lower 330 K and 340 K trials failed the fines constraint despite good purity (runner-operation-0072 and -0084). The 347.5 K result is the highest qualifying recovery observed, not a proven continuous optimum.

**Decision.** Recommend lifecycle batch 12: S2 (0.08 L), reagent 0.04 mol, C1 0.005 mol; heat at 347.5 K for 3600 s with 400 rpm; seed 0.05 g; cool to 250 K over 14400 s; hold 7200 s at 200 rpm; filter. It meets both constraints with the highest observed qualifying crystal yield. Change this decision if a repeat shows fines above 0.50 or if a neighboring-temperature replicate yields materially higher qualifying recovery.
