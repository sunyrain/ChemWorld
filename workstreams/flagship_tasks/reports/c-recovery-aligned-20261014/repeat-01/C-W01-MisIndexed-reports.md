# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome
The fixed recommendation is **batch 10**: 0.040 mol reagent in 0.080 L solvent-S2 with 0.005 mol catalyst-C0 under nitrogen, controlled toward 350 K for 3,600 s, seeded with 0.050 g, cooled to 250 K over 14,400 s, and filtered. Its final assay gave seed-excluded crystal recovery **0.483**, purity **0.979**, fines number fraction **0.285**, size index **0.080**, and CSD-quality index **0.712**. It therefore met both constraints with substantial margins.

### Material effects
**Catalyst:** In the controlled S2/350 K screen, C0, C1, and C3 had similar feasible recovery: batch 2 (C0) gave 0.416, batch 1 (C1) 0.411, and batch 4 (C3) 0.417. These differences are smaller than, or comparable to, assay uncertainty, so their recovery ranking is unresolved. C0 nevertheless gave the best overall particle balance in that screen: fines 0.394 and size 0.110 in batch 2, compared with 0.423/0.076 for C1 and 0.425/0.080 for C3. C2 was clearly poorer: batch 3 recovered only 0.323, versus about 0.41–0.42 for the other catalysts. Thus I revised the initial C1 activity-based lead to C0, while treating the small C0/C1/C3 differences cautiously.

**Solvent:** Solvent identity affected both reaction performance and crystallization. With C0 and the baseline thermal history, S0 gave the highest reaction yield and recovery—0.616 and 0.450 in batch 5—but an unacceptable fines fraction of 0.872. S1 and S3 also failed the fines constraint, at 0.689 in batch 6 and 0.801 in batch 7, with recoveries of 0.375 and 0.329. S2 was the only baseline solvent yielding a clearly feasible CSD: batch 2 had recovery 0.416, purity 0.983, and fines 0.394.

This agrees directionally with the nominal dossier: S2 had relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. I interpret S2 as promoting deposition on existing surfaces rather than prolific secondary nucleation. S0 appears favorable for reaction selectivity but unfavorable for particle-number control. The long/deep S0 experiment confirmed this conflict: batch 12 reached the campaign’s highest recovery, 0.526, and purity 0.987, but fines remained 0.685 and therefore disqualified it.

### Reaction–crystallization coupling
A useful decomposition is

**Y_crystal = Y_reaction × η_capture**,

where Y_crystal is seed-excluded solid target divided by initial reagent, Y_reaction is the upstream target-product yield, and η_capture is the fraction of produced target recovered as crystals. This is an interpretive bookkeeping relation rather than a separately measured kinetic law.

For batch 2, η_capture was approximately 0.416/0.537 ≈ 0.77. Deep-cooled batches 9 and 10 had approximate capture fractions of 0.482/0.540 ≈ 0.89 and 0.483/0.546 ≈ 0.89. Thus the main improvement from the baseline to batch 10 came from recovering more of the already-formed target, not from a large increase in reaction yield.

Solvent effects show why reaction yield alone is insufficient. Batch 12 had reaction yield 0.589 and crystal recovery 0.526, but its excessive nucleation/fines made it infeasible. Batch 10 had somewhat lower reaction yield but converted the product into a constraint-compliant crystal population. Purity stayed high for S2, consistent with its low nominal impurity-occlusion tendency.

The reaction history may also change the downstream supersaturation path through target concentration and impurity composition. At a 330 K reaction target, batch 8 gave reaction yield 0.507, recovery 0.418, and fines 0.643, versus 0.537, 0.416, and 0.394 for the otherwise corresponding 350 K batch 2. The reduced degradation signal at 330 K did not translate into a better crystallization. Because there was only one batch at each temperature, it remains unclear whether this fines increase arose from reaction-mixture composition, the thermal trajectory, or run-to-run variability.

### Process-history dependence
The qualitative crystallization relations I used are

**S = C/C*(T, solvent)**,

**J ∝ k_n(S−1)^m** and **G ∝ k_g(S−1)^g**,

where S is supersaturation, J is nucleation rate, and G is growth rate. Cooling lowers equilibrium solubility C*, but rapid generation of high supersaturation can favor many small particles. Seed surface area can consume supersaturation through growth, while extended aging permits further growth and possibly dissolution/redeposition of fines.

The data show a strong endpoint effect. Changing C0/S2 cooling from 278 K in batch 2 to 250 K in batch 9 increased recovery from 0.416 to 0.482, while purity remained high and fines remained feasible at 0.450. This is consistent with lower terminal solubility increasing capture.

Duration strongly affected particle quality. At 250 K, extending cooling/growth from 7,200 s in batch 9 to 14,400 s in batch 10 changed recovery only from 0.482 to 0.483—no meaningful recovery difference—but reduced fines from 0.450 to 0.285 and improved size from 0.059 to 0.080. This large fines change is well beyond the stated measurement noise and supports a genuine growth/aging effect.

Seed dose revealed an unresolved quality/recovery tradeoff. Lowering seed from 0.050 g in batch 10 to 0.010 g in batch 11 produced numerically better particle quality: fines fell from 0.285 to 0.264, size rose from 0.080 to 0.085, CSD quality rose from 0.712 to 0.742, and purity rose from 0.979 to 0.993. However, observed recovery fell from 0.483 to 0.474. The recovery difference of 0.009 is smaller than the approximate combined uncertainty of two assays, so a real recovery penalty is not established. Batch 10 remains the fixed recommendation because it had the highest observed feasible recovery, whereas batch 11 is a plausible quality-focused alternative requiring replication.

### Revisions and uncertainty
The initial hypothesis favored C1/S2 from nominal material properties. S2 was supported, but the catalyst screen shifted the working choice to C0; C2 was rejected, while the small C0/C1/C3 ordering remains uncertain. The prediction that deeper cooling would improve recovery was supported. The anticipated risk of greater nucleation appeared in batch 9’s fines of 0.450, but extending the growth history in batch 10 reduced those fines without sacrificing recovery. Lower seed improved observed CSD quality in batch 11, but its recovery effect remains unresolved.

All comparisons are based on single batches, with final-assay standard deviations of roughly 0.010 for crystal recovery and purity, 0.018 for fines/CSD quality, and 0.025 for size. Consequently, the large solvent effects, the C2 deficit, the deep-cooling recovery gain, and the long-aging fines reduction are persuasive; small catalyst rankings and the batch-10 versus batch-11 recovery difference are not. The selected process is the best observed feasible condition, not proof of a global optimum.

Untested alternatives include S0/S2 mixtures, staged solvent addition, temperature cycling or controlled fines dissolution, seed-size-distribution control, agitation optimization, washing, solvent-volume changes, and replicated response-surface studies around the batch-10 history. These might reconcile S0’s reaction advantage with S2-like CSD control, but no experimental evidence here establishes that outcome.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.31 | 0.18 | 0.46 |
| Q01 | crystal_purity | 0.985 | 0.94 | 1 |
| Q01 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q01 | crystal_yield | 0.37 | 0.29 | 0.45 |
| Q02 | crystal_fines_fraction | 0.43 | 0.28 | 0.6 |
| Q02 | crystal_purity | 0.973 | 0.91 | 1 |
| Q02 | crystal_size | 0.15 | 0.07 | 0.25 |
| Q02 | crystal_yield | 0.33 | 0.24 | 0.42 |
| Q03 | crystal_fines_fraction | 0.2 | 0.1 | 0.31 |
| Q03 | crystal_purity | 0.978 | 0.93 | 1 |
| Q03 | crystal_size | 0.27 | 0.16 | 0.38 |
| Q03 | crystal_yield | 0.46 | 0.38 | 0.53 |
| Q04 | crystal_fines_fraction | 0.29 | 0.18 | 0.42 |
| Q04 | crystal_purity | 0.972 | 0.92 | 1 |
| Q04 | crystal_size | 0.105 | 0.06 | 0.16 |
| Q04 | crystal_yield | 0.45 | 0.37 | 0.52 |
| Q05 | crystal_fines_fraction | 0.27 | 0.16 | 0.4 |
| Q05 | crystal_purity | 0.975 | 0.93 | 1 |
| Q05 | crystal_size | 0.12 | 0.07 | 0.18 |
| Q05 | crystal_yield | 0.46 | 0.38 | 0.54 |
| Q06 | crystal_fines_fraction | 0.6 | 0.44 | 0.76 |
| Q06 | crystal_purity | 0.961 | 0.9 | 1 |
| Q06 | crystal_size | 0.075 | 0.04 | 0.12 |
| Q06 | crystal_yield | 0.47 | 0.39 | 0.55 |
| Q07 | crystal_fines_fraction | 0.24 | 0.13 | 0.36 |
| Q07 | crystal_purity | 0.977 | 0.93 | 1 |
| Q07 | crystal_size | 0.135 | 0.08 | 0.2 |
| Q07 | crystal_yield | 0.47 | 0.39 | 0.54 |
| Q08 | crystal_fines_fraction | 0.16 | 0.07 | 0.28 |
| Q08 | crystal_purity | 0.987 | 0.95 | 1 |
| Q08 | crystal_size | 0.17 | 0.1 | 0.25 |
| Q08 | crystal_yield | 0.42 | 0.34 | 0.49 |
| Q09 | crystal_fines_fraction | 0.73 | 0.55 | 0.9 |
| Q09 | crystal_purity | 0.98 | 0.92 | 1 |
| Q09 | crystal_size | 0.05 | 0.025 | 0.08 |
| Q09 | crystal_yield | 0.05 | 0.005 | 0.12 |
| Q10 | crystal_fines_fraction | 0.54 | 0.38 | 0.7 |
| Q10 | crystal_purity | 0.974 | 0.91 | 1 |
| Q10 | crystal_size | 0.075 | 0.04 | 0.12 |
| Q10 | crystal_yield | 0.25 | 0.15 | 0.36 |
| Q11 | crystal_fines_fraction | 0.26 | 0.15 | 0.39 |
| Q11 | crystal_purity | 0.976 | 0.93 | 1 |
| Q11 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q11 | crystal_yield | 0.46 | 0.38 | 0.54 |
| Q12 | crystal_fines_fraction | 0.43 | 0.27 | 0.6 |
| Q12 | crystal_purity | 0.955 | 0.89 | 0.995 |
| Q12 | crystal_size | 0.185 | 0.1 | 0.28 |
| Q12 | crystal_yield | 0.53 | 0.43 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The solvent comparison follows the campaign’s fixed-world evidence: S1 previously outperformed S3 in recovery, purity, and fines, although the very slow staged cooling should make both substantially better than their earlier rapid-cooling batches. In the seed pair, lower seed loading is expected to produce fewer, larger particles and fewer fines, with little change in seed-excluded equilibrium recovery; the magnitude is uncertain because the earlier 0.01-versus-0.05 g comparison was not replicated. For cooling history, a slow ramp should suppress primary/secondary nucleation, whereas the near-instant drop in Q06 should create persistent fines even after a long hold; endpoint recovery should be similar. The heat cycle in Q08 should selectively dissolve small crystals and improve size, purity, and fines relative to Q07, but incomplete recovery during the short recooling step may lower yield. Q09 should contain seed particles but little seed-excluded product after only 60 seconds; continued growth in Q10 raises recovery and size, though it may not reduce fines below 0.50. Doubling upstream reagent loading in Q12 should raise supersaturation and recovery relative to Q11, while worsening occlusion and fines despite producing larger crystals. Intervals are deliberately broad because these recipes extrapolate far beyond the tested durations, concentrations, and thermal histories; paired directions are more certain than absolute values, and Q02 and Q12 are especially close to the fines feasibility boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Solvent-S2 was the most reliable route to constraint-compliant particles.** Under the baseline history, batch 2 (C0/S2) gave crystal yield 0.416, purity 0.983, and fines 0.394. Corresponding C0 batches with S0, S1, and S3 had fines of 0.872, 0.689, and 0.801 (batches 5–7). The observation is direct; attributing it to S2’s lower nucleation and impurity-occlusion tendencies is mechanistic interpretation.
- **Solvent-S0 offered a recovery advantage but a severe CSD penalty.** Batch 5 had higher reaction yield and crystal recovery than baseline S2 but failed the fines constraint. Even after long, deep cooling and reduced seed, batch 12 achieved the highest recovery, 0.526, yet still had fines of 0.685. This directly supports a quality/recovery conflict for the tested S0 conditions.
- **Catalyst-C2 was inferior in the tested S2 screen.** Batch 3 recovered 0.323, versus 0.411–0.417 for C1, C0, and C3 in batches 1, 2, and 4. The much smaller differences among C0, C1, and C3 remain unresolved.
- **Cooling to 250 K improved overall recovery.** Batch 9 differed from batch 2 principally in its lower crystallization endpoint and recovered 0.482 versus 0.416, while remaining feasible. Interpreting this as reduced terminal solubility and increased capture is reasonable but not directly measured.
- **Longer aging strongly improved particle quality at 250 K.** Extending cooling from 7,200 s in batch 9 to 14,400 s in batch 10 changed recovery negligibly, 0.482 to 0.483, but reduced fines from 0.450 to 0.285 and increased size from 0.059 to 0.080. The numerical effect is direct and substantially exceeds stated fines uncertainty. Growth or ripening is an interpretation.

### Contradicted or revised
- **The initial C1 activity-based lead was not supported as uniquely best.** Batch 1 did not outperform batch 2’s C0 process. C0 became the practical lead, although the catalyst ranking among C0, C1, and C3 is not statistically settled.
- **Nominal solvent properties alone did not correctly rank every solvent.** Despite S3’s nominally more favorable growth, nucleation, and occlusion properties than S1, batch 7 was worse than batch 6 in both recovery and fines. Fixed-world residuals or reaction–crystallization coupling therefore mattered.
- **Lower reaction temperature was not uniformly beneficial.** Batch 8 at 330 K had a lower degradation warning than batch 2 at 350 K, but its fines rose to 0.643 and its recovery did not improve. This contradicts any simple account in which suppressing degradation necessarily improves the final crystals.

### Still unresolved or untested
- The seed-dose effect is unresolved: batch 11 at 0.010 g seed had better observed fines, size, CSD quality, and purity than batch 10 at 0.050 g, but recovery was 0.009 lower—within approximate combined recovery uncertainty.
- The proposed nucleation, growth, and Ostwald-ripening mechanisms were not measured directly. No supersaturation, dissolved-target concentration, nucleation rate, or time-resolved size distribution was obtained.
- The approximate decomposition `crystal yield = reaction yield × capture fraction` is useful bookkeeping, not a validated kinetic law.
- Solvent mixtures, seed-size distributions, agitation effects, washing, temperature cycling, and concentration/loading effects were not tested in the campaign.

## 2. Best single additional experiment

I would repeat the batch-10 C0/S2 process in one vessel but add non-destructive particle-size measurements after 7,200 s and 14,400 s at 250 K, together with minimal mother-liquor HPLC samples at those times, followed by the normal filtration and final assay.

This would distinguish three explanations for the batch-9/batch-10 difference:

1. **Growth/ripening at nearly constant recovery:** d50 should increase and fines should fall between measurements, while mother-liquor target concentration changes little. Final crystal yield should remain near the batch-9/batch-10 plateau.
2. **Continuing precipitation rather than primarily ripening:** fines and d50 may improve, but dissolved target should also fall materially and final recovery should rise with time.
3. **Between-batch or assay variation:** the within-vessel particle measurements would show little systematic change, making the batch-9/batch-10 fines contrast less mechanistically persuasive.

A repeat near batch 10 also tests reproducibility at the recommended operating point without changing the sealed recommendation.

## 3. Underused observation and least reliable prediction

The account used the **pre-filtration particle-size measurements** least effectively. For example, batch 1’s in-situ measurement gave fines about 0.447 and size about 0.063, while its final assay reported 0.423 and 0.076. I relied mainly on final-assay values and did not systematically use these paired readings to separate true process evolution, filtration effects, and instrument disagreement. That limited the strength of the growth/ripening interpretation.

The least reliable held-out prediction is **Q12**, the doubled-reagent upstream-loading case. The campaign did not vary reagent concentration or catalyst-to-reagent ratio, whereas Q12 simultaneously doubles concentration, halves catalyst equivalents and seed mass per mole of reagent, and then applies a much longer staged cooling history than any campaign batch. Those changes have opposing possible effects on conversion, supersaturation, crystal growth, impurity occlusion, and secondary nucleation. Its predicted fines value was also close enough to the 0.50 boundary that the sealed feasibility classification is particularly fragile. Q09 is also uncertain because it extrapolates to only 60 seconds of growth, but Q12 depends on more untested coupled effects.
