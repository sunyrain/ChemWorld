# repeat-01 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:10:28.222820+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

**H1 [tentative]** Solvent S2 should favor high crystal recovery and acceptable purity/fines because its nominal solubility and impurity occlusion are low and growth is high; S3 is the conservative alternative. A slow cooled, seeded growth/hold after a productive reaction should outperform rapid unseeded cooling in size and fines. This expectation will be tested against final assays; catalyst identity and reaction temperature remain uncertain.

**Plan** First screen a high-activity catalyst/solvent combination with moderate thermal exposure, then vary catalyst, solvent, seed dose, cooling rate, hold, and loading. I will prioritize feasible purity and fines before maximizing recovery.

## Revision 2

Recorded: 2026-10-13T17:11:53.494740+00:00; available public operations: 41; reviewed through: runner-operation-0041.

# Working hypotheses after batches 1–3

**H1 [supported in limited scope]** S2 can deliver highly pure crystals (>0.98 observed) with acceptable fines under a seeded staged/moderate cool. Batch 1 (final event runner-operation-0013) gave crystal yield 0.392 and fines 0.434; batch 3 (runner-operation-0041) gave yield 0.374 and fines 0.305. The purity condition appears robust so far.

**H2 [unresolved]** Deeper cooling and greater seed dose may raise recovery, but batch 2 (runner-operation-0028) had higher recovery 0.472 while fines 0.566 failed the constraint. Temperature, seed dose, catalyst, reaction duration, and cooling history are confounded, so the numerical difference is not yet attributable.

**H3 [tentative]** Staged cooling/low agitation may suppress fines relative to a single deep cool. Test across solvents and thermal histories. I will keep seed near 0.05 g where possible and explore solvent effects, then refine the best feasible recovery.

## Revision 3

Recorded: 2026-10-13T17:13:37.220800+00:00; available public operations: 148; reviewed through: runner-operation-0148.

# Working hypotheses after batches 1–11

**H1 [revised; supported in tested scope]** S1, not the nominally favored S2, gives the best feasible recovery under staged cooling. Batches 6 and 8 (runner-operation-0080, runner-operation-0106) both met purity/fines constraints with crystal yields 0.534 and 0.537. S2 also meets quality but its best tested feasible yield was 0.444 (batch 4, runner-operation-0054). This is evidence that world-specific behavior overrides the nominal solvent prior.

**H2 [supported qualitatively]** Solvent strongly affects the recovery–fines tradeoff. S0 had yield 0.560 but fines 0.645 (runner-operation-0093); S3 had fines 0.662 (runner-operation-0067). S1 staged recipes were feasible. A concentrated S1 charge numerically moved fines to 0.505 (runner-operation-0119), just beyond the limit, without improving recovery; avoid 0.04 L solvent loading.

**H3 [narrowed]** A staged cool to 310 K then 250 K with a finite hold and low agitation is preferred. Extending the 250 K hold to three 4 h periods did not continue beneficial growth: batch 11 had fines 0.660 and lower yield 0.478 (runner-operation-0148). This may reflect secondary nucleation/attrition rather than simple growth. Single-batch differences and final-assay noise remain limitations.

**H4 [unresolved]** Seed mass from 0.05 to 0.10 g had little clear effect within S1 staged runs (runner-operation-0106 vs runner-operation-0133); catalyst C1 versus C3 likewise did not materially separate recovery in batches 6 and 8. Final batch will test a modestly shorter post-cool hold to avoid the adverse long-hold regime while retaining staged cooling.

## Revision 4

Recorded: 2026-10-13T17:14:05.242226+00:00; available public operations: 160; reviewed through: runner-operation-0160.

# Final source-stage interpretation

**H1 [supported in tested scope]** S1 with 0.04 mol reagent in 0.06 L solvent, 0.005 mol catalyst, seeded staged cooling (310 K then 250 K), and a moderate low-agitation hold repeatedly satisfied purity and fines limits. Batches 6, 8, 10, and 12 all did so (final events runner-operation-0080, -0106, -0133, -0160).

**H2 [supported qualitatively]** The main observed tradeoff was solvent/loading/thermal-history dependent. S0 achieved the largest numerical recovery overall but failed fines badly; concentrated S1 was borderline failing; very long cold holding also failed fines. Thus continuing growth indefinitely is not supported.

**Decision** Recommend batch 8: it has the highest measured crystal yield among constraint-satisfying completed batches (0.537), with purity 0.985 and fines 0.403. Batch 6 is a near replicate (yield 0.534, purity 1.000, fines 0.409), supporting the operating region, though the small yield difference is not evidence that C1 is intrinsically superior to C3. Batch 12 confirms a shorter hold remains feasible but did not exceed recovery. I would change the recommendation only if repeat measurements showed batch 8's yield advantage was noise or fines crossed 0.50.
