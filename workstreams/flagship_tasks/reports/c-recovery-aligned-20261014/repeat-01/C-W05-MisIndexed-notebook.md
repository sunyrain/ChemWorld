# repeat-01 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:01:22.383702+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Catalyst C1 should give high conversion at moderate temperature based on the nominal activity prior, while solvent S2 should favor lower solubility, crystal growth, and reduced impurity occlusion. A full-charge C1/S2 batch reacted near 350 K, then seeded and cooled slowly, is expected to exceed 0.10 overall crystal recovery with purity above 0.80 and fines below 0.50. This expectation is untested and may fail because world-specific material residuals are hidden.

## H2 [tentative]
Slow cooling plus a modest seed dose should trade nucleation/fines for growth and therefore improve size and fines relative to an unseeded or fast-cooled process. Yield may decline if the final temperature is too high. Testable consequence: at comparable upstream conditions, seeded slow cooling to a low but legal temperature should produce fewer fines than fast/unseeded cooling.

## Revision 2

Recorded: 2026-10-14T11:04:48.514465+00:00; available public operations: 81; reviewed through: runner-operation-0081.

# Working hypotheses

## H1 [revised: supported for purity, unresolved for optimal recovery]
Across S2 batches, all recovered solids were very pure (final assays at runner-operation-0014, -0027, -0040, -0055, -0068, -0081), supporting low impurity occlusion in this scope. C3 gave the highest observed crystal recovery (~0.47) and reaction yield among the catalyst screen (runner-operation-0068), but produced essentially all fines under that crystallization history. C1 gave lower recovery (~0.38–0.41) but the only near-passing fines result (~0.50–0.57; runner-operation-0014 and -0027). Catalyst effects are confounded with crystal loading/supersaturation and should not yet be treated as purely reaction effects.

## H2 [revised: simple seed-dose claim rejected]
The initial claim that a modest seed dose plus slow cooling necessarily suppresses fines is not supported. Very low seed produced nearly all fines (runner-operation-0040), while 0.02–0.05 g gave variable outcomes from near-threshold to all fines. Seeds were often added at 329–349 K and may have dissolved, so effective seed population is unresolved. A 315 K addition did not rescue the high-recovery C3 batch (runner-operation-0081).

## H3 [tentative, prospective]
Fines appear coupled to high product loading/supersaturation. Lower reagent concentration and/or a dissolution–recooling cycle may permit ripening and reduce fines while retaining useful overall recovery. Next test: C3/S2 with lower reagent loading and more solvent, followed by partial reheat and slow recooling. A passing fines fraction with materially retained recovery would support this; persistent fines near 1 would shift optimization back toward C1 and thermal holding.

## Revision 3

Recorded: 2026-10-14T11:06:42.119480+00:00; available public operations: 159; reviewed through: runner-operation-0159.

# Final working interpretation

## H1 [supported in tested scope]
S2 consistently gave very high crystal purity across all tested catalysts and histories. Catalyst C3 improved reaction and crystal recovery (maximum observed recovery about 0.494 in runner-operation-0094) but high product loading was accompanied by excessive fines (0.777 or higher in the C3 optimization batches). Thus recovery alone was not predictive of acceptable particle quality.

## H2 [rejected as a general rule]
Neither larger nominal seed dose nor slower cooling alone ensured fewer fines. Results varied strongly with upstream catalyst/loading and thermal history, and seed addition temperature likely altered whether seeds survived. The campaign does not isolate a monotone seed-dose effect.

## H3 [partially supported, insufficient]
Partial reheat or ambient warming could reduce fines in some C1/S2 conditions, but deliberate dissolution–recooling did not meet the <=0.50 constraint. The closest result was batch 1 (runner-operation-0014): crystal yield 0.3843, purity 0.9894, fines 0.5031. The difference from the 0.50 limit is small relative to the declared final-assay noise scale, but the observed value is still formally noncompliant. All later batches had higher observed fines; the highest recovery, batch 7, had fines 0.7770.

## Decision
No completed batch met both formal quality constraints. Recommend completed batch 1 as the closest observed compromise and best candidate for confirmatory replication/particle-control refinement, not as a demonstrated compliant process. This decision would change if a confirmatory assay established fines <=0.50 for another batch with higher recovery, or if the specification were evaluated with an uncertainty-aware acceptance rule.
