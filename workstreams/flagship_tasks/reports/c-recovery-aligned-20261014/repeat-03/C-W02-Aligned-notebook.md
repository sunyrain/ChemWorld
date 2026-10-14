# repeat-03 / C-W02-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:44:46.514357+00:00; available public operations: 0; reviewed through: None.

# Crystallization hypotheses

## H1 [tentative; pre-experiment]
Within the anonymous materials, solvent S2 is the leading prior for high-purity, coarse crystals because its dossier combines low solubility and nucleation with high growth and low impurity occlusion; catalyst C1 is the leading robust reaction prior. A moderate reagent concentration, near-maximum catalyst loading, hot reaction hold, slow cooling, modest seeding, cold growth hold, and filtration should yield >0.10 seed-excluded recovery while meeting purity >=0.80 and fines <=0.50.

Predicted contrasts: S0 should make more fines/occlusion; S1 may be a safer intermediate; excessive seed or rapid cooling may increase fines. Early batches will screen catalyst/solvent and thermal history; later batches will refine the best compliant recovery. This claim will change if final assays show low conversion with C1/S2, poor purity, or persistent fines.

## Revision 2

Recorded: 2026-10-14T11:50:17.064735+00:00; available public operations: 241; reviewed through: runner-operation-0241.

# Crystallization hypotheses and conclusions

## H1 [partly supported, quality objective not achieved]
The dossier correctly suggested that S2 can support high-purity recovery, but it did not yield coarse material in the tested operating window. C0 outperformed the initially preferred C1 on reaction selectivity under the compared (confounded) conditions: the C0/S2 batch gave higher HPLC selectivity and later recovery (events runner-operation-0021, runner-operation-0027) than the C1/S2 baseline (runner-operation-0007, runner-operation-0014). Catalyst/time/temperature were not independently replicated, so the catalyst effect is supported only for this tested recipe family.

## H2 [supported in tested scope]
Fines control, not purity or recovery, was the binding limitation. All 12 final assays had purity above 0.97, and several had recovery above 0.5, but every final fines estimate was about 0.987–1.000 (final assay events runner-operation-0014 through runner-operation-0241). Thus no completed batch met fines <=0.50. The best measured recovery was batch 8 (event runner-operation-0120: recovery 0.6404, purity 0.9810, fines 0.9870), so it is the least-bad recommendation only by recovery, not a constraint-feasible process.

## H3 [rejected/shelved]
Within this campaign, simply extending cold holds, partial reheating/recooling, or increasing seed dose did not solve fines. Long cold aging (batch 9), a reheat/recool cycle (batch 5), 0.5 g warm seeding (batch 7), and 3 g cold seeding (batch 12) all retained near-unity fines. Numerical differences in size and fines were noisy and not replicated; no beneficial causal seed or hold effect is claimed.

## Decision
Recommend batch 8 because it has the highest observed seed-excluded recovery and compliant purity, while explicitly stating that it violates the fines constraint. A future campaign should seek a qualitatively different agglomeration/classification or nucleation-control regime rather than repeat the explored seed/hold changes.
