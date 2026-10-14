# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Overall picture
The data support a coupled process in which solvent and catalyst determine how much target product is present after reaction, while the resulting product concentration and the subsequent supersaturation history determine how much of that product is recovered as acceptably coarse crystals. Crystal purity was consistently high after isolation; the difficult constraint was the number fraction of particles below 20 µm.

A useful empirical decomposition is

**crystal yield ≈ reaction-stage target yield × crystallization capture fraction.**

For batches 1, 8, 9, 10, 11, and 12, the observed ratio of crystal yield to final-assay target yield was approximately 0.80, 0.84, 0.84, 0.84, 0.85, and 0.79, respectively. Thus most of the improvement through batch 10 came from increasing upstream target formation, while crystallization usually captured roughly four-fifths of that target. This is an empirical relationship, not a proven mass-balance law.

### Material effects
The nominal dossier initially suggested S2 because it combined low solubility, high growth tendency, low nucleation tendency, and low impurity occlusion. Experiments revised that expectation. With C1 at 370 K, S1 produced substantially more target and crystal recovery than S2: batch 7 gave final target yield 0.568 and crystal yield 0.469, compared with batch 1 at 0.496 and 0.399. S1 therefore appears to improve reaction selectivity enough to outweigh its less favorable nominal solubility relative to S2.

The comparison also demonstrates solvent coupling: S1 improved recovery but batch 7 had excessive fines (0.539), whereas batch 1 with S2 had fines of 0.404. Changing solvent affected both reaction chemistry and nucleation/growth, so these observations cannot be assigned solely to solubility.

S3 was unfavorable in the tested history. Batch 6 had final target yield 0.479, crystal yield 0.379, and fines 0.738 despite high nominal reference activity. This suggests that its realized world-specific behavior and stronger nucleation/occlusion tendencies outweighed the nominal activity advantage. S0 was not tested, and the solvent screen was not a replicated full factorial.

Within S2 at 370 K, the catalyst screen gave crystal yields of 0.399 for C1 (batch 1), 0.387 for C0 (batch 3), 0.358 for C2 (batch 4), and 0.392 for C3 (batch 5). C1 was therefore retained, although C0 and C3 were close enough that single-run differences should not be interpreted as a precise catalyst ranking. Catalyst-by-solvent interactions remain untested.

### Reaction behavior and its coupling to crystallization
A minimal conceptual reaction model is

**dR/dt = −k(T,C,S)R**

**dP/dt = k₁(T,C,S)R − k₂(T,C,S)P**, 

where the second term represents conversion of target product to byproducts or degradation products. The experiments do not identify these rate laws, but they explain why temperature and residence time must be considered together rather than independently.

At 370 K for 3600 s with S1/C1, batches 7–8 gave final target yields near 0.565. Raising the reaction temperature while shortening residence time improved target production: batch 9 at 390 K for 2400 s gave final target yield 0.637, while batch 10 at 410 K for 1800 s gave 0.687. HPLC showed the same direction: approximately 0.643 target yield for batch 9 and 0.705 for batch 10. The interpretation is that a hotter, shorter reaction reached high conversion while limiting residence in slower competing pathways. This is a local empirical trend, not evidence that still higher temperature would continue to help.

The benefit carried into crystallization: crystal yield increased from 0.476 in batch 8 to 0.535 in batch 9 and 0.578 in batch 10. However, the greater target concentration also plausibly raised supersaturation during cooling, increasing nucleation and hence fines. Batch 10 had the highest recovery but failed the fines constraint at 0.524.

HPLC and final assays were taken at different process states and have independent noise. Some reaction or degradation could also continue during later thermal operations. Their numerical differences should therefore not be treated as direct instrument bias.

### Crystallization mechanism and process-history dependence
A useful qualitative framework is supersaturation

**σ = (C − C*)/C***,

with nucleation and growth represented schematically as

**B ∝ σᵇ** and **G ∝ σᵍ**.

Rapid creation of high supersaturation favors many nuclei and a high number fraction of fines; lower, sustained supersaturation favors growth on existing crystals. Agitation, secondary nucleation, seed survival, and temperature-dependent solubility can all modify this simple picture.

The first S1 process used 0.02 g seed and gave good recovery but excessive fines in batch 7. Increasing seed to 0.05 g and extending slow cooling/low-agitation aging produced batch 8 with crystal yield 0.476, purity 0.980, and fines 0.449. The interpretation was that more growth surface and a longer maturation history reduced spontaneous or secondary nucleation. Because seed was introduced while the mixture was still hot, partial seed dissolution is an unresolved alternative explanation; the effective surviving seed population was not measured.

Batch 9 retained that crystallization strategy after the 390 K reaction and achieved crystal yield 0.535, purity 0.984, and fines 0.459. It is the sealed recommendation and the best completed batch satisfying both constraints.

Particle quality was nevertheless history-sensitive. Batch 10 used a similar nominal crystallization program after the more productive 410 K reaction but gave fines of 0.524. This supports a recovery–quality tradeoff: more target was available for crystallization, but the corresponding supersaturation apparently crossed into a stronger nucleation regime.

Reheating and recooling did not resolve that tradeoff in the tested forms. In batch 11, particle imaging before intervention showed fines of 0.517. Mild reheating to 310 K followed by recooling and aging only reduced the final-assay value to 0.508, while crystal yield was 0.545. Batch 12 used staged cooling followed by a stronger 330 K reheat, additional seeding, and recooling; it ended with lower crystal yield, 0.505, and much worse fines, 0.693. Thus the original idea that selective dissolution of fines would provide effective Ostwald ripening was revised and rejected for these particular histories. Possible explanations include renewed nucleation during recooling, excessive seed-derived particle counts, or incomplete dissolution of the fine population.

Passive waiting also allowed temperature to return toward ambient rather than maintaining the cooling endpoint. Any apparent aging benefit therefore combines time, warming, dissolution, and growth; those effects were not separated.

### Quality/recovery tradeoff and uncertainty
Purity was not limiting: isolated-crystal purities were generally about 0.98–1.00, comfortably above 0.80. Fines were the active constraint. Batch 9 was only about 0.041 below the 0.50 limit, while batch 10 was about 0.024 above it. Given the stated final-assay fines noise of roughly 0.018 and the observed between-batch process variation, batch 9 should be regarded as feasible but not yet robustly validated.

There were no exact process replicates, and most material comparisons were single batches. Differences therefore combine recipe effects, process-history differences, and analytical noise. The contrast between batches 9 and 10 is mechanistically plausible, but it does not establish a sharp temperature threshold. Likewise, the catalyst ranking and the improvement attributed to seed dose require replication.

The most important untested alternatives are: exact replication of batch 9; a finer temperature/residence-time map between 390 and 410 K; controlled low-supersaturation cooling without passive warming; adjustment of cooling rate to the higher product concentration; variation of seed timing, size distribution, and dose; agitation-rate studies to limit secondary nucleation; lower catalyst loading; S0; and catalyst-by-solvent interactions. These could potentially retain the recovery advantage of batch 10 while restoring fines below 0.50, but the completed campaign does not demonstrate that outcome.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.19 | 0.08 | 0.34 |
| Q01 | crystal_purity | 0.982 | 0.955 | 0.997 |
| Q01 | crystal_size | 0.36 | 0.24 | 0.49 |
| Q01 | crystal_yield | 0.535 | 0.43 | 0.63 |
| Q02 | crystal_fines_fraction | 0.31 | 0.16 | 0.49 |
| Q02 | crystal_purity | 0.968 | 0.925 | 0.994 |
| Q02 | crystal_size | 0.29 | 0.17 | 0.43 |
| Q02 | crystal_yield | 0.425 | 0.31 | 0.54 |
| Q03 | crystal_fines_fraction | 0.62 | 0.43 | 0.79 |
| Q03 | crystal_purity | 0.935 | 0.86 | 0.98 |
| Q03 | crystal_size | 0.16 | 0.07 | 0.28 |
| Q03 | crystal_yield | 0.335 | 0.22 | 0.45 |
| Q04 | crystal_fines_fraction | 0.37 | 0.22 | 0.55 |
| Q04 | crystal_purity | 0.956 | 0.9 | 0.989 |
| Q04 | crystal_size | 0.28 | 0.17 | 0.41 |
| Q04 | crystal_yield | 0.365 | 0.25 | 0.48 |
| Q05 | crystal_fines_fraction | 0.36 | 0.21 | 0.54 |
| Q05 | crystal_purity | 0.954 | 0.895 | 0.989 |
| Q05 | crystal_size | 0.29 | 0.18 | 0.42 |
| Q05 | crystal_yield | 0.365 | 0.25 | 0.48 |
| Q06 | crystal_fines_fraction | 0.61 | 0.43 | 0.78 |
| Q06 | crystal_purity | 0.925 | 0.84 | 0.975 |
| Q06 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q06 | crystal_yield | 0.375 | 0.25 | 0.5 |
| Q07 | crystal_fines_fraction | 0.35 | 0.2 | 0.53 |
| Q07 | crystal_purity | 0.953 | 0.895 | 0.989 |
| Q07 | crystal_size | 0.3 | 0.18 | 0.43 |
| Q07 | crystal_yield | 0.37 | 0.25 | 0.49 |
| Q08 | crystal_fines_fraction | 0.57 | 0.38 | 0.75 |
| Q08 | crystal_purity | 0.965 | 0.91 | 0.994 |
| Q08 | crystal_size | 0.27 | 0.15 | 0.41 |
| Q08 | crystal_yield | 0.315 | 0.2 | 0.44 |
| Q09 | crystal_fines_fraction | 0.78 | 0.6 | 0.91 |
| Q09 | crystal_purity | 0.94 | 0.82 | 0.99 |
| Q09 | crystal_size | 0.055 | 0.015 | 0.13 |
| Q09 | crystal_yield | 0.045 | 0.005 | 0.12 |
| Q10 | crystal_fines_fraction | 0.59 | 0.4 | 0.77 |
| Q10 | crystal_purity | 0.945 | 0.865 | 0.987 |
| Q10 | crystal_size | 0.105 | 0.04 | 0.21 |
| Q10 | crystal_yield | 0.18 | 0.09 | 0.29 |
| Q11 | crystal_fines_fraction | 0.36 | 0.21 | 0.54 |
| Q11 | crystal_purity | 0.955 | 0.895 | 0.99 |
| Q11 | crystal_size | 0.285 | 0.17 | 0.42 |
| Q11 | crystal_yield | 0.37 | 0.25 | 0.49 |
| Q12 | crystal_fines_fraction | 0.53 | 0.34 | 0.71 |
| Q12 | crystal_purity | 0.925 | 0.84 | 0.977 |
| Q12 | crystal_size | 0.23 | 0.12 | 0.37 |
| Q12 | crystal_yield | 0.425 | 0.29 | 0.56 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is predicted to outperform S3 in recovery and particle quality, consistent with the campaign solvent comparison and S1's lower nominal solubility/nucleation and occlusion tendencies. Q03–Q04: increasing seed from 0.001 to 0.045 g should suppress uncontrolled nucleation and fines, with only a modest recovery change. Q05–Q06: gradual cooling should produce larger crystals and fewer fines than a 120 s crash; the long final hold makes total recovery similar. Q07–Q08: the 315 K reheat followed by rapid recooling is expected to dissolve some product and trigger renewed nucleation, lowering recovery and worsening fines, as observed qualitatively in campaign reheating trials. Q09–Q10: particles are expected because seed was added, but the 60 s process gives little seed-excluded recovery; two additional hours at 292 K permit appreciable growth while probably remaining fines-limited. Q11–Q12: doubling reagent loading raises supersaturation and likely recovery, but reduces normalized catalyst loading and increases nucleation/occlusion, creating a fines and purity tradeoff. Intervals are intentionally broad because S0 was untested in the campaign, these cooling programs are far longer than the explored histories, and no exact recipe replicates separated process variability from analytical noise.

## K2

## 1. Status of the main claims

### Supported within the tested scope
- **S1 was the strongest tested solvent for recovery.** Directly observed: with C1 at 370 K, batch 7 gave crystal yield 0.469 versus 0.399 for S2 in batch 1; S3 gave only 0.379 with fines 0.738 in batch 6. Interpretation: S1’s reaction advantage outweighed S2’s nominal crystallization advantages. This is not a complete solvent ranking because S0 was never tested and the comparisons were unreplicated.
- **Hotter, shorter reactions improved target production over the tested range.** Directly observed: final target/crystal yields rose from approximately 0.565/0.476 in batch 8 at 370 K for 3600 s, to 0.637/0.535 in batch 9 at 390 K for 2400 s, and 0.687/0.578 in batch 10 at 410 K for 1800 s. Interpretation: higher temperature accelerated productive conversion relative to competing pathways. Temperature and time changed together, so separate kinetic effects remain unresolved.
- **Fines, rather than purity, were the binding quality constraint.** All isolated-crystal purities were about 0.98–1.00, while fines crossed the 0.50 boundary repeatedly: batches 8 and 9 passed at 0.449 and 0.459, whereas batches 10–12 failed at 0.524, 0.508, and 0.693.
- **Process history strongly affected particle quality.** Batch 7 failed the fines criterion at 0.539, while batch 8 passed at 0.449 after increasing seed and extending cooling/aging. This directly establishes a numerical history dependence, although it does not isolate seed dose from cooling duration or random variation.
- **The tested reheating strategies did not rescue quality.** Batch 11 had particle-imaging fines of 0.517 before mild reheating and final-assay fines of 0.508 afterward; batch 12 ended at 0.693 after stronger reheating and recooling. The direct evidence supports “no demonstrated rescue,” not a universal claim that annealing cannot work.

### Contradicted or revised
- **The initial expectation that S2 would be best overall was contradicted.** Its favorable nominal solubility, growth, nucleation, and occlusion properties did not compensate for S1’s better realized target formation.
- **The proposed simple Ostwald-ripening remedy was contradicted in its tested forms.** Mild reheating produced, at most, a small ambiguous improvement in batch 11, and the stronger sequence in batch 12 substantially worsened fines and reduced recovery.
- **The idea that the 0.05 g seed/long-aging program would robustly ensure compliant fines was contradicted by batch 10.** Batches 8 and 9 passed, but batch 10 failed under a broadly similar crystallization program. Higher upstream product concentration or ordinary process variability could explain the difference.
- **Maximum recovery was not equivalent to the best feasible outcome.** Batch 10 had the largest crystal yield, 0.578, but failed the fines constraint; batch 9 remained the best feasible batch.

### Still untested
The campaign did not establish a rate law, directly measure supersaturation, identify degradation pathways, or determine whether seeds partially dissolved at the hot addition temperature. S0, catalyst–solvent interactions, seed-size distribution, exact recipe replication, isolated effects of seed dose and cooling duration, controlled agitation effects, doubled reagent loading, crash cooling, and the very long multistep cooling programs in the held-out set all remain untested.

## 2. One additional experiment

I would run an **exact replicate of batch 10**, retaining S1/C1, 410 K for 1800 s, 0.05 g seed, and the same cooling and aging program. I would add an HPLC measurement immediately after quench and a particle-size measurement immediately before filtration.

This would distinguish two leading explanations for the batch 9–10 difference:

1. **Systematic supersaturation coupling:** the 410 K reaction consistently produces more target, and that higher concentration systematically causes excess nucleation during the fixed cooling program.
2. **Run-to-run particle variability:** batch 10’s fines failure was stochastic or caused by an uncontrolled history detail rather than the higher upstream yield.

Expected outcomes:
- If the replicate again shows high upstream target yield near batch 10 and fines above 0.50, the systematic coupling explanation is strengthened.
- If it retains high target yield but gives fines near batch 9, process variability is the better explanation and the 410 K process may be feasible but insufficiently robust.
- If lower upstream target yield is accompanied by lower fines, that would support a concentration–supersaturation relationship without proving its functional form.
- If particle imaging passes but final assay fails, sampling or filtration history would become a leading explanation.

An exact replicate is more informative than introducing another optimization variable because the main unresolved issue is reproducibility at the quality boundary.

## 3. Least effectively used evidence and least reliable prediction

The account used the **intermediate particle-size observation from batch 11** least effectively. Fines changed from 0.517 before reheating to 0.508 in the final assay. I grouped this with batch 12 as evidence against reheating, but the batch-11 change was small, came from different instruments/process times, and was directionally favorable. The defensible conclusion is only that mild reheating did not produce a sufficiently large, clearly resolved improvement. It does not show that the intervention worsened fines.

The least reliable held-out prediction is **Q09**. It combines several extrapolations absent from the campaign: S0, a tenfold smaller reagent charge, lower relative catalyst loading, and only 60 seconds of cooling before filtration. Its solid population may be dominated by introduced seed rather than newly crystallized target, making particle presence, seed-excluded yield, size, and fines unusually sensitive to how seed survival and counting are represented. The campaign contained no comparably short crystallization history, so both the point estimates and the assumed particles-present classification for Q09 are less secure than those for the long-cooling queries.
