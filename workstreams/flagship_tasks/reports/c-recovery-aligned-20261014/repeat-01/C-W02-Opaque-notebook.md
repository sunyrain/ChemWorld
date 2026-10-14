# repeat-01 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:26:47.905974+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Reaction performance will depend strongly on anonymous catalyst/solvent pairing and thermal severity. Initial factorial screening should identify a productive pair. Prediction: at least one catalyst-solvent combination at 0.04 mol reagent, 0.005 mol catalyst, moderate heating will exceed 0.10 overall crystal recovery after seeded slow cooling.

## H2 [tentative]
For a productive reaction mixture, controlled seeding near the onset of cooling followed by slow cooling and a cold hold should reduce fines relative to unseeded or rapid cooling. This may trade some seed-excluded recovery for size/purity. A particle-size measurement before final filtration can diagnose this.

No task-specific material dossier exists, so catalyst and solvent rankings are initially unresolved.

## Revision 2

Recorded: 2026-10-14T10:29:01.428221+00:00; available public operations: 55; reviewed through: runner-operation-0055.

# Hypothesis notebook

## H1 [supported in screened scope]
Catalyst/solvent choice materially affects both reaction and crystallization. With C0 and the common 380 K reaction plus seeded slow cooling/hold near 300 K, S1 and S2 met both quality constraints, while S0 and S3 produced excessive fines. Final-assay evidence: batch 2 (event runner-operation-0022) gave recovery 0.512, purity 0.980, fines 0.424; batch 4 (runner-operation-0044) gave 0.494, 1.000, 0.285. Batches 3 and 5 failed the fines criterion (runner-operation-0033, runner-operation-0055). These are numerical contrasts from single batches; repeatability is unresolved.

## H2 [narrowed]
Slow cooling/hold is not sufficient by itself to suppress fines: it succeeded with S1/S2 but not S0/S3. Solvent-dependent nucleation/growth is therefore the leading explanation. Continue catalyst screening in S1, then optimize thermal history using the best feasible catalyst-solvent pair. A result with higher recovery and fines <=0.50 would change the current lead (batch 2).

## Revision 3

Recorded: 2026-10-14T10:30:24.680226+00:00; available public operations: 118; reviewed through: runner-operation-0118.

# Hypothesis notebook

## H1 [supported in screened scope]
Among catalysts tested in S1 under the common 380 K reaction, C0 gave the highest feasible recovery. C1, C2 and C3 did not improve on C0 (final assays runner-operation-0066, -0077, -0088 versus C0 at -0022). Single-batch uncertainty remains, but the numerical ranking is large enough to retain C0 for optimization.

## H2 [supported in screened scope]
With C0/S1, omitting the long post-cooling hold and cooling farther increased recovery without breaching the fines limit: 295 K/0.05 g seed gave recovery 0.553 and fines 0.453 (runner-operation-0098); 290 K/0.01 g gave 0.570 and 0.448 (-0108); 285 K/0.01 g gave 0.575 and 0.428 (-0118). This supports a broad feasible window rather than a precise monotonic effect because each condition is unreplicated and assay noise/process variability are present. Batch 11 is the current lead.

## H3 [tentative, prospective]
A modestly milder reaction (370 K rather than 380 K) may reduce byproduct/degradation while retaining near-complete conversion; combining it with 280 K slow cooling and 0.01 g seed may improve recovery. If conversion or recovery falls, retain batch 11 rather than extrapolating.

## Revision 4

Recorded: 2026-10-14T10:30:45.497471+00:00; available public operations: 127; reviewed through: runner-operation-0127.

# Hypothesis notebook

## H1 [supported in screened scope]
C0/S1 is the best catalyst-solvent pairing found for feasible seed-excluded crystal recovery. Alternatives C1-C3 in S1 and solvents S0/S3 with C0 were inferior or failed the fines constraint; S2 was feasible but lower recovery. Evidence is the completed final assays through runner-operation-0127; conditions are mostly unreplicated, so rankings should not be treated as universal material laws.

## H2 [supported in screened scope]
For C0/S1, a small seed charge (0.01 g), slow 14,400 s cooling without a long cold hold, and an endpoint in the 280-290 K range gave consistently feasible fines and progressively high recovery. Batches 10-12 all met purity and fines constraints (runner-operation-0108, -0118, -0127). The exact endpoint effect remains unresolved because reaction temperature also changed in batch 12 and differences are near expected assay variability.

## H3 [supported for the tested recipe]
The final 370 K reaction plus 280 K crystallization produced the highest observed feasible recovery: batch 12 final assay (runner-operation-0127) recovery 0.584, purity 0.991, fines 0.416. It also retained complete measured conversion with lower byproduct signal than several 380 K screens. Batch 12 is therefore selected; this is an empirical recipe decision, not proof that 370 K or 280 K is individually optimal.

## Remaining uncertainty
No replicate campaign was possible. Seed-dose and endpoint effects are partially confounded, and final-assay noise can reorder small numerical differences. A future confirmation should replicate batch 12 and bracket 365-375 K reaction temperature and 278-285 K cooling endpoints while preserving the 0.01 g seed and slow cooling.
