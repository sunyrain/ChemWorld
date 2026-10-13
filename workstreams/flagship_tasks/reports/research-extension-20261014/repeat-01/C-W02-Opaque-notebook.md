# repeat-01 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T16:43:03.518120+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Within the legal anonymous-material space, catalyst and solvent identity will materially affect target formation and crystal recovery. A moderate hot reaction followed by controlled seeded cooling is expected to outperform unseeded rapid cooling in recovery while keeping fines below 0.50.

**Testable expectations:** HPLC after a standardized reaction will distinguish productive catalyst/solvent combinations; among adequately converted batches, slower cooling plus a growth hold (and possibly a mild anneal) should increase size/CSD quality and reduce fines. Excessively long/hot reaction may raise byproduct/degradation.

**Plan/decision rule:** use early batches to screen material identity and establish crystallization feasibility, then spend later batches on thermal history, seed dose, and upstream loading around the best observed region. Final selection will prioritize assay crystal yield only among batches meeting purity >=0.80 and fines <=0.50; numerical differences close to stated instrument noise will be treated cautiously.

## Revision 2

Recorded: 2026-10-13T16:48:48.938519+00:00; available public operations: 192; reviewed through: runner-operation-0192.

# Hypothesis notebook

## H1 [supported for reaction performance; rejected for fines control]
Catalyst-C0/solvent-S0 at full loading and about 360 K gives reproducibly high conversion and target yield, and cooling recovers roughly half of the target as high-purity crystals. Batch 1 (runner-operation-0015) and batch 12 (runner-operation-0192) support this scope; solvent substitutions in batches 3–5 did not improve the central crystallization problem.

The pre-experiment expectation that ordinary slow seeded cooling or annealing would suppress fines is rejected over the tested scope. Unseeded cooling, seed doses from 0.005 g to about 1 g, staircase cooling, extended holds, and repeated 305 K/cool cycles all left final fines near unity (final assays runner-operation-0015 through runner-operation-0192). Particle-size checks were consistent with a predominantly sub-20 µm population. Differences in size/CSD quality were not reliably accompanied by lower fines.

## H2 [supported in tested loading range]
Lowering reactant/catalyst loading reduced crystallization-stage recovery without solving fines: batch 10 gave crystal yield about 0.23 with fines 1.0 (runner-operation-0147), versus about 0.56–0.57 for several full-loading C0/S0 batches. Thus full loading is preferred if recovery is the priority.

## Final decision
No completed batch meets the fines constraint (<=0.50), although all reported crystal purities were comfortably above 0.80. Batch 12 is the least-bad recommendation because it has the highest observed crystal recovery (~0.574), high purity (~0.989), and the largest observed size index (~0.081) among the high-recovery runs, but its fines fraction is 1.0 and therefore it is explicitly noncompliant. A future campaign should reserve solvent for post-filtration resuspension/classification or test an operation regime outside the present cooling/seed scope; the current data do not establish that such a step would work.
