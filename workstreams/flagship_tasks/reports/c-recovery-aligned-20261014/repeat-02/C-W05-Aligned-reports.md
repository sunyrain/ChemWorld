# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Reaction-stage material effects

**Observation.** In the directly comparable C0–C3 screen using S2 at 390 K for 3600 s, conversion was essentially complete, but product selectivity differed. C0 gave the best final reaction yield/selectivity and the highest downstream crystal recovery: batch 4 had reaction yield 0.539, selectivity 0.553, and crystal yield 0.452. The corresponding crystal yields were 0.409 for C1 (batch 1), 0.419 for C2 (batch 5), and 0.373 for C3 (batch 3). All four S2 batches had high crystal purity and fines below 0.50.

**Interpretation.** A useful minimal reaction model is a competition between desired and byproduct pathways,

`R → P` with rate `kP`, and `R → B` with rate `kB`,

so that at high conversion the intrinsic selectivity is approximately `kP/(kP+kB)`. The catalysts appear to change this rate ratio more than the ultimate conversion. C0 favored the desired pathway under the tested S2 conditions; C3 produced more byproduct and degradation. This revised the initial dossier-based expectation that C1 or C3 might be preferable.

**Uncertainty.** Each catalyst was tested only once under the common condition. The ordering is therefore supported within this local process window, not established as a universal catalyst ranking. Catalyst–solvent interactions, catalyst loading effects, and shorter optimized reaction times remain untested.

### 2. Solvent effects and reaction–crystallization coupling

**Observation.** With C0 and otherwise similar reaction histories, changing solvent strongly affected both reaction performance and particle quality:

- Batch 4, S2: crystal yield 0.452, purity 1.000, fines 0.413.
- Batch 6, S1: crystal yield 0.534, purity 0.998, fines 0.622.
- Batch 8, S0: crystal yield 0.540, purity 0.980, fines 0.811.
- Batch 7, S3: crystal yield 0.409, purity 0.968, fines 0.793.

S0 and S1 gave the strongest reaction-stage product yields—approximately 0.650 and 0.624—but both violated the fines constraint. S2 sacrificed some reaction yield while furnishing a much better particle population. Purity was high in every solvent, so fines, rather than chemical purity, controlled feasibility.

**Interpretation.** The solvent acts twice. First, it changes reaction selectivity and byproduct formation. Second, it sets product solubility, supersaturation, nucleation, growth, and impurity occlusion during cooling. A useful recovery decomposition is

`Ycrystal ≈ Yreaction × Rcapture`,

where `Ycrystal` is seed-excluded target solid divided by initial reagent, `Yreaction` is the target-product yield before isolation, and `Rcapture` is the fraction of that product captured as crystals. Approximate capture ratios were 0.84 for batch 4, 0.86 for batch 6, 0.83 for batch 8, and 0.77 for batch 7. Thus the large solvent differences in final recovery arose mainly upstream, whereas the decisive specification difference arose from nucleation and growth downstream.

A qualitative crystallization description is

`S(t) = C(t)/C*(T,solvent) − 1`,

`Nprimary ∝ ∫ kn[max(S(t),0)]^m dt`,

`growth ∝ ∫ kg[max(S(t),0)]^g dt`.

S0 and S1 likely generated a supersaturation trajectory favoring many nuclei relative to growth, explaining their high number fraction below 20 µm. S2's nominally lower nucleation tendency, stronger growth, and lower impurity occlusion are consistent with its high purity and lower fines. This remains a mechanistic interpretation rather than a directly measured supersaturation or nucleation-rate law.

### 3. Process-history dependence

The results show that final quality cannot be inferred from endpoint temperature alone; the entire thermal, seeding, concentration, and agitation history matters.

- Batch 2 used C1 at 360 K and cooled to 265 K. It gave fines of 1.000, versus 0.442 in batch 1, which used C1 at 390 K and cooled to 270 K. Because both reaction temperature and crystallization endpoint changed, this contrast does not isolate a 265 K endpoint effect. It nevertheless warns that the combined lower-temperature history can enter a severe secondary-nucleation regime.
- For S0, changing from the standard history in batch 8 to 0.20 g seed, a 275 K endpoint, slower cooling, and a longer hold in batch 9 reduced fines from 0.811 to 0.721, but also reduced crystal yield from 0.540 to 0.518. The improvement was insufficient for specification and cannot be assigned to any one altered variable.
- A related S1 modification in batch 10—0.20 g seed, 280 K endpoint, slow cooling, and long hold—gave yield 0.518 and fines 0.638, offering no convincing quality improvement over batch 6.

More seed supplies growth surface and can consume supersaturation, but it also adds many particles to a number-weighted distribution and may not prevent primary or secondary nucleation. Warmer endpoints reduce supersaturation and recovery. Slow cooling helps only if growth can consume solute quickly enough; solvent-specific nucleation may still dominate.

### 4. Concentration and the unresolved quality–recovery boundary

**Observation.** Concentrating the C0/S2 process increased recovery but destabilized fines performance. Relative to batch 4 with 0.08 L S2, batch 11 used 0.06 L and increased crystal yield from 0.452 to 0.467, while fines increased from 0.413 to 0.512. Batch 12 used an intermediate 0.065 L and gave nearly identical yield, 0.467, but unexpectedly higher fines, 0.601.

**Revision.** Before batch 12, I expected intermediate dilution to preserve most of the recovery gain while restoring fines below 0.50. Batch 12 disconfirmed that simple interpolation. The response is evidently noisy, nonlinear, or sensitive to uncontrolled trajectory differences. It should not be represented as a smooth monotonic loading law on the present evidence.

**Measurement uncertainty.** Paid particle measurements and final assays sometimes differed by roughly 0.01–0.03 in fines: batch 11 read 0.523 in situ and 0.512 at final assay; batch 9 read 0.730 and 0.721; batch 10 read 0.617 and 0.638. Consequently, batch 11 is not a robustly feasible boundary point even though its excess over 0.50 is small. No replicate batches were run, so process variability cannot be separated from instrument noise.

### 5. Recommended mechanistic operating window

The sealed recommendation remains batch 4: 0.04 mol reagent, 0.08 L S2, 0.005 mol C0, nitrogen control, reaction at 390 K for 3600 s, quench, 0.05 g seed, cooling to 270 K over 10800 s, holding 7200 s at 200 rpm, and filtration. Its final assay—crystal yield 0.4525, purity 1.000, and fines 0.413—provided the highest measured recovery among batches satisfying both constraints.

This is a conservative interior-quality choice rather than the maximum observed recovery. S0, S1, and concentrated S2 demonstrated that recovery near 0.47–0.54 is possible, but every such tested process exceeded the fines limit.

### 6. Untested alternatives

Potential routes to break the tradeoff include staged cooling with a controlled supersaturation set point, changing seed size rather than only seed mass, adding seed at a lower supersaturation, varying agitation during nucleation and growth separately, mixed-solvent operation, staged solvent addition, and optimizing C0 reaction time to reduce degradation without losing conversion. These alternatives were not tested and should not be treated as demonstrated improvements. Replication around batch 4 and the batch-11 boundary would be the first priority for estimating reproducibility and determining whether a higher-recovery process can meet the fines constraint reliably.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.45 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.16 | 0.1 | 0.24 |
| Q01 | crystal_yield | 0.48 | 0.38 | 0.58 |
| Q02 | crystal_fines_fraction | 0.52 | 0.34 | 0.69 |
| Q02 | crystal_purity | 0.955 | 0.9 | 0.99 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q02 | crystal_yield | 0.38 | 0.28 | 0.49 |
| Q03 | crystal_fines_fraction | 0.66 | 0.48 | 0.81 |
| Q03 | crystal_purity | 0.96 | 0.91 | 0.99 |
| Q03 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q03 | crystal_yield | 0.4 | 0.31 | 0.5 |
| Q04 | crystal_fines_fraction | 0.47 | 0.32 | 0.62 |
| Q04 | crystal_purity | 0.965 | 0.92 | 0.995 |
| Q04 | crystal_size | 0.08 | 0.04 | 0.14 |
| Q04 | crystal_yield | 0.41 | 0.32 | 0.51 |
| Q05 | crystal_fines_fraction | 0.43 | 0.29 | 0.58 |
| Q05 | crystal_purity | 0.97 | 0.93 | 0.997 |
| Q05 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q05 | crystal_yield | 0.41 | 0.32 | 0.51 |
| Q06 | crystal_fines_fraction | 0.68 | 0.52 | 0.82 |
| Q06 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q06 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q06 | crystal_yield | 0.42 | 0.33 | 0.52 |
| Q07 | crystal_fines_fraction | 0.44 | 0.29 | 0.59 |
| Q07 | crystal_purity | 0.97 | 0.93 | 0.997 |
| Q07 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q07 | crystal_yield | 0.42 | 0.33 | 0.52 |
| Q08 | crystal_fines_fraction | 0.58 | 0.39 | 0.75 |
| Q08 | crystal_purity | 0.975 | 0.93 | 1 |
| Q08 | crystal_size | 0.085 | 0.04 | 0.16 |
| Q08 | crystal_yield | 0.37 | 0.26 | 0.48 |
| Q09 | crystal_fines_fraction | 0.58 | 0.38 | 0.76 |
| Q09 | crystal_purity | 0.98 | 0.93 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.09 |
| Q09 | crystal_yield | 0.08 | 0.01 | 0.18 |
| Q10 | crystal_fines_fraction | 0.48 | 0.31 | 0.65 |
| Q10 | crystal_purity | 0.975 | 0.93 | 1 |
| Q10 | crystal_size | 0.065 | 0.025 | 0.12 |
| Q10 | crystal_yield | 0.2 | 0.1 | 0.32 |
| Q11 | crystal_fines_fraction | 0.47 | 0.31 | 0.63 |
| Q11 | crystal_purity | 0.965 | 0.92 | 0.995 |
| Q11 | crystal_size | 0.085 | 0.04 | 0.15 |
| Q11 | crystal_yield | 0.41 | 0.31 | 0.51 |
| Q12 | crystal_fines_fraction | 0.6 | 0.43 | 0.76 |
| Q12 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q12 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q12 | crystal_yield | 0.45 | 0.34 | 0.56 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where little seed-excluded product crystallizes. For the solvent pair, S1 is predicted to outperform S3 in recovery, purity, growth, and fines because campaign batches 6 and 7 showed the same direction and the nominal dossier favors S1 for lower solubility, lower occlusion, and lower nucleation. For the seed pair, 0.045 g should suppress spontaneous nucleation relative to 0.001 g, although distributing solute over more seed surface limits size. Gradual cooling (Q05) should produce fewer fines and larger particles than the rapid quench-and-hold history (Q06); equal final temperatures do not erase early nucleation history. The 315 K recycle in Q08 may dissolve small crystals but, with only a one-hour recool, is expected to reduce recovered yield and regenerate fines relative to the uninterrupted history Q07. Extending growth at 292 K from 60 s to two hours raises seed-excluded yield and size and lowers fines (Q09–Q10), though recovery remains incomplete. Doubling reagent loading (Q11–Q12) raises supersaturation and predicted recovery but also nucleation, fines, and impurity occlusion. Intervals are epistemic 80% ranges for the noise-free latent outcomes, not final-assay noise; they are broad because the campaign had no replicates and did not directly test these very long multistage cooling programs, extreme seed-to-reagent ratios, or the thermal recycle. Feasibility flags use the point estimates, so Q02, Q04, Q05, Q07, Q10, and Q11 are especially sensitive to the unresolved fines boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **C0 was the best tested catalyst in S2 at 390 K for 3600 s.** Under closely matched crystallization conditions, batch 4 produced crystal yield 0.4525, versus 0.4090 for C1 (batch 1), 0.4193 for C2 (batch 5), and 0.3728 for C3 (batch 3). All four met the purity and fines specifications. This supports a local catalyst ranking, not a universal one.
- **There was a strong solvent-dependent recovery–fines tradeoff.** With C0, S0 and S1 increased crystal yield to 0.5400 and 0.5341 in batches 8 and 6, but fines rose to 0.8111 and 0.6215. S2 in batch 4 gave lower recovery, 0.4525, but acceptable fines of 0.4130. S3 in batch 7 combined lower recovery, 0.4088, with excessive fines, 0.7928.
- **Purity was not the limiting quality attribute.** The relevant final assays were all comfortably above 0.80 purity; feasibility was governed principally by the number fraction below 20 µm.
- **Increasing S2 concentration exposed a quality boundary.** Reducing S2 from 0.08 L in batch 4 to 0.06 L in batch 11 raised crystal yield from 0.4525 to 0.4666, but fines rose from 0.4130 to 0.5123. Batch 12 at 0.065 L gave similar yield, 0.4668, but still worse fines, 0.6013.

### Contradicted or revised

- **The initial expectation that C1 or C3 might outperform C0 was contradicted** by batches 1, 3, 4, and 5 under the common C/S2 process window.
- **The precommitted interpolation for batch 12 was contradicted.** I expected 0.065 L S2 to retain most of the concentrated-process recovery while restoring fines below 0.50. Instead, batch 12 had fines of 0.6013.
- **A simple claim that more seed, slower cooling, or a warmer endpoint would rescue S0/S1 was not supported.** The combined modifications in batch 9 reduced S0 fines from 0.8111 to 0.7208 but did not achieve feasibility. The corresponding S1 modification in batch 10 gave fines of 0.6381, no improvement over batch 6 within the resolution of these single runs.

### Interpretations rather than direct observations

- The parallel desired/byproduct reaction model and the interpretation that C0 improves the ratio of desired to byproduct rates are consistent with conversion, selectivity, and byproduct signals, but pathway-specific rate constants were not measured.
- The explanation that S0/S1 generate a nucleation-dominated supersaturation trajectory, while S2 favors growth, is consistent with the material dossier and particle outcomes. Supersaturation, nucleation rate, growth rate, and seed-size distributions were not directly observed.
- Broad process-history dependence is supported, but individual causal effects are unresolved because batches 9 and 10 simultaneously changed seed mass, cooling time, endpoint, and hold time.

### Still untested

Catalyst–solvent interactions, replication and batch variability, seed-size effects independent of seed mass, isolated cooling-rate effects, seeding-temperature effects, staged supersaturation control, mixed solvents, reaction-time optimization, and deliberate dissolution–recrystallization cycles remain untested.

## 2. One additional experiment

I would repeat the batch-8 S0/C0 recipe while changing only the cooling duration: retain 0.04 mol reagent, 0.08 L S0, 0.005 mol C0, the 390 K/3600 s reaction, 0.05 g seed, 270 K endpoint, 7200 s final hold, and 200 rpm agitation, but extend the 343-to-270 K cooling ramp from 10,800 s to about 57,600 s. Non-destructive particle measurements at several temperature waypoints could be included within the same experiment.

This would distinguish two competing explanations:

1. **Supersaturation-generation-rate explanation:** batch 8 made many fines because cooling created supersaturation faster than seeded growth could consume it. A much slower ramp should then suppress the rise in fines, increase particle size, and potentially bring fines below 0.50 while retaining crystal yield near the batch-8 level.
2. **Solvent-intrinsic or seed-population explanation:** S0 has such a strong nucleation tendency—or the seed population contributes so many small particles—that slowing the ramp alone cannot solve the problem. Fines would remain high, plausibly above roughly 0.65, while final yield changed little.

An intermediate result would suggest both mechanisms contribute. Unlike batches 8 and 9, this experiment would isolate cooling rate rather than changing seed mass, endpoint, ramp time, and hold simultaneously.

## 3. Least effectively used observation and least reliable prediction

### Least effectively used observation

**Batch 2** was used least effectively. It produced the striking fines value of 1.000, but it differed from batch 1 in both reaction temperature and crystallization endpoint: 360 K and 265 K in batch 2 versus 390 K and 270 K in batch 1. Its HPLC result also showed lower upstream yield/selectivity. I could therefore use it only as evidence that the combined history was poor; it could not identify whether the extreme fines arose from deeper cooling, altered impurity composition, reaction history, or their interaction. My early interpretation leaned too heavily toward the colder endpoint before explicitly recognizing this confounding.

### Least reliable held-out prediction

**Q08 is the least reliable prediction.** It applies a 315 K reheat after a very long crystallization and then allows only a one-hour recool. No campaign batch tested a dissolution–recrystallization cycle. The outcome depends on unknown solubility at 315 K, whether all small crystals or even the seeds dissolve, and whether the rapid recool favors growth on surviving crystals or renewed nucleation. Those alternatives predict opposite fines responses: selective dissolution could reduce fines, whereas complete dissolution followed by rapid recooling could increase them. Consequently, the sealed Q08 point estimate rests on substantially more extrapolation than the ordinary solvent, loading, or hold-time comparisons.
