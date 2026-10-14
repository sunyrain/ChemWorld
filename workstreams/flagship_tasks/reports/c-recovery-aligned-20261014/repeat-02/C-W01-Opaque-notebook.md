# repeat-02 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:25:42.220694+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Catalyst and solvent identities are opaque; reaction performance may vary strongly across their 4×4 combinations. Initial screen will hold reagent/catalyst loading and thermal history approximately fixed, while varying identities. Prediction: at least one combination will exceed 0.10 overall crystal recovery with purity ≥0.80 after seeded slow cooling; absence across a diverse screen would shift focus to temperature/time/loading.

## H2 [tentative]
For a productive reaction, a moderate seed dose followed by slow cooling and a low-temperature hold should reduce nucleation-driven fines versus unseeded or rapid cooling, though seed-excluded yield may be penalized by excessive seed. Later batches should compare thermal/seed conditions around the best reaction recipe.

Decision rule: prioritize qualifying crystal yield; use purity and fines as hard constraints, not composite score. Instrument readings will be interpreted with their declared noise and unknown process variability.

## Revision 2

Recorded: 2026-10-14T11:26:56.793323+00:00; available public operations: 13; reviewed through: runner-operation-0013.

# Hypothesis notebook

## H1 [partly supported]
The initial C0/S0 recipe (0.04 mol reagent, 0.005 mol catalyst, 0.06 L solvent; 370 K/3600 s) is chemically productive: batch 1 final assay gave overall crystal yield 0.524 and purity 0.985 (event runner-operation-0013). Thus the feasibility target is exceeded, but the product fails the fines constraint (0.745).

## H2 [challenged in tested conditions]
A 0.02 g seed and nominal 7200 s cool to 280 K did not prevent high fines in batch 1 (particle event runner-operation-0010; final event runner-operation-0013). The subsequent 3600 s wait warmed the slurry to 291.2 K (runner-operation-0009), confounding any interpretation of a true low-temperature hold. Alternatives are excessive supersaturation, insufficient seed, and secondary nucleation.

## H3 [prospective]
Higher solvent dilution, maximal allowed seed, and staged slow cooling should reduce fines by limiting supersaturation and providing growth surface, possibly at some yield cost. Reheating/recooling may ripen fines. Next decision: first test dilution + 0.05 g seed + staged slow cooling while retaining C0/S0 reaction chemistry.

## Revision 3

Recorded: 2026-10-14T11:28:32.281043+00:00; available public operations: 104; reviewed through: runner-operation-0104.

# Hypothesis notebook

## H1 [supported within screen]
Identity effects are consequential. Under the common 370 K/3600 s reaction and 0.08 L solvent, 0.05 g seed, two-stage 320→270 K cooling, S2/C0 (batch 7) gave the best qualifying outcome so far: crystal yield 0.537, purity 0.981, fines 0.131 (runner-operation-0091). S1 and S3 also controlled fines but had lower yields 0.469 and 0.441 (runner-operation-0078, runner-operation-0104). S0 was near the fines boundary and catalyst substitution did not clearly improve yield (batches 2–5; runner-operation-0026 through -0065).

## H2 [supported, scope limited]
Relative to batch 1, the combined changes of dilution, maximal seeding, and staged slow cooling reduced fines substantially (batch 2 final 0.491 versus batch 1 final 0.745), but those changes are confounded. The much stronger S2 result (0.131 fines) shows solvent identity dominates or interacts strongly with crystallization under the common protocol. Particle and final-assay values differ within declared noise/process variation but agree on qualitative ranking.

## H3 [prospective]
With S2/C0, conversion is already saturated while selectivity is only about 0.60 and degradation warning about 0.15 (runner-operation-0091). Lower reaction temperature with longer time, or reduced catalyst loading, may preserve conversion while improving target selectivity and therefore seed-excluded crystal yield. Next tests will retain the robust S2 crystallization protocol and alter one upstream factor at a time where possible.

## Revision 4

Recorded: 2026-10-14T11:29:33.596634+00:00; available public operations: 156; reviewed through: runner-operation-0156.

# Hypothesis notebook

## H1 [supported within explored domain]
S2/C0 is the preferred material pair. Under the common seeded two-stage cooling, it combined high recovery with a wide fines margin (batch 7: yield 0.537, purity 0.981, fines 0.131; runner-operation-0091). Other screened solvents either lowered recovery or approached the fines boundary; catalyst changes in S0 did not show a useful advantage.

## H2 [supported for S2 protocol]
The S2 crystallization protocol—0.08 L solvent, 0.05 g seed, 14400 s to 320 K then 14400 s to 270 K—consistently produced low fines in batches 7 and 9–12. Particle-size readings before filtration and final assays qualitatively agreed. This supports a robust margin below 0.50, though seed, dilution, and cooling effects were not individually resolved.

## H3 [supported trend, exact optimum unresolved]
For S2/C0 at fixed loading and crystallization, shorter/hotter reaction histories improved final recovery across the tested sequence: 350 K/7200 s gave 0.407 (runner-operation-0117), 390 K/1800 s 0.633 (runner-operation-0130), 410 K/1200 s 0.673 (runner-operation-0143), and 430 K/900 s 0.704 (runner-operation-0156). These are numerical differences from single batches with simultaneous temperature/time changes, so the separate causal effects and optimum beyond the explored boundary remain unresolved. Higher temperature did not breach the stated safety limit in the tested recipe.

## Final decision
Recommend completed batch 12: highest observed qualifying crystal yield 0.704, purity 0.996, fines 0.195, with the independent pre-filtration particle reading also showing fines 0.197 (runner-operation-0153). Batch 11 is the nearest tested alternative but has lower observed yield 0.673. The decision would change if replication showed batch 12's recovery advantage was not reproducible or if operation beyond 430 K/900 s were shown to improve recovery safely without raising fines or degrading purity.
