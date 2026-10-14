# repeat-03 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:36:14.987620+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Reaction conversion/selectivity will depend strongly on anonymous catalyst, temperature, and time. Initial screen will compare catalysts under a common moderate-hot reaction; HPLC will distinguish productive conditions.

H2 [tentative] Slow cooling with a modest seed dose followed by a cold hold should reduce fines relative to unseeded/fast cooling while preserving recovery. Greater reagent loading and colder endpoint should raise overall crystal recovery, potentially trading against purity or fines.

Decision: screen broadly first, then spend later batches refining the best feasible process. These claims would change if early assays show weak catalyst effects or no crystallization.

## Revision 2

Recorded: 2026-10-14T11:38:48.788207+00:00; available public operations: 94; reviewed through: runner-operation-0094.

# Working hypotheses

H1 [supported in screened scope] Catalyst/solvent and thermal history materially affect reaction and crystallization outcomes. Under C0, 360 K/1800 s, the solvent screen gave large morphology differences: S0 remained overwhelmingly fine (batches 1 and 3), S1 was near the fines boundary with higher recovery (batch 4), S2 met both constraints with somewhat lower recovery (batch 5), and S3 produced excessive fines (batch 6). These are numerical single-batch comparisons; replication is still needed.

H2 [revised] A 0.05 g seed plus slow cooling alone is not generally enough to suppress fines; solvent identity is dominant in the tested recipes. For S1, slightly warmer endpoints, longer ripening, or mild thermal cycling should plausibly move fines below 0.50 while retaining much of the observed ~0.53 recovery. For S2, colder operation may raise recovery while preserving the observed fines margin.

Decision: focus remaining batches on S1/S2 boundary optimization and replication. Prefer feasible final-assay results over particle-size snapshots when selecting because the required endpoint is the destructive final assay. Suspend broad catalyst screening unless refined crystallization loses feasibility.

## Revision 3

Recorded: 2026-10-14T11:40:18.446296+00:00; available public operations: 177; reviewed through: runner-operation-0177.

# Final working interpretation

H1 [supported in tested scope] Solvent identity dominates morphology for the common C0 reaction and slow-cooling protocol. S0 and S3 gave excessive fines; S1 remained near or above the 0.50 limit despite warmer endpoints and one mild thermal cycle (batches 4, 7, 8). S2 produced feasible solids across batches 5 and 9–12.

H2 [supported in tested S2 scope] Lowering the S2 crystallization endpoint from 290 K to 280, 270, and 250 K increased observed overall recovery while final fines stayed below 0.50 (batches 5, 9, 10, 11). Because these are not exact replicates and final-assay noise/process variability are present, the trend is useful but not a precision law.

H3 [tentative] Raising concentration from 0.04 mol/0.08 L to 0.04 mol/0.06 L at the 250 K endpoint further improved recovery and size without violating purity/fines constraints (batch 12 versus batch 11), but this single comparison is confounded by run-to-run variability.

Decision: recommend batch 12. It has the highest observed feasible crystal_yield (~0.554), with crystal_purity ~0.997 and fines ~0.414. Batch 11 is a nearby, lower-loading feasible fallback (~0.547 yield, ~0.992 purity, ~0.372 fines) if a larger fines margin is prioritized. Claims are confined to anonymous benchmark materials and the tested operating window.
