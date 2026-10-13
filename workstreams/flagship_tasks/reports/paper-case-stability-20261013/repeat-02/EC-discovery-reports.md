# EC-discovery — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Experimental scope

All 12 batches used 0.020 mol of limiting reagent in 0.040 L of one solvent, corresponding to a nominal initial loading of 0.50 mol L⁻¹. The controlled variables were potential, current cap, electrolysis duration, solvent label, and electrolyte label. Every batch received an intermediate UV–visible measurement and a final assay. The labels S0–S3 and E0–E3 are anonymous benchmark materials, so no molecular identities or real-material properties can be inferred.

The principal comparison set was S0/E0. Batches 1–4 tested polarity and potential magnitude at 100 mA for 600 s. Batches 5–6 varied duration at +1 V and 100 mA. Batches 7–8 varied the current cap at +1 V for 3600 s. Batches 9–12 explored material combinations at +1 V, 100 mA, and 3600 s.

### Proposed process structure

I infer that target formation requires access to a relatively narrow, positive-potential electrochemical window. Within that window, productive conversion accumulates with exposure time, but the current cap determines whether the cell is rate-limited, productive, or driven into an inefficient competing regime. Solvent and electrolyte alter charge transport, faradaic utilization, selectivity, pH-like state, and precipitation behavior.

A useful phenomenological decomposition is

C(t,V,I,S,E) = Cmax(S,E)·[1 − exp(−k(S,E)·gV(V)·gI(I)·t)],

where C is conversion, gV is a polarity-sensitive potential-window function, and gI is a non-monotonic current-regime factor. Target yield may then be approximated at adequately resolved signal levels by

Ytarget ≈ C·Sel,

with Sel governed by potential, current regime, and materials. A balanced efficiency score additionally depends on faradaic, transport, ohmic, and energy efficiencies, so maximum conversion need not maximize the reported score.

This is an empirical model, not a uniquely identified elementary mechanism. In particular, configured current is only a cap; delivered current and total charge were not measured. Thus k·gI cannot be interpreted directly as an electron-transfer rate constant or Coulombic dose.

### Evidence for a polarity-sensitive potential window

Batch 1, at S0/E0, +1 V, 100 mA, and 600 s, produced final conversion 0.0206 and selectivity 0.9496. Its faradaic, transport, ohmic, and energy efficiencies were 0.832, 0.803, 0.970, and 0.801, respectively. This showed that +1 V lies in a productive, efficient regime, although the final selective-yield estimate was clipped or resolved as zero at this low product level.

Changing only the potential sign in batch 2 (−1 V) gave final conversion reported as zero, selectivity 0.626, faradaic efficiency 0.393, transport efficiency 0.419, and energy efficiency 0.240. The independently processed selective-yield channel was 0.0127 despite zero reported conversion. I treat that low-signal inconsistency as measurement/processing uncertainty, not evidence that yield is physically independent of conversion.

Increasing the magnitude did not improve production. Batch 3 at +2 V gave zero conversion, zero selectivity, and essentially zero faradaic, transport, and energy efficiency. Batch 4 at −2 V gave conversion 0.00011, selective yield 0.00270, selectivity 0.463, faradaic efficiency 0.279, transport efficiency 0.247, and energy efficiency 0.0252.

These four batches rule out a simple dependence on |V| or a monotonic acceleration with increasing positive voltage. A plausible gV is a peaked function centered somewhere near +1 V, such as

gV(V) ≈ exp[−(V−V*)²/(2σV²)]·P(V),

where V* is near +1 V and P(V) imposes the observed polarity asymmetry. The precise optimum and width are not identifiable because only ±1 and ±2 V were sampled. A threshold-plus-degradation model is an equally plausible alternative: target reduction/oxidation begins at a positive onset, while +2 V activates solvent/electrolyte decomposition or another parasitic pathway.

### Time dependence in the productive regime

At S0/E0, +1 V, and 100 mA, extending electrolysis increased conversion while selectivity remained nearly constant:

- Batch 1, 600 s: conversion 0.0206; selectivity 0.9496.
- Batch 5, 3600 s: conversion 0.07645; selectivity 0.9457; selective yield 0.0770.
- Batch 6, 14400 s: conversion 0.2637; selectivity 0.9435; selective yield 0.2560.

The 3600 and 14400 s conversions are described well by C(t)=1−exp(−kt) with k around 2.1×10⁻⁵ s⁻¹: this gives approximately 0.073 at 3600 s and 0.263 at 14400 s. It predicts about 0.013 at 600 s, somewhat below the observed 0.0206. That discrepancy could reflect assay noise, a fast initial component, or inadequacy of the single-exponential model.

At the two higher-conversion points, C·Sel is close to the measured selective yield: 0.07645×0.9457≈0.0723 versus measured 0.0770, and 0.2637×0.9435≈0.2488 versus measured 0.2560. The residuals are of the scale expected from independently noisy assay channels. These data support accumulation of a mostly selective target in this time range. They do not establish an ultimate conversion plateau because the longest tested duration was 14400 s.

Efficiency declined modestly with extended operation. Batch 5 had faradaic/transport/energy efficiencies of 0.794/0.783/0.743; batch 6 had 0.725/0.700/0.686. This suggests progressive depletion, increasing polarization, product inhibition, or greater parasitic charge consumption. The experiment does not distinguish these processes.

### Non-monotonic current-cap coupling

Batches 5, 7, and 8 compared current caps at +1 V, 3600 s, S0/E0:

- Batch 7, 20 mA: conversion 0.0274, selective yield 0.0233, selectivity 0.937, faradaic efficiency 0.917, transport efficiency 0.920, energy efficiency 0.901, and ohmic efficiency reported at 1.000.
- Batch 5, 100 mA: conversion 0.07645, selective yield 0.0770, selectivity 0.946, faradaic efficiency 0.794, transport efficiency 0.783, energy efficiency 0.743, and ohmic efficiency 0.977.
- Batch 8, 500 mA: conversion and selective yield both zero, selectivity zero, faradaic efficiency 0.0081, transport efficiency 0.0016, energy efficiency zero, and ohmic efficiency 0.910.

Thus low current is slow but efficient, an intermediate cap increases productive throughput, and a very high cap causes catastrophic loss of productive faradaic and transport behavior. A simple monotonic current law is untenable. One possible form is

gI(I) = [I/(KI+I)]·exp[−(I/Ibad)^n],

while the efficiency channels could decrease separately with current or overpotential. With only three caps, the parameters cannot be estimated reliably. The collapse at 500 mA could arise from mass-transfer limitation, electrode passivation, gas evolution, electrolyte breakdown, local concentration changes, or a simulator-level overload regime. No direct observation distinguishes these alternatives.

The UV–visible measurements generally recognized the same operational regimes before the final assay. For example, batch 7 UV–visible estimates were faradaic 0.910 and transport 0.912, whereas batch 8 estimates were zero and 0.0325. This agreement supports a real regime change rather than a single anomalous final-assay channel.

### Material effects and couplings

At +1 V, 100 mA, and 3600 s, the material comparisons were:

- Batch 5, S0/E0: conversion 0.07645, yield 0.0770, selectivity 0.9457, faradaic 0.7936, transport 0.7831, energy 0.7434, score 0.5358, pH-normalized 0.2345, precipitation 0.9869, and risk 0.0722.
- Batch 9, S1/E1: conversion 0.07595, yield 0.0880, selectivity 0.8998, faradaic 0.8260, transport 0.8468, energy 0.9088, score 0.5687, pH-normalized 0.2040, precipitation 0.7300, and risk 0.0956.
- Batch 10, S2/E2: conversion 0.08006, yield 0.0446, selectivity 0.7463, faradaic 0.7026, transport 0.7039, energy 0.7022, score 0.4681, pH-normalized 0.16595, precipitation zero, and risk 0.1136.
- Batch 11, S3/E3: conversion 0.05886, yield 0.0411, selectivity 0.8611, faradaic 0.4890, transport 0.4961, energy 0.7525, score 0.4471, pH-normalized 0.2842, precipitation 0.00524, and risk 0.1262.
- Batch 12, S0/E1: conversion 0.06971, yield 0.09339, selectivity 0.9387, faradaic 0.8891, transport 0.9103, energy 0.9240, score 0.5914, pH-normalized 0.1993, precipitation 0.8552, and risk 0.0722.

The S0/E1 cross-point is particularly informative. Relative to S0/E0, E1 at this condition numerically improved faradaic, transport, and energy efficiencies and selective yield while giving slightly lower conversion. Relative to S1/E1, changing S1 to S0 improved selectivity, yield, faradaic/transport efficiencies, score, and safety. Therefore S0/E1 appears to balance good medium transport with high selectivity, rather than simply maximizing conversion.

However, solvent and electrolyte effects are incompletely identifiable. E2 was observed only with S2, and E3 only with S3, so their individual contributions and interactions cannot be separated. The poor selectivity of S2/E2 and poor faradaic/transport performance of S3/E3 might be caused by the solvent, electrolyte, or their combination. Even S0/E1 versus S1/E1 identifies a solvent effect only within E1; it does not prove that solvent ordering is invariant across electrolytes.

### pH-like and precipitation observables

The pH-normalized signal varied mainly with materials: approximately 0.166 for S2/E2, 0.199–0.204 for E1-containing batches, 0.23 for S0/E0, and 0.284 for S3/E3. This could indicate electrolyte-dependent acid/base balance, ion pairing, or simply a material-specific calibrated response. There was no controlled pH intervention, so pH cannot be assigned a causal role.

Precipitation was nearly saturated in every S0/E0 run, including productive and failed conditions: it was around 0.98–1.00 in batches 1–8. It fell to 0.855 for S0/E1, 0.730 for S1/E1, zero for S2/E2, and 0.005 for S3/E3. Because high precipitation occurred in both batch 6, which produced substantial target, and batch 8, which produced none, precipitation is not a specific target indicator. It is more plausibly a medium-state, salt-solubility, or nonspecific phase signal. A precipitated target remains possible, but the current evidence cannot establish it.

### Efficiencies and proposed causal ordering

A compact causal account consistent with the data is:

1. Potential determines whether the desired electron-transfer channel is accessible and whether strong parasitic channels are activated.
2. Current cap and medium determine actual charge delivery relative to transport capacity.
3. Productive faradaic fraction and transport efficiency jointly set the rate of desired conversion.
4. Selectivity determines how much converted reagent reaches target rather than impurity pathways.
5. Time integrates the productive rate, while depletion or parasitic processes gradually lower efficiency.
6. Solvent/electrolyte also set pH-like state, precipitation, ohmic loss, and safety risk.

One pseudocode representation is:

productive_flux = base_rate × potential_window(V) × current_regime(I,S,E) × transport(S,E,state) × faradaic_fraction(V,I,S,E,state)
conversion += productive_flux × dt × remaining_fraction
side_flux = competing_pathways(V,I,S,E,state)
selectivity = productive_flux / (productive_flux + side_flux)
target_yield ≈ conversion × selectivity

At +2 V or 500 mA, competing pathways or cell failure dominate; at 20 mA, productive flux is small but efficiently utilized; at +1 V and about 100 mA, productive flux is larger while selectivity remains high.

### Scope and limitations

This explanation is supported only at a nominal 0.50 mol L⁻¹ initial loading, volumes near 0.040 L, the tested anonymous materials, potentials of ±1 and ±2 V, current caps of 20, 100, and 500 mA, and durations from 600 to 14400 s. Loading dependence, volume dependence, mixed solvents, intermediate potentials, intermediate current caps, temperature effects, electrode-area effects, delivered current, total charge, and temporal concentration profiles were not measured.

The single-exponential time law is interpolation within one S0/E0 operating regime, not a universal kinetic law. The potential-window and current-penalty functions are qualitative because there are too few levels to determine their shapes. Numerical differences between material batches include both actual effects and assay noise; no replicate batches were performed. Final-assay channel noise is especially consequential near zero, as shown by the low-signal inconsistencies in batches 1 and 2.

### Plausible alternative explanations

Several mechanisms remain consistent with the observations:

- The +1 V optimum may reflect an elementary target redox potential, while +2 V directly degrades target or solvent.
- It may instead reflect an electrode-surface state: insufficient activation at negative potentials, an active surface near +1 V, and passivation at +2 V or high current.
- The 500 mA collapse may be mass-transfer limitation, gas evolution, ohmic heating, passivation, or electrolyte decomposition.
- The declining efficiency with time may be reagent depletion, buildup of an inhibiting product, electrode fouling, or increasing contribution from background electrolysis.
- Material effects may arise from conductivity, viscosity, target solvation, ion pairing, proton activity, precipitation, or hidden interactions; anonymous labels prevent chemical assignment.

The campaign discriminates among operational models—most importantly, it rejects monotonic voltage and current relationships—but it does not identify molecular intermediates or a unique elementary pathway.

### Overall conclusion

The world behaves like a polarity-selective electrochemical conversion with a narrow productive voltage window and a strongly non-monotonic current/transport coupling. At the tested loading, +1 V is productive; −1 V is inefficient, and ±2 V are largely destructive or nonproductive. Near +1 V and 100 mA, conversion grows approximately as a saturating exposure process while selectivity remains around 0.94 in S0-containing media. Low current sacrifices rate for excellent efficiency, whereas 500 mA collapses productive electrochemistry. Material identity changes the efficiency/selectivity balance and the pH/precipitation state, with S0/E1 providing the best demonstrated balanced performance in batch 12 and long-duration S0/E0 in batch 6 providing the highest demonstrated conversion and selective yield. These conclusions are predictive within the sampled operating region but should not be extrapolated as a molecularly unique mechanism or beyond the tested loading and duration without additional evidence.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.68 | 0.48 | 0.82 |
| Q01 | energy_efficiency | 0.32 | 0.18 | 0.47 |
| Q01 | faradaic_efficiency | 0.45 | 0.3 | 0.58 |
| Q01 | score | 0.12 | 0 | 0.31 |
| Q01 | selective_product_yield | 0.007 | 0 | 0.02 |
| Q01 | transport_efficiency | 0.47 | 0.31 | 0.61 |
| Q02 | electrochemical_selectivity | 0.95 | 0.9 | 0.98 |
| Q02 | energy_efficiency | 0.85 | 0.76 | 0.92 |
| Q02 | faradaic_efficiency | 0.86 | 0.78 | 0.93 |
| Q02 | score | 0.36 | 0.1 | 0.56 |
| Q02 | selective_product_yield | 0.013 | 0.003 | 0.032 |
| Q02 | transport_efficiency | 0.84 | 0.74 | 0.91 |
| Q03 | electrochemical_selectivity | 0.68 | 0.45 | 0.84 |
| Q03 | energy_efficiency | 0.29 | 0.13 | 0.45 |
| Q03 | faradaic_efficiency | 0.4 | 0.23 | 0.56 |
| Q03 | score | 0.24 | 0.04 | 0.4 |
| Q03 | selective_product_yield | 0.015 | 0.002 | 0.036 |
| Q03 | transport_efficiency | 0.43 | 0.25 | 0.59 |
| Q04 | electrochemical_selectivity | 0.945 | 0.9 | 0.98 |
| Q04 | energy_efficiency | 0.72 | 0.62 | 0.82 |
| Q04 | faradaic_efficiency | 0.76 | 0.68 | 0.84 |
| Q04 | score | 0.55 | 0.48 | 0.61 |
| Q04 | selective_product_yield | 0.13 | 0.09 | 0.18 |
| Q04 | transport_efficiency | 0.75 | 0.66 | 0.83 |
| Q05 | electrochemical_selectivity | 0.67 | 0.43 | 0.84 |
| Q05 | energy_efficiency | 0.42 | 0.22 | 0.61 |
| Q05 | faradaic_efficiency | 0.48 | 0.28 | 0.66 |
| Q05 | score | 0.29 | 0.05 | 0.46 |
| Q05 | selective_product_yield | 0.016 | 0.002 | 0.041 |
| Q05 | transport_efficiency | 0.52 | 0.31 | 0.7 |
| Q06 | electrochemical_selectivity | 0.94 | 0.89 | 0.98 |
| Q06 | energy_efficiency | 0.9 | 0.8 | 0.97 |
| Q06 | faradaic_efficiency | 0.86 | 0.76 | 0.94 |
| Q06 | score | 0.6 | 0.52 | 0.66 |
| Q06 | selective_product_yield | 0.13 | 0.085 | 0.19 |
| Q06 | transport_efficiency | 0.88 | 0.78 | 0.95 |
| Q07 | electrochemical_selectivity | 0.6 | 0.32 | 0.81 |
| Q07 | energy_efficiency | 0.34 | 0.13 | 0.56 |
| Q07 | faradaic_efficiency | 0.28 | 0.09 | 0.5 |
| Q07 | score | 0.13 | 0.01 | 0.32 |
| Q07 | selective_product_yield | 0.009 | 0 | 0.031 |
| Q07 | transport_efficiency | 0.3 | 0.1 | 0.52 |
| Q08 | electrochemical_selectivity | 0.88 | 0.68 | 0.97 |
| Q08 | energy_efficiency | 0.72 | 0.5 | 0.88 |
| Q08 | faradaic_efficiency | 0.56 | 0.3 | 0.78 |
| Q08 | score | 0.47 | 0.3 | 0.59 |
| Q08 | selective_product_yield | 0.09 | 0.035 | 0.16 |
| Q08 | transport_efficiency | 0.57 | 0.31 | 0.79 |
| Q09 | electrochemical_selectivity | 0.58 | 0.32 | 0.79 |
| Q09 | energy_efficiency | 0.28 | 0.1 | 0.48 |
| Q09 | faradaic_efficiency | 0.36 | 0.16 | 0.56 |
| Q09 | score | 0.15 | 0.01 | 0.34 |
| Q09 | selective_product_yield | 0.01 | 0 | 0.033 |
| Q09 | transport_efficiency | 0.38 | 0.17 | 0.58 |
| Q10 | electrochemical_selectivity | 0.82 | 0.65 | 0.94 |
| Q10 | energy_efficiency | 0.72 | 0.55 | 0.85 |
| Q10 | faradaic_efficiency | 0.74 | 0.58 | 0.86 |
| Q10 | score | 0.5 | 0.37 | 0.59 |
| Q10 | selective_product_yield | 0.105 | 0.05 | 0.17 |
| Q10 | transport_efficiency | 0.74 | 0.57 | 0.86 |
| Q11 | electrochemical_selectivity | 0.12 | 0 | 0.38 |
| Q11 | energy_efficiency | 0.01 | 0 | 0.1 |
| Q11 | faradaic_efficiency | 0.02 | 0 | 0.13 |
| Q11 | score | 0.005 | 0 | 0.06 |
| Q11 | selective_product_yield | 0.001 | 0 | 0.009 |
| Q11 | transport_efficiency | 0.02 | 0 | 0.14 |
| Q12 | electrochemical_selectivity | 0.3 | 0 | 0.65 |
| Q12 | energy_efficiency | 0.05 | 0 | 0.22 |
| Q12 | faradaic_efficiency | 0.08 | 0 | 0.27 |
| Q12 | score | 0.037 | 0 | 0.2 |
| Q12 | selective_product_yield | 0.005 | 0 | 0.025 |
| Q12 | transport_efficiency | 0.08 | 0 | 0.28 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions interpolate the observed narrow productive window near +1 V, the approximately saturating time response at 100 mA, and the severe efficiency collapse at 500 mA. E1 is credited with the efficiency gains observed in S0/E1, while E3 and the unseen S2/E0 combination receive wider intervals because solvent and electrolyte effects were partly confounded. The 0.48 mol/L query loading is treated as close to the studied 0.50 mol/L loading. Score estimates apply the published weighted components and the selective-yield gate; intervals widen sharply near its 0.02 threshold and for negative-potential or previously unseen material combinations.

## K2

### 1. Status of claims and laws

No instance-specific prior mechanism, nominal material-property dossier, or supplied chemical identity was provided. The only initial expectations were therefore self-developed; the anonymous material labels did not encode usable prior chemistry.

- **Supported:** Product formation is polarity-sensitive and has a finite productive potential window. Batch 1 at +1 V retained high selectivity and efficiencies, whereas batch 2 at −1 V was much less efficient and essentially unresolved in conversion. Batches 3 and 4 then changed my judgment from “positive voltage may simply be better” to “the response is peaked”: both +2 and −2 V were largely nonproductive.
- **Supported within a narrow scope:** At S0/E0, +1 V, and 100 mA, conversion increases approximately as a saturating exposure process. Batches 1, 5, and 6 increased from about 0.021 conversion at 600 s to 0.076 at 3600 s and 0.264 at 14400 s, while selectivity stayed near 0.94–0.95. The proposed single-exponential law is only an economical interpolation; the 600 s point was somewhat above the curve defined by batches 5 and 6.
- **Supported:** Current-cap effects are non-monotonic. Batch 7 at 20 mA was slow but efficient, batch 5 at 100 mA produced more conversion, and batch 8 at 500 mA collapsed faradaic and transport efficiency along with product formation. This contradicted any simple law in which productive rate increases monotonically with configured current.
- **Partly supported:** Materials affect transport, energy efficiency, selectivity, and medium state. Batch 12, S0/E1, improved the balanced efficiency profile relative to batch 5, S0/E0. Comparing batches 9 and 12 also supported an S0-versus-S1 effect within E1. However, the separate effects of E2 versus S2 and E3 versus S3 remained unidentifiable because batches 10 and 11 changed solvent and electrolyte together.
- **Contradicted as a simple diagnostic:** Precipitation was not a specific indicator of desired product. It was near unity in both productive S0/E0 batches and failed batch 8, while batches 10 and 11 had almost no precipitation. The pH-normalized signal likewise tracked materials more clearly than product performance.
- **Untested:** Loading dependence, delivered-current or charge laws, the exact optimal potential and current, behavior beyond 14400 s, reversibility of the high-drive failure, molecular intermediates, electrode-state changes, and whether material rankings transfer across all solvent/electrolyte combinations.

The most consequential evidence changes were the +2 V failure in batch 3, which rejected monotonic positive-voltage acceleration; the 500 mA failure in batch 8, which rejected monotonic current acceleration; and batch 12, which showed that E1 could improve balanced efficiency without maximizing conversion.

### 2. One discriminating experiment

I would run the standard batch used in the campaign—0.020 mol reagent in 0.040 L S0 with E0 and a 100 mA cap—but apply +2 V for 600 s, take an intermediate UV–visible measurement, then switch to +1 V for 3600 s before the final assay.

This distinguishes my leading, approximately memoryless “instantaneous potential-window” explanation from an alternative involving persistent electrode passivation, stable inhibitory products, or irreversible medium damage at high potential.

- If the +1 V segment restores faradaic/transport efficiencies and generates roughly the product expected from batch 5, I would favor reversible potential gating: +2 V is nonproductive mainly while it is applied.
- If efficiencies and yield remain close to the collapsed behavior of batch 3 despite the subsequent +1 V segment, I would favor a persistent state change such as passivation or inhibitor formation.
- If the +2 V pretreatment increases subsequent production beyond batch 5, I would revise toward an activation or induction mechanism; batch 3 would then represent insufficient post-activation productive time rather than purely destructive voltage.
- An intermediate result would imply partial recovery or simultaneous irreversible consumption and reversible gating. The experiment would not uniquely distinguish electrode damage from stable solution-phase inhibition, but it would establish whether the system has memory of the high-potential excursion.

### 3. Unused evidence, reliability, and goal effects

The raw UV–visible spectra and final-assay artifacts were not analyzed band-by-band; I used their processed estimates. Cost data were largely irrelevant to the mechanism, and safety-risk differences were used mainly in the operating recommendation rather than the kinetic account. The campaign also lacked direct delivered-current, charge, electrode-state, temperature, or species-resolved time-series evidence. No replicate batches were collected, so process variability could not be separated from instrument noise. Low-signal inconsistencies—especially batch 1 reporting zero selective yield with measurable conversion and batch 2 reporting a small yield with zero conversion—were treated as noisy independent assay channels rather than fitted mechanistic facts.

The least reliable blind predictions are Q03, Q05, Q07, and Q09 because they extrapolate negative-potential behavior from short, sparse source data to 7200 s; Q07 additionally uses the unseen S0/E3 combination and Q09 the unseen S2/E0 combination. Q11 and Q12 are also weak because the 500 mA regime was represented only by batch 8 at +1 V and 3600 s. All predictions at ±0.8 V interpolate a potential curve whose actual width was not identified. Scores for Q01–Q03 and other low-yield cases are particularly uncertain because the published score gate changes rapidly around selective yield 0.02.

The batch-12 recommendation is reasonably supported as the best observed balanced result, but it is a single realization and its superiority over nearby conditions was not replicated. Batch 6 is more defensible if conversion or yield alone is prioritized, although its longer duration and declining efficiency make extrapolation uncertain.

The assigned explanatory and predictive goal materially affected evidence collection. I prioritized polarity, duration, current, and material contrasts rather than repeatedly optimizing the best condition. That produced strong qualitative discrimination but sacrificed replication, a dense search around +1 V and 100 mA, and a complete solvent-by-electrolyte factorial design. I used UV–visible measurements for electrochemical efficiency information rather than spending intermediate measurements on the pH meter. There was no clear conflict with the goal, but a score-only campaign would probably have devoted more batches to local optimization and replication around S0/E1 instead of broad mechanism testing.
