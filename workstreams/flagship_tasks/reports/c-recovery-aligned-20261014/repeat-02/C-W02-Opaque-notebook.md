# repeat-02 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:28:53.966940+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Catalyst and solvent identities are opaque. I expect reaction conversion/selectivity to depend strongly on catalyst, temperature, and residence time; an initial screen should separate catalyst effects before crystallization optimization. A moderate reaction temperature (about 350 K), then seeded slow cooling to about 275 K and a growth hold, is expected to provide feasible recovery while limiting fines. This expectation will be rejected if the first screened recipes show negligible product or excessive impurity.

## H2 [tentative; pre-experiment]
For a given productive reaction, lower seed dose and slower cooling may reduce number-weighted fines and increase size, whereas deeper cooling/longer holding may improve recovery. A later factorial-style comparison should test this tradeoff.

## Revision 2

Recorded: 2026-10-14T11:33:21.776072+00:00; available public operations: 181; reviewed through: runner-operation-0181.

# Hypothesis notebook

## H1 [supported only for the screened conditions]
Catalyst C0 was the most productive catalyst in solvent S0 at 350 K/3600 s: its early HPLC yield exceeded the C1–C3 screen (events runner-operation-0007, -0021, -0035, -0049). Solvent identity also mattered: with C0, S2 substantially reduced fines relative to S0/S1/S3, although numerical comparisons remain confounded by batch-to-batch instrument/process variation (final assays runner-operation-0014, -0070, -0084, -0098).

## H2 [partly supported; broad claim rejected]
Slow staged cooling and seeding did not by themselves achieve the <=0.50 fines constraint. Across tested seed doses and histories, all final assays remained above the limit. A single 310 K dissolution/recooling cycle with C0/S2 gave the best observed compromise (batch 8, runner-operation-0115: recovery about 0.537, purity about 0.979, fines about 0.575), but the numerical improvement over uncylced batch 6 is not independently replicated.

## H3 [rejected in tested scope]
More aggressive or repeated reheating was not a reliable fines-removal strategy: batch 9 worsened fines after two cycles (runner-operation-0135), and final warm filtration after 325–330 K produced high fines and lower recovery in batch 12 (runner-operation-0181). Lower upstream reagent loading also failed to improve fines (batch 10, runner-operation-0152).

## Decision
No completed batch met both purity >=0.80 and fines <=0.50. I will recommend batch 8 as the closest quality/recovery compromise, not as a constraint-satisfying process. This decision would change if a replicate established a lower-fines S2 trajectory or if a future experiment found a selective fines-removal step below the 0.50 boundary.
