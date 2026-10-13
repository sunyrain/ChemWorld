# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The recommended process is batch 8: 0.040 mol limiting reagent, 0.040 L solvent S2, 0.005 mol catalyst C1, reaction at 390 K for 3,600 s with 500 rpm stirring, addition of 0.001 g seed, cooling to 250 K over 14,400 s, a further 14,400 s cold hold at 300 rpm, filtration, and final assay. It gave seed-excluded crystal recovery 0.553, crystal purity 0.989, and a number fraction below 20 µm of 0.275. Thus it satisfied purity ≥0.80 and fines ≤0.50.

Material effects

The prior dossier motivated S2 because it had the lowest nominal solubility (0.70 relative), low nucleation tendency (0.65), high crystal-growth tendency (1.30), and low impurity occlusion (0.65). Those properties suggest that cooling in S2 can generate substantial supersaturation while favoring growth on existing crystals rather than extensive secondary nucleation or impurity trapping. The consistently high crystal purity in all tested S2 batches—approximately 0.983–1.000—is compatible with that interpretation.

However, every completed batch used S2, so no experimental solvent comparison was made. The apparent agreement with the dossier is supportive, not proof that S2 is better than S0, S1, or S3. Hidden fixed-world solvent residuals and alternative solvent-dependent reaction effects remain untested.

C1 was selected from its relatively high nominal catalytic activity. With C1/S2 at 390 K for 3,600 s, conversion was generally about 0.99–1.00. Nevertheless, final-assay selectivity was only about 0.54–0.58, with byproduct signal around 0.34–0.38 and degradation warning around 0.22–0.25. No catalyst comparison was performed, so C1 is demonstrated to be adequate for conversion, not established as the most selective catalyst.

Reaction–crystallization coupling

A useful separation of quantities is

crystallization recovery = (recovered target product excluding seed contribution)/(target product present immediately before separation).

This is not overall yield from charged reagent. In a schematic overall balance,

overall isolated target fraction ≈ reaction target yield × crystallization recovery.

Consequently, nearly complete conversion did not imply high overall target production because reaction selectivity remained moderate. Conversely, the measured crystal recovery near 0.55 describes recovery of the target that had already formed. The high final crystal purity despite moderate reaction selectivity suggests preferential incorporation of target and rejection of reaction byproducts during crystallization in S2. This is an interpretation; direct mother-liquor composition and impurity partitioning were not independently quantified.

Crystallization can be described qualitatively through supersaturation,

S(t) = C(t)/C*(T, solvent),

with nucleation rate increasing steeply with S while crystal growth consumes supersaturation on existing surfaces. Cooling rate, concentration, seeding, and residence time therefore determine whether available target becomes a smaller number of grown crystals or a large population of fines.

Process-history dependence

1. Seed loading and cooling history mattered. Batch 1 used 0.010 g seed and a 7,200 s cooling step, yielding recovery 0.503 and fines 0.471. Batch 2 reduced seed to 0.001 g and cooled over 14,400 s; recovery was 0.511 and fines fell to 0.329, with normalized size increasing from 0.073 to 0.114. Cooling duration and seed mass changed together, so this does not isolate a seed effect.

2. Near-zero seeding was not clearly superior. Batch 3 used 0.00001 g seed with the long cooling program and gave recovery 0.511, fines 0.319, and size 0.075. Relative to batch 2, fines were similar but measured size was smaller. This led to retention of the modest 0.001 g seed dose rather than eliminating seeding.

3. A cold hold may increase recovery, but the effect is not firmly resolved. Batch 4 added a 14,400 s hold after slow cooling and measured recovery 0.526 versus 0.511 in batch 2, while remaining feasible at purity 1.000 and fines 0.341. The difference is modest and these were not otherwise replicated pairs.

4. Staged cooling was unfavorable under the tested schedule. Batch 5 paused at 280 K before reaching 250 K and produced recovery 0.510, fines 0.447, and size 0.060. It did not outperform the direct slow cool and approached the fines limit.

5. Rapid generation of supersaturation caused a strong recovery/quality tradeoff. Batch 6 cooled to 250 K in only 1,800 s and then held cold. Recovery rose to 0.534, but fines increased to 0.785, violating the constraint. Batch 7 added a 280 K reheat followed by recooling; recovery reached 0.540, but fines remained 0.753. Thus the tested annealing cycle did not erase the fine-particle population generated during the initial rapid cool. This supports a history-dependent nucleation interpretation: once excessive nuclei formed, later thermal treatment was insufficient to remove them.

6. Concentration had a non-monotonic or plateau-like effect within the feasible region. With the same slow-cool/cold-hold program, batch 8 used 0.040 L solvent and gave recovery 0.553, purity 0.989, and fines 0.275. Batch 9 used 0.020 L and gave recovery 0.551, purity 0.993, and fines 0.212. Batch 10 used 0.030 L and gave recovery 0.548, purity 0.988, and fines 0.294. These recovery differences are small enough that a precise optimum between 0.02 and 0.04 L is not established.

7. Excessive concentration crossed a particle-quality boundary. Batch 12 used only 0.010 L solvent and retained high recovery, 0.554, and purity, 1.000, but its fines fraction was 1.000. It was therefore ineligible despite marginally exceeding batch 8’s measured recovery. A plausible explanation is an abrupt rise in supersaturation and nucleation density at this concentration. Direct evidence distinguishing primary nucleation, agglomeration, and attrition was not collected.

Revisions to the working interpretation

The initial expectation was that S2/C1 with deep, slow cooling would be promising. Early results supported the material choice but showed that the initial 0.010 g seed and shorter cool were not optimal for particle quality. The working process was revised to 0.001 g seed, a 14,400 s cool, and a 14,400 s cold hold. Rapid cooling was then rejected because batches 6 and 7 failed the fines constraint. Concentration screening shifted the preferred solvent volume from 0.080 L toward 0.040 L. The final 0.010 L test demonstrated that concentration could not be increased indefinitely without severe fines formation.

Uncertainty and unresolved tradeoffs

Final-assay standard uncertainties were approximately 0.010 for recovery, 0.010 for purity, 0.018 for fines, and 0.025 for normalized size, in addition to process variability. Exact replication of the batch-8 recipe in batch 11 gave recovery 0.536, purity 1.000, and fines 0.282. Both runs comfortably met the constraints, but their recovery difference of about 0.017 is comparable to combined analytical uncertainty and possible batch variability. Therefore 0.553 should be treated as the observed result of the selected completed batch, not a precisely known expected recovery.

The main unresolved tradeoff is that more aggressive supersaturation can preserve or slightly increase recovery while producing unacceptable fines. Rapid cooling and the 0.010 L formulation illustrate this sharply. Within the feasible 0.02–0.04 L range, recovery appeared near a plateau while particle metrics varied. Batch 8 was selected because it had the highest measured feasible recovery, not because its superiority over batches 9–11 was statistically established. Additional replication and a finer 0.035–0.050 L concentration map would be needed to locate a robust optimum. Alternative catalysts, solvents, seed-size distributions, agitation histories, and more effective dissolution/annealing cycles remain untested.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.2 | 0.07 | 0.39 |
| Q01 | crystal_purity | 0.93 | 0.84 | 0.98 |
| Q01 | crystal_size | 0.35 | 0.17 | 0.55 |
| Q01 | crystal_yield | 0.28 | 0.13 | 0.45 |
| Q02 | crystal_fines_fraction | 0.12 | 0.03 | 0.28 |
| Q02 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q02 | crystal_size | 0.4 | 0.21 | 0.61 |
| Q02 | crystal_yield | 0.39 | 0.21 | 0.57 |
| Q03 | crystal_fines_fraction | 0.4 | 0.2 | 0.63 |
| Q03 | crystal_purity | 0.88 | 0.74 | 0.96 |
| Q03 | crystal_size | 0.38 | 0.17 | 0.61 |
| Q03 | crystal_yield | 0.17 | 0.04 | 0.34 |
| Q04 | crystal_fines_fraction | 0.23 | 0.09 | 0.43 |
| Q04 | crystal_purity | 0.91 | 0.79 | 0.97 |
| Q04 | crystal_size | 0.25 | 0.11 | 0.43 |
| Q04 | crystal_yield | 0.21 | 0.07 | 0.38 |
| Q05 | crystal_fines_fraction | 0.21 | 0.07 | 0.41 |
| Q05 | crystal_purity | 0.91 | 0.79 | 0.97 |
| Q05 | crystal_size | 0.27 | 0.12 | 0.46 |
| Q05 | crystal_yield | 0.22 | 0.08 | 0.39 |
| Q06 | crystal_fines_fraction | 0.68 | 0.46 | 0.87 |
| Q06 | crystal_purity | 0.87 | 0.72 | 0.96 |
| Q06 | crystal_size | 0.1 | 0.03 | 0.23 |
| Q06 | crystal_yield | 0.23 | 0.08 | 0.41 |
| Q07 | crystal_fines_fraction | 0.19 | 0.06 | 0.39 |
| Q07 | crystal_purity | 0.92 | 0.81 | 0.98 |
| Q07 | crystal_size | 0.3 | 0.14 | 0.5 |
| Q07 | crystal_yield | 0.23 | 0.09 | 0.4 |
| Q08 | crystal_fines_fraction | 0.6 | 0.36 | 0.82 |
| Q08 | crystal_purity | 0.91 | 0.78 | 0.98 |
| Q08 | crystal_size | 0.18 | 0.07 | 0.35 |
| Q08 | crystal_yield | 0.15 | 0.03 | 0.32 |
| Q09 | crystal_fines_fraction | 0.3 | 0.12 | 0.53 |
| Q09 | crystal_purity | 0.96 | 0.84 | 0.995 |
| Q09 | crystal_size | 0.14 | 0.06 | 0.27 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.27 | 0.1 | 0.49 |
| Q10 | crystal_purity | 0.92 | 0.79 | 0.98 |
| Q10 | crystal_size | 0.16 | 0.07 | 0.3 |
| Q10 | crystal_yield | 0.065 | 0.01 | 0.16 |
| Q11 | crystal_fines_fraction | 0.22 | 0.08 | 0.42 |
| Q11 | crystal_purity | 0.91 | 0.79 | 0.97 |
| Q11 | crystal_size | 0.27 | 0.12 | 0.46 |
| Q11 | crystal_yield | 0.22 | 0.08 | 0.39 |
| Q12 | crystal_fines_fraction | 0.35 | 0.16 | 0.59 |
| Q12 | crystal_purity | 0.87 | 0.72 | 0.96 |
| Q12 | crystal_size | 0.31 | 0.14 | 0.52 |
| Q12 | crystal_yield | 0.36 | 0.19 | 0.54 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where little new target crystallizes. Q01–Q02: lower-solubility, lower-occlusion S3 is predicted to recover more target with higher purity and fewer fines than S1. Q03–Q04: increasing seed mass should provide more growth area, modestly raise recovery, and suppress secondary nucleation, but distribute growth over more particles and therefore reduce d50. Q05–Q06: the slow ramp should remain feasible; the rapid initial drop should create persistent fines despite the long cold residence, as seen qualitatively in campaign batches 6–7. Q07–Q08: a short final hold should preserve the coarse slow-ramp population, whereas heating to 315 K and rapidly recooling may dissolve recovered product and renucleate fines. Q09–Q10: immediate filtration at 292 K should give almost no seed-excluded recovery; the two-hour hold permits limited additional growth. Q11–Q12: doubling reagent concentration should increase supersaturation and recovery, but also increase impurity occlusion and fines. Intervals are deliberately broad because S0, S1 and S3 were not experimentally screened, the query endpoint is warmer than the campaign conditions, and very long staged cooling and large seed charges are substantial extrapolations; feasibility booleans use the point estimates rather than requiring the full interval to satisfy the limits.

## K2

1. Status of the main claims

**Supported by direct observations**

- **The selected S2/C1 process family can meet both quality constraints.** Batches 1–5 and 8–11 all had purity above 0.98 and fines below 0.50. Batch 8 directly demonstrated recovery 0.553, purity 0.989, and fines 0.275. This supports feasibility, although not solvent or catalyst optimality.
- **Cooling history strongly affects fines.** The slow-cooling batches were generally feasible, whereas batch 6 used a rapid 1,800 s drop and had fines 0.785. Batch 7 added reheating and recooling but still had fines 0.753. The observation is direct; interpreting it as excessive early nucleation that persists through later processing is mechanistic inference.
- **Extreme concentration can destroy particle quality without improving recovery materially.** Batch 12, at 0.010 L solvent, gave recovery 0.554 and purity 1.000 but fines 1.000. By contrast, batches 8–11 at 0.020–0.040 L remained feasible. This directly supports a lower-volume quality boundary in the tested process.
- **C1/S2 at 390 K was adequate for conversion but not highly selective.** Conversion was usually about 0.99–1.00, while selectivity was approximately 0.54–0.58 with appreciable byproduct and degradation signals. Those are direct assay observations.

**Supported only tentatively or with important confounding**

- **A cold hold may increase recovery.** Batch 4, with a 14,400 s hold, measured 0.526 recovery versus 0.511 for otherwise similar batch 2 without the hold. The difference is modest relative to analytical and process variation and was not replicated as a controlled pair.
- **A 0.001 g seed charge is preferable to either 0.010 g or almost no seed.** Batch 2 had better particle results than batch 1, but cooling duration and endpoint also changed. Batch 3 used almost no seed and had similar recovery and fines but smaller measured crystals than batch 2. These observations suggest an intermediate seed charge, but they do not isolate seed causality.
- **Approximately 0.040 L is a useful operating concentration.** Batch 8 had the highest measured feasible recovery, but its exact replicate, batch 11, measured 0.536 rather than 0.553. Batches 9 and 10 at 0.020 and 0.030 L were also close in recovery. The evidence supports a feasible 0.020–0.040 L window more strongly than a precise optimum at 0.040 L.
- **Crystallization rejected reaction impurities.** High crystal purity coexisted with moderate reaction selectivity. Preferential impurity rejection is a plausible interpretation, but separate target and impurity concentrations in the mother liquor were not measured.

**Contradicted or narrowed**

- A simple claim that increasing concentration monotonically improves useful recovery was contradicted. Batches 8–11 showed a recovery plateau with run-to-run variation, while batch 12 crossed into complete fines failure.
- The idea that reheating would readily repair a fine-rich population was contradicted under the tested cycle: batch 7 remained far above the fines limit after reheating and recooling.
- The staged intermediate-temperature schedule was not beneficial in the tested form. Batch 5 produced only 0.510 recovery, fines 0.447, and relatively small crystals.

**Still untested**

- Whether S2 is actually superior to S0, S1, or S3; every campaign batch used S2.
- Whether C1 is superior to C0, C2, or C3.
- The separate effects of seed mass, seed size distribution, agitation, and solvent identity.
- Whether a different annealing temperature or duration could remove fines successfully.
- Whether the observed crystal purity results from equilibrium rejection, kinetic exclusion, washing during filtration, or another partitioning mechanism.

2. One additional experiment

I would repeat the batch-8 formulation and thermal program **without the 14,400 s cold hold**: 0.040 mol reagent, 0.040 L S2, 0.005 mol C1, 390 K for 3,600 s, 0.001 g seed, slow cooling to 250 K over 14,400 s, followed immediately by filtration and final assay. All other actions would match batch 8.

This would distinguish two explanations:

- **Continued cold growth/equilibration:** the hold causes additional target deposition and perhaps ripening.
- **Cooling-path sufficiency:** most recovery and particle selection are already fixed during the slow ramp, and the apparent batch-4 hold benefit was noise or ordinary batch variability.

If continued cold growth is important, I would expect the no-hold run to have lower recovery—roughly around 0.51–0.53 rather than the batch-8/11 range—with purity still high and possibly somewhat more fines or smaller crystals. If the ramp is sufficient, recovery should remain near 0.54–0.55 with particle metrics similar to batches 8 and 11. A result with similar recovery but worse fines would instead suggest that the hold mainly ripens the particle population rather than increasing recovered mass.

3. Least effectively used observation and least reliable prediction

The account used the **intermediate particle-size measurements** least effectively. Particle sizing was performed in most batches before filtration, but the interpretation relied primarily on final-assay particle metrics. Quantitatively comparing the in-process and final particle readings could have separated genuine population evolution from final-assay noise and clarified whether filtration changed the representative slurry measurement. The account also did not fully reconcile cases such as batch 9, which had very low fines but a smaller normalized median size than batch 8.

**Q02 is the least reliable held-out prediction.** It predicts a substantial advantage for S3 over S1 based almost entirely on nominal dossier properties. No campaign experiment used either solvent, and hidden solvent residuals were explicitly possible. Q02 also extrapolates simultaneously to a warmer 278.15 K endpoint, a 0.045 g seed charge, much lower reagent and catalyst loadings, and an exceptionally long staged cooling history. Thus both its absolute estimates and the claimed S3 advantage are much less grounded than predictions based on the observed S2 cooling-rate and concentration effects. Q06 is also uncertain because a very long low-temperature residence might partially erase rapid-cooling effects, but at least its direction is anchored by the fine-rich rapid-cooling outcomes of batches 6 and 7.
