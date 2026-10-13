# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

The sealed recommendation remains batch 10, but it is explicitly a noncompliant starting point rather than a specification-meeting process.

Observed material effects

Batches 1–4 screened catalysts C0–C3 under the same S0 charge, 360 K/1 h reaction, quench, 0.05 g seeding, cooling to 270 K, and growth hold. Conversion was approximately complete in all four, but C2 was clearly inferior: batch 3 had reaction yield 0.485, selectivity 0.486, and crystal recovery 0.368. Batches 1, 2, and 4 gave similar reaction yields (0.593, 0.589, and 0.577) and recoveries (0.476, 0.472, and 0.479). Thus the evidence supports rejecting C2 in this regime, but the small recovery differences among C0, C1, and C3 are not strong evidence of a true ordering. C3 was retained because batch 4 had the largest observed recovery in that screen and provided a useful basis for downstream development.

Batches 4–7 compared solvents using C3. Relative to S0 in batch 4, S1–S3 increased byproduct/degradation signals and generally reduced reaction selectivity. S3 was especially unfavorable: batch 7 had selectivity 0.423, reaction yield 0.450, and crystal recovery 0.361. S0 therefore appeared best for the coupled reaction–crystallization process. Because each solvent changes both reaction chemistry and product solubility, these experiments do not isolate a purely kinetic reaction effect from a crystallization-solvent effect.

Reaction–crystallization coupling

A useful approximate decomposition is

overall isolated target fraction ≈ Y_rxn × R_cryst,

where Y_rxn is the target yield entering crystallization and R_cryst is the reported seed-excluded recovery of target already present before separation. For batch 10, this gives approximately 0.588 × 0.518 ≈ 0.30 of the initial limiting-reagent scale. The distinction matters: its 0.518 crystal recovery is not an overall chemical yield.

Upstream selectivity affected the amount and type of impurity presented to crystallization. Nevertheless, crystallization rejected impurities effectively in every tested case: final crystal purities were about 0.97–1.00 even when reaction selectivity was only moderate. Batch 7 illustrates both sides of the coupling: its purity remained 0.972, but poor upstream selectivity and yield limited the amount of target available and its recovery was only 0.361. Thus purity was not the binding constraint; particle-number distribution was.

Crystallization mechanism and history dependence

The working physical picture was competition between nucleation and growth under temperature-dependent supersaturation. In conventional notation,

S(t)=C(t)/C*(T(t)),
J(t)≈k_n[S(t)−1]^n,
G(t)≈k_g[S(t)−1]^g,

where J is nucleation rate and G is crystal growth rate. The final number fraction of fines depends strongly on the time integral of nucleation, whereas recovered mass depends on desupersaturation and growth. Seeding was intended to supply growth area and reduce new nucleation; slow cooling and low-agitation holds were intended to keep supersaturation modest.

The observations did not support that intended mechanism strongly enough to obtain acceptable morphology. The standard seeded process in batches 1–7 produced fines fractions of approximately 0.987–1.000. Batch 8 replaced the single cooling ramp with stages at 310, 300, 290, 280, and 270 K followed by a long hold. Recovery rose to 0.500, but fines remained 0.987. Batch 9 added a 270→300→270 K thermal cycle intended to dissolve fines and permit Ostwald ripening; recovery was 0.492 and fines were still 1.000. Therefore, within the tested temperatures and durations, neither reduced cooling rate nor one mild thermal cycle produced measurable fines control.

Increasing concentration did affect recovery. Batch 10 used 0.04 mol reagent in 0.03 L S0, rather than 0.06 L, with seeded two-stage cooling and long holds. It produced the campaign-high observed recovery of 0.518 and purity of 0.985, but its fines fraction was 1.000. This is consistent with greater supersaturation increasing crystallized mass, while also maintaining or increasing nucleation. That interpretation is plausible rather than proven, because concentration was changed together with the cooling schedule.

The process-history hypotheses were revised twice. First, slow cooling and extended growth were expected to lower fines; batches 8 and 9 contradicted that expectation. Second, late secondary nucleation was proposed, implying that stopping warm should sacrifice recovery but improve morphology. Batch 11 was filtered after cooling only to 300 K. Recovery fell to 0.465, yet fines remained 0.994, so there was no useful recovery–fines tradeoff. Finally, seed crystals themselves were considered a possible source of excessive particle counts. Batch 12 omitted seed, reached recovery 0.512 and purity 1.000, but still had fines 1.000. This argues against seed addition being the sole cause, although it does not rule out effects of seed size or quality that were not experimentally adjustable.

Uncertainty and unresolved alternatives

All recipe comparisons were single runs. Final-assay uncertainty, process variation, and differences between in-situ particle measurements and post-filtration final assays make small numerical rankings unreliable. For example, the differences among batches 1, 2, and 4 are too small to establish a catalyst ranking confidently. Some crystal-size readings also varied substantially between particle imaging and the final assay, while the fines result remained consistently extreme; consequently, the repeated fines failure is much more persuasive than small differences in reported size or recovery.

No completed batch satisfied both purity ≥0.80 and fines ≤0.50. Purity was comfortably satisfied, but fines missed the limit by roughly 0.49–0.50 in absolute fraction—far beyond ordinary assay noise. The campaign therefore did not reveal a compliant quality/recovery tradeoff: warmer stopping lowered recovery without fixing fines, whereas higher concentration improved recovery without fixing fines.

Untested alternatives include substantially different seed size distributions, much larger effective seed surface area, different mixing hardware or shear history, antisolvent addition, solvent exchange, a more aggressive partial-dissolution/ripening cycle, and independent control of reaction solvent versus crystallization solvent. These could alter the nucleation-to-growth balance, but no claim about their effectiveness follows from the completed experiments. Batch 10 remains the sealed recommendation solely because it combined the highest observed seed-excluded recovery (0.518) with high purity (0.985); its fines fraction of 1.000 must remain an explicit process limitation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.18 | 0.05 | 0.42 |
| Q01 | crystal_purity | 0.982 | 0.94 | 1 |
| Q01 | crystal_size | 0.24 | 0.1 | 0.4 |
| Q01 | crystal_yield | 0.46 | 0.3 | 0.62 |
| Q02 | crystal_fines_fraction | 0.15 | 0.03 | 0.4 |
| Q02 | crystal_purity | 0.955 | 0.88 | 0.995 |
| Q02 | crystal_size | 0.27 | 0.1 | 0.47 |
| Q02 | crystal_yield | 0.34 | 0.17 | 0.52 |
| Q03 | crystal_fines_fraction | 0.58 | 0.27 | 0.84 |
| Q03 | crystal_purity | 0.99 | 0.95 | 1 |
| Q03 | crystal_size | 0.07 | 0.025 | 0.18 |
| Q03 | crystal_yield | 0.43 | 0.24 | 0.61 |
| Q04 | crystal_fines_fraction | 0.13 | 0.025 | 0.34 |
| Q04 | crystal_purity | 0.991 | 0.96 | 1 |
| Q04 | crystal_size | 0.26 | 0.12 | 0.44 |
| Q04 | crystal_yield | 0.48 | 0.32 | 0.63 |
| Q05 | crystal_fines_fraction | 0.1 | 0.015 | 0.29 |
| Q05 | crystal_purity | 0.992 | 0.96 | 1 |
| Q05 | crystal_size | 0.29 | 0.14 | 0.48 |
| Q05 | crystal_yield | 0.5 | 0.34 | 0.65 |
| Q06 | crystal_fines_fraction | 0.78 | 0.52 | 0.96 |
| Q06 | crystal_purity | 0.981 | 0.93 | 1 |
| Q06 | crystal_size | 0.05 | 0.015 | 0.12 |
| Q06 | crystal_yield | 0.51 | 0.34 | 0.66 |
| Q07 | crystal_fines_fraction | 0.08 | 0.01 | 0.25 |
| Q07 | crystal_purity | 0.993 | 0.965 | 1 |
| Q07 | crystal_size | 0.31 | 0.15 | 0.51 |
| Q07 | crystal_yield | 0.51 | 0.35 | 0.66 |
| Q08 | crystal_fines_fraction | 0.68 | 0.38 | 0.91 |
| Q08 | crystal_purity | 0.995 | 0.965 | 1 |
| Q08 | crystal_size | 0.065 | 0.02 | 0.16 |
| Q08 | crystal_yield | 0.3 | 0.12 | 0.49 |
| Q09 | crystal_fines_fraction | 0.2 | 0.04 | 0.47 |
| Q09 | crystal_purity | 0.995 | 0.95 | 1 |
| Q09 | crystal_size | 0.1 | 0.05 | 0.2 |
| Q09 | crystal_yield | 0.05 | 0 | 0.16 |
| Q10 | crystal_fines_fraction | 0.14 | 0.025 | 0.37 |
| Q10 | crystal_purity | 0.994 | 0.955 | 1 |
| Q10 | crystal_size | 0.15 | 0.07 | 0.28 |
| Q10 | crystal_yield | 0.18 | 0.06 | 0.34 |
| Q11 | crystal_fines_fraction | 0.09 | 0.01 | 0.27 |
| Q11 | crystal_purity | 0.993 | 0.965 | 1 |
| Q11 | crystal_size | 0.3 | 0.14 | 0.5 |
| Q11 | crystal_yield | 0.51 | 0.35 | 0.66 |
| Q12 | crystal_fines_fraction | 0.58 | 0.3 | 0.82 |
| Q12 | crystal_purity | 0.98 | 0.93 | 1 |
| Q12 | crystal_size | 0.07 | 0.025 | 0.16 |
| Q12 | crystal_yield | 0.57 | 0.4 | 0.72 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even when seed-excluded recovery is small. Q01–Q02: prior solvent screening suggests S1 should recover more target and give higher purity than S3; S3 may produce fewer fines/larger particles, but this morphology inference is weak. Q03–Q04: adequate seed loading should suppress secondary nucleation; the very low seed dose in Q03 is predicted to leave many new fines despite some coarse crystals. Q05–Q06: gradual cooling should favor seeded growth, whereas the initial crash in Q06 should create a persistent fine population even after equal total aging. Q07–Q08: the added low-temperature hold should preserve growth, while heating to 315 K may dissolve much of the crop and the one-hour recool may regenerate fines with incomplete recovery. Q09–Q10: immediate filtration gives little seed-excluded recovery; two hours at 292 K permits additional growth and recovery. Q11–Q12: doubling loading should increase recovery but also supersaturation and nucleation, producing a predicted recovery–fines tradeoff. Intervals are broad because these recipes use much lower charge/catalyst levels and far longer, finer cooling schedules than the completed experiments; morphology predictions are especially uncertain, and feasibility classifications near the fines threshold should not be treated as assured.

## K2

1. Claims supported, contradicted, or untested

Supported by direct observations:
- C2 was inferior under the matched catalyst-screen conditions. Batch 3 had lower selectivity (0.486), reaction yield (0.485), and crystal recovery (0.368) than batches 1, 2, and 4. Interpreting this as a general property of C2 would exceed the evidence; it is supported only for the screened S0/360 K recipe.
- Solvent identity affected the coupled process. With C3, S3 in batch 7 gave lower selectivity (0.423), reaction yield (0.450), and crystal recovery (0.361) than S0 in batch 4. Batches 5–7 also had larger byproduct/degradation signals than batch 4. The direct observation is the outcome difference; attributing it specifically to reaction kinetics, solubility, or both remains interpretive.
- Purity was not the binding constraint. Every final crop had purity around 0.97–1.00, whereas fines remained approximately 0.987–1.00 in all 12 batches.
- Batch 10 had the largest observed recovery, 0.518, with purity 0.985 and fines 1.000. Calling increased concentration the cause is tentative because its cooling history also differed from the original baseline.
- None of the tested histories solved the morphology problem: staged slow cooling in batch 8, a 270→300→270 K cycle in batch 9, concentrated staged cooling in batch 10, warm stopping in batch 11, and omission of seed in batch 12 all retained extremely high fines.

Contradicted within the tested scope:
- The initial claim that slower staged cooling and long growth holds would adequately suppress fines was contradicted by batch 8: recovery reached 0.500, but fines remained 0.987.
- The proposed mild ripening cycle was contradicted for the specific cycle used in batch 9, which still had fines 1.000.
- The late-secondary-nucleation explanation predicted that stopping warm would improve morphology. Batch 11 stopped at 300 K but still had fines 0.994 while sacrificing recovery, so that simple explanation was contradicted.
- Seed addition as the sole source of excessive fines was contradicted by unseeded batch 12, which still had fines 1.000.

Still untested or unresolved:
- The relative merits of C0, C1, and C3 are unresolved because batches 1, 2, and 4 differed only slightly and were not replicated.
- The proposed nucleation-versus-growth equations are organizing interpretations, not fitted or directly validated laws.
- Seed size distribution and seed quality were not varied; batch 12 only tested presence versus absence of seed.
- Filtration-induced attrition, mixing/shear effects during cooling, antisolvent operation, solvent exchange, aggressive partial dissolution, and independent reaction and crystallization solvents remain untested.
- A usable recovery–fines tradeoff was not demonstrated. Warm stopping reduced recovery without fixing fines, while higher loading improved recovery without fixing fines.

2. One additional experiment

I would run one diagnostic, time-resolved S0 crystallization with non-destructive particle-size measurements at four points: immediately after adding a characterized 0.05 g seed charge at about 300 K; after a modest cool to 292 K; after reaching 278 K; and immediately after filtration, followed by the final assay. I would use the established C3/S0 reaction and otherwise low, fixed agitation so that temperature history is the main changing variable.

This single trajectory would distinguish several explanations:
- If fines are already near 1 immediately after seeding, the seed population itself is predominantly fine or the instrument classifies it that way.
- If the seed population is initially coarse but fines rise during early cooling, a supersaturation-driven nucleation burst is favored.
- If fines remain low until the final low-temperature segment, late secondary nucleation is favored despite batch 11.
- If in-situ fines remain low through cooling but rise only after filtration/final assay, filtration attrition, sampling-domain differences, or cross-instrument inconsistency becomes the leading explanation.
- If fines rise and then fall while size increases during the hold, growth or ripening is active; if both remain static, extending residence time is unlikely to help.

The experiment is diagnostic rather than another blind optimization: it locates when the unacceptable number distribution appears and therefore determines which intervention is rational next.

3. Least-effectively used observation and least-reliable prediction

The account used the paired pre-filter particle measurements and final-assay morphology least effectively. Batch 8, for example, had a pre-filter crystal-size estimate of 0.040 and a final value of 0.083, while fines changed from approximately 0.999 to 0.987. Similar cross-instrument variation occurred elsewhere. I noted this generally as uncertainty but could not determine whether it reflected filtration, different measurement contracts, process heterogeneity, or independent noise. Without time-resolved measurements or replicates, those discrepancies could not support a specific mechanism. The occasional combination of a size estimate near or above the 20 µm median threshold with an extreme fines estimate also cautions against overinterpreting either morphology channel alone.

Q08 is the least reliable held-out prediction. It extrapolates from batch 9’s mild reheat to 300 K to a substantially hotter 315 K treatment after a much longer cooling history, followed by only one hour of recooling. Whether 315 K partially dissolves, completely dissolves, ripens, or leaves the crop largely intact depends on an unmeasured solubility curve and dissolution kinetics. Its predicted recovery loss and renewed fines therefore rest on mechanistic extrapolation rather than a close experimental analogue. No prediction truth has been used, and the sealed Q08 values are unchanged.
