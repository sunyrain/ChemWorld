# C-12 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-12T17:51:07.544574+00:00; public operations available: 0; reviewed through: not specified.

# Working hypotheses

H1 [tentative] Solvent S2 should favor larger, purer crystals because its dossier indicates high growth and low occlusion/nucleation, while S1 may offer a useful intermediate; S0 risks fines and occlusion. Test with otherwise comparable seeded cooling.

H2 [tentative] Catalyst C1 is the safest initial activity choice; C3 may improve reaction throughput but could increase byproduct if pushed hot/long. Test reaction conversion/selectivity before crystallization where useful.

H3 [tentative] Slow cooling with a modest seed dose and a low-temperature hold should reduce fines versus rapid unseeded cooling. Higher seed dose may improve recovery but could reduce seed-excluded yield denominator behavior and size; use dose and thermal history as later optimization factors.

Initial batch prediction: 0.04 mol reagent, 0.005 mol C1, 0.08 L S2, moderate hot reaction, then seed/slow cool/hold/filter should meet purity and fines constraints and provide at least 0.10 crystal recovery. A failure would redirect catalyst/temperature or crystallization solvent strategy.

---

## Revision 2

Recorded: 2026-10-12T17:52:25.629021+00:00; public operations available: 25; reviewed through: runner-operation-0025.

# Working hypotheses

H1 [supported in tested S2 scope] S2 can give very high crystal purity. Batch 1 (event runner-operation-0015) produced purity 0.987 but its interrupted cooling/ambient-warming history left fines near the limit (0.506) and recovery 0.392. Batch 2 (runner-operation-0025), with 340 K/1800 s reaction, 0.01 g seed and uninterrupted 14,400 s cooling to 250 K, improved recovery to 0.439 and fines to 0.384 while retaining purity 0.984. This supports slow uninterrupted deep cooling rather than the nominal low-temperature hold implemented by `wait`, which warmed the vessel.

H2 [unresolved] Reaction conditions affect crystallization feed quality and perhaps recovery. The 360 K/3600 s batch had high degradation warning (0.194) versus 0.058 at 340 K/1800 s, but seed dose and cooling history were confounded. Test catalysts and milder thermal exposure using the same slow-cooling crystallization.

H3 [supported in tested comparison, confounded] Lower seed (0.01 versus 0.02 g) plus uninterrupted slow cooling coincided with fewer fines and larger crystals. Seed effect alone remains unresolved; test a 0.05 g dose under the batch-2 thermal program.

Decision: treat batch 2 as current benchmark meeting both constraints; optimize recovery while preserving purity >=0.80 and fines <=0.50. A repeated failure of batch-2-like runs would weaken the thermal-history claim.

---

## Revision 3

Recorded: 2026-10-12T17:54:17.989903+00:00; public operations available: 144; reviewed through: runner-operation-0144.

# Final working hypotheses

H1 [supported in S2/C3 scope] A deliberately staged slow cooling sequence (320, 300, 280, 260, then 250 K; 14,400 s at each step) suppresses fines while maintaining high crystallization recovery. Under C3 at 340 K/1800 s and 0.01 g seed, batch 9 (runner-operation-0102) gave recovery 0.526, purity 0.983 and fines 0.315; the same recipe in batch 11 (runner-operation-0130) gave 0.518, 0.994 and 0.307. Thus the constraint-satisfying behavior repeated, although numerical differences should not be overinterpreted beyond assay uncertainty and process variability.

H2 [supported, scope limited] C3 improves recovery relative to tested C0/C1/C2 feeds but needs staged cooling. A single long C3 cool (runner-operation-0065) reached recovery 0.524 but failed fines at 0.540. Two-stage cooling and a reheat/recool (runner-operation-0076 and runner-operation-0088) still narrowly failed fines. Full staging in batches 9 and 11 resolved that tradeoff. The 330 K variant (runner-operation-0116) had lower recovery and failed fines, so 340 K is retained for this catalyst/solvent recipe.

H3 [supported for size, unresolved for recovery] Increasing seed from 0.01 to 0.05 g under full staging (batch 12, runner-operation-0144) retained recovery/purity/fines (0.521/0.996/0.311) and increased the measured size index to 0.105, but did not exceed batch 9 recovery. Seed-excluded recovery therefore does not show a clear benefit from the larger seed dose.

H4 [supported] S2 provides strong impurity rejection across tested conditions: all principal optimized batches had crystal purity about 0.98-1.00 even when upstream selectivity was only moderate. This conclusion is empirical for the anonymous benchmark materials, not a real-material identity claim.

Decision: recommend completed batch 9 because it has the highest observed crystal recovery among batches satisfying purity >=0.80 and fines <=0.50 (0.526 recovery, 0.983 purity, 0.315 fines). Batch 11 is the direct supporting repeat; batch 12 is a viable larger-size alternative. I would change the selection only if repeatability data showed batch 9's recovery advantage over batches 11-12 was noise and size robustness were prioritized.

---
