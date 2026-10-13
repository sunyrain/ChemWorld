# repeat-01 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T16:55:07.839954+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Within the anonymous dossier, solvent S2 should favor larger, purer crystals because it combines higher nominal growth with lower nucleation and impurity occlusion, but its lower solubility may trade against manageable supersaturation/fines. Prediction: a seeded, slow cooling/hold process in S2 will meet purity and fines constraints more readily than rapid unseeded cooling.

## H2 [tentative]
Catalyst C1 is the best initial reaction choice from nominal activity, though fixed-world residuals could reverse the ranking. Prediction: moderate-hot reaction with C1 followed by quench will give useful target loading without excessive degradation.

## Design decision
Start with a conservative seeded S2 baseline, then vary upstream catalyst/temperature and crystallization seed dose/cooling/hold. A result with low recovery but acceptable purity/fines will motivate deeper cooling or longer growth; excessive fines will motivate slower cooling, warmer seeding, or reduced seed dose.

## Revision 2

Recorded: 2026-10-13T17:00:27.793017+00:00; available public operations: 209; reviewed through: runner-operation-0209.

# Final working interpretation

## H1 [supported only directionally; constraint unmet]
Lower upstream loading reduces the fines problem, but did not solve it in the tested range. The low-loading S1 batch (event `runner-operation-0209`) gave fines 0.865, numerically much lower than the roughly 0.987–1.000 values in the full-loading S1/S2/S3 and S0 trials, while retaining purity 0.990 and crystal recovery 0.378. Because this comparison also changes catalyst charge relative to absolute target loading and was not replicated, the magnitude remains unresolved. Testable consequence: still lower loading or a broader solvent-to-target ratio should further reduce fines, though recovery and particle mass may eventually suffer.

## H2 [rejected in tested scope]
The initial expectation that seeded slow cooling/holding in S2 would meet the fines constraint was not supported. The baseline (event `runner-operation-0013`) had high purity and recovery but fines 0.997; lower seed and longer holds (`runner-operation-0028`), high seed attempts (`runner-operation-0061`), shallow cooling (`runner-operation-0106`), and repeated thermal cycling (`runner-operation-0164`) all remained dominated by fines. Numerical differences in size/CSD were not sufficient evidence of a useful effect given single runs and measurement noise.

## H3 [unsupported in tested scope]
Post-filtration resuspension/warm treatment did not selectively remove enough fines: events `runner-operation-0092` and `runner-operation-0181` still reported fines 1.000. The treatment also reduced recovery, so it is not recommended without a substantially different solvent/temperature window.

## Material scope and decision
All completed batches met crystal purity >=0.80, but none met fines <=0.50. Solvent changes S0/S1/S2/S3 and the tested thermal histories did not establish a feasible full-loading process. Select batch 12 as the most informative/closest-to-feasible candidate because it had the lowest observed fines while preserving useful seed-excluded recovery and high purity; this is not a claim that it satisfies the quality constraints.
