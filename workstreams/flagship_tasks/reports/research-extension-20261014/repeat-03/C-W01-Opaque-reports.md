# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign separates two related but distinct stages: catalytic formation of the target in solution, followed by recovery of that already-formed target as crystals. The reported crystal_yield is therefore a crystallization-stage recovery, not an overall yield from charged reagent.

Useful mass-balance relationships are:

reaction target yield ≈ conversion × selectivity,

m_target,recovered = crystal_yield × m_target,pre-separation,

overall recovered target / initial reactant ≈ reaction yield × crystal_yield.

Thus reaction chemistry determines the amount and impurity environment entering crystallization, whereas crystal_yield measures what fraction of that target is recovered. Crystal purity and particle-size quality determine whether that recovery is usable.

Material effects

Solvent identity was the strongest demonstrated material effect. Under the common C0 catalyst, 360 K reaction, unseeded crystallization, and two long cooling segments to 300 K, S2 in batch 7 gave recovery 0.448, purity 0.980, and fines 0.244. S1 in batch 6 gave recovery 0.358 and a final fines result of 0.521, while S3 in batch 8 gave recovery 0.307 and fines 0.682. S2 therefore changed not merely solubility/recovery but the nucleation–growth balance, producing a much better number-weighted particle distribution.

A plausible interpretation is that each solvent changes the target solubility curve C*(T), interfacial free energy, impurity adsorption, nucleation rate J, and growth rate G. Supersaturation may be represented as σ=(C−C*)/C*. Cooling raises σ; recovery tends to increase as C*(T) falls, but nucleation usually grows more steeply with σ than crystal growth. Excessive nucleation produces many particles below 20 µm. S2 apparently offered a favorable regime in which cooling increased recovery without causing the severe fine-particle population seen with the other solvents.

Catalyst effects were not resolved: all completed recipes used C0. Consequently, no comparative claim about C1–C3 is supported. C0 did reliably permit near-complete conversion. In S2 batches 7 and 9–12, final conversion was approximately 0.986–1.000, reaction yield about 0.581–0.592, and selectivity about 0.563–0.600. Those moderate reaction selectivities coexisted with crystal purities of 0.978–0.995, indicating effective rejection of reaction impurities during S2 crystallization. This is an observation of purification, not proof of a particular molecular rejection mechanism.

Reaction–crystallization coupling

The coupling was principally through target concentration and impurity load. Higher reaction yield supplies more target, while byproducts can alter solubility, nucleation, growth, agglomeration, or occlusion. Nevertheless, fractional crystal recovery cannot by itself reveal overall process yield. For batch 12, the approximate overall recovered-target fraction is 0.585×0.541≈0.316, despite the crystallization recovery being 0.541. Batch 1 similarly combined reaction yield about 0.642 with crystal recovery 0.495, but its fines fraction was 0.897 and therefore unusable under the quality constraint.

This comparison shows why optimizing reaction yield or crystallization recovery alone would have been misleading. S0 sometimes had numerically higher reaction selectivity than S2, yet its tested crystallizations produced unacceptable fines. S2 sacrificed some reaction selectivity but delivered high crystal purity and a qualified particle population.

Process-history dependence

Particle outcomes depended strongly on the entire thermal and seeding history, not only the final temperature.

The initial hypothesis was that seeding followed by slow cooling would suppress primary nucleation. It was revised after the S0 experiments. Batch 2 used 0.05 g seed and prolonged growth near 300 K but still gave fines 0.890 and recovery 0.389. Raising the total seed dose to 1.0 g in batch 3 worsened the final fines result to 0.940, with recovery 0.332. A mechanistic interpretation is that the added seed population itself was too numerous or too small for a number-weighted specification, or that it promoted secondary nucleation. This conclusion is restricted to the tested S0 histories; high-dose seeding was never tested in S2.

A second hypothesis was that warm ripening would dissolve fines preferentially and allow material to regrow on larger crystals. An unseeded S0 cool–reheat–recool history in batch 4 reduced fines to 0.779 compared with the seeded S0 batches, while retaining recovery 0.386. This initially appeared directionally encouraging. However, the stronger reheat in batch 5 produced recovery 0.247 and fines 0.981. Possible explanations include excessive dissolution followed by renewed nucleation, insufficient controlled regrowth, or degradation during the longer warm exposure. Because temperature, residence time, and prior nucleation history changed together, these alternatives remain unresolved; the campaign did not establish a general ripening law.

After identifying S2, endpoint temperature gave the clearest systematic relationship. With otherwise similar unseeded long-cooling histories, final recovery increased from 0.448 at 300 K in batch 7, to 0.475 at 290 K in batch 9, 0.512 at 275 K in batch 10, and 0.538 at 250 K in batch 11. Final fines remained qualified at 0.244, 0.241, 0.273, and 0.276, respectively, and purity remained at least 0.978. This is consistent with lower equilibrium solubility increasing recovery while S2 keeps nucleation sufficiently controlled.

Batch 12 repeated the 250 K endpoint but doubled the cold residence from two to four 14,400 s segments. It gave the highest observed qualified recovery, 0.541, with purity 0.995, fines 0.284, normalized crystal size 0.112, and CSD quality 0.743. The extra residence may have allowed additional approach to solid–liquid equilibrium and growth, but that causal interpretation is not resolved.

Revisions and uncertainty

Three major revisions occurred. First, the general seeded-cooling hypothesis was rejected for the tested S0 regime after batches 2 and 3. Second, warm ripening was initially considered promising after batch 4 but was downgraded after batch 5. Third, the program shifted from manipulating seed and thermal history in S0 to solvent screening; batch 7 then identified S2, after which lower endpoint temperature became the productive optimization variable.

The endpoint trend across S2 batches is large and monotonic enough to be practically persuasive, but it was not randomized or independently replicated. Batch-to-batch reaction variation and chronological drift cannot be completely excluded. The final-assay noise model gives standard deviations of about 0.01 for crystal recovery and purity, 0.018 for fines and CSD quality, and 0.025 for normalized crystal size. Consequently, the recovery difference between batch 11 (0.538) and batch 12 (0.541) is much smaller than one assay standard deviation. Batch 12 has the highest observed recovery, but the benefit of doubling cold residence is not established; batch 11 is a shorter, statistically near-equivalent process.

Batch 6 also illustrates boundary uncertainty: its in-process particle measurement reported fines 0.482, whereas its final assay reported 0.521. That batch should be regarded as borderline rather than qualified. By contrast, batches 7 and 9–12 had fines around 0.24–0.28, leaving margins much larger than the stated measurement noise.

The principal unresolved quality/recovery tradeoff is whether still more aggressive cooling or alternative S2 histories could raise recovery beyond approximately 0.54 without eventually increasing fines, occlusion, or degradation. The tested range did not reach that quality boundary: even the 250 K batches retained substantial fines margin and very high purity. Untested alternatives include other catalysts, catalyst loading, reaction temperature/time optimization, S2-specific low-dose seeding, controlled antisolvent addition, and carefully staged S2 ripening. They may improve overall recovered target or shorten processing, but the present evidence does not justify assuming that they would outperform the completed qualified S2 process.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.43 | 0.27 | 0.59 |
| Q01 | crystal_purity | 0.97 | 0.91 | 1 |
| Q01 | crystal_size | 0.092 | 0.058 | 0.132 |
| Q01 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q02 | crystal_fines_fraction | 0.62 | 0.45 | 0.78 |
| Q02 | crystal_purity | 0.96 | 0.89 | 1 |
| Q02 | crystal_size | 0.069 | 0.039 | 0.108 |
| Q02 | crystal_yield | 0.29 | 0.18 | 0.42 |
| Q03 | crystal_fines_fraction | 0.34 | 0.18 | 0.53 |
| Q03 | crystal_purity | 0.98 | 0.92 | 1 |
| Q03 | crystal_size | 0.112 | 0.073 | 0.16 |
| Q03 | crystal_yield | 0.32 | 0.2 | 0.45 |
| Q04 | crystal_fines_fraction | 0.58 | 0.4 | 0.75 |
| Q04 | crystal_purity | 0.98 | 0.92 | 1 |
| Q04 | crystal_size | 0.074 | 0.044 | 0.113 |
| Q04 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q05 | crystal_fines_fraction | 0.39 | 0.23 | 0.57 |
| Q05 | crystal_purity | 0.98 | 0.92 | 1 |
| Q05 | crystal_size | 0.105 | 0.069 | 0.15 |
| Q05 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q06 | crystal_fines_fraction | 0.76 | 0.59 | 0.9 |
| Q06 | crystal_purity | 0.97 | 0.9 | 1 |
| Q06 | crystal_size | 0.052 | 0.027 | 0.084 |
| Q06 | crystal_yield | 0.38 | 0.26 | 0.51 |
| Q07 | crystal_fines_fraction | 0.41 | 0.25 | 0.58 |
| Q07 | crystal_purity | 0.98 | 0.92 | 1 |
| Q07 | crystal_size | 0.103 | 0.067 | 0.148 |
| Q07 | crystal_yield | 0.36 | 0.24 | 0.49 |
| Q08 | crystal_fines_fraction | 0.31 | 0.14 | 0.55 |
| Q08 | crystal_purity | 0.985 | 0.93 | 1 |
| Q08 | crystal_size | 0.126 | 0.076 | 0.19 |
| Q08 | crystal_yield | 0.29 | 0.16 | 0.43 |
| Q09 | crystal_fines_fraction | 0.94 | 0.81 | 1 |
| Q09 | crystal_purity | 0.96 | 0.84 | 1 |
| Q09 | crystal_size | 0.026 | 0.008 | 0.052 |
| Q09 | crystal_yield | 0.008 | 0 | 0.04 |
| Q10 | crystal_fines_fraction | 0.73 | 0.53 | 0.89 |
| Q10 | crystal_purity | 0.97 | 0.88 | 1 |
| Q10 | crystal_size | 0.058 | 0.028 | 0.096 |
| Q10 | crystal_yield | 0.105 | 0.035 | 0.21 |
| Q11 | crystal_fines_fraction | 0.44 | 0.27 | 0.61 |
| Q11 | crystal_purity | 0.98 | 0.92 | 1 |
| Q11 | crystal_size | 0.099 | 0.063 | 0.144 |
| Q11 | crystal_yield | 0.36 | 0.24 | 0.49 |
| Q12 | crystal_fines_fraction | 0.65 | 0.47 | 0.81 |
| Q12 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q12 | crystal_size | 0.067 | 0.037 | 0.105 |
| Q12 | crystal_yield | 0.51 | 0.39 | 0.63 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The six comparisons were treated as controlled contrasts, but all require extrapolation from the sealed campaign because catalyst C1 and these dilute, very long crystallizations were not tested. Q01–Q02 assigns S1 a better growth/fines balance than S3, consistent with the solvent ranking observed previously. Q03–Q04 predicts that increasing seed mass raises the number of small particles and slightly accelerates recovery; the low-seed case therefore has larger crystals and fewer fines. Q05–Q06 contrasts gradual cooling with an immediate crash: similar eventual recovery is expected, but the crash should cause a nucleation burst, smaller crystals and substantially more fines. Q07–Q08 treats the 315 K anneal as partial dissolution/ripening: it may enlarge crystals and reduce fines, while lowering recovery because only one hour is allowed for recooling; this pair has especially wide intervals because earlier reheating effects were inconsistent. Q09–Q10 predicts that seed particles are present in both cases, but the 60-second batch has almost no seed-excluded recovery; a two-hour hold permits measurable growth yet likely remains fines-limited. Q11–Q12 predicts that doubling reagent concentration increases fractional recovery through greater supersaturation but also increases secondary nucleation and impurity occlusion, creating a recovery–quality tradeoff. Intervals are epistemic 80% ranges and include reaction-condition, catalyst, concentration and history extrapolation; several fines intervals cross 0.50, so their feasibility classifications are less certain than the central estimates suggest.

## K2

1. Status of the main claims

Supported by direct observations:

- Solvent S2 was the most robust crystallization medium tested. Under the common C0/360 K/unseeded 300 K process, batch 7 gave recovery 0.448, purity 0.980 and fines 0.244, compared with batch 6 using S1 (0.358, 0.996, 0.521) and batch 8 using S3 (0.307, 0.971, 0.682). The observed solvent ranking is strong for S1–S3 under that recipe. Interpreting it as a change in solubility, nucleation and growth kinetics is plausible but not directly measured.

- Lower S2 endpoints increased recovery without violating the quality constraints. Recovery rose from 0.448 at 300 K in batch 7 to 0.475 at 290 K in batch 9, 0.512 at 275 K in batch 10, and 0.538 at 250 K in batch 11. Purity stayed at 0.978–0.993 and fines at 0.241–0.276. The monotonic sequence supports a temperature/recovery relationship, although it was neither randomized nor replicated.

- S2 crystallization provided substantial purification. Batches 7 and 9–12 had only moderate reaction selectivity, approximately 0.56–0.60, but crystal purity of 0.978–0.995. The numerical separation is directly observed. Selective rejection of impurities is an interpretation; impurity partitioning was not measured independently.

- The tested high-seed S0 process did not improve particle quality. Batch 3, with 1.0 g total seed, gave fines 0.940 and recovery 0.332, while batch 2, with 0.05 g seed, gave fines 0.890 and recovery 0.389. This contradicts the initial expectation that simply adding more seed would suppress fines in that regime. However, the batches also differed in thermal history, so attributing the entire difference to seed number is not justified.

Contradicted or weakened:

- A general claim that warm ripening improves the S0 particle distribution was not sustained. Batch 4’s moderate cool–reheat–recool history gave fines 0.779, which looked directionally better than the seeded S0 batches. A stronger reheat in batch 5 instead gave fines 0.981 and recovery 0.247. The observations contradict a simple monotonic “more annealing is better” rule. They do not distinguish excessive dissolution, renewed nucleation and degradation.

- A meaningful benefit from doubling the 250 K residence was not demonstrated. Batch 12 gave recovery 0.541 versus 0.538 in batch 11, a difference smaller than the stated 0.01 final-assay recovery noise. Batch 12 also had larger measured normalized size, 0.112 versus 0.091, but that difference is smaller than the 0.025 size-noise scale. Thus batch 12 was the highest observed qualified result, but the residence-time mechanism remains unresolved.

Still untested or only weakly tested:

- Catalyst effects are untested because every campaign batch used C0. Nothing in the source experiments establishes how C1–C3 affect conversion, impurity formation or crystallization.

- S0 was not included in the same clean, unseeded 300 K solvent comparison used for batches 6–8. Therefore, the full four-solvent ranking is not directly established.

- S2-specific seeding, annealing, concentration effects and antisolvent strategies remain untested. Conclusions from seeded or reheated S0 batches should not automatically be transferred to S2.

- The proposed nucleation and growth explanation was not verified by concentration-versus-temperature data, microscopy over time, solubility measurements or population-balance fitting.

2. One additional experiment

I would run a paired split-batch residence-time experiment using the batch-11/12 chemistry: C0, S2, the same reaction history, unseeded cooling to 250 K, and a single homogeneous reaction mixture divided into two equivalent crystallization vessels before cooling. One branch would be filtered after two 14,400 s segments; the other after four segments. Both would receive identical final assays and particle measurements.

This design would distinguish three explanations:

- Continued equilibration/growth: the longer branch should show a recovery increase materially larger than assay uncertainty—roughly more than 0.02—together with stable or larger particle size and no important increase in fines.

- Equilibrium already reached by eight hours: recovery, purity and particle metrics should agree within measurement uncertainty. That result would favor the shorter batch-11 process and identify the batch-12 advantage as ordinary batch or assay variation.

- Secondary nucleation during prolonged cold residence: the longer branch could gain recovery but show higher fines, lower number-weighted size or poorer CSD quality. That would reveal a genuine recovery–quality tradeoff that the existing batch-11/batch-12 comparison was too noisy to establish.

Splitting one homogeneous precursor mixture is important because it removes much of the reaction-stage and initial-composition variation that confounds two independent batches.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was the disagreement in batch 6 between the in-process particle measurement, which gave fines 0.482, and the final assay, which gave 0.521. I cited it mainly as evidence that S1 was borderline. It could have been used more rigorously to examine combined measurement uncertainty, the representativeness of the analytical slurry, and whether filtration or sampling context changes the reported particle population. Because the two values straddle the specification, this observation is especially important for calibrating confidence in feasibility classifications near 0.50.

The least reliable held-out prediction is Q08. It predicts that a 315 K anneal after a very long S0 cooling ramp will reduce fines and enlarge particles, followed by only one hour of recooling. That direction was inferred from the partially encouraging batch 4 result, but batch 5 showed the opposite outcome under a stronger reheat. Q08 also extrapolates to C1, much lower concentration, different seed loading and a substantially different time history. Those simultaneous extrapolations make dissolution, ripening and renewed nucleation difficult to balance, so its predicted recovery and particle-quality intervals are the most mechanism-dependent of the sealed set.
