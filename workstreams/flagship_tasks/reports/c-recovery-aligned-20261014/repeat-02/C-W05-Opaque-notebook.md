# repeat-02 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:19:06.623338+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Reaction performance likely depends strongly on anonymous catalyst/solvent identity and temperature. Initial factorial scouting across identities is needed before thermal optimization. A productive condition should show increased HPLC conversion/yield after a moderate hot hold without excessive byproduct.

## H2 [tentative]
For a productive reaction liquor, seeded slow cooling followed by a cold hold should improve recovery and particle-size distribution relative to abrupt unseeded cooling. Excessive seed may inflate fines, while too little seed may delay nucleation. Initial consequence: test a moderate seed dose and controlled cooling, then vary seed and thermal history once a feasible material pair is identified.

Because no nominal dossier is available, these are broad benchmark expectations; observations will be authoritative.

## Revision 2

Recorded: 2026-10-14T11:20:22.203749+00:00; available public operations: 29; reviewed through: runner-operation-0029.

# Hypothesis notebook

## H1 [unresolved]
At 370 K for 3600 s in solvent S0, catalysts C0 and C1 both give high conversion but only about 0.56–0.58 reaction yield/selectivity near 0.59 (events runner-operation-0007, -0016, -0022, -0029). The numerical differences are comparable to instrument/process uncertainty and are not evidence of a catalyst effect. Continue identity screening.

## H2 [revised; unsupported in tested scope]
The initial seeded cooling schedules produced high-purity crystals and substantial recovery (0.43 for C0; 0.37 for C1), but essentially all particles were fines in both final assays (runner-operation-0016, -0029). Reducing seed from 0.02 g to 0.001 g and using a shallower 295 K endpoint increased the reported size index numerically, but did not resolve fines. Simple low seed plus slow cooling is insufficient in this scope.

## H3 [tentative, prospective]
Fines may be driven by excessive supersaturation/secondary nucleation. Test substantially shallower crystallization endpoints, staged growth, and/or a heat–redissolve–recool cycle. Prediction: accepting lower recovery at a warmer endpoint or annealing should reduce fines below 0.50 if supersaturation is causal. Solvent identity remains a major unresolved alternative.

## Revision 3

Recorded: 2026-10-14T11:22:00.452106+00:00; available public operations: 111; reviewed through: runner-operation-0111.

# Hypothesis notebook

## H1 [supported in screened scope]
At 370 K/3600 s, C3 in S0 gave the best observed reaction yield/selectivity among C0–C3, although differences from C0/C1 are moderate and each condition is unreplicated (events runner-operation-0007, -0022, -0035, -0049). I will use C3 for downstream optimization unless particle behavior forces a tradeoff.

## H2 [supported directionally, constraint not met]
Solvent changes particle outcomes: at a common C3, 0.001 g seed, and 300 K schedule, S1–S3 reduced final fines from the near-unity S0 results, but all remained above 0.80 in final assays (runner-operation-0070, -0083, -0096). S1 offered the best recovery among these solvent screens (~0.40), so it is the current compromise. These single runs establish numerical rankings, not repeatable effect sizes.

## H3 [not supported for tested cycle]
A 300→312→300 K annealing cycle in S1 did not improve fines relative to the corresponding noncycled run (runner-operation-0111 versus -0070); the difference is small and opposite the prediction. A mild single heat cycle is therefore suspended.

## H4 [tentative, prospective]
Abrupt supersaturation may dominate secondary nucleation even during a nominally long ramp. Test a finely staged 320→315→310→305→300 K cooling path, holding/ramping 14400 s per stage with 0.001 g seed. Prediction: if supersaturation rate is causal, fines should fall substantially versus the direct 320→300 K schedules. If not, investigate seed dose/loading and accept that solvent S1 may intrinsically form fines.

## Revision 4

Recorded: 2026-10-14T11:23:08.020079+00:00; available public operations: 150; reviewed through: runner-operation-0150.

# Hypothesis notebook

## H1 [supported in screened scope]
C3 is the preferred catalyst from the 370 K/3600 s screen; S1 is the preferred solvent compromise because it retained higher recovery than S2/S3 while reducing fines versus S0. Rankings remain based mainly on single runs.

## H2 [rejected in tested scope]
Neither a mild annealing cycle, fine thermal staging at full 0.04 mol loading, nor increasing seed from 0.001 to 0.05 g solved the fines constraint (events runner-operation-0111, -0125, -0137). Those manipulations gave final fines about 0.84–0.87 in S1.

## H3 [supported directionally; near constraint]
Reducing concentration to 0.02 mol reagent in 0.08 L S1 (with proportional catalyst), followed by staged cooling to 290 K, increased CSD quality and reduced final fines to 0.533 while retaining 0.351 seed-excluded recovery and 0.991 purity (runner-operation-0150). This is a large numerical change relative to full-loading S1 runs, though unreplicated and still just outside the stated fines limit.

## H4 [prospective final test]
Use 0.018 mol reagent in 0.08 L S1, proportional C3 catalyst, 0.001 g seed, and 5 K/14400 s cooling stages from 320 to 290 K. Prediction: slightly lower loading plus finer staging should push fines below 0.50 while preserving recovery near the ~0.35 observed at 0.02 mol. If it fails, no completed batch will have demonstrated all constraints.

## Revision 5

Recorded: 2026-10-14T11:23:38.198058+00:00; available public operations: 166; reviewed through: runner-operation-0166.

# Hypothesis notebook

## H1 [supported in screened scope]
C3/S1 was the best practical reaction–crystallization compromise found. Catalyst and solvent rankings are mostly single-run comparisons, so exact effect sizes remain uncertain.

## H2 [supported for this loading window]
Lower upstream concentration was the decisive control for particle quality. Full 0.04 mol loading in 0.08 L gave final fines roughly 0.84–0.87 in S1 despite annealing, staging, and seed-dose changes (runner-operation-0070, -0111, -0125, -0137). At 0.02 mol, fines fell to 0.533 (runner-operation-0150). At 0.018 mol with finer 5 K staging, fines fell to 0.228 and CSD quality rose to 0.819 (runner-operation-0166). Loading and staging are confounded between the last two batches; both may contribute, and repeatability is unknown.

## H3 [final decision]
Batch 12 is the only demonstrated batch meeting both constraints: crystal purity 0.992 ≥ 0.80 and fines 0.228 ≤ 0.50, with seed-excluded crystal recovery 0.333 (runner-operation-0166). Recommend it despite batch 11's numerically higher recovery (0.351), because batch 11 missed the fines constraint. The selected recipe used 0.018 mol reagent, 0.08 L S1, 0.00225 mol C3, reaction at 370 K for 3600 s, cooling to 320 K, 0.001 g seed, then 5 K stages to 290 K with 14400 s per stage, followed by filtration.
