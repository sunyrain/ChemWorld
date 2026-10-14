# repeat-01 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:35:25.064000+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

**H1 [tentative, pre-experiment].** Catalyst and solvent identities will materially affect reaction conversion/selectivity; an initial broad screen at equal maximum reagent loading and moderate thermal treatment should identify a productive pair. A result with higher HPLC yield/selectivity will motivate crystallization tests.

**H2 [tentative, pre-experiment].** For a productive reaction, seeded slow cooling followed by a cold hold should reduce fines and improve recovery relative to rapid unseeded cooling. This may trade off purity if the cold endpoint is too low. The first batch is an exploratory baseline; these claims will be revised only from public observations.

## Revision 2

Recorded: 2026-10-14T10:36:39.747473+00:00; available public operations: 27; reviewed through: runner-operation-0027.

# Working hypotheses

**H1 [supported in tested scope].** At 370 K for 3600 s in S0, C1 is more productive/selective than C0, though reagent loading and crystallization history are confounded. Final assays: batch 1 (event runner-operation-0014) crystal yield 0.405, reaction yield 0.475, selectivity 0.477; batch 2 (runner-operation-0027) crystal yield 0.506, reaction yield 0.608, selectivity 0.619. Test C1 across other solvents and thermal conditions.

**H2 [tentatively supported, specification unresolved].** Reducing seed from 0.05 g to 0.005 g and using staged/longer cooling increased size index from 0.062 to 0.104 and reduced fines from 0.751 to 0.521 (events runner-operation-0014, -0027), while recovery increased. Because catalyst/loading also changed and uncertainty/repeatability are unknown, causality is unresolved. Prediction: still lower seed and/or a warmer nucleation/growth hold should move fines below 0.50; retain cold finishing for recovery.

**Decision.** Favor C1/S0 as current reaction baseline, but screen material identities while refining a low-seed staged cooling sequence. Quality gate is purity >=0.80 and fines <=0.50; batch 2 narrowly misses fines.

## Revision 3

Recorded: 2026-10-14T10:38:52.047659+00:00; available public operations: 157; reviewed through: runner-operation-0157.

# Final working hypotheses

**H1 [supported in tested scope].** C1/S2 was the best tested material pair for overall crystal recovery under the common low-seed staged cooling history. At 370 K, batch 4 produced crystal yield 0.507 with purity 1.000 and fines 0.304 (runner-operation-0053), versus C2/S2 yield 0.453 (runner-operation-0079) and C3/S2 yield 0.469 (runner-operation-0092). Solvent comparisons with C1 also favored S2 over S1 and S3, although these are single batches.

**H2 [supported in this scope].** A low seed dose (0.001 g) and two long cooling stages (325 K then 290 K, 14400 s each) gave acceptable fines in batches 3–7 and 9–11. Batch 4 achieved 0.304 fines (runner-operation-0053), and higher-temperature reaction histories subsequently gave 0.220, 0.146, and 0.138 fines in batches 9–11 (runner-operation-0118, -0131, -0144). The seed/cooling effect remains partly confounded with upstream changes, so extrapolation outside these materials is uncertain.

**H3 [supported over 350–430 K; nonmonotone beyond].** With C1/S2 and the common crystallization sequence, shorter/hotter reaction treatment improved selectivity and crystal recovery: 350 K/7200 s gave crystal yield 0.387 (runner-operation-0105), 390 K/1800 s 0.627 (runner-operation-0118), 410 K/1200 s 0.677 (runner-operation-0131), and 430 K/900 s 0.694 (runner-operation-0144). Batch 11 met both quality gates (purity 1.000, fines 0.138). The 450 K/600 s variant had high reaction yield/selectivity but virtually no recovered crystals (crystal yield 0.003; runner-operation-0157), rejecting monotone extrapolation and suggesting a sharp upstream/solid-state or solubility-history failure.

**Decision.** Recommend completed batch 11. It has the highest qualifying crystal recovery (0.694 observed), high purity, and ample fines margin among completed batches. Batch 12 is not recommended despite high reaction yield because overall crystal recovery is the authoritative objective.
