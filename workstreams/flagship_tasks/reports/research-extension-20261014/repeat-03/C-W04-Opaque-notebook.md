# repeat-03 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:14:24.547441+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

**H1 [tentative]** Reaction performance will depend strongly on anonymous catalyst, solvent, temperature, and time. I will first screen these jointly with a common crystallization workflow.

**H2 [tentative]** Slow cooling with a modest seed dose and a low-temperature hold should reduce fines relative to abrupt cooling, while deeper cooling should raise crystal recovery. A reheating/recooling cycle may trade recovery for larger particles.

**Pre-experiment expectation:** a catalyst/solvent combination exists that gives useful target loading, and controlled seeded cooling will achieve crystal recovery above 0.10 while retaining purity >=0.80 and fines <=0.50. Early batches will prioritize broad screening; later batches will refine the best feasible region.

## Revision 2

Recorded: 2026-10-13T18:16:40.405658+00:00; available public operations: 73; reviewed through: runner-operation-0073.

# Working hypotheses after batches 1–6

**H1 [supported in screened scope]** Solvent identity strongly affects crystallization habit/fines. Under otherwise slow seeded cooling, S1 gave feasible fines (~0.43 in batches 2 and 5), whereas S0 remained very fine (~0.82 in batch 6). This comparison is confounded by reaction temperature/catalyst in batch 2 but batch 5 vs 6 keeps C0 and most crystallization settings close; the large difference exceeds the stated assay noise. Evidence: runner-operation-0061 and runner-operation-0073.

**H2 [supported in screened scope]** Extending cooling from 7200 s to 14400 s can move the S1 process into the fines specification. Batch 1 (S0, 7200 s) was highly fine, so solvent remains an alternative explanation; duration effect is not separately identified. Evidence: runner-operation-0013, -0025.

**H3 [tentative]** C0/S1 is preferable to C1/S1 for recovery because batch 5 had slightly higher crystal yield than batch 2 (~0.406 vs ~0.398), but the numerical difference is comparable to assay noise and is not yet evidence of a catalyst effect.

**Decision:** retain S1 and 14400 s cooling. Use remaining batches to vary seed dose, endpoint temperature, reaction severity, and thermal cycling. I will prefer recovery only among batches satisfying purity >=0.80 and fines <=0.50.

## Revision 3

Recorded: 2026-10-13T18:18:09.808861+00:00; available public operations: 147; reviewed through: runner-operation-0147.

# Final source-stage hypotheses

**H1 [supported in tested scope]** S1 is the most reliable solvent for meeting the fines constraint under seeded 14400 s cooling. S0 produced much higher fines in a close C0 comparison (batches 5–6; runner-operation-0061 and -0073). Other solvent/catalyst screens were not competitive.

**H2 [supported in tested scope]** For C0/S1 with 0.01 g seed and 14400 s cooling, deeper endpoints increased observed seed-excluded crystal recovery: about 0.424 at 280 K, 0.452 at 270 K, 0.460 at 260 K, and 0.474 at 250 K (batches 7–10; runner-operation-0085, -0097, -0109, -0121). Purity stayed well above 0.80. Fines rose toward the 0.50 limit at 250 K. Adjacent yield differences are near the final-assay noise, so monotonicity is a trend rather than a precisely estimated law.

**H3 [rejected for tested cycle]** A 290 K reheat after an initial 250 K cool did not improve size distribution: batch 11 had fines ~0.63 and failed the constraint (runner-operation-0135). Do not recommend this cycle.

**H4 [unresolved seed effect]** Reducing seed from 0.01 g to 0.005 g at 250 K gave observed recovery ~0.468 and fines ~0.468 in batch 12 versus ~0.474 and ~0.478 in batch 10. Differences are smaller than or comparable to measurement noise, so no seed-dose effect is claimed.

**Recommendation decision:** batch 10 has the highest observed recovery among batches meeting measured purity and fines limits. Its fines margin is narrow relative to assay noise; batch 9 is the more conservative alternative (lower recovery ~0.460, fines ~0.444). I will select batch 10 because the stated objective is maximum recovery subject to the observed constraints; additional replication would be required to establish robust compliance at the boundary.
