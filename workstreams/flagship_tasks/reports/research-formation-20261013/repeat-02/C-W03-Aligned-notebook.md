# repeat-02 / C-W03-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:45:36.263642+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Within the supplied nominal dossier, S2 should favor larger, purer crystals and high recovery because it combines low solubility, low nucleation tendency, high growth, and low occlusion. A moderate seed dose plus slow cooling and a low-temperature hold should reduce fines relative to unseeded or rapid cooling. This expectation would be weakened if an S2 batch has poor reaction conversion or if particle/final assays show excess fines or purity below 0.80.

## H2 [tentative; pre-experiment]
C1 is the initial reaction catalyst choice because its nominal activity is high with less variability than C2/C3; reaction HPLC will be used selectively to distinguish actual fixed-world behavior. Higher reaction temperature/time may raise conversion but could increase degradation, so optimization should avoid needless severe exposure.

## Plan
First establish a feasible S2/C1 seeded slow-cool process, then vary catalyst/solvent, seed dose, cooling rate, hold, and thermal history. Prioritize final crystal yield subject to purity and fines constraints; numerical differences smaller than instrument/process uncertainty will remain unresolved.

## Revision 2

Recorded: 2026-10-13T11:47:26.120591+00:00; available public operations: 65; reviewed through: runner-operation-0065.

# Hypothesis notebook

## H1 [partly rejected; S2 purity/recovery useful, seed/hold size claim failed]
S2 processes gave high crystal purity (~0.97-0.98) and substantial recovery (~0.30-0.39), but all completed batches had fines near 1.0 and size indices only ~0.03-0.07 (final assays at events runner-operation-0015, -0030, -0065). Reducing seed from 0.05 g to 0.001 g and extending low-temperature hold did not meet the fines constraint; the numerical size changes are confounded by temperature and histories and are not reliable evidence of a seed-dose effect. An attempted 1e-6 g seed did not establish an effective seed population (runner-operation-0039), defining a practical lower limit above that value.

## H2 [supported only for conversion, selectivity unresolved]
C1 at 330-360 K reached near-complete conversion but selectivity remained only ~0.43-0.48 with moderate degradation. Crystal purity nevertheless passed 0.80, so upstream selectivity is not currently the binding constraint. Other catalysts remain untested.

## H3 [tentative; pre-test]
A partial-redissolution thermal cycle may preferentially remove fines and permit regrowth on surviving crystals. Prediction: heat a formed slurry moderately, then recool slowly; compared with single-pass S2 batches, particle-size assay should show fines materially below ~0.98. If not, shift solvent and cooling/nucleation strategy rather than simply extending isothermal holds.

## Decision
Test thermal cycling next, then compare solvent identities and low/no-seed nucleation. Continue prioritizing final crystal yield only among batches satisfying purity >=0.80 and fines <=0.50.

## Revision 3

Recorded: 2026-10-13T11:51:04.707420+00:00; available public operations: 224; reviewed through: runner-operation-0224.

# Hypothesis notebook

## H1 [supported in narrowed scope]
S2 supported high purity and useful recovery, but the original idea that seed reduction or long low-temperature holds alone would control fines was rejected: quenched single-pass batches 1-5 retained fines near 1.0 despite seed and hold changes (final assays runner-operation-0015, -0030, -0065, -0081, -0095).

## H2 [supported only for conversion; upstream selectivity not binding]
C1 at about 340 K repeatedly produced near-complete conversion while final selectivity was modest. Nevertheless S2 crystal purity repeatedly exceeded 0.97, so upstream selectivity did not prevent meeting the crystal-purity constraint in this campaign. Catalyst comparisons were confounded with downstream changes and do not justify a catalyst ranking.

## H3 [supported in tested S2 scope]
Avoiding the rapid quench and using a staged, seeded cool transformed the particle outcome. Batch 6 gave fines 0.210 with purity 1.000 and recovery 0.379 (runner-operation-0111), versus near-unit fines in quenched predecessors. Cooling farther to 250 K in batch 7 gave fines 0.141, purity 0.981, and the highest observed compliant recovery 0.396 (runner-operation-0129). Replicates/near-replicates remained compliant: batch 11, fines 0.148 and recovery 0.385 (runner-operation-0204); batch 12, fines 0.156 and recovery 0.387 (runner-operation-0224). This supports the thermal-history effect, not merely a numerical difference.

## Optimization interpretation
Batch 7 is the observed recovery leader among compliant batches. Its recovery advantage over batches 11-12 is only about 0.009-0.012, comparable to the stated final-assay recovery noise (0.01), so the exact ranking is not strong evidence of a reproducible yield difference. Reduced solvent loading (batch 8) and altered seed/loading/extra staging (batches 9-10) remained compliant but did not improve observed recovery (runner-operation-0146, -0164, -0186). Longer terminal holding in batch 12 did not clearly improve recovery over the baseline staged process.

## Final decision
Recommend completed batch 7: S2 at 0.08 L with 0.04 mol reagent and C1 at 0.005 mol; react near 340 K, do not quench, seed with 0.01 g, cool in long stages through 315/300/285/270 to 250 K, hold twice at low agitation, then filter. It maximized observed seed-excluded recovery while clearly meeting purity and fines constraints. Replicates 11-12 establish that the compliant particle outcome is reproducible, while the exact recovery lead remains within uncertainty.
