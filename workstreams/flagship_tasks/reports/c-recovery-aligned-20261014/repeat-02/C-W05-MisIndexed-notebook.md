# repeat-02 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:13:25.903121+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Solvent S2 should favor crystal growth, lower impurity occlusion, and lower nucleation than S0/S1; therefore a seeded, controlled slow cooling in S2 is expected to meet purity >=0.80 and fines <=0.50 more readily, though its lower solubility may complicate reaction loading.

## H2 [tentative]
Catalyst C1 is the strongest nominal starting choice for reaction conversion, but fixed-world residuals may reverse the ranking. An initial C1/S2 batch followed by material screens will test this.

## Initial testable expectation
At 0.04 mol reagent in 0.08 L S2 with 0.005 mol C1, warm reaction followed by modest seeding and slow cooling/hold should give detectable seed-excluded recovery (>0.10) with purity above 0.80 and fines below 0.50. If reaction HPLC is weak, vary catalyst/solvent or thermal severity; if final fines are high, reduce supersaturation/cooling rate and increase growth hold.

## Revision 2

Recorded: 2026-10-14T11:15:34.577657+00:00; available public operations: 65; reviewed through: runner-operation-0065.

# Working hypotheses

## H1 [supported in tested S2 scope]
S2 with staged slow cooling can achieve the purity/fines constraints. Batch 2 (event runner-operation-0026) gave crystal yield 0.346, purity 0.982, fines 0.409. Batches 3-4 also met both constraints but had lower recoveries (0.310 and 0.276; events runner-operation-0039 and -0052). The single-step batch 1 missed the fines limit (0.598; -0013), consistent with staged cooling being preferable, though catalyst and reaction temperature are confounded.

## H2 [revised: C0 best constrained candidate; C3 high-recovery risk]
At 330 K/3600 s in S2, C0 currently gives the best qualifying recovery. C3 gave higher recovery 0.371 but fines 0.542 (event -0065). C1 and C2 were lower recovery. Numerical differences exceed the final assay noise scale, but no exact recipe replicate yet separates catalyst effects from run-to-run crystallization response.

## H3 [tentative]
High product loading/supersaturation may drive excess fines for C3. Prediction before batch 6: lengthening and splitting the cooling trajectory should lower fines enough to qualify while retaining recovery near the C3 result. A lower reaction temperature is also tested, so interpretation will remain confounded unless followed by a targeted comparison.

## Decision
Prioritize C3 slow multistage cooling, then refine C0 reaction temperature and screen solvents. Recommend only a batch that directly meets purity >=0.80 and fines <=0.50.
