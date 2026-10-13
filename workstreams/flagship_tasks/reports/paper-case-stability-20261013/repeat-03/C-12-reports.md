# C-12 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects
The public material dossier suggested that solvent S2 should be favorable for crystallization: relatively low solubility (0.70), strong crystal growth (1.30), low nucleation tendency (0.65), and low impurity occlusion (0.65). All completed batches used S2, so its importance is mechanistically plausible but was not experimentally isolated against S0, S1, or S3. Solvent superiority therefore remains an untested alternative rather than a demonstrated causal effect.

Catalyst C1 became the practical lead. Under the mature process it supported high conversion and improving selectivity as reagent loading fell. C2 performed poorly in batch 4: final reaction yield was about 0.209, selectivity 0.222, and crystal recovery 0.171. However, catalyst, reaction temperature, and crystallization history changed together, so batch 4 does not prove an intrinsic C2 disadvantage. C0 in batch 3 and C3 in batch 2 gave constrained crystal recoveries of about 0.313 and 0.275, respectively, but these comparisons are likewise confounded.

### 2. Reaction behavior and coupling to crystallization
Useful bookkeeping relationships are

- reaction conversion: X = (n_R,0 − n_R)/n_R,0;
- reaction target yield: Y_rxn ≈ X·S, where S is target selectivity;
- crystal recovery: R_c = recovered target in crystals / target present before separation, explicitly excluding seed mass;
- approximate recovered pure-product yield from charged reagent: Y_total ≈ Y_rxn·R_c·P_c, where P_c is crystal purity.

The objective optimized R_c rather than Y_total, but reaction quality still affected impurity burden and the amount/composition entering crystallization. Batch 1 demonstrated this coupling: C1/S2 at approximately 380 K reached complete conversion, yet final selectivity was only about 0.408, with byproduct signal 0.429. Its crystals were very pure (0.985) and recovery was useful (0.320), but fines were 0.647, so the process was infeasible.

As reagent loading decreased at fixed 0.08 L S2, 0.005 mol C1, and the same nominal 380 K reaction, reaction selectivity and yield rose monotonically in the observed batches:

- batch 8, 0.04 mol reagent: selectivity 0.536, reaction yield 0.528;
- batch 10, 0.03 mol: 0.566 and 0.575;
- batch 11, 0.02 mol: 0.641 and 0.621;
- batch 12, 0.01 mol: 0.713 and 0.718.

A plausible interpretation is that lower concentration suppressed a competing or degradation pathway and reduced the impurity load presented to crystallization. Because these were nonreplicated, sequential batches with somewhat different cooling histories, concentration-dependent selectivity is supported as an empirical trend but not established as a unique mechanism.

For batch 12, the approximate charge-to-pure-crystal yield is 0.718 × 0.513 × 0.998 ≈ 0.37. This illustrates why high crystallization-stage recovery alone should not be confused with overall synthetic yield.

### 3. Crystallization mechanism
A useful qualitative variable is supersaturation,

σ = (C − C*)/C*,

where C* depends on solvent, temperature, and composition. Primary/secondary nucleation rates generally increase steeply with σ, whereas controlled growth on existing seeds can consume supersaturation without creating as many new particles. The working interpretation is therefore:

1. S2 and cooling reduce C* and drive recovery.
2. The 0.05 g seed charge supplies growth surfaces.
3. Gradual cooling limits transient supersaturation and nucleation bursts.
4. Repeated 250 K crystallization stages permit further equilibration and growth while retaining a low solubility driving force.

Batch 1 showed that a seed charge followed by only one 7200 s cool to 275 K was insufficient: final fines were 0.647. An additional 14400 s ordinary wait warmed the slurry from 275 K toward 298 K. Particle measurements showed a numerical size-index increase from about 0.051 to 0.070, but fines remained essentially unchanged (0.671 to 0.669). Thus simple warming may have promoted limited growth or ripening, but it did not repair the fines population; temperature change and elapsed time were confounded.

Extended cold histories were much more effective. Batch 5, using staged cooling and repeated 250 K residence, gave recovery 0.315 with fines 0.217. At the stronger 380 K/C1 reaction condition, batches 6–8 gave recoveries of 0.469, 0.475, and 0.480, with fines of 0.308, 0.276, and 0.276. The small recovery increments suggested approach to a cold-stage plateau, while particle size and fines remained process-history dependent.

A deliberate reheat/recool cycle did not help. Batch 9 reheated the crystallized slurry to 310 K and then recooled it; recovery fell to 0.429 and fines rose to 0.347 relative to nearby noncycled batches. The interpretation is partial dissolution followed by renewed nucleation or incomplete re-equilibration. This rejects thermal cycling in the tested form, not every possible temperature-cycle design.

### 4. Loading–quality tradeoff and final history
Lower reagent loading increased measured recovery fraction but initially worsened fines:

- batch 8, 0.04 mol: recovery 0.480, fines 0.276;
- batch 10, 0.03 mol: recovery 0.496, fines 0.341;
- batch 11, 0.02 mol: recovery 0.512, fines 0.439.

Because crystal recovery is normalized to target present before separation, this is not merely a smaller-denominator mass effect. Possible contributors include a higher seed-to-target ratio, reduced impurity inhibition/occlusion, and a different supersaturation trajectory. The worsening fines may indicate that the lower target inventory supported fewer growth-dominated particles or that the cooling schedule was no longer matched to the loading.

Batch 12 addressed that tradeoff with a more gradual and longer history: 0.01 mol reagent in 0.08 L S2, 0.005 mol C1, reaction at 380 K for 3600 s at 300 rpm, 0.05 g seed, 14400 s stages through 330, 300, 275, and 250 K, followed by extended repeated 250 K crystallization before filtration. It produced crystal recovery 0.5128, purity 0.9975, fines 0.3609, CSD-quality index 0.6899, and size index 0.1029. Under the public size definition, the latter corresponds to a number-weighted d50 of roughly 25.7 µm. This history restored a comfortable fines margin while retaining the high-recovery plateau.

### 5. Revisions to the working account
The initial hypothesis was that S2/C1 plus slow seeded cooling would itself be sufficient. Batch 1 contradicted that view: purity and recovery were promising, but fines and reaction selectivity were unacceptable. The account was revised to emphasize extended low-temperature residence rather than a single cool followed by ambient aging.

Batches 6–8 then suggested a recovery plateau near 0.47–0.48. Lower-loading batches 10 and 11 revised that estimate upward to about 0.51, although with a worsening fines tradeoff. Before batch 12, the expectation was that 0.01 mol loading might raise recovery slightly but risk fines above 0.50. The observed recovery was effectively unchanged from batch 11, while gradual cooling reduced fines to 0.361. Thus the final revision is that recovery is probably near a plateau around 0.51 under this process family, and cooling history can improve quality margin without a demonstrated recovery gain.

### 6. Uncertainty and unresolved alternatives
Each batch had only one final assay. The stated standard deviations were approximately 0.010 for crystal recovery and purity and 0.018 for fines/CSD quality. The recovery difference between batches 11 and 12 was only about 0.0009—far below the combined assay noise—so they are experimentally tied in recovery. Batch 12 is stronger operationally because its fines margin, purity, size, reaction selectivity, and reaction yield were all favorable, not because a real recovery advantage over batch 11 was established.

Purities near 1.0 may also be affected by bounded measurement clipping. Batch order was not randomized, and catalyst, temperature, loading, and cooling history were not varied in a complete factorial design. Consequently, observed trends should not be interpreted as fully identified kinetic constants.

Unresolved alternatives include other solvents or solvent mixtures, different seed timing or morphology, alternative agitation histories, still lower reagent loading, washing/resuspension, and longer true equilibrium holds. Replicates of batches 11 and 12 would be needed to resolve their recovery ranking. The central supported conclusion is narrower: within the tested C1/S2 family, low upstream loading combined with seeded, gradual, prolonged cold crystallization gave the best balance of seed-excluded recovery, purity, and fines control.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.27 | 0.15 | 0.42 |
| Q01 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q01 | crystal_size | 0.105 | 0.065 | 0.15 |
| Q01 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q02 | crystal_fines_fraction | 0.42 | 0.28 | 0.59 |
| Q02 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q02 | crystal_size | 0.085 | 0.045 | 0.13 |
| Q02 | crystal_yield | 0.27 | 0.16 | 0.39 |
| Q03 | crystal_fines_fraction | 0.78 | 0.62 | 0.91 |
| Q03 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q03 | crystal_size | 0.038 | 0.015 | 0.075 |
| Q03 | crystal_yield | 0.2 | 0.09 | 0.32 |
| Q04 | crystal_fines_fraction | 0.46 | 0.31 | 0.63 |
| Q04 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q04 | crystal_size | 0.075 | 0.04 | 0.12 |
| Q04 | crystal_yield | 0.23 | 0.12 | 0.35 |
| Q05 | crystal_fines_fraction | 0.45 | 0.3 | 0.61 |
| Q05 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q05 | crystal_size | 0.08 | 0.04 | 0.125 |
| Q05 | crystal_yield | 0.24 | 0.13 | 0.36 |
| Q06 | crystal_fines_fraction | 0.66 | 0.5 | 0.81 |
| Q06 | crystal_purity | 0.88 | 0.77 | 0.96 |
| Q06 | crystal_size | 0.052 | 0.025 | 0.09 |
| Q06 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q07 | crystal_fines_fraction | 0.48 | 0.33 | 0.64 |
| Q07 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q07 | crystal_size | 0.082 | 0.04 | 0.13 |
| Q07 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q08 | crystal_fines_fraction | 0.58 | 0.42 | 0.73 |
| Q08 | crystal_purity | 0.88 | 0.77 | 0.96 |
| Q08 | crystal_size | 0.06 | 0.03 | 0.1 |
| Q08 | crystal_yield | 0.19 | 0.08 | 0.31 |
| Q09 | crystal_fines_fraction | 0.64 | 0.45 | 0.82 |
| Q09 | crystal_purity | 0.91 | 0.78 | 0.99 |
| Q09 | crystal_size | 0.04 | 0.015 | 0.08 |
| Q09 | crystal_yield | 0.025 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.48 | 0.33 | 0.64 |
| Q10 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q10 | crystal_size | 0.065 | 0.03 | 0.105 |
| Q10 | crystal_yield | 0.11 | 0.045 | 0.2 |
| Q11 | crystal_fines_fraction | 0.46 | 0.31 | 0.62 |
| Q11 | crystal_purity | 0.91 | 0.81 | 0.97 |
| Q11 | crystal_size | 0.085 | 0.045 | 0.135 |
| Q11 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q12 | crystal_fines_fraction | 0.35 | 0.22 | 0.51 |
| Q12 | crystal_purity | 0.88 | 0.77 | 0.96 |
| Q12 | crystal_size | 0.09 | 0.05 | 0.14 |
| Q12 | crystal_yield | 0.23 | 0.12 | 0.35 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: the nominal S1 profile has lower solubility, lower nucleation tendency, faster growth and less impurity occlusion than S3, so I predict higher recovery, purity and size with fewer fines. Q03–Q04: increasing S0 seed mass should redirect supersaturation toward seeded growth; recovery changes modestly, but size and fines improve substantially. Q05–Q06: the gradual ramp should avoid the nucleation burst caused by the 120 s temperature drop; the long cold residence makes recovery similar, while the rapid-cool history retains more fines. Q07–Q08: the 315 K reheat is expected to dissolve part of the crop and, after only a short recool, reduce recovery and worsen the number distribution, consistent with the unfavorable thermal-cycle result in batch 9. Q09–Q10: particles remain present because both recipes are seeded, but the extra 7200 s hold permits appreciable target deposition and growth; Q09 has very low seed-excluded recovery. Q11–Q12: doubling loading is predicted to lower fractional recovery and purity slightly but reduce fines by supplying more material for growth, echoing the observed loading–fines tradeoff. Intervals are deliberately broad because S0, S1 and S3 were not tested in the campaign, the queried final temperature is warmer than the leading process, and several estimates lie near the fines or purity feasibility boundaries.

## K2

## 1. Status of the main claims

### Supported within the tested scope
- **Staged, prolonged cold crystallization controls fines better than a single cooling step.** Batch 1 directly observed recovery 0.320 and purity 0.985 but fines 0.647 after one 7200 s cool to 275 K. With staged cooling and repeated 250 K stages, batches 6–8 directly gave recoveries of 0.469–0.480 and fines of 0.276–0.308. Interpreting this as suppression of nucleation bursts and additional seeded growth is plausible, but nucleation and growth rates were not measured directly.
- **Lower reagent loading correlated with higher fractional recovery and reaction selectivity.** At otherwise similar C1/S2 conditions, batches 8, 10, 11 and 12 progressed from 0.04 to 0.01 mol reagent while observed recovery rose from 0.480 to about 0.513 and selectivity from 0.536 to 0.713. This trend is direct observation; attributing it to reduced side reaction, impurity inhibition, or a larger seed-to-target ratio remains interpretation because cooling histories were not identical.
- **The tested 310 K thermal cycle was unfavorable.** Batch 9 directly produced lower recovery, 0.429, and higher fines, 0.347, than nearby noncycled batches 7–8. Partial dissolution followed by renewed nucleation is an interpretation, not a measured mechanism.
- **C2 was poor under its tested condition.** Batch 4 directly gave reaction yield 0.209, selectivity 0.222 and crystal recovery 0.171. This supports avoiding that particular C2/320 K/history combination, not a general claim that C2 is intrinsically inferior.

### Contradicted or revised
- **The initial claim that S2/C1 plus ordinary seeded cooling would be sufficient was contradicted by batch 1**, chiefly because fines were 0.647.
- **Ambient aging was not an effective fines remedy.** In batch 1, the particle-size index increased numerically from about 0.051 to 0.070 during a 14400 s wait that also warmed the slurry, while fines stayed essentially unchanged at 0.671 versus 0.669. The observation contradicts a strong “aging fixes fines” claim, although warming and elapsed time were confounded.
- **A recovery plateau near 0.47–0.48 was revised.** Batches 10–12 reached approximately 0.496–0.513. The later evidence supports a higher plateau near 0.51 for the tested family, but batch 11 versus 12 differed by only 0.0009—far below final-assay resolution.
- **Beneficial thermal ripening was contradicted in the tested form** by batch 9; it remains possible under a different cycle.

### Still untested
- S2 superiority over S0, S1 and S3 was never experimentally tested; every campaign batch used S2. Claims about solvent effects rely on nominal dossier properties and may be altered by hidden solvent residuals.
- Intrinsic catalyst ordering is unresolved because catalyst, temperature and crystallization history were confounded.
- No direct measurements established whether loading acts through reaction selectivity, impurity-mediated crystallization, seed-to-target ratio, or supersaturation kinetics.
- Seed-dose causality, agitation effects, lower-than-0.01 mol loading, washing/resuspension, and true equilibrium recovery remain untested.

## 2. One additional experiment
I would run a **cross-over batch at 0.02 mol reagent using the complete batch-12 process history**: 0.08 L S2, 0.005 mol C1, 380 K for 3600 s at 300 rpm, 0.05 g seed, the same 330→300→275→250 K staged cooling, and the same extended sequence of 250 K stages. I would add non-destructive particle measurements immediately after first reaching 250 K and immediately before filtration, followed by the final assay.

This would compare directly with batch 12 while changing only loading, and with batch 11 while chiefly changing cooling history. It would distinguish:

- **Loading/seed-to-target control:** the 0.02 mol cross-over should retain batch-11-like fines near 0.44 or show the higher-loading tendency toward fewer fines, while fractional recovery should be slightly below the 0.01 mol result.
- **Cooling-history control:** if batch 12’s improved fines primarily came from its more gradual and longer cooling, the cross-over should reduce batch-11 fines toward roughly 0.35 or below while keeping recovery near 0.51.
- **Early nucleation versus late growth:** high fines at the first 250 K measurement followed by a later decline would support ripening/growth; little change would imply that the particle-number distribution is established earlier and largely irreversible.
- **Batch residual or assay noise:** a materially different recovery from both batches 11 and 12, without corresponding intermediate particle changes, would weaken the proposed loading/history account.

## 3. Least-used observation and least-reliable prediction
The account used **batch 10’s intermediate HPLC measurement** least effectively. Before crystallization it showed conversion 0.985, selectivity 0.542 and yield 0.554; the final assay showed 0.986, 0.566 and 0.575. This was the best available within-batch evidence for whether downstream processing materially changed apparent reaction composition. I cited the loading trend but did not fully exploit this paired observation to separate reaction formation from crystallization-stage selection or measurement differences.

**Q09 is the least reliable held-out prediction.** It filters only 60 s after a seeded 300→292 K cooling step. No campaign batch assayed such a seed-dominated, minimally grown solid population. Although particles should remain present because seed was added, the seed-excluded target recovery could be near zero, and purity, size and fines may be governed more by the benchmark’s treatment of seed particles than by the growth behavior learned from long crystallizations. Consequently, both its numerical intervals and its predicted infeasibility are more extrapolative than the long-duration predictions. Q01–Q02 also carry substantial uncertainty because their solvents were untested, but their long seeded histories are at least closer to the campaign’s crystallization-time regime.
