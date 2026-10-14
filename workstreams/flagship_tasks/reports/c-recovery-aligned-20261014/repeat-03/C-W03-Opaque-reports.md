# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign separates naturally into reaction formation and downstream crystallization/isolation. Each batch began with 0.040 mol limiting reagent. The reported crystal recovery was

Y_crystal = n(target in isolated solid, excluding seed)/n(reagent initially charged).

A useful empirical decomposition is

Y_crystal ≈ Y_reaction × η_capture,

where Y_reaction is the final-assay target yield and η_capture combines crystallization, mother-liquor retention, and isolation losses. This is diagnostic rather than an exact mass balance because both outputs are noisy synthetic measurements. Across batches, Y_crystal/Y_reaction ranged from about 0.63 to 0.88, demonstrating that reaction performance alone did not determine isolated recovery.

Material effects

Observation: C0/S0 recipes produced several of the highest recoveries. Batch 1 gave Y_crystal = 0.4855, purity = 0.9876, reaction yield = 0.5957, selectivity = 0.5978, and byproduct signal = 0.2694. Related C0/S0 batches 4 and 10 gave recoveries of 0.4807 and 0.4678. Batch 6, using C0/S2, also performed well at 0.4722 recovery and 0.9992 purity, although its degradation warning was higher (0.2095 versus 0.1161 in batch 1).

Interpretation: C0 with S0 or S2 supported a comparatively favorable combination of target formation and crystallization capture. The consistently high crystal purity despite only moderate reaction selectivity suggests that the solid phase strongly rejected reaction impurities.

This is not an independently established catalyst ranking. Batch 2 used C1/S0 and had reaction selectivity 0.6153—slightly above batch 1—but its different seed dose and crystallization history confound the lower crystal recovery of 0.4577. Likewise, the poor result for C2/S1 in batch 3—reaction yield 0.3473, selectivity 0.3482, byproduct signal 0.4343, and crystal recovery 0.2243—identifies that combined recipe as unfavorable, but does not isolate whether C2, S1, or their interaction was responsible.

Batch 7, involving S3 followed by filtration, S0 resuspension, reheating, and recrystallization, had very low byproduct and degradation signals (0.0389 and 0.0175) but only 0.3355 selectivity and 0.2417 crystal recovery. This may indicate suppression or removal of detectable side products at the expense of target retention, but the solvent exchange and second crystallization make an intrinsic S3 effect unidentifiable.

Reaction–crystallization coupling

Batch 1 converted a reaction yield of 0.5957 into crystal recovery of 0.4855, corresponding to an empirical capture ratio near 0.82. Batch 3 combined weak reaction formation with a lower capture ratio near 0.65, compounding the recovery loss. By contrast, batch 12 had lower reaction yield, 0.5011, but a capture ratio near 0.88 after cooling to 250 K; its final crystal recovery was nevertheless only 0.4392. Thus deep recovery cannot compensate fully for inadequate selective target formation.

The results are consistent with the usual supersaturation framework

S(t) = C(t)/C*(T(t)),

with nucleation and growth responding differently to process history. Qualitatively, nucleation rate rises steeply with supersaturation—for example, classical theory gives J proportional to exp[-A/(ln S)^2]—while crystal growth is often represented as G proportional to (S−1)^g. The final number fraction of fines depends on the time-integrated balance between formation of new particles and growth of existing particles, not merely the final temperature.

Process-history dependence

Several histories changed recovery without resolving particle quality:

• Batch 1 used a small seed dose, cooling to 275 K, and a subsequent hold. It gave the highest numerical recovery, 0.4855.
• Batch 8 stopped at the warmer 315 K endpoint and filtered promptly. Recovery fell to 0.3871, consistent with more target remaining in solution, although this was not an isolated endpoint-temperature comparison.
• Batch 9 used more solvent (0.080 L rather than 0.055 L) and recovered 0.4501. This is consistent with dilution increasing mother-liquor retention, but the single comparison cannot establish causality.
• Batch 12 cooled more deeply to 250 K and achieved a high capture ratio, yet its different 350 K/7200 s reaction history lowered reaction yield and left total crystal recovery below batch 1.
• Batch 10 used staged cooling and long intermediate holds; recovery was 0.4678. Batch 4 added a heat/cool recycle and gave 0.4807. Neither history generated a clear recovery improvement over batch 1.
• Increased seed mass was ineffective in the tested scope. Batch 2 received approximately 0.5 g total seed and batch 5 approximately 2 g, yet their recoveries were 0.4577 and 0.4275. Their final fines fractions were both reported as 1.0. This suggests that added seed mass did not suppress secondary nucleation or that the seed population itself contributed many small particles.

Particle-quality result and revision

The initial mechanistic expectation was that seeding, slow cooling, and aging would shift supersaturation consumption from nucleation toward growth and reduce fines. That expectation was rejected for the explored operating window. Small and large seed charges, an unseeded run, warm and deep endpoints, prolonged holds, staged cooling, thermal cycling, and resuspension/recrystallization all produced final fines fractions of approximately 0.987–1.000. Batch 1 itself had fines = 0.9973. Pre-filtration particle measurements agreed qualitatively, commonly giving about 0.98–1.00.

The purity constraint was comfortably satisfied by every final result discussed here, generally around 0.97–1.00. The unresolved tradeoff was therefore not primarily purity versus recovery; it was recovery versus an essentially unmet particle-number specification. Some changes reduced recovery without materially reducing fines. The gap from the required fines fraction of 0.50 is much larger than the stated measurement noise, so the conclusion that no tested batch was compliant is robust.

Crystal-size readings should be interpreted cautiously. The normalized size channel corresponds to min(d50/250 µm, 1), while fines is a number fraction below 20 µm. A d50-like reading near the threshold can coexist with a high measured fines fraction if the distribution is unusual, but several individual size/fines pairs also reflect instrument noise and process uncertainty. The fines channel, not size alone, is the governing specification.

Uncertainty and limits

Most recipes were single, deliberately different experiments rather than replicated factorial comparisons. Catalyst, solvent, reaction temperature, solvent volume, seed dose, and cooling history were often changed together. Numerical differences such as batch 1 versus batch 4 recovery (0.4855 versus 0.4807) are smaller than the approximate combined assay uncertainty and are not strong evidence of a true advantage. Batch 1 remains the sealed recommendation because it had the highest observed recovery while satisfying purity, not because its superiority over nearby C0/S0 results is statistically proven. It remains explicitly noncompliant on fines.

Untested alternatives include independently factorial catalyst/solvent experiments with replication; seeds having a controlled and independently measured size distribution; very-low-supersaturation growth with product or solvent feed; antisolvent addition separated from reaction-solvent choice; evaporation control; lower-attrition hydrodynamics; selective dissolution or classification of fines; and mother-liquor recycle. Any of these could alter the nucleation-to-growth balance, but the present campaign provides no evidence that they would meet the specification.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.27 | 0.1 | 0.5 |
| Q01 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q01 | crystal_size | 0.24 | 0.12 | 0.37 |
| Q01 | crystal_yield | 0.34 | 0.2 | 0.48 |
| Q02 | crystal_fines_fraction | 0.22 | 0.07 | 0.47 |
| Q02 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q02 | crystal_size | 0.27 | 0.13 | 0.43 |
| Q02 | crystal_yield | 0.23 | 0.1 | 0.38 |
| Q03 | crystal_fines_fraction | 0.16 | 0.04 | 0.38 |
| Q03 | crystal_purity | 0.985 | 0.95 | 1 |
| Q03 | crystal_size | 0.34 | 0.18 | 0.52 |
| Q03 | crystal_yield | 0.44 | 0.3 | 0.56 |
| Q04 | crystal_fines_fraction | 0.29 | 0.1 | 0.55 |
| Q04 | crystal_purity | 0.985 | 0.95 | 1 |
| Q04 | crystal_size | 0.23 | 0.12 | 0.36 |
| Q04 | crystal_yield | 0.46 | 0.33 | 0.58 |
| Q05 | crystal_fines_fraction | 0.2 | 0.06 | 0.43 |
| Q05 | crystal_purity | 0.986 | 0.95 | 1 |
| Q05 | crystal_size | 0.27 | 0.15 | 0.42 |
| Q05 | crystal_yield | 0.47 | 0.34 | 0.59 |
| Q06 | crystal_fines_fraction | 0.62 | 0.38 | 0.84 |
| Q06 | crystal_purity | 0.98 | 0.94 | 1 |
| Q06 | crystal_size | 0.13 | 0.06 | 0.24 |
| Q06 | crystal_yield | 0.48 | 0.35 | 0.6 |
| Q07 | crystal_fines_fraction | 0.17 | 0.05 | 0.39 |
| Q07 | crystal_purity | 0.988 | 0.95 | 1 |
| Q07 | crystal_size | 0.29 | 0.16 | 0.45 |
| Q07 | crystal_yield | 0.48 | 0.35 | 0.6 |
| Q08 | crystal_fines_fraction | 0.39 | 0.16 | 0.68 |
| Q08 | crystal_purity | 0.99 | 0.96 | 1 |
| Q08 | crystal_size | 0.21 | 0.1 | 0.37 |
| Q08 | crystal_yield | 0.43 | 0.28 | 0.57 |
| Q09 | crystal_fines_fraction | 0.82 | 0.58 | 0.98 |
| Q09 | crystal_purity | 0.99 | 0.93 | 1 |
| Q09 | crystal_size | 0.07 | 0.02 | 0.14 |
| Q09 | crystal_yield | 0.015 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.7 | 0.42 | 0.91 |
| Q10 | crystal_purity | 0.985 | 0.94 | 1 |
| Q10 | crystal_size | 0.1 | 0.04 | 0.2 |
| Q10 | crystal_yield | 0.16 | 0.06 | 0.29 |
| Q11 | crystal_fines_fraction | 0.86 | 0.63 | 1 |
| Q11 | crystal_purity | 0.995 | 0.96 | 1 |
| Q11 | crystal_size | 0.06 | 0.015 | 0.13 |
| Q11 | crystal_yield | 0 | 0 | 0.01 |
| Q12 | crystal_fines_fraction | 0.46 | 0.22 | 0.72 |
| Q12 | crystal_purity | 0.98 | 0.94 | 1 |
| Q12 | crystal_size | 0.18 | 0.08 | 0.32 |
| Q12 | crystal_yield | 0.47 | 0.34 | 0.59 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even for Q11, which has no reagent charge and therefore essentially zero seed-excluded yield. For the solvent pair, S1 is predicted to retain more recovery than S3, while S3 gives slightly coarser, lower-fines solids. In the seed pair, 0.001 g provides fewer growth sites and is therefore predicted to give larger particles and fewer fines than 0.045 g, with similar overall recovery. Slow staged cooling (Q05) should suppress secondary nucleation relative to the rapid drop and long cold hold (Q06); their equilibrium recoveries are predicted to be similar. The heat/recool cycle in Q08 may dissolve some solids and then renucleate during rapid recooling, lowering recovery and worsening fines relative to continued low-temperature growth in Q07. Extending growth at 292 K raises recovery in Q10 versus Q09, but two hours is still predicted to leave a fine-rich population. Increased upstream loading in Q12 creates substantial seed-excluded recovery but also raises supersaturation and makes fines borderline. Intervals are deliberately broad because the requested reaction loading, catalyst loading, and multi-day cooling histories extrapolate well beyond the sealed campaign; feasibility near the 0.50 fines boundary is especially uncertain for Q01, Q04, Q08, and Q12.

## K2

1. Claim status

Supported by direct observations:
- Batch 1 was the highest observed recovery result: crystal_yield 0.4855, purity 0.9876, and fines 0.9973. Batches 4 and 10, also based on C0/S0, gave similarly high recoveries of 0.4807 and 0.4678. This supports only the local observation that C0/S0 recipes performed well among those tested.
- Crystallization produced high-purity solids despite moderate reaction selectivity. For example, batch 1 had reaction selectivity 0.5978 but crystal purity 0.9876; batch 6 had selectivity 0.5707 and purity 0.9992. Interpreting this as impurity rejection by the solid phase is reasonable, although direct solid/mother-liquor partition measurements were not made.
- Reaction formation and crystallization capture were both consequential. Batch 3 combined low reaction yield (0.3473) with low crystal recovery (0.2243), whereas batch 12 converted a reaction yield of 0.5011 into recovery of 0.4392. These directly observed differences support the empirical reaction-yield × capture decomposition.
- No tested process met the fines requirement. Final fines were approximately 0.987–1.000 across all 12 batches, corroborated by the available pre-filtration particle measurements. The distance from the 0.50 limit is much larger than stated assay noise.

Contradicted within the tested scope:
- The initial claim that more seeding, slow cooling, or prolonged aging would materially suppress fines was contradicted. Batch 2 used about 0.5 g seed, batch 5 about 2 g, batch 3 was unseeded, batch 10 used staged cooling and long holds, batch 4 used a thermal recycle, and batch 7 included resuspension/recrystallization; none reduced final fines below about 0.987.
- A simple monotonic “colder endpoint gives greater overall recovery” account was not supported. Batch 12 cooled to 250 K but recovered 0.4392, below batch 1 at 275 K, because its upstream reaction history differed. Endpoint temperature alone therefore cannot explain overall recovery.

Still untested or unresolved:
- A causal catalyst ranking remains untested. Batch 2 with C1/S0 had slightly higher reaction selectivity than batch 1 with C0/S0, but seed dose and crystallization history differed. Batch 3 confounded C2 with S1, while batch 11 confounded C3 with concentration and reaction history.
- Independent solvent effects remain unresolved for the same reason. Batch 6 suggests C0/S2 can preserve recovery and purity, whereas batch 7’s S3 result is inseparable from solvent exchange and recrystallization.
- Whether the persistent fines originated in the supplied seed population, secondary nucleation during cooling, attrition, or a growth-rate limitation was not directly measured.
- Antisolvent addition, controlled feed or evaporation, independently characterized seed size, particle classification, and low-attrition hydrodynamics were not tested.

2. One additional experiment

I would run one time-resolved C0/S0 experiment based on batch 1, keeping its reagent charge, catalyst charge, and reaction stage fixed. After quenching, I would add one controlled seed charge and measure particle size immediately, then cool in widely separated stages—approximately 315, 300, 290, and 278 K—with equal holds and particle-size measurements after each stage. I would obtain one reaction HPLC measurement before seeding and the normal final assay after filtration.

This single trajectory would distinguish three competing explanations:
- Seed-dominated fines: the immediate post-seed measurement would already show a high fines fraction, with little qualitative change during cooling.
- Secondary nucleation: the initial seed population would be relatively coarse, followed by a sharp rise in fines at the stage where supersaturation crosses the nucleation threshold.
- Growth limitation or insufficient residence: fines would initially be high but decrease progressively while d50 increases during the holds. Failure to change over long holds would oppose this explanation.

A systematic divergence between in-process particle measurements and the final assay beyond their stated uncertainty would instead raise concern about filtration, sampling representativeness, or measurement-model differences. This design is preferable to another endpoint-only recipe because the campaign already established that many different endpoints can converge to the same fine-rich result.

3. Least effectively used observation and least reliable prediction

The account used batch 2 least effectively. Its C1/S0 reaction selectivity of 0.6153 was slightly better than batch 1’s 0.5978, yet its lower crystal recovery was discussed mainly as evidence favoring the C0/S0 region. Because batch 2 also changed seed dose, endpoint temperature, and residence time, it actually provides little evidence against C1 and should primarily have been treated as evidence that reaction selectivity and downstream recovery can move independently.

Q11 is the least reliable held-out prediction. It contains no reagent charge but does contain seed, making seed-excluded crystal_yield near zero comparatively secure while particles_present, purity, size, and fines depend almost entirely on whether the seed persists, dissolves, or recrystallizes during the exceptionally long cooling history. The campaign contained no seed-only control and did not characterize the initial seed-size distribution. Thus Q11 extrapolates outside the observed reaction–crystallization regime more severely than the other queries. This identifies uncertainty in the sealed prediction; it does not revise its values.
