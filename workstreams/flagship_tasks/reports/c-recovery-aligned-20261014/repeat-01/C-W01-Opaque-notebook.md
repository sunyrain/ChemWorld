# repeat-01 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:26:41.714408+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypotheses

H1 [tentative]
With opaque materials, catalyst/solvent identity and reaction temperature are the largest upstream uncertainties. A first screening batch at a moderate elevated reaction temperature should establish feasibility; later batches will vary identities before refining thermal history.

H2 [tentative]
For crystallization, controlled cooling plus modest seeding and a growth hold should reduce fines relative to an abrupt unseeded crash. If crystals remain sparse, a lower endpoint or longer hold is the next test; if fines are excessive, use slower cooling/warmer growth rather than more seed.

Pre-batch-1 expectation: 0.04 mol reagent with 0.005 mol catalyst in 0.08 L solvent, reacted near 350 K then slowly cooled and seeded, should produce detectable target crystals, though purity and recovery are unknown.

## Revision 2

Recorded: 2026-10-14T10:29:30.643399+00:00; available public operations: 138; reviewed through: runner-operation-0138.

# Source-stage hypotheses

H1 [supported in screened scope]
Catalyst C0 is the best of C0-C3 under the tested S0 conditions. Batch 1 (event runner-operation-0015) gave crystal yield 0.518 but excessive fines 0.872; C1-C3 batches 2-4 produced lower yields (0.318, 0.200, 0.312; events 0032, 0052, 0069). Because thermal histories were not identical for batch 1, the magnitude is confounded, but the catalyst ranking is sufficient to focus later work on C0.

H2 [supported in tested slow-cooling scope]
Solvent S2 with C0 and staged slow cooling gives compliant morphology and purity: batch 6 yielded 0.443, purity 1.00, fines 0.257 (event runner-operation-0103). S1 was also compliant but lower-yielding (0.341; event 0086); S0 and S3 were marginal/noncompliant in comparable slow-cooling runs. A 1:1 S0/S2 mixture was also compliant with yield 0.449 and fines 0.306 (event 0138), not clearly different from neat S2 given assay noise and single runs.

H3 [revised]
Slow staged cooling, seeding near 315 K, and low-agitation growth can reduce fines below 0.50 in favorable solvents. The first abrupt/shorter S0 process was noncompliant, while S2 batches were compliant. Solvent is a confound, so a general thermal-history effect remains unresolved. Reheating in the C2 run did not rescue morphology, but catalyst/solvent confounding prevents rejecting ripening generally.

Decision: retain C0 and S2 or S0/S2; use remaining batches to vary reaction temperature/time and then replicate the best compliant condition. A material improvement would require a crystal-yield increase exceeding the small batch-6/batch-8 difference while retaining purity >=0.80 and fines <=0.50.

## Revision 3

Recorded: 2026-10-14T10:30:58.532360+00:00; available public operations: 207; reviewed through: runner-operation-0207.

# Source-stage hypotheses

H1 [supported in screened scope]
Catalyst C0 is preferred among C0-C3 under the tested conditions. C1-C3 batches 2-4 had crystal yields 0.318, 0.200, and 0.312 (events runner-operation-0032, -0052, -0069), below C0 results. Exact effect size remains confounded by thermal-history differences in the earliest comparison.

H2 [supported in scope]
Solvent S2 combined with staged slow cooling, seeding near 315 K, and low-agitation growth reliably enabled high purity and low fines at moderate concentration. Batch 6 (0.08 L S2) was compliant at yield 0.443, purity 1.00, fines 0.257 (event 0103). A 1:1 S0/S2 mixture was likewise compliant but not clearly better (yield 0.449, fines 0.306; event 0138).

H3 [supported with a lower-concentration boundary]
Increasing reagent loading in S2 from 0.5 mol/L nominal (batch 6) to 1.0 mol/L nominal (batch 11) raised observed crystal yield from 0.443 to 0.488 while retaining purity 0.997 and fines 0.280 (events 0103, 0190). At 2.0 mol/L nominal, batch 12 raised yield to 0.518 but produced fines 1.00 and is noncompliant (event 0207). Thus the useful concentration window has a morphology boundary between the tested 1.0 and 2.0 mol/L points; differences are single-run observations, not repeatability estimates.

H4 [supported in tested range]
Reaction at 350 K for 3600 s outperformed a 330 K/7200 s test: batch 9 yielded only 0.316 and was marginally noncompliant for fines (event 0155). This comparison supports retaining 350 K/3600 s for C0/S2, though time and temperature were changed together.

Final decision
Recommend completed batch 11. It has the highest measured crystal recovery among batches satisfying purity >=0.80 and fines <=0.50: crystal yield 0.488, purity 0.997, fines 0.280 (event runner-operation-0190). Batch 12 and batch 1 had numerically higher recovery near 0.518 but failed the fines constraint. Conditions that would change this decision: a repeat showing batch 11 above the fines limit, or a compliant intermediate concentration between 1 and 2 mol/L with recovery above 0.488.
