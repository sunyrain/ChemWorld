# C-24 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Observed material effects
The strongest constrained region used catalyst C0 with solvent S1. In the catalyst screen at otherwise common C2-solvent conditions (S2, 350 K for 3600 s, 0.005 g seed, cooling to 265 K over 14,400 s), C0 gave 0.398 crystal recovery with 0.982 purity and 0.325 fines (batch 2). C3 was nearly tied in recovery at 0.397 (batch 5), whereas C1 and C2 gave 0.362 and 0.342 (batches 3–4). Thus C0 was selected empirically, revising the initial nominal-property preference for C1/C3; the small C0–C3 difference remains uncertain because this screen was unreplicated.

Solvent choice produced a larger and more mechanistically interpretable effect. S0 gave high recovery, 0.483, but excessive fines, 0.810 (batch 6). S3 likewise failed the fines constraint at 0.773 and gave only 0.375 recovery (batch 8). S2 consistently produced relatively low fines—0.325 and 0.322 in batches 2 and 9—but only 0.398–0.423 recovery. S1 provided the best balance: batch 7 reached 0.495 recovery, 0.977 purity, and 0.414 fines. I interpret S0 as promoting excessive nucleation relative to growth, S2 as favoring cleaner/coarser crystallization but retaining more product in solution or otherwise limiting recovery, and S1 as supplying sufficient supersaturation for recovery without uncontrolled secondary nucleation. These are benchmark-world interpretations, not real chemical identities.

### Reaction–crystallization coupling
Reaction conversion was often essentially complete, but upstream selectivity and degradation history still changed downstream recovery and particle quality. At fixed C0/S1 crystallization conditions, batch 21—350 K for only 1800 s—gave selectivity 0.605, degradation warning 0.051, crystal recovery 0.569, purity 0.986, and fines 0.455. Extending the reaction to 7200 s reduced crystal recovery to 0.398 and selectivity to 0.436 while raising degradation warning to 0.220 (batch 22). At 330 K, recovery was 0.456 but fines rose to 0.714 (batch 18); 370 K gave 0.515 recovery with 0.429 fines (batch 19), while 390 K was only marginally feasible at 0.494 fines and 0.494 recovery (batch 20).

A useful qualitative scheme is

R → P,   R or P → I/D,

where P is target product and I/D denotes byproduct or degradation material. Even when conversion X is near one, target formation is governed by selectivity S, approximately Y_P ≈ X·S. Impurities then affect nucleation, growth, occlusion, and effective solubility. Hence reaction severity can alter crystallization recovery and fines even though the reported crystal recovery is normalized to target product present before separation.

For bookkeeping,

crystal recovery = recovered target in crystals / target present before separation.

Because the numerator excludes seed-derived material, adding seed cannot directly inflate this metric. An approximate overall isolated-target measure would instead scale as reaction target yield × crystallization recovery, although that was not the stated optimization objective.

### Crystallization history
Lower final temperature increased recovery in the controlled endpoint screen. With C0/S1 and otherwise common conditions, recovery decreased monotonically from 0.499 at 250 K (batch 14) to 0.458 at 275 K, 0.434 at 285 K, and 0.401 at 300 K (batches 15–17). All four met the quality limits. This is consistent with decreasing equilibrium solubility as temperature falls:

supersaturation σ = (C − C*)/C*,

with lower C*(T) increasing the thermodynamic driving force and recovered fraction. Excessive σ can also increase nucleation and fines, explaining why the lowest-temperature strategy must be combined with controlled cooling and suitable solvent/history rather than interpreted as “colder is always better.”

Seed mass had only a modest resolved effect over 0.001–0.05 g. Batches 10–13 gave recovery 0.474–0.492 and fines 0.421–0.439, comparable with batch 7 at 0.005 g (0.495 recovery, 0.414 fines). The initial batch used 0.05 g seed with a shorter/warmer crystallization history and produced 0.363 recovery and 0.549 fines (batch 1), but that comparison was confounded. The evidence therefore supports 0.005 g as a resource-efficient operating value, not a sharply proven optimum.

Continuing growth for 7200 s after reaching 250 K reduced fines from 0.455 in batch 21 to 0.411 in batch 23 and increased normalized crystal size from 0.057 to 0.096. Recovery was numerically lower, 0.551 versus 0.569. This is consistent with ripening or growth of existing particles at the expense of smaller ones. By contrast, cooling to 270 K, reheating to 300 K, and recooling to 250 K gave 0.539 recovery but 0.597 fines (batch 24), failing the specification. That rejects this particular reheat/recool schedule; slower reheating, a different peak temperature, or a longer post-reheat growth period were not tested.

### Revisions and uncertainty
The initial dossier-driven hypothesis favored C1/C3 with S2. Experimental results revised this twice: the catalyst screen favored C0, and the solvent screen showed that S1 maximized constrained recovery while S2 mainly improved the fines margin. A second revision was that upstream reaction history mattered strongly: the short 1800 s reaction outperformed prolonged reaction despite high conversion, implicating impurity/degradation-mediated crystallization effects.

Final-assay nominal standard uncertainties were about 0.010 for crystal recovery and purity and 0.018 for fines, in addition to uncontrolled batch-to-batch process variation. The 0.018 recovery difference between batches 21 and 23 is therefore modest, while their fines difference of about 0.044 is meaningful but still based on single batches. This leaves an unresolved operating tradeoff: batch 21 provides the highest observed feasible recovery, whereas batch 23 provides a wider fines margin and larger particles with slightly lower observed recovery. The sealed recommendation remains batch 21 because it maximized measured seed-excluded recovery while satisfying purity ≥0.80 and fines ≤0.50.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.29 | 0.18 | 0.43 |
| Q01 | crystal_purity | 0.98 | 0.94 | 1 |
| Q01 | crystal_size | 0.18 | 0.1 | 0.28 |
| Q01 | crystal_yield | 0.43 | 0.33 | 0.53 |
| Q02 | crystal_fines_fraction | 0.57 | 0.43 | 0.7 |
| Q02 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.13 | 0.06 | 0.22 |
| Q02 | crystal_yield | 0.35 | 0.25 | 0.45 |
| Q03 | crystal_fines_fraction | 0.42 | 0.29 | 0.56 |
| Q03 | crystal_purity | 0.98 | 0.93 | 1 |
| Q03 | crystal_size | 0.22 | 0.12 | 0.34 |
| Q03 | crystal_yield | 0.43 | 0.32 | 0.53 |
| Q04 | crystal_fines_fraction | 0.38 | 0.26 | 0.51 |
| Q04 | crystal_purity | 0.98 | 0.94 | 1 |
| Q04 | crystal_size | 0.16 | 0.09 | 0.25 |
| Q04 | crystal_yield | 0.44 | 0.34 | 0.54 |
| Q05 | crystal_fines_fraction | 0.37 | 0.25 | 0.51 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.18 | 0.1 | 0.29 |
| Q05 | crystal_yield | 0.44 | 0.33 | 0.55 |
| Q06 | crystal_fines_fraction | 0.72 | 0.58 | 0.84 |
| Q06 | crystal_purity | 0.97 | 0.91 | 1 |
| Q06 | crystal_size | 0.07 | 0.03 | 0.14 |
| Q06 | crystal_yield | 0.45 | 0.34 | 0.56 |
| Q07 | crystal_fines_fraction | 0.34 | 0.23 | 0.47 |
| Q07 | crystal_purity | 0.98 | 0.94 | 1 |
| Q07 | crystal_size | 0.2 | 0.11 | 0.31 |
| Q07 | crystal_yield | 0.45 | 0.35 | 0.55 |
| Q08 | crystal_fines_fraction | 0.6 | 0.46 | 0.73 |
| Q08 | crystal_purity | 0.98 | 0.92 | 1 |
| Q08 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q08 | crystal_yield | 0.4 | 0.29 | 0.51 |
| Q09 | crystal_fines_fraction | 0.88 | 0.72 | 0.97 |
| Q09 | crystal_purity | 0.94 | 0.75 | 1 |
| Q09 | crystal_size | 0.025 | 0.01 | 0.05 |
| Q09 | crystal_yield | 0.03 | 0 | 0.09 |
| Q10 | crystal_fines_fraction | 0.64 | 0.48 | 0.78 |
| Q10 | crystal_purity | 0.97 | 0.9 | 1 |
| Q10 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q10 | crystal_yield | 0.27 | 0.15 | 0.39 |
| Q11 | crystal_fines_fraction | 0.39 | 0.27 | 0.52 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q11 | crystal_yield | 0.44 | 0.34 | 0.54 |
| Q12 | crystal_fines_fraction | 0.59 | 0.44 | 0.72 |
| Q12 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q12 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q12 | crystal_yield | 0.59 | 0.48 | 0.7 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 applies the observed solvent ranking: S1 should give higher recovery and fewer fines than S3. Q03–Q04 predicts only a modest seed-dose effect; more seed slightly suppresses uncontrolled nucleation but produces a smaller number-weighted size. Q05–Q06 contrasts gradual cooling with an initial temperature crash: endpoint recovery is similar, but the crash should generate substantially more fines. Q07–Q08 reflects the campaign result that continued low-temperature growth improves size/fines, whereas reheating and rapid recooling can redissolve crystals and trigger renewed nucleation. Q09–Q10 predicts little seed-excluded recovery after only 60 seconds, followed by appreciable growth during the 7200-second hold, though the rapid initial quench leaves a fines penalty. Q11–Q12 predicts that doubling reagent concentration increases fractional recovery through greater supersaturation but also increases nucleation and impurity occlusion, making the high-charge case likely fail the fines limit. Intervals are wider than assay noise because these recipes use lower concentration, catalyst C1, very long segmented cooling, and histories not directly tested; feasibility labels use the point estimates.

## K2

1. **Status of the main claims**

- **Supported directly:** Material choice mattered. In the common S2 catalyst screen, C0 gave 0.398 recovery (batch 2), versus 0.362 for C1 and 0.342 for C2 (batches 3–4); C3 was essentially tied at 0.397 (batch 5). Thus C0 was a reasonable provisional choice, but a strict C0-over-C3 ranking remains unresolved.
- **Supported directly:** Solvent strongly affected the recovery–fines balance. S1 gave 0.495 recovery and 0.414 fines (batch 7). S0 gave similar recovery but 0.810 fines (batch 6), S3 gave 0.375 recovery and 0.773 fines (batch 8), and S2 gave lower fines but only 0.398–0.423 recovery (batches 2 and 9). Interpreting these differences as relative nucleation, growth, and solubility effects is plausible but not directly observed mechanistically.
- **Supported directly:** Cooling endpoint affected recovery. At otherwise common conditions, recovery declined from 0.499 at 250 K to 0.458, 0.434, and 0.401 at 275, 285, and 300 K (batches 14–17). The solubility/supersaturation explanation is an interpretation; concentrations and nucleation rates were not measured.
- **Supported directly:** Reaction history coupled to downstream crystallization. A 350 K, 1800 s reaction gave 0.569 recovery with 0.455 fines (batch 21), whereas 7200 s gave 0.398 recovery, lower selectivity, and greater degradation warning (batch 22). This supports a history effect, but attributing it specifically to degradation products altering crystallization remains interpretive because impurity identities were hidden.
- **Supported but not decisive:** An added 7200 s growth hold produced lower fines and larger particles in batch 23 than in batch 21, while recovery fell from 0.569 to 0.551. This is consistent with growth or ripening, but the batches were independent and the recovery difference was modest relative to measurement and process uncertainty.
- **Contradicted:** The initial prior that C1/C3 with S2 would be optimal was contradicted operationally by the C0/S1 results. The prior expectation that more nominally favorable S2 growth properties would maximize constrained recovery was also contradicted: S2 improved fines but lost recovery relative to S1.
- **Still unresolved:** Seed dose had no clear monotonic effect over 0.001–0.05 g in batches 7 and 10–13. Reheating in the particular batch-24 schedule failed the fines criterion, but other reheating temperatures, rates, and growth holds remain untested. Repeatability of batches 21 and 23 is also untested.

2. **One additional experiment**

I would run a randomized, split-batch comparison based on batch 21. After completing the same C0/S1 reaction and controlled cooling to 250 K, I would divide a well-mixed slurry into two equivalent arms. One arm would be filtered immediately; the other would receive the batch-23 hold of 7200 s at 250 K. Both arms would receive particle-size measurements immediately before their respective filtration and separate final assays.

This would distinguish three explanations: (a) genuine ripening/growth during the hold, (b) additional precipitation caused simply by approaching equilibrium, and (c) the observed batch-21/batch-23 difference being ordinary batch variation. Ripening predicts increased size and reduced fines after the hold, with similar or slightly reduced recovery. Continued precipitation predicts increased recovery, potentially accompanied by more fines if secondary nucleation occurs. No material paired-arm difference would indicate that the earlier contrast was dominated by run variation or assay noise. The split design removes upstream reaction and initial-cooling differences as confounders.

3. **Least effectively used evidence and least reliable prediction**

The account used the paired particle-size and final-assay observations from batch 1 least effectively. Before filtration, particle imaging measured size about 0.055 and fines about 0.573; the final assay later gave about 0.069 and 0.549. Their broad agreement could have been used to assess measurement consistency and whether filtration materially changed the representative slurry result. Instead, the account treated batch 1 mainly as a confounded seed/cooling comparison.

Q09 is the least reliable held-out prediction. It stops only 60 seconds after a rapid cool to 292 K, far outside the campaign’s tested crystallization durations. Although seed particles are physically present, seed-excluded target recovery may be near zero, making predicted purity, number-weighted size, and fines highly sensitive to how the benchmark treats seeds and very small amounts of deposited target. There was no close experimental analogue for this transient regime, so the nonlinear onset of nucleation and growth dominates uncertainty. Q10 is also uncertain, but its additional 7200 s hold makes it less extreme.
