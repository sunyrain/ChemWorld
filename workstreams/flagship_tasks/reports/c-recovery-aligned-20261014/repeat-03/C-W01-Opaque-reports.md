# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Scope
The catalysts (C0–C3) and solvents (S0–S3) are anonymous benchmark materials, so the evidence supports process-level mechanisms, not claims about molecular identities, functional groups, polymorphs, or real substances.

### 1. Reaction network and material effects
A useful minimal reaction model is parallel target and impurity formation, with possible subsequent target degradation:

R → P, rate kP(C,S,T); R → I, rate kI(C,S,T); P → D, rate kD(C,S,T).

For an idealized constant-temperature batch,

X ≈ 1 − exp[−(kP+kI)t], and target yield ≈ X·kP/(kP+kI),

before accounting for degradation. The experiments indicate that conversion was generally near completion, while selectivity—not conversion—limited the available target-product pool. For example, batch 1 (C0/S0, 360 K, 1 h) had HPLC conversion 1.00, selectivity 0.649, and reaction yield 0.643. Batch 3 (C2/S1) also had conversion about 0.998 but much lower selectivity and yield, about 0.413–0.414. Thus longer reaction alone would not necessarily help: once conversion is nearly saturated, extra exposure can mainly permit impurity formation or degradation.

Catalyst effects were clearest within S2 under the long seeded cooling program. Final-assay reaction yields/crystal yields were approximately 0.591/0.474 for C1 (batch 7), 0.517/0.412 for C2 (batch 8), and 0.572/0.456 for C3 (batch 9). C1 therefore provided the largest productive pool and the greatest recovered crystal yield in that comparison. C0/S2 in batch 6 gave crystal yield 0.469, but its different cooling endpoint and duration prevent a clean catalyst ranking against batches 7–9.

Solvent affected both reaction selectivity and crystallization much more strongly than a simple inert-diluent model would predict. S0 supported relatively good reaction yield with C0 or C1, but consistently produced an unacceptable fine-particle population. S2 gave the best overall reaction/solid-form compromise. Because the initial solvent screen changed catalyst and solvent together in several batches, independent solvent coefficients cannot be inferred from those diagonal comparisons.

### 2. Reaction–crystallization coupling
The overall reported crystal yield is

Ycr = n(target in recovered solid, excluding seed)/n(initial reagent).

It is not merely crystallization-stage recovery. A useful diagnostic, although not an official metric, is

ηapparent ≈ Ycr/Yreaction,

which estimates how much of the reaction-stage target appeared in the recovered solid. It was about 0.77 in batch 1, 0.80 in batch 7, 0.85 in batch 11, and 0.89 in batch 12. These ratios are approximate because reaction yield and crystal yield are separate noisy channels observed at different process stages, but their progression supports improved recovery at higher concentration.

Crystallization also acted as a strong purification step. Reaction selectivities were only about 0.52–0.65 in many useful batches, yet recovered-crystal purity was generally 0.98–1.00. This is consistent with preferential incorporation of target product and rejection of reaction impurities into the mother liquor. Consequently, a moderately selective reaction could still furnish highly pure crystals, but low reaction selectivity reduced the maximum recoverable target mass.

### 3. Supersaturation, nucleation, and growth
A suitable qualitative description uses supersaturation

σ = (CP − C*(S,T))/C*(S,T),

where C* is the solvent- and temperature-dependent target solubility. Crystal growth often scales as G ∝ σ^g, whereas primary nucleation can rise much more steeply, for example

J ∝ exp[−B/(ln(1+σ))²].

A rapid or deep increase in σ can therefore create many new small particles before existing seeds consume the supersaturation. Slow staged cooling and seeding instead provide existing surface area and time for growth, reducing the nucleation burst. Solvent can change C*, interfacial energy, aggregation, and impurity adsorption, so it can change particle-size distribution even when reaction conversion is similar.

The observations support this framework but do not identify which microscopic solvent effect dominates. Batch 1, using S0 and a relatively shorter cooling history, had fines 0.901 and normalized size 0.057. Batch 2 used S0 with slower staged cooling; normalized size increased to 0.093, but fines remained 0.893. Thus slow cooling enlarged part of the population without eliminating the fine tail, possibly producing a broad or bimodal distribution.

A stronger process-history comparison is C3/S2. Batch 4 used 2 h cooling stages and gave crystal yield 0.457, fines 0.520, and CSD quality 0.652. Batch 9 used 4 h stages with a slightly warmer final endpoint and gave essentially unchanged yield, 0.456, but fines fell to 0.481 and CSD quality rose to 0.665. This indicates that time spent along the supersaturation trajectory, rather than final temperature alone, can determine whether the fines constraint is met. However, normalized median size decreased from 0.075 to 0.057, so “fewer fines” did not simply mean “larger median particles”; distribution shape and measurement noise matter.

### 4. Concentration and process-history dependence
Within C1/S2, reducing solvent volume increased overall crystal recovery:

- Batch 7: 0.08 L S2, long staged cooling; crystal yield 0.474, purity 0.982, fines 0.456.
- Batch 11: 0.05 L S2; crystal yield 0.490, purity 1.000, fines 0.481.
- Batch 12: 0.03 L S2 with additional 10 K cooling stages to 280 K; crystal yield 0.516, purity 1.000, fines 0.487.

The mechanistic interpretation is that reduced solvent volume increased product concentration and the fraction driven out of solution. In batch 12, the long sequence through 320, 310, 300, 290, and 280 K helped distribute that larger supersaturation load over time rather than applying it as one abrupt quench. Its normalized crystal-size value of 0.0978 corresponds to a number-weighted d50 of approximately 24.4 µm.

This concentration series is not a perfectly controlled experiment: batch 12 had more cooling stages than batches 7 and 11. The yield improvement may therefore combine concentration, endpoint, and residence-time effects. Solvent loss during sampling was small, but HPLC sampling also means batches were not strictly untouched before isolation.

Reaction-temperature evidence did not justify a strong optimum claim. Batch 7 used 360 K and produced crystal yield 0.474; batch 10 used 340 K and produced 0.456. Their crystallization histories also differed slightly. The lower-temperature batch did not improve observed selectivity or recovery, but the comparison cannot separate reaction temperature from later history with precision.

### 5. Revisions to the working interpretation
The initial expectation was that catalyst and reaction conditions would dominate performance and that generally slower cooling would cure fines. The first five batches revised that view:

1. Near-complete conversion was common, making selectivity and degradation more important than further conversion.
2. S0 remained near 90% fines despite slower cooling, showing that cooling rate alone could not overcome an unfavorable material/solid-form combination.
3. S2 moved fines close to the specification and retained useful recovery, shifting the program toward an S2 catalyst screen.
4. The long S2 cooling histories in batches 7–9 crossed the fines threshold, establishing strong process-history dependence.
5. Batches 11–12 then showed that concentration could increase recovery while slow staged cooling largely preserved particle quality.

### 6. Uncertainty and unresolved tradeoffs
The final assay is noisy: the stated standard deviations include approximately 0.010 for crystal yield, 0.010 for purity, 0.018 for fines fraction, and 0.025 for normalized size, in addition to process uncertainty. Every recipe was assayed only once. Small batch-to-batch differences should therefore not be interpreted as precise causal effect sizes.

Purity is not the limiting uncertainty: the leading batches were roughly 0.98–1.00, far above the 0.80 requirement. The unresolved tradeoff is recovery versus fines. Increasing concentration from batches 7 to 11 to 12 raised measured recovery but moved fines from 0.456 to 0.481 to 0.487, progressively closer to the 0.50 limit. Batch 12 passed as observed and had the highest eligible recovery, but its 0.013 margin is smaller than the nominal fines measurement standard deviation. Its superiority in yield over batch 11, about 0.026, is also based on a single comparison confounded by cooling history.

Untested alternatives include holding concentration constant while independently varying each cooling stage, testing intermediate solvent volumes, varying seed mass independently, applying a controlled ripening or temperature-cycle step, and replicating the leading recipes. These could determine whether the apparent recovery–fines tension is fundamental or can be relaxed through better supersaturation management. The existing evidence supports the recommended batch as the best observed result, but not as a fully mapped or statistically replicated global optimum.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.21 | 0.48 |
| Q01 | crystal_purity | 0.98 | 0.93 | 1 |
| Q01 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q01 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q02 | crystal_fines_fraction | 0.3 | 0.18 | 0.44 |
| Q02 | crystal_purity | 0.97 | 0.91 | 1 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.2 |
| Q02 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q03 | crystal_fines_fraction | 0.56 | 0.4 | 0.71 |
| Q03 | crystal_purity | 0.98 | 0.93 | 1 |
| Q03 | crystal_size | 0.18 | 0.1 | 0.27 |
| Q03 | crystal_yield | 0.4 | 0.3 | 0.51 |
| Q04 | crystal_fines_fraction | 0.43 | 0.29 | 0.57 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.12 | 0.06 | 0.19 |
| Q04 | crystal_yield | 0.41 | 0.31 | 0.52 |
| Q05 | crystal_fines_fraction | 0.39 | 0.26 | 0.53 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q05 | crystal_yield | 0.42 | 0.33 | 0.52 |
| Q06 | crystal_fines_fraction | 0.69 | 0.54 | 0.82 |
| Q06 | crystal_purity | 0.97 | 0.91 | 1 |
| Q06 | crystal_size | 0.06 | 0.02 | 0.12 |
| Q06 | crystal_yield | 0.43 | 0.33 | 0.53 |
| Q07 | crystal_fines_fraction | 0.37 | 0.24 | 0.51 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.14 | 0.07 | 0.22 |
| Q07 | crystal_yield | 0.42 | 0.32 | 0.52 |
| Q08 | crystal_fines_fraction | 0.65 | 0.48 | 0.79 |
| Q08 | crystal_purity | 0.96 | 0.88 | 1 |
| Q08 | crystal_size | 0.07 | 0.02 | 0.14 |
| Q08 | crystal_yield | 0.38 | 0.27 | 0.49 |
| Q09 | crystal_fines_fraction | 0.82 | 0.67 | 0.93 |
| Q09 | crystal_purity | 0.96 | 0.86 | 1 |
| Q09 | crystal_size | 0.05 | 0.01 | 0.11 |
| Q09 | crystal_yield | 0.02 | 0 | 0.07 |
| Q10 | crystal_fines_fraction | 0.65 | 0.48 | 0.79 |
| Q10 | crystal_purity | 0.97 | 0.89 | 1 |
| Q10 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q10 | crystal_yield | 0.14 | 0.06 | 0.24 |
| Q11 | crystal_fines_fraction | 0.4 | 0.27 | 0.54 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.13 | 0.07 | 0.2 |
| Q11 | crystal_yield | 0.42 | 0.32 | 0.52 |
| Q12 | crystal_fines_fraction | 0.54 | 0.39 | 0.68 |
| Q12 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q12 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q12 | crystal_yield | 0.4 | 0.28 | 0.52 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where seed-excluded target recovery is small. Q01–Q02: S3 is predicted to recover more target and form slightly fewer fines than S1, but solvent effects remain catalyst-dependent. Q03–Q04: the larger seed charge should suppress secondary nucleation and lower fines, while the small seed charge may yield a larger median size but a broader fine-rich distribution. Q05–Q06: gradual cooling should consume supersaturation by growth; the rapid drop creates a nucleation burst that a long cold hold may not fully erase, although final recovery can be similar. Q07–Q08: reheating to 315 K may dissolve much of the established population, and the subsequent one-hour recooling is expected to regenerate fines and incompletely restore recovery. Q09–Q10: an additional two-hour growth period should materially increase seed-excluded yield and size, but at 292 K it is unlikely to cure the fine-rich distribution. Q11–Q12: doubling reagent at fixed catalyst raises supersaturation but halves catalyst loading relative to reagent; higher recovery driving force is therefore offset by less complete/selective reaction and more nucleation, leaving fractional yield similar or lower and fines higher. Intervals are deliberately broad because these recipes extrapolate to 385 K, much lower scale, unusually long cooling histories, and unreplicated seed/load regimes; feasibility flags use point estimates, and several fine-fraction intervals cross the 0.50 boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Conversion was usually nearly complete, while selectivity limited target formation.** Batch 1 had HPLC conversion 1.00 but selectivity 0.649; batch 3 had conversion about 0.998 but selectivity about 0.413. The interpretation that parallel impurity formation mattered more than additional conversion is supported, although the proposed rate equations remain conceptual rather than fitted.
- **Crystallization strongly purified the reaction mixture.** Despite reaction selectivities around 0.52–0.65, batches 7–12 generally produced crystal purity near 0.98–1.00. Preferential target crystallization is an interpretation; high final purity is the direct observation.
- **S0 was associated with a persistent fines problem.** Batches 1 and 2 gave fines of 0.901 and 0.893 despite different catalyst, seed dose, and cooling history. This directly contradicts the initial expectation that slower cooling alone would cure fines.
- **S2 plus long staged cooling was the best observed quality regime.** Batches 7–9 all met the purity and fines specifications, with fines of 0.456, 0.483, and 0.481. Batch 4 versus batch 9 is especially informative: both used C3/S2 and had nearly identical crystal yield, about 0.457 versus 0.456, but extending the staged cooling reduced fines from 0.520 to 0.481.
- **C1 gave the highest recovery in the comparable long-cooling S2 catalyst screen.** Batches 7, 8, and 9 gave crystal yields of 0.474, 0.412, and 0.456 for C1, C2, and C3. This supports a catalyst effect within that tested scope, not a universal catalyst ranking.
- **Higher concentration was associated with higher recovery.** In the C1/S2 sequence, batches 7, 11, and 12 used 0.08, 0.05, and 0.03 L solvent and gave crystal yields of 0.474, 0.490, and 0.516. The association is direct; attributing it solely to concentration is not, because batch 12 also used more cooling stages.

### Contradicted or substantially revised
- **“Slower cooling produces both fewer fines and a larger median particle size” was too simple.** Batch 4 to batch 9 reduced fines, but normalized size decreased from 0.075 to 0.057. Fines fraction and d50 describe different aspects of the distribution and need not move together.
- **Reaction conditions were not the sole dominant control.** The campaign began with that emphasis, but solvent and thermal history determined whether the fines constraint was crossed.
- **Lower reaction temperature was not shown to improve performance.** Batch 10 at 340 K gave crystal yield 0.456 versus 0.474 for batch 7 at 360 K, with no convincing selectivity advantage. The comparison is not perfectly controlled, so this is absence of support rather than proof that 340 K is intrinsically worse.

### Still untested
- The molecular reasons for the solvent effects—solubility, interfacial energy, polymorph selection, impurity adsorption, or aggregation—remain unknown.
- Catalyst–solvent interactions were not mapped factorially; several early solvent comparisons changed catalyst simultaneously.
- Seed mass was never varied while all other conditions were held fixed.
- The apparent concentration effect is confounded with cooling schedule, and none of the leading batches was replicated.
- Post-crystallization thermal cycling, quantitative nucleation/growth laws, and a true global optimum remain untested.
- The approximate ratio crystal_yield/reaction_yield is only a diagnostic, not a validated crystallization-stage recovery measurement.

## 2. One additional experiment

I would run **C1/S2 with 0.05 L solvent, 0.04 mol reagent, 0.005 mol catalyst, and the same 360 K reaction used in batches 11–12, but apply the exact five-stage cooling history of batch 12: seed at 330 K, then 320, 310, 300, 290, and 280 K for 4 h per stage**. This creates the missing condition “batch-11 concentration plus batch-12 cooling.”

It would distinguish three explanations:

1. **Cooling-history explanation:** If the new batch approaches batch 12—yield near 0.516 with fines near 0.487—the extra cooling stages, rather than concentration, explain most of the improvement.
2. **Concentration explanation:** If it remains close to batch 11—yield near 0.490 and fines near 0.481—the lower solvent volume in batch 12 is the primary cause.
3. **Combined or stochastic explanation:** An intermediate result would support contributions from both factors. A large departure, especially fines above 0.50, would indicate substantial batch-to-batch nucleation variability and weaken confidence in all single-run comparisons.

This design is more discriminating than simply repeating batch 12, although replication would still be the next priority afterward.

## 3. Least effectively used evidence and least reliable held-out prediction

The account used the **degradation-warning observations** least effectively. It invoked degradation in the reaction network but did not systematically reconcile the measured warnings—for example, approximately 0.096 in batch 8 versus 0.185–0.188 in batches 7 and 9 under nominally similar reaction temperatures. Catalyst, solvent, and downstream history may influence this channel, but the campaign did not isolate them. Consequently, the report's discussion of thermal degradation was plausible rather than quantitatively demonstrated, which is important because the held-out recipes used 385 K.

The least reliable held-out prediction is **Q08**, the reheating-cycle case. No campaign batch reheated an established low-temperature crystal population to 315 K and then recooled it rapidly. I predicted that dissolution followed by rapid renucleation would lower recovery and raise fines, but the competing outcome—selective dissolution of fines followed by growth on surviving crystals—is also physically plausible. The result depends on an unmeasured solubility curve, whether seeds survive at 315 K, dissolution kinetics, and the balance between secondary nucleation and regrowth. Q08 therefore extrapolates beyond the experimental support more strongly than the solvent, seed, or gradual-versus-rapid cooling comparisons.
