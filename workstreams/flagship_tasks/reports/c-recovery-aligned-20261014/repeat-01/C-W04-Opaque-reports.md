# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Working process picture
The process comprises two coupled selections. The heated catalytic reaction determines how much target product is available and how much byproduct/degradation accompanies it. Cooling then partitions the target and impurities between crystals and mother liquor while determining nucleation, growth, and agglomeration. The reported crystal recovery is seed-excluded target in isolated solids divided by the initial reagent charge, not merely the fraction crystallized from already formed product:

crystal recovery = n(target in isolated crystals, excluding seed) / n(initial reagent).

A useful qualitative decomposition is therefore

crystal recovery ≈ reaction target yield × crystallization capture fraction,

with the caveat that the reported channels are separately noisy synthetic measurements rather than an exact mass-balance factorization. For batch 12, for example, crystal recovery was 0.525 while the reaction-yield channel was 0.607, consistent with substantial—but incomplete—capture of formed target.

### 2. Reaction-side material effects
**Observations.** With S0, 360 K for 3600 s, and otherwise matched processing, catalyst identity produced modest but meaningful differences. Final crystal recoveries were approximately 0.491 for C0 (batch 4), 0.511 for C1 (batch 5), 0.465 for C2 (batch 6), and 0.515 for C3 (batch 7). All four batches had near-complete measured conversion and high crystal purity. C1 gave the highest measured selectivity in that screen (0.641 in batch 5), whereas C3 gave the highest crystal recovery (0.515 in batch 7), but their difference was small.

**Interpretation.** Once conversion is effectively complete, catalyst choice mainly shifts the competition between target formation and byproduct/degradation rather than increasing reagent disappearance. Thus conversion alone was not a useful optimization endpoint. C1 and C3 appear preferable to C0 and C2 in S0, but the campaign did not establish a statistically secure ordering between C1 and C3.

Solvent identity affected both reaction outcome and crystal population. Using C1 with the same extended cooling history, S0–S3 gave crystal recoveries of about 0.511, 0.504, 0.448, and 0.426 in batches 5, 8, 9, and 10, respectively. Conversely, final fines were about 0.418, 0.171, 0.132, and 0.251. S1–S3 therefore generated cleaner particle-size distributions than S0 but generally sacrificed overall recovery. This can be explained by solvent-dependent reaction selectivity and by different solubility/supersaturation trajectories; the experiment did not isolate those two contributions.

Lowering the reaction temperature from 360 K (batch 5) to 340 K (batch 11), with C1/S0, reduced the degradation-warning channel from roughly 0.126 to 0.078 but also reduced crystal recovery from 0.511 to 0.480. Both still reached nearly complete conversion. The interpretation is that lower temperature suppressed degradation but did not improve net isolated target under the tested residence time—possibly because it altered target/byproduct kinetics or the liquor entering crystallization. This was only a single matched comparison.

### 3. Crystallization history and seed effects
A conventional supersaturation description is useful:

S(T) = C_target / C*_target(T),

where C* is the temperature- and solvent-dependent solubility. Nucleation commonly increases much more steeply with supersaturation than crystal growth. Rapidly traversing a high-S region therefore creates many small particles, while controlled residence at moderate S allows existing crystals to grow. In qualitative population-balance terms,

dN/dt = B(S, seed surface, agitation),

dL/dt = G(S, T),

where B is the nucleation rate and G the linear growth rate. Fines rise when B dominates G over too much of the history.

**Initial observation and revision.** Batch 1 used 0.02 g seed and a relatively fast cool to 280 K. It achieved high purity (0.978) and recovery of 0.445 but produced a fines fraction of 0.953. This showed that the chemistry was feasible but particle quality, not purity, was the immediate constraint.

Batch 2 reduced seed to 0.001 g and used slower staged cooling through 330 K before 280 K. Fines improved to 0.576 at similar recovery (0.438), supporting the idea that lower seed loading and slower supersaturation generation favor growth relative to excessive particle formation. However, seed dose and thermal history changed together, so their individual effects remain confounded. A subsequent 300 K reheat/recool cycle worsened the in-process particle result rather than improving it; that exact cycle was therefore abandoned.

Batch 3 tested an extremely small nominal seed charge. A 0.000001 g charge did not establish an effective crystal population, and cooling could not proceed until approximately 0.000099 g additional seed was supplied. After staged cooling through 330, 300, and 280 K, the in-process fines estimate was 0.492, while the final assay reported 0.502. This identified both an operational seed threshold and the importance of measurement uncertainty close to the 0.50 specification.

The successful revision was an effective seed dose of about 0.0001 g followed by long cooling/holding stages: two stages at 330 K, two at 310 K, two at 290 K, and a final stage at 270 K, each lasting 14,400 s. Batch 4, using C0/S0, then reached recovery 0.491, purity 1.000, and fines 0.415. Batches 5–10 using this history all met the fines constraint. The mechanistic interpretation is that the early high-temperature holds limited uncontrolled primary nucleation and established a small population for growth; subsequent stepped supersaturation supplied material gradually, while the low final temperature increased recovery.

The experiments demonstrate strong path dependence: reaching 270–280 K is not sufficient to predict the result. Seed population, rate and staging of cooling, time spent at intermediate temperatures, and any reheating determine the final number distribution and recovery.

### 4. Reaction–crystallization coupling
Impurities generated during reaction can remain dissolved, incorporate into crystals, poison growth faces, or promote secondary nucleation. Despite changes in byproduct and degradation signals, final purity remained at least about 0.97 in all mature staged-cooling batches. This suggests preferential crystallization of the target in the tested domain, but it does not prove that impurities had no influence on nucleation or growth.

Concentration was also important. Batch 12 used C3/S0 with 0.06 L solvent rather than the 0.08 L used in batch 7. It delivered the highest observed qualifying recovery, 0.5252, with purity 0.9936 and fines 0.3247, compared with 0.5155, 0.9740, and 0.4036 in batch 7. A plausible mechanism is that the more concentrated liquor entered cooling with a larger target inventory per unit solvent and attained useful supersaturation earlier, increasing capture. The long staged history apparently prevented the higher loading from causing a fines failure. However, catalyst, loading, and independent batch variability were not separated factorially, so this concentration effect remains tentative.

### 5. Quality–recovery tradeoff
The solvent screen exposed an unresolved tradeoff. S1 and especially S2 produced much lower fines and higher crystal-size-distribution quality than S0, but at lower recovery. S0 offered the highest recovery while still meeting the fines limit when paired with the extended schedule. Thus the process optimum depends on whether fines merely need to satisfy the stated threshold or whether additional particle-quality margin has independent value.

The final recommendation remains batch 12 because it had the highest observed recovery among qualifying batches and comfortable margins to both constraints. Nevertheless, its recovery advantage over batch 7 was only about 0.010, comparable to the stated final-assay crystal-yield noise scale and obtained without replication. The selection is therefore an empirical incumbent, not proof of a unique optimum.

### 6. Untested alternatives and uncertainty
Important untested or unresolved alternatives include a factorial comparison of C1 versus C3 at both solvent volumes; replicate batches to separate process variability from assay noise; intermediate solvent volumes between 0.06 and 0.08 L; shorter versions of the long holding schedule; seed charges near but above the effective threshold; and agitation effects on secondary nucleation and attrition. No experiment independently varied each cooling hold, so the minimum necessary residence time is unknown. A gentler or narrower reheating step than the unsuccessful batch-2 cycle might enable Ostwald ripening, but that was not tested.

Final-assay noise was approximately 0.01 for crystal yield, 0.01 for purity, and 0.018 for fines, in addition to process uncertainty. Differences near those scales should not be treated as established material effects. The broad conclusions—rapid cooling produced excessive fines, extended staged cooling repeatedly met the fines requirement, and S0 gave higher recovery than S2/S3—are better supported than the precise ranking of close batches or the inferred benefit of concentrated loading.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.28 | 0.15 | 0.44 |
| Q01 | crystal_purity | 0.978 | 0.94 | 0.998 |
| Q01 | crystal_size | 0.115 | 0.075 | 0.17 |
| Q01 | crystal_yield | 0.455 | 0.36 | 0.54 |
| Q02 | crystal_fines_fraction | 0.36 | 0.2 | 0.56 |
| Q02 | crystal_purity | 0.968 | 0.92 | 0.995 |
| Q02 | crystal_size | 0.1 | 0.06 | 0.155 |
| Q02 | crystal_yield | 0.385 | 0.29 | 0.48 |
| Q03 | crystal_fines_fraction | 0.18 | 0.08 | 0.33 |
| Q03 | crystal_purity | 0.975 | 0.935 | 0.998 |
| Q03 | crystal_size | 0.155 | 0.1 | 0.225 |
| Q03 | crystal_yield | 0.455 | 0.35 | 0.55 |
| Q04 | crystal_fines_fraction | 0.43 | 0.27 | 0.61 |
| Q04 | crystal_purity | 0.971 | 0.925 | 0.997 |
| Q04 | crystal_size | 0.095 | 0.055 | 0.145 |
| Q04 | crystal_yield | 0.475 | 0.38 | 0.56 |
| Q05 | crystal_fines_fraction | 0.36 | 0.22 | 0.53 |
| Q05 | crystal_purity | 0.976 | 0.935 | 0.998 |
| Q05 | crystal_size | 0.105 | 0.07 | 0.155 |
| Q05 | crystal_yield | 0.48 | 0.39 | 0.56 |
| Q06 | crystal_fines_fraction | 0.75 | 0.57 | 0.89 |
| Q06 | crystal_purity | 0.968 | 0.92 | 0.996 |
| Q06 | crystal_size | 0.052 | 0.025 | 0.078 |
| Q06 | crystal_yield | 0.49 | 0.4 | 0.57 |
| Q07 | crystal_fines_fraction | 0.28 | 0.16 | 0.44 |
| Q07 | crystal_purity | 0.978 | 0.94 | 0.998 |
| Q07 | crystal_size | 0.12 | 0.08 | 0.175 |
| Q07 | crystal_yield | 0.49 | 0.4 | 0.57 |
| Q08 | crystal_fines_fraction | 0.57 | 0.38 | 0.75 |
| Q08 | crystal_purity | 0.98 | 0.94 | 0.999 |
| Q08 | crystal_size | 0.07 | 0.04 | 0.11 |
| Q08 | crystal_yield | 0.44 | 0.33 | 0.54 |
| Q09 | crystal_fines_fraction | 0.86 | 0.7 | 0.96 |
| Q09 | crystal_purity | 0.95 | 0.84 | 0.995 |
| Q09 | crystal_size | 0.045 | 0.018 | 0.073 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.15 |
| Q10 | crystal_fines_fraction | 0.62 | 0.43 | 0.8 |
| Q10 | crystal_purity | 0.96 | 0.88 | 0.997 |
| Q10 | crystal_size | 0.067 | 0.035 | 0.105 |
| Q10 | crystal_yield | 0.22 | 0.11 | 0.35 |
| Q11 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q11 | crystal_purity | 0.975 | 0.93 | 0.998 |
| Q11 | crystal_size | 0.098 | 0.06 | 0.15 |
| Q11 | crystal_yield | 0.48 | 0.39 | 0.56 |
| Q12 | crystal_fines_fraction | 0.47 | 0.29 | 0.66 |
| Q12 | crystal_purity | 0.958 | 0.89 | 0.993 |
| Q12 | crystal_size | 0.085 | 0.048 | 0.135 |
| Q12 | crystal_yield | 0.52 | 0.41 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 transfer the observed solvent ordering: S1 should retain more target and give fewer fines than S3. Q03–Q04 assume that both seed charges nucleate, but the smaller charge produces fewer, larger particles; the large charge modestly improves capture while worsening fines. Q05–Q06 contrast gradual supersaturation generation with an abrupt plunge: endpoint recovery is similar, but rapid cooling is predicted to create many persistent fines. Q07–Q08 assign the slow history good growth, while the 315 K reheat followed by rapid recooling partly redissolves product and renews nucleation, lowering recovery and worsening fines. Q09–Q10 contain seed particles in both cases; the extra 7200 s permits appreciable seed-excluded deposition and growth, but is probably insufficient to reach the mature-process quality region. Q11–Q12 treat doubled upstream loading as increasing normalized recovery through stronger supersaturation, with a possible purity and fines penalty. Uncertainty is deliberately broad because 385 K reaction/quench conditions, very high seed-to-reagent ratios, and these fine cooling grids were not directly tested; intervals crossing the fines threshold identify particularly uncertain feasibility calls.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **The reaction–crystallization sequence is feasible and purity is not the limiting constraint in the tested region.** Batch 1 already gave crystal yield 0.445 and purity 0.978. The mature staged-cooling batches generally gave purity above 0.97. Interpreting this as preferential target crystallization is plausible, but impurity partitioning was not measured directly.
- **Process history strongly affects particle quality.** Batch 1’s faster cooling produced fines of 0.953. Progressively slower histories gave 0.576 in batch 2, approximately 0.502 in batch 3, and 0.415 in batch 4. Batches 4–12 using the extended staged schedule all met the fines limit. This directly establishes a robust association; seed dose and cooling history were changed together during early development, so their separate causal contributions remain unresolved.
- **A nominal seed charge can be too small to establish an effective population.** In batch 3, 0.000001 g seed did not satisfy the crystallization precondition; adding approximately 0.000099 g did. This directly contradicts the possibility that any nonzero nominal seed charge is operationally sufficient.
- **The tested 300 K reheat/recool cycle did not improve particles.** In batch 2, the in-process fines estimate worsened from 0.533 before reheating to 0.576 afterward, while the size estimate also declined. This contradicts the specific hypothesis that this cycle would promote useful ripening, but not every possible thermal cycle.
- **Catalyst identity affected outcome modestly under S0.** With otherwise similar mature processing, batches 4–7 gave recoveries of 0.491, 0.511, 0.465, and 0.515 for C0–C3. C1 and C3 were numerically preferable, but single batches do not establish that their small difference is reproducible.
- **The solvent screen exhibited a quality/recovery tradeoff.** Relative to C1/S0 in batch 5, S1–S3 in batches 8–10 generally reduced fines substantially but also reduced recovery, especially for S2 and S3. This is a direct matched-screen observation. Attribution to solubility, reaction selectivity, or impurity-mediated growth remains interpretive.
- **Lowering reaction temperature was not beneficial for recovery in the tested comparison.** Batch 11 at 340 K showed less degradation warning than batch 5 at 360 K, but recovery fell from 0.511 to 0.480. This supports a degradation-versus-recovery tradeoff for that specific residence time.
- **Higher concentration was favorable in the available C3/S0 comparison.** Batch 12 used 0.06 L S0 and gave yield 0.525, purity 0.994, and fines 0.325; batch 7 used 0.08 L and gave 0.515, 0.974, and 0.404. Both used C3 and the same main thermal schedule, so my earlier suggestion that catalyst and loading were confounded was overly cautious. The comparison is nevertheless unreplicated, and the yield difference is close to the assay noise scale.

### Interpretive rather than directly demonstrated
- The explanation that gradual supersaturation generation suppresses primary nucleation while intermediate holds favor growth is consistent with the particle results, but nucleation and growth rates were not observed directly.
- The assertion that S1–S3 alter solubility and impurity effects is mechanistically plausible, but the campaign did not measure solubility curves, liquor composition during cooling, or impurity incorporation.
- The decomposition of overall crystal yield into reaction target formation and crystallization capture is useful conceptually, but the measured channels are independently noisy and do not constitute an exact mass balance.

### Still untested
Replicability of the batch-12 advantage; the minimum necessary duration of each cooling hold; monotonic dependence on solvent volume; independent seed-dose effects under one fixed temperature program; agitation and attrition effects; direct mother-liquor recovery; impurity incorporation; and a replicated C1-versus-C3 comparison remain untested.

## 2. One additional experiment

I would repeat **batch 12 exactly**—C3, S0, 0.04 mol reagent, 0.06 L solvent, 360 K for 3600 s, approximately 0.0001 g seed, and the established 330/310/290/270 K schedule—but add a small HPLC sample immediately before seeding and nondestructive particle-size readings after the final 330, 290, and 270 K stages.

This experiment would distinguish three explanations:

1. **Reproducible concentration-driven improvement:** Final recovery again near 0.525 with qualifying fines, while the upstream HPLC target-yield channel remains similar to batch 7. That would support improved crystallization capture at higher concentration.
2. **Reaction-side improvement:** The HPLC reading shows materially more target or better selectivity than suggested by batch 7. The recovery increase would then be partly upstream rather than purely a supersaturation/capture effect.
3. **Noise or unstable particle history:** Final recovery returns near or below batch 7, or fines vary substantially despite the same recipe. That would weaken the claimed concentration advantage and indicate that batch-to-batch variability or stochastic nucleation dominated the small observed difference.

The staged particle readings would additionally show whether fines are established early and then diminish through growth, or appear mainly during the coldest stages.

## 3. Least-used observation and least-reliable prediction

**Least effectively used observation:** the normalized crystal-size channel. My account relied mainly on fines and CSD quality, even though crystal size supplied an independent number-weighted d50 indicator. Some final observations were internally awkward—for example, batch 5 reported fines below 0.50 but a normalized size below 0.08, which would correspond to a d50 below 20 µm. Independent channel noise can produce such inconsistencies, but I should have used the discrepancy more explicitly to temper particle-mechanism claims and to motivate replicated particle measurements.

**Least reliable held-out prediction:** Q08. It extrapolated from the single unsuccessful batch-2 reheat to a materially different history: prolonged slow cooling, heating to 315 K, and rapid recooling. Depending on how much solid dissolves, that treatment could either remove fines through selective dissolution and regrowth or generate a renewed nucleation burst during recooling. No campaign batch mapped that temperature window or measured dissolved mass, so even the direction of the size/fines effect is uncertain. Its prediction interval was therefore broad and its feasibility classification should be regarded as especially fragile.
