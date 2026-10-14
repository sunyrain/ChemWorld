# repeat-03 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:42:39.617213+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment expectations

H1 [tentative] Reaction outcome will depend strongly on anonymous catalyst/solvent identity and thermal exposure. A broad screen should identify a productive pair; HPLC conversion/selectivity before crystallization will discriminate reaction failure from isolation failure.

H2 [tentative] For a productive liquor, controlled cooling with modest seeding and sufficient growth hold should raise recovery while avoiding fines. Rapid/deep cooling may raise yield but risk the fines constraint; a slow cool and post-seed hold is the initial baseline.

Decision: begin with a representative C0/S0 batch at moderate reaction temperature, then revise using measurements and final assays. Results inconsistent with product formation will trigger material/temperature screening rather than crystallization fine-tuning.

## Revision 2

Recorded: 2026-10-14T11:44:38.833079+00:00; available public operations: 69; reviewed through: runner-operation-0069.

# Working hypotheses after batches 1–5

H1 [supported in screened scope] All tested material pairs at 360 K/1 h produced substantial reaction yield, but selectivity varies. C0/S0 and C1/S0 were highest among current HPLC estimates (~0.64); C2/S1 was lowest (~0.41). Because catalyst and solvent were jointly changed in later batches, their individual effects remain unresolved (events runner-operation-0006, -0019, -0033, -0047, -0061).

H2 [supported qualitatively] Solvent/solid-form conditions dominate particle distribution. S0 batches gave very high fines (~0.89–0.90), whereas S1–S3 diagonal screens gave ~0.52–0.60 under slow staged cooling. Exact solvent causality is confounded with catalyst, but S2 is the most promising tested condition: batch 4 had crystal yield ~0.46, purity at the upper bound, and fines ~0.52 (runner-operation-0055).

H3 [unresolved] Slower staged cooling increased measured size relative to the faster batch-1 recipe, but did not materially cure S0 fines; the numerical changes are confounded by catalyst/seed dose and single noisy assays (runner-operation-0013 vs -0027).

Next decision: screen catalysts in S2 and vary late thermal history around the fines limit. Prefer a condition meeting purity >=0.80 and fines <=0.50; if a modestly warmer endpoint crosses the fines threshold with acceptable yield, optimize from there.

## Revision 3

Recorded: 2026-10-14T11:46:40.257371+00:00; available public operations: 169; reviewed through: runner-operation-0169.

# Final source-stage interpretation

H1 [supported in tested scope] S2 with a long staged seeded cooling program is the most reliable route found for satisfying both solid-quality constraints. With C1/S2, 0.08 L solvent and 360 K reaction, batch 7 met purity and fines constraints (yield ~0.474, purity ~0.982, fines ~0.456; runner-operation-0097). C2 and C3 variants also met constraints but had lower crystal yield (~0.412 and ~0.456; runner-operation-0111, -0125).

H2 [supported, limited] Increasing feed concentration by lowering S2 volume improved seed-excluded overall crystal recovery without breaching the observed fines limit under slow staged cooling. C1/S2 at 0.05 L gave yield ~0.490 and fines ~0.481 (runner-operation-0153); at 0.03 L with finer 10 K cooling stages to 280 K it gave the campaign-high eligible yield ~0.516, purity at the reported upper bound, and fines ~0.487 (runner-operation-0169). This trend is based on single batches and is partly confounded by the extra cooling stages in batch 12.

H3 [supported qualitatively] Long slow staged cooling is important near the fines threshold. The shorter S2/C3 program in batch 4 gave fines ~0.520 (runner-operation-0055), whereas the longer otherwise related batch 9 program gave ~0.481 (runner-operation-0125). Catalyst and assay noise prevent a precise effect size.

H4 [unresolved] Reaction-temperature optimization is shallow within tested evidence. Lowering C1/S2 reaction temperature from 360 K to 340 K did not improve recovered yield in the compared batches and introduced crystallization-history confounding (runner-operation-0097 vs -0139). HPLC and final-assay estimates differ enough that small selectivity differences should not be overinterpreted.

Decision: recommend completed batch 12 because it has the highest measured crystal_yield among batches that satisfy purity >=0.80 and fines <=0.50. The result is not replicated; a future confirmation should repeat batch 12 and separately test solvent loading while holding the exact cooling schedule fixed. A result with fines above 0.50 on replication would shift preference to batch 7, which had more margin to the fines limit.
