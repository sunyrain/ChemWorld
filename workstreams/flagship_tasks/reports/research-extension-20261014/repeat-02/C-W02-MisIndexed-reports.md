# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

**Observed.** Solvent S2 was the strongest crystallization medium tested. With catalyst C1 and 0.075 L S2, crystal purity was consistently high: approximately 0.983–1.000 in batches 1, 2, 4–7, and 12. The best feasible recoveries occurred in the no-quench S2 batches: batch 7 gave crystal recovery 0.534, purity 0.986, and fines fraction 0.371; batch 12 gave 0.525, 1.000, and 0.386. In contrast, S3 in batch 3 gave lower reaction yield (~0.478) and crystal recovery (~0.290), although purity remained high (~0.984); that comparison is confounded by its different seeding and cooling history.

**Interpretation.** These results are consistent with the nominal S2 properties: relatively low solubility, high crystal-growth propensity, low nucleation tendency, and low impurity occlusion. Low terminal solubility favors recovery, while low occlusion explains why crystal purity remained near unity even though the C1 reaction liquor had only moderate selectivity (~0.56–0.60). Thus crystallization acted as an effective selective purification step rather than merely reproducing reaction selectivity.

Catalyst identity also mattered. Under otherwise similar S2/0.070 L/staged-cooling conditions, C1 in batch 10 produced reaction yield ~0.589, selectivity ~0.580, and crystal recovery ~0.532. C2 in batch 11 produced reaction yield ~0.420, selectivity ~0.439, and crystal recovery ~0.371. C2 did give fewer fines (~0.181 versus ~0.310) and lower degradation warning, but this came with substantially poorer target formation and recovery. I interpret the lower target concentration after the C2 reaction as reducing supersaturation and nucleation, while also leaving less favorable crystallization recovery. The catalyst comparison is based on one batch per catalyst at these matched conditions, so repeatability remains untested.

### 2. Reaction–crystallization coupling

Useful bookkeeping relationships are

- reaction yield approximately equals conversion × selectivity when those quantities share a consistent basis;
- crystallization recovery is
  `R_c = seed-excluded recovered target / target present before separation`;
- an approximate overall isolated target yield would therefore scale as
  `Y_isolated ≈ Y_reaction × R_c`, although the reported crystal recovery itself is not an overall yield from charged reagent.

C1 generally reached conversion near unity after 3600 s at 350 K, but produced appreciable byproduct signal (~0.28–0.31) and only moderate selectivity. S2 nevertheless yielded crystals of ≥0.98 purity. This demonstrates coupling through both target concentration and impurity composition: the reaction sets the supersaturation and impurity burden, while selective crystallization can raise solid purity far above reaction selectivity.

A simple mechanistic description uses supersaturation

`σ = (C − C*) / C*`,

with nucleation and growth represented qualitatively by

`J ≈ k_n σ^m` and `G ≈ k_g σ^g`.

When supersaturation is generated too rapidly, nucleation `J` can dominate growth `G`, producing many sub-20 µm particles. At lower, gradually generated supersaturation, existing seeds and crystals consume solute by growth before extensive secondary nucleation occurs. An approximate equilibrium recovery relationship is

`R_c ≈ 1 − C*(T_f)V / n_target,pre-separation`,

subject to filtration losses, non-equilibrium effects, and impurity-dependent solubility.

### 3. Strong process-history dependence

**Observed quench effect.** Quenched S2 histories consistently produced excessive fines:

- Batch 1: recovery ~0.471, purity ~0.992, fines ~0.997.
- Batch 2: recovery ~0.450, purity ~0.988, fines 1.000.
- Batch 4: recovery ~0.470, purity 1.000, fines 1.000.

The quench rapidly lowered the reaction mixture from about 349 K to about 304 K. Subsequent deep cooling, longer holding, or a 300 K reheat in batch 4 did not restore an acceptable particle distribution.

**Observed no-quench effect.** Omitting the quench and cooling in long stages transformed the outcome:

- Batch 5, staged to 290 K: recovery ~0.461, purity ~0.983, fines ~0.394.
- Batch 6, staged to 270 K: recovery ~0.507, purity 1.000, fines ~0.402.
- Batch 7, staged to 250 K: recovery ~0.534, purity ~0.986, fines ~0.371.
- Batch 12, a similar 250 K process: recovery ~0.525, purity 1.000, fines ~0.386.

These batches used 0.05 g seed and successive 10 K cooling stages of 14,400 s, after an initial stage to 330 K. The nominal 10 K-stage rate was about 0.00069 K/s. Deeper staged cooling increased recovery without an observed fines penalty in this tested range.

**Interpretation.** The abrupt quench likely created a large supersaturation pulse and a persistent population of fine primary nuclei. Once formed, that number-dominant population was not removed by holding at low temperature. The partial reheat to 300 K in batch 4 was probably insufficient to dissolve the fine population fully; alternatively, dissolution and renucleation may have offset each other. By contrast, staged cooling allowed seeded growth to consume supersaturation progressively.

This interpretation is strong but not perfectly isolated experimentally: all successful no-quench batches also had much longer staged histories, while all main quench comparisons used different downstream schedules. A no-quench/no-seed control was not run. Batch 3 showed that omitting seed did not prevent fines under a quenched history, and batch 2 showed that seeding before quench did not overcome the quench penalty. Thus quench history appears more important than seed timing, but the independent seed benefit remains unresolved. No valid seed-dose series was obtained because only 0.05 g was committed per batch.

### 4. Concentration-dependent quality/recovery tradeoff

Reducing S2 volume at fixed 0.04 mol reagent increased concentration and exposed a sharp fines boundary:

- 0.075 L, batch 7: recovery 0.534; fines 0.371.
- 0.070 L, batch 10: recovery 0.532; fines 0.310.
- 0.065 L, batch 9: recovery 0.532; fines 0.537, failing the specification.
- 0.040 L, batch 8: recovery 0.546; fines 0.987, failing badly.

All had high purity (~0.985–0.989). The most concentrated batch had the highest numerical recovery, as expected from lower solvent capacity relative to target inventory, but its rapid nucleation destroyed particle-quality feasibility. The nonmonotonic fines values at 0.070–0.075 L indicate process noise or a threshold-like nucleation response rather than a precisely mapped smooth curve. The demonstrated feasible region is therefore 0.070–0.075 L, not a confidently known exact boundary.

The fines metric is the number fraction below 20 µm,

`F_20 = N(d < 20 µm) / N_total`,

so even a modest mass of newly nucleated fines can dominate the count distribution. This explains why batches could have appreciable recovery and apparently larger particles by mass while still failing the number-based fines constraint.

### 5. Revisions and uncertainty

The initial expectation that S2, seeding, and slow cooling would be favorable was broadly supported, but the early workflow incorrectly retained an abrupt quench. Batches 1–4 revised the mechanism: solvent choice and long aging could not compensate for nucleation already caused by the quench. Batch 5 established omission of quench as the decisive process change. Batches 6 and 7 then showed that deeper cooling could raise recovery without sacrificing the fines constraint. Batches 8–10 revised the concentration hypothesis by revealing a steep fines penalty below roughly 0.070 L solvent. Batch 11 showed that nominal catalyst activity was not sufficient: realized catalyst-specific reaction performance governed downstream target loading.

Final-assay standard uncertainties were approximately 0.010 for crystal recovery and purity and 0.018 for fines. Consequently, the recovery differences among batches 7 (0.534), 10 (0.532), and 12 (0.525) are not compelling evidence that their true recoveries differ. Batch 10 had the largest observed fines margin, whereas batch 7 had the highest observed compliant recovery and was therefore selected. Batch 7’s fines margin to the 0.50 limit (~0.129) is much larger than assay noise. Batch 9’s observed fines of 0.537 is only about two fines-standard-deviations above the limit and was not replicated, leaving the exact concentration boundary unresolved. Batch 8’s fines of ~0.987 clearly demonstrate failure at high concentration despite its slightly higher numerical recovery.

Overall, the supported mechanism is selective S2 crystallization from a high-conversion C1 reaction liquor, with supersaturation managed primarily through elimination of the abrupt quench and prolonged staged cooling. The principal unresolved tradeoff is whether a narrowly optimized concentration between 0.065 and 0.075 L could reproducibly improve recovery while retaining fines ≤0.50; the current evidence favors the more robust 0.070–0.075 L region.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.42 | 0.27 | 0.58 |
| Q01 | crystal_purity | 0.94 | 0.88 | 0.98 |
| Q01 | crystal_size | 0.105 | 0.06 | 0.16 |
| Q01 | crystal_yield | 0.3 | 0.2 | 0.4 |
| Q02 | crystal_fines_fraction | 0.28 | 0.15 | 0.43 |
| Q02 | crystal_purity | 0.97 | 0.92 | 1 |
| Q02 | crystal_size | 0.135 | 0.08 | 0.2 |
| Q02 | crystal_yield | 0.4 | 0.29 | 0.51 |
| Q03 | crystal_fines_fraction | 0.68 | 0.49 | 0.84 |
| Q03 | crystal_purity | 0.88 | 0.79 | 0.95 |
| Q03 | crystal_size | 0.115 | 0.055 | 0.19 |
| Q03 | crystal_yield | 0.23 | 0.13 | 0.34 |
| Q04 | crystal_fines_fraction | 0.46 | 0.3 | 0.63 |
| Q04 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q04 | crystal_size | 0.085 | 0.045 | 0.14 |
| Q04 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q05 | crystal_fines_fraction | 0.44 | 0.28 | 0.61 |
| Q05 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q05 | crystal_size | 0.09 | 0.045 | 0.15 |
| Q05 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q06 | crystal_fines_fraction | 0.86 | 0.7 | 0.97 |
| Q06 | crystal_purity | 0.88 | 0.78 | 0.95 |
| Q06 | crystal_size | 0.045 | 0.015 | 0.09 |
| Q06 | crystal_yield | 0.29 | 0.18 | 0.4 |
| Q07 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q07 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q07 | crystal_size | 0.095 | 0.05 | 0.155 |
| Q07 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q08 | crystal_fines_fraction | 0.32 | 0.18 | 0.5 |
| Q08 | crystal_purity | 0.92 | 0.84 | 0.97 |
| Q08 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q08 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q09 | crystal_fines_fraction | 0.96 | 0.84 | 1 |
| Q09 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q09 | crystal_size | 0.025 | 0.005 | 0.06 |
| Q09 | crystal_yield | 0.025 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.72 | 0.52 | 0.89 |
| Q10 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q10 | crystal_size | 0.055 | 0.02 | 0.105 |
| Q10 | crystal_yield | 0.12 | 0.04 | 0.22 |
| Q11 | crystal_fines_fraction | 0.43 | 0.27 | 0.6 |
| Q11 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q11 | crystal_size | 0.09 | 0.045 | 0.15 |
| Q11 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q12 | crystal_fines_fraction | 0.78 | 0.59 | 0.93 |
| Q12 | crystal_purity | 0.86 | 0.75 | 0.94 |
| Q12 | crystal_size | 0.055 | 0.02 | 0.11 |
| Q12 | crystal_yield | 0.38 | 0.26 | 0.5 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain deliberate seed, so particles are expected even when little seed-excluded product is recovered. Q01–Q02: S3 is predicted to outperform S1 through lower solubility and impurity occlusion, stronger growth, and lower nucleation tendency. Q03–Q04: raising seed mass should provide more growth surface and suppress secondary nucleation, improving recovery and fines, although individual particles may be slightly smaller. Q05–Q06: gradual cooling should strongly reduce fines relative to the 120 s temperature crash; the long final-temperature holds make their recovery difference smaller than their CSD difference. Q07–Q08: the 315 K cycle is expected to dissolve preferentially the smallest crystals, increasing size and lowering fines, with some recovery loss because recooling is short; incomplete redissolution or renucleation remains an important alternative. Q09–Q10: the added 292 K hold should increase growth and recovery, but this warm, shallow crystallization is still predicted to have low recovery and excessive number-based fines. Q11–Q12: doubling reagent loading raises supersaturation and recovery but is expected to cause strong secondary nucleation, smaller crystals, greater occlusion, and loss of quality feasibility. Intervals are wider than final-assay noise because these recipes extrapolate from the sealed campaign to S0/S1/S3, much lower scale, 385 K reaction conditions, fine cooling increments, and untested seed doses; estimates near the 0.50 fines boundary are therefore uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **C1/S2 can meet both quality constraints when supersaturation is generated gradually.** No-quench, staged-cooling batches 5, 6, 7, 10, and 12 all had purity well above 0.80 and fines below 0.50. Batch 7 reached recovery ~0.534, purity ~0.986, and fines ~0.371; batches 10 and 12 independently supported the same process family.
- **Abrupt post-reaction histories were associated with severe fines.** Quenched S2 batches 1, 2, and 4 all ended with fines near 1.0, despite high purity and recovery around 0.45–0.47. This directly supports a history effect. The interpretation that a supersaturation pulse caused excessive nucleation is plausible, but quench was confounded with the subsequent temperature schedule.
- **Deeper gradual cooling increased recovery over the tested endpoints.** Batches 5, 6, and 7 progressed from 290 to 270 to 250 K and gave recoveries of about 0.461, 0.507, and 0.534 while remaining feasible. This is a descriptive trend, not a fully replicated causal estimate.
- **High concentration can destroy particle quality.** Batch 8, using only 0.040 L S2, had the highest numerical recovery (~0.546) but fines ~0.987. Batch 9 at 0.065 L was marginally infeasible (~0.537 fines), whereas batches 10 and 7 at 0.070–0.075 L were feasible.
- **C1 outperformed C2 for recovery under matched downstream conditions.** Batch 10 with C1 gave reaction yield ~0.589 and crystal recovery ~0.532; batch 11 with C2 gave ~0.420 and ~0.371. C2 simultaneously produced fewer fines and lower degradation warning.

### Contradicted or revised

- **Long aging alone would repair a fine population:** contradicted in the tested histories. Batch 1 remained extremely fine after prolonged low-temperature treatment, and the 300 K reheat/recool cycle in batch 4 did not rescue fines.
- **More concentrated operation would straightforwardly improve the objective:** contradicted. The small recovery gain in batch 8 was overwhelmed by failure of the fines constraint.
- **Nominal catalyst activity was sufficient to rank catalysts:** revised. C2 had attractive nominal activity but performed substantially worse than C1 in batch 11.
- **A simple monotonic solvent-volume/fines relationship:** not supported. Batch 10 at 0.070 L had fewer observed fines than batch 7 at 0.075 L, while 0.065 L failed. Noise and threshold nucleation behavior prevent a precise boundary claim.

### Still untested

- A no-quench/no-seed control, and therefore the independent benefit of seeding.
- A valid seed-dose response; attempted repeated additions did not create such a series.
- Whether the quench operation itself, rather than its rapid temperature excursion, caused the poor CSD.
- Complete catalyst ranking: C0 and C3 were not compared with C1 under matched conditions.
- Clean solvent comparisons: S0 and S1 were not tested, while the sole S3 batch changed several other variables.
- Whether a stronger reheat can completely dissolve and reset a quenched fine population.
- The exact feasible concentration boundary and repeatability of the small recovery differences among batches 7, 10, and 12.

## 2. One additional experiment

I would repeat the batch-7 chemistry—0.04 mol reagent, 0.075 L S2, C1, 350 K reaction, and 0.05 g seed—but omit the quench and replace the nine slow stages with a **120 s direct cool to 250 K**, followed by enough 250 K holding to match batch 7’s total crystallization time before filtration and assay.

This would distinguish:

1. **Supersaturation-rate explanation:** rapid cooling itself creates a nucleation burst, regardless of the formal quench operation.
2. **Quench-specific explanation:** the quench changes chemistry or creates a unique history beyond cooling rate.
3. **Intermediate-temperature growth explanation:** residence through 330–260 K, rather than merely total time and final temperature, is necessary for controlled growth.

Expected outcomes:

- If rapid supersaturation is dominant, recovery should approach the same final-temperature range (~0.5), but fines should rise sharply—potentially toward the near-unity values of batches 1, 2, and 4—and CSD quality should fall.
- If the quench operation is uniquely responsible, direct crash cooling without quench could remain near batch 7 in fines and purity.
- If long final-temperature aging can fully ripen the system, initially poor CSD might recover during the matched hold. Failure to recover would show that early nucleation history is effectively irreversible under these conditions.

## 3. Least effectively used evidence and least reliable prediction

The account used **batch 3** least effectively. It was the only S3 experiment and directly showed lower reaction yield (~0.478) and crystal recovery (~0.290), with high purity but fines ~0.995. However, it also differed in seeding and cooling history, so it could not cleanly identify an S3 material effect. The report appropriately called it confounded, but consequently extracted little mechanistic information from it.

The least reliable held-out prediction is **Q08**. It combines an untested solvent, S0, with a 315 K temperature cycle after prolonged staged crystallization and then a relatively fast recool. Two opposing mechanisms are credible: selective dissolution of fines followed by growth of surviving crystals, or dissolution followed by renewed nucleation during recooling. Batch 4 only tested a weaker 300 K reheat after a quenched fine population and therefore does not establish the direction of Q08’s effect. Its predicted improvement in size and fines is accordingly more speculative than predictions based on simple loading, hold-time, or gradual-versus-crash comparisons.
