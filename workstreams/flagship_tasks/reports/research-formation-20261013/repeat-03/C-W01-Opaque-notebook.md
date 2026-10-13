# repeat-03 / C-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:30:30.957145+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Reaction performance will depend strongly on anonymous catalyst/solvent pairing and temperature. Initial screen will compare pairings under a common moderate hot hold; HPLC conversion/selectivity will guide later batches.

## H2 [tentative]
For a productive reaction mixture, controlled seeded cooling followed by a low-temperature growth hold should improve seed-excluded recovery while limiting fines relative to an abrupt unseeded crash. Testable consequence: modest seed dose plus slow cooling should give crystal_yield >0.10, purity >=0.80, fines <=0.50.

## Decision plan
Use early batches for broad material/temperature and crystallization scouting, then exploit the best qualified recovery. Claims will remain unresolved where comparisons are confounded or within declared measurement noise.

## Revision 2

Recorded: 2026-10-13T12:32:13.806533+00:00; available public operations: 29; reviewed through: runner-operation-0029.

# Hypothesis notebook

## H1 [tentative]
C0/S0 at 360 K for 1 h gives complete conversion but only about 0.65 selectivity (HPLC event runner-operation-0007; final assays runner-operation-0016 and -0029). Material effects remain unscreened.

## H2 [not supported at tested seed dose]
A single 0.05 g seed addition plus slow cooling did not control fines: both deep cooling to 275 K and extended 300 K growth produced fines near 0.9, although crystal purity was ~0.97–0.98 and recovery 0.39–0.49 (events runner-operation-0016, -0029). The 300 K profile increased size numerically but still failed fines specification.

## H3 [tentative, prospective]
The seed dose may be far below the regime needed to suppress secondary nucleation. Next test raises total seed mass substantially at a warmer 310 K endpoint and long hold. If fines remain >0.5, I will prioritize thermal ripening/reheat or solvent effects rather than further small seed changes.

## Decision
Quality constraint, especially fines, is now primary; recovery optimization follows only among qualified batches.

## Revision 3

Recorded: 2026-10-13T12:32:47.991624+00:00; available public operations: 74; reviewed through: runner-operation-0074.

# Hypothesis notebook

## H1 [tentative]
C0/S0 at 360 K for 1 h reproducibly gives near-complete conversion but moderate selectivity. Reaction material effects remain unscreened.

## H2 [rejected for positive seed-dose effect in this scope]
Increasing total seed from 0.05 g to 1.0 g at 325 K worsened number-weighted fines (~0.94 at final assay, event runner-operation-0061) rather than suppressing them. Seed particles themselves and/or excessive nuclei likely dominate the number distribution. Further high-dose seeding is suspended.

## H3 [partially supported]
An unseeded cool–reheat–recool profile reduced fines numerically from ~0.89–0.94 to ~0.78 while preserving ~0.39 recovery and purity 1.0 (event runner-operation-0074). The comparison is confounded by seeding and trajectory but motivates stronger warm ripening. Next test reheats closer to 330 K and finishes warmer to preferentially remove fines; a qualified fines result would justify recovery tuning downward/upward around that profile.

## Decision
Focus remaining thermal exploration on unseeded reheat/recool, while reserving later batches for solvent/catalyst effects once a qualified particle regime is found.

## Revision 4

Recorded: 2026-10-13T12:33:44.170221+00:00; available public operations: 120; reviewed through: runner-operation-0120.

# Hypothesis notebook

## H1 [supported in screened scope]
At C0, 360 K reaction and common unseeded 300 K crystallization, solvent identity strongly affects particle outcomes. S2 gave final fines 0.244, purity 0.980 and recovery 0.448 (runner-operation-0109), clearly superior in qualification to S0/S3 and numerically better than borderline S1 (runner-operation-0098). Reaction selectivity remained moderate, but crystallization purity was high.

## H2 [rejected for positive high seed-dose effect]
High seed dose worsened fines in S0; do not use purchased seed for the current leading S2 regime.

## H3 [shelved]
Strong reheat at 330 K did not improve S0 and coincided with worse fines and degradation (runner-operation-0087). Reheat may be solvent-specific, but direct S2 cooling optimization has higher priority.

## Prospective optimization
Because S2 at 300 K has substantial fines margin below 0.50, lower endpoints may raise recovery. Next test 290 K under the same two-stage long cooling. If final fines remain qualified, continue lower or lengthen cold growth; if it fails, bracket between 290 and 300 K. Numerical changes will be interpreted cautiously against assay noise, but the large solvent differences exceed it.

## Revision 5

Recorded: 2026-10-13T12:34:44.591274+00:00; available public operations: 153; reviewed through: runner-operation-0153.

# Hypothesis notebook

## H1 [supported in screened scope]
S2 is the only clearly robust qualified solvent under the common C0/360 K/unseeded long-cooling process. Across endpoints 300, 290, 275, and 250 K, final purity was 0.978–0.993 and fines 0.241–0.276 (events runner-operation-0109, -0131, -0142, -0153).

## H2 [supported trend, not isolated replication]
Within the S2 endpoint series, recovery increased monotonically as the endpoint fell: about 0.448 (300 K), 0.475 (290 K), 0.512 (275 K), and 0.538 (250 K), while fines stayed well below 0.50. Temperature is confounded with batch variation, but the monotonic effect and magnitude motivate choosing 250 K.

## H3 [prospective]
At the minimum legal endpoint, extra low-temperature residence may further approach crystallization equilibrium without sacrificing the large fines margin. Final batch will repeat the leading recipe with twice the cold residence (four 14,400 s cooling/holding segments). If recovery does not improve beyond assay-scale variation, prefer the simpler batch 11 process; if it improves and remains qualified, select batch 12.

## Suspended alternatives
High seed dose and strong reheat are not supported in tested S0 scope. Catalyst optimization is lower priority because the stated recovery is normalized to target present before separation and S2 crystals already meet purity.

## Revision 6

Recorded: 2026-10-13T12:35:09.129693+00:00; available public operations: 165; reviewed through: runner-operation-0165.

# Hypothesis notebook

## H1 [supported in screened scope]
S2 is the robust qualified solvent under C0, 360 K for 1 h, unseeded crystallization. Its 250–300 K endpoint series consistently met purity and fines constraints; other screened solvents were inferior or borderline in fines.

## H2 [supported endpoint trend; residence effect unresolved]
Lowering the S2 endpoint from 300 to 250 K increased measured recovery from ~0.448 to ~0.538 without approaching the fines limit (events runner-operation-0109 and -0153). Doubling cold residence at 250 K produced recovery 0.541, purity 0.995, fines 0.284, size 0.112 and CSD quality 0.743 (event runner-operation-0165). The 0.003 recovery difference versus batch 11 is smaller than the declared final-assay crystal-yield noise (0.01), so extra-residence benefit is unresolved rather than established.

## H3 [rejected/shelved in tested scope]
High seed dose did not suppress fines in S0, and strong reheat did not improve its outcome. These conclusions may not transfer to S2 but are not needed for the qualified recommendation.

## Final decision
Recommend completed batch 12 because it has the highest observed qualified seed-excluded recovery (0.541), with substantial margins on purity (0.995 >= 0.80) and fines (0.284 <= 0.50). Batch 11 is a shorter near-equivalent alternative; the observed recovery advantage of batch 12 is not evidence of a residence-time effect without replication.
