# repeat-01 / C-W03-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:24:59.159941+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative, pre-experiment].** Solvent S2 should favor high recovery and large/low-fines crystals because its dossier combines low relative solubility and nucleation with high growth and low occlusion. S1 is the conservative purity comparator; S3 may improve reaction activity but crystallize less well.

**H2 [tentative, pre-experiment].** A high-conversion reaction followed by modest seeding, slow cooling, and a growth hold should meet purity >=0.80 and fines <=0.50. Excess seed or rapid/deep cooling may raise recovery but increase number-weighted fines.

**Plan/test.** First establish a S2/C1 baseline using near-full per-batch charge, warm reaction, then seed/slow cool/hold/filter. Subsequent batches will vary catalyst, solvent, temperature/time, seed dose, cooling rate/end point, and thermal history. A failure of S2 on purity or recovery will shift emphasis to S1 or mixed-solvent strategies.

## Revision 2

Recorded: 2026-10-13T11:25:58.498513+00:00; available public operations: 32; reviewed through: runner-operation-0032.

# Working hypotheses

**H1 [supported only for purity/recovery; contradicted for fines].** S2 produced high crystal purity (0.985 and 0.975) and substantial recovery (0.471 and 0.412) in batches 1–2, but both violated the fines constraint (0.683 and 1.000; final assays at runner-operation-0015 and -0032). Thus S2 remains useful only if its particle population can be controlled.

**H2 [revised].** Lowering seed from 0.020 g to 0.001 g while adding staged slow cooling and long holds did not reduce fines; the observed fines rose by about 0.32 despite confounding catalyst/reaction temperature and cooling path. A higher seed dose is now the leading test because more growth sites may moderate supersaturation, though its effect on number-weighted size is unresolved.

**H3 [tentative].** C1 at 373 K gave higher reaction selectivity/yield than C3 at 350 K in these confounded batches; keep C1 as current reaction baseline while screening crystallization. Test C2 separately before drawing a catalyst conclusion.

**Decision.** Next test 0.050 g seed with staged cooling in S2. If fines remain >0.50, prioritize S1 (lower stated nucleation tendency) and/or partial reheating/recooling to dissolve fines. Continue to treat numerical differences as provisional because recipes were not paired replicates.

## Revision 3

Recorded: 2026-10-13T11:26:59.156420+00:00; available public operations: 90; reviewed through: runner-operation-0090.

# Working hypotheses

**H1 [supported in current scope].** S2 repeatedly gives high crystal purity (~0.976–1.000) and recovery ~0.47–0.50 under direct/deep cooling, but deep-cool products are dominated by fines. S1 did not improve fines in the confounded batch 4 comparison (final fines clipped at 1.0).

**H2 [rejected as simple monotonic seed claim].** Across S2 batches, 0, 0.001, 0.020 and 0.050 g seed plus differing paths all gave excessive fines; 0.020 g in the simple batch-1 path remains the least-bad observed (0.683). Seed dose alone is not sufficient.

**H4 [unsupported by batch 6].** A 310 K reheat/recool cycle did not selectively remove fines; final fines were 1.0 (runner-operation-0090), confounded by the longer recool/hold.

**H5 [tentative, prospective].** Deep cooling itself drives secondary nucleation. Stopping at a shallow endpoint near 320 K may sacrifice recovery but could reduce fines below 0.50. If feasible, endpoint can then be lowered incrementally to maximize constrained recovery.

**Decision.** Screen shallow endpoint before more solvent or seed changes. Maintain C1/S2 and 0.020 g seed to compare with batch 1. If 320 K fails the fines constraint, test S0/S3 or very early filtration rather than further deep-cooling holds.

## Revision 4

Recorded: 2026-10-13T11:28:32.743468+00:00; available public operations: 158; reviewed through: runner-operation-0158.

# Working hypotheses

**H1 [supported in current scope].** S2 consistently provides crystal purity well above 0.80 and roughly 0.47–0.50 recovery under direct deep cooling, but full reagent loading produces excessive fines.

**H6 [supported provisionally; prospective extension].** Lowering reagent charge from 0.040 to 0.020 mol at nearly unchanged solvent, catalyst, seed and direct cooling reduced final fines from the full-loading range (best 0.683 in batch 1) to 0.591 in batch 11 while retaining 0.492 recovery and 0.994 purity (runner-operation-0158). This is a numerical improvement larger than assay noise, but the comparison is not a replicate and solvent volume differed slightly.

**Prospective prediction.** Further lowering reagent to 0.010 mol at 0.075 L S2 should reduce supersaturation/nucleation enough to cross fines <=0.50 while retaining useful seed-excluded crystallization recovery. This final batch will use the same C1, 0.020 g seed, reaction temperature and direct 278 K cooling as batch 11.

**Rejected/shelved alternatives.** Shallow endpoint, long holds, a 310 K reheat/recool, S0/S1/S3 substitutions, no seed, and washing/resuspension did not meet the fines constraint in the tested recipes (final assays through runner-operation-0158). Exact causal rankings remain confounded, but none merits the last batch over loading reduction.

## Revision 5

Recorded: 2026-10-13T11:29:00.939518+00:00; available public operations: 170; reviewed through: runner-operation-0170.

# Final source-stage interpretation

**Outcome.** No completed batch met both quality constraints. All final crystal purities were comfortably >=0.80, but every final fines fraction exceeded 0.50.

**H1 [supported for tested S2 recipes].** S2/direct deep cooling can recover about 0.47–0.50 of available target with very high crystal purity, but particle fines are the limiting attribute.

**H6 [narrowed, non-monotonic].** Moderate loading reduction to 0.020 mol reagent improved fines to the campaign minimum 0.591 while retaining 0.492 recovery and 0.994 purity in batch 11 (runner-operation-0158). The 0.010 mol continuation contradicted a monotonic loading hypothesis: batch 12 fines rose to 0.846 and recovery fell to 0.402 (runner-operation-0170). Thus an interior loading optimum is plausible, not established.

**Best constrained-near candidate.** Batch 11 is the closest approach: crystal_yield 0.492, purity 0.994, fines 0.591. It does not satisfy the fines specification and must not be described as qualified.

**Scope and gaps.** Seed dose, cooling history, solvent, stopping point, reheating, washing and upstream loading were explored without a qualifying batch. Comparisons are mostly single, partially confounded runs; particle-size assay noise is much smaller than the remaining 0.091 fines gap for batch 11, so qualification is not plausible from uncertainty alone. A future campaign should map reagent loading around 0.020 mol and alter seed size/quality or classification/filtration capability rather than merely deepening or extending cooling.
