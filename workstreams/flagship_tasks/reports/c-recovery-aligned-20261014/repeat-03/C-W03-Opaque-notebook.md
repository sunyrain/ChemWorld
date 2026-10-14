# repeat-03 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:54:25.210787+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## Prior expectations (before batch 1)
**H1 [tentative].** Because identities are opaque, catalyst/solvent choice and reaction temperature may dominate target formation. A broad categorical screen is warranted before local optimization.

**H2 [tentative].** For crystallization, seeding before a controlled slow cool and a low-temperature hold should reduce fines relative to an abrupt unseeded cool, while adequate reaction conversion and low-temperature residence should improve seed-excluded recovery. This may fail if the selected solvent retains product or if seed-induced nucleation creates many fines.

**Decision.** Use early batches to span catalyst/solvent and reaction temperature, with particle-size measurements on each batch when possible; then exploit the best spec-feasible region. A result would change this plan if no crystals or inadequate purity are observed.

## Revision 2

Recorded: 2026-10-14T12:00:02.513549+00:00; available public operations: 233; reviewed through: runner-operation-0233.

# Hypothesis notebook

## H1 [supported only for reaction/recovery ranking]
Within the tested recipes, C0/S0 near 370 K gave the strongest combination of target formation and seed-excluded crystal recovery. Batch 1 returned crystal yield 0.4855 and purity 0.9876 (runner-operation-0015), numerically the highest observed recovery. Related C0/S0 variants remained near 0.44–0.48 recovery (runner-operation-0070, runner-operation-0206, runner-operation-0233). Categorical and thermal changes were confounded in some comparisons, so this is a local process conclusion rather than a material main-effect estimate.

## H2 [rejected in the explored scope]
The prior expectation that seeding plus slow cooling/holding would bring fines below 0.50 was not supported. Small seed, repeated seed addition, no seed, long low-temperature holds, staged cooling, thermal cycling, and one resuspension/recrystallization all gave final fines about 0.99–1.00 (final-assay evidence runner-operation-0015, -0038, -0051, -0070, -0124, -0139, -0160, -0173, -0187, -0206, -0220, -0233). Particle-size readings before filtration agreed qualitatively (e.g. runner-operation-0012, -0035, -0048, -0067, -0121, -0136, -0149, -0170, -0184, -0203, -0217). Thus the campaign found no spec-feasible batch.

## H3 [unresolved]
Fines appear insensitive to the tested seed dose, solvent volume, endpoint temperature, and residence histories, but those factors were not independently replicated and measurement uncertainty plus recipe confounding prevent claiming zero effect. The consistently narrow outcome range suggests an untested control or crystallization regime may be required. A future test should alter growth/nucleation conditions orthogonally rather than repeat the tested cool-and-hold patterns.

## Final decision
Recommend batch 1 because it has the highest observed seed-excluded crystal recovery while meeting the purity constraint. It fails the fines constraint (0.9973), so the recommendation is explicitly the best non-feasible result, not a compliant process.
