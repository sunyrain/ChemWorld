# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended process (unchanged): batch 12 used 0.040 mol reagent, 0.080 L S1, 0.005 mol C0, reaction at 370 K for 3,600 s with 500 rpm agitation, 0.010 g seed added before cooling, cooling to 320 K over 14,400 s and then to 260 K over 14,400 s, followed by filtration. Its final assay gave crystal recovery 0.542, purity 0.992, fines number fraction 0.259, normalized crystal size 0.112 (about 28 µm d50), and CSD quality 0.762.

Material effects

Observed: In the matched C0/S2 catalyst comparison, batch 2 outperformed batches 3 and 4 in crystal recovery: C0 gave 0.433 versus 0.381 for C2 and 0.407 for C3. C0 also gave the highest reaction selectivity in that set, 0.551 versus 0.491 and 0.505. The initial C1/S2 batch 1 had selectivity about 0.502, although its crystallization history differed. This caused the working catalyst choice to change from the nominal-prior choice C1 to C0.

Interpretation: C0 likely provides a more favorable target/byproduct kinetic partition in this fixed world. Catalyst identity can affect crystallization indirectly through the amount and identity of impurities delivered to the crystallizer. It should not, however, be interpreted as directly causing the recovery ranking, because crystal recovery is normalized to target already present before separation.

Observed: Solvent had a much larger particle-population effect. Under the C0, 370 K, seeded long-cool recipe, S1 in batch 5 gave recovery 0.517, purity 0.975 and fines 0.412. S2 in batch 2 gave 0.433, 0.982 and 0.364. S0 in batch 6 gave similar recovery to S1, 0.518, but failed badly on fines at 0.833. S3 in batch 7 gave lower recovery, 0.404, and fines 0.806. Reaction selectivity was also higher with S1 and S0, about 0.637 and 0.634, than with S2 or S3 in these runs.

Interpretation: S1 gave the best joint reaction–crystallization behavior rather than the highest value of either isolated property. S0 appears to generate excessive nucleation or insufficient growth despite good target formation and high crystal purity. S3 likewise favored a fine-rich population. The original dossier-based hypothesis that S2 would be optimal because of its high nominal growth and low impurity occlusion was therefore revised: S2 produced clean, relatively coarse crystals, but S1 recovered more target while remaining within specification.

Reaction/crystallization coupling

The useful distinction is

R_crystal = (seed-excluded recovered target)/(target present immediately before separation),

whereas reaction yield measures target formation from the initial charge. Thus a high crystallization recovery cannot repair poor chemical yield, and a high reaction yield does not guarantee acceptable particles. As a rough combined indicator, batch 12 had reaction yield 0.604 and crystal recovery 0.542, corresponding to about 0.327 of the initial-reagent basis if those two normalized quantities are multiplied. Batch 5 was similar overall despite a different partition: approximately 0.631 × 0.517 = 0.326.

All optimized C0/S1 reactions reached approximately complete conversion, but selectivity remained around 0.60–0.64 and degradation warnings around 0.15–0.17. The resulting impurities can change solubility, nucleation, crystal-surface poisoning and occlusion. Nevertheless, final crystal purity remained 0.975–0.992 in the optimized S1 batches, suggesting that the separation rejected most reaction impurities effectively.

Process-history dependence

A useful qualitative framework is supersaturation S = C/C*(T,solvent). Crystal growth may be represented as G ≈ k_g(S−1)^g, while primary or secondary nucleation often changes much more steeply, schematically J ≈ A exp[−B/(ln S)^2]. Rapid creation of high supersaturation therefore produces many small particles, whereas staged cooling and adequate seed surface allow target material to be consumed by growth before a large nucleation burst.

The data strongly indicate that final temperature alone is insufficient to describe the result:

• Batch 1 used S2 with a 7,200 s cool to 280 K followed by a wait during which the mixture warmed toward ambient. It gave fines 0.538 and recovery 0.384. Batch 2 used a single 14,400 s cool to 270 K and gave fines 0.364 and recovery 0.433. Catalyst identity is a confound, but the result motivated slower, colder cooling.

• Batch 8 used S1/C0, cooled unseeded to 320 K, then received seed and cooled to 260 K. It produced the highest numerical recovery in the campaign, 0.556, but failed the fines constraint at 0.556. Delayed seeding plausibly allowed an uncontrolled nuclei population to form before seed surface became available; lower final temperature also increased supersaturation.

• Adding seed before any cooling and staging through 320 K improved the balance. Batch 9, with 0.050 g seed and a 7,200 s first stage followed by 14,400 s to 270 K, gave recovery 0.531 and fines 0.425. Batch 10 reduced seed to 0.010 g under the same thermal history and gave nearly identical recovery and fines, 0.532 and 0.428, but a larger measured d50. This suggests seed dose affected population size more than recovered mass over the tested range, though the comparison is unreplicated.

• Extending the 320 K stage to 14,400 s in batch 11 reduced fines to 0.243 and increased CSD quality to 0.756, with recovery 0.523. This is consistent with growth under modest supersaturation depleting solute before the colder stage.

• Keeping that long upper stage but cooling finally to 260 K in batch 12 raised recovery to 0.542 while retaining low fines, 0.259. Mechanistically, the long 320 K stage appears to establish a growth-dominated crystal population, after which the lower final temperature harvests additional dissolved target without recreating the fines surge seen with delayed seeding in batch 8.

Revisions and uncertainty

The study revised three initial views: C0 replaced C1 as the working catalyst; S1 replaced the nominally attractive S2 as the best coupled solvent; and a simple cold hold was replaced by seed-before-cooling, two-stage cooling. These revisions were driven by final-assay evidence rather than the nominal material dossier.

Most comparisons are single batches, and several vary more than one factor. Instrument standard deviations were approximately 0.010 for crystal recovery, 0.010 for purity and 0.018 for fines, but these do not capture batch-to-batch process variability. Consequently, the recovery difference between batch 12 (0.542) and batches 9–10 (about 0.531–0.532) is only about one single-assay standard deviation and is not proof of a reproducible improvement. By contrast, batch 12 has large observed margins to both constraints: purity is about 0.192 above its limit and fines about 0.241 below its limit. Those margins are analytically strong, although true process repeatability remains unmeasured.

The unresolved tradeoff is between maximum observed recovery and particle-quality robustness. Batch 8 reached recovery 0.556 but failed on fines. Batch 11 had the lowest fines and nearly the highest CSD quality, but recovery was 0.523. Batch 12 provided the best observed feasible compromise and the highest feasible recovery. Untested alternatives include replicate confirmation, intermediate final temperatures between 260 and 270 K, a finer cooling ramp, alternative seed-size distributions, seeding near—but before—onset of supersaturation, and impurity-specific polishing. These could clarify whether batch 12 is a stable optimum or one favorable realization, but they do not alter the sealed recommendation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.16 | 0.07 | 0.3 |
| Q01 | crystal_purity | 0.985 | 0.95 | 0.999 |
| Q01 | crystal_size | 0.18 | 0.1 | 0.3 |
| Q01 | crystal_yield | 0.36 | 0.25 | 0.47 |
| Q02 | crystal_fines_fraction | 0.32 | 0.16 | 0.51 |
| Q02 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.15 | 0.07 | 0.27 |
| Q02 | crystal_yield | 0.28 | 0.17 | 0.4 |
| Q03 | crystal_fines_fraction | 0.58 | 0.38 | 0.77 |
| Q03 | crystal_purity | 0.975 | 0.92 | 0.998 |
| Q03 | crystal_size | 0.18 | 0.08 | 0.31 |
| Q03 | crystal_yield | 0.29 | 0.17 | 0.41 |
| Q04 | crystal_fines_fraction | 0.34 | 0.19 | 0.52 |
| Q04 | crystal_purity | 0.985 | 0.94 | 0.999 |
| Q04 | crystal_size | 0.13 | 0.06 | 0.23 |
| Q04 | crystal_yield | 0.34 | 0.23 | 0.45 |
| Q05 | crystal_fines_fraction | 0.29 | 0.15 | 0.47 |
| Q05 | crystal_purity | 0.986 | 0.94 | 0.999 |
| Q05 | crystal_size | 0.15 | 0.07 | 0.26 |
| Q05 | crystal_yield | 0.35 | 0.24 | 0.46 |
| Q06 | crystal_fines_fraction | 0.72 | 0.52 | 0.87 |
| Q06 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q06 | crystal_size | 0.065 | 0.025 | 0.14 |
| Q06 | crystal_yield | 0.36 | 0.24 | 0.48 |
| Q07 | crystal_fines_fraction | 0.25 | 0.12 | 0.43 |
| Q07 | crystal_purity | 0.987 | 0.94 | 0.999 |
| Q07 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q07 | crystal_yield | 0.36 | 0.25 | 0.47 |
| Q08 | crystal_fines_fraction | 0.62 | 0.39 | 0.81 |
| Q08 | crystal_purity | 0.955 | 0.86 | 0.995 |
| Q08 | crystal_size | 0.09 | 0.035 | 0.19 |
| Q08 | crystal_yield | 0.29 | 0.17 | 0.42 |
| Q09 | crystal_fines_fraction | 0.78 | 0.56 | 0.92 |
| Q09 | crystal_purity | 0.96 | 0.84 | 0.998 |
| Q09 | crystal_size | 0.03 | 0.008 | 0.075 |
| Q09 | crystal_yield | 0.025 | 0.003 | 0.075 |
| Q10 | crystal_fines_fraction | 0.57 | 0.36 | 0.76 |
| Q10 | crystal_purity | 0.97 | 0.88 | 0.998 |
| Q10 | crystal_size | 0.065 | 0.025 | 0.14 |
| Q10 | crystal_yield | 0.14 | 0.05 | 0.25 |
| Q11 | crystal_fines_fraction | 0.3 | 0.16 | 0.49 |
| Q11 | crystal_purity | 0.985 | 0.94 | 0.999 |
| Q11 | crystal_size | 0.15 | 0.07 | 0.26 |
| Q11 | crystal_yield | 0.35 | 0.23 | 0.46 |
| Q12 | crystal_fines_fraction | 0.42 | 0.24 | 0.62 |
| Q12 | crystal_purity | 0.97 | 0.9 | 0.998 |
| Q12 | crystal_size | 0.19 | 0.09 | 0.32 |
| Q12 | crystal_yield | 0.48 | 0.36 | 0.59 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and cool below the seeding temperature, so some particles are expected even when seed-excluded recovery is small. Q01–Q02: S1 is predicted to outperform S3 in recovery, purity and fines, consistent with the campaign solvent screen, although the exceptionally slow ramp may make both feasible. Q03–Q04: increasing S0 seed mass should provide more growth surface and suppress secondary nucleation; the low-seed case is therefore predicted to have more fines. Q05–Q06: equal total cold time does not erase history—gradual cooling should limit peak supersaturation, whereas the rapid initial drop should generate a persistent fine-rich population. Q07–Q08: the 315 K excursion may dissolve much of the established population; rapid recooling is predicted to regenerate fines and reduce recovered mass, though partial-survival/Ostwald-ripening behavior is a major uncertainty. Q09–Q10: an immediate 292 K filtration should recover little new target; a two-hour hold increases growth and recovery but is unlikely to fully repair the fine population created by the 60-second cool. Q11–Q12: doubling reagent concentration should increase supersaturation and recovery, but also nucleation and occlusion risk; the very slow ramp is expected to keep the point estimate feasible. Intervals are intentionally broad because these recipes extrapolate far beyond the tested charge scale, cooling duration and thermal histories; several fines intervals cross the 0.50 boundary.

## K2

1. Status of the main claims

Supported by direct observations:

• **C0 was the best catalyst among the matched S2 trials.** Batches 2–4 used the same S2 reaction and crystallization history while changing C0, C2 and C3. C0 gave recovery 0.433 and reaction selectivity 0.551, versus 0.381/0.491 for C2 and 0.407/0.505 for C3. This supports the empirical choice of C0 within that tested domain. The interpretation that C0 has intrinsically better kinetic selectivity remains tentative because each catalyst was tested once.

• **S1 offered the best observed recovery–quality compromise.** With C0 and the same long cooling program, batch 5 (S1) gave recovery 0.517, purity 0.975 and fines 0.412. Batch 2 (S2) was feasible but recovered less, 0.433; batch 6 (S0) recovered 0.518 but failed on fines at 0.833; batch 7 (S3) had recovery 0.404 and fines 0.806. These are direct observations. Assigning the differences to solvent-dependent solubility, nucleation and impurity occlusion is a mechanistic interpretation rather than a directly measured molecular mechanism.

• **Process history mattered.** Batch 8, with delayed seeding and a final temperature of 260 K, reached recovery 0.556 but failed with fines 0.556. Seed-before-cooling programs in batches 9–12 were feasible. Extending the 320 K stage from 7,200 s in batch 10 to 14,400 s in batch 11 coincided with a fines decrease from 0.428 to 0.243, while recovery changed from 0.532 to 0.523. Batch 12 retained the long upper stage and lowered the endpoint to 260 K, giving recovery 0.542 and fines 0.259. These results support history dependence, but they do not independently identify cooling rate, residence time and seed timing because several comparisons remain coupled.

• **The recommendation met the constraints with large observed margins.** Batch 12 directly measured purity 0.992 and fines 0.259, while giving the highest feasible recovery, 0.542.

Contradicted or revised:

• **The initial S2-is-best prior was contradicted operationally.** S2 produced clean, relatively coarse material, but S1 recovered more target while remaining feasible.

• **The initial preference for C1 was not supported.** Batch 1 with C1 was not a matched catalyst comparison, so C1 was not conclusively disproved; nevertheless, the matched C0/C2/C3 evidence favored C0 and caused the practical revision.

• **A strong seed-mass effect was not observed between 0.050 and 0.010 g.** Batches 9 and 10 had nearly identical recovery and fines. The lower seed mass produced a numerically larger crystal-size metric, but a large effect on recovery or fines was contradicted over that tested range.

• **Lower endpoint temperature did not necessarily cause unacceptable fines.** Batch 8 suggested that 260 K might drive a fines penalty, but batch 12 showed that 260 K remained feasible after a longer seeded upper-temperature stage. Thus endpoint temperature alone was an inadequate explanation.

Still untested:

• Reproducibility of batch 12 and whether its approximately 0.01 recovery advantage over batches 9–10 is larger than true batch variability.
• Independent causal effects of seed timing, ramp rate, upper-stage duration and total crystallization time.
• Seed-size distribution, seeding near the actual supersaturation onset, intermediate endpoints between 260 and 270 K, and impurity-specific effects.
• The extreme charge scales, 385 K reaction/quench sequence, multi-day ramps and post-crystallization thermal cycle in the held-out recipes. The sealed predictions for these are extrapolations, not experimentally supported claims.

2. One additional experiment

I would repeat the batch-12 chemistry and seed dose but remove the long 320 K conditioning stage: C0/S1, 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, 370 K for 3,600 s, 0.010 g seed before cooling, then one 14,400 s cool directly to 260 K, followed by filtration and final assay.

This would distinguish three explanations:

• **Supersaturation-history mechanism:** The long 320 K stage allows growth on seed while supersaturation is modest, suppressing the later nucleation burst. The direct cool should then retain reasonably high recovery but produce markedly more fines and lower CSD quality than batch 12.

• **Endpoint-equilibrium mechanism:** Final temperature primarily determines recovery and particle outcomes. The direct-cool result should then be close to batch 12 despite the missing stage.

• **Residence-time-limited growth mechanism:** Total time, rather than the specific 320 K pathway, is dominant. The shorter experiment should show both lower recovery and smaller crystals; fines might rise only as a secondary consequence.

A result near batch 8 in fines would strongly favor the history mechanism, although batch 8 itself was confounded by delayed seeding. A result near batch 12 would weaken the proposed staged-supersaturation account. This experiment would not replace a true replicate for estimating reproducibility.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was the **pre-crystallization HPLC result from batch 1**: conversion 1.000, selectivity about 0.507 and byproduct signal about 0.367 before crystallization. It was the clearest direct separation of reaction behavior from downstream crystallization, but no comparable HPLC series was collected for the later catalyst and solvent conditions. Consequently, the account relied heavily on reaction channels from final assays and could not rigorously determine whether solvent effects arose during reaction, crystallization or both.

The least reliable held-out prediction is **Q08**, the post-crystallization heat cycle to 315 K followed by rapid recooling. No source batch reheated an established crystal population. Two opposing mechanisms are plausible: complete dissolution followed by effectively unseeded renucleation, which would raise fines as predicted, or selective dissolution of small particles with survival and regrowth of large crystals, which could instead improve the size distribution. The extent of dissolution at 315 K, seed survival and recrystallization kinetics are all unconstrained by the campaign, so Q08 has the weakest mechanistic anchoring despite its broad intervals.
