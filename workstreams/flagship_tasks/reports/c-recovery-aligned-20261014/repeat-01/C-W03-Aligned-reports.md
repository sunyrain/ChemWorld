# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The process appears to combine a moderately selective catalytic reaction with a highly history-sensitive crystallization. The most useful definitions are

R_crystal = n(target in isolated solid, excluding added seed) / n(initial limiting reagent),

P_crystal = n(target in solid) / n(total measured solid),

F20 = N(particles below 20 µm) / N(all particles).

The objective therefore cannot be inferred from purity or particle appearance alone: a vessel can contain clean, large seed-derived particles while having very little seed-excluded product recovery.

Material effects—observations and interpretation

Solvent S2 with catalyst C1 was the most extensively studied combination. It repeatedly gave very pure isolated solids and the largest recoveries when filtered soon after cold crystallization. Batch 1 gave R_crystal = 0.389 and P_crystal = 0.986; batches 2 and 6 gave recoveries of 0.384 and 0.375 with purities of 0.979 and 0.996. This supports the nominal expectation that S2’s low solubility, strong growth tendency, and low impurity occlusion favor recovery and purity. It did not, by itself, ensure an acceptable number distribution: F20 was 0.601 in batch 1 and approximately 1 in batches 2 and 6.

At 335 K for 1800 s, the reaction-stage HPLC results weakly favored C1 over C0 in S2: batch 2 had selectivity 0.452 and yield 0.422, versus 0.421 and 0.421 in batch 3. Their final recoveries were similarly close, 0.384 and 0.378. Because seed histories differed and no replication isolated catalyst identity, this is only weak evidence for a C1 advantage.

C2 appeared inferior under the tested, milder history. Batch 5, run at 325 K for 900 s, initially showed conversion 0.872, selectivity 0.307, and reaction yield 0.259; its final crystal recovery was 0.222. Temperature and duration were changed simultaneously with catalyst identity, so the experiment does not establish that C2 itself caused the loss.

S1/C1 in batch 4 gave reaction selectivity 0.403 and crystal recovery 0.347, below the main S2/C1 results. Its purity was 1.00 but F20 was 1.00. The solvent comparison is confounded by a 305 K reheat and recooling step, so it supports—but does not prove—an S2 advantage.

Reaction–crystallization coupling

Reaction conversion was commonly near unity, but useful target yield was much lower because parallel byproduct formation limited selectivity. For example, batch 1 had conversion 1.00, HPLC selectivity 0.469, yield 0.463, and byproduct signal 0.356 before crystallization. Its eventual crystal recovery of 0.389 is consistent with crystallization recovering much, but not all, of the target formed. Thus a useful conceptual balance is

n(target solid) ≈ n(reagent charged) × conversion × chemical selectivity × crystallization-recovery fraction − process losses.

The 355 K/3600 s history in batch 1 produced the highest measured crystal recovery, but also a degradation warning of 0.155. Milder 335 K histories reduced that warning—for example 0.049 in batch 2—without materially improving reaction selectivity. This suggests competing productive and degradative pathways, although the campaign did not independently vary temperature and time enough to fit kinetic constants.

Post-filtration reaction metrics in low-recovery batches sometimes appeared internally unusual, such as very low conversion together with a processed yield near one. I do not interpret those as reaction kinetics: they were obtained after phase-changing crystallization and filtration, whereas the pre-separation HPLC measurements are the appropriate evidence for reaction behavior. The final-assay crystal metrics remain the relevant measures of isolated solids.

Process-history dependence

Particle quality was much more sensitive to history than purity. Immediate or staged cold isolation retained product but generated many fines. Batch 2 used 0.20 g total seed and gave F20 = 1.00; batch 3 used no seed and gave F20 = 0.995; batch 5 used 0.01 g and gave F20 = 1.00. Consequently, neither more seed nor removal of seed was a general solution. Added seed may itself contribute numerous counted particles, while insufficient seed permits extensive primary nucleation; these alternatives were not cleanly separated.

Warm aging or reheating changed the result dramatically. In-process particle measurements in batches 7–11 showed normalized sizes around 0.38–0.40, CSD quality near 1, and F20 near zero after aging or reheating. However, final seed-excluded recovery collapsed:

• Batch 7: recovery 0.0119, purity 0.992, F20 = 0.
• Batch 8: recovery 0.0170, purity 0.992, F20 = 0.
• Batch 9, reheated to about 295 K: recovery 0.00793, F20 = 0.0014.
• Batch 10, reheated to about 285 K: recovery 0.00905, F20 = 0.0113.
• Batch 11, reheated to about 278 K: recovery approximately 0.000008, F20 = 0.
• Batch 12, held through repeated nominal 275 K crystallization stages: recovery 0.00296, purity 1.00, F20 = 0.00196.

The leading interpretation is dissolution/ripening: fine product crystals dissolve preferentially, leaving a small population of large particles, much of which may be added seed. Because recovery explicitly excludes seed mass, excellent size and fines measurements can coexist with negligible product recovery. A schematic population balance is

dN(d,t)/dt = nucleation + growth transport − dissolution − aggregation/breakage,

while the solid target balance is

dn_target,solid/dt = precipitation − dissolution − physical loss.

The data imply that histories reducing N for small d also reduced n_target,solid too strongly.

Revisions and uncertainty

The initial expectation was that increased seed and slow cooling would suppress fines while preserving recovery. Batches 2–6 contradicted that simple model: high, low, and zero seed all produced nearly all-fines populations under their respective histories. The hypothesis was revised toward thermal-history control.

Batches 7 and 8 then appeared to validate warm aging as a particle-quality intervention, but their low seed-excluded recoveries showed that particle quality alone was misleading. The model was revised again to a sharp dissolution/ripening tradeoff. Even mild reheating and prolonged 275 K treatment reproduced the loss, strengthening that interpretation.

Important uncertainty remains. Batch 1 retained 0.389 recovery after a nominally related cooling/aging sequence but had F20 = 0.601, whereas batch 7 produced excellent particles and only 0.0119 recovery. The histories were not truly identical: controller configuration, analytical interruption, detailed temperature trajectory, and realized endpoint temperature differed. This discrepancy indicates a narrow and poorly resolved transition rather than a fitted deterministic law. Instrument noise alone is unlikely to explain the order-of-magnitude recovery changes, but it can affect comparisons near the F20 = 0.50 boundary.

Untested alternatives include polymorph-dependent solubility, seed-size effects, aggregation or breakage under stirring, transient supersaturation during ramps, and nonlinear controller behavior. No polymorph-specific instrument was available, and the design did not independently map stirring, ramp rate, seed size, and aging time.

Unresolved quality/recovery tradeoff

The campaign found high-recovery/high-purity material or low-fines/high-purity material, but not both at useful recovery. Batches 1–6 reached recoveries of roughly 0.22–0.39 but failed F20 ≤ 0.50. Batches 7–12 met the purity and fines constraints but recovered only 0.000008–0.017 of the initial reagent. Batch 8 remains the selected operating recommendation because its recovery of 0.0170 was the highest among constraint-compliant batches, not because it achieved the 0.10 feasibility target.

The key unresolved region is the earliest low-temperature aging interval between immediate 275 K isolation and the onset of detectable dissolution/ripening. A future study would need dense time/temperature sampling there, with quantity-sensitive crystal assays paired with particle measurements, to determine whether fines can cross below 0.50 before recovery falls below 0.10.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.18 | 0.05 | 0.39 |
| Q01 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q01 | crystal_size | 0.36 | 0.24 | 0.49 |
| Q01 | crystal_yield | 0.22 | 0.1 | 0.36 |
| Q02 | crystal_fines_fraction | 0.34 | 0.13 | 0.59 |
| Q02 | crystal_purity | 0.89 | 0.78 | 0.97 |
| Q02 | crystal_size | 0.29 | 0.18 | 0.43 |
| Q02 | crystal_yield | 0.24 | 0.11 | 0.4 |
| Q03 | crystal_fines_fraction | 0.76 | 0.52 | 0.94 |
| Q03 | crystal_purity | 0.84 | 0.72 | 0.94 |
| Q03 | crystal_size | 0.13 | 0.05 | 0.25 |
| Q03 | crystal_yield | 0.105 | 0.035 | 0.22 |
| Q04 | crystal_fines_fraction | 0.33 | 0.13 | 0.56 |
| Q04 | crystal_purity | 0.89 | 0.8 | 0.96 |
| Q04 | crystal_size | 0.3 | 0.18 | 0.43 |
| Q04 | crystal_yield | 0.11 | 0.04 | 0.23 |
| Q05 | crystal_fines_fraction | 0.3 | 0.11 | 0.54 |
| Q05 | crystal_purity | 0.89 | 0.79 | 0.96 |
| Q05 | crystal_size | 0.31 | 0.19 | 0.44 |
| Q05 | crystal_yield | 0.11 | 0.04 | 0.23 |
| Q06 | crystal_fines_fraction | 0.7 | 0.44 | 0.9 |
| Q06 | crystal_purity | 0.84 | 0.71 | 0.94 |
| Q06 | crystal_size | 0.15 | 0.06 | 0.28 |
| Q06 | crystal_yield | 0.115 | 0.04 | 0.24 |
| Q07 | crystal_fines_fraction | 0.27 | 0.09 | 0.5 |
| Q07 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q07 | crystal_size | 0.33 | 0.21 | 0.46 |
| Q07 | crystal_yield | 0.115 | 0.04 | 0.24 |
| Q08 | crystal_fines_fraction | 0.05 | 0 | 0.18 |
| Q08 | crystal_purity | 0.97 | 0.89 | 1 |
| Q08 | crystal_size | 0.41 | 0.28 | 0.54 |
| Q08 | crystal_yield | 0.018 | 0.002 | 0.07 |
| Q09 | crystal_fines_fraction | 0.02 | 0 | 0.12 |
| Q09 | crystal_purity | 0.995 | 0.96 | 1 |
| Q09 | crystal_size | 0.39 | 0.28 | 0.5 |
| Q09 | crystal_yield | 0.003 | 0 | 0.018 |
| Q10 | crystal_fines_fraction | 0.38 | 0.15 | 0.65 |
| Q10 | crystal_purity | 0.93 | 0.82 | 0.99 |
| Q10 | crystal_size | 0.25 | 0.14 | 0.38 |
| Q10 | crystal_yield | 0.035 | 0.008 | 0.1 |
| Q11 | crystal_fines_fraction | 0.28 | 0.1 | 0.52 |
| Q11 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q11 | crystal_size | 0.32 | 0.2 | 0.45 |
| Q11 | crystal_yield | 0.11 | 0.04 | 0.23 |
| Q12 | crystal_fines_fraction | 0.6 | 0.35 | 0.82 |
| Q12 | crystal_purity | 0.84 | 0.72 | 0.94 |
| Q12 | crystal_size | 0.2 | 0.1 | 0.33 |
| Q12 | crystal_yield | 0.18 | 0.07 | 0.32 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All batches contain added seed, so particles are expected even when seed-excluded product recovery is nearly zero. Q01–Q02: S3's greater nominal reaction activity may slightly raise recovery, while S1's lower solubility, lower nucleation tendency, stronger growth and lower occlusion should give cleaner, larger particles with fewer fines. Q03–Q04: increasing seed from 0.001 to 0.045 g is expected to shift deposition toward existing crystals and suppress secondary nucleation, with little thermodynamic effect on seed-excluded yield. Q05–Q06: gradual cooling should reduce supersaturation peaks; the crash-and-hold history should have similar ultimate recovery but substantially more fines and occlusion. Q07–Q08: the 315 K excursion is expected to dissolve much of the newly formed product, particularly fines, leaving large, pure, predominantly seed-derived particles and sharply lower recovery. Q09–Q10: after only 60 s at 292 K, isolated solids should be almost entirely seed; two additional hours permit measurable growth and recovery but also some new fine-particle formation. Q11–Q12: doubled reagent loading should increase recovery through greater supersaturation, but the unchanged catalyst charge and higher solids burden should reduce purity and size and raise fines. The 80% intervals are deliberately broad because these recipes use S0 extensively, operate at 385 K, include quenching, and employ much longer cooling histories than the completed campaign; the largest uncertainties concern reaction degradation, solvent-specific solubility, and whether the onset of secondary nucleation crosses the fines threshold.

## K2

1. Status of the main claims

Supported by direct observations:

- S2/C1 can give high-purity, relatively high-recovery crystals, but with excessive fines. Batch 1 directly measured crystal yield 0.389, purity 0.986 and fines 0.601; batches 2 and 6 gave yields of 0.384 and 0.375 with purity of 0.979–0.996, but fines near 1.
- Reaction selectivity, rather than conversion alone, limited target production. The pre-separation HPLC in batch 1 showed conversion 1.00 but selectivity 0.469 and yield 0.463. Batches 2–4 likewise had near-complete conversion but only about 0.40–0.45 selectivity.
- Large, low-fines particles can coexist with very little seed-excluded product. Batches 7–12 directly showed particle quality near 1 and fines near zero after extended aging or reheating, while final crystal yield was only 0.000008–0.017.
- A simple monotonic claim that more seed suppresses fines was contradicted. Batch 2 used 0.20 g seed yet had fines 1.00; batch 3 used no seed and had fines 0.995; batch 5 used 0.01 g and had fines 1.00. These batches were not otherwise identical, so they contradict the simple rule but do not isolate the seed-dose response.

Supported as an interpretation, but not directly demonstrated:

- Preferential dissolution/Ostwald ripening is the leading explanation for the transition from high recovery with fines to large, clean particles with low recovery. Batches 7–12 support the associated outcome pattern, but dissolved target concentration and solid mass were not tracked during the transition. Chemical degradation, phase-selection effects or physical loss could also contribute.
- C1 may be slightly better than C0 in S2. At 335 K, batch 2 with C1 had selectivity 0.452 versus 0.421 in batch 3 with C0, while final recoveries were 0.384 and 0.378. Different seed histories prevent a strong catalyst conclusion.
- S2 may be preferable to S1 for recovery. Batch 4 with S1/C1 recovered 0.347 versus roughly 0.38 for several S2/C1 batches, but batch 4 also contained a reheat/recool cycle.

Contradicted or substantially revised:

- The initial expectation that slow cooling plus greater seed loading would jointly preserve recovery and eliminate fines was contradicted by batches 2–6.
- The later expectation that warm aging would improve particle quality without a major recovery penalty was contradicted by batches 7–12. Warm or prolonged aging improved size and fines but usually left predominantly seed-derived solids.
- A simple smooth dependence on aging time or nominal temperature is not supported. Batch 1 retained high recovery after a nominally related cooling/aging history, whereas batches 7 and 8 did not. Actual temperature trajectories, controller configuration and analytical interruptions differed, leaving a reproducibility problem.

Still untested:

- Polymorph changes, aggregation/breakage, seed-size distribution, and transient supersaturation were not measured directly.
- No experiment cleanly separated dissolution from chemical degradation or filtration loss.
- The six held-out paired comparisons remain predictions only: no truth was supplied. In particular, the proposed effects of S1 versus S3, low versus high seed in S0, gradual versus crash cooling, a 315 K excursion, continued growth at 292 K, and doubled reagent loading are untested.

2. One additional experiment

I would repeat the S2/C1 process with the reaction and initial crystallization fixed, then instrument the suspected transition:

- Use the batch-1 reaction conditions, 0.05 g seed and controlled cooling to 275 K.
- Establish a tightly controlled 298 K aging stage rather than an uncontrolled wait.
- At the start of aging and after approximately 15, 60 and 120 minutes, measure particle size and obtain small liquid-phase HPLC samples.
- Record actual temperature continuously, then filter and perform the final assay.

This single time-course experiment would distinguish several explanations:

- Preferential dissolution/ripening: fines should fall and size should rise while dissolved target increases and final seed-excluded solid recovery decreases; purity should remain high without a corresponding increase in degradation products.
- Chemical degradation: target recovery should fall without a matching rise in dissolved target, while byproduct or degradation signals increase.
- Filtration or phase-accounting loss: in-vessel target and particle properties should remain stable, with the apparent loss emerging only after filtration/final assay.
- Controller-history sensitivity: a tightly controlled temperature trace should make the outcome reproducible; failure to reproduce would implicate another uncontrolled variable.

The most informative result would be an early interval where fines cross below 0.50 before crystal yield falls below 0.10. If fines decline only after dissolved target rises sharply, the quality/recovery tradeoff is genuinely mechanistic rather than merely operational.

3. Least effectively used observation and least reliable prediction

The actual temperature trajectories during nominal “wait” or aging operations were used least effectively. For example, batch 1 ended its wait near 298 K, batch 7 near 299 K, and batch 8 reached about 303 K after a shorter wait. I grouped these as related warm-aging histories, but a few kelvin may be decisive near a steep solubility boundary. The controller state and realized trajectory should have been treated as primary explanatory variables rather than secondary procedural details.

Q09 is the least reliable held-out prediction. It assumes that after only 60 seconds of cooling to 292 K the isolated particles would be mainly the added seed, giving near-zero seed-excluded recovery, large size and very low fines. No campaign experiment probed such a short crystallization interval, and the onset of nucleation can be threshold-like. If supersaturation and nucleation develop within seconds, Q09 could instead produce appreciable fine product; if 292 K remains undersaturated, the seed-only interpretation would be correct. Its particle presence is secure because seed is added, but its yield, fines and quality classification are therefore especially uncertain.
