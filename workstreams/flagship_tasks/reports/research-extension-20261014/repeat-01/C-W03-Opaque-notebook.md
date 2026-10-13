# repeat-01 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:23:52.520846+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Reaction performance will depend strongly on catalyst identity and thermal exposure; initial batches will screen C0–C3 under matched charge and reaction conditions. A result with higher conversion/selectivity and lower byproduct signal will guide later batches.

H2 [tentative] Seeded, controlled cooling followed by a moderate growth hold should reduce fines relative to an unseeded or fast-cooled process, while lower final temperature should increase seed-excluded recovery. This could fail if solvent choice dominates solubility or if excessive nucleation occurs.

H3 [tentative] Solvent identity and seed dose may trade recovery against purity/fines. I will reserve later batches to combine the best upstream condition with slower cooling, growth holding, and possible thermal cycling. The decision criterion is maximum crystal_yield among batches satisfying purity >=0.80 and fines <=0.50.

## Revision 2

Recorded: 2026-10-13T11:25:54.822715+00:00; available public operations: 91; reviewed through: runner-operation-0091.

# Working hypotheses

H1 [supported only for current screen] All four catalysts reached near-complete conversion at 360 K/1 h in S0, but reaction selectivity differed. C3 gave the largest observed crystallization recovery (0.479) among catalyst-screen batches, only slightly above C0 (0.476) and C1 (0.472), so the catalyst recovery ordering is unresolved at assay noise scale; C2 was clearly lower (0.368). Evidence: final assays at runner-operation-0013, -0026, -0039, -0052 and HPLC events within those batches. Decision: retain C3 while attacking the binding fines constraint.

H2 [rejected for tested implementation] A single 4 h cooling ramp from about 314 K to 270 K plus 2 h hold and 0.05 g seed did not control fines: final fines were approximately 0.99–1.00 in every catalyst screen (runner-operation-0013, -0026, -0039, -0052). This does not reject seeding generally; it rejects this ramp/hold schedule.

H3 [supported in this scope] Changing from S0 to S1–S3 did not solve fines, and S3 reduced recovery materially. S0/C3 remains the working condition; observed final recovery/purity/fines were 0.479/1.000/1.000 for S0, 0.452/0.980/1.000 for S1, 0.469/1.000/1.000 for S2, and 0.361/0.972/0.987 for S3 (runner-operation-0052, -0065, -0078, -0091). Differences among S0–S2 recovery may include run noise and solvent-linked reaction confounding.

H4 [prediction before batch 8] Much slower staged cooling at minimum stirring should suppress secondary nucleation and allow seeded growth, lowering fines and increasing size relative to batch 4. If this is inadequate, a mild reheat/redissolution cycle followed by slow recooling is the next test.

## Revision 3

Recorded: 2026-10-13T11:26:47.771603+00:00; available public operations: 139; reviewed through: runner-operation-0139.

# Working hypotheses

H1 [supported only for screened recipes] C3/S0 remains the upstream choice. Across completed variants its reaction yield is about 0.58–0.59 and purity of recovered crystals about 0.98–1.00; therefore fines, not chemical purity, is the binding specification.

H2 [rejected for tested implementations] Neither a very slow staged cool/long hold (batch 8, runner-operation-0108) nor a 270→300→270 K thermal cycle (batch 9, runner-operation-0124) lowered fines materially; both assayed near 0.99–1.00 fines. Their observed recoveries near 0.50 show crystallization itself is feasible. These tests do not resolve whether a different reheat temperature would ripen crystals.

H3 [supported for recovery, not morphology] Raising loading by halving S0 volume to 0.03 L increased the observed recovery to 0.518 (runner-operation-0139), the largest so far, but fines remained 1.00. This recipe is infeasible under the stated fines constraint despite high purity.

H4 [prediction before batch 11] Late-stage secondary nucleation may dominate the number distribution. Stopping at a warmer temperature soon after limited seeded growth should sacrifice recovery but could sharply reduce the number fraction below 20 µm. If batch 11 meets fines <=0.50, batch 12 will adjust the stop temperature downward to seek more recovery; otherwise I will test an unseeded/limited-growth alternative.

## Revision 4

Recorded: 2026-10-13T11:27:24.947088+00:00; available public operations: 163; reviewed through: runner-operation-0163.

# Final source-stage conclusions

H1 [supported within this campaign] C3/S0 at 360 K for 1 h was the most useful upstream condition among those screened. Chemical purity was never the limiting constraint in the developed crystallizations; final crystal purities were generally about 0.97–1.00.

H2 [rejected across tested scope] The tested seed dose, slower staged cooling, long low-agitation holds, one mild reheat/recool cycle, warmer early stopping, and omission of seed all failed to bring fines near the <=0.50 requirement. Final fines stayed approximately 0.987–1.00 in every batch, well beyond instrument noise from the limit. Batch 11's warmer stop (runner-operation-0151) and unseeded batch 12 (runner-operation-0163) specifically oppose the late-secondary-nucleation and seed-caused-fines alternatives.

H3 [supported for recovery only] Higher loading (0.04 mol in 0.03 L S0) produced the largest observed recovery, 0.518 in seeded batch 10 (runner-operation-0139); unseeded batch 12 was similar at 0.512 (runner-operation-0163). These numerical differences are small relative to single-assay uncertainty/process variation and do not establish a seed effect.

Decision: no completed batch satisfies both purity >=0.80 and fines <=0.50. Batch 10 is the recommendation only as the highest observed recovery/high-purity starting point, explicitly not a specification-compliant process. Further work should change morphology-control factors not reached here (for example seed quality/size or a substantially different dissolution/antisolvent regime), rather than merely extending the tested cooling holds.
