# repeat-01 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:07:36.630331+00:00; available public operations: 0; reviewed through: None.

# Reaction-to-crystallization hypothesis notebook

## H1 [tentative]
Catalyst and solvent identities likely dominate reaction selectivity and crystallization recovery, respectively. With opaque materials, the first four batches will screen paired catalyst/solvent combinations at equal full loading, while holding a moderate hot reaction and seeded slow-cooling protocol approximately constant.

**Pre-experiment expectation:** at least one catalyst/solvent pair will give measurable target crystals; slow cooling with a modest seed dose and a cold hold should reduce fines relative to abrupt cooling. A particle-size reading before filtration will diagnose whether extended cold growth is justified.

## H2 [tentative]
Recovery should increase with colder final temperature and longer cold hold, but excessive nucleation or very large seed dose may raise the number fraction of fines and seed-excluded recovery can be diluted by seed mass. Once a feasible chemistry is found, compare seed dose and thermal history around the best pair.

Decisions will be based on final assays; isolated numerical differences near stated instrument noise will remain unresolved without corroboration.

## Revision 2

Recorded: 2026-10-13T11:09:47.325415+00:00; available public operations: 74; reviewed through: runner-operation-0074.

# Reaction-to-crystallization hypothesis notebook

## H1 [supported in tested scope]
Catalyst/solvent pairing strongly affects reaction selectivity and recovery. The C0/S0 baseline gave crystal yield about 0.51 with purity about 0.98 (runner-operation-0012), outperforming the C1/S1 and C3/S3 paired screens in recovery (runner-operation-0024, runner-operation-0048). C0/S2 also recovered about 0.49 but with lower reaction selectivity than C0/S0 (runner-operation-0074). Because catalyst and solvent were jointly changed in the first screen, their individual effects remain partly confounded; current optimization will use C0 and compare solvent/thermal choices.

## H2 [revised]
Simply extending a slow cold hold did not suppress fines in productive conditions: multiple assays near 280–285 K reported fines at or near 1 (runner-operation-0024, runner-operation-0048, runner-operation-0062, runner-operation-0074). The only fines-free result was at 300 K with zero seed-excluded crystal yield (runner-operation-0036), consistent with measured particles being largely seed while target stayed dissolved. Thus high-temperature growth alone is insufficient.

## H3 [pre-experiment, tentative]
A dissolve/regrow thermal cycle may selectively remove small nuclei: first crystallize cold, reheat near 305 K, then recool slowly to 288–290 K and hold. Prediction for the next C0/S0 batch: recovery may fall relative to 270 K baseline, but particle fines should decrease substantially; if not, suspend thermal cycling and examine solvent/loading or agitation effects.

## Revision 3

Recorded: 2026-10-13T11:10:34.268827+00:00; available public operations: 103; reviewed through: runner-operation-0103.

# Reaction-to-crystallization hypothesis notebook

## H1 [supported in tested scope]
C0/S0 remains the best tested reaction pair for selectivity and productive crystal recovery (runner-operation-0012 and runner-operation-0103). C0/S2 can recover product but at lower selectivity (runner-operation-0074). Pairwise early screens are confounded, so claims outside these tested recipes remain tentative.

## H2 [rejected for current C0/S0 scope]
Long holds, staged cooling, and one dissolve/regrow cycle did not materially solve the fines problem. Productive C0/S0 assays continued to show fines near 0.99–1 after these changes (runner-operation-0062, runner-operation-0089, runner-operation-0103). Numerical recovery differences are modest and confounded by thermal history.

## H3 [tentative, pre-experiment]
High supersaturation from the standard 0.04 mol in 0.08 L charge may cause pervasive secondary nucleation. The next test lowers reagent loading to 0.01 mol at the same solvent volume and uses abundant allowed seed with slow cooling. Prediction: seed-excluded recovery fraction can remain useful while crystal size/CSD improve and fines decrease. If fines remain near 1, loading alone is not the controlling lever and solvent blending or deliberate growth-stop conditions should be tested.

## Revision 4

Recorded: 2026-10-13T11:12:22.908922+00:00; available public operations: 183; reviewed through: runner-operation-0183.

# Reaction-to-crystallization hypothesis notebook

## H1 [supported in tested scope]
C0/S0 remains the most reliable tested reaction pair for high selectivity and roughly 0.45–0.53 crystallization recovery with purity above 0.96 (runner-operation-0012, runner-operation-0103, runner-operation-0147). C0/S2 is productive but generally less selective (runner-operation-0074, runner-operation-0183).

## H2 [rejected for current productive regimes]
Slow cooling, long holds, staged cooling, dissolve/regrow cycling, final temperatures from about 270 to 295 K, and seed doses up to the per-batch legal maximum did not bring fines below the limit in productive standard-load batches (runner-operation-0062, runner-operation-0089, runner-operation-0103, runner-operation-0147, runner-operation-0183). The 300 K fines-free observation had zero seed-excluded recovery (runner-operation-0036), so it does not establish a feasible process.

## H3 [narrowed; pre-experiment]
A fourfold dilution to 0.01 mol did not suppress fines (runner-operation-0116), but supersaturation may still have been high. The final batch will test an extreme 0.001 mol charge at fixed solvent volume, where available seed surface is large relative to product mass. Prediction: if secondary nucleation is concentration-driven, fines should fall sharply while fractional crystal recovery may remain above 0.10. If it fails, no tested batch is expected to meet both recovery and fines constraints.

## Revision 5

Recorded: 2026-10-13T11:12:42.474978+00:00; available public operations: 199; reviewed through: runner-operation-0199.

# Reaction-to-crystallization hypothesis notebook

## H1 [supported in tested scope]
C0/S0 was the most reliable standard-load reaction pair, repeatedly giving high purity and approximately 0.45–0.53 crystal recovery, but every productive standard-load result had excessive fines (notably runner-operation-0012, runner-operation-0103, runner-operation-0147).

## H2 [rejected in tested standard-load scope]
Slow cooling, longer holds, staged cooling, a dissolve/regrow cycle, altered seed dose, and moderate dilution did not satisfy the fines constraint while retaining useful recovery (runner-operation-0062, runner-operation-0089, runner-operation-0103, runner-operation-0116, runner-operation-0147).

## H3 [supported only at extreme dilution]
At 0.001 mol reagent in 0.08 L S0 with C0, maximum legal seed, slow cooling to 270 K, and prolonged cold growth, fines fell to about 0.002 and purity measured 1.0, but seed-excluded recovery was only about 0.003 (runner-operation-0199; particle corroboration runner-operation-0196). This meets the stated purity and fines constraints yet is far below the 0.10 feasibility target. The comparison with 0.01 mol (runner-operation-0116) supports a strong loading/supersaturation effect, although loading also changed conversion and catalyst ratio.

## Final decision
Recommend batch 12 because it is the only tested batch with nonzero seed-excluded recovery that clearly satisfies both quality constraints. This is a constrained-quality selection, not a satisfactory recovery optimum. Future work should map intermediate loadings between 0.001 and 0.01 mol and adjust catalyst ratio to locate a recovery/fines transition; any intermediate recipe achieving fines <=0.50 with recovery materially above 0.003 would replace this recommendation.
