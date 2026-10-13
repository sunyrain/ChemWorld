# repeat-01 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:00:49.777466+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## Prior expectations (before batch 1)

**H1 [tentative].** Reaction performance will depend strongly on anonymous catalyst/solvent pairing and reaction temperature; screen broad categorical combinations first. I expect hotter/longer reaction to increase conversion but possibly increase byproduct.

**H2 [tentative].** For crystallization, a seeded slow cooling profile followed by a cold hold should improve seed-excluded recovery and reduce fines relative to abrupt unseeded cooling. Excess seed may inflate nuclei counts and fines, so initial trials will compare 0–1 g around a common thermal profile.

**Decision rule.** Early batches prioritize finding a feasible pairing (purity >=0.80, fines <=0.50, crystal yield >=0.10). Later batches refine cooling/hold and upstream loading around the best observed region. Instrument results, not anonymous labels, are authoritative.

## Revision 2

Recorded: 2026-10-13T17:02:53.734947+00:00; available public operations: 65; reviewed through: runner-operation-0065.

# Hypothesis notebook

## Prior expectations (before batch 1)
**H1 [tentative].** Reaction performance depends on catalyst/solvent pairing and temperature; hotter/longer reaction may raise conversion but byproduct risk rises.

**H2 [revised; supported for tested scope].** A two-stage slow cool (to 300 K, then 250 K; 4 h each) controls fines far better than a direct 250 K cool, while maintaining substantial recovery. Direct-cool batches 1–2 gave fines about 0.81 (events runner-operation-0013, -0026), whereas two-stage batches 3–5 gave about 0.27–0.46 (events -0039, -0052, -0065). Because catalyst and solvent also changed, exact effect size remains confounded, but the large consistent separation warrants using the staged profile.

**H3 [tentative].** Solvent S2 is the best current crystallization medium: batch 4 had crystal yield ~0.423, purity at ceiling, fines ~0.274 (event -0052), marginally better than S1 on recovery/fines. S3 was feasible but near the fines limit. Catalyst comparison remains confounded with solvent; C0/C1 appear to give higher reaction selectivity than C2/C3 in observed screens.

**Next tests.** Combine C1 with S2 under the staged profile; then test concentration, seed dose, intermediate temperature, and cold growth without warming. Retain purity >=0.80 and fines <=0.50 as hard selection constraints.

## Revision 3

Recorded: 2026-10-13T17:04:05.171902+00:00; available public operations: 116; reviewed through: runner-operation-0116.

# Hypothesis notebook

## Prior expectations (before batch 1)
**H1 [tentative].** Reaction performance depends on catalyst/solvent pairing and temperature; hotter/longer reaction may raise conversion but byproduct risk rises.

**H2 [supported in tested scope].** Staged slow cooling controls fines far better than direct cooling. Direct-cool batches 1–2: fines ~0.81 (events runner-operation-0013, -0026). Two-stage 300→250 K batches 3–9: fines ~0.23–0.46 (events -0039 through -0116). Categorical changes confound the exact effect size, but later repeated S2/C1 results remain consistently low-fines.

**H3 [supported in tested scope].** C1/S2 with 0.04 mol reagent in 0.08 L is the best tested combination. Batch 6 yielded ~0.440 at purity 1.00 and fines ~0.277 (event -0078). Reducing solvent to 0.06 L did not improve recovery (batch 7, event -0091), so concentrate-driven improvement is not supported.

**H4 [tentative].** Low seed dose (~0.01 g) may improve seed-excluded recovery and particle attributes relative to 0.05 g. Batch 8 gave yield ~0.451, fines ~0.232, size ~0.120 (event -0104) versus batch 6 ~0.440/~0.277/~0.065 (event -0078). However, these are single runs with instrument/process uncertainty; the unseeded result (batch 9, event -0116) was intermediate in yield and smaller in size.

**Next tests.** Retain C1/S2, 0.08 L, 0.01 g seed. Test a gentler three-stage cooling path and cold maturation without ambient warming, then replicate the most promising profile. A result exceeding batch 8 recovery while maintaining purity/fines constraints changes the recommendation.

## Revision 4

Recorded: 2026-10-13T17:05:21.217782+00:00; available public operations: 159; reviewed through: runner-operation-0159.

# Hypothesis notebook

## Final source-stage interpretation

**H1 [supported only qualitatively].** Anonymous catalyst/solvent choice affects reaction selectivity and crystallization behavior. C1/S2 was the most useful tested combination, though categorical effects were not isolated in a full factorial design.

**H2 [supported in tested scope].** Staged slow cooling is necessary for acceptable fines in this study. Direct 250 K cooling in batches 1–2 produced the highest apparent recoveries (~0.51–0.53) but failed the fines constraint badly (~0.81; events runner-operation-0013, -0026). Two-stage or gentler profiles yielded feasible fines in later batches.

**H3 [supported in tested scope].** C1/S2, 0.04 mol reagent, 0.08 L solvent, 0.005 mol catalyst, 360 K reaction for 1 h, 0.01 g seed, and 300→250 K cooling (4 h per stage) is the best observed constrained process. Batch 8 had crystal yield ~0.451, purity ~0.982, fines ~0.232, and size ~0.120 (event runner-operation-0104). All quality constraints were met, and its recovery exceeded every other feasible batch.

**H4 [unresolved effect, practical decision retained].** Lowering seed from 0.05 to 0.01 g numerically improved recovery and particle attributes when comparing batches 6 and 8 (events -0078, -0104), but these are single runs and the recovery difference is near combined measurement/process uncertainty. An unseeded batch was intermediate (event -0116). Use 0.01 g provisionally; replicate before claiming a causal seed effect.

**H5 [not supported as an improvement].** Three-stage cooling reduced fines further but did not exceed batch 8 recovery (batch 10: ~0.445 yield, ~0.178 fines; event -0130). A prolonged 250 K stage and a 310 K reheat/recool cycle also did not improve recovery (events -0144, -0159). The reheat cycle may trade recovery against ripening, but one experiment is insufficient to generalize.

**Recommendation decision.** Select completed batch 8 because it maximizes observed seed-excluded crystal recovery among batches satisfying purity >=0.80 and fines <=0.50. Batch 10 is a reasonable lower-fines alternative if robustness of particle specification is valued over the small recovery difference.
