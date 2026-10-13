# repeat-03 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:49:56.213773+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Solvent S2 should favor the quality-constrained objective because its dossier indicates low solubility, high growth, low nucleation, and low impurity occlusion; prediction: seeded, slow-cooled S2 batches will give higher recovery and fewer fines than fast/unseeded variants, while retaining purity >=0.80.

H2 [tentative] Catalyst C1 is the best initial reaction choice from nominal activity. A moderate thermal reaction will outperform low-temperature reaction without excessive degradation; HPLC after reaction can distinguish this.

H3 [tentative] Seed plus slow cooling and a growth hold should suppress fines relative to abrupt cooling. Reheating/recooling may dissolve fines and increase size, but could sacrifice recovery.

Initial design: establish a feasible C1/S2 baseline, then vary catalyst, solvent, thermal severity, seed dose, cooling rate/end point, hold, and a reheat/recool cycle. Interpret numerical differences cautiously because single-batch comparisons are confounded and instrument noise is declared.

## Revision 2

Recorded: 2026-10-13T17:52:01.291620+00:00; available public operations: 58; reviewed through: runner-operation-0058.

# Working hypotheses

H1 [unresolved; narrowed] S2 gives high crystal purity (~0.98–1.00) and recovery ~0.38–0.43 in batches 1–4, but none meets the fines constraint. Seeded S2 processes produced fines 0.76 to 1.00 (final assays: runner-operation-0014, -0028, -0042, -0058). Thus nominal low nucleation/high growth is insufficient in this tested range.

H2 [tentative] Moderate C1 reaction conditions (350 K/2400 s) reduce degradation/byproduct relative to the first 370 K/3600 s batch, while preserving near-complete conversion. This is only cross-batch evidence and crystallization histories differ.

H3 [partly contradicted] Slower cooling/long holds alone did not suppress fines. Reducing seed from 0.05 g to 0.001 g also failed (batch 3), and one 305 K reheat/slow-recool cycle failed (batch 4). Seed dose effects remain confounded by batch noise and thermal history. A solvent screen is now higher priority.

Decision: screen S0, S1, and S3 under a common deep, slow cooling protocol with 0.05 g seed, then exploit the best solvent. A qualifying process requires final-assay purity >=0.80 and fines <=0.50; recovery is optimized only among qualifiers.

## Revision 3

Recorded: 2026-10-13T17:54:27.494219+00:00; available public operations: 183; reviewed through: runner-operation-0183.

# Final working interpretation

H1 [supported in tested scope] High-temperature seeding is the decisive control for fines. With S2, moving the seed point from about 304 K (batches 2–4) to 330 K reduced final fines to 0.628 (batch 9, runner-operation-0138), and 345 K reduced them to 0.377 while preserving ~0.441 recovery (batch 10, runner-operation-0153). This monotonic pattern is cross-batch rather than replicated, but the effect size is large relative to declared assay noise.

H2 [supported in tested scope] S1 has higher achievable crystallization recovery than S2 under matched deep-cooling histories. At a 345 K seed point and 275 K endpoint, S1 gave recovery 0.498, purity 0.995, fines 0.442 (batch 11, runner-operation-0168), versus S2 recovery 0.441, purity 0.979, fines 0.377 (batch 10, runner-operation-0153). This is a recovery/fines tradeoff; both qualify.

H3 [supported provisionally] A slightly hotter seed point (347 K) combined with deeper cooling to 270 K improved the observed S1 result to recovery 0.511, purity 0.996, fines 0.428, and size index 0.098 (batch 12, runner-operation-0183). Batch 12 is the best qualifying recovery and has modest fines margin relative to the 0.50 constraint. Because batches 11 and 12 differ in both seed temperature and endpoint and are unreplicated, attribution between those factors remains unresolved.

H4 [rejected in tested scope] Merely extending low-temperature holds, lowering seed dose, or applying the tested 305 K reheat/recool cycle did not control fines (batches 3, 4, 8). Solvent screens seeded near 304 K all remained fines-dominated (batches 5–7), so solvent choice alone is insufficient.

Decision: recommend batch 12. Conditions that would change this decision: a replicate showing fines above 0.50, or a matched test demonstrating higher qualifying recovery with a safer fines margin. Batch 11 is the nearest fallback.
