# C-W05-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The recommended process remains batch 12. It used 0.040 mol reagent, 0.080 L S1, and 0.005 mol C1; reaction at 350 K for 2400 s under nitrogen; quenching; reheating to 347 K for 300 s; addition of 0.050 g seed; slow cooling to 270 K over 14,400 s; a 14,400 s low-agitation growth hold; filtration; and final assay. It produced crystal recovery 0.511, purity 0.996, fines fraction 0.428, and a normalized size of 0.098 (approximately 24.5 µm number-weighted d50).

Material effects—observations

Only C1 was tested, so no comparative catalyst ranking is experimentally justified. Under the common moderate reaction regime, solvent affected both reaction and crystallization. S1 generally gave the highest crystallization recovery: 0.504 in batch 6, 0.515 in batch 8, 0.498 in batch 11, and 0.511 in batch 12. S0 gave 0.459 in batch 5; S2 generally gave about 0.38–0.44; and S3 gave 0.378 in batch 7. S0 and S1 also showed higher reaction selectivity than S2 or S3 in the approximately matched solvent screen, although each solvent was represented by only one directly comparable batch.

All screened solvents produced high final crystal purity, normally about 0.97–1.00. Thus the solid phase strongly rejected reaction impurities under these conditions. For example, the severe first reaction had byproduct signal 0.367 and degradation warning 0.204, yet batch 1 crystals still had purity 0.987. This indicates that reaction cleanliness and crystal purity were coupled less strongly than reaction composition and absolute product mass.

Interpretation

The nominal dossier suggested S2 should combine low nucleation, strong growth, low solubility, and low impurity occlusion. S2 did give excellent purity and ultimately the widest fines margin in batch 10, but it did not maximize recovery. The empirical evidence therefore revised the initial material prior in favor of S1 when recovery is the primary objective. Hidden solvent-specific residuals, differences in target concentration, and unmeasured solid-state kinetics are plausible explanations; the experiments do not identify which one is responsible.

Reaction–crystallization coupling

A useful decomposition is

R_overall ≈ Y_reaction × R_crystal,

where R_crystal = moles of seed-excluded target recovered as crystals divided by moles of target present immediately before separation. The campaign objective used R_crystal, not overall yield from charged reagent. Nevertheless, reaction yield and selectivity influence the absolute target concentration, impurity loading, and supersaturation trajectory entering crystallization. For illustration, multiplying the observed reaction yield by crystal recovery gives approximate overall recovered-target fractions of 0.299 for batch 11 and 0.309 for batch 12.

The high crystal purities imply effective impurity rejection, but impurities may still change nucleation or growth without being extensively occluded. Batch 6 and batch 11 illustrate this distinction: both used S1 and had comparable reaction performance and recovery, but batch 6 had a fines fraction of 1.00 whereas batch 11 had 0.442. Their principal difference was crystallization history, especially the much hotter seed point in batch 11. Thus reaction composition alone cannot explain particle quality.

Process-history dependence

The decisive observed variable was the thermal history around seeding, not simply final temperature or elapsed holding time. Early S2 batches seeded near 304 K remained fines-dominated: batch 2 had fines 1.00, batch 3 had 0.995, and batch 4 had 1.00. Raising the S2 seed point to 330 K reduced fines to 0.628 in batch 9; raising it to 345 K reduced fines further to 0.377 in batch 10 while maintaining recovery near 0.441. This large change exceeds the declared fines-measurement noise and was corroborated by in-process particle measurements.

A conventional interpretation uses supersaturation σ = (C − C*)/C*, with nucleation J ≈ k_n σ^n and growth G ≈ k_g σ^g, commonly with nucleation more strongly dependent on supersaturation than growth. Introducing seed before deep supersaturation, followed by gradual cooling, provides surface area for growth and avoids a burst of secondary nuclei. An additional plausible mechanism is partial dissolution of the seed population at the hotter seed point: fewer surviving particles would subsequently grow larger, reducing the number-weighted fines fraction. These interpretations are consistent with the observations but were not directly distinguished.

Several initially plausible remedies failed. Reducing seed from 0.050 g to 0.001 g did not suppress fines in batch 3. A 305 K reheat/recool cycle did not help in batch 4. Ten additional 14,400 s low-temperature holds in batch 8 increased recovery to 0.515 but left fines at 0.987. Hence low-temperature aging alone did not coarsen the population detectably; the path by which supersaturation was generated mattered more than total residence time.

Quality–recovery tradeoff

Batch 10, using S2 and a 345 K seed point, gave recovery 0.441, purity 0.979, and fines 0.377. Batch 11, using S1 under an otherwise similar high-temperature seeding strategy, increased recovery to 0.498 but moved fines upward to 0.442. This is the clearest unresolved material tradeoff: S2 supplied more fines margin, while S1 recovered more target.

Batch 12 combined S1 with a 347 K seed point and a deeper 270 K endpoint. It gave recovery 0.511, purity 0.996, and fines 0.428. Relative to batch 11, recovery increased by only 0.0127 and fines decreased by 0.0136. Those differences are comparable to the declared final-assay noise (approximately 0.010 for recovery and 0.018 for fines), so they should not be treated as proof that either the 2 K hotter seed point or the 5 K deeper endpoint is intrinsically superior. Both variables changed together. Batch 12 is recommended because it has the best observed qualifying recovery, not because the incremental mechanism has been conclusively resolved.

Uncertainty and untested alternatives

The strongest conclusion is the large hot-seeding effect between batches 9 and 10 and the consistent qualification of batches 10–12. In-process and final fines estimates agreed well: batch 10 measured 0.356 then 0.377, batch 11 measured 0.453 then 0.442, and batch 12 measured 0.430 then 0.428. Purity has a very large margin above 0.80. Batch 12 has a fines margin of about 0.072 below the limit, larger than instrumental noise but not validated against batch-to-batch process variability.

All important comparisons are unreplicated, and catalyst choice was never screened. Batch 11 versus batch 12 confounds seed temperature with cooling endpoint. Solvent comparisons may also include fixed hidden residuals and ordinary process variation. Untested alternatives include a factorial grid of seed temperature and endpoint, replication near the 0.50 fines boundary, other catalysts, intermediate seed masses, alternative agitation profiles, solvent mixtures, washing or resuspension, and controlled dissolution–recrystallization protocols. A replicate of batch 12 exceeding 0.50 fines, or a replicated process with higher qualifying recovery and a safer fines margin, would weaken the present recommendation; batch 11 is the closest demonstrated fallback.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.46 | 0.28 | 0.66 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.09 | 0.045 | 0.145 |
| Q01 | crystal_yield | 0.16 | 0.06 | 0.28 |
| Q02 | crystal_fines_fraction | 0.34 | 0.17 | 0.55 |
| Q02 | crystal_purity | 0.98 | 0.93 | 1 |
| Q02 | crystal_size | 0.11 | 0.055 | 0.17 |
| Q02 | crystal_yield | 0.11 | 0.025 | 0.23 |
| Q03 | crystal_fines_fraction | 0.59 | 0.35 | 0.82 |
| Q03 | crystal_purity | 0.97 | 0.91 | 1 |
| Q03 | crystal_size | 0.074 | 0.025 | 0.14 |
| Q03 | crystal_yield | 0.075 | 0.005 | 0.19 |
| Q04 | crystal_fines_fraction | 0.41 | 0.22 | 0.64 |
| Q04 | crystal_purity | 0.97 | 0.91 | 1 |
| Q04 | crystal_size | 0.096 | 0.045 | 0.155 |
| Q04 | crystal_yield | 0.1 | 0.015 | 0.22 |
| Q05 | crystal_fines_fraction | 0.39 | 0.2 | 0.62 |
| Q05 | crystal_purity | 0.97 | 0.91 | 1 |
| Q05 | crystal_size | 0.1 | 0.05 | 0.16 |
| Q05 | crystal_yield | 0.105 | 0.02 | 0.23 |
| Q06 | crystal_fines_fraction | 0.88 | 0.7 | 1 |
| Q06 | crystal_purity | 0.95 | 0.87 | 0.995 |
| Q06 | crystal_size | 0.041 | 0.008 | 0.09 |
| Q06 | crystal_yield | 0.11 | 0.02 | 0.24 |
| Q07 | crystal_fines_fraction | 0.37 | 0.18 | 0.6 |
| Q07 | crystal_purity | 0.97 | 0.91 | 1 |
| Q07 | crystal_size | 0.105 | 0.052 | 0.17 |
| Q07 | crystal_yield | 0.11 | 0.02 | 0.235 |
| Q08 | crystal_fines_fraction | 0.63 | 0.39 | 0.85 |
| Q08 | crystal_purity | 0.965 | 0.9 | 1 |
| Q08 | crystal_size | 0.071 | 0.025 | 0.13 |
| Q08 | crystal_yield | 0.08 | 0.005 | 0.19 |
| Q09 | crystal_fines_fraction | 0.74 | 0.48 | 0.94 |
| Q09 | crystal_purity | 0.98 | 0.91 | 1 |
| Q09 | crystal_size | 0.052 | 0.01 | 0.11 |
| Q09 | crystal_yield | 0.012 | 0 | 0.065 |
| Q10 | crystal_fines_fraction | 0.65 | 0.4 | 0.87 |
| Q10 | crystal_purity | 0.975 | 0.91 | 1 |
| Q10 | crystal_size | 0.064 | 0.017 | 0.125 |
| Q10 | crystal_yield | 0.045 | 0 | 0.13 |
| Q11 | crystal_fines_fraction | 0.36 | 0.17 | 0.59 |
| Q11 | crystal_purity | 0.97 | 0.91 | 1 |
| Q11 | crystal_size | 0.108 | 0.055 | 0.17 |
| Q11 | crystal_yield | 0.11 | 0.02 | 0.235 |
| Q12 | crystal_fines_fraction | 0.61 | 0.39 | 0.81 |
| Q12 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q12 | crystal_size | 0.073 | 0.03 | 0.125 |
| Q12 | crystal_yield | 0.37 | 0.24 | 0.51 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is assigned higher recovery, while S3's lower nominal nucleation and occlusion tendencies give larger particles and fewer fines. Q03–Q04: the very small seed charge is expected to permit more secondary nucleation; the larger charge better controls fines during the slow ramp. Q05–Q06: gradual cooling should suppress a nucleation burst, whereas the 120 s crash creates persistent fines despite the long endpoint hold. Q07–Q08: the 315 K cycle may dissolve some solids, but the rapid recooling can renucleate them; prior campaign evidence did not support thermal cycling as a reliable coarsening method. Q09–Q10: the additional 292 K hold raises seed-excluded recovery and permits some growth, but both remain fines-dominated. Q11–Q12: doubling concentration strongly raises recovery but also raises supersaturation, impurity occlusion, and fines, producing the main quality/recovery tradeoff. Intervals are deliberately broad because these recipes extrapolate to lower concentration, much longer staged cooling, and harsher reaction conditions than the campaign; seed survival near undersaturation and cycle-induced dissolution are the largest uncertainties.

## K2

1. Status of the main claims

Supported by direct observations:
- Crystallization history dominated fines control. Under closely matched S2 conditions, raising the post-quench seed point from 330 K in batch 9 to 345 K in batch 10 changed final fines from 0.628 to 0.377 while recovery stayed nearly constant, 0.440 versus 0.441. This supports a strong seed-temperature/history effect, although the proposed suppression-of-secondary-nucleation mechanism remains an interpretation.
- S1 offered more recovery than S2 under the matched 345 K-seeding protocol. Batch 10 (S2) gave recovery 0.441 and fines 0.377; batch 11 (S1) gave 0.498 and 0.442. The recovery/fines tradeoff is observed directly; attributing it to solubility, nucleation, or growth constants is interpretive.
- Batches 10–12 directly met both quality constraints. Batch 12 had recovery 0.511, purity 0.996, and fines 0.428; batch 11 was the nearest fallback.
- Long low-temperature aging alone did not solve the fines problem. Batch 8 received ten extended holds but still had fines 0.987. Likewise, the tested low-seed protocol in batch 3 and the 305 K reheat/recool protocol in batch 4 both gave fines near 1.00.
- Crystallization strongly rejected impurities in the tested processes. Purity remained about 0.97–1.00 across the campaign, including batch 1 despite its high byproduct and degradation signals.

Contradicted or substantially revised:
- The initial expectation that nominally favorable S2 would maximize the constrained recovery was revised. S2 provided the best fines margin in batch 10, but qualifying S1 batches 11 and 12 recovered more target.
- The initial expectation that slow cooling plus a long hold would by itself suppress fines was contradicted by batches 2 and 8.
- The proposed benefits of simply lowering seed mass or applying a modest dissolution–recooling cycle were not supported by batches 3 and 4. This rejection applies only to those specific protocols, not to every possible seed loading or thermal cycle.

Still untested or unresolved:
- No catalyst other than C1 was tested, so catalyst ranking is wholly untested.
- The microscopic explanation for hot seeding—suppressed secondary nucleation versus partial dissolution of excess seed particles—was not observed directly.
- Batch 11 versus batch 12 confounded seed temperature (345 versus 347 K) with endpoint (275 versus 270 K). Their small recovery and fines differences were comparable to assay noise.
- Repeatability and process variance near the fines limit were not measured. The batches were unreplicated.
- Polymorph identity, seed-size distribution, solvent mixtures, washing/resuspension, and more aggressive controlled dissolution cycles remain untested.

2. One additional experiment

I would repeat the complete S1 protocol while using a 347 K seed point and a 275 K cooling endpoint. This fills the missing corner between batch 11 (345/275 K) and batch 12 (347/270 K), with all other operations held fixed.

It would distinguish three explanations:
- If hotter seeding is the principal fines-control mechanism, the new batch should retain approximately batch-11 recovery, around 0.50, but show lower fines or larger particles than batch 11, approaching batch 12.
- If the deeper 270 K endpoint caused most of batch 12’s change, the 347/275 K batch should resemble batch 11; batch 12’s extra recovery would then be attributed mainly to the lower endpoint.
- If the batch-11/batch-12 differences were chiefly noise, the new result should overlap both without a coherent split between recovery and particle quality.

A materially lower fines fraction at essentially unchanged recovery would particularly support the hot-seeding interpretation. Similarity to batch 11 would weaken the claimed importance of the 2 K seed-temperature increment, although it would not by itself distinguish an endpoint effect from random batch variation.

3. Least-used observation and least-reliable prediction

The account used the batch-1 intermediate HPLC observation least effectively. It measured conversion 1.00, selectivity about 0.507, and byproduct signal about 0.367 before downstream processing, but no comparable HPLC time series was collected in later batches. Consequently, it could not isolate reaction kinetics, quench effects, or how reaction composition changed during the post-quench reheats. The report relied mainly on final-assay reaction channels instead.

Q09 is the least reliable held-out prediction. It filters only 60 seconds after cooling to 292 K, a regime with no close campaign analogue. Its outcome depends on poorly constrained early-time growth and on whether the 0.025 g seed charge remains as particles or dissolves in the relatively dilute liquor. That uncertainty affects not merely the numerical size and fines estimates but potentially the particles_present classification itself. The campaign chiefly observed established slurries after much longer cooling, so extrapolation to this nearly seed-only, short-time state is especially weak.
