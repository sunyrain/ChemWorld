# EC-optimization — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T05:13:44.204176+00:00; public operations available: 0; reviewed through: not specified.

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading (0.020 mol reagent in 0.050 L solvent), the balanced score should show an interior optimum in potential/current/time: insufficient charge limits conversion, while excessive forcing lowers selectivity and energy efficiency. Prediction before experiments: a moderate potential magnitude, nonbinding-to-moderate current cap, and intermediate duration will outperform both mild/short and aggressive/long conditions.

## H2 [tentative]
Anonymous solvent and electrolyte identities may strongly affect transport, ohmic efficiency, and selectivity. Initial factorial screening should identify promising S/E combinations before local optimization. Because identity-property mapping is unavailable, no direction is asserted in advance.

Plan: use one UV-vis measurement per batch after electrolysis to spend the 12 intermediate measurements consistently; final assay remains authoritative. Early batches screen sign, materials, and forcing; later batches refine the best region and assess repeatability. Numerical differences smaller than declared measurement noise will remain unresolved.

---

## Revision 2

Recorded: 2026-10-13T05:15:23.991574+00:00; public operations available: 28; reviewed through: runner-operation-0028.

# Electrochemical campaign hypotheses

## H1 [supported qualitatively; optimum unresolved]
At fixed 0.020 mol / 0.050 L loading, forcing has a nonmonotone effect. Mild positive operation (+1.0 V, 100 mA cap, 1800 s, S0/E0) gave high selectivity (~0.95) but only ~0.038 conversion and score ~0.325 (event runner-operation-0007). Reversing sign while increasing cap/time (-1.0 V, 500 mA, 7200 s) raised conversion only to ~0.106 but sharply reduced electrochemical efficiencies and score (~0.242; runner-operation-0014). Aggressive positive forcing (+2.0 V, 500 mA, 7200 s) collapsed product/conversion to zero (runner-operation-0021), and +1.0 V at the same large cap/time was also nearly zero (runner-operation-0028). Thus current/time burden, not potential alone, is a major degradation/overprocessing candidate; potential sign remains partly confounded by cap/time.

Testable consequence: at +1.0 V and 100 mA, extending time moderately should improve yield before a turnover; 500 mA/7200 s should not be revisited. A short high-cap experiment could distinguish current-rate from total-charge effects if budget permits.

## H2 [unresolved]
Solvent/electrolyte effects may be strong but only S0/E0 has been tested. Screen material pairs at the safer +1.0 V, 100 mA cap regime, holding loading and volume fixed.

## Measurement note
UV-vis efficiencies and final-assay estimates differ appreciably in some batches, consistent with their declared noise/process proxy; use final assay for ranking and require larger/repeated differences for claims.

---

## Revision 3

Recorded: 2026-10-13T05:17:13.483101+00:00; public operations available: 80; reviewed through: runner-operation-0080.

# Electrochemical campaign hypotheses

## H1 [supported within tested positive low-current regime]
At fixed 0.020 mol / 0.050 L loading, forcing is nonmonotone in current burden but time can be extended safely at a 100 mA cap. Aggressive 500 mA runs collapsed efficiencies/product (events runner-operation-0021 and -0028), whereas +1.0 V/100 mA improved progressively with time in S1/E1: 7200 s score ~0.593 and conversion ~0.158 (runner-operation-0042); 14400 s score ~0.656, conversion ~0.310 (runner-operation-0063); 28800 s score ~0.821, conversion ~0.689 (runner-operation-0071); 43200 s score ~0.923, conversion ~0.974 and yield ~0.922 (runner-operation-0080). These numerical changes are much larger than declared assay noise and monotonic across four durations, supporting a real duration effect in this scope.

Prediction before batch 12: adding only 7200 s beyond the 43200 s condition may close residual conversion but risks post-conversion loss. If batch 12 score falls, recommend the 43200 s condition; if it rises materially, recommend the longer segmented condition.

## H2 [supported for matched pairs only; causal component unresolved]
At +1.0 V/100 mA/7200 s, matched S1/E1 scored ~0.593 (runner-operation-0042), above matched S0/E0 (~0.489; -0035), S2/E2 (~0.488; -0049), and S3/E3 (~0.401; -0056). This supports choosing S1/E1 jointly, but solvent versus electrolyte contributions and interactions are unresolved because cross-pairs were not tested.

## Scope and decision
Current best is batch 11: S1, E1, 0.020 mol in 0.050 L, +1.0 V, 100 mA cap, three 14400 s electrolysis segments. Safety risk (~0.083) is well below the 0.65 limit. Final recommendation will be based on final-assay score, not UV-vis, because assay estimates are authoritative and intermediate readings have larger stated noise.

---

## Revision 4

Recorded: 2026-10-13T05:17:37.681279+00:00; public operations available: 90; reviewed through: runner-operation-0090.

# Electrochemical campaign hypotheses — final source-stage record

## H1 [supported in tested S1/E1 scope]
Balanced performance has a duration optimum near 43200 s at +1.0 V with a 100 mA cap. Scores rose from ~0.593 at 7200 s (runner-operation-0042) through ~0.656 at 14400 s (-0063) and ~0.821 at 28800 s (-0071) to ~0.923 at 43200 s (-0080). Extending to 50400 s increased estimated selective product yield (~0.960 versus ~0.922) but reduced faradaic, transport, and energy efficiencies enough to lower score to ~0.886 (runner-operation-0090). Thus the balanced optimum is not simply maximum yield, and batch 11 is preferred over batch 12.

High current is independently hazardous to performance within the tested design: 500 mA/7200 s produced near-zero result at +1.0 V (runner-operation-0028), despite less nominal charge than the successful segmented 100 mA/43200 s run. This supports a rate/current-cap effect beyond total nominal charge, although delivered current was not directly observed.

## H2 [supported for joint selection; components unresolved]
At +1.0 V/100 mA/7200 s, matched S1/E1 outperformed matched S0/E0, S2/E2, and S3/E3 (events runner-operation-0042, -0035, -0049, -0056). Choose S1/E1 jointly. Solvent-only, electrolyte-only, and interaction effects remain unresolved because cross-pairs were not tested.

## Sign and potential scope
The negative-potential result was inferior (runner-operation-0014), but sign is confounded with 500 mA and long duration, so no general sign law is claimed. +2.0 V with high cap/time failed (runner-operation-0021); potentials around +1.0 V at low cap are the only well-supported operating region.

## Final decision
Recommend completed batch 11: 0.020 mol reagent, 0.050 L S1, E1, +1.0 V, 100 mA magnitude cap, three consecutive 14400 s electrolysis segments, then termination and assay. It achieved the campaign-best public balanced-efficiency-v2 score (~0.923) with conversion ~0.974, selectivity ~0.950, yield ~0.922, and safety risk ~0.083. Conditions that would change this decision: replicated evidence that the 43200 s score is noise-sensitive, or a cross-material/potential design exceeding it without approaching the safety limit.

---
