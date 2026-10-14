# repeat-02 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:20:29.804147+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative].** Solvent S2 should favor larger, purer crystals and fewer fines because its nominal profile combines high growth, low nucleation, low occlusion, and low solubility. A slow cooling ramp with modest seeding and a cold hold should increase seed-excluded recovery while keeping fines <=0.50. If early S2 batches fail purity or recovery, test S3 and solvent/material effects rather than assuming the dossier is correctly indexed.

**H2 [tentative].** Catalyst C1 is the best initial reaction choice from nominal activity; sufficient hot residence should raise conversion, while excessive temperature/time may increase degradation/byproduct. Compare catalyst/temperature after establishing a baseline.

**Initial testable expectation.** A 0.04 mol reagent, 0.005 mol C1, 0.08 L S2 batch reacted near 365 K, then slowly cooled to about 275 K, seeded modestly, held, and filtered will achieve crystal_yield >=0.10, crystal_purity >=0.80, and fines <=0.50. A pre-crystallization HPLC will diagnose whether a failure is upstream or separation-driven.

## Revision 2

Recorded: 2026-10-14T11:24:07.444879+00:00; available public operations: 145; reviewed through: runner-operation-0145.

# Working hypotheses — final source-stage revision

**H1 [supported in tested scope].** S2 with slow deep cooling produced high-purity crystals and acceptable fines once seed dose was reduced. The initial 0.020 g seed / 275 K history gave fines 0.519 and yield 0.317 (event runner-operation-0015), whereas 0.005 g seed / 260 K under improved upstream conditions gave fines 0.225–0.299 and yield 0.510–0.697 (events runner-operation-0063 through -0099). This comparison is confounded by changing reaction conditions, so it supports the combined process rather than an isolated seed effect.

**H2 [revised, supported in tested scope].** C0, not nominally favored C1, was the strongest tested catalyst. At 340 K/7200 s, C0 gave crystal yield 0.374 (runner-operation-0027), versus C2 0.301 and C3 0.347 in otherwise matched batches (runner-operation-0039, -0051). C1 at 365 K/7200 s suffered high byproduct/degradation and is not competitive (runner-operation-0015); temperature/time confounding prevents a pure C1-versus-C0 attribution.

**H3 [supported trend over tested coupled profiles].** For C0/S2, hotter-shorter reaction profiles improved final recovery and reduced degradation across 360 K/3600 s, 370 K/1800 s, 380 K/900 s, and 390 K/600 s: crystal yield rose from 0.510 to 0.605, 0.668, and 0.697 (runner-operation-0063, -0075, -0087, -0099). The 400 K/450 s batch was slightly lower at 0.691 (runner-operation-0111), so the optimum is near 390–395 K for roughly 600 s rather than monotonically hotter.

**H4 [best current decision].** Deep cooling to 250 K with 0.001 g seed preserved low fines and slightly improved recovery: batch 10 yielded 0.702 with purity 0.979 and fines 0.270 (runner-operation-0123). Unseeded batch 11 was numerically lower at 0.693 (runner-operation-0134), but the difference is comparable to assay noise and remains unresolved. Batch 12 at 395 K/600 s, S2, C0, 0.001 g seed, 250 K/14400 s gave the highest observed crystal yield 0.705, purity 0.995, and fines 0.260 (runner-operation-0145), meeting both constraints. Recommend batch 12; change this decision only if repeatability shows its small yield advantage over batch 10 is not robust.
