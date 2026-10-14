# repeat-02 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:05:15.970896+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

H1 [tentative] Reaction performance likely depends strongly on anonymous catalyst/solvent and temperature. Initial screen will vary catalyst and solvent at equal maximum reagent/catalyst charge; an HPLC reading after a fixed hot hold will identify promising reaction conditions.

H2 [tentative] Slow cooling with modest seeding near the onset of supersaturation, followed by a low-temperature hold, should reduce fines relative to abrupt cooling. Because crystal yield is overall reagent recovery and excludes seed, maximize upstream target formation before optimizing crystallization.

Decision rule: first establish a feasible reaction/crystallization baseline, then use later batches to screen materials and thermal/seeding history. Any observed differences remain unresolved until separated from simultaneous changes or repeated.

## Revision 2

Recorded: 2026-10-14T11:07:28.695095+00:00; available public operations: 61; reviewed through: runner-operation-0061.

# Working hypotheses after batches 1–4

H1 [supported in screened scope] At 370 K in S0 with fixed hot hold and crystallization history, catalyst identity materially changes overall target formation/recovery. C1 gave the highest final crystal yield (0.448, event runner-operation-0031), compared with C0 0.381 (runner-operation-0016) and C2 0.359 (runner-operation-0046); C3 was similar to C1 at 0.448 (runner-operation-0061). C1 also had the best final selectivity among these runs. Single runs and assay noise leave the C1–C3 difference unresolved.

H2 [revised: unsupported baseline] The initial slow seeded cooling recipe did not meet the fines constraint in any screened batch: final fines ranged about 0.53–0.87 (events runner-operation-0016, -0031, -0046, -0061), despite high purity. Thus reaction feasibility is established, but particle control is the limiting constraint.

Next tests: hold C1 fixed and screen solvents, then change thermal history (including reheating/recooling or warmer endpoint) to seek fines <=0.50 without sacrificing recovery. A repeated low-fines result would be needed before claiming robust compliance.

## Revision 3

Recorded: 2026-10-14T11:08:35.175264+00:00; available public operations: 151; reviewed through: runner-operation-0151.

# Working hypotheses after batches 1–10

H1 [supported in screened scope] Solvent S2 with catalyst C1 is the best tested material pair. At 370 K it produced crystal yield 0.487 with purity 1.00 and fines 0.340 (runner-operation-0091), outperforming S0/S1/S3 on recovery or fines (runner-operation-0031, -0076, -0106). C3/S2 also met quality but recovered less (0.446; runner-operation-0121).

H2 [supported in current recipe] S2 changes particle behavior substantially: multiple S2 runs with C1/C3 met the fines limit, unlike most S0/S3 runs. This is reproducible across events runner-operation-0091, -0121, -0136, and -0151, though catalyst and temperature also varied.

H3 [tentative] For C1/S2, 350–390 K gives similar observed recovery (~0.478–0.480 at events runner-operation-0136 and -0151 versus 0.487 at 370 K), while 350 K gave the lowest fines and degradation warning. Differences in recovery are not resolved relative to assay/process noise; 350 K is preferred for quality margin.

Next test: lower the final crystallization endpoint to 250 K at otherwise preferred 350 K conditions. Prediction made before batch 11: recovery may rise from greater supersaturation, but fines may increase. If it remains within fines <=0.50, use it for confirmation; otherwise confirm the 350 K/278 K recipe.

## Revision 4

Recorded: 2026-10-14T11:09:17.055105+00:00; available public operations: 180; reviewed through: runner-operation-0180.

# Final source-stage conclusions

H1 [supported in tested domain] Catalyst C1 with solvent S2 is the preferred material pair. It repeatedly produced high recovery and compliant purity/fines over 350–390 K (runner-operation-0091, -0136, -0151, -0166, -0180).

H2 [supported in tested domain] A 250 K crystallization endpoint improved observed recovery while retaining a substantial fines margin. Batch 11 reached crystal yield 0.517, purity 0.994, fines 0.342 (runner-operation-0166), above the best 278 K result of 0.487 yield (runner-operation-0091). This endpoint effect is supported by the independent batch-12 confirmation.

H3 [unresolved small effect] Extending the final 250 K hold from 7200 s to 14400 s changed observed crystal yield from 0.5167 to 0.5195 and size index from 0.0828 to 0.1043 (runner-operation-0166 versus -0180), with both batches compliant. The direction is consistent with continued growth, but the recovery difference is too small to claim beyond assay/process variability without further repeats.

Decision: recommend batch 12 because it has the highest observed compliant crystal yield (0.5195), purity 0.9956, and fines 0.3485 (runner-operation-0180). Batch 11 is a near-equivalent confirmation. Scope is limited to the tested anonymous materials, charges, and histories; exact robustness to loading changes remains untested.
