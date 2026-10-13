# C-12 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T06:04:06.391641+00:00; public operations available: 0; reviewed through: not specified.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Within the available anonymous materials, solvent S2 should favor higher crystal recovery, larger particles, lower fines, and lower impurity occlusion than S0; S1 may be a robust intermediate. Catalyst C1 or C3 should outperform C0 in reaction productivity, while C2 may be variable. A slow cooling ramp, modest seeding near supersaturation, and a growth hold should reduce fines versus abrupt cooling.

Testable consequence: an initial full-charge S2/C1 batch with controlled reaction and seeded slow cooling should clear purity 0.80 and fines 0.50 while achieving crystal recovery above the 0.10 feasibility target. If reaction conversion is poor, change catalyst/thermal exposure; if purity/fines fail despite good reaction, focus on solvent, seed dose, and cooling history.

---

## Revision 2

Recorded: 2026-10-13T06:05:44.160066+00:00; public operations available: 15; reviewed through: runner-operation-0015.

# Hypothesis notebook

## H1 [partly contradicted; scope: S2/C1 at hot reaction]
The S2/C1 full-charge process gave complete conversion but low selectivity (~0.41) after 3600 s near 379 K (HPLC event runner-operation-0007; final event runner-operation-0015). Thus the prior that C1/S2 alone would provide strong reaction quality is not supported under this hot exposure; temperature or catalyst-specific residuals remain alternatives.

## H2 [supported directionally, insufficient]
S2 cooling produced high crystal purity (~0.985) and useful recovery (~0.32), but failed the fines constraint (~0.647) and had a very small size index (~0.064) at final assay (runner-operation-0015). A 14400 s ambient-warming wait after cooling produced a numerical size increase in particle measurements but little fines change (runner-operation-0010 versus runner-operation-0012); because temperature changed and only single noisy measurements exist, growth versus warming is confounded.

## Next tests [pre-specified]
Use lower reaction temperature and alternative catalysts, while seeding closer to the crystallization region rather than at ~379 K. Compare longer, colder, staged cooling and thermal ripening. A process will only be a recommendation candidate if final purity >=0.80 and final fines <=0.50; among such batches prioritize measured crystal recovery.

---

## Revision 3

Recorded: 2026-10-13T06:08:06.313879+00:00; public operations available: 93; reviewed through: runner-operation-0093.

# Hypothesis notebook

## H1 [supported in tested scope]
For S2 with 0.05 g seed, extended staged cooling ending in repeated 250 K crystallization stages can satisfy the fines constraint. Valid final assays include batch 2 (yield ~0.275, fines ~0.413; runner-operation-0028), batch 3 (~0.313, ~0.478; runner-operation-0041), batch 5 (~0.315, ~0.217; runner-operation-0067), batch 6 (~0.469, ~0.308; runner-operation-0079), and batch 7 (~0.475, ~0.276; runner-operation-0093). All also exceeded purity 0.80.

## H2 [supported directionally; plateau unresolved]
At the C1/S2, 380 K reaction condition, replacing the ambient-warming post-cool hold of batch 1 with staged 300→250 K processing and repeated cold stages substantially improved both valid recovery and fines (batches 6-7 versus batch 1). A fourth cold stage in batch 7 gave only a small numerical recovery increase over batch 6 (~0.006, smaller than combined single-assay noise scale), so a recovery plateau near 0.47 is possible but unresolved.

## H3 [narrow empirical decision]
C2 at 320 K performed poorly for target production and crystal recovery in batch 4 (runner-operation-0054), so suspend C2 testing. Continue C1/S2 around 380 K and test whether additional cold residence, solvent loading, or controlled thermal cycling raises recovery without reintroducing fines. Recommend by constrained crystal recovery, not reaction score.

---

## Revision 4

Recorded: 2026-10-13T06:09:39.074472+00:00; public operations available: 158; reviewed through: runner-operation-0158.

# Hypothesis notebook

## H1 [supported in tested scope]
C1/S2 at 380 K followed by seeded staged cooling to 250 K and repeated cold crystallization is the leading family. Batches 6-8 reached constrained crystal recoveries ~0.469-0.480 with fines ~0.276-0.308 (runner-operation-0079, -0093, -0110).

## H2 [supported trend, constraint tradeoff]
Reducing upstream reagent charge at fixed 0.08 L S2 increased observed seed-excluded recovery fraction and reaction selectivity: 0.04 mol batch 8 gave recovery ~0.480/fines ~0.276; 0.03 mol batch 10 ~0.496/~0.341 (runner-operation-0143); 0.02 mol batch 11 ~0.512/~0.439 (runner-operation-0158). This is a numerical monotone trend across nonreplicated batches, but fines worsen as loading falls. Alternative explanations include batch-to-batch process residuals.

## Final planned test [prediction before experiment]
Test 0.01 mol reagent with C1/S2 and the same 380 K reaction, adding more gradual 330→300→275→250 K cooling plus extended 250 K residence. Expect recovery potentially above 0.51, but fines are at risk of exceeding 0.50; the extra staged cooling is intended to keep fines compliant. If it fails fines, batch 11 remains the leading constrained candidate.

---

## Revision 5

Recorded: 2026-10-13T06:10:30.418036+00:00; public operations available: 179; reviewed through: runner-operation-0179.

# Hypothesis notebook

## H1 [supported in tested scope]
C1/S2 at 380 K followed by 0.05 g seeding, gradual cooling, and repeated 250 K crystallization is the leading process family. It repeatedly met purity and fines limits while reaching recovery near 0.47-0.51 (batches 6-8, 10-12; final-assay events runner-operation-0079, -0093, -0110, -0143, -0158, -0179).

## H2 [supported trend with unresolved plateau]
At fixed 0.08 L S2 and C1, lower upstream reagent loading increased observed recovery fraction and selectivity but initially worsened fines: batch 8 (0.04 mol) recovery ~0.480/fines ~0.276; batch 10 (0.03 mol) ~0.496/~0.341; batch 11 (0.02 mol) ~0.512/~0.439. Batch 12 at 0.01 mol plus more gradual/longer cooling gave ~0.513 recovery, ~0.361 fines, ~0.998 purity, and size index ~0.103 (runner-operation-0179). The batch 11→12 recovery difference is much smaller than assay noise and does not establish a real improvement; recovery appears near a plateau, while the better fines margin and other quality attributes favor batch 12 operationally.

## H3 [not favored]
A 310 K reheat/recool cycle reduced observed recovery and worsened fines relative to nearby noncycled batches (batch 9, runner-operation-0127), so thermal cycling is not recommended in this tested scope. C2 at 320 K also performed poorly (batch 4, runner-operation-0054).

## Decision
Recommend completed batch 12: it has the highest measured constrained recovery (~0.513, effectively tied with batch 11), ample purity/fines margins, and the best overall quality among the top-recovery candidates. This choice would change if replicate assays showed batch 11 reliably higher recovery or if process-time/throughput were weighted strongly enough to penalize batch 12's extended cooling.

---
