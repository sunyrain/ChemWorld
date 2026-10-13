# repeat-02 / C-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:20:22.811380+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Solvent S2 should favor high recovery and acceptable morphology because its dossier combines low relative solubility, high growth, low nucleation and low occlusion. Catalyst C1 is the initial reaction prior because of high panel activity with lower variability than C2/C3. A moderate seed dose and slow cooling/hold should reduce fines versus unseeded or rapid cooling.

**Testable expectation before batch 1:** a C1/S2 reaction followed by seeding and controlled cooling will produce measurable crystals; slower growth-focused thermal history should improve fines and purity, while colder endpoints should primarily increase recovery.

Unresolved: actual reaction-temperature optimum, catalyst residuals, seed-dose optimum, and whether low-solubility S2 impairs upstream conversion.

## Revision 2

Recorded: 2026-10-13T17:24:44.366512+00:00; available public operations: 138; reviewed through: runner-operation-0138.

# Working hypotheses — final source-stage revision

## H1 [supported in tested scope]
For S1/C1, reducing seed dose from 0.05 g to 0.005–0.001 g improved the morphology/constraint outcome without sacrificing recovery. The 0.05 g S1 result was borderline/high in final fines (event `runner-operation-0046`, 0.520), whereas 0.005 g at 285 K met the limit (event `runner-operation-0093`, 0.481) and 0.001 g at 278–270 K also met it (events `runner-operation-0104`, 0.490; `runner-operation-0115`, 0.497). This is evidence over several batches, but endpoint temperature and run-to-run noise are confounded with dose except for the broader contrast.

## H2 [supported in tested scope]
Cooling endpoint trades recovery against fines near the constraint boundary for low-seed S1/C1. At 270 K, batch 10 gave higher recovery (0.373) but fines very near 0.50 (`runner-operation-0115`); at 260 K, recovery rose to 0.383 but fines failed at 0.529 (`runner-operation-0126`). Thus 270 K is the practical lower endpoint from these tests, not necessarily a mechanistic optimum.

## H3 [supported for selection; mechanism unresolved]
S1/C1 outperformed initial S2 morphology expectations. The initial S2 batch had high purity and recovery but excessive fines (`runner-operation-0013`), and the long-cool S2 alternatives remained borderline or failed (`runner-operation-0024`, `runner-operation-0035`). S1/C1 low-seed batches produced the best constraint-feasible recoveries.

## H4 [unresolved]
A warm reheat/recool cycle did not improve the observed morphology in the one tested implementation (`runner-operation-0059`), but this single confounded test does not reject optimized ripening cycles. Likewise, a repeated isothermal cooling command did not clearly improve final fines (`runner-operation-0071`).

## Decision
Recommend batch 12 (`runner-operation-0138`): it is constraint-feasible with final crystal recovery 0.358, purity 0.990, and fines 0.488, and has more margin to the fines limit than batch 10 despite slightly lower recovery. Batch 10 has the highest feasible observed recovery (0.373) but only ~0.003 fines margin, smaller than measurement/process uncertainty, so it is not the robust recommendation. This decision would change if replay/replication established batch 10 fines reliably below 0.50.
