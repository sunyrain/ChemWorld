# C-24 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T05:52:17.271252+00:00; public operations available: 0; reviewed through: not specified.

# Initial hypotheses

**H1 [tentative].** Solvent S2 should favor the goal because its dossier combines low solubility and impurity occlusion with high growth and low nucleation. Prediction: relative to S0 under matched reaction and thermal history, S2 will give higher crystal recovery/purity, larger crystals, and fewer fines.

**H2 [tentative].** Catalyst C1 is the best initial reaction choice from nominal activity and variability; C2/C3 remain plausible fixed-world winners. A sufficiently hot but not prolonged reaction should improve target loading without excessive degradation.

**H3 [tentative].** Moderate seeding near the start of slow cooling, followed by a low-temperature hold, should suppress uncontrolled nucleation and grow fewer/larger crystals. Reheating may improve purity/size but could lower recovery unless followed by recooling.

Initial screening decision: establish a complete baseline in S2/C1, then vary catalysts, solvents, seed dose, cooling rate/end point, and thermal history. Instrument observations will override dossier priors.

---

## Revision 2

Recorded: 2026-10-13T05:54:54.036846+00:00; public operations available: 41; reviewed through: runner-operation-0041.

# Working hypotheses after batches 1-2

**H1 [partly supported].** S2 produces high-purity recovered solids (final purity about 0.98 in batches 1-2), but the current deep-cooling route gives almost entirely fines. Its favorable nominal growth/nucleation ranking therefore does not by itself prevent fines under a large temperature drop.

**H2 [supported only directionally].** Lowering the C1/S2 reaction from the batch-1 history (about 373 K/1800 s) to the batch-2 history (about 350 K/1200 s) improved measured HPLC selectivity/yield and lowered byproduct signal, but temperature and time changed together, so their individual effects remain unresolved. Both final crystallization recoveries exceeded the 0.10 feasibility target.

**H3 [disconfirmed in tested scope].** Increasing post-quench seed from 0.05 g to 0.50 g, together with slower cooling, did not solve fines: particle and final assays remained near a fines fraction of 1. This is a numerical comparison across confounded histories, not a clean seed-dose effect.

**H4 [new, tentative].** The abrupt 45 K quench may create nuclei before seeding; seeds added afterward cannot reverse that population. Prediction before batch 3: seeding before any large temperature drop and stopping at a warmer endpoint should materially reduce fines, possibly at the expense of crystal recovery. If fines remain near 1, test solvent/thermal cycling rather than further post-quench seed escalation.

---

## Revision 3

Recorded: 2026-10-13T05:56:33.313696+00:00; public operations available: 129; reviewed through: runner-operation-0129.

# Working hypotheses after batches 1-5

**H1 [supported in current scope].** S2 with direct seeded cooling can satisfy both quality constraints: batches 3-5 all had final purity well above 0.80 and fines below 0.50, with crystal recovery about 0.38-0.40.

**H2 [supported only directionally].** The milder C1/S2 reaction history near 350 K/1200 s remains preferable to the hotter/longer initial history for reaction selectivity; temperature and time are still confounded.

**H3 [rejected as a general rule].** Post-quench seeding is not an adequate fines-control strategy in the tested deep-cooling histories (batches 1-2). Seed dose alone cannot explain the improvement because the successful batches also omitted the quench and used warmer endpoints.

**H4 [supported in tested scope].** Seeding before the temperature drop and cooling directly, without the abrupt quench, markedly reduces fines. Batch 3 at a warm endpoint met the fines limit; batches 4-5 with 1.0 g total seed also met it. This supports a thermal-history effect, though direct-cooling endpoint, longer growth, and seed dose remain partly confounded.

**H5 [tentative].** A somewhat colder direct-cooling endpoint may raise recovery without violating the fines limit. Batch 5 (294 K, no separate hold) had lower measured fines than warmer histories and recovery near 0.40. Prediction: 290 K under the same seeded direct-cooling recipe will maintain fines below 0.50 and may improve recovery; failure would indicate a recovery plateau or renewed nucleation.

---

## Revision 4

Recorded: 2026-10-13T06:00:13.076823+00:00; public operations available: 354; reviewed through: runner-operation-0354.

# Working hypotheses after batches 1-12

**H1 [supported in current scope].** S2 with pre-drop seeding and direct cooling robustly satisfies purity and fines constraints over endpoints from about 298 K down to 250 K. All matched later batches remained high-purity and below the fines limit.

**H2 [supported only directionally].** The C1/S2 reaction near 350 K/1200 s is a workable upstream condition; final selectivity varies substantially between batches, so small numerical differences should not be overinterpreted.

**H3 [rejected as a general rule].** Post-quench seeding is not an adequate fines-control strategy in the tested deep-cooling histories.

**H4 [supported].** Avoiding the abrupt quench and seeding before cooling is the dominant observed change associated with meeting the fines limit. Under this route, colder endpoints increased final recovery from roughly 0.38 at the warm end to roughly 0.49 at 250 K while fines remained acceptable.

**H5 [supported with uncertainty].** Recovery increases as the direct-cooling endpoint is lowered in the tested S2/C1 range, apparently approaching a plateau near 0.49 at 250 K. Single-assay noise means adjacent endpoint differences are not necessarily effects.

**H6 [tentative].** A two-stage slow cool (350→300→250 K) improves particle-quality margin relative to a one-stage 350→250 K cool: batch 12 had much lower fines and higher CSD quality than batch 11, while recovery was numerically similar. Prediction: solvent changes will mostly shift recovery through solubility; S2 should remain best, but fixed-world residuals justify direct matched tests.

---

## Revision 5

Recorded: 2026-10-13T06:07:08.669206+00:00; public operations available: 616; reviewed through: runner-operation-0616.

# Working hypotheses after batches 1-20

**H1 [revised].** S1, not dossier-predicted S2, is the best observed solvent under matched two-stage seeded cooling. S1 batch 13 exceeded the analogous S2 recovery while meeting purity/fines constraints. S3 and S0 produced excessive fines in matched tests; S0 nevertheless had substantial recovery, so its failure is a particle-quality issue rather than absence of crystallization.

**H2 [revised].** Fixed-world catalyst behavior overrides the nominal panel prior. In the matched lower-loading S1 series, C3 gave the highest observed recovery and selectivity (batch 20), C0 was next (batch 17), C1 lower (batch 18), and C2 lower still (batch 19). Single runs leave repeatability unresolved, but the separation is large enough to prioritize C3.

**H3 [supported].** Avoiding the abrupt quench and seeding before cooling is associated with meeting the fines constraint. Two-stage 350→300→250 K cooling provides a strong fines margin for S1/S2.

**H4 [supported with scope].** Colder direct-cooling endpoints raised recovery in S2 up to the allowed 250 K endpoint while fines stayed acceptable; adjacent differences remain within assay uncertainty.

**H5 [new, supported by disconfirmation].** Stop and filter promptly after reaching the endpoint. Continuing under an additional 250 K controlled hold in batch 16 caused a severe loss of apparent recovery and a fines fraction near 1, contrary to the earlier growth-hold hypothesis. The exact cause (secondary nucleation versus redissolution/process transition) is unresolved, but operationally the hold is harmful.

**H6 [tentative].** Lower upstream loading may improve recovery/quality: the lower-loading C1 batch 18 numerically exceeded higher-loading C1 batch 13 in recovery, but the effect is modest and not replicated. Prediction: C3/S1 under the lower-loading, two-stage, prompt-filter route should remain the best feasible family. Thermal recycle or seed-dose changes may improve fines but should be accepted only if recovery is retained.

---

## Revision 6

Recorded: 2026-10-13T06:10:13.002869+00:00; public operations available: 754; reviewed through: runner-operation-0754.

# Final source-stage hypotheses (24 completed batches)

**H1 [supported in studied domain].** The robust feasible family is solvent S1 with catalyst C3, pre-drop seeding, two-stage direct cooling (about 350→300→250 K), and prompt filtration. It repeatedly gave purity near 1, fines comfortably below 0.50, and recovery around 0.62-0.63 (batches 20, 22-24; event endpoints runner-operation-0616, -0692, -0723, -0754).

**H2 [supported].** Experimental fixed-world rankings override the nominal dossier: S1 outperformed S2 for recovery under matched staged cooling, while S0/S3 failed the fines limit. In the matched lower-loading S1 catalyst screen, C3 was best observed.

**H3 [supported].** Abrupt quench followed by seeding generated excessive fines, whereas seeding before gradual direct cooling met the fines constraint. Two-stage cooling improved the fines margin relative to one-stage histories.

**H4 [supported operationally].** Stop growth promptly at the endpoint. An added controlled hold (batch 16) was strongly harmful. A reheat/recool cycle (batch 21) retained feasibility and gave the numerically highest recovery, but its advantage over simpler batches is far below assay noise and it worsened the fines margin; it is therefore not justified as the preferred added complexity.

**H5 [supported tentatively].** Reducing each upstream reactant from 0.0175 to 0.015 mol under C3/S1 retained or slightly improved recovery and selectivity in batch 24. This is one comparison, so the loading effect remains less certain than the catalyst/solvent/thermal-history conclusions.

**Final decision.** Recommend batch 24 rather than the numerically near-tied batch 21: batch 24 combines recovery about 0.632 with purity 1.00 and fines about 0.313, uses the simpler staged-cooling route without a thermal recycle, and has a larger quality margin. The observed recovery difference from batch 21 is not meaningful at the stated assay noise.

---
