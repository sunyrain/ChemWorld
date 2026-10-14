# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended operating point (unchanged): batch 10 used 0.040 mol reagent, 0.011 L S0 plus 0.044 L S1 (20:80 by volume), 0.004 mol C3, nitrogen at 101325 Pa, reaction at 365 K for 3600 s with 600 rpm stirring, 0.050 g seed, cooling to 250 K for 14400 s, then filtration. Its final assay gave seed-excluded crystal yield 0.50085, purity 0.97663, and number fraction below 20 µm of 0.45082. Exact-recipe batch 12 independently gave 0.49476, 0.99288, and 0.44143, respectively.

Material effects

The dominant observed material effect was the solvent-dependent tradeoff between chemical formation and crystal population quality. Under otherwise common C3/365 K conditions, pure S0 gave the highest reaction and crystal yields in batch 5 (0.6101 and 0.5239), but fines were 0.6794 and therefore unacceptable. Pure S1 in batch 6 lowered those yields to 0.5373 and 0.4857 but passed the fines limit at 0.4509. Pure S2 in batch 4 was still coarser (fines 0.4060) but recovered only 0.4213, while S3 in batch 7 gave 0.4277 recovery with borderline fines of 0.4993. Purities remained high, 0.969–1.000, throughout this solvent comparison.

I interpret S0 as promoting useful product formation but also strong secondary nucleation or another route to numerous small particles. S2 appears to suppress nucleation and/or favor growth, producing a better size distribution at the cost of chemical yield. S1 supplies the most useful compromise. This interpretation is consistent with the nominal material dossier, but the unexpectedly strong reaction performance of S0 shows that the nominal cross-reaction activity ranking was not sufficient to predict this particular world.

Blending S0 and S1 partially separated these effects. The 20% S0 blend in batch 10 increased reaction yield to 0.5604 and crystal yield to 0.5008 while retaining fines of 0.4508. Batch 12 reproduced the same regime. A 30% S0 blend in batch 11 was also compliant—yield 0.4970, purity 0.9917, fines 0.4427—but did not establish a further recovery gain.

Catalyst effects were smaller and less certain. In the controlled S2 comparison, batches 2, 3, and 4 used C0, C2, and C3, respectively. Their reaction yields were 0.4730, 0.4340, and 0.4692, and crystal yields were 0.4058, 0.3636, and 0.4213. C2 was disfavored; C3 gave the highest observed final recovery, although C0 had a slightly higher reaction yield. These were single runs, so the C0–C3 difference may reflect crystallization variability or assay noise rather than a robust catalytic advantage. Batch 1 used C1 but also had a different seed and cooling schedule, so it was not a clean catalyst comparison.

Reaction–crystallization coupling

A useful decomposition is

Y_crystal = Y_reaction × η_capture,

where Y_crystal is seed-excluded target in isolated solid divided by initial reagent, Y_reaction is the analytical target yield before isolation, and η_capture is an empirical crystallization/separation fraction. Across the most relevant batches, η_capture was approximately 0.86 for direct S0 batch 5, 0.90 for pure-S1 batch 6, and 0.894–0.895 for blend batches 10–12. Thus higher chemical yield did not automatically give a viable process: S0 made more target, but its high nucleation burden violated the particle constraint.

Crystal purity was much higher than liquid-phase selectivity. For example, batch 6 had reaction selectivity 0.535 but crystal purity 0.999; batch 10 had selectivity 0.551 but purity 0.977. Preferential incorporation of target and rejection of byproduct into the mother liquor therefore appear to provide strong solid-phase purification. Solvent-dependent impurity occlusion may modify this, but purity never approached the 0.80 limit in the successful crystallizations. Particle quality, rather than purity, was the active constraint.

A classical qualitative description is useful. With supersaturation σ = (C−C*)/C*, nucleation may behave as J ∝ exp[−B/(ln(1+σ))²], while crystal growth can be written G ∝ σ^g. Solvent changes C*, the nucleation barrier B, growth kinetics, and impurity attachment. S0 is consistent with a high effective J/G ratio; S2 with a lower J/G ratio; the S0/S1 blend moderates both reaction activity and J/G. These equations are interpretive rather than fitted laws.

Reaction behavior is also consistent with competing target, byproduct, and degradation pathways. Lowering the S1/C3 reaction temperature from 365 K in batch 6 to 350 K in batch 9 reduced the degradation warning from 0.157 to 0.117, but reaction yield fell from 0.537 to 0.510 and crystal yield from 0.486 to 0.459. Both assays reported essentially complete conversion, suggesting that useful selectivity—not gross conversion—controlled the yield change. A simple conceptual relationship is Y_reaction ≈ X·S_target, with solvent, catalyst, temperature, and time altering the relative target/byproduct rate constants.

Process-history dependence

The crystal-size distribution depended on the complete thermal and seeding history, not only the final temperature. Batch 1 used 0.020 g seed and a 7200 s cool to 275 K and produced fines of 0.466 and crystal-size score 0.073. Later batches used 0.050 g seed and a 14400 s cool to 250 K and generally obtained larger fines margins. Because catalyst and other conditions also differed, this only supports the direction of the seeding/cooling hypothesis; it is not a clean causal estimate.

The explicit S0 thermal-cycle test was unfavorable. Batch 8 cooled to 270 K, reheated to 300 K, and recooled to 250 K. Relative to direct-cool S0 batch 5, crystal yield rose from 0.5239 to 0.5371 and the size score rose from 0.0475 to 0.0931, but fines worsened from 0.6794 to 0.8052 and CSD quality fell from 0.5794 to 0.5440. The simultaneous increase in size score and fines suggests a broadened or bimodal number distribution rather than uniform ripening. Thus the tested reheat cycle did not solve the S0 quality problem.

Revisions and uncertainty

The initial expectation favored S2 because of its nominal low solubility, low nucleation tendency, high growth, and low occlusion. Experiments supported its coarse, pure crystallization behavior but showed that its lower reaction yield limited overall recovery. The program therefore shifted from pure-S2 optimization to S1 and then to S0/S1 blends. The hypothesis that an S0 heat cycle would ripen away fines was rejected for the exact batch-8 history.

Final-assay standard deviations were approximately 0.010 for crystal yield and purity, 0.018 for fines, 0.006 for reaction yield, and 0.025 for the size score. Consequently, the recovery differences among batches 10, 11, and 12 are not resolved as intrinsic effects. In particular, the data do not prove that 20% S0 is superior to 30% S0; they show that the 20% recipe is reproducibly feasible and that batch 10 had the highest observed compliant recovery. The unresolved optimization question is whether a nearby blend fraction, catalyst choice, concentration, or cooling profile could retain fines safely below 0.50 while moving recovery toward the noncompliant S0 values above 0.52. Untested alternatives include staged solvent addition, seeding at a controlled supersaturation, different seed-size distributions, intermediate blend ratios, and other cooling ramps. These are hypotheses only and are not part of the sealed recommendation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.18 | 0.07 | 0.33 |
| Q01 | crystal_purity | 0.985 | 0.94 | 1 |
| Q01 | crystal_size | 0.36 | 0.21 | 0.53 |
| Q01 | crystal_yield | 0.38 | 0.27 | 0.49 |
| Q02 | crystal_fines_fraction | 0.29 | 0.14 | 0.48 |
| Q02 | crystal_purity | 0.955 | 0.88 | 0.995 |
| Q02 | crystal_size | 0.27 | 0.14 | 0.43 |
| Q02 | crystal_yield | 0.27 | 0.17 | 0.39 |
| Q03 | crystal_fines_fraction | 0.52 | 0.31 | 0.72 |
| Q03 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q03 | crystal_size | 0.23 | 0.1 | 0.4 |
| Q03 | crystal_yield | 0.31 | 0.2 | 0.42 |
| Q04 | crystal_fines_fraction | 0.22 | 0.09 | 0.39 |
| Q04 | crystal_purity | 0.97 | 0.91 | 1 |
| Q04 | crystal_size | 0.38 | 0.22 | 0.56 |
| Q04 | crystal_yield | 0.33 | 0.23 | 0.44 |
| Q05 | crystal_fines_fraction | 0.18 | 0.07 | 0.34 |
| Q05 | crystal_purity | 0.97 | 0.91 | 1 |
| Q05 | crystal_size | 0.4 | 0.24 | 0.58 |
| Q05 | crystal_yield | 0.33 | 0.23 | 0.44 |
| Q06 | crystal_fines_fraction | 0.58 | 0.37 | 0.76 |
| Q06 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q06 | crystal_size | 0.18 | 0.07 | 0.34 |
| Q06 | crystal_yield | 0.34 | 0.23 | 0.45 |
| Q07 | crystal_fines_fraction | 0.2 | 0.08 | 0.36 |
| Q07 | crystal_purity | 0.97 | 0.91 | 1 |
| Q07 | crystal_size | 0.39 | 0.23 | 0.57 |
| Q07 | crystal_yield | 0.34 | 0.23 | 0.45 |
| Q08 | crystal_fines_fraction | 0.6 | 0.38 | 0.78 |
| Q08 | crystal_purity | 0.96 | 0.87 | 1 |
| Q08 | crystal_size | 0.43 | 0.24 | 0.63 |
| Q08 | crystal_yield | 0.28 | 0.16 | 0.41 |
| Q09 | crystal_fines_fraction | 0.92 | 0.76 | 0.99 |
| Q09 | crystal_purity | 0.97 | 0.83 | 1 |
| Q09 | crystal_size | 0.025 | 0.005 | 0.07 |
| Q09 | crystal_yield | 0.006 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.78 | 0.58 | 0.92 |
| Q10 | crystal_purity | 0.96 | 0.85 | 1 |
| Q10 | crystal_size | 0.06 | 0.02 | 0.14 |
| Q10 | crystal_yield | 0.09 | 0.03 | 0.18 |
| Q11 | crystal_fines_fraction | 0.2 | 0.08 | 0.37 |
| Q11 | crystal_purity | 0.97 | 0.9 | 1 |
| Q11 | crystal_size | 0.39 | 0.22 | 0.58 |
| Q11 | crystal_yield | 0.33 | 0.22 | 0.44 |
| Q12 | crystal_fines_fraction | 0.46 | 0.27 | 0.65 |
| Q12 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q12 | crystal_size | 0.29 | 0.14 | 0.47 |
| Q12 | crystal_yield | 0.37 | 0.24 | 0.5 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even when seed-excluded product growth is very small. For the solvent pair, S1 is predicted to outperform S3 in recovery, purity, growth and fines control, consistent with the campaign’s observed S1–S3 ordering. For the seed pair, 0.045 g seed should suppress secondary nucleation relative to 0.001 g; seed is excluded from yield, so its main predicted benefit is CSD quality rather than apparent mass. For cooling history, the slow staged ramp should produce larger crystals and fewer fines than an immediate drop to 278.15 K, while the long final hold makes their yields similar. For thermal history, reheating to 315 K followed by only a short recool is expected to dissolve product and generate a broad, fine-rich population on recooling; this follows the unfavorable direction observed for the earlier heat-cycle batch, although the exact magnitude is uncertain. For continued growth, 60 seconds at 292 K should give almost no seed-excluded recovery and predominantly sub-20 µm particles; a two-hour hold raises yield and size but probably remains fine-rich. Doubling upstream reagent loading should increase supersaturation and fractional isolation, but fixed catalyst and seed amounts introduce lower catalyst/seed ratios and more secondary nucleation, creating a recovery–fines tradeoff. Intervals are deliberately broad because these recipes use much lower loading, hotter/shorter reaction conditions, much longer cooling histories, and different catalyst ratios than the completed campaign; feasibility classifications use the point estimates, with Q03, Q06, Q08–Q10 clearly fines-limited and Q12 borderline.

## K2

1. Status of the main claims

Supported by direct observations:
- A solvent-controlled recovery–particle-quality tradeoff was the strongest result. Under the common C3/365 K process, batch 5 with S0 produced crystal yield 0.5239 but failed the fines requirement at 0.6794. Batch 6 with S1 gave lower recovery, 0.4857, but passed at 0.4509 fines. Batch 4 with S2 was coarser but lower-yielding, while batch 7 with S3 was lower-yielding and nearly at the fines limit. Interpreting these differences as changes in solubility, nucleation and growth is mechanistic inference; the yield and particle measurements themselves are direct observations.
- The 20% S0/80% S1 blend was reproducibly feasible. Batches 10 and 12 used the same recipe and gave crystal yields of 0.5008 and 0.4948, purities of 0.9766 and 0.9929, and fines of 0.4508 and 0.4414. This supports feasibility and approximate reproducibility, not a precisely known mean response.
- Crystallization strongly purified the target. For example, batch 6 had reaction selectivity 0.535 but crystal purity 0.999; batch 10 had selectivity 0.551 and crystal purity 0.977. Preferential target crystallization is a reasonable interpretation, although the experiments did not directly measure impurity partition coefficients.
- Lower reaction temperature reduced the degradation signal but also reduced recovery: batch 9 at 350 K had degradation warning 0.117 and crystal yield 0.4588, versus 0.157 and 0.4857 for otherwise similar batch 6 at 365 K. The proposed competing-pathway explanation is interpretive and rests on a single comparison.

Supported only within a narrow scope:
- C2 was disfavored in the S2 catalyst screen. Batches 2, 3 and 4 gave crystal yields of 0.4058, 0.3636 and 0.4213 for C0, C2 and C3. C3 had the highest final recovery, but C0 had slightly higher reaction yield, so a general claim that C3 is intrinsically best is not established. Batch 1 cannot cleanly add C1 to this comparison because its seed and cooling schedule differed.
- More seed and colder, longer cooling were associated with better particle outcomes than the initial process, but the comparison is confounded by catalyst and other changes. It supports the direction of the hypothesis, not a quantitative seed or cooling law.

Contradicted for the tested conditions:
- The proposed S0 ripening cycle did not eliminate fines. Relative to direct-cool batch 5, cyclic batch 8 increased the size score and crystal yield but worsened fines from 0.6794 to 0.8052 and reduced CSD quality. Thus simple reheating and recooling was not a solution for that particular history.
- A simple monotonic claim that increasing the S0 fraction necessarily increases observed recovery was not supported: the 30% blend in batch 11 gave 0.4970 recovery, slightly below batch 10’s 0.5008. The difference is too small relative to uncertainty to establish the opposite trend either.

Still untested or unresolved:
- The optimum S0/S1 fraction, the true C0-versus-C3 ranking, staged solvent addition, controlled-supersaturation seeding, seed-size effects, and concentration–cooling interactions remain unresolved.
- No fitted kinetic or population-balance law was established. The nucleation/growth equations in the mechanism report were explanatory frameworks rather than identified models.
- The observed 20% versus 30% blend differences are comparable with assay uncertainty, so the local recovery–fines frontier remains uncertain.

2. One additional experiment

I would repeat the batch-11 30% S0/70% S1 recipe under the same operating conditions, while adding a post-reaction HPLC measurement before seeding and an in-situ particle-size measurement immediately before filtration. The final assay would remain the decisive endpoint.

This experiment would distinguish three explanations:
- Blend-composition effect: if 30% S0 reproducibly raises post-reaction target yield relative to the 20% formulation but also raises fines, S0 is improving reaction formation while worsening nucleation control.
- Crystallization-capture effect: if post-reaction yield is unchanged but final crystal recovery differs, the blend is acting mainly through solubility, capture or mother-liquor retention.
- Run/assay variation: if the replicate resembles batches 10 and 12 rather than batch 11, the small apparent difference among the blend batches was mostly noise.

A compelling improvement would be final crystal yield above roughly 0.50 with purity above 0.80 and fines safely below 0.50. Higher reaction yield accompanied by fines above 0.50 would confirm the unresolved recovery–quality tradeoff. Similar reaction and final outcomes to batches 10–12 would indicate a broad local plateau rather than a sharply optimized blend fraction.

3. Least effectively used observation and least reliable prediction

The account used the paired particle measurements in batch 1 least effectively. Before filtration, particle imaging reported size about 0.0597 and fines about 0.4900; the final assay later reported about 0.0733 and 0.4659. I relied mainly on final-assay values and did not fully exploit this discrepancy to discuss measurement noise, sampling representation, filtration history, or temporal evolution. It warns against treating small differences in size or fines across batches as deterministic material effects.

The least reliable held-out prediction is Q09. It extrapolates to only 60 seconds of cooling at 292 K, whereas the campaign evidence came from much longer crystallizations at lower final temperatures. Because seed is present but seed mass is excluded from crystal yield, the recipe lies near a difficult boundary: particles can exist while newly formed target solid is almost absent. The size, fines and purity of such a nearly seed-only population were not directly calibrated by any completed batch. Q08 is also uncertain because its 315 K reheat differs substantially from batch 8’s cycle, but Q09 is farther outside the observed growth-time and supersaturation domain.
