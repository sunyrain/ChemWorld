# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

The strongest empirical material combination was catalyst C1 with solvent S2. S2 had been expected to favor crystallization because its public dossier assigned it relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The recovery results were broadly consistent with the solubility/growth part of that prior: several C1/S2 batches produced seed-excluded crystal yields near 0.52–0.56, and batch 12 reached 0.593. Purities were generally 0.98–1.00. However, the predicted control of nucleation was not realized: all S2 processes still produced overwhelmingly sub-20-µm particles.

Single-solvent comparisons suggest, but do not prove, an S2 recovery advantage. Batch 10 with S3 gave crystal yield 0.391 and purity 0.975; batch 11 with S0 gave 0.470 and 0.994; batch 4 with S1 gave 0.585 and purity 1.00. Batch 4 shows that S1 may also be competitive. These batches had different thermal histories, so the numerical differences cannot be assigned solely to solvent.

Catalyst C1 was used in most informative batches and gave high conversion, typically about 0.98–1.00. Catalyst C3 was tested in batch 9, but that batch also underwent filtration, resuspension, and recrystallization. Its final selectivity was only 0.492 and crystal yield 0.460, so it did not motivate replacing C1; nevertheless, the catalyst effect remains confounded by the extra processing.

### 2. Reaction mechanism and temperature effects

A useful empirical representation is

r_target = k_target(C,S,T)[R],

r_byproduct = k_byproduct(C,S,T)[R],

with conversion governed by the sum of productive and competing rates and selectivity approximately

S_target = k_target/(k_target + k_byproduct + k_degradation).

The experiments indicate that heating readily drove conversion close to unity, but greater thermal severity did not translate proportionally into isolated target. For example, batch 1 at 360 K for 1,800 s had conversion 1.00, reaction yield 0.650, selectivity 0.652, byproduct signal 0.227, and degradation warning 0.086. Batch 2 at 345 K for 1,200 s still reached conversion 0.999, with reaction yield 0.623 and a lower degradation warning of 0.041. This supports a fast reaction with parallel byproduct/degradation pathways that become more consequential with severe histories, although solvent and subsequent histories prevent a clean Arrhenius fit.

### 3. Reaction–crystallization coupling

Crystal yield was seed-excluded target solid divided by initial reagent charge, so it includes both chemical formation and physical recovery. A useful mass-balance decomposition is

Y_crystal ≈ X · S_target · f_survival · f_solid_capture,

or, using the measured reaction yield,

Y_crystal ≈ Y_reaction · f_solid_capture.

For batch 12, Y_crystal = 0.593 and Y_reaction = 0.629, suggesting an apparent solid-capture fraction near 0.94. For batch 1, the corresponding ratio was about 0.86. These ratios are approximate because both channels are noisy processed estimates, but they show that reaction formation and crystallization recovery were both consequential.

Purity and recovery were not tightly opposed in the tested region. Even when reaction byproduct signals were around 0.18–0.23, isolated crystals often assayed near 0.99 purity. This is consistent with preferential target crystallization and rejection of soluble impurities into the mother liquor. The unresolved tradeoff instead involved recovery versus particle-number quality: deeper cooling increased solid capture, but also promoted many new particles, leaving almost all particles below 20 µm.

### 4. Nucleation, growth, and process-history dependence

A standard population-balance interpretation is useful:

∂n(L,t)/∂t + G(S,T)∂n(L,t)/∂L = B(S,T)δ(L−L0) − loss/agglomeration terms,

where supersaturation S drives both growth G and nucleation B. The data imply that B increased too strongly relative to G during cooling. Because the reported size is number-weighted, even a modest mass of newly nucleated fines can dominate both d50 and the sub-20-µm number fraction.

All final size indices were below about 0.065. Since the size index equals min(d50/250 µm,1), the largest observed final d50 values were only about 15–16 µm. A number-weighted d50 below 20 µm itself implies that at least half the population lies below 20 µm, so it is structurally inconsistent with satisfying a fines fraction below 0.50. In practice the measured fines fractions were much worse—approximately 0.987–1.00.

Seeding did not solve this problem:

- Batch 3 used 0.001 g seed and finished with size index 0.0208, fines 0.995, and crystal yield 0.508.
- Batch 5 used 0.05 g seed and finished with size index 0.0151, fines 1.00, and yield 0.542.
- Batch 2 was unseeded and had a larger size index, 0.0609, but still fines 1.00 and yield 0.549.

These observations contradict the initial expectation that modest seeding plus slow cooling would suppress fines. One interpretation is that the added seed population was itself numerous on a number basis, or that it did not prevent secondary nucleation. Seed size distribution was not independently characterized, so those alternatives cannot be separated.

Thermal history was strongly path-dependent. In batch 7, the in-process size index was about 0.0357 at 298 K with fines 1.00; after further cooling to 285 K and holding, it fell to about 0.0020, consistent with a burst of secondary nucleation dominating the number distribution. Batch 12 used a very small effective seed and exceptionally slow stepped cooling. Its size index rose from 0.0111 near 298 K to 0.0647 near 251 K, showing that slow staged cooling could promote growth. Nevertheless, fines remained 0.992. Ten additional low-temperature holds then reduced the measured size index to 0.0341 and returned fines to 1.00, again indicating continued nucleation or attrition rather than clean ripening. Subsequent reheating and recooling produced a final size index of 0.0530 and fines 1.00.

Batch 9 tested filtration, resuspension in S2, heating, slow recooling, and refiltration. Its final size index was only 0.0163 and yield fell to 0.460. Thus the attempted recrystallization sacrificed recovery without establishing a particle-quality benefit.

### 5. Revisions and uncertainty

The initial working hypothesis was that C1/S2, modest seed, slow cooling, and a growth hold would exceed the recovery threshold while satisfying purity and fines specifications. Recovery and purity were indeed strong, but the fines prediction was decisively rejected over the tested range. A second expectation—that longer holds or reheating would selectively dissolve fines and enlarge surviving crystals—was also not supported. Batch 12 briefly showed improved size during stepped cooling, but neither prolonged holding nor a reheat/recool cycle crossed the 20-µm median threshold.

Instrument noise can explain small differences between particle-size readings and final assays, but it cannot plausibly explain fines values consistently near one rather than below 0.50. By contrast, rankings involving similar recoveries or purities should remain tentative because most recipes were not replicated and multiple factors changed together.

### 6. Unresolved tradeoff and untested alternatives

No completed batch met both purity ≥0.80 and fines ≤0.50. Batch 12 had the highest observed recovery, 0.593, and purity 1.00, but fines 1.00; it is therefore a high-recovery, non-feasible process rather than a quality-qualified optimum.

The campaign did not test several potentially important alternatives: controlled reagent feeding to cap supersaturation, solvent mixtures or antisolvent trajectories, independently characterized coarse seeds, deliberate particle classification or fines removal, substantially different hydrodynamics, or direct feedback from an in-process supersaturation measurement. Those routes could alter the balance between nucleation and growth. The available evidence supports S2/C1 for recovery but does not establish any feasible method for meeting the particle-number constraint.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.97 | 0.84 | 1 |
| Q01 | crystal_purity | 0.982 | 0.93 | 1 |
| Q01 | crystal_size | 0.02 | 0.006 | 0.045 |
| Q01 | crystal_yield | 0.52 | 0.4 | 0.63 |
| Q02 | crystal_fines_fraction | 0.99 | 0.9 | 1 |
| Q02 | crystal_purity | 0.955 | 0.87 | 0.995 |
| Q02 | crystal_size | 0.012 | 0.002 | 0.032 |
| Q02 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q03 | crystal_fines_fraction | 0.93 | 0.7 | 1 |
| Q03 | crystal_purity | 0.968 | 0.9 | 1 |
| Q03 | crystal_size | 0.042 | 0.015 | 0.085 |
| Q03 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q04 | crystal_fines_fraction | 0.99 | 0.91 | 1 |
| Q04 | crystal_purity | 0.965 | 0.89 | 1 |
| Q04 | crystal_size | 0.012 | 0.003 | 0.032 |
| Q04 | crystal_yield | 0.41 | 0.3 | 0.52 |
| Q05 | crystal_fines_fraction | 0.985 | 0.88 | 1 |
| Q05 | crystal_purity | 0.967 | 0.9 | 1 |
| Q05 | crystal_size | 0.016 | 0.005 | 0.039 |
| Q05 | crystal_yield | 0.42 | 0.31 | 0.54 |
| Q06 | crystal_fines_fraction | 0.997 | 0.94 | 1 |
| Q06 | crystal_purity | 0.953 | 0.86 | 0.997 |
| Q06 | crystal_size | 0.007 | 0.001 | 0.022 |
| Q06 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q07 | crystal_fines_fraction | 0.982 | 0.86 | 1 |
| Q07 | crystal_purity | 0.968 | 0.9 | 1 |
| Q07 | crystal_size | 0.017 | 0.006 | 0.041 |
| Q07 | crystal_yield | 0.43 | 0.32 | 0.55 |
| Q08 | crystal_fines_fraction | 0.97 | 0.82 | 1 |
| Q08 | crystal_purity | 0.98 | 0.92 | 1 |
| Q08 | crystal_size | 0.025 | 0.008 | 0.055 |
| Q08 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q09 | crystal_fines_fraction | 0.998 | 0.95 | 1 |
| Q09 | crystal_purity | 0.985 | 0.92 | 1 |
| Q09 | crystal_size | 0.006 | 0.001 | 0.018 |
| Q09 | crystal_yield | 0.14 | 0.05 | 0.27 |
| Q10 | crystal_fines_fraction | 0.991 | 0.9 | 1 |
| Q10 | crystal_purity | 0.975 | 0.89 | 1 |
| Q10 | crystal_size | 0.013 | 0.003 | 0.034 |
| Q10 | crystal_yield | 0.3 | 0.17 | 0.44 |
| Q11 | crystal_fines_fraction | 0.989 | 0.9 | 1 |
| Q11 | crystal_purity | 0.966 | 0.89 | 1 |
| Q11 | crystal_size | 0.014 | 0.004 | 0.036 |
| Q11 | crystal_yield | 0.42 | 0.31 | 0.54 |
| Q12 | crystal_fines_fraction | 0.975 | 0.82 | 1 |
| Q12 | crystal_purity | 0.947 | 0.84 | 0.995 |
| Q12 | crystal_size | 0.02 | 0.006 | 0.048 |
| Q12 | crystal_yield | 0.53 | 0.4 | 0.65 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain effective seeding and cooling, so particles are expected. The campaign showed consistently high crystal purity but number-weighted d50 below 20 µm and fines near unity; therefore none is predicted quality-feasible. Q01 versus Q02 favors S1 over S3 for recovery, purity and growth, based on the observed solvent trend, though the intervals overlap. Q03 versus Q04 assigns the smaller seed charge fewer nuclei and hence larger particles and fewer fines, with slightly lower capture. Q05 versus Q06 favors staged cooling for size and fines control; the rapid initial crash should nucleate many fines, while final recovery may be similar. Q07 versus Q08 treats reheating as partial dissolution/ripening that may enlarge survivors and improve purity but lowers recovery; rapid recooling can still regenerate fines. Q09 versus Q10 predicts that two additional hours at 292 K substantially increase deposition and recovery, but not enough to remove the number-dominant fines population. Q11 versus Q12 predicts higher loading increases fractional solid recovery and mass available per seed, while greater supersaturation raises occlusion and secondary-nucleation risk. Intervals are broad because these recipes use smaller, more dilute charges, 385 K reaction histories, and seed-to-product ratios outside the main campaign region.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Purity was not the binding constraint.** The leading batches had final crystal purity near 0.98–1.00: batch 1 was 0.992, batch 4 was 1.00, batch 8 was 0.985, and batch 12 was 1.00. Interpreting this as preferential crystallization with impurity rejection is plausible, but only the high-purity result is directly observed.
- **The fines constraint was consistently missed.** Every completed final assay reported a fines fraction around 0.987–1.00. Final size indices were below about 0.065, corresponding to number-weighted d50 values below roughly 16 µm. Thus the direct observations establish that none of the tested processes met fines ≤0.50.
- **Reaction conversion was generally high while isolated recovery remained lower.** For example, batch 1 had conversion 1.00, reaction yield 0.650 and crystal yield 0.561; batch 12 had conversion 1.00, reaction yield 0.629 and crystal yield 0.593. The decomposition into reaction formation and solid capture is an interpretation of those measurements, not a separately measured mechanism.
- **Process history mattered.** In batch 12, the particle-size index increased from about 0.011 near 298 K to 0.065 near 251 K during stepped cooling, then fell to about 0.034 after prolonged low-temperature holding. Batch 7 similarly showed a much smaller particle-size reading after further cooling and holding. These are direct temporal observations consistent with changing particle populations.

### Contradicted or substantially weakened

- **The initial claim that modest seeding plus slow cooling would deliver acceptable fines was contradicted.** Batch 3 used 0.001 g seed and finished with fines 0.995; batch 5 used 0.05 g and finished at 1.00. Unseeded batch 2 also finished at 1.00, so neither tested seed level nor omission of seed solved the problem.
- **The expectation that long holds would mainly grow existing crystals was contradicted over the tested conditions.** The extended history in batch 6 produced a final size index of only 0.0105. In batch 12, prolonged low-temperature holding worsened rather than improved the measured number distribution.
- **Reheating or recrystallization as a reliable fines-removal step was not supported.** Batch 9 underwent filtration, resuspension, heating and recooling but ended with size index 0.0163 and crystal yield 0.460. Batch 12’s final reheat/recool cycle still gave fines 1.00.
- **A strong claim that S2 uniquely controls nucleation is contradicted by the fines data.** S2 often supported good recovery, but S2 batches still produced nearly all fines.

### Still untested or unresolved

- **The cause of the fines population remains unresolved.** Secondary nucleation during cooling is a reasonable interpretation, but the experiments did not independently characterize the seed-size distribution, particle number immediately after seeding, agglomeration, or attrition. Seed-derived fines, secondary nucleation and agitation-induced breakage therefore remain competing explanations.
- **Solvent causality is unresolved.** Batch 4 with S1 achieved crystal yield 0.585 and purity 1.00, close to the strongest S2 results. S0 and S3 performed less well in batches 11 and 10, but their histories were not exact matched controls and none was replicated.
- **Catalyst ranking is unresolved.** C1 dominated the study. The C3 result in batch 9 was confounded by resuspension and recrystallization.
- **The proposed population-balance and parallel-reaction equations are organizing models, not fitted laws.** No kinetic coefficients, nucleation order or growth law was identified.
- Controlled feeding, solvent mixtures, independently characterized coarse seeds, particle classification and substantially different hydrodynamics were not tested.

## 2. One additional experiment

I would repeat a C1/S2 process close to batch 12 but use a deliberately diagnostic history: the same small effective seed and slow stepped cooling, non-destructive particle measurements immediately after seeding and at several cooling stages, followed by one isothermal hold at the temperature where size first peaks, then immediate filtration and final assay. I would avoid the subsequent deep hold and reheat/recool sequence.

This single time-resolved experiment would distinguish three explanations:

1. **Seed population dominates:** fines are already high immediately after seeding and change little during cooling. The remedy would require a different, coarser seed distribution rather than merely slower cooling.
2. **Secondary nucleation dominates:** the initial seeded population is relatively coarse, but fines rise sharply after a particular temperature or supersaturation threshold. Earlier stopping should reduce recovery but materially improve fines.
3. **Isothermal attrition or continued nucleation dominates:** staged cooling initially improves size, but the fixed-temperature hold causes size to fall and fines to rise. If agitation is responsible, the deterioration should accompany accumulated stirred time even without an additional temperature drop.

The most favorable outcome would be a size index above 0.08 and fines below 0.50 before the deep-cooling region, probably with lower crystal yield than batch 12. If fines are already near one immediately after seeding, the current seed operation itself is implicated. If fines appear only after cooling or holding, the experiment would identify the process stage that creates them.

## 3. Least-used observation and least-reliable prediction

The account used **batch 4** least effectively. Its S1 result—crystal yield 0.585, purity 1.00 and reaction yield 0.660—was nearly as strong as the best S2 recovery results. That observation should prevent a confident claim that S2 is the uniquely preferred recovery solvent. Because batch 4 was not a matched or replicated comparison, it cannot establish S1 superiority either, but it materially weakens the solvent ranking.

The least reliable held-out prediction is **Q09**. It filters only 60 seconds after a rapid drop to 292 K. None of the campaign batches directly constrained seed-excluded target deposition on that time scale, especially with the much smaller and more dilute charge used in the held-out recipe. The prediction therefore extrapolated both short-time crystallization kinetics and the distinction between merely present seed particles and newly recovered target product. Particle presence is comparatively credible because seed was added, but the predicted crystal yield, size and fines intervals are much less reliable. No held-out truth has been supplied, so this is an uncertainty assessment rather than a revision of the sealed prediction.
