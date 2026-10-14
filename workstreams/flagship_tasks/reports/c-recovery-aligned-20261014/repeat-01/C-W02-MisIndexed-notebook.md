# repeat-01 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:34:57.065118+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

**H1 [tentative]** — Solvent S2 should give the best crystallization quality because its nominal profile combines low solubility/nucleation/occlusion with high growth. Prediction: among otherwise comparable batches, S2 will reduce fines and raise purity/size versus S0; S3 is a plausible compromise.

**H2 [tentative]** — Catalyst C1 is the first reaction-screen choice due to highest nominal activity, but fixed-world residuals may reverse rank. Prediction: adequate hot reaction time with C1 and S1/S2 will produce more target than C0 at matched loading.

**Design decision** — Start with a baseline using 0.04 mol reagent, 0.005 mol C1, 0.08 L S2, hot reaction, quench, controlled seeded cooling and growth hold. Use early batches to screen catalyst/solvent and thermal history; change claims only after final assays/diagnostics. Quality constraints are purity >=0.80 and fines <=0.50; prioritize seed-excluded recovery among feasible batches.

## Revision 2

Recorded: 2026-10-14T10:37:06.326708+00:00; available public operations: 62; reviewed through: runner-operation-0062.

# Working hypotheses after five completed batches

**H1 [supported in screened scope]** — S2 is capable of high-quality crystallization: all tested S2 batches met purity and fines constraints. Slow cooling to 250 K without a subsequent ambient-temperature wait improved recovery and fines relative to the baseline that rewarmed during its wait (batch 1 assay, runner-operation-0014, versus batch 2, runner-operation-0026). This comparison is confounded by reaction temperature/time, so the thermal-history contribution remains unresolved.

**H2 [rejected as catalyst ranking; supported for C0]** — The nominal activity prior favoring C1 did not predict the realized best catalyst. At 360 K/1800 s in S2, C0 gave the highest observed reaction yield/selectivity and final crystal recovery (batch 3, runner-operation-0038; crystal yield about 0.617), while C2 was clearly poorer (batch 4, runner-operation-0050) and C3/C1 intermediate (runner-operation-0062/0026). Because each condition has one final assay, small differences are not treated as precise effects, but the large C0–C2 contrast is decision-relevant.

**H3 [tentative]** — With C0, reaction selectivity rather than crystallization purity currently limits seed-excluded recovery. Next tests will keep full charge and C0 while varying solvent and reaction temperature/time, then vary seed/cooling history around the best chemistry. I will retain low-final-temperature filtration and avoid uncontrolled warm holds. A result above batch 3 recovery while meeting purity >=0.80 and fines <=0.50 changes the incumbent.

## Revision 3

Recorded: 2026-10-14T10:39:05.281691+00:00; available public operations: 138; reviewed through: runner-operation-0138.

# Final source-stage hypotheses

**H1 [supported in this campaign]** — Catalyst C0 and solvent S1 form the best observed chemistry-quality combination. The solvent screen at 360 K/1800 s showed S1 feasible with recovery about 0.684 (batch 7, runner-operation-0082); S0 gave numerically lower-quality particles with fines about 0.74 despite good recovery (runner-operation-0072), and S3 failed the fines constraint (runner-operation-0092). S2 remained feasible but lower recovery in the matched catalyst screen (batch 3, runner-operation-0038).

**H2 [supported locally, optimum unresolved]** — For C0/S1, hotter and shorter reaction histories improved target formation versus 340 K/3600 s. At 370 K/1200 s, batch 10 achieved recovery about 0.719 with purity about 0.978 and fines about 0.464 (runner-operation-0114). At 380 K/600 s with 0.10 g total seed, batch 11 achieved the best feasible observed recovery, about 0.725, with purity about 0.994 and fines about 0.407 (runner-operation-0125). These are single assays, so the small recovery difference between batches 10 and 11 is numerical rather than a confirmed effect.

**H3 [qualified]** — More conversion does not guarantee a feasible product-size distribution. Extending the 380 K reaction to 900 s and using staged cooling raised observed recovery to about 0.741, but fines rose to about 0.565, violating the constraint (batch 12, runner-operation-0138). Reaction time and staged cooling are confounded in that comparison; the cause of the fines increase is unresolved.

**Decision** — Recommend completed batch 11 because it has the highest observed seed-excluded crystal recovery among batches meeting both constraints. Batch 12 has higher numerical recovery but is ineligible on fines. The recommendation would change if repeat assays showed batch 11 fines above 0.50 or if a repeated/stabilized batch 12-type cooling history brought fines below 0.50.
