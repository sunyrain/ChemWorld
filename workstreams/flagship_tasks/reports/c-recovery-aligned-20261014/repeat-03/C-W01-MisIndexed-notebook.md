# repeat-03 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:43:38.189320+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Catalyst C1 and solvent S1 should favor reaction conversion because their nominal activity is highest; C2/S2 may instead favor cleaner, larger crystals because S2 has low solubility, low nucleation, high growth, and low occlusion.

H2 [tentative] A hot reaction followed by controlled cooling, modest seeding, and a growth hold should outperform an unseeded rapid quench in fines while preserving recovery. Too much seed may inflate particle counts and reduce the seed-excluded yield basis.

Plan: first screen catalyst/solvent combinations under comparable charge and thermal history, then vary seed dose and cooling/hold history around the best feasible chemistry. Results would overturn the priors if measured conversion/purity or crystal recovery rankings disagree.

## Revision 2

Recorded: 2026-10-14T11:44:46.505634+00:00; available public operations: 26; reviewed through: runner-operation-0026.

# Working hypotheses

H1 [supported in tested comparison, chemistry confounded] C1/S2 at 340 K gave higher final crystal recovery (0.444) than C1/S1 at 370 K (0.253), while both had final purity about 0.98 (events runner-operation-0013, -0026). Temperature and solvent changed together, so the causal source is unresolved. The HPLC direction (less byproduct and higher selectivity/yield in batch 2, runner-operation-0018 vs -0005) motivates retaining S2 and moderate reaction temperature.

H2 [challenged] Increasing seed from 0.02 g to 0.05 g did not improve fines under changed solvent/thermal conditions; final fines rose from about 0.70 to 1.00 (events -0013, -0026). This is not an isolated seed-dose estimate because chemistry and cooling also changed. Next test much lower seed with staged slow cooling; if fines remain high, examine unseeded or reheating/ripening histories.

Decision: prioritize meeting fines <=0.50 before further recovery optimization, while screening catalyst/temperature only when crystallization history is comparable.

## Revision 3

Recorded: 2026-10-14T11:45:31.452185+00:00; available public operations: 67; reviewed through: runner-operation-0067.

# Working hypotheses

H1 [supported in current scope] C1/S2 at 340 K reproducibly gives high conversion, final purity near 1, and recovery roughly 0.44–0.48 (events runner-operation-0026, -0040, -0053). C1/S1 at the same temperature gave lower recovery 0.414 (event -0067).

H2 [rejected as simple seed-dose claim] Across 0, 0.005, and 0.05 g seed in S2, final fines stayed about 0.99–1.00 (events -0026, -0040, -0053). Seed dose alone is not a useful lever in this tested slow/deep-cooling regime.

H3 [tentative] Deep cooling to 260 K and prolonged holds may drive secondary nucleation; even S1 reached fines 1.00 under that history (-0067), whereas the shallower 278 K endpoint in batch 1 had fines 0.70 (-0013). Next use partial reheating/redissolution after initial crystallization and a shallower recool to test whether dissolution/ripening can suppress fines. A final fines value below 0.50 would support this route.

## Revision 4

Recorded: 2026-10-14T11:46:21.450254+00:00; available public operations: 106; reviewed through: runner-operation-0106.

# Working hypotheses

H1 [supported in current scope] C1/S2 at 340 K remains the strongest recovery chemistry tested, but deep post-quench cooling causes essentially all-fines product.

H2 [supported for one batch, needs repeat/near-boundary caution] Avoiding the abrupt quench and cooling directly from 340 to 310 K with 0.02 g seed plus two warm growth holds produced recovery 0.375, purity 0.980, and fines 0.490 (runner-operation-0106), the first batch meeting both quality constraints. Its particle result before filtration was consistent at fines 0.502 but lies near the cutoff (runner-operation-0103); assay noise and process repeatability matter.

H3 [tentative] Warm holds allow growth to consume supersaturation without the secondary nucleation caused by deep cooling, at a recovery cost relative to cold S2 batches. Next compare shorter versus longer warm holding and a slightly lower endpoint to seek a safer fines margin and higher recovery. A repeat above 0.50 fines would weaken confidence in the boundary-feasible recipe.

## Revision 5

Recorded: 2026-10-14T11:46:57.310055+00:00; available public operations: 140; reviewed through: runner-operation-0140.

# Working hypotheses

H1 [supported in tested scope] The dominant fines lever is thermal history, not seed dose: direct warm cooling to 310–312 K yields fines near 0.49–0.51, versus about 1.0 after quench/deep cooling.

H2 [supported directionally, magnitude unresolved] A single 310 K hold failed narrowly (fines 0.504, recovery 0.366; runner-operation-0117); two holds passed narrowly with higher recovery 0.375 (runner-operation-0106); three holds failed narrowly at fines 0.514 and recovery 0.367 while degradation increased (runner-operation-0129). These differences are comparable to assay noise and uncontrolled process variation, so no monotonic hold-time effect is established.

H3 [supported for one batch] Raising the endpoint to 312 K with two holds passed at purity 0.993 and fines 0.496, but reduced recovery to 0.350 (runner-operation-0140). Thus 310 K is the higher-recovery candidate, while 312 K is not demonstrably safer given near-boundary noise.

Decision: use the last batch as an exact 310 K/two-hold repeat. Recommend the highest-recovery completed batch that actually satisfies both final-assay constraints; acknowledge boundary uncertainty.

## Revision 6

Recorded: 2026-10-14T11:47:18.265498+00:00; available public operations: 151; reviewed through: runner-operation-0151.

# Final source-stage interpretation

H1 [supported in this campaign] Direct warm crystallization is essential for acceptable particle quality. The best deep-cooled S2 batches had higher recovery (up to 0.484) but fines near 1.0, so they fail the stated constraint.

H2 [supported, boundary-limited] The C1/S2 recipe reacted at 340 K, seeded with 0.02 g before direct 14,400 s cooling to 310 K, then held twice for 14,400 s at low stirring. Batch 8 met both constraints with crystal yield 0.375, purity 0.980, and fines 0.490 (runner-operation-0106). Exact-repeat batch 12 gave yield 0.361, purity 0.994, and fines 0.505 (runner-operation-0151), showing that fines performance is borderline rather than robust.

H3 [supported alternative] A 312 K endpoint with two holds also met constraints in batch 11 (yield 0.350, purity 0.993, fines 0.496; runner-operation-0140), but did not create a convincing fines margin and sacrificed recovery.

Decision: recommend completed batch 8 because it has the highest measured seed-excluded recovery among batches whose final assay actually satisfies purity >=0.80 and fines <=0.50. The condition for changing this decision would be a robustness-oriented criterion favoring batch 11, or replicate evidence that batch 8's true fines rate exceeds the limit.
