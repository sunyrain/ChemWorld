# repeat-02 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:59:26.370499+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] With opaque materials, catalyst/solvent identity and reaction temperature will dominate target formation. Initial screen will use full 0.04 mol reagent, 0.005 mol catalyst, and 0.08 L solvent per batch while varying identities.

H2 [tentative] Slow cooling with a modest seed dose and an isothermal growth hold should reduce fines relative to an unseeded or rapid-cooling trajectory, while deeper cooling should raise seed-excluded recovery. Test consequence: seeded slow-cooled batches should meet fines <=0.50 more often; longer cold holds may raise recovery.

H3 [tentative] Excessive reaction heat/time or severe thermal cycling may increase degradation and lower crystal purity. I will first use a moderate reaction temperature, then adapt from HPLC/final assays.

## Revision 2

Recorded: 2026-10-13T12:02:16.925077+00:00; available public operations: 103; reviewed through: runner-operation-0103.

# Working hypotheses

H1 [supported in screened scope] Full reagent/catalyst charge at 350 K for 1800 s gives near-complete conversion across the paired C0/S0 through C3/S3 screens, but target selectivity varies. C0/S0 is currently strongest (batch 1 final assay, runner-operation-0014), while C2/S2 and C3/S3 are poorer (runner-operation-0090, runner-operation-0103). This comparison is confounded because catalyst and solvent changed together; retain C0/S0 for downstream process work.

H2 [revised; unresolved] Ordinary seeded cooling produced high crystal recovery (~0.38-0.51) and purity above 0.96, but fines stayed near 1.0 in every tested solvent pair (runner-operation-0014, -0077, -0090, -0103). A 1.0 g seed charge and a mild reheat/recool cycle did not materially solve fines (runner-operation-0064 and -0030). Thus seed dose and one shallow cycle are not sufficient in this domain. Next test: greatly extended low-agitation growth holds and deeper final cooling; improvement would be a clear movement of fines toward the <=0.50 constraint.

H3 [supported in tested range] The 350 K/1800 s reaction has high crystal purity and modest degradation for C0/S0; no evidence yet that this thermal exposure is the limiting quality factor. The dominant unmet constraint is particle fines.

## Revision 3

Recorded: 2026-10-13T12:06:44.762667+00:00; available public operations: 235; reviewed through: runner-operation-0235.

# Final source-stage hypotheses

H1 [supported in screened scope] C0/S0 at 350 K for 1800 s is the best tested paired material system for target formation among the four diagonal C/S pairs. Material main effects remain unresolved because the screen changed catalyst and solvent together.

H2 [rejected for feasibility in tested space] Neither ordinary seeding, a 1 g seed charge, extended holds, high agitation, ultra-slow staged cooling, repeated reheat/recool cycles, nor a post-filtration resuspension reduced the number fines fraction near the required <=0.50. Across all completed batches the final fines estimate remained approximately 0.987-1.0. Thus no tested batch meets the full quality constraints; the particle-size mechanism or an untested process dimension dominates.

H3 [supported but confounded] Lower upstream loading in batch 12 increased final selectivity and crystallization-stage recovery to about 0.64 while retaining ~0.996 purity (runner-operation-0235), the highest observed recovery. This single comparison also changed solvent volume and catalyst/reagent ratio, so it supports a useful recipe but not a unique causal attribution. Repeating around this loading and identifying a genuine fines-control lever would be the next priority.

Decision: recommend completed batch 12 because it maximizes observed crystal recovery with high purity, while explicitly flagging that it fails the fines constraint (final estimate 1.0). No completed batch is quality-feasible.
