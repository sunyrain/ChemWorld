# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The process separates into two coupled functions: reaction generates the target and impurities, then crystallization partitions part of the target into a solid product. A useful bookkeeping relation is approximately

isolated target fraction ≈ reaction target yield × seed-excluded crystal recovery,

while crystal purity describes the composition of the recovered solid. Seed mass is excluded from the recovery numerator. Thus high conversion alone is insufficient: selectivity controls how much target reaches crystallization, and crystallization history controls how much is recovered and in what particle-size distribution.

Material effects

Observation: Under the commonly used 350 K, one-hour reaction, conversion was generally near unity, but selectivity and byproduct signal varied substantially. Repeated C0/S0 batches gave selectivities mostly around 0.56–0.62 and reaction yields around 0.58–0.61. Batch 12 gave conversion 1.000, selectivity 0.571, reaction yield 0.576, and byproduct signal 0.256. In contrast, the C2/S2 condition in batch 4 gave selectivity 0.443, reaction yield 0.430, and crystal recovery 0.347. With C0 but S3, batch 6 gave selectivity 0.489 and recovery 0.357. C3/S0 in batch 10 remained competitive: selectivity 0.587 and recovery 0.506.

Interpretation: Catalyst and solvent identity primarily affected target-versus-byproduct formation rather than gross conversion. C0/S0 was the most consistently productive tested combination. The comparison of C0/S0 with C0/S3 suggests a solvent effect, but most other comparisons changed catalyst and solvent together, so separate catalyst and solvent contributions cannot be uniquely assigned. A complete factorial screen and replicated reactions would be required to distinguish kinetic catalysis, solvent stabilization, and measurement variation.

Reaction–crystallization coupling

Observation: Final crystal purity was high in every completed batch, generally about 0.975–1.000, despite only moderate reaction selectivity. For example, batch 12 had crystal purity 1.000 even though reaction selectivity was 0.571. Batch 4 also assayed at purity 1.000 despite its lower reaction selectivity of 0.443.

Interpretation: Crystallization strongly rejected reaction byproducts from the recovered solid. This purification came with incomplete target recovery: recoveries ranged from about 0.30 to 0.54. The data are consistent with target and impurities having different effective solid–liquid partitioning, but they do not identify a molecular lattice mechanism. Impurity-dependent nucleation or growth inhibition is possible, especially because lower-selectivity batches 4 and 6 also had lower recoveries, but that relationship is confounded by solvent and thermal history and was not isolated experimentally.

For batch 12, multiplying reaction yield 0.576 by crystal recovery 0.541 gives an approximate overall isolated-target fraction of 0.31 relative to charged reagent, before any additional accounting corrections. This illustrates why the reported crystal recovery should not be read as overall chemical yield.

Process-history dependence

The initial hypothesis was that a moderate seed dose, slow cooling, and a cold hold would suppress primary nucleation and fines. Batch 1 used 0.05 g seed, slow cooling, a hold, and a reheat/recool cycle. It produced recovery 0.464 and purity 0.984, but fines fraction 0.997. Extending low-temperature residence did not solve the problem: batch 3 used C0/S0 with roughly 80 hours of cold holding and still gave fines 0.995 and recovery 0.460. Staged cooling with holds in batch 4 likewise ended at fines 1.000.

The hypothesis was then revised to test whether seed population was the missing control. Increasing total seed to about 1 g in batch 5 did not help: recovery was 0.484 and fines remained 1.000. Removing seed and using staged cooling in batch 7 raised recovery to 0.513 but still gave fines 0.987. Intermediate seed doses also failed: batch 10 used 0.005 g seed and finished at fines 1.000, while batch 11 used 0.0001 g and finished at fines 0.994. A 0.000001 g trial in batch 8 did not initially generate recoverable solids at the mild endpoint; additional seed and deeper cooling were required, after which recovery was 0.518 and fines 0.987.

A selective-dissolution interpretation was also tested. In batch 9, crystals formed cold were heated successively to 290, 300, and 310 K in an attempt to dissolve small particles preferentially. Particle measurements remained around 0.97–1.00 fines. Resuspension and recrystallization then reduced final recovery to 0.302 without improving fines, which remained 1.000. Consequently, neither ordinary Ostwald ripening nor the tested wash/recrystallization history provided useful size classification.

Concentration had the clearest relationship with recovery. Batch 12 used the same 0.04 mol reagent charge but only 0.02 L S0, versus approximately 0.067–0.08 L in most other batches. With C0, 0.0001 g seed, staged cooling to 265 K, and extended holds, it achieved the campaign-high recovery of 0.541 and purity 1.000. This is consistent with greater supersaturation or a larger crystallizable target inventory per solvent volume. However, it also produced fines 1.000, so concentration improved recovery without resolving particle quality. Its normalized crystal-size estimate was 0.050, corresponding nominally to a d50 near 12.5 micrometres.

Quality–recovery tradeoff and uncertainty

No completed batch met the fines requirement of at most 0.50, although all met the purity requirement of at least 0.80. The fines estimates clustered near 0.98–1.00, far enough above the threshold that normal stated instrument noise is unlikely to change the feasibility conclusion. The particle-size and fines channels are separately noisy; occasional larger normalized-size readings, such as batch 8, should therefore not be treated as deterministically consistent with the independently measured fines fraction.

Batch 12 is the strongest recovery benchmark, not a fully feasible solution. Relative to batches 7, 8, 10, and 11, its recovery advantage is numerical but not a clean causal estimate because solvent loading, seed dose, and thermal history differed and there were no true replicates. Conversely, the persistent fines failure across direct cooling, staged cooling, long holds, unseeded operation, seed doses spanning several orders of magnitude, thermal ripening, and resuspension is broad evidence that the tested controls did not access a coarse-particle regime.

Important untested alternatives include explicit size-selective classification, different seed-size distributions rather than seed mass alone, independently controlled supersaturation or antisolvent addition, alternative agitation profiles during nucleation, and a full catalyst–solvent factorial design. Atmosphere and pressure were not systematically varied. Attrition, secondary nucleation, and growth-rate limitation remain alternative explanations for the fines; the observations do not distinguish among them.

Overall, reaction optimization and crystallization purification were successful enough to give near-complete conversion, high solid purity, and recovery above 0.5. The unresolved limitation is particle-number distribution: conditions that increased recovery, especially the concentrated batch 12 process, did not reduce fines and may intensify nucleation. Any future optimization should therefore treat recovery and fines as competing responses rather than assuming that longer cooling or more seed will improve both.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.49 | 0.25 | 0.75 |
| Q01 | crystal_purity | 0.982 | 0.945 | 0.999 |
| Q01 | crystal_size | 0.082 | 0.045 | 0.125 |
| Q01 | crystal_yield | 0.34 | 0.24 | 0.45 |
| Q02 | crystal_fines_fraction | 0.7 | 0.43 | 0.92 |
| Q02 | crystal_purity | 0.975 | 0.93 | 0.998 |
| Q02 | crystal_size | 0.06 | 0.028 | 0.1 |
| Q02 | crystal_yield | 0.25 | 0.15 | 0.37 |
| Q03 | crystal_fines_fraction | 0.32 | 0.13 | 0.59 |
| Q03 | crystal_purity | 0.987 | 0.955 | 1 |
| Q03 | crystal_size | 0.105 | 0.062 | 0.16 |
| Q03 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q04 | crystal_fines_fraction | 0.46 | 0.23 | 0.72 |
| Q04 | crystal_purity | 0.985 | 0.95 | 1 |
| Q04 | crystal_size | 0.084 | 0.046 | 0.132 |
| Q04 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q05 | crystal_fines_fraction | 0.34 | 0.15 | 0.61 |
| Q05 | crystal_purity | 0.986 | 0.953 | 1 |
| Q05 | crystal_size | 0.1 | 0.058 | 0.153 |
| Q05 | crystal_yield | 0.37 | 0.26 | 0.49 |
| Q06 | crystal_fines_fraction | 0.86 | 0.65 | 0.99 |
| Q06 | crystal_purity | 0.982 | 0.943 | 1 |
| Q06 | crystal_size | 0.045 | 0.018 | 0.079 |
| Q06 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q07 | crystal_fines_fraction | 0.28 | 0.1 | 0.53 |
| Q07 | crystal_purity | 0.987 | 0.955 | 1 |
| Q07 | crystal_size | 0.11 | 0.066 | 0.165 |
| Q07 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q08 | crystal_fines_fraction | 0.8 | 0.55 | 0.98 |
| Q08 | crystal_purity | 0.979 | 0.936 | 0.999 |
| Q08 | crystal_size | 0.052 | 0.021 | 0.092 |
| Q08 | crystal_yield | 0.31 | 0.19 | 0.44 |
| Q09 | crystal_fines_fraction | 0.93 | 0.75 | 1 |
| Q09 | crystal_purity | 0.995 | 0.97 | 1 |
| Q09 | crystal_size | 0.04 | 0.014 | 0.074 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.8 | 0.56 | 0.98 |
| Q10 | crystal_purity | 0.991 | 0.961 | 1 |
| Q10 | crystal_size | 0.052 | 0.021 | 0.093 |
| Q10 | crystal_yield | 0.08 | 0.02 | 0.17 |
| Q11 | crystal_fines_fraction | 0.41 | 0.2 | 0.68 |
| Q11 | crystal_purity | 0.986 | 0.952 | 1 |
| Q11 | crystal_size | 0.09 | 0.05 | 0.141 |
| Q11 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q12 | crystal_fines_fraction | 0.73 | 0.46 | 0.94 |
| Q12 | crystal_purity | 0.965 | 0.91 | 0.995 |
| Q12 | crystal_size | 0.058 | 0.026 | 0.099 |
| Q12 | crystal_yield | 0.56 | 0.43 | 0.68 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where seed-excluded recovery is small. Q01–Q02: S1 is predicted to give greater recovery and coarser particles than S3, based on the campaign's directionally better S1 result, although catalyst/solvent confounding makes this uncertain. Q03–Q04: reducing seed mass should lower particle number and favor growth per particle, with little equilibrium-recovery change; this is uncertain because earlier seed-dose changes did not consistently solve fines. Q05–Q06: the gradual ramp should suppress burst nucleation relative to the rapid drop and long cold hold, while both approach similar recovery. Q07–Q08: the late 315 K excursion followed by rapid recooling is predicted to dissolve solids transiently and then regenerate fines, reducing recovery and quality versus uninterrupted maturation. Q09–Q10: two hours at 292 K should increase seed-excluded deposition and modestly grow particles, but both remain fines-limited. Q11–Q12: doubling reagent concentration should substantially raise recovery, while increased supersaturation promotes secondary nucleation, smaller particles, more fines, and slightly lower purity. Intervals are deliberately broad because these exact low-scale, high-temperature reactions and very slow cooling histories were not tested; feasibility labels use point estimates for the latent pre-assay outcomes.

## K2

1. Status of the main claims

Supported by direct observations

• Material choice affected observed reaction performance. Repeated C0/S0 batches generally gave selectivity around 0.56–0.62 and recovery around 0.46–0.54. By comparison, batch 4 (C2/S2) gave selectivity 0.443 and recovery 0.347, while batch 6 (C0/S3) gave selectivity 0.489 and recovery 0.357. The observation is supported; the interpretation that catalyst and solvent have separate causal effects remains only partial because most comparisons were confounded.

• Crystallization strongly purified the target. All completed batches had crystal purity roughly 0.975–1.000 despite substantially lower reaction selectivity. Batch 12, for example, had selectivity 0.571 but crystal purity 1.000. This directly supports selective exclusion of impurities from the recovered solid, although it does not establish a molecular lattice mechanism.

• None of the tested processes solved the fines problem. Final fines fractions were approximately 0.98–1.00 in every batch, far above 0.50. This remained true after direct or staged cooling, long holds, unseeded operation, seed-dose changes, heating, and resuspension. The conclusion is robust within the tested domain.

• Recovery and particle quality remained unresolved competing responses. Batch 12 had the highest recovery, 0.541, and purity 1.000, but fines 1.000. Batch 7 recovered 0.513 with fines 0.987, and batch 8 recovered 0.518 with fines 0.987. Thus higher recovery did not imply acceptable particle quality.

Contradicted in the tested scope

• The initial interpretation that moderate seeding, slow cooling, and holding would suppress fines was contradicted. Batch 1 used that strategy but had fines 0.997; batches 3 and 4 extended or staged the cooling history and still ended near 1.000 fines.

• The revised hypothesis that seed quantity was the missing control was also contradicted. About 1 g total seed in batch 5 gave fines 1.000, while no initial seed in batch 7, 0.005 g in batch 10, and 0.0001 g in batch 11 all remained near 0.99–1.00.

• Selective dissolution or ordinary ripening at 290–310 K was not supported. Within batch 9, particle measurements remained near 0.97–1.00 fines through successive heating. Resuspension/recrystallization then reduced recovery to 0.302 without improving final fines.

Still untested or unresolved

• Whether the fines originated mainly from secondary nucleation, mechanical attrition, intrinsically slow growth, or the supplied seed-size distribution was not determined.

• Separate catalyst and solvent effects remain unresolved because there was no complete factorial design with replication. Even the C0/S0 versus C0/S3 comparison also differed in crystallization history.

• The association between concentration and recovery is not a clean causal result. Batch 12 used less solvent and had the highest recovery, but it also differed in seed dose and temperature history.

• Seed particle size, explicit size classification, alternative agitation schedules during nucleation, antisolvent control, atmosphere, and pressure were not systematically tested. Repeatability is also unknown because there were no true replicate batches.

2. One additional experiment

I would reproduce the concentrated C0/S0 chemistry of batch 12, including the same reaction charge, catalyst, reaction temperature, seed dose, and final temperature, but turn crystallization into a time-resolved agitation-perturbation experiment. After quenching, I would obtain one HPLC measurement to fix the upstream composition. During staged cooling I would make non-destructive particle-size measurements after initial particle appearance, after a long isothermal hold at 100 rpm, after a matched isothermal interval at approximately 1000 rpm, and after returning to 100 rpm. Temperature and composition would otherwise remain unchanged during the agitation perturbation, followed by the usual filtration and final assay.

This would distinguish three leading explanations:

• Attrition-dominated fines: raising agitation at constant temperature should cause an abrupt fall in d50, an increase in fines, and poorer CSD quality. Returning to low agitation would stop further damage but would not rapidly restore the original distribution.

• Supersaturation-driven secondary nucleation: fines should increase mainly during cooling increments, not specifically when agitation changes after an isothermal hold. Once supersaturation is depleted during the hold, the distribution should stabilize or slowly coarsen.

• Growth- or mass-transfer-limited behavior: the low-agitation hold should show gradual size growth and declining fines. Higher agitation might accelerate growth without a fines spike if transport is limiting; that response would oppose the attrition prediction.

If none of these time-resolved signatures appeared and fines were already near unity immediately after adding seed, the seed-size distribution or measurement/model representation would become the leading explanation. The experiment would be more diagnostic than another endpoint-only batch because it provides within-batch comparisons without changing catalyst, solvent, concentration, or impurity inventory.

3. Least effectively used observation and least reliable prediction

The account used the within-batch particle trajectory in batch 1 least effectively. After initial cooling, normalized size increased from about 0.034 to 0.053 and CSD quality from about 0.495 to 0.524 during a hold, while fines remained 1.000. This is stronger evidence than cross-batch comparisons because chemistry and particle population were held constant. It indicates that measurable growth occurred but was insufficient to move a meaningful number fraction across the 20 micrometre threshold. I cited the endpoint failure but did not fully exploit this observation to distinguish “no growth” from “growth without threshold crossing.”

Q03 is the least reliable held-out prediction. I predicted that reducing seed to 0.001 g under an extremely slow S0 cooling schedule could produce a feasible fines fraction. That estimate relied on the interpretation that fewer seeds would provide more solute per particle. However, the campaign supplied contrary prior evidence: 0.005 g in batch 10 and 0.0001 g in batch 11 still produced fines near 1.000, and even unseeded batch 7 remained near 0.987. The held-out schedule is milder and slower than those batches, so the prediction is not impossible, but the claimed feasibility extrapolates beyond the demonstrated evidence. Q01, Q04, Q05, Q07, and Q11 share some of this uncertainty because their predicted feasibility similarly assumes that very slow shallow cooling accesses a coarse-particle regime that the campaign never directly demonstrated.
