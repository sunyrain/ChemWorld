# C-W01-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Observed process landscape
All materials were anonymous benchmark materials, so the conclusions are empirical within this campaign rather than claims about real chemical identities. Catalyst C1 and solvent S2 formed the principal process system. The recommended batch remains **batch 7**.

Two distinct regimes appeared:

- **High target loading:** substantial seed-excluded crystal recovery, high purity, but almost entirely sub-20 µm particles.
- **Low target loading with a large seed charge:** coarse, high-quality particles meeting the fines limit, but very little seed-excluded product was recovered.

No batch combined the quality constraints with the 0.10 initial recovery target. Because 0.10 was not a hard constraint, batch 7 was selected as the highest observed recovery among the constraint-compliant batches.

### 2. Material effects

#### Solvent
The nominal dossier suggested S2 should favor crystallization because it had relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The experiments partly supported that prior.

The closest solvent comparison was:

- **Batch 2, S2:** crystal recovery 0.524, purity 0.987, CSD quality 0.546, fines 1.000.
- **Batch 5, S1:** recovery 0.465, purity 0.980, CSD quality 0.486, fines 1.000.

Both used 0.04 mol reagent, C1, a short 360 K reaction, 0.01 g seed, and two 290 K crystallization periods. S2 was numerically better in recovery, purity, CSD quality, and reaction selectivity, consistent with its nominal properties. However, the comparison was not replicated and stirring differed slightly, so it is suggestive rather than a definitive solvent ranking. Neither solvent cured secondary nucleation at high loading.

S0 and S3 were not experimentally characterized. Their effects, as well as hidden fixed solvent residuals, remain untested alternatives.

#### Catalyst
Only C1 was used, based initially on its favorable nominal activity and moderate variability. Thus the campaign establishes that C1 can provide near-complete conversion under the tested conditions, but it provides no experimental evidence that C1 is superior to C0, C2, or C3.

### 3. Reaction mechanism and residence-time effects
A useful reaction-side representation is

`reactant -> target product -> degradation products`

with a competing branch

`reactant -> byproducts`.

For discussion, conversion and selectivity can be represented as

`X = reacted reactant / charged reactant`

`S = target formed / (target formed + byproducts formed)`.

The long hot history in **batch 1** produced complete conversion but low selectivity, about 0.395, and a degradation warning of about 0.292. With the hot residence shortened from roughly 7200 s to 1800 s, **batch 2** retained complete conversion while selectivity rose to about 0.675 and the degradation warning fell to about 0.091. This is consistent with target degradation or continued byproduct formation after reactant depletion.

That interpretation motivated the later 1800–3600 s reaction residence. It is not a clean kinetic proof: batches 1 and 2 also differed in crystallization temperature and seed charge. Nonetheless, the combination of complete conversion and reduced degradation makes prolonged heating unattractive.

At reduced catalyst and reagent loading, reaction results were less uniform. For example, batch 6 reached conversion about 0.916, whereas batches 7–9 were near complete after 3600 s. This suggests that catalyst amount and residence time should scale with charge rather than being reduced indiscriminately.

### 4. Reaction–crystallization coupling
The coupling is principally through the target concentration entering crystallization. A useful approximation is

`C_target,0 ∝ n_reagent × X × S / V`.

The crystallization driving force is supersaturation,

`σ = C_target / C*(T, solvent) - 1`,

where `C*` is the equilibrium solubility. Crystal growth and nucleation may then be represented qualitatively as

`G = k_g σ^g`

`J = k_n σ^m`,

with nucleation commonly more sensitive to supersaturation than growth (`m > g`). This explains the main observation: high loading or deeper cooling raised recovery but drove a much larger number of new, fine particles.

The relevant product metric was

`R_c = seed-excluded target recovered in crystals / target present before separation`.

Consequently, reaction yield and crystallization recovery are different quantities. Improving reaction yield increases the absolute target concentration and can indirectly increase supersaturation, while `R_c` measures only downstream recovery from the target already present.

Crystal purity stayed high even when reaction selectivity was moderate. For example, batch 2 had reaction selectivity around 0.675 but crystal purity around 0.987. This indicates substantial impurity rejection by the S2 crystal lattice or mother-liquor partitioning. It should not be interpreted as the reaction itself being 99% selective.

### 5. Seed surface versus spontaneous nucleation
The low-loading experiments imply competition between solute capture on seed surface and formation of new nuclei. A qualitative dimensionless relationship is

`Π ≈ supersaturation-generation rate / (available seed area × growth capacity)`.

Low `Π` favors growth on existing seeds; high `Π` favors nucleation. Seed area depends on seed mass and unknown seed size, approximately

`A_seed ∝ m_seed / (ρ d_seed)`.

At 0.005 mol reagent, 0.08 L S2, and 0.05 g seed, direct cooling to 290 K produced a seed-dominated coarse population:

- **Batch 7:** recovery 0.0119, purity 0.992, fines 0.000, normalized crystal size 0.409 (about 102 µm d50), CSD quality 0.998.
- **Batch 10**, with much longer 290 K aging: recovery 0.0090, purity 0.991, fines 0.011, normalized size 0.390.

Both comfortably satisfied purity and fines constraints, but their seed-excluded recovery was very low. The high seed-to-product ratio likely provided ample growth surface while also making the number distribution dominated by coarse seed-derived particles.

Increasing reagent to 0.007 mol at the same solvent volume and seed charge crossed into a fine-particle regime:

- **Batch 9:** recovery 0.0730, purity 0.990, fines 0.995.

At 0.010 mol:

- **Batch 6:** recovery 0.238, purity 1.000, fines 0.779.

Thus the transition was strongly nonlinear rather than a smooth recovery–quality response.

### 6. Process-history dependence

#### Cooling depth
Cooling depth was a powerful but unfavorable recovery lever. With the batch-7 loading, changing the endpoint from 290 K to 280 K gave:

- **Batch 8:** recovery 0.0908, purity 0.989, fines 0.981.

The recovery approached 0.10, but the fines constraint failed severely. This supports a nucleation threshold between the two thermal histories.

#### Isothermal aging
Extending the 290 K hold did not increase recovery materially. Batch 10 used about ten cooling/holding intervals but had essentially the same very low recovery as batch 7. Once the slurry reached its low-supersaturation state, additional time supplied little further thermodynamic driving force. The difference between batch-7 and batch-10 recovery is much smaller than assay uncertainty.

At high loading, extended aging also failed to coarsen the population: **batch 3**, after extensive 300 K aging, still had fines about 0.995 and recovery about 0.496. Aging alone therefore did not reverse an already established high particle number.

#### Staged cooling
The hypothesis that small cooling increments would feed growth while avoiding nucleation was rejected in the tested form. **Batch 11** used sequential 310, 305, 300, 295, 290, 285, and 280 K stages. It reached recovery 0.0627, but fines remained about 0.982 and CSD quality fell to about 0.090. Slowly crossing the nucleation boundary did not prevent many particles from appearing.

#### Thermal cycling and reheating
Two variants were tried:

- **Batch 4:** unseeded cooling followed by repeated 312/305 K cycles; recovery 0.493, purity 1.000, fines 1.000.
- **Batch 12:** 0.010 mol loading, 0.05 g seed, cooling to 275 K followed by prolonged reheating at 300 K; recovery 0.121, purity 0.997, fines 1.000.

The intended interpretation was selective dissolution of small crystals followed by growth of large ones. The observed results show that these temperature cycles did not dissolve enough fines, or that fines regenerated during the history. Batch 12 demonstrated that recovery above 0.10 was possible, but not together with the fines constraint.

### 7. Revisions to the working mechanism
The initial hypothesis was that S2, seeded slow cooling, and a long cold hold would simultaneously give high recovery, high purity, and low fines. **Batch 1** rejected that hypothesis: purity and recovery were good, but fines were about 0.997.

The next hypothesis attributed the failure to insufficient growth time. Batches 3 and 10 rejected that explanation: long holds did not materially improve the recovery–fines balance.

Thermal cycling and staged cooling were then considered as ways to remove or avoid fines. Batches 4, 11, and 12 rejected those implementations.

The final revision was that **upstream target loading, relative to seed surface, controls whether the process enters a nucleation-dominated or seed-growth-dominated regime**. Batches 6–10 support that interpretation. It explains why dilution solved the fines problem but exposed a fundamental quality/recovery tradeoff.

### 8. Uncertainty and unresolved tradeoff
Final-assay standard uncertainties were approximately 0.010 for crystal recovery and purity, 0.018 for fines and CSD quality, and 0.025 for normalized size. Therefore:

- Batch 7 is safely above the purity requirement and safely below the fines limit.
- Its recovery of 0.0119 is close to the recovery measurement uncertainty and should be regarded as very low.
- Batch 10 is also quality-compliant. Its observed recovery, 0.0090, differs from batch 7 by only about 0.0028—far below the assay uncertainty. Batch 7 is the highest observed qualifying result, not demonstrably superior in a statistical sense.
- Results near fines 0 or 1 may also reflect bounded/clipped reporting, although both are far enough from the 0.50 constraint to leave their pass/fail status unambiguous.

The campaign therefore leaves an unresolved recovery–quality frontier: increasing supersaturation improves seed-excluded recovery but produces excessive numbers of fines; suppressing nucleation gives coarse, pure material but almost no new recovered product.

### 9. Untested alternatives
The following remain plausible but were not established:

- using seeds with a controlled, independently larger initial size or narrower seed distribution;
- continuous antisolvent or reagent feeding to limit instantaneous supersaturation;
- direct removal or classification of fines after crystallization;
- different S2/S1 solvent mixtures, since only pure benchmark solvents were available;
- systematic catalyst screening to increase target concentration without increasing impurity burden;
- feedback cooling based on measured supersaturation rather than fixed temperature stages;
- optimized filtration or washing, including resuspension, to alter recovered particle-number distributions.

Within the tested action space, batch 7 represents the observed constraint-compliant regime, while batches 2 and 12 illustrate the opposite, high-recovery/high-fines regime.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.9 | 0.68 | 0.99 |
| Q01 | crystal_purity | 0.96 | 0.88 | 1 |
| Q01 | crystal_size | 0.085 | 0.035 | 0.18 |
| Q01 | crystal_yield | 0.47 | 0.28 | 0.65 |
| Q02 | crystal_fines_fraction | 0.96 | 0.79 | 1 |
| Q02 | crystal_purity | 0.93 | 0.82 | 0.99 |
| Q02 | crystal_size | 0.058 | 0.02 | 0.13 |
| Q02 | crystal_yield | 0.34 | 0.16 | 0.54 |
| Q03 | crystal_fines_fraction | 0.995 | 0.91 | 1 |
| Q03 | crystal_purity | 0.89 | 0.76 | 0.97 |
| Q03 | crystal_size | 0.025 | 0.006 | 0.07 |
| Q03 | crystal_yield | 0.29 | 0.12 | 0.48 |
| Q04 | crystal_fines_fraction | 0.95 | 0.74 | 1 |
| Q04 | crystal_purity | 0.91 | 0.79 | 0.98 |
| Q04 | crystal_size | 0.065 | 0.025 | 0.15 |
| Q04 | crystal_yield | 0.27 | 0.1 | 0.46 |
| Q05 | crystal_fines_fraction | 0.95 | 0.73 | 1 |
| Q05 | crystal_purity | 0.91 | 0.79 | 0.98 |
| Q05 | crystal_size | 0.062 | 0.024 | 0.15 |
| Q05 | crystal_yield | 0.27 | 0.1 | 0.46 |
| Q06 | crystal_fines_fraction | 0.995 | 0.91 | 1 |
| Q06 | crystal_purity | 0.89 | 0.75 | 0.97 |
| Q06 | crystal_size | 0.03 | 0.008 | 0.075 |
| Q06 | crystal_yield | 0.28 | 0.11 | 0.48 |
| Q07 | crystal_fines_fraction | 0.97 | 0.8 | 1 |
| Q07 | crystal_purity | 0.9 | 0.78 | 0.98 |
| Q07 | crystal_size | 0.052 | 0.018 | 0.125 |
| Q07 | crystal_yield | 0.27 | 0.1 | 0.47 |
| Q08 | crystal_fines_fraction | 0.91 | 0.62 | 0.99 |
| Q08 | crystal_purity | 0.92 | 0.8 | 0.99 |
| Q08 | crystal_size | 0.073 | 0.027 | 0.17 |
| Q08 | crystal_yield | 0.22 | 0.07 | 0.41 |
| Q09 | crystal_fines_fraction | 0.08 | 0 | 0.3 |
| Q09 | crystal_purity | 0.95 | 0.84 | 1 |
| Q09 | crystal_size | 0.36 | 0.18 | 0.58 |
| Q09 | crystal_yield | 0.004 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.32 | 0.07 | 0.68 |
| Q10 | crystal_purity | 0.94 | 0.82 | 0.99 |
| Q10 | crystal_size | 0.22 | 0.09 | 0.43 |
| Q10 | crystal_yield | 0.04 | 0.005 | 0.12 |
| Q11 | crystal_fines_fraction | 0.95 | 0.73 | 1 |
| Q11 | crystal_purity | 0.91 | 0.79 | 0.98 |
| Q11 | crystal_size | 0.064 | 0.024 | 0.15 |
| Q11 | crystal_yield | 0.27 | 0.1 | 0.47 |
| Q12 | crystal_fines_fraction | 0.995 | 0.92 | 1 |
| Q12 | crystal_purity | 0.86 | 0.71 | 0.96 |
| Q12 | crystal_size | 0.033 | 0.008 | 0.085 |
| Q12 | crystal_yield | 0.58 | 0.38 | 0.76 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The six pairs isolate solvent (Q01/Q02), seed charge (Q03/Q04), gradual versus crash cooling (Q05/Q06), a terminal thermal cycle (Q07/Q08), short versus extended shallow crystallization (Q09/Q10), and loading (Q11/Q12). I expect S1 to outperform S3 in recovery and growth because its nominal solubility, nucleation, and occlusion tendencies are lower. For S0, the long descent to 278.15 K is expected to cross a secondary-nucleation threshold regardless of seed charge; more seed, gradual cooling, or reheating may modestly coarsen the population but probably will not bring fines below 0.50. Crash cooling should give the finest distribution. Q09 should contain mainly the added seed with negligible seed-excluded recovery, while the 292 K hold in Q10 permits some growth and nucleation, raising recovery and fines but remaining marginally feasible on the point estimate. Doubling loading in Q12 should strongly raise recovery while driving nucleation, occlusion, and fines. Intervals are deliberately broad because S0 and S3 were not tested in the sealed campaign, the 385 K reaction history is extrapolative, and prior results showed sharp, nonlinear changes in fines near supersaturation thresholds.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **A strong recovery–fines tradeoff exists in the tested S2 process.** Batch 7 met the quality constraints but had only about 0.0119 crystal recovery, whereas batch 8 reached about 0.0908 recovery after deeper cooling but had about 0.981 fines. Batch 12 exceeded 0.10 recovery but had fines of 1.0.
- **Cooling depth can trigger a sharp nucleation transition.** Batches 7 and 8 were closely matched except for the 290 versus 280 K endpoint; the deeper endpoint greatly increased recovery and destroyed particle quality.
- **Nominal loading also controls the transition.** At 290 K, batch 7 used 0.005 mol and had zero reported fines, while batch 9 used 0.007 mol and had about 0.995 fines. This is direct evidence of a narrow operating window, although nominal loading is only a proxy for actual target concentration.
- **Long isothermal aging did not improve seed-excluded recovery.** Batch 10 extended the 290 K history relative to batch 7 but retained similarly low recovery and low fines. Their recovery difference is below assay uncertainty.
- **Crystal purity was robustly high.** Batches 1–12 generally gave purity near 0.98–1.00 despite moderate reaction selectivity, directly showing strong downstream impurity rejection in the tested systems.

### Supported as interpretations, but not proven
- **Secondary nucleation is the likely cause of the fines transition.** The abrupt response to loading and cooling depth is consistent with nucleation being more supersaturation-sensitive than growth. No supersaturation or particle-number trajectory was measured directly, so this remains an interpretation.
- **Long hot residence promotes target degradation or byproduct formation.** Batch 1 had complete conversion, selectivity near 0.395 and degradation warning near 0.292; batch 2, with a shorter hot residence, had selectivity near 0.675 and degradation warning near 0.091. This pattern supports overreaction, but crystallization and seed conditions also differed.
- **The low-loading coarse regime is seed-dominated.** Batches 7 and 10 combined a large seed-to-product ratio with coarse particles and very low seed-excluded recovery. Seed-derived dominance is plausible, but the experiment did not separately count seed crystals and newly nucleated crystals.

### Contradicted or substantially weakened
- **The original expectation that ordinary seeded slow cooling would simultaneously give good recovery and low fines was contradicted.** Batches 1 and 2 had useful recovery and high purity but essentially all particles were fines.
- **The hypothesis that additional aging alone would convert fines into coarse crystals was contradicted by batches 3 and 10.**
- **The tested staged-cooling strategy was contradicted by batch 11,** which still had about 0.982 fines.
- **The tested thermal-cycle strategies did not solve the tradeoff.** Batch 4 remained entirely fine, and batch 12 retained fines of 1.0 after cool/reheat processing.
- **The nominal low-nucleation character of S2 was not sufficient at high supersaturation.** It may still be favorable relative to other solvents, but it did not prevent fines in batches 1–4.

### Still untested
- Catalyst ranking: only C1 was used.
- S0 and S3 behavior and their hidden fixed residuals.
- Controlled seed-size or seed-number effects independent of seed mass.
- Direct solubility, supersaturation, nucleation-rate and growth-rate measurements.
- Continuous feed, antisolvent addition, fines classification, or optimized washing/resuspension.
- Whether S2 is truly superior to S1: batches 2 and 5 suggest it, but the comparison was unreplicated and slightly confounded.

## 2. One additional experiment
I would run a **single trajectory experiment based on batch 7**, with non-destructive particle measurements at three points:

1. Use 0.005 mol reagent, 0.08 L S2, C1, the batch-7 reaction history, and 0.05 g seed.
2. Hold at 290 K as in batch 7; measure particle size and fines.
3. Cool to 280 K for one long interval; measure again.
4. Reheat to 290–300 K and hold; measure a third time, then filter and perform the final assay.

This would distinguish several explanations:

- **Supersaturation-threshold secondary nucleation:** fines should remain low at 290 K, jump sharply after cooling to 280 K, and d50 should collapse.
- **Time-dependent attrition or seed fragmentation:** fines should rise during the initial 290 K hold, without requiring the deeper cooling threshold.
- **Reversible selective dissolution/Ostwald ripening:** reheating should reduce fines and increase d50, accompanied by some loss of crystal recovery.
- **Persistent nuclei or rapid renucleation:** fines should remain high after reheating, as implied—but not temporally resolved—by batch 12.
- **Pure number-weighting/seed-dominance effect:** the first reading should be dominated by coarse seed particles, followed by a large distribution change as even a modest amount of new product appears.

The value of this experiment is the within-batch particle trajectory; another final-only assay would not reveal when the fines appeared or whether reheating temporarily removed them.

## 3. Weakest use of evidence and least reliable prediction

### Observation used least effectively
I used the reaction-side observations in the loading series—especially **batch 6**—less effectively than I should have. Batch 6 had conversion around 0.916, unlike the near-complete conversion in batches 7–9. I described the crystallization transition mainly using nominal reagent concentration, although the actual relevant variable is target concentration before separation, approximately proportional to charge × conversion × target selectivity divided by volume. The qualitative loading conclusion remains plausible, but the threshold should not be assigned solely to nominal reagent loading without correcting for reaction performance.

The final-only thermal-cycle results, particularly batch 12, were also mechanistically incomplete: they prove that the final product remained fine, but not whether reheating ever dissolved fines before they persisted or regenerated.

### Least reliable held-out prediction
**Q12 is the least reliable prediction.** It combines several extrapolations: untested solvent S0, twice the charge of Q11, a catalyst-to-reagent ratio outside the most informative campaign conditions, a 385 K reaction history, and a very long staged descent through a nonlinear nucleation threshold. Its predicted high recovery and near-unity fines follow the campaign’s qualitative loading trend, but the numerical recovery and purity intervals depend strongly on unknown S0 solubility, occlusion and hidden residuals. Q02 is also weak because S3 was never tested, but Q12 compounds material, loading and reaction-history extrapolations in one recipe.
