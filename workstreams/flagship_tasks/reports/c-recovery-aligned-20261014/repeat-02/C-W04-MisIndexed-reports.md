# C-W04-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Proposed reaction and crystallization mechanism

A useful minimal reaction scheme is

R → P, R → B, and P → D,

where R is limiting reagent, P is target product, B is a competing byproduct, and D is degradation material. A corresponding kinetic model is

dR/dt = −(kP + kB)R,

dP/dt = kP R − kD P.

This explains why nearly complete conversion did not guarantee high target yield: the 350–380 K experiments generally reached conversion near 1, while selectivity and liquid-phase yield varied substantially. Temperature and residence time therefore changed the competition among target formation, byproduct formation, and degradation rather than simply determining conversion.

Crystallization can be described through supersaturation, σ = C/C*(T, solvent) − 1. Crystal growth may scale as G = kgσ^g, whereas primary and secondary nucleation may scale more steeply, J = kJσ^b, commonly with b > g. Thus a rapid increase in supersaturation can create many small crystals even when solid recovery is high. Because the fines constraint is a number fraction, numerous low-mass secondary nuclei can cause failure without greatly changing total recovered mass.

The measured seed-excluded crystal yield is approximately

Ycrystal = nP,solid / nR,0,

so it couples reaction selectivity, degradation, solubility, nucleation, growth, and isolation losses. Added seed contributes surface area and controls nucleation history but is excluded from the numerator.

### Material effects

Solvent S2 was used throughout the developed process. Its dossier suggested relatively low solubility and nucleation tendency, high crystal-growth propensity, and low impurity occlusion. The observations are consistent with the last of these: final crystal purities were generally about 0.98–1.00. However, no other solvent was experimentally compared, so superiority of S2 over S0, S1, or S3 remains an untested interpretation rather than an experimental conclusion.

Catalyst identity affected the coupled reaction/crystallization result. Under the batch-7-style process:

- C1, batch 7: crystal yield 0.459, purity 0.982, fines 0.479.
- C2, batch 8: yield 0.414, purity 0.979, fines 0.510; the fines constraint was missed.
- C3, batch 9: yield 0.441, purity 0.981, fines 0.493.
- C0, batch 10: yield 0.450, purity 0.977, fines 0.497.

These observations support C1 for this recipe. They do not establish an intrinsic catalyst ranking because each alternative was tested only once and the downstream particle distribution responds to the product and impurity concentrations generated upstream.

### Reaction–crystallization coupling

The clearest coupling is between reaction outcome, product loading, and secondary nucleation. Batch 2 used C1/S2 at 350 K for 7200 s and produced relatively poor reaction performance: liquid yield about 0.363 and selectivity about 0.375. Its crystal recovery was only 0.287, but fines were low at 0.417. In contrast, batches 3–4 generated more target product and recovered 0.430–0.445 as crystals, yet their final fines fractions were 0.508–0.529. The interpretation is that higher product loading improved recoverable mass but also generated greater supersaturation during cooling, raising the number of secondary nuclei.

The best observed compromise occurred around a 370–375 K, 3600 s reaction treatment. Batch 6 at 370 K gave yield 0.452, purity 1.000, and fines 0.481. Batch 7 at 375 K gave the campaign-high feasible yield of 0.459 with purity 0.982 and fines 0.479. This suggests a local kinetic window in which target formation was high enough for good recovery without pushing the subsequent crystallization too far into nucleation-dominated behavior. The data do not justify a precise optimum between 370 and 375 K.

Impurities may also alter nucleation, growth, or surface poisoning. The generally high solid purity despite moderate reaction selectivity suggests that S2 crystallization rejected much of the reaction impurity from the lattice. That exclusion is inferred from the mismatch between liquid reaction selectivity and final solid purity; direct impurity-partition measurements were not performed.

### Process-history dependence

Thermal trajectory mattered, not merely the final temperature. In batch 1, material was cooled to 270 K, then a normal wait allowed warming to about 298 K, followed by recooling. The final recovery was good (0.432) and purity high (0.989), but fines were severe at 0.724. A plausible mechanism is partial dissolution during warming followed by renewed nucleation on recooling. This interpretation is physically consistent but confounded because batch 1 was not paired with an otherwise identical controlled thermal cycle.

Subsequent work therefore used `cool_crystallize` operations for cold residence rather than an uncontrolled wait. Batch 3, with slow cooling and cold residence, reduced fines dramatically relative to batch 1, although its final value of 0.508 remained just above specification.

The initial hypothesis that simply lowering seed mass and extending cold residence would remove fines was not supported. Batch 4 reduced seed from 0.005 g to 0.001 g and added cold time, yet final fines were 0.529. This indicates that spontaneous or secondary nucleation, rather than the number of deliberately added seeds alone, controlled much of the number distribution.

A second revision concerned endpoint temperature. Holding at 290 K was expected to favor controlled growth over nucleation, but batch 5 instead gave lower recovery (0.401) and worse fines (0.613). One interpretation is that insufficient driving force limited growth on the seed population while leaving a poorly matured fine population. Alternative explanations include run variability or an unfavorable interaction between dissolution and nucleation history.

More elaborate staged cooling through 300, 285, and 270 K in batch 11 was feasible—yield 0.447, purity 0.996, fines 0.481—but did not improve recovery over the simpler batch-7 trajectory. Thus extra staging was not demonstrably beneficial within the tested schedules.

### Uncertainty and unresolved tradeoff

The main unresolved issue is the recovery–fines frontier. High product generation tends to increase recovery but can also increase supersaturation and fines. Several results lay very close to the 0.50 limit. Independent particle-size and final-assay readings sometimes crossed the boundary: batch 3 gave about 0.497 by particle measurement but 0.508 by final assay; batch 4 gave about 0.494 and 0.529, respectively. These differences are compatible with measurement noise, slurry heterogeneity, or sampling variation and warn against overinterpreting hundredths near the threshold.

Batch 12 repeated the batch-7 recipe and remained feasible, with yield 0.450, purity 0.997, and fines 0.494. This supports reproducibility of the operating region, although its fines margin was smaller and its recovery was below batch 7. Batches 6 and 11 offered somewhat more apparent fines margin but lower observed recovery. Consequently, batch 7 remains the sealed recommendation because it had the highest measured recovery among constraint-satisfying batches, while the evidence also shows that its quality margin is not large.

Untested alternatives include solvent screening, factorial catalyst–solvent interactions, controlled agitation during crystallization, seed-size rather than seed-mass variation, antisolvent or concentration changes, and replicated experiments sufficient to estimate process variance. These could clarify whether the observed frontier is fundamental or can be shifted toward simultaneously higher recovery and a more robustly low fines fraction.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.44 | 0.31 | 0.57 |
| Q01 | crystal_purity | 0.9 | 0.83 | 0.96 |
| Q01 | crystal_size | 0.1 | 0.04 | 0.17 |
| Q01 | crystal_yield | 0.3 | 0.2 | 0.4 |
| Q02 | crystal_fines_fraction | 0.32 | 0.2 | 0.45 |
| Q02 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q02 | crystal_size | 0.14 | 0.07 | 0.22 |
| Q02 | crystal_yield | 0.32 | 0.22 | 0.43 |
| Q03 | crystal_fines_fraction | 0.55 | 0.39 | 0.7 |
| Q03 | crystal_purity | 0.86 | 0.76 | 0.94 |
| Q03 | crystal_size | 0.13 | 0.05 | 0.23 |
| Q03 | crystal_yield | 0.18 | 0.1 | 0.27 |
| Q04 | crystal_fines_fraction | 0.43 | 0.3 | 0.56 |
| Q04 | crystal_purity | 0.89 | 0.81 | 0.95 |
| Q04 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q04 | crystal_yield | 0.2 | 0.12 | 0.29 |
| Q05 | crystal_fines_fraction | 0.4 | 0.28 | 0.53 |
| Q05 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q05 | crystal_size | 0.11 | 0.05 | 0.18 |
| Q05 | crystal_yield | 0.21 | 0.13 | 0.3 |
| Q06 | crystal_fines_fraction | 0.69 | 0.54 | 0.82 |
| Q06 | crystal_purity | 0.86 | 0.75 | 0.94 |
| Q06 | crystal_size | 0.055 | 0.015 | 0.11 |
| Q06 | crystal_yield | 0.22 | 0.13 | 0.31 |
| Q07 | crystal_fines_fraction | 0.35 | 0.24 | 0.48 |
| Q07 | crystal_purity | 0.91 | 0.84 | 0.97 |
| Q07 | crystal_size | 0.14 | 0.07 | 0.22 |
| Q07 | crystal_yield | 0.22 | 0.14 | 0.31 |
| Q08 | crystal_fines_fraction | 0.67 | 0.51 | 0.81 |
| Q08 | crystal_purity | 0.88 | 0.78 | 0.95 |
| Q08 | crystal_size | 0.07 | 0.02 | 0.14 |
| Q08 | crystal_yield | 0.18 | 0.09 | 0.27 |
| Q09 | crystal_fines_fraction | 0.84 | 0.7 | 0.94 |
| Q09 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.09 |
| Q09 | crystal_yield | 0.03 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.63 | 0.47 | 0.78 |
| Q10 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q10 | crystal_size | 0.07 | 0.02 | 0.14 |
| Q10 | crystal_yield | 0.1 | 0.04 | 0.17 |
| Q11 | crystal_fines_fraction | 0.37 | 0.25 | 0.5 |
| Q11 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q11 | crystal_size | 0.12 | 0.05 | 0.2 |
| Q11 | crystal_yield | 0.22 | 0.14 | 0.31 |
| Q12 | crystal_fines_fraction | 0.57 | 0.42 | 0.71 |
| Q12 | crystal_purity | 0.85 | 0.74 | 0.93 |
| Q12 | crystal_size | 0.08 | 0.025 | 0.15 |
| Q12 | crystal_yield | 0.3 | 0.2 | 0.4 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S3 is expected to offset its somewhat weaker reaction activity with lower solubility, nucleation tendency, and impurity occlusion than S1, giving cleaner, coarser crystals and slightly higher overall recovery. Q03–Q04: more seed supplies controlled growth area and suppresses uncontrolled nucleation, but distributes product over more particles, so Q04 has fewer fines but a smaller median size. Q05–Q06: gradual cooling limits the supersaturation peak; crash cooling should preserve similar recovery but generate many more fines. Q07–Q08: reheating after crystallization can dissolve solids and the short recooling can renucleate them, analogous to the poor particle outcome after warming and recooling in campaign batch 1. Q09–Q10: continued growth at 292 K raises seed-excluded recovery and size and lowers fines, although two hours is predicted to remain insufficient for feasibility. Q11–Q12: doubled reagent loading increases fractional recovery by reducing the relative dissolved-product loss, but greater supersaturation increases nucleation, occlusion, and fines. Intervals are deliberately broad because S0, S1, and S3 were not screened as solvents in the campaign, these recipes use much smaller charge and much larger seed-to-reagent ratios than the campaign, and prior paired particle/final-assay readings sometimes differed across the 0.50 fines boundary.

## K2

## 1. Status of the main claims

### Supported within the tested campaign scope

- **A local C1/S2 operating region near 370–375 K gave the best feasible recovery.** Direct observations: batch 6 gave crystal yield 0.452, purity 1.000, and fines 0.481; batch 7 gave 0.459, 0.982, and 0.479. Batch 12 repeated the batch-7 recipe and remained feasible at 0.450, 0.997, and 0.494. Interpretation: this is a useful local operating window, not proof of a sharp temperature optimum.
- **Reaction and crystallization were coupled through product/impurity loading.** Direct observations: batch 2 had low liquid yield and selectivity and only 0.287 crystal yield, but fines were 0.417; higher-recovery batches 3–4 reached 0.430–0.445 crystal yield but had fines of 0.508–0.529. Interpretation: greater target loading probably raised supersaturation and secondary nucleation. The association is supported, but causality was not isolated because reaction temperature, time, and crystallization history were not varied independently.
- **C1 was the best tested catalyst for the selected recipe.** Batch 7 with C1 exceeded C2 in batch 8 (yield 0.414, fines 0.510), C3 in batch 9 (0.441, 0.493), and C0 in batch 10 (0.450, 0.497). This is direct comparative evidence, although each alternative had only one run.
- **A warm excursion followed by recooling was associated with poor particles.** Batch 1, which warmed after reaching 270 K and was then recooled, had fines of 0.724 despite yield 0.432 and purity 0.989. Monotonic schedules in batches 6, 7, 11, and 12 gave fines near 0.48–0.49. The observation supports process-history dependence; dissolution followed by renucleation remains an interpretation because batch 1 was not a matched thermal-history experiment.

### Contradicted or weakened

- **Lower seed dose plus more cold residence would necessarily suppress fines.** Batch 4 used less seed and additional cold time but had fines of 0.529, compared with 0.508 in batch 3. This contradicted the simple seed-number hypothesis, although measurement variation prevents a precise seed-effect estimate.
- **A warmer 290 K crystallization endpoint would necessarily favor clean growth.** Batch 5 produced lower recovery, 0.401, and worse fines, 0.613. That contradicts the directional prediction under the tested schedule; it does not prove that every warmer or staged trajectory is inferior.
- **More elaborate staging would improve the recovery–quality balance.** Batch 11’s 300→285→270 K schedule was feasible, with yield 0.447 and fines 0.481, but did not outperform the simpler batch-7 schedule.

### Still untested or unresolved

- **Solvent superiority is untested.** All campaign batches used S2. Its high purity is consistent with the dossier’s low-occlusion description, but no experimental S0/S1/S3 comparison was made.
- **The proposed R→P, R→B, P→D kinetic network is a useful interpretation, not an identified mechanism.** Conversion, selectivity, byproduct signal, and degradation warning are compatible with it, but no time series or species-specific mapping was obtained.
- **The exact cause of fines remains unresolved.** Supersaturation, secondary nucleation, seed population, impurities, and thermal cycling are plausible contributors. The campaign did not independently manipulate them.
- **Robust compliance near fines = 0.50 remains uncertain.** Particle and final-assay readings crossed the boundary in batches 3 and 4, and batch 12 finished at 0.494. Batch 7 is the highest observed feasible recovery, but its constraint margin is modest.

## 2. One additional experiment

I would run a **matched split-batch thermal-history experiment**. I would perform one C1/S2 reaction under the batch-7 upstream conditions, quench and homogenize it, then divide it equally into two containers. Both aliquots would receive the same seed mass per mole and the same total crystallization time. Arm A would undergo monotonic slow cooling to 270 K; arm B would reach 270 K, be reheated to approximately 315 K, and then recooled to 270 K. Pre-split HPLC would document the common reaction state, and each arm would receive particle-size measurement and a final assay.

This would distinguish the proposed **partial dissolution/renucleation mechanism** from explanations based on different reaction conversion, impurity loading, or ordinary batch-to-batch variability.

- If thermal cycling causes dissolution and renewed nucleation, arm B should have smaller particles, more fines, and possibly lower recovered yield than arm A while retaining similar solid purity.
- If the batch-1 result arose mainly from upstream chemistry or random variation, the two arms should be similar within measurement uncertainty.
- If reheating instead promotes effective ripening, arm B could show larger particles and fewer fines; that outcome would directly contradict my current interpretation.

## 3. Least effectively used observation and least reliable prediction

The observation used least effectively was **batch 5’s combination of a 290 K endpoint, lower recovery, and substantially worse fines**. I described it as possibly reflecting insufficient growth driving force, but that explanation is weak: lower supersaturation should also reduce nucleation, and the experiment did not measure particles over time or separate dissolution, growth, and nucleation. Batch 5 therefore deserved more weight as evidence that my simple supersaturation narrative was incomplete.

The least reliable held-out prediction is **Q09**, the 60-second crystallization followed immediately by filtration. The campaign contained no crystallization on that timescale, so its seed-excluded yield and particle distribution require a large kinetic extrapolation. Moreover, the large seed-to-reagent ratio makes particles likely even if almost no new target crystallizes, creating uncertainty about how seed-dominated solids affect reported purity, size, and fines. The sealed Q09 values should therefore be treated as substantially less secure than predictions for long, monotonic cooling schedules. The Q01–Q02 solvent comparison is also weak because those solvents were never tested, but at least the public material dossier supplied qualitative priors for that comparison.
