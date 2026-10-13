# repeat-03 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:23:07.078143+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the supplied nominal-property scope, S2 should favor low occlusion, rapid growth, and low solubility, so a productive C1/C3 reaction followed by modest seeding and slow deep cooling should give the best chance of high recovery with purity >=0.80 and fines <=0.50. This prior may be misindexed; direct observations govern.

## H2 [tentative]
Fast/deep unseeded cooling should raise recovery but may increase fines; seeding near the onset of supersaturation followed by a hold should trade nucleation for growth. A warm digestion/reheat after initial nucleation may reduce fines, but could sacrifice recovery unless followed by deep recooling.

Initial screen decision: vary catalyst/solvent first while keeping charge near 0.04 mol reagent, 0.005 mol catalyst, and 0.08 L solvent. Use HPLC or particle size selectively, then refine thermal history. Material dossier is prior evidence only.

## Revision 2

Recorded: 2026-10-13T12:26:42.123107+00:00; available public operations: 83; reviewed through: runner-operation-0083.

# Hypothesis notebook

## H1 [supported in screened scope]
C0 is the most promising screened catalyst at 350 K/1800 s. With S2 it gave final reaction yield about 0.575 and crystal recovery 0.388 with passing purity/fines (event runner-operation-0038), whereas C2/S2 gave lower recovery 0.339 under a somewhat deeper crystallization endpoint (runner-operation-0050). The comparison is confounded by final temperature, so catalyst superiority is strongest from the pre-crystallization HPLC screen (runner-operation-0032 versus runner-operation-0044), not from recovery alone.

## H2 [revised]
Slow cooling with 0.05 g seed can meet the fines constraint. For C0/S2, 300 K over 14400 s gave fines 0.380 and recovery 0.388 (runner-operation-0038). A deeper 290 K endpoint with C2/S2 also passed fines at 0.339 (runner-operation-0050). The earlier staged operation was confounded because an uncontrolled `wait` drifted from 330 K toward ambient; its high fines do not isolate staging (runner-operation-0021).

## H3 [tentative]
S1 offers the best recovery opportunity: C0/S1 at 290 K produced recovery 0.486, but fines 0.518 narrowly failed (runner-operation-0061). A slightly warmer endpoint (about 295-300 K), longer/slower cooling, or warm digestion should move fines below 0.50 while retaining recovery above the passing S2 baseline. S0 and S3 showed substantially higher fines at 290 K (runner-operation-0083 and runner-operation-0072), so they are deprioritized.

Decision: spend remaining batches refining C0/S1 endpoint, seed dose, and digestion/recooling; retain C0/S2/300 K as the current robust feasible fallback.

## Revision 3

Recorded: 2026-10-13T12:28:26.568709+00:00; available public operations: 137; reviewed through: runner-operation-0137.

# Hypothesis notebook

## H1 [supported in this campaign scope]
The most useful screened reaction condition was C0 with S1 at 350 K for 1800 s after charging 0.04 mol reagent, 0.005 mol catalyst, and 0.08 L solvent. This combination repeatedly gave high conversion, moderate selectivity/yield, and final crystal purity well above 0.80 (events runner-operation-0061, -0094, -0104, -0126, -0137). Material labels remain benchmark-specific.

## H2 [supported locally; boundary-sensitive]
For C0/S1 with 0.05 g seed, slow cooling to roughly 295-297.5 K is the observed purity/fines tradeoff region. At 295 K for 14400 s, batch 8 achieved recovery 0.495, purity 0.977, and fines 0.492 (runner-operation-0094). At 297.5 K, recovery fell to 0.470 while fines remained just passing at 0.497 (runner-operation-0126). The differences are numerical single-batch observations; variability and assay noise prevent a precise endpoint law.

## H3 [not supported / narrowed]
Warm digestion as tested (285 K crystallization, 315 K reheat, 290 K recooling) did not reduce fines: final fines were 0.666 at recovery 0.482 (runner-operation-0116). An added 295 K hold likewise did not reliably improve the boundary, ending at fines 0.507 and recovery 0.481 (runner-operation-0137). These failures do not exclude other reheating profiles.

## H4 [tentative seed-dose effect]
Reducing seed from 0.05 g to 0.02 g at otherwise similar C0/S1/295 K conditions numerically worsened fines (0.509) and reduced recovery (0.486; runner-operation-0104) relative to batch 8 (runner-operation-0094). With only one comparison and close-to-noise differences, treat this as directional rather than established.

## Final decision
Recommend completed batch 8 because it has the highest observed crystal recovery among batches that satisfy both constraints: recovery 0.495, purity 0.977, fines 0.492 (runner-operation-0094). The fines margin is narrow; batch 3 (C0/S2, 300 K) is a more conservative fallback at recovery 0.388 and fines 0.380 (runner-operation-0038). New evidence showing repeatable failure of batch 8 near the 0.50 fines limit would switch the decision toward a warmer endpoint or the S2 fallback.
