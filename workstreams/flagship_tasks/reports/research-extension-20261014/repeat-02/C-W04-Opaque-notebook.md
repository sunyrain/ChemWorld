# repeat-02 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:23:19.340115+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative]** Reaction performance will depend strongly on anonymous catalyst/solvent identity and temperature. Initial screen will vary these while holding charge near 0.04 mol reagent, 0.08 L solvent, and 0.005 mol catalyst.

**H2 [tentative]** For crystallization, moderate seeding followed by slow cooling and a cold hold should increase seed-excluded recovery while limiting fines compared with unseeded/fast cooling. Excess seed may inflate nuclei count and fines.

**H3 [tentative]** A sufficiently warm reaction hold followed by quench, controlled cooling, filtration should produce assayable target crystals. If early HPLC shows poor conversion or high byproduct, later batches will change catalyst/solvent or thermal severity.

Testable expectation for batch 1: catalyst-C0/solvent-S0 at elevated temperature, then seeded slow cooling, will give detectable product and nonzero crystal recovery; it may or may not meet purity/fines constraints.

## Revision 2

Recorded: 2026-10-13T17:26:09.475372+00:00; available public operations: 96; reviewed through: runner-operation-0096.

# Working hypotheses

**H1 [supported in tested scope]** catalyst-C0/solvent-S0 at 370 K for 1 h gives essentially complete conversion and about 0.63 selectivity/yield by HPLC (runner-operation-0007). Final assays of batches 1, 2, and 5 remain consistent with this reaction regime, whereas C1/S1 at 350 K was less selective and more byproduct-rich (runner-operation-0063). Identity effects remain confounded in the C1/S1 comparison.

**H2 [revised; unresolved]** Effective seeding is required for crystallization: 0.000001 g was accepted but ineffective and cooling failed (runner-operation-0024), while adding 0.001 g rescued crystallization. Across 0.001–0.02 g seed, low-temperature cooling produced high purity and substantial seed-excluded recovery (about 0.32–0.47) but nearly all particles were fines (runner-operation-0015, runner-operation-0040, runner-operation-0096). Thus “slow cooling alone limits fines” is opposed by current evidence.

**H3 [tentative]** Fines may arise from deep supercooling/secondary nucleation rather than insufficient elapsed time. Thermal cycling did not improve fines in one confounded trial (runner-operation-0083). A testable alternative is a long hold at mild supersaturation near 310 K with minimal effective seed, stopping before deep cooling. It should increase particle size with less secondary nucleation, though recovery may be lower.

Decision: prioritize meeting fines <=0.50 even at moderate recovery; if long mild-temperature growth still yields nearly all fines, explore solvent identity and post-filtration resuspension rather than simply extending cold holds.

## Revision 3

Recorded: 2026-10-13T17:28:28.233607+00:00; available public operations: 215; reviewed through: runner-operation-0215.

# Final source-stage hypotheses and decision

**H1 [supported in tested scope]** catalyst-C0/solvent-S0 at 370 K for 1 h gave the strongest observed reaction performance among the limited comparisons: essentially complete conversion with about 0.63 selectivity/yield by HPLC (runner-operation-0007). Changing both catalyst and solvent to C1/S1 reduced selectivity and increased byproduct (runner-operation-0063), but the individual identity effects were not separated.

**H2 [supported]** Effective seed population is necessary: 0.000001 g seed did not enable cooling (runner-operation-0024), whereas 0.001 g did. With S0, varied slow cooling, long holds, mild-temperature growth, and thermal cycling all retained very high fines fractions, despite crystal purity generally above 0.96 and recovery up to about 0.47 (runner-operation-0015, runner-operation-0040, runner-operation-0083, runner-operation-0118).

**H3 [supported in a narrow recipe comparison]** Solvent-S3 with 0.001 g seed and two-stage cooling to 300 K then 280 K reduced fines materially relative to S0/S1/S2 recipes. Batch 8 gave final fines 0.718, purity 0.968, and crystal recovery 0.415 (runner-operation-0148); an exact process replicate in batch 12 gave 0.733, 0.982, and 0.401 (runner-operation-0215). The repeat supports a real recipe-region difference, although neither meets the required fines <=0.50. Lower or higher seed, stopping at 300 K, or much finer staging all worsened fines in their single trials (runner-operation-0161, runner-operation-0176, runner-operation-0201).

**Decision.** No completed batch met both quality constraints. Select batch 8 as the closest observed compromise because it had the lowest final-assay fines fraction (0.718) while retaining high purity (0.968) and higher recovery (0.415) than its confirming replicate. This is not a compliant process recommendation; further work should focus on an untested lever for suppressing secondary nucleation or separating fines, using the S3/0.001 g region as the baseline.
