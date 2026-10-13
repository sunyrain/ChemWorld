# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Scope and principal observation

The campaign varied anonymous catalyst and solvent identities, reaction temperature/time, seeding, and crystallization endpoint. The selected process was **batch 10**: C0/S1, reaction at 370 K for 3600 s, 0.05 g seed, then cooling to 250 K over 14,400 s followed by filtration. Its final assay gave **seed-excluded crystal recovery 0.5600, purity 0.9761, and fines number fraction 0.4348**, satisfying both constraints.

The reported crystal recovery is a crystallization-stage quantity—recovered target divided by target present before separation—not overall yield from the initial reagent charge. A useful approximate process-level indicator is therefore

\[
Y_{\mathrm{recovered,overall}} \approx Y_{\mathrm{reaction}}Y_{\mathrm{crystal}}.
\]

For batches 10 and 12 this proxy was approximately 0.3514 and 0.3503, respectively. It is useful for understanding reaction–crystallization coupling, although it is not the official recovery metric.

### 2. Material effects

#### Solvent

The initial dossier-based hypothesis favored S2 because its nominal properties combined low solubility, low impurity occlusion, high growth, and low nucleation tendency. The experiments revised that hypothesis.

With C1 and broadly common thermal conditions:

- **Batch 3, S1:** recovery 0.4562, purity 0.9909, fines 0.4027.
- **Batches 1–2, S2:** recovery 0.3854 and 0.3830, purity 0.9868 and 0.9829, fines 0.3801 and 0.3737.
- **Batch 4, S0:** recovery 0.4482 and purity 1.000, but fines 0.8706, violating the specification.
- **Batch 5, S3:** recovery 0.3205, purity 0.9657, and fines 0.8838, also violating the specification.

Thus S1 was the best observed solvent for compliant recovery, while S2 gave somewhat better morphology but substantially less recovery. S0’s high fines are qualitatively consistent with its nominal high nucleation tendency. S3’s very high fines were not anticipated from the nominal dossier and may reflect the fixed world-specific solvent residual, a solvent–reaction interaction, or both.

Solvent also changed upstream chemistry. In the C1 solvent screen, final reaction yield/selectivity varied from roughly 0.49/0.50 with S2 to 0.59–0.60/0.59–0.61 with S1 or S0. Consequently, solvent effects cannot be assigned purely to solubility or nucleation: solvent altered the impurity and target concentrations entering crystallization as well as the crystallization kinetics themselves.

#### Catalyst

At S1, 370 K for 3600 s, and a 280 K crystallization endpoint:

- **Batch 6, C0:** recovery 0.5081, purity 0.9982, fines 0.4048.
- **Batch 3, C1:** recovery 0.4562, purity 0.9909, fines 0.4027.
- **Batch 7, C2:** recovery 0.4601, purity 0.9774, fines 0.4531.
- **Batch 8, C3:** recovery 0.4858, purity 0.9796, fines 0.4234.

C0 therefore produced the highest observed compliant recovery despite not having the highest nominal reference-panel activity. Its higher upstream yield/selectivity likely increased the target-to-impurity ratio and improved the crystallization feed. Because each catalyst was tested once and only in one principal solvent regime, catalyst–solvent interactions and run-to-run variation remain unresolved.

### 3. Reaction–crystallization coupling

A simple conceptual sequence is

\[
\text{reactant}\xrightarrow{k_1}\text{target},\qquad
\text{reactant or target}\xrightarrow{k_2}\text{byproducts/degradation},
\]

followed by target partitioning between crystals and mother liquor. Reaction conditions determine target concentration, impurity concentration, and possibly impurity identities. Those variables then affect supersaturation, competitive adsorption, occlusion, and nucleation.

Supersaturation may be represented as

\[
\sigma=\frac{C-C^*(T,\text{solvent})}{C^*(T,\text{solvent})},
\]

where \(C^*\) is the temperature- and solvent-dependent target solubility. Crystal growth commonly increases as \(G\propto\sigma^g\), whereas primary nucleation can rise much more steeply, schematically

\[
J\propto\exp\!\left[-\frac{A}{(\ln S)^2}\right],\qquad S=C/C^*.
\]

These relationships explain why deeper cooling can raise recovery by lowering solubility but can also create more nuclei and fines. They also explain why upstream selectivity matters: impurities may change effective solubility, inhibit growth, or become occluded.

Batch 11 illustrates the coupling, although not cleanly. Its 350 K/7200 s reaction followed by cooling to 270 K gave selectivity 0.4996, reaction yield 0.4802, and crystal recovery only 0.3921. This was markedly worse than the C0/S1 370 K condition. However, temperature, reaction duration, and crystallization endpoint all differed, so the result does not establish that 350 K itself is harmful.

### 4. Process-history dependence

With C0/S1 and the same 370 K/3600 s reaction and 14,400 s cooling duration, progressively colder endpoints increased observed recovery:

- **Batch 6, 280 K:** recovery 0.5081; fines 0.4048.
- **Batch 9, 260 K:** recovery 0.5467; fines 0.4351.
- **Batch 10, 250 K:** recovery 0.5600; fines 0.4348.

This is consistent with lower equilibrium solubility at colder temperature. The accompanying increase in fines from about 0.405 to about 0.435 suggests increasing nucleation or reduced growth time per particle, but all three batches remained compliant. Since 250 K was the legal lower bound, the location of an unconstrained recovery optimum was not determined.

History mattered beyond endpoint temperature. Batch 1 was cooled to 280 K and then subjected to a 7200 s nominal wait, during which it warmed to about 297.6 K before filtration. Batch 2 was unseeded and filtered after the 280 K cooling operation. Their recoveries were almost identical, 0.3854 and 0.3830, but batch 2 had a larger normalized size. This comparison cannot isolate a seed effect because seeding was confounded with the warming/hold history. The warm excursion may have promoted partial dissolution or Ostwald ripening, while the absence of a controlled isothermal hold prevents a firm conclusion.

### 5. Revision of the working mechanism

The original expectation was that S2 plus seeding and slow cooling would maximize compliant recovery. The evidence forced two revisions:

1. **S2 retained a morphology advantage but not a recovery advantage.** S1 became the preferred solvent after batch 3.
2. **C0 replaced the initially favored C1.** Under S1, C0 gave the largest observed recovery and favorable upstream selectivity.

Subsequent endpoint experiments supported deeper cooling as the clearest recovery lever. Reaction-temperature optimization remained unresolved: **batch 12**, using 380 K rather than 370 K and the same 250 K endpoint, gave recovery 0.5595, essentially tied with batch 10’s 0.5600.

### 6. Quality–recovery tradeoff and uncertainty

Batches 10 and 12 expose the remaining tradeoff:

- **Batch 10:** recovery 0.5600, purity 0.9761, fines 0.4348, normalized size 0.0743.
- **Batch 12:** recovery 0.5595, purity 0.9926, fines 0.4658, normalized size 0.0993.

Thus the hotter reaction produced nearly the same recovery, with numerically higher purity and larger particles but also more fines. The normalized sizes correspond approximately to number-weighted d50 values of 18.6 and 24.8 µm under the published normalization. The recovery difference of 0.0005 is far below the final-assay recovery noise scale, so there is no evidence that one temperature is intrinsically superior for recovery. The purity and fines differences are suggestive but based on single batches and remain uncertain relative to measurement variability and process noise.

Batch 10 was retained because it had the highest observed recovery and met both hard specifications, not because the tiny advantage over batch 12 was mechanistically resolved. Batch 12 could be preferable under a stronger purity or particle-size objective, but its higher fines fraction reduced its margin to the 0.50 limit.

Other comparisons are also single-run observations. The solvent and catalyst differences are often much larger than the stated analytical noise and are therefore credible screening signals, but their exact magnitudes should not be treated as replicated effect sizes.

### 7. Untested alternatives

The campaign did not independently determine:

- the effect of seed mass or seed-size distribution;
- cooling rate versus final temperature, because the endpoint series used a common total cooling duration;
- a controlled low-temperature aging time without reheating;
- whether a dissolution–recrystallization or temperature-cycling step could reduce fines while retaining recovery;
- reaction temperature and duration in a factorial design;
- catalyst–solvent interactions outside the principal S1 screen;
- agitation effects on secondary nucleation and attrition;
- concentration or solvent-volume effects;
- repeatability of the near-tied batches 10 and 12.

Accordingly, the supported mechanism is empirical and conditional: C0/S1 generated the best observed reaction feed; deep, slow cooling raised seed-excluded recovery; and the gain was accompanied by a modest morphology penalty. The precise kinetic origin—lower solubility, altered nucleation, impurity-mediated growth, or a combination—was not directly measured.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.45 |
| Q01 | crystal_purity | 0.975 | 0.94 | 0.995 |
| Q01 | crystal_size | 0.18 | 0.1 | 0.28 |
| Q01 | crystal_yield | 0.4 | 0.28 | 0.52 |
| Q02 | crystal_fines_fraction | 0.68 | 0.51 | 0.84 |
| Q02 | crystal_purity | 0.94 | 0.87 | 0.98 |
| Q02 | crystal_size | 0.085 | 0.035 | 0.16 |
| Q02 | crystal_yield | 0.29 | 0.17 | 0.43 |
| Q03 | crystal_fines_fraction | 0.7 | 0.52 | 0.86 |
| Q03 | crystal_purity | 0.955 | 0.89 | 0.99 |
| Q03 | crystal_size | 0.075 | 0.03 | 0.15 |
| Q03 | crystal_yield | 0.3 | 0.17 | 0.43 |
| Q04 | crystal_fines_fraction | 0.45 | 0.3 | 0.61 |
| Q04 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q04 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q04 | crystal_yield | 0.35 | 0.22 | 0.48 |
| Q05 | crystal_fines_fraction | 0.43 | 0.29 | 0.59 |
| Q05 | crystal_purity | 0.968 | 0.915 | 0.995 |
| Q05 | crystal_size | 0.16 | 0.08 | 0.25 |
| Q05 | crystal_yield | 0.37 | 0.23 | 0.5 |
| Q06 | crystal_fines_fraction | 0.61 | 0.43 | 0.78 |
| Q06 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q06 | crystal_size | 0.09 | 0.035 | 0.18 |
| Q06 | crystal_yield | 0.38 | 0.24 | 0.52 |
| Q07 | crystal_fines_fraction | 0.4 | 0.26 | 0.56 |
| Q07 | crystal_purity | 0.97 | 0.92 | 0.996 |
| Q07 | crystal_size | 0.18 | 0.09 | 0.28 |
| Q07 | crystal_yield | 0.38 | 0.24 | 0.51 |
| Q08 | crystal_fines_fraction | 0.3 | 0.17 | 0.47 |
| Q08 | crystal_purity | 0.982 | 0.94 | 0.999 |
| Q08 | crystal_size | 0.23 | 0.12 | 0.36 |
| Q08 | crystal_yield | 0.31 | 0.18 | 0.44 |
| Q09 | crystal_fines_fraction | 0.9 | 0.75 | 0.98 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.05 | 0.02 | 0.09 |
| Q09 | crystal_yield | 0.025 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.72 | 0.53 | 0.87 |
| Q10 | crystal_purity | 0.982 | 0.93 | 1 |
| Q10 | crystal_size | 0.085 | 0.035 | 0.16 |
| Q10 | crystal_yield | 0.12 | 0.04 | 0.22 |
| Q11 | crystal_fines_fraction | 0.43 | 0.28 | 0.59 |
| Q11 | crystal_purity | 0.968 | 0.91 | 0.996 |
| Q11 | crystal_size | 0.16 | 0.075 | 0.26 |
| Q11 | crystal_yield | 0.38 | 0.24 | 0.51 |
| Q12 | crystal_fines_fraction | 0.57 | 0.4 | 0.74 |
| Q12 | crystal_purity | 0.94 | 0.86 | 0.985 |
| Q12 | crystal_size | 0.12 | 0.055 | 0.21 |
| Q12 | crystal_yield | 0.53 | 0.39 | 0.65 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even when little seed-excluded product grows. Q01–Q02 apply the observed solvent ranking: S1 should give higher recovery, growth and purity with fewer fines than S3. Q03–Q04 treat greater seeding as suppressing uncontrolled S0 nucleation, although the effect was not isolated experimentally. Q05–Q06 contrast gradual cooling with an initial temperature crash: similar eventual recovery is plausible, but the crash should leave more persistent fines despite the long hold. Q07–Q08 assign the 315 K cycle partial dissolution/ripening of fines, improving size and fines at some recovery cost. Q09–Q10 predict that a 292 K hold permits more growth than immediate filtration but remains insufficient for acceptable S0 morphology. Q11–Q12 assign doubled concentration higher recovery but greater supersaturation, occlusion and fines, creating a recovery–quality tradeoff. Intervals are epistemic 80% ranges for the noise-free state, not assay-noise intervals; they are deliberately broad because these recipes extrapolate to lower concentration, much longer staged histories, quench/reheat operations and seed-load effects not independently resolved in the campaign.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **S1 was the best compliant solvent observed in the C1 screen.** Batch 3 gave recovery 0.456, purity 0.991 and fines 0.403. S2 gave only about 0.383–0.385 recovery in batches 1–2, while S0 and S3 produced excessive fines in batches 4–5. This ranking is directly observed, but only for the tested reaction and cooling regime.
- **C0 outperformed the other catalysts under S1 conditions.** Batch 6 had recovery 0.508 versus 0.456, 0.460 and 0.486 for C1, C2 and C3 in batches 3, 7 and 8. All were single runs, so this supports screening selection rather than a precise effect size.
- **Deeper cooling increased recovery in the tested C0/S1 series.** Recovery rose from 0.508 at 280 K in batch 6 to 0.547 at 260 K in batch 9 and 0.560 at 250 K in batch 10. Fines increased modestly but remained below 0.50.
- **Batch 10 and batch 12 were practically tied in recovery.** Their values, 0.5600 and 0.5595, differ by much less than the assay noise scale. Batch 12 was numerically purer and larger but had more fines.

### Supported as interpretations, but not directly demonstrated

- I interpreted the endpoint trend as reduced target solubility at lower temperature. Solubility itself was not measured; longer effective growth, kinetic trapping or impurity effects could also contribute.
- I attributed part of C0’s crystallization advantage to its better reaction feed. The upstream yield/selectivity observations support coupling, but no experiment independently varied feed composition while holding crystallization conditions fixed.
- I interpreted the batch-10/batch-12 differences as a possible purity/size-versus-fines tradeoff. With one run at each reaction temperature, this remains suggestive rather than established.

### Contradicted or revised

- The initial dossier-based expectation that **S2 would maximize recovery** was contradicted by batches 1–3: S2 retained acceptable morphology but recovered substantially less target than S1.
- The initial preference for **C1 as a strong catalyst choice** was revised after the catalyst screen, where C0 produced the highest recovery under S1 conditions.
- Batch 11 contradicted any simple expectation that a longer, milder 350 K reaction would reduce degradation and improve the process. It was worse, but temperature and duration were changed together, so the cause is unresolved.

### Still untested

- A causal seed-mass effect: batches 1 and 2 confounded seeding with a post-cooling warm excursion.
- Cooling-rate effects independent of endpoint and total time.
- Controlled low-temperature aging, thermal cycling and deliberate ripening.
- Concentration effects, including whether higher supersaturation increases recovery at an unacceptable fines cost.
- Catalyst–solvent interactions, agitation effects and repeatability of the best conditions.
- The long, staged cooling, quench/reheat and concentration regimes appearing in the held-out recipes; none closely matched the campaign histories.

## 2. One additional experiment

I would run the batch-10 chemistry and reaction conditions through its normal 250 K crystallization, then add a controlled thermal cycle:

1. C0/S1 reaction at 370 K for 3600 s and the same seed loading as batch 10.
2. Cool to 250 K over 14,400 s.
3. Measure particle size in situ.
4. Reheat to 315 K for 3600 s and measure again.
5. Recool to 250 K for 3600 s, measure again, then filter and perform the final assay.

This uses batch 10 as an existing matched reference and distinguishes three explanations:

- **Selective dissolution/Ostwald ripening:** reheating would reduce fines and raise d50; after recooling, recovery would mostly return while the larger size and lower fines persisted.
- **Crystal reset followed by secondary nucleation:** reheating would dissolve much of the solid population, and rapid recooling would produce smaller particles and more fines, possibly with incomplete recovery.
- **Approximately path-independent equilibrium:** after returning to 250 K, recovery and morphology would approach batch 10 regardless of the intermediate excursion.

The intermediate non-destructive measurements are important: a final assay alone could not distinguish transient dissolution from later re-nucleation.

## 3. Weakest use of evidence and least reliable prediction

The account used the **pre-filtration particle-size measurements** least effectively. They were collected in every batch, but the interpretation relied mainly on final-assay morphology. More systematic comparison of the direct d50/fines readings with the final assay could have identified measurement disagreement and better separated growth, attrition and filtration effects. Batch 1’s unintended warming was also underexploited, although it could not isolate aging because seeding differed from batch 2.

**Q08 is the least reliable held-out prediction.** It adds a 315 K reheating step after an extremely long staged crystallization and then provides only a short recooling period. No campaign batch tested post-crystallization reheating. The prediction assumed selective dissolution and ripening would dominate, but the same operation could instead dissolve most product and cause rapid secondary nucleation on recooling. Consequently, even the directions of the size, fines and recovery changes are less secure than for the solvent or endpoint comparisons. Q12 is the next-largest uncertainty because the doubled concentration extrapolates beyond the campaign and could alter both reaction composition and nucleation nonlinearly.
