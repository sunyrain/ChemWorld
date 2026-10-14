# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Working process picture

The data support a two-stage description:

1. **Catalytic reaction:** limiting reagent is converted into target product and byproduct. A useful empirical relation is
   \[
   Y_{\mathrm{rxn}} \approx X\,S,
   \]
   where \(X\) is conversion and \(S\) is target selectivity; assay noise and the benchmark’s signal mapping account for imperfect equality.
2. **Crystallization and isolation:** only part of the target-product inventory becomes recovered, seed-excluded crystal product. I interpret
   \[
   Y_{\mathrm{crystal}}=Y_{\mathrm{rxn}}f_{\mathrm{recover}},
   \]
   where \(f_{\mathrm{recover}}\) summarizes supersaturation generation, growth, nucleation, solid-state/history effects, and filtration losses. It is an empirical bookkeeping factor, not a separately measured equilibrium constant.

For the successful 420–430 K batches, the apparent \(f_{\mathrm{recover}}\) was about 0.90–0.92: batch 8, 0.673/0.732 = 0.919; batch 11, 0.675/0.747 = 0.903; batch 12, 0.678/0.751 = 0.902. At 440 K it collapsed to roughly 0.010–0.012 despite high reaction yield (batches 9–10). Thus reaction optimization alone was insufficient.

### 2. Material effects

**Solvent S2.** Its nominal dossier suggested relatively low solubility, strong crystal growth, low nucleation tendency, and low impurity occlusion. The experiments were consistent with the purity part of that prior: all tested S2 processes gave final crystal purity of about 0.976–1.000. In the qualified high-temperature region, batch 8 gave purity 0.986, batch 11 gave 0.999, and batch 12 gave 1.000. This supports using S2 as a growth- and purification-favoring medium in this world, although no controlled solvent screen was completed, so superiority over S1 or S3 remains untested.

**Catalyst effects.** The early screen did not isolate catalyst identity cleanly because temperature and crystallization histories also changed. C2 at 345 K was unfavorable in batch 3 (reaction yield 0.420; crystal yield 0.337). C0 at 360 K in batch 2 and C3 at 345 K in batch 4 both produced crystal yield near 0.400. C1 ultimately supported much higher recovery after its temperature/time conditions were optimized: 0.567 in batch 6, 0.633 in batch 7, and about 0.673–0.678 in batches 8, 11, and 12. This establishes C1 as effective in the optimized region, but it does not prove a catalyst main effect independent of temperature.

### 3. Reaction temperature and time

My initial concern was that lower temperature would suppress degradation and improve selectivity. Batch 5 falsified that expectation for C1/S2: 330 K for 7200 s gave final reaction yield 0.364, selectivity 0.371, degradation warning 0.206, and crystal yield only 0.287.

Shorter, hotter reactions instead improved the measured reaction outcome:

- **Batch 6:** 380 K/1800 s; reaction yield 0.630, selectivity 0.629, degradation warning 0.131, crystal yield 0.567.
- **Batch 7:** 400 K/1200 s; reaction yield 0.699, selectivity 0.673, degradation warning 0.101, crystal yield 0.633.
- **Batch 8:** 420 K/900 s; reaction yield 0.732, selectivity 0.740, degradation warning 0.094, crystal yield 0.673.
- **Batch 11:** 430 K/750 s; reaction yield 0.747, selectivity 0.767, degradation warning 0.063, crystal yield 0.675.

One interpretation is that rapid high-temperature conversion reduces residence time in a byproduct-forming regime. An alternative is that temperature directly changes the hidden selectivity network rather than merely accelerating the desired pathway. The available measurements cannot distinguish these explanations.

### 4. Reaction–crystallization coupling and the 440 K cliff

The most important process-history effect was a sharp loss of crystallizability between the tested 430 and 440 K histories.

- **Batch 9:** 440 K/600 s, cooled to 265 K; reaction yield 0.770 but crystal yield only 0.0079. Fines were 0.0014 and size index 0.376.
- **Batch 10:** replicated 440 K/600 s but cooled to 270 K; reaction yield 0.778 but crystal yield only 0.0090. Fines were 0.011 and size index 0.390.
- **Batch 11:** returning to 430 K/750 s and cooling to 270 K restored crystal yield to 0.675.

Because batch 10 retained the loss after changing the endpoint from 265 to 270 K, simple overcooling is not a sufficient explanation. The replicated collapse indicates that the upstream 440 K history changed something important to downstream recovery.

Plausible but untested explanations include formation of a highly soluble or noncrystallizing target state, a hidden product-form or speciation change, inhibitor formation not resolved by the liquid assay, altered seed compatibility, or a kinetic history effect. The very large-particle/low-fines readings in batches 9–10 do not indicate good bulk recovery: when almost no new product crystallizes, a small population dominated by seed or sparse grown crystals can look exceptionally coarse. Thus particle quality must be interpreted jointly with seed-excluded yield.

### 5. Seeding and cooling history

The initial batch used 0.020 g seed and had crystal yield 0.416, purity 0.988, and fines 0.515, just outside specification. Later recipes used 0.005 g seed and a 14,400 s cooling period. Qualified low-seed batches commonly had fines around 0.33–0.39—for example 0.340 in batch 2, 0.331 in batch 6, 0.332 in batch 7, 0.354 in batch 8, 0.376 in batch 11, and 0.385 in batch 12.

This is consistent with fewer seed particles allowing more growth per particle and reducing the number fraction below 20 micrometres. It is not a clean causal estimate, however, because catalyst, reaction temperature, cooling endpoint, and duration also changed between batch 1 and later batches.

Batch 12 repeated the 430 K reaction but extended the 270 K crystallization history from 14,400 to 28,800 s. Relative to batch 11, its size index increased from 0.083 to 0.105, while observed crystal yield changed only from 0.675 to 0.678 and fines from 0.376 to 0.385. The yield difference is smaller than the stated final-assay crystal-yield noise (standard deviation 0.01), and the size difference is also comparable to its 0.025 noise. Therefore the extra hold may promote growth, but neither a size nor recovery benefit is established without replication.

### 6. Uncertainty and quality/recovery tradeoff

Final-assay noise standards were approximately 0.01 for crystal yield and purity, 0.018 for fines, and 0.025 for size. Consequently, batches 11 and 12 are effectively tied on recovery. Batch 12 has the highest observed qualified crystal yield, 0.678, with purity 1.000 and fines 0.385, but batch 11 reaches nearly the same recovery in less process time.

The unresolved tradeoff is therefore twofold:

- **Within the qualified 430 K region:** the longer batch-12 hold may give larger crystals, but its improvement is uncertain and costs time.
- **At 440 K:** apparent particle quality becomes excellent—very low fines and large particles—but almost all bulk crystal recovery is lost. Those quality metrics are misleading unless constrained by yield.

Overall, the evidence supports a narrow high-temperature operating window: C1/S2, 430 K for about 750 s, 0.005 g seed per 0.04 mol reagent, slow cooling to 270 K, and extended growth/isolation as used in batch 12. The upper boundary is critical: 440 K produced better liquid reaction assays but catastrophically poor crystal recovery.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.44 | 0.27 | 0.62 |
| Q01 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q01 | crystal_size | 0.09 | 0.03 | 0.18 |
| Q01 | crystal_yield | 0.5 | 0.34 | 0.65 |
| Q02 | crystal_fines_fraction | 0.58 | 0.39 | 0.76 |
| Q02 | crystal_purity | 0.89 | 0.78 | 0.97 |
| Q02 | crystal_size | 0.065 | 0.02 | 0.15 |
| Q02 | crystal_yield | 0.54 | 0.37 | 0.7 |
| Q03 | crystal_fines_fraction | 0.36 | 0.19 | 0.55 |
| Q03 | crystal_purity | 0.85 | 0.73 | 0.94 |
| Q03 | crystal_size | 0.18 | 0.08 | 0.31 |
| Q03 | crystal_yield | 0.39 | 0.24 | 0.54 |
| Q04 | crystal_fines_fraction | 0.67 | 0.49 | 0.82 |
| Q04 | crystal_purity | 0.84 | 0.72 | 0.94 |
| Q04 | crystal_size | 0.06 | 0.015 | 0.14 |
| Q04 | crystal_yield | 0.42 | 0.27 | 0.57 |
| Q05 | crystal_fines_fraction | 0.62 | 0.43 | 0.79 |
| Q05 | crystal_purity | 0.85 | 0.73 | 0.94 |
| Q05 | crystal_size | 0.075 | 0.02 | 0.16 |
| Q05 | crystal_yield | 0.42 | 0.27 | 0.57 |
| Q06 | crystal_fines_fraction | 0.76 | 0.58 | 0.89 |
| Q06 | crystal_purity | 0.82 | 0.68 | 0.93 |
| Q06 | crystal_size | 0.045 | 0.01 | 0.11 |
| Q06 | crystal_yield | 0.44 | 0.28 | 0.59 |
| Q07 | crystal_fines_fraction | 0.57 | 0.38 | 0.74 |
| Q07 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q07 | crystal_size | 0.085 | 0.025 | 0.18 |
| Q07 | crystal_yield | 0.43 | 0.28 | 0.58 |
| Q08 | crystal_fines_fraction | 0.39 | 0.21 | 0.59 |
| Q08 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q08 | crystal_size | 0.15 | 0.06 | 0.28 |
| Q08 | crystal_yield | 0.29 | 0.12 | 0.47 |
| Q09 | crystal_fines_fraction | 0.32 | 0.11 | 0.57 |
| Q09 | crystal_purity | 0.89 | 0.75 | 0.97 |
| Q09 | crystal_size | 0.18 | 0.06 | 0.36 |
| Q09 | crystal_yield | 0.015 | 0.001 | 0.06 |
| Q10 | crystal_fines_fraction | 0.19 | 0.06 | 0.4 |
| Q10 | crystal_purity | 0.87 | 0.74 | 0.96 |
| Q10 | crystal_size | 0.27 | 0.12 | 0.47 |
| Q10 | crystal_yield | 0.12 | 0.04 | 0.25 |
| Q11 | crystal_fines_fraction | 0.64 | 0.45 | 0.8 |
| Q11 | crystal_purity | 0.85 | 0.73 | 0.94 |
| Q11 | crystal_size | 0.07 | 0.02 | 0.16 |
| Q11 | crystal_yield | 0.42 | 0.27 | 0.57 |
| Q12 | crystal_fines_fraction | 0.52 | 0.33 | 0.71 |
| Q12 | crystal_purity | 0.82 | 0.68 | 0.92 |
| Q12 | crystal_size | 0.11 | 0.035 | 0.23 |
| Q12 | crystal_yield | 0.36 | 0.21 | 0.52 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when little seed-excluded product crystallizes. For the solvent pair, S1 is predicted to give cleaner, coarser material and fewer fines than S3 because its nominal occlusion and nucleation tendencies are lower; S3's greater reaction activity gives slightly higher recovery. In the seed pair, low seed should reduce particle-number density and fines while increasing size, whereas high seed modestly improves capture but fails the fines constraint. Slow staged cooling is expected to suppress burst nucleation relative to an immediate crash to 278.15 K; the crash may recover slightly more product but with smaller, finer crystals. The 315 K reheat is predicted to dissolve preferentially small/impure material and improve size, purity, and fines at the expense of recovery. Continuing growth at 292 K should substantially increase seed-excluded yield and coarsen the population relative to the 60-second endpoint. Doubling reagent at fixed catalyst and seed raises supersaturation and growth per seed, but likely lowers fractional reaction conversion and purity while leaving fines near the feasibility boundary. Intervals are deliberately broad because these recipes extrapolate from the sealed campaign in solvent, concentration, catalyst ratio, seed-to-charge ratio, and multi-day thermal history; feasibility flags use point estimates, and Q08/Q09/Q12 remain especially boundary-sensitive.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **A narrow productive C1/S2 high-temperature region exists near 420–430 K.** Batches 8, 11, and 12 directly returned crystal yields of 0.673, 0.675, and 0.678, respectively, with purity 0.986–1.000 and fines 0.354–0.385. The interpretation that this is an operating window, rather than an isolated result, is supported by three qualified batches.
- **The 440 K history causes a reproducible recovery collapse.** Batches 9 and 10 both retained high liquid-reaction yield, about 0.770–0.778, but gave crystal yield of only 0.0079–0.0090. Changing the cooling endpoint from 265 K to 270 K did not restore recovery. The observations establish reproducibility and implicate the upstream thermal history; they do not identify the molecular cause.
- **Cooler/longer C1 operation was inferior in this world.** Batch 5 at 330 K/7200 s gave reaction yield 0.364, degradation warning 0.206, and crystal yield 0.287. Progressively hotter, shorter conditions improved the observed results through batches 6–8. This contradicted my initial expectation that lower temperature would necessarily reduce degradation.
- **S2 produced high-purity crystals throughout the tested campaign.** Final purity was approximately 0.976–1.000 across the S2 batches. That is direct evidence for robust purification under those recipes.
- **Low-seed recipes were compatible with acceptable fines.** The 0.005 g recipes in batches 2, 6, 7, 8, 11, and 12 generally gave fines of 0.33–0.39, whereas batch 1, using 0.020 g seed, gave 0.515. The numerical contrast is observed, but attributing it solely to seed amount is not justified because reaction and cooling histories also differed.

### Supported only as interpretations

- **The apparent recovery factor collapsed at 440 K.** Writing crystal yield as reaction yield times an empirical crystallization-recovery factor summarizes the measurements well: approximately 0.90–0.92 at 420–430 K versus about 0.01 at 440 K. This factor is derived bookkeeping, not an independently measured physical constant.
- **The coarse, nearly fines-free particles in batches 9–10 represented a sparse seed-dominated population.** Their size indices were about 0.38–0.39 while seed-excluded yield was near zero. Seed dominance is a plausible interpretation, but particle counts and seed/product identity were not directly resolved.
- **Short high-temperature residence suppresses a competing pathway.** The trend in selectivity and degradation warning supports this idea, but it could instead reflect direct temperature-dependent selectivity or hidden state changes.

### Contradicted or weakened

- **Lower temperature should improve selectivity by suppressing degradation:** contradicted by batch 5 relative to batches 6–8.
- **Higher liquid reaction yield should translate monotonically into higher crystal recovery:** strongly contradicted by batches 9–10.
- **The extra 270 K hold in batch 12 clearly improves recovery or size:** not supported. Its yield advantage over batch 11 was only 0.003, below the 0.01 assay noise scale, and the size difference was comparable to size-measurement noise.

### Still untested

- Whether the 440 K cliff is caused by reversible speciation, a polymorphic/seed-compatibility transition, increased effective solubility, an inhibitor, or irreversible chemical transformation.
- Whether S2 is actually superior to S1 or S3 under the optimized reaction conditions; no controlled solvent comparison was performed.
- A catalyst main-effect ranking independent of temperature and thermal history.
- A controlled seed-dose response at fixed reaction and cooling conditions.
- Repeatability sufficient to distinguish batches 11 and 12.

## 2. One additional experiment

I would run **C1/S2 at 440 K for 300 s**, followed by the same 0.005 g seed and 14,400 s cooling to 270 K used in the successful region, with HPLC immediately after the reaction and particle measurement before filtration, then the final assay.

This would distinguish two leading explanations:

1. **Thermal-dose/residence-time mechanism:** the 600 s exposure at 440 K progressively creates an inhibitor or noncrystallizing target state. A 300 s exposure should retain substantial reaction yield while restoring crystal recovery toward the 420–430 K results—roughly above 0.5, with ordinary size and fines.
2. **Peak-temperature threshold mechanism:** merely reaching 440 K rapidly switches speciation, solid-form compatibility, or effective solubility. The 300 s experiment should still show high liquid target signal but crystal yield near the 0.01 observed in batches 9–10, with a sparse coarse population.

An intermediate outcome would suggest continuous competition between target formation and loss of crystallizability rather than a sharp switch. This experiment is more diagnostic than another 430 K replicate because the recovery difference between batches 11 and 12 is already below measurement resolution.

## 3. Least effectively used observation and least reliable prediction

The **intermediate particle measurement in batch 10** was used least effectively. Before filtration it already showed size about 0.387 and essentially zero fines, and the final assay remained similar while crystal yield was only 0.009. I used this mainly to describe a sparse, coarse population, but without absolute particle count or seed/product discrimination it could not establish whether the particles were unchanged seed, lightly grown seed, or a few new crystals. The observation was informative about morphology but weakly connected to mass recovery.

**Q09 is the least reliable held-out prediction.** It ends after only 60 s of cooling to 292 K following a relatively large seed charge. No campaign batch sampled such an early crystallization state. Seed alone guarantees particles, but the expected seed-excluded yield and the number-weighted size/fines metrics depend sensitively on whether the simulator treats those particles as unchanged seed, immediate secondary nuclei, or lightly grown crystals. Purity is also difficult to interpret when almost no new product may have crystallized. Consequently, its predicted low yield and nominal quality feasibility were much more extrapolative than predictions for long cooled histories.
