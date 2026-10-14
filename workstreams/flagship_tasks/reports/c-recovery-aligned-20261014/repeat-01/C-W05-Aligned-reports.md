# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The process is best understood as two coupled steps: formation of target product in solution, followed by selective capture of that product as crystals. For initial reagent amount \(n_0\), a useful decomposition is

\[
Y_{crystal}=\frac{n_{target,solid}}{n_0}\approx Y_{reaction}\,f_{capture},
\]

where \(Y_{reaction}\) represents target formation and \(f_{capture}\) is the fraction subsequently recovered as seed-excluded solid. Observed \(Y_{crystal}/Y_{reaction}\) ratios were roughly 0.78–0.88 in representative batches, showing that both reaction selectivity and crystallization losses mattered.

### Material effects

**Catalyst identity affected target formation and particle behavior.** In the matched S2, 330 K, 1,800 s catalyst screen, C3 gave the highest crystal recovery: batch 3 yielded 0.436, versus 0.368 for C1 (batch 2), 0.303 for C2 (batch 4), and 0.406 for C0 (batch 5). C3 also gave higher final reaction selectivity than C1 or C2. I therefore interpret C3 as the strongest target-forming catalyst under these conditions. However, its full-loading S2 batches produced excessive fines: 0.590 in batch 3 and 0.612 in batch 6. Catalyst-dependent product/impurity composition may therefore alter nucleation as well as reaction yield, although that causal pathway was not directly measured.

**Solvent controlled the recovery–particle-size balance.** S1 with C3 produced the highest recovery before loading optimization—0.532 in batch 7—but an unacceptable fines fraction of 0.987. S3/C3 gave 0.414 recovery and 0.648 fines in batch 8. C1/S1 also failed on fines at 0.659 in batch 9. S2 was consequently the best tested solvent for constraint control.

The initial nominal-property prior suggested that S1’s low nucleation tendency might suppress fines. The experiments contradicted that prediction. One possible interpretation is delayed supersaturation followed by burst nucleation during cooling; another is that the realized solvent residual or reaction composition overrode the nominal reference-panel behavior. These alternatives were not separately tested.

### Reaction–crystallization coupling

A standard crystallization description is

\[
\sigma=\frac{C-C^*}{C^*},\qquad B\sim k_B\sigma^b,\qquad G\sim k_G\sigma^g,
\]

where \(\sigma\) is supersaturation, \(B\) is nucleation rate, and \(G\) is growth rate. Fines increase when nucleation dominates growth. Reaction conditions determine both target concentration and impurity concentration, so a catalyst or solvent that improves solution yield can simultaneously create excessive supersaturation or impurity-mediated nucleation.

This coupling was clearest in the C3/S2 loading series. With otherwise closely matched reaction, seeding, and slow-cooling conditions:

- Batch 3, 0.04 mol reagent: recovery 0.436, purity 0.989, fines 0.590.
- Batch 11, 0.03 mol: recovery 0.488, purity 0.993, fines 0.529.
- Batch 12, 0.02 mol: recovery 0.520, purity 0.994, fines 0.387.

Lower loading also increased reaction selectivity, reaching 0.657 in batch 12. My interpretation is that dilution reduced competing reaction and moderated supersaturation, allowing seeded growth to outcompete secondary nucleation. This produced the best fractional recovery and the only clearly specification-compliant C3 result.

There is nevertheless a throughput tradeoff hidden by the fractional recovery objective. Approximate recovered target amounts for batches 3, 11, and 12 were 0.0175, 0.0146, and 0.0104 mol, respectively. Thus batch 12 maximized recovery relative to charged reagent and met quality constraints, but it did not maximize product moles per vessel.

### Process-history dependence

Particle quality depended on the complete thermal and seeding history, not merely final temperature:

- Batch 1 used 0.05 g seed, cooling, an intervening hold that allowed warming, and recooling. It gave 0.373 recovery and 0.531 fines.
- Batch 2 used 0.01 g seed and one 14,400 s cool to 270 K. It achieved 0.368 recovery and 0.480 fines, establishing the first feasible process.
- Reducing seed to 0.001 g and using staged cooling in batch 6 did not improve C3/S2 particles; fines were 0.612 and crystal size decreased.
- A high-seed cooling–reheat–recooling cycle was tested in batch 10 as a possible fines-dissolution strategy. It instead worsened fines to 0.819, rejecting that remedy in the tested scope.

These results suggest that additional cooling stages or thermal cycling can create fresh nucleation events rather than simply ripen existing crystals. They also show that a crystallization schedule successful with one catalyst cannot be assumed transferable to another.

### Purity and unresolved tradeoffs

Purity was generally high after filtration—approximately 0.967–1.000—so the binding quality constraint was fines rather than chemical purity. High-recovery S1 and full-loading C3/S2 conditions failed primarily because of particle number distribution. Batch 12 resolved the observed fractional recovery–fines tradeoff through dilution, but at reduced absolute throughput.

The recommended batch remains batch 12: 0.02 mol reagent, 0.08 L S2, 0.005 mol C3, reaction at 330 K for 1,800 s, 0.01 g seed, cooling to 270 K over 14,400 s, then filtration. Its final assay gave crystal recovery 0.520, purity 0.994, and fines 0.387.

### Revisions and uncertainty

The working mechanism changed with evidence. The initial plan favored C1/S2 and expected low seed loading or S1 to reduce fines. Catalyst screening shifted the reaction lead to C3; batches 6–10 rejected low-seed staged cooling, S1, S3, and high-seed thermal cycling as fines solutions. The final loading series then supported concentration reduction as the most effective control variable.

All designs were single batches without true process replicates. Instrument noise also matters: paired particle-size and final-assay fines readings differed, for example 0.573 versus 0.612 in batch 6 and 0.797 versus 0.819 in batch 10. Batch 2’s value of 0.480 is therefore close to the 0.50 boundary, whereas batch 12 has a substantially larger observed margin. Still untested are replication of batch 12, intermediate loadings between 0.02 and 0.03 mol, catalyst-loading reduction at low reagent charge, alternative seed sizes, controlled antisolvent addition, and ripening protocols without reheating. Consequently, the dilution mechanism is strongly suggested by the ordered series but is not yet independently replicated or uniquely proven.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.44 | 0.29 | 0.6 |
| Q01 | crystal_purity | 0.965 | 0.91 | 0.995 |
| Q01 | crystal_size | 0.3 | 0.18 | 0.44 |
| Q01 | crystal_yield | 0.39 | 0.27 | 0.52 |
| Q02 | crystal_fines_fraction | 0.36 | 0.23 | 0.52 |
| Q02 | crystal_purity | 0.94 | 0.86 | 0.98 |
| Q02 | crystal_size | 0.28 | 0.16 | 0.42 |
| Q02 | crystal_yield | 0.34 | 0.22 | 0.47 |
| Q03 | crystal_fines_fraction | 0.66 | 0.48 | 0.82 |
| Q03 | crystal_purity | 0.92 | 0.84 | 0.97 |
| Q03 | crystal_size | 0.17 | 0.08 | 0.3 |
| Q03 | crystal_yield | 0.25 | 0.14 | 0.38 |
| Q04 | crystal_fines_fraction | 0.45 | 0.29 | 0.62 |
| Q04 | crystal_purity | 0.94 | 0.87 | 0.98 |
| Q04 | crystal_size | 0.31 | 0.18 | 0.46 |
| Q04 | crystal_yield | 0.27 | 0.16 | 0.4 |
| Q05 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q05 | crystal_purity | 0.945 | 0.88 | 0.985 |
| Q05 | crystal_size | 0.34 | 0.21 | 0.49 |
| Q05 | crystal_yield | 0.28 | 0.17 | 0.41 |
| Q06 | crystal_fines_fraction | 0.72 | 0.56 | 0.86 |
| Q06 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q06 | crystal_size | 0.22 | 0.11 | 0.36 |
| Q06 | crystal_yield | 0.29 | 0.18 | 0.42 |
| Q07 | crystal_fines_fraction | 0.36 | 0.22 | 0.53 |
| Q07 | crystal_purity | 0.95 | 0.89 | 0.987 |
| Q07 | crystal_size | 0.37 | 0.23 | 0.53 |
| Q07 | crystal_yield | 0.29 | 0.18 | 0.42 |
| Q08 | crystal_fines_fraction | 0.65 | 0.47 | 0.81 |
| Q08 | crystal_purity | 0.94 | 0.86 | 0.982 |
| Q08 | crystal_size | 0.23 | 0.11 | 0.38 |
| Q08 | crystal_yield | 0.24 | 0.13 | 0.37 |
| Q09 | crystal_fines_fraction | 0.84 | 0.62 | 0.96 |
| Q09 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q09 | crystal_size | 0.07 | 0.025 | 0.14 |
| Q09 | crystal_yield | 0.025 | 0.003 | 0.09 |
| Q10 | crystal_fines_fraction | 0.62 | 0.43 | 0.8 |
| Q10 | crystal_purity | 0.9 | 0.8 | 0.965 |
| Q10 | crystal_size | 0.13 | 0.06 | 0.24 |
| Q10 | crystal_yield | 0.12 | 0.045 | 0.23 |
| Q11 | crystal_fines_fraction | 0.39 | 0.24 | 0.56 |
| Q11 | crystal_purity | 0.95 | 0.89 | 0.987 |
| Q11 | crystal_size | 0.34 | 0.21 | 0.5 |
| Q11 | crystal_yield | 0.28 | 0.17 | 0.41 |
| Q12 | crystal_fines_fraction | 0.6 | 0.43 | 0.76 |
| Q12 | crystal_purity | 0.92 | 0.83 | 0.975 |
| Q12 | crystal_size | 0.27 | 0.15 | 0.42 |
| Q12 | crystal_yield | 0.33 | 0.21 | 0.46 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even when seed-excluded target recovery is small. Q01–Q02: S1 is predicted to give higher recovery, while S3 gives fewer fines; the very long staged cooling makes both point predictions feasible, although Q01 remains uncertain because S1 produced many fines in the campaign. Q03–Q04: increasing seed mass should suppress secondary nucleation and increase number-weighted size, with little effect on equilibrium recovery. Q05–Q06: gradual cooling should favor growth, whereas the rapid initial drop should create persistent fines despite the subsequent cold holds. Q07–Q08: the final hold should preserve the coarse distribution, while reheating and rapid recooling may redissolve product and trigger renewed nucleation, consistent with the adverse campaign thermal-cycle result. Q09–Q10: two additional hours at 292 K should increase seed-excluded deposition and particle size, but likely not enough to make fines reliably compliant. Q11–Q12: higher loading should increase crystallization driving force and recovery in high-solubility S0, but at the cost of secondary nucleation and some impurity occlusion. Intervals are epistemic 80% ranges and are deliberately broad because these recipes extrapolate to S0, 385 K reaction conditions, multi-day cooling histories, and unreplicated pairwise effects; feasibility labels use the point estimates.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C3 was the strongest tested recovery catalyst under the matched S2 schedule.** Batch 3 gave crystal yield 0.436, compared with C1 0.368 (batch 2), C2 0.303 (batch 4), and C0 0.406 (batch 5). This supports the empirical ranking for that operating region, not a universal molecular mechanism.
- **S2 controlled fines better than the tested solvent alternatives with C3.** C3/S2 batch 3 had fines 0.590, versus 0.987 for C3/S1 (batch 7) and 0.648 for C3/S3 (batch 8). S1 produced higher recovery, 0.532, but unacceptable particles. The observation supports a solvent-dependent recovery–quality tradeoff.
- **Reduced reagent loading coincided with improved fractional recovery and particle quality.** In the closely related C3/S2 series, batches 3, 11, and 12 used 0.04, 0.03, and 0.02 mol reagent and gave crystal yields 0.436, 0.488, and 0.520, with fines 0.590, 0.529, and 0.387. Batch 12 directly met both constraints with purity 0.994.
- **Purity was rarely the binding constraint.** Final crystal purities across the campaign were generally about 0.967–1.000; failures were predominantly caused by fines.
- **A fractional-recovery/throughput tradeoff remained.** From charge times fractional yield, batches 3, 11, and 12 recovered approximately 0.0175, 0.0146, and 0.0104 mol target. Thus batch 12 optimized the specified fractional recovery and quality, not product moles per vessel.

### Contradicted or narrowed
- **The initial expectation that S1 would suppress fines was contradicted.** Batch 7 produced fines of 0.987 with C3/S1, and batch 9 produced 0.659 with C1/S1. The nominal low-nucleation prior did not describe the realized processes.
- **Lower seed mass plus staged cooling did not improve particles.** Batch 6 used 0.001 g seed and staged cooling but gave smaller crystals and fines of 0.612. This contradicted the proposed remedy, although seed amount and cooling history changed together.
- **High-seed thermal cycling did not dissolve fines beneficially.** Batch 10 gave fines of 0.819, substantially worse than the simpler C3/S2 histories. The proposed ripening mechanism was therefore contradicted for that particular cycle.
- **The batch-2 crystallization result did not transfer across catalysts.** Batch 2 was feasible at fines 0.480, but the nominally similar C3, C2, and C0 batches gave 0.590, 0.504, and 0.681. Catalyst-dependent composition or variability must be considered.

### Interpretive rather than directly demonstrated
- The explanation that dilution reduced supersaturation and secondary nucleation is consistent with batches 3/11/12, but supersaturation and nucleation rates were not measured.
- The suggestion that catalyst-dependent impurities changed nucleation is plausible because particle outcomes changed across the catalyst screen, but impurity-specific nucleation effects were not isolated.
- Delayed supersaturation followed by burst nucleation was proposed for S1, but no in-process concentration or nucleation-time data were collected.

### Still untested
- Replication of batch 12 and the repeatability of its margins.
- Intermediate reagent loadings between 0.02 and 0.03 mol.
- Independent effects of reagent concentration and catalyst-to-reagent ratio.
- Seed-size distribution, controlled antisolvent addition, and ripening without a hot recooling cycle.

## 2. One additional experiment

I would repeat the batch-12 process but reduce C3 from 0.005 to **0.0025 mol**, keeping 0.02 mol reagent, 0.08 L S2, 330 K for 1,800 s, 0.01 g seed, and the 14,400 s cool to 270 K. This preserves the 12.5 mol% catalyst-to-reagent ratio used in batch 3; batch 12 instead used 25 mol% because catalyst charge was held constant while reagent charge was reduced.

This experiment would distinguish two coupled explanations:

1. **Concentration/supersaturation mechanism:** If dilution itself drove both selectivity and particle improvement, the new batch should remain near batch 12—high fractional recovery, purity near unity, and fines clearly below 0.50—although reaction completion might be somewhat slower.
2. **Catalyst-ratio mechanism:** If batch 12’s higher reaction selectivity primarily resulted from its doubled catalyst fraction, reducing catalyst should lower reaction and crystal yield toward the full-loading C3 result. If fines nevertheless remain near 0.39, that would separate the mechanisms: concentration controls particles, while catalyst ratio controls target formation.

If both recovery and particle quality deteriorated, the successful outcome likely required an interaction between high catalyst ratio and low concentration. A large unexplained departure in either direction would also increase concern that batch 12 was not reproducible.

## 3. Least effectively used observation and least reliable prediction

The account used **batch 1’s paired particle measurements** least effectively. Before and after its warm hold, crystal size increased from about 0.057 to 0.076 while fines stayed nearly unchanged, about 0.555 to 0.553; after recooling, final fines were 0.531. I summarized batch 1 as a complicated history but did not fully exploit this internal observation: warming/holding appeared capable of growing particles without materially eliminating the fines population. That is more specific evidence than the broad statement that history mattered.

The least reliable held-out prediction is **Q12**. It extrapolated simultaneously to untested solvent S0, a 385 K reaction, twice the paired reagent loading, and a multi-day staged cooling history. No campaign batch used S0, so the balance between its nominally high solubility, high nucleation tendency, reaction activity, and impurity occlusion was unconstrained by direct evidence. The prediction that higher loading would raise fractional crystal recovery also competed with the observed C3/S2 loading trend, where lower loading improved fractional recovery. Its yield and fines estimates should therefore be regarded as especially model-dependent, with the stated interval potentially still understating structural uncertainty.
