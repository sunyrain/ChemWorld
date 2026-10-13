# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign supports a coupled reaction–crystallization picture in which the reaction establishes the amount and impurity environment of dissolved target, while solvent identity and subsequent thermal history govern supersaturation, nucleation, growth, and recovery. The reported crystal_yield is specifically seed-excluded recovered target divided by target present before separation; it is therefore a crystallization-stage recovery, not an overall yield from the original reagent charge.

Reaction stage

The selected reaction conditions used solvent-S1, catalyst-C0, 0.040 mol reagent, 0.005 mol catalyst, nitrogen, and 350 K for 3,600 s at 500 rpm. In the later S1/C0 series, conversion remained approximately 0.986–1.000, selectivity approximately 0.49–0.55, and reaction yield approximately 0.50–0.54. Thus, changes in crystal recovery across batches 5–10 are unlikely to arise primarily from large conversion changes. Nevertheless, reaction composition still couples to crystallization: target concentration controls the available crystallizable mass, while byproducts and degradation products can change target solubility, inhibit growth, promote heterogeneous nucleation, or become incorporated into crystals.

Catalyst effects were not isolated cleanly. Batches 1–4 changed catalyst together with crystallization history, and only C0 was used throughout the systematic S1 temperature series. For example, batch 1 with S0/C0 showed conversion 1.00 and selectivity about 0.57, whereas batches 2–4 with C1–C3 had lower selectivities, but their thermal and seeding histories also differed. It is therefore reasonable to interpret C0 as an empirically reliable catalyst under the selected conditions, but not to claim that it is intrinsically optimal across every solvent and temperature.

Crystallization mechanism and material effects

A useful organizing variable is supersaturation,

S(t) = C(t) / C*(T(t), solvent, impurity composition),

where C* is the equilibrium solubility. Cooling lowers C* and raises S. Crystal growth may be represented qualitatively as G proportional to (S−1)^g, while primary nucleation commonly rises much more sharply, for example J proportional to exp[−A/(ln S)^2]. Consequently, rapid or excessive supersaturation can create many new particles and a high number fraction of fines, whereas controlled cooling and adequate existing crystal surface can direct solute toward growth.

The strongest empirical material association was with solvent. All S0 batches failed the fines constraint: batch 1 had recovery 0.417, purity 0.980, and fines 0.899; batches 2–4 had fines approximately 0.803–0.963. By contrast, every S1/C0 batch from 5 through 12 met fines <=0.50, with purity above 0.97. This suggests that S1 provides a more favorable combination of solubility curve, interfacial energy, crystal habit, and growth-to-nucleation kinetics. However, the solvent comparison was not a perfectly controlled substitution: batch 1 and batches 5–12 also differed in seed dose, cooling rate, endpoint, and hold. An identical-history S0/S1 comparison remains untested, so “S1 causes the improvement” is a well-supported interpretation rather than a uniquely proven mechanism.

Process-history dependence

Seeding showed a non-monotonic practical effect. The initial expectation was that more seed surface would consume supersaturation and suppress nucleation. Batch 3 revised that view: ten additions totaling 0.50 g produced recovery only 0.196 and fines 0.963. Because fines are number-weighted, introducing many small seed particles can itself raise the counted fine population, while excessive seed surface can divide deposited mass among too many particles. At 250 K in S1, increasing seed from 0.005 g in batch 10 to 0.020 g in batch 11 did not improve recovery: it changed recovery from 0.501 to 0.492. Thus 0.005 g was retained as the preferred tested dose. Whether an even smaller dose or no seed would improve the S1 process was not tested.

The cooling trajectory and hold were also important. Batches 5–10 used 0.005 g seed, a 14,400 s cooling period, and a further 14,400 s hold at 100 rpm. Lowering the endpoint produced an approximately monotonic recovery progression:

• Batch 5, 300 K: recovery 0.379, purity 0.973, fines 0.454.
• Batch 6, 290 K: recovery 0.424, purity 0.996, fines 0.461.
• Batch 7, 280 K: recovery 0.455, purity 0.976, fines 0.427.
• Batch 8, 270 K: recovery 0.481, purity 0.977, fines 0.424.
• Batch 9, 260 K: recovery 0.488, purity 0.980, fines 0.435.
• Batch 10, 250 K: recovery 0.501, purity 0.976, fines 0.442.

This is consistent with progressively lower terminal solubility increasing the equilibrium fraction available for recovery. Slow cooling and the low-agitation hold apparently prevented the extra supersaturation from producing a fines excursion in S1. The hold likely allowed mother-liquor target to deposit on existing particles and may also have allowed some ripening, although no time-resolved concentration or particle-population measurement directly demonstrated those mechanisms.

Revisions during the campaign

The initial S0 work suggested that warmer, slower crystallization with a small seed dose might reduce fines: batch 2 improved fines from batch 1’s 0.899 to 0.803. That interpretation was only partial and still infeasible. Batch 3 refuted the simple “more seed is better” hypothesis, and unseeded batch 4 still had fines 0.856. The major revision came with batch 5, where S1 gave fines 0.454 and recovery 0.379. Research then shifted from achieving feasibility to maximizing recovery within the S1/C0 regime. The endpoint-temperature series supported deeper cooling, and batch 10 became the highest observed qualifying recovery. Batch 12 repeated the batch-10 recipe and returned recovery 0.495, purity 0.992, and fines 0.433, corroborating performance near 0.50 recovery.

Uncertainty and unresolved tradeoffs

Final-assay noise was stated as roughly 0.01 for crystal_yield and purity and 0.018 for fines. The 0.006 recovery difference between batches 10 and 12 is therefore not persuasive evidence of a real difference; they are best viewed as replicate evidence for a process centered near 0.50 recovery. Likewise, batch 11’s 0.492 recovery does not conclusively establish a detrimental effect from 0.020 g seed. The full 300-to-250 K recovery trend is more compelling than any adjacent pair, but each endpoint except 250 K was tested only once.

No purity/recovery penalty appeared over the tested S1 temperature series: purity stayed well above 0.80 and fines stayed below 0.50 while recovery increased. However, other quality metrics fluctuated. Batch 10 had crystal CSD quality about 0.662 and normalized crystal size about 0.071, whereas batch 8 had CSD quality about 0.726 and size about 0.108. Batch 12 gave CSD quality about 0.694 and size about 0.098. These variations suggest a possible unresolved tradeoff between maximum recovery and particle-size-distribution quality, even though the formal purity and fines constraints were satisfied. A larger replicated design would be required to separate a true low-temperature effect from assay and process variability.

Other unresolved alternatives include solvent-dependent crystal polymorph or habit changes, impurity-mediated nucleation, seed-size-distribution effects, and stochastic primary nucleation. No polymorph measurement, solubility curve, mother-liquor assay, or time-resolved population balance was obtained. Longer holds, staged cooling, altered agitation, washing/resuspension, S1 catalyst screening, and a strictly matched S0/S1 comparison remain untested routes for determining whether recovery can be increased beyond approximately 0.50 without degrading particle quality.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.4 | 0.23 | 0.59 |
| Q01 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q01 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q01 | crystal_yield | 0.38 | 0.24 | 0.53 |
| Q02 | crystal_fines_fraction | 0.68 | 0.47 | 0.85 |
| Q02 | crystal_purity | 0.95 | 0.84 | 0.995 |
| Q02 | crystal_size | 0.09 | 0.035 | 0.18 |
| Q02 | crystal_yield | 0.34 | 0.18 | 0.51 |
| Q03 | crystal_fines_fraction | 0.44 | 0.25 | 0.64 |
| Q03 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q03 | crystal_size | 0.16 | 0.075 | 0.27 |
| Q03 | crystal_yield | 0.37 | 0.22 | 0.52 |
| Q04 | crystal_fines_fraction | 0.67 | 0.49 | 0.83 |
| Q04 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q04 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q04 | crystal_yield | 0.4 | 0.25 | 0.55 |
| Q05 | crystal_fines_fraction | 0.56 | 0.37 | 0.73 |
| Q05 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q05 | crystal_size | 0.12 | 0.055 | 0.22 |
| Q05 | crystal_yield | 0.4 | 0.25 | 0.55 |
| Q06 | crystal_fines_fraction | 0.78 | 0.61 | 0.91 |
| Q06 | crystal_purity | 0.95 | 0.86 | 0.995 |
| Q06 | crystal_size | 0.06 | 0.02 | 0.13 |
| Q06 | crystal_yield | 0.41 | 0.26 | 0.56 |
| Q07 | crystal_fines_fraction | 0.54 | 0.35 | 0.72 |
| Q07 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q07 | crystal_size | 0.13 | 0.06 | 0.23 |
| Q07 | crystal_yield | 0.41 | 0.26 | 0.56 |
| Q08 | crystal_fines_fraction | 0.38 | 0.2 | 0.59 |
| Q08 | crystal_purity | 0.97 | 0.9 | 0.998 |
| Q08 | crystal_size | 0.18 | 0.09 | 0.3 |
| Q08 | crystal_yield | 0.37 | 0.21 | 0.53 |
| Q09 | crystal_fines_fraction | 0.9 | 0.75 | 0.98 |
| Q09 | crystal_purity | 0.92 | 0.75 | 0.99 |
| Q09 | crystal_size | 0.025 | 0.005 | 0.07 |
| Q09 | crystal_yield | 0.05 | 0.005 | 0.14 |
| Q10 | crystal_fines_fraction | 0.78 | 0.6 | 0.91 |
| Q10 | crystal_purity | 0.95 | 0.84 | 0.995 |
| Q10 | crystal_size | 0.055 | 0.015 | 0.13 |
| Q10 | crystal_yield | 0.18 | 0.07 | 0.32 |
| Q11 | crystal_fines_fraction | 0.62 | 0.43 | 0.79 |
| Q11 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q11 | crystal_size | 0.1 | 0.045 | 0.19 |
| Q11 | crystal_yield | 0.4 | 0.25 | 0.55 |
| Q12 | crystal_fines_fraction | 0.46 | 0.28 | 0.66 |
| Q12 | crystal_purity | 0.93 | 0.82 | 0.985 |
| Q12 | crystal_size | 0.14 | 0.065 | 0.24 |
| Q12 | crystal_yield | 0.52 | 0.36 | 0.67 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and a crystallization step, so particles are expected. Q01–Q02 isolates solvent: S1 is predicted to preserve the favorable growth-to-nucleation behavior observed in the campaign, while untested S3 receives wider uncertainty and a higher expected fines fraction. Q03–Q04 tests seed loading: the smaller charge should leave fewer counted seed particles and permit larger crystals during the exceptionally slow ramp; 0.045 g is expected to increase number-weighted fines. Q05–Q06 compares gradual cooling with a temperature crash followed by an equal-duration hold: similar terminal recovery is expected, but the crash should create more fines and smaller particles. Q07–Q08 tests thermal cycling: reheating should preferentially dissolve small crystals and permit coarser regrowth, at the cost of modest recovery. Q09–Q10 tests a 292 K hold: the immediate filtration case should recover little seed-excluded product, whereas two hours permits additional deposition but likely not enough to remove the fines problem. Q11–Q12 doubles reagent concentration: greater supersaturation and more product per seed should raise fractional recovery and particle growth, though purity and fines remain uncertain because impurity trapping and secondary nucleation are plausible alternatives. Intervals are deliberately broad because catalyst C1 at 385 K, S3, multi-day staged cooling, thermal cycling, and these concentration/seed ratios were not directly studied; several feasibility intervals cross the fines threshold.

## K2

1. Status of the main claims

Supported by direct observations:

- The selected S1/C0 process is reproducible near 0.50 crystallization-stage recovery while meeting both quality constraints. Batch 10 gave crystal_yield 0.501, purity 0.976, and fines 0.442; the same recipe in batch 12 gave 0.495, 0.992, and 0.433. Their recovery difference is smaller than the stated assay noise, so they support repeatability rather than a meaningful ranking between those two runs.
- Within the S1/C0, 0.005 g-seed series, deeper cooling was associated with higher recovery without loss of feasibility: batches 5–10 progressed from 0.379 at 300 K to 0.501 at 250 K, while all purities exceeded 0.97 and fines remained about 0.42–0.46. The multi-batch monotone trend supports a terminal-solubility interpretation, although only the 250 K recipe was replicated.
- Excessive seeding was not beneficial in the tested cases. Batch 3, with 0.50 g total seed, had recovery 0.196 and fines 0.963. At 250 K, batch 11 with 0.020 g seed did not exceed batch 10 with 0.005 g seed: recoveries were 0.492 and 0.501, respectively.
- All tested S0 batches failed the fines constraint, whereas all later S1/C0 batches met it. S0 batches 1–4 had fines of roughly 0.80–0.96; S1 batches 5–12 had roughly 0.42–0.46.

Supported as interpretations, but not uniquely established:

- S1 likely changes solubility, crystal habit, or the growth-to-nucleation balance. The observations support a solvent association, but S0 and S1 were not compared under identical catalyst, seed, cooling, and hold histories.
- Slow cooling and a low-agitation hold likely directed supersaturation toward growth rather than primary nucleation. This is mechanistically consistent with the results, but the campaign did not include a matched slow-ramp versus crash-cool comparison.
- Reaction composition probably affects crystallization through target concentration and impurities. Later S1/C0 batches had similar conversion and reaction-yield estimates while crystal recovery changed with endpoint temperature, supporting a major crystallization contribution. However, no mother-liquor concentration or impurity-partition measurement directly demonstrated the coupling.

Contradicted or revised:

- The simple hypothesis that increasing seed surface should suppress fines was contradicted by batch 3 and was not rescued by batch 11. Seed number, seed size, and competition for deposited mass appear at least as important as nominal seed mass.
- The early expectation that modest changes to the S0 thermal history alone might achieve acceptable fines was not supported: batch 2 improved over batch 1 but still had fines around 0.803, and unseeded batch 4 remained around 0.856.

Still untested:

- A strictly matched S0/S1 substitution; catalyst screening within S1; unseeded or sub-0.005 g seeding in S1; staged cooling versus a single ramp; deliberate thermal cycling; agitation effects; washing or resuspension; polymorph identity; solubility curves; and time-resolved mother-liquor and particle-population behavior.
- Whether the lower CSD-quality estimate in batch 10 relative to some warmer batches represents a real recovery/particle-quality tradeoff or ordinary process and assay variability.

2. Best single additional experiment

I would repeat the complete batch-10 procedure with only solvent changed from S1 to S0: C0, identical concentrations, 350 K reaction for 3,600 s at 500 rpm, 0.005 g seed, 14,400 s cooling to 250 K, 14,400 s at 100 rpm, filtration, and final assay. I would include an intermediate HPLC measurement immediately before crystallization if the measurement allowance were part of the experiment.

This would distinguish two principal explanations:

- Solvent-specific explanation: S1 intrinsically provides a more favorable reaction composition, solubility curve, habit, or nucleation/growth balance.
- Process-history explanation: the deep, slow cooling and long hold are sufficient by themselves, and the apparent S1 advantage arose because the earlier S0 runs used different histories.

If the solvent-specific explanation is correct, the matched S0 batch should return to a high fines fraction resembling batches 1–4, possibly with changed recovery, despite using the optimized history. If process history is dominant, S0 should approach batches 10 and 12, with recovery near 0.50 and fines below 0.50. An intermediate HPLC result similar to the S1 reaction composition followed by poor S0 crystallization would localize the solvent effect mainly to crystallization; a substantially different HPLC composition would instead implicate reaction–crystallization coupling. One batch cannot fully separate reaction-solvent and crystallization-solvent effects, but it is the most informative missing control against the existing campaign.

3. Least effectively used observation and least reliable prediction

The account used the paired in-situ particle-size and final-assay observations least effectively. For example, batch 10 gave an in-situ fines estimate of 0.421 and CSD quality 0.715 before filtration, versus final values of 0.442 and 0.662. Similar paired readings existed in several batches. I treated the final assays as authoritative but did not analyze whether these differences were consistent with instrument noise, filtration-related population changes, or run-to-run measurement variability. Those pairs could have better constrained claims about filtration and the apparent CSD-quality tradeoff.

Q02 is the least reliable held-out prediction. It uses solvent-S3, which was never tested in the campaign and had no public property dossier. Its estimated solvent effect was therefore extrapolated from the S0/S1 contrast rather than grounded in S3 evidence. The unusually long staged cooling and relatively large seed charge further extend beyond the studied regime. Accordingly, both the predicted fines failure and the recovery estimate for Q02 are substantially more uncertain than predictions based on S0 or S1; no prediction truth has been used here.
