# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Scope

The catalyst and solvent labels are anonymous benchmark materials, so this account describes the observed synthetic system rather than a transferable real-chemical mechanism.

## Mechanistic picture

A useful decomposition is

- reaction yield: approximately \(Y_{rxn}\approx X\,S\), where \(X\) is conversion and \(S\) is selectivity;
- crystal yield: \(Y_{cr}=n_{target,solid}/n_{reagent,0}\), excluding seed;
- apparent crystallization capture: \(f_{cap}\approx Y_{cr}/Y_{rxn}\).

Thus overall recovery couples upstream target formation to downstream capture. A solvent can improve reaction yield yet still be unacceptable if crystallization produces too many fines.

For crystallization, the conventional qualitative relations are useful:

\[\sigma=(c-c^*)/c^*,\qquad B\propto\sigma^b,\qquad G\propto\sigma^g,\]

where \(\sigma\) is supersaturation, \(B\) is nucleation rate, and \(G\) is growth rate. Conditions with excessive nucleation relative to growth generate a high number fraction of fines. These equations are interpretations, not fitted laws from this campaign.

## Material effects

### Catalyst

My initial prior favored C1 from its nominal activity dossier, but the experiments revised that view. Under the common S2, 340 K/3,600 s reaction and long cooling protocol:

- batch 2, C0: reaction yield 0.590 and crystal yield 0.503;
- batch 3, C2: reaction yield 0.384 and crystal yield 0.301;
- batch 4, C3: reaction yield 0.484 and crystal yield 0.421.

C0 was therefore the best tested catalyst in that controlled comparison. Batch 1 used C1 and gave reaction yield 0.572 and crystal yield 0.471, but it also used 360 K and a different post-cooling history, so it does not isolate a C0–C1 catalyst effect. The anonymous catalyst residuals evidently mattered more than the nominal reference-panel ranking.

### Solvent

The material dossier characterized S2 as relatively low-solubility, low-nucleation, high-growth, and low-occlusion. The results are broadly consistent with that description: S2 repeatedly gave very high purity and was the only solvent to combine high recovery with an observed fines fraction below 0.50 in the leading process.

Other solvents improved upstream production or nominal recovery but failed the particle constraint:

- batch 6, S3: crystal yield 0.422, purity 0.989, fines 0.644;
- batch 7, S1: crystal yield 0.577, purity 0.976, fines 0.710;
- batch 10, S0: crystal yield 0.564, purity 0.971, fines 0.696.

S1 and S0 therefore formed more target upstream—reaction yields were 0.653 and 0.667, respectively—but their apparent high recovery was coupled to excessive particle counts below 20 µm. My interpretation is that their realized supersaturation/nucleation histories favored many new particles rather than controlled growth. An alternative, not separately tested, is that solvent-specific agglomeration or breakage rather than primary nucleation dominated the number-weighted fines measurement.

## Reaction–crystallization coupling

The recommended batch 12 had conversion 1.000, selectivity 0.588, reaction yield 0.593, and crystal yield 0.524. Its apparent capture fraction was therefore about 0.88. Batch 2, using nearly the same recipe, had reaction yield 0.590 and crystal yield 0.503, corresponding to capture near 0.85. By comparison, S1 batch 8 reached reaction yield 0.630 and crystal yield 0.582, or capture near 0.92, but its fines fraction was 0.713 and therefore disqualified it.

This shows why conversion alone was uninformative: conversion was essentially complete in many batches, while selectivity, solvent-dependent recovery, and particle formation determined whether the product met the objective.

Purity was not the limiting response in the leading S2 region. Batches 1–4 and 11–12 all showed crystal purity around 0.98–1.00. This is consistent with low impurity occlusion in S2, although selective dissolution or rejection during crystallization is an untested alternative explanation.

## Process-history dependence

History mattered substantially:

- Batch 2 used C0/S2, 340 K for 3,600 s, 0.05 g seed, and 14,400 s cooling toward 260 K. It produced crystal yield 0.503, purity 0.982, and fines 0.491.
- Batch 12 repeated that process region and gave the campaign-leading qualifying result: crystal yield 0.524, purity 0.993, and fines 0.489.
- Batch 5 lowered the reaction target to 330 K but doubled the hold to 7,200 s. Recovery fell to 0.407 and fines rose to 1.000. Its degradation warning also increased to 0.171, versus 0.105 in batch 2. This contradicts the original expectation that lower temperature would automatically improve quality; residence time and pathway history appear important.
- Batch 1 underwent cooling followed by a long wait during which the material warmed toward ambient. It gave a lower crystal yield of 0.471 but a substantially lower fines fraction of 0.399. Possible dissolution/ripening during the warm hold is mechanistically plausible, but catalyst, reaction temperature, cooling duration, and hold history were all confounded, so that explanation remains unproven.
- Reducing seed from 0.05 g to 0.005 g did not reduce fines. S1 batches 7 and 8 gave fines of 0.710 and 0.713, respectively. The low-seed S2 batch 11 reached fines of 0.752. In this system, fewer added seeds apparently allowed uncontrolled secondary or primary nucleation rather than directing mass into fewer large crystals.
- A reheat/recool cycle in batch 9 did not rescue S1: recovery remained high at 0.567, but fines increased to 0.750. The tested cycle may have redissolved useful crystals, regenerated supersaturation, or caused renewed nucleation. Other cycle temperatures and durations remain untested.

## Revision of the working model

The original model favored nominally active C1 and S2 and assumed that gentler reaction conditions and less seed might improve quality. The campaign retained S2 but revised the other elements:

1. C0 replaced C1 as the best experimentally supported catalyst.
2. A 340 K/3,600 s reaction was superior to the tested 330 K/7,200 s alternative.
3. The maximum tested seed charge, 0.05 g, was retained because lower seed charges produced more—not fewer—fines.
4. Higher-recovery S0/S1 processes were rejected because recovery could not be separated from their particle-quality failure.

## Uncertainty and unresolved tradeoff

Batch 12 is the largest observed qualifying recovery, but the boundary is not robustly resolved. Its fines fraction was 0.4887, only 0.0113 below the 0.50 limit, while the stated final-assay fines standard deviation was 0.018. Batch 2 was similarly close at 0.4914. Their crystal-yield difference, about 0.021, is modest relative to a 0.01 standard deviation per assay and possible batch variation. Moreover, batch 2 had an upstream HPLC sample removed while batch 12 did not, so they are near-replicates rather than exact replicates.

Batch 1 provides a larger observed fines margin—0.399—but sacrifices recovery, reaching only 0.471. Conversely, S0 and S1 offered crystal yields around 0.56–0.58 but clearly violated the fines constraint. The unresolved engineering question is therefore whether an S2 aging or cooling schedule can retain recovery near or above batch 12 while moving the fines distribution safely below 0.50. Narrow replicated studies of S2 cooling rate, seed timing, controlled aging temperature, and agitation would be more informative than further solvent screening.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.36 | 0.22 | 0.5 |
| Q01 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q01 | crystal_size | 0.15 | 0.09 | 0.23 |
| Q01 | crystal_yield | 0.3 | 0.18 | 0.42 |
| Q02 | crystal_fines_fraction | 0.24 | 0.12 | 0.39 |
| Q02 | crystal_purity | 0.98 | 0.94 | 1 |
| Q02 | crystal_size | 0.2 | 0.12 | 0.3 |
| Q02 | crystal_yield | 0.24 | 0.13 | 0.36 |
| Q03 | crystal_fines_fraction | 0.56 | 0.39 | 0.72 |
| Q03 | crystal_purity | 0.93 | 0.86 | 0.98 |
| Q03 | crystal_size | 0.11 | 0.05 | 0.19 |
| Q03 | crystal_yield | 0.21 | 0.12 | 0.31 |
| Q04 | crystal_fines_fraction | 0.38 | 0.24 | 0.54 |
| Q04 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q04 | crystal_size | 0.16 | 0.09 | 0.24 |
| Q04 | crystal_yield | 0.23 | 0.14 | 0.34 |
| Q05 | crystal_fines_fraction | 0.31 | 0.18 | 0.47 |
| Q05 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q05 | crystal_size | 0.18 | 0.11 | 0.27 |
| Q05 | crystal_yield | 0.23 | 0.14 | 0.34 |
| Q06 | crystal_fines_fraction | 0.72 | 0.56 | 0.86 |
| Q06 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q06 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q06 | crystal_yield | 0.24 | 0.14 | 0.35 |
| Q07 | crystal_fines_fraction | 0.28 | 0.16 | 0.44 |
| Q07 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q07 | crystal_size | 0.2 | 0.12 | 0.3 |
| Q07 | crystal_yield | 0.24 | 0.15 | 0.35 |
| Q08 | crystal_fines_fraction | 0.58 | 0.4 | 0.74 |
| Q08 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q08 | crystal_size | 0.11 | 0.05 | 0.19 |
| Q08 | crystal_yield | 0.17 | 0.08 | 0.28 |
| Q09 | crystal_fines_fraction | 0.93 | 0.78 | 1 |
| Q09 | crystal_purity | 0.97 | 0.88 | 1 |
| Q09 | crystal_size | 0.025 | 0.005 | 0.06 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.72 | 0.53 | 0.88 |
| Q10 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q10 | crystal_size | 0.06 | 0.02 | 0.13 |
| Q10 | crystal_yield | 0.08 | 0.02 | 0.17 |
| Q11 | crystal_fines_fraction | 0.3 | 0.17 | 0.47 |
| Q11 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q11 | crystal_size | 0.18 | 0.1 | 0.27 |
| Q11 | crystal_yield | 0.23 | 0.14 | 0.34 |
| Q12 | crystal_fines_fraction | 0.64 | 0.46 | 0.8 |
| Q12 | crystal_purity | 0.9 | 0.82 | 0.97 |
| Q12 | crystal_size | 0.1 | 0.04 | 0.18 |
| Q12 | crystal_yield | 0.39 | 0.27 | 0.51 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where seed-excluded product recovery is very small. Q01–Q02: S1 is predicted to provide more upstream target formation, while lower-solubility, lower-nucleation S3 should give purer, larger crystals with fewer fines; their opposing reaction and capture effects leave yields relatively close. Q03–Q04: in high-nucleation S0, very low seed loading is expected to permit uncontrolled nucleation, whereas 0.045 g seed better directs supersaturation into growth. Q05–Q06: gradual staged cooling should suppress the supersaturation spike and fines generated by rapid cooling; the common endpoint makes overall yield similar. Q07–Q08: the long monotonic ramp should favor growth, while reheating followed by only a short recooling period risks partial dissolution, incomplete recovery, and renewed nucleation. Q09–Q10: after only 60 seconds, seed-excluded crystallization should be minimal; two additional hours permit some growth and recovery but likely remain fines-rich. Q11–Q12: doubling reagent loading raises supersaturation and absolute crystallization driving force, increasing normalized recovery, but the fixed catalyst charge and higher solids loading are expected to reduce purity and worsen fines. Intervals are intentionally broad because these recipes use much lower concentration, catalyst loading, much longer cooling histories, and a hotter upstream reaction than the completed campaign; uncertainty reflects mechanistic extrapolation and process variability rather than final-assay sampling noise.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **C0 outperformed C2 and C3 under the tested S2 process.** Batches 2–4 used the same nominal reaction and crystallization conditions except catalyst. Crystal yields were 0.503 for C0, 0.301 for C2, and 0.421 for C3. This directly supports C0 over C2/C3 in that scope. It does not establish C0 over C1 because batch 1 used C1 at 360 K with a different cooling/holding history.
- **S2 provided the best observed recovery–quality compromise.** Batches 2 and 12 both met purity and fines specifications, with crystal yields of 0.503 and 0.524 and fines of 0.491 and 0.489. By contrast, S3 batch 6 had fines 0.644, S1 batches 7–9 had fines 0.710–0.750, and S0 batch 10 had fines 0.696. The observation is direct; attributing it specifically to lower nucleation and stronger growth in S2 is mechanistic interpretation.
- **Higher upstream or crystal yield did not guarantee feasibility.** S1 batches 7–8 and S0 batch 10 produced crystal yields around 0.56–0.58 but violated the fines limit. This directly supports treating reaction formation, recovery, and particle quality as coupled but distinct objectives.
- **The tested reheat/recool cycle did not improve S1.** Relative to batch 8, batch 9 had lower crystal yield, 0.567 versus 0.582, and higher fines, 0.750 versus 0.713. This supports rejection of that particular cycle, not all thermal cycling.
- **Reducing seed did not improve S1 particle quality.** Batches 7 and 8 differed principally in seed charge, 0.05 versus 0.005 g, yet fines were essentially unchanged at 0.710 and 0.713. This contradicts the simple expectation that less seed would necessarily produce fewer fines.

### Contradicted or revised

- **The nominal catalyst ranking was contradicted.** The original prior favored C1, but the controlled C0/C2/C3 comparison favored C0. C1 remains incompletely compared rather than definitively inferior.
- **“Lower temperature is gentler and therefore better” was contradicted in the tested implementation.** Batch 5 at 330 K for 7,200 s performed worse than batch 2 at 340 K for 3,600 s: lower crystal yield and fines reported at 1.0. Because temperature and duration changed together, the result contradicts the combined recipe, not lower temperature in isolation.
- **Low seed as a general route to large, low-fines crystals was contradicted by batches 8 and 11.** Batch 11, with 0.005 g seed in S2, had fines 0.752. However, its cooling schedule also differed from batch 2, so the S2 comparison is confounded.

### Still untested or unresolved

- **Ostwald ripening during the warm hold in batch 1 remains untested.** Batch 1 had lower fines, 0.399, after warming toward ambient, but it also differed in catalyst, reaction temperature, cooling duration, and final temperature history.
- **The causal particle mechanism is unresolved.** High fines could reflect primary nucleation, secondary nucleation, breakage, agglomeration behavior, or properties of the seed population. Final number-weighted measurements alone do not separate these mechanisms.
- **The precise C0–C1 comparison is untested.** No otherwise identical C0 and C1 pair was completed.
- **Robust compliance at the selected operating point remains uncertain.** Batches 2 and 12 were below the 0.50 fines limit, but only by 0.009 and 0.011, smaller than the stated 0.018 final-assay noise standard deviation. Batch 12 was numerically best, but its recovery advantage over batch 2 was also modest.

## 2. One additional experiment

I would reproduce batch 12 through its completed 14,400 s cooling step, take a non-destructive particle-size measurement, then apply a controlled warm-aging stage near 298 K for about 7,200 s at low agitation, take a second particle-size measurement, filter, terminate, and perform the final assay.

This within-batch before/after comparison would distinguish three explanations:

1. **Selective dissolution/Ostwald ripening:** fines should fall materially, normalized size should rise, and crystal yield may decline modestly as the smallest crystals dissolve. Purity should remain high or improve.
2. **Secondary nucleation or attrition during reheating/agitation:** fines should rise and size or CSD quality should deteriorate, potentially resembling the adverse thermal-cycle result in batch 9.
3. **Batch-1 confounding or measurement variation:** particle metrics should change little, implying that batch 1’s lower fines were more likely due to its catalyst/reaction history or noise rather than its warm hold.

Using the same batch before and after aging would be more discriminating than comparing two terminal batches because it controls upstream composition, seed charge, and initial crystal population.

## 3. Least effectively used evidence and least reliable prediction

The account used the **paired in-process and final particle observations from batch 1** least effectively. Before filtration, particle imaging reported fines about 0.423 and normalized size about 0.061; the final assay reported fines about 0.399 and size about 0.075. I relied mainly on the final values and the warm-history narrative. The difference is comparable to measurement uncertainty and should have been used more explicitly to show that the apparent fines improvement might be analytical variation rather than physical ripening.

The least reliable held-out prediction is **Q09**. It terminates only 60 seconds after initiating cooling to 292 K, a regime far outside the campaign’s multi-hour crystallizations. The solid population would be dominated by the introduced seed, while seed-excluded target deposition could be nearly zero. No campaign observation characterized the initial seed size distribution or minute-scale nucleation and growth, so the predicted size and fines depend heavily on unverified assumptions about how the benchmark represents seed particles. The prediction that particles are present is comparatively secure because seed is added; the numerical yield, size, and fines estimates are not.
