# repeat-01 / C-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:01:23.643075+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Solvent S2 should favor large, relatively pure crystals because its dossier combines high growth, low occlusion, low nucleation, and low solubility. A slow cool with modest seeding and a cold hold should therefore meet purity/fines constraints while improving recovery relative to fast cooling.

H2 [tentative] Catalyst C1 or C3 may give strong reaction performance; initial screen will use C1 with full reagent/catalyst loading and a high-temperature hold. A paid HPLC reading will distinguish insufficient conversion from downstream crystallization loss.

Prediction before batch 1: C1/S2, 0.04 mol reagent, 0.005 mol catalyst, reaction near 370 K, then slow cooling to ~275 K with modest seed and hold should form filterable crystals with fines <=0.50 and purity >=0.80. If conversion is poor, vary catalyst/temperature; if crystal recovery is poor despite conversion, intensify cold hold or reduce solvent.

## Revision 2

Recorded: 2026-10-13T17:02:35.161741+00:00; available public operations: 27; reviewed through: runner-operation-0027.

# Working hypotheses after batches 1–2

H1 [supported in tested scope] S2 gives high crystal purity (~0.99 final assay in both batches). Batch 2's slower/deeper crystallization with lower seed and longer hold reduced fines from ~0.50 to ~0.39 and increased size/CSD quality, while measured crystal recovery remained ~0.423 (events runner-operation-0014 and -0027). Because reaction catalyst, solvent volume, and thermal history changed together, the recovery invariance is numerical rather than isolated causal evidence.

H2 [revised] C1 at 370 K and C3 at 350 K both reached complete apparent conversion by HPLC/final assay, but selectivity/yield were only about 0.48–0.53 with substantial byproduct. Reaction selectivity is not the binding product-crystal purity constraint under S2, but lower reaction temperature/catalyst alternatives remain worth screening.

H3 [tentative] Crystal recovery may be limited by S2 equilibrium/filter capture near 0.42 rather than reaction loading. Test consequence: lowering S2 volume further at the same reagent charge and cold endpoint should raise recovery if dissolved-product loss dominates; if recovery remains unchanged, a solvent/material-specific ceiling or filtration loss is more likely.

Decision: retain slow cooling to 250 K, long cold hold, low seed, and S2 as current feasible baseline; vary solvent volume and thermal cycling next. A substantially higher recovery with purity >=0.80 and fines <=0.50 would supersede batch 2.

## Revision 3

Recorded: 2026-10-13T17:04:37.968614+00:00; available public operations: 135; reviewed through: runner-operation-0135.

# Working hypotheses after batches 3–10

H1 [supported, bounded scope] S2 remains the only tested solvent consistently combining ~0.98–1.00 crystal purity with controllable fines. S1 can raise recovery (up to ~0.48) but its observed fines were 0.67–1.00, so it does not meet the stated constraint (events runner-operation-0053, -0068).

H3 [revised] Recovery and fines show a coupled concentration/seed regime rather than a simple dissolved-loss trend. S2 at 0.02 L or 0.05 L produced extreme fines (~0.995–1.0; events -0040, -0122). At 0.06 L with 0.001–0.003 g seed, recovery rose to ~0.45 but final fines sat just above 0.50 (-0096, -0109). At 0.04 L and 0.005 g seed, recovery was ~0.451 with fines ~0.398 and purity ~0.983 (-0135), exceeding the earlier feasible batch 2 recovery (~0.423).

H4 [supported in tested scope] Reheating already crystallized slurry and recooling sharply increased fines to 1.0 in both S1 and S2, even when reheating was mild (events -0068 and -0083). Suspend thermal cycling unless a materially different temperature policy is available.

Decision: current recommendation candidate is batch 10. Test slightly lower seed at otherwise matched S2/0.04 L conditions; retain batch 10 unless recovery improves while final fines remain <=0.50. Differences near 0.50 are treated cautiously because final-assay fines noise is stated as 0.018.

## Revision 4

Recorded: 2026-10-13T17:05:12.604103+00:00; available public operations: 160; reviewed through: runner-operation-0160.

# Final source-stage interpretation

H1 [supported in campaign scope] S2 at 0.04 L with full 0.04 mol reagent and 0.005 mol C3, reaction at 350 K, small seeding, slow cooling to 250 K, and a long cold hold is the most reliable tested region for meeting purity and fines constraints.

H3 [supported in tested local region; magnitude uncertain] Batch 10 (0.005 g seed) gave the highest observed qualifying crystal recovery, ~0.451, with purity ~0.983 and fines ~0.398 (runner-operation-0135). Batch 12 repeated the same recipe and also qualified, with recovery ~0.444, purity ~0.999, and fines ~0.388 (runner-operation-0160). The ~0.006 recovery difference is smaller than the stated 0.01 final-assay recovery noise, so batch 10 is selected on observed value but not claimed superior to its replicate.

H4 [supported in tested scope] Reheat/recool policies tested here caused extreme fines and should not be recommended. More concentrated (0.02 or 0.05 L) and more dilute/low-seed (0.06 L) regimes also failed the fines constraint or sat just above it.

Final decision: recommend completed batch 10 because it has the highest observed crystal recovery among batches satisfying purity >=0.80 and fines <=0.50. Batch 12 is corroborating evidence for recipe robustness. Change this decision only if repeat testing establishes a higher qualifying recovery, especially near the 0.05–0.06 L boundary without the observed fines penalty.
