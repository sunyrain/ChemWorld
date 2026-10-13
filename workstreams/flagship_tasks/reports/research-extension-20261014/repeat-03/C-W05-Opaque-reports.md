# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Process and principal observation

The successful process combined 0.040 mol reagent, 0.005 mol catalyst C2, 0.080 L solvent S1, a 360 K reaction period of 3,600 s under nitrogen, 0.050 g seed, and a controlled 14,400 s cooling step. Batch 8, cooled to 260 K, gave the recommended balance: seed-excluded crystal recovery 0.4797, crystal purity 0.9777, fines number fraction 0.4172, normalized crystal size 0.1094, and CSD quality 0.7036.

“Crystal recovery” here is the recovered target product divided by target product present before separation; it excludes seed mass and is not the overall yield from the original reagent. Batch 8’s reaction yield was 0.5417, so their product (about 0.260) is only a rough overall-yield indicator, not a separately calibrated mass yield.

### 2. Reaction mechanism and material effects

A useful minimal reaction network is parallel target and byproduct formation, followed by possible target degradation:

- R → P, rate kP(C,S,T)
- R → B, rate kB(C,S,T)
- P → D, rate kD(S,T)

with Arrhenius-type rate constants, k = A exp(−Ea/RT). Catalyst and solvent can therefore change conversion, selectivity, and degradation independently.

**Observation:** Conversion was essentially complete in all developed recipes, generally about 0.99–1.00. Material combinations nevertheless differed in selectivity and reaction yield. C0/S0 in batch 1 gave selectivity 0.610 and reaction yield 0.608; C1/S0 in batch 2 gave 0.591 and 0.580. The C2/S1 series generally gave selectivity about 0.52–0.56 and reaction yield about 0.53–0.55. C2/S2 in batch 11 was lower, at selectivity 0.480 and reaction yield 0.460.

**Interpretation:** Near-complete conversion did not imply equally favorable chemistry. Differences in the relative target/byproduct rate constants remained important after reagent depletion. Solvent S1 was particularly valuable downstream even though its observed reaction selectivity was not the highest.

**Limitation:** Catalyst and solvent were not independently crossed in a full factorial design. Batches 1–2 used S0 with C0 or C1 and different crystallization histories, whereas batches 3–12 mostly used C2. Thus the data do not establish a standalone catalyst ranking. The apparent reaction differences could be caused by catalyst, solvent, or their interaction.

### 3. Reaction–crystallization coupling

Reaction composition set the amount and impurity environment entering crystallization. Crystallization then acted as both a recovery and purification step.

**Observation:** Despite only moderate reaction selectivity, feasible S1 batches produced crystals with purity approximately 0.976–1.000. For example, batch 8 had reaction selectivity 0.550 but crystal purity 0.978. This indicates strong rejection of byproducts or degradation products from the recovered solid. The S0 batches also had high crystal purity, about 0.984–0.986, despite poor particle quality.

**Interpretation:** Impurity exclusion was effective, so the principal optimization conflict was not purity versus recovery but recovery versus particle-number fines. Nevertheless, impurities may have influenced nucleation, growth, or agglomeration even when they were excluded from the final lattice. This is a plausible reason solvent and reaction composition affected particle distributions so strongly.

### 4. Crystallization mechanism

A conventional supersaturation framework is consistent with the observations. Define

S = (c − c*(T,S))/(c*(T,S)),

where c* is the solvent- and temperature-dependent equilibrium solubility. A qualitative primary-nucleation relation is

J ≈ kJ exp[−B/(ln(1+S))²],

whereas crystal growth may be represented as

G ≈ kG S^g.

Cooling raises supersaturation by lowering c*. Excessively rapid or deep passage through the metastable region can make nucleation dominate growth, producing many particles below 20 µm. Seeding provides existing surface area and can direct supersaturation into growth instead of new nuclei.

**Material effect:** S0 gave high recovery but very poor number-based particle quality. Batch 1 recovered 0.450 with fines 0.962, and batch 2 recovered 0.451 with fines 0.981. In contrast, S1 under slow cooling gave fines near 0.42–0.44 over much of the investigated range. This suggests that S1 altered solubility, interfacial energy, impurity adsorption, or growth kinetics so that seeded growth could compete successfully with secondary nucleation. The experiment does not distinguish these alternatives.

S2 in batch 11 gave especially low fines, 0.370, and high purity, 0.992, but recovery was only 0.392. This is consistent with either greater low-temperature solubility or weaker supersaturation generation: particle quality improved at the expense of recovery.

### 5. Endpoint-temperature relationship in S1

The controlled C2/S1 series showed a clear recovery trend:

- Batch 3, 300 K: recovery 0.3498, fines 0.4363
- Batch 4, 295 K: recovery 0.3822, fines 0.4448
- Batch 5, 290 K: recovery 0.3936, fines 0.4332
- Batch 6, 280 K: recovery 0.4320, fines 0.4434
- Batch 7, 270 K: recovery 0.4585, fines 0.4328
- Batch 8, 260 K: recovery 0.4797, fines 0.4172
- Batch 9, 250 K: recovery 0.4828, fines 0.4858

**Interpretation:** Lowering the endpoint from 300 to 260 K progressively reduced dissolved product and increased recovery without triggering a nucleation burst, presumably because the 14,400 s trajectory kept supersaturation sufficiently controlled. Below about 260 K, recovery approached a plateau while fines increased toward the constraint. This is the unresolved quality/recovery boundary.

The exact curve should not be over-interpreted: adjacent recovery differences are often comparable to the final-assay crystal-yield standard deviation of about 0.01. The full 300-to-260 K increase is persuasive, but individual 5–10 K increments are not all independently resolved.

### 6. Process-history dependence

Cooling endpoint alone was insufficient to describe the result.

Batch 10 used two stages—cooling first to 300 K over 7,200 s and then to 250 K over 14,400 s. It gave recovery 0.4839, purity 0.9757, and fines 0.4839. This was nominally the highest observed recovery, but only 0.0042 above batch 8, less than the assay noise. The longer two-stage history therefore demonstrated no resolved recovery advantage and approached the fines limit more closely.

Batch 12 used a single 14,400 s step to 255 K and gave recovery 0.4722 and fines 0.4570. Batch 9 at 250 K gave 0.4828 recovery and 0.4858 fines. These results reinforce that small endpoint changes near the boundary produce differences comparable to run-to-run or measurement uncertainty.

Batch 1 also illustrates controller-history sensitivity: after cooling, its subsequent wait occurred while the earlier hot control target remained active, allowing reheating toward 294 K. It therefore cannot be treated as a clean endpoint-temperature comparison. Batch 2 reset the cold target before its hold yet still produced very high fines, supporting a genuine adverse S0 effect rather than attributing all S0 behavior to batch 1’s control history.

### 7. Revision of the working model

The initial expectation was that moderate seeding, slower cooling, and a cold growth hold would generally reduce fines. The experiments narrowed that claim substantially:

1. Seeding and slow cooling were not sufficient in S0; batches 1–2 remained dominated by fines.
2. Solvent identity was therefore elevated from a secondary variable to the principal particle-quality variable.
3. Within S1, slow single-stage cooling gave a broad feasible region and showed that deeper cooling could increase recovery without degrading fines until approximately 250–255 K.
4. A two-stage trajectory did not deliver a resolved advantage over the simpler 260 K process.

Thus the final interpretation is not “cool as deeply as possible,” but “use a solvent/process combination that supports seeded growth, then cool only until marginal recovery gains cease to justify the shrinking fines margin.”

### 8. Uncertainty and unresolved alternatives

Final-assay standard deviations were approximately 0.01 for crystal recovery, 0.01 for purity, 0.018 for fines and CSD quality, and 0.025 for normalized size. Consequently, batches 8–10 are indistinguishable in recovery on a single-run basis. Batch 8’s fines value, however, is materially farther below 0.50 than those of batches 9–10, which motivated retaining batch 8 as the recommendation.

No replicate batches were run, so process variability is not separated from measurement noise. Untested alternatives include solvent mixtures, independent catalyst-by-solvent factorial screening, lower catalyst loading, shorter or cooler reaction stages, different seeding temperature or seed size distribution, agitation changes during cooling, controlled ripening holds, washing, and partial dissolution/recrystallization cycles. Any of these could alter the recovery–fines frontier. In particular, a replicated comparison of the 260 K single-stage and 250 K two-stage processes would be needed before claiming that the latter truly improves recovery without violating the fines constraint.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.19 | 0.49 |
| Q01 | crystal_purity | 0.98 | 0.93 | 1 |
| Q01 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q01 | crystal_yield | 0.3 | 0.15 | 0.45 |
| Q02 | crystal_fines_fraction | 0.45 | 0.18 | 0.75 |
| Q02 | crystal_purity | 0.96 | 0.84 | 1 |
| Q02 | crystal_size | 0.13 | 0.04 | 0.28 |
| Q02 | crystal_yield | 0.25 | 0.05 | 0.48 |
| Q03 | crystal_fines_fraction | 0.67 | 0.47 | 0.86 |
| Q03 | crystal_purity | 0.97 | 0.89 | 1 |
| Q03 | crystal_size | 0.08 | 0.02 | 0.18 |
| Q03 | crystal_yield | 0.27 | 0.11 | 0.43 |
| Q04 | crystal_fines_fraction | 0.36 | 0.2 | 0.52 |
| Q04 | crystal_purity | 0.98 | 0.92 | 1 |
| Q04 | crystal_size | 0.16 | 0.07 | 0.29 |
| Q04 | crystal_yield | 0.28 | 0.13 | 0.43 |
| Q05 | crystal_fines_fraction | 0.33 | 0.18 | 0.48 |
| Q05 | crystal_purity | 0.98 | 0.92 | 1 |
| Q05 | crystal_size | 0.18 | 0.08 | 0.31 |
| Q05 | crystal_yield | 0.29 | 0.14 | 0.44 |
| Q06 | crystal_fines_fraction | 0.7 | 0.51 | 0.87 |
| Q06 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q06 | crystal_size | 0.08 | 0.02 | 0.18 |
| Q06 | crystal_yield | 0.3 | 0.14 | 0.46 |
| Q07 | crystal_fines_fraction | 0.3 | 0.16 | 0.45 |
| Q07 | crystal_purity | 0.98 | 0.92 | 1 |
| Q07 | crystal_size | 0.19 | 0.09 | 0.33 |
| Q07 | crystal_yield | 0.3 | 0.15 | 0.45 |
| Q08 | crystal_fines_fraction | 0.25 | 0.11 | 0.43 |
| Q08 | crystal_purity | 0.98 | 0.91 | 1 |
| Q08 | crystal_size | 0.23 | 0.11 | 0.39 |
| Q08 | crystal_yield | 0.28 | 0.12 | 0.44 |
| Q09 | crystal_fines_fraction | 0.58 | 0.35 | 0.79 |
| Q09 | crystal_purity | 0.97 | 0.86 | 1 |
| Q09 | crystal_size | 0.07 | 0.02 | 0.16 |
| Q09 | crystal_yield | 0.03 | 0 | 0.11 |
| Q10 | crystal_fines_fraction | 0.47 | 0.28 | 0.67 |
| Q10 | crystal_purity | 0.98 | 0.89 | 1 |
| Q10 | crystal_size | 0.11 | 0.04 | 0.22 |
| Q10 | crystal_yield | 0.12 | 0.03 | 0.25 |
| Q11 | crystal_fines_fraction | 0.32 | 0.17 | 0.48 |
| Q11 | crystal_purity | 0.98 | 0.92 | 1 |
| Q11 | crystal_size | 0.18 | 0.08 | 0.32 |
| Q11 | crystal_yield | 0.29 | 0.14 | 0.44 |
| Q12 | crystal_fines_fraction | 0.46 | 0.29 | 0.64 |
| Q12 | crystal_purity | 0.96 | 0.87 | 1 |
| Q12 | crystal_size | 0.14 | 0.06 | 0.27 |
| Q12 | crystal_yield | 0.51 | 0.35 | 0.66 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are latent, noise-free process predictions; the 80% intervals primarily reflect extrapolation from the sealed campaign rather than final-assay noise. Q01–Q02 isolates solvent: S1 is supported by the campaign, whereas S3 was untested, so Q02 is substantially less certain. Q03–Q04 predicts that the larger seed charge diverts supersaturation toward growth and lowers fines, with little direct effect on equilibrium recovery. Q05–Q06 contrasts gradual cooling with an initial thermal shock: similar long-time recovery is expected, but the rapid drop should cause a nucleation burst and persistent fines. Q07–Q08 assigns the 315 K anneal a partial-dissolution/Ostwald-ripening benefit—larger particles and fewer fines—while allowing a small recovery penalty; rapid renucleation after reheating remains an alternative. Q09–Q10 predicts little deposition after only 60 seconds at 292 K, but appreciable seeded growth during the added hold. Q11–Q12 predicts that doubling concentration raises supersaturation and recovery, while narrowing the fines and purity margins. All recipes contain seed crystals, so particles are expected even when seed-excluded product recovery is small. Feasibility labels use the point estimates; Q02, Q04, Q10 and Q12 remain close or uncertain enough that their intervals cross the fines or purity limits.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **A slow, seeded C2/S1 process provides a feasible crystallization window.** Batches 3–8 all had purity above 0.97 and fines below 0.45 while using slow 14,400 s cooling. Batch 8 achieved recovery 0.4797, purity 0.9777 and fines 0.4172.
- **Lowering the S1 endpoint from 300 to 260 K increased recovery.** Recovery rose from 0.3498 in batch 3 (300 K) to 0.4797 in batch 8 (260 K). The full-range change exceeds the approximately 0.01 assay noise, although individual adjacent differences are not all resolved.
- **Further cooling gave diminishing recovery and reduced fines margin.** Batch 9 at 250 K gave recovery 0.4828 but fines 0.4858. Batch 10’s two-stage trajectory gave recovery 0.4839 and fines 0.4839. Neither showed a convincing recovery advantage over batch 8 given assay uncertainty.
- **Crystallization strongly purified the target.** For example, batch 8 had reaction selectivity 0.550 but crystal purity 0.978. High crystal purity was also observed in batches 1–2 and 11, so impurity rejection is an observation rather than merely a mechanistic assumption.
- **S0 was associated with very poor particle quality in the tested histories.** Batches 1 and 2 had fines of 0.962 and 0.981, respectively, despite recoveries near 0.45. Batch 2 retained high fines even after resetting the cold controller, so batch 1’s reheating error cannot explain the entire S0 result.
- **S2 traded recovery for particle quality in the one tested recipe.** Batch 11 gave lower recovery, 0.3917, but fines of 0.3704 and purity of 0.9923.

### Interpretations that remain only partly supported

- **The proposed supersaturation/nucleation explanation**—S1 favoring seeded growth while S0 favors nucleation—is consistent with the recovery and fines data, but nucleation rate, solubility and growth rate were never measured independently.
- **A solvent effect is likely, but its direct magnitude is unresolved.** S0 and S1 were not compared with the same catalyst and thermal history. Catalyst, reaction impurity profile and cooling history remain confounders.
- **The two-stage process offers no useful benefit** is supported only by one batch, batch 10. Its nominal recovery was highest, but the difference from batch 8 was below measurement resolution.
- **The apparent recovery plateau below 260 K** is plausible from batches 8–10 and 12, but replication is needed because the differences are comparable to assay noise.

### Contradicted or revised claims

- The initial broad claim that **seeding plus slow cooling would generally suppress fines** was contradicted by S0 batches 1–2. The revised claim is conditional on material identity and thermal trajectory.
- The expectation that **deeper cooling necessarily worsens fines** was contradicted over the S1 range from 300 to 260 K: recovery increased while fines remained roughly 0.42–0.44. Deterioration appeared only near 250–255 K.
- There was no evidence that **near-complete conversion guarantees favorable reaction yield or selectivity**. Conversion was about 0.99–1.00, while selectivity still varied materially.

### Still untested

Independent catalyst effects, S3 behavior, solvent mixtures, seed-size distribution, unseeded operation, agitation effects during cooling, replicate variability, washing, and deliberate annealing/ripening remain untested. The concentration, seed-loading, cooling-shock, annealing and short-hold effects appearing in Q03–Q12 were predictions, not observations.

## 2. One additional experiment

I would repeat the complete batch-8 recipe but replace S1 with S0, retaining C2, all charges, the 360 K reaction, 0.050 g seed, and the single 14,400 s cooling step to 260 K. I would include HPLC immediately before crystallization and particle sizing immediately before filtration, followed by the final assay.

This matched experiment would distinguish three explanations:

1. **Direct solvent control of nucleation/growth.** If S0 again produced very high fines—approximately 0.8–1.0—despite the batch-8 history, the solvent association would become strong evidence for a direct solubility, interfacial-energy or growth-kinetic effect.
2. **Thermal-history explanation.** If S0 instead gave fines near the batch-8 value of about 0.42, the earlier S0 failures would be attributable mainly to their faster cooling, holds or controller history rather than solvent identity.
3. **Reaction-composition-mediated solvent effect.** If pre-crystallization HPLC showed a substantially different impurity profile and the particle result changed with it, solvent could be acting indirectly through reaction composition. Similar HPLC composition but very different fines would favor a direct crystallization-stage effect.

Intermediate particle sizing would also show whether fines were already present before filtration; a low pre-filter fines value followed by high final-assay fines would instead implicate filtration or post-growth handling.

## 3. Least effectively used observation and least reliable prediction

The account used the **batch-1 in-process particle-size measurement** least effectively. Before filtration it already showed fines of about 0.986, close to the final-assay value of 0.962. That comparison could have been used more explicitly to localize the failure to crystallization rather than filtration. Its interpretation remains limited because the measurement followed an unintended reheating period.

**Q02 is the least reliable held-out prediction.** It is the only solvent-S3 case, and S3 was never tested in the campaign. The materials are anonymous, so its index supplies no defensible chemical analogy. Consequently, its predicted yield, particle distribution and feasibility rely on an essentially uncalibrated solvent extrapolation. Q02’s wide intervals acknowledge this, but even their center and shape are less grounded than predictions involving S0 or S1.
