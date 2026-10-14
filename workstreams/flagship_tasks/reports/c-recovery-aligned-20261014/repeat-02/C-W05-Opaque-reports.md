# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The materials are anonymous benchmark identities, so the following is a process-level interpretation rather than a claim about real molecular structures.

### Reaction-stage material effects

Under the common S0 reaction condition (0.04 mol reagent, 0.005 mol catalyst, 370 K for 3600 s), all catalysts produced high conversion, but selective product formation differed moderately. C0 and C1 gave HPLC yields around 0.56–0.58 with selectivity near 0.59 (batches 1–2); C2 was worse, with yield 0.527 and selectivity 0.526 (batch 3); C3 gave the highest screening HPLC yield, 0.611, with selectivity 0.600 (batch 4). I therefore interpreted C3 as the best catalyst in the screened region. These were unreplicated comparisons, so the exact catalyst ranking remains uncertain, particularly between C0, C1, and C3.

Solvent affected both reaction quality and crystallization. With C3 and broadly comparable processing, final reaction yield decreased from about 0.576 in S1 (batch 5) to 0.476 in S2 (batch 6) and 0.463 in S3 (batch 7); byproduct and degradation signals were also higher in S2/S3. S1 was therefore the best overall compromise rather than the best solvent on every individual particle metric.

A useful coupling relation is

`Y_crystal ≈ Y_reaction × f_crystallized × f_isolated`,

where crystal yield is explicitly seed-excluded and normalized to initial reagent. For recommended batch 12, reaction yield was 0.579 and crystal yield was 0.333, implying an apparent combined crystallization/isolation fraction of about 0.575. Thus incomplete selective reaction and incomplete transfer of target product from solution to isolated solids both limited recovery.

### Crystallization mechanism and history dependence

The early full-loading processes generated pure but very fine crystals. Batch 1 reached crystal yield 0.428 and purity 0.982, but fines were 0.997. Batch 2 reduced seed from 0.020 g to 0.001 g and used a warmer endpoint, yet fines remained 1.000 while recovery fell to 0.370. Batch 4 used the best screened catalyst and extended warm growth at 310 K, but still gave fines of 1.000. These observations ruled out the initial simple expectation that low seed and long cooling alone would solve particle quality.

Changing solvent helped numerically but did not meet the fines constraint at full loading. Batches 5–7 gave final fines of 0.849, 0.800, and 0.839 for S1, S2, and S3, respectively. S1 retained the greatest recovery, 0.404, compared with 0.340 for S2 and 0.231 for S3. High crystal purities throughout these batches show that crystallization strongly rejected reaction impurities even when its particle-size distribution was poor.

Several history modifications were ineffective within the tested scope:

- A 300→312→300 K annealing cycle gave fines 0.864 and recovery 0.397 in batch 8, essentially no improvement over batch 5.
- Fine thermal staging at full 0.04 mol loading gave fines 0.839 and recovery 0.418 in batch 9.
- Raising seed mass from 0.001 g to 0.050 g gave fines 0.869 and recovery 0.419 in batch 10.

Accordingly, neither mild annealing, full-loading staging, nor seed-dose increase was the controlling lever. Batch 3 also showed that an extremely small seed dose was below the simulator’s effective-seed precondition; its very low recovery therefore cannot be interpreted as a clean seed-dose result.

The decisive change was reduced reagent concentration. Batch 11 used 0.020 mol reagent in 0.08 L S1 with proportional C3 and staged cooling to 290 K. It improved CSD quality to 0.671 and reduced fines to 0.533 while maintaining purity 0.991 and recovery 0.351. Batch 12 reduced reagent to 0.018 mol and used finer 5 K stages from 320 to 290 K. It achieved CSD quality 0.819, size index 0.107, fines 0.228, purity 0.992, and recovery 0.333.

A plausible interpretation is that full loading generated excessive supersaturation and a large nucleation burst. In classical qualitative terms,

`J ∝ exp[-B/(ln S)^2]`,

where `J` is nucleation rate and `S` is supersaturation, while growth commonly varies more smoothly as `G ∝ (S−1)^g`. Lowering concentration and limiting the supersaturation increment per cooling stage can therefore suppress new-particle formation more strongly than it suppresses growth on existing crystals. This explains the sharp improvement in fines at reduced loading. It remains an interpretation: concentration and staging changed together between batches 11 and 12, so their individual contributions are unresolved.

### Revisions, uncertainty, and tradeoff

The working mechanism was revised three times. First, catalyst screening selected C3. Second, solvent screening selected S1 as the reaction/recovery compromise. Third, failures of annealing, seed-dose adjustment, and full-loading staging shifted the hypothesis from insufficient residence time or seeding to excessive concentration-driven nucleation.

The principal unresolved tradeoff is recovery versus particle quality. Batch 9 recovered 0.418 but had fines 0.839. Batch 11 recovered 0.351 but narrowly failed the fines limit at 0.533. Batch 12 reduced recovery to 0.333 but clearly satisfied both required constraints: purity 0.992 ≥ 0.80 and fines 0.228 ≤ 0.50. Because each optimized condition was run once and final-assay noise is nonzero, repeatability and the exact constraint boundary are uncertain. The large margin in batch 12’s fines result makes it more defensible than selecting the slightly higher-recovery batch 11.

The sealed recommendation therefore remains batch 12: 0.018 mol reagent, 0.08 L S1, 0.00225 mol C3; react at 370 K for 3600 s; cool to 320 K; add 0.001 g seed; cool through 315, 310, 305, 300, 295, and 290 K using 14400 s per 5 K stage; then filter. Its demonstrated seed-excluded crystal recovery was 0.333.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.35 | 0.16 | 0.57 |
| Q01 | crystal_purity | 0.985 | 0.945 | 1 |
| Q01 | crystal_size | 0.125 | 0.07 | 0.185 |
| Q01 | crystal_yield | 0.39 | 0.28 | 0.5 |
| Q02 | crystal_fines_fraction | 0.3 | 0.12 | 0.53 |
| Q02 | crystal_purity | 0.965 | 0.91 | 1 |
| Q02 | crystal_size | 0.145 | 0.08 | 0.215 |
| Q02 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q03 | crystal_fines_fraction | 0.28 | 0.1 | 0.55 |
| Q03 | crystal_purity | 0.982 | 0.94 | 1 |
| Q03 | crystal_size | 0.15 | 0.08 | 0.23 |
| Q03 | crystal_yield | 0.4 | 0.29 | 0.51 |
| Q04 | crystal_fines_fraction | 0.46 | 0.25 | 0.69 |
| Q04 | crystal_purity | 0.98 | 0.935 | 1 |
| Q04 | crystal_size | 0.105 | 0.055 | 0.17 |
| Q04 | crystal_yield | 0.41 | 0.3 | 0.52 |
| Q05 | crystal_fines_fraction | 0.43 | 0.22 | 0.66 |
| Q05 | crystal_purity | 0.98 | 0.935 | 1 |
| Q05 | crystal_size | 0.115 | 0.06 | 0.18 |
| Q05 | crystal_yield | 0.41 | 0.3 | 0.52 |
| Q06 | crystal_fines_fraction | 0.88 | 0.7 | 1 |
| Q06 | crystal_purity | 0.96 | 0.9 | 1 |
| Q06 | crystal_size | 0.045 | 0.015 | 0.085 |
| Q06 | crystal_yield | 0.44 | 0.33 | 0.55 |
| Q07 | crystal_fines_fraction | 0.39 | 0.19 | 0.63 |
| Q07 | crystal_purity | 0.981 | 0.935 | 1 |
| Q07 | crystal_size | 0.125 | 0.065 | 0.195 |
| Q07 | crystal_yield | 0.42 | 0.31 | 0.53 |
| Q08 | crystal_fines_fraction | 0.68 | 0.43 | 0.89 |
| Q08 | crystal_purity | 0.975 | 0.925 | 1 |
| Q08 | crystal_size | 0.07 | 0.03 | 0.125 |
| Q08 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q09 | crystal_fines_fraction | 0.9 | 0.69 | 1 |
| Q09 | crystal_purity | 0.93 | 0.82 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.085 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.14 |
| Q10 | crystal_fines_fraction | 0.72 | 0.47 | 0.93 |
| Q10 | crystal_purity | 0.96 | 0.89 | 1 |
| Q10 | crystal_size | 0.075 | 0.03 | 0.13 |
| Q10 | crystal_yield | 0.19 | 0.09 | 0.31 |
| Q11 | crystal_fines_fraction | 0.45 | 0.24 | 0.68 |
| Q11 | crystal_purity | 0.98 | 0.935 | 1 |
| Q11 | crystal_size | 0.11 | 0.055 | 0.175 |
| Q11 | crystal_yield | 0.41 | 0.3 | 0.52 |
| Q12 | crystal_fines_fraction | 0.86 | 0.66 | 1 |
| Q12 | crystal_purity | 0.955 | 0.89 | 0.995 |
| Q12 | crystal_size | 0.055 | 0.02 | 0.1 |
| Q12 | crystal_yield | 0.36 | 0.24 | 0.49 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All batches are expected to contain particles because each is effectively seeded. For Q01–Q02, S1 is predicted to retain more target product than S3, while S3 may give somewhat larger particles and fewer fines; this follows the observed solvent recovery ranking but remains weakly identified. For Q03–Q04, the lower seed charge should create fewer competing particles and a larger d50, whereas the high seed charge may suppress primary nucleation but increases the number population; prior evidence weakly favored the former effect. For Q05–Q06, gradual cooling should limit peak supersaturation and secondary nucleation, while the rapid drop should improve recovery slightly at the cost of severe fines. For Q07–Q08, the terminal cold hold should preserve slow-growth benefits; reheating to 315 K followed by rapid recooling may dissolve some solid and then regenerate fines, consistent with the previously unsuccessful annealing test. For Q09–Q10, two hours of continued growth at 292 K should materially increase seed-excluded recovery and particle size, but probably not enough to meet the fines limit. For Q11–Q12, doubling reagent loading at fixed solvent and catalyst is predicted to raise supersaturation and reduce catalyst-to-reagent ratio, producing many more fines and a somewhat lower normalized recovery. Purity is expected to remain high because crystallization previously rejected reaction impurities efficiently. Intervals are deliberately broad because catalyst C1 at 385 K, S0 at these low loadings, very long cooling histories, and several paired interventions were not directly replicated; intervals represent epistemic process uncertainty around noise-free outcomes, not final-assay measurement noise.

## K2

### 1. Status of the main claims

**Supported by direct observations**

- **C3 was the best catalyst in the limited S0 screen.** At 370 K for 3600 s, batch 4 had HPLC yield 0.611 and selectivity 0.600, versus yields of about 0.584, 0.560, and 0.527 for C0, C1, and C2 in batches 1–3. The ranking is observed, but its generality is interpretive because each catalyst was tested once.
- **Solvent identity affected both reaction and crystallization.** With C3, batches 5–7 showed lower recovery moving from S1 (0.404) to S2 (0.340) and S3 (0.231). Their fines also differed numerically. These are direct observations; assigning them to solubility or nucleation behavior is interpretation.
- **Crystallization rejected impurities effectively.** Many batches had imperfect reaction selectivity yet final crystal purity near 0.97–1.00, including batches 1, 5–7, 11, and 12. Selective impurity rejection is therefore strongly supported within the tested system.
- **Reduced loading was associated with much better particle quality.** Full-loading S1 batches 5, 8–10 had fines around 0.84–0.87. Batch 11 at 0.020 mol gave 0.533, and batch 12 at 0.018 mol gave 0.228. This supports a loading-sensitive regime, although loading and cooling-stage spacing were confounded between batches 11 and 12.

**Contradicted or not supported in the tested scope**

- **Simply reducing seed and cooling slowly would solve fines.** Batch 2 used only 0.001 g seed but still had fines of 1.000. Batch 4 also retained essentially all fines after extended warm growth.
- **A mild heat–cool annealing cycle would remove fines.** Batch 8 gave fines 0.864, no improvement over the comparable noncycled batch 5 at 0.849.
- **More seed would suppress secondary nucleation enough to improve quality.** Raising seed from 0.001 g to 0.050 g did not help: batch 10 had fines 0.869. This result does not establish that seed is always harmful, only that the tested increase was ineffective.
- **Fine thermal staging alone was sufficient at full loading.** Batch 9 used fine staging but retained fines of 0.839.

**Still untested or unresolved**

- The proposed supersaturation–nucleation mechanism is plausible but not directly measured. No solubility, supersaturation, nucleation-rate, or growth-rate observations were available.
- The respective contributions of the lower loading and finer 5 K staging in batch 12 remain unresolved.
- Repeatability is unknown because the optimized conditions were not replicated.
- The catalyst ranking outside S0 and the solvent ranking outside C3 were not tested factorially.
- Batch 3 does not provide a clean test of ultralow seeding because its seed population failed the effective-seed precondition.
- The prediction recipes using C1 at 385 K, low loading, quenching, and extremely long cooling histories lie substantially outside the experimental campaign.

### 2. One additional experiment

I would run the **missing cross-condition between batches 11 and 12**: use 0.020 mol reagent, 0.08 L S1, proportional C3 catalyst, the same reaction and 0.001 g seed, but apply batch 12’s 5 K/14400 s stages from 320 to 290 K.

This would distinguish two leading explanations for batch 12:

1. **Cooling-stage spacing is dominant.** Fines should approach batch 12’s value, roughly 0.23–0.30, while recovery should remain near batch 11’s approximately 0.35.
2. **A concentration threshold is dominant.** Fines should remain near batch 11’s approximately 0.53 despite the finer schedule.
3. **Both factors interact.** An intermediate fines fraction, approximately 0.30–0.45, would be expected.

A result near or above 0.53 would weaken the claim that staging caused the improvement. A result near 0.23 would weaken the claim that the modest change from 0.020 to 0.018 mol was decisive. One experiment would not establish repeatability, but it would remove the largest designed confound in the mechanistic account.

### 3. Least effectively used observation and least reliable prediction

**Least effectively used observation:** batch 3’s failed effective-seed precondition. I treated its very low recovery primarily as uninterpretable, but it still supplied useful boundary information: 0.000001 g was not an operationally effective seed population under that history. The account could have used this more clearly to bound the seed regime and to distinguish “low seed” from “no effective seeding.” Its particle and recovery outcomes should not have been compared quantitatively with successfully seeded batches.

**Least reliable held-out prediction:** Q09. It filters after only a 60-second cooling step to 292 K. No campaign batch examined such a short crystallization interval, and all useful recovery observations followed hours of cooling or growth. The filtered solids might be dominated by the added seed, while crystal yield explicitly excludes seed. Consequently, small differences in how quickly target product deposits during that minute could change the predicted yield by a large relative amount. Particle size, fines, and apparent purity would also be unusually sensitive to the seed population and to poorly constrained early-time kinetics. Q10 is similarly uncertain, but its additional two-hour growth period makes it less extreme than Q09.
