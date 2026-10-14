# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended operating history and observed outcome
The sealed recommendation is **batch 8**. It used 0.040 mol limiting reagent, 0.080 L solvent S2, and 0.005 mol catalyst C1 under nitrogen near 1 atm. The reaction was heated at 360 K for 3,600 s with 600 rpm stirring. It was then cooled to 325 K over 3,600 s, seeded with 0.020 g seed, cooled to 290 K over 14,400 s, filtered, terminated, and assayed.

Batch 8 gave seed-excluded crystal recovery 0.413, purity 0.981, and number fraction below 20 µm of 0.471. It was selected because it had the highest observed recovery among batches satisfying purity ≥0.80 and fines ≤0.50.

### Reaction and material effects
The pre-crystallization HPLC catalyst screen in S0 showed nearly complete conversion for all four catalysts, but different selectivity and product yield:

- Batch 1, C0: conversion 1.000, liquid-product yield 0.609, selectivity 0.615.
- Batch 2, C1: conversion 0.985, yield 0.596, selectivity 0.625.
- Batch 3, C2: conversion 0.998, yield 0.539, selectivity 0.538.
- Batch 4, C3: conversion 0.989, yield 0.599, selectivity 0.613.

**Observation:** C2 was inferior in this screen, whereas C0, C1, and C3 were closer. C1 had the highest measured selectivity and was therefore carried forward.

**Interpretation:** the reaction was conversion-saturated, so catalyst choice mainly altered branching between target and byproduct rather than disappearance of reagent. A useful schematic is

`R → P` with rate `kP(C,S,T)`, and `R or P → I` with rate `kI(C,S,T)`.

At high conversion, target formation is governed more by `kP/(kP+kI)` and subsequent degradation than by conversion alone. These are phenomenological rates; no molecular identity or elementary pathway was disclosed.

Solvent had an even stronger effect on the combined reaction/crystallization outcome. With C1 and a common 360 K reaction followed by a 285 K seeded crystallization:

- Batch 5, S1: crystal recovery 0.442, purity 0.977, fines 0.588.
- Batch 6, S2: recovery 0.414, purity 1.000, fines 0.504.
- Batch 7, S3: recovery 0.382, purity 0.970, fines 0.696.

S1 gave the highest recovery but failed the fines requirement; S2 was closest to feasibility; S3 was poorer on both recovery and fines. Earlier S0 batches had fines of approximately 0.945–1.000. Thus solvent selection was indispensable for particle control.

Mechanistically, solvent can affect both reaction selectivity and crystallization through target solubility `C*(T,S)`, supersaturation, interfacial energy, nucleation, growth, and impurity rejection. The evidence does not identify which of these dominates.

### Reaction–crystallization coupling
The reported recovery is

`Ycrystal = n(P in recovered solid, excluding seed) / n(R initially charged)`.

A useful approximate decomposition is

`Ycrystal ≈ Yreaction × fcapture × fretention`,

where `Yreaction` is target formed per initial reagent, `fcapture` is the fraction transferred from solution to crystals, and `fretention` represents separation retention. These factors were not independently assayed, so the decomposition is interpretive rather than fitted.

For example, batch 8 had liquid-product yield about 0.510 and crystal recovery 0.413, corresponding to an apparent overall capture/retention factor near 0.81. Batch 5 combined higher liquid-product yield, 0.583, with recovery 0.442, but its particle population failed the fines constraint. Maximizing reaction yield alone therefore did not maximize qualified recovery.

Purity was generally high after crystallization, often around 0.98–1.00, even when reaction selectivity was only about 0.5. This is consistent with preferential incorporation of target and rejection of impurities into mother liquor. It is not proof of a particular crystal lattice or impurity mechanism.

### Supersaturation and particle-history interpretation
A conventional description is

`S = C/C*(T,Ssolvent)`

with primary or secondary nucleation increasing steeply with supersaturation, for example

`J ≈ A exp[-B/(ln S)^2]`,

and crystal growth approximated by

`G ≈ kg(S−1)^g`.

The number-based fines metric is

`ffines = N(D < 20 µm) / Ntotal`.

Because it is number-weighted, many small secondary nuclei can dominate the metric even if they contain little mass. A colder endpoint can increase recovery by lowering solubility, but may also increase supersaturation enough to create many fines.

The cleanest temperature comparison was between C1/S2 batches 6 and 8:

- Batch 6 stopped at 285 K: recovery 0.414, fines 0.504, normalized size 0.052.
- Batch 8 stopped at 290 K: recovery 0.413, fines 0.471, normalized size 0.106.

The recovery difference is negligible relative to assay noise, while the warmer endpoint produced fewer fines and a larger measured particle-size response. This supports the interpretation that stopping at 290 K suppressed late secondary nucleation while retaining nearly all practically accessible recovery.

Additional local tests supported a narrow operating window:

- Batch 10, 288 K with C1/S2: recovery 0.410, purity 0.979, fines 0.496.
- Batch 11, repeat at 290 K: recovery 0.396, purity 0.994, fines 0.478.
- Batch 9, 289 K but C0: recovery 0.390, purity 0.981, fines 0.500.

Thus 288–290 K repeatedly approached or met the specification, but 290 K provided more fines margin. The lower batch-11 recovery shows meaningful batch variation and prevents claiming a precisely optimized temperature.

### Process-history dependence and revisions
My initial expectation was that slow cooling, seeding, and prolonged aging or temperature cycling would necessarily reduce fines. The S0 results did not support that generalization:

- Batch 1 used 0.050 g seed and deep cooling to 278 K; recovery was 0.450 but fines were 0.985.
- Batch 2 used 0.005 g seed and stopped at 295 K; recovery was 0.401 and fines 0.945.
- Batch 3 included a heat/cool cycle and two additional 14,400 s periods at 295 K; recovery fell to 0.322 and fines remained 0.973.
- Batch 4 used nearly zero seed and shallow cooling to 315 K; recovery was only 0.082 and fines were 1.000.

These batches differed in catalyst as well as crystallization history, so they do not isolate seed mass or aging. Nevertheless, they show that extra time or cycling was not sufficient to rescue an unfavorable solvent regime. I therefore revised the working account: solvent-dependent nucleation/solubility and the terminal supersaturation window were more important than simply adding seed or extending the batch.

A second initial expectation was that lowering reaction temperature might reduce degradation. Batch 12 combined 350 K with a longer 5,400 s hold. It reached conversion 1.000 but gave selectivity 0.421, byproduct signal 0.412, degradation warning 0.246, and crystal recovery only 0.320. Its purity and fines still passed. Because temperature and duration changed together, this does not establish that 350 K itself is harmful; it establishes only that this combined lower-temperature/longer-history recipe was inferior. Residence time, solvent-specific degradation, or continued product conversion are unresolved alternatives.

### Uncertainty and unresolved trade-off
The final-assay standard noise scales were approximately 0.010 for crystal recovery and purity, 0.018 for fines, and 0.025 for normalized size. Consequently:

- Recovery differences among batches 6, 8, and 10 are not strong evidence of distinct underlying recoveries.
- Batch 8’s fines result of 0.471 has only a modest margin below 0.50, although batches 10 and 11 provide supporting local evidence.
- Batch 10 at 0.496 and batch 9 at 0.500 are borderline and would not be robust choices.
- Purity is comfortably above 0.80 and is not the binding constraint.

The unresolved trade-off is therefore colder crystallization for potentially greater mass recovery versus warmer termination for lower number-weighted fines. In the observed range, cooling from 290 K to 285 K did not measurably improve recovery but did worsen fines, favoring 290 K. It remains untested whether a more sophisticated trajectory could recover additional mass without causing secondary nucleation.

Untested alternatives include mixed solvents, controlled antisolvent addition, independently varied reaction temperature and residence time, seed-size distribution rather than seed mass alone, cooling-stage agitation changes, crystal washing, and a full catalyst-by-solvent factorial screen. These could change the mechanistic interpretation and should not be inferred from the present data.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.32 | 0.15 | 0.53 |
| Q01 | crystal_purity | 0.98 | 0.93 | 1 |
| Q01 | crystal_size | 0.16 | 0.08 | 0.26 |
| Q01 | crystal_yield | 0.46 | 0.36 | 0.55 |
| Q02 | crystal_fines_fraction | 0.58 | 0.37 | 0.78 |
| Q02 | crystal_purity | 0.97 | 0.91 | 1 |
| Q02 | crystal_size | 0.105 | 0.045 | 0.19 |
| Q02 | crystal_yield | 0.39 | 0.29 | 0.49 |
| Q03 | crystal_fines_fraction | 0.72 | 0.48 | 0.91 |
| Q03 | crystal_purity | 0.98 | 0.92 | 1 |
| Q03 | crystal_size | 0.09 | 0.035 | 0.18 |
| Q03 | crystal_yield | 0.43 | 0.32 | 0.53 |
| Q04 | crystal_fines_fraction | 0.4 | 0.22 | 0.61 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q04 | crystal_yield | 0.45 | 0.34 | 0.55 |
| Q05 | crystal_fines_fraction | 0.38 | 0.2 | 0.59 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.145 | 0.07 | 0.24 |
| Q05 | crystal_yield | 0.45 | 0.34 | 0.55 |
| Q06 | crystal_fines_fraction | 0.84 | 0.65 | 0.97 |
| Q06 | crystal_purity | 0.98 | 0.92 | 1 |
| Q06 | crystal_size | 0.065 | 0.02 | 0.14 |
| Q06 | crystal_yield | 0.46 | 0.35 | 0.56 |
| Q07 | crystal_fines_fraction | 0.36 | 0.18 | 0.57 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.15 | 0.075 | 0.25 |
| Q07 | crystal_yield | 0.46 | 0.35 | 0.56 |
| Q08 | crystal_fines_fraction | 0.27 | 0.11 | 0.49 |
| Q08 | crystal_purity | 0.98 | 0.92 | 1 |
| Q08 | crystal_size | 0.19 | 0.09 | 0.31 |
| Q08 | crystal_yield | 0.41 | 0.29 | 0.52 |
| Q09 | crystal_fines_fraction | 0.68 | 0.38 | 0.92 |
| Q09 | crystal_purity | 0.96 | 0.82 | 1 |
| Q09 | crystal_size | 0.075 | 0.025 | 0.15 |
| Q09 | crystal_yield | 0.035 | 0 | 0.12 |
| Q10 | crystal_fines_fraction | 0.49 | 0.27 | 0.71 |
| Q10 | crystal_purity | 0.98 | 0.91 | 1 |
| Q10 | crystal_size | 0.11 | 0.05 | 0.2 |
| Q10 | crystal_yield | 0.19 | 0.08 | 0.32 |
| Q11 | crystal_fines_fraction | 0.35 | 0.17 | 0.56 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.15 | 0.075 | 0.25 |
| Q11 | crystal_yield | 0.45 | 0.34 | 0.55 |
| Q12 | crystal_fines_fraction | 0.68 | 0.45 | 0.87 |
| Q12 | crystal_purity | 0.97 | 0.89 | 1 |
| Q12 | crystal_size | 0.09 | 0.035 | 0.18 |
| Q12 | crystal_yield | 0.4 | 0.28 | 0.52 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where little seed-excluded product crystallizes. Q01–Q02: prior solvent screening favored S1 over S3 for both recovery and fines, so S1 is predicted feasible while S3 remains fine-rich. Q03–Q04: under the exceptionally slow ramp, the larger seed charge should provide enough growth area to suppress uncontrolled nucleation; the very small seed charge has a substantial primary/secondary-nucleation risk. Q05–Q06: gradual cooling should preserve yield while strongly reducing fines relative to an immediate 278.15 K crash, even after equal total aging. Q07–Q08: a 315 K temperature cycle is expected to dissolve preferentially the smallest particles and increase d50, but with some loss of recovered mass and uncertainty about rapid-renucleation on recooling. Q09–Q10: the 60-second endpoint should recover little newly formed target; an additional two-hour hold should increase seed-excluded recovery and grow part of the fine population, though feasibility is borderline. Q11–Q12: doubling reagent at fixed solvent, catalyst, and seed raises supersaturation while halving catalyst-to-reagent ratio, so fractional recovery is predicted slightly lower and fines substantially higher. Purity is expected to remain high because crystallization previously rejected reaction impurities effectively. Intervals are deliberately broad because these recipes extrapolate to 385 K, lower loading, multi-day cooling histories, and seed charges not cleanly isolated in the completed campaign; fines near 0.50 and the temperature-cycle response are the least certain classifications.

## K2

## 1. Status of the main claims

### Supported by observations
- **Solvent identity strongly affects particle quality.** Under the common C1 protocol, batches 5–7 gave fines of 0.588 for S1, 0.504 for S2, and 0.696 for S3, while S0 batches 1–4 gave approximately 0.945–1.000. The direct observation is the large solvent-associated contrast. Attribution to solubility, interfacial energy, or nucleation kinetics remains interpretation.
- **The 288–290 K stopping region is preferable to 285 K for C1/S2.** Batch 6 at 285 K gave recovery 0.414 and fines 0.504. Batches 8, 10, and 11 at 288–290 K gave recoveries 0.396–0.413 and fines 0.471–0.496. Directly, warmer stopping improved qualification without an observed recovery benefit from cooling to 285 K. Suppression of late secondary nucleation is a plausible interpretation, not directly measured.
- **Purity was not the binding constraint.** Qualified-region batches 8, 10, and 11 had purity 0.979–0.994, and even many poor-CSD batches had purity near 0.98–1.00. Preferential impurity rejection into mother liquor is an interpretation supported by the contrast between moderate reaction selectivity and high crystal purity.
- **C2 was inferior in the S0 catalyst screen.** Pre-crystallization HPLC in batch 3 gave yield 0.539 and selectivity 0.538, below the corresponding C0, C1, and C3 results in batches 1, 2, and 4. This is a direct upstream observation under a common nominal reaction protocol.
- **Process history matters.** Batch 12’s 350 K/5,400 s reaction produced lower crystal recovery, 0.320, and worse byproduct/degradation signals than the 360 K/3,600 s qualified runs. Batch 3’s prolonged cycling and aging also failed to improve its fine-rich S0 population.

### Contradicted or revised claims
- **“More seed or more aging necessarily reduces fines” was contradicted.** S0 remained extremely fine across seed charges from nearly zero to 0.050 g in batches 1–4, and the prolonged cycle in batch 3 ended with fines 0.973. Because catalyst, endpoint, and history also varied, these batches contradict the universal claim but do not determine the isolated seed effect.
- **“Colder crystallization necessarily increases useful recovery” was not supported locally.** Batch 6 at 285 K did not exceed batch 8 at 290 K beyond assay uncertainty, but it crossed to the wrong side of the fines limit.
- **“Lower reaction temperature should reduce degradation” was not supported by batch 12.** However, that batch also increased residence time, so only the combined 350 K/5,400 s recipe is contradicted; a pure temperature effect was not tested.

### Still untested
The elementary reaction network, the physical solvent properties responsible for the material effects, catalyst-by-solvent interactions, seed-size-distribution effects, cooling-stage agitation, separate crystallization capture and filtration retention, mixed-solvent or antisolvent strategies, and independently varied reaction temperature and residence time remain untested. The claim that thermal cycling selectively dissolves fines also remains unresolved.

## 2. One additional experiment
I would repeat the batch-8 C1/S2 process through the 290 K endpoint, measure particle size non-destructively, then apply a controlled cycle of 315 K for 3,600 s followed by recooling to 290 K over 3,600 s, measure particles again, filter, terminate, and perform the final assay.

This creates a within-batch before/after comparison and distinguishes three explanations:

1. **Selective dissolution/Ostwald-growth explanation:** heating preferentially dissolves fines and material regrows on larger crystals. Expected result: lower fines, higher normalized size, stable purity, and a modest recovery loss if recooling is incomplete.
2. **Rapid-renucleation explanation:** the heat step dissolves particles, but rapid recooling creates a new fine population. Expected result: no improvement or an increase in fines, limited size gain, and recovery near the uncylced process.
3. **Chemical-history explanation:** additional warm residence degrades target rather than primarily restructuring particles. Expected result: lower final recovery or purity and higher byproduct/degradation signals without a compensating CSD improvement.

The appropriate comparator would be batches 8 and 11, which used the same materials and 290 K endpoint without cycling. This experiment would directly test the assumption underlying my most uncertain thermal-cycle prediction while avoiding the catalyst and solvent confounds present in batch 3.

## 3. Underused observation and least reliable prediction
The account used the **prefiltration particle-size measurements** least effectively. It relied mainly on final-assay CSD values rather than systematically comparing each in-situ particle reading with its final result. In batch 3, for example, the prefiltration measurement gave fines about 0.963 and normalized size about 0.062, while the final assay gave fines 0.973 and size 0.049. Their broad agreement suggests filtration did not rescue the distribution, but a full paired analysis could have separated process evolution, instrument noise, and separation effects more clearly.

The least reliable held-out prediction is **Q08**, the 315 K thermal-cycle case. Its forecast assumed selective dissolution would enlarge particles and reduce fines, yet the campaign contained no clean matched demonstration of that mechanism. Batch 3’s cycle did not improve its final S0 distribution, but it was confounded by C2, a different temperature window, and prolonged aging. Q08 also couples dissolution, possible chemical degradation, and rapid recooling-driven renucleation, so the direction of its fines and size effects is substantially less secure than the solvent, cooling-rate, or loading comparisons.
