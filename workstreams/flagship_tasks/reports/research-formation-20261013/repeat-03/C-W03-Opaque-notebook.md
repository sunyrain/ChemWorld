# repeat-03 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:42:44.951723+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## Prior expectations (before batch 1)
H1 [tentative]: Reaction performance will depend strongly on anonymous catalyst/solvent pairing and temperature; initial screening should separate upstream conversion/selectivity from crystallization recovery.

H2 [tentative]: For a productive liquor, modest seeding followed by slower cooling and a low-temperature hold should increase seed-excluded recovery and size while limiting fines versus abrupt unseeded cooling. This may fail if the solvent keeps product soluble or if excess seed dominates number counts.

Decision: screen diverse catalyst/solvent and thermal conditions, using final assays as authoritative; spend optional instruments mainly on promising slurries. A first result meeting purity >=0.80 and fines <=0.50 will establish feasibility, then later batches will optimize crystal_yield.

## Revision 2

Recorded: 2026-10-13T12:45:20.990350+00:00; available public operations: 48; reviewed through: runner-operation-0048.

# Hypothesis notebook

## Prior expectations
H1: Reaction performance depends on catalyst/solvent and temperature; initial screening separates reaction and crystallization effects.

H2 [partly supported, scope narrow]: A small seed dose plus warmer slow cooling/hold improved the number-weighted size/fines relative to batch 1, but neither met the fines constraint. Batch 1 (event stream around final assay runner-operation-0013) used 0.05 g seed and cooling to 275 K: recovery about 0.417, purity 0.980, fines about 0.899. Batch 2 (final assay near runner-operation-0026) used 0.01 g, cooling/holding at 300 K: lower recovery about 0.313 but fines about 0.803. Differences are confounded by catalyst and hold.

H3 [supported against large dose in tested scope]: Repeating seed additions to 0.5 g did not suppress fines; batch 3 gave fines about 0.963 and recovery about 0.196. Large seed dose is therefore suspended as an optimization path because it likely increases fine particle counts or competes for growth. Catalyst also changed, so causal attribution is not exclusive.

Next decision: prioritize very low seed dose or unseeded, high crystallization temperature, long growth hold, and low agitation; explore solvent/catalyst pairings. A result with fines <=0.50 will shift effort toward recovery optimization under that thermal regime.

## Revision 3

Recorded: 2026-10-13T12:47:27.157501+00:00; available public operations: 163; reviewed through: runner-operation-0163.

# Hypothesis notebook

## Final source-stage interpretation
H1 [supported in tested scope]: Solvent-S1 is the decisive crystallization choice relative to S0 under otherwise related processing. S0 batches 1–4 all had fines about 0.80–0.96, whereas S1 batches 5–12 consistently met the fines <=0.50 constraint while retaining high purity. Catalyst/solvent effects remain partly confounded in early screens, but the later S1/C0 series is internally consistent.

H2 [supported in tested S1/C0 scope]: With 0.005 g seed, 14,400 s slow cooling and a 14,400 s low-agitation hold, lowering the final temperature from 300 to 250 K increased observed crystal recovery from about 0.379 (batch 5) through 0.424, 0.455, 0.481, 0.488 to 0.501 (batches 6–10), without violating fines or purity constraints. The monotone trend exceeds a single noisy comparison, although individual final assays have stated noise and temperature is not isolated from run-to-run process variation.

H3 [supported against excessive seeding]: Batch 3's 0.5 g total seed produced very high fines and low recovery. At 250 K in S1/C0, 0.02 g seed (batch 11) did not improve recovery over 0.005 g (batch 10). Thus 0.005 g is preferred; whether still lower seed is better remains unresolved.

Replication: Batch 12 repeated the selected 0.005 g/250 K process and gave recovery about 0.495, purity about 0.992, fines about 0.433, consistent with batch 10 (0.501, 0.976, 0.442) within measurement variability. This supports robustness near 0.50 recovery.

Decision: recommend completed batch 10 because it has the highest observed qualifying crystal_yield. Batch 12 is corroborating evidence and may be practically interchangeable given assay noise. Conditions: S1 (0.08 L), reagent 0.04 mol, C0 (0.005 mol), nitrogen control, reaction at 350 K for 3600 s with 500 rpm, seed 0.005 g, cool to 250 K over 14,400 s, hold 14,400 s at 100 rpm, then filter. This recommendation would change if repeat assays established batch 12 or another qualifying recipe has materially higher recovery.
