# C-24 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome
The sealed recommendation is **batch 21**. It used 0.040 mol reagent and 0.005 mol catalyst C1 in 0.080 L solvent S2 under nitrogen, reacted at 380 K for 3600 s with 500 rpm stirring, quenched, and seeded with 0.050 g seed. Crystallization comprised 14,400 s stages at 320 and 295 K, a 7200 s anneal at 315 K with 100 rpm stirring, renewed 14,400 s stages at 295, 275, and 250 K, and four additional 14,400 s holds at 250 K and 100 rpm before filtration.

Its final assay observed crystal recovery 0.4586, purity 0.9915, fines fraction 0.4976, normalized crystal size 0.0623, and CSD quality 0.7163. Thus it had the highest measured recovery among batches whose point estimates met purity ≥0.80 and fines ≤0.50. Crystal recovery here is seed-excluded crystallization-stage recovery, not overall yield from charged reagent.

### Material effects
The strongest crystallization material effect was the solvent. The nominal dossier characterized S2 as having relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The experiments were consistent with that prior: S2 commonly gave purity around 0.98–1.00 and, after suitable thermal histories, fines below 0.50.

The other solvents did not provide feasible morphology under the shared seeded staged-cooling recipe. Batch 6 with S1 produced high recovery (0.4725) and purity 1.000 but fines 0.8552. Batch 7 with S0 gave recovery 0.4515 and fines 0.7091. Batch 8 with S3 gave recovery 0.3281 and fines 0.6183. These are observations from one common protocol, not proof that those solvents could never be optimized.

Solvent choice also affected reaction performance. S1 and S0 in batches 6 and 7 gave reaction selectivities near 0.59 and reaction yields near 0.59–0.62, better than the roughly 0.50 values often observed with S2/C1 at 380 K. Nevertheless, their excessive fines made them unsuitable for the stated crystallization constraint. This demonstrates that improving upstream reaction yield or selectivity need not improve the final feasible process.

Catalyst screening within S2 was less decisive. Batches 9–11 tested C0, C2, and C3 against C1-based runs. Their final recoveries were approximately 0.432, 0.393, and 0.371, while fines were 0.563, 0.545, and 0.560. None displaced C1 for the constrained objective. Because each comparison was limited and thermal-history variability was substantial, catalyst superiority should not be treated as a universal mechanistic conclusion.

All material identifiers are anonymous benchmark identities. References to solubility, growth, or nucleation describe nominal benchmark properties, not real chemical identities.

### Reaction–crystallization coupling
A useful accounting relation is

`Y_crystal = n(target recovered as crystals, excluding seed) / n(target present before separation)`.

If reaction and separation bases were perfectly aligned, an overall recovered-target fraction would scale approximately as

`Y_overall ≈ Y_reaction × Y_crystal`,

but the official recovery objective was only the second factor. Reaction impurities and degradation can still influence nucleation, growth, occlusion, and the resulting particle-size distribution.

Evidence for such coupling appeared in the temperature comparison. Batch 22 reacted at 350 K and then received deep staged cooling; it had recovery 0.4138 but fines 0.9986 and CSD quality 0.4972. Batch 23 reacted at 410 K before an otherwise related S2 cold-growth sequence and produced recovery 0.4294, purity 0.9987, fines only 0.1398, and CSD quality 0.7962. Its normalized size of 0.1167 corresponds to a number-weighted d50 of about 29 µm, versus about 16 µm for batch 21. The 410 K result suggests that the upstream composition strongly altered later nucleation or agglomeration behavior. However, batch 23 was not replicated and showed a higher degradation warning (0.2997), so the specific cause remains unresolved. Possible alternatives include a change in impurity spectrum, product concentration, polymorphic state, or an unobserved interaction with the quench.

### Process-history dependence
A conventional supersaturation description is useful:

`S = C/C*(T)` or equivalently `σ = (C − C*)/C*`,

where `C*` is temperature-dependent solubility. Nucleation rate generally rises much more steeply with supersaturation than crystal-growth rate. Rapidly entering a high-supersaturation region can therefore create many small particles, whereas seeding, staged cooling, and long low-temperature holds can channel material onto existing crystals. This is an interpretation consistent with the results, not an identified kinetic law for the hidden benchmark.

Batch 1 established the early baseline: a shorter seeded cooling to 285 K gave recovery 0.3778, purity 0.9864, and fines 0.6397. Extending and staging the cooling reduced fines toward 0.51 in batches 2–5. This caused the initial belief—simply use S2 and a modest seeded cooling—to be revised: thermal history was at least as important as solvent identity.

The importance of reaching sufficiently low temperature was especially clear. Batch 14 stopped at 300 K despite long holds and produced recovery 0.3456 with fines 0.7389. In contrast, batch 13 proceeded through 325, 315, 300, and 285 K with prolonged holding and achieved fines 0.4833, although recovery was only 0.3843. Batch 15 extended the descent to 250 K and achieved recovery 0.4437 with fines 0.4992. These observations support continued desupersaturation and growth at low temperature, while also showing that time alone at a warmer temperature was ineffective.

Annealing offered another route. Batch 16 used a reheat/recool cycle and achieved fines 0.4733, but recovery was only 0.3875. Batch 21 combined annealing with subsequent cooling to 250 K and improved recovery to 0.4586. Mechanistically, partial dissolution of the smallest particles during annealing followed by regrowth on surviving crystals is plausible. It was not directly measured, so alternatives such as altered aggregation or secondary nucleation remain open.

Seed dose was not monotonic. Under related deep-cooling histories, batch 17 used 0.050 g seed and gave recovery 0.4562 with fines 0.4586; batch 19 used 0.020 g and gave recovery 0.4545 with fines 0.4686; unseeded batch 20 gave recovery 0.4455 with fines 0.5030. These data weakly favor seeding but do not identify an optimum dose. Seed surface area and size distribution were not independently varied.

### Revisions, uncertainty, and unresolved tradeoff
The campaign began with the expectation that S2, slow cooling, and seeding would give cleaner, larger particles. The solvent preference survived testing, but the mechanism was revised in three ways:

1. Long, deeply staged cooling was necessary; the initial batch still had excessive fines.
2. Seed mass alone did not explain morphology.
3. Upstream reaction temperature unexpectedly exerted a very large influence on fines, as shown by batches 22 and 23.

Final-assay standard deviations were approximately 0.018 for fines, 0.010 for purity and recovery, and 0.025 for normalized size, in addition to real process variability. Batch 21 is only 0.0024 below the fines limit, so its constraint satisfaction is not robust to that uncertainty. Batch 17 offered nearly the same recovery (0.4562) with a larger measured fines margin (0.4586). Conversely, nominally similar batch 24 gave recovery 0.4347 and fines 0.5192, demonstrating meaningful replicate scatter. Batch 18 also showed that four additional cold holds did not monotonically improve quality: recovery was 0.4454 and fines 0.5062.

Accordingly, the unresolved tradeoff is between maximizing the observed recovery and maintaining a reliable fines margin. Batch 21 maximizes measured feasible recovery and therefore remains the sealed recommendation. Batch 17 is the more conservative high-recovery alternative, while batch 23 provides the strongest fines margin at lower recovery. Replicated comparisons of batches 17, 21, and 23 would be the most important unperformed work, together with direct time-resolved concentration and particle-population measurements to distinguish dissolution/regrowth, secondary nucleation, and aggregation mechanisms.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.62 | 0.43 | 0.79 |
| Q01 | crystal_purity | 0.99 | 0.94 | 1 |
| Q01 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q01 | crystal_yield | 0.38 | 0.27 | 0.49 |
| Q02 | crystal_fines_fraction | 0.44 | 0.27 | 0.62 |
| Q02 | crystal_purity | 0.97 | 0.91 | 1 |
| Q02 | crystal_size | 0.14 | 0.07 | 0.22 |
| Q02 | crystal_yield | 0.26 | 0.16 | 0.37 |
| Q03 | crystal_fines_fraction | 0.71 | 0.53 | 0.86 |
| Q03 | crystal_purity | 0.98 | 0.92 | 1 |
| Q03 | crystal_size | 0.055 | 0.015 | 0.12 |
| Q03 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q04 | crystal_fines_fraction | 0.47 | 0.3 | 0.64 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.115 | 0.055 | 0.19 |
| Q04 | crystal_yield | 0.34 | 0.23 | 0.45 |
| Q05 | crystal_fines_fraction | 0.46 | 0.29 | 0.63 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q05 | crystal_yield | 0.35 | 0.24 | 0.46 |
| Q06 | crystal_fines_fraction | 0.64 | 0.45 | 0.8 |
| Q06 | crystal_purity | 0.97 | 0.9 | 1 |
| Q06 | crystal_size | 0.065 | 0.02 | 0.135 |
| Q06 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q07 | crystal_fines_fraction | 0.47 | 0.3 | 0.64 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.115 | 0.055 | 0.19 |
| Q07 | crystal_yield | 0.35 | 0.24 | 0.46 |
| Q08 | crystal_fines_fraction | 0.37 | 0.21 | 0.55 |
| Q08 | crystal_purity | 0.98 | 0.92 | 1 |
| Q08 | crystal_size | 0.155 | 0.08 | 0.25 |
| Q08 | crystal_yield | 0.32 | 0.21 | 0.44 |
| Q09 | crystal_fines_fraction | 0.65 | 0.43 | 0.84 |
| Q09 | crystal_purity | 0.96 | 0.85 | 1 |
| Q09 | crystal_size | 0.06 | 0.015 | 0.13 |
| Q09 | crystal_yield | 0.025 | 0 | 0.08 |
| Q10 | crystal_fines_fraction | 0.56 | 0.36 | 0.74 |
| Q10 | crystal_purity | 0.97 | 0.88 | 1 |
| Q10 | crystal_size | 0.08 | 0.025 | 0.15 |
| Q10 | crystal_yield | 0.16 | 0.07 | 0.27 |
| Q11 | crystal_fines_fraction | 0.45 | 0.28 | 0.62 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.125 | 0.06 | 0.205 |
| Q11 | crystal_yield | 0.35 | 0.24 | 0.46 |
| Q12 | crystal_fines_fraction | 0.61 | 0.42 | 0.78 |
| Q12 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q12 | crystal_size | 0.085 | 0.03 | 0.16 |
| Q12 | crystal_yield | 0.5 | 0.39 | 0.61 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are noise-free process predictions with epistemic 80% intervals, not final-assay noise intervals. All recipes contain seed and a crystallization step, so particles are expected even where seed-excluded product recovery is small. Q01–Q02: campaign batches 6 and 8 suggest S1 gives greater recovery but substantially more fines than S3; the exceptionally slow ramps should improve both morphologies, but S1 is still predicted to miss the fines limit. Q03–Q04: increasing S0 seed from 0.001 to 0.045 g should suppress secondary nucleation and increase size, with little effect on equilibrium recovery. Q05–Q06: gradual cooling should favor growth over nucleation; an initial 120 s crash is expected to leave a persistent excess of fines despite the equally long cold residence. Q07–Q08: the 315 K anneal should preferentially dissolve small particles and increase subsequent size, at a modest recovery cost because recooling lasts only one hour. Q09–Q10: two hours at 292 K should raise recovery and allow some growth relative to immediate filtration, but likely not enough to establish a low-fines distribution. Q11–Q12: doubling reagent concentration should raise fractional recovery by increasing supersaturation relative to residual solubility, but should also intensify nucleation and impurity incorporation, reducing size and purity and increasing fines. Uncertainty is broad because these recipes use lower volume, catalyst concentration, and reagent concentration than the campaign, and because nominally similar campaign histories showed appreciable process scatter near the 0.50 fines boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S2 was the best tested solvent for controlling fines under the studied conditions.** With a shared seeded staged-cooling protocol, S2 in batch 2 gave fines 0.517, versus 0.855 for S1 (batch 6), 0.709 for S0 (batch 7), and 0.618 for S3 (batch 8). Purity remained high throughout. Interpreting this as lower effective nucleation and stronger growth in S2 is plausible and consistent with its nominal dossier, but the measurements directly establish only the outcome ordering for those recipes.
- **Thermal history strongly affected morphology.** Batch 14 stopped at 300 K and gave fines 0.739, whereas deeper multistage cooling gave 0.483 in batch 13, 0.499 in batch 15, 0.459 in batch 17, and 0.469 in batch 19. This directly supports the importance of deep cooling and process history.
- **High recovery and feasible quality could coexist.** Batches 17, 19, and 21 all had recovery near 0.45, purity well above 0.80, and fines below 0.50 by point estimate. Batch 21 had the highest feasible measured recovery, 0.4586.
- **Seed dose was not the sole determinant.** Related deep-cooling runs gave recovery/fines of 0.456/0.459 with 0.050 g seed (batch 17), 0.455/0.469 with 0.020 g (batch 19), and 0.446/0.503 without seed (batch 20). Seeding weakly favored feasibility, but no monotonic optimum was demonstrated.
- **Constraint robustness was unresolved.** A nominally similar repeat, batch 24, gave fines 0.519 versus 0.459 in batch 17. Batch 21 was only 0.0024 below the limit. These observations directly show that pointwise feasibility does not imply robust feasibility.

### Supported only as interpretations
- **Growth-versus-nucleation interpretation:** slower, deeper cooling was interpreted as directing supersaturation toward growth rather than new-particle formation. The observed histories support this qualitatively, but nucleation and growth rates were never measured separately.
- **Reaction–crystallization coupling:** batch 22 at 350 K had fines 0.999, whereas batch 23 at 410 K had fines 0.140 under related downstream processing. This is strong evidence that upstream history mattered, but attributing it to a changed impurity spectrum, product concentration, or precursor state is interpretive because batch 23 was unreplicated and lacked composition-resolved intermediate measurements.
- **Annealing as selective dissolution/Ostwald ripening:** batches 16 and 21 showed that reheat/recool histories can produce feasible fines. Selective dissolution of small particles is plausible, but aggregation, polymorphic change, or altered secondary nucleation could produce similar final observations.

### Contradicted or materially weakened
- **“Longer cold residence monotonically lowers fines” was contradicted.** Batch 18 used more cold holding than batch 17 but had fines 0.506 rather than 0.459. Batch 24 also failed the limit despite a nominally similar history. Time at low temperature was therefore not sufficient by itself.
- **“Larger median size necessarily means fewer fines” was weakened.** Batch 18 had normalized size 0.128—among the largest measured—yet fines were 0.506. Median size and the number fraction below 20 µm describe different parts of the distribution.
- **The initial expectation that S2 plus modest seeding and one cooling step would be sufficient was contradicted by batch 1**, which had high purity but fines 0.640.
- A general claim that annealing must reduce recovery was not supported: batch 16 had low recovery, but batch 21 combined annealing with recovery 0.459.

### Still untested
- Direct identification of primary nucleation, secondary nucleation, dissolution/regrowth, aggregation, or polymorphic transformation.
- Replication of the extreme 410 K result from batch 23 and a replicated 350/380/410 K temperature response.
- Whether batch 21 remains feasible on a robust confidence-bound basis.
- Independent effects of seed number, seed size distribution, and seed surface area.
- Equilibrium solubility curves and time-resolved liquid concentration.
- Scale and concentration transfer to the much smaller held-out recipes.

## 2. One additional experiment

I would exactly replicate **batch 23** at 410 K, but add a pre-quench HPLC measurement and non-destructive particle-size measurements after the first appearance of crystals and after each major cooling/holding stage. The final isolation and assay would remain unchanged.

This single experiment would address two leading alternatives:

1. **Repeatable upstream-state effect:** 410 K reproducibly creates a feed composition that suppresses later nucleation.
2. **Stochastic or isolated downstream event:** batch 23’s very low fines arose from process variability, aggregation, or an assay realization rather than a reproducible temperature effect.

Different trajectories would further separate mechanisms:
- If the replicate again gives fines near 0.14 and particles are already coarse and low-fines at the first measurement, that would support early nucleation suppression caused by the 410 K feed.
- If fines begin high and decline during later holds while size increases, that would support dissolution/regrowth or aggregation during crystallization.
- If pre-quench composition resembles the 380 K runs but the low-fines result repeats, a persistent physical precursor or quench-mediated explanation becomes more plausible than ordinary conversion/selectivity differences.
- If the final fines return to roughly 0.45–0.55, batch 23 was probably an unusually favorable realization rather than evidence for a robust 410 K regime.

This would not identify a hidden species by itself, but it would sharply distinguish an early, repeatable temperature-conditioned effect from a late or stochastic morphology change.

## 3. Least effectively used observation and least reliable prediction

The account used **batch 18** least effectively. It had a large normalized median size, 0.128, after extended cold holding, yet fines remained 0.506. I acknowledged its non-monotonic result but still relied too heavily on a simple “more time → more growth → fewer fines” narrative. Batch 18 shows why d50 and fines cannot be substituted for each other: substantial growth of the central population can coexist with a persistent population of sub-20-µm particles.

The least reliable held-out prediction is **Q09**. It filters only 60 seconds after a rapid cooling step, so recovered product may be extremely small relative to the deliberately added seed. No campaign batch probed that timescale or the interpretation of particle-size and purity metrics when particles are dominated by seed but seed-excluded product recovery is near zero. Consequently, the predicted crystal yield, size, and fines depend on unverified assumptions about the seed population, onset time of crystallization, and how the benchmark forms its representative slurry measurement. Q12 is also extrapolative because it doubles concentration, but Q09 is more structurally outside the observed process regime.
