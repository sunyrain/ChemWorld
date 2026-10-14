# repeat-03 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:50:03.145534+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative].** With opaque materials, catalyst/solvent identity and reaction temperature are likely the dominant upstream controls of target formation and purity. A broad screen should locate a feasible chemistry before crystallization refinement.

**H2 [tentative].** Seeded, slow cooling with a growth hold should reduce number-weighted fines relative to abrupt unseeded cooling, while sufficiently low terminal temperature should improve overall crystal recovery. Prediction for the first batch: a moderate reaction temperature followed by seeding and slow cooling will produce detectable crystals, but feasibility (purity >=0.80 and fines <=0.50) is uncertain.

**Decision rule.** Use early batches for material/temperature screening, then spend later batches around the best feasible result; prefer higher crystal_yield only among batches satisfying both quality constraints. These commitments will be revised only using public observations.

## Revision 2

Recorded: 2026-10-14T11:51:59.044398+00:00; available public operations: 46; reviewed through: runner-operation-0046.

# Working hypotheses

**H1 [supported in screened scope].** At 0.04 mol reagent, 0.08 L S0, 0.005 mol catalyst, 360 K for 1800 s, C0 gave the highest observed crystal recovery (~0.569) and reaction yield (~0.737); C1 and C3 were modestly lower, while C2 was substantially lower (~0.380 crystal recovery). Evidence: final assays runner-operation-0013, -0024, -0035, -0046. Because batches were not replicated and batch 1 had a different post-cooling hold, numerical catalyst differences remain provisional.

**H2 [rejected for current recipe].** A 0.05 g seed followed by 7200 s cooling to 278 K does not control fines: batches 2–4 all had final fines ~0.89–0.98 despite high purity. Evidence: runner-operation-0024, -0035, -0046. Batch 1 was also fines-rich (~0.87; runner-operation-0013). The next crystallization tests should reduce nucleation density and/or add a dissolution-ripening cycle rather than merely repeat this schedule.

**H3 [tentative].** Solvent identity may change both upstream selectivity and crystallization recovery. Screen S1–S3 with C0 before fixing upstream conditions.

**Decision rule.** Optimize fines only after the solvent screen, retaining C0 unless another solvent-catalyst combination clearly improves feasible recovery. Quality feasibility still requires purity >=0.80 and fines <=0.50.

## Revision 3

Recorded: 2026-10-14T11:53:54.384217+00:00; available public operations: 134; reviewed through: runner-operation-0134.

# Final source-stage hypotheses

**H1 [supported in screened scope].** C0 is the preferred catalyst among C0–C3 for the tested 360 K/1800 s regime. The catalyst screen in S0 gave the highest observed recovery with C0; exact differences remain unreplicated (runner-operation-0013, -0024, -0035, -0046).

**H3 [supported in screened scope].** Solvent identity strongly affected particle quality. With otherwise matched C0/360 K chemistry and 0.05 g seed, S2 achieved the first feasible result (crystal_yield ~0.609, purity 1.00, fines ~0.456; runner-operation-0068), whereas S0, S1, and S3 exceeded the fines limit (runner-operation-0013, -0057, -0079).

**H4 [supported in S2 scope].** Reducing seed from 0.05 g to 0.005 g and extending cooling to 14400 s substantially reduced fines while maintaining or improving recovery. At terminal temperatures 278, 268, and 250 K, final fines were ~0.306, 0.324, and 0.342 and recoveries ~0.620, 0.626, and 0.647 (runner-operation-0090, -0101, -0112). These are numerical single-batch comparisons, so repeatability is unresolved, but all three comfortably met both constraints.

**H5 [narrowed].** Lowering reaction temperature to 340 K for 3600 s worsened recovery and selectivity in the tested S2 process (runner-operation-0123), opposing the hypothesis that milder heating would suppress byproduct. Reducing S2 volume to 0.06 L retained high recovery (~0.645) but marginally failed the fines constraint (~0.510; runner-operation-0134), so the apparent concentration benefit is not recommended without further particle-control work.

**Decision.** Recommend batch 10: 0.04 mol reagent, 0.08 L S2, 0.005 mol C0; heat 360 K for 1800 s at 500 rpm; seed 0.005 g; cool to 250 K over 14400 s; filter. It had the highest observed feasible seed-excluded crystal recovery (~0.647), with purity ~0.979 and fines ~0.342 (runner-operation-0112). Batch 9 is a slightly lower-recovery feasible fallback. A replicate of batch 10 would be the first follow-up because measurement/process variability is not established.
