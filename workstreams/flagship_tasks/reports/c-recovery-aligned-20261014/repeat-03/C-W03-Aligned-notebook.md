# repeat-03 / C-W03-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:52:05.552463+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative, pre-experiment]** Within the supplied prior, catalyst C1 or C3 and solvent S2 should favor product formation, while S2 should also improve crystal growth and reduce impurity occlusion. A full 0.04 mol charge in 0.08 L with 0.005 mol catalyst, controlled warm reaction, then slow cooling with modest seeding and a growth hold is expected to exceed 0.10 overall crystal recovery while meeting purity/fines constraints. This will be tested first; if conversion or selectivity is poor, catalyst/temperature will be varied, and if fines are high, cooling rate, seed dose, and growth hold will be varied.

Key uncertainty: nominal dossier may be misindexed or overridden by fixed residuals; actual analytical observations govern decisions.

## Revision 2

Recorded: 2026-10-14T11:54:22.423903+00:00; available public operations: 59; reviewed through: runner-operation-0059.

# Working hypotheses

**H1 [supported for reaction, unresolved for particle quality]** Solvent S2 with catalyst C1 at ~373 K gives near-complete conversion and about 0.59 reaction yield, leading to high-purity crystals and 0.476 overall crystal recovery (events runner-operation-0007, runner-operation-0015). Catalyst C3 at 363 K was lower-yielding by HPLC (~0.50) and final recovery (~0.43), although catalyst and temperature are confounded (runner-operation-0022, runner-operation-0059). Continue C1 as the reaction baseline; a later controlled temperature test can separate these factors.

**H2 [disconfirmed in tested range]** Raising seed charge from 0.05 g to 1.0 g plus a long low-temperature hold did not solve fines: particle fines estimates remained ~0.99–1.00 (runner-operation-0012, runner-operation-0051), despite a numerical size increase. A 300 K reheat/recool cycle increased final size index to ~0.092 but final fines still clipped at 1 (runner-operation-0059). Seed-dose benefit is therefore not supported in this range.

**H3 [tentative, pre-experiment]** Excess supersaturation/rapid passage through the crystallization window may dominate nucleation. A much slower multistage cooling profile with a minimal seed charge should reduce fines below the one-step cooling results. If this fails, solvent choice or stopping growth before late secondary nucleation becomes the next alternatives.

## Revision 3

Recorded: 2026-10-14T11:56:43.121927+00:00; available public operations: 144; reviewed through: runner-operation-0144.

# Working hypotheses

**H1 [supported in tested reaction scope]** C1 with S2, S1, or S0 at ~373 K gives near-complete conversion; S0 produced the highest observed reaction yield (~0.619) and crystal recovery (~0.494), whereas C3/S2 at 363 K was poorer, with catalyst and temperature confounded (runner-operation-0015, -0059, -0118, -0144). Crystal purities were consistently high (>0.97).

**H2 [rejected as primary explanation]** Neither 1 g seed plus extended holding/reheat nor very slow multistage cooling materially resolved the extreme fines in S2; all relevant fines estimates remained ~0.98–1.00 (runner-operation-0051, -0059, -0079, -0082, -0092 through -0105). Numerical size changes lack a consistent paired fines improvement.

**H3 [supported as a solvent-dependent lead]** Solvent identity dominates attainable particle distribution in the tested standard workup. S3 reduced final fines to ~0.662 with CSD quality ~0.584, while S0/S1/S2 remained near unity under similar or more intensive histories (runner-operation-0131 versus -0118 and -0144). This is still above the <=0.50 constraint and has lower recovery (~0.376).

**H4 [tentative, pre-experiment]** In S3, a larger seed population combined with extended low-temperature growth and a mild reheat/recool ripening cycle may lower fines from ~0.66 to <=0.50. If not, catalyst selection in S3 and alternative stopping temperatures are the remaining major levers.

## Revision 4

Recorded: 2026-10-14T11:59:13.463802+00:00; available public operations: 313; reviewed through: runner-operation-0313.

# Final source-stage hypotheses

**H1 [supported in tested scope]** Reaction and crystallization are strongly coupled to material identity. S0/C1 gave the largest unconstrained recovery observed (~0.494) but extreme fines (~0.987; runner-operation-0144). S3/C1 sacrifices some recovery but enables a qualitatively different particle regime.

**H2 [rejected as general control strategy]** For S2, larger seed charge, long holding, reheat/recool, and very slow staged cooling did not reduce fines below ~0.98 (runner-operation-0051, -0059, -0079, -0082, -0092 through -0105). These variables cannot be assumed transferable across solvents.

**H3 [supported, narrow process window]** With S3/C1, cooling only to 300 K gave fines ~0.756 (runner-operation-0225), whereas continued cooling to 250 K followed by twelve 4 h low-temperature holds produced purity ~0.976, fines ~0.388, and seed-excluded recovery ~0.427 (runner-operation-0241). The effect is associated with the combined deeper cooling plus long hold; those factors were not separated.

**H4 [supported catalyst specificity]** Repeating the deep-cool/long-hold S3 workup with C0, C2, or C3 did not reproduce compliant fines (all ~0.675–0.693; runner-operation-0265, -0289, -0313). Thus C1 is required within the tested catalyst set, despite C0 giving a numerically higher recovery than C1 under that workup.

**Decision.** Recommend batch 9: it is the only observed batch satisfying both purity >=0.80 and fines <=0.50, and its recovery (~0.427) substantially exceeds the initial feasibility target. Key unresolved question is whether the 250 K endpoint or the 48 h hold is the dominant cause; either change could invalidate compliance.
