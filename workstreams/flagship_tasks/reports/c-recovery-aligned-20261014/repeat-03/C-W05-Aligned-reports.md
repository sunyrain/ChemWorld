# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Process and key outcome
The recommended batch remains **batch 12**. It used catalyst C0 and solvent S2, a 415 K reaction treatment for 1,500 s, 0.005 g seed, staged cooling to 310 K and then 265 K, followed by a 7,200 s low-agitation hold before filtration. Its final assay gave seed-excluded crystal recovery 0.626, purity 0.999, and number fraction below 20 µm of 0.468. Thus it had the highest observed feasible recovery, although its fines margin was limited.

### Material effects
**Observed:** In the catalyst screen at 355 K with S2, C0 gave the highest crystal recovery among the tested catalysts: 0.417 in batch 2, versus 0.388 for C1 in batch 1, 0.350 for C2 in batch 3, and 0.408 for C3 in batch 4. All four met the purity and fines specifications. C2 also had the weakest final selectivity, 0.439, while C0 reached 0.515.

**Interpretation:** Catalyst choice primarily altered partitioning between target and byproduct rather than gross conversion, because conversion was already near unity. C0 was therefore selected empirically despite not having the highest nominal reference-panel activity. This revised the initial expectation that C1 or C3 might lead and indicates that fixed, reaction-specific catalyst effects outweighed the nominal aggregate ranking. The numerical differences among C0, C1 and C3 were not replicated, so only the poor performance of C2 appears comparatively clear.

The S2 dossier described low relative solubility, low nucleation tendency, high crystal-growth tendency and low impurity occlusion. The experiments were consistent with clean crystallization: every S2 batch had approximately 0.98–1.00 crystal purity, and most satisfied the fines limit. At otherwise similar 355 K reaction conditions, S1 gave high recovery in batch 7 (0.519) but fines of 0.550, while S3 gave recovery 0.397 and fines 0.793 in batch 8. Thus the initially proposed preference for S2 was retained. These comparisons do not isolate solvent effects perfectly, and S0 was not tested.

### Reaction mechanism and temperature dependence
Across the useful conditions, conversion was essentially complete; the important upstream variable was selectivity. For C0/S2, batch 5 at 335 K for 7,200 s gave selectivity 0.379, byproduct signal 0.453 and crystal recovery 0.291. Batch 2 at 355 K for 3,600 s gave selectivity 0.515 and recovery 0.417. Batch 6 at 375 K for 2,400 s gave selectivity 0.589 and recovery 0.524. With the refined crystallization history, batch 11 at 395 K for 1,800 s gave selectivity 0.656 and recovery 0.592, and batch 12 at 415 K for 1,500 s gave selectivity 0.669 and recovery 0.626.

A useful minimal interpretation is competitive target and byproduct formation,

k_T = A_T exp(-E_T/RT),  k_B = A_B exp(-E_B/RT),

with an approximate intrinsic selectivity k_T/(k_T+k_B). The observed improvement at higher temperature is consistent with the target channel having a stronger temperature response than the competing channel. An equally plausible alternative is process-history control: the progressively shorter hot residence may have suppressed a slower secondary or degradation pathway. Temperature and residence time changed together, so the campaign cannot distinguish these explanations or establish an optimum above 415 K. Conversion saturation also means further heating should be judged by selectivity and degradation, not conversion alone.

### Reaction–crystallization coupling
Overall crystal recovery can be represented as

Y_crystal = Y_target,liquid × f_capture,

where Y_crystal is explicitly seed-excluded and normalized to initial reagent. Using final chemical yield as a proxy for Y_target,liquid, the apparent capture fraction increased from about 0.828 in batch 2 to 0.886 in batch 6, 0.895 in batch 9, 0.923 in batch 10, 0.929 in batch 11 and 0.929 in batch 12. Therefore the later recovery gains had two components: improved reaction selectivity raised the available target amount, while the refined crystallization history recovered a larger fraction of that target as isolated solid.

Purity remained high even when upstream selectivity was only moderate. This suggests that S2 crystallization strongly rejected the measured byproduct from the lattice or left it in the mother liquor. High isolated purity consequently does not imply a clean reaction; upstream byproduct formation still reduced the maximum recoverable target mass.

### Process-history dependence
Batch 6 used 0.020 g seed and direct cooling to 278 K over 7,200 s, producing recovery 0.524 and fines 0.421. Batch 9 reduced seed to 0.005 g and used staged cooling—first to 310 K, then slowly to 278 K—giving recovery 0.527 and fines 0.452. Batch 10 retained low seed, cooled in stages to 265 K, and added a 7,200 s low-agitation hold; recovery rose to 0.544 while fines were 0.435.

The mechanistic rationale is supersaturation control. With S = C/C*, crystal growth may be written schematically as G = k_g(S-1)^g and nucleation as B = k_b(S-1)^b. Because nucleation commonly becomes more sensitive than growth at high supersaturation, abrupt deep cooling can create many fines. Staged cooling and existing seed surface let growth consume supersaturation before uncontrolled nucleation, while the final hold can permit additional deposition and ripening. The batch 9–10 comparison is consistent with this account, but deeper final cooling and the hold were introduced together; their separate effects remain untested. Seed amount was also not independently replicated.

### Revisions and uncertainty
The initial working view favored S2 and moderate-temperature reaction conditions, with C1 or C3 considered plausible catalyst leaders. The catalyst screen revised the catalyst choice to C0. The temperature series then revised the moderate-temperature assumption: within the sampled range, hotter and shorter processing improved target selectivity and recovery without approaching the safety limit. Finally, staged deep cooling plus a hold replaced simple direct cooling after it increased apparent capture while retaining acceptable fines.

Instrument and run variability limit the strength of these conclusions. Each leading condition was run once, temperature was confounded with residence time, and crystallization changes were bundled. Particle-size readings also differed modestly by measurement stage: for example, batch 10 gave fines 0.414 in situ and 0.435 in the final assay; batch 12 gave 0.470 and 0.468, respectively. Such differences are compatible with measurement noise and sampling-stage effects rather than true process changes.

### Unresolved recovery–quality tradeoff
Batch 12 maximized observed recovery but had fines 0.468, only 0.032 below the 0.50 limit. Batch 11 had lower recovery, 0.592, but a more comfortable fines value of 0.431. Purity was not the limiting quality attribute: both were near 1.00. Thus the unresolved tradeoff is recovery versus robustness to the fines constraint. Batch 12 remains the recommendation because it was feasible and had the greatest observed recovery, but confirmation would be important. Reproducible fines above 0.50 or lower recovery at its conditions would favor the more conservative batch-11 history; no such confirmation was available in this campaign.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.43 |
| Q01 | crystal_purity | 0.975 | 0.94 | 0.995 |
| Q01 | crystal_size | 0.14 | 0.09 | 0.2 |
| Q01 | crystal_yield | 0.36 | 0.25 | 0.47 |
| Q02 | crystal_fines_fraction | 0.55 | 0.4 | 0.7 |
| Q02 | crystal_purity | 0.94 | 0.87 | 0.98 |
| Q02 | crystal_size | 0.1 | 0.06 | 0.15 |
| Q02 | crystal_yield | 0.23 | 0.12 | 0.34 |
| Q03 | crystal_fines_fraction | 0.6 | 0.4 | 0.78 |
| Q03 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q03 | crystal_size | 0.1 | 0.05 | 0.18 |
| Q03 | crystal_yield | 0.02 | 0 | 0.08 |
| Q04 | crystal_fines_fraction | 0.47 | 0.32 | 0.62 |
| Q04 | crystal_purity | 0.95 | 0.87 | 0.995 |
| Q04 | crystal_size | 0.08 | 0.05 | 0.13 |
| Q04 | crystal_yield | 0.035 | 0 | 0.1 |
| Q05 | crystal_fines_fraction | 0.44 | 0.3 | 0.59 |
| Q05 | crystal_purity | 0.95 | 0.87 | 0.995 |
| Q05 | crystal_size | 0.09 | 0.055 | 0.145 |
| Q05 | crystal_yield | 0.035 | 0 | 0.1 |
| Q06 | crystal_fines_fraction | 0.72 | 0.56 | 0.85 |
| Q06 | crystal_purity | 0.88 | 0.78 | 0.96 |
| Q06 | crystal_size | 0.055 | 0.025 | 0.1 |
| Q06 | crystal_yield | 0.04 | 0 | 0.11 |
| Q07 | crystal_fines_fraction | 0.42 | 0.28 | 0.57 |
| Q07 | crystal_purity | 0.95 | 0.87 | 0.995 |
| Q07 | crystal_size | 0.095 | 0.06 | 0.15 |
| Q07 | crystal_yield | 0.04 | 0 | 0.11 |
| Q08 | crystal_fines_fraction | 0.28 | 0.16 | 0.43 |
| Q08 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q08 | crystal_size | 0.13 | 0.075 | 0.2 |
| Q08 | crystal_yield | 0.025 | 0 | 0.09 |
| Q09 | crystal_fines_fraction | 0.46 | 0.3 | 0.63 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.075 | 0.04 | 0.12 |
| Q09 | crystal_yield | 0.002 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q10 | crystal_purity | 0.985 | 0.93 | 1 |
| Q10 | crystal_size | 0.085 | 0.045 | 0.14 |
| Q10 | crystal_yield | 0.008 | 0 | 0.04 |
| Q11 | crystal_fines_fraction | 0.46 | 0.31 | 0.61 |
| Q11 | crystal_purity | 0.95 | 0.86 | 0.995 |
| Q11 | crystal_size | 0.085 | 0.05 | 0.14 |
| Q11 | crystal_yield | 0.035 | 0 | 0.1 |
| Q12 | crystal_fines_fraction | 0.68 | 0.52 | 0.82 |
| Q12 | crystal_purity | 0.86 | 0.74 | 0.94 |
| Q12 | crystal_size | 0.06 | 0.03 | 0.1 |
| Q12 | crystal_yield | 0.23 | 0.13 | 0.34 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is predicted to outperform S3 in recovery and particle quality because its lower solubility, lower nucleation tendency, higher growth tendency, and lower impurity occlusion favor capture into cleaner, coarser crystals. Q03–Q04: with high-nucleation S0, the larger seed charge should consume supersaturation more effectively and reduce secondary fines, although the seed-excluded recovery remains small at this dilute loading. Q05–Q06: slow distributed cooling should suppress the nucleation burst produced by an initial crash; the long subsequent hold can improve recovery but cannot fully erase the crash-generated number population. Q07–Q08: the 315 K thermal cycle is expected to dissolve preferentially small or defective crystals and recrystallize a coarser, purer population, at a modest recovery penalty. Q09–Q10: particles are present from seeding, but only negligible seed-excluded product is expected after the 60-second step; the additional 292 K hold permits limited growth and ripening. Q11–Q12: doubling reagent loading greatly increases supersaturation and therefore overall seed-excluded recovery, but is predicted to increase impurity occlusion and secondary nucleation enough to violate the fines limit. Intervals are deliberately broad because S0 was not tested in the campaign, these recipes use much lower concentration and catalyst loading than the source experiments, and seed loading, cooling duration, and thermal cycling were not independently replicated.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C0 was the best observed catalyst at 355 K in S2.** Under the common screened recipe, batch 2 gave crystal yield 0.417, compared with 0.388 for C1 (batch 1), 0.350 for C2 (batch 3), and 0.408 for C3 (batch 4). This directly supports the empirical choice of C0, especially over C2. It does not establish a general catalyst ranking because each condition was run once.
- **Reaction outcome improved along the tested hotter/shorter sequence.** For C0/S2, batch 5 (335 K, 7,200 s) gave final selectivity 0.379 and crystal yield 0.291; batch 2 (355 K, 3,600 s) gave 0.515 and 0.417; batch 6 (375 K, 2,400 s) gave 0.589 and 0.524. With the refined crystallization history, batch 11 (395 K, 1,800 s) gave 0.656 and 0.592, while batch 12 (415 K, 1,500 s) gave 0.669 and 0.626. The trend itself is observed.
- **S2 provided a better recovery/quality compromise than the tested alternatives.** At the 355 K comparison, S1 in batch 7 produced high recovery, 0.519, but failed the fines criterion at 0.550. S3 in batch 8 gave lower recovery, 0.397, and much worse fines, 0.793. S2 in batch 2 gave 0.417 recovery with fines 0.476. Thus S2 was directly feasible where S1 and S3 were not, although reaction and crystallization solvent effects were not separated.
- **High crystal purity did not require high reaction selectivity.** Batches 1–4 had final selectivities of roughly 0.44–0.51 but crystal purities of 0.983–1.000. This directly supports selective rejection of byproduct during crystallization or filtration.
- **The leading process met the stated constraints.** Batch 12 directly measured yield 0.626, purity 0.999, and fines 0.468. Batch 11 also met the constraints, with yield 0.592 and a wider fines margin at 0.431.

### Supported as trends, but not causally isolated
- **Staged/deeper cooling and a hold improved capture.** Batch 6 used direct cooling to 278 K and gave an apparent capture ratio of about 0.886. Batch 9 used lower seed and staged cooling to 278 K and reached about 0.895; batch 10 added cooling to 265 K plus a hold and reached about 0.923. These observations support process-history dependence, but seed dose, endpoint temperature, cooling profile, and hold time changed together.
- **S2 behaves consistently with its nominal low-solubility, high-growth, low-occlusion description.** Its consistently high purity and generally acceptable fines support that interpretation. They do not prove the nominal material descriptors are the causal variables.

### Contradicted or revised
- **The initial expectation that C1 or C3 might lead was contradicted within the 355 K screen.** C0 was numerically best, while C2 was clearly poorer.
- **The initial preference for a moderate reaction temperature was revised.** Every sampled move toward hotter, shorter treatment improved the observed selectivity and recovery through batch 12.
- **A simple belief that deeper cooling necessarily worsens fines was not supported.** Batch 10, with a 265 K endpoint and hold, had fines 0.435 versus 0.452 in batch 9 at 278 K. However, the hold prevents attributing this result to endpoint temperature alone.

### Still untested
- Whether the temperature trend reflects a larger activation energy for target formation, suppression of a time-dependent secondary pathway by shorter residence, or both.
- Replication of batches 11 and 12, behavior above 415 K, and the actual location of the temperature optimum.
- Independent effects of seed mass, cooling rate, final temperature, and ripening time.
- S0 solvent behavior; it was absent from the completed campaign.
- Thermal cycling or reheating after crystallization.
- Whether the calculated “capture ratios” truly represent equilibrium recovery: they use final chemical yield as a proxy and combine process and analytical uncertainty.

## 2. One additional experiment

I would run **C0/S2 at 395 K for 1,500 s**, using exactly the same loading, 0.005 g seed, staged cooling to 310 K and 265 K, 7,200 s low-agitation hold, filtration, and assays used in batches 11–12.

This fills the missing corner between batch 11 (395 K, 1,800 s) and batch 12 (415 K, 1,500 s):
- Comparing it with batch 11 isolates the effect of shortening residence from 1,800 to 1,500 s at 395 K.
- Comparing it with batch 12 isolates the effect of raising temperature from 395 to 415 K at a fixed 1,500 s.

Expected diagnostic outcomes:
- **Higher-activation-energy target pathway:** the new batch would remain clearly below batch 12 in selectivity and recovery, while shortening the 395 K residence would have little benefit relative to batch 11.
- **Time-dependent byproduct or degradation pathway:** shortening to 1,500 s at 395 K would materially improve on batch 11 and could approach batch 12, showing that residence time caused much of the apparent temperature trend.
- **Both mechanisms:** it would improve on batch 11 but remain below batch 12.
- **No reproducible difference:** values overlapping both prior batches would indicate that the apparent trend is too small relative to batch variability to support either mechanism strongly.

One batch cannot establish repeatability, but this condition provides the cleanest discrimination available from a single additional experiment.

## 3. Least-used observation and least-reliable prediction

The account used the **intermediate particle-size measurements in batches 9–12** least effectively. It noted their disagreement with final assays but did not fully exploit it. For example, batch 12 changed from an in-situ size index of 0.059 and fines 0.470 to final values of 0.099 and 0.468; batch 10 changed from fines 0.414 to 0.435. Across the four batches, the directions were not consistent. These data could have been used more explicitly to separate measurement noise from filtration-stage selection, settling, or sampling effects and to widen uncertainty on size predictions.

The least reliable held-out prediction is **Q08**, the reheating/thermal-cycle recipe. No completed batch reheated an established crystal population to 315 K and then recrystallized it over only 3,600 s. My prediction that this would preferentially dissolve fines and yield larger, purer crystals with a recovery penalty was mechanistically plausible but unsupported by direct campaign evidence. Depending on the unknown solubility curve, the reheating could instead dissolve nearly all solids, leave insufficient time for recrystallization, or trigger a new nucleation burst. Its predicted particle size, fines fraction, and even particle persistence therefore have unusually high structural uncertainty. Q12 is also uncertain because it extrapolates untested S0 behavior and doubled loading, but it does not introduce an entirely new unit operation history as Q08 does.
