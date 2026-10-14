# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome
The sealed recommendation is batch 12. It used catalyst C1 and solvent S2; 0.0182 mol each of limiting reagent and component, 0.005 mol catalyst, and 0.080 L solvent. The mixture was heated at 350 K for 3,600 s under nitrogen with 600 rpm stirring, seeded with 0.05 g, cooled toward 250 K in two successive 14,400 s crystallization stages, held for 14,400 s at 300 rpm, filtered, and assayed.

Its final observed metrics were crystal yield 0.5195, purity 0.9956, and number fraction below 20 µm of 0.3485. Thus it exceeded both constraints with substantial margin. Batch 11, using the same material pair and temperatures but a 7,200 s final hold, gave yield 0.5167, purity 0.9944, and fines 0.3423, providing near-confirmation of the operating region.

### Reaction mechanism at the observable level
Because the catalyst and solvent identities are deliberately anonymous, the experiments do not support a molecular elementary-step assignment. A useful phenomenological description is

X = 1 − n_R/n_R,0

and

Y_target ≈ X·S_target,

where X is reagent conversion and S_target is effective selectivity to crystallizable target. Overall crystal recovery can then be decomposed as

Y_crystal ≈ Y_target·f_precipitation·f_capture,

where f_precipitation is the fraction of target transferred into solid during cooling and f_capture includes losses during filtration. This decomposition explains why essentially complete conversion did not imply complete crystal recovery.

For batch 12, conversion was reported as 1.000, liquid-stage target yield as 0.5761, and final crystal yield as 0.5195. Thus roughly nine-tenths of the generated target was represented in recovered crystals, while reaction selectivity and byproduct formation imposed the larger remaining ceiling. The byproduct signal was 0.3313 and selectivity 0.5710.

### Material effects
**Catalyst.** In the S0 screen at otherwise matched later-batch loading and history, C1 gave crystal yield 0.4483 and selectivity 0.6195 in batch 2; C2 gave 0.3586 and 0.5218 in batch 3; C3 gave 0.4479 and 0.5955 in batch 4. These observations make C2 inferior under that condition. C1 and C3 were effectively tied on recovery in this small screen, although C1 showed somewhat higher selectivity. Batch 1 is not a clean catalyst comparison because it used a larger reagent/component charge.

A cross-check in S2 favored C1 over C3: batch 6 with C1 gave yield 0.4867, whereas batch 8 with C3 gave 0.4455. Both met the purity and fines constraints. This supports, but does not prove, a C1 advantage because each condition was run once and catalyst-by-solvent interaction was not fully replicated.

**Solvent.** Solvent was the clearest combined reaction/crystallization lever. With C1 and the common 370 K history:

- Batch 2, S0: yield 0.4483, purity 0.9827, fines 0.7682.
- Batch 5, S1: yield 0.4661, purity 0.9791, fines 0.4991.
- Batch 6, S2: yield 0.4867, purity 1.000, fines 0.3400.
- Batch 7, S3: yield 0.3627, purity 0.9706, fines 0.8051.

S2 therefore improved both observed recovery and particle-number quality. Mechanistically, S2 may alter catalyst activity/selectivity, product solubility, the metastable-zone width, or the relative rates of nucleation and growth. The experiments establish the empirical effect but do not distinguish those alternatives.

### Reaction–crystallization coupling
Reaction conditions determine the amount of target, impurity burden, and solution composition presented to crystallization. Crystallization then partitions target and impurities between solid and mother liquor. High final purity—generally about 0.98–1.00 in the promising S2 batches—shows that the solid phase rejected much of the reaction impurity even when liquid-stage selectivity was only about 0.56–0.60.

The coupling is nevertheless important: a catalyst or solvent that raises liquid yield can also change supersaturation and nucleation. This is illustrated by S0 batches, where respectable reaction yield did not ensure acceptable fines. Consequently, optimizing only conversion or HPLC yield would have selected an incomplete process.

A standard qualitative crystallization model is

σ = C/C*(T,solvent) − 1,

B = k_b σ^b,

G = k_g σ^g,

where σ is supersaturation, B is nucleation rate, and G is crystal-growth rate. A solvent or cooling history that causes a large transient σ can produce many fine particles; controlled seeding and residence time can direct solute toward growth on existing surfaces. S2 apparently shifted the effective B/G balance toward fewer fines under the tested protocol.

### Temperature and process-history dependence
At fixed C1/S2 materials and a 278 K crystallization endpoint, reaction temperatures of 350, 370, and 390 K produced similar observed recoveries:

- Batch 9, 350 K: yield 0.4784, fines 0.2896, degradation warning 0.1847.
- Batch 6, 370 K: yield 0.4867, fines 0.3400, degradation warning 0.2425.
- Batch 10, 390 K: yield 0.4800, fines 0.4085, degradation warning 0.2949.

The recovery differences are small relative to single-batch variability, but increasing temperature was accompanied by progressively worse degradation warning and smaller fines margin. I therefore interpret 350 K as the more robust reaction temperature, not as conclusively superior in intrinsic yield.

The crystallization endpoint had a larger observed effect. Batch 9 used the 350 K reaction and a 278 K endpoint, giving yield 0.4784. Batch 11 retained the same main conditions but cooled to 250 K, giving yield 0.5167 while fines remained compliant at 0.3423. Greater low-temperature supersaturation plausibly transferred more target from mother liquor to solid. The pre-test concern was that this would sharply increase nucleation and fines; that alternative was not observed in S2 under seeded cooling.

Extending the final 250 K hold from 7,200 s in batch 11 to 14,400 s in batch 12 changed yield only from 0.5167 to 0.5195. The reported normalized size rose from 0.0828 to 0.1043, corresponding nominally to d50 values of about 21 and 26 µm, while fines remained similar. This direction is consistent with continued growth or ripening, but the changes are not large enough to establish the mechanism confidently.

### Revisions during the campaign
The initial hypothesis was that slow seeded cooling alone would control fines. That was revised after the S0 catalyst screen: batches 1–4 gave fines of approximately 0.53–0.87, so particle quality—not basic reaction feasibility—became the limiting issue.

The solvent screen then revised the model again. S2 repeatedly produced compliant fines in batches 6, 8, 9, 10, 11, and 12, indicating that solvent-controlled crystallization behavior was at least as important as the nominal cooling schedule.

Finally, lowering the endpoint to 250 K had been expected to increase recovery at the risk of more fines. Batches 11 and 12 supported the recovery part but did not show a constraint-breaking fines penalty. The recommended process therefore uses the colder endpoint and a long final hold.

### Uncertainty and unresolved tradeoffs
The batch-11 versus batch-12 yield difference is only 0.0028, smaller than the declared final-assay crystal-yield noise scale of about 0.01. Accordingly, the longer hold is not proven to increase recovery; batch 12 is the highest observed compliant result, while batch 11 should be regarded as near-equivalent evidence. Their fines values differ by only 0.0062, also below the declared fines noise scale of about 0.018.

The main quality/recovery tradeoff remains supersaturation versus particle number: colder operation increased recovery here, but more aggressive cooling, different scale, or altered mixing could still trigger secondary nucleation. The selected recipe has a useful observed fines margin of roughly 0.15 below the 0.50 limit, but robustness was not mapped.

Untested alternatives include reagent/component ratio and concentration, seed size distribution and loading, intermediate seeding temperature, explicit cooling-rate profiles, agitation dependence, longer reaction time, washing or reslurrying the cake, and randomized replication. Polymorph identity, solubility curves, true nucleation kinetics, and catalyst deactivation were not measured. Therefore the mechanistic account is a process-level interpretation of the public observations, not a unique molecular mechanism.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.19 | 0.51 |
| Q01 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q01 | crystal_size | 0.17 | 0.08 | 0.27 |
| Q01 | crystal_yield | 0.4 | 0.26 | 0.53 |
| Q02 | crystal_fines_fraction | 0.66 | 0.48 | 0.83 |
| Q02 | crystal_purity | 0.94 | 0.83 | 0.99 |
| Q02 | crystal_size | 0.1 | 0.035 | 0.19 |
| Q02 | crystal_yield | 0.29 | 0.16 | 0.42 |
| Q03 | crystal_fines_fraction | 0.72 | 0.53 | 0.88 |
| Q03 | crystal_purity | 0.96 | 0.87 | 0.995 |
| Q03 | crystal_size | 0.08 | 0.025 | 0.16 |
| Q03 | crystal_yield | 0.38 | 0.24 | 0.51 |
| Q04 | crystal_fines_fraction | 0.39 | 0.23 | 0.56 |
| Q04 | crystal_purity | 0.97 | 0.89 | 0.998 |
| Q04 | crystal_size | 0.15 | 0.07 | 0.25 |
| Q04 | crystal_yield | 0.39 | 0.25 | 0.52 |
| Q05 | crystal_fines_fraction | 0.4 | 0.24 | 0.57 |
| Q05 | crystal_purity | 0.97 | 0.89 | 0.998 |
| Q05 | crystal_size | 0.15 | 0.07 | 0.25 |
| Q05 | crystal_yield | 0.39 | 0.25 | 0.52 |
| Q06 | crystal_fines_fraction | 0.68 | 0.5 | 0.84 |
| Q06 | crystal_purity | 0.96 | 0.87 | 0.995 |
| Q06 | crystal_size | 0.09 | 0.03 | 0.18 |
| Q06 | crystal_yield | 0.4 | 0.26 | 0.53 |
| Q07 | crystal_fines_fraction | 0.37 | 0.21 | 0.54 |
| Q07 | crystal_purity | 0.97 | 0.89 | 0.998 |
| Q07 | crystal_size | 0.16 | 0.075 | 0.26 |
| Q07 | crystal_yield | 0.4 | 0.26 | 0.53 |
| Q08 | crystal_fines_fraction | 0.3 | 0.15 | 0.48 |
| Q08 | crystal_purity | 0.98 | 0.91 | 1 |
| Q08 | crystal_size | 0.19 | 0.09 | 0.31 |
| Q08 | crystal_yield | 0.36 | 0.22 | 0.5 |
| Q09 | crystal_fines_fraction | 0.43 | 0.24 | 0.64 |
| Q09 | crystal_purity | 0.98 | 0.88 | 1 |
| Q09 | crystal_size | 0.09 | 0.035 | 0.17 |
| Q09 | crystal_yield | 0.015 | 0 | 0.07 |
| Q10 | crystal_fines_fraction | 0.31 | 0.15 | 0.5 |
| Q10 | crystal_purity | 0.97 | 0.88 | 1 |
| Q10 | crystal_size | 0.13 | 0.06 | 0.23 |
| Q10 | crystal_yield | 0.2 | 0.08 | 0.34 |
| Q11 | crystal_fines_fraction | 0.38 | 0.22 | 0.55 |
| Q11 | crystal_purity | 0.97 | 0.89 | 0.998 |
| Q11 | crystal_size | 0.16 | 0.075 | 0.26 |
| Q11 | crystal_yield | 0.39 | 0.25 | 0.52 |
| Q12 | crystal_fines_fraction | 0.55 | 0.37 | 0.72 |
| Q12 | crystal_purity | 0.95 | 0.85 | 0.995 |
| Q12 | crystal_size | 0.12 | 0.05 | 0.22 |
| Q12 | crystal_yield | 0.46 | 0.3 | 0.6 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Paired rankings are more reliable than the absolute levels because these recipes extrapolate beyond the campaign in catalyst loading, concentration, very long cooling histories, and omission of the component used in the campaign. Q01–Q02 follows the observed S1 advantage over S3 in both recovery and fines. Q03–Q04 assigns higher seed loading a lower secondary-nucleation burden. Q05–Q06 treats gradual cooling as favoring growth over the nucleation burst expected from an initial temperature crash. Q07–Q08 allows the reheat cycle to dissolve fines and enlarge survivors, with some recovery loss from incomplete reprecipitation. Q09–Q10 predicts little seed-excluded solid after only 60 seconds, followed by appreciable growth during the added two-hour hold. Q11–Q12 assigns higher loading greater fractional precipitation but also greater supersaturation, fines, and impurity risk. All batches are seeded, so particles are expected even where seed-excluded yield is very low. Intervals are deliberately broad; uncertainty is largest for absolute reaction yield, short-history Q09–Q10, and whether thermal cycling or doubled loading crosses the fines threshold.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C1/S2 is the best tested material combination.** Batch 6 (C1/S2) gave crystal yield 0.4867, purity 1.000, and fines 0.3400. Batch 8 (C3/S2) remained feasible but recovered less, 0.4455. In the solvent screen with C1, S2 also outperformed S0, S1, and S3 overall: batches 2, 5, 6, and 7 gave yields of 0.4483, 0.4661, 0.4867, and 0.3627, respectively. This ranking is observed; attributing it specifically to reaction kinetics, solubility, or nucleation remains interpretation.
- **S2 provided the most reproducible fines control.** Batches 6, 8, 9, 10, 11, and 12 all had fines below 0.50. By contrast, S0 batches 2–4 and S3 batch 7 generally failed the fines constraint. This directly supports an S2-associated process advantage, although catalyst and temperature were not identical across every comparison.
- **The 250 K endpoint improved observed recovery without breaking the fines limit.** Batch 9 used C1/S2, a 350 K reaction, and a 278 K endpoint, giving yield 0.4784 and fines 0.2896. Batch 11 used the same main reaction conditions with a 250 K endpoint, giving yield 0.5167 and fines 0.3423. Batch 12 repeated the colder regime and gave yield 0.5195 and fines 0.3485. The observations support the operating choice; greater low-temperature precipitation is the mechanistic interpretation.
- **Higher reaction temperature did not deliver a clear recovery benefit.** At 350, 370, and 390 K, batches 9, 6, and 10 gave similar yields of 0.4784, 0.4867, and 0.4800. Their degradation warnings increased from 0.1847 to 0.2425 to 0.2949. Thus 350 K had the best observed degradation and fines margin, while the small recovery differences are unresolved.

### Contradicted or revised
- **The original expectation that slow seeded cooling alone would control fines was contradicted.** Despite seeding and extended cooling, S0 batches 1–4 produced final fines of roughly 0.53–0.87. Solvent identity was evidently an essential part of particle control.
- **The concern that lowering the endpoint to 250 K would necessarily create excessive fines was not supported under C1/S2 conditions.** Batches 11 and 12 retained large margins below the 0.50 limit. This does not prove that colder or faster cooling is universally safe.
- **C1 was not clearly superior to C3 in every environment.** In S0, batches 2 and 4 had nearly identical crystal yields, 0.4483 and 0.4479. The C1 preference rests more strongly on the S2 comparison between batches 6 and 8 and on selectivity, not on a universal catalyst ranking.

### Still untested or unresolved
- The molecular identities and elementary reaction pathway remain untested because all materials were anonymous.
- It is unresolved whether S2 acts mainly through reaction selectivity, equilibrium solubility, metastable-zone width, nucleation suppression, or some combination.
- The apparent benefit of extending the 250 K hold is unresolved. Batch 12 exceeded batch 11 by only 0.0028 in yield, below the final-assay noise scale, although its size estimate was larger.
- Seed necessity, seed-size effects, agitation dependence, washing/reslurrying, polymorphism, and scale robustness were not tested.
- Batch 1 cannot cleanly support catalyst comparisons because its reagent/component loading differed from later batches.

## 2. One additional experiment

I would repeat the batch-11 recipe—C1/S2, 350 K reaction, two 14,400 s cooling stages to 250 K, and a 7,200 s final hold—but **omit the 0.05 g seed charge**. I would include an in-situ particle-size measurement before filtration and the normal final assay.

This would distinguish two explanations for the successful particle distribution:

1. **Seed-dominated control:** the added crystals consume supersaturation and suppress primary or secondary nucleation. Without seed, I would expect an induction period followed by a nucleation burst, giving smaller particles, substantially higher fines, and possibly less reproducible recovery. Purity might remain high.
2. **S2-dominated control:** S2 intrinsically provides a broad metastable region or favorable growth-to-nucleation ratio. If this dominates, the unseeded batch should still produce fines below 0.50 with recovery reasonably close to batch 11, although particle size and induction time could change.

A third possible outcome—little or no crystallization—would show that the successful S2 process depends on heterogeneous nucleation from the seed rather than merely on favorable growth kinetics. This experiment is preferable to another exact replicate because it targets the largest unresolved causal element in the recommended crystallization mechanism.

## 3. Least-used observation and least-reliable prediction

The account used the **intermediate particle-size observations** least effectively. For example, batch 1 measured fines of about 0.558 and size 0.056 before final closeout, whereas its final assay reported fines about 0.534 and size 0.070. I relied mainly on final-assay CSD values and did not systematically analyze such paired readings. They could have helped separate true filtration/history effects from particle-instrument and final-assay noise, and could have tested whether filtration selectively altered the representative particle population.

The least reliable held-out prediction is **Q09**. It contains only 60 seconds of cooling to 292 K before filtration, so recovered target solid may be nearly absent and the measured particle population may be dominated by the deliberately added seed. The campaign contained no comparable ultrashort crystallization. Consequently, crystal purity, size, and fines depend on how seed-only or seed-dominated solids are represented, while crystal yield explicitly excludes seed mass. The prediction that particles remain present but seed-excluded yield is near zero is mechanistically plausible, yet its quality-feasibility classification is much less secure than predictions for mature crystal slurries.
