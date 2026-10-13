# repeat-03 / C-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:10:32.126956+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Within the nominal dossier, solvent S2 should favor larger, purer crystals and lower fines because it combines high relative growth with low nucleation and impurity occlusion; its lower solubility may also improve recovery. This may fail if the dossier is misindexed or if reaction conversion in S2 is poor.

## H2 [tentative]
Catalyst C1 is the safest first reaction choice because its nominal activity is high with lower panel variability than C2/C3. A moderate-to-hot reaction followed by quench and slow seeded cooling should produce target while limiting degradation and uncontrolled nucleation.

## Test plan
First establish a feasible full workflow in S2/C1 with near-maximum charge, then vary catalyst/solvent and crystallization history. Pre-experiment expectation: seeded slow cooling plus a low-temperature hold will exceed 0.10 crystallization recovery, purity 0.80, and fines at most 0.50. If early assays contradict this, prioritize empirical solvent/catalyst screening and adjust supersaturation/seed timing.

## Revision 2

Recorded: 2026-10-13T18:12:26.399713+00:00; available public operations: 42; reviewed through: runner-operation-0042.

# Working hypotheses

## H1 [partly supported; fines mechanism unresolved]
S2/C1 with slow seeded cooling gives strong seed-excluded recovery (about 0.41–0.46) and crystal purity about 0.99, supporting the recovery/purity part of the prior. However, all first three batches have extremely high fines (final assays at runner-operation-0013, -0027, -0042), so the expectation of meeting the fines constraint is rejected for simple one-pass cooling. The particle readings and assays both indicate number-weighted sizes far below 20 um; differences among these batches are too small relative to the major constraint failure to establish a useful seed/hold effect.

## H2 [supported only for feasible reaction]
C1 at 340–350 K gives essentially complete conversion, while shorter/lower-temperature reaction reduced degradation warning and improved selectivity numerically (runner-operation-0027 versus -0013), though reaction time and temperature are confounded. Crystal purity remains acceptable regardless.

## H3 [tentative, prospective]
Thermal cycling after initial crystallization may dissolve the smallest crystals preferentially and regrow larger particles on recooling, reducing the number fraction below 20 um. Test with a partial reheat/hold/slow recool in S2; abandon simple extended isothermal holding if cycling also leaves fines near 1. A result below 0.50 fines would support the mechanism; values near the current 0.98–1.00 would refute practical effectiveness in this scope.

## Revision 3

Recorded: 2026-10-13T18:13:16.873790+00:00; available public operations: 77; reviewed through: runner-operation-0077.

# Working hypotheses

## H1 [supported for recovery/purity; rejected for fines]
Across S2/C1 batches, crystallization recovery remains roughly 0.41–0.47 and purity about 0.98–1.00, but simple seeded, held, thermally cycled, and unseeded/staged cooling all give fines essentially 0.98–1.00 (runner-operation-0013 through -0077). Thus S2 is robustly feasible on recovery and purity but does not meet the particle constraint at the tested high loading.

## H2 [supported only for feasible reaction]
C1 at 340–350 K produces essentially complete conversion. Shorter/lower-temperature reaction numerically lowers degradation relative to the initial longer/hotter run, with remaining confounding.

## H3 [rejected in tested scope]
Two partial reheat/recool cycles did not materially reduce fines (runner-operation-0060). Slow staged unseeded cooling also failed (runner-operation-0077). Thermal history alone is therefore unlikely to rescue high-loading S2 in the tested range.

## H4 [tentative, prospective]
Particle count may be dominated by high supersaturation from the 0.04 mol charge. Reducing upstream reagent concentration while retaining a relatively large seed dose should shift deposition toward seeded growth and may reduce fines, while crystallization recovery (a ratio to target present) can remain high. Test a tenfold lower reagent loading with maximum seed; if fines remain near 1, screen solvent identity rather than further reducing loading.

## Revision 4

Recorded: 2026-10-13T18:14:16.464492+00:00; available public operations: 133; reviewed through: runner-operation-0133.

# Working hypotheses

## H1 [supported for recovery/purity; particle constraint unresolved]
At 0.04 mol loading, all four solvents give high purity and useful recovery, but final fines remain about 0.99–1.00 (S1 runner-operation-0105, S3 -0119, S0 -0133; earlier S2 series). Numerically, S0 gives the highest recovery so far (0.531) and best reaction selectivity, while S1 gives 0.508 recovery. These single-batch differences are not repeatability evidence.

## H2 [supported only for feasible reaction]
C1 at 340 K/1800 s is a robust feasible reaction condition with near-complete conversion across solvent identities and acceptable final crystal purity.

## H3 [rejected in tested scope]
Partial thermal cycling, extended/staged cooling, and absence of seed do not rescue fines at high loading.

## H4 [rejected]
Tenfold lower reagent loading did not promote seeded growth; it sharply reduced recovery and still gave fines near 1 (runner-operation-0091), confounded by incomplete conversion.

## H5 [tentative, prospective]
The 0.05 g per-operation seed cap is not a per-batch cap. A much larger cumulative seed dose may supply enough coarse growth sites to suppress secondary nucleation or dominate the number distribution without entering the seed-excluded recovery numerator. Test about 2 g cumulative seed in the empirically high-recovery S0 condition. If fines remain above 0.50, the practical dose mechanism is unsupported; if it succeeds, refine dose downward and verify recovery/purity.

## Revision 5

Recorded: 2026-10-13T18:15:40.417696+00:00; available public operations: 229; reviewed through: runner-operation-0229.

# Working hypotheses

## H1 [supported for recovery/purity; constraint unmet]
S0/C1 at high loading reproducibly gives crystallization recovery around 0.52–0.53 and purity around 0.98–0.99 (runner-operation-0133, -0186, -0229), but fines remain essentially 1. The recovery differences among these replicates are small and not evidence of distinct effects.

## H2 [supported only for feasible reaction]
C1 at 340 K/1800 s remains a robust feasible reaction condition across solvents.

## H3 [rejected in tested scope]
Thermal cycling, staged cooling, unseeded operation, and very long low-temperature holding do not materially improve fines. Thirty additional holds still ended at fines about 0.994 (runner-operation-0229).

## H4 [rejected]
Tenfold lower loading reduced recovery and did not fix fines (runner-operation-0091).

## H5 [rejected in tested dose range]
Increasing cumulative seed from 0.05 g to about 2 g did not reduce fines and produced essentially the same S0 recovery as the ordinary-dose condition (runner-operation-0186 versus -0133). Seed mass is not the limiting control in this range.

## H6 [tentative, prospective]
A true second recrystallization after filtration may change the particle population more than in-slurry partial thermal cycling. The final batch will test filtration, resuspension/redissolution in S2, and slow recooling. If it fails, no tested process will satisfy the fines constraint and recommendation must be explicitly constraint-infeasible.

## Revision 6

Recorded: 2026-10-13T18:16:38.236841+00:00; available public operations: 249; reviewed through: runner-operation-0249.

# Final source-stage hypotheses and decision

## H1 [supported for recovery/purity; quality constraint unmet]
High-loading S0/C1 is the most consistently high-recovery regime tested: batches 9–11 gave crystallization recovery about 0.52–0.53 with purity about 0.98–0.99 (runner-operation-0133, -0186, -0229). Batch 10 has the highest observed recovery (0.5323) by a small numerical margin, but every tested batch violates the fines limit badly.

## H2 [supported in tested scope]
C1 at 340 K for 1800 s is a robust feasible reaction condition. Reaction conversion was near complete at full loading, and crystal purity was never the binding constraint in the principal full-loading conditions.

## H3 [rejected in tested scope]
Simple slow cooling, long holds, staged cooling, unseeded operation, partial thermal cycling, and post-filtration redissolution/recrystallization did not reduce fines to an acceptable level. The second recrystallization still ended at fines 1.0 despite purity 1.0 and recovery 0.525 (runner-operation-0249).

## H4 [rejected]
Tenfold lower upstream loading sharply reduced recovery without resolving fines. This does not support dilution as a useful lever under the paired lower-catalyst test.

## H5 [rejected in tested dose range]
Cumulative seed escalation to about 2 g did not improve the particle distribution relative to 0.05 g dosing and left recovery essentially unchanged.

## Final decision
No completed batch meets both purity >=0.80 and fines <=0.50; the failure is large compared with stated instrument noise. Select batch 10 only as the best observed recovery fallback (0.5323, purity 0.9787), while clearly flagging its fines result of 1.0. Batch 9 is an almost indistinguishable ordinary-seed alternative (recovery 0.5312) and would be preferred operationally if minimizing seed use mattered, but that was not the primary objective.
