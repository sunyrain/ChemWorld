# repeat-02 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:28:17.933821+00:00; available public operations: 0; reviewed through: None.

# Hypotheses before experimentation

**H1 [tentative].** Solvent S2 should favor the quality-constrained objective because its dossier combines high crystal growth, low nucleation, low impurity occlusion, and low solubility. At equal reaction history, I expect slower cooling plus modest seeding in S2 to reduce fines versus rapid unseeded cooling, while maintaining or increasing recovery.

**H2 [tentative].** Catalyst C1 is the first reaction choice because of the highest nominal activity geomean; however, fixed world residuals may reverse the ranking. A hot hold should raise conversion until degradation begins, so HPLC will be used on early batches to locate a suitable reaction hold.

**Initial test.** Begin with 0.04 mol reagent in 0.08 L S2 and 0.005 mol C1, react hot, inspect HPLC, then cool slowly with a modest seed and hold before filtration. Later batches will vary catalyst/solvent, thermal history, and seed dose. Evidence that S2 gives poor conversion or fails the purity/fines constraints will change the solvent decision.

## Revision 2

Recorded: 2026-10-14T11:31:45.570815+00:00; available public operations: 135; reviewed through: runner-operation-0135.

# Source-stage hypothesis notebook — finalized

**H1 [supported in tested scope].** S2 with seeded cooling can produce high-purity crystals, but particle fines depend strongly on upstream reaction severity rather than on crystallization duration or seed dose alone. Early milder-reaction batches produced very high fines despite high purity (final assays runner-operation-0024, -0035, -0046). This contradicted the initial expectation that slower/longer cooling or seed-dose adjustment would by itself suppress fines.

**H2 [supported as a trade-off, mechanism unresolved].** In the fixed S2/C1 recipe, increasing hot-reaction severity reduced final fines but also reduced seed-excluded recovery, consistent with an upstream composition/byproduct-mediated crystallization change. The exact causal species is unassigned. At 405 K/5400 s, batch 8 met the fines constraint but had only 0.409 recovery (runner-operation-0092). Intermediate hot histories improved the constrained trade-off: batch 9 gave 0.434 recovery and 0.466 fines (runner-operation-0103); batch 10 gave 0.453 recovery and 0.471 fines (runner-operation-0114); batch 11 gave 0.462 recovery and 0.459 fines (runner-operation-0125). Numerical differences are larger than a single reported instrument noise scale in some comparisons, but process variability was not independently quantified.

**H3 [rejected in tested form].** Partial reheating/redissolution followed by recooling did not improve size distribution in the tested S2/C1 cycle; batch 6 returned fines near 1 with recovery 0.607 (runner-operation-0070). This does not exclude other reheating endpoints.

**Boundary uncertainty.** Batch 12 used a slightly milder 398 K/4200 s hot history and gave marginally higher recovery 0.466 but measured fines 0.504, just outside specification (runner-operation-0135). This locates the practical boundary near the batch 11 history, but assay noise and lack of replicate process variance make the exact threshold unresolved.

**Decision.** Recommend completed batch 11: it has the highest observed seed-excluded crystal recovery among batches whose final assay satisfies purity >=0.80 and fines <=0.50. I would change this decision only with a confirmatory replicate showing batch 12 is reliably below the fines limit, or a nearby thermal-history experiment giving higher recovery with adequate margin to the fines boundary.
