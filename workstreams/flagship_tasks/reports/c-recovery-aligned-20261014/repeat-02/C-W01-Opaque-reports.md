# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Observed material effects
All material identities were anonymous benchmark labels, so the data support functional rather than molecular assignments.

With the reaction history and crystallization protocol held approximately constant, solvent identity had the clearest effect. Using C0 at 370 K for 3600 s, batches 6–8 gave:

- S1, batch 6: crystal yield 0.469, purity 0.997, fines 0.348.
- S2, batch 7: crystal yield 0.537, purity 0.981, fines 0.131.
- S3, batch 8: crystal yield 0.441, purity 0.972, fines 0.412.

The corresponding S0 batch 2 gave yield 0.529, purity 0.977 and fines 0.491. Thus S2 preserved good recovery while producing a much smaller fine-particle fraction. A plausible interpretation is that S2 provides a more favorable solubility or interfacial-kinetic window: supersaturation is relieved predominantly by growth on existing crystals rather than by secondary nucleation. This property was not directly measured, so alternatives such as solvent-dependent agglomeration, polymorph selection or impurity adsorption remain open.

The catalyst screen was less decisive. Under S0 and the common crystallization protocol, C0, C1, C2 and C3 in batches 2–5 gave crystal yields of 0.529, 0.524, 0.458 and 0.525, respectively. C2 was clearly unfavorable in that screen, while C0, C1 and C3 were not cleanly separated by single-batch evidence. Catalyst–solvent interactions were not comprehensively tested; consequently, C0 is the best demonstrated catalyst for S2, not necessarily the globally optimal one.

### Reaction mechanism and history dependence
A useful qualitative network is

reactant → target product,
reactant → primary byproducts,
target product → degradation products.

For parallel or sequential steps, each rate constant may be represented as k_i = A_i exp(−E_i/RT). The results suggest that the desired transformation benefits more from high temperature than the competing pathways over the tested short residence times, while extended exposure permits secondary byproduct formation or degradation.

This interpretation arose from batches 7 and 9–12, which all used C0/S2 with the same reagent, catalyst, solvent, seed and staged-cooling quantities but different reaction histories:

- Batch 9, 350 K/7200 s: conversion 1.000, selectivity 0.475, byproduct signal 0.387, degradation warning 0.205 and crystal yield 0.407.
- Batch 7, 370 K/3600 s: conversion 1.000, selectivity 0.598, byproduct 0.284, degradation 0.146 and crystal yield 0.537.
- Batch 10, 390 K/1800 s: conversion 0.986, selectivity 0.721, byproduct 0.199, degradation 0.103 and crystal yield 0.633.
- Batch 11, 410 K/1200 s: conversion 0.999, selectivity 0.789, byproduct 0.172, degradation 0.061 and crystal yield 0.673.
- Batch 12, 430 K/900 s: conversion 1.000, selectivity 0.798, byproduct 0.135, degradation 0.071 and crystal yield 0.704.

The monotonic recovery improvement is therefore associated with a hotter, shorter history and reduced byproduct formation. Temperature and time were changed together, however, so their separate causal effects and kinetic parameters cannot be identified. The optimum may lie beyond the tested boundary, or excessive temperature may eventually reverse the trend through decomposition or safety limitations.

### Reaction–crystallization coupling
The reported crystal yield is the seed-excluded moles of solid target divided by the initial reagent charge:

Y_crystal = n(target in recovered crystals, excluding seed) / n(initial reagent).

It can be viewed approximately as

Y_crystal ≈ Y_reaction × f_crystallized × f_recovered,

although independently noisy assay channels prevent treating this as an exact measured identity. For example, batch 12 had reaction yield 0.803 and crystal yield 0.704, implying that most—but not all—formed target was recovered as seed-excluded solid. Improving reaction selectivity therefore raised the available product inventory, while the S2 crystallization history converted a consistently large fraction of that inventory into acceptable crystals.

A classical qualitative crystallization description is useful. With supersaturation S = C/C*, nucleation may scale approximately as

J ∝ exp[−B/(ln S)^2],

whereas growth can be represented as G = k_g(S−1)^g. Dilution, additional seed surface and gradual cooling limit peaks in S, suppressing J relative to G. Batch 1 used only 0.06 L S0, 0.02 g seed and a less controlled cooling/hold history; it produced yield 0.524 and purity 0.985 but fines 0.745. Its post-cooling wait also warmed the slurry from 280 K to about 291 K, so it was not a clean low-temperature hold. Batch 2 combined 0.08 L solvent, 0.05 g seed and two 14400 s cooling stages, first to 320 K and then to 270 K. Yield remained 0.529 while fines fell to 0.491. This supports supersaturation management, but dilution, seed loading and cooling profile were changed simultaneously and cannot be assigned individual effects.

Solvent S2 then provided a substantially wider particle-quality margin: batches 7 and 9–12 had final fines fractions of approximately 0.13–0.20. In batch 12, the pre-filtration particle measurement gave fines 0.197 and the final assay gave 0.195, supporting the conclusion with two measurements at different workflow stages. Final purity was 0.996, indicating effective impurity rejection despite high overall recovery.

### Revisions during the study
The initial expectation was that moderate seeding and slow cooling alone would control fines. Batch 1 contradicted that expectation. The next interpretation emphasized dilution, maximal seeding and staged cooling; batch 2 supported their combined benefit but only narrowly met the fines limit. The solvent screen then shifted the main explanation toward a strong solvent-dependent nucleation/growth effect, especially for S2.

A subsequent hypothesis predicted that lower reaction temperature with a longer hold would reduce degradation. Batch 9 contradicted it: despite complete conversion, selectivity and crystal recovery declined and both byproduct and degradation signals rose. The working mechanism was therefore revised to favor rapid high-temperature conversion followed immediately by controlled crystallization.

### Uncertainty and unresolved tradeoffs
Every recipe was run once, and several comparisons changed multiple factors together. Instrument noise was declared, but batch-to-batch process variability was not independently estimated. The 0.031 crystal-yield advantage of batch 12 over batch 11 exceeds the final-assay crystal-yield noise scale of about 0.01, but replication would still be needed to establish reproducibility.

No serious purity–recovery conflict appeared: purity remained well above 0.80 in all leading S2 batches. A weaker recovery–particle-quality tension may exist. As reaction recovery increased from batch 7 to batches 10–12, fines rose from about 0.13 to roughly 0.18–0.20, consistent with a larger product inventory generating higher supersaturation. This trend is small, non-monotonic across all readings and confounded with reaction history, so it is unresolved. Importantly, batch 12 retained a wide margin below the 0.50 fines limit.

The recommended batch 12 is therefore the strongest demonstrated coupled process: C0/S2, 430 K for 900 s, followed by 0.05 g seeding and staged 320 K then 270 K cooling. It achieved the highest observed qualifying seed-excluded crystal yield, 0.704, with purity 0.996 and fines 0.195. This is an empirical optimum at the explored boundary, not proof of a global mechanistic optimum.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.28 | 0.15 | 0.43 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.13 | 0.08 | 0.2 |
| Q01 | crystal_yield | 0.34 | 0.22 | 0.46 |
| Q02 | crystal_fines_fraction | 0.38 | 0.23 | 0.55 |
| Q02 | crystal_purity | 0.98 | 0.94 | 1 |
| Q02 | crystal_size | 0.105 | 0.065 | 0.17 |
| Q02 | crystal_yield | 0.31 | 0.19 | 0.43 |
| Q03 | crystal_fines_fraction | 0.54 | 0.36 | 0.71 |
| Q03 | crystal_purity | 0.985 | 0.94 | 1 |
| Q03 | crystal_size | 0.07 | 0.035 | 0.12 |
| Q03 | crystal_yield | 0.26 | 0.15 | 0.37 |
| Q04 | crystal_fines_fraction | 0.38 | 0.22 | 0.55 |
| Q04 | crystal_purity | 0.988 | 0.95 | 1 |
| Q04 | crystal_size | 0.105 | 0.065 | 0.16 |
| Q04 | crystal_yield | 0.28 | 0.17 | 0.39 |
| Q05 | crystal_fines_fraction | 0.34 | 0.19 | 0.5 |
| Q05 | crystal_purity | 0.989 | 0.95 | 1 |
| Q05 | crystal_size | 0.12 | 0.075 | 0.18 |
| Q05 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q06 | crystal_fines_fraction | 0.57 | 0.4 | 0.74 |
| Q06 | crystal_purity | 0.985 | 0.94 | 1 |
| Q06 | crystal_size | 0.065 | 0.03 | 0.105 |
| Q06 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q07 | crystal_fines_fraction | 0.35 | 0.2 | 0.51 |
| Q07 | crystal_purity | 0.988 | 0.95 | 1 |
| Q07 | crystal_size | 0.115 | 0.07 | 0.17 |
| Q07 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q08 | crystal_fines_fraction | 0.25 | 0.12 | 0.42 |
| Q08 | crystal_purity | 0.993 | 0.96 | 1 |
| Q08 | crystal_size | 0.145 | 0.085 | 0.22 |
| Q08 | crystal_yield | 0.25 | 0.14 | 0.37 |
| Q09 | crystal_fines_fraction | 0.48 | 0.29 | 0.67 |
| Q09 | crystal_purity | 0.98 | 0.92 | 1 |
| Q09 | crystal_size | 0.082 | 0.045 | 0.13 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.13 |
| Q10 | crystal_fines_fraction | 0.4 | 0.23 | 0.58 |
| Q10 | crystal_purity | 0.985 | 0.94 | 1 |
| Q10 | crystal_size | 0.1 | 0.06 | 0.155 |
| Q10 | crystal_yield | 0.16 | 0.07 | 0.26 |
| Q11 | crystal_fines_fraction | 0.33 | 0.18 | 0.5 |
| Q11 | crystal_purity | 0.988 | 0.95 | 1 |
| Q11 | crystal_size | 0.12 | 0.075 | 0.18 |
| Q11 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q12 | crystal_fines_fraction | 0.55 | 0.36 | 0.72 |
| Q12 | crystal_purity | 0.98 | 0.93 | 1 |
| Q12 | crystal_size | 0.07 | 0.035 | 0.115 |
| Q12 | crystal_yield | 0.36 | 0.23 | 0.49 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and cooling, so particles are expected. Q01–Q02: prior material trends favor S1 over S3 for lower fines and slightly better recovery. Q03–Q04: high seed loading should provide more growth surface and suppress secondary nucleation; the very low-seed case is predicted to cross the fines limit. Q05–Q06: gradual cooling should limit peak supersaturation, whereas the crash cool should produce more fines; their final equilibrium recovery should be similar. Q07–Q08: the 315 K thermal cycle is expected to dissolve fines preferentially and promote regrowth on recooling, improving size and fines at a modest recovery cost. Q09–Q10: two additional hours at 292 K should substantially increase seed-excluded deposition and growth relative to immediate filtration. Q11–Q12: doubling reagent loading should raise supersaturation and recovery but also secondary nucleation, creating a recovery–quality tradeoff. Intervals are deliberately broad because the requested catalyst loading, concentration, multi-day cooling histories and thermal cycle extend beyond the directly studied recipes; several fines intervals cross the 0.50 feasibility boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S2 was the best demonstrated solvent for combined recovery and particle quality.** With C0 and the common 370 K/3600 s reaction and staged crystallization, batch 7 gave crystal yield 0.537 and fines 0.131, versus batch 6/S1 at 0.469 and 0.348, batch 8/S3 at 0.441 and 0.412, and batch 2/S0 at 0.529 and 0.491. The numerical ranking is observed; attributing it specifically to solubility or interfacial kinetics is interpretation.
- **Hotter, shorter reaction histories were associated with better reaction selectivity and crystal recovery for C0/S2.** Crystal yield increased from 0.407 in batch 9 (350 K/7200 s) to 0.633, 0.673 and 0.704 in batches 10–12 (390 K/1800 s, 410 K/1200 s and 430 K/900 s). Byproduct signals generally fell and selectivity rose. This association is direct, but temperature and time were confounded.
- **The recommended batch met both quality constraints with substantial margin.** Batch 12 directly measured purity 0.996 and final fines 0.195; its pre-filtration particle measurement gave fines 0.197. Its seed-excluded crystal yield was 0.704.
- **The leading processes showed no observed purity–recovery conflict.** Purities remained approximately 0.97–1.00 across the successful batches.

### Contradicted or revised claims
- **Moderate seeding and nominally slow cooling were not sufficient by themselves to control fines.** Batch 1 used 0.02 g seed but produced fines 0.745. Its later warming to about 291 K also made it an imperfect test of a low-temperature hold.
- **Lower temperature with longer residence did not preserve selectivity in the tested S2 process.** Batch 9 instead showed selectivity 0.475, byproduct signal 0.387 and crystal yield 0.407, all worse than the hotter, shorter batches. This contradicted the prospective lower-temperature hypothesis.

### Still untested or only weakly supported
- The proposed solvent mechanism—lower effective supersaturation, suppressed nucleation or altered interfacial growth—was not measured directly. Polymorph selection, agglomeration and impurity adsorption remain alternatives.
- Batch 1 versus batch 2 supports the combined benefit of dilution, higher seed loading and staged cooling, but does not identify which change caused the fines reduction from 0.745 to 0.491.
- C2 was unfavorable in the S0 catalyst screen, but C0, C1 and C3 were not convincingly separated. Catalyst–solvent interactions, especially with S2, remain untested.
- The apparent recovery–fines tradeoff is unresolved. Fines increased from about 0.13 in batch 7 to 0.18–0.20 in batches 10–12 as recovery rose, but reaction history also changed and there were no replicates.
- The optimum lies at the explored 430 K/900 s boundary; behavior beyond that boundary and process reproducibility remain unknown.

## 2. Most informative additional experiment

I would repeat the complete C0/S2 batch-12 recipe and crystallization protocol, but change only the reaction residence from **430 K/900 s to 430 K/3600 s**.

This supplies a missing crossed condition. Comparison with batch 12 isolates residence time at 430 K, while comparison with batch 7 (370 K/3600 s) approximately isolates temperature at the longer residence.

It would distinguish:
- **Temperature-controlled selectivity:** if high temperature intrinsically favors the desired pathway, the 430 K/3600 s experiment should retain high selectivity and recovery near batch 12, with relatively low byproduct signal.
- **Residence-time-controlled degradation:** if short exposure is the main advantage, extending the 430 K hold should increase degradation/byproduct signals and lower selectivity and crystal yield toward batch 7 or below it.
- **Sequential target degradation:** complete conversion accompanied by falling target yield and rising degradation would indicate that target forms rapidly and is then consumed during the extra hold.

The S2 crystallization protocol should still tend to satisfy purity and fines constraints, although a larger impurity inventory could alter nucleation or occlusion. A replicate of batch 12 would be preferable for estimating reproducibility, but the crossed 430 K/3600 s condition provides greater mechanistic discrimination with only one experiment.

## 3. Least-used observation and least-reliable prediction

The account used **crystal_size** least effectively. It emphasized fines because fines were the explicit constraint, but did not develop the non-monotonic size observations or reconcile instrument-stage differences. For example, batch 12 had normalized size 0.075 before filtration and 0.116 in the final assay, despite nearly identical fines readings. That discrepancy could reflect measurement noise, sampling representation or changes associated with filtration, and it limits any strong size-growth interpretation.

The least reliable held-out prediction is **Q08**, the reheating/recooling thermal-cycle case. The predicted increase in size and reduction in fines assumed preferential dissolution of fines followed by regrowth, but no campaign batch applied a post-crystallization heat cycle. Heating to 315 K could instead dissolve substantial product or seeds, induce fresh nucleation during the rapid recool, or change recovery without improving the number distribution. Thus both the direction and magnitude of the Q08 size, fines and yield changes are more speculative than predictions interpolating among tested solvents or cooling histories.
