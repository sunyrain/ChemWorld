# EC-optimization — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic interpretation

I interpret this benchmark as a charge-driven electrochemical conversion with four coupled layers: (1) charge delivery and ohmic behavior, (2) transport through the solvent/electrolyte medium, (3) competition between productive and parasitic electron-transfer pathways, and (4) time-dependent destruction or further reaction of product at excessive exposure. The experiments support a narrow productive operating window rather than a rule that more voltage or more charge is always beneficial.

All quantitative statements below are observations from the completed campaign unless explicitly labeled as inference or conjecture. The tested standard loading was 0.020 mol reagent in 0.040 L solvent, nominally 0.50 mol/L before sampling. The configured current was a cap/setpoint; actual current or total coulombs passed were not publicly measured, so Faraday-law calculations cannot be treated as measured charge balances.

## 1. Potential polarity and productive voltage window

The polarity comparison was clearest between batches 1 and 2. Both used S0/E0, 100 mA, and 3600 s. At +1.0 V, batch 1 produced conversion 0.0810, selectivity 0.9496, selective yield 0.0545, and score 0.5356. At -1.0 V, batch 2 gave conversion 0.0286, selectivity 0.6256, selective yield 0.0315, and score 0.3095. Thus positive polarization is the productive direction in this tested formulation. The negative direction was not completely inert, but it had poorer conversion, selectivity, Faradaic efficiency (0.3927 versus 0.8071), transport efficiency (0.4190 versus 0.7784), and energy efficiency (0.2405 versus 0.7765).

Stronger positive polarization was not beneficial. Batches 3–6 used +1.5 V, 200 mA, and 7200 s with S0 and E1, E2, E3, or E0, respectively. All were essentially unproductive. Batch 6, the most direct comparison because it retained E0, had conversion 0.00215, selectivity 0.00424, selective yield 0.01034, energy and transport efficiencies reported as zero, and score 0.0437. Batches 3–5 scored 0, 0.0032, and 0.0351. This strongly suggests that the productive chemistry has a bounded potential window near +1.0 V and that +1.5 V activates parasitic or destructive pathways.

A plausible kinetic representation is

r_target = k_target(S,E,V) C_R,
r_side = k_side(S,E,V) C_R + k_deg(S,E,V) C_P,

dC_R/dt = -(r_target + r_side),
dC_P/dt = r_target - k_deg C_P.

My inference is that k_target becomes appreciable around +1.0 V, whereas one or both of k_side and k_deg rise steeply before +1.5 V. A Butler–Volmer-like voltage dependence could underlie the initial activation, but a single monotonic Butler–Volmer term cannot explain the loss of product at stronger drive without parallel chemistry, transport failure, or product degradation.

The +1.5 V experiments also used twice the current setting and twice the duration of the initial +1.0 V runs. Consequently, the exact voltage threshold is not identifiable: the collapse could depend on potential, accumulated exposure, current density, or their interaction. Nevertheless, batch 6 shows that E0 itself does not rescue the +1.5 V condition, and the later duration series at +1.0 V shows that 7200–14400 s can be productive. These comparisons make excessive potential, rather than duration alone, the leading explanation for batches 3–6.

## 2. Solvent-mediated transport and selectivity

Batches 1, 7, 8, and 9 form a clean solvent comparison because they all used E0, +1.0 V, 100 mA, 3600 s, 0.020 mol reagent, and 0.040 L solvent.

- Batch 1, S0: conversion 0.0810, selectivity 0.9496, selective yield 0.0545, Faradaic efficiency 0.8071, transport efficiency 0.7784, energy efficiency 0.7765, score 0.5356.
- Batch 7, S1: conversion 0.0892, selectivity 0.9531, selective yield 0.0827, Faradaic efficiency 0.8480, transport efficiency 0.8514, energy efficiency 0.9284, score 0.5828.
- Batch 8, S2: conversion 0.0626, selectivity 0.7442, selective yield 0.0299, Faradaic efficiency 0.7331, transport efficiency 0.7266, energy efficiency 0.7208, score 0.4743.
- Batch 9, S3: conversion 0.0493, selectivity 0.8303, selective yield 0.0602, Faradaic efficiency 0.5398, transport efficiency 0.5606, energy efficiency 0.6363, score 0.4438.

S1 therefore appears to improve several coupled functions simultaneously: productive conversion, selectivity, charge utilization, transport, and energy efficiency. Its advantage is not attributable solely to ohmic efficiency, because all four runs had high assay ohmic efficiencies (approximately 0.984–1.000). I infer that S1 improves interfacial mass transport or the relative stability/reactivity of the productive intermediate more than it changes bulk resistance.

A useful factorization is

productive yield ≈ conversion × chemical selectivity × collection/recovery factor,

overall energy efficiency ≈ ohmic efficiency × transport efficiency × Faradaic/chemical factor.

The reported numbers do not obey these identities exactly, which is expected because the channels are separately calibrated noisy synthetic observables. Nevertheless, the factorization describes the qualitative coupling: high ohmic efficiency alone was insufficient, while high transport and Faradaic efficiencies accompanied every good S1 run.

## 3. Electrolyte profile

E0 is the only electrolyte demonstrated to work in the productive +1.0 V region. E1–E3 were tested only at the harsh +1.5 V, 200 mA, 7200 s condition in batches 3–5. Their near-zero responses do not establish that they are intrinsically poor at +1.0 V, because the E0 control at the same harsh setting, batch 6, also failed.

The electrolyte screening is therefore partially unidentifiable. The defensible conclusion is operational: E0 is supported in the productive window; no positive evidence supports E1–E3. A plausible alternative is that one of E1–E3 would outperform E0 at +1.0 V, but the campaign did not test that combination. Claims that E0 is universally optimal would exceed the evidence.

## 4. Duration, charge exposure, and over-electrolysis

The strongest mechanistic evidence came from the S1/E0 duration series at +1.0 V and 100 mA:

- Batch 7, 3600 s: conversion 0.0892, selectivity 0.9531, selective yield 0.0827, score 0.5828.
- Batch 10, 7200 s: conversion 0.1732, selectivity 0.9743, selective yield 0.1483, score 0.6145.
- Batch 11, 14400 s: conversion 0.3290, selectivity 0.9467, selective yield 0.3031, score 0.6723.
- Batch 12, 28800 s delivered as two 14400 s segments: conversion 0.1776, selectivity 0.9095, selective yield 0.1898, score 0.5056.

From 3600 to 14400 s, conversion rose approximately in proportion to time but with mild sublinearity: doubling 3600 to 7200 s increased conversion from 0.089 to 0.173, and doubling again to 14400 s increased it to 0.329. Selectivity remained around 0.95, while final-assay energy, Faradaic, and transport efficiencies remained high. This is consistent with productive charge accumulation over that interval.

The 28800 s result changed the explanation. If conversion were merely approaching a saturation plateau, it should not fall from 0.329 to 0.178. Instead, the lower conversion signal, lower selectivity, and pronounced efficiency collapse indicate over-electrolysis, reactant/product destruction, electrode or medium deterioration, or another history-dependent process. Final energy, Faradaic, and transport efficiencies in batch 12 were 0.6112, 0.5528, and 0.5740, compared with 0.9414, 0.8480, and 0.8552 in batch 11. Ohmic efficiency remained high (0.9879), arguing against simple bulk-resistance failure.

A minimal empirical model capable of this behavior is sequential formation and destruction:

R --k1(V,S,E)--> P --k2(V,S,E)--> D,

possibly with a parallel reactant loss R --k3--> D. For constant effective rates,

P(t) = [k1 R0/(k2-k1)] [exp(-k1 t) - exp(-k2 t)]

for the simplest first-order sequential scheme. This naturally creates an interior maximum in product. I do not claim the elementary kinetics are first order; the equation is a compact representation of the observed rise and subsequent fall.

Batch 12 included an intervening UV–visible measurement after its first 14400 s segment. At that point, UV–visible estimates remained strong: energy efficiency 0.8953, Faradaic efficiency 0.8879, transport efficiency 0.8908, and ohmic efficiency 0.9651. After the second segment, the final assay showed the collapse. This temporal contrast supports deterioration during the extra exposure. However, batch 12 was segmented whereas batch 11 was continuous, and the small UV–visible sample was removed between segments. Segmentation, restart history, or measurement perturbation are plausible confounders, although the tiny sample volume makes sample removal alone an unlikely explanation for the large change.

The best sampled exposure was therefore 14400 s, not necessarily the exact mathematical optimum. The true optimum could lie anywhere between the tested 7200 and 28800 s points, plausibly near but not exactly at 14400 s.

## 5. pH, precipitation, and safety

The productive E0/S0 and E0/S1 assays had normalized pH values near 0.23. In the S1 duration series, pH_normalized was remarkably stable: 0.2342, 0.2322, 0.2332, and 0.2337 for batches 7, 10, 11, and 12. Thus the duration optimum was not accompanied by a large observable bulk-pH shift.

Precipitation signals were also near unity in the productive S0/S1 runs: 1.000 in batch 1 and approximately 0.978–0.996 in batches 7, 10, 11, and 12. Because precipitation remained high in both good and degraded runs, it is not by itself diagnostic of product yield. It may indicate a persistent phase behavior or public proxy unrelated to the rate-limiting loss. The chemical identity of the precipitating material is hidden, so assigning it to product would be unjustified.

All observed safety risks were below the published limit of 0.65. At the common 0.040 L loading, risks were about 0.0722 for S0, 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3. S1 therefore trades a modestly higher risk than S0 for better performance, but remains far below the limit in the tested configuration. Risk did not grow with electrolysis duration in the public observations, suggesting it was dominated by setup/material choice rather than accumulated electrochemical exposure in this benchmark.

## 6. Relationship to the balanced score

The public score weights selective product yield most heavily, followed by selectivity and energy efficiency, with smaller contributions from conversion, Faradaic, transport, and ohmic efficiencies. This explains why batch 11 won: it retained approximately the same strong efficiency profile as batches 7 and 10 while raising selective yield to 0.3031. Conversely, the +1.5 V batches retained high ohmic efficiency but lost nearly every chemistry-sensitive component, so their scores were low.

The selective-yield gate also makes extremely low-yield conditions especially unattractive. Thus optimizing voltage or time solely for ohmic efficiency would be mechanistically and statistically misguided. The appropriate operating objective is to maximize productive charge utilization before degradation becomes important.

## 7. Resulting process picture

My working process model is:

1. Reagent and medium establish a solvent/electrolyte-dependent interfacial environment.
2. Positive polarization near +1.0 V enables productive electron transfer.
3. S1/E0 gives the best tested combination of transport, Faradaic utilization, and target-path selectivity.
4. Product accumulates with exposure through at least 14400 s.
5. Excess voltage or prolonged exposure activates parasitic conversion and/or product destruction. These losses primarily appear in Faradaic, transport, conversion, and selectivity channels while ohmic efficiency can remain high.
6. The observed score is therefore maximized at an interior point in voltage–time space.

In pseudocode:

productive_drive = activation(V, polarity) * solvent_factor[S] * electrolyte_factor[E]
side_drive = high_voltage_penalty(V) + long_exposure_penalty(V,t,state)
formation = productive_drive * available_reactant
loss = side_drive * (available_reactant + product)
product += formation*dt - loss_product*dt
score = weighted_assay_components(product, conversion, selectivity,
                                    faradaic, transport, ohmic, energy)

Here, high_voltage_penalty is small near +1.0 V but large by +1.5 V under the tested conditions, and long_exposure_penalty becomes important somewhere between 14400 and 28800 s for S1/E0.

## 8. Scope and unresolved alternatives

This explanation is restricted to the campaign domain. Only one reagent amount, approximate concentration, volume, and current range around the selected condition were systematically used. There were no replicate batches, so assay noise and run-to-run variability cannot be separated from small effects. The final-assay standard deviations were roughly 0.01 for conversion and selective yield, 0.012 for selectivity and Faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Large contrasts—such as batch 11 versus the +1.5 V failures or batch 11 versus batch 12—are much larger than these nominal uncertainties, but fine ranking near the optimum would require replication.

Important unidentifiable factors include actual current history, electron stoichiometry, electrode area, temperature evolution, concentrations of intermediates, whether product and reactant signals share calibration biases, and the identities of the solvent, electrolyte, precipitate, byproducts, and degradation products. The current setting could be a limiting cap rather than delivered current, so current × time is not a measured charge dose. No mechanistic assignment to real chemical species is warranted because the materials are anonymous benchmark labels.

Plausible alternatives to the sequential-degradation interpretation include electrode passivation followed by reduced productive conversion; depletion of an unobserved cofactor or electrolyte component; phase separation that hides material from the final conversion channel; a restart-dependent state change in segmented batch 12; or a nonlinear instrument/process-state interaction. The persistent high ohmic efficiency makes catastrophic resistance growth less likely, but does not rule out surface passivation or selective blockage. Distinguishing these alternatives would require measurements that were not performed.

Overall, the most evidence-supported account is a polarity-specific, solvent-assisted productive pathway around +1.0 V, opposed by high-field and long-exposure side processes. Batch 11—S1/E0, 0.020 mol reagent in 0.040 L, +1.0 V, 100 mA setting, and 14400 s—best balanced formation against destruction and was therefore the sealed recommendation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.55 | 0.25 | 0.8 |
| Q01 | energy_efficiency | 0.3 | 0.15 | 0.45 |
| Q01 | faradaic_efficiency | 0.36 | 0.2 | 0.52 |
| Q01 | score | 0.04 | 0 | 0.18 |
| Q01 | selective_product_yield | 0.0025 | 0 | 0.012 |
| Q01 | transport_efficiency | 0.4 | 0.23 | 0.58 |
| Q02 | electrochemical_selectivity | 0.94 | 0.84 | 0.99 |
| Q02 | energy_efficiency | 0.82 | 0.68 | 0.93 |
| Q02 | faradaic_efficiency | 0.78 | 0.65 | 0.89 |
| Q02 | score | 0.36 | 0.12 | 0.55 |
| Q02 | selective_product_yield | 0.014 | 0.004 | 0.032 |
| Q02 | transport_efficiency | 0.74 | 0.58 | 0.87 |
| Q03 | electrochemical_selectivity | 0.67 | 0.48 | 0.82 |
| Q03 | energy_efficiency | 0.29 | 0.16 | 0.43 |
| Q03 | faradaic_efficiency | 0.39 | 0.25 | 0.54 |
| Q03 | score | 0.333 | 0.25 | 0.42 |
| Q03 | selective_product_yield | 0.05 | 0.025 | 0.085 |
| Q03 | transport_efficiency | 0.42 | 0.27 | 0.58 |
| Q04 | electrochemical_selectivity | 0.95 | 0.89 | 0.99 |
| Q04 | energy_efficiency | 0.86 | 0.74 | 0.95 |
| Q04 | faradaic_efficiency | 0.8 | 0.69 | 0.9 |
| Q04 | score | 0.582 | 0.53 | 0.64 |
| Q04 | selective_product_yield | 0.14 | 0.1 | 0.2 |
| Q04 | transport_efficiency | 0.78 | 0.65 | 0.89 |
| Q05 | electrochemical_selectivity | 0.58 | 0.25 | 0.82 |
| Q05 | energy_efficiency | 0.24 | 0.05 | 0.48 |
| Q05 | faradaic_efficiency | 0.32 | 0.08 | 0.57 |
| Q05 | score | 0.287 | 0.12 | 0.42 |
| Q05 | selective_product_yield | 0.035 | 0.008 | 0.09 |
| Q05 | transport_efficiency | 0.32 | 0.07 | 0.6 |
| Q06 | electrochemical_selectivity | 0.82 | 0.55 | 0.95 |
| Q06 | energy_efficiency | 0.68 | 0.38 | 0.88 |
| Q06 | faradaic_efficiency | 0.62 | 0.32 | 0.82 |
| Q06 | score | 0.48 | 0.32 | 0.59 |
| Q06 | selective_product_yield | 0.1 | 0.035 | 0.2 |
| Q06 | transport_efficiency | 0.6 | 0.3 | 0.82 |
| Q07 | electrochemical_selectivity | 0.6 | 0.27 | 0.84 |
| Q07 | energy_efficiency | 0.25 | 0.06 | 0.49 |
| Q07 | faradaic_efficiency | 0.34 | 0.09 | 0.59 |
| Q07 | score | 0.3 | 0.13 | 0.44 |
| Q07 | selective_product_yield | 0.04 | 0.009 | 0.1 |
| Q07 | transport_efficiency | 0.35 | 0.08 | 0.62 |
| Q08 | electrochemical_selectivity | 0.85 | 0.58 | 0.96 |
| Q08 | energy_efficiency | 0.7 | 0.4 | 0.9 |
| Q08 | faradaic_efficiency | 0.65 | 0.34 | 0.85 |
| Q08 | score | 0.5 | 0.34 | 0.61 |
| Q08 | selective_product_yield | 0.105 | 0.038 | 0.21 |
| Q08 | transport_efficiency | 0.63 | 0.32 | 0.84 |
| Q09 | electrochemical_selectivity | 0.53 | 0.31 | 0.73 |
| Q09 | energy_efficiency | 0.25 | 0.11 | 0.41 |
| Q09 | faradaic_efficiency | 0.34 | 0.18 | 0.5 |
| Q09 | score | 0.28 | 0.18 | 0.38 |
| Q09 | selective_product_yield | 0.032 | 0.012 | 0.065 |
| Q09 | transport_efficiency | 0.36 | 0.19 | 0.54 |
| Q10 | electrochemical_selectivity | 0.76 | 0.61 | 0.88 |
| Q10 | energy_efficiency | 0.7 | 0.55 | 0.83 |
| Q10 | faradaic_efficiency | 0.7 | 0.56 | 0.82 |
| Q10 | score | 0.486 | 0.4 | 0.56 |
| Q10 | selective_product_yield | 0.075 | 0.04 | 0.125 |
| Q10 | transport_efficiency | 0.7 | 0.54 | 0.83 |
| Q11 | electrochemical_selectivity | 0.45 | 0.18 | 0.7 |
| Q11 | energy_efficiency | 0.15 | 0.02 | 0.36 |
| Q11 | faradaic_efficiency | 0.22 | 0.03 | 0.46 |
| Q11 | score | 0.25 | 0.1 | 0.43 |
| Q11 | selective_product_yield | 0.045 | 0.006 | 0.14 |
| Q11 | transport_efficiency | 0.32 | 0.09 | 0.58 |
| Q12 | electrochemical_selectivity | 0.8 | 0.59 | 0.92 |
| Q12 | energy_efficiency | 0.48 | 0.25 | 0.7 |
| Q12 | faradaic_efficiency | 0.48 | 0.24 | 0.7 |
| Q12 | score | 0.5 | 0.38 | 0.61 |
| Q12 | selective_product_yield | 0.24 | 0.1 | 0.42 |
| Q12 | transport_efficiency | 0.68 | 0.45 | 0.84 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions extrapolate the observed polarity advantage near positive potential, the productive but bounded voltage–time window, and the S0/S2 efficiency contrast. Charge exposure was scaled for the lower reagent amount, with the 600 s cases treated as yield-limited and therefore strongly affected by the score’s yield gate. Intervals combine assay noise with larger model uncertainty for electrolyte profiles E1/E3 and the untested 500 mA regime; high-current estimates allow both increased conversion and over-electrolysis losses.

## K2

1. **Status of claims and laws.** No instance-specific prior or nominal property dossier was supplied; only anonymous material identifiers and the public scoring/instrument contracts were available. My initial self-developed expectation of an interior voltage–exposure optimum was supported. Batch 1 (+1.0 V, S0/E0, 3600 s) scored 0.5356, while the otherwise matched negative-polarity batch 2 scored 0.3095, establishing the productive polarity. Batches 3–6 then contradicted any simple law that stronger positive potential, current, or charge exposure must improve conversion: all +1.5 V conditions were nearly unproductive, including the E0 control in batch 6, which scored 0.0437. The clean solvent comparison in batches 1 and 7–9 supported a medium effect, with S1 giving the best common-condition score (0.5828 in batch 7). The duration series supported productive accumulation from 3600 to 14400 s: batches 7, 10, and 11 increased in score from 0.5828 to 0.6145 to 0.6723. Batch 12 contradicted monotonic improvement with duration; extending exposure to 28800 s reduced the score to 0.5056 and substantially lowered Faradaic, transport, and energy efficiencies. That result changed my judgment from simple accumulation toward an interior optimum involving degradation, parasitic chemistry, or history-dependent electrode behavior. Untested claims include whether E0 is intrinsically superior to E1–E3 at +1.0 V, the exact optimum between tested durations, concentration and loading laws, current scaling, reaction order, electron stoichiometry, and whether the loss in batch 12 was chemical product destruction rather than passivation or a segmented-run artifact.

2. **One additional discriminating experiment.** I would replicate the S1/E0, +1.0 V, 100 mA, nominal 28800 s condition of batch 12 using two required 14400 s electrolysis segments but omit the intervening UV–visible measurement, then perform only the terminal assay. This directly tests the leading over-exposure explanation against the alternative that the batch-12 collapse arose from intermediate sampling, restart history, or an anomalous run. A second low-yield, low-efficiency result resembling batch 12 would strongly support a real exposure-dependent loss. If ohmic efficiency remained high while Faradaic and transport efficiencies fell, I would favor parasitic chemistry, product destruction, or selective surface poisoning over simple bulk-resistance growth. A pronounced ohmic-efficiency decline would instead strengthen electrode passivation or conductivity-loss explanations. If the replicate retained or exceeded batch 11’s conversion, selective yield, and efficiency, I would withdraw the claimed 14400–28800 s degradation trend and treat batch 12 as a sampling/segmentation or stochastic anomaly. An intermediate outcome would leave the optimum location unresolved and motivate replicated time-course experiments rather than a single mechanistic assignment.

3. **Unused evidence, reliability, and goal effects.** Most raw spectral traces and individual peak shapes were unused; decisions relied primarily on calibrated processed estimates. Cost was recorded but was not an objective component, and safety risk was used mainly as a constraint because every tested batch remained well below 0.65. The stable normalized-pH and precipitation signals were considered but were weakly diagnostic and did not drive optimization. No pH-meter measurements were taken, and intermediate UV–visible data were used mainly for qualitative viability checks rather than fitted quantitatively. There were also no replicates, so small differences cannot be separated cleanly from process and assay noise.

The least reliable blind predictions are Q05–Q08, because E1 and E3 were never tested in the productive +0.8 to +1.0 V region, and Q11–Q12, because 500 mA was outside the empirically isolated regime and could alter charge delivery, heating, passivation, or degradation. Q01–Q02 are also uncertain because very small yields interact strongly with the score’s multiplicative yield gate. The sealed recommendation of batch 11 is reliable as the highest observed batch, but less reliable as the exact global optimum: it was unreplicated, the surrounding potential–duration surface was sparse, and E1–E3 were not evaluated under its voltage.

The maximization goal did affect evidence collection. It encouraged transition from broad screening to exploitation after S1/E0 emerged, producing a useful duration series but leaving electrolyte identity, current, concentration, and fine potential effects underexplored. It also favored spending every batch on a final assay rather than replication. There was no clear conflict with safety because observed risks were comfortably below the limit, but the optimization emphasis reduced mechanistic identifiability and made several factor effects confounded.
