# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

The initial material-based prior favored solvent S2 and catalyst C1. S2 was nominally characterized by relatively high crystal-growth propensity (1.30), low nucleation tendency (0.65), low impurity occlusion (0.65), and low relative solubility (0.70). C1 had the highest nominal catalyst activity geomean. These properties motivated the predominantly S2/C1 campaign.

The results partly support that choice: S2/C1 consistently produced very pure isolated crystals, generally 0.98–1.00 purity, and substantial recovery. However, the favorable nominal growth/nucleation properties did not by themselves guarantee a low number fraction of fines. Under mild reaction histories, S2 batches often had fines fractions near one.

Only one S3 experiment was performed. Batch 5, using S3 with a 375 K/1800 s reaction and seeded cooling to 270 K, gave 0.497 crystal recovery, 0.979 purity, and 0.842 fines. It therefore did not solve the particle-quality problem. Because its downstream settings were not a perfect matched control and no S0 or S1 batches were run, a quantitative solvent ranking is not established. Likewise, catalysts C0, C2, and C3 were not tested, so C1 is a well-performing choice rather than a demonstrated global optimum.

### 2. Reaction behavior and useful balances

A useful first-order description is

`Y_rxn ≈ conversion × selectivity`

followed by

`Y_crystal = Y_rxn × f_isolation`,

where `Y_crystal` is the seed-excluded target moles in isolated solid divided by the initial reagent moles, and `f_isolation` includes crystallization and filtration losses. For representative batches, `Y_crystal/Y_rxn` was about 0.85–0.90: 0.849 in batch 1, 0.903 in batch 3, 0.890 in batch 8, 0.875 in batch 11, and 0.875 in batch 12. Thus most of the variation in final recovery near the recommended operating region was inherited from reaction-stage target yield, not solely from isolation efficiency.

Conversion was generally close to one, so selectivity and degradation were more important than incomplete conversion. Increasing hot-reaction severity raised byproduct and degradation signals and reduced selectivity. For example:

- Batch 3, 375 K for 1800 s: reaction yield 0.678, final crystal recovery 0.612, byproduct signal 0.215, and degradation warning 0.110.
- Batch 11, 399 K for 4200 s: reaction yield 0.528 and crystal recovery 0.462, with byproduct signal 0.402 and degradation warning 0.277.
- Batch 8, 405 K for 5400 s: reaction yield 0.459 and crystal recovery 0.409, with byproduct signal 0.470 and degradation warning 0.376.

This is evidence for a severity-dependent loss of target through competing reaction or degradation. The chemistry of those species remains unidentified.

### 3. Reaction–crystallization coupling

The strongest campaign result was that particle quality depended on upstream reaction history. Mild, high-yield reaction conditions generated very fine particle populations even after substantial changes to seed dose and cooling history:

- Batch 2: 375 K/1800 s, 0.005 g seed, cooling to 285 K over 14400 s; recovery 0.558 and fines 1.000.
- Batch 3: the same reaction, 0.001 g seed, cooling to 250 K over 14400 s; recovery 0.612 and fines 0.995.
- Batch 4: the same reaction, 0.050 g seed, cooling to 270 K over 3600 s; recovery 0.606 and fines 1.000.

Thus neither deeper cooling, longer cooling, nor the tested 50-fold seed-dose range independently suppressed fines in that mild-reaction regime.

In contrast, harsher reaction histories progressively moved the process into the acceptable fines region:

- Batch 7, 390 K/3600 s: recovery 0.513 and fines 0.629.
- Batch 11, 399 K/4200 s: recovery 0.462 and fines 0.459.
- Batch 9, 402.5 K/4800 s: recovery 0.434 and fines 0.466.
- Batch 8, 405 K/5400 s: recovery 0.409 and fines 0.438.

Batches 1 and 7 were close replicates of the 390 K/3600 s process and gave similar fines, 0.640 and 0.629, respectively. That repeatability supports a real process-history effect, although it does not identify its cause.

A plausible population-balance interpretation is

`dN_nuc/dt ∝ k_n × (supersaturation)^m × φ(reaction history)`

and

`dL/dt ∝ k_g × (supersaturation)^g`,

where `N_nuc` is the number of nuclei, `L` is characteristic particle size, and `φ` represents the effect of byproducts, degradation products, or other reaction-history-dependent solution properties. The observed trend is consistent with harsher reaction mixtures suppressing secondary nucleation relative to growth. Because fines are number-weighted,

`F20 = N(d < 20 µm)/N_total`,

a large number of low-mass nuclei can dominate the fines metric without dominating solid mass.

This inhibitor-like explanation is an interpretation, not an identified mechanism. Untested alternatives include changes in target speciation, supersaturation trajectory, viscosity, aggregation, seed-surface behavior, or an unobserved thermal-history effect. The data do not reveal which byproduct, if any, is causal.

### 4. Process-history dependence and failed alternatives

The original hypothesis was that S2 plus slower cooling and modest seeding would directly reduce fines. Batches 2–4 contradicted that hypothesis: downstream manipulations alone did not overcome the high-fines behavior of the mild reaction mixture.

A reheating/redissolution strategy was also tested. Batch 6 underwent initial seeded crystallization, partial reheating to 300 K, and recooling. It gave high recovery, 0.607, but fines of 1.000 and low CSD quality. Therefore that particular cycle was ineffective. Other reheating endpoints, dissolution fractions, or ripening holds remain untested.

The campaign consequently revised its working model: hot-reaction history controls both the amount of target available and the subsequent nucleation environment. Crystallization cannot be optimized independently of reaction selectivity and byproduct formation.

### 5. Purity and the unresolved quality–recovery tradeoff

Crystal purity remained high even as liquid-stage selectivity fell. Batch 8, for example, had reaction selectivity only 0.467 but crystal purity 0.984. This suggests preferential incorporation of the target and rejection of reaction impurities during crystallization. It also explains why harsher reaction conditions could satisfy the purity constraint despite producing more byproduct. The interpretation is selective purification by the crystal lattice; direct impurity identities or solid-state incorporation measurements were not available.

The principal unresolved tradeoff is therefore recovery versus number-weighted fines, not recovery versus purity. Around the operating boundary:

- Batch 10: recovery 0.453, purity 0.983, fines 0.471.
- Batch 11: recovery 0.462, purity 0.998, fines 0.459.
- Batch 12: recovery 0.466, purity 0.999, fines 0.504.

Batch 12 recovered slightly more than batch 11 but missed the fines limit by 0.0043. The declared final-assay noise scale for fines was 0.018, so that small excursion does not precisely locate the underlying physical boundary. Nevertheless, batch 11 has a much larger observed compliance margin—about 0.041—and is the highest-recovery completed batch whose final assay met both constraints. The sealed recommendation therefore remains batch 11.

No exact process replicate of batch 11 was obtained, so run-to-run process variability is unresolved. A confirmatory study would replicate batches 11 and 12 and densely sample the approximately 398–399 K, 4200 s boundary. Such work might show that a slightly milder process reliably meets the fines constraint, but the present evidence is insufficient to replace the recommended batch.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.16 | 0.48 |
| Q01 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q01 | crystal_size | 0.31 | 0.17 | 0.47 |
| Q01 | crystal_yield | 0.5 | 0.37 | 0.62 |
| Q02 | crystal_fines_fraction | 0.21 | 0.1 | 0.39 |
| Q02 | crystal_purity | 0.97 | 0.91 | 0.997 |
| Q02 | crystal_size | 0.39 | 0.23 | 0.56 |
| Q02 | crystal_yield | 0.49 | 0.36 | 0.61 |
| Q03 | crystal_fines_fraction | 0.58 | 0.37 | 0.78 |
| Q03 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q03 | crystal_size | 0.18 | 0.08 | 0.32 |
| Q03 | crystal_yield | 0.4 | 0.27 | 0.53 |
| Q04 | crystal_fines_fraction | 0.39 | 0.23 | 0.58 |
| Q04 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q04 | crystal_size | 0.3 | 0.16 | 0.46 |
| Q04 | crystal_yield | 0.41 | 0.28 | 0.54 |
| Q05 | crystal_fines_fraction | 0.36 | 0.21 | 0.54 |
| Q05 | crystal_purity | 0.94 | 0.86 | 0.985 |
| Q05 | crystal_size | 0.32 | 0.18 | 0.49 |
| Q05 | crystal_yield | 0.41 | 0.28 | 0.54 |
| Q06 | crystal_fines_fraction | 0.68 | 0.49 | 0.85 |
| Q06 | crystal_purity | 0.89 | 0.78 | 0.96 |
| Q06 | crystal_size | 0.15 | 0.06 | 0.29 |
| Q06 | crystal_yield | 0.42 | 0.29 | 0.55 |
| Q07 | crystal_fines_fraction | 0.34 | 0.19 | 0.52 |
| Q07 | crystal_purity | 0.94 | 0.86 | 0.985 |
| Q07 | crystal_size | 0.34 | 0.19 | 0.51 |
| Q07 | crystal_yield | 0.42 | 0.29 | 0.55 |
| Q08 | crystal_fines_fraction | 0.55 | 0.33 | 0.75 |
| Q08 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q08 | crystal_size | 0.22 | 0.09 | 0.39 |
| Q08 | crystal_yield | 0.35 | 0.21 | 0.49 |
| Q09 | crystal_fines_fraction | 0.56 | 0.34 | 0.77 |
| Q09 | crystal_purity | 0.98 | 0.89 | 1 |
| Q09 | crystal_size | 0.1 | 0.03 | 0.22 |
| Q09 | crystal_yield | 0.04 | 0.005 | 0.11 |
| Q10 | crystal_fines_fraction | 0.4 | 0.22 | 0.62 |
| Q10 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q10 | crystal_size | 0.17 | 0.07 | 0.31 |
| Q10 | crystal_yield | 0.16 | 0.07 | 0.28 |
| Q11 | crystal_fines_fraction | 0.37 | 0.21 | 0.56 |
| Q11 | crystal_purity | 0.93 | 0.84 | 0.98 |
| Q11 | crystal_size | 0.31 | 0.17 | 0.48 |
| Q11 | crystal_yield | 0.4 | 0.27 | 0.53 |
| Q12 | crystal_fines_fraction | 0.62 | 0.42 | 0.8 |
| Q12 | crystal_purity | 0.88 | 0.76 | 0.96 |
| Q12 | crystal_size | 0.2 | 0.09 | 0.35 |
| Q12 | crystal_yield | 0.47 | 0.32 | 0.61 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S3 is predicted to give larger, cleaner crystals and fewer fines than S1 because its nominal solubility, nucleation tendency, and impurity occlusion are lower, although S1's higher reaction activity leaves their overall recoveries similar. Q03–Q04: increasing seed mass should provide more controlled growth surface and suppress secondary nucleation, improving size and fines with little effect on seed-excluded recovery. Q05–Q06: gradual cooling should limit the nucleation burst and occlusion seen after an immediate deep temperature step; the long final holds make their recoveries similar. Q07–Q08: the late 315 K reheat can dissolve product, while the short recooling may incompletely restore recovery and can renucleate fines; this is assigned wide uncertainty because the campaign's single reheating test was unfavorable but not closely matched. Q09–Q10: particles are expected from the added seed in both, but 60 seconds permits little seed-excluded deposition; the additional two-hour hold increases recovery and growth and is expected to reduce the fines fraction. Q11–Q12: doubled reagent loading raises supersaturation and predicted recovery fraction but also promotes nucleation and impurity occlusion, reducing size, purity, and feasibility. Intervals are deliberately broad because these recipes use S0/S1 and multi-day histories not directly tested in the campaign; solvent-specific reaction residuals, seed-number distribution, long-time ripening, and reheat-induced renucleation are the largest uncertainties.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Reaction severity and crystallization quality were coupled in S2/C1.** As the hot history became more severe, fines generally fell while recovery fell: batch 7 (390 K/3600 s) gave recovery 0.513 and fines 0.629; batch 11 (399 K/4200 s) gave 0.462 and 0.459; batch 8 (405 K/5400 s) gave 0.409 and 0.438. Simultaneously, byproduct and degradation signals increased. This supports a process-history relationship, though not its molecular cause.
- **Purity was robust.** Final crystal purity was approximately 0.98–1.00 across the principal S2/C1 experiments, including harsher, less selective reactions. Thus crystallization evidently separated target-rich solid from much of the reaction impurity burden.
- **The recovery–fines boundary was near batches 11–12.** Batch 11 passed with recovery 0.462 and fines 0.459, whereas slightly milder batch 12 recovered 0.466 but measured fines of 0.504. This directly establishes a narrow observed tradeoff, although assay noise and process variability blur the exact boundary.
- **The tested reheating cycle was ineffective.** Batch 6 gave recovery 0.607 but fines near 1 after partial reheating and recooling.

### Contradicted or substantially revised

- **The initial claim that slow cooling and seeding in S2 would independently suppress fines was contradicted in the tested mild-reaction regime.** Batches 2–4 all used the same 375 K/1800 s reaction but varied seed from 0.001 to 0.050 g and used markedly different cooling endpoints and durations. Their fines remained approximately 0.995–1.000.
- **Seed dose alone was not shown to control particle quality.** The campaign did not reveal the expected monotonic improvement with added seed. This does not prove seed is irrelevant; it shows that its effect was overwhelmed under those conditions.
- **Longer or deeper cooling was not automatically better.** Batch 3 used long cooling to 250 K yet retained almost entirely fine particles.

### Interpretations rather than direct observations

- The proposal that reaction byproducts or degradation products inhibit secondary nucleation is consistent with the severity trend, but no species was identified or deliberately varied.
- Preferential lattice rejection of impurities is a reasonable explanation for high crystal purity despite poor reaction selectivity, but solid-phase impurity identities were not measured.
- The approximate factorization `crystal yield ≈ reaction yield × isolation fraction` was useful descriptively; it is not a validated kinetic law.

### Still untested

- Whether lower target supersaturation, rather than an inhibitory byproduct, explains the lower fines after harsher reactions.
- Catalysts C0, C2, and C3; solvents S0 and S1; and a controlled solvent ranking. Batch 5 provided only one imperfectly matched S3 comparison.
- Exact replication and process variance at the batch-11 boundary.
- Alternative ripening or partial-dissolution endpoints that might improve fines without the recovery loss seen in batch 6.

## 2. One additional experiment

I would perform a **supersaturation-matched mild-reaction experiment**. I would reproduce the mild S2/C1 reaction concentration and history associated with batches 2–4, take an intermediate HPLC measurement, and then add a calculated quantity of S2 before seeding so that the estimated target concentration entering crystallization matches that of batch 11. The downstream seed dose, cooling trajectory, and filtration would match batch 11 as closely as scale permits.

This would distinguish two leading explanations:

1. **Target-concentration/supersaturation explanation:** harsh reaction conditions reduce target formation, thereby reducing the nucleation burst. If this dominates, diluting a mild, selective reaction to the same target concentration should lower fines toward the batch-11 region, roughly 0.45–0.50, even though its byproduct signal remains low.
2. **Byproduct-mediated inhibition explanation:** harsh reaction products directly suppress nucleation or alter aggregation. If this dominates, the diluted mild mixture should retain the high-fines behavior of batches 2–4, potentially near 1, despite matched target concentration.

An intermediate result would indicate contributions from both target concentration and reaction-derived modifiers. The experiment would not identify the inhibitor chemically, but it would test whether target depletion alone is sufficient.

## 3. Least effectively used observation and least reliable prediction

The account used **crystal-size and CSD-quality observations** least effectively. It concentrated on the specification-defining fines fraction, yet normalized size was low and non-monotonic: batch 8 had fines 0.438 and size 0.109, batch 11 had fines 0.459 and size 0.077, and batch 12 had size 0.097 but fines 0.504. These observations warn that a single d50 does not determine the number-weighted lower tail. A fuller population-balance interpretation should have treated size, fines, and CSD quality jointly rather than describing the trend mainly as nucleation suppression.

**Q09 is the least reliable held-out prediction.** It filters only 60 seconds after cooling to 292 K. No campaign experiment probed this immediate post-seeding regime, and the result depends strongly on unknown seed-size distribution, how rapidly target deposits on seeds, and how seed particles contribute to measured size, fines, and purity while being excluded from crystal yield. Consequently, its predicted low yield is qualitatively plausible, but its particle-size, fines, purity, and feasibility estimates are much less grounded than predictions for long crystallization histories. Q08 is also uncertain because reheating was tested only once under unmatched conditions, but at least batch 6 supplies some direct evidence for that direction.
