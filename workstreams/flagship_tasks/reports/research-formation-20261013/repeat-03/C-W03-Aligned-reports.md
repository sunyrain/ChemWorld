# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The process is best understood as two coupled but distinct stages. Reaction creates a target-containing liquor with impurities; crystallization then partitions the target already present before separation into recoverable crystals. The reported crystal_yield is therefore a crystallization-stage recovery, not an overall yield from the initial reagent. A useful approximate decomposition is

overall isolated target fraction ≈ conversion × selectivity × crystal recovery,

while the measured crystallization recovery is

R_c = n(target recovered as crystals) / n(target present before separation).

Material effects

Solvent S2 was the decisive material choice. Its nominal dossier—low relative solubility (0.70), high crystal growth tendency (1.30), low impurity occlusion (0.65), and low nucleation tendency (0.65)—was consistent with the experiments. Under matched 0.06 L, slow-cooling conditions, S2 in batch 3 gave recovery 0.484, purity 0.992, and fines 0.474. S1 in batch 4 gave recovery 0.474 and purity 1.000 but fines 0.645; S3 in batch 5 gave only 0.384 recovery with fines 0.600 and purity 0.975. Thus S1 and S3 did not satisfy the fines constraint under the tested matched history. S0 was not tested, so its apparently unfavorable nominal solubility/nucleation properties remain an extrapolation rather than an observation.

The likely physical interpretation is supersaturation control. Defining S = C/C*(T,solvent), crystal growth may be represented schematically as G = k_g(S−1)^g, whereas primary nucleation often has a much steeper dependence, for example J ≈ J0 exp[−A/(ln S)^2]. S2 lowers equilibrium solubility and supports growth, but excessive concentration can still drive J sharply upward. That explains the observed nonlinear loading boundary: with S2, 0.055 L solvent produced a favorable CSD, whereas 0.050 and 0.040 L produced almost entirely sub-20-micrometre particles.

Catalyst C1 at 0.005 mol and a 340 K, 3600 s reaction was retained in the successful local process region. It routinely produced near-complete conversion, but liquid-phase selectivity remained only about 0.53–0.59, showing substantial byproduct formation. Nevertheless, crystals from feasible S2 batches were very pure (approximately 0.98–1.00), consistent with selective crystallization rejecting much of the reaction impurity. C3 was tested only in batch 2 and was confounded with a different thermal history; it showed greater byproduct/degradation signals and lower selectivity than the selected region. C0 and C2 were not tested, so no ranking of all catalysts is justified.

Reaction–crystallization coupling

Reaction composition affects the amount and impurity environment of target available to crystallize, but high conversion alone does not maximize isolated target. Batch 1 reached conversion 1.00 but selectivity about 0.588 and crystallization recovery 0.462. In the 340 K C1 region, conversion was also approximately complete and final crystal purity remained high, despite only moderate reaction selectivity. This suggests that S2 crystallization provided an effective impurity-rejection step. However, the campaign did not independently vary impurity loading at fixed crystallization conditions, so the precise effect of byproducts on nucleation, habit, or occlusion remains unresolved.

Because R_c is normalized to target present before separation, reaction improvements could raise overall isolated target without increasing the reported crystal recovery. Conversely, a high R_c from a poorly selective reaction would not necessarily maximize total target obtained from reagent. The operating recommendation was selected according to the stated crystallization-recovery objective and its purity/fines constraints.

Concentration and the quality/recovery tradeoff

The strongest process relationship was a sharp concentration-dependent CSD transition:

• Batch 3, 0.060 L S2: recovery 0.484, fines 0.474.
• Batch 8, 0.055 L S2: recovery 0.520, fines 0.370, purity 0.983.
• Batch 9, 0.050 L S2: recovery 0.512, fines 1.000.
• Batch 6, 0.040 L S2: recovery 0.513, fines 1.000.

Thus decreasing solvent from 0.055 to 0.050 L did not materially improve recovery, but it caused catastrophic fines formation. This is consistent with crossing a nucleation threshold rather than a smooth linear response. The useful region was therefore not the most concentrated liquor, but a narrow balance where supersaturation was high enough for recovery while seeded growth could still dominate new nucleation.

Batch 8 was the best observed feasible balance: 0.5197 recovery, 0.9828 purity, 0.3696 fines, CSD quality 0.760, and normalized crystal-size metric 0.108. Batches 10–12, all at 0.055 L S2, independently remained feasible, with recoveries 0.5117, 0.5127, and 0.5056 and fines 0.3940, 0.3543, and 0.3846. These later results support the robustness of the 0.055 L region, although they also show that batch 8’s numerical recovery advantage is small and may reflect process or assay variability rather than a reproducible superiority.

Process-history dependence

The effective history used a 0.05 g seed charge, the minimum configured ramp rate of 0.001 K/s, cooling to 250 K, and cold residence before filtration. Seeding supplies surface area for growth and slow cooling limits the instantaneous supersaturation that would otherwise promote secondary or primary nucleation. The results support the combined history, but they do not isolate the independent seed effect because unseeded controls were not run. Seeding occurred while the liquor was still hot; partial seed dissolution is plausible but was not measured, and alternative seeding temperatures remain untested.

Cold-aging duration showed no clear monotonic benefit. At 0.055 L S2, batch 10 used one 14,400 s crystallization segment and gave recovery 0.5117 with fines 0.3940. Batch 8 used two segments and gave 0.5197 with fines 0.3696; batch 11 also used two segments but gave 0.5127 with fines 0.3543. Batch 12 used three segments and gave only 0.5056 with fines 0.3846. These differences are small and inconsistent, so the evidence supports adequate cold residence but not a kinetic claim that every added segment improves recovery.

A deliberate 290 K reheat/recool cycle at the over-concentrated 0.040 L condition did not repair the CSD. Batch 7 retained recovery 0.514 but fines 0.987. The tested cycle therefore failed to dissolve or ripen away the fine population sufficiently. A higher dissolution temperature, longer anneal, controlled solvent addition, or classified fines removal could behave differently, but none was tested.

Stirring history was only weakly explored. Reducing the reaction-heating stir rate from 400 rpm to 200 rpm in batch 11 coincided with good fines (0.354) and purity (0.996), but recovery was 0.513 rather than batch 8’s 0.520. Since cooling agitation was not independently controlled and the runs were not replicated as a factorial comparison, no causal stirring effect is claimed.

Revision of the working interpretation

The initial expectation was that S2 and slow seeded cooling would be favorable; this was supported. The early expectation that simply cooling farther or aging longer would monotonically raise recovery was revised after batches 2, 10, and 12. Batch 2’s post-cooling wait allowed the material to warm toward ambient, confounding its intended aging test, while the controlled one-, two-, and three-segment comparisons later showed no monotonic recovery trend.

The largest revision concerned solvent loading. A simple solubility argument would predict progressively greater recovery as solvent volume falls. Batches 6, 8, and 9 showed instead that recovery plateaued near 0.51–0.52 while fines changed discontinuously. The mechanism was therefore revised from recovery-limited solubility control to a coupled solubility–nucleation boundary in which further concentration sacrifices CSD without a useful recovery gain.

Uncertainty and unresolved alternatives

Final-assay values contain stated channel noise, and process variability was not separately quantified. Consequently, differences of roughly one percentage point in recovery among batches 8 and 10–12 should not be treated as statistically resolved. Particle-size measurements taken before filtration and final-assay fines values were broadly consistent but not identical, as expected from measurement noise and continued process evolution.

Purity had ample margin in all successful 0.055 L S2 batches, so the unresolved tradeoff is primarily recovery versus particle quality, not recovery versus chemical purity. The observed feasible plateau was roughly 0.506–0.520 recovery with fines 0.35–0.39. Moving to 0.050 L or below preserved similar recovery but destroyed particle quality. Untested ways to move the frontier include intermediate solvent volumes between 0.050 and 0.055 L, staged antisolvent or solvent addition, different seeding temperature or seed surface area, controlled cooling agitation, and more aggressive but carefully designed dissolution–recrystallization cycles. None should be assumed superior without experiments.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.22 | 0.1 | 0.4 |
| Q01 | crystal_purity | 0.97 | 0.9 | 1 |
| Q01 | crystal_size | 0.18 | 0.1 | 0.28 |
| Q01 | crystal_yield | 0.39 | 0.25 | 0.53 |
| Q02 | crystal_fines_fraction | 0.35 | 0.18 | 0.57 |
| Q02 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q02 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q02 | crystal_yield | 0.3 | 0.17 | 0.45 |
| Q03 | crystal_fines_fraction | 0.66 | 0.42 | 0.86 |
| Q03 | crystal_purity | 0.94 | 0.83 | 0.99 |
| Q03 | crystal_size | 0.06 | 0.025 | 0.12 |
| Q03 | crystal_yield | 0.27 | 0.14 | 0.42 |
| Q04 | crystal_fines_fraction | 0.32 | 0.16 | 0.52 |
| Q04 | crystal_purity | 0.96 | 0.88 | 1 |
| Q04 | crystal_size | 0.16 | 0.08 | 0.26 |
| Q04 | crystal_yield | 0.31 | 0.17 | 0.46 |
| Q05 | crystal_fines_fraction | 0.3 | 0.14 | 0.5 |
| Q05 | crystal_purity | 0.96 | 0.87 | 1 |
| Q05 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q05 | crystal_yield | 0.32 | 0.18 | 0.47 |
| Q06 | crystal_fines_fraction | 0.65 | 0.4 | 0.85 |
| Q06 | crystal_purity | 0.94 | 0.83 | 0.99 |
| Q06 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q06 | crystal_yield | 0.33 | 0.18 | 0.48 |
| Q07 | crystal_fines_fraction | 0.34 | 0.17 | 0.55 |
| Q07 | crystal_purity | 0.96 | 0.87 | 1 |
| Q07 | crystal_size | 0.16 | 0.08 | 0.26 |
| Q07 | crystal_yield | 0.32 | 0.18 | 0.47 |
| Q08 | crystal_fines_fraction | 0.2 | 0.08 | 0.4 |
| Q08 | crystal_purity | 0.97 | 0.89 | 1 |
| Q08 | crystal_size | 0.22 | 0.11 | 0.35 |
| Q08 | crystal_yield | 0.27 | 0.12 | 0.43 |
| Q09 | crystal_fines_fraction | 0.58 | 0.31 | 0.82 |
| Q09 | crystal_purity | 0.93 | 0.76 | 0.99 |
| Q09 | crystal_size | 0.04 | 0.012 | 0.085 |
| Q09 | crystal_yield | 0.015 | 0 | 0.065 |
| Q10 | crystal_fines_fraction | 0.46 | 0.23 | 0.7 |
| Q10 | crystal_purity | 0.95 | 0.83 | 1 |
| Q10 | crystal_size | 0.065 | 0.025 | 0.13 |
| Q10 | crystal_yield | 0.1 | 0.025 | 0.22 |
| Q11 | crystal_fines_fraction | 0.29 | 0.13 | 0.5 |
| Q11 | crystal_purity | 0.96 | 0.87 | 1 |
| Q11 | crystal_size | 0.17 | 0.085 | 0.28 |
| Q11 | crystal_yield | 0.32 | 0.18 | 0.47 |
| Q12 | crystal_fines_fraction | 0.7 | 0.45 | 0.89 |
| Q12 | crystal_purity | 0.91 | 0.78 | 0.98 |
| Q12 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q12 | crystal_yield | 0.43 | 0.28 | 0.58 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The six pairs isolate solvent, seed loading, cooling history, annealing, residence time, and reagent concentration. Q01 is favored over Q02 because S1 has lower nominal solubility, nucleation, and impurity occlusion than S3. Q04 is favored over Q03 because the larger seed charge should divert supersaturation toward seeded growth and away from fine-particle nucleation. Q05 and Q06 should approach similar equilibrium recovery, but the staged cooling in Q05 should yield larger crystals and fewer fines than the initial crash in Q06. The 315 K anneal in Q08 is expected to dissolve fines and promote regrowth relative to Q07, at the cost of some recovery after the short recooling period; this benefit is uncertain because the milder 290 K cycle tested previously did not rescue an over-concentrated batch. Q10 adds enough residence at 292 K to grow more seed-excluded product than Q09, although both short processes are extrapolations and Q10 lies near the fines threshold. Doubling reagent in Q12 should increase supersaturation and fractional recovery relative to Q11, but likely crosses into nucleation-dominated, high-fines behavior. Purity is expected to remain high because prior crystallizations rejected reaction impurities effectively. Intervals are widest for the untested S0 solvent, the short Q09/Q10 histories, and threshold-sensitive fines; all recipes contain seed, so particles are expected even where seed-excluded recovery is very low.

## K2

1. Status of the main claims

Supported by direct observations:

• S2 was the best tested solvent for jointly satisfying recovery, purity, and fines constraints. Under matched 0.06 L histories, batch 3 (S2) gave recovery 0.484 and fines 0.474, whereas batch 4 (S1) gave 0.474 and 0.645 and batch 5 (S3) gave 0.384 and 0.600. The observation is the solvent-associated difference; attributing it specifically to solubility, nucleation, growth, or impurity occlusion remains an interpretation because those rates were not measured separately.

• A narrow solvent-loading boundary was observed for S2. Batch 8 at 0.055 L gave recovery 0.520 and fines 0.370; batches 6 and 9 at 0.040 and 0.050 L retained recoveries near 0.51 but had fines near 1. Batches 10–12 independently showed that 0.055 L remained feasible, with fines 0.354–0.394. Calling this a supersaturation-driven nucleation threshold is a mechanistic interpretation, but the abrupt CSD association itself is well supported.

• Purity was not the binding constraint in the successful region. Batches 8 and 10–12 all had purity about 0.98–1.00. Selective impurity rejection by crystallization is plausible, but direct impurity partition measurements were not made.

• Added cold residence did not show a monotonic recovery benefit. One cold segment in batch 10 gave recovery 0.512; two segments in batches 8 and 11 gave 0.520 and 0.513; three segments in batch 12 gave 0.506. This contradicts the initial simple claim that every additional aging segment should increase recovery.

• The tested 290 K reheat/recool treatment did not rescue the concentrated high-fines regime. Batch 7 still had fines 0.987, similar to batch 6 without that cycle. This contradicts the specific proposed rescue mechanism under those conditions, although it does not exclude stronger or longer annealing.

Contradicted or revised:

• The original monotonic concentration argument—less solvent should continuously improve useful recovery—was contradicted. Below 0.055 L, recovery barely changed while particle quality collapsed.

• A general claim that longer aging necessarily improves recovery was contradicted by batches 8 and 10–12.

• The tested mild thermal cycle was ineffective, contradicting the expectation that modest reheating would dissolve fines sufficiently for productive regrowth.

Still untested:

• S0 was never tested during the campaign, so all later S0 predictions were extrapolations from its nominal dossier and the behavior of other solvents.

• The interval between 0.050 and 0.055 L was not mapped. Consequently, the location and sharpness of the inferred CSD boundary remain unknown.

• Seed amount and seeding temperature were not independently varied. The claim that seeding suppressed primary nucleation is mechanistically reasonable but not demonstrated by a seeded/unseeded comparison.

• Cooling agitation, staged solvent addition, antisolvent operation, C0/C2 catalysts, and aggressive dissolution–recrystallization cycles remain untested.

• Reaction–crystallization coupling was inferred rather than isolated. Reaction conversion/selectivity and crystallization history changed together across several batches, so the effect of a particular byproduct concentration on nucleation or occlusion is unresolved.

2. One additional experiment

I would run the batch-8 process exactly, except use 0.0525 L S2—midway between the feasible 0.055 L condition and the high-fines 0.050 L condition. I would retain 0.04 mol reagent, 0.005 mol C1, the 340 K/3600 s reaction, 0.05 g seed, minimum cooling ramp, two 14,400 s segments at 250 K, and measure particle size after the first and second segments before filtration.

This would distinguish three explanations:

• Sharp nucleation threshold: the result should fall predominantly into one of the two observed regimes—either fines around 0.35–0.40 with larger particles, or fines near 1 with small particles—while recovery remains near 0.51.

• Smooth concentration response: fines and size should be intermediate between batches 8 and 9, roughly a broad mid-fines state rather than a binary transition.

• Predominantly stochastic or history-sensitive behavior: intermediate measurements might fluctuate or disagree with the final state, and the result might not align consistently with either neighboring loading despite an otherwise matched recipe.

The two in-process particle measurements would also show whether excessive fines appear during the first cooling segment or accumulate during cold aging. A high fines fraction at the first measurement would support early supersaturation-driven nucleation; initially acceptable particles followed by deterioration would instead implicate attrition, secondary nucleation, or prolonged cold residence.

3. Least effectively used observation and least reliable prediction

The least effectively used observation was batch 2’s intermediate particle-size measurement followed by its warming wait. At 260 K it showed fines 0.298 and normalized size 0.096; after the wait warmed the batch toward ambient, the final assay showed fines 0.315 and size 0.116 with recovery 0.456. This was the campaign’s most informative within-batch history observation, but my account mostly treated it as a confound. It could suggest limited ripening or size growth during warming without a recovery benefit. That inference remains weak because the two readings came from different measurement contexts, filtration intervened, and instrument/process uncertainty was not independently quantified.

Q09 is the least reliable held-out prediction. It contains only a 60 s cooling step to 292 K before filtration, far outside the long crystallization histories actually studied. My prediction therefore depends strongly on unverified assumptions about whether charged seed alone guarantees a measurable particle population, how seed mass is handled in the size and fines statistics, and how close to zero seed-excluded recovery remains after such a short interval. Purity and CSD metrics may also become unstable or operationally different when nearly all collected solid is seed rather than newly crystallized product. Q08’s 315 K annealing prediction is also uncertain, but Q09 is the more severe extrapolation because no comparably short crystallization was observed.
