# repeat-01 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:43:20.004586+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the anonymous dossier, solvent S2 should favor larger, purer crystals and lower fines because it has the highest nominal growth and lowest nucleation/occlusion tendencies, but its lower solubility may trade against reaction performance. I expect seeded slow cooling in S2 after a high-activity catalyst reaction to meet purity >=0.80 and fines <=0.50 more readily than fast unseeded cooling.

## H2 [tentative]
Catalyst C1 is the initial reaction choice because its nominal activity is highest; a moderate-to-hot reaction hold should raise conversion, while excessive high-temperature residence could increase degradation. An HPLC after reaction will decide whether to extend or quench.

## Initial test
Batch 1: full charge (0.04 mol reagent, 0.08 L S2, 0.005 mol C1), controlled hot reaction, quench, seed, slow cooling/hold, then filtration. This predicts feasible crystal recovery (>0.10), purity >=0.80, and fines <=0.50. Later batches will separate material and thermal-history effects.

## Revision 2

Recorded: 2026-10-14T10:48:26.080527+00:00; available public operations: 168; reviewed through: runner-operation-0168.

# Hypothesis notebook

## H1 [narrowed; supported only qualitatively]
Solvent S2 consistently gave high crystal purity, but the nominal expectation of low fines was not enough to meet the campaign limit. Direct seeded S2 crystallizations with C1 produced purity about 0.98–0.99 and recovery about 0.39–0.42, yet fines remained about 0.71–0.72 in the replicated full-loading recipes (final assays runner-operation-0014 and runner-operation-0091). Thus S2 is retained for purity/recovery, not claimed sufficient for particle control.

## H2 [rejected as an optimization rule]
Higher seed dose and longer/two-stage cooling did not monotonically reduce fines. The 0.05 g, two-stage batch reached fines 1.0 (runner-operation-0027), while 0.02–0.03 g direct-cooling batches remained near 0.72 (runner-operation-0014, runner-operation-0148). Differences are confounded in some comparisons, but the large-dose strategy is clearly not supported here.

## H3 [supported in tested scope]
Lower upstream loading improved particle quality. Reducing reagent from 0.04 to 0.02 mol (with 0.06 L S2, 0.0025 mol C1, 0.01 g seed, and a 14,400 s cool to 278 K) gave the campaign-best morphology: fines 0.559, CSD quality 0.662, size index 0.094, purity 0.995, and recovery 0.409 (runner-operation-0168). This is a numerical improvement over the replicated full-loading recipe, but it still misses the fines specification of 0.50, so the effect and an extrapolation to still lower loading remain unresolved.

## Other tested alternatives
C0, C2, and C3 substitutions, S1/S3 solvents, extended holds, and a filter–resuspend–reheat–recool cycle did not produce a compliant batch (final assays runner-operation-0027 through runner-operation-0136). The resuspension cycle increased fines to about 0.987 (runner-operation-0108), opposing the selective-fines-dissolution conjecture under those conditions.

## Decision
No completed batch met both purity >=0.80 and fines <=0.50. Recommend batch 12 only as the closest tested candidate and best basis for further work, not as specification-compliant. A future test would reduce loading modestly below batch 12 while preserving S2/C1 and slow direct cooling; success would require fines to fall below 0.50 without materially lowering its roughly 0.41 overall recovery.
