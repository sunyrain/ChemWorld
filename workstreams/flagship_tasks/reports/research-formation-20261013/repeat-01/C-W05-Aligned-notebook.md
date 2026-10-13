# repeat-01 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:37:06.932137+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

**H1 [tentative].** Solvent S2 should favor larger, purer crystals because its nominal growth is highest and impurity occlusion/nucleation lowest, but its low solubility may require a hot dissolution step and could trade purity against recovery. A seeded, slow cool followed by a cold hold should exceed the 0.10 recovery feasibility target with fines below 0.50.

**H2 [tentative].** Catalyst C1 is the safest first reaction choice from its strong nominal activity and lower variability than C2/C3. A hot reaction with moderate catalyst loading should give adequate target concentration while limiting degradation. Experimental HPLC and final assays override these priors.

**Plan.** First establish a complete S2/C1 seeded slow-cooling baseline; subsequent batches vary catalyst, solvent, seed dose, reaction time/temperature, cooling rate, and cold hold. I will retain conditions only when purity and fines constraints are met.

## Revision 2

Recorded: 2026-10-13T11:38:37.023994+00:00; available public operations: 46; reviewed through: runner-operation-0046.

# Working hypotheses after four batches

**H1 [supported in tested S2 scope].** A long single seeded cool from the hot reaction mixture to 270 K produces constraint-feasible crystals. Relative to the shorter cool plus ambient-warming hold in batch 1, batches 2–4 had substantially lower measured fines (~0.36–0.38 versus 0.54) and retained very high purity; the temperature history is confounded with catalyst and the difference is not yet a replicate (final assays: runner-operation-0013, -0024, -0035, -0046). Test consequence: retain the long cold trajectory while screening solvent and then cooling details.

**H2 [tentatively supported].** Under identical S2/370 K/1 h/seeded-long-cool conditions, C0 gave the highest observed crystallization recovery (0.433) and reaction selectivity (0.551) among C0, C2, C3, while all passed purity/fines (runner-operation-0024, -0035, -0046). This is a numerical ranking from single noisy runs; catalyst may affect target/impurity composition but recovery is normalized to pre-separation target. Use C0 for solvent/thermal optimization unless later data contradict it.

**H3 [unresolved].** S2 nominal low solubility/high growth may be responsible for good recovery and low fines. Screen S1, S0, and S3 using the C0 long-cool reference. If a different solvent improves recovery while remaining purity >=0.80 and fines <=0.50, shift optimization to it.

## Revision 3

Recorded: 2026-10-13T11:39:25.557687+00:00; available public operations: 91; reviewed through: runner-operation-0091.

# Working hypotheses after solvent screen and seed-timing test

**H1 [supported in tested scope].** S1 with C0 and a seeded 14,400 s cool to 270 K is currently the best constraint-feasible process: batch 5 recovery 0.517, purity 0.975, fines 0.412 (runner-operation-0057). S0 gave similar recovery but severe fines (0.833), and S3 had both lower recovery and severe fines; S2 was feasible but lower recovery (runner-operation-0068, -0079, -0024).

**H2 [revised].** Cooling lower to 260 K after an unseeded pre-cool to 320 K increased observed recovery to 0.556 but fines rose to 0.556, failing the constraint (runner-operation-0091). This does not isolate final temperature from seed timing/two-stage history. Prediction: putting seed in before any cooling and lengthening the upper-temperature segment may suppress secondary nucleation enough to retain the recovery gain with fines <=0.50.

**H3 [decision].** Continue with S1/C0. Optimize seed timing and staged cooling first; then test seed dose and reaction severity. Retain batch 5 as fallback.

## Revision 4

Recorded: 2026-10-13T11:40:07.960856+00:00; available public operations: 127; reviewed through: runner-operation-0127.

# Late-stage optimization hypotheses

**H1 [supported for S1/C0].** Seeding before cooling and staging through 320 K improved the feasible recovery from 0.517 (batch 5) to about 0.531–0.532 (batches 9–10), with fines ~0.425–0.428 (runner-operation-0103, -0115). Reducing seed from 0.05 g to 0.01 g produced a larger measured size but essentially unchanged recovery/fines; this single comparison does not establish a seed-dose effect.

**H2 [supported qualitative thermal effect].** Extending the 320 K stage from 7,200 to 14,400 s at 0.01 g seed sharply reduced observed fines to 0.243 and raised CSD quality, while recovery was 0.523 (runner-operation-0127). The magnitude exceeds assay noise but remains unreplicated and may include stochastic process variation.

**H3 [final test prediction].** With seed present before cooling and the longer 320 K stage, lowering the final target from 270 to 260 K should raise recovery above the current feasible maximum (~0.532); the longer upper stage may keep fines <=0.50. If fines fail, batch 10 is the recovery-maximizing fallback, while batch 11 is the more robust particle-quality option.

## Revision 5

Recorded: 2026-10-13T11:40:39.216547+00:00; available public operations: 139; reviewed through: runner-operation-0139.

# Final source-stage conclusions

**H1 [supported in the explored domain].** The best observed process used C0/S1, 0.04 mol reagent in 0.08 L solvent with 0.005 mol catalyst, reaction at 370 K for 3,600 s, 0.01 g seed added before cooling, staged cooling to 320 K over 14,400 s and then 260 K over 14,400 s, followed by filtration. Batch 12 achieved the highest constraint-feasible crystal recovery, 0.542, with purity 0.992 and fines 0.259 (runner-operation-0139). It also had the campaign's highest observed score and strong CSD quality.

**H2 [supported qualitative relationship, bounded scope].** Within C0/S1 tests, extended staged cooling with seed present before cooling reduced fines relative to a shorter stage or delayed seeding. Lowering the final target from 270 K in batch 11 to 260 K in batch 12 numerically increased recovery (0.523 to 0.542) without sacrificing the fines constraint (runner-operation-0127, -0139). These are single runs with coupled thermal changes across the broader set, so precise causal magnitudes and repeatability remain unresolved.

**H3 [rejected as general prior].** The nominal dossier suggestion that S2 would be the best crystallization solvent did not hold for recovery in this world: S1 gave higher feasible recovery under matched long-cool conditions. S0/S3 produced excessive fines in the tested recipe.

**Decision.** Recommend completed batch 12. Batch 10 is a shorter-cycle fallback with recovery 0.532, purity 0.975, fines 0.428; batch 11 is a 270 K staged-cooling robustness fallback with especially low fines. I would change the recommendation only if replicate data showed the batch-12 recovery advantage was not reproducible or if unreported cycle-time constraints outweighed its gain.
