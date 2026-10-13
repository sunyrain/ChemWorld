# C-W01-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

The strongest crystallization effect was associated with solvent identity. The nominal dossier described S2 as having low relative solubility (0.70), low nucleation tendency (0.65), high crystal-growth tendency (1.30), and low impurity occlusion (0.65). The experiments were consistent with that qualitative profile: direct seeded cooling to 250 K produced broad specification margins with S2. For example, batch 6 (C0/S2) gave crystal recovery 0.562, purity 1.000, and fines fraction 0.311. Batches 9 and 10 also gave recoveries of 0.564–0.565 and fines of 0.290–0.293.

S0 behaved differently. Its nominal high nucleation tendency (1.25), slower growth (0.80), and higher impurity-occlusion tendency (1.20) suggested a risk of many small crystals. Direct cooling confirmed the fines risk: batch 3 achieved recovery 0.567 and purity 0.993, but fines were 0.712, well above the 0.50 limit. However, S0 ultimately supported the greatest qualifying recovery once its thermal history was altered. Thus, solvent identity did not set a fixed outcome; it changed the process window and sensitivity to cooling history.

S1 and S3 were inferior under the directly cooled screening recipe. Batch 4 (S1) gave recovery 0.472 and fines 0.540, while batch 5 (S3) gave recovery 0.434 and fines 0.644. These are observations for one recipe per solvent, not proof that those solvents cannot be optimized.

Catalyst screening within S2 showed that C0 gave the best observed combination under the common direct-cooling protocol: batch 6 gave recovery 0.562, compared with 0.507 for C1 in batch 2, 0.508 for C2 in batch 7, and 0.528 for C3 in batch 8. C0 also gave upstream yield/selectivity of approximately 0.622/0.620 in batch 6. Nevertheless, these were unreplicated comparisons, and the final recommended S0 process used C1. Catalyst effects should therefore be interpreted primarily as effects on upstream target and impurity formation rather than as an independently established change in crystal-growth kinetics.

### 2. Reaction–crystallization coupling

The reported crystal recovery was

`Y_crystal = recovered target product excluding seed / target product present before separation`.

It is therefore a crystallization-stage recovery, not overall yield from the limiting reagent. A useful approximate overall relationship is

`recovered target from charge ≈ reaction target yield × Y_crystal`,

subject to sampling, degradation, and mass-balance effects. Upstream chemistry still influences crystallization indirectly through target concentration, impurity concentration, and supersaturation. Impurities can alter nucleation, inhibit particular crystal faces, or become occluded in rapidly formed crystals.

This coupling appeared in the solvent/catalyst screen. Reaction selectivity and yield varied substantially even though conversion was usually near unity. For example, batch 3 had selectivity 0.672 and reaction yield 0.672, whereas batch 5 had selectivity 0.535 and yield 0.529. These differences changed the composition entering crystallization and plausibly contributed to the different recoveries and particle populations. The assays do not identify a particular molecular inhibition or incorporation mechanism, so face poisoning, solution-complex effects, and simple concentration effects remain alternatives.

Purity remained high in nearly every filtered product, including the fines-heavy S0 batches. This indicates that the main optimization conflict was not bulk impurity rejection but recovery versus particle-number distribution.

### 3. Process-history dependence

A conventional supersaturation description is useful:

`S = C / C*(T, solvent)`,

where `C*` is equilibrium solubility. Nucleation commonly increases much more sharply with supersaturation than growth; schematically,

`J ∝ exp[-B/(ln S)^2]`,

while growth may be represented as

`G = k_g (S - 1)^g`.

These are interpretive relationships, not fitted laws for this benchmark. They explain why a rapid excursion to low temperature can generate a large number of fines, whereas staged cooling can consume supersaturation through growth before the next temperature reduction.

The S0 sequence supplied the clearest history evidence:

- Batch 3, direct seeded cooling to 250 K: recovery 0.567, purity 0.993, fines 0.712.
- Batch 11, staged 300→250 K cooling: recovery 0.584, purity 0.996, fines 0.572. Recovery improved, but the fines constraint still failed.
- Batch 12, staged 320→285→250 K cooling: recovery 0.587, purity 0.997, fines 0.465. This was the highest observed qualifying recovery and remains the recommended batch.

The monotonic reduction in fines across those histories is consistent with suppressing a nucleation burst and allowing more growth or ripening before the final cold stage. The simultaneous increase in recovery suggests that staging did not merely sacrifice crystallized mass to improve size; the final 250 K stage still extracted substantial target.

S2 was much less sensitive. Batch 6 used one 14,400 s cooling step and gave recovery 0.562 with fines 0.311. Batch 9 added another 14,400 s cold-growth step and gave recovery 0.564 with fines 0.293. Those changes are small relative to measurement uncertainty, so additional cold residence was not demonstrated to have a meaningful effect. Batch 10 omitted seed and still gave recovery 0.565 and fines 0.290; consequently, a seed benefit was not established for S2 under these conditions.

Batch 1 illustrates a confound. It initially cooled to 285 K but was then held using an operation that allowed the vessel to drift back toward approximately 298 K. Its recovery was only 0.452 and fines were 0.425. Batch 2 used a fully controlled, colder 250 K crystallization and improved to recovery 0.507 and fines 0.332. Because temperature endpoint, residence history, and drift all changed, this comparison supports the controlled recipe as a package but does not isolate any one factor.

### 4. Revisions to the working interpretation

The initial expectation was that S2 with C1 or C3 would be optimal because the nominal material properties favored growth, low nucleation, and low occlusion. The S2 crystallization hypothesis was supported for robustness, but the catalyst ranking was revised when C0/S2 outperformed the other directly screened S2 catalysts.

The larger revision concerned S0. Direct cooling initially made S0 appear unsuitable because of severe fines. The later staged-cooling experiments showed that its high recovery could be retained while progressively reducing fines. Batch 12 therefore displaced the more conservative S2 route as the recommendation, not because S2 failed, but because S0 under the revised history produced the highest observed qualifying recovery.

### 5. Uncertainty and unresolved tradeoffs

The final-assay standard uncertainties were approximately 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines. Batch 12's fines value of 0.465 is only 0.035 below the limit—about two reported standard deviations for a single assay—so its compliance margin is materially narrower than that of batches 6, 9, or 10. Its recovery advantage over the best S2 observations is about 0.022–0.025, which is suggestive but not decisive given two noisy, unreplicated measurements.

Batch 11 and batch 12 differed by only 0.003 in recovery, far below assay-scale uncertainty, while their fines differed by 0.107. Thus, the evidence for improved particle quality from the additional staging is stronger than the evidence for a recovery increase. Batch 11 itself was noncompliant, however, so batch 12 remains the maximum observed qualifying result.

The unresolved tradeoff is therefore robustness versus observed recovery: batch 12 offers the highest measured recovery but a modest fines margin, whereas the C0/S2 route offers slightly lower recovery with a much larger fines margin. Replication of batch 12 and nearby staged-cooling schedules would be required to quantify failure probability and determine whether the apparent S0 recovery advantage is reproducible.

Untested alternatives include different stage temperatures or durations, controlled annealing/reheating to dissolve fines, reduced agitation during growth, and systematic seed-size or seed-loading studies. No claim is made that the three-stage schedule is globally optimal or that S1/S3 cannot be rescued by comparable process development.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.22 | 0.12 | 0.35 |
| Q01 | crystal_purity | 0.982 | 0.95 | 1 |
| Q01 | crystal_size | 0.13 | 0.08 | 0.19 |
| Q01 | crystal_yield | 0.5 | 0.38 | 0.61 |
| Q02 | crystal_fines_fraction | 0.36 | 0.23 | 0.51 |
| Q02 | crystal_purity | 0.962 | 0.91 | 0.995 |
| Q02 | crystal_size | 0.1 | 0.05 | 0.16 |
| Q02 | crystal_yield | 0.42 | 0.3 | 0.54 |
| Q03 | crystal_fines_fraction | 0.43 | 0.28 | 0.6 |
| Q03 | crystal_purity | 0.986 | 0.95 | 1 |
| Q03 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q03 | crystal_yield | 0.47 | 0.34 | 0.59 |
| Q04 | crystal_fines_fraction | 0.27 | 0.16 | 0.4 |
| Q04 | crystal_purity | 0.989 | 0.96 | 1 |
| Q04 | crystal_size | 0.12 | 0.07 | 0.18 |
| Q04 | crystal_yield | 0.5 | 0.39 | 0.61 |
| Q05 | crystal_fines_fraction | 0.23 | 0.14 | 0.34 |
| Q05 | crystal_purity | 0.99 | 0.96 | 1 |
| Q05 | crystal_size | 0.14 | 0.09 | 0.2 |
| Q05 | crystal_yield | 0.5 | 0.4 | 0.6 |
| Q06 | crystal_fines_fraction | 0.44 | 0.29 | 0.61 |
| Q06 | crystal_purity | 0.975 | 0.93 | 1 |
| Q06 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q06 | crystal_yield | 0.53 | 0.42 | 0.64 |
| Q07 | crystal_fines_fraction | 0.21 | 0.12 | 0.33 |
| Q07 | crystal_purity | 0.99 | 0.96 | 1 |
| Q07 | crystal_size | 0.15 | 0.09 | 0.22 |
| Q07 | crystal_yield | 0.51 | 0.4 | 0.61 |
| Q08 | crystal_fines_fraction | 0.18 | 0.09 | 0.32 |
| Q08 | crystal_purity | 0.99 | 0.95 | 1 |
| Q08 | crystal_size | 0.17 | 0.1 | 0.25 |
| Q08 | crystal_yield | 0.43 | 0.29 | 0.56 |
| Q09 | crystal_fines_fraction | 0.78 | 0.58 | 0.94 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.055 | 0.02 | 0.1 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.62 | 0.42 | 0.81 |
| Q10 | crystal_purity | 0.989 | 0.95 | 1 |
| Q10 | crystal_size | 0.075 | 0.03 | 0.13 |
| Q10 | crystal_yield | 0.11 | 0.04 | 0.22 |
| Q11 | crystal_fines_fraction | 0.24 | 0.14 | 0.37 |
| Q11 | crystal_purity | 0.99 | 0.96 | 1 |
| Q11 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q11 | crystal_yield | 0.51 | 0.4 | 0.62 |
| Q12 | crystal_fines_fraction | 0.38 | 0.24 | 0.54 |
| Q12 | crystal_purity | 0.975 | 0.93 | 1 |
| Q12 | crystal_size | 0.115 | 0.06 | 0.18 |
| Q12 | crystal_yield | 0.64 | 0.52 | 0.75 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when seed-excluded product recovery is very small. Q01–Q02: S1 is predicted to outperform S3 through lower nominal solubility, nucleation, and impurity occlusion. Q03–Q04: greater seed loading should provide more controlled growth surfaces, modestly increasing recovery and reducing secondary fines. Q05–Q06: the gradual ramp should suppress the initial nucleation burst; the crash-and-hold may recover slightly more product but retain more fines despite long aging. Q07–Q08: the 315 K anneal should dissolve preferentially small particles and increase size, but the short recooling period likely lowers final recovery. Q09–Q10: a two-hour hold should increase recovery and growth relative to immediate filtration, although both remain fines-limited. Q11–Q12: doubling reagent charge raises target concentration and predicted fractional recovery, while the added supersaturation increases fines and slightly lowers purity and size. Intervals are 80% epistemic predictive ranges for noise-free outcomes; they are wider than assay noise because these recipes extrapolate to much smaller charges and much longer histories than the sealed experiments. Q02, Q03, Q06, and Q12 have material probability of crossing the fines limit despite feasible point estimates.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S2 provided the most robust direct-cooling process window.** Batches 6, 9, and 10 all met both constraints, with recovery 0.562–0.565, purity 0.978–1.000, and fines 0.290–0.311. This directly supports robustness within the tested C0/S2 conditions.
- **S0 was strongly process-history dependent.** Direct cooling in batch 3 gave fines 0.712; two-stage cooling in batch 11 reduced them to 0.572; three-stage cooling in batch 12 reduced them to 0.465 while maintaining recovery near 0.587. The numerical trend is observed. Interpreting it as suppression of a supersaturation-driven nucleation burst is mechanistic inference rather than direct measurement.
- **Batch 12 was the highest observed qualifying-recovery batch.** Its measured recovery was 0.587, purity 0.997, and fines 0.465. This is a direct result, although its superiority over nearby recoveries is not statistically secure.
- **S1 and S3 were inferior under the particular screening recipe.** Batches 4 and 5 had recoveries of 0.472 and 0.434 and fines of 0.540 and 0.644. This does not establish that the solvents are intrinsically unsuitable under other histories.

### Contradicted or revised
- **The initial expectation that C1 or C3 would be the best S2 catalyst was contradicted by the direct screen.** Batch 6 using C0/S2 gave recovery 0.562, versus 0.507 for C1 in batch 2, 0.508 for C2 in batch 7, and 0.528 for C3 in batch 8. Because these were single runs, the ranking remains provisional.
- **The early conclusion that S0 was unsuitable because of fines was revised.** Batch 3 failed badly, but batch 12 showed that a different cooling history could bring fines below 0.50 without losing its recovery advantage.
- **A strong seed benefit was not supported for S2.** Seeded batch 6 and unseeded batch 10 had very similar recovery and fines. This does not prove equivalence because other stochastic and history effects were not replicated.

### Still untested or unresolved
- The proposed nucleation-versus-growth mechanism was not measured directly: supersaturation, nucleation rate, crystal-count trajectories, and growth rates were not observed.
- Staging was confounded with total residence time. Batches 3, 11, and 12 changed both temperature path and accumulated crystallization time.
- Repeatability of batch 12 remains unknown. Its fines margin was only 0.035, and its recovery advantage over the best S2 batches was modest relative to assay uncertainty.
- Annealing, controlled reheating, agitation effects, seed-size distribution, and systematic seed-loading effects were not tested.
- Catalyst effects on crystal recovery may actually be mediated by target concentration or impurity composition; no experiment isolated a direct catalyst–crystal interaction.

## 2. One additional experiment

I would run the batch-12 S0/C1 chemistry and seed loading but replace its 320→285→250 K schedule with **three consecutive 14,400 s periods at 250 K**, keeping total crystallization time equal to batch 12. I would make non-destructive particle-size measurements after each period, then filter, terminate, and perform the final assay.

This would distinguish two leading explanations:

1. **Temperature-path mechanism:** gradual staging prevents an early nucleation burst and directs supersaturation into growth.
2. **Residence/ripening mechanism:** batch 12 improved mainly because it simply received more crystallization time than batch 3, irrespective of the staged temperatures.

If staging is causal, the direct-to-250 K experiment should rapidly generate many fines and remain smaller or above the 0.50 fines limit even after extended aging; recovery could be comparable to or greater than batch 12. If residence or ripening dominates, fines should progressively decline during the repeated 250 K holds and approach batch 12’s 0.465, with comparable size and recovery. If neither trajectory reproduces batch 12, its apparent advantage may reflect run variability or an interaction specific to the staged path. The serial particle measurements would reveal whether improvement occurs continuously during cold aging or specifically before the final temperature step.

## 3. Least effectively used evidence and least reliable prediction

The account used the **reaction-side degradation and byproduct observations** least effectively. For example, batch 7 had the lowest degradation warning (0.121) but only 0.508 crystal recovery; batch 11 had a low warning (0.137) and high recovery (0.584) but failed the fines constraint; batch 5 had a high warning (0.260) and low recovery (0.434). These observations could indicate coupling between impurity burden and crystallization, but the solvent, catalyst, and cooling histories were confounded, so I did not extract a defensible quantitative relationship.

The least reliable held-out prediction is **Q08**, which includes reheating an established slurry to 315 K followed by only one hour of recooling. No campaign batch used post-crystallization annealing. Consequently, the sealed prediction had to extrapolate whether the treatment would selectively dissolve fines, dissolve most product, alter purity, or cause a new nucleation burst during recooling. Q08’s predicted combination of lower recovery, larger particles, and fewer fines is mechanistically plausible, but it rests on an untested thermal-cycle response and is less reliable than predictions interpolating among the observed slow-cooling histories.
