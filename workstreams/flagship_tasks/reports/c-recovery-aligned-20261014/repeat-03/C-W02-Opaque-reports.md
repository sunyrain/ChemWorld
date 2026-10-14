# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The benchmark materials are anonymous, so the discussion below concerns observed functional roles rather than real chemical identities.

### 1. Reaction-stage material effects

**Observation.** At 0.04 mol reagent, 0.08 L S0, 0.005 mol catalyst, 360 K and 1800 s, conversion was nearly complete across catalysts, but selectivity and target yield varied. C0 gave selectivity 0.740, reaction yield 0.737 and final crystal yield 0.569 (batch 1). C1 was slightly poorer (0.728, 0.715 and 0.544; batch 2), C3 poorer again (0.691, 0.675 and 0.525; batch 4), and C2 was clearly weakest (0.556, 0.550 and 0.380; batch 3).

**Interpretation.** Catalyst identity primarily changed branching between target and byproduct rather than reagent disappearance. High conversion alone was therefore not a useful optimization criterion. C0 was retained because it gave the best observed target-forming selectivity in this screen.

**Uncertainty and alternatives.** Each catalyst was tested once, and batch 1 had a different post-cooling history, so small C0–C1 differences are provisional. Catalyst rankings could change with temperature, solvent or loading; catalyst–solvent interactions were not factorially mapped.

Solvent identity affected both reaction and particle formation. With C0 and the initial 0.05 g seed/278 K cooling schedule, S1 produced the highest reaction yield and crystal yield (0.759 and 0.623) but failed the fines requirement at 0.583 (batch 5). S2 gave somewhat lower reaction yield and crystal yield (0.703 and 0.609) but passed with fines 0.456 and purity 1.000 (batch 6). S0 generated very high fines (0.874 in batch 1), while S3 was inferior in both recovery and fines (crystal yield 0.498, fines 0.751; batch 7).

This indicates that solvent choice changes more than solubility: it likely modifies reaction selectivity, supersaturation development, primary or secondary nucleation, and growth kinetics. S1 favored target formation but not an acceptable number distribution; S2 provided the best compromise.

### 2. Reaction–crystallization coupling

The reported overall recovery is

`Y_crystal = n(target in isolated solid, excluding seed) / n(reagent initially charged)`.

A useful approximate decomposition is

`Y_crystal ≈ Y_reaction,target × f_capture`,

where `f_capture` is the fraction of formed target ultimately recovered as seed-excluded solid. Using the assay reaction-yield channel as a proxy, inferred capture ratios increased from about 0.867 in batch 6 to 0.903, 0.912 and 0.933 in batches 8, 9 and 10. Thus the improvement from batch 6 to batch 10 was mainly downstream capture and particle-history control, not improved reaction yield.

Reaction selectivity and crystal purity were also distinct. For example, batch 10 had reaction selectivity 0.684 but crystal purity 0.979. Across the campaign, crystals generally remained highly pure even when substantial byproduct was formed. The solid phase therefore acted as a selective separation, but it could not recover target that had never formed.

### 3. Supersaturation and process-history dependence

A qualitative crystallization model is

`S(t) = C(t)/C*(T(t), solvent)`,  `Δμ = RT ln S`,

with nucleation and growth represented schematically by

`J ∝ exp[-B/(ln S)^2]`,  `G = k_g(S−1)^g`.

Solvent changes the solubility curve `C*` and kinetic coefficients. Cooling rate controls how quickly supersaturation accumulates, while seed mass controls available growth surface and can also influence secondary nucleation. These relations explain why the same upstream reaction can give very different particle populations.

The initial hypothesis that 0.05 g seeding followed by cooling to 278 K would adequately suppress fines was rejected. Batches 1–4 all produced final fines of approximately 0.87–0.98. Batch 1 additionally included a 3600 s stirred hold during which the material warmed from 278 K to about 288 K under the still-active control history, so it is not a clean replicate of batches 2–4.

A tenfold seed reduction to 0.005 g combined with a 14400 s cooling trajectory was decisive in S2. Cooling from about 360 K to 278 K, 268 K and 250 K in batches 8–10 gave:

- Batch 8: crystal yield 0.620, purity 0.981, fines 0.306.
- Batch 9: crystal yield 0.626, purity 0.983, fines 0.324.
- Batch 10: crystal yield 0.647, purity 0.979, fines 0.342.

The batch-10 nominal cooling rate was about 0.00764 K/s, versus about 0.01139 K/s for the earlier 7200 s trajectory to 278 K. The large fines reduction cannot be assigned uniquely to cooling rate because seed mass was changed simultaneously. My interpretation is that the smaller seed charge reduced seed-derived counts and/or secondary nucleation, while the slower trajectory allowed existing particles to consume supersaturation by growth before extensive new nucleation occurred.

Within batches 8–10, deeper terminal cooling increased recovery but modestly increased fines and reduced the CSD-quality metric: CSD quality declined from 0.789 in batch 8 to 0.714 in batch 10. This is consistent with stronger late-stage supersaturation improving thermodynamic capture while generating some additional small particles. It defines the unresolved quality/recovery tradeoff: 250 K maximized observed feasible recovery, whereas 278 K gave the best particle distribution.

### 4. Concentration and thermal-history tests

The standard charge corresponded to 0.50 mol/L reagent and a catalyst/reagent ratio of 0.125. Batch 12 reduced S2 from 0.08 to 0.06 L, raising nominal concentration to 0.667 mol/L. Its crystal yield was 0.645—essentially unchanged from batch 10—but fines rose to 0.510, just beyond specification. This is consistent with higher concentration driving a faster supersaturation excursion and more nucleation. Because the yield difference from batch 10 was only 0.0018, far below the final-assay crystal-yield noise scale of 0.01, there is no evidence of a real recovery advantage from concentrating the batch.

Batch 11 tested a milder but longer reaction, 340 K for 3600 s, before the optimized crystallization schedule. It produced lower selectivity (0.590), reaction yield (0.570) and crystal yield (0.531), while degradation warning increased to 0.093. This contradicted the initial idea that milder heating would suppress side reaction. Possible alternatives are unfavorable time-dependent branching, a temperature-dependent catalyst state, or simply operation away from a kinetic selectivity optimum. A broader temperature–time design would be needed to distinguish them.

### 5. Recommended process and uncertainty

The sealed recommendation remains batch 10: charge 0.04 mol reagent, 0.08 L S2 and 0.005 mol C0; heat at 360 K for 1800 s with 500 rpm stirring; add 0.005 g seed; cool to 250 K over 14400 s; then filter. Its observed crystal yield was 0.6465, purity 0.9795 and number fraction below 20 µm 0.3419, making it the highest-recovery batch that clearly met both constraints.

Instrument standard deviations were approximately 0.01 for crystal yield and purity and 0.018 for fines, but these do not include batch-to-batch process variability. Differences between batches 8 and 9 are smaller than, or comparable to, assay noise. Batch 10 exceeded batch 9 by about 0.020 in recovery, suggestive but not confirmed without replication. Batch 12's fines result of 0.510 is close enough to the limit to be analytically marginal, but it was conservatively treated as a failure and offers no demonstrated recovery benefit. Batch 10 has a much larger fines margin and is therefore the more defensible operating point. The most valuable unresolved experiment would be a replicate of batch 10, followed by separate seed-mass and cooling-rate perturbations to disentangle their contributions.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.2 | 0.51 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.26 | 0.13 | 0.42 |
| Q01 | crystal_yield | 0.58 | 0.46 | 0.68 |
| Q02 | crystal_fines_fraction | 0.53 | 0.36 | 0.72 |
| Q02 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.2 | 0.08 | 0.35 |
| Q02 | crystal_yield | 0.43 | 0.31 | 0.56 |
| Q03 | crystal_fines_fraction | 0.18 | 0.07 | 0.34 |
| Q03 | crystal_purity | 0.98 | 0.93 | 1 |
| Q03 | crystal_size | 0.38 | 0.2 | 0.58 |
| Q03 | crystal_yield | 0.55 | 0.43 | 0.66 |
| Q04 | crystal_fines_fraction | 0.44 | 0.27 | 0.62 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.23 | 0.1 | 0.39 |
| Q04 | crystal_yield | 0.57 | 0.45 | 0.67 |
| Q05 | crystal_fines_fraction | 0.36 | 0.21 | 0.53 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.3 | 0.16 | 0.47 |
| Q05 | crystal_yield | 0.56 | 0.44 | 0.67 |
| Q06 | crystal_fines_fraction | 0.61 | 0.44 | 0.77 |
| Q06 | crystal_purity | 0.98 | 0.92 | 1 |
| Q06 | crystal_size | 0.19 | 0.07 | 0.32 |
| Q06 | crystal_yield | 0.57 | 0.46 | 0.68 |
| Q07 | crystal_fines_fraction | 0.32 | 0.18 | 0.49 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.32 | 0.17 | 0.49 |
| Q07 | crystal_yield | 0.57 | 0.45 | 0.68 |
| Q08 | crystal_fines_fraction | 0.22 | 0.1 | 0.39 |
| Q08 | crystal_purity | 0.99 | 0.94 | 1 |
| Q08 | crystal_size | 0.4 | 0.22 | 0.6 |
| Q08 | crystal_yield | 0.53 | 0.4 | 0.65 |
| Q09 | crystal_fines_fraction | 0.92 | 0.72 | 0.99 |
| Q09 | crystal_purity | 0.94 | 0.82 | 0.99 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.1 |
| Q09 | crystal_yield | 0.08 | 0.02 | 0.18 |
| Q10 | crystal_fines_fraction | 0.59 | 0.4 | 0.8 |
| Q10 | crystal_purity | 0.96 | 0.88 | 1 |
| Q10 | crystal_size | 0.13 | 0.04 | 0.25 |
| Q10 | crystal_yield | 0.28 | 0.15 | 0.42 |
| Q11 | crystal_fines_fraction | 0.4 | 0.24 | 0.58 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.25 | 0.12 | 0.42 |
| Q11 | crystal_yield | 0.56 | 0.44 | 0.67 |
| Q12 | crystal_fines_fraction | 0.55 | 0.36 | 0.72 |
| Q12 | crystal_purity | 0.96 | 0.88 | 1 |
| Q12 | crystal_size | 0.24 | 0.1 | 0.42 |
| Q12 | crystal_yield | 0.45 | 0.31 | 0.58 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are extrapolations from the sealed campaign, not new experiments. Q01–Q02: S1 previously supported better target formation and fewer fines than S3, so Q01 is predicted to have higher recovery and be feasible. Q03–Q04: reducing seed mass should lower particle count and secondary nucleation, producing larger crystals and fewer fines, with only a small recovery penalty. Q05–Q06: both spend about 72 h crystallizing, but the gradual ramp should limit peak supersaturation; rapid cooling followed by a long low-temperature hold should achieve similar recovery but retain a finer population. Q07–Q08: the 315 K reheat is expected to dissolve preferentially small particles and improve size and fines after recooling, at the cost of some incompletely recovered product. Q09–Q10: the additional 7200 s at 292 K should materially increase growth and recovery, although the relatively warm endpoint and short overall history are still expected to leave low recovery and excessive fines. Q11–Q12: doubling reagent at fixed solvent and catalyst doubles concentration while halving catalyst-to-reagent ratio; the predicted result is lower fractional reaction/recovery and more supersaturation-driven fines, not doubled crystal_yield. All batches are seeded, so particles are expected. Intervals are deliberately broad because the recipes use 385 K chemistry, lower catalyst loading, much longer cooling histories, and solvent/seed combinations not directly replicated; several feasibility classifications near fines=0.50 are therefore uncertain.

## K2

## 1. Status of the main claims

### Supported within the tested scope

- **Catalyst identity affected target selectivity more than conversion.** Directly observed in the S0 catalyst screen at 360 K/1800 s: batches 1–4 all approached complete conversion, while selectivity, reaction yield and crystal yield varied substantially. C0 performed best overall (batch 1), C2 worst (batch 3), with C1 and C3 intermediate (batches 2 and 4). Interpreting this as altered reaction branching is mechanistic inference; the measurements directly establish only the differing outputs.
- **Solvent strongly coupled reaction performance to crystallization quality.** Under the initial crystallization schedule, S1 gave relatively high recovery but failed the fines constraint (batch 5), S2 gave slightly lower recovery but passed both constraints (batch 6), and S3 was poorer in recovery and fines (batch 7). This directly supports a material effect. Attribution to solubility, nucleation or growth coefficients remains interpretation because those quantities were not measured.
- **The combined low-seed/slow-cooling change improved particle quality.** Relative to batch 6, batch 8 reduced seed from 0.05 to 0.005 g and doubled cooling time to 14,400 s; fines fell from 0.456 to 0.306 while recovery remained about 0.61–0.62. Batches 9 and 10 retained feasibility at lower endpoints. The improvement is observed, but assigning it specifically to seed mass or cooling rate is not yet supported because both changed together.
- **Deeper terminal cooling produced a recovery–quality tradeoff in S2.** Across batches 8, 9 and 10, terminal temperatures of 278, 268 and 250 K corresponded to crystal yields of 0.620, 0.626 and 0.647, while fines rose from 0.306 to 0.324 and 0.342 and CSD quality declined. This is a consistent numerical trend, though it lacks replication and the batch-8/batch-9 yield difference is smaller than assay uncertainty.
- **The 340 K/3600 s reaction history was inferior to 360 K/1800 s in the tested process.** Batch 11 had lower selectivity, reaction yield and crystal yield than batch 10. The observation is direct; explanations such as unfavorable time-dependent branching or catalyst-state changes remain speculative.
- **Increasing concentration did not demonstrate a recovery benefit.** Batch 12 used 0.06 L rather than 0.08 L S2 and obtained nearly the same crystal yield as batch 10, but fines increased to 0.510. The inference that stronger supersaturation caused the fines increase is plausible but unmeasured.

### Contradicted or revised

- The initial expectation that **0.05 g seed plus nominally slow cooling would control fines** was contradicted by batches 1–4, whose final fines were approximately 0.87–0.98.
- The expectation that **milder reaction temperature would suppress side products** was contradicted by batch 11: the longer 340 K treatment reduced rather than improved selectivity.
- Any expectation that **greater concentration would materially raise fractional crystal recovery** was not supported by batch 12; its recovery was indistinguishable from batch 10 within measurement uncertainty, while quality worsened.

### Still untested

- The separate causal contributions of seed mass and cooling rate.
- Reproducibility of batch 10 and the size of genuine process variability.
- Catalyst-by-solvent interactions, because catalysts were screened only in S0.
- A reaction temperature–time response surface around 360 K.
- Direct solubility, supersaturation, nucleation-rate and growth-rate measurements; the classical nucleation equations in the account were explanatory models, not fitted laws.
- Whether a deliberate post-crystallization annealing cycle dissolves fines preferentially or instead causes renewed nucleation.

## 2. One additional experiment

I would run the batch-6 S2 process with only one change: reduce seed from 0.05 g to 0.005 g while retaining 360 K/1800 s reaction conditions and the 7200 s cooling trajectory to 278 K. I would measure particle size immediately before filtration and perform the normal final assay.

This experiment would triangulate batches 6 and 8:

- Batch 6: high seed, faster cooling, fines 0.456.
- Proposed experiment: low seed, faster cooling.
- Batch 8: low seed, slower cooling, fines 0.306.

If **seed population or seed-driven secondary nucleation is dominant**, the proposed batch should approach batch 8, with fines roughly 0.30–0.38 despite the faster cooling. If **cooling rate is dominant**, fines should remain near batch 6, roughly 0.42–0.48. An intermediate result would indicate that both factors contribute; comparison with batch 8 would then estimate the incremental value of slower cooling at fixed low seed. A result outside these ranges would challenge either the assumed monotonic mechanism or the reproducibility of the original batches.

## 3. Least-used observation and least-reliable prediction

The account used the **intermediate HPLC observation from batch 1** least effectively. Before crystallization it measured conversion about 0.996, yield about 0.733 and selectivity about 0.743; the final assay gave very similar reaction metrics. That agreement was useful evidence that the later cooling, warming and filtration history changed solid recovery and particle attributes without materially altering the upstream reaction composition. I relied mainly on final assays and did not exploit this direct stage-separation evidence enough. The paired in-process and final particle measurements likewise could have been used more explicitly to illustrate analytical variability.

The least reliable held-out prediction is **Q08**, the deliberate 315 K reheat followed by recooling. No campaign batch applied a comparable thermal annealing cycle to an established crystal population. Batch 1 experienced only an unintended warming from 278 to about 288 K and therefore provides weak guidance. Q08 could preferentially dissolve fines and improve size, as predicted, but it could instead dissolve substantial product, generate renewed supersaturation and nucleation during recooling, or alter impurity incorporation. Consequently, both the predicted quality improvement and the direction of the recovery change are more speculative than for comparisons that interpolate among observed seed, solvent or endpoint changes.
