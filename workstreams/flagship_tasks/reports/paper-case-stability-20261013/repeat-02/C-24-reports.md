# C-24 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process context
The sealed recommendation is batch 24: 0.015 mol each of limiting reagent and component, 0.080 L S1, 0.005 mol C3, reaction near 350 K for 1,200 s under nitrogen, 1.0 g total seed added before cooling, two-stage cooling to 300 K for 14,400 s and then 250 K for 14,400 s, followed by prompt filtration. Its final assay gave crystal recovery 0.632, purity 1.000, and fines fraction 0.313.

### Reaction behavior and coupling to crystallization
The early C1/S2 reaction at about 373 K for 1,800 s gave complete conversion but poor selectivity (0.437), yield 0.430, and byproduct signal 0.332 in batch 1. The milder batch-2 history near 350 K for 1,200 s gave selectivity 0.542, yield 0.507, and byproduct signal 0.250. This initially suggested that excessive temperature or residence time promoted parallel byproduct formation. However, temperature, time, and charge concentration changed together, so their individual effects were never isolated.

Later material selection and lower loading improved the reaction substantially. Batch 24 gave conversion 0.989, selectivity 0.748, reaction yield 0.748, and byproduct signal 0.173 with C3/S1. This likely reduced impurity competition and occlusion during crystal growth.

The reported crystal recovery is

crystal recovery = seed-excluded recovered target / target present before separation.

It is therefore a crystallization-stage recovery rather than an overall yield from charged reagent. Upstream conversion and selectivity do not enter this ratio directly, but they alter target concentration, impurity burden, supersaturation, and hence nucleation and growth. Overall isolated target production would scale approximately as reaction target yield × crystallization recovery.

### Material effects
The nominal dossier led initially to S2 and C1 because S2 was described as having low solubility, low nucleation tendency, high growth, and low impurity occlusion. Experiments revised both choices.

In the matched C1, two-stage cooling solvent comparison:
- Batch 12, S2: recovery 0.491, purity 0.996, fines 0.231.
- Batch 13, S1: recovery 0.537, purity 0.983, fines 0.325.
- Batch 14, S3: recovery 0.443, purity 0.958, fines 0.557.
- Batch 15, S0: recovery 0.516, purity 0.991, fines 0.610.

Thus S1 provided the best feasible recovery in this comparison. S2 offered a larger fines margin but lower recovery. S0 recovered substantial material but failed because excessive nucleation produced too many particles below 20 µm; S3 also failed the fines constraint. The result shows that fixed-world material residuals and reaction–solvent interactions outweighed the nominal solvent ranking.

At the lower matched loading in S1, batches 17–20 screened catalysts:
- C0, batch 17: recovery 0.601, purity 0.997, fines 0.272.
- C1, batch 18: recovery 0.562, purity 0.997, fines 0.333.
- C2, batch 19: recovery 0.500, purity 0.971, fines 0.258.
- C3, batch 20: recovery 0.626, purity 0.994, fines 0.385.

C3 maximized recovery and reaction selectivity, although C0 and C2 produced fewer fines. This is the principal observed recovery–particle-quality tradeoff. C3 remained below the fines limit, and later C3 repeats provided a better margin.

### Crystallization mechanism and process-history dependence
A useful qualitative description is supersaturation S = C/C*(T, solvent). Crystal growth and primary/secondary nucleation can be represented schematically as

G ∝ (S − 1)^g,
B ∝ (S − 1)^n,

with nucleation usually much more sensitive to supersaturation than growth. Rapid temperature changes can therefore generate many new nuclei, whereas gradual cooling in the presence of seed surface directs solute toward growth on existing particles. Impurities can modify both rates and may be incorporated or adsorbed during rapid growth.

This framework explains the strongest process-history result. Batch 1 used an abrupt quench, only 0.05 g seed, deep cooling, and a hold; it gave recovery 0.355 but fines 0.997. Batch 2 increased post-quench seed to 0.50 g and slowed cooling, yet fines remained 1.000. Adding seed after the quench evidently could not undo the population of nuclei already created.

Batch 3 instead seeded before the large temperature drop and cooled directly without quenching. Despite stopping at the warmer endpoint near 298 K, it achieved recovery 0.376 with fines 0.417 and purity 0.989. Because endpoint, seed dose, and quench history changed together, this is not a pure causal estimate; nevertheless, all later pre-seeded direct-cooling batches remained feasible, whereas both post-quench batches failed badly. Avoidance of abrupt supersaturation is therefore the best-supported interpretation.

For S2 with 1.0 g seed and prompt filtration, progressively colder endpoints raised recovery while maintaining acceptable fines: approximately 0.400 at 294 K (batch 5), 0.424 at 290 K (batch 6), 0.440 at 286 K (batch 7), 0.455 near 282–278 K (batches 8–9), 0.471 at 270 K (batch 10), and 0.488 at 250 K (batch 11). This is consistent with decreasing solubility increasing the crystallized fraction. Adjacent differences are small relative to the final-assay crystal-recovery noise scale of about 0.01, so the detailed curve and apparent plateau should not be overinterpreted.

Splitting the cooling trajectory into 350→300→250 K improved particle quality. Batch 12 gave recovery 0.491 and fines 0.231, versus 0.488 and fines 0.316 for the one-stage batch 11. The recovery difference is negligible, but the fines improvement is larger than the stated fines-noise scale and is mechanistically consistent with maintaining growth-dominated supersaturation.

Stopping history was also critical. Batch 16 matched the S1 staged process but added a controlled 250 K hold. Recovery collapsed to 0.168 and fines rose to 0.987, compared with 0.537 recovery and 0.325 fines for prompt-filtered batch 13. Possible explanations include secondary nucleation, redissolution, aggregation/breakage dynamics, or a benchmark process-state transition; the available measurements do not distinguish them. Operationally, prompt filtration is strongly supported.

A reheat/recool cycle in batch 21 remained feasible and gave the numerically highest recovery, 0.634, but fines worsened to 0.395. Its recovery advantage over simpler C3 batches was much smaller than assay noise. The cycle therefore did not establish a useful Ostwald-ripening benefit and added unnecessary process risk and complexity.

Increasing seed from 1.0 to 1.5 g in batch 22 did not improve recovery: it gave 0.626 recovery and 0.374 fines. More seed surface may have divided available solute among more growing particles, consistent with its modest particle-quality result. The seed-dose optimum was not mapped finely.

### Reproducibility and remaining uncertainty
The preferred C3/S1 staged family reproduced well: batches 20, 22, 23, and 24 gave recoveries 0.626, 0.626, 0.621, and 0.632, respectively, with all purities at least 0.994 and fines between 0.313 and 0.385. This repeatability is stronger evidence than the single numerical maximum in batch 21.

Lowering each reactant from 0.0175 mol to 0.015 mol in batch 24 retained or slightly improved recovery and selectivity, but this loading comparison was not replicated. Possible mechanisms include reduced impurity concentration or reduced uncontrolled nucleation; alternatively, the difference may simply be assay/process variation.

Unresolved issues include the exact kinetic cause of the harmful endpoint hold, the independent effects of reaction temperature and residence time, and whether a seed dose between 1.0 and 1.5 g or a refined intermediate cooling trajectory could improve size without sacrificing recovery. The observed catalyst tradeoff also remains relevant: C0 offered a larger fines margin, while C3 offered higher recovery. Within the tested domain, however, the repeated C3/S1 two-stage process provides the strongest combination of recovery, purity, and compliance with the fines constraint.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.2 | 0.08 | 0.38 |
| Q01 | crystal_purity | 0.98 | 0.93 | 1 |
| Q01 | crystal_size | 0.22 | 0.13 | 0.32 |
| Q01 | crystal_yield | 0.55 | 0.42 | 0.66 |
| Q02 | crystal_fines_fraction | 0.52 | 0.32 | 0.7 |
| Q02 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q02 | crystal_size | 0.15 | 0.07 | 0.25 |
| Q02 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q03 | crystal_fines_fraction | 0.66 | 0.45 | 0.84 |
| Q03 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q03 | crystal_size | 0.1 | 0.04 | 0.19 |
| Q03 | crystal_yield | 0.41 | 0.27 | 0.54 |
| Q04 | crystal_fines_fraction | 0.39 | 0.22 | 0.58 |
| Q04 | crystal_purity | 0.97 | 0.9 | 1 |
| Q04 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q04 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q05 | crystal_fines_fraction | 0.36 | 0.19 | 0.55 |
| Q05 | crystal_purity | 0.97 | 0.9 | 1 |
| Q05 | crystal_size | 0.19 | 0.1 | 0.3 |
| Q05 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q06 | crystal_fines_fraction | 0.72 | 0.52 | 0.89 |
| Q06 | crystal_purity | 0.96 | 0.88 | 1 |
| Q06 | crystal_size | 0.09 | 0.03 | 0.17 |
| Q06 | crystal_yield | 0.47 | 0.34 | 0.6 |
| Q07 | crystal_fines_fraction | 0.34 | 0.17 | 0.54 |
| Q07 | crystal_purity | 0.97 | 0.9 | 1 |
| Q07 | crystal_size | 0.2 | 0.11 | 0.31 |
| Q07 | crystal_yield | 0.46 | 0.33 | 0.59 |
| Q08 | crystal_fines_fraction | 0.53 | 0.33 | 0.72 |
| Q08 | crystal_purity | 0.98 | 0.91 | 1 |
| Q08 | crystal_size | 0.16 | 0.07 | 0.27 |
| Q08 | crystal_yield | 0.42 | 0.28 | 0.56 |
| Q09 | crystal_fines_fraction | 0.25 | 0.08 | 0.49 |
| Q09 | crystal_purity | 0.98 | 0.88 | 1 |
| Q09 | crystal_size | 0.12 | 0.05 | 0.22 |
| Q09 | crystal_yield | 0.03 | 0 | 0.1 |
| Q10 | crystal_fines_fraction | 0.32 | 0.14 | 0.55 |
| Q10 | crystal_purity | 0.97 | 0.88 | 1 |
| Q10 | crystal_size | 0.15 | 0.07 | 0.26 |
| Q10 | crystal_yield | 0.18 | 0.07 | 0.3 |
| Q11 | crystal_fines_fraction | 0.37 | 0.2 | 0.56 |
| Q11 | crystal_purity | 0.97 | 0.9 | 1 |
| Q11 | crystal_size | 0.19 | 0.1 | 0.3 |
| Q11 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q12 | crystal_fines_fraction | 0.56 | 0.36 | 0.74 |
| Q12 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q12 | crystal_size | 0.14 | 0.06 | 0.24 |
| Q12 | crystal_yield | 0.64 | 0.5 | 0.76 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 applies the observed solvent ranking: S1 should give higher recovery and much better fines control than S3. Q03–Q04 assigns the larger seed charge better control of primary nucleation. Q05–Q06 treats gradual staged cooling as growth-dominated, while the rapid initial drop creates a persistent fine population despite the long cold residence. Q07–Q08 reflects the campaign evidence that reheating/recooling did not establish a recovery benefit and tended to erode the fines margin. Q09–Q10 predicts little seed-excluded recovery after only 60 seconds, with a 292 K growth period increasing recovery and size. Q11–Q12 predicts that doubled loading increases fractional recovery but also supersaturation, occlusion risk, and fines. Every recipe contains seed, so particles are expected even where seed-excluded product recovery is small. Intervals are deliberately broad because these recipes use much smaller charges, longer histories, post-quench seeding, and no exact campaign analogue; classifications near the 0.50 fines boundary are correspondingly uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S1/C3 was the best robust feasible material combination tested.** In the matched lower-loading S1 catalyst screen, recovery was 0.601 for C0 (batch 17), 0.562 for C1 (18), 0.500 for C2 (19), and 0.626 for C3 (20). All were feasible, although C3 had a smaller fines margin than C0/C2. C3/S1 then reproduced at recovery 0.626, 0.621, and 0.632 in batches 22–24, with purity ≥0.994 and fines 0.313–0.374.
- **S1 offered the best feasible solvent balance in the matched screen.** With C1 and staged cooling, S1 gave recovery 0.537 and fines 0.325 (batch 13), compared with S2 at 0.491/0.231 (12), S3 at 0.443/0.557 (14), and S0 at 0.516/0.610 (15). Directly observed: S1 improved recovery over S2, while S0 and S3 failed the fines limit. Interpretation: solvent-dependent solubility and nucleation/growth behavior caused the ranking.
- **Colder endpoints increased S2 recovery within the tested range.** Recovery rose from about 0.400 at 294 K (batch 5) to 0.488 at 250 K (11), while fines remained below 0.50. Adjacent changes are not individually compelling relative to assay noise, but the full trend is credible.
- **Two-stage cooling improved the fines margin without materially changing recovery.** Batch 12, cooled 350→300→250 K, gave recovery 0.491 and fines 0.231; the one-stage batch 11 gave 0.488 and 0.316. The recovery difference is negligible, whereas the fines difference is meaningful.
- **The extra controlled endpoint hold was harmful under the tested implementation.** Batch 16 fell to recovery 0.168 and fines 0.987, versus 0.537 and 0.325 for the otherwise similar prompt-filtered batch 13. What is directly established is the process outcome, not whether it arose from secondary nucleation, redissolution, or control-operation semantics.

### Supported, but confounded
- **Pre-drop seeding with gradual direct cooling was associated with effective fines control.** Post-quench batches 1–2 had fines near 1, whereas batch 3, seeded before direct cooling, had fines 0.417. Later direct-cooling batches were also feasible. However, seed dose, endpoint, cooling history, and quench use changed together, so the claim that quench-induced nucleation was the sole cause remains interpretive.
- **Milder reaction conditions appeared to reduce byproduct formation.** Batch 1 gave selectivity 0.437 and byproduct signal 0.332, while batch 2 gave 0.542 and 0.250. Temperature, residence time, and loading all changed, so no individual kinetic effect was isolated.
- **Lower loading may be beneficial.** Batch 24 at 0.015 mol per reactant gave recovery 0.632 and selectivity 0.748, while nearby C3 recipes at 0.0175 mol gave recovery around 0.621–0.626. The difference is small and unreplicated, so it may be ordinary process/assay variation.

### Contradicted or revised
- **The dossier-based expectation that S2/C1 would be optimal was contradicted.** S2 gave excellent fines control, but S1 improved recovery; C3 outperformed C1 experimentally.
- **A general benefit from prolonged endpoint aging was contradicted by batch 16.** The tested hold sharply worsened both recovery and fines.
- **More seed was not monotonically beneficial.** Raising seed from 1.0 to 1.5 g in batch 22 did not improve recovery and did not clearly improve final size or fines.
- **A reheat/recool benefit was not established.** Batch 21 had the numerically highest recovery, 0.634, but this was indistinguishable from simpler C3 batches and came with fines of 0.395. Added complexity was therefore unsupported.

### Still untested
The independent effects of reaction temperature and time, the detailed seed-dose optimum, whether C0 could outperform C3 after separate optimization, the precise cause of batch 16’s failure, and whether the material rankings persist outside the tested loading and thermal window remain unresolved.

## 2. One additional experiment

I would repeat the batch-13 S1/C1 recipe exactly, including staged 350→300→250 K cooling, but replace batch 16’s reconfiguration plus `advance_control` hold with a single 7,200 s `cool_crystallize` operation at 250 K before filtration.

This would distinguish two explanations for batch 16:
1. **Physical cold-residence mechanism:** prolonged residence at high supersaturation causes secondary nucleation, attrition, degradation, or redissolution. The new experiment should then resemble batch 16—substantially lower recovery and fines approaching 1.
2. **Operation/control-state mechanism:** the harmful transition was specifically caused by reconfiguring control and advancing it, rather than by elapsed time at 250 K. The new experiment should then remain near batch 13—roughly 0.54 recovery, high purity, and fines near 0.33—or show only a modest change.

An intermediate outcome, such as preserved recovery but elevated fines, would suggest that residence promotes secondary nucleation while the severe recovery loss requires the control-state transition.

## 3. Least effectively used observation and least reliable prediction

The account used the **batch-16 observation** least effectively at the mechanistic level. It correctly treated the outcome as operationally important, but too readily discussed it as a conventional cold hold. The actual intervention combined control reconfiguration, `advance_control`, and time; therefore secondary nucleation and redissolution were only hypotheses, not uniquely supported mechanisms.

The least reliable held-out prediction is **Q06**. It combines a 120 s plunge to 278.15 K with approximately 72 hours of repeated same-target `cool_crystallize` operations—a history far outside the campaign. The data do not establish whether repeated same-target operations behave as benign growth holds, cause continued secondary nucleation, or trigger the kind of deterioration seen in batch 16. Consequently, its predicted high fines and its recovery/size intervals depend heavily on extrapolated process semantics rather than a close experimental analogue.
