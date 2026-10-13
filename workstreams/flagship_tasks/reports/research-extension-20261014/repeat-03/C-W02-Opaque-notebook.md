# repeat-03 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:01:43.389295+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypothesis notebook

## Prior expectations (before batch 1)
H1 [tentative] Reaction outcome will vary materially across anonymous catalyst/solvent identities; screen combinations before optimizing crystallization. Prediction: at least one combination gives higher target yield/selectivity without degradation.

H2 [tentative] For a productive liquor, moderate seed addition followed by slow cooling and a low-temperature hold should increase seed-excluded crystal recovery and reduce fines relative to abrupt unseeded cooling. Excess seed could depress the seed-excluded metric or increase counts of fines. Prediction: a seeded slow-cool batch will meet purity >=0.80 and fines <=0.50 more reliably than a rapid/unseeded batch.

Decision: use early batches for broad material/thermal screening with one paid diagnostic per batch where helpful, then replicate/refine the best feasible process. These claims will be revised only from observed public evidence.

## Revision 2

Recorded: 2026-10-13T18:03:18.538198+00:00; available public operations: 48; reviewed through: runner-operation-0048.

# Source-stage hypothesis notebook

## H1 [supported for paired combinations; identities unresolved]
At 370 K/3600 s and fixed charge, paired C0/S0 gave the strongest reaction outcome observed (batch 1 final assay: yield ~0.702, selectivity ~0.704), followed by C1/S1 (batch 2: ~0.619/~0.631); C2/S2 and C3/S3 were worse (events runner-operation-0012, -0024, -0036, -0048). Catalyst and solvent effects are confounded because identities were paired. Decision: prioritize C0/S0 for crystallization optimization, while treating individual identity attribution as unresolved.

## H2 [supported in tested scope]
A low seed dose (0.005 g), slow cooling to 300 K over 14400 s, and growth hold produced a feasible solid for C1/S1: purity ~0.986, fines ~0.418, recovery ~0.472 (runner-operation-0024). By contrast, faster/deeper cooling with 0.020 g seed gave recovery ~0.550 but fines ~0.877 (runner-operation-0012). The comparison is confounded by material pair and endpoint, but supports testing the gentle profile with C0/S0. Prediction made now: C0/S0 under the batch-2 thermal profile will retain purity >=0.80 and fines <=0.50, with recovery at least comparable to 0.47.

## H3 [tentative]
Within a fixed productive material pair, lowering the endpoint from 300 K should raise recovery but risks secondary nucleation/fines. Long low-agitation holds may allow growth/ripening and restore compliance. Decision: bracket 295–300 K first, then test staged cooling/annealing if fines rise.

## Revision 3

Recorded: 2026-10-13T18:05:01.063568+00:00; available public operations: 144; reviewed through: runner-operation-0144.

# Source-stage hypothesis notebook

## H1 [supported for process selection; causal identities partly unresolved]
The C1/S1 pair is the most useful observed compromise: it repeatedly supported high-purity, low-fines crystallization under gentle cooling (batches 2, 6–12), whereas C0/S0 gave stronger reaction yield but high fines even under the tested gentle profile (batch 5; runner-operation-0060). The initial paired screen cannot separate catalyst from solvent causality.

## H2 [supported in C1/S1 scope]
With 0.04 mol reagent, 0.075 L S1, 0.005 mol C1, reaction at 370 K for 3600 s, low seed dose, cooling over 14400 s, and a 14400 s low-agitation hold, endpoints from 295 down to 250 K all met purity >=0.80 and fines <=0.50 (runner-operation-0072 through -0144). Recovery increased numerically as the endpoint fell: ~0.511 (295 K), 0.532 (290 K), 0.550 (285 K), 0.552 (280 K), 0.564 (275 K), 0.572 (265 K with 0.002 g seed), and 0.593 (250 K with 0.002 g seed). Because endpoint and seed changed at 265 K, the seed contribution is unresolved.

## H3 [qualified]
Deep slow cooling increased observed recovery without violating the fines constraint in this material pair, but fines at 250 K were ~0.471, closer to the 0.50 boundary than at 265 K (~0.399). Final-assay noise is declared (fines std 0.018, recovery std 0.01), so the 250 K recovery advantage over 265 K is numerical rather than strong replicated evidence. Still, batch 12 has the highest observed compliant recovery (~0.593), purity ~0.999, and observed fines ~0.471 (runner-operation-0144); select it for the stated objective. A robustness-first decision would instead favor batch 11.

## Unresolved tests
Replicate batches 11 and 12; independently vary seed dose at fixed endpoint; cross C1 with other solvents and S1 with other catalysts; test staged cooling/annealing to retain batch-12 recovery while increasing fines margin.
