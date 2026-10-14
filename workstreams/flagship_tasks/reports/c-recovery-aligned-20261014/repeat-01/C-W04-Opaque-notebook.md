# repeat-01 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:43:11.418103+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

H1 [tentative] Reaction performance will depend strongly on catalyst identity and temperature; an initial screen across catalyst/solvent combinations should identify a productive region. I expect moderate heating (about 340–370 K) followed by controlled cooling and seeding to yield more target crystals than an unoptimized ambient process.

H2 [tentative] For a productive reaction liquor, seeding near the onset of cooling and a slow cool/hold should reduce fines relative to abrupt cooling. This could trade some recovery for particle quality. I will first screen broad chemistry, then vary seed dose and thermal history around the best feasible recipe.

Decision rule: prioritize measured crystal_yield only among batches meeting purity >=0.80 and fines <=0.50; if none meet both, report that clearly.

## Revision 2

Recorded: 2026-10-14T10:44:35.197280+00:00; available public operations: 29; reviewed through: runner-operation-0029.

# Working hypotheses after batches 1–2

H1 [supported in this scope] C0/S0 at 360 K for 1 h gives complete conversion and substantial target formation (batch 1 HPLC, event runner-operation-0007), and final crystal purity is high in both batches 1–2. Recovery is about 0.44, so chemistry is feasible, but selectivity/degradation limit the theoretical ceiling.

H2 [partly supported] Slower staged cooling and much lower seed reduced fines markedly versus the first fast-cool recipe: final fines changed from about 0.95 (batch 1) to 0.58 (batch 2), with similar recovery and purity. This is a numerical difference across confounded thermal/seed changes, not yet an isolated seed effect. Batch 2 still misses the <=0.50 specification.

H3 [tentative] Further reducing seed and avoiding the unsuccessful 300 K reheat/recool may cross the fines limit while retaining recovery. The reheat cycle worsened the in-process particle readout (events runner-operation-0023 vs -0026), so suspend that exact cycle unless later evidence suggests a narrower useful temperature.

Decision: hold C0/S0 chemistry constant for one cleaner seed/thermal test; then screen catalyst/solvent identity while using the best cooling pattern.

## Revision 3

Recorded: 2026-10-14T10:46:57.428814+00:00; available public operations: 118; reviewed through: runner-operation-0118.

# Working hypotheses after batches 1–7

H1 [supported in tested scope] C0–C3 in S0 all produce high-conversion, high-purity crystals at 360 K/1 h. Catalyst identity changes measured selectivity/recovery modestly: C1 and C3 gave the highest final recoveries so far (about 0.511 and 0.515), while C2 was lower (about 0.465). Single batches and assay noise mean the small C1/C3 difference is unresolved.

H2 [supported in tested scope] A very low but effective seed population (~0.0001 g) plus extended staged cooling/holds at 330, 310, 290, then 270 K consistently brings fines below 0.50 (batches 4–7) while retaining ~0.46–0.52 overall recovery and purity >0.97. The minimally effective seed threshold matters: 0.000001 g did not enable crystallization in batch 3 until supplemented (events runner-operation-0035 to -0043).

H3 [tentative] Solvent identity may shift recovery more strongly than the small catalyst differences. Next, screen S1–S3 with C1 and the established qualifying crystallization schedule. Last batches will refine the best chemistry/temperature combination.

Decision: current qualifying incumbent is batch 7 by measured recovery, with batch 5 essentially tied. Prefer C1 for solvent screening because its measured reaction selectivity was highest among the S0 catalyst screen.

## Revision 4

Recorded: 2026-10-14T10:48:24.143071+00:00; available public operations: 201; reviewed through: runner-operation-0201.

# Final source-stage interpretation

H1 [supported in tested scope] All tested catalyst/solvent combinations could give high-purity crystals, but S0 was the best recovery solvent in the C1 screen. S1–S3 improved particle quality substantially yet reduced recovery relative to S0 (batches 8–10 versus batch 5). Catalyst effects within S0 were modest; C1/C3 outperformed C0/C2 numerically, without replication sufficient to separate C1 from C3.

H2 [supported in tested scope] The decisive particle-quality intervention was an effective low seed dose (~0.0001 g) followed by long staged cooling/holds at 330, 310, 290, and 270 K. Batches 4–12 using this schedule met the fines constraint in final assays, whereas faster or less-developed schedules in batches 1–3 gave borderline or excessive fines. Exact causal shares of seed dose and residence time remain confounded.

H3 [supported for the tested comparison] Reducing reaction temperature from 360 to 340 K did not improve recovery: batch 11 gave ~0.480 despite lower degradation warning. Thus the 360 K condition remains preferred within the tested range.

H4 [tentative but decision-relevant] Increasing upstream concentration by reducing S0 volume from 0.08 to 0.06 L improved recovery in the single C3 comparison. Batch 12 achieved the campaign-best measured crystal_yield 0.5252 with purity 0.9936 and fines 0.3247 (event runner-operation-0201), versus batch 7 at 0.5155 yield, 0.9740 purity, 0.4036 fines. Because catalyst and loading were not varied factorially and differences are small, the concentration effect needs replication.

Final decision: recommend batch 12. It has the highest observed recovery among qualifying batches and comfortable purity/fines margins. This choice would change if replicated assays showed its recovery advantage was noise or if concentrated loading caused reproducibility/safety problems outside this bounded run.
