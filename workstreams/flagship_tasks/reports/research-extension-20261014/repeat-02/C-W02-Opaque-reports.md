# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The materials are anonymous benchmark identities, so the mechanism below is phenomenological rather than a claim about real chemical structures. Catalyst C0, nitrogen atmosphere, near-ambient pressure, a 350 K/1800 s reaction, and a 0.04 mol reagent charge were held essentially fixed. Consequently, the campaign supports strong conclusions about solvent and crystallization history, but not about alternative catalysts, atmospheres, or reaction mechanisms.

Reaction stage and coupling to crystallization

With S0, batch 1 gave essentially complete conversion by HPLC (0.9992), but only about 0.726 selectivity and 0.718 reaction yield. Thus conversion was not the limiting variable: competitive byproduct formation determined the target inventory entering crystallization. Final-assay reaction yield declined across the solvent series under otherwise comparable processing: approximately 0.695 for S1 (batch 7), 0.646 for S2 (batch 8), and 0.550 for S3 (batch 9). I interpret this as a solvent effect on reaction selectivity, although altered analytical response or another solvent-dependent kinetic pathway remains untested.

A useful inventory relation is

n_target,pre-separation ≈ n_reagent,0 × reaction yield,

while the reported seed-excluded crystal recovery is

Y_crystal = n_target,recovered crystals / n_target,pre-separation.

Therefore Y_crystal is a separation-stage recovery, not overall isolated yield. A rough overall target yield is reaction yield × Y_crystal. This product was about 0.401 for batch 10. For comparison, batch 7 was about 0.430, but it violated the fines constraint. Solvent choice therefore imposed a genuine reaction–crystallization compromise: S1 preserved more target before separation, whereas S2 produced a much better particle population.

Material effects

Solvent was the dominant observed material variable. Under the same small-seed/annealing program, final fines fractions were 0.583 for S1 (batch 7), 0.273 for S2 (batch 8), and 0.462 for S3 (batch 9). Corresponding crystal recoveries were 0.619, 0.594, and 0.460. S2 therefore offered the best robust combination of recovery and particle quality. S3 technically met the fines limit, but with substantially lower recovery; S1 had slightly higher recovery but failed the fines specification. Because the declared fines noise was 0.018, the S2–S1 difference is much larger than measurement noise. S3’s 0.462 result was only modestly below the 0.50 boundary and is less robust.

My interpretation is that S2 reduced the rate of secondary nucleation relative to crystal growth. This could reflect a more favorable solubility–temperature curve, interfacial energy, viscosity, or seed wetting, but those alternatives were not separately measured. No molecular identity is available, so selecting among them would be speculative.

All tested crystal purities were high—typically 0.98–1.00—even when reaction selectivity was only about 0.54–0.72. Crystallization therefore rejected much of the reaction impurity/byproduct population. Purity can be represented as

P = n_target,solid / n_total,solid,

and the particle constraint as

F20 = N(d < 20 micrometres) / N_total ≤ 0.50.

The fact that purity remained high while fines varied widely indicates that chemical rejection and particle-number control were largely separable in this campaign.

Process-history dependence

Direct cooling was insufficient in S0. Batch 1 used 0.020 g seed and cooling to 280 K; it recovered 0.577 with purity 0.985 but had a fines fraction of 0.827. Reducing the seed to 0.001 g and cooling more slowly to 300 K in batch 2 lowered fines to 0.705 and increased the normalized size estimate, but still failed the particle constraint. This comparison is confounded by endpoint and cooling time, so it supports—but does not isolate—a seed-number effect.

A partial-redissolution cycle improved particle quality. In batch 4, material was slowly cooled, reheated to 315 K, recooled, and finally cooled to 280 K. Recovery was 0.577 and fines fell to 0.622, better than the earlier S0 batches but still infeasible. The plausible mechanism is preferential dissolution of small, high-curvature particles during reheating, followed by deposition onto surviving larger crystals during recooling—an Ostwald-ripening-like selection step. A second annealing cycle in batch 5 did not further reduce S0 fines: recovery increased to 0.610 after cooling to 250 K, but fines remained 0.622. Thus annealing alone could not overcome the unfavorable S0 nucleation regime.

Seeding after an initial precool to 330 K did not help. Batch 6 produced recovery 0.585 but fines 0.744. This revised the initial expectation that seeding nearer the metastable region would necessarily favor controlled growth. Possible explanations include spontaneous nuclei forming before seed addition or excessive supersaturation at the eventual growth stage; neither alternative was directly observed.

Concentration was critical. Batch 11 reduced S2 volume from 0.060 L to 0.040 L. Recovery remained about 0.614, but fines rose catastrophically to 0.994 and CSD quality fell to 0.522. I interpret this as a secondary-nucleation burst caused by excessive supersaturation: increasing concentration produced no useful recovery benefit because target material was redistributed among many fine particles. This result strongly rejects the concentrated formulation for the stated objective.

Within S2 at 0.060 L, lowering the final temperature from 280 K in batch 8 to 250 K in batch 10 increased observed recovery from 0.594 to 0.615 while retaining acceptable fines (0.301) and purity (0.982). This is consistent with lower equilibrium solubility at the colder endpoint. However, the recovery difference is only about 0.021 and each assay has a declared crystal-yield standard deviation of 0.010, so the improvement is suggestive rather than a precise causal estimate.

An additional 250 K crystallization stage in batch 12 did not improve recovery: it gave 0.609 versus 0.615 in batch 10. Batch 12 had a larger normalized crystal-size estimate (0.099 versus 0.072) and somewhat higher CSD quality (0.790 versus 0.759), consistent with continued ripening, but the crystal-size noise is 0.025, making that apparent size increase uncertain. The extra cold residence may have changed morphology without appreciably changing equilibrium recovery.

Recommended batch and unresolved tradeoff

The sealed recommendation remains batch 10: S2 at 0.060 L, C0, 350 K reaction for 1800 s, 0.001 g seed, slow cooling to 300 K, partial redissolution at 315 K, slow recooling to 300 K, final slow cooling to 250 K, then filtration. Its final assay gave crystal recovery 0.6147, purity 0.9816, and fines 0.3014. It had the highest observed recovery among batches clearly satisfying both constraints.

Batch 12 was a close feasible confirmation at recovery 0.6086, purity 0.9979, and fines 0.2920. The batch-10 versus batch-12 recovery difference, 0.0061, is smaller than the 0.010 single-assay recovery noise and well below the uncertainty of their difference. Thus the intrinsic recovery ordering of those two histories is unresolved; batch 10 is retained because it had the highest observed feasible recovery and avoids an unnecessary extra cold stage.

The main unresolved tradeoff is that conditions increasing supersaturation or lowering temperature can increase recovery but may also increase secondary nucleation. S2 provided enough morphological margin to cool to 250 K, whereas higher concentration destroyed that margin. The best untested directions would be replicated S2 runs near the batch-10 conditions, modest changes to the 315 K anneal, or alternative catalysts that improve reaction selectivity without changing crystallization behavior. Those possibilities were not tested and are not part of the recommendation.

Revision of the working account

The initial hypothesis emphasized slow seeded cooling as sufficient to control fines. Batches 1–3 contradicted that strong form: recovery and purity were good, but fines remained excessive. The account was revised first to include selective redissolution/annealing (batches 4–6), which helped but was insufficient in S0, and then to recognize solvent identity as the dominant control variable (batches 7–9). Final S2 experiments showed that cold-end recovery could be raised while retaining a wide fines margin, but also demonstrated that concentration cannot be increased indiscriminately. Conclusions based on large solvent and concentration effects are relatively strong; small differences among batches 8, 10, and 12 remain uncertain because they are comparable to assay noise and were not replicated exactly.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.53 | 0.4 | 0.66 |
| Q01 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q01 | crystal_size | 0.076 | 0.045 | 0.115 |
| Q01 | crystal_yield | 0.6 | 0.47 | 0.71 |
| Q02 | crystal_fines_fraction | 0.42 | 0.29 | 0.55 |
| Q02 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.105 | 0.065 | 0.155 |
| Q02 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q03 | crystal_fines_fraction | 0.26 | 0.14 | 0.41 |
| Q03 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q03 | crystal_size | 0.155 | 0.095 | 0.225 |
| Q03 | crystal_yield | 0.54 | 0.41 | 0.66 |
| Q04 | crystal_fines_fraction | 0.58 | 0.44 | 0.71 |
| Q04 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q04 | crystal_size | 0.071 | 0.04 | 0.11 |
| Q04 | crystal_yield | 0.57 | 0.44 | 0.69 |
| Q05 | crystal_fines_fraction | 0.45 | 0.32 | 0.59 |
| Q05 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q05 | crystal_size | 0.1 | 0.058 | 0.155 |
| Q05 | crystal_yield | 0.57 | 0.44 | 0.69 |
| Q06 | crystal_fines_fraction | 0.74 | 0.59 | 0.87 |
| Q06 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q06 | crystal_size | 0.052 | 0.025 | 0.09 |
| Q06 | crystal_yield | 0.6 | 0.47 | 0.72 |
| Q07 | crystal_fines_fraction | 0.41 | 0.28 | 0.55 |
| Q07 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q07 | crystal_size | 0.112 | 0.065 | 0.17 |
| Q07 | crystal_yield | 0.58 | 0.45 | 0.7 |
| Q08 | crystal_fines_fraction | 0.27 | 0.15 | 0.42 |
| Q08 | crystal_purity | 0.98 | 0.93 | 0.998 |
| Q08 | crystal_size | 0.16 | 0.095 | 0.235 |
| Q08 | crystal_yield | 0.48 | 0.34 | 0.62 |
| Q09 | crystal_fines_fraction | 0.88 | 0.72 | 0.97 |
| Q09 | crystal_purity | 0.985 | 0.93 | 1 |
| Q09 | crystal_size | 0.035 | 0.015 | 0.065 |
| Q09 | crystal_yield | 0.025 | 0 | 0.09 |
| Q10 | crystal_fines_fraction | 0.61 | 0.45 | 0.76 |
| Q10 | crystal_purity | 0.975 | 0.91 | 0.999 |
| Q10 | crystal_size | 0.068 | 0.035 | 0.11 |
| Q10 | crystal_yield | 0.3 | 0.17 | 0.44 |
| Q11 | crystal_fines_fraction | 0.48 | 0.34 | 0.62 |
| Q11 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q11 | crystal_size | 0.09 | 0.052 | 0.14 |
| Q11 | crystal_yield | 0.59 | 0.46 | 0.71 |
| Q12 | crystal_fines_fraction | 0.81 | 0.65 | 0.93 |
| Q12 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q12 | crystal_size | 0.048 | 0.022 | 0.085 |
| Q12 | crystal_yield | 0.7 | 0.56 | 0.81 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when seed-excluded product recovery is very small. Q01/Q02: S1 is predicted to recover more target but generate more fines than S3, echoing the observed solvent-dependent recovery–morphology tradeoff. Q03/Q04: reducing seed mass should lower the initial particle count, increasing number-weighted size and reducing fines, with little change in equilibrium recovery. Q05/Q06: gradual cooling should suppress a nucleation burst; rapid cooling to 278.15 K can reach similar recovery after the long hold but leaves a finer population. Q07/Q08: the terminal 315 K anneal should preferentially dissolve small particles and improve size/fines, while the short recooling period leaves lower recovery. Q09/Q10: 60 seconds permits almost no seed-excluded recovery; a 7200-second hold adds product and growth but is still predicted to remain fines-infeasible. Q11/Q12: doubling reagent concentration should raise fractional recovery through greater supersaturation but strongly increase secondary nucleation and impurity incorporation. The 80% intervals are epistemic and deliberately broad because catalyst C1, the 385 K reaction/quench sequence, very long multistage cooling, and these seed-to-charge ratios were not directly tested. Feasibility flags use point estimates; Q02, Q05, and especially Q11 remain boundary-sensitive.

## K2

1. Claim status

Supported by direct observations:
- Solvent identity strongly affected crystal morphology and recovery. Under closely matched processing, batch 7 (S1) gave recovery 0.619 and fines 0.583, batch 8 (S2) gave 0.594 and 0.273, and batch 9 (S3) gave 0.460 and 0.462. The interpretation that S2 favored growth over secondary nucleation is plausible, but the specific physical cause—solubility curve, interfacial energy, viscosity, or seed wetting—remains unmeasured.
- Concentration strongly affected fines. Batch 10 used 0.060 L S2 and gave recovery 0.615 with fines 0.301; batch 11 used 0.040 L and gave similar recovery, 0.614, but fines 0.994. The observed adverse concentration effect is strong. Attributing it specifically to a supersaturation-driven secondary-nucleation burst is interpretation rather than direct observation.
- High purity was broadly maintained despite moderate reaction selectivity. Examples include batches 7–12, with crystal purities about 0.976–1.000. This directly supports effective impurity rejection during crystallization.
- Batch 10 and batch 12 both demonstrated feasible S2 processes: respectively, recovery/purity/fines of 0.615/0.982/0.301 and 0.609/0.998/0.292.

Partly supported or confounded:
- Lower seed loading appeared beneficial for particle quality: batch 1 used 0.020 g seed and had fines 0.827, whereas batch 2 used 0.001 g and had fines 0.705. However, cooling endpoint and duration also changed, so seed mass was not isolated.
- Partial redissolution appeared to improve S0 morphology. Batch 4, including a 315 K anneal, had fines 0.622 versus 0.705 in batch 2, but other thermal-history differences prevent a clean causal attribution. A second annealing cycle in batch 5 did not improve fines beyond about 0.622.
- Cooling S2 to 250 K may have increased recovery: batch 10 gave 0.615 versus 0.594 for batch 8 at a warmer endpoint. The difference is only about 0.021, close to the uncertainty of comparing two assays, so the magnitude remains uncertain.
- The larger size and higher CSD quality in batch 12 relative to batch 10 are consistent with continued ripening, but the size difference is comparable to the declared size uncertainty.

Contradicted or narrowed:
- The initial claim that slow seeded cooling alone would ensure acceptable fines was contradicted by batches 1–3, whose fines remained approximately 0.68–0.83.
- The idea that seeding after precooling would improve control was contradicted in the tested S0 implementation: batch 6 had fines 0.744.
- The idea that simply adding more annealing cycles would continue improving S0 morphology was contradicted by batch 5, which retained fines near 0.622.
- Increasing concentration as a route to higher quality-constrained recovery was contradicted by batch 11: recovery did not materially improve, while particle quality collapsed.

Still untested:
- Alternative catalysts, including whether they could improve reaction selectivity without harming crystallization.
- The molecular reason S2 suppresses fines.
- An S2 process identical to batch 10 but without the 315 K anneal.
- Exact repeatability of batches 10 and 12; their recovery ordering is unresolved.
- Independent effects of atmosphere, pressure, stirring during crystallization, seed-size distribution, and seed purity.

2. One additional experiment

I would repeat the batch-10 S2 process but omit the 315 K reheating step: 0.060 L S2, C0, the same reaction and 0.001 g seed, slow cooling to 300 K, continued slow cooling to 250 K, filtration, and final assay. I would include non-destructive particle-size measurements immediately after reaching 300 K and immediately before filtration.

This would distinguish two explanations:
- Anneal-controlled mechanism: reheating selectively dissolves fine particles, after which material grows on surviving crystals.
- Solvent-controlled mechanism: S2 itself establishes the favorable particle distribution, and the anneal contributes little or merely reduces recovery through temporary redissolution.

Expected alternatives:
- If the no-anneal batch has substantially higher fines and lower size/CSD quality than batch 10 at similar recovery, the selective-redissolution account is supported.
- If its final fines remain near 0.30 with comparable recovery, S2 is the dominant cause and the anneal is unnecessary.
- If omitting annealing raises recovery but also pushes fines toward or above 0.50, that would demonstrate a real recovery–quality tradeoff.
- If both recovery and particle metrics vary only within measurement uncertainty, neither mechanism is resolved and replication, rather than further recipe elaboration, becomes the priority.

3. Least effectively used evidence and least reliable prediction

The account used the paired in-process particle-size readings least effectively. Several batches had a particle measurement before filtration and a final-assay particle estimate afterward—for example, batch 10 had prefilter fines about 0.280 and final fines 0.301, while batch 7 had about 0.597 and 0.583. I mostly relied on final assays instead of using these pairs to assess measurement variability, possible filtration effects, and the robustness of feasibility classifications. Because the two instruments have different noise models and the measurements occur at different process points, they cannot simply be treated as replicates, but their discrepancies were still informative.

Q09 is the least reliable held-out prediction. Its crystallization consists of only a 60-second drop to 292 K before filtration, whereas the source experiments used crystallization periods of thousands to tens of thousands of seconds. The predicted seed-excluded yield therefore required an extreme short-time kinetic extrapolation with no direct calibration. The large 0.025 g seed guarantees particles but does not guarantee newly crystallized target, making it especially difficult to separate seed presence from seed-excluded recovery and to predict the number-weighted size distribution. Q12 is also uncertain because it extrapolates the batch-11 concentration effect into a different absolute concentration and reaction regime, but at least its directional claim has a direct source-stage analogue.
