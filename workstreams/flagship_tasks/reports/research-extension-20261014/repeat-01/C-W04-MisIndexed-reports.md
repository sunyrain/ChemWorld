# C-W04-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign separates two coupled but distinct stages. The reaction creates the target and impurities; crystallization then determines seed-excluded recovery, purity, particle size, and fines. The reported crystal recovery is

Y_c = (recovered target product, excluding seed)/(target product present before separation),

so it is not an overall yield from the original reagent charge. Overall isolated target would scale approximately as reaction yield × Y_c.

Material effects

The reaction screen used catalyst C1 throughout. At 365 K for 3,600 s it consistently produced essentially complete conversion, but only moderate selectivity (about 0.51–0.55), reaction yield near 0.52–0.54, and degradation warning near 0.18–0.23. Thus conversion was not limiting, whereas impurity formation remained substantial. Nevertheless, filtered crystals generally had purity 0.98–1.00, showing that the S2 crystallization rejected most reaction impurities. This supports coupling through impurity load and occlusion rather than through conversion alone. Because C0, C2, and C3 were not tested, C1 cannot be claimed to be the optimal catalyst; its selection remained based on the nominal activity prior and adequate observed performance.

Solvent S2 was favored initially because its dossier suggested low relative solubility, low nucleation tendency, low impurity occlusion, and high crystal growth. The experiments were consistent with that qualitative prior. At otherwise similar concentrated, deeply cooled conditions, S2 batch 8 gave recovery 0.4949, purity 0.9862, and fines 0.3797. S3 batch 10 gave recovery 0.4789, purity 0.9787, and fines 0.4752. This comparison suggests that S2 better balances recovery and particle quality, but only one S3 batch was run and S0/S1 were not tested. Moreover, the recovery difference between S3 batch 10 and the lower of the two S2 recipe replicates, batch 12, was small; therefore a universal solvent ranking is not established.

Reaction–crystallization coupling

Complete conversion did not guarantee high crystal recovery. Batches 2–4 all used the same C1/S2 reaction recipe, yet progressively deeper and slower cooling changed recovery from 0.4217 at 278 K/7,200 s (batch 2), to 0.4468 at 260 K/10,800 s (batch 3), and 0.4716 at 250 K/14,400 s (batch 4). Purity stayed at 0.986–1.000. The most direct interpretation is that lower temperature reduced target solubility and increased supersaturation, transferring more target into the solid phase.

A useful qualitative framework is

S = C/C*(T, solvent),
J ∝ exp[-A/(ln S)^2],
G ∝ (S−1)^g,

where S is supersaturation, C* is equilibrium solubility, J is nucleation rate, and G is crystal growth rate. Cooling and concentration increase S. Moderate supersaturation can improve recovery through growth, while excessive supersaturation can increase J sharply and generate fines.

The concentration series revealed this boundary. With 0.040 mol reagent, the nominal starting concentrations based on solvent volume were approximately 0.53 M at 0.075 L, 0.67 M at 0.060 L, 0.73 M at 0.055 L, 0.80 M at 0.050 L, and 1.00 M at 0.040 L. At 250 K with slow cooling:

• Batch 4, 0.075 L: recovery 0.4716; fines 0.4017.
• Batch 6, 0.060 L: recovery 0.4829; fines 0.3548.
• Batch 8, 0.055 L: recovery 0.4949; fines 0.3797.
• Batch 9, 0.050 L: recovery 0.4869; fines 0.3942.
• Batch 7, 0.040 L: recovery 0.4933; fines 0.6097, violating the 0.50 limit.

Thus moderate concentration improved recovery without sacrificing quality, but the most concentrated batch crossed a nucleation/fines threshold. This is the clearest unresolved quality–recovery tradeoff: further concentration may retain or increase recovery, but risks a sharp loss of particle quality. Batch 7 demonstrates that maximizing recovery without the fines constraint would select a mechanistically different, unacceptable regime.

Process-history dependence

Thermal path mattered, not merely final temperature. Batch 11 used S2 at 0.055 L but cooled first to 300 K for 7,200 s and then to 250 K for 14,400 s. It produced recovery 0.4779 and fines 0.4017, below the direct-cooling batch 8 result. A plausible interpretation is that prolonged residence at intermediate temperature delayed productive low-temperature supersaturation or allowed competing impurity/degradation processes. However, batch 11 was not replicated, and its recovery was close to the direct-recipe replicate in batch 12; a specific kinetic mechanism is therefore unproven.

Batch 1 included a post-cooling wait during which the temperature drifted back toward ambient before filtration. Its recovery was 0.4229, essentially the same as direct-filter batch 2 at 0.4217. Consequently, the campaign did not demonstrate a beneficial low-temperature aging effect, and the hold was removed to avoid an uncontrolled endpoint. It also did not conclusively show that the warm drift was harmful because the two values were within assay uncertainty.

Seeding was less influential than initially expected over the tested range. At 0.075 L S2 and 250 K, batch 4 used 0.05 g seed and gave recovery 0.4716 with fines 0.4017; batch 5 used 0.01 g and gave recovery 0.4675 with fines 0.3913. These differences are comparable to measurement noise. Seed may still suppress stochastic primary nucleation, but an unseeded control was not performed, so seed necessity and the optimal dose remain unresolved.

Revisions to the working account

The initial model emphasized S2, C1, slow cooling, and seeding. Evidence supported S2 and deep slow cooling within the tested domain, but did not establish comparative superiority of C1 or a seed-dose effect. After batches 1–3, the focus shifted from adding a low-temperature hold to maintaining a colder endpoint and filtering directly. Batches 4–9 then showed that solvent volume—and hence concentration—was a stronger optimization variable than the tested seed-dose change. The expectation that a staged cooling path might improve particle growth was not supported by batch 11. The final account therefore centers on a supersaturation window: enough concentration and cooling for high recovery, but not enough to trigger excessive number-weighted fines.

Uncertainty and scope

Final-assay standard deviations were approximately 0.01 for crystal recovery, 0.01 for purity, and 0.018 for fines; crystal-size uncertainty was larger. Exact batch-8 recipe replication in batch 12 produced recovery 0.4808, purity 1.000, and fines 0.3947. The two-replicate mean is approximately 0.4879 recovery and 0.3872 fines. Their recovery spread of about 0.014 is modest but meaningful relative to the stated single-assay noise, so batch 8 should be viewed as the best observed qualifying batch rather than proof that its expected recovery is exactly 0.4949. Batches 6, 8, 9, and 12 may belong to a relatively broad feasible optimum around 0.05–0.06 L S2.

The strong fines failure in batch 7 is much larger than instrument uncertainty and robustly identifies the 0.040 L condition as unacceptable under the stated constraint. By contrast, smaller recovery differences among batches 6, 8, 9, 10, and 12 are not decisive without additional replication. Untested alternatives include other catalysts, S0/S1, unseeded crystallization, factorial separation of cooling endpoint from duration, altered agitation, and controlled low-temperature aging. These alternatives could refine the mechanism but are not required to explain the observed recommendation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.23 | 0.46 |
| Q01 | crystal_purity | 0.9 | 0.83 | 0.96 |
| Q01 | crystal_size | 0.28 | 0.17 | 0.4 |
| Q01 | crystal_yield | 0.3 | 0.21 | 0.39 |
| Q02 | crystal_fines_fraction | 0.25 | 0.15 | 0.37 |
| Q02 | crystal_purity | 0.94 | 0.89 | 0.98 |
| Q02 | crystal_size | 0.34 | 0.23 | 0.46 |
| Q02 | crystal_yield | 0.39 | 0.3 | 0.48 |
| Q03 | crystal_fines_fraction | 0.53 | 0.4 | 0.65 |
| Q03 | crystal_purity | 0.84 | 0.74 | 0.91 |
| Q03 | crystal_size | 0.16 | 0.07 | 0.27 |
| Q03 | crystal_yield | 0.22 | 0.13 | 0.31 |
| Q04 | crystal_fines_fraction | 0.44 | 0.32 | 0.56 |
| Q04 | crystal_purity | 0.86 | 0.78 | 0.93 |
| Q04 | crystal_size | 0.23 | 0.13 | 0.34 |
| Q04 | crystal_yield | 0.27 | 0.18 | 0.36 |
| Q05 | crystal_fines_fraction | 0.43 | 0.31 | 0.55 |
| Q05 | crystal_purity | 0.86 | 0.78 | 0.93 |
| Q05 | crystal_size | 0.25 | 0.15 | 0.36 |
| Q05 | crystal_yield | 0.28 | 0.19 | 0.37 |
| Q06 | crystal_fines_fraction | 0.54 | 0.42 | 0.66 |
| Q06 | crystal_purity | 0.83 | 0.75 | 0.91 |
| Q06 | crystal_size | 0.14 | 0.06 | 0.25 |
| Q06 | crystal_yield | 0.29 | 0.2 | 0.38 |
| Q07 | crystal_fines_fraction | 0.4 | 0.29 | 0.52 |
| Q07 | crystal_purity | 0.87 | 0.79 | 0.94 |
| Q07 | crystal_size | 0.28 | 0.18 | 0.39 |
| Q07 | crystal_yield | 0.3 | 0.21 | 0.39 |
| Q08 | crystal_fines_fraction | 0.34 | 0.22 | 0.47 |
| Q08 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q08 | crystal_size | 0.31 | 0.19 | 0.44 |
| Q08 | crystal_yield | 0.24 | 0.14 | 0.34 |
| Q09 | crystal_fines_fraction | 0.82 | 0.7 | 0.94 |
| Q09 | crystal_purity | 0.86 | 0.72 | 0.95 |
| Q09 | crystal_size | 0.05 | 0.01 | 0.12 |
| Q09 | crystal_yield | 0.015 | 0 | 0.04 |
| Q10 | crystal_fines_fraction | 0.66 | 0.52 | 0.8 |
| Q10 | crystal_purity | 0.87 | 0.76 | 0.94 |
| Q10 | crystal_size | 0.12 | 0.05 | 0.21 |
| Q10 | crystal_yield | 0.12 | 0.05 | 0.2 |
| Q11 | crystal_fines_fraction | 0.42 | 0.31 | 0.54 |
| Q11 | crystal_purity | 0.87 | 0.79 | 0.94 |
| Q11 | crystal_size | 0.25 | 0.16 | 0.36 |
| Q11 | crystal_yield | 0.29 | 0.2 | 0.38 |
| Q12 | crystal_fines_fraction | 0.59 | 0.47 | 0.71 |
| Q12 | crystal_purity | 0.82 | 0.7 | 0.9 |
| Q12 | crystal_size | 0.18 | 0.09 | 0.3 |
| Q12 | crystal_yield | 0.42 | 0.33 | 0.51 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where little new target crystallizes. Q01/Q02: S3 is predicted to outperform S1 through lower solubility and impurity occlusion, with larger particles and fewer fines. Q03/Q04: raising the seed charge should improve nucleation control and growth enough to move S0 from marginally excessive fines to nominal feasibility, although the intervals cross both quality limits. Q05/Q06: gradual cooling and rapid cooling followed by an equal-duration hold should approach similar recovery, but the rapid supersaturation pulse is expected to leave more fines and smaller particles despite aging. Q07/Q08: reheating should dissolve some recovered solid, lowering yield, while preferentially removing fines and improving size and purity after recooling. Q09/Q10: 60 seconds at 292 K gives almost no seed-excluded recovery; a two-hour hold increases recovery and size but is unlikely to erase the fine-particle population created by the rapid drop. Q11/Q12: doubling reagent concentration raises recovery but is predicted to cross the S0 nucleation/fines boundary and increase occlusion. Intervals are deliberately broad because the campaign directly constrained S2 much better than S0/S1, did not isolate long-duration aging laws, and showed roughly 0.01 assay-scale yield noise plus larger recipe-to-recipe CSD variability.

## K2

1. Status of the main claims

Supported by direct observations:
- A colder, longer S2 cooling program was associated with higher recovery while retaining acceptable quality. Batch 2 (278 K/7,200 s) gave recovery 0.4217 and fines 0.4779; batch 3 (260 K/10,800 s) gave 0.4468 and 0.3818; batch 4 (250 K/14,400 s) gave 0.4716 and 0.4017. The observation is a recipe trend; attributing it specifically to lower equilibrium solubility is interpretation because temperature and duration changed together.
- Concentration had a quality boundary. At 0.060, 0.055, and 0.050 L S2, batches 6, 8, and 9 remained feasible, with recoveries 0.4829, 0.4949, and 0.4869 and fines 0.3548–0.3942. At 0.040 L, batch 7 retained high recovery (0.4933) but fines rose to 0.6097. The large fines change exceeds assay noise and supports a real concentrated-regime penalty. Calling it a sharp nucleation threshold rather than a continuous response is still interpretation.
- The recommended S2 recipe was reproducibly feasible, though its exact recovery was variable. Batches 8 and 12 used the same direct-cooling recipe and gave recovery 0.4949 and 0.4808, purity 0.9862 and 1.000, and fines 0.3797 and 0.3947.
- Reaction conversion was essentially complete while selectivity remained moderate, yet filtered-crystal purity was generally 0.98–1.00. This directly shows substantial purification between reaction mixture and recovered crystals. Selective impurity rejection is the likely interpretation, not a directly identified molecular mechanism.

Weakly supported:
- S2 appeared preferable to S3 under the tested concentrated recipe: batch 8 outperformed S3 batch 10 in recovery and fines. However, batch 10 was the sole S3 observation, and its recovery was close to S2 replicate batch 12. The solvent ranking therefore remains provisional.
- A large seed-dose effect was not observed. Batches 4 and 5, using 0.05 and 0.01 g seed, differed by amounts comparable to uncertainty. This supports dose insensitivity only within that interval and recipe.

Contradicted or not supported:
- The expectation that staged cooling would improve growth without sacrificing recovery was not supported. Batch 11 gave recovery 0.4779, below batch 8, without a decisive fines advantage.
- A beneficial post-cooling aging step was not demonstrated. Batch 1, which underwent a temperature-drifting wait, and direct-filter batch 2 had nearly identical recovery.

Still untested:
- Comparative catalyst effects; C1 was used throughout.
- S0 and S1 in the completed campaign, unseeded crystallization, and whether seed is necessary rather than merely dose-insensitive.
- A factorial separation of cooling endpoint, cooling duration, agitation, and low-temperature residence time.
- Whether the batch-7 transition is abrupt, gradual, or partly batch-specific.

2. One additional experiment

I would run the batch-8 process unchanged except use 0.045 L S2 per 0.040 mol reagent, with the same C1 reaction, 0.05 g seed, direct 14,400 s cooling to 250 K, immediate filtration, particle-size measurement, and final assay.

This interpolates between feasible batch 9 at 0.050 L and failing batch 7 at 0.040 L. It would distinguish three explanations:
- A genuine concentration-triggered nucleation boundary: fines should exceed 0.50 while recovery remains near 0.49.
- A narrow boundary confined closer to 0.040 L, or an anomalous batch-7 result: fines should remain near 0.38–0.45 and the batch should be feasible.
- A smooth recovery–quality tradeoff: fines should fall between the neighboring results, near the specification boundary, rather than switching abruptly.

Purity failure accompanied by high fines would instead implicate impurity occlusion as concentration rises, whereas high fines with unchanged high purity would favor excessive target nucleation as the dominant explanation.

3. Least-used observation and least-reliable prediction

The in-situ particle-size measurements collected before filtration in batches 2–12 were used least effectively. The account relied mainly on final-assay size and fines and did not systematically compare those values with the pre-filtration particle measurements. That comparison could have separated genuine process-history effects from filtration or final-assay variation and tested whether the batch-7 fines excursion was already present in the slurry.

Q09 is the least reliable held-out prediction. It combines untested S0 with an extreme 60-second cooling/crystallization interval, far outside the campaign’s multi-hour cooling histories. Its result may be dominated by how the benchmark counts added seed versus newly grown target particles, a behavior not identified experimentally. Consequently, the sealed near-zero recovery, very small size, and high-fines estimates for Q09 depend more on extrapolation than the other predictions.
