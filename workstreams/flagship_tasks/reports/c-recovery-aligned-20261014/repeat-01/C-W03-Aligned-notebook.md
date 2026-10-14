# repeat-01 / C-W03-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:35:27.944821+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Solvent S2 plus catalyst C1 is the best initial combination because the dossier suggests high reaction activity, low solubility, strong growth, and low occlusion. A moderate catalyst loading, hot reaction hold, seeded slow cooling, cold growth hold, and filtration should produce purity above 0.80, fines below 0.50, and recovery above 0.10.

H2 [tentative] Higher seed dose and slower cooling should reduce fines, whereas colder/longer terminal holds should increase recovery; excessive heat or long hot holds may increase degradation. Initial factorial batches will test material identity first, then thermal and seed variables.

Decision: start with a balanced S2/C1 recipe. Revise if direct HPLC/final assays contradict the dossier.

## Revision 2

Recorded: 2026-10-14T10:39:00.918615+00:00; available public operations: 88; reviewed through: runner-operation-0088.

# Working hypotheses after batches 1–7

H1 [supported for purity, unresolved for recovery-size tradeoff] S2/C1 generally gives high-purity crystals and approximately 0.38 overall crystal recovery under hot reaction and cooling, but particle outcomes depend sharply on thermal history. Batch 1 reached crystal_yield 0.389 and purity 0.986 but fines 0.601 (event runner-operation-0013). Batches 2–6 usually had fines near 1 despite purity near 0.98–1 (events 0028, 0039, 0052, 0064, 0076). Thus purity is robust in the tested region, while acceptable fines are not.

H2 [revised] More seed is not monotonically beneficial: 0.20 g total seed in batch 2 coincided with fines=1 (0028), whereas 0.05 g in batch 1 was less poor. Zero or 0.01 g also gave near-unity fines (0039, 0064). This is numerical evidence, not yet an isolated seed effect because histories differ.

H3 [supported locally, tradeoff unresolved] A 355 K reaction, 0.05 g seed, slow cooling to 275 K and a 7200 s ambient-warming stirred age produced excellent in-process particle attributes in batch 7 (fines 0.0017, size 0.397, event 0085). After filtration its final crystal_yield was only 0.0119 (0088), unlike batch 1's nominally similar history. The likely alternative explanations are strong sensitivity to unrecorded control configuration/temperature path or dissolution during warm aging; repeatability is unresolved.

Decision: repeat the promising particle history with explicit control configuration and intermediate particle measurement, then shorten or stop warm aging when size passes. A result with recovery >0.10 and fines <0.50 would change the current conclusion that size and recovery trade off sharply.

## Revision 3

Recorded: 2026-10-14T10:41:12.034833+00:00; available public operations: 151; reviewed through: runner-operation-0151.

# Final source-stage hypotheses

H1 [supported in tested scope] S2/C1 with a 355 K reaction and direct cold isolation gives comparatively high seed-excluded recovery (~0.37–0.39) and purity above 0.97, but the recovered solids are dominated by fines. Examples: batch 1 (yield 0.389, fines 0.601; event 0013), batch 2 (0.384, fines 1; 0028), and batch 6 (0.375, fines 1; 0076). None of these high-recovery batches satisfies the fines constraint.

H2 [supported in tested scope] Warm aging/reheat or prolonged cold aging strongly selects for large, low-fines particles but removes most seed-excluded target solids, consistent with redissolution leaving mainly the purchased seed population. Batch 8 after a 303 K warm age had yield 0.0170, purity 0.992, fines 0 (0101); batch 9 after 295 K reheating had yield 0.00793 and fines 0.0014 (0113); batch 10 after 285 K reheating had yield 0.00905 and fines 0.0113 (0125); batch 11 after 278 K reheating had negligible yield (0137). Even prolonged nominal 275 K aging gave only 0.00296 yield with fines 0.00196 in batch 12 (0151). The direction is clear despite instrument noise; the exact temperature/time boundary is unresolved.

H3 [rejected as a general remedy] Increasing seed or simply extending cooling did not recover both objectives: 0.20 g seed coincided with fines=1 (0028), while prolonged 275 K treatment ultimately sacrificed recovery (0151).

Final decision: among completed batches satisfying purity >=0.80 and fines <=0.50, batch 8 has the highest measured crystal_yield (0.0170). It is the defensible recommendation, but it misses the 0.10 feasibility target by a wide margin. No tested recipe combined recovery >=0.10 with the stated purity and fines constraints. A future campaign should densely map the very early/low-temperature aging window between immediate 275 K isolation and the first warming step, with repeated quantity-sensitive assays rather than particle measurements alone.
