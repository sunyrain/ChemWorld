# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Overall result
Twelve batches were completed. Every final assay met the crystal-purity requirement of at least 0.80, but none met the required number fraction below 20 µm of at most 0.50. The sealed recommendation remains batch 12 because it was closest to the fines specification: crystal recovery 0.378, purity 0.990, and fines fraction 0.865. It should be regarded as a development lead, not a specification-compliant process.

### Material effects
The initial material-based hypothesis favored solvent S2: its dossier indicated relatively low solubility and nucleation tendency, high crystal-growth propensity, and low impurity occlusion. The purity and recovery observations partly supported this expectation, but the particle-size prediction failed. Full-loading S2 processes generally gave high purity (about 0.98–1.00) and recovery around 0.44–0.48, yet fines remained approximately 0.99–1.00. For example, batch 1 gave recovery 0.479 and purity 0.988, but fines 0.997. Thus S2 promoted product recovery without producing an acceptable number-weighted size distribution under the tested histories.

Solvent changes did not independently solve the problem. Batch 7, using S3, gave recovery 0.376, purity 0.975, and fines 0.987. Full-loading S1 batch 8 gave recovery 0.462, purity 0.980, and fines 0.987. Batch 11 used S0 together with catalyst C2 and gave the lowest recovery among these solvent comparisons, 0.298, with purity 0.979 and fines 0.994. Because batch 11 changed catalyst as well as solvent and temperature, its poorer outcome cannot be assigned uniquely to S0.

Catalyst C1 was used in most batches and generally produced nearly complete conversion. Catalyst effects were not established by a controlled factorial comparison: C2 was used only in the confounded S0 batch, while C0 and C3 were not tested. Consequently, C1 is supported as a workable catalyst, not proven optimal.

### Reaction–crystallization coupling
A useful minimal reaction model is

- dR/dt = -(kT + kB + kD)R,
- dP/dt = kT R,
- selectivity ≈ kT/(kT + kB + kD),
- product yield ≈ conversion × selectivity.

Here the effective rate constants depend on catalyst, solvent, temperature, and time. Batch 1 at the hotter reaction condition showed complete conversion, selectivity about 0.576, byproduct signal 0.317, and degradation warning 0.167. Several 335 K C1 batches also approached complete conversion but had selectivity around 0.50–0.55. These observations indicate that conversion was not the principal limitation; competing product/byproduct formation remained important.

Crystallization recovery is conditional on the target already present before separation:

crystal recovery = seed-excluded target recovered as crystals / target present before separation.

It is therefore not the same as overall yield from charged reagent. Nevertheless, reaction conditions affect target concentration and impurity loading, which determine supersaturation, nucleation, growth, and occlusion. This explains why a process can have a respectable crystallization recovery but only moderate overall reaction yield.

For crystallization, the following relationships are useful:

- supersaturation ratio S = C/C*(T) - 1,
- nucleation rate J ≈ kn max(S,0)^n,
- growth rate G ≈ kg max(S,0)^g,
- characteristic particle diameter d ∝ [Mcrystal/(ρN)]^(1/3),

where C*(T) is solubility, N is the number of particles, and Mcrystal is crystallized mass. High J relative to G creates many small particles. The consistently high fines suggest that the tested cooling paths generated or retained too many nuclei relative to the available growth mass.

Batch 12 provides the clearest evidence for concentration coupling. It reduced reagent charge from 0.040 to 0.010 mol, used 0.080 L of S1 and only 0.001 g seed, and returned fines of 0.865—substantially below the approximately 0.99 values of the full-loading batches—while maintaining purity 0.990 and recovery 0.378. My interpretation is that lower target concentration reduced primary or secondary nucleation. However, this was a single, unreplicated result and simultaneously changed reagent loading, catalyst amount, seed mass, and solvent-to-target ratio. The magnitude and causal attribution remain uncertain.

### Process-history dependence
The original expectation was that seeding, slow cooling, and long growth holds in S2 would suppress fines. The observations rejected that expectation within the tested range:

- Batch 1: 0.050 g seed and cooling to 270 K gave recovery 0.479 but fines 0.997.
- Batch 2: 0.005 g seed, a warm hold, slower cooling, and additional cold holding gave recovery 0.453 but final fines 1.000.
- Batch 6: shallow cooling only to 292 K with long holds still gave recovery 0.438 and fines 1.000; its particle-size estimate was particularly small.

Thus additional residence time did not measurably convert the fine population into a compliant coarse population. Possible explanations include rapid nucleation during initial supersaturation generation, growth-limited kinetics, attrition or secondary nucleation, or a simulated morphology law that responds weakly to holding time.

Thermal cycling was also ineffective. Batch 4 underwent cooling, reheating to 290 K, holding, and recooling; it gave recovery 0.461, purity 1.000, and fines 1.000. Batch 9 underwent five 292/265 K cycles and achieved the highest observed recovery, 0.484, but fines remained 1.000 and the final size estimate was small. This suggests that cycling recovered additional mass without preferentially removing the fine-particle population. It does not support effective Ostwald ripening under those conditions.

Post-filtration resuspension likewise showed an unfavorable quality/recovery tradeoff. Batch 5 was resuspended in S0 and refiltered, giving recovery 0.451 and fines 1.000. Batch 10 used a larger S0 resuspension followed by warming to 280 K; recovery fell to 0.364 while fines remained 1.000. The tested washes apparently dissolved or lost product without selectively eliminating enough fines.

### Measurement uncertainty
Final-assay estimates have stated synthetic noise, and particle-size imaging and final assay are separate observation channels. Numerical differences between single batches should therefore not be treated as replicated effects. Batch 12 illustrates this issue: its in-process particle measurement and final assay agreed closely on fines (0.867 and 0.865), supporting the conclusion that the batch remained noncompliant. Their normalized size estimates differed appreciably, however. This channel disagreement means that apparent d50 changes should not override the directly reported fines fraction. The fines conclusion is much stronger than any precise ranking of particle size or CSD quality.

### Revisions and unresolved tradeoff
The initial S2-centered hypothesis was revised after batches 1–6: S2 was useful for recovery and purity but did not control fines. The subsequent solvent, thermal-cycle, and wash hypotheses were not supported. The final working hypothesis is narrower: lowering target loading or supersaturation intensity may reduce fines, as suggested by batch 12, but probably at the cost of throughput and possibly recovery.

The central unresolved tradeoff is therefore recovery versus particle-number quality. Deep or repeated crystallization histories preserved recovery around 0.45–0.48 but left essentially all particles below the required cutoff. Lower loading improved fines to 0.865 but also reduced recovery to 0.378 and still missed the specification substantially.

Untested alternatives include still lower loading, a replicated loading series, mixed-solvent or staged-solvent addition, seeding exactly at a measured supersaturation threshold, gentler agitation to reduce secondary nucleation, and controlled comparisons of all four catalysts. These are mechanistic alternatives rather than demonstrated remedies. No tested batch establishes that the fines constraint is reachable without a material recovery or throughput penalty.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.36 | 0.19 | 0.56 |
| Q01 | crystal_purity | 0.95 | 0.89 | 0.985 |
| Q01 | crystal_size | 0.125 | 0.065 | 0.195 |
| Q01 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q02 | crystal_fines_fraction | 0.25 | 0.11 | 0.44 |
| Q02 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q02 | crystal_size | 0.155 | 0.09 | 0.235 |
| Q02 | crystal_yield | 0.43 | 0.31 | 0.56 |
| Q03 | crystal_fines_fraction | 0.56 | 0.35 | 0.75 |
| Q03 | crystal_purity | 0.92 | 0.84 | 0.97 |
| Q03 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q03 | crystal_yield | 0.25 | 0.15 | 0.37 |
| Q04 | crystal_fines_fraction | 0.42 | 0.24 | 0.62 |
| Q04 | crystal_purity | 0.93 | 0.86 | 0.975 |
| Q04 | crystal_size | 0.105 | 0.05 | 0.175 |
| Q04 | crystal_yield | 0.29 | 0.19 | 0.41 |
| Q05 | crystal_fines_fraction | 0.35 | 0.19 | 0.55 |
| Q05 | crystal_purity | 0.93 | 0.86 | 0.976 |
| Q05 | crystal_size | 0.125 | 0.065 | 0.2 |
| Q05 | crystal_yield | 0.31 | 0.2 | 0.43 |
| Q06 | crystal_fines_fraction | 0.7 | 0.5 | 0.86 |
| Q06 | crystal_purity | 0.91 | 0.82 | 0.965 |
| Q06 | crystal_size | 0.065 | 0.02 | 0.125 |
| Q06 | crystal_yield | 0.34 | 0.22 | 0.47 |
| Q07 | crystal_fines_fraction | 0.31 | 0.16 | 0.5 |
| Q07 | crystal_purity | 0.935 | 0.87 | 0.978 |
| Q07 | crystal_size | 0.14 | 0.075 | 0.22 |
| Q07 | crystal_yield | 0.32 | 0.21 | 0.44 |
| Q08 | crystal_fines_fraction | 0.64 | 0.42 | 0.82 |
| Q08 | crystal_purity | 0.94 | 0.87 | 0.982 |
| Q08 | crystal_size | 0.075 | 0.025 | 0.14 |
| Q08 | crystal_yield | 0.25 | 0.14 | 0.38 |
| Q09 | crystal_fines_fraction | 0.48 | 0.25 | 0.7 |
| Q09 | crystal_purity | 0.96 | 0.86 | 0.995 |
| Q09 | crystal_size | 0.105 | 0.045 | 0.175 |
| Q09 | crystal_yield | 0.045 | 0.005 | 0.13 |
| Q10 | crystal_fines_fraction | 0.42 | 0.22 | 0.63 |
| Q10 | crystal_purity | 0.95 | 0.87 | 0.989 |
| Q10 | crystal_size | 0.12 | 0.06 | 0.195 |
| Q10 | crystal_yield | 0.16 | 0.06 | 0.29 |
| Q11 | crystal_fines_fraction | 0.34 | 0.18 | 0.54 |
| Q11 | crystal_purity | 0.93 | 0.86 | 0.976 |
| Q11 | crystal_size | 0.13 | 0.07 | 0.205 |
| Q11 | crystal_yield | 0.315 | 0.205 | 0.44 |
| Q12 | crystal_fines_fraction | 0.62 | 0.41 | 0.8 |
| Q12 | crystal_purity | 0.9 | 0.81 | 0.96 |
| Q12 | crystal_size | 0.08 | 0.03 | 0.145 |
| Q12 | crystal_yield | 0.43 | 0.3 | 0.56 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and a cooling operation, so particles are expected even where seed-excluded product recovery is small. Q01/Q02 isolate solvent: S3 is predicted to outperform S1 through lower solubility, lower nucleation tendency, faster growth and less occlusion, giving higher recovery, purity and size with fewer fines. Q03/Q04 compare seed loading in S0: the larger seed charge should provide enough growth surface to suppress uncontrolled primary nucleation, although its quality advantage is uncertain because more seeds can also limit final size. Q05/Q06 compare gradual cooling with an initial crash to 278.15 K; the crash should establish supersaturation too quickly, producing more fines despite comparable or slightly greater recovery. Q07/Q08 test a late 315 K excursion: partial dissolution followed by rapid recooling is expected to sacrifice recovery and regenerate fines rather than achieve effective ripening. Q09/Q10 compare immediate filtration with a two-hour hold at 292 K; the hold should substantially increase seed-excluded recovery and permit some growth, while Q09 remains a very-low-recovery seeded solid. Q11/Q12 expose the quality/recovery tradeoff from doubling reagent loading: higher loading raises fractional recovery but also nucleation and occlusion, reducing size and making fines noncompliant. Intervals are epistemic 80% ranges for noise-free outcomes, not final-assay noise; they are deliberately broad because the campaign did not directly test these exceptionally slow multistage schedules, the 385 K reaction history, or most paired changes in isolation. Feasibility flags use the point estimates, so several intervals still cross the fines threshold.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Purity was not the limiting constraint in the tested region.** Every completed batch had final crystal purity above 0.97, comfortably exceeding 0.80. This is direct assay evidence, although it does not prove purity would remain high outside the tested conditions.
- **The tested full-loading processes produced excessive fines.** Batches 1–11 generally reported fines fractions of about 0.987–1.000. Batch 1, for example, combined recovery 0.479 and purity 0.988 with fines 0.997. This directly supports the conclusion that recovery and purity alone were insufficient.
- **Long holds, shallow cooling, thermal cycling, and the tested washes did not solve the fines problem.** Batch 2 used extended holds and slow cooling but ended at fines 1.000. Batch 6 used shallow cooling to 292 K and also ended at 1.000. Batch 9 underwent repeated thermal cycles and achieved recovery 0.484 but fines 1.000. Warm resuspension in batch 10 reduced recovery to 0.364 while leaving fines at 1.000.
- **Lower-loading batch 12 had the lowest observed fines.** Its particle and final measurements gave 0.867 and 0.865, respectively, with final recovery 0.378 and purity 0.990. The numerical improvement is directly observed.
- **C1 was operationally effective for conversion.** Most C1 batches approached complete conversion. This supports C1 as workable, but not as uniquely optimal.

### Contradicted or revised
- **The initial claim that seeded, slowly cooled S2 would meet the fines limit was contradicted.** Batch 1 and the modified S2 histories in batches 2, 4, 6, and 9 all remained strongly noncompliant.
- **The expectation that thermal cycling would cause useful ripening was contradicted within the tested window.** Batches 4 and 9 did not show the anticipated reduction in fines; repeated cycling in batch 9 coincided with a small final size estimate.
- **The proposed selective removal of fines by S0 resuspension was contradicted for the tested wash conditions.** Batches 5 and 10 lost recovery without obtaining acceptable fines.

### Interpretations that remain uncertain
- **Reduced supersaturation caused the better fines result in batch 12.** This is plausible, but not isolated experimentally: batch 12 simultaneously changed reagent loading, solvent-to-target ratio, catalyst amount, seed mass, and thermal conditions relative to most earlier batches.
- **S2 intrinsically favors recovery while S3 or S1 favors particle quality.** The observed solvent comparisons were confounded by volume, seed, catalyst, temperature, and history. They establish outcomes for particular recipes, not clean solvent effects.
- **High nucleation relative to growth caused the fine population.** This interpretation is consistent with the observations and material dossier, but nucleation and growth rates were not measured directly.

### Still untested
Catalysts C0 and C3, a controlled catalyst comparison, a replicated loading series, mixed-solvent or staged-solvent addition, seeding at a measured supersaturation threshold, and genuinely low-shear crystallization remain untested. No experiment established whether the fines constraint is attainable without sacrificing substantial recovery or throughput.

## 2. One additional experiment

I would repeat the batch-12 process with the same S1 volume, seed mass, temperatures, cooling history, and catalyst-to-reagent ratio, but halve both reagent and catalyst charges to 0.005 mol and 0.000625 mol. This is the most direct prospective test of the proposed loading/supersaturation mechanism while approximately preserving reaction stoichiometry.

It would distinguish three explanations:

1. **Supersaturation-driven nucleation:** fines should fall materially below batch 12's 0.865, while fractional recovery may decrease or remain similar and throughput would fall.
2. **A solvent/history floor independent of loading:** fines should remain near 0.865 despite the lower charge; this would weaken the loading interpretation.
3. **Insufficient crystal mass for growth:** lower loading could instead reduce size and increase fines, showing that batch 12 improved for another reason or that the loading effect is non-monotonic.

A replicate would ultimately be necessary because this single comparison would still be vulnerable to process variability, but it would be the most discriminating next experiment.

## 3. Least effectively used observation and least reliable prediction

The account used the paired in-process particle measurements and final-assay particle channels least effectively. Several batches showed sizable disagreement in crystal-size estimates—for example, batch 4 was about 0.069 before filtration versus 0.045 at final assay, while batch 8 was about 0.028 versus 0.071. I mostly relied on the final values instead of systematically using these pairs to estimate channel disagreement or determine whether filtration altered the representative slurry. The fines channels were more consistent near saturation, but the size discrepancies should have led to even more caution about inferred growth and ripening effects.

The least reliable held-out prediction is **Q09**. It filters after only a 60-second cooling step at 292 K, leaving a solid population that may be dominated by the introduced seed while crystal yield explicitly excludes seed mass. None of the campaign batches sampled such an early, seed-dominated endpoint. Consequently, particles_present is plausible, but the predicted seed-excluded recovery, size distribution, fines fraction, and resulting feasibility depend on poorly tested simulator semantics and kinetics. Q08 is also uncertain because its 315 K dissolution–recooling excursion exceeds the campaign's thermal-cycle range, but Q09 requires the larger extrapolation.
