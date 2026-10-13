# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome
The sealed recommendation is **batch 10**. It used 0.040 mol reagent, 0.005 mol catalyst C1, and 0.035 L solvent S2; reaction at 360 K for 900 s with 600 rpm stirring; 0.0002 g seed; direct cooling to 250 K over 14,400 s; two 14,400 s cold holds at 100 rpm; filtration and final assay. Its observed crystal recovery was **0.6762**, purity **0.9874**, and number fraction below 20 µm **0.1453**. Batch 12 repeated this process family and remained compliant: recovery 0.6701, purity 1.000, and fines 0.1359.

### Material effects
The initial material dossier suggested that C1 had relatively high reaction activity, while S2 combined low relative solubility and nucleation tendency with high crystal-growth tendency and low impurity occlusion. The experiments were consistent with S2 supporting high purity and useful crystal recovery. However, nearly all optimization batches used C1/S2, so their superiority over C0/C2/C3 or S0/S1/S3 was not experimentally isolated. The material explanation therefore remains a dossier-supported interpretation, not a comparative experimental ranking.

C1/S2 reaction performance was generally high in conversion but only moderate in selectivity. For example, batch 10 gave conversion 0.9858 and selectivity 0.6954, while batch 12 gave conversion 1.000 and selectivity 0.6919. Despite this byproduct formation, crystal purity stayed near unity. This suggests preferential incorporation of target material and/or rejection of impurities by the S2 crystal phase. It does not establish the molecular identity of the impurity or the microscopic rejection mechanism.

### Reaction–crystallization coupling
A useful approximate decomposition is

`target before separation ≈ initial reagent × conversion × selectivity`,

followed by

`crystal recovery R_c = seed-excluded recovered target / target present before separation`.

Thus the reported crystal recovery is a crystallization-stage fraction, not overall yield from the original reagent. Overall recovered target would scale approximately as `conversion × selectivity × R_c`. High crystallization recovery cannot compensate fully for poor reaction selectivity, although selectivity does not directly enter the stated recovery denominator.

Reaction history also determines the impurity inventory presented to crystallization. Longer hot exposure produced variable byproduct and degradation signals. Batch 1, heated for 1,800 s, showed byproduct signal 0.227 and degradation warning 0.099; the 900 s processes generally retained near-complete conversion while limiting unnecessary hot residence. Because reaction time was changed together with crystallization history in early batches, its independent effect was not precisely estimated.

### Supersaturation, recovery, and fines
A conventional qualitative description is

`S = C/C*(T)`

where `C` is target concentration and `C*(T)` is its equilibrium solubility. Cooling and reducing solvent volume increase supersaturation. A simplified equilibrium recovery relationship is

`R_c ≈ 1 − C*(T_f)V/M_target,pre`,

subject to kinetic trapping, mother-liquor retention, and finite residence time. This explains why cooling from 270 K to 250 K and reducing solvent volume initially improved recovery.

Nucleation is expected to respond much more sharply than growth to supersaturation, often represented qualitatively by

`J ∝ exp[−B/(ln S)^2]`,

whereas crystal growth varies more smoothly with supersaturation. Consequently, a modest concentration increase can cross from growth-dominated behavior into a nucleation burst, producing many fines.

The experiments showed exactly such a constraint-limited loading boundary:

- At 0.080 L S2, batches 3–5 gave recoveries 0.6369–0.6520 with purity 0.9829–1.000 and fines about 0.268–0.289.
- Reducing S2 to 0.040 L in batch 6 raised recovery to 0.6718 while retaining purity 1.000 and fines 0.3150.
- At 0.035 L, batch 10 gave recovery 0.6762 and fines 0.1453; batch 12 replicated compliance with recovery 0.6701 and fines 0.1359.
- At 0.0325 L, batch 11 was also compliant, with recovery 0.6680, purity 1.000, and fines 0.0341.
- At 0.030 L, batches 8 and 9 reached recoveries 0.6840 and 0.6767 but had fines 0.9870 and 1.000, respectively.
- At 0.020 L, batch 7 likewise produced fines 0.9869 and lower recovery, 0.5670.

The non-monotonic recovery at extreme concentration indicates that simple equilibrium solubility is insufficient. Excessive nucleation, kinetic trapping, poor growth, or altered slurry/filter behavior plausibly reduced effective recovery at 0.020 L. These alternatives were not separately measured.

### Seed and process-history effects
Seed dose and thermal history mattered strongly. Batch 1 used 0.05 g seed after a quench and produced essentially all fines: final fines 0.9972, despite purity 0.9909 and recovery 0.5641. In contrast, batches using 0.001–0.0002 g seed with slow direct cooling generally gave fines below 0.32 at moderate loading. Batch 5 showed that no added seed could also work at 0.080 L, giving recovery 0.6479 and fines 0.2842.

This supports the interpretation that the large seed charge supplied too many particle-number sites, but the comparison is confounded: batch 1 also used a quench, faster cooling, a higher final temperature, and longer reaction time. Therefore, the direction is convincing for the combined process history, while the isolated seed-dose effect is not quantified.

Process history could not rescue an over-concentrated 0.030 L slurry. Batch 8 used cooling to 250 K, partial reheating to 290 K, recooling, and holding; recovery was 0.6840, but fines remained 0.9870. Batch 9 used four slow cooling stages through 330, 300, 275, and 250 K; recovery was 0.6767, but fines were 1.000. These observations argue that the loading-induced nucleation regime was stronger than the tested ripening or staged-cooling interventions. Untested alternatives include a much longer near-saturation growth stage, different agitation, antisolvent scheduling, or a different solvent, but no claim can be made for them.

### Revisions during the campaign
The initial view was that C1/S2, seeding, and slow cooling would be favorable. Batch 1 forced a revision: a nominally growth-favoring solvent did not prevent fines when combined with a large seed charge and abrupt history. Batches 2–5 then established that very low seed, slower cooling, and a colder endpoint restored compliance.

The next working hypothesis was that less solvent would monotonically improve recovery. Batch 6 supported it, but batch 7 rejected monotonic extrapolation by revealing a high-fines, lower-recovery regime at 0.020 L. Batches 8 and 9 showed that thermal cycling and slower staged cooling did not overcome that regime at 0.030 L. The final revision was therefore to treat solvent loading as a sharp quality boundary and operate slightly above it. Batches 10–12 located a compliant region around 0.0325–0.035 L, with 0.035 L selected because batch 10 had the highest observed compliant recovery and batch 12 confirmed process-family compliance.

### Uncertainty and unresolved tradeoff
The final-assay noise model assigns standard deviations of approximately 0.01 to crystal recovery and purity and 0.018 to fines, in addition to process variability. The recovery difference between batches 10 and 12 is therefore not strong evidence of a true difference. Likewise, the small recovery differences among compliant batches 6, 10, 11, and 12 should not be overinterpreted.

The principal unresolved tradeoff is clear: the highest measured recovery was batch 8 at 0.6840, but it violated the fines limit severely. The best compliant results sacrificed only a small amount of measured recovery while moving far inside the fines constraint. Purity was not the active limitation in this region. The remaining uncertainty is whether a narrow condition between 0.030 and 0.0325 L, or an untested history at high loading, could retain the approximately 0.684 recovery while suppressing fines. The completed campaign did not demonstrate such a process.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.92 | 0.78 | 1 |
| Q01 | crystal_purity | 0.92 | 0.84 | 0.98 |
| Q01 | crystal_size | 0.032 | 0.015 | 0.06 |
| Q01 | crystal_yield | 0.18 | 0.07 | 0.31 |
| Q02 | crystal_fines_fraction | 0.76 | 0.56 | 0.92 |
| Q02 | crystal_purity | 0.96 | 0.9 | 1 |
| Q02 | crystal_size | 0.047 | 0.022 | 0.082 |
| Q02 | crystal_yield | 0.3 | 0.16 | 0.44 |
| Q03 | crystal_fines_fraction | 0.4 | 0.22 | 0.6 |
| Q03 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q03 | crystal_size | 0.082 | 0.04 | 0.135 |
| Q03 | crystal_yield | 0.1 | 0.02 | 0.22 |
| Q04 | crystal_fines_fraction | 0.97 | 0.89 | 1 |
| Q04 | crystal_purity | 0.91 | 0.81 | 0.98 |
| Q04 | crystal_size | 0.024 | 0.01 | 0.048 |
| Q04 | crystal_yield | 0.11 | 0.03 | 0.24 |
| Q05 | crystal_fines_fraction | 0.91 | 0.77 | 1 |
| Q05 | crystal_purity | 0.91 | 0.81 | 0.98 |
| Q05 | crystal_size | 0.031 | 0.014 | 0.06 |
| Q05 | crystal_yield | 0.13 | 0.04 | 0.26 |
| Q06 | crystal_fines_fraction | 0.99 | 0.94 | 1 |
| Q06 | crystal_purity | 0.89 | 0.78 | 0.97 |
| Q06 | crystal_size | 0.021 | 0.008 | 0.044 |
| Q06 | crystal_yield | 0.14 | 0.05 | 0.28 |
| Q07 | crystal_fines_fraction | 0.88 | 0.71 | 0.98 |
| Q07 | crystal_purity | 0.91 | 0.82 | 0.98 |
| Q07 | crystal_size | 0.034 | 0.016 | 0.064 |
| Q07 | crystal_yield | 0.14 | 0.05 | 0.27 |
| Q08 | crystal_fines_fraction | 0.96 | 0.86 | 1 |
| Q08 | crystal_purity | 0.93 | 0.84 | 0.99 |
| Q08 | crystal_size | 0.026 | 0.01 | 0.054 |
| Q08 | crystal_yield | 0.1 | 0.02 | 0.23 |
| Q09 | crystal_fines_fraction | 0.995 | 0.97 | 1 |
| Q09 | crystal_purity | 0.97 | 0.9 | 1 |
| Q09 | crystal_size | 0.015 | 0.005 | 0.032 |
| Q09 | crystal_yield | 0.008 | 0 | 0.03 |
| Q10 | crystal_fines_fraction | 0.98 | 0.91 | 1 |
| Q10 | crystal_purity | 0.95 | 0.87 | 1 |
| Q10 | crystal_size | 0.022 | 0.008 | 0.045 |
| Q10 | crystal_yield | 0.045 | 0.01 | 0.1 |
| Q11 | crystal_fines_fraction | 0.95 | 0.84 | 1 |
| Q11 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q11 | crystal_size | 0.026 | 0.011 | 0.052 |
| Q11 | crystal_yield | 0.13 | 0.04 | 0.26 |
| Q12 | crystal_fines_fraction | 0.98 | 0.91 | 1 |
| Q12 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q12 | crystal_size | 0.039 | 0.017 | 0.075 |
| Q12 | crystal_yield | 0.27 | 0.12 | 0.43 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even when seed-excluded product recovery is very small. Q01–Q02: S3 is predicted to outperform S1 through lower solubility, lower nucleation tendency, faster growth and less impurity occlusion, although the 0.045 g seed charge still drives excessive number-weighted fines. Q03–Q04: reducing S0 seed from 0.045 to 0.001 g should sharply reduce particle number and increase size; Q03 is the only point-estimate-feasible case, but its fines interval crosses 0.50. Q05–Q06: gradual cooling should favor growth over nucleation, whereas the rapid initial drop in Q06 creates persistent fines despite the long endpoint residence; final recovery may be similar. Q07–Q08: the post-ramp 315 K reheat can redissolve deposited product, followed by renewed nucleation during rapid recooling, so Q08 is assigned lower recovery and poorer size/fines but slightly cleaner solids. Q09–Q10: two hours at 292 K permits some additional seed-excluded deposition and growth, but both remain seed-dominated and highly fine. Q11–Q12: doubling reagent increases supersaturation and recovery, but with S0's high nucleation and occlusion tendencies it is expected to worsen fines and purity. Uncertainty is broad because the campaign directly characterized mainly C1/S2 at much larger charge, while these predictions extrapolate to S0/S1/S3, unusually large seed-to-reagent ratios, a hotter reaction, and very long thermal histories.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **A compliant C1/S2 operating region exists.** Batches 2–6 and 10–12 directly produced particles with purity above 0.80 and fines below 0.50. Batch 10 gave recovery 0.6762, purity 0.9874 and fines 0.1453; its 0.035 L process family remained compliant in batch 12.
- **Solvent loading has a strong, nonlinear association with fines.** At 0.030 L S2, batches 8 and 9 had fines of 0.987 and 1.000. At 0.0325–0.035 L, batches 10–12 had fines of 0.034–0.145. The observed transition is real within these batches, although calling it a mechanistic nucleation threshold remains an interpretation.
- **The tested large-seed/quench history was unsuitable.** Batch 1, with 0.05 g seed and a quench, produced fines of 0.997. Low-seed or unseeded slow-cooling batches 2–5 produced fines around 0.27–0.29. This supports an association but does not isolate seed mass because cooling and reaction histories also differed.
- **Tested rescue strategies did not repair the 0.030 L regime.** A reheat/recool cycle in batch 8 and multistage slow cooling in batch 9 both ended with nearly all fines. This conclusion is limited to those specific histories.
- **Added seed was not necessary under every condition.** Unseeded batch 5 still crystallized and was compliant, contradicting any strong claim that seeding was required.

### Contradicted or substantially revised
- **Monotonically reducing solvent should improve recovery** was contradicted. Recovery increased when moving from 0.080 to 0.040–0.035 L, but the 0.020 L batch 7 had lower recovery, 0.5670, and fines of 0.9869.
- **An equilibrium-solubility-only account is sufficient** was contradicted by the non-monotonic recovery and drastic particle-quality changes. Kinetic nucleation, growth, slurry history or separation behavior must contribute.
- **Thermal ripening would necessarily remove fines** was contradicted for the tested 0.030 L process by batch 8.

### Still untested or only indirectly supported
- C1 or S2 being superior to the other anonymous catalysts or solvents was not established experimentally; almost all optimization used C1/S2. That claim relies mainly on the material dossier.
- Preferential impurity rejection by S2 is a plausible interpretation of high crystal purity despite moderate reaction selectivity, but no mother-liquor composition or impurity-incorporation measurement directly demonstrated it.
- The proposed supersaturation-driven nucleation mechanism was inferred from endpoint measurements. No time-resolved particle measurement located when the fine-particle population formed.
- The independent effects of seed dose, quenching, cooling rate, reaction time and agitation remain partly confounded.
- None of the twelve held-out predictions has truth data, so their solvent, history and scale extrapolations remain untested.

## 2. One additional experiment

I would run the batch-10 process at the boundary midpoint, using **0.03125 L S2**, 0.040 mol reagent, 0.005 mol C1, 360 K for 900 s, 0.0002 g seed, the same 14,400 s cooling to 250 K and two cold holds. I would add non-destructive particle-size measurements immediately after seeding, at several points during cooling, on reaching 250 K, after each hold and before filtration.

This single trajectory would distinguish several explanations using the existing 0.030, 0.0325 and 0.035 L batches as comparators:

- **Sharp supersaturation/nucleation boundary:** fines should rise abruptly during a particular cooling interval and remain above 0.50, while recovery may remain near 0.67.
- **Smooth concentration effect or batch variability:** particle metrics should change gradually, with an endpoint intermediate between batches 9 and 11 rather than an abrupt all-fines transition.
- **Seed-population mechanism:** excessive fines should already be evident immediately after seeding and change comparatively little during cooling.
- **Late secondary nucleation:** the slurry should initially be acceptable, then cross into high fines during low-temperature cooling or holding.
- **Filtration or endpoint-assay artifact:** in-situ measurements should remain acceptable while the post-filtration final assay alone reports high fines.

The experiment would not prove a molecular mechanism, but it would locate the history segment responsible for the quality transition and test whether the apparent 0.030–0.0325 L boundary is reproducible.

## 3. Least-used observation and least-reliable prediction

The account used the **crystal-size channel** least effectively. It concentrated on recovery, purity and the hard fines constraint without reconciling size and fines quantitatively. For example, batch 10 reported normalized crystal size 0.0738, corresponding nominally to a number-weighted d50 below 20 µm, yet its reported fraction below 20 µm was only 0.145. Batch 11 shows a similar tension, whereas batch 12 is more internally consistent. Independent channel noise, synthetic-channel construction or unreported distributional details may explain this, but the mechanism report should have highlighted the inconsistency rather than treating fines and size as fully interchangeable evidence.

The least reliable held-out prediction is **Q03**. Its prediction is the only point estimate classified as quality-feasible, but its fines estimate is 0.40 with an 80% interval of 0.22–0.60, directly crossing the 0.50 limit. It also extrapolates simultaneously from S2 to experimentally untested S0, from 0.040 mol to 0.004 mol reagent, to a much larger seed-to-product ratio, a 385 K reaction and an exceptionally long cooling program. Whether low seed suppresses particle number or whether low target concentration leaves mostly fine seed particles is unresolved. This assessment does not change the sealed Q03 prediction; it identifies why confidence in it is lowest.
