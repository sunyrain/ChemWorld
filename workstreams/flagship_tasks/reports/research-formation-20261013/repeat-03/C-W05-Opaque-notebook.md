# repeat-03 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:22:23.836394+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

H1 [tentative] Reaction performance will vary strongly with anonymous catalyst and solvent; initial batches will screen combinations at full common loading (0.04 mol reagent, 0.005 mol catalyst, 0.08 L solvent) under otherwise comparable thermal history. A supported combination should give higher conversion/selectivity by HPLC and acceptable final crystal purity.

H2 [tentative] For crystallization, moderate seed loading near 1 g, controlled cooling from a fully dissolved hot state, and a cold growth hold should reduce fines versus unseeded rapid cooling. Slower cooling/longer hold is expected to improve recovery and size until degradation or secondary nucleation intervenes.

Decision: use early batches for broad material/process screening, then spend later batches on promising conditions and thermal-history refinements. Revise if particle or assay evidence contradicts these expectations.

## Revision 2

Recorded: 2026-10-13T12:24:08.464719+00:00; available public operations: 42; reviewed through: runner-operation-0042.

# Working hypotheses

H1 [supported only for process feasibility] Full loading at 360 K gives near-complete conversion for tested C0/S0, C1/S0, and C2/S1 combinations, but selectivity differs and is confounded with solvent and catalyst changes (final assays in events runner-operation-0017, -0030, -0042). Do not assign a catalyst ranking yet.

H2 [supported in tested scope] Deep cooling of S0 material to 270–280 K produced high recovery (~0.45) but overwhelmingly fine crystals (fines ~0.96–0.98), failing the <=0.50 constraint (events -0017, -0030). In contrast, slow 14,400 s cooling of C2/S1 material to 300 K gave feasible fines ~0.436, purity ~0.988, and recovery ~0.350 (event -0042). Solvent identity is confounded with endpoint/rate, so the improvement cannot yet be assigned to either.

Prediction: near the S1/300 K process, modestly lower endpoints may raise recovery while approaching the fines limit. Test 295 and 290 K under otherwise matched conditions; if fines remain <=0.50, prefer the higher-recovery endpoint. Also screen remaining solvents at 300 K.

## Revision 3

Recorded: 2026-10-13T12:26:22.218195+00:00; available public operations: 152; reviewed through: runner-operation-0152.

# Final source-stage hypotheses and decision

H1 [supported in tested scope] Solvent S1 with catalyst C2 and a 0.05 g seed, followed by a single slow 14,400 s cooling stage, defines a broad feasible crystallization window. From 300 to 260 K, observed recovery increased from ~0.350 to ~0.480 while fines stayed ~0.42–0.44 and purity stayed well above 0.80 (events runner-operation-0042, -0054, -0066, -0078, -0090, -0102). The monotonic recovery trend is larger than assay noise over the full range; small adjacent differences are not individually decisive.

H2 [supported] Material choice dominates fines behavior in the tested recipes: S0 deep-cooling batches had fines ~0.96–0.98 (events -0017, -0030), while matched-style slow cooling with S1 gave feasible fines. S2 at 260 K also met constraints but had lower recovery (~0.392; event -0140). Catalyst effects remain confounded and are not separately claimed.

H3 [unresolved] At 250–255 K and with two-stage cooling, observed recovery remained near 0.472–0.484 but fines approached the 0.50 limit (events -0114, -0128, -0152). Differences among the highest observed recoveries are smaller than the stated crystal-yield assay noise (~0.01), so there is no persuasive recovery advantage over the single-stage 260 K batch.

Decision: recommend batch 8 (event -0102): recovery 0.4797, purity 0.9777, fines 0.4172. It sacrifices no demonstrated recovery relative to nominally higher batches 9/10 while retaining materially more fines margin and a simpler one-stage cooling history. This preference would change if replicated assays established a real recovery gain for the 250 K/two-stage process without raising true fines above 0.50.
