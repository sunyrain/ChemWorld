# C-W01-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Working process picture

The campaign is consistent with two coupled stages:

1. **Catalytic reaction:** limiting reagent is converted into target product while a competing pathway forms byproduct/degradation material.
2. **Crystallization and isolation:** dissolved target product is supersaturated by cooling, partitions into seeded crystals, and is recovered by filtration. Excess supersaturation can increase recovery but also produces many fine particles.

A useful bookkeeping relationship is

\[
Y_{crystal}\approx Y_{reaction}\,f_{crystallized}\,f_{isolated},
\]

where crystal yield is the seed-excluded solid target product divided by the initial reagent charge. Thus high conversion alone is insufficient: selectivity limits how much target exists, while solubility, nucleation, growth, and filtration determine how much becomes acceptable solid.

A corresponding qualitative supersaturation measure is

\[
S(T)=\frac{C_{target}}{C^*_{target}(T)}.
\]

Cooling and reducing solvent volume raise \(S\). Moderate supersaturation favors growth on seeds; excessive supersaturation favors primary/secondary nucleation and fines.

### 2. Material effects

#### Catalyst

The initial prior favored C1 or C3 based on their nominal activity. Batch 1 used C1/S2 and reached complete measured conversion, but final reaction yield was only 0.576, selectivity 0.578, and degradation warning 0.215. Its crystal yield was 0.466.

The catalyst screen revised that view:

- **Batch 2, C3:** crystal yield 0.429.
- **Batch 3, C2:** crystal yield 0.426.
- **Batch 4, C0:** crystal yield 0.516, purity 1.000, fines 0.278.

Batches 3 and 4 are the cleanest comparison because both used S2, 0.08 L solvent, 365 K for 3600 s, and a 268 K crystallization endpoint. C0 increased final reaction yield from about 0.534 to 0.602 and crystal yield from 0.426 to 0.516. This supports a C0-specific advantage in productive selectivity or suppression of competing chemistry in this world, despite C0's less impressive nominal activity dossier.

The broader catalyst ranking remains somewhat uncertain because C1 and C3 were tested with different thermal histories. Catalyst–temperature and catalyst–solvent interactions were not mapped factorially.

#### Solvent

All completed experiments used S2, so there is no direct experimental solvent ranking. Selection of S2 rested on its nominal combination of low relative solubility, low nucleation tendency, high crystal growth, and low impurity occlusion. The consistently high final crystal purities—approximately 0.978 to 1.000—are compatible with that prior, but do not establish that S2 is superior to S0, S1, or S3.

An alternative explanation is that the product/impurity system intrinsically rejects impurity well under all tested conditions. Direct solvent comparisons would be required to distinguish this from a specific S2 effect.

### 3. Reaction–crystallization coupling

C0 recipes generally produced final reaction yields near 0.59–0.60. Changes in crystal yield thereafter largely reflected downstream recovery.

For example:

- **Batch 4:** reaction yield 0.602 and crystal yield 0.516, implying roughly 86% downstream capture of the reaction-stage target.
- **Batch 8:** reaction yield 0.589 and crystal yield 0.552, implying roughly 94% capture.

The higher crystal recovery in batch 8 therefore did not arise from a clearly better reaction. It arose mainly from greater crystallization/isolation efficiency at higher concentration and a colder endpoint.

Temperature and residence time also affected upstream quality. Batch 5 held C0 at 355 K for 5400 s and gave only 0.443 crystal yield, with byproduct signal 0.356 and degradation warning 0.179. By contrast, batch 6 used 355 K for 3600 s and gave 0.522 crystal yield, byproduct signal 0.294, and degradation warning 0.128. This suggests that unnecessary hot residence can erode productive material through continued side reaction or degradation. Because these were single batches, stochastic assay variation remains an alternative explanation.

### 4. Concentration and the quality/recovery boundary

With C0, 355 K for 3600 s, and increasingly concentrated S2 solutions, the observed trend was:

- **Batch 6, 0.08 L S2:** crystal yield 0.522; fines 0.300.
- **Batch 7, 0.06 L S2:** crystal yield 0.544; fines 0.314.
- **Batch 8, 0.04 L S2:** crystal yield 0.552; fines 0.377.
- **Batch 9, 0.03 L S2:** crystal yield 0.549; fines 1.000.

For a 0.04 mol charge, these volumes correspond nominally to 0.50, 0.67, 1.00, and 1.33 mol/L before reaction-volume changes. Recovery improved as concentration rose to about 1.0 mol/L, consistent with lower dissolved-product loss. However, the transition from 0.04 to 0.03 L crossed a sharp nucleation boundary: recovery no longer improved, while every counted particle was reported below 20 µm.

This is the principal unresolved quality/recovery tradeoff. Less concentrated batches had lower recovery but a larger fines margin; batch 8 had the best feasible recovery but only about 0.123 absolute margin below the 0.50 fines limit. Batch 9 shows that a small additional concentration increase can destroy morphology without improving recovery.

Purity was not the active constraint in this region: batch 8 purity was 0.985 and batch 9 purity was 0.989. The limiting quality attribute was particle-size distribution.

### 5. Process-history dependence

The campaign tested whether more elaborate thermal histories could improve the batch-8 base process:

- **Batch 8, direct cooling to 250 K for 14400 s:** yield 0.552; fines 0.377.
- **Batch 10, staged cooling through 300 K:** yield 0.547; fines 0.460.
- **Batch 11, cooling, partial reheating to 310 K, then recooling:** yield 0.534; fines 0.444.
- **Batch 12, direct cooling followed by another 14400 s at 250 K:** yield 0.541; fines 0.392.

Contrary to the initial expectation, staged cooling and partial dissolution/recrystallization did not produce larger, cleaner crystals. A possible mechanism is that these histories created additional nucleation episodes or crystal attrition rather than sustained seed growth. The reheat may also have redissolved useful solid without allowing complete regrowth.

However, these mechanistic explanations are interpretations rather than demonstrated causes. There were no independent replicates, and batch 12 differed from batch 8 by less than would justify a strong claim once final-assay noise and process variability are considered. The evidence supports using the simpler direct cooling history, not a universal conclusion that staged cooling is harmful.

### 6. Revisions during the campaign

The main revisions were:

1. **Catalyst prior revised:** nominal activity initially favored C1/C3, but batches 1–4 shifted the working choice to C0.
2. **Concentration trend bounded:** batches 6–8 suggested that increasing concentration improved recovery; batch 9 falsified monotonic extrapolation by revealing catastrophic fines at 0.03 L.
3. **Complex thermal histories rejected provisionally:** batches 10–12 did not improve upon direct cooling and often worsened fines or recovery.
4. **Objective focus revised:** purity was initially uncertain, but remained comfortably above 0.80. Optimization therefore became a recovery-versus-fines problem rather than a recovery-versus-purity problem.

### 7. Uncertainty and untested alternatives

The final assays have stated noise scales of about 0.01 for crystal yield and 0.018 for fines fraction, in addition to unquantified process variability. Consequently, the yield differences among batches 7, 8, 9, 10, and 12 are small enough that their precise ranking is not strongly resolved by single runs. Batch 8 remains the appropriate operating choice because it had the highest observed feasible recovery, not because its advantage has been replicated.

Important untested alternatives include:

- Solvent identity and solvent mixtures.
- Catalyst–solvent and catalyst–temperature interactions.
- Solvent volumes narrowly between 0.03 and 0.04 L, where a higher-recovery feasible window might exist.
- Alternative seed loading, seed size, or seed-addition temperature.
- Controlled agitation during crystallization and filtration-washing conditions.
- Replication to separate real process-history effects from batch variability.

Overall, the observations support a mechanism in which C0 supplies the best tested target-product pool, while S2 concentration and cooling determine whether that pool is recovered by seed growth or lost to excessive fine-particle nucleation. Batch 8 lies near the favorable side of that morphology boundary: high recovery and purity with compliant, but not widely buffered, fines.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.16 | 0.06 | 0.31 |
| Q01 | crystal_purity | 0.97 | 0.91 | 1 |
| Q01 | crystal_size | 0.24 | 0.14 | 0.35 |
| Q01 | crystal_yield | 0.3 | 0.2 | 0.4 |
| Q02 | crystal_fines_fraction | 0.27 | 0.13 | 0.46 |
| Q02 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q02 | crystal_size | 0.18 | 0.09 | 0.28 |
| Q02 | crystal_yield | 0.23 | 0.14 | 0.34 |
| Q03 | crystal_fines_fraction | 0.59 | 0.39 | 0.78 |
| Q03 | crystal_purity | 0.93 | 0.84 | 0.99 |
| Q03 | crystal_size | 0.09 | 0.035 | 0.17 |
| Q03 | crystal_yield | 0.12 | 0.055 | 0.21 |
| Q04 | crystal_fines_fraction | 0.42 | 0.25 | 0.61 |
| Q04 | crystal_purity | 0.92 | 0.83 | 0.99 |
| Q04 | crystal_size | 0.13 | 0.065 | 0.22 |
| Q04 | crystal_yield | 0.14 | 0.07 | 0.23 |
| Q05 | crystal_fines_fraction | 0.4 | 0.23 | 0.59 |
| Q05 | crystal_purity | 0.92 | 0.83 | 0.99 |
| Q05 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q05 | crystal_yield | 0.14 | 0.07 | 0.23 |
| Q06 | crystal_fines_fraction | 0.7 | 0.5 | 0.87 |
| Q06 | crystal_purity | 0.9 | 0.8 | 0.98 |
| Q06 | crystal_size | 0.06 | 0.02 | 0.13 |
| Q06 | crystal_yield | 0.15 | 0.075 | 0.24 |
| Q07 | crystal_fines_fraction | 0.38 | 0.21 | 0.57 |
| Q07 | crystal_purity | 0.93 | 0.84 | 0.99 |
| Q07 | crystal_size | 0.15 | 0.075 | 0.24 |
| Q07 | crystal_yield | 0.145 | 0.07 | 0.235 |
| Q08 | crystal_fines_fraction | 0.48 | 0.28 | 0.68 |
| Q08 | crystal_purity | 0.94 | 0.85 | 1 |
| Q08 | crystal_size | 0.12 | 0.055 | 0.21 |
| Q08 | crystal_yield | 0.125 | 0.055 | 0.215 |
| Q09 | crystal_fines_fraction | 0.85 | 0.65 | 0.98 |
| Q09 | crystal_purity | 0.96 | 0.85 | 1 |
| Q09 | crystal_size | 0.05 | 0.015 | 0.11 |
| Q09 | crystal_yield | 0.008 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.46 | 0.27 | 0.67 |
| Q10 | crystal_purity | 0.94 | 0.84 | 1 |
| Q10 | crystal_size | 0.11 | 0.045 | 0.2 |
| Q10 | crystal_yield | 0.055 | 0.018 | 0.11 |
| Q11 | crystal_fines_fraction | 0.39 | 0.22 | 0.58 |
| Q11 | crystal_purity | 0.93 | 0.84 | 0.99 |
| Q11 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q11 | crystal_yield | 0.14 | 0.07 | 0.23 |
| Q12 | crystal_fines_fraction | 0.68 | 0.47 | 0.86 |
| Q12 | crystal_purity | 0.87 | 0.76 | 0.96 |
| Q12 | crystal_size | 0.09 | 0.035 | 0.17 |
| Q12 | crystal_yield | 0.32 | 0.2 | 0.45 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is predicted to give better recovery, growth and impurity rejection than more soluble S3, while S3's higher nominal reaction activity partly offsets its crystallization disadvantage. Q03–Q04: the larger seed charge should control supersaturation and suppress secondary nucleation; the very small seed charge is assigned more fines and slightly lower recovery. Q05–Q06: slow staged cooling should favor seed growth, whereas the rapid temperature drop should cause a nucleation burst even after a long cold hold. Q07–Q08: the 315 K reheat is expected to redissolve some product and trigger another nucleation episode on recooling, reducing recovery and worsening fines; this direction follows the campaign's unsuccessful reheat/recool test, but transfer to S0 is uncertain. Q09–Q10: seeds ensure particles are present in both; 60 seconds gives almost no seed-excluded recovery, while the additional 7200 seconds permits appreciable growth and may bring fines just below the specification. Q11–Q12: doubling reagent loading raises supersaturation and recovery but is expected to cross into excessive nucleation and impurity occlusion. Intervals are deliberately broad because S0, S1 and S3 were not tested in the sealed campaign, these recipes use much smaller charges and far longer cooling histories, and several feasibility calls lie close to the fines threshold.

## K2

## 1. Status of the main claims

### Supported within the tested scope

- **C0 was the best tested catalyst under comparable S2 conditions.** The strongest direct comparison is batch 3 versus batch 4: both used 0.08 L S2, 365 K for 3600 s, and a 268 K crystallization endpoint. Crystal yield increased from 0.426 with C2 to 0.516 with C0, while both met the quality limits. Interpreting this as better productive selectivity for C0 is reasonable, but the observation itself is only the outcome difference.
- **Concentrating the solution improved recovery until a morphology boundary was reached.** With the C0 process, batches 6, 7, and 8 used 0.08, 0.06, and 0.04 L S2 and gave crystal yields of 0.522, 0.544, and 0.552, while fines rose from 0.300 to 0.377. Batch 9 at 0.03 L retained similar yield, 0.549, but fines reached 1.000. The observed boundary is strong; attributing it specifically to a supersaturation-driven nucleation burst remains mechanistic interpretation.
- **Purity was not the active constraint in the explored S2 region.** Final purity remained about 0.978–1.000 across all twelve batches. The practical tradeoff was recovery versus fines.
- **The tested complex thermal histories did not improve upon direct cooling.** Relative to batch 8, staged cooling in batch 10, reheat/recooling in batch 11, and an extended 250 K continuation in batch 12 gave lower observed yields and generally poorer fines. This supports choosing the simpler history, although single-batch comparisons do not prove that the histories are intrinsically harmful.
- **Prolonged hot residence was unfavorable in the tested C0 recipe.** Batch 5, heated at 355 K for 5400 s, had higher byproduct/degradation signals and lower crystal yield than batch 6, heated for 3600 s. This is suggestive rather than decisive because the downstream endpoints also differed.

### Contradicted or revised

- **The nominal catalyst prior favoring C1 or C3 was contradicted by the campaign.** Batches 1–4 shifted the operating choice to C0.
- **A monotonic concentration–recovery extrapolation was contradicted by batch 9.** Reducing S2 below 0.04 L did not increase recovery and catastrophically worsened fines.
- **The expectation that slower staging or a dissolution–regrowth cycle would improve particle quality was contradicted in the tested implementations.** Batches 10 and 11 did not outperform batch 8.

### Still untested

- S2 superiority over S0, S1, or S3: every campaign batch used S2.
- Catalyst–solvent and catalyst–temperature interactions beyond the limited comparisons.
- Effects of seed mass, seed size, seed-addition temperature, and crystallization agitation.
- Whether the batch-9 fines transition is a reproducible concentration threshold rather than an unusual realization.
- Whether an intermediate solvent volume between 0.03 and 0.04 L offers higher feasible recovery.
- Replicate variability; none of the key recipes was independently replicated.

## 2. One additional experiment

I would run an **intermediate-boundary experiment** identical to batch 8 except for **0.035 L S2**: 0.04 mol reagent, 0.005 mol C0, 355 K for 3600 s, 0.05 g seed, direct cooling to 250 K for 14400 s, particle-size measurement, filtration, termination, and final assay.

This would distinguish three explanations:

1. **A sharp concentration-driven nucleation threshold:** fines would exceed 0.50, with recovery remaining near 0.55. That would place the usable boundary between 0.035 and 0.04 L and support the supersaturation interpretation of batch 9.
2. **A narrower optimum between batches 8 and 9:** fines would remain at or below 0.50 and recovery would equal or exceed batch 8. That would show that 0.03 L crossed the threshold but that 0.04 L was not the true feasible optimum.
3. **Batch variability or a non-monotonic process effect:** recovery or fines would differ substantially from the interpolation between batches 8 and 9 without a clear boundary pattern. That outcome would weaken the claim that concentration alone caused batch 9.

One batch cannot fully quantify repeatability, but this design has more discriminatory value than another distant condition because it probes the decision-critical boundary directly.

## 3. Least effectively used observation and least reliable prediction

The account used the **paired pre-filtration particle measurements and final-assay particle results** least effectively. For example, fines changed from 0.438 before filtration to 0.460 at final assay in batch 10, from 0.455 to 0.444 in batch 11, and from 0.288 to 0.298 in batch 3. I emphasized final values but did not exploit these pairs to show that instrument variation and/or filtration-associated changes are comparable to some differences between thermal histories. That omission made the process-history interpretation sound more certain than warranted.

The least reliable held-out prediction is **Q09**. It extrapolates from long crystallizations to only 60 seconds of cooling at 292 K. The campaign did not observe such an early endpoint, and the prediction depends on uncertain simulator semantics: whether introduced seed alone guarantees the reported particle population, how seed particles enter number-weighted size and fines, and how quickly seed-excluded product deposits. Consequently, its predicted near-zero yield, very high fines, and even the confidence that particles are reportable have substantially weaker empirical support than predictions for long seeded cooling histories. The solvent predictions Q01–Q04 are also weak because S0, S1, and S3 were never tested, but Q09 requires the most extreme kinetic extrapolation.
