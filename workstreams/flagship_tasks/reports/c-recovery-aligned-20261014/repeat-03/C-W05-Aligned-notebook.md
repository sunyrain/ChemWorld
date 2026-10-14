# repeat-03 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:34:15.220753+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Solvent S2 should favor recovery and coarse, clean crystals because its dossier combines low relative solubility, high growth, low nucleation and low impurity occlusion. S1 is the conservative comparator; S0 is expected to give more fines/occlusion.

H2 [tentative] Catalyst C1 or C3 may outperform C0, but world-specific residuals could reverse the nominal ranking. A moderate-temperature reaction followed by controlled seeded cooling should preserve purity better than aggressive heat or crash cooling.

Prediction for batch 1: C1/S2 with near-full charge, moderate heating, seeding, slow cooling and growth hold will exceed the 0.10 recovery feasibility target while meeting purity >=0.80 and fines <=0.50. If reaction conversion is weak, test catalyst/temperature before refining crystallization; if fines are high, reduce seed and slow/interrupt cooling.

## Revision 2

Recorded: 2026-10-14T11:35:54.896361+00:00; available public operations: 48; reviewed through: runner-operation-0048.

# Working hypotheses

H1 [supported in tested scope] S2 permits clean product: all four S2 batches met purity and fines constraints, with final crystal yields 0.35-0.42 (events runner-operation-0012, -0024, -0036, -0048). This is far above the feasibility target. Crystals remain small and fines are near the upper bound, so crystallization history still merits optimization.

H2 [tentative, revised] At 355 K/3600 s, C0 is the leading catalyst (batch 2, yield 0.417) but its numerical advantage over C3 (0.408) and C1 (0.388) is not yet repeatability evidence; C2 was poorer (0.350). HPLC selectivity/yield rankings broadly agree that C2 is weak, while C0/C1/C3 are close (events runner-operation-0007, -0019, -0031, -0043).

Next tests: use C0/S2 to map reaction temperature, then compare solvents. Prediction: lower reaction temperature may reduce byproduct but risk incomplete conversion; S1 may improve purity but lower recovery, while S3 may improve upstream formation but worsen crystallization quality. After identifying a reaction regime, test deeper/slower cooling and growth holds to raise recovery without pushing fines above 0.50.

## Revision 3

Recorded: 2026-10-14T11:36:46.662161+00:00; available public operations: 109; reviewed through: runner-operation-0109.

# Working hypotheses

H1 [supported in tested scope] Reaction temperature dominates the tested upstream conditions: C0/S2 at 375 K for 2400 s produced 0.524 crystal yield with acceptable purity/fines (batch 6, runner-operation-0072), versus 0.417 at 355 K (batch 2) and 0.291 at 335 K (batch 5). HPLC selectivity increased correspondingly (runner-operation-0055, -0067). The tested safety risk remained below the campaign limit.

H2 [supported qualitatively] S2 is preferable downstream. S1 at 355 K gave similar high yield but fines 0.550 (batch 7), and S3 produced fines 0.793 (batch 8); both violated the fines constraint. This solvent comparison is confounded by temperature relative to the selected 375 K regime, so it supports but does not prove an intrinsic solvent effect.

H3 [tentative] With C0/S2 at 375 K, low seed dose and staged slow cooling should modestly improve recovery while retaining fines compliance. Batch 9 used 0.005 g seed and staged cooling to 278 K and reached yield 0.527, purity 0.985, fines 0.452 (runner-operation-0109); the numerical gain over batch 6 is small relative to unknown run variability. Test deeper cooling plus a growth/ripening hold; abandon deeper cooling if fines cross 0.50.

## Revision 4

Recorded: 2026-10-14T11:37:38.146164+00:00; available public operations: 151; reviewed through: runner-operation-0151.

# Final source-stage hypotheses

H1 [supported in sampled domain] For C0/S2 with the tested loading, hotter short reaction treatments improved overall crystal recovery and reaction selectivity without violating purity or fines constraints: 375 K gave 0.544 yield after deep staged cooling/hold (batch 10, runner-operation-0123), 395 K gave 0.592 (batch 11, runner-operation-0137), and 415 K gave 0.626 (batch 12, runner-operation-0151). The upward differences are numerically larger than adjacent instrument noise, but temperature and duration changed together and each condition lacks replication, so the precise causal law and optimum remain unresolved.

H2 [supported in sampled domain] Staged cooling to 265 K followed by a low-agitation hold retained fines compliance while increasing recovery relative to the earlier 278 K recipes. Batch 10 reached fines 0.435 and yield 0.544 versus batch 9 at fines 0.452 and yield 0.527 (events runner-operation-0123 and -0109). This comparison is not a clean decomposition because the final temperature and hold both changed.

H3 [supported for decision] Batch 12 is the best observed feasible process: crystal yield 0.626, purity 0.999, fines 0.468, with crystal size index 0.099 and CSD quality 0.661 (runner-operation-0151). Batch 11 provides a more comfortable fines margin (0.431) but lower yield (0.592). Since the research goal prioritizes maximum recovery subject to the stated constraints, select batch 12.

Scope and unresolved alternatives: the campaign did not replicate the leading condition, independently separate reaction temperature from residence time, or test beyond 415 K. The batch-12 fines result is close enough to the 0.50 limit that confirmation would be prudent. A future result showing reproducible fines above 0.50 or lower recovery would favor batch 11; otherwise extend the temperature/residence-time map cautiously and refine the 265 K hold.
