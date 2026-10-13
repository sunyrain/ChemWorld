# repeat-01 / C-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:04:52.882661+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

**H1 [tentative].** Solvent S2 should favor larger, purer crystals because its dossier combines high relative growth (1.3), low nucleation (0.65), and low impurity occlusion (0.65), while its lower relative solubility (0.7) may improve recovery. Prediction: a seeded, slow-cooled S2 batch will meet purity/fines constraints more readily than rapid/unseeded cooling; stronger cooling or longer low-temperature hold should raise recovery until fines or purity worsen.

**H2 [tentative].** Catalyst C1 is the best starting reaction catalyst from nominal geomean activity. A moderate-hot reaction hold should produce target without excessive degradation. HPLC, where used, will distinguish inadequate conversion from crystallization loss.

**Planned learning.** First establish a feasible S2 seeded slow-cool baseline, then vary reaction catalyst/temperature and crystallization seed dose, cooling rate, endpoint, hold, and reheat/recool. Numerical assay differences will be treated as suggestive unless replicated or substantially larger than stated instrument noise.

## Revision 2

Recorded: 2026-10-13T17:07:15.268365+00:00; available public operations: 57; reviewed through: runner-operation-0057.

# Working hypotheses after batches 1–5

**H1 [supported in tested S2 scope].** Deep, slow cooling in solvent S2 improves feasible crystallization recovery while retaining high purity and acceptable fines. Relative to 278 K runs (final assays runner-operation-0013 and -0024; recovery ~0.422, fines ~0.47–0.48), 260 K (runner-operation-0035) gave recovery ~0.447 and fines ~0.382, while 250 K/14,400 s (runner-operation-0046) gave the current best recovery ~0.472, purity 1.00, fines ~0.402. Differences in recovery from 278 to 250 K exceed a single assay noise scale, but the endpoint and duration are confounded.

**H2 [unresolved].** Within 0.01–0.05 g seed, dose has no demonstrated effect: the 0.01 g 250 K result (runner-operation-0057) was numerically close to the 0.05 g result, with differences comparable to assay variability. Test unseeded and/or replicate best condition.

**H3 [narrowed].** The 365 K/C1/S2 reaction is reproducibly complete but only moderately selective; nevertheless filtered crystal purity is 0.98–1.00 in tested batches. Because the objective is crystallization-stage recovery under crystal specifications, prioritize crystallization and concentration/solvent effects unless purity fails.

**Decision.** Continue testing concentration, solvent identity, staged cooling, and best-condition repeatability. Prefer immediate filtration after maintained low-temperature cooling; the batch-1 ambient-drifting wait is not necessary and confounds endpoint.

## Revision 3

Recorded: 2026-10-13T17:08:32.187858+00:00; available public operations: 135; reviewed through: runner-operation-0135.

# Final source-stage hypotheses

**H1 [supported in tested scope].** For C1/S2 reaction mixtures, deeper cooling to 250 K increases crystal recovery relative to 278 K while meeting purity and fines specifications when cooling is slow (14,400 s). Evidence: final assays runner-operation-0024, -0035, and -0046. Endpoint and duration were not fully factorial, so the claim is about the tested recipes rather than an isolated temperature coefficient.

**H2 [supported with a boundary].** Upstream concentration has a non-monotone quality tradeoff. At 0.055–0.060 L solvent per 0.040 mol reagent, direct 250 K cooling gave recovery ~0.48–0.495 with fines ~0.35–0.39 (runner-operation-0068, -0090, -0135). At 0.040 L, recovery was numerically high (~0.493) but fines failed at ~0.610 (runner-operation-0079). Thus concentrating beyond the tested feasible band triggers excessive nucleation/fines.

**H3 [supported in comparison tested].** Solvent S2 is preferred over S3 for the focused 0.055 L, 250 K slow-cool recipe: S3 met constraints but gave recovery ~0.479 and fines ~0.475 (runner-operation-0112), versus S2 direct-cool replicates with recovery ~0.495 and ~0.481 and fines ~0.380 and ~0.395 (runner-operation-0090 and -0135). This is limited evidence without a contemporaneous S3 replicate.

**H4 [unresolved].** Seed dose between 0.01 and 0.05 g did not show a clear effect (runner-operation-0046 vs -0057); unseeded behavior remains untested. A staged warm-to-cold trajectory was not superior: runner-operation-0124 gave recovery ~0.478, below the direct 0.055 L recipe's best result, though the difference from one direct replicate is near one assay-noise scale.

**Recommendation decision.** Select lifecycle batch 8 (runner-operation-0090): it has the highest measured crystal recovery among batches satisfying purity >=0.80 and fines <=0.50 (recovery ~0.495, purity ~0.986, fines ~0.380). Batch 7 had nearly comparable recovery but is ineligible because fines were ~0.610. Batch 12 is an exact recipe replicate supporting feasibility, albeit with recovery ~0.481. The recommendation would change if repeat assays established another qualifying recipe has higher expected recovery, or if the batch-8 fines result were not reproducible.
