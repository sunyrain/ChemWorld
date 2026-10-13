# EC-optimization — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic interpretation

### 1. Scope and evidential basis

This report describes the bounded synthetic electrochemical world explored in 12 completed batches. The solvent and electrolyte labels are anonymous benchmark identities, so statements about S0–S3 and E0–E3 are empirical within this world and are not claims about real chemical substances.

Except for batch 1, every batch used 0.020 mol limiting reagent in 0.050 L solvent, one constant potential/current-cap setting, and one uninterrupted electrolysis period. Consequently, the campaign identifies useful operating relationships but cannot uniquely identify molecular intermediates, electrode kinetics, stoichiometric electron count, mass-transfer coefficients, or causal solvent properties. Most settings received only one final assay, so differences should not be treated as replicated effects.

### 2. Public objective

Above the selective-product-yield gate of 0.02, the reported score is consistent with the weighted sum

S = 0.30Y + 0.15Sel + 0.10X + 0.15E + 0.12FE + 0.10TE + 0.08OE,

where Y is selective product yield, Sel electrochemical selectivity, X conversion, E energy efficiency, FE faradaic efficiency, TE transport efficiency, and OE ohmic efficiency. Selective yield therefore dominates the objective, but conversion bought through inefficient or unselective electrolysis can be counterproductive. Batch 1 had measured yield 0 and consequently score 0 despite several nonzero efficiency estimates, illustrating the gate.

### 3. Polarity and productive electrochemistry

The reaction is cathodic in the explored sign convention. In batch 1, S0/E0 was first held at +1.2 V and a 100 mA cap for 1800 s. The intervening UV–vis measurement reported energy, faradaic, and transport efficiencies as zero, with only ohmic efficiency near 0.995. Switching that same vessel to −1.2 V for another 1800 s produced only a weak final response: conversion 0.0258, selectivity 0.599, faradaic efficiency 0.204, transport efficiency 0.176, and measured yield 0. Because both polarities were applied sequentially, the final assay cannot isolate the negative segment quantitatively, but the intermediate measurement strongly indicates that the positive segment was nonproductive.

All subsequent productive batches used negative potentials. I therefore infer a cathodic activation step, schematically

R + n e− → I → P,

competing with unproductive electron transfer, side-product formation, or loss of intermediate I. The identities of R, I, P, and any proton donor are unobservable and should not be inferred from the anonymous labels.

### 4. Charge delivery, potential, and the current cap

A useful qualitative process model is

Icell(t) = min[Icap, Ikinetic(V, medium, composition), Itransport(t)],

dξ/dt ≈ FE(V, medium, ξ) Icell/(nF),

X = f(ξ), and Y ≈ X × chemical selectivity, subject to losses and assay noise.

The configured current is a ceiling, not evidence that the cell always operated at that current. Electrolysis cost also changed with potential and cap, consistent with different realized current or energy draw.

Duration was clearly important. With S0/E1 at −1.8 V and a 300 mA cap, extending electrolysis from 7200 s in batch 6 to 14400 s in batch 9 increased conversion from 0.152 to 0.298 and selective yield from 0.0876 to 0.1718. The score rose from 0.2724 to 0.3155. Selectivity remained approximately stable within the resolution of single assays (0.519 versus 0.506). Thus this region was substantially charge-limited at 7200 s rather than already at a severe degradation plateau.

Potential magnitude showed a nonmonotonic efficiency tradeoff. At 14400 s and a 300 mA cap, changing from −1.8 V in batch 9 to −1.4 V in batch 10 increased conversion from 0.298 to 0.375, selectivity from 0.506 to 0.583, selective yield from 0.172 to 0.200, energy efficiency from 0.133 to 0.186, faradaic efficiency from 0.259 to 0.330, and score from 0.3155 to 0.3605. The less negative setting was therefore better, not merely cheaper. A plausible explanation is that −1.8 V drives more parasitic reduction or incurs excess overpotential, decreasing the fraction of energy and charge directed to target formation.

The current cap was also consequential. Batches 10 and 11 differed only in the cap, 300 versus 500 mA, at −1.4 V for 14400 s. Raising the cap increased conversion from 0.375 to 0.626, selective yield from 0.200 to 0.351, transport efficiency from 0.331 to 0.338, and score from 0.3605 to 0.4270. Selectivity changed from 0.583 to 0.561, while ohmic efficiency decreased from 0.936 to 0.915. This pattern suggests that the 300 mA ceiling constrained productive charge throughput. The higher cap accelerated conversion but imposed modest selectivity and ohmic penalties.

At the 500 mA cap, reducing the potential magnitude again—from −1.4 V in batch 11 to −1.2 V in batch 12—improved the complete balance. Batch 12 gave conversion 0.6534, selectivity 0.5789, selective yield 0.4104, energy efficiency 0.2282, faradaic efficiency 0.3249, transport efficiency 0.3462, ohmic efficiency 0.9135, and score 0.4562. Batch 11 gave 0.6256, 0.5614, 0.3505, 0.1902, 0.3304, 0.3375, 0.9148, and 0.4270, respectively. Faradaic and ohmic efficiencies were essentially similar relative to their assay uncertainties, but the yield and energy-efficiency gains favored −1.2 V.

I interpret these results as an operating window in which decreasing |V| suppresses parasitic pathways and improves energy utilization, while the high current ceiling still permits substantial charge delivery. This does not establish that −1.2 V is the true optimum: the optimum may lie at a still less-negative potential, or a time-varying potential may be superior.

### 5. Medium and electrolyte effects

The first four-pair screen was confounded because solvent and electrolyte changed together. At −1.8 V, 300 mA, and 7200 s, the observed results were:

- Batch 2, S0/E0: score 0.2424, conversion 0.106, selectivity 0.529, yield 0.0683.
- Batch 3, S1/E1: score 0.2403, conversion 0.131, selectivity 0.479, yield 0.0565.
- Batch 4, S2/E2: score 0.2089, conversion 0.112, selectivity 0.369, yield 0.0468.
- Batch 5, S3/E3: score 0.2023, conversion 0.0751, selectivity 0.474, yield 0.0420.

This established that S2/E2 and S3/E3 were relatively weak combinations, but it did not show whether solvent or electrolyte caused the differences.

Batches 2, 6, 7, and 8 isolated electrolyte identity in S0 under the same electrical program:

- E0, batch 2: score 0.2424, conversion 0.106, yield 0.0683, FE 0.204, TE 0.230.
- E1, batch 6: score 0.2724, conversion 0.152, yield 0.0876, FE 0.292, TE 0.267.
- E2, batch 7: score 0.2617, conversion 0.150, yield 0.0765, FE 0.251, TE 0.254.
- E3, batch 8: score 0.2225, conversion 0.0968, yield 0.0296, FE 0.190, TE 0.183.

E1 was the best observed electrolyte in S0, with E2 a plausible but slightly inferior alternative. E1 improved both charge utilization and transport rather than only shifting selectivity. A generic explanation is that electrolyte identity changes conductivity, interfacial charge transfer, ion pairing, and reactant delivery to the electrode. Those mechanisms are plausible but not separately identifiable from the measurements.

Solvent effects remain poorly isolated. Only S0 received a full electrolyte comparison; S1–S3 were each tested with a single matching electrolyte. It is therefore unsupported to claim that S0 is intrinsically the best solvent independently of electrolyte. The recommendation properly concerns the tested S0/E1 combination.

### 6. Coupled efficiency losses

The observations suggest several coupled loss channels:

1. **Activation loss:** At the tested positive polarity, essentially no productive electrochemical response was detected. A sufficiently negative potential is needed to enter the productive regime.
2. **Parasitic faradaic loss:** FE was only about 0.14–0.33 in final assays, indicating that much of the effective charge proxy was not assigned to target formation. More negative potential did not improve FE and sometimes worsened overall performance.
3. **Transport limitation:** TE rose from roughly 0.18–0.28 in the lower-throughput screen to 0.338–0.346 in the high-cap batches. E1 performed well on this measure. Transport and conversion therefore appear coupled to electrolyte and current ceiling.
4. **Ohmic loss:** OE remained high, approximately 0.91–0.99, but declined modestly at high throughput. This is consistent with a tradeoff in which increased current delivers more productive charge while incurring greater resistive loss.
5. **Energy loss:** Energy efficiency improved as the successful operating point moved from −1.8 toward −1.2 V. This supports excess-overpotential loss at more negative settings.
6. **Chemical selectivity loss:** Selectivity was typically 0.47–0.60 rather than near unity. It did not collapse at the largest observed conversion, so target loss was not overwhelmingly conversion-driven over the tested range, but secondary chemistry remains plausible.

A compact phenomenological representation would be

rP = kP(V,S,E) C_R gtransport(Icap,E,S),
rside = kside(V,S,E) C_R + kdeg(V,S,E) C_P,
FE ≈ nF rP/Icell,
Sel ≈ rP/(rP+rside),
Eeff ≈ useful chemical output/(|V| Icell),

with heating/resistance lowering OE as realized current rises. The data support the directions of these relationships but do not provide enough independent points to estimate the functions or rate constants.

### 7. pH and precipitation signals

Final pH-normalized values varied with medium: approximately 0.15–0.29 across the campaign. In the optimized S0/E1 sequence they were stable near 0.198–0.200 in batches 6, 9, 10, 11, and 12. That stability suggests the large electrical-performance changes among batches 9–12 were not driven by a gross pH shift detectable by this channel.

Precipitation signal was high for S0/E0 and S0/E1 (often about 0.85–1.0), near zero for S0/E2 and S0/E3, and medium-dependent in the paired screen. Because high precipitation coexisted with both poor batch 1 and strong batch 12 performance, it is not by itself a sufficient cause of high yield. It may represent formation or separation of target, an electrolyte salt response, or an unrelated solid phase. No solid was independently isolated or identified, so all such interpretations remain alternatives.

### 8. How the explanation changed during the campaign

The initial expectation was an interior optimum in potential and time plus strong medium effects. Batch 1 established the productive polarity and caused abandonment of positive-potential exploration. Batches 2–5 revealed meaningful medium dependence but also exposed the solvent/electrolyte confound. Batches 6–8 isolated electrolyte effects and selected E1 in S0. Batch 9 showed that the 7200 s screen was charge-limited. Batch 10 overturned any simple belief that stronger negative potential must improve conversion: −1.4 V outperformed −1.8 V across the main score components. Batch 11 demonstrated that the current ceiling constrained the −1.4 V process. Batch 12 then showed that −1.2 V with the larger cap gave the best observed balance.

Thus the final account is not simply “more voltage and current produce more product.” It is “provide sufficient cathodic driving force and charge throughput, but avoid unnecessary overpotential; use a medium that supports productive charge transfer and transport.”

### 9. Recommended procedure and interpretation

The sealed recommendation is batch 12:

- limiting reagent: 0.020 mol;
- solvent: 0.050 L S0;
- electrolyte profile: E1;
- potential: −1.2 V;
- current magnitude cap: 500 mA;
- electrolysis duration: 14400 s;
- then terminate and assay.

Its observed score was 0.4562 at safety risk 0.0593, well below the public limit of 0.65. It was selected because it had the campaign’s highest score and highest measured selective product yield, not because its molecular mechanism is known.

### 10. Limits, unidentifiable factors, and alternatives

- No condition was replicated, so process variability and final-assay noise cannot be separated from small treatment effects. The batch 12 versus batch 11 advantage is supported by coordinated changes, especially yield, but still needs replication.
- Potential and current were configured values; actual current-time traces were not observed. Delivered charge and current density are therefore unknown.
- Electrode area, electrode material, mixing, temperature trajectory, and cell geometry were not public observables. Any of them could be embedded in the synthetic response.
- The electron stoichiometry n is unknown, so conversion cannot be converted into a physical coulomb balance.
- Solvent effects were not factorially resolved. E1 could interact specifically with S0 rather than being universally superior.
- The high precipitation signal could describe target precipitation, electrolyte precipitation, or a correlated proxy. It cannot be assigned mechanistically.
- The apparent potential optimum remains open. A setting less negative than −1.2 V might improve energy efficiency and selectivity while retaining enough current; alternatively, conversion might fall sharply near a cathodic threshold.
- A staged program—initially −1.4 V to establish throughput, followed by −1.2 V to preserve selectivity—or feedback control using current/UV–vis information could outperform every constant-potential batch. This is conjecture, not an observed result.
- Longer than 14400 s might raise conversion, but extrapolation is risky because substrate depletion, product degradation, selectivity loss, and increasing resistive limitation could produce a plateau or decline.

Overall, the most defensible world model is a cathodically activated conversion governed jointly by delivered charge, overpotential-dependent parasitic chemistry, electrolyte-dependent interfacial/transport efficiency, and modest ohmic loss. The experiments locate a favorable tested region at S0/E1, −1.2 V, a 500 mA cap, and 14400 s, while leaving the exact kinetic law and global optimum unidentified.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.64 | 0.5 | 0.76 |
| Q01 | energy_efficiency | 0.16 | 0.05 | 0.28 |
| Q01 | faradaic_efficiency | 0.21 | 0.1 | 0.32 |
| Q01 | score | 0 | 0 | 0.03 |
| Q01 | selective_product_yield | 0.004 | 0 | 0.018 |
| Q01 | transport_efficiency | 0.14 | 0.05 | 0.24 |
| Q02 | electrochemical_selectivity | 0.62 | 0.39 | 0.78 |
| Q02 | energy_efficiency | 0 | 0 | 0.05 |
| Q02 | faradaic_efficiency | 0 | 0 | 0.035 |
| Q02 | score | 0 | 0 | 0.02 |
| Q02 | selective_product_yield | 0 | 0 | 0.014 |
| Q02 | transport_efficiency | 0 | 0 | 0.045 |
| Q03 | electrochemical_selectivity | 0.64 | 0.53 | 0.74 |
| Q03 | energy_efficiency | 0.23 | 0.12 | 0.35 |
| Q03 | faradaic_efficiency | 0.25 | 0.16 | 0.35 |
| Q03 | score | 0.278 | 0.21 | 0.345 |
| Q03 | selective_product_yield | 0.052 | 0.018 | 0.1 |
| Q03 | transport_efficiency | 0.2 | 0.11 | 0.29 |
| Q04 | electrochemical_selectivity | 0.62 | 0.39 | 0.78 |
| Q04 | energy_efficiency | 0 | 0 | 0.05 |
| Q04 | faradaic_efficiency | 0 | 0 | 0.035 |
| Q04 | score | 0 | 0 | 0.02 |
| Q04 | selective_product_yield | 0 | 0 | 0.014 |
| Q04 | transport_efficiency | 0 | 0 | 0.045 |
| Q05 | electrochemical_selectivity | 0.63 | 0.52 | 0.73 |
| Q05 | energy_efficiency | 0.27 | 0.15 | 0.39 |
| Q05 | faradaic_efficiency | 0.32 | 0.22 | 0.42 |
| Q05 | score | 0.314 | 0.245 | 0.385 |
| Q05 | selective_product_yield | 0.08 | 0.035 | 0.14 |
| Q05 | transport_efficiency | 0.24 | 0.15 | 0.34 |
| Q06 | electrochemical_selectivity | 0.61 | 0.38 | 0.78 |
| Q06 | energy_efficiency | 0 | 0 | 0.055 |
| Q06 | faradaic_efficiency | 0 | 0 | 0.04 |
| Q06 | score | 0 | 0 | 0.02 |
| Q06 | selective_product_yield | 0 | 0 | 0.014 |
| Q06 | transport_efficiency | 0 | 0 | 0.05 |
| Q07 | electrochemical_selectivity | 0.59 | 0.46 | 0.71 |
| Q07 | energy_efficiency | 0.17 | 0.07 | 0.29 |
| Q07 | faradaic_efficiency | 0.18 | 0.09 | 0.28 |
| Q07 | score | 0.24 | 0 | 0.31 |
| Q07 | selective_product_yield | 0.03 | 0.004 | 0.07 |
| Q07 | transport_efficiency | 0.15 | 0.07 | 0.24 |
| Q08 | electrochemical_selectivity | 0.57 | 0.34 | 0.75 |
| Q08 | energy_efficiency | 0 | 0 | 0.05 |
| Q08 | faradaic_efficiency | 0 | 0 | 0.035 |
| Q08 | score | 0 | 0 | 0.02 |
| Q08 | selective_product_yield | 0 | 0 | 0.014 |
| Q08 | transport_efficiency | 0 | 0 | 0.045 |
| Q09 | electrochemical_selectivity | 0.49 | 0.36 | 0.62 |
| Q09 | energy_efficiency | 0.17 | 0.06 | 0.29 |
| Q09 | faradaic_efficiency | 0.2 | 0.1 | 0.3 |
| Q09 | score | 0.234 | 0.16 | 0.305 |
| Q09 | selective_product_yield | 0.04 | 0.008 | 0.085 |
| Q09 | transport_efficiency | 0.16 | 0.07 | 0.26 |
| Q10 | electrochemical_selectivity | 0.47 | 0.27 | 0.67 |
| Q10 | energy_efficiency | 0 | 0 | 0.05 |
| Q10 | faradaic_efficiency | 0 | 0 | 0.035 |
| Q10 | score | 0 | 0 | 0.02 |
| Q10 | selective_product_yield | 0 | 0 | 0.014 |
| Q10 | transport_efficiency | 0 | 0 | 0.045 |
| Q11 | electrochemical_selectivity | 0.64 | 0.53 | 0.74 |
| Q11 | energy_efficiency | 0.34 | 0.21 | 0.47 |
| Q11 | faradaic_efficiency | 0.28 | 0.19 | 0.38 |
| Q11 | score | 0.395 | 0.31 | 0.48 |
| Q11 | selective_product_yield | 0.24 | 0.13 | 0.36 |
| Q11 | transport_efficiency | 0.31 | 0.21 | 0.41 |
| Q12 | electrochemical_selectivity | 0.62 | 0.38 | 0.79 |
| Q12 | energy_efficiency | 0 | 0 | 0.06 |
| Q12 | faradaic_efficiency | 0 | 0 | 0.04 |
| Q12 | score | 0 | 0 | 0.02 |
| Q12 | selective_product_yield | 0 | 0 | 0.015 |
| Q12 | transport_efficiency | 0 | 0 | 0.05 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The campaign indicated a polarity gate: negative potentials were productive, while the tested positive segment produced essentially zero faradaic, transport, and energy response. For negative-potential queries I scaled charge throughput by duration, current cap, and the smaller reagent inventory, allowed lower overpotential to improve selectivity and energy efficiency, and applied the observed electrolyte ordering E1 > E0 > E3. Q11 is highest because its 500 mA cap should deliver substantially more charge; the 600 s case is expected to remain below the selective-yield score gate. Intervals are widened for extrapolation from −1.2 V to −0.8 V, unreplicated medium effects, unknown realized current, and final-assay/process uncertainty.

## K2

### 1. Status of claims and laws

No instance-specific prior, nominal property dossier, or supplied mechanistic law was provided. The only supplied quantitative law relevant here was the public score contract: a weighted combination dominated by selective product yield, with a 0.02 yield gate. The observed scores were consistent with that contract; batch 1 had zero reported yield and zero score despite nonzero values for several other components.

**Supported self-developed claims:**

- **Negative polarity is required in the explored sign convention.** In batch 1, the UV–vis measurement after +1.2 V reported zero energy, faradaic, and transport efficiencies. Product-related signals appeared only after the vessel was subsequently operated at −1.2 V. All productive independent batches used negative potential. Because batch 1 mixed both polarities before its final assay, this supports a polarity gate but does not quantify the negative segment cleanly.
- **Electrolysis was charge/time limited at 7200 s.** With S0/E1, −1.8 V, and a 300 mA cap, extending time from 7200 s in batch 6 to 14400 s in batch 9 increased conversion from 0.152 to 0.298, yield from 0.0876 to 0.1718, and score from 0.2724 to 0.3155.
- **The 300 mA cap constrained the −1.4 V process.** Raising it to 500 mA between batches 10 and 11 increased conversion from 0.375 to 0.626 and yield from 0.200 to 0.351, while score increased from 0.3605 to 0.4270. The modest declines in selectivity and ohmic efficiency are consistent with a throughput/loss tradeoff.
- **Excess negative potential was detrimental over the tested high-charge region.** At 300 mA and 14400 s, batch 10 at −1.4 V outperformed batch 9 at −1.8 V in conversion, selectivity, yield, energy efficiency, faradaic efficiency, and score. At 500 mA, batch 12 at −1.2 V also outperformed batch 11 at −1.4 V, with scores 0.4562 versus 0.4270. This supported the proposed coupling between overpotential, parasitic reactions, and energy loss.
- **Electrolyte identity affects productive charge use and transport.** In S0 at the same −1.8 V/300 mA/7200 s program, E1 in batch 6 gave score 0.2724, compared with E0 at 0.2424 in batch 2, E2 at 0.2617 in batch 7, and E3 at 0.2225 in batch 8. E1 also had the best observed combination of yield, faradaic efficiency, and transport efficiency.

**Contradicted or narrowed claims:**

- Any simple law that “more negative potential produces more conversion or a better score” was contradicted by batches 9–10 and 11–12. Less-negative potentials performed better in both comparisons.
- The initial paired-material screen did not establish S0/E0 as uniquely best. Batch 2 and batch 3 had nearly equal scores, 0.2424 and 0.2403, and the comparison changed solvent and electrolyte simultaneously. Later electrolyte-isolation batches shifted the preferred formulation to S0/E1.
- A simple proportional-charge law is inadequate. Changing the current ceiling from 300 to 500 mA produced a large response, but potential changes also altered conversion and efficiency in directions that cannot be explained by nominal charge alone.

**Untested or unresolved claims:**

- An interior potential optimum was not bracketed. Performance improved through the least-negative productive condition tested, −1.2 V, so the optimum could lie at −1.2 V, at a less-negative value, or near an activation threshold.
- Product degradation at long times was not demonstrated; no duration beyond 14400 s was tested.
- A staged potential program was not tested.
- Solvent effects were not separated factorially from electrolyte effects outside S0.
- The precipitation signal was not identified as product, electrolyte, or an unrelated solid phase.
- Actual current, transferred charge, electron stoichiometry, and molecular intermediates remained unobserved.

The evidence that most changed the interpretation was the zero-response positive segment in batch 1, the E1 advantage isolated in batch 6, the duration comparison between batches 6 and 9, the unexpected superiority of −1.4 V over −1.8 V in batches 9–10, and the strong cap effect in batches 10–11.

### 2. Best additional discriminating experiment

I would run one new S0/E1 batch with 0.020 mol reagent in 0.050 L solvent, a 500 mA cap, −1.0 V, and 14400 s, followed by the final assay. This interpolates between the recommended −1.2 V condition and the untested low-overpotential region while holding the other important variables fixed.

The leading explanation is that −1.8 and −1.4 V incur avoidable overpotential-dependent losses, while a high current ceiling permits productive throughput at a less-negative potential. The principal alternative is that −1.2 V is already close to a cathodic activation threshold and its superiority over −1.4 V partly reflects assay/process variation rather than a continuing potential trend.

- If −1.0 V retained conversion near batch 12 while increasing selectivity or energy efficiency and produced a score above 0.456, I would strengthen the excess-overpotential explanation and move the recommended potential toward −1.0 V.
- If conversion and yield fell sharply while energy efficiency rose only modestly, I would infer a kinetic/onset threshold between −1.0 and −1.2 V and retain batch 12 as the best supported operating point.
- If all major metrics were statistically compatible with batch 12, I would regard the optimum as a broad plateau and prefer −1.0 V for lower driving force only after replication.
- If −1.0 V unexpectedly increased conversion but reduced selectivity enough to lower score, I would revise the model toward potential-dependent competition among multiple productive and side pathways rather than a simple activation-versus-overpotential tradeoff.

A replicate of batch 12 would be better for estimating repeatability, but the proposed −1.0 V experiment has greater ability to distinguish the two leading mechanistic explanations.

### 3. Unused evidence, reliability, and goal effects

Substantial public evidence was not used fully. The raw final-assay and UV–vis artifacts were not inspected beyond their processed summaries, so peak shapes, baselines, and channel-level consistency did not influence the model. Intermediate UV–vis results were mainly used qualitatively. The pH-normalized and precipitation channels were recorded but did not drive optimization; their chemical assignments were unidentifiable. Cost, temperature changes, sample consumption, and detailed spectral peak coordinates were also not modeled. Actual current-time traces and delivered charge were unavailable rather than merely unused.

The least reliable predictions are those for the new ±0.8 V batches because −0.8 V was outside the tested negative-potential range and +0.8 V was never tested in an independent final-assay batch. Selectivity is especially ill-defined near zero conversion, making the positive-polarity selectivity predictions weak. Q01 is sensitive to the discontinuous yield gate, Q09 combines S2 with E0 even though that pair was never observed, and Q11 extrapolates the large high-current benefit to a less-negative potential where the 500 mA cap may not be reached. The prediction intervals attempted to reflect these limitations.

The batch 12 recommendation is reliable as the **best observed** procedure but less reliable as a global optimum. It was not replicated, the potential optimum was not bracketed, solvent S0 was not fully compared with other solvents under E1, and no time beyond 14400 s was studied.

The assigned goal did affect evidence collection. Maximizing the public score encouraged adaptive exploitation after E1 and the high-current region appeared promising. This produced useful local optimization in batches 9–12 but sacrificed replication, a complete solvent-by-electrolyte factorial design, independent positive-polarity controls, and detailed duration/potential response curves. The early paired-material screen also confounded solvent and electrolyte. There was no direct conflict between the goal and mechanism learning, but the score-maximization objective clearly favored finding a strong operating point over resolving every causal factor.
