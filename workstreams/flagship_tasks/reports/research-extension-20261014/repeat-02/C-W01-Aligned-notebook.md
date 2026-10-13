# repeat-02 / C-W01-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:04:00.737519+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the supplied nominal dossier, solvent S2 should favor comparatively high crystal recovery, purity, and coarse growth because it combines low relative solubility (0.7), high growth (1.3), low nucleation tendency (0.65), and low impurity occlusion (0.65). The hidden fixed residual may reverse this ordering. Prediction: a moderate/high-conversion reaction in S2 followed by seeded, slow cooling and a cold hold will meet purity >=0.80 and fines <=0.50 and exceed the 0.10 feasibility recovery.

## H2 [tentative]
Catalyst C1 is the initial reaction choice because its nominal activity is high with less panel variability than C2/C3. Prediction: at matched loading and thermal history, C1 will provide a robust conversion/selectivity baseline; HPLC will decide whether catalyst or residence-time changes are warranted.

## Experimental decision
Start with 0.04 mol reagent, 0.08 L S2, 0.005 mol C1; run a controlled warm reaction, quench, seed, slow-cool, hold, and filter. Subsequent batches will vary one or a small number of levers around observed feasible conditions. Results inconsistent with adequate reaction conversion will trigger reaction-side changes; adequate conversion but poor recovery/fines will trigger crystallization-side changes.

## Revision 2

Recorded: 2026-10-13T12:05:57.651909+00:00; available public operations: 28; reviewed through: runner-operation-0028.

# Hypothesis notebook

## H1 [partly supported, quality constraint unresolved]
S2 gave high crystal purity in both completed batches, and the shorter reaction plus milder 290 K crystallization increased recovery from about 0.32 to 0.52 (final assays at runner-operation-0015 and -0028). However, both batches had essentially all particles below 20 um, so the original expectation that an ordinary seeded slow cool would satisfy the fines limit is rejected.

## H2 [revised]
C1 at 360 K reaches complete conversion rapidly. Cutting hot residence from 7200 s to 1800 s coincided with higher selectivity (~0.40 to ~0.67) and lower degradation warning (~0.29 to ~0.09), but reaction time is confounded with the crystallization recipe between events -0015 and -0028. Use the shorter hot residence as the working condition; a catalyst claim remains unresolved.

## H3 [tentative]
The fines failure reflects insufficient growth/aging relative to nucleation. Batch 2's milder endpoint and lower seed dose produced only a small numerical size improvement and did not satisfy fines. Prediction before batch 3: substantially extended isothermal aging near 300 K with a very small seed dose will shift the number distribution above 20 um while retaining useful recovery. If fines remain >0.50, test thermal cycling/reheating or upstream dilution rather than deeper cooling.

## Revision 3

Recorded: 2026-10-13T12:08:58.068159+00:00; available public operations: 185; reviewed through: runner-operation-0185.

# Hypothesis notebook

## H1 [supported only for purity; recovery/fines tradeoff]
S2 consistently produced very high crystal purity in the tested scope. High-load batches achieved much better seed-excluded recovery but essentially all-number fines; extended holds and thermal cycling did not resolve that conflict (final assays runner-operation-0028, -0049, -0068).

## H2 [working reaction condition]
C1 at 360 K with a short 1800–3600 s residence was operationally robust and generally avoided the severe degradation seen after the 7200 s baseline. Catalyst identity was not independently compared, so this remains a process choice rather than a causal catalyst ranking.

## H3 [supported loading threshold in tested S2 recipes]
Upstream dilution was the only tested lever that clearly crossed the fines specification. At 0.005 mol reagent in 0.08 L S2 with 0.05 g seed and 290 K crystallization, batch 7 gave purity ~0.992, fines 0, and recovery ~0.0119 (runner-operation-0107); a long hold replicate remained within quality but did not raise recovery (batch 10, runner-operation-0154). Raising loading to 0.007 mol caused fines ~0.995 (runner-operation-0133), while deeper/staged cooling at 0.005 mol likewise restored fines ~0.98 (runner-operation-0120 and -0172). Thus the observed feasible window is narrow and low-recovery.

## H4 [rejected in tested form]
Extended isothermal aging, gradual staged cooling, and simple cool/reheat thermal cycling did not selectively grow product without generating or retaining fines. Batch 12 reached recovery ~0.121 after cool/reheat but fines remained 1.0 (runner-operation-0185).

## Final decision
No completed batch met both quality constraints and the 0.10 initial recovery target. The target was stated as an initial feasibility target rather than a hard constraint; among batches satisfying the actual purity and fines constraints, batch 7 has the highest observed seed-excluded recovery (~0.0119 versus ~0.0090 for batch 10). Recommend batch 7 while explicitly noting its low recovery. This decision would change if a future recipe achieved fines <=0.50 and purity >=0.80 at recovery above ~0.012; the most relevant untested space is seed crystal size/quality or alternative separation of fines, neither available as a direct lever here.
