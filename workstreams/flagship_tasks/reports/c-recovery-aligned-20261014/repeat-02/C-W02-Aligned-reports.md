# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

The system is best described as a reaction-limited target-forming step followed by efficient but strongly nucleating crystallization.

The useful bookkeeping relationship is

Y_crystal = n(target in isolated crystals)/n(initial reagent) ≈ X·S·η_capture,

where X is conversion, S is target selectivity among converted material, and η_capture represents crystallization plus isolation. This is an interpretation rather than an exact fitted law because the assay channels are independently noisy. For batch 12, reaction yield was 0.636 and crystal yield was 0.575, implying an approximate capture fraction of 0.90. Thus most target formed by the reaction was recovered, and further recovery gains would increasingly require better reaction selectivity as well as crystallization.

Material effects

Catalyst identity had the clearest experimentally supported effect. In the approximately standardized C0/C1/C2/C3 screen using S2, 0.04 mol reagent, 0.07 L solvent, 365 K reaction, and staged cooling, reaction yield/crystal yield were approximately: C0 batch 9, 0.637/0.552; C1 batch 7, 0.591/0.509; C2 batch 10, 0.464/0.381; and C3 batch 11, 0.520/0.437. C0 therefore outperformed the catalysts that had appeared stronger from nominal reference-panel activity. I interpret this as reaction-specific or fixed-world catalyst compatibility not represented by the aggregate material dossier. This comparison is strong relative to assay noise, but it lacks replication.

S2 was the most useful solvent in the explored recipes. Its nominal low solubility, low impurity occlusion, and high growth tendency are consistent with the high recovery and purity obtained in batches 7, 9, and 12. However, its nominally low nucleation tendency did not predict acceptable particle quality. S3 gave only 0.330 crystal yield in batch 8, while S1 gave 0.481 in batch 6. Those solvent comparisons are only suggestive because reaction temperature, seed amount, and cooling history were not completely matched. S0 was tested mainly as a resuspension solvent rather than in a controlled primary-solvent comparison.

Reaction–crystallization coupling

Conversion was usually near unity, but target yield varied substantially. For example, batch 12 had conversion 1.000, selectivity 0.631, byproduct signal 0.269, and reaction yield 0.636. Batch 10 also had high conversion, 0.986, but reaction yield was only 0.464. High conversion was therefore not sufficient: catalyst-dependent partitioning between target, byproduct, and degradation controlled the maximum recoverable target.

Crystallization then captured a large fraction of whatever target had formed. Approximate capture ratios Y_crystal/Y_reaction were 0.83 in batch 1, 0.87 in batch 9, and 0.90 in batch 12. Deeper cooling plausibly increased this ratio by reducing target solubility. Batch 9, ending at 278 K with 0.07 L S2, gave 0.552 recovery; batch 12, using 0.08 L S2 and cooling to 250 K, gave 0.575. Because both endpoint temperature and solvent volume changed and neither condition was replicated, the 0.023 difference is directional evidence, not an isolated estimate of the temperature effect.

Process-history dependence and particle mechanism

Particle quality is naturally represented by the number-based population balance

F20 = ∫[0,20 µm] n(L)dL / ∫[0,∞] n(L)dL.

Every completed batch gave F20 near 0.98–1.00, far above the required 0.50. I interpret this as pervasive primary or secondary nucleation producing a very large number of small particles. Number weighting makes even a modest mass of fines dominate F20. Individual normalized crystal-size estimates were noisy and occasionally appeared inconsistent with the reported fines fraction; consequently, the repeated fines measurements and their large distance from the threshold are more persuasive than any single size estimate.

Several history interventions failed to remove this fine-particle population:

- Batch 3 stopped crystallization at 310 K, yet recovery was 0.390 and fines were 0.995. Avoiding the deepest supersaturation therefore did not restore acceptable size.
- Batch 4 halved reagent loading to 0.02 mol at fixed solvent volume, but still gave fines 1.000, recovery 0.341, and purity 1.000. Dilution reduced reaction and recovery performance without solving nucleation.
- Batch 5 omitted seed, used extremely long cold aging, and included S0 resuspension/warming; its final fines fraction remained 1.000 and recovery was 0.380. Thus ordinary Ostwald-ripening or selective-dissolution interpretations were not supported in the tested conditions.
- Batch 2 used staged cooling followed by partial reheating and recooling; it still gave fines 1.000 and recovery 0.429.
- Seed charges from 0.001 to 0.05 g did not solve fines. An apparent plan to test cumulative high seed loading was later rejected as an interpretation because the campaign ledger showed repeated identical seed calls did not create a cumulative dose: only 0.05 g was recorded for those batches. A true high-dose or controlled seed-size-distribution experiment therefore remains untested.

The principal unresolved tradeoff is that colder, more exhaustive crystallization improved overall recovery but did not improve particle compliance and could mechanistically intensify secondary nucleation. Purity was not the limiting quality attribute: batch 12 had purity 0.995, and most batches were around 0.97–1.00. The unresolved problem is recovery versus number-based fines, not recovery versus chemical purity.

Revisions and uncertainty

The initial expectation was that C1 and S2 would be favored by their nominal activity and crystallization properties. Experimental evidence retained S2 but overturned the catalyst ranking in favor of C0. After batches 1–3 showed excellent purity and recovery but nearly all-fines populations, the working hypothesis shifted from ordinary slow cooling to dilution, no-seed aging, thermal cycling, and selective resuspension. Batches 4–6 failed to support those remedies. A subsequent high-seed hypothesis was withdrawn when resource accounting showed that a cumulative high dose had not actually been executed. The final catalyst screen then established C0/S2 as the best observed recovery combination.

Final-assay noise was approximately 0.01 for crystal yield and purity and 0.018 for fines. Single-batch rankings close together should therefore be treated cautiously, especially without replication. Nevertheless, the conclusion of noncompliance is robust: observed fines fractions were roughly 0.48–0.50 above the specification, far beyond measurement uncertainty, while purity margins were large.

Batch 12 remains the sealed operating recommendation because it had the highest observed seed-excluded recovery, 0.575, with purity 0.995. It is explicitly not a specification-compliant process because its fines fraction was 1.000. Untested alternatives include controlled reagent feeding to manage supersaturation, seeds with a characterized coarse size distribution, lower-shear equipment outside the available range, size-selective solid separation, and fundamentally different solvent-mixture or antisolvent trajectories. None should be presented as demonstrated solutions.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.28 | 0.12 | 0.48 |
| Q01 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q01 | crystal_size | 0.13 | 0.09 | 0.18 |
| Q01 | crystal_yield | 0.48 | 0.36 | 0.59 |
| Q02 | crystal_fines_fraction | 0.62 | 0.42 | 0.82 |
| Q02 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q02 | crystal_size | 0.072 | 0.035 | 0.115 |
| Q02 | crystal_yield | 0.42 | 0.3 | 0.54 |
| Q03 | crystal_fines_fraction | 0.72 | 0.51 | 0.9 |
| Q03 | crystal_purity | 0.93 | 0.84 | 0.98 |
| Q03 | crystal_size | 0.065 | 0.028 | 0.11 |
| Q03 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q04 | crystal_fines_fraction | 0.42 | 0.22 | 0.64 |
| Q04 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q04 | crystal_size | 0.105 | 0.06 | 0.155 |
| Q04 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q05 | crystal_fines_fraction | 0.36 | 0.18 | 0.57 |
| Q05 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q05 | crystal_size | 0.115 | 0.072 | 0.165 |
| Q05 | crystal_yield | 0.39 | 0.28 | 0.51 |
| Q06 | crystal_fines_fraction | 0.82 | 0.63 | 0.96 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q06 | crystal_size | 0.048 | 0.018 | 0.085 |
| Q06 | crystal_yield | 0.4 | 0.28 | 0.52 |
| Q07 | crystal_fines_fraction | 0.44 | 0.24 | 0.65 |
| Q07 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q07 | crystal_size | 0.108 | 0.065 | 0.16 |
| Q07 | crystal_yield | 0.4 | 0.28 | 0.52 |
| Q08 | crystal_fines_fraction | 0.32 | 0.13 | 0.58 |
| Q08 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q08 | crystal_size | 0.135 | 0.075 | 0.2 |
| Q08 | crystal_yield | 0.34 | 0.22 | 0.47 |
| Q09 | crystal_fines_fraction | 0.9 | 0.72 | 1 |
| Q09 | crystal_purity | 0.9 | 0.78 | 0.97 |
| Q09 | crystal_size | 0.04 | 0.012 | 0.075 |
| Q09 | crystal_yield | 0.07 | 0.01 | 0.16 |
| Q10 | crystal_fines_fraction | 0.66 | 0.43 | 0.85 |
| Q10 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q10 | crystal_size | 0.07 | 0.03 | 0.115 |
| Q10 | crystal_yield | 0.2 | 0.1 | 0.32 |
| Q11 | crystal_fines_fraction | 0.4 | 0.21 | 0.62 |
| Q11 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q11 | crystal_size | 0.11 | 0.065 | 0.16 |
| Q11 | crystal_yield | 0.39 | 0.28 | 0.51 |
| Q12 | crystal_fines_fraction | 0.7 | 0.49 | 0.88 |
| Q12 | crystal_purity | 0.87 | 0.75 | 0.95 |
| Q12 | crystal_size | 0.065 | 0.03 | 0.11 |
| Q12 | crystal_yield | 0.45 | 0.32 | 0.58 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is expected to outperform S3 in purity and particle quality because of its lower nominal solubility, nucleation tendency, and impurity occlusion, although S3 may support somewhat stronger reaction activity. Q03–Q04: the larger seed charge should consume supersaturation on existing surfaces and reduce secondary nucleation. Q05–Q06: gradual cooling should sharply reduce fines relative to an immediate temperature crash; equilibrium recovery should be similar. Q07–Q08: the 315 K thermal cycle may preferentially dissolve fines and enlarge survivors, but likely sacrifices recovery and has broad uncertainty because prior reheating did not reliably improve particles. Q09–Q10: continued growth at 292 K should increase seed-excluded recovery and size, but two hours is unlikely to erase the fine population created by the rapid initial cool. Q11–Q12: doubling reagent loading should increase supersaturation and recovery while worsening occlusion and number-based fines. All recipes contain seed, so particles are expected. Intervals are intentionally broad: these recipes extrapolate to smaller charges, 385 K reaction conditions, S0 as the primary solvent, and multi-day cooling histories not directly tested. The campaign’s persistent near-unity fines makes all predicted feasibility calls—especially those close to 0.50—substantially less certain than the purity predictions.

## K2

1. Status of the main claims

Supported by direct observations:
- Catalyst identity strongly affected target formation. Under broadly matched S2 recipes, batch 9 (C0) gave reaction yield 0.637 and crystal yield 0.552, versus batch 7 (C1: 0.591/0.509), batch 10 (C2: 0.464/0.381), and batch 11 (C3: 0.520/0.437). Interpreting C0 as the best catalyst in that tested regime is supported, although unreplicated.
- High conversion did not ensure high target yield. Batches 9–12 all had approximately complete conversion, yet reaction yields ranged from 0.464 to 0.637. The direct observation is the channel divergence; catalyst-dependent selectivity/byproduct partitioning is the mechanistic interpretation.
- Chemical purity was generally adequate while particle quality was not. Final purity was usually about 0.97–1.00, whereas every batch had a fines fraction near 0.98–1.00. The conclusion that fines—not chemical purity—were the binding constraint is strongly supported and robust to assay noise.
- Batch 12 was the highest-recovery observation: crystal yield 0.575 and purity 0.995, but fines 1.000. Its approximate crystal-capture ratio, 0.575/0.636 ≈ 0.90, supports efficient recovery of formed target.

Partly supported or conditional:
- S2 was operationally the most successful solvent, but a clean solvent-effect estimate was not obtained. S2 supported the best batches, while S3 batch 8 gave only 0.330 recovery. S1 batch 6 still gave 0.481. Temperature, seed charge, and cooling history differed, so attributing the ranking solely to solvent properties remains interpretive.
- Deeper cooling may improve recovery. Batch 12, cooled to 250 K, exceeded the related 278 K batch 9 by 0.023 in crystal yield. Solvent volume also differed and neither condition was replicated, so this is directional rather than causal evidence.
- Crystallization captured much of the target formed. Ratios of crystal yield to reaction yield were roughly 0.83–0.90 in several batches. Treating that ratio as a physical capture efficiency is useful but approximate because the assay channels are independently noisy.

Contradicted in the tested scope:
- Ordinary dilution, long aging, and simple thermal or solvent treatment would solve fines. Batch 4 halved reagent loading but still had fines 1.000. Batch 5 used no seed, prolonged cold aging, and S0 resuspension/warming but also ended at 1.000. Batch 2 included reheating and recooling without improvement. Batch 3 stopped at 310 K yet had fines 0.995.
- Nominal catalyst-panel activity would predict the best catalyst. C0 had the weakest nominal prior but was best experimentally; the aggregate dossier did not transfer directly to this reaction.
- Repeated seed operations constituted a high-dose seed experiment. Resource accounting showed only 0.05 g was actually recorded, so that interpretation was withdrawn.

Still untested:
- A genuinely coarse, characterized seed-size distribution or a true high cumulative seed dose.
- Controlled reagent or antisolvent feeding that limits instantaneous supersaturation.
- Size-selective separation, lower-shear equipment, or a fundamentally different solvent-mixture trajectory.
- The exact multi-day fine-step cooling programs and 315 K annealing cycle appearing in the held-out recipes. Campaign batches explored related ideas but not those precise histories.

2. One additional experiment

I would run a single paired, within-batch annealing experiment using the C0/S2 chemistry of batch 12. After a slow seeded ramp to 278 K, I would make a non-destructive particle-size measurement, heat the same slurry to 315 K for one hour, recool it slowly—not in one rapid step—over roughly 24 hours, and measure particle size again before filtration and final assay.

This would distinguish three explanations with minimal batch-to-batch confounding:
- Selective-dissolution/ripening mechanism: heating dissolves fines preferentially and survivors regrow. Expected outcome: larger d50, substantially lower F20, a transient loss of solid recovery, and partial recovery after recooling.
- Rapid-renucleation mechanism: dissolved material forms new nuclei during recooling. Expected outcome: recovery returns, but F20 stays near 1 or rises and d50 does not improve.
- History-insensitive or seed-population mechanism: the observed fines are imposed by seed CSD, fragmentation, or another persistent population source. Expected outcome: little before/after change despite the thermal cycle.

The within-batch before/after measurements are essential: a final assay alone could not distinguish selective dissolution from different initial particle populations.

3. Least effectively used evidence and least reliable prediction

The observation used least effectively was batch 5. It accumulated more than 200,000 seconds of process time, included prolonged low-temperature aging and a warm S0 resuspension treatment, yet finished with fines 1.000. That is unusually strong negative evidence against the idea that time, mild ripening, or simple selective dissolution will readily produce a coarse number-weighted distribution. My account mentioned it, but the held-out predictions still gave considerable benefit to long gradual cooling and annealing. A better-calibrated treatment would have pulled those predicted fines upward or widened their intervals further. Gradual cooling is not identical to constant cold aging, so batch 5 does not fully decide the issue, but it deserved more weight.

Q08 is the least reliable held-out prediction. Its favorable size and fines estimates depend on a speculative 315 K selective-dissolution/annealing effect. The closest campaign evidence—batch 2 reheating/recooling and batch 5 warm resuspension—did not improve fines. Conversely, neither campaign treatment exactly reproduced Q08’s long preceding ramp and 315 K cycle. Thus both the direction and magnitude of the thermal-cycle effect are weakly identified. This reliability assessment does not revise the sealed Q08 values.
