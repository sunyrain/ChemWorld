# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Reaction stage and material effects

The reaction behaved as a fast, high-conversion catalytic transformation, but conversion alone did not determine useful target production. A useful empirical decomposition is

**reaction target yield ≈ conversion × selectivity**,  
**overall isolated target fraction ≈ reaction target yield × crystallization recovery**,

where the reported crystallization recovery is seed-excluded recovered target divided by target present before separation. It is therefore not an overall yield from the reagent charge.

Catalyst C1 at approximately 340 K for 1,800 s was a robust operating choice at full loading. Conversion was generally near unity, while selectivity remained only moderate. Raising severity did not appear beneficial: batch 1, run at 350 K for 3,600 s, had selectivity 0.502 and degradation warning 0.166, whereas batch 2 at 340 K for 1,800 s had selectivity 0.571 and degradation warning 0.068. This is observationally consistent with prolonged heating promoting byproduct formation or degradation, although time and temperature changed together, so their individual effects are unresolved.

Solvent identity affected both reaction composition and crystallization recovery. In the closely matched S1, S3, and S0 experiments (batches 7–9), recovery was respectively 0.508, 0.480, and 0.531. Batch 9 in S0 also had reaction selectivity 0.644 and reaction yield 0.652. Thus S0 was empirically the strongest recovery solvent among those matched runs, despite the nominal dossier initially suggesting that S2—with low solubility, strong growth, and low impurity occlusion—would be preferable. The likely interpretation is that solvent-specific reaction effects, hidden fixed residuals, and realized solubility dominate the nominal reference-panel ranking. A complete four-solvent comparison was not perfectly controlled because the S2 batches used different thermal histories.

### 2. Reaction–crystallization coupling

At full loading, reaction mixtures with only moderate selectivity nevertheless produced crystals of very high purity. For example, batch 9 had reaction selectivity 0.644 but crystal purity 0.983; batch 10 had selectivity 0.655 and purity 0.979. Crystallization therefore strongly rejected soluble reaction impurities. Purity was not the binding constraint in any principal full-loading experiment.

This separation benefit did not extend to particle quality. The reported normalized size is `min(d50/250 µm, 1)`. Values of roughly 0.02–0.075 correspond to number-weighted median diameters mostly below 20 µm, consistent with the measured fines fractions near one. Batch 8 gave the largest final normalized size observed, 0.0746, yet its fines fraction was still 0.987. Thus a modest increase in median size did not sufficiently remove the numerous sub-20-µm particles.

The tenfold lower-loading test, batch 6, was intended to reduce supersaturation and redirect deposition toward seed growth. Instead, conversion fell to 0.735 and crystallization recovery collapsed to 0.0209, while fines remained 0.996. This result revised the initial dilution hypothesis: lower concentration did not solve particle quality and introduced a severe recovery penalty. Because catalyst loading was also reduced, dilution and catalytic insufficiency remain confounded.

### 3. Process-history dependence

Several histories were tested to determine whether nucleation, growth, or ripening controlled the fines population:

- Batch 2 used a larger seed dose, slower cooling to 285 K, and a hold; recovery was 0.429 and fines were 1.000.
- Batch 3 included a long post-seeding hold before cooling; recovery rose numerically to 0.459, but fines remained 0.995.
- Batch 4 used two partial reheat/recool cycles to favor dissolution of small crystals and regrowth; recovery was 0.473, purity 1.000, and fines 1.000.
- Batch 5 used no seed and staged cooling; recovery was 0.468, but fines remained 1.000.
- Batch 10 increased cumulative seed from 0.05 g to about 2 g. It achieved the highest observed recovery, 0.5323, but fines were still 1.000. Its recovery was essentially tied with ordinary-seed batch 9 at 0.5312, so there is no persuasive seed-dose benefit.
- Batch 11 added thirty extended low-temperature holds. Recovery was 0.523 and fines 0.994, rejecting practical ripening as a solution over the tested duration.
- Batch 12 applied filtration followed by resuspension/redissolution in S2 and a second slow crystallization. Purity reached 1.000 and the byproduct signal fell to 0.0099, consistent with effective purification, but fines remained 1.000 and recovery was 0.525.

These results indicate strong process-history dependence for purification and modest recovery differences, but striking robustness of the undesirable particle-number distribution. Secondary nucleation or attrition may be sufficiently strong that conventional seeding, slow cooling, cycling, and aging cannot overcome it. Alternatively, the benchmark particle model may depend on an untested control such as crystallizer hydrodynamics, seed size distribution, antisolvent composition, selective fines removal, or a narrow metastable-zone trajectory.

### 4. Revisions to the working mechanism

The initial mechanism predicted that S2, seeded slow cooling, and a low-temperature hold would combine good recovery, purity, and low fines. Recovery and purity were achieved, but the fines prediction was decisively contradicted by batches 1–3.

Thermal cycling was then proposed as an Ostwald-ripening mechanism; batch 4 did not support it. Unseeded staged cooling, lower loading, massive seed escalation, and very long aging were subsequently tested and rejected in their tested ranges. Finally, true post-filtration recrystallization improved purification but not particle quality in batch 12.

The revised account is therefore that solvent and reaction severity control the amount and cleanliness of target available, while formation of a very large population of fine particles is a separate, dominant phenomenon that was insensitive to the accessible thermal and seed histories.

### 5. Uncertainty and unresolved tradeoff

No completed batch satisfied both purity ≥0.80 and fines ≤0.50. All main batches exceeded the fines limit by roughly 0.49 or more, far beyond the stated fines measurement noise of 0.018. The infeasibility conclusion is therefore much stronger than rankings among recoveries.

Recovery differences among the best S0 batches were small relative to assay noise: batch 9 gave 0.5312, batch 10 gave 0.5323, and batch 11 gave 0.5232, with recovery noise stated as 0.01. Batch 10 remains the sealed recommendation as the highest observed recovery fallback, not as evidence that its 2 g seed dose is superior. Batch 9 is operationally simpler and statistically nearly indistinguishable, but changing the recommendation is outside this report.

The central unresolved tradeoff is not purity versus recovery—both were simultaneously high—but recovery versus acceptable particle-number distribution. Untested alternatives include controlling supersaturation without lowering catalyst loading, changing agitation geometry rather than only speed, using characterized coarse seeds, selectively removing or dissolving fines, or employing a different solvent mixture/antisolvent trajectory. None can be claimed effective from the completed evidence.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.32 | 0.14 | 0.58 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.18 | 0.08 | 0.3 |
| Q01 | crystal_yield | 0.31 | 0.17 | 0.45 |
| Q02 | crystal_fines_fraction | 0.55 | 0.3 | 0.81 |
| Q02 | crystal_purity | 0.965 | 0.91 | 1 |
| Q02 | crystal_size | 0.12 | 0.04 | 0.24 |
| Q02 | crystal_yield | 0.23 | 0.1 | 0.38 |
| Q03 | crystal_fines_fraction | 0.59 | 0.33 | 0.84 |
| Q03 | crystal_purity | 0.97 | 0.92 | 1 |
| Q03 | crystal_size | 0.15 | 0.05 | 0.28 |
| Q03 | crystal_yield | 0.28 | 0.14 | 0.43 |
| Q04 | crystal_fines_fraction | 0.38 | 0.17 | 0.66 |
| Q04 | crystal_purity | 0.975 | 0.93 | 1 |
| Q04 | crystal_size | 0.19 | 0.08 | 0.32 |
| Q04 | crystal_yield | 0.3 | 0.16 | 0.45 |
| Q05 | crystal_fines_fraction | 0.34 | 0.14 | 0.61 |
| Q05 | crystal_purity | 0.977 | 0.93 | 1 |
| Q05 | crystal_size | 0.2 | 0.09 | 0.34 |
| Q05 | crystal_yield | 0.3 | 0.16 | 0.45 |
| Q06 | crystal_fines_fraction | 0.82 | 0.59 | 0.98 |
| Q06 | crystal_purity | 0.965 | 0.9 | 1 |
| Q06 | crystal_size | 0.07 | 0.015 | 0.17 |
| Q06 | crystal_yield | 0.36 | 0.21 | 0.51 |
| Q07 | crystal_fines_fraction | 0.32 | 0.13 | 0.59 |
| Q07 | crystal_purity | 0.978 | 0.93 | 1 |
| Q07 | crystal_size | 0.21 | 0.09 | 0.35 |
| Q07 | crystal_yield | 0.31 | 0.17 | 0.46 |
| Q08 | crystal_fines_fraction | 0.76 | 0.48 | 0.96 |
| Q08 | crystal_purity | 0.98 | 0.93 | 1 |
| Q08 | crystal_size | 0.08 | 0.02 | 0.2 |
| Q08 | crystal_yield | 0.18 | 0.06 | 0.34 |
| Q09 | crystal_fines_fraction | 0.22 | 0.04 | 0.55 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.16 | 0.06 | 0.3 |
| Q09 | crystal_yield | 0.006 | 0 | 0.035 |
| Q10 | crystal_fines_fraction | 0.18 | 0.03 | 0.48 |
| Q10 | crystal_purity | 0.987 | 0.94 | 1 |
| Q10 | crystal_size | 0.18 | 0.07 | 0.32 |
| Q10 | crystal_yield | 0.055 | 0.01 | 0.14 |
| Q11 | crystal_fines_fraction | 0.36 | 0.15 | 0.64 |
| Q11 | crystal_purity | 0.976 | 0.93 | 1 |
| Q11 | crystal_size | 0.19 | 0.08 | 0.33 |
| Q11 | crystal_yield | 0.3 | 0.16 | 0.45 |
| Q12 | crystal_fines_fraction | 0.66 | 0.39 | 0.89 |
| Q12 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q12 | crystal_size | 0.11 | 0.035 | 0.23 |
| Q12 | crystal_yield | 0.49 | 0.34 | 0.63 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are noise-free process predictions; the 80% intervals represent mechanistic and extrapolation uncertainty, not final-assay noise. Q01 versus Q02 favors S1 over S3 because its lower nominal solubility, lower nucleation tendency, faster growth and lower impurity occlusion should raise recovery and reduce fines. Q03 versus Q04 predicts that the larger seed charge provides more controlled growth area and suppresses secondary nucleation during the unusually slow ramp, although prior high-supersaturation experiments showed weak seed-dose sensitivity. Q05 versus Q06 expresses the main history tradeoff: slow cooling should produce larger particles and fewer fines, while the rapid crash followed by long cold aging may recover slightly more target but cannot readily erase the initially nucleated fines. Q07 versus Q08 predicts that reheating to 315 K substantially redissolves the crop and the subsequent one-hour crash recreates fines, rather than giving effective mild ripening. Q09 versus Q10 predicts very little seed-excluded recovery after only 60 seconds at 292 K and a modest increase during the two-hour hold; particles remain present because both recipes are seeded. Q11 versus Q12 predicts that doubling reagent concentration raises fractional recovery by moving farther above terminal solubility, but increases supersaturation, secondary nucleation and impurity occlusion enough to lose particle-quality feasibility. Confidence is limited because the campaign did not directly study these very slow, low-volume ramps; in particular, fines intervals straddle 0.50 for several nominally feasible cases, while the recovery ordering is more credible than the exact particle metrics.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Purity was not the binding constraint.** Full-loading batches generally produced crystal purity around 0.97–1.00. Examples include batch 7 (0.981), batch 9 (0.983), batch 10 (0.979), batch 11 (0.994), and batch 12 (1.000). Interpreting this as impurity rejection by crystallization is reasonable, although no mother-liquor mass balance directly established the rejection mechanism.
- **The fines constraint failed robustly under every tested history.** Final fines were about 0.987–1.000 in the principal batches, far above 0.50 and far beyond the stated assay noise. Independent particle-size measurements before filtration also reported fines near one. This directly supports infeasibility within the tested operating region.
- **S0/C1 was a reproducible high-recovery region.** Batches 9–11 returned recoveries of 0.531, 0.532, and 0.523. The small differences are not meaningful relative to recovery noise, so these runs support a recovery plateau near 0.52–0.53 rather than a special advantage for batch 10’s large seed dose.
- **C1 at approximately 340 K for 1,800 s was operationally robust at full loading.** Batches 2 and 7–11 generally reached near-complete conversion with acceptable purity. This directly supports feasibility, not catalyst optimality.

### Contradicted or narrowed

- **The initial S2/slow-cooling hypothesis was contradicted for particle quality.** Batches 1–5 combined S2 with several seed and thermal histories but retained fines near one.
- **Thermal cycling as practical Ostwald ripening was contradicted in the tested range.** Batch 4 used partial reheat/recool cycles without a useful fines reduction.
- **Unseeded staged cooling did not prevent fines.** Batch 5 ended with fines 1.000.
- **Simple dilution was not a solution.** Batch 6 had recovery only 0.021 and fines 0.996. However, dilution and reduced catalyst charge were confounded, so the broader claim that all low-concentration operation must fail is not established.
- **Large cumulative seed addition was ineffective under the tested S0 history.** Batch 10 used about 2 g seed but was essentially indistinguishable in recovery and fines from ordinary-seed batch 9.
- **Long cold aging did not repair an existing fine population.** Batch 11 retained fines 0.994 after thirty additional holds.
- **A second recrystallization improved chemical cleanup but not particle quality.** Batch 12 reached purity 1.000 and a very low byproduct signal, yet fines remained 1.000.

### Still untested

- Catalyst identity was never tested in a controlled catalyst-only comparison, so C1 cannot be called optimal.
- Temperature and time effects on reaction selectivity were changed together in batches 1 and 2.
- Truly continuous or very finely stepped slow cooling at low concentration was not performed in the campaign; it was only addressed in the sealed held-out predictions.
- Seed size distribution was not characterized. Seed mass therefore cannot be cleanly translated into seed number or growth area.
- Attrition versus secondary nucleation was not separated experimentally.
- Solvent mixtures, antisolvent trajectories, selective fines dissolution/removal, and altered hydrodynamic geometry remain untested.

## 2. One additional diagnostic experiment

I would run one low-concentration S0/C1 batch matching the slow-ramp regime underlying Q05: 0.004 mol reagent in 0.02 L S0, 0.00025 mol C1, the stated 385 K reaction and quench/reheat sequence, 0.04 g seed, and a slow stepped ramp from 300 to 278.15 K. I would add nondestructive particle-size measurements immediately after seeding, near 292 K, near 285 K, on reaching 278.15 K, and after a long stirred hold, followed by filtration and final assay.

This single trajectory would distinguish several explanations:

- **Intrinsically fine seed:** fines are already high immediately after seed addition and change little thereafter.
- **Secondary nucleation during cooling:** the seeded suspension initially appears coarse, followed by a sharp rise in fines over a particular temperature interval.
- **Attrition during prolonged stirring:** size is initially acceptable at 278.15 K but decreases and fines rise during the isothermal hold.
- **Successful low-supersaturation seeded growth:** size rises progressively and fines remain below 0.50 while recovery accumulates.
- **Measurement/domain mismatch:** serial in-situ measurements remain coarse, but the final slurry/cake assay reports high fines.

The experiment would be more diagnostic than another endpoint-only optimization because it would locate when the fine population appears.

## 3. Least-used observation and least-reliable prediction

The account used **batch 12’s exceptionally low byproduct signal** least effectively. After filtration and recrystallization, its byproduct signal was about 0.010, compared with roughly 0.20 in several ordinary S0 batches. I noted this as evidence of purification but did not fully analyze whether it arose from impurity rejection, removal of mother liquor, a changed analytical basis, or downstream degradation suppression. Phase-resolved assays before and after resuspension would have been needed to exploit that observation mechanistically.

The least reliable held-out prediction is **Q09**. It contains only 60 seconds of cooling to 292 K after seeding, so the predicted seed-excluded yield is near zero and the particle metrics may be dominated by the uncharacterized seed population. The campaign did not measure the seed size distribution or establish how a nearly seed-only suspension maps onto final crystal purity, size, and fines. Consequently, the sealed prediction that particles are present and quality is feasible depends more on assumptions about the seeds than on demonstrated product crystallization behavior.
