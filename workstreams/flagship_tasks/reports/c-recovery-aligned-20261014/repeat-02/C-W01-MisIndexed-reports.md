# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Scope
The catalyst and solvent labels are anonymous benchmark materials, not identifiable real chemicals. The mechanism below is therefore a process-level interpretation of the observed data, not a claim about a particular molecular pathway.

All batches used 0.040 mol limiting reagent, 0.080 L solvent S2, and 0.005 mol catalyst. Except where noted, crystallization used 0.005 g seed, cooling to 260 K over 14,400 s, followed by filtration.

### 1. Material effects

**Catalyst effect—observed.** The most controlled catalyst comparison was at 340 K for 7,200 s:

- Batch 2, C0: crystal yield 0.374, purity 0.983, fines 0.356.
- Batch 3, C2: yield 0.301, purity 0.990, fines 0.308.
- Batch 4, C3: yield 0.347, purity 1.000, fines 0.347.

Thus C0 gave the highest recovery in that matched group. C1 in batch 1 gave only 0.317 crystal yield, high byproduct signal (0.508), and degradation warning (0.366), but it was tested at 365 K for 7,200 s with a different crystallization history. Consequently, C1 cannot be separated cleanly from its temperature/time confound.

**Interpretation.** C0 appears to provide the best realized balance between target formation and competing chemistry, despite C1 having the strongest nominal reference-panel activity. This was a major revision from the initial hypothesis that C1 would be preferred: the fixed-world material response was more important than nominal activity.

**Solvent effect—partly prior-based, not experimentally isolated.** Every completed batch used S2, so no causal solvent comparison was performed. Its nominal dossier—low relative solubility (0.7), low nucleation tendency (0.65), high growth tendency (1.3), and low impurity occlusion (0.65)—is consistent with the observed high crystal purities and generally acceptable fines. However, S2 superiority over S0, S1, or S3 remains untested.

### 2. Reaction kinetics and the hotter–shorter window

For C0/S2, coupled temperature/time profiles produced a strong systematic trend:

- Batch 5: 360 K, 3,600 s → reaction yield 0.586; crystal yield 0.510; degradation 0.133.
- Batch 6: 370 K, 1,800 s → reaction yield 0.661; crystal yield 0.605; degradation 0.080.
- Batch 7: 380 K, 900 s → reaction yield 0.726; crystal yield 0.668; degradation 0.037.
- Batch 8: 390 K, 600 s → reaction yield 0.747; crystal yield 0.697; degradation 0.030.
- Batch 9: 400 K, 450 s → reaction yield 0.750; crystal yield 0.691; degradation 0.015.

The improvement was therefore not caused by temperature alone: increasing temperature while sharply reducing residence time improved selectivity and limited accumulated exposure. Batch 9 did not improve crystal recovery beyond batch 8, indicating a broad optimum near 390–395 K rather than a monotonic benefit from still higher temperature.

A useful qualitative kinetic representation is

`dP/dt = kP(T)R − kD(T)P`

`dB/dt = kB(T)R + kDB(T)P`

where `R`, `P`, and `B` denote reactant, desired product, and combined byproduct/degradation pools. The data are consistent with a hot, short pulse making target rapidly while limiting the time integral of degradation. These equations are explanatory rather than fitted laws; the experiments do not identify individual rate constants or prove whether byproduct is formed in parallel, consecutively, or both.

### 3. Reaction–crystallization coupling

The reported recovery is an overall, seed-excluded quantity:

`Ycrystal = n(target product in isolated solid, excluding seed) / n(initial reagent)`.

A useful decomposition is

`Ycrystal ≈ X × Srxn × ηsep`,

where `X` is reaction conversion, `Srxn` is target selectivity, and `ηsep` is the fraction of target product recovered during crystallization and filtration. This is a bookkeeping relationship, not evidence that the factors are independent.

Final crystal recovery closely followed upstream target yield. For example, reaction yield rose from 0.586 in batch 5 to about 0.747 in batch 8, while crystal yield rose from 0.510 to 0.697. In the best late batches, crystal yield was roughly nine-tenths of measured reaction yield. Thus the main gain came from improving target formation, with crystallization then capturing a relatively stable large fraction.

Crystal purity remained approximately 0.978–1.000 even when reaction selectivity was only about 0.59–0.77. This suggests that S2 crystallization and filtration preferentially rejected byproduct into the liquid phase. It also explains why low reaction selectivity did not translate directly into low crystal purity. No mother-liquor assay, wash study, or impurity-specific solid analysis was performed, so the exact rejection mechanism remains uncertain.

### 4. Crystallization history and particle formation

A standard supersaturation description is

`σ = C/C*(T) − 1`,

with nucleation and growth represented qualitatively by

`B0 = kb σ^b`,  `G = kg σ^g`.

Rapid creation of high supersaturation favors many nuclei and fines; controlled cooling and a small seed population can direct material toward growth instead. S2's nominal low solubility and high growth/low nucleation profile are consistent with that picture.

**History dependence was clear.** Batch 1 used 0.020 g seed and initially cooled to 275 K, but a subsequent wait occurred while the hot control target remained active, allowing the batch to warm to about 297 K before it was cooled again. It ended with fines 0.519, just above specification, and crystal yield 0.317. This is not a clean seed-dose experiment: reaction quality, the warm excursion, and the shallower final temperature all differed. Nevertheless, it demonstrates that an endpoint temperature alone is not an adequate recipe descriptor.

With improved reaction conditions, 0.005 g seed and slow cooling to 260 K produced fines of 0.299, 0.271, 0.225, 0.256, and 0.277 in batches 5–9. Cooling more deeply to 250 K with only 0.001 g seed gave batch 10 a crystal yield of 0.702, purity 0.979, and fines 0.270.

The unseeded batch 11 gave yield 0.693, purity 0.994, and fines 0.252. Numerically, omitting seed slightly reduced recovery and fines, but the differences from batch 10 are comparable to assay uncertainty and single-batch variability. A true seed effect is therefore unresolved.

### 5. Recommended process and why it was selected

Batch 12 used C0/S2, 395 K for 600 s, 0.001 g seed, cooling to 250 K over 14,400 s, filtration, and final assay. It achieved:

- Seed-excluded crystal yield: 0.7045
- Crystal purity: 0.9951
- Fines below 20 µm: 0.2603
- Crystal-size metric: 0.1116
- CSD-quality metric: 0.7408
- Reaction yield: 0.7552
- Selectivity: 0.7578
- Degradation warning: 0.0339

It had the highest observed crystal recovery and comfortably met purity ≥0.80 and fines ≤0.50. Its result also agrees with the hotter–shorter reaction trend and the successful deep-cooling histories, rather than being an isolated high result.

### 6. Revisions, uncertainty, and unresolved tradeoffs

1. **Catalyst revision:** the initial C1 preference based on nominal activity was rejected in favor of experimentally superior C0.
2. **Reaction revision:** long hot residence was replaced by a hotter, much shorter reaction pulse after high byproduct and degradation were observed.
3. **Crystallization revision:** the initial 0.020 g seed/275 K process was replaced by smaller seed doses and deeper, slow cooling after excessive fines in batch 1.
4. **Uncertainty:** each complete recipe was run once, and final-assay standard deviations were approximately 0.010 for crystal yield and purity and 0.018 for fines. The small yield differences among batches 8, 10, 11, and 12 are therefore not strong evidence for fine-scale ranking, although all support the same process region.
5. **Quality/recovery tradeoff:** deeper cooling and reduced seeding increased or maintained recovery without threatening the fines limit in this study, but batch 10 had slightly lower purity/CSD quality than batches 11–12. Batch 8 had somewhat larger particles than some later batches but lower recovery. The apparent tradeoff is modest and unresolved because seed dose, endpoint temperature, and run-to-run variation were not independently replicated.
6. **Untested alternatives:** solvent identity, catalyst loading, staged cooling, seed-addition temperature, agitation during crystallization, washing, resuspension, and repeated confirmation of the 390–395 K optimum were not studied. These could alter recovery, impurity rejection, and particle-size distribution.

Overall, the evidence supports a coupled mechanism in which C0 under a hot–short reaction history maximizes target availability, while S2, low seeding, slow deep cooling, and filtration convert most of that target into high-purity crystals with acceptable fines.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.43 | 0.3 | 0.57 |
| Q01 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q01 | crystal_size | 0.075 | 0.04 | 0.12 |
| Q01 | crystal_yield | 0.5 | 0.37 | 0.62 |
| Q02 | crystal_fines_fraction | 0.31 | 0.2 | 0.44 |
| Q02 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q02 | crystal_size | 0.098 | 0.055 | 0.15 |
| Q02 | crystal_yield | 0.52 | 0.39 | 0.64 |
| Q03 | crystal_fines_fraction | 0.43 | 0.29 | 0.58 |
| Q03 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q03 | crystal_size | 0.105 | 0.055 | 0.17 |
| Q03 | crystal_yield | 0.27 | 0.15 | 0.4 |
| Q04 | crystal_fines_fraction | 0.54 | 0.4 | 0.68 |
| Q04 | crystal_purity | 0.89 | 0.78 | 0.97 |
| Q04 | crystal_size | 0.064 | 0.03 | 0.11 |
| Q04 | crystal_yield | 0.29 | 0.17 | 0.42 |
| Q05 | crystal_fines_fraction | 0.47 | 0.33 | 0.61 |
| Q05 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q05 | crystal_size | 0.075 | 0.038 | 0.13 |
| Q05 | crystal_yield | 0.29 | 0.17 | 0.42 |
| Q06 | crystal_fines_fraction | 0.65 | 0.51 | 0.78 |
| Q06 | crystal_purity | 0.85 | 0.72 | 0.95 |
| Q06 | crystal_size | 0.043 | 0.018 | 0.08 |
| Q06 | crystal_yield | 0.3 | 0.18 | 0.43 |
| Q07 | crystal_fines_fraction | 0.45 | 0.31 | 0.59 |
| Q07 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q07 | crystal_size | 0.08 | 0.04 | 0.135 |
| Q07 | crystal_yield | 0.3 | 0.18 | 0.43 |
| Q08 | crystal_fines_fraction | 0.4 | 0.26 | 0.55 |
| Q08 | crystal_purity | 0.93 | 0.83 | 0.99 |
| Q08 | crystal_size | 0.09 | 0.045 | 0.15 |
| Q08 | crystal_yield | 0.24 | 0.12 | 0.38 |
| Q09 | crystal_fines_fraction | 0.7 | 0.54 | 0.83 |
| Q09 | crystal_purity | 0.92 | 0.8 | 0.99 |
| Q09 | crystal_size | 0.033 | 0.01 | 0.07 |
| Q09 | crystal_yield | 0.018 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.44 | 0.29 | 0.6 |
| Q10 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q10 | crystal_size | 0.064 | 0.028 | 0.115 |
| Q10 | crystal_yield | 0.14 | 0.06 | 0.25 |
| Q11 | crystal_fines_fraction | 0.49 | 0.35 | 0.63 |
| Q11 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q11 | crystal_size | 0.07 | 0.034 | 0.12 |
| Q11 | crystal_yield | 0.29 | 0.17 | 0.42 |
| Q12 | crystal_fines_fraction | 0.6 | 0.45 | 0.74 |
| Q12 | crystal_purity | 0.84 | 0.7 | 0.94 |
| Q12 | crystal_size | 0.056 | 0.025 | 0.1 |
| Q12 | crystal_yield | 0.41 | 0.27 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes add seed, so particles are expected even when little new target crystallizes. Q01–Q02: S3's lower nominal solubility, nucleation tendency, and impurity occlusion should give cleaner, coarser crystals than S1, partly offsetting S1's greater upstream activity. Q03–Q04: the very large seed charge should slightly improve capture but shift the number distribution toward smaller particles and more fines; this seed effect was only weakly resolved experimentally, so intervals overlap. Q05–Q06: gradual cooling should suppress the supersaturation spike and fines relative to an immediate crash, while long-time recovery remains similar. Q07–Q08: reheating after crystallization should dissolve some solid and preferentially remove small or impure crystals, improving purity/size but lowering recovery because only one hour of recooling follows. Q09–Q10: the extra two-hour growth period should materially increase seed-excluded recovery, size, and feasibility relative to filtering after 60 seconds. Q11–Q12: doubling reagent at fixed solvent and catalyst raises supersaturation and expected recovery but also increases impurity occlusion and secondary nucleation, worsening purity and fines. Uncertainty is widest for S0 because it was not tested in the campaign, for C1 under this scaled loading, and for the extreme seed, thermal-cycle, and short-growth histories.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **C0 was the best catalyst among the matched C0/C2/C3 comparison.** At 340 K for 7,200 s, batch 2 (C0) gave crystal yield 0.374, versus 0.301 for C2 in batch 3 and 0.347 for C3 in batch 4. Purity and fines were acceptable in all three. The ranking is observed directly; attributing it to intrinsic catalytic selectivity remains an interpretation.
- **The tested hotter–shorter C0 profiles improved upstream and final recovery.** From batch 5 through batch 8, reaction yield increased from 0.586 to 0.747 and crystal yield from 0.510 to 0.697 as the profile changed from 360 K/3,600 s to 390 K/600 s. Degradation warning fell from 0.133 to 0.030. Batch 9 at 400 K/450 s gave a slightly lower crystal yield of 0.691, supporting a plateau near 390–395 K rather than unlimited benefit from higher temperature.
- **Upstream target formation and crystal recovery were coupled.** Batches 5–9 show crystal yield tracking reaction yield. This directly supports correlation; the proposed decomposition into conversion, selectivity, and separation efficiency is interpretation rather than a fitted causal model.
- **The final process region was feasible.** Batches 8, 10, 11, and 12 all met the purity and fines constraints. Batch 12 had the highest observed recovery: yield 0.705, purity 0.995, and fines 0.260.

### Supported, but with important confounding

- **Long residence promoted byproduct/degradation.** Batch 1, using C1 at 365 K for 7,200 s, had byproduct signal 0.508 and degradation warning 0.366, whereas hotter–shorter C0 batches were much cleaner. This is consistent with cumulative degradation, but catalyst identity, temperature, duration, and downstream history all changed.
- **Smaller seed/deeper cooling improved the process relative to the initial recipe.** Batch 1 used 0.020 g seed and an irregular 275 K history and produced fines 0.519. Later batches using 0.005 or 0.001 g seed and cooling to 260 or 250 K had fines around 0.225–0.299. Because reaction quality and thermal history also changed, this supports the combined recipe change, not an isolated seed-dose law.
- **Crystallization rejected reaction impurities.** Final crystal purity remained roughly 0.978–1.000 even when reaction selectivity was only about 0.59–0.77. Preferential impurity retention in the liquid phase is a plausible interpretation, but no mother-liquor mass balance or impurity-specific solid analysis directly demonstrated it.

### Contradicted or revised

- **The initial expectation that nominally active C1 would be best was contradicted operationally.** Batch 1 was inferior to the C0 process. However, C1 was never tested under the optimized short-residence conditions, so the stronger claim that C0 is intrinsically superior to C1 under all relevant conditions remains unproven.
- **A monotonic benefit from increasing reaction temperature was contradicted.** Batch 9 did not improve recovery over batch 8 despite its higher temperature.

### Still untested or unresolved

- S2 was used in every campaign batch, so its proposed superiority over S0, S1, and S3 is untested experimentally.
- The effects of seed mass and endpoint temperature were not independently separated. Batch 10 (0.001 g seed), batch 11 (unseeded), and batch 12 differed only modestly, at about the scale of assay uncertainty.
- The warm excursion in batch 1 shows that history can matter, but it does not isolate whether the adverse result came from reheating, large seed mass, shallow cooling, or poor upstream chemistry.
- Staged cooling, agitation effects, washing, resuspension, and repeatability of the small batch-12 advantage were not tested.

## 2. One additional experiment

I would repeat the complete batch-12 process but substitute **C1 for C0**, keeping S2, reagent and catalyst loadings, 395 K for 600 s, 0.001 g seed, cooling to 250 K over 14,400 s, filtration, and assay unchanged. I would include a reaction-stage HPLC immediately before crystallization, accepting its small sample depletion.

This experiment would use batch 12 as the existing matched C0 comparator and distinguish two explanations for batch 1:

1. **Catalyst-identity explanation:** C1 intrinsically gives poorer target selectivity or more degradation in this world. Expected result: lower pre-crystallization target yield/selectivity, higher byproduct or degradation, and lower final crystal yield than batch 12.
2. **Residence-history explanation:** Batch 1 failed mainly because C1 was held hot too long, not because C1 itself was inferior. Expected result: under the 395 K/600 s pulse, C1 would approach or exceed batch 12 in reaction and crystal yield while retaining high purity and acceptable fines.

If reaction-stage results matched batch 12 but final recovery differed, that would instead implicate catalyst-dependent downstream composition or nucleation behavior. A replicate of batch 12 would better measure precision, but the C1 substitution provides more mechanistic discrimination with one experiment.

## 3. Least effectively used observation and least reliable prediction

**Least effectively used observation:** the campaign collected crystal-size and CSD-quality values, but the account relied mainly on yield, purity, and fines. For example, batch 8 had a crystal-size metric of 0.122, while batches 10–12 ranged about 0.085–0.112, yet these variations were not incorporated into a quantitative population-balance relationship. They were noisy, non-monotonic, and confounded by reaction profile, seed dose, and cooling endpoint. Consequently, the proposed nucleation-versus-growth explanation was more qualitative than the available size observations ideally warranted.

**Least reliable held-out prediction:** Q12, the doubled-reagent upstream-loading case. It simultaneously extrapolated to solvent S0, a C1 process at a much smaller absolute scale than the campaign, a large seed charge, and twice the reagent concentration at fixed catalyst amount. The fractional crystal-yield definition creates competing effects: higher concentration should promote crystallization, while the lower catalyst-to-reagent ratio could reduce conversion and increased supersaturation could worsen occlusion and secondary nucleation. None of those concentration effects was isolated in the campaign. Therefore, both the predicted recovery increase and the predicted loss of quality for Q12 are substantially less secure than predictions based mainly on cooling or hold-time contrasts.
