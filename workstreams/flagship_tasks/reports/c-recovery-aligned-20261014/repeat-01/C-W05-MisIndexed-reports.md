# C-W05-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign indicates a strongly coupled reaction–crystallization system rather than two independently optimizable stages. Reaction severity and catalyst determine how much target and byproduct enter crystallization; that composition then controls supersaturation, nucleation, growth, impurity rejection, and the recovery–fines tradeoff.

Material effects

All experiments used solvent S2, selected from the nominal dossier for low relative solubility and nucleation, high growth, and low impurity occlusion. The consistently high final crystal purity, 0.981–1.000 across the campaign, is compatible with that prior. However, because no other solvent was tested, a comparative S2 advantage is an interpretation, not an experimentally isolated solvent effect.

The catalyst screen at otherwise similar 330 K/1200 s conditions showed clear reaction differences. Pre-crystallization HPLC gave approximately:
- Batch 2, C1: conversion 0.976, selectivity 0.476, liquid yield 0.443.
- Batch 3, C0: conversion 0.979, selectivity 0.484, liquid yield 0.475.
- Batch 4, C2: conversion 0.980, selectivity 0.387, liquid yield 0.386.
- Batch 5, C3: conversion 0.983, selectivity 0.557, liquid yield 0.540.

Thus C3 was the strongest target-producing catalyst in this tested regime, while C2 was least selective. C3 subsequently enabled high crystal recovery—0.467 in batch 5, 0.469 in batch 6, and the campaign maximum of 0.494 in batch 7—but these batches had excessive fines. C1 generally sacrificed some reaction output but gave the closest approach to the particle specification.

A useful minimal reaction model is competitive target and byproduct formation:

-dR/dt = (kP + kB)aC R,
selectivity ≈ kP/(kP + kB),
reaction yield ≈ conversion × selectivity.

The data suggest that temperature, time, and catalyst alter both total conversion and the kP:kB balance. Conversion was already near unity in most batches, so additional severity mainly increased byproduct or degradation rather than useful conversion. For example, the long 350 K treatment in batch 1 gave final byproduct signal 0.366 and degradation warning 0.161, versus 0.286 and 0.032 in the milder batch 2. Their final liquid yields were nevertheless only about 0.458 and 0.486. This supports avoiding reaction severity beyond that required for near-complete conversion.

Reaction–crystallization coupling

The reported crystal recovery was

Ycrystal = n(target in recovered solid, excluding seed)/n(initial reagent).

It can be viewed approximately as

Ycrystal = Yreaction × fprecipitation × frecovery,

where the last two factors include equilibrium retention in the mother liquor and physical separation. Across the campaign, Ycrystal was roughly 61–88% of the corresponding final liquid-stage yield. The fraction fell when warmer finishing conditions retained more target in solution: about 0.73 in batch 11 and 0.61 in batch 12, compared with approximately 0.84 in batches 1–3. Thus raising the terminal crystallization temperature can reduce recovery without necessarily solving fines.

Crystallization behavior can be organized using supersaturation σ = c/c*(T) − 1, with schematic rates

J ≈ kn σ^m  (new-particle nucleation),
G ≈ kg σ^g  (growth of existing particles).

High target concentration or rapid creation of supersaturation can make J dominate G, producing many particles below 20 µm. C3 increased target formation and therefore likely increased the supersaturation burden. This explains the observed association between its high recovery and poor number-based fines: batches 5 and 6 had recoveries near 0.47 but final fines fractions of 1.00. This explanation is plausible rather than uniquely established because catalyst identity, thermal history, and product loading were not varied orthogonally.

Lowering the reagent concentration improved reaction selectivity but did not remove the particle problem. With C3, reducing the charge from 0.04 mol in 0.06 L to 0.03 mol in 0.08 L raised final reaction yield to 0.631 and crystal recovery to 0.494 in batch 7, while fines improved from 1.00 to 0.777. Further dilution to 0.02 mol in 0.08 L in batch 8 raised reaction yield to 0.698, but crystal recovery fell to 0.457 and fines remained high at 0.816. The non-monotonic result shows that concentration alone is insufficient; the crystallization path and fraction precipitated also matter.

Process-history dependence

The best particle result arose from a specific history, not simply the highest seed charge or warmest endpoint. Batch 1 used C1/S2, 0.04 mol reagent in 0.06 L solvent, 0.005 mol catalyst, a 350 K/3600 s reaction, 0.02 g nominal seed, cooling to 270 K over 7200 s, and then a 3600 s wait during which the slurry warmed toward 295 K. Its final assay was crystal recovery 0.3843, purity 0.9894, and fines 0.5031. The warming period may have partially dissolved the smallest crystals and promoted ripening, but that mechanism was not directly measured.

The original hypothesis that more seed plus slower cooling would monotonically suppress fines was rejected. Batch 3 used only 0.005 g seed and produced fines 0.995, but batch 4 used 0.20 g and still produced fines 0.742. These batches also differed in catalyst, so they do not define a clean seed-dose curve. In several runs seed was added at 329–349 K, where partial or complete dissolution was possible; nominal seed mass was therefore not necessarily the surviving seed population.

Moving seed addition to about 315 K did not rescue C3: batch 6 still had fines 1.00. Deliberate dissolution–recooling cycles also failed to establish a simple improvement. Batch 7 reached fines 0.777; the analogous C1 cycle in batch 9 gave 0.759. Batch 11 cooled deeply, reheated to 310 K, seeded, and recooled to 300 K; recovery fell to 0.334 while fines remained 0.573. Batch 12 used very slow cooling from about 320 to 315 K, but recovery fell to 0.262 and fines were 1.00. These results suggest that merely choosing a warmer endpoint does not guarantee selective removal of fines. The timing of nucleation, survival of seeds, and amount already precipitated before reheating are likely important.

Purity was comparatively insensitive to these histories. Even the highest-recovery batch 7 had purity 0.980, well above the 0.80 requirement. The unresolved optimization is therefore principally recovery versus particle-number distribution, not recovery versus purity.

Revisions and uncertainty

The initial expectations were that C1/S2 would be broadly favorable and that modest seeding plus slow cooling would suppress fines. The experiments revised this view: C3 was better for target formation, S2 was compatible with excellent purity, but seed dose and cooling rate alone did not control fines. The more defensible current hypothesis is that fines depend on the complete supersaturation trajectory, including reaction output, cooling, seed survival, any deep-cooling nucleation burst, and subsequent dissolution or ripening.

Final-assay noise scales were about 0.010 for crystal recovery and purity and 0.018 for fines. Particle-size readings also varied from final assays; for example, batch 1 gave an in-process fines estimate of 0.527 and a final estimate of 0.503. Consequently, batch 1's excess over the 0.50 limit is much smaller than one stated fines-noise scale. It is scientifically ambiguous near the boundary but formally noncompliant on the observed point estimate. No completed batch demonstrated both constraints. Batch 1 remains the sealed recommendation because it combined useful recovery and high purity with the closest observed fines result; it should be treated as a confirmatory and refinement candidate, not as proven compliant.

Untested alternatives include adding seeds only after independently locating the metastable-zone boundary, holding temperature under active control for true ripening rather than allowing passive warming, staged or feedback-controlled antinucleation cooling, controlled slurry dilution after reaction, and solvent comparisons. These could distinguish seed survival, supersaturation, and solvent-specific effects, but the present campaign provides no direct evidence for their outcomes.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.36 | 0.19 | 0.55 |
| Q01 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q01 | crystal_size | 0.16 | 0.08 | 0.26 |
| Q01 | crystal_yield | 0.29 | 0.18 | 0.41 |
| Q02 | crystal_fines_fraction | 0.27 | 0.13 | 0.46 |
| Q02 | crystal_purity | 0.97 | 0.92 | 1 |
| Q02 | crystal_size | 0.2 | 0.11 | 0.31 |
| Q02 | crystal_yield | 0.34 | 0.22 | 0.47 |
| Q03 | crystal_fines_fraction | 0.79 | 0.58 | 0.96 |
| Q03 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q03 | crystal_size | 0.07 | 0.025 | 0.14 |
| Q03 | crystal_yield | 0.2 | 0.1 | 0.32 |
| Q04 | crystal_fines_fraction | 0.39 | 0.21 | 0.59 |
| Q04 | crystal_purity | 0.92 | 0.83 | 0.98 |
| Q04 | crystal_size | 0.15 | 0.075 | 0.25 |
| Q04 | crystal_yield | 0.23 | 0.13 | 0.35 |
| Q05 | crystal_fines_fraction | 0.35 | 0.18 | 0.55 |
| Q05 | crystal_purity | 0.92 | 0.83 | 0.98 |
| Q05 | crystal_size | 0.16 | 0.08 | 0.27 |
| Q05 | crystal_yield | 0.235 | 0.13 | 0.36 |
| Q06 | crystal_fines_fraction | 0.6 | 0.39 | 0.8 |
| Q06 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q06 | crystal_size | 0.1 | 0.045 | 0.19 |
| Q06 | crystal_yield | 0.255 | 0.14 | 0.38 |
| Q07 | crystal_fines_fraction | 0.33 | 0.16 | 0.53 |
| Q07 | crystal_purity | 0.925 | 0.84 | 0.985 |
| Q07 | crystal_size | 0.175 | 0.09 | 0.29 |
| Q07 | crystal_yield | 0.24 | 0.135 | 0.365 |
| Q08 | crystal_fines_fraction | 0.61 | 0.38 | 0.82 |
| Q08 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q08 | crystal_size | 0.105 | 0.04 | 0.21 |
| Q08 | crystal_yield | 0.19 | 0.08 | 0.32 |
| Q09 | crystal_fines_fraction | 0.47 | 0.25 | 0.7 |
| Q09 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q09 | crystal_size | 0.11 | 0.045 | 0.21 |
| Q09 | crystal_yield | 0.055 | 0.01 | 0.14 |
| Q10 | crystal_fines_fraction | 0.38 | 0.19 | 0.6 |
| Q10 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q10 | crystal_size | 0.145 | 0.065 | 0.25 |
| Q10 | crystal_yield | 0.12 | 0.045 | 0.23 |
| Q11 | crystal_fines_fraction | 0.31 | 0.15 | 0.51 |
| Q11 | crystal_purity | 0.925 | 0.84 | 0.985 |
| Q11 | crystal_size | 0.18 | 0.095 | 0.3 |
| Q11 | crystal_yield | 0.245 | 0.14 | 0.37 |
| Q12 | crystal_fines_fraction | 0.58 | 0.36 | 0.79 |
| Q12 | crystal_purity | 0.88 | 0.77 | 0.96 |
| Q12 | crystal_size | 0.115 | 0.05 | 0.22 |
| Q12 | crystal_yield | 0.29 | 0.16 | 0.43 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S3's lower nominal solubility and nucleation tendency, higher growth tendency, and lower impurity occlusion should give Q02 higher recovery, purity, and size with fewer fines than S1, although S1 may support somewhat stronger reaction activity. Q03–Q04: at 300 K, 0.001 g seed may provide too little surviving surface area, so secondary nucleation dominates; 0.045 g should shift material toward seeded growth. Q05–Q06: gradual cooling limits the initial supersaturation excursion, whereas the 120 s crash creates many nuclei; the long hold permits some growth but may not eliminate their number-fraction signature. Q07–Q08: the long monotonic history favors growth and ripening; reheating to 315 K may dissolve product and seeds, and the subsequent one-hour recooling can regenerate fines before full recovery. Q09–Q10: particles should remain because seed was added, but the 60 s treatment alone gives little seed-excluded product; the 7200 s continuation increases deposition, size, and yield while reducing fines. Q11–Q12: doubling reagent loading raises absolute supersaturation and likely recovery, but also increases secondary nucleation and impurity occlusion, worsening fines and purity. Intervals are deliberately broad because the campaign did not directly test S0/S1/S3 or these multi-day histories; several fines estimates straddle 0.50, so quality classifications reflect the central estimates rather than assured compliance.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Purity was not the limiting quality attribute under the tested S2 conditions.** Every completed batch had final crystal purity around 0.981–1.000, comfortably above 0.80. This directly supports the narrower claim that S2 was compatible with strong impurity rejection in the tested campaign. It does **not** establish that S2 is superior to other solvents, because only S2 was used.

- **Catalyst choice affected reaction selectivity and target formation.** Under approximately matched 330 K/1200 s conditions, pre-crystallization HPLC showed C3 performing best in batch 5 (yield 0.540, selectivity 0.557), C2 worst in batch 4 (yield 0.386, selectivity 0.387), with C0 and C1 intermediate in batches 3 and 2. These are direct observations. Interpreting them as intrinsic catalyst effects is reasonable but still conditional on S2 and that reaction regime.

- **Higher reaction output was coupled to a difficult fines problem.** C3 batches 5–8 delivered crystal recoveries of approximately 0.457–0.494, including the campaign maximum in batch 7, but their fines fractions were 0.777–1.000. Conversely, batch 1 had lower recovery, 0.384, but the lowest fines estimate, 0.503. The numerical association is observed; the proposed cause—greater product loading producing a nucleation-dominated supersaturation excursion—is mechanistic interpretation.

- **Neither nominal seed mass nor slow cooling alone guaranteed acceptable fines.** Batch 3 used 0.005 g seed and produced 0.995 fines, while batch 4 used 0.20 g and still produced 0.742. Batches 5 and 6 also reached approximately 1.00 fines despite 0.05 and 0.02 g seed. These observations contradict the original simple monotonic seed-dose hypothesis. They do not define a clean dose-response relationship because catalyst, temperature, and seed-addition history were confounded.

- **Deliberate reheat–recool histories did not reliably solve the tradeoff.** Batch 7 gave recovery 0.494 and fines 0.777; batch 9 gave 0.419 and 0.759; batch 11 reduced recovery to 0.334 while fines remained 0.573. Batch 12 reduced recovery further to 0.262 and had fines 1.00. Thus the tested cycles did not demonstrate compliance.

### Partly supported or contradicted

- **Lower loading might reduce nucleation pressure:** only partly supported. Relative to higher-loading C3 batches, batch 7 improved fines from about 1.00 to 0.777 while raising fractional recovery to 0.494. But further dilution in batch 8 worsened fines to 0.816 and lowered recovery to 0.457. Concentration therefore mattered, but not monotonically or independently of thermal history.

- **Passive warming after deep cooling promoted ripening:** still only an interpretation. Batch 1, which cooled to 270 K and then passively warmed toward 295 K, gave the best fines result. However, batch 10 followed a related history and gave fines 0.735. There was no matched measurement immediately before and after warming, so selective dissolution of fines was not directly demonstrated.

- **Greater reaction severity beyond near-complete conversion was detrimental:** moderately supported. Batch 1’s long 350 K reaction had higher byproduct and degradation signals than milder batch 2 without a corresponding gain in liquid yield. Nonetheless, reaction severity was not independently varied while every downstream condition was held fixed.

### Still untested

- Comparative solvent effects remain untested: S0, S1, and S3 were never run in the campaign. Claims about their solubility, growth, nucleation, or impurity effects rely only on the nominal dossier and may be altered by hidden fixed residuals.
- Effective seed survival was not measured. Seeds added at 315–349 K may have partially or completely dissolved.
- The metastable-zone boundary, supersaturation, dissolved target concentration, and nucleation onset were not observed directly.
- No final assay was replicated, so batch 1’s 0.503 fines result cannot be separated from final-assay noise. Its 0.003 excess over the limit is much smaller than the stated 0.018 fines noise scale, but its point estimate remains formally noncompliant.

## 2. One additional experiment

I would reproduce batch 1’s C1/S2 upstream recipe and thermal history, but add non-destructive particle-size measurements at three defined stages:

1. immediately after cooling to 270 K;
2. after a controlled 270 K hold;
3. after controlled warming to 295 K and holding there for the same duration as batch 1’s passive wait.

I would also take one HPLC measurement immediately after reaction/quench to establish target and byproduct loading, then filter and perform the final assay. Temperature would be actively controlled rather than allowed to drift.

This single time-resolved experiment would distinguish three explanations:

- **Selective dissolution/ripening explanation:** fines should fall and normalized size should rise specifically during the 295 K stage. Final recovery may decrease modestly as small crystals redissolve, while purity should remain stable or improve.
- **Low upstream target-loading explanation:** the particle distribution should already be relatively favorable at 270 K, with little additional improvement on warming. HPLC would show whether batch 1’s reaction produced unusually little crystallizable target.
- **Batch-to-batch or measurement-noise explanation:** successive particle measurements would show no coherent stage-dependent change, and the final fines result could return anywhere around the earlier near-boundary value.

If fines increased during the initial 270 K hold but decreased reproducibly on warming, that would be especially strong evidence for a nucleation-then-ripening mechanism. If warming instead reduced recovery without improving fines, it would disfavor the ripening account and imply that primary nucleation or seed survival must be controlled earlier.

## 3. Underused observation and least reliable held-out prediction

The account used the **intermediate particle-size observations** least effectively. It emphasized final fines but did not fully exploit paired in-process and final readings: batch 1 changed from 0.527 to 0.503 fines, batch 2 from 0.557 to 0.574, batch 6 from 0.980 to 1.000, batch 8 from 0.829 to 0.816, and batch 10 from 0.714 to 0.735. Most differences are comparable to measurement noise, but collectively they show that filtration/final characterization did not cause a uniform directional shift. The accompanying normalized sizes, generally only about 0.03–0.09, also indicate that even apparently improved fines outcomes arose from relatively small particle populations rather than clearly coarse crystals. Using these observations more explicitly would have constrained the ripening narrative.

**Q02 is the least reliable held-out prediction.** It extrapolates to S3 even though the campaign used only S2, and it assumes that S3’s nominal lower solubility, lower nucleation tendency, greater growth tendency, and lower occlusion survive an unknown world-specific residual. S3 also affects both the severe 385 K reaction and the multi-day crystallization, so errors in reaction activity and solid-state behavior compound. The predicted direction relative to Q01 follows the public material prior, but its numerical recovery, purity, size, and fines estimates have no direct campaign anchor. Q08 is also highly uncertain because reheating and rapid recooling were non-monotonic in the campaign, but at least batches 7, 9, and 11 provide qualitative thermal-cycle analogues.
