# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended process (unchanged): batch 12. It used 0.040 mol reagent, 0.060 L solvent-S3, and 0.005 mol catalyst-C1; reaction at 370 K for 1,800 s with 500 rpm stirring; 0.050 g seed added while the mixture was still hot; sequential 14,400 s cooling stages at 330, 310, 290, 270, and 250 K; a final 14,400 s hold at 250 K and 100 rpm; filtration. Its final assay gave seed-excluded crystal recovery 0.574, purity 0.996, fines fraction 0.187, normalized size 0.117, and CSD quality 0.795.

Material effects

Observation: all catalyst/solvent identities were anonymous, so conclusions are empirical rather than chemical-identity claims. In solvent-S0 at 350 K, C0–C3 generally gave near-complete conversion but only moderate selectivity. For example, batch 1 (C0) had HPLC selectivity 0.594 and batch 2 (C1) 0.612; C2 and C3 did not show a decisive improvement. Final crystal recoveries were roughly 0.42–0.48, but fines were approximately 0.99–1.00 in batches 1–4.

Interpretation: catalyst choice affected the target/side-product balance, but did not control the dominant particle-formation problem. C1 was retained because it was at least competitive in the initial screen and later performed well with S3. The available single measurements do not establish a general catalyst ranking.

Observation: solvent changes affected both reaction performance and crystallization. Batch 5 (C1/S1, 330 K) had final crystal recovery 0.398 and fines 1.00. Batch 6 (C1/S2, 370 K) improved recovery to 0.511 but still had fines 1.00. By contrast, batch 7 (C1/S3, 350 K, hot seeding) had fines 0.203 and normalized size 0.105, although its recovery was only 0.405.

Interpretation: S3 appears to provide a more favorable crystal-growth environment, but S3 alone is insufficient. Batch 9 also used S3, yet quenching before seeding produced fines 1.00 and recovery 0.258. Thus the important effect is an interaction between solvent and thermal/seeding history, not a simple intrinsic “good solvent” designation.

Reaction mechanism and temperature dependence

A useful reaction bookkeeping model is

X = (n_R,0 − n_R)/n_R,0,
S = n_target/(n_target + n_byproduct),
Y_target ≈ X·S,

with later degradation capable of reducing the target inventory. These equations are descriptive; the hidden benchmark species mapping was not observed.

Observation: C1/S3 at 370 K for 1,800 s reproducibly gave near-complete conversion and target-related assay yields around 0.61–0.65 in batches 10–12. Batch 10 HPLC reported conversion 0.985, selectivity 0.624, and yield 0.636. Batch 11 reported 0.987, 0.607, and 0.648; batch 12 reported 0.991, 0.605, and 0.625. Their final-assay target yields were 0.612, 0.623, and 0.628, respectively.

By comparison, batch 9 used C0/S3 at 330 K for 7,200 s and gave HPLC selectivity 0.335 and yield 0.328. Batch 7 used C1/S3 at 350 K for 3,600 s; its final selectivity was 0.455 and degradation warning 0.217. Batch 10 at 370 K had final selectivity 0.604 and degradation warning 0.172.

Interpretation: in the tested C1/S3 system, a relatively short 370 K treatment reached the high-conversion regime while limiting time available for competing or degradative pathways. The poorer lower-temperature result in batch 9 is confounded by catalyst and residence time, so it does not independently prove an Arrhenius selectivity effect. Untested alternatives include a different C1 residence time near 360–380 K, lower catalyst loading, or staged reaction temperature.

Reaction–crystallization coupling

Overall seed-excluded crystal recovery can be represented approximately as

Y_crystal = Y_target,pre-separation · f_crystallized · f_retained,

where f_crystallized is the fraction of target transferred into solids and f_retained includes filtration and handling. Purity depends additionally on impurity rejection or co-precipitation.

Using final-assay target yield as a noisy proxy for available product, apparent capture ratios were about 0.86 for batch 10 (0.525/0.612), 0.91 for batch 11 (0.565/0.623), and 0.91 for batch 12 (0.574/0.628). These ratios are illustrative rather than separately measured crystallization yields.

The reaction therefore set a ceiling on recovery: batch 7 formed attractive particles but began with poorer target selectivity, so its recovery remained 0.405. Conversely, batch 6 generated more target but its post-quench crystallization produced essentially all fines. The successful process required both the higher-yielding C1/S3 reaction regime and the favorable hot-seeded cooling trajectory.

Process-history dependence and proposed crystallization mechanism

Observation: quench-first, low-temperature seeding commonly produced very small particles. Batches 1–6 and 9 had fines near 1.00 despite changes in catalyst, solvent, seed amount, cooling duration, and thermal cycling. Increasing total seed from 0.020 g in batch 1 to 0.50 g in batch 4 did not solve the problem. Batch 5 included a warm cycle after crystallization, yet its normalized size was only 0.024 and fines remained 1.00.

In contrast, batches 7, 8, and 10–12 were seeded before quenching and cooled slowly from the hot reaction state. Their fines fractions were 0.203, 0.219, 0.283, 0.227, and 0.187. Their CSD-quality values were approximately 0.73–0.80 in the optimized runs.

Interpretation: quenching likely drove the system rapidly into a high-supersaturation region. In classical terms, nucleation and growth can be expressed qualitatively as

J ∝ exp[−A/(T³(ln S_sup)²)],
G = k_g(S_sup − 1)^g,

where J is nucleation rate, G is growth rate, and S_sup is supersaturation. A rapid quench produces a large supersaturation spike, making primary or secondary nucleation dominate and creating many sub-20 µm particles. Adding more seed after that spike cannot reverse particles already nucleated.

Hot seeding followed by long, shallow temperature steps plausibly allowed target material to deposit on an existing limited population while keeping supersaturation below the strong homogeneous-nucleation regime. The low-speed terminal hold could permit further growth or ripening without severe attrition. This account is consistent with the history dependence, but nucleation rates, solubility curves, polymorphs, and attrition were not directly measured. Alternatives include a hidden S3-specific agglomeration effect or temperature-dependent impurity adsorption rather than classical growth alone.

Cooling endpoint and solvent-volume effects

Observation: batch 10 cooled to 275 K and gave recovery 0.525, purity 0.975, and fines 0.283. Otherwise similar batch 11 extended the cascade to 250 K and gave recovery 0.565, purity 0.991, and fines 0.227. This is consistent with lower terminal solubility increasing recovery without breaching the fines constraint.

Batch 12 retained the 250 K cascade but reduced S3 volume from 0.080 to 0.060 L. It produced the highest observed recovery, 0.574, together with purity 0.996 and fines 0.187. A possible interpretation is that reduced solvent volume lowered the amount of target remaining dissolved at the endpoint. However, the improvement over batch 11 was only 0.009 in recovery, comparable to the final-assay crystal-yield noise scale of about 0.01. Because solvent volume was not replicated, this is not strong evidence for a causal concentration effect.

Revisions during the study

The initial expectation was that longer cooling and more seed would reduce fines. Batches 2–4 revised that view: staged cooling and even 0.50 g total seed did not help when the material was seeded after quench. The working hypothesis then shifted toward a solvent-controlled morphology effect after batch 7. Batch 9 forced a second revision: S3 was not sufficient; preservation of the hot-state trajectory and seeding before the supersaturation excursion were critical. Batches 10–12 then combined that process history with the better C1/S3 reaction regime and a lower endpoint.

Uncertainty and unresolved tradeoffs

All batches were single realizations with noisy synthetic assays. Differences among batches also contain deliberate confounding because conditions were adapted sequentially rather than varied factorially. The robust qualitative result is the large separation between post-quench processes, with fines near 1.00, and hot-seeded S3 processes, with fines near 0.19–0.28. Smaller differences—especially batch 11 versus batch 12—remain uncertain.

No purity/recovery conflict appeared within the final operating window: batches 10–12 all exceeded 0.80 purity and remained below 0.50 fines while recovery increased. Nevertheless, deeper cooling or still higher concentration could eventually increase secondary nucleation, impurity occlusion, slurry viscosity, or filtration loss. Thus the apparent absence of a tradeoff should not be extrapolated beyond the tested 250 K endpoint and 0.060 L solvent volume. Replication of batches 11 and 12 and local variations in solvent volume, hot-seed temperature, and individual cooling-stage duration would be the most useful next tests.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.78 | 0.58 | 0.94 |
| Q01 | crystal_purity | 0.96 | 0.91 | 0.99 |
| Q01 | crystal_size | 0.065 | 0.025 | 0.12 |
| Q01 | crystal_yield | 0.4 | 0.3 | 0.5 |
| Q02 | crystal_fines_fraction | 0.3 | 0.14 | 0.5 |
| Q02 | crystal_purity | 0.98 | 0.94 | 1 |
| Q02 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q02 | crystal_yield | 0.46 | 0.35 | 0.57 |
| Q03 | crystal_fines_fraction | 0.82 | 0.63 | 0.97 |
| Q03 | crystal_purity | 0.97 | 0.92 | 1 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.11 |
| Q03 | crystal_yield | 0.45 | 0.34 | 0.56 |
| Q04 | crystal_fines_fraction | 0.32 | 0.15 | 0.54 |
| Q04 | crystal_purity | 0.98 | 0.94 | 1 |
| Q04 | crystal_size | 0.13 | 0.075 | 0.2 |
| Q04 | crystal_yield | 0.48 | 0.37 | 0.59 |
| Q05 | crystal_fines_fraction | 0.27 | 0.12 | 0.47 |
| Q05 | crystal_purity | 0.98 | 0.94 | 1 |
| Q05 | crystal_size | 0.145 | 0.085 | 0.22 |
| Q05 | crystal_yield | 0.49 | 0.38 | 0.6 |
| Q06 | crystal_fines_fraction | 0.86 | 0.68 | 0.98 |
| Q06 | crystal_purity | 0.97 | 0.92 | 1 |
| Q06 | crystal_size | 0.055 | 0.02 | 0.105 |
| Q06 | crystal_yield | 0.5 | 0.39 | 0.61 |
| Q07 | crystal_fines_fraction | 0.23 | 0.1 | 0.42 |
| Q07 | crystal_purity | 0.98 | 0.94 | 1 |
| Q07 | crystal_size | 0.155 | 0.09 | 0.23 |
| Q07 | crystal_yield | 0.5 | 0.39 | 0.61 |
| Q08 | crystal_fines_fraction | 0.6 | 0.37 | 0.81 |
| Q08 | crystal_purity | 0.97 | 0.91 | 1 |
| Q08 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q08 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q09 | crystal_fines_fraction | 0.94 | 0.8 | 1 |
| Q09 | crystal_purity | 0.96 | 0.87 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.085 |
| Q09 | crystal_yield | 0.025 | 0.003 | 0.07 |
| Q10 | crystal_fines_fraction | 0.73 | 0.51 | 0.91 |
| Q10 | crystal_purity | 0.97 | 0.9 | 1 |
| Q10 | crystal_size | 0.07 | 0.03 | 0.125 |
| Q10 | crystal_yield | 0.14 | 0.07 | 0.24 |
| Q11 | crystal_fines_fraction | 0.25 | 0.11 | 0.45 |
| Q11 | crystal_purity | 0.98 | 0.94 | 1 |
| Q11 | crystal_size | 0.15 | 0.09 | 0.225 |
| Q11 | crystal_yield | 0.49 | 0.38 | 0.6 |
| Q12 | crystal_fines_fraction | 0.56 | 0.34 | 0.77 |
| Q12 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q12 | crystal_size | 0.105 | 0.055 | 0.17 |
| Q12 | crystal_yield | 0.43 | 0.31 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S3 is predicted to outperform S1 in morphology, consistent with the campaign's strong S3-by-history interaction, though post-quench seeding makes this extrapolation uncertain. Q03–Q04: 0.001 g seed is likely insufficient to suppress secondary nucleation; 0.045 g should provide substantially more growth surface. Q05–Q06: equal endpoint and residence time do not erase history—the gradual ramp should limit the supersaturation peak, whereas the 120 s drop should generate persistent fines. Q07–Q08: the terminal 315 K cycle may redissolve product and the fast recooling may renucleate it; earlier warm cycling did not improve morphology. Q09–Q10: seeds ensure particles are present, but immediate filtration gives negligible seed-excluded recovery; a 2 h hold permits additional deposition without reaching the recovery of deep cooling. Q11–Q12: doubling reagent at fixed catalyst lowers catalyst-to-reagent ratio and raises supersaturation; absolute solid may increase, but fractional seed-excluded recovery and morphology may worsen. Intervals are deliberately broad because these recipes use smaller scale, 385 K reaction conditions, unusually long cooling schedules, and mostly S0—regions not directly replicated in the sealed campaign.

## K2

1. Status of the main claims

Supported by direct observations:

- Reaction performance and particle quality are coupled but distinct. Batch 6 produced relatively high crystal recovery (0.511) yet fines were 1.00, while batch 7 produced much better morphology (fines 0.203) but lower recovery (0.405). Batches 10–12 combined a stronger C1/S3 reaction regime with acceptable morphology and reached recoveries of 0.525, 0.565, and 0.574. The interpretation that reaction yield sets an upper bound while crystallization history controls capture and morphology is therefore consistent with the data.
- Process history strongly correlates with morphology. Hot-seeded, slowly cooled S3 batches 7, 8, and 10–12 had fines of 0.187–0.283. Quench-first batches 1–6 and 9 generally had fines near 1.00. This contrast is directly observed; attributing it specifically to suppression of a supersaturation-driven nucleation burst is mechanistic interpretation because supersaturation and nucleation rates were not measured.
- Extending the C1/S3 cooling endpoint from 275 K in batch 10 to 250 K in batch 11 coincided with increased recovery, from 0.525 to 0.565, while maintaining high purity and acceptable fines. This supports, but does not prove, the interpretation that lower terminal solubility increased target capture.
- Batch 12 was the best observed qualifying result: recovery 0.574, purity 0.996, and fines 0.187. Its lower S3 volume coincided with slightly better recovery and morphology than batch 11.

Contradicted or substantially revised:

- The initial idea that more seed and longer cooling alone would solve fines was contradicted. Batch 2 used more seed and slower processing than batch 1 but still had fines 1.00; batch 4 used 0.50 g total seed and also had fines 1.00. Thus seed quantity was not sufficient under the tested post-quench histories.
- A simple “S3 intrinsically gives good particles” claim was contradicted by batch 9. Despite using S3, it was quenched before seeding and ended with fines 1.00 and recovery 0.258. The revised claim is an S3-by-thermal-history interaction.
- Warm cycling as a reliable ripening treatment was not supported. Batch 5 included a warm cycle but had normalized size 0.024 and fines 1.00. This argues against assuming that any reheating step selectively dissolves fines and improves the CSD.

Still untested or only weakly supported:

- High-temperature seeding was never isolated as the sole changed variable. The successful and unsuccessful batches also differed in solvent, catalyst, reaction temperature, and cooling schedules. Its causal importance remains an inference from a strong but confounded contrast.
- The classical-nucleation explanation—rapid quenching causing a supersaturation spike and slow cooling favoring growth—was not directly tested with concentration, solubility, or nucleation-rate measurements.
- The apparent advantage of 0.060 L rather than 0.080 L S3 is uncertain. Batches 11 and 12 provide a useful comparison, but the recovery difference was only 0.009 and each condition was run once.
- Polymorphism, agglomeration, attrition, impurity adsorption, and filtration efficiency were not separately characterized. These remain alternatives to the proposed growth-versus-nucleation account.

2. One additional experiment

I would run a direct post-quench counterpart to batch 11. I would keep its reagent charge, 0.080 L S3, C1 loading, 370 K/1,800 s reaction, 0.050 g seed, staged cooling to 250 K, terminal hold, and filtration unchanged. The sole deliberate change would be to quench after reaction, equilibrate near 300 K, and only then add seed. A particle-size measurement after the first cooling stage could be included as an intermediate diagnostic, followed by the normal final assay.

The existing comparator would be batch 11, which was seeded from the hot reaction state and gave recovery 0.565, purity 0.991, fines 0.227, and size 0.089.

Competing explanations and expected outcomes:

- If preservation of the hot seeded trajectory is causal, the new post-quench batch should show a much higher fines fraction, lower normalized size, and possibly lower recovery than batch 11. An early particle measurement should already reveal excessive fines.
- If S3 plus an extremely slow cooling cascade is sufficient, the post-quench batch should recover toward batch-11 morphology despite its altered early history.
- If the main difference is reaction degradation rather than nucleation history, reaction composition before crystallization should be similar, and the final recovery change should track target loss more than particle size or fines.
- If S3 promotes agglomeration independently of nucleation history, acceptable apparent size might re-emerge late even if the early measurement shows fines.

This single experiment would be more informative than another optimization run because it isolates the most important unresolved causal claim against an existing successful reference.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was batch 4: adding a total of 0.50 g seed still produced fines 1.00. I used it mainly to reject the simple claim that more seed necessarily improves morphology. However, batch 4 also changed catalyst and cooling history, and the very large seed mass may have altered the number distribution, surface area, or assay basis in ways not modeled. Consequently, it cannot establish the shape of the seed-dose response or show whether 0.050 g was near an optimum.

The least reliable held-out prediction is Q12. It doubles reagent from 0.004 to 0.008 mol while holding catalyst, solvent volume, and seed mass fixed. Several opposing effects are extrapolated simultaneously: lower catalyst-to-reagent ratio may reduce fractional conversion; higher concentration may increase fractional crystallization and absolute solid mass; higher supersaturation may increase fines; and crystal_yield is normalized by the doubled initial reagent charge rather than by product entering crystallization. The campaign did not independently vary reagent loading at fixed catalyst and solvent, and its catalyst-to-reagent ratio differed from Q12. Therefore my Q12 estimates for both recovery and feasibility depend more on assumed coupling than on a close empirical analogue.
