# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Scope and material identity
The catalysts C0–C3 and solvents S0–S3 are anonymous benchmark materials, so the mechanism can only be expressed through functional roles inferred from the experiments, not real molecular identities.

Reaction behavior
Across most batches, conversion was approximately 0.985–1.000, while reaction yield and selectivity were only about 0.51–0.62. Thus incomplete conversion was not the principal upstream limitation; product-versus-byproduct partitioning was. A useful empirical relation is

Y_rxn ≈ X × S_eff,

where X is conversion and S_eff represents effective selectivity after degradation and byproduct formation. The measured byproduct and degradation channels show that these losses remained relevant even at nearly complete conversion.

Under the common S1 recipe—0.04 mol reagent, 0.005 mol catalyst, 360 K for 3600 s—the catalyst screen gave crystal recoveries of 0.510 for C0 (batch 4), 0.495 for C1 (batch 7), 0.465 for C2 (batch 8), and 0.498 for C3 (batch 9). The corresponding reaction yields were approximately 0.601, 0.582, 0.542, and 0.585. This observation supports C0 as the best observed catalyst for recovery, but it does not establish a large intrinsic difference between C0 and C3: their crystal-recovery difference, 0.012, is close to the final-assay crystal-yield standard uncertainty of 0.01. C3 also showed a larger degradation warning (0.220 versus 0.128 for C0), which is consistent with a less favorable reaction history, although that channel is mechanistic evidence rather than a directly identified species balance.

Solvent effects
Solvent identity had the clearest effect on crystallization behavior. With C0 and the same reaction, seeding, and cooling program, the observations were:

• S0, batch 2: crystal recovery 0.482, purity 0.985, fines 0.583.
• S1, batch 4: recovery 0.510, purity 1.000, fines 0.368.
• S2, batch 5: recovery 0.433, purity 0.978, fines 0.260.
• S3, batch 6: recovery 0.389, purity 0.989, fines 0.614.

My interpretation is that the solvents alter both target-product solubility and the balance between nucleation and growth. In conventional supersaturation notation,

S = C/C*(T, solvent),
J ≈ k_n(S−1)^m,
G ≈ k_g(S−1)^g,

where J is nucleation rate and G is crystal growth rate. S1 appears to provide a favorable compromise: sufficient supersaturation for recovery without the excessive secondary nucleation/fines seen in S0 and S3. S2 appears even more growth-selective or less nucleation-prone, but its lower recovery suggests greater residual solubility or reduced upstream target availability. These are interpretations; solubility curves and direct nucleation kinetics were not measured.

Reaction–crystallization coupling
Overall crystal recovery is defined relative to the initial reagent charge, so a useful decomposition is

Y_crystal = Y_rxn × f_capture,

where f_capture is the fraction of reaction-stage target ultimately recovered as seed-excluded crystal product. Approximate examples are:

• Batch 4: 0.510/0.601 ≈ 0.85 capture.
• Batch 2: 0.482/0.620 ≈ 0.78 capture.
• Batch 10: 0.538/0.614 ≈ 0.88 capture, but with excessive fines.

Consequently, improving reaction yield alone is insufficient: the crystallization must also capture product without driving the fines fraction above 0.50. High final crystal purity, generally 0.978–1.000 in the principal screen, despite reaction selectivities near 0.55–0.62, indicates that filtration/crystallization rejected much of the reaction-derived impurity into the liquid phase. Purity was therefore not the active constraint in this campaign; morphology was.

Process-history dependence
The crystal-size distribution depended strongly on the complete thermal and seeding history, not merely the final temperature.

Batch 1 used S0, 0.03 g seed, one 7200 s cooling step, and then a passive wait during which the slurry warmed to about 290.5 K. It produced fines of 0.861 and normalized crystal size 0.057. Batch 2 increased seed to 0.05 g and used two controlled 14400 s stages, first to 300 K and then to 278 K. Recovery stayed essentially unchanged (0.483 versus 0.482), but fines fell to 0.583 and size increased to 0.101. The observation supports slower controlled supersaturation generation and greater seed surface area as morphology-control measures.

An initially plausible alternative was to cool before seeding so that seed would be introduced nearer a supersaturated state. Batch 3 tested delayed seeding at 320 K and later included a 310 K reheat/recool cycle. Its fines were 0.638 before the cycle and 0.687 afterward; final recovery was 0.467. Thus delayed seeding and thermal cycling did not improve this S0 process. Possible interpretations include uncontrolled primary nucleation before seed addition, loss of productive seed history, or new nucleation during recooling. Seed dissolution was not measured, so these alternatives remain unresolved.

Concentration tradeoff
Reducing S1 volume increased recovery but worsened morphology:

• 0.060 L, batch 4: recovery 0.510, fines 0.368.
• 0.050 L, batch 11: recovery 0.521, fines 0.518.
• 0.040 L, batch 10: recovery 0.538, fines 0.602.

This is consistent with higher concentration producing greater supersaturation and capture but also a much higher nucleation rate. Batch 12 repeated the 0.050 L condition with an additional 14400 s stage at 278 K. Recovery rose slightly to 0.524, but fines remained noncompliant at 0.526. Therefore, a simple low-temperature growth hold did not reverse fines formed earlier in the trajectory.

The unresolved optimization region lies between 0.050 and 0.060 L S1, potentially combined with altered seed timing, a gentler initial cooling ramp, or staged solvent addition. Volumes in that interval were not tested. It is possible that a narrow condition could exceed batch 4 recovery while maintaining fines below 0.50, but the existing evidence does not establish it.

Revisions to the working account
The initial expectation emphasized catalyst identity and reaction temperature. The campaign revised that view: catalyst affected upstream yield, but solvent identity and supersaturation history dominated whether the final crystals met the fines constraint. The initial belief that seeding nearer supersaturation would necessarily reduce fines was also revised after batch 3. Finally, the concentration studies showed that maximizing isolated recovery without accounting for nucleation produces an unacceptable particle population.

Uncertainty and evidential limits
Final-assay standard uncertainties were approximately 0.01 for crystal recovery, 0.01 for purity, 0.018 for fines, 0.025 for normalized size, and 0.006 for reaction yield. Batch 4 exceeded the purity threshold by 0.20 and was below the fines limit by 0.132, margins much larger than analytical noise. Its recovery advantage over several other compliant batches was smaller: batch 9 reached 0.498 and batch 7 reached 0.495. More importantly, batch 4 was not exactly replicated, so process repeatability and batch-to-batch variance remain unknown. The recommendation is therefore the highest observed compliant result, not a statistically validated global optimum.

All observed safety risks were well below the 0.65 limit, generally about 0.15–0.21. The mechanistic conclusions are specific to this bounded synthetic system and should not be interpreted as claims about real catalysts, solvents, or physical substances.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.24 | 0.12 | 0.39 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q01 | crystal_yield | 0.39 | 0.29 | 0.49 |
| Q02 | crystal_fines_fraction | 0.54 | 0.36 | 0.71 |
| Q02 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q02 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q02 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q03 | crystal_fines_fraction | 0.78 | 0.61 | 0.9 |
| Q03 | crystal_purity | 0.96 | 0.89 | 1 |
| Q03 | crystal_size | 0.045 | 0.015 | 0.09 |
| Q03 | crystal_yield | 0.36 | 0.25 | 0.47 |
| Q04 | crystal_fines_fraction | 0.35 | 0.2 | 0.51 |
| Q04 | crystal_purity | 0.97 | 0.91 | 1 |
| Q04 | crystal_size | 0.09 | 0.04 | 0.15 |
| Q04 | crystal_yield | 0.38 | 0.28 | 0.49 |
| Q05 | crystal_fines_fraction | 0.34 | 0.19 | 0.5 |
| Q05 | crystal_purity | 0.97 | 0.91 | 1 |
| Q05 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q05 | crystal_yield | 0.38 | 0.28 | 0.49 |
| Q06 | crystal_fines_fraction | 0.55 | 0.38 | 0.71 |
| Q06 | crystal_purity | 0.96 | 0.89 | 1 |
| Q06 | crystal_size | 0.065 | 0.025 | 0.12 |
| Q06 | crystal_yield | 0.39 | 0.28 | 0.5 |
| Q07 | crystal_fines_fraction | 0.31 | 0.17 | 0.47 |
| Q07 | crystal_purity | 0.97 | 0.91 | 1 |
| Q07 | crystal_size | 0.11 | 0.055 | 0.18 |
| Q07 | crystal_yield | 0.38 | 0.28 | 0.49 |
| Q08 | crystal_fines_fraction | 0.57 | 0.39 | 0.73 |
| Q08 | crystal_purity | 0.96 | 0.88 | 1 |
| Q08 | crystal_size | 0.075 | 0.03 | 0.14 |
| Q08 | crystal_yield | 0.33 | 0.22 | 0.45 |
| Q09 | crystal_fines_fraction | 0.75 | 0.55 | 0.9 |
| Q09 | crystal_purity | 0.84 | 0.7 | 0.94 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.08 |
| Q09 | crystal_yield | 0.03 | 0 | 0.1 |
| Q10 | crystal_fines_fraction | 0.58 | 0.39 | 0.75 |
| Q10 | crystal_purity | 0.92 | 0.81 | 0.98 |
| Q10 | crystal_size | 0.06 | 0.02 | 0.12 |
| Q10 | crystal_yield | 0.17 | 0.07 | 0.29 |
| Q11 | crystal_fines_fraction | 0.33 | 0.18 | 0.49 |
| Q11 | crystal_purity | 0.97 | 0.91 | 1 |
| Q11 | crystal_size | 0.095 | 0.045 | 0.16 |
| Q11 | crystal_yield | 0.38 | 0.28 | 0.49 |
| Q12 | crystal_fines_fraction | 0.56 | 0.38 | 0.73 |
| Q12 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q12 | crystal_size | 0.085 | 0.035 | 0.15 |
| Q12 | crystal_yield | 0.41 | 0.28 | 0.54 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 applies the observed solvent ranking: S1 should retain more target with fewer fines than S3. Q03–Q04 assigns the larger seed charge lower nucleation-driven fines and larger particles, with little yield change because seed is excluded from recovery. Q05–Q06 favors gradual cooling over an initial crash; equal total time should give similar recovery, but the crash is expected to establish a finer population that holding cannot fully erase. Q07–Q08 treats the 315 K reheat/rapid recool as partial redissolution followed by renewed nucleation, consistent with the campaign’s unfavorable thermal-cycle result. Q09–Q10 predicts that a 292 K growth hold raises seed-excluded recovery and size relative to immediate filtration, but probably remains fines-limited. Q11–Q12 reflects the observed concentration tradeoff: doubled reagent loading can increase capture while worsening fines and modestly reducing purity, with additional uncertainty from the halved catalyst-to-reagent ratio. Intervals are deliberately broad because these recipes extrapolate to lower charge, higher reaction temperature, much longer cooling histories, and catalyst C1; several morphology intervals cross the 0.50 feasibility boundary.

## K2

1. Status of the main claims

Supported by direct observations

• Solvent identity strongly affects the recovery–morphology balance. Under the common C0/360 K reaction and slow-cooling recipe, S1 in batch 4 gave crystal yield 0.510, purity 1.000 and fines 0.368. S0 in batch 2 gave 0.482/0.985/0.583, S2 in batch 5 gave 0.433/0.978/0.260, and S3 in batch 6 gave 0.389/0.989/0.614. The numerical solvent ranking is directly observed. The explanation in terms of solvent-dependent solubility, nucleation and growth constants remains an interpretation because no solubility curve or nucleation rate was measured.

• Concentration created an unresolved recovery–quality tradeoff. With S1/C0, reducing solvent from 0.060 L in batch 4 to 0.050 L in batch 11 raised yield from 0.510 to 0.521 but raised fines from 0.368 to 0.518. At 0.040 L, batch 10 reached yield 0.538 but fines 0.602. Batch 12 added another 14,400 s at 278 K to the 0.050 L process and still had fines 0.526. These outcomes directly support the tradeoff and show that a simple terminal hold did not repair it. Attribution to supersaturation-driven primary or secondary nucleation is plausible but not directly measured.

• Process history matters. In S0, batch 1’s shorter cooling/passive-warming history produced fines 0.861 and size 0.057, whereas batch 2’s larger seed charge and two controlled cooling stages produced fines 0.583 and size 0.101 at essentially unchanged recovery. This directly shows a history-dependent difference, although seed mass, cooling duration and temperature control were confounded.

• C0 was the best observed catalyst for compliant recovery in S1, but the catalyst ranking is weak. Batches 4, 7, 8 and 9 gave yields of 0.510, 0.495, 0.465 and 0.498 for C0–C3. C0 versus C3 differs by only about the 0.01 assay uncertainty, so a decisive intrinsic catalyst advantage is not established.

• Crystallization provided impurity rejection. Final crystal purities were generally 0.978–1.000 despite reaction yields/selectivities near 0.54–0.62. The direct observation is the coexistence of modest reaction selectivity and high crystal purity. Preferential exclusion of impurities into the liquid is the interpretation; liquid-phase impurity inventories were not assayed separately.

Contradicted or revised

• The initial expectation that delaying seed addition until nearer supersaturation would necessarily reduce fines was contradicted by batch 3. Delayed seeding at 320 K gave fines about 0.638 before a thermal cycle, and the subsequent 310 K reheat/recool increased them to about 0.687; final yield was 0.467.

• The idea that extra low-temperature growth time alone could restore compliance at higher concentration was contradicted by batch 12 relative to batch 11. Yield increased slightly, but fines did not fall below 0.50.

• A simple assumption that larger median size always implies fewer fines is not fully supported. For example, batch 5 had very low fines (0.260) but only moderate normalized size (0.070), while batch 8 had size 0.113 and fines 0.282. The two metrics describe different parts of the number-weighted distribution.

Still untested

• No exact replicate of batch 4 was performed, so process repeatability is unresolved.

• Solubility curves, metastable-zone widths, nucleation rates, growth rates, seed dissolution and impurity partition coefficients were not measured.

• The potentially useful S1 volume interval between 0.050 and 0.060 L was not tested.

• Catalyst-by-solvent and catalyst-by-temperature interactions remain largely untested. The catalyst screen was performed only in S1 at one principal temperature history.

2. One additional experiment

I would repeat the batch-11 chemistry—0.04 mol reagent, 0.050 L S1, 0.005 mol C0, 360 K for 3600 s and 0.05 g seed—but replace its two large cooling stages with a finely divided linear ramp from the post-reaction temperature through 300 K to 278 K, keeping the total cooling time equal to 28,800 s. I would take nondestructive particle-size readings near 300 K, midway through the ramp and at 278 K before filtration.

This experiment would distinguish two explanations for batches 11–12:

• Rate/history explanation: the coarse two-stage temperature changes caused an early supersaturation excursion and nucleation burst. A fine ramp should suppress the early rise in fines, produce a progressively larger d50, retain approximately 0.52 recovery and finish below 0.50 fines.

• Concentration/seed-capacity explanation: at 0.050 L, the supersaturation or product-to-seed ratio is intrinsically too high, regardless of ramp smoothness. Fines would approach or exceed about 0.52 again, even with the gentle ramp. Intermediate readings would show whether they appear early or accumulate throughout cooling.

A result with low intermediate fines but high final fines would instead support late secondary nucleation or attrition. A result with high fines at the first reading would support an early nucleation burst or inadequate seed surface. Because this is only one batch, it would diagnose trajectory more effectively than it would establish repeatability.

3. Least effectively used observation and least reliable prediction

The account used the crystal-size observations least effectively. It emphasized fines and treated larger size as a general sign of growth-dominated crystallization, but the campaign showed that d50 and the sub-20 µm number fraction can move somewhat independently. The S2 and catalyst-screen results indicate that a distribution can have modest d50 yet few fines, or a larger d50 while retaining a meaningful fine tail. A better account would model at least two population features rather than a single nucleation-versus-growth axis. Size also had relatively large assay uncertainty (0.025), limiting pairwise interpretation.

Q09 is the least reliable held-out prediction. It filters only 60 s after cooling to 292 K, far outside the campaign’s multi-hour crystallization histories. Seed particles should remain present, but crystal yield is seed-excluded, so the predicted value depends on a very small and unobserved amount of target deposited on those seeds. Purity, fines and normalized size are also unusually sensitive to how seed-only or minimally grown solids are represented. The campaign supplied no close analogue, making Q09 a much larger extrapolation than the solvent, seed, cooling-history or loading comparisons. No prediction truth was available when making this assessment.
