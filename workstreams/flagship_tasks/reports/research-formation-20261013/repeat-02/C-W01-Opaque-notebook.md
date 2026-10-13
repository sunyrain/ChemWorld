# repeat-02 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:12:42.796050+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Catalyst and solvent identities will materially affect reaction conversion/selectivity; a first-pass screen should identify a productive pair. Prediction: at least one of the first four deliberately varied catalyst/solvent conditions will outperform the others in reaction score.

H2 [tentative] For crystallization, moderate seeding followed by slow cooling and a cold hold should reduce fines relative to an unseeded fast cool while maintaining useful seed-excluded recovery. Prediction: once a productive upstream condition is found, seeded slow-cooled batches will more often satisfy purity >=0.80 and fines <=0.50.

Decision: use early batches to screen chemistry and thermal handling, then concentrate remaining batches around the best feasible process. Apparent differences comparable to stated instrument noise will remain unresolved until supported by additional batches.

## Revision 2

Recorded: 2026-10-13T12:15:20.033538+00:00; available public operations: 86; reviewed through: runner-operation-0086.

# Working hypotheses after seven completed batches

H1 [supported in screened scope] Material identities materially affect both reaction and crystallization. Catalyst C1 gave the best upstream performance among the S0 catalyst screen by final-assay reaction metrics, although the comparisons are confounded by crystallization variants (events runner-operation-0025, -0037, -0050). Solvent S2 with C1 was the first clearly feasible crystallization outcome: purity 1.00, fines 0.273, crystal yield 0.429 (runner-operation-0074). S1 was near the fines boundary (0.532) and S3/S0 were worse (runner-operation-0062, -0086, -0025).

H2 [narrowed] Slow cooling plus 0.05 g seed is not sufficient across all solvents; solvent S2 appears decisive for low fines in the tested direct-cooling process. The S0 results remained fines-rich despite changes in endpoint and staged seeding (runner-operation-0013, -0025, -0037, -0050). Alternative: the apparent solvent effect could include catalyst-solvent interaction; test other catalysts in S2.

Decision: hold S2 and the direct 360 K to 290 K/14400 s seeded cooling procedure while screening remaining catalysts, then use final batches for thermal refinement around the best feasible pair. A later S2 result with fines above 0.50 would weaken the solvent-generalization claim.

## Revision 3

Recorded: 2026-10-13T12:16:43.277571+00:00; available public operations: 146; reviewed through: runner-operation-0146.

# Final source-stage interpretation

H1 [supported in tested domain] Solvent S2 is the robust low-fines choice for the direct seeded cooling process. All five S2 batches tested across catalysts C0-C3 and repeated C0 runs met fines <=0.50 and purity >=0.80 (final-assay events runner-operation-0074, -0098, -0110, -0122, -0134, -0146). This is materially different from the mostly fines-rich S0/S1/S3 observations, though the study does not establish a general solvent law outside these recipes.

H2 [supported in tested domain] With S2, catalyst C0 is preferred: at the common 290 K endpoint it gave crystal yield 0.456, purity 0.981, fines 0.223 (runner-operation-0098), exceeding the observed yield of C1/C2/C3 analogues (runner-operation-0074, -0110, -0122). Single-batch comparisons remain potentially affected by run variation, but the direction motivated confirmatory C0 thermal trials.

H3 [supported over 250-290 K endpoints] For C0/S2 with 0.05 g seed and 14400 s cooling, colder endpoints increased observed recovery without losing specifications: yield 0.456 at 290 K, 0.483 at 270 K, and 0.512 at 250 K (runner-operation-0098, -0134, -0146). The 250 versus 270 K difference (~0.030) exceeds the stated 0.01 per-assay yield noise scale, but there are no exact thermal replicates, so monotonicity is provisional rather than a precision model.

Decision: recommend batch 12. It has the highest observed feasible seed-excluded crystal recovery (0.512), with purity 0.995 and fines 0.265; batch 11 is a nearby feasible fallback. This recommendation would change if a replicate showed the colder endpoint systematically violates the fines constraint or fails to reproduce the recovery advantage.
