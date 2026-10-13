# repeat-01 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:34:36.349640+00:00; available public operations: 0; reviewed through: None.

# Prospective hypotheses

H1 [tentative] Reaction performance will depend strongly on anonymous catalyst/solvent choice and thermal residence. Initial screening should compare catalyst–solvent pairs at matched maximum loading (0.04 mol reagent, 0.005 mol catalyst, 0.08 L solvent), while avoiding temperatures near the 0.65 safety ceiling.

H2 [tentative] Seeded, slower cooling followed by a cold hold should reduce the number fraction of fines relative to abrupt unseeded crystallization, but excessive seed mass may itself increase counted fines and is excluded from recovery numerator. First batch prediction: moderate seed (about 0.5 g), controlled cooling, and hold should give measurable recovery with fines below an abrupt-cooling baseline.

Decision rule: use early HPLC/particle-size measurements diagnostically, then spend later batches around the best feasible region (purity >=0.80, fines <=0.50), prioritizing crystal_yield over the native composite score.

## Revision 2

Recorded: 2026-10-13T11:36:50.789810+00:00; available public operations: 96; reviewed through: runner-operation-0096.

# Working hypotheses after batches 1–4

H1 [supported in screened scope] Catalyst/solvent choice affects upstream selectivity and crystal recovery. C0/S0 gave the highest observed reaction selectivity (~0.60) and crystal recovery (~0.46), while the C2/S2 diagonal condition was lower in both (~0.44 selectivity, ~0.35 recovery); these are confounded pair changes and not isolated catalyst or solvent effects (final assays at events runner-operation-0019, -0040, -0072, -0096).

H2 [not supported for low seed dose] A single 0.05 g seed addition plus slow cooling did not meet the fines constraint. Direct cooling, extended cold holds, one reheat/recool, and staged cooling all produced fines estimates near 0.98–1.00 (particle/final results at runner-operation-0011, -0013, -0069, -0072, -0093, -0096). Longer isothermal holding alone did not show a practically meaningful reduction in fines; batch-to-batch differences are also confounded.

H3 [tentative, prospective] Seed dose may be the missing control variable: the available 12 g stock is far above the 0.05 g per-operation cap. Test approximately 1 g total seed under the best upstream C0/S0 condition. If fines remain near 1, suspend the simple 'more seed solves fines' claim and test high-temperature ripening/partial redissolution and solvent identity instead.

Decision: prioritize feasibility of fines <=0.50. Once feasible, optimize recovery using C0/S0 and thermal endpoint.

## Revision 3

Recorded: 2026-10-13T11:40:28.092140+00:00; available public operations: 260; reviewed through: runner-operation-0260.

# Working hypotheses after batches 1–9

H1 [supported in screened scope] C0/S0 has repeatedly produced upstream selectivity near 0.56–0.62 and the campaign's highest recoveries (~0.51–0.52 in batches 7–8; final events runner-operation-0189 and -0228). Other tested diagonal or S3 conditions were lower, though catalyst and solvent effects remain partly confounded.

H2 [rejected as a simple claim] Neither prolonged holding, staged cooling, 1 g total seed, nor unseeded cooling reliably lowered fines: final fines remained about 0.98–1.00 (events runner-operation-0134, -0189). Seed dose increase from 0.05 to 1 g did not show a fines benefit and cannot be treated as the missing control.

H3 [not supported in tested range] Post-growth heating to 290–310 K did not selectively eliminate enough fines; particle measurements remained about 0.97–1.00 fines (runner-operation-0242, -0244, -0246). A resuspension/recrystallization sequence reduced recovery to ~0.30 without improving final fines (runner-operation-0260).

H4 [tentative, prospective] The wide gap between the failed 1 microgram seed attempt (no solids at 295 K) and prior 0.05 g dosing leaves an intermediate low-seed regime unresolved. Test ~0.005 g seed with slow staged cooling; if fines remain far above 0.50, conclude feasibility was not found rather than overstate a process effect.

Decision: use remaining batches to test intermediate seed dose and the unscreened C3 catalyst, while retaining C0/S0 as the recovery benchmark.

## Revision 4

Recorded: 2026-10-13T11:42:37.397099+00:00; available public operations: 343; reviewed through: runner-operation-0343.

# Final source-stage interpretation

H1 [supported only as an empirical benchmark] Across this campaign, C0/S0 repeatedly gave relatively strong upstream performance and recovery, but catalyst and solvent effects were not isolated in a fully crossed design. Batch 12, using C0/S0 at higher concentration (0.04 mol reagent in 0.02 L), had the highest observed crystal recovery, 0.541, and purity 1.000 (runner-operation-0343). The numerical increase over prior best recoveries (~0.51–0.52 at runner-operation-0189 and -0228) is confounded by solvent loading and thermal history; with single final assays and stated instrument noise, it should not be claimed as a precisely estimated causal effect.

H2 [rejected in tested scope] Low-to-high seed-dose changes, staged versus direct cooling, prolonged low-temperature holding, and unseeded operation did not achieve the fines requirement. Intermediate seed doses (0.005 g and 0.0001 g) also ended near 0.99–1.00 fines (runner-operation-0284, -0314). Post-growth 290–310 K ripening and one resuspension did not solve the problem (runner-operation-0242, -0244, -0246, -0260).

H3 [unresolved mechanism] Persistent fines may reflect an intrinsic nucleation/growth balance or benchmark seed/particle model not controlled by the tested histories. No unsupported mechanistic distinction is made among secondary nucleation, attrition, and limited growth. A future test should vary concentration independently with several replicates and examine size over time, or add an explicit size-classification operation if available.

Final decision: no completed batch met both quality constraints because all final fines estimates were far above 0.50, although purity was consistently above 0.80. Select batch 12 as the best recovery benchmark (0.541) with purity 1.000, explicitly noting its fines failure (1.000).
