# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The process is best understood as a coupled reaction–population-balance problem. The reaction establishes the target-product/impurity inventory entering crystallization; solvent composition and thermal history then control supersaturation, nucleation, growth, impurity rejection, and the fraction of target recovered as filterable crystals.

Useful definitions are

R_c = n(target recovered in crystals, excluding seed) / n(target present before separation),

P_c = n(target in recovered crystals) / n(total material in recovered crystals),

and

F_20 = N(d < 20 µm) / N(total particles).

Thus crystal yield is a crystallization-stage recovery, not an overall yield from charged reagent, while F_20 is number-weighted and can be dominated by many small particles. A qualitative population-balance description is dN/dt = J(S,T,solvent,impurities) and dL/dt = G(S,T,solvent,impurities), where supersaturation S may be represented as C/C*(T). High nucleation rate J creates many fines; sustained growth G on fewer nuclei gives larger particles. Reaction impurities can alter both rates through adsorption, occlusion, or heterogeneous nucleation.

Material effects

The nominal dossier suggested that S2 combined low nucleation tendency and impurity occlusion with high crystal growth. Experiments supported that qualitative particle-quality prediction: pure-S2 batches 1–3 had compliant fines of 0.398, 0.345, and 0.336, respectively, with final crystal purities of 0.991, 0.988, and 0.995. However, their recoveries plateaued near 0.48–0.49. This revised the initial expectation that S2’s nominally low solubility would necessarily maximize recovery: its strongest observed advantage was particle quality rather than recovery.

Pure S0 and S1 shifted the balance toward recovery but generated excessive fines. Batch 4 with S0 reached recovery 0.557 but F_20 = 1.000. Batches 5 and 6 with S1 reached recoveries 0.555 and 0.567, but their fines were 0.576 and 0.580. S0’s nominally high nucleation tendency and low growth tendency offer a plausible explanation for batch 4. The S1 results indicate that even its intermediate nucleation/growth properties did not provide enough fines control under the tested conditions.

Blending S1 and S2 produced the useful compromise. Batch 7 used 0.04 L each of S1 and S2 and gave the highest observed qualifying recovery, 0.5467, with purity 0.9841 and F_20 = 0.4962. Batch 8 shifted the blend to 0.03 L S1 plus 0.05 L S2 and retained recovery 0.5450 while reducing fines to 0.4536. Its nominal interpretation is that S1 supplies the higher-recovery tendency while additional S2 suppresses excessive nucleation/occlusion and favors growth. This interpolation is empirical; the data do not establish an ideal-mixture law or rule out nonlinear solvent interactions.

Reaction–crystallization coupling

C1 was used for most batches. Despite only moderate reaction selectivity—about 0.55–0.58 in several final assays—crystal purities were generally 0.98–1.00. Crystallization therefore acted as a strong purification step, rejecting much of the reaction impurity pool. High crystal purity does not imply a highly selective reaction.

Catalyst identity nevertheless affected downstream recovery. In batch 11, replacing C1 with C3 while retaining the 0.03/0.05 S1/S2 process reduced recovery to 0.4748. Its final reaction selectivity was 0.526 and byproduct signal 0.362, versus selectivity 0.577/byproduct 0.300 in C1 batch 8 and 0.563/0.296 in C1 batch 12. A plausible interpretation is that C3 produced a less favorable mother-liquor composition: lower target inventory quality or higher impurity burden may have impeded target crystallization even though recovered crystals remained pure (0.994). This is only a C1-versus-C3 comparison; C0 and C2 were not tested, and catalyst effects are confounded with batch variability.

Process-history dependence

Cooling to 250 K slowly was favorable relative to the warmer initial crystallization. Batch 1 stopped at 275 K and obtained recovery 0.476 with fines 0.398. Batch 2 cooled to 250 K over 14,400 s and obtained recovery 0.490 with fines 0.345. Because temperature, cooling duration, and hold history changed together, this comparison supports—but does not isolate—the effects of deeper or slower cooling.

Seed effects were weaker than initially expected. Removing the 0.01 g seed and extending the cold hold in batch 3 produced recovery 0.489 and fines 0.336, nearly matching seeded batch 2. Conversely, increasing S1 seed to 0.05 g in batch 6 did not bring fines below 0.50 and did not clearly improve the S1 outcome relative to unseeded batch 5. These observations revised the initial hypothesis that seed dose would be the principal fines-control lever. They do not show that seeding is irrelevant: seed size distribution, addition temperature, and seed conditioning were not varied independently.

A reduced-solvent hypothesis was also revised. Batch 9 lowered the mixed-solvent volume from 0.08 to 0.06 L, expecting stronger supersaturation and recovery. Instead, recovery fell to 0.538 and fines rose to 0.580. The likely interpretation is that the more concentrated trajectory generated excessive nucleation or impurity-mediated growth inhibition; a simple equilibrium-solubility argument was inadequate.

Thermal cycling was not beneficial in the tested form. Batch 10 partially reheated the 0.03/0.05 blend to 300 K and recooled it. Recovery fell to 0.521, while fines were still 0.484. Partial dissolution may have lost solid mass without providing sufficient ripening or regrowth before filtration. Other cycle temperatures and durations remain untested.

Uncertainty and unresolved tradeoff

Batch 7 is the sealed recommendation because it had the maximum measured recovery among batches satisfying purity ≥0.80 and F_20 ≤0.50. Its fines result, 0.4962, is very close to the limit. Given the stated final-assay fines noise of approximately 0.018 and the absence of a replicate of the exact 1:1 recipe, compliance should be regarded as borderline rather than robust.

The 0.03/0.05 S1/S2 process had a larger quality margin. Batches 8 and 12 gave recoveries of 0.5450 and 0.5309, purities of 0.9847 and 0.9990, and fines of 0.4536 and 0.4686. Their recovery spread shows meaningful batch/process uncertainty, and the 0.0017 difference between batches 7 and 8 is far too small to establish a true recovery advantage. Consequently, the scientific conclusion is a recovery–robustness tradeoff: batch 7 is the highest observed qualifying result, whereas the slightly more S2-rich region has stronger evidence of fines compliance at potentially little average recovery cost.

Untested alternatives include finer blend-ratio mapping near the S1/S2 boundary, independent replication of batch 7, C0 and C2 screening, controlled seed-size and seed-addition-temperature studies, and different cooling profiles without simultaneously changing hold time. Because the materials are anonymous benchmarks with hidden fixed residuals, these relationships apply only to this campaign’s tested material set and should not be generalized to real chemical identities.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.16 | 0.46 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q01 | crystal_yield | 0.43 | 0.3 | 0.56 |
| Q02 | crystal_fines_fraction | 0.44 | 0.27 | 0.62 |
| Q02 | crystal_purity | 0.965 | 0.9 | 0.995 |
| Q02 | crystal_size | 0.105 | 0.055 | 0.17 |
| Q02 | crystal_yield | 0.34 | 0.2 | 0.49 |
| Q03 | crystal_fines_fraction | 0.62 | 0.43 | 0.8 |
| Q03 | crystal_purity | 0.985 | 0.94 | 1 |
| Q03 | crystal_size | 0.075 | 0.035 | 0.14 |
| Q03 | crystal_yield | 0.42 | 0.28 | 0.56 |
| Q04 | crystal_fines_fraction | 0.38 | 0.22 | 0.55 |
| Q04 | crystal_purity | 0.985 | 0.95 | 1 |
| Q04 | crystal_size | 0.12 | 0.065 | 0.19 |
| Q04 | crystal_yield | 0.46 | 0.33 | 0.59 |
| Q05 | crystal_fines_fraction | 0.34 | 0.18 | 0.51 |
| Q05 | crystal_purity | 0.985 | 0.95 | 1 |
| Q05 | crystal_size | 0.13 | 0.075 | 0.2 |
| Q05 | crystal_yield | 0.47 | 0.34 | 0.6 |
| Q06 | crystal_fines_fraction | 0.7 | 0.52 | 0.86 |
| Q06 | crystal_purity | 0.975 | 0.92 | 1 |
| Q06 | crystal_size | 0.07 | 0.03 | 0.125 |
| Q06 | crystal_yield | 0.5 | 0.37 | 0.63 |
| Q07 | crystal_fines_fraction | 0.29 | 0.14 | 0.46 |
| Q07 | crystal_purity | 0.988 | 0.955 | 1 |
| Q07 | crystal_size | 0.15 | 0.085 | 0.23 |
| Q07 | crystal_yield | 0.48 | 0.35 | 0.61 |
| Q08 | crystal_fines_fraction | 0.6 | 0.4 | 0.78 |
| Q08 | crystal_purity | 0.975 | 0.92 | 1 |
| Q08 | crystal_size | 0.08 | 0.035 | 0.145 |
| Q08 | crystal_yield | 0.39 | 0.25 | 0.53 |
| Q09 | crystal_fines_fraction | 0.58 | 0.39 | 0.77 |
| Q09 | crystal_purity | 0.995 | 0.96 | 1 |
| Q09 | crystal_size | 0.07 | 0.03 | 0.12 |
| Q09 | crystal_yield | 0.01 | 0 | 0.04 |
| Q10 | crystal_fines_fraction | 0.47 | 0.29 | 0.65 |
| Q10 | crystal_purity | 0.99 | 0.95 | 1 |
| Q10 | crystal_size | 0.095 | 0.045 | 0.16 |
| Q10 | crystal_yield | 0.13 | 0.05 | 0.24 |
| Q11 | crystal_fines_fraction | 0.36 | 0.2 | 0.54 |
| Q11 | crystal_purity | 0.985 | 0.95 | 1 |
| Q11 | crystal_size | 0.125 | 0.07 | 0.195 |
| Q11 | crystal_yield | 0.46 | 0.33 | 0.59 |
| Q12 | crystal_fines_fraction | 0.57 | 0.38 | 0.75 |
| Q12 | crystal_purity | 0.965 | 0.9 | 0.995 |
| Q12 | crystal_size | 0.085 | 0.04 | 0.145 |
| Q12 | crystal_yield | 0.59 | 0.45 | 0.72 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is predicted to give lower solubility, less occlusion and less nucleation than S3, hence higher recovery, purity and size with fewer fines. Q03–Q04: very low seeding in nucleation-prone S0 is expected to permit secondary nucleation; heavier seeding buffers supersaturation and improves the number-weighted CSD, although this seed effect is uncertain. Q05–Q06: gradual cooling should suppress fines and favor growth, while the rapid drop gives slightly greater low-temperature exposure and recovery but a much finer CSD. Q07–Q08: the 315 K reheat followed by rapid recooling is expected to dissolve product and then renucleate fines; this follows the adverse thermal-cycle direction observed previously. Q09–Q10: seed guarantees particles in both, but the 60-second run should recover almost no seed-excluded product; the additional two-hour hold permits modest deposition and growth. Q11–Q12: doubling reagent concentration should increase supersaturation and recovery, but also secondary nucleation and impurity occlusion, creating a recovery–quality tradeoff. Intervals are deliberately broad because these recipes use much smaller charges, exceptionally long staged cooling, and seed-to-product ratios outside the experimental campaign; they represent process-model uncertainty and exclude final-assay sampling noise.

## K2

1. Status of the main claims

Supported by direct observations:

- Solvent identity strongly affected the recovery–particle-quality tradeoff. Pure S2 gave compliant fines but moderate recovery in batches 1–3: crystal yields were about 0.476–0.490 and fines 0.336–0.398. Pure S0 or S1 increased observed recovery to about 0.555–0.567 in batches 4–6, but fines failed the 0.50 limit, reaching 1.000 for batch 4 and about 0.576–0.580 for batches 5–6. The interpretation that nucleation/growth tendencies caused this pattern is plausible, but the numerical tradeoff itself is directly observed.

- S1/S2 blending produced a useful compromise. Batch 7 gave yield 0.5467, purity 0.9841 and fines 0.4962; batch 8 gave yield 0.5450, purity 0.9847 and fines 0.4536. Batch 12 repeated the S2-richer region with yield 0.5309, purity 0.9990 and fines 0.4686. These observations support a feasible blend region, but not a precisely located optimum.

- Crystallization provided strong apparent purification. Final crystal purities were generally 0.98–1.00 despite reaction selectivities around 0.53–0.63. Impurity rejection during crystallization is an interpretation; the high final purity and moderate reaction selectivity are observations.

- The tested C3 process was inferior to comparable C1 processes. Batch 11, using C3 with the 0.03/0.05 S1/S2 blend, gave yield 0.4748, versus 0.5450 and 0.5309 for C1 batches 8 and 12. Batch 11 also had lower selectivity and a higher byproduct signal. The claim is supported only for this single C3 comparison; attributing the lower crystallization recovery specifically to impurity-mediated growth inhibition remains interpretive.

- The tested concentration increase and thermal cycle were not beneficial. Reducing total mixed-solvent volume in batch 9 gave yield 0.5381 with fines 0.5795, worse than batch 8. The 300 K reheat/recool cycle in batch 10 gave yield 0.5212 and fines 0.4842, also worse than the noncycled batch 8 in recovery. These are direct outcomes; excessive nucleation, partial dissolution and inadequate regrowth are proposed mechanisms rather than demonstrated causes.

Contradicted or substantially revised:

- The initial expectation that pure S2 would maximize recovery because of its nominally low solubility was contradicted: S0 and S1 recovered more product, although with unacceptable fines.

- The simple expectation that less solvent would raise recovery through higher supersaturation was contradicted by batch 9.

- The expectation that more seed would reliably suppress fines was not supported. Unseeded S1 batch 5 and heavily seeded batch 6 both failed the fines limit, while seeded and unseeded S2 batches 2 and 3 were similar. Because hold histories also differed, this is not a clean demonstration that seed has no effect.

- Beneficial Ostwald ripening from the tested thermal cycle was contradicted by batch 10’s lower recovery and lack of a clear fines advantage.

Still untested or unresolved:

- C0 and C2 catalysts, nonlinear solvent-blend interactions, the exact S1/S2 feasibility boundary, seed crystal size distribution, seed-addition temperature, and staged seeding were not tested.

- Cooling depth, cooling rate and cold-hold duration were not independently separated. Batch 1 versus batch 2 changed several of these simultaneously.

- Batch 7’s exact 1:1 recipe was not replicated. Its final fines result was only 0.0038 below the limit, so its robustness remains unresolved.

- Small differences such as batch 7 versus batch 8 are not established effects given assay noise and batch variability.

2. One additional experiment

I would exactly replicate batch 7: C1, 0.04 L S1 plus 0.04 L S2, the same reagent and catalyst charges, 350 K reaction, 0.01 g seed, slow cooling to 250 K, the same cold hold and filtration. I would include the same prefilter particle-size measurement and final assay.

This would distinguish two leading explanations for batch 7’s result:

- A reproducible composition effect: the 1:1 blend genuinely lies near the optimal recovery–fines frontier.
- A noise or process-variability explanation: its 0.5467 recovery and 0.4962 fines were a favorable realization, while the more S2-rich batch-8/12 region is the more reliable feasible process.

If the composition effect is real, I would expect recovery near 0.54–0.55 and fines again just below 0.50. If batch 7 was a favorable fluctuation, the repeat could either exceed 0.50 fines or show recovery closer to the 0.531–0.545 range of batches 8 and 12. A much lower prefilter fines value followed by borderline final-assay fines would instead implicate instrument/sampling differences; agreement between the two measurements would favor genuine process variability.

3. Least effectively used observation and least reliable prediction

The account used the prefilter particle-size measurements least effectively, especially in batch 7. Its particle-size measurement reported fines of about 0.511 before filtration, whereas the final assay reported 0.496. Batch 8 similarly changed from about 0.466 to 0.454, while batch 10 changed in the opposite direction, from about 0.463 to 0.484. I relied mainly on final-assay values and did not fully use these paired observations to emphasize sampling, instrument and filtration-stage uncertainty. For a recommendation lying almost exactly on the fines limit, that omission matters.

Q09 is the least reliable held-out prediction. It contains 0.025 g seed but only 60 seconds of cooling to 292 K before filtration. No campaign batch measured the immediate, essentially seed-dominated state. Consequently, there is little evidence for how particle presence, number-weighted size and fines behave before appreciable product deposition, particularly because seed is excluded from crystal yield but may still contribute to the particle population. The predicted near-zero recovery is mechanistically plausible, but its particles_present classification, size, fines and therefore quality_feasible classification require the largest extrapolation.
