# repeat-02 / C-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:10:13.277135+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Solvent S2 should favor larger, purer crystals and lower fines because its dossier indicates high growth, low nucleation and low occlusion, although its low solubility may trade against reaction performance. S1 is the reaction-activity comparator.

H2 [tentative] C1 is the best initial catalyst choice from nominal activity. A warm reaction hold followed by controlled seeded cooling and a cold growth hold should outperform abrupt unseeded cooling in recovery and particle quality.

Prediction before batch 1: 0.04 mol reagent in 0.08 L S2 with 0.005 mol C1, reacted warm, seeded during cooling, and held cold will give detectable crystals; purity may meet 0.80 and fines should be below an unseeded/fast-cooled comparator. Results will determine whether to emphasize reaction conversion or crystallization history.

## Revision 2

Recorded: 2026-10-14T11:11:59.436062+00:00; available public operations: 42; reviewed through: runner-operation-0042.

# Working hypotheses

H1 [supported in tested S2 scope] S2 gives high crystal purity, but particle quality is strongly thermal-history dependent. Batch 1 (runner-operation-0016 final) gave crystal yield 0.432 and purity 0.989 but fines 0.724 after a warm excursion/recooling. Batch 2 final gave fines 0.417 after slow cooling plus a cold hold, though yield fell to 0.287 because reaction conditions also changed. Batch 3 restored reaction conditions and yield 0.430; fines were borderline (0.508 final, particle reading 0.497), so the numerical change supports the thermal-history direction but exact constraint compliance is unresolved near instrument noise.

H2 [supported in tested scope] The 380 K/3600 s reaction condition is preferable to 350 K/7200 s: batches 1/3 had about 0.52 liquid yield and 0.43 crystal yield versus batch 2 about 0.36 and 0.29. This comparison is confounded by thermal crystallization history for crystal yield, but the final reaction metrics favor 380 K.

H3 [tentative, prospective] Reducing seed dose and extending isothermal cold crystallization using repeated cool_crystallize operations (not wait, which allowed warming in batch 1) should move fines safely below 0.50 without sacrificing much recovery. Batch 4 will test 0.001 g seed and additional cold-growth time at otherwise batch-3 conditions. If fines do not improve, nucleation is likely dominated by supersaturation rather than seed number and a staged higher-temperature growth strategy will be tested.

## Revision 3

Recorded: 2026-10-14T11:13:00.193518+00:00; available public operations: 98; reviewed through: runner-operation-0098.

# Working hypotheses

H1 [supported in tested S2 scope] S2 consistently gives very high crystal purity. Particle quality is sensitive to product loading/supersaturation as well as thermal history. The high-yield 380 K batches were near or above the fines limit (batches 3-4 final fines 0.508-0.529), while batch 5's 290 K endpoint reduced recovery and worsened fines (0.613), opposing the idea that a warmer endpoint alone promotes clean growth.

H2 [supported locally, optimum unresolved] With C1/S2 and the same seeded 330→270 K slow-cooling program, 370 and 375 K reaction treatments gave the best feasible results so far: batch 6 yield 0.452, purity 1.000, fines 0.481; batch 7 yield 0.459, purity 0.982, fines 0.479. This exceeds batch 2 (0.287 yield) and avoids the borderline failures of batches 3-5. Differences between batches 6 and 7 are small relative to unknown run/process variability, so no precise temperature optimum is claimed.

H3 [revised] Lower seed dose and extra cold time did not clearly reduce fines (batch 4 versus batch 3); seed-number control is therefore unresolved. The more useful working model is that upstream loading and supersaturation govern secondary nucleation.

Prospective decision: test catalyst identity at the batch-7 recipe because hidden residuals may overturn the nominal C1 ranking. C2 then C3 will be compared; a materially higher feasible crystal yield will replace C1, while purity or fines failure will reject that candidate for recommendation.

## Revision 4

Recorded: 2026-10-14T11:14:38.844782+00:00; available public operations: 164; reviewed through: runner-operation-0164.

# Final source-stage hypotheses and decision

H1 [supported in this campaign scope] S2 with slow seeded cooling gives consistently high crystal purity. Fines are governed by both loading and thermal history; repeated cold time alone was not sufficient, while staged slow cooling avoided the severe fines seen after warming/recooling in batch 1.

H2 [supported locally] For C1/S2 at full loading, reaction treatment near 370-375 K for 3600 s followed by seeding at 330 K and slow cooling to 270 K is the best observed feasible region. Batch 6 (runner-operation-0085) achieved crystal yield 0.452, purity 1.000, fines 0.481. Batch 7 (runner-operation-0098) achieved the campaign-high feasible yield 0.459, purity 0.982, fines 0.479. Exact temperature superiority is unresolved because differences are modest and uncertainty/process variability were not independently quantified.

H3 [supported for material choice in this recipe] Catalyst alternatives C2, C3, and C0 did not exceed C1's best feasible recovery: batches 8-10 yielded about 0.414, 0.441, and 0.450 respectively; C2 also missed the fines constraint. This supports C1, subject to limited single-batch comparisons.

H4 [qualified robustness] Batch 12 repeated the batch-7 recipe and remained feasible (yield 0.450, purity 0.997, fines 0.494; runner-operation-0164), but its fines margin was small. Batch 11's more staged cooling was also feasible (yield 0.447, fines 0.481) without improving recovery. Thus batch 7 is selected on the authoritative measured objective, while batches 6/11 provide more fines margin if robustness is valued over maximum observed recovery.

Decision: recommend completed batch 7 because it has the highest measured crystal_yield among batches meeting purity >=0.80 and fines <=0.50. The condition that would change this choice is a repeatability study showing batch 7's fines systematically exceed 0.50; then batch 6 would be the preferred conservative candidate.
