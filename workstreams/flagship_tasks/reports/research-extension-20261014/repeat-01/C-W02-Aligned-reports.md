# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Process studied
All 12 batches used catalyst C1 under nitrogen, with 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and a nominal reaction at 370 K for 3600 s before quenching and crystallization. Consequently, solvent and crystallization history are experimentally informative, whereas catalyst identity, catalyst loading, reaction temperature, and atmosphere were not independently tested.

### Material effects and reaction–crystallization coupling
Conversion was essentially complete in nearly every batch, but solvent substantially affected selectivity, byproduct formation, reaction yield, crystal recovery, and particle distribution. S0 and S1 gave the strongest reaction-stage performance: batch 7 (S0) had reaction yield 0.677, selectivity 0.651, and byproduct signal 0.244; batch 6 (S1) gave yield 0.658 and selectivity 0.657. They also gave relatively high crystallization recovery—0.531 and 0.551—but almost entirely fine populations, with final fines fractions 0.987 and 1.000. Thus maximizing reaction output or crystallization recovery alone did not produce acceptable particles.

S2 produced high-purity crystals and recoveries near 0.48–0.49, but all tested S2 histories had fines near unity. Examples include batch 1 (recovery 0.479, purity 0.992, fines 0.997), batch 4 (0.492, 1.000, 1.000), and batch 5 (0.489, 0.983, 1.000). This contradicted the initial dossier-based expectation that S2’s nominally high growth and low nucleation tendencies would create a coarse distribution.

S3 reduced reaction performance—batch 8 had reaction yield 0.527, selectivity 0.536, and crystal recovery 0.407—but markedly improved the particle distribution: fines 0.647 and CSD quality 0.647. Deep-cooling S3 batches 11 and 12 further reduced fines to 0.513 and 0.518 while maintaining purity of 0.993 and 0.995. The observed solvent effect therefore appears to be a genuine coupling: the solvent that best moderated crystallization nucleation/distribution was not the solvent that maximized reaction yield or crystal recovery.

The crystallization recovery is conditional on target product already present before separation. A useful mass relation is

recovered target from charge ≈ charged reactant × reaction yield × crystal recovery.

For example, batch 11 corresponds to an approximate charge-to-recovered-target fraction of 0.523 × 0.451 ≈ 0.236, whereas batch 6 is about 0.658 × 0.551 ≈ 0.362 but fails the fines constraint. Crystal purity remained above 0.97 in all leading cases, suggesting that the unresolved limitation was particle population rather than impurity rejection.

### Crystallization mechanism and process history
A conventional supersaturation/population-balance interpretation is useful. Let S=C/C* be supersaturation. Qualitatively,

nucleation rate B ∝ (S−1)^b,
growth rate G ∝ (S−1)^g,

and the number distribution may be represented by

∂n(L,t)/∂t + ∂[G n(L,t)]/∂L = Bδ(L−L0) plus secondary-nucleation, aggregation, breakage, and dissolution terms.

The fines metric is the number fraction ∫₀²⁰ n(L)dL / ∫₀∞ n(L)dL. Solvent changes solubility C*, nucleation and growth constants, and impurity occlusion. Cooling history determines whether supersaturation is consumed by growth on established crystals or by creation of many new particles.

The observations imply strong history dependence, but several intuitive interventions failed in S2. Lowering seed from 0.05 g to 0.005 or 0.0001 g, extending cold holds, delaying seeding until 310 K, and cycling between 305 and 278 K did not reduce final fines (batches 2–5). One interpretation is that primary or secondary nucleation was already dominant and the tested seed surface area could not control supersaturation. Another is that seed introduced above the metastable region partly dissolved. However, delayed seeding in batch 4 also failed, so seed timing alone is insufficient. The simulator’s `wait` and `cool_crystallize` histories may also represent kinetically distinct regimes; long waits in batch 3 did not reproduce continued productive growth.

Within S3, deeper cooling was the clearest useful change. Batch 8 ended at 278 K and assayed at recovery 0.407 and fines 0.647. Batch 9, using less seed and stopping at 285 K, was worse on both recovery (0.375) and fines (0.823). Batch 11 used staged cooling to 250 K and improved both recovery to 0.451 and fines to 0.513. This local improvement suggests that, for S3, established crystals could consume additional supersaturation during deep cooling faster than new fine particles accumulated. It is not proof of that mechanism: endpoint, staging, and seed history were not fully factorial.

A cumulative 1 g seed addition did not improve S3 materially (batch 10: recovery 0.399, fines 0.669), so simply adding more seed is not supported. Repeating nominal growth/cooling operations at 250 K in batch 12 produced recovery 0.454 and fines 0.518, numerically close to batch 11 rather than clearly superior. This suggests diminishing returns or near-equilibration, although no exact replicate was run.

### Revisions and uncertainty
The principal revision was rejection of S2 as the preferred crystallization solvent despite its favorable nominal dossier. Direct experiments instead supported S3 for particle control. A second revision was that larger seed loading and extended residence time were not reliable remedies; the best evidence favored solvent selection and deep staged cooling.

These conclusions remain conditional. Only C1 was tested, so catalyst–solvent interactions and whether another catalyst could improve S3 reaction selectivity are untested. Reaction conditions were nearly fixed, and solvent comparisons were not exact crystallization-history replicates. Each batch had one final assay, so batch-to-batch differences close to the declared noise are not evidence of an effect. In particular, batches 11 and 12 are effectively tied: their recovery difference is only 0.003 and their fines difference 0.006. Reported normalized crystal size also has appreciable noise; batch 12’s size 0.0938 corresponds nominally to d50≈23.4 µm, yet its independently noisy fines estimate was 0.518.

### Unresolved quality/recovery tradeoff
No completed batch satisfied the observed fines requirement of ≤0.50, although all leading batches comfortably satisfied purity ≥0.80. High-recovery S0/S1 processes had unacceptable fines, while S3 sacrificed reaction output and some recovery to approach the particle specification. Deep cooling improved both S3 recovery and fines over the tested 278–285 K histories, so a strict local recovery–quality tradeoff was not established; nevertheless, the specification boundary remained unresolved. Batch 11 remains the sealed recommendation because it was closest to feasible: recovery 0.451, purity 0.993, and fines 0.513. Batch 12 had slightly higher recovery but a slightly larger fines violation. Replicated measurements around the S3/250 K process, followed by controlled changes to cooling trajectory or reaction selectivity, would be needed to establish whether the true process crosses the 0.50 boundary.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.32 | 0.15 | 0.56 |
| Q01 | crystal_purity | 0.99 | 0.96 | 1 |
| Q01 | crystal_size | 0.19 | 0.1 | 0.3 |
| Q01 | crystal_yield | 0.28 | 0.12 | 0.44 |
| Q02 | crystal_fines_fraction | 0.24 | 0.08 | 0.48 |
| Q02 | crystal_purity | 0.98 | 0.93 | 1 |
| Q02 | crystal_size | 0.23 | 0.12 | 0.36 |
| Q02 | crystal_yield | 0.18 | 0.06 | 0.33 |
| Q03 | crystal_fines_fraction | 0.7 | 0.45 | 0.92 |
| Q03 | crystal_purity | 0.98 | 0.93 | 1 |
| Q03 | crystal_size | 0.09 | 0.03 | 0.18 |
| Q03 | crystal_yield | 0.15 | 0.03 | 0.3 |
| Q04 | crystal_fines_fraction | 0.48 | 0.25 | 0.72 |
| Q04 | crystal_purity | 0.985 | 0.94 | 1 |
| Q04 | crystal_size | 0.15 | 0.07 | 0.26 |
| Q04 | crystal_yield | 0.16 | 0.04 | 0.31 |
| Q05 | crystal_fines_fraction | 0.44 | 0.22 | 0.68 |
| Q05 | crystal_purity | 0.986 | 0.94 | 1 |
| Q05 | crystal_size | 0.16 | 0.08 | 0.28 |
| Q05 | crystal_yield | 0.16 | 0.04 | 0.32 |
| Q06 | crystal_fines_fraction | 0.9 | 0.7 | 1 |
| Q06 | crystal_purity | 0.976 | 0.91 | 1 |
| Q06 | crystal_size | 0.065 | 0.015 | 0.15 |
| Q06 | crystal_yield | 0.17 | 0.04 | 0.33 |
| Q07 | crystal_fines_fraction | 0.39 | 0.18 | 0.63 |
| Q07 | crystal_purity | 0.988 | 0.95 | 1 |
| Q07 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q07 | crystal_yield | 0.17 | 0.04 | 0.33 |
| Q08 | crystal_fines_fraction | 0.61 | 0.34 | 0.84 |
| Q08 | crystal_purity | 0.987 | 0.94 | 1 |
| Q08 | crystal_size | 0.115 | 0.045 | 0.23 |
| Q08 | crystal_yield | 0.14 | 0.02 | 0.3 |
| Q09 | crystal_fines_fraction | 0.96 | 0.8 | 1 |
| Q09 | crystal_purity | 0.97 | 0.87 | 1 |
| Q09 | crystal_size | 0.035 | 0.005 | 0.1 |
| Q09 | crystal_yield | 0.02 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.82 | 0.56 | 0.98 |
| Q10 | crystal_purity | 0.977 | 0.9 | 1 |
| Q10 | crystal_size | 0.065 | 0.015 | 0.15 |
| Q10 | crystal_yield | 0.07 | 0 | 0.18 |
| Q11 | crystal_fines_fraction | 0.42 | 0.2 | 0.66 |
| Q11 | crystal_purity | 0.987 | 0.94 | 1 |
| Q11 | crystal_size | 0.165 | 0.08 | 0.28 |
| Q11 | crystal_yield | 0.17 | 0.04 | 0.33 |
| Q12 | crystal_fines_fraction | 0.67 | 0.43 | 0.87 |
| Q12 | crystal_purity | 0.975 | 0.91 | 1 |
| Q12 | crystal_size | 0.11 | 0.045 | 0.21 |
| Q12 | crystal_yield | 0.44 | 0.29 | 0.58 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01/Q02: the very slow ramps should favor growth over fresh nucleation; S3 is predicted to give the better particle distribution but lower recovery than S1, consistent with the campaign’s solvent tradeoff. Q03/Q04: increasing seed from 0.001 to 0.045 g should provide enough growth surface to suppress uncontrolled nucleation, with little effect on equilibrium-limited recovery. Q05/Q06: gradual cooling should produce far fewer fines than a 120 s crash followed by isothermal aging, even though final recovery is similar. Q07/Q08: the 315 K excursion may dissolve part of the crop, while the rapid one-hour recooling can regenerate fines; therefore it is predicted to be worse than the uninterrupted slow-ramp/hold history, although this direction is uncertain. Q09/Q10: two hours at 292 K should increase seed-excluded recovery and growth relative to immediate filtration, but neither is expected to achieve a coarse distribution. Q11/Q12: doubling reagent concentration should substantially increase fractional recovery, but the larger supersaturation is expected to increase nucleation, fines, and occlusion. Intervals are broad because the queries extrapolate to lower concentration, lower catalyst ratio, much longer ramps, and larger relative seed charges than the completed campaign; threshold classifications near fines=0.50 are correspondingly uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Solvent strongly affected both reaction and crystallization outcomes.** Under broadly comparable histories, S0 and S1 produced higher reaction and crystal recovery but very poor particle distributions: batch 6 (S1) had crystal yield 0.551 and fines 1.000; batch 7 (S0) had yield 0.531 and fines 0.987. Batch 8 (S3) had lower yield, 0.407, but much lower fines, 0.647, and better CSD quality, 0.647. The observation is direct; attributing it to solvent-dependent solubility, nucleation, and growth constants is interpretation.
- **Purity was not the limiting quality attribute.** The leading batches all had purity well above 0.80, including batches 8, 11, and 12 at 0.979, 0.993, and 0.995. Fines prevented feasibility.
- **S3 plus deep cooling approached the particle specification most closely.** Batch 11, cooled to 250 K, reached yield 0.451 and fines 0.513; batch 12 reached 0.454 and 0.518. These are direct results, although the causal attribution to deep cooling is only partially supported because the comparison with warmer S3 batches was not a clean one-factor experiment.
- **More seed was not a sufficient remedy.** Batch 10 used 1 g cumulative seed but still had fines 0.669, similar to the 0.647 of batch 8 with 0.05 g. This directly contradicts a large monotonic seed benefit in those histories, though it does not establish that seed amount has no effect.

### Contradicted or weakened
- **The initial expectation that S2 would give the best particles was contradicted.** Batches 1–5 all finished with fines approximately 0.995–1.000 despite favorable nominal S2 properties and variations in seed, staging, residence time, delayed seeding, and thermal cycling.
- **Extended aging alone would coarsen the S2 population** was not supported. Batch 3 added ten long waits but still assayed at fines 0.995 and normalized size 0.050.
- **Delayed seeding or modest thermal cycling would rescue S2** was contradicted in the tested forms. Delayed seeding in batch 4 left fines at 1.000; three 305/278 K cycles in batch 5 also left fines at 1.000.
- **Additional nominal growth at 250 K would materially improve S3** was weakened by batches 11 and 12. Eight extra `cool_crystallize` calls in batch 12 produced only a 0.003 numerical recovery increase and slightly worse fines. Those differences are smaller than a persuasive one-batch effect.

### Still untested or unresolved
- Catalyst identity and catalyst–solvent interaction remain untested because every batch used C1.
- The independent effects of reaction temperature, catalyst loading, reagent concentration, atmosphere, and stirring remain untested.
- It is unresolved whether S3’s advantage arises primarily from lower effective nucleation, faster growth of established particles, aggregation, altered seed persistence, filtration behavior, or a fixed hidden solvent residual.
- No exact process replicate was performed, so the repeatability and true noise-free feasibility of batches 11–12 are unresolved. Both observed fines values were close enough to 0.50 that measurement and process variability matter.
- The reaction–crystallization coupling is observational: solvent changed reaction selectivity and particle outcomes together, but the campaign did not independently vary reaction composition while holding crystallization solvent and history fixed.

## 2. One additional experiment

I would run an **exact batch-11 replicate with non-destructive particle measurements during the cooling trajectory**:

1. Repeat the C1/S3 charge, reaction, quench, and seeding conditions of batch 11.
2. Cool to 280 K using the same staged history and measure particle size/fines.
3. Continue to 250 K and measure again.
4. Hold or repeat `cool_crystallize` at 250 K for the same added duration represented by batch 12, then measure a third time.
5. Filter, terminate, and perform the final assay.

This single within-batch trajectory would distinguish three explanations:

- **Growth-dominant deep cooling:** d50 and CSD quality should increase from 280 to 250 K while fines decrease; the additional 250 K period should then show diminishing change. Final recovery should be near batches 11–12.
- **Nucleation-dominant deep cooling:** cooling from 280 to 250 K should increase particle count and recovery but increase fines or reduce d50. The low final fines previously observed would then be more plausibly noise or filtration-related.
- **No reproducible thermal effect:** intermediate measurements would show little systematic evolution, or the final result would not reproduce the approximately 0.51 fines region. That would favor fixed solvent effects, measurement variation, or uncontrolled batch variability over the proposed growth mechanism.

The experiment would not fully separate filtration from analytical noise, but the repeated in-situ measurements would remove much of the between-batch confounding that limited the original campaign.

## 3. Least effectively used evidence and least reliable prediction

### Least effectively used observation
I used the **differences between pre-filter particle-size measurements and final-assay particle metrics** least effectively. For batch 11, the in-situ measurement gave normalized size 0.060 and fines 0.524, while the final assay gave 0.072 and 0.513. For batch 12, the corresponding values were 0.053/0.521 and 0.094/0.518. Because final-assay sampling does not itself advance chemistry, these shifts could reflect measurement noise, filtration context, or differences between instrument estimators. My account relied mainly on final assays rather than using these paired readings to quantify uncertainty or question how tightly size and fines should be coupled.

### Least reliable held-out prediction
**Q08 is the least reliable prediction.** It extrapolated an S0 process through a 315 K dissolution/annealing excursion followed by rapid recooling, whereas the only campaign evidence for thermal cycling was batch 5 in S2 at a milder 305 K. Classical ripening suggests that heating could dissolve fines and improve the distribution, but rapid recooling could instead regenerate nuclei, reduce recovery through incomplete regrowth, or erase the prior slow-ramp benefit. The campaign did not resolve those competing effects for S0, so the predicted direction—worse fines than Q07—rests on a weak cross-solvent extrapolation and appropriately broad uncertainty.
