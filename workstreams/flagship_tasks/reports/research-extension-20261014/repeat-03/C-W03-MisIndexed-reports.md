# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Reaction stage and material effects

The reaction and crystallization stages were coupled primarily through the amount and composition of target-containing liquor delivered to crystallization. For the reaction, a useful approximate relation is

**reaction yield ≈ conversion × selectivity**, 

with deviations expected from assay noise and minor mass-balance terms. For example, batch 11 gave conversion 0.979, selectivity 0.658, and reaction yield 0.626.

Catalyst C1 was used in most batches because its nominal dossier suggested high activity. It generally gave high conversion, but selectivity remained condition-dependent: batch 1 reached conversion 1.00 with selectivity 0.584, while lower-loading batch 8 gave conversion 0.872 and selectivity 0.785. These observations do not establish a catalyst law because reagent concentration, catalyst quantity, thermal history, and crystallization recipe changed together. Catalyst C2 was used only in batch 4, which gave final conversion 0.989 and selectivity 0.458; that single confounded comparison is insufficient to rank C2 against C1.

Solvent S2 was the most useful crystallization medium. Its nominal properties—lower relative solubility and nucleation tendency, higher growth tendency, and lower impurity occlusion—were qualitatively consistent with the consistently high crystal purities observed in S2. Nevertheless, the low nominal nucleation tendency did not prevent massive nucleation when supersaturation was generated too quickly. Solvent S3, tested in batch 3 with a thermal cycle, gave crystal yield 0.231, purity 0.977, and fines 0.995. This was worse than the principal S2 results, but solvent identity was confounded with reaction and temperature history, so it is evidence against that particular S3 process rather than proof that S3 is intrinsically inferior.

### 2. Crystallization mechanism and reaction–crystallization coupling

A useful interpretation is based on supersaturation:

**S = (C − C*)/C***,

where C is dissolved target concentration and C* is its temperature- and solvent-dependent equilibrium solubility. Crystal growth may be represented schematically as **G = k_g S^g**, whereas primary nucleation often rises much more sharply, for example **J ∝ exp[−B/(ln(1+S))²]**. These are interpretive relationships, not fitted laws for this campaign.

The experiments indicate a narrow operating region in which existing seeds can consume supersaturation by growth before extensive secondary or primary nucleation occurs. Above that region, many new particles form, producing a number distribution dominated by particles below 20 µm. Because the reported fines metric is number-weighted, even a modest mass of newly nucleated particles can make the fines fraction approach one.

Upstream loading therefore affected crystallization in two ways: it changed the amount of target available and the supersaturation trajectory after cooling. Impurities and byproducts could also modify nucleation or growth, although their specific role was not isolated. High final crystal purities suggest strong impurity rejection from the lattice, but high purity did not guarantee acceptable particle size.

The measured crystal yield was the seed-excluded crystallization recovery,

**Y_crystal = recovered target product excluding seed / target product present before separation**.

It is not overall yield from charged reagent. A rough overall isolated-target fraction would instead scale with reaction yield × crystal yield. Thus batch 11 combined reaction yield 0.626 with crystallization recovery 0.281, while its optimization target remained the latter quantity.

### 3. Process-history dependence

Direct cooling at high loading repeatedly generated excessive fines:

- Batch 1, using S2, 0.040 mol reagent, 0.05 g seed, and direct cooling to 275 K, gave crystal yield 0.464 and purity 0.985, but fines 0.997.
- Batch 2 used less seed and a warmer/slower terminal condition, yet still gave yield 0.402 and fines 1.00.
- Batch 5 added approximately forty hours of low-temperature holding after direct cooling. It still gave fines 1.00 and yield 0.416.

Batch 5 is especially important: once a large population of fine particles had formed, extra terminal holding did not measurably coarsen it. This suggests that nucleation history, rather than final temperature or total residence time alone, controlled the particle distribution. Possible explanations include insufficient Ostwald ripening, continued secondary nucleation, or agitation-induced attrition.

A simple reheat/recool cycle was also inadequate. Batch 3 remained at fines 0.995. In batch 4, an initially unseeded warm hold produced no measurable crystals; subsequent seeding and colder cooling produced crystals, but the final fines fraction was again 1.00. This supports the importance of seeds for initiating recovery under mild supersaturation, while also showing that adding seed does not by itself prevent later nucleation.

Lowering concentration exposed the quality/recovery tradeoff. Batch 8 used 0.005 mol reagent in 0.080 L S2 with 0.05 g seed. It produced purity 0.992, fines 0, and high apparent size/CSD quality, but crystal yield was only 0.017. The liquor was apparently dilute enough to favor growth on a small particle population but retained almost all target in solution. At higher or less dilute loadings, recovery increased but fines returned: batch 6 gave yield 0.244 and fines 0.726; batch 7 gave yield 0.291 and fines 0.690; batches 9 and 10 gave fines near one.

The successful history in batch 11 was different. It used 0.010 mol reagent in 0.080 L S2, catalyst C1, a 340 K reaction, 0.05 g seed, and sequential four-hour cooling stages at 295, 290, 285, 280, and 275 K, followed by a four-hour cold hold. The interpretation is that each intermediate stage allowed seeded growth to consume supersaturation before the next solubility decrease. Its in-process particle measurement gave fines 0.199, and its final assay gave crystal yield 0.281, purity 0.997, fines 0.188, and CSD quality 0.724. Agreement between the independent in-process and final fines readings supports the conclusion that this was a genuinely low-fines batch rather than a single noisy value.

The staged-cooling benefit had a loading limit. Batch 12 used an even more finely divided cooling schedule but raised reagent loading to 0.015 mol. Recovery increased to 0.367 and purity remained 0.996, yet fines returned to 1.00. Thus ramp subdivision alone was not sufficient when the target inventory—and hence supersaturation burden—was too high.

### 4. Revisions to the working mechanism

The initial hypothesis was that S2, seeding, and slow cooling would directly produce large, pure crystals with few fines. Purity and recovery were supported, but the predicted low fines were rejected by batches 1, 2, and 5.

The next hypothesis emphasized thermal cycling or changing to S3. Batch 3 did not support that approach, and the long hold in batch 5 showed that additional elapsed time after nucleation was not enough.

The third revision focused on loading and seed-to-product ratio. Batch 8 demonstrated that very dilute operation could eliminate measurable fines, but at unacceptable recovery. The final revision combined an intermediate loading with staged removal of supersaturation. Batch 11 supported this mechanism, whereas batch 12 established that the successful regime did not extend to substantially higher loading.

### 5. Uncertainty and unresolved alternatives

The principal unresolved issue is the sharp, sometimes non-monotonic transition between low-fines and high-fines outcomes. For example, batches 8, 9, and 10 changed loading over a relatively small range but showed very different fines behavior. Stochastic nucleation, assay noise, small differences in target concentration, and uncontrolled interactions among seed ratio, reaction composition, and cooling history may all contribute. The observed response should therefore be treated as a threshold region rather than a precisely known boundary.

No recipe was replicated exactly. Final-assay and particle-size measurements were noisy, and values at zero or one may include clipping. Batch 11 is more credible than a single endpoint because its particle-size and final-assay fines measurements agreed, but replication is still needed to estimate run-to-run reliability.

Other untested explanations or improvements include lower agitation to reduce attrition, alternative seed-size distributions, adaptive cooling based on an in-process supersaturation or particle signal, washing or resuspension to alter purity and fines, solvent mixtures, and a systematic catalyst/temperature screen to improve reaction selectivity before crystallization. These alternatives remain speculative.

The central unresolved tradeoff is clear: dilute operation suppressed nucleation but sacrificed recovery; higher loading improved recovery but often caused nearly all particles to fall below 20 µm. Batch 11 was the observed compromise that best satisfied both quality constraints while retaining useful seed-excluded recovery.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.4 | 0.2 | 0.65 |
| Q01 | crystal_purity | 0.945 | 0.86 | 0.99 |
| Q01 | crystal_size | 0.14 | 0.06 | 0.25 |
| Q01 | crystal_yield | 0.25 | 0.14 | 0.36 |
| Q02 | crystal_fines_fraction | 0.27 | 0.1 | 0.5 |
| Q02 | crystal_purity | 0.97 | 0.91 | 1 |
| Q02 | crystal_size | 0.19 | 0.09 | 0.32 |
| Q02 | crystal_yield | 0.31 | 0.19 | 0.43 |
| Q03 | crystal_fines_fraction | 0.93 | 0.72 | 1 |
| Q03 | crystal_purity | 0.87 | 0.74 | 0.96 |
| Q03 | crystal_size | 0.035 | 0.01 | 0.09 |
| Q03 | crystal_yield | 0.23 | 0.12 | 0.34 |
| Q04 | crystal_fines_fraction | 0.31 | 0.12 | 0.57 |
| Q04 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q04 | crystal_size | 0.17 | 0.08 | 0.3 |
| Q04 | crystal_yield | 0.24 | 0.14 | 0.35 |
| Q05 | crystal_fines_fraction | 0.34 | 0.14 | 0.59 |
| Q05 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q05 | crystal_size | 0.16 | 0.07 | 0.29 |
| Q05 | crystal_yield | 0.24 | 0.14 | 0.35 |
| Q06 | crystal_fines_fraction | 0.96 | 0.8 | 1 |
| Q06 | crystal_purity | 0.87 | 0.73 | 0.96 |
| Q06 | crystal_size | 0.03 | 0.008 | 0.075 |
| Q06 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q07 | crystal_fines_fraction | 0.36 | 0.15 | 0.62 |
| Q07 | crystal_purity | 0.915 | 0.81 | 0.98 |
| Q07 | crystal_size | 0.15 | 0.065 | 0.28 |
| Q07 | crystal_yield | 0.245 | 0.14 | 0.36 |
| Q08 | crystal_fines_fraction | 0.78 | 0.5 | 0.98 |
| Q08 | crystal_purity | 0.9 | 0.78 | 0.97 |
| Q08 | crystal_size | 0.055 | 0.015 | 0.14 |
| Q08 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q09 | crystal_fines_fraction | 0.04 | 0 | 0.18 |
| Q09 | crystal_purity | 0.96 | 0.87 | 1 |
| Q09 | crystal_size | 0.38 | 0.25 | 0.52 |
| Q09 | crystal_yield | 0.006 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.1 | 0 | 0.3 |
| Q10 | crystal_purity | 0.955 | 0.86 | 1 |
| Q10 | crystal_size | 0.39 | 0.25 | 0.54 |
| Q10 | crystal_yield | 0.04 | 0.01 | 0.09 |
| Q11 | crystal_fines_fraction | 0.29 | 0.11 | 0.54 |
| Q11 | crystal_purity | 0.925 | 0.83 | 0.985 |
| Q11 | crystal_size | 0.18 | 0.08 | 0.31 |
| Q11 | crystal_yield | 0.24 | 0.14 | 0.35 |
| Q12 | crystal_fines_fraction | 0.93 | 0.7 | 1 |
| Q12 | crystal_purity | 0.89 | 0.76 | 0.97 |
| Q12 | crystal_size | 0.035 | 0.01 | 0.09 |
| Q12 | crystal_yield | 0.42 | 0.29 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where seed-excluded product recovery is very small. Q01–Q02: S3 is expected to give greater recovery, growth and purity with fewer fines than S1 because of its lower nominal solubility, lower nucleation/occlusion and higher growth tendency. Q03–Q04: raising seed from 0.001 to 0.045 g should provide enough surface area to consume supersaturation, strongly reducing new-nucleus fines. Q05–Q06: gradual staged cooling should preserve seed growth, whereas the 120 s temperature crash should create a large fine-particle population; final-temperature recovery may remain similar after the long hold. Q07–Q08: the late 315 K reheat can redissolve product, and the subsequent one-hour recool is expected to regenerate fines and leave lower recovery than the uninterrupted cold hold. Q09–Q10: at 292 K, two additional hours should increase seed-excluded deposition modestly while retaining a seed-dominated, coarse distribution. Q11–Q12: doubling reagent loading should raise recovery but overwhelm the seed surface and cross into the high-nucleation regime, reproducing the observed quality/recovery tradeoff. Intervals are wide because solvent S0 was not systematically calibrated, nucleation showed threshold-like variability, and none of these exact histories was replicated.

## K2

## 1. Status of the main claims

### Supported

- **Cooling history controls fines, not merely final temperature.** Direct observation: at the same S2 loading of 0.010 mol reagent in 0.080 L solvent, batch 6 used essentially direct cooling and gave crystal yield 0.244 with fines 0.726, whereas staged-cooling batch 11 gave yield 0.281 with fines 0.188. Interpretation: intermediate stages allowed seeded growth to consume supersaturation before secondary nucleation accelerated. The comparison is strong but not perfectly isolated because the terminal temperatures and total residence times differed.
- **Higher loading creates a quality/recovery tradeoff.** Direct observation: batch 11 passed both constraints at yield 0.281, purity 0.997 and fines 0.188; batch 12 increased loading from 0.010 to 0.015 mol and increased recovery to 0.367, but fines rose to 1.00 despite a finely divided cooling schedule. Interpretation: available seed surface was insufficient to buffer the larger supersaturation burden.
- **Dilution can suppress fines at the expense of recovery.** Direct observation: dilute batch 8 gave fines 0 and purity 0.992 but only 0.017 recovery. More concentrated batches 6, 9 and 10 recovered more target but had fines of 0.726, 0.991 and 1.00, respectively. Interpretation: the system crosses a sharp nucleation threshold rather than following a smooth linear response.
- **A long terminal hold cannot reliably repair a fine distribution created earlier.** Direct observation: high-loading batch 5 remained at fines 1.00 after approximately forty hours of additional low-temperature holding. Batches 1 and 2 also remained near fines 1 under shorter direct-cooling histories. Interpretation: particle number was established during the supersaturation excursion and subsequent ripening was too weak to reverse it.
- **Batch 11’s low-fines result has some internal corroboration.** Its pre-filtration particle measurement gave fines 0.199, while the final assay gave 0.188. This agreement supports the observed result, although it is not an independent batch replicate.

### Contradicted or narrowed

- **The initial claim that S2 plus seeding and slow cooling would automatically produce few fines was contradicted.** Batches 1, 2 and 5 all used S2 and seed but produced fines near 1. The claim had to be narrowed to an intermediate-loading, staged-supersaturation regime.
- **Simple thermal cycling as a general remedy was not supported.** Batch 3 included a reheat/recool cycle but ended with fines 0.995. Because it also used S3 and a different history, this contradicts only the broad claim that any thermal cycle will remove fines; it does not exclude a specifically optimized dissolution–regrowth cycle.
- **Residence time alone was contradicted as the dominant control.** Batch 5’s long hold did not improve the distribution, while batch 11’s structured trajectory did.

### Still untested or weakly tested

- **Intrinsic solvent ranking remains untested.** S2 performed best in the campaign, but S3 was represented only by confounded batch 3, and S0 and S1 were not tested. The proposed roles of solubility, growth, nucleation and impurity occlusion therefore remain dossier-based interpretations rather than experimentally isolated effects.
- **Catalyst ranking is untested.** C1 dominated the campaign; C2 appeared only in batch 4 under a different workflow, while C0 and C3 were not tested.
- **Impurity-driven nucleation, growth inhibition and lattice occlusion are untested mechanisms.** High crystal purity shows effective impurity rejection, but it does not identify whether impurities altered nucleation kinetics.
- **Attrition versus secondary nucleation is unresolved.** Agitation was not independently varied during otherwise matched crystallizations.
- **Run-to-run stochasticity is unresolved.** No complete recipe was replicated, so the sharp transition among batches 8–12 could partly reflect stochastic nucleation rather than only deterministic thresholds.

## 2. One additional experiment

I would run a **time-matched direct-cooling control for batch 11**. I would keep its chemistry fixed: S2, 0.080 L solvent, 0.010 mol reagent, 0.00125 mol C1, the same 340 K reaction, and 0.05 g seed. Instead of the five 4-hour stages at 295, 290, 285, 280 and 275 K followed by the cold hold, I would cool directly to 275 K in the first 4-hour period and then hold at 275 K for the remainder of the same total crystallization time. Particle-size measurements immediately after the first period and before filtration would be especially informative.

This would distinguish:

- **Staged supersaturation management:** expect early formation of many particles, final fines above 0.50, smaller crystal size, and recovery similar to or slightly greater than batch 11.
- **Final temperature/total residence-time control:** expect results close to batch 11 despite the different path.
- **Slow ripening after an initial nucleation burst:** expect high early fines followed by a substantial decline during the matched hold.
- **Strong stochastic nucleation:** an unexpectedly low-fines direct-cool result would weaken the causal attribution to staging and emphasize the need for exact replication.

The experiment would not by itself estimate reproducibility, but it would isolate temperature trajectory more cleanly than the existing batch 6 versus batch 11 comparison.

## 3. Least-used observation and least-reliable held-out prediction

The account used the **batch 6 versus batch 7 comparison** least effectively. Both had approximately the same reagent concentration, 0.125 mol/L, but batch 7 halved both reagent and solvent while retaining 0.05 g seed. Batch 7 gave larger crystals and slightly lower fines than batch 6. This observation suggests that absolute product-to-seed ratio or scale-dependent hydrodynamics matters independently of concentration. My account acknowledged that seed ratio and concentration were confounded but did not exploit this near concentration-matched comparison sufficiently.

The least reliable held-out prediction is **Q08**. It combines several extrapolations: untested solvent S0, a 315 K reheat, possible partial or complete dissolution of both product crystals and seeds, and a rapid recool to 278.15 K. The only campaign thermal-cycle example, batch 3, used S3 and a much milder 305-to-295 K cycle, so it provides little quantitative calibration for dissolution extent, renucleation or final recovery in Q08. Consequently, both the direction and magnitude of its size and fines response are less secure than for comparisons based directly on the batch 6/11/12 loading and cooling-history evidence.
