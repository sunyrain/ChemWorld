# C-W01-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Decision context
The sealed recommendation remains **batch 11**, because it was the only completed batch satisfying both formal constraints: crystal purity ≥0.80 and number fraction below 20 µm ≤0.50. Its final assay gave purity 1.00 and fines 0.00. However, its seed-excluded crystal recovery was only 8.3×10⁻⁶, so it did not reach the 0.10 feasibility target. No tested batch combined acceptable fines with practically useful recovery.

### Reaction and material effects
The reaction was generally conversion-rich but only moderately selective at full loading. With catalyst C1 in S2 at 360 K for 3600 s, batch 1 showed conversion 1.00, selectivity about 0.59, reaction yield about 0.59, and degradation warning about 0.18. Batch 2 was similar. Thus, longer/hotter operation with C1 apparently drove reagent consumption to completion without preventing byproduct formation.

Changing to catalyst C3 and a milder 350 K, 2400 s reaction improved the observed degradation profile. For example, S2 batch 4 had conversion 0.989, selectivity 0.609, yield 0.595, and degradation warning 0.088. Later C3/S2 batches generally retained near-complete conversion with degradation warnings around 0.09–0.11. I interpret this as evidence that C3 under the milder history better limited degradation, although catalyst, temperature, time, seeding, and crystallization history were changed together, so the catalyst effect was not isolated.

Solvent affected both reaction composition and recovery, but it did not solve the fines problem under direct crystallization. Representative full-loading C3 results were:

- **S2, batch 4:** crystal recovery 0.526, purity 1.00, fines 1.00.
- **S3, batch 8:** recovery 0.442, purity 0.969, fines 0.987.
- **S0, batch 9:** recovery 0.546, purity 0.979, fines 1.00; reaction selectivity 0.655 and yield 0.666.
- **S1, batch 3:** recovery 0.420, purity 0.991, fines 0.995.

These observations broadly favor S0 or S2 for recovery in the tested direct-crystallization histories. They do not establish an intrinsic solvent ranking because each solvent received only limited, non-replicated histories.

Reducing reagent loading from 0.04 to 0.01 mol in S0 increased measured reaction selectivity to 0.817 and yield to 0.820 in **batch 10**, but crystal recovery was 0.457 and fines remained 1.00. Consequently, improved upstream selectivity did not by itself control the number-weighted crystal population.

### Reaction–crystallization coupling
Crystal purity was consistently high—usually about 0.97–1.00—even when reaction selectivity was only about 0.55–0.65. Separation therefore rejected much of the reaction impurity effectively. The binding quality constraint was particle size, not chemical purity.

The reported crystal recovery was defined as

`Yc = recovered target product excluding added seed / target product present before separation`.

It is therefore a crystallization-stage recovery rather than an overall yield from charged reagent. A rough process-yield concept is `Yoverall ≈ Yreaction × Yc`, but that product was not the official measured objective and should only be used qualitatively.

For particle quality, the relevant constraint was

`F20 = N(d < 20 µm) / Ntotal ≤ 0.50`.

Because this is number-weighted, a large population of low-mass fines can dominate F20 even when larger crystals contain most of the solid mass. The normalized size channel corresponds to approximately `d50 = 250 µm × crystal_size`.

### Process-history dependence
Direct `cool_crystallize` histories consistently generated substantial recovery but an overwhelming fine population. This remained true after changing:

- seed mass from 0.05 g in batch 1 to 0.005 g in batch 2;
- cooling from one-stage to three 14,400 s stages in batch 2;
- solvent in batches 3, 8, and 9;
- seeded versus unseeded operation in batch 4;
- warm stopping at 300 K in batch 5;
- three reheat/recool ripening cycles in batch 6;
- rapid cooling in batch 7; and
- reactant loading in batch 10.

All of these direct-crystallization batches ended with fines near 0.99–1.00. Recoveries, however, were commonly 0.42–0.55. This indicates a robust quality/recovery conflict within the tested direct-crystallization operation class.

A useful qualitative population-balance interpretation is

`dNf/dt = Jprimary + Jsecondary + Bbreakage − Ddissolution − Aagglomeration`,

with supersaturation `S = C/C*` and approximate rate laws such as `J ∝ (S−1)^n` and `G ∝ (S−1)^g`. The results suggest that direct crystallization caused nucleation or secondary-fines generation to outrun growth onto the established particles. These equations are explanatory relationships, not fitted laws for this campaign.

The decisive history contrast was **batch 11**. It used S2/C3, seed addition, and a configured 0.001 K s⁻¹ control ramp from approximately 304 to 270 K, followed by a hold, but no direct `cool_crystallize` operation. Before filtration, particle imaging gave normalized size 0.384 and fines 0.0045. The final assay gave normalized size 0.396—about 99 µm d50—CSD quality 0.990, fines 0.00, and purity 1.00. These changes are far larger than the instrument noise and demonstrate that the controlled history preserved a coarse, narrow particle population.

Yet batch 11 recovered virtually no seed-excluded target. My interpretation is that the observed coarse solids were predominantly the purchased seeds: the control ramp matured or preserved them but did not precipitate appreciable newly formed target product.

This interpretation was challenged prospectively in **batch 12**. That batch first matured seeds with a slow control ramp to about 295 K and then invoked a 14,400 s warm `cool_crystallize` operation. Recovery rose to 0.472, but particle imaging immediately returned fines 1.00, and the final assay gave fines 1.00 and normalized size 0.055, roughly 14 µm d50. Thus, adding direct crystallization restored recovery but created a new fine population despite the presence of previously matured seeds.

### Revisions to the working mechanism
1. **Initial view:** S2, low seed loading, and slow staged cooling should favor growth over nucleation because of the nominal material dossier.
2. **Revision after batches 1–4:** slower cooling, lower seed mass, alternative solvent, unseeded operation, and a mild reheat did not materially reduce fines. The simple seed-dose/cooling-rate explanation was rejected.
3. **Revision after batches 5–10:** warm stopping, repeated thermal cycling, rapid cooling, solvent screening, and reduced loading also failed. I shifted from a purely material-based explanation to an operation-history/population-generation explanation.
4. **Revision after batch 11:** the slow configured-control ramp demonstrated that excellent particle quality was possible, but only without useful target recovery.
5. **Final revision after batch 12:** seed maturation was insufficient to protect particle quality once direct target precipitation was initiated. The unresolved mechanism is therefore not merely insufficiently large seeds; it is likely coupled to how the direct crystallization operation generates supersaturation and nuclei.

### Uncertainty and unresolved alternatives
The final-assay standard uncertainties were approximately 0.01 for crystal recovery, 0.01 for purity, 0.025 for normalized size, and 0.018 for fines; particle imaging used about 0.015 for its particle channels. Small differences among the many fines values near 1.00 are not meaningful. In contrast, the difference between batch 11 fines near zero and every direct-crystallization batch near one is decisive relative to measurement noise.

Most recipes were not replicated, and several comparisons confound catalyst, temperature, solvent, seed state, and thermal history. The proposed nucleation/secondary-fines account is therefore an interpretation rather than an identified kinetic model.

Untested possibilities include a genuinely coupled feedback-controlled precipitation mode that adds target gradually without invoking the fines-generating direct operation, in-process size classification or fines dissolution with selective removal, alternative seed-size distributions, and more narrowly spaced supersaturation-control stages. Those alternatives cannot be inferred as successful from the present evidence.

The principal unresolved tradeoff is sharp: **direct crystallization delivered useful recovery but failed the fines constraint, whereas the control-only batch delivered excellent purity and particle quality but essentially zero seed-excluded recovery**. Batch 11 remains the constrained recommendation, with this severe limitation explicitly acknowledged.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.12 | 0.03 | 0.28 |
| Q01 | crystal_purity | 0.97 | 0.93 | 1 |
| Q01 | crystal_size | 0.34 | 0.22 | 0.47 |
| Q01 | crystal_yield | 0.62 | 0.5 | 0.73 |
| Q02 | crystal_fines_fraction | 0.31 | 0.14 | 0.52 |
| Q02 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q02 | crystal_size | 0.23 | 0.13 | 0.36 |
| Q02 | crystal_yield | 0.5 | 0.38 | 0.62 |
| Q03 | crystal_fines_fraction | 0.72 | 0.49 | 0.9 |
| Q03 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q03 | crystal_size | 0.1 | 0.04 | 0.2 |
| Q03 | crystal_yield | 0.47 | 0.34 | 0.59 |
| Q04 | crystal_fines_fraction | 0.34 | 0.17 | 0.55 |
| Q04 | crystal_purity | 0.91 | 0.84 | 0.97 |
| Q04 | crystal_size | 0.24 | 0.14 | 0.37 |
| Q04 | crystal_yield | 0.53 | 0.41 | 0.64 |
| Q05 | crystal_fines_fraction | 0.3 | 0.14 | 0.5 |
| Q05 | crystal_purity | 0.92 | 0.85 | 0.97 |
| Q05 | crystal_size | 0.25 | 0.15 | 0.38 |
| Q05 | crystal_yield | 0.54 | 0.42 | 0.65 |
| Q06 | crystal_fines_fraction | 0.92 | 0.76 | 1 |
| Q06 | crystal_purity | 0.89 | 0.81 | 0.96 |
| Q06 | crystal_size | 0.07 | 0.02 | 0.16 |
| Q06 | crystal_yield | 0.58 | 0.46 | 0.69 |
| Q07 | crystal_fines_fraction | 0.25 | 0.1 | 0.45 |
| Q07 | crystal_purity | 0.92 | 0.85 | 0.97 |
| Q07 | crystal_size | 0.27 | 0.16 | 0.4 |
| Q07 | crystal_yield | 0.55 | 0.43 | 0.66 |
| Q08 | crystal_fines_fraction | 0.85 | 0.64 | 0.98 |
| Q08 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q08 | crystal_size | 0.08 | 0.02 | 0.18 |
| Q08 | crystal_yield | 0.49 | 0.35 | 0.61 |
| Q09 | crystal_fines_fraction | 0.08 | 0 | 0.25 |
| Q09 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q09 | crystal_size | 0.32 | 0.19 | 0.47 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.15 |
| Q10 | crystal_fines_fraction | 0.18 | 0.05 | 0.38 |
| Q10 | crystal_purity | 0.93 | 0.86 | 0.98 |
| Q10 | crystal_size | 0.28 | 0.16 | 0.42 |
| Q10 | crystal_yield | 0.28 | 0.17 | 0.4 |
| Q11 | crystal_fines_fraction | 0.23 | 0.09 | 0.43 |
| Q11 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q11 | crystal_size | 0.28 | 0.17 | 0.41 |
| Q11 | crystal_yield | 0.5 | 0.38 | 0.61 |
| Q12 | crystal_fines_fraction | 0.58 | 0.35 | 0.79 |
| Q12 | crystal_purity | 0.89 | 0.8 | 0.96 |
| Q12 | crystal_size | 0.16 | 0.07 | 0.28 |
| Q12 | crystal_yield | 0.61 | 0.49 | 0.72 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected. Q01–Q02: the very gentle staged ramp should favor growth; S1 is predicted to outperform S3 because its nominal lower nucleation, lower solubility and lower impurity occlusion favor recovery, size and purity. Q03–Q04: in nucleation-prone S0, 0.001 g seed provides too little surface to buffer supersaturation, whereas 0.045 g should suppress secondary nucleation. Q05–Q06: gradual cooling should give far fewer fines than the 120 s temperature plunge; the plunge may slightly increase recovery but produces a fine-dominated population. Q07–Q08: an added cold hold should permit growth/ripening, while heating to 315 K followed by a one-hour recool is expected to dissolve solids and then regenerate fines. Q09–Q10: the initial 60 s step should leave mostly coarse seed and little seed-excluded recovery; the 7200 s hold raises recovery through deposition while remaining warm enough to limit new nucleation. Q11–Q12: doubling loading should raise recovery but also supersaturation, impurity occlusion and fines, making Q12 borderline-to-infeasible. Intervals are deliberately wider than assay noise because these extremely slow, finely staged schedules extrapolate beyond the campaign histories; estimates near the 0.50 fines or 0.80 purity boundaries are correspondingly uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Particle quality, rather than chemical purity, was the binding constraint.** Direct final assays showed purity around 0.97–1.00 in most completed batches, while every batch using `cool_crystallize` had fines near 0.99–1.00. Examples include batches 1, 2, 4, 8, 9, 10 and 12.
- **Direct crystallization produced useful recovery but a fine-dominated population in the tested histories.** Recoveries were commonly about 0.42–0.55: batch 4 reached 0.526, batch 9 reached 0.546, and batch 12 reached 0.472, but each had fines at or near 1.00.
- **The control-only history gave coarse particles but negligible seed-excluded recovery.** Batch 11 directly showed pre-filter fines 0.0045 and normalized size 0.384; its final assay gave fines 0, size 0.396, purity 1.00, and crystal yield only 8.3×10⁻⁶.
- **Adding direct crystallization after seed maturation restored recovery but destroyed particle quality.** Batch 12 directly showed recovery 0.472, but pre-filter and final fines were both 1.00. This contradicts the prospective hypothesis that mature seeds would necessarily absorb the deposited target without forming a new fine population.
- **Lower reagent loading improved reaction selectivity but not fines.** Batch 10 directly showed selectivity 0.817 and reaction yield 0.820 at reduced loading, yet its final fines remained 1.00.

### Supported as interpretations, but not causally isolated
- **C3 under the milder reaction history appeared less degradative than C1 under the hotter/longer history.** C1 batches 1–2 had degradation warnings near 0.18, whereas several C3 batches were near 0.09–0.11. This is an interpretation because catalyst, temperature, duration and downstream history were confounded.
- **A direct crystallization step likely generated a new fine population.** The batch 11/12 contrast strongly supports this interpretation, but it does not identify whether the cause was operation semantics, supersaturation at the time of invocation, secondary nucleation, or breakage.
- **Batch 11 solids were predominantly purchased seed.** This follows from the combination of coarse particles and essentially zero seed-excluded recovery, but the solid composition was not independently measured.

### Contradicted or substantially weakened
- The initial expectation that **S2, low seed loading and ordinary slow staged cooling would control fines** was contradicted by batches 1, 2 and 4.
- The hypothesis that **warm stopping or thermal ripening would remove the fine population** was contradicted by batches 5 and 6.
- The expectation that **lower supersaturation through reduced loading would solve the particle problem** was contradicted by batch 10.
- The proposed **hybrid seed-maturation/direct-growth process** was contradicted by batch 12.

### Still untested
- Whether a sufficiently small, feedback-controlled target deposition increment can grow the coarse seed population without crossing a secondary-nucleation threshold.
- Whether the decisive batch 11/12 difference reflects the `cool_crystallize` operation itself or merely the supersaturation present when it was invoked.
- Size-selective solids removal, deliberate fines dissolution with removal, alternative seed-size distributions, and true antisolvent or feed-controlled crystallization were not tested.
- Most solvent and catalyst effects remain unreplicated and confounded.

## 2. One additional experiment

I would reproduce the batch 11 upstream recipe in S2 with C3 and 0.05 g seed, but use one batch as an **onset-mapping experiment**:

1. Apply the configured 0.001 K s⁻¹ control history only to about 304 K and obtain a non-destructive particle-size baseline.
2. Invoke `cool_crystallize` for 14,400 s at essentially the same temperature, with negligible temperature change, and remeasure particles.
3. Continue in small 1–2 K, 14,400 s increments, measuring particles after each increment.
4. Filter and obtain a final assay to measure seed-excluded recovery and purity.

This would distinguish three explanations:

- **Operation-intrinsic nucleation:** fines would jump sharply after the first nearly isothermal `cool_crystallize` call, even before appreciable cooling; size would collapse and some recovery would appear.
- **Supersaturation-threshold mechanism:** early increments would preserve low fines while recovery gradually increased; fines would rise only below a particular temperature or after a particular deposited fraction.
- **Seed preservation without target deposition:** particles would remain coarse throughout the mild increments, but final seed-excluded recovery would stay near zero, as in batch 11.

The most valuable outcome would be a region with increasing recovery, purity above 0.80 and fines still below 0.50. Its absence would make the operation-intrinsic or sharply thresholded nucleation explanation much stronger.

## 3. Least effectively used evidence and least reliable prediction

### Underused observation
I used the **paired pre-filter particle measurements and final-assay particle results** less effectively than I should have. They show that filtration did not rescue or create the observed distributions: batch 2 had pre-filter fines 0.987 and final fines 1.00; batch 4 had 0.981 before filtration and 1.00 finally; batch 11 had 0.0045 before filtration and 0 finally; batch 12 had 1.00 at both points. This evidence strengthens the conclusion that particle quality was established during crystallization rather than by the filtration step.

### Least reliable held-out prediction
**Q01 is the least reliable prediction.** I predicted that the exceptionally gentle, many-stage S1 schedule would be quality-feasible with low fines. That estimate relies on nominal S1 properties and extrapolation to a much slower schedule than any campaign batch. The only direct S1 experiment, batch 3, still produced final fines 0.995, and it was confounded by a different thermal history. Thus Q01’s predicted improvement from nearly complete fines failure to a fines estimate of 0.12 is much larger than any experimentally demonstrated solvent effect. Its uncertainty interval may therefore understate model-form uncertainty, even though no prediction truth has been supplied.
