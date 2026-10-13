# repeat-01 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T16:43:06.401838+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative; pre-experiment]** Solvent S2 should give the best feasible crystals because the dossier combines low solubility/nucleation/occlusion with high growth. Prediction: against S0/S1 at comparable reaction and thermal history, S2 will increase recovery and size while reducing fines and improving purity.

**H2 [tentative; pre-experiment]** Catalyst C1 is the best initial reaction choice based on nominal panel activity, but hidden residuals may reverse the ranking. Prediction: HPLC after a standardized hot reaction will distinguish catalyst/solvent combinations; C2/C3 remain alternatives.

**H3 [tentative; pre-experiment]** Moderate seeding followed by slow cooling and a cold hold should suppress fines relative to an unseeded or fast-cooled process; excessive seed may reduce the seed-excluded recovery metric. I will first establish material effects, then refine seed dose and thermal history. Numerical differences smaller than stated instrument/process uncertainty will remain unresolved.

## Revision 2

Recorded: 2026-10-13T16:45:26.100361+00:00; available public operations: 75; reviewed through: runner-operation-0075.

# Working hypotheses

**H1 [supported only for the tested S2 scope]** S2 with a staged, seeded slow cool can satisfy purity and fines constraints. Batches 2 and 4–6 gave final purity 0.978–1.000 and fines 0.347–0.394 (events runner-operation-0027, -0051, -0063, -0075). Other solvents remain untested, so the dossier-based solvent ranking is unresolved.

**H2 [rejected as a unique catalyst preference]** C1 is not clearly superior. At the standardized 350 K/1800 s reaction and identical S2 crystallization, C0, C1, and C3 all gave feasible crystals; C3 had the largest observed crystal recovery (0.568 at runner-operation-0075 versus 0.558 for C1 at -0027 and 0.555 for C0 at -0051), but these differences are near assay noise and are not yet evidence of a catalyst effect. C2 was numerically worse (0.442, -0063), confounded with reaction composition.

**H3 [supported in this process window]** The 0.05 g seed plus 320→260 K slow-cool process sharply reduced observed fines versus the initial 0.02 g process with a warming hold (0.35–0.39 versus 0.563 final; runner-operation-0027 and -0015). Seed dose and avoiding the warming hold are confounded. Continue using the feasible slow-cool platform, then isolate seed/thermal effects.

**H4 [tentative]** The 350 K/1800 s reaction is preferable to 335 K/3600 s for this fixed world: the cooler/longer batch had lower observed selectivity and recovery (runner-operation-0039). Test changes around the 350 K platform rather than assuming monotonic temperature behavior.

## Revision 3

Recorded: 2026-10-13T16:46:38.564695+00:00; available public operations: 136; reviewed through: runner-operation-0136.

# Working hypotheses

**H1 [supported in tested solvent set]** S2 is the best robust solvent for the constrained objective. Under the common 0.08 L seeded slow-cool platform it produced feasible recovery around 0.56 with fines below 0.40 (runner-operation-0027 and -0075). S0 gave higher numerical recovery but failed fines badly (0.687, -0087); S1 barely met fines with lower recovery (-0099); S3 failed fines and had lower recovery (-0111).

**H2 [unresolved among C0/C1/C3; C2 disfavored]** Standardized comparisons did not separate C0, C1, and C3 beyond assay-scale numerical differences. C3 remains the working choice because it had the largest observed recovery among the 0.08 L S2 comparisons (runner-operation-0075); this is a pragmatic selection, not a confirmed causal catalyst advantage.

**H3 [supported for feasibility, causal components confounded]** A 0.05 g seed and slow cooling avoid the excessive fines of the initial 0.02 g/warming-hold process (runner-operation-0015 versus -0027 and later). Seed dose, cooling duration, and absence of warming are not individually identified.

**H4 [supported locally]** Concentration raises recovery but also nucleation/fines. Reducing S2 from 0.08 to 0.04 L increased observed recovery to 0.586 but fines to 0.633 (runner-operation-0123). At 0.06 L with an added 300 K slow stage, recovery was 0.569 and fines 0.473 (runner-operation-0136), currently the largest clearly feasible result, although it is numerically tied with batch 6 within uncertainty.

**Final prospective test.** Use 0.055 L S2 with C3 and additional 310/290 K slow stages before 260 K. Prediction: recovery may exceed 0.569 while added growth time keeps fines at or below 0.50. If it fails the fines constraint, retain batch 11 (or batch 6) rather than extrapolating.

## Revision 4

Recorded: 2026-10-13T16:47:15.423550+00:00; available public operations: 149; reviewed through: runner-operation-0149.

# Final source-stage conclusions

**H1 [supported in this campaign]** S2 provided the most robust purity/fines tradeoff among all four tested solvents. S0's larger numerical recovery did not compensate for its clear fines failure (runner-operation-0087); S1 and S3 were inferior on recovery and/or fines (runner-operation-0099, -0111).

**H2 [unresolved among C0/C1/C3; C2 disfavored]** The campaign does not establish a catalyst effect among C0, C1, and C3 because their recovery differences were near measurement uncertainty and reaction composition is a potential confound. C3 was retained pragmatically after the standardized comparison; no broader catalyst mechanism is claimed.

**H3 [supported for the tested process family]** Seeded slow staged cooling produced feasible fines, whereas either the initial warming hold/low seed or increased concentration without extra staging produced excessive fines (runner-operation-0015 and -0123). The individual effects of seed dose and thermal history remain unresolved.

**H4 [supported locally]** Increasing concentration can improve recovery at the cost of fines. Thermal staging allowed an intermediate concentration to recover part of that gain: the prospective 0.055 L S2 batch reached crystal recovery 0.574, purity 0.998, and fines 0.482 (runner-operation-0149). This is the largest observed recovery satisfying both constraints, narrowly above batch 11 (0.569 recovery, 0.473 fines; runner-operation-0136). The difference is numerical, not evidence of a repeatable improvement.

**Decision.** Recommend batch 12 because it is the observed constrained optimum. Conditions: 0.04 mol reagent, 0.055 L S2, 0.005 mol C3; 350 K for 1800 s; cool to 320 K for 3600 s, add 0.05 g seed, then cool through 310 K, 290 K, and 260 K for 14400 s each; filter without a warming hold. The recommendation would change if replicate results put fines above 0.50 or showed batch 11's more conservative 0.06 L process to have equal/higher recovery.
