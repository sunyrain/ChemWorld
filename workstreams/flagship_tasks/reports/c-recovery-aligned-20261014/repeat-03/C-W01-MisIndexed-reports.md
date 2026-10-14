# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended process (unchanged): batch 8 used 0.040 mol reagent, 0.080 L solvent S2, and 0.005 mol catalyst C1. It was reacted at 340 K for 3,600 s with 400 rpm stirring, seeded with 0.020 g before cooling, cooled directly to 310 K over 14,400 s without quenching, held twice for 14,400 s at 100 rpm, filtered, terminated, and assayed. Its final measured crystal yield was 0.375, purity 0.980, and number fraction below 20 µm was 0.490.

Reaction mechanism and material effects

A useful phenomenological reaction scheme is R → P → I/D, with desired-product formation competing with impurity and degradation pathways. One representation is dR/dt = −k1(T,C,S)R and dP/dt = k1R − [k2(T,S)+kd(T,S)]P. Catalyst and solvent can affect all three rate constants, while elevated temperature or excessive residence time can increase secondary loss after conversion is nearly complete.

The observations support C1/S2 as the strongest tested reaction combination, although catalyst identity was not independently screened. In batch 2, C1/S2 at 340 K gave an HPLC conversion of 0.985, selectivity of 0.546, and liquid-phase yield of 0.517. Under broadly related 340 K conditions, C1/S1 in batch 5 gave selectivity 0.485 and yield 0.476, while C1/S3 in batch 7 gave 0.486 and 0.443. These comparisons suggest a favorable S2 effect on desired-product formation, but differing downstream histories and measurement noise prevent treating the differences as isolated solvent coefficients. Solvent S0 and catalysts C0, C2, and C3 were not tested, so their inferiority is unproven.

Batch 1 illustrates reaction severity: C1/S1 at 370 K for 7,200 s reached conversion 1.00 but only 0.383 selectivity, with byproduct signal 0.524 and liquid yield 0.377. Reducing the reaction to 340 K and 3,600 s in later batches generally improved selectivity and reduced byproduct formation. Temperature, solvent, and time changed together between batches 1 and 2, however, so the campaign supports a moderate-severity operating region rather than a separately estimated temperature effect.

Reaction–crystallization coupling

Overall crystal recovery can be viewed approximately as

Ycrystal ≈ Xreaction × Sreaction × Fcrystallized × Fretained,

where Xreaction is conversion, Sreaction is chemical selectivity, Fcrystallized is the fraction of target product transferred into solids, and Fretained accounts for filtration and other losses. The reported crystal yield is specifically seed-excluded target-product moles in the recovered solid divided by the initial reagent charge; seed mass therefore cannot directly create apparent product yield.

Crystallization is governed by supersaturation, for example σ = (c−c*)/c*, with c* depending strongly on solvent and temperature. A qualitative population-balance description is nucleation rate B = kbσ^b and linear growth rate G = kgσ^g. Rapid creation of large supersaturation can make the time integral of B dominate growth, producing many sub-20-µm particles even when bulk recovery is high. Conversely, a warm, gradual trajectory can keep σ moderate so existing particles grow rather than continually nucleating.

This coupling explains the main tradeoff. Deep-cooled S2 batches recovered more product but produced almost entirely fines: batch 2 yielded 0.444 with fines 1.000; batch 3 yielded 0.469 with fines 0.995; and unseeded batch 4 yielded 0.484 with fines 1.000. Their purities were 0.985–1.000, so chemical purity was not the limiting attribute. The likely interpretation is that S2’s favorable recovery or low effective solubility generated excessive supersaturation during quenching and deep cooling. An untested alternative is that a solvent-specific nucleation residual, rather than supersaturation alone, caused the S2 fines.

Process-history dependence and revisions

The initial hypothesis was that greater seeding plus slow, deep cooling would improve particle size. That simple hypothesis was rejected. Across S2 batches with 0, 0.005, and 0.050 g seed, final fines remained about 0.995–1.000 (batches 2–4). These batches did not provide a perfectly controlled seed-dose series, but they showed that seed dose could not overcome the chosen deep-cooling history.

Changing solvent alone also did not solve the problem. Deep-cooled S1 batch 5 had yield 0.414 and fines 1.000; S3 batch 7 had yield 0.352 and fines 0.987. A partial dissolution/ripening attempt in batch 6—cooling, reheating to 305 K, then recooling—still gave fines 1.000 and reduced yield to 0.371. Thus the working interpretation shifted from “add seed and cool deeply” to “avoid the abrupt quench and remain in a warm growth regime.” The failed reheating result does not rule out all temperature cycling; different dissolution fractions or much longer ripening times remain untested.

That revision was supported by batch 8. Direct cooling from the reaction temperature to 310 K, followed by two warm holds, reduced fines to 0.490 while retaining 0.375 recovery and 0.980 purity. Its crystal-size metric was 0.101 and CSD-quality metric 0.706, both substantially better than the deeply cooled products. The warm trajectory deliberately accepted incomplete precipitation to suppress secondary nucleation.

Warm residence time also coupled back to reaction quality because the mixture was not quenched. One 310 K hold in batch 9 gave byproduct signal 0.384, degradation warning 0.198, yield 0.366, and fines 0.504. Two holds in batch 8 gave corresponding values 0.424, 0.245, 0.375, and 0.490. Three holds in batch 10 increased byproduct signal to 0.462 and degradation warning to 0.274, while yield remained 0.367 and fines were 0.514. This suggests prolonged warm residence promotes secondary reaction, while its particle-size benefit is weak and non-monotonic at the observed resolution. Two holds are therefore a practical compromise, not a proven kinetic optimum.

A 312 K endpoint with two holds in batch 11 also met the formal constraints: yield 0.350, purity 0.993, and fines 0.496. The reduced recovery is consistent with less supersaturation at the warmer endpoint, but it did not provide a convincing fines margin. Batch 8 consequently remains the highest-recovery completed batch whose final assay satisfied both constraints.

Uncertainty and unresolved tradeoff

The main uncertainty is robustness at the fines boundary. The exact batch-8 repeat, batch 12, produced yield 0.361, purity 0.994, and fines 0.505. Batch 9, batch 10, and batch 11 also lay between approximately 0.496 and 0.514. The final-assay noise specification for fines was 0.018, comparable to these differences. Thus batch 8 is valid as the best observed feasible batch, but the evidence does not establish that its underlying process mean is safely below 0.50.

The unresolved tradeoff is therefore clear: deep cooling raises seed-excluded recovery toward 0.44–0.48 but causes grossly excessive fines, whereas warm direct cooling lowers recovery to roughly 0.35–0.38 and only narrowly controls fines. Purity remained comfortably above 0.80 throughout the leading conditions. Further work would need replicated warm-endpoint experiments, tighter control of cooling and residence time, and possibly a factorial solvent/catalyst screen. Those alternatives were not tested and do not alter the sealed recommendation of batch 8.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.36 | 0.23 | 0.51 |
| Q01 | crystal_purity | 0.93 | 0.86 | 0.98 |
| Q01 | crystal_size | 0.18 | 0.1 | 0.28 |
| Q01 | crystal_yield | 0.34 | 0.24 | 0.44 |
| Q02 | crystal_fines_fraction | 0.25 | 0.14 | 0.39 |
| Q02 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.23 | 0.14 | 0.35 |
| Q02 | crystal_yield | 0.38 | 0.28 | 0.48 |
| Q03 | crystal_fines_fraction | 0.62 | 0.45 | 0.78 |
| Q03 | crystal_purity | 0.88 | 0.78 | 0.95 |
| Q03 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q03 | crystal_yield | 0.27 | 0.18 | 0.37 |
| Q04 | crystal_fines_fraction | 0.44 | 0.28 | 0.61 |
| Q04 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q04 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q04 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q05 | crystal_fines_fraction | 0.42 | 0.27 | 0.58 |
| Q05 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q05 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q05 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q06 | crystal_fines_fraction | 0.78 | 0.62 | 0.91 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.94 |
| Q06 | crystal_size | 0.07 | 0.03 | 0.14 |
| Q06 | crystal_yield | 0.32 | 0.22 | 0.42 |
| Q07 | crystal_fines_fraction | 0.4 | 0.25 | 0.56 |
| Q07 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q07 | crystal_size | 0.18 | 0.1 | 0.29 |
| Q07 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q08 | crystal_fines_fraction | 0.3 | 0.17 | 0.47 |
| Q08 | crystal_purity | 0.94 | 0.87 | 0.98 |
| Q08 | crystal_size | 0.22 | 0.12 | 0.34 |
| Q08 | crystal_yield | 0.26 | 0.16 | 0.36 |
| Q09 | crystal_fines_fraction | 0.8 | 0.62 | 0.94 |
| Q09 | crystal_purity | 0.83 | 0.68 | 0.93 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.1 |
| Q09 | crystal_yield | 0.04 | 0.01 | 0.1 |
| Q10 | crystal_fines_fraction | 0.62 | 0.44 | 0.79 |
| Q10 | crystal_purity | 0.86 | 0.74 | 0.94 |
| Q10 | crystal_size | 0.08 | 0.03 | 0.16 |
| Q10 | crystal_yield | 0.13 | 0.06 | 0.22 |
| Q11 | crystal_fines_fraction | 0.43 | 0.27 | 0.59 |
| Q11 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q11 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q11 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q12 | crystal_fines_fraction | 0.59 | 0.42 | 0.75 |
| Q12 | crystal_purity | 0.84 | 0.72 | 0.93 |
| Q12 | crystal_size | 0.11 | 0.05 | 0.2 |
| Q12 | crystal_yield | 0.28 | 0.18 | 0.39 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are extrapolations from K1, not new experimental results. Q01–Q02: S3 is expected to outperform S1 in particle growth, impurity exclusion, and recovery because of its lower nominal solubility, nucleation tendency, and occlusion, despite S1's stronger nominal reaction activity. Q03–Q04: very low seeding leaves more supersaturation for uncontrolled secondary nucleation; heavier seeding should improve capture and reduce fines, although the estimated effect crosses the quality boundary with substantial uncertainty. Q05–Q06: staged cooling should limit the nucleation burst, whereas rapid chilling followed by equal cold residence should give similar recovery but much smaller, finer crystals and somewhat poorer purity. Q07–Q08: the 315 K cycle is interpreted as selectively dissolving fines and permitting regrowth, improving size, fines, and purity at the cost of some recovered product; the campaign's unsuccessful reheating attempt makes this comparison especially uncertain. Q09–Q10: particles are present because seeds were added, but immediate filtration allows little seed-excluded deposition; two hours at 292 K increases recovery and growth but is still predicted to miss the fines constraint. Q11–Q12: doubling reagent at fixed catalyst and solvent raises supersaturation but halves the catalyst-to-reagent ratio, so the predicted fractional recovery and purity decline while fines increase. Feasibility flags use the point estimates; several intervals, especially Q01, Q04, Q05, Q07, Q10, and Q11, span the fines threshold.

## K2

1. Status of the main claims

Supported by direct observations:
- Process history strongly controlled particle quality. Deeply cooled or quenched batches 2–7 had final fines of about 0.987–1.000, whereas the warm direct-cooling series, batches 8–12, gave about 0.490–0.514. Interpreting this as a supersaturation/nucleation effect is mechanistic inference, but the history–fines association itself is directly observed.
- High recovery and low fines traded off. Deep-cooled S2 batches 2–4 gave crystal yields of 0.444–0.484 but failed the fines constraint. Warm batches 8–12 gave lower yields of 0.350–0.375 and approached the 0.50 fines limit.
- Purity was not the binding constraint in the leading processes: batches 2–12 generally had final crystal purity around 0.97–1.00.
- Batch 8 was the highest-recovery observed feasible batch: yield 0.375, purity 0.980, and fines 0.490. This is an observed ranking, not proof that its underlying process mean is feasible.
- Feasibility was borderline. The exact batch-8 repeat, batch 12, returned yield 0.361, purity 0.994, and fines 0.505. Batch 11 was also barely feasible at 0.496 fines.

Supported only tentatively or partly:
- S2 appeared favorable for reaction and recovery. Batch 2 had better HPLC selectivity and yield than the broadly related S1 batch 5 and S3 batch 7, and S2 batches 2–4 had the highest cold-process recoveries. However, the solvent comparisons were not perfectly matched, so a causal solvent effect remains an interpretation.
- Longer warm residence appeared to increase secondary chemistry: degradation warning/byproduct signal rose broadly from one hold in batch 9 through two holds in batch 8 to three holds in batch 10. Because yield and fines were non-monotonic and the batches were noisy, this is suggestive rather than a fitted kinetic law.
- The proposed nucleation-versus-growth explanation is consistent with the large fines reduction under warm direct cooling, but supersaturation, ongoing reaction, and residence time changed together.

Contradicted or narrowed:
- The initial claim that more seed plus slow deep cooling would solve fines was contradicted in the tested regime. S2 batches 2–4 used 0.050, 0.005, and 0 g seed yet all had fines near 1.00. This does not prove seed dose is irrelevant under warm crystallization.
- A simple claim that more warm holding monotonically reduces fines was contradicted: batches 9, 8, and 10 gave fines of 0.504, 0.490, and 0.514 for one, two, and three holds.
- Partial reheating did not rescue the specific deep-cooled process in batch 6; it produced yield 0.371 and fines 1.000. Thus a general ripening benefit was not observed under that cycle.
- Raising the endpoint to 312 K did not establish a safer quality margin. Batch 11 passed only narrowly at 0.496 fines and lost recovery relative to batch 8.

Still untested:
- Catalyst effects: every completed batch used C1, so C0, C2, and C3 were not experimentally ranked.
- Solvent S0 and fully matched solvent comparisons.
- Independent effects of reaction temperature and duration; batch 1 versus batch 2 changed solvent, temperature, and time together.
- Whether continuing reaction during unquenched cooling was essential to batch 8, rather than the thermal trajectory alone.
- Whether the true mean fines value of the recommended process is below 0.50; the two nominal replicates straddled the limit.
- Alternative reheating amplitudes, seed doses in the warm route, and more sophisticated supersaturation control.

2. One additional experiment

I would repeat the batch-8 recipe with one deliberate change: after the 340 K reaction, quench the mixture to stop reaction, reheat it to 340 K, then apply the same 0.020 g seed, 14,400 s direct cooling to 310 K, two 14,400 s holds at 100 rpm, filtration, and final assay. A pre-crystallization HPLC measurement would document the locked reaction composition if permitted within the single batch.

Compared with batch 8, this distinguishes two explanations:
- Thermal-path explanation: controlled warm supersaturation is sufficient to suppress secondary nucleation.
- Coupled-reaction explanation: continuing product formation during unquenched cooling provides gradual supersaturation generation that is essential to the particle distribution.

If the thermal-path explanation dominates, the quenched/reheated batch should retain approximately batch-8 particle quality—fines near 0.49 and similar size—while showing less byproduct/degradation; yield might be slightly lower because no additional product forms during cooling. If continuing reaction is important, quenching should materially alter recovery and the size distribution: likely lower yield and either more fines from a more abrupt fixed product inventory or fewer particles if supersaturation becomes insufficient. A large particle-quality change at similar starting composition would instead indicate that quench/reheat history itself changes nucleation. One batch would not settle repeatability, but it would remove a major mechanistic confound.

3. Weakest use of evidence and least reliable prediction

The observation used least effectively was batch 6. It was the campaign’s only explicit reheating/ripening test, and it failed badly: yield 0.371 with fines 1.000. My account acknowledged that result, but the held-out predictions still assigned Q08 a substantial fines and size improvement from reheating to 315 K. Q08 differs from batch 6 because it begins with an extremely long staged cooling program, so the comparison is not direct; nevertheless, batch 6 should have caused a more conservative point estimate and wider uncertainty for any claimed thermal-cycle benefit.

Accordingly, Q08 is the least reliable held-out prediction. Its forecast depends on selective dissolution of fines followed by favorable regrowth, yet the only campaign cycle did not demonstrate that mechanism. The 315 K excursion could instead dissolve useful product, trigger renewed nucleation during rapid recooling, or change purity and recovery without improving fines. Q08 also extrapolates far beyond the campaign in total crystallization time. Q03–Q04 are another uncertain pair because seed dose was never isolated in the warm regime, but Q08 combines the strongest extrapolation with directly cautionary prior evidence.
