# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

The strongest material prior concerned solvent S2: nominally it had the lowest relative solubility (0.70), lowest nucleation tendency (0.65), highest crystal-growth factor (1.30), and lowest impurity-occlusion factor (0.65). The experiments broadly supported S2 as a useful crystallization medium: S2 batches commonly produced final crystal purities around 0.98–1.00 and recovery around 0.37–0.40 when the thermal history was favorable. These observations are consistent with low terminal solubility promoting recovery and low occlusion promoting purity, although the experiments do not independently identify those two causal contributions.

S1 was less effective under the tested conditions. The unseeded, quenched S1 process in batch 5 gave recovery 0.245, purity 0.967, and fines fraction 1.00. This agrees qualitatively with its higher nominal solubility and lower growth factor than S2, but the solvent comparison was confounded by catalyst, seeding, and process history; it is not a clean solvent-only test. S0 and S3 were not adequately isolated in completed comparisons, so their realized crystallization behavior remains untested.

Catalyst C1 was used in most of the successful processes. At approximately 330–360 K it generally produced near-complete conversion, but final selectivity remained modest, roughly 0.39–0.48, with byproduct signals around 0.35–0.40. C2 and C3 appeared in batches with different downstream histories, so no reliable catalyst ranking can be inferred. The observations support C1 as operationally adequate, not necessarily intrinsically optimal.

### 2. Reaction–crystallization coupling

The reaction and crystallization objectives were related but not identical. Near-complete reactant conversion did not imply high selective reaction yield: substantial byproduct signal remained. Nevertheless, the recovered crystals could have purity above 0.97. Thus crystallization acted as a selective separation that rejected much of the reaction impurity from the solid phase.

A useful decomposition is

- reaction target amount before separation: approximately proportional to charged reactant × conversion × selectivity;
- recovered target amount: target before separation × crystallization recovery;
- reported crystal yield: recovered seed-excluded target / target present before separation.

Because the campaign objective used the last ratio, improving reaction selectivity would increase absolute product mass but need not directly raise the reported crystallization-stage recovery. This explains why modest reaction selectivity could coexist with a crystal recovery near 0.40 and very high crystal purity.

The high purity also shows that the byproduct signal was not simply incorporated in proportion to its liquid-phase abundance. A distribution or rejection coefficient below unity for impurity incorporation is a plausible interpretation, especially for S2 with its low nominal occlusion tendency, but that coefficient was not measured directly.

### 3. Supersaturation and population mechanism

The results are consistent with a standard competition between nucleation and growth. Define supersaturation as

S = C/C*(T),

where C is dissolved target concentration and C*(T) is its equilibrium solubility. Nucleation is often much more nonlinear in supersaturation than growth, schematically

J ≈ J0 exp[-B/(ln S)^2],

while crystal growth can be represented more smoothly as

G ≈ kg(S − 1)^g.

A rapid temperature drop can therefore create a short, intense nucleation burst: J becomes large, many particles form, and the available target is divided among many crystals. Slow staged cooling keeps supersaturation lower and allows existing crystals to consume target through growth before secondary nucleation accelerates.

In population-balance language,

∂n(L,t)/∂t + ∂[G(L,t)n(L,t)]/∂L = Bnuc − Dattr,

where n is the number distribution, Bnuc represents new nuclei, and Dattr includes loss or redistribution through dissolution, aggregation, or attrition. The campaign did not measure these terms separately, but the final number fraction below 20 µm strongly indicates that the thermal path changed the balance between Bnuc and growth.

### 4. Dominant process-history effect

The decisive variable was whether the process was rapidly quenched before controlled crystallization.

Batches 1–5 all included a quench or otherwise retained an unfavorable nucleation history. They finished with fines fractions near 1.00 despite changes in seed quantity, holding time, solvent, and reheating:

- Batch 1: S2, C1, 0.05 g seed, slow cool after quench; recovery 0.390 and purity 0.984, but fines 0.997.
- Batch 2: S2 with only 0.001 g seed and much longer holding; recovery 0.340, purity 0.974, fines 1.00.
- Batch 3: an attempted 0.000001 g seed failed to establish an effective seed population; after correction and long processing, recovery was 0.301 and fines 0.995.
- Batch 4: quench followed by crystallization, partial reheating, and recooling; recovery 0.378 and purity 1.00, but fines 1.00.
- Batch 5: unseeded S1 process after quench; recovery 0.245 and fines 1.00.

These results caused a revision of the initial hypothesis. Initially, lower seed loading plus long low-temperature holding was expected to produce larger particles. That expectation was rejected in the quenched regime: neither reducing seed nor extending an isothermal hold solved the fines problem. Batch 4 further showed that moderate reheating after a quench did not erase the previously established fine population. A plausible interpretation is that the quench crossed the metastable zone too quickly and created many nuclei; later growth or thermal cycling was insufficient to remove their number dominance.

Batch 6 removed the quench and instead seeded the hot reaction mixture with 0.01 g, followed by long staged cooling through 310, 295, 280, and 260 K. The final assay gave recovery 0.379, purity 1.00, fines 0.210, and CSD quality 0.806. This was the key mechanistic discontinuity: fines fell from approximately unity to about 0.21 without sacrificing purity or much recovery.

Batch 7 extended the no-quench staged path through 315, 300, 285, 270, and 250 K, followed by two low-agitation holds. It gave the highest observed compliant recovery, 0.396, with purity 0.981, fines 0.141, and CSD quality 0.836. The inference is that gradual supersaturation generation allowed seed-directed growth while suppressing burst nucleation.

The same qualitative outcome was reproduced:

- Batch 11, essentially a batch-7 replicate: recovery 0.385, purity 0.994, fines 0.148.
- Batch 12, with four terminal holds: recovery 0.387, purity 0.996, fines 0.156.

Thus the robust claim is not that one exact cooling stage is uniquely optimal, but that avoiding the quench and using seeded, staged cooling moves the process into a reproducibly compliant particle regime.

### 5. Seed, concentration, cooling, and holding effects

Seed was necessary at more than a merely formal quantity: the 0.000001 g charge in batch 3 failed the effective-seed-population condition. Above that threshold, however, the campaign did not establish a simple monotonic seed law.

In the successful no-quench regime:

- Batch 7 used 0.01 g seed and gave recovery 0.396 with fines 0.141.
- Batch 9 used 0.02 g seed and gave recovery 0.374 with fines 0.215.
- Batch 10 used 0.005 g seed but also changed solvent loading and cooling stages; recovery was 0.373 with fines 0.344.

These results are compatible with excess seeds increasing the number of small crystals and with insufficient seed surface permitting some secondary nucleation, but the comparisons are confounded and do not establish an optimum seed mass independently. The supported operational region is approximately 0.01 g for the tested 0.08 L S2 charge.

Reducing S2 volume from 0.08 L to 0.06 L in batch 8 increased concentration but did not improve recovery: recovery was 0.392, purity 0.981, and fines 0.283. The higher fines are consistent with stronger supersaturation and additional nucleation, while the small recovery difference from batch 7 is not compelling. Batch 10 at 0.07 L, with more cooling stages and longer holding, likewise gave lower observed recovery (0.373) and more fines (0.344). Therefore, simply concentrating the solution did not produce a favorable recovery/quality tradeoff.

Long terminal holding also showed diminishing returns. Batch 7 used two holds, batch 11 repeated that history, and batch 12 used four holds. Their recoveries were 0.396, 0.385, and 0.387, respectively. Extra holding did not measurably improve equilibrium recovery and may only add time and possible attrition or degradation exposure.

### 6. Quality–recovery tradeoff and uncertainty

A clear early tradeoff was observed: batch 1 had recovery 0.390 and excellent purity but failed catastrophically on fines. The process was therefore not usable despite a recovery close to that of batch 7. The no-quench staged strategy largely removed this tradeoff, retaining recovery around 0.38–0.40 while lowering fines to approximately 0.14–0.21.

Within the compliant group, the unresolved tradeoff is subtler. More concentrated or altered-seed processes remained below the fines limit but shifted fines upward and did not improve recovery. Conversely, additional holding did not increase recovery. The data suggest a practical recovery plateau near 0.39–0.40 for S2 at 250 K under the tested separation procedure, but equilibrium solubility was not measured, so this is an empirical plateau rather than a proven thermodynamic ceiling.

Final-assay noise for crystal recovery was stated as 0.01. Batch 7 exceeded batches 11 and 12 by only about 0.012 and 0.009, respectively. Those differences are comparable to the measurement noise and could also reflect process variability. Consequently, batch 7 is the highest observed compliant batch, but the evidence does not prove it has a reproducibly higher true recovery than batches 11–12. In contrast, the change in fines from roughly 1.0 in quenched batches to roughly 0.15 in staged no-quench batches is far larger than the fines uncertainty and is strong evidence of a real history effect.

Particle-size measurements and final assays sometimes differed numerically, as expected from their noise and sampling contracts, but they agreed on the qualitative classification: quenched batches were overwhelmingly fine, and the staged no-quench batches were comfortably below the 0.50 constraint.

### 7. Untested alternatives

Several mechanisms remain plausible but untested:

- Direct measurement of a metastable-zone boundary could permit a more efficient seed-addition temperature and shorter cooling schedule.
- Controlled antisolvent addition was not studied; it might improve recovery but could recreate burst nucleation.
- A carefully designed partial-dissolution cycle applied to an initially well-controlled, no-quench population might improve size distribution; batch 4 only tested reheating after an already damaging quench.
- Agitation below 100 rpm, variable agitation during nucleation and growth, or direct attrition measurements were unavailable, so mechanical breakage was not separated from primary or secondary nucleation.
- Solvent mixtures and systematic S0/S3 comparisons were not performed.
- Catalyst effects on impurity identity and subsequent crystal habit were not isolated.
- Washing or resuspension might improve purity further, but purity was already nonbinding and such steps could reduce recovery.

Overall, the most defensible mechanism is that S2 provides a favorable purity/recovery environment, while supersaturation history determines particle compliance. Reaction conversion was adequate but chemically nonselective; crystallization supplied the decisive purification. Avoiding the rapid quench and consuming supersaturation gradually on an effective seed population suppressed the otherwise dominant nucleation burst and produced the reproducible compliant regime represented by batches 6, 7, 11, and 12.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.9 | 0.7 | 1 |
| Q01 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q01 | crystal_size | 0.06 | 0.025 | 0.105 |
| Q01 | crystal_yield | 0.24 | 0.13 | 0.36 |
| Q02 | crystal_fines_fraction | 0.96 | 0.8 | 1 |
| Q02 | crystal_purity | 0.91 | 0.81 | 0.98 |
| Q02 | crystal_size | 0.047 | 0.018 | 0.09 |
| Q02 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q03 | crystal_fines_fraction | 0.91 | 0.68 | 1 |
| Q03 | crystal_purity | 0.89 | 0.78 | 0.97 |
| Q03 | crystal_size | 0.066 | 0.025 | 0.12 |
| Q03 | crystal_yield | 0.13 | 0.04 | 0.25 |
| Q04 | crystal_fines_fraction | 0.98 | 0.85 | 1 |
| Q04 | crystal_purity | 0.9 | 0.8 | 0.98 |
| Q04 | crystal_size | 0.045 | 0.017 | 0.083 |
| Q04 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q05 | crystal_fines_fraction | 0.97 | 0.81 | 1 |
| Q05 | crystal_purity | 0.9 | 0.8 | 0.98 |
| Q05 | crystal_size | 0.05 | 0.02 | 0.092 |
| Q05 | crystal_yield | 0.19 | 0.09 | 0.31 |
| Q06 | crystal_fines_fraction | 0.995 | 0.91 | 1 |
| Q06 | crystal_purity | 0.88 | 0.76 | 0.97 |
| Q06 | crystal_size | 0.034 | 0.012 | 0.068 |
| Q06 | crystal_yield | 0.2 | 0.09 | 0.32 |
| Q07 | crystal_fines_fraction | 0.96 | 0.78 | 1 |
| Q07 | crystal_purity | 0.9 | 0.8 | 0.98 |
| Q07 | crystal_size | 0.053 | 0.021 | 0.098 |
| Q07 | crystal_yield | 0.19 | 0.09 | 0.31 |
| Q08 | crystal_fines_fraction | 0.98 | 0.84 | 1 |
| Q08 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q08 | crystal_size | 0.045 | 0.017 | 0.087 |
| Q08 | crystal_yield | 0.13 | 0.04 | 0.25 |
| Q09 | crystal_fines_fraction | 0.995 | 0.91 | 1 |
| Q09 | crystal_purity | 0.92 | 0.8 | 0.99 |
| Q09 | crystal_size | 0.036 | 0.012 | 0.07 |
| Q09 | crystal_yield | 0.02 | 0 | 0.07 |
| Q10 | crystal_fines_fraction | 0.98 | 0.82 | 1 |
| Q10 | crystal_purity | 0.91 | 0.79 | 0.98 |
| Q10 | crystal_size | 0.045 | 0.016 | 0.085 |
| Q10 | crystal_yield | 0.07 | 0.01 | 0.16 |
| Q11 | crystal_fines_fraction | 0.98 | 0.83 | 1 |
| Q11 | crystal_purity | 0.9 | 0.79 | 0.98 |
| Q11 | crystal_size | 0.048 | 0.018 | 0.09 |
| Q11 | crystal_yield | 0.19 | 0.09 | 0.31 |
| Q12 | crystal_fines_fraction | 0.98 | 0.82 | 1 |
| Q12 | crystal_purity | 0.86 | 0.73 | 0.96 |
| Q12 | crystal_size | 0.052 | 0.019 | 0.1 |
| Q12 | crystal_yield | 0.32 | 0.19 | 0.45 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain an effective seed charge, so particles are expected. However, each also quenches and then moves rapidly to 300 K before seeding. In the campaign, this pre-seed history was strongly associated with a persistent fine-particle population that long subsequent cooling or reheating did not repair; therefore all quality-feasible calls are false because predicted fines remain above 0.50. Q01 versus Q02 favors S1 over S3 in recovery, purity, and particle growth because S1 has lower nominal solubility, nucleation, and occlusion. Q03 versus Q04 predicts that the larger seed charge accelerates recovery but creates a more number-dominant fine population. Q05 versus Q06 assigns similar terminal recovery but substantially worse size and fines to the initial cooling shock in Q06. Q07 versus Q08 predicts that the extra low-temperature hold preserves recovery better than the partial-dissolution/reprecipitation cycle, which previously failed to erase an established fine population. Q09 versus Q10 predicts low recovery in both, with the two-hour hold allowing additional growth and recovery. Q11 versus Q12 predicts much higher recovery at doubled reagent concentration, accompanied by somewhat lower purity and no reliable fines benefit. Intervals are epistemic, not assay-noise intervals; they are broad because S0 and S3 were not cleanly characterized, the query scale and 385 K reaction differ from the campaign, and the effects of very long staged cooling are extrapolations.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **A no-quench, seeded, staged S2 cooling history reproducibly produced acceptable particles.** Batch 6 gave fines 0.210, purity 1.000, and recovery 0.379. Batch 7 improved this to fines 0.141, purity 0.981, and recovery 0.396. Near-replicates 11 and 12 remained compliant, with fines 0.148 and 0.156 and recoveries 0.385 and 0.387. The direct observation is the repeatable association; suppression of a nucleation burst is the mechanistic interpretation.
- **Rapidly quenched histories were associated with excessive fines.** Batches 1–5 all finished with fines near 1.00 despite changes in seed loading, holding time, solvent, and reheating. This contrast is much larger than measurement uncertainty.
- **Crystallization supplied substantial purification.** Near-complete conversion coexisted with modest reaction selectivity—roughly 0.39–0.48 and appreciable byproduct signal—yet many S2 crystals had purity above 0.97. Directly observed metrics support phase rejection of impurity; a low impurity-incorporation coefficient is an interpretation rather than a measured constant.
- **S2 was operationally effective.** It repeatedly delivered high purity and recovery around 0.37–0.40 under favorable histories. This agrees with its nominal low solubility, high growth, and low occlusion properties, although the individual material-property contributions were not independently identified.

### Contradicted or substantially weakened

- **Lower seed loading plus long holding alone would eliminate fines.** Batch 2 used much less seed than batch 1 and much longer holding but retained fines of 1.00. Batch 3 also remained near unit fines after a corrected low-seed treatment and prolonged processing. The original seed-dose hypothesis was therefore contradicted within the quenched regime.
- **Post-nucleation reheating would readily repair the distribution.** Batch 4 used a reheating/recooling cycle but still had fines of 1.00. This contradicts a simple repair mechanism, though it does not rule out a better-designed partial-dissolution cycle.
- **More concentration or more terminal holding would necessarily raise recovery.** Batch 8 used less solvent but gave recovery 0.392 rather than exceeding batch 7; batch 10 gave only 0.373. Four terminal holds in batch 12 did not improve recovery over the two-hold processes. These observations weaken simple monotonic relationships.

### Still untested or unresolved

- The **causal quench effect** was not tested with a single-factor matched comparison. The observed contrast between batches 1–5 and 6–7 also included seed dose, temperature path, and other details.
- A quantitative **seed optimum** remains unresolved because batches 7, 9, and 10 changed more than seed mass.
- **Catalyst ranking** is untested: C2 and C3 were confounded with downstream changes.
- S0 and S3 were not cleanly characterized, and the single S1 result in batch 5 was confounded by its unseeded, quenched history.
- Metastable-zone limits, nucleation and growth rates, impurity distribution coefficients, attrition, solvent mixtures, antisolvent addition, and washing/recrystallization tradeoffs were not measured directly.
- The apparent recovery plateau near 0.39–0.40 is empirical, not a demonstrated thermodynamic ceiling. Batch 7’s lead over batches 11–12 is comparable to the stated recovery noise.

## 2. One additional experiment

I would run a **matched quench challenge against batch 7**. I would use the same S2 volume, reagent and C1 charges, reaction conditions, 0.01 g seed, staged cooling endpoints, low agitation, holds, filtration, and final assay. The only deliberate change would be to insert the rapid quench after reaction. I would also make a non-destructive particle-size measurement immediately after the quench and before seed addition, then proceed with the batch-7 cooling program.

This would distinguish three explanations:

1. **Quench-induced primary nucleation:** particles or a strongly fine distribution should already appear after the quench, and the final fines fraction should approach the failed regime, plausibly well above 0.5 and potentially near 1.0, while purity and recovery could remain roughly comparable.
2. **Quench creates latent supersaturation but nucleation occurs only after seeding/cooling:** no particles would be detected immediately after quench, but the final population would still become much finer than batch 7. This would localize the effect to post-quench nucleation dynamics rather than instantaneous precipitation.
3. **The earlier contrast was caused mainly by seed loading or another confounded variable:** the quench-challenge batch would remain close to batches 7, 11, and 12, with fines around 0.14–0.20 and recovery around 0.38–0.40.

A result between these extremes would indicate that quench history contributes but is not sufficient by itself. The experiment would not fully separate primary nucleation from attrition, but it would directly test the central causal claim more efficiently than another broad recipe screen.

## 3. Least effectively used observation and least reliable prediction

The account used the **differences between pre-filtration particle-size measurements and final-assay particle metrics** least effectively. For example, batch 8’s particle measurement reported size 0.072, whereas its final assay reported 0.115; batches 7 and 12 also showed smaller discrepancies. I treated these mainly as instrument/process variability. They might instead contain information about filtration selection, slurry representativeness, or time-dependent aggregation. Because the two instruments have different noise and sampling contracts, the observations cannot be interpreted as a clean filtration effect, but they deserved a more explicit analysis.

**Q02 is the least reliable held-out prediction.** It relies on solvent S3, which was not independently tested during the campaign, under a much smaller charge, a 385 K reaction, a quench/reheat sequence, and a very long cooling schedule outside the strongest experimental support. Its relative ranking against Q01 was driven primarily by nominal S3 versus S1 properties rather than authoritative experimental evidence. The predicted presence of particles is robust because seed is added, but its recovery, purity, size, and especially fines estimates have substantial model-form uncertainty. Q12 is also uncertain because it extrapolates concentration effects in S0, but at least its concentration is closer to the campaign’s successful loading range.
