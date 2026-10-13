# C-12 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The process consists of two coupled but distinct stages: catalytic formation of the target in solution, followed by nucleation, growth, and solid–liquid separation. I interpret the crystallization recovery as R_c = n(target recovered in crystals, excluding seed)/n(target present immediately before separation). It is therefore not the overall yield from charged reagent. A useful approximate overall isolated-target metric would be Y_overall ≈ Y_reaction × R_c, while solid purity and particle-size quality remain separate constraints. The fines metric is number-based, F_<20 = N(d < 20 µm)/N_total, so even a small mass of newly nucleated particles can dominate it.

Material effects—observations

Only catalyst C1 was used, so the campaign provides no experimental catalyst comparison. Any ranking of C0–C3 remains untested.

Solvent effects were explored, although not in a fully controlled factorial design. S1 gave the strongest group of crystallization recoveries: batch 3 reached 0.450, batch 5 reached 0.465, batch 6 reached 0.477, batch 9 was not S1 but reached 0.475, and batch 10 reached 0.476. By comparison, the two S2 batches gave 0.346 (batch 1) and 0.234 (batch 2), while S3 gave 0.286 in batch 8. S0 gave 0.475 in batch 9. All these solids were quite pure, generally about 0.96–1.00.

Interpretation: S1 was a robust empirical choice in the tested histories, consistent with its nominal combination of moderate solubility, growth, and low impurity occlusion. S0 could also deliver high recovery, as batch 9 demonstrates. The apparent disadvantage of S2 and S3 cannot be attributed solely to solvent because reaction temperature, cooling trajectory, seed dose, and residence time changed simultaneously. World-specific solvent residuals or solvent–reaction interactions are plausible alternatives.

Reaction/crystallization coupling

Reaction performance varied materially before crystallization. For example, batch 1 had reaction/final-assay yield near 0.43 and selectivity near 0.43, whereas several S1 batches had yield around 0.51–0.53 and selectivity around 0.49–0.55. Batch 2, run longer at 340 K, had lower reaction yield (about 0.305), lower selectivity (about 0.316), and higher degradation warning (about 0.201) than batch 1. Thus additional reaction residence time did not necessarily improve useful target production.

Despite imperfect reaction selectivity, crystallization strongly enriched the target: batch 6 combined reaction yield 0.528 with crystal purity reported at 1.000, and batch 3 combined reaction yield 0.508 with crystal purity 0.991. This indicates effective rejection of soluble impurities under these conditions. Batch 4’s resuspension/recrystallization history reduced the final byproduct signal to about 0.024 and produced purity 1.000, but recovery was only 0.441 and particle quality remained unacceptable. Purification and crystallization recovery therefore did not translate into acceptable particle morphology.

A qualitative framework is supersaturation S = C/C*(T, solvent). Nucleation may be represented as J ∝ exp[-B/(ln S)^2], while growth may be represented as G = k_g(S−1)^g. Cooling to low temperature increases S and recovery but can cause a burst of secondary nucleation. Because F_<20 is number-weighted, a large J can leave nearly all particles below 20 µm even when appreciable product mass is recovered. A population-balance description, ∂n/∂t + ∂(Gn)/∂L = B_nuc − D, is more appropriate than using median size alone.

Process-history dependence—observations

The initial S2 process in batch 1 used 0.020 g seed, cooling to 275 K, and a hold; it recovered 0.346 with purity 0.986 but fines 0.997. Batch 2 used only 0.001 g seed and much slower staged cooling, yet fines remained 1.000 and recovery fell to 0.234. Thus slower cooling and lower seeding did not solve the problem in S2.

Within S1, removing seed in batch 5 gave recovery 0.465 but fines 1.000. Increasing seed to 0.050 g in batch 6 raised observed recovery to 0.477 and purity to 1.000, but fines again equaled 1.000. Raising total seed to 1 g in batch 11 did not rescue morphology: recovery was 0.467 and fines about 0.994. Seed dose over the tested range therefore had no demonstrated monotonic benefit for number-weighted fines.

Stopping at a warmer crystallization temperature also did not suffice. Batch 7, crystallized at 290 K, had lower recovery (0.427) and fines about 0.987. Batch 8, using S3 with repeated 290 K stages, produced the largest final normalized size observed (about 0.087, corresponding qualitatively to a larger d50), but fines were still about 0.987 and recovery only 0.286. A larger median-like size metric did not imply removal of the fine-particle mode.

Two explicit history tests opposed a simple growth-time explanation. Batch 10 used cooling, partial reheating to 285 K, and staged recooling; recovery was 0.476, but fines were 1.000. Batch 12 used fifty repeated 290 K crystallization stages; recovery was 0.423 and fines remained 1.000. Batch 4 also included filtration, resuspension, reheating, and recrystallization, but ended with fines 1.000. These observations suggest persistent or renewed secondary nucleation rather than merely insufficient growth residence time.

Interpretation and revisions

My initial hypothesis was that S2, modest seeding, and slow cooling would give larger, cleaner crystals. The high purities were consistent with low impurity occlusion, but the particle-size prediction was rejected: batches 1 and 2 had nearly unity fines. I then considered insufficient seed surface, excessive seed count, cooling depth, and insufficient ripening. Unseeded, low-seed, high-seed, massive-seed, warm-endpoint, reheating, recrystallization, and very long growth histories all failed to reduce fines below 0.50. The evidence therefore argues against seed dose or simple elapsed growth time as the dominant controllable variable in the tested domain.

An untested alternative is that an interaction among solvent composition, supersaturation at the onset of crystallization, mixing/shear, and a narrow metastable-zone boundary governs secondary nucleation. The experiments did not independently vary agitation during crystallization, antisolvent composition, feed rate, or controlled supersaturation. Another possibility is a hidden material residual that changes nucleation kinetics relative to the nominal dossier. These remain hypotheses, not observations.

Uncertainty and unresolved tradeoff

No completed batch satisfied both purity ≥0.80 and fines ≤0.50. Purity was consistently acceptable; particle-number quality was not. Recovery optimization therefore occurred entirely outside the feasible region. Batch 6 remains the sealed recommendation because it had the highest observed recovery, 0.477, with reported purity 1.000. It must not be described as constraint-feasible: its fines fraction was 1.000.

The recovery advantage of batch 6 over batch 10 (0.477 versus 0.476) is only about 0.001, far below the final-assay recovery noise scale of approximately 0.01 and confounded by different histories. It is therefore a selection by observed maximum, not evidence of a reproducibly superior mechanism. Similarly, fines differences between roughly 0.987 and 1.000 are small relative to the distance from the required 0.50 threshold and do not establish meaningful feasibility progress.

The central unresolved tradeoff is that deep precipitation produced recovery near 0.45–0.48 and high purity but an overwhelming number of fine particles, while warmer or alternative histories reduced recovery without approaching the fines limit. Future mechanistic work should first suppress the nucleation burst—ideally through direct supersaturation control and controlled mixing—before attempting to maximize recovery.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.38 | 0.16 | 0.68 |
| Q01 | crystal_purity | 0.975 | 0.93 | 0.995 |
| Q01 | crystal_size | 0.14 | 0.075 | 0.22 |
| Q01 | crystal_yield | 0.34 | 0.2 | 0.48 |
| Q02 | crystal_fines_fraction | 0.61 | 0.32 | 0.87 |
| Q02 | crystal_purity | 0.94 | 0.86 | 0.98 |
| Q02 | crystal_size | 0.095 | 0.045 | 0.17 |
| Q02 | crystal_yield | 0.23 | 0.11 | 0.38 |
| Q03 | crystal_fines_fraction | 0.74 | 0.4 | 0.95 |
| Q03 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q03 | crystal_size | 0.075 | 0.03 | 0.15 |
| Q03 | crystal_yield | 0.2 | 0.08 | 0.34 |
| Q04 | crystal_fines_fraction | 0.32 | 0.12 | 0.65 |
| Q04 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q04 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q04 | crystal_yield | 0.24 | 0.11 | 0.39 |
| Q05 | crystal_fines_fraction | 0.28 | 0.1 | 0.6 |
| Q05 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q05 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q05 | crystal_yield | 0.25 | 0.12 | 0.4 |
| Q06 | crystal_fines_fraction | 0.82 | 0.55 | 0.98 |
| Q06 | crystal_purity | 0.93 | 0.83 | 0.98 |
| Q06 | crystal_size | 0.065 | 0.025 | 0.13 |
| Q06 | crystal_yield | 0.28 | 0.14 | 0.44 |
| Q07 | crystal_fines_fraction | 0.25 | 0.08 | 0.56 |
| Q07 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q07 | crystal_size | 0.16 | 0.085 | 0.25 |
| Q07 | crystal_yield | 0.27 | 0.13 | 0.42 |
| Q08 | crystal_fines_fraction | 0.68 | 0.35 | 0.92 |
| Q08 | crystal_purity | 0.97 | 0.9 | 0.995 |
| Q08 | crystal_size | 0.08 | 0.035 | 0.16 |
| Q08 | crystal_yield | 0.2 | 0.08 | 0.35 |
| Q09 | crystal_fines_fraction | 0.48 | 0.2 | 0.8 |
| Q09 | crystal_purity | 0.97 | 0.89 | 0.995 |
| Q09 | crystal_size | 0.095 | 0.045 | 0.17 |
| Q09 | crystal_yield | 0.015 | 0.001 | 0.06 |
| Q10 | crystal_fines_fraction | 0.35 | 0.14 | 0.68 |
| Q10 | crystal_purity | 0.965 | 0.89 | 0.995 |
| Q10 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q10 | crystal_yield | 0.075 | 0.02 | 0.17 |
| Q11 | crystal_fines_fraction | 0.28 | 0.1 | 0.59 |
| Q11 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q11 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q11 | crystal_yield | 0.25 | 0.12 | 0.41 |
| Q12 | crystal_fines_fraction | 0.72 | 0.41 | 0.94 |
| Q12 | crystal_purity | 0.91 | 0.8 | 0.97 |
| Q12 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q12 | crystal_yield | 0.38 | 0.22 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 isolates solvent: I expect S1's lower nominal solubility, lower nucleation tendency and lower occlusion than S3 to increase recovery, purity and particle size while reducing fines. Q03–Q04 tests seed loading: at this lower concentration I expect 0.001 g to be insufficient to control secondary nucleation, while 0.045 g provides enough growth surface; this reverses the simple 'more seed means smaller crystals' expectation when uncontrolled nucleation dominates. Q05–Q06 compares gradual cooling with a temperature shock at equal approximate elapsed time: the shock should give slightly higher cold-end recovery but a severe nucleation burst, smaller particles, more fines and somewhat more occlusion. Q07–Q08 tests a post-cooling thermal cycle: heating to 315 K may dissolve product and seeds, followed by rapid recooling that can renucleate; I therefore predict lower recovery and worse size distribution than the uninterrupted slow trajectory, despite similar or slightly better purity. Q09–Q10 compares a 60 s crystallization with an added 2 h growth hold: seed particles remain present in both, but seed-excluded recovery is near zero after 60 s and rises during the hold, with modest growth and fewer fines. Q11–Q12 doubles reagent concentration: greater supersaturation should raise fractional crystallization recovery but also promote nucleation and impurity occlusion, reducing purity and particle quality. Uncertainty is wide because these recipes extrapolate to lower charge, much longer cooling histories and higher reaction temperature than the sealed experiments; intervals include possible reversals near the fines threshold. Feasibility flags use the point estimates only.

## K2

1. Claim status

Supported by direct observations:
- Persistent fines were the dominant failure mode. Every completed batch had purity above 0.80, but none had fines at or below 0.50. Examples include batch 6 (recovery 0.477, purity 1.000, fines 1.000), batch 8 (0.286, 0.964, 0.987), and batch 12 (0.423, 0.995, 1.000).
- Crystallization strongly purified imperfect reaction mixtures. Batch 6 had reaction yield about 0.528 and selectivity about 0.526 but crystal purity 1.000; batch 3 had reaction yield about 0.508 and crystal purity 0.991. Interpreting this as impurity rejection by the solid phase is reasonable, although the precise exclusion mechanism was not measured.
- Seed loading alone did not solve particle quality. The unseeded batch 5, 0.001 g-seeded batch 3, 0.050 g-seeded batch 6, and 1 g-seeded batch 11 all produced fines near unity. This directly contradicts a simple monotonic seed-dose remedy.
- Simple extension of residence time did not solve the problem. Batch 12 underwent fifty repeated warm crystallization stages yet finished with fines 1.000. Batch 10’s partial reheating and staged recooling and batch 4’s resuspension/recrystallization also left fines at 1.000.
- S1 produced several of the largest observed recoveries: batches 3, 5, 6 and 10 gave approximately 0.450, 0.465, 0.477 and 0.476. However, calling S1 causally superior is only partially supported because these were not matched solvent-only comparisons. S0 also reached 0.475 in batch 9.

Contradicted or revised:
- The initial prediction that S2 plus slow cooling and modest seeding would yield good particles was contradicted. Batches 1 and 2 had fines of approximately 0.997 and 1.000, respectively; batch 2’s slower staged history also reduced recovery to 0.234.
- The interpretation that insufficient growth time was the main cause of fines was contradicted by batch 12.
- The idea that mild reheating or recrystallization would preferentially remove fines was not supported by batches 4 and 10.
- The apparent recovery superiority of batch 6 over batch 10 is not strongly supported: 0.477 versus 0.476 is much smaller than assay uncertainty and arose from different histories.

Still untested:
- Catalyst effects remain untested because all batches used C1.
- A causal solvent ranking remains untested because solvent was confounded with cooling and seeding history.
- The proposed roles of a metastable-zone boundary, mixing/shear, attrition, and a late supersaturation-driven secondary-nucleation burst remain interpretations. Supersaturation and particle populations were not measured during cooling.
- Whether the persistent fines are formed early, generated during deep cooling, produced by attrition, or partly reflect measurement inconsistency remains unresolved.

2. One additional experiment

I would run one time-resolved S0 batch at the lower-concentration conditions used in the held-out recipes: 0.004 mol reagent in 0.020 L, C1, 0.040 g seed, and a slow programmed cooling trajectory. I would measure particle size immediately after seeding, near 290 K, at 278 K, after a mild reheat to about 285–288 K, and after a second slow recooling, before final filtration. Reaction conditions, composition and agitation would otherwise remain fixed.

This would distinguish three explanations:
- Late supersaturation-driven secondary nucleation: fines should initially be low, rise sharply during the final cooling segment, fall after mild reheating as small particles dissolve, and remain lower after sufficiently slow recooling.
- Early nucleation or an intrinsically fine seed population: fines should already be high immediately after seeding or at 290 K and should show little reversible response to the late cooling segment.
- Attrition or persistent non-equilibrium fragmentation: fines should increase with elapsed handling and fail to decrease substantially on mild reheating, even if supersaturation is reduced.

A reversible reduction in fines on reheating would support dissolution/ripening control. A sharp late-cooling increase would support a metastable-zone explanation. High fines from the first measurement with little subsequent change would instead weaken both explanations and focus attention on seed properties, shear, or the measurement model.

3. Least-effective observation and least-reliable prediction

The observation used least effectively was batch 8’s combination of the largest reported normalized crystal size, about 0.087, with fines about 0.987. Since crystal size represents number-weighted d50/250, the point estimates are difficult to reconcile literally: 0.087 corresponds to a d50 near 22 µm, whereas a fines fraction near 0.99 implies almost all particles are below 20 µm. I noted that a larger size metric did not guarantee fewer fines, but I did not adequately emphasize that independent assay noise, a broad or irregular population, or metric inconsistency could dominate that comparison. The pre-filtration particle measurement in batch 8—size about 0.044 and fines about 0.999—also suggests that the final size increase may largely be measurement variation rather than genuine growth.

Q09 is the least reliable held-out prediction. It contains only 60 seconds of crystallization at 292 K, so recovered solids may be almost entirely the charged seed while crystal_yield explicitly excludes seed mass. No campaign batch probed this seed-dominated, near-zero-product limit. Consequently, particle presence is likely, but the predicted seed-excluded yield, the purity assigned to a mostly seed-derived cake, and the number-weighted size/fines values all require extrapolation beyond the observed histories. The Q03–Q04 seed comparison is also uncertain because it assumes that high seeding becomes effective at lower concentration despite the sealed campaign showing no seed-dose solution at higher concentration.
