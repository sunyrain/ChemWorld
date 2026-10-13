# C-24 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T06:06:00.870545+00:00; public operations available: 0; reviewed through: not specified.

# Hypothesis notebook

## H1 [tentative]
Catalyst C1 or C3 paired with solvent S2 should give strong target formation, while S2's low nominal solubility and high growth/low occlusion should favor high recovery, purity, and low fines relative to S0. This prior may fail because fixed-world residuals are hidden.

## H2 [tentative]
A hot reaction followed by controlled cooling, moderate seeding, and a growth hold should outperform an unseeded/fast-cool process on fines without sacrificing much recovery. Reheating after nucleation may reduce fines but could lose recovery.

## Planned tests
Begin with a broad catalyst/solvent and thermal-history screen. Use paid HPLC selectively for reaction optimization and particle sizing for crystallization diagnostics. A quality-feasible result requires purity >=0.80 and fines <=0.50; among feasible batches, prioritize measured crystal_yield.

---

## Revision 2

Recorded: 2026-10-13T06:07:50.833455+00:00; public operations available: 57; reviewed through: runner-operation-0057.

# Hypothesis notebook

## H1 [partly supported; narrowed]
With solvent S2 at 350 K/3600 s and a 0.005 g seed followed by 265 K/14400 s cooling, C0 gave the highest measured crystal recovery among the four catalysts (batch 2: 0.398) and met both quality constraints (purity 0.982, fines 0.325). C3 was numerically close in recovery (batch 5: 0.397), so catalyst ranking is not secure without replication; C1 and C2 were lower in this screen (batches 3-4). The nominal dossier preference for C1/C3 is therefore not authoritative in this world.

## H2 [supported in tested comparison, mechanism unresolved]
Reducing seed from 0.05 g and cooling lower/longer coincided with a large fines reduction: batch 1 had fines 0.549, whereas batches 2-5 using 0.005 g and 265 K/14400 s had fines 0.325-0.419. This comparison is confounded by reaction temperature and catalyst, so the causal contributions of seed dose, cooling endpoint, and duration remain unresolved. Test isolated seed and cooling-history changes around the C0/S2 recipe.

## Decision
Use C0 provisionally for solvent and crystallization screens. Recommend only quality-feasible batches; maximize final-assay crystal_yield, treating differences near assay uncertainty as unresolved unless replicated.

---

## Revision 3

Recorded: 2026-10-13T06:09:06.306877+00:00; public operations available: 145; reviewed through: runner-operation-0145.

# Hypothesis notebook

## H1 [supported in tested scope]
C0/S1 is the leading material pair at 350 K/3600 s with controlled cooling. Batch 7 achieved crystal_yield 0.495 with purity 0.977 and fines 0.414. S0 gave similar recovery (0.483) but failed the fines constraint badly (batch 6, 0.810); S3 also failed fines (batch 8). S2 was consistently lower recovery in two trials (batches 2 and 9: 0.398, 0.423) but had lower fines (~0.32). Thus nominal S2 growth/occlusion advantages help CSD but do not maximize constrained recovery versus S1.

## H2 [seed effect unresolved / small over tested range]
At C0/S1 and 265 K/14400 s, seed doses 0.001-0.05 g all produced feasible purity and fines, with crystal_yield 0.474-0.492 (batches 10-13), comparable to 0.495 at 0.005 g (batch 7). Numerical differences are modest relative to run variation; retain 0.005 g as a resource-efficient provisional dose.

## Next tests
Vary cooling endpoint and duration around C0/S1/0.005 g. Lower endpoints should increase recovery but may increase fines; a growth hold or mild reheat/recool may improve size distribution. A result changes the decision if it gives clearly higher measured recovery while retaining purity >=0.80 and fines <=0.50.

---

## Revision 4

Recorded: 2026-10-13T06:10:31.852804+00:00; public operations available: 244; reviewed through: runner-operation-0244.

# Hypothesis notebook

## H1 [supported in tested scope]
C0/S1 remains the leading material pair. Cooling endpoint showed the expected recovery trend: 250 K gave 0.499 recovery (batch 14) versus 0.458, 0.434, and 0.401 at 275, 285, and 300 K (batches 15-17), all quality-feasible. The effect is large and monotonic in this screen, although batches are unreplicated.

## H2 [revised: upstream history materially affects crystallization]
At fixed downstream conditions, reaction duration and temperature changed recovery and fines. Batch 21 (350 K, 1800 s) gave the campaign-leading recovery 0.569 with purity 0.986 and fines 0.455, while 7200 s lowered recovery to 0.398 (batch 22) and increased degradation warning. At 330 K fines failed (batch 18); 370 K was feasible with recovery 0.515 (batch 19); 390 K was borderline on fines (batch 20). This suggests impurity/degradation history modifies crystallization rather than recovery being purely solvent/temperature controlled.

## Final planned tests
Using the batch-21 upstream recipe, compare stopping after cooling against an added growth hold and against a mild reheat/recool history. Batch 21 is the provisional recommendation; replace it only if a later quality-feasible batch clearly improves measured recovery.

---

## Revision 5

Recorded: 2026-10-13T06:11:33.366138+00:00; public operations available: 269; reviewed through: runner-operation-0269.

# Hypothesis notebook

## H1 [supported in tested scope]
The best constrained region found uses C0/S1, a 350 K reaction, short 1800 s reaction time, 0.005 g seed, and cooling to 250 K over 14400 s. Batch 21 measured crystal_yield 0.569, purity 0.986, and fines 0.455 (final assay event runner-operation-0233), satisfying both constraints. Lower cooling endpoints improved recovery in the endpoint screen (batches 14-17), and extending reaction to 7200 s reduced recovery while increasing degradation warning (batch 22).

## H2 [growth hold useful for robustness, not maximum recovery]
Continuing growth for 7200 s after reaching 250 K gave batch 23 recovery 0.551, purity 0.994, and fines 0.411 (runner-operation-0256). Relative to batch 21, recovery was numerically lower by about 0.018 but fines improved by about 0.044. Given single-run assay uncertainty and uncontrolled run variation, the recovery difference is modest; batch 23 is a quality-margin alternative, while batch 21 remains the maximum measured feasible recovery.

## H3 [reheat/recool rejected in tested form]
A 270 K cool, 300 K reheat, and 250 K recool produced recovery 0.539 but fines 0.597 (batch 24, runner-operation-0269), failing the fines constraint. This rejects that specific thermal history, not reheating in general.

## Final decision
Recommend lifecycle batch 21 because it has the highest measured seed-excluded crystal recovery among quality-feasible completed batches. Batch 23 is the fallback when a wider fines margin is valued. Material rankings and thermal effects are limited to the tested anonymous benchmark world; unreplicated small differences remain uncertain.

---
