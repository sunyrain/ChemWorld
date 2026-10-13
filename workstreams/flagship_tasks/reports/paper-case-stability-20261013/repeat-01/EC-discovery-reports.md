# EC-discovery — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Experimental scope

All 12 batches used 0.020 mol of limiting reagent in 0.040 L of solvent, corresponding to a nominal initial loading of 0.50 mol L⁻¹. Each batch was configured with a signed potential, a current cap, and an anonymous electrolyte; it was then electrolyzed, measured by UV–visible spectroscopy, terminated, and subjected to a final assay. Consequently, the evidence supports comparisons within this fixed loading and volume, but it does not identify concentration or scale effects.

The strongest overall interpretation is a cathodic potential-window mechanism coupled to charge dose and material-dependent transport/pathway selection. Negative potential enables the productive route, but increasingly negative potential does not monotonically improve it. Electrolysis time and current cap govern conversion through effective delivered charge, while solvent and electrolyte influence transport, precipitation, pH, and the fraction of converted material reaching the desired product.

### 2. Proposed process model

A useful conceptual sequence is:

reactant → electrochemically activated intermediate → target product

with competing branches:

reactant or intermediate → byproducts/degradation/precipitated material.

I would describe the hidden state with the following schematic equations:

- Effective current: `I_eff = min(I_cap, I_kinetic(V,E,S,C), I_transport(E,S,C))`
- Effective charge: `Q_eff = ∫ I_eff dt`
- Conversion: `X ≈ 1 − exp(−k_charge(V,E,S) Q_eff / n0)`
- Productive branching fraction: `f_target = f(V,E,S,pH,precipitation,Q_eff)`
- Selective product amount: `P ∝ X × f_target`, with possible additional assay-specific scaling or independent response channels.
- Faradaic efficiency reflects productive electron use; transport efficiency reflects delivery of electroactive material or ions to the interface; ohmic efficiency reflects resistive loss; energy efficiency combines these effects with the potential penalty.

These equations are explanatory rather than fitted laws. Delivered current was not observed, so `Q_eff` cannot be calculated directly from the current cap and duration. In particular, the cap should not be mistaken for a measured constant current.

### 3. Signed potential and the productive window

Batches 1–3 established that the sign and magnitude of potential are mechanistically decisive. They all used S0/E0, a 100 mA cap, and 1800 s:

- Batch 1 at +1.5 V had final conversion 0.0080, selectivity 0.0103, zero reported selective yield, faradaic efficiency 0.0245, transport efficiency 0, energy efficiency 0.0053, and score 0.
- Batch 2 at −1.5 V had conversion 0.0066, selectivity 0.5601, selective yield 0.0170, faradaic efficiency 0.3136, transport efficiency 0.3398, energy efficiency 0.1074, and score 0.2183.
- Batch 3 at −2.5 V had conversion 0.0038, selectivity 0.4259, zero reported selective yield, faradaic efficiency 0.1724, transport efficiency 0.1889, energy efficiency 0.0306, and score 0.

Thus, simply increasing |V| cannot explain the system. Reversing +1.5 V to −1.5 V caused a large change in selectivity and electrochemical efficiencies, even though measured conversion remained small. Driving farther negative to −2.5 V then reduced the useful response. My interpretation is that the desired electron-transfer step is cathodic, but excessive cathodic overpotential favors an unproductive interfacial reaction, worsens energetic cost, or moves the surface away from the potential range where the desired intermediate is selectively formed.

Batch 12 later refined the location of the favorable window. On S3/E2 at 7200 s and a 100 mA cap, −1.0 V produced conversion 0.0412, selectivity 0.5008, selective yield 0.0409, faradaic efficiency 0.2749, transport efficiency 0.2961, energy efficiency 0.2754, and the best score, 0.2738. The corresponding −1.5 V condition in batch 10 gave higher conversion, 0.0614, but lower selective yield, 0.0189, and energy efficiency, 0.1497. This suggests that −1.5 V accelerates total substrate consumption relative to −1.0 V, while −1.0 V better preserves productive branching and energy efficiency. The optimum is therefore a compromise between reaction rate and pathway selectivity, plausibly near −1.0 to −1.5 V under S3/E2 conditions.

This comparison is not a clean potential-only replicate because there was only one run at each setting, but all specified preparation variables were otherwise matched.

### 4. Electrolysis time and current cap

Batches 9–11 clarify the charge-dose contribution under S3/E2 at −1.5 V:

- Batch 9: 100 mA cap, 1800 s; conversion 0.0096, selectivity 0.4538, yield 0.0226, score 0.2352.
- Batch 10: 100 mA cap, 7200 s; conversion 0.0614, selectivity 0.4820, yield 0.0189, score 0.2266.
- Batch 11: 20 mA cap, 7200 s; conversion 0.0225, selectivity 0.4514, yield 0.0058, score 0.0659.

Extending time fourfold at the 100 mA cap increased conversion by roughly sixfold in these individual observations, although selective yield did not increase. Lowering the current cap from 100 to 20 mA at 7200 s reduced conversion from 0.0614 to 0.0225 and yield from 0.0189 to 0.0058. Therefore both time and current availability matter, and the 20 mA cap restricted productive progress.

The failure of selective yield to track conversion monotonically is important. Longer or stronger electrolysis appears able to consume more reactant without proportionately accumulating the desired product. Possible causes include parallel byproduct formation, secondary transformation of the product, depletion of a favorable interfacial state, or response noise. This is consistent with a conversion-versus-selectivity tradeoff rather than a single first-order conversion law.

A saturating dose model is consequently more plausible than a linear one. At low effective charge, conversion should rise with `I_eff × t`. At higher dose, reactant depletion, transport limitation, or competing chemistry should progressively reduce marginal productive yield. The tested data do not locate the saturation point precisely.

### 5. Electrolyte effects

Batches 2, 4, 5, and 6 compared E0–E3 at fixed S0, −1.5 V, 100 mA, and 1800 s:

- E0, batch 2: conversion 0.0066, yield 0.0170, faradaic efficiency 0.3136, pH-normalized value 0.2295, precipitation signal 1.000.
- E1, batch 4: conversion 0.0102, yield 0.0084, faradaic efficiency 0.3280, pH 0.1991, precipitation 0.8491.
- E2, batch 5: conversion 0.0164, yield 0.0152, faradaic efficiency 0.2881, pH 0.1564, precipitation 0.
- E3, batch 6: conversion 0.0150, yield 0.0171, faradaic efficiency 0.2997, pH 0.2748, precipitation 0.0024.

E2 and E3 produced numerically greater conversion than E0/E1 and nearly eliminated the strong precipitation signal. The electrolyte also shifted the normalized pH substantially. These coupled changes suggest that electrolyte identity affects more than bulk conductivity: it may modify acid/base balance, ion pairing, interfacial stabilization, solubility, or mass transport. E2 was selected for subsequent solvent and dose experiments because it combined relatively high conversion with negligible precipitation.

The electrolyte ranking is not definitive. E1 had the largest measured faradaic efficiency in this screen despite lower conversion and appreciable precipitation, and E3 had the highest energy efficiency of the four (0.1379). Each category was observed only once, so exact differences may contain assay noise.

### 6. Solvent effects

Batches 5 and 7–9 compared solvents with E2 at −1.5 V, 100 mA, and 1800 s:

- S0, batch 5: conversion 0.0164, selectivity 0.5302, yield 0.0152, energy efficiency 0.1181, score 0.1859, safety risk 0.0722.
- S1, batch 7: conversion 0.0221, selectivity 0.4964, yield 0.0131, energy efficiency 0.1456, score 0.1566, risk 0.0956.
- S2, batch 8: conversion 0.0055, selectivity 0.4089, zero reported yield, energy efficiency 0.1148, score 0, risk 0.1136.
- S3, batch 9: conversion 0.0096, selectivity 0.4538, yield 0.0226, energy efficiency 0.1665, score 0.2352, risk 0.1262.

The solvent giving the most conversion was not the one giving the most target yield. S1 had the largest conversion, whereas S3 gave the largest reported yield, energy efficiency, and score in this short-duration screen. S2 was unfavorable across several metrics. This again supports separate control of total conversion and productive branching.

A plausible solvent role is to change reactant/intermediate solvation, electrode double-layer organization, viscosity or diffusivity, and product stability. Since the solvent labels are anonymous, these microscopic properties are not identifiable. S3 also increased reported safety risk relative to S0. That risk remained below the stated limit of 0.65, but it is a real operating tradeoff rather than a mechanistic benefit.

### 7. Efficiency coupling and precipitation

Ohmic efficiency was consistently high, approximately 0.965–1.000 in the productive negative-potential batches. By contrast, faradaic and transport efficiencies varied much more and were essentially absent at the wrong polarity. This pattern argues against gross solution resistance as the dominant limitation. The larger limitations appear to be transport to the active interface and competition between productive and unproductive electron-transfer pathways.

Precipitation was strongly associated with the S0/E0 and S0/E1 conditions: batches 1–3 had signals near 0.987–1.000, and batch 4 had 0.849. E2/E3 conditions generally had signals near zero. However, precipitation cannot be claimed as the sole cause of poor performance. Batch 2 had precipitation 1.000 yet respectable selectivity and score, while several precipitation-free batches differed considerably in yield. I therefore treat precipitation as an electrolyte-dependent state marker or secondary loss channel, not a sufficient predictor of success.

Normalized pH also changed mainly with electrolyte identity and stayed near 0.156–0.166 through the later E2/S1–S3 series. Because no direct acid/base perturbation was performed, pH may be a correlated consequence of electrolyte choice rather than the causal control variable.

### 8. How the explanation changed during the campaign

The initial hypothesis was that charge dose would increase conversion and that excessive electrolysis might harm selectivity. Batch 1 immediately showed that polarity was indispensable; current and time alone could not explain an inactive +1.5 V run. Batch 2 established the productive negative polarity. Batch 3 rejected a monotonic dependence on voltage magnitude and motivated the potential-window model.

Batches 4–6 then showed that electrolyte choice coupled conversion to pH and precipitation, leading to adoption of E2 as a low-precipitation baseline. Batches 7–9 separated solvent effects from electrolyte effects and showed that maximum conversion was not equivalent to maximum target yield; S3 was retained because its yield/efficiency balance was best despite higher risk.

Batches 10 and 11 confirmed that time and current cap affect conversion, while revealing that additional conversion does not guarantee additional desired product. Finally, batch 12 showed that moving from −1.5 to −1.0 V could sacrifice some conversion but substantially improve measured yield and energy efficiency. That result sharpened the account from “negative potential plus charge” to “negative potential window plus dose-dependent pathway competition.”

### 9. Measurement limitations and unidentifiable factors

The final-assay channels should not be forced into exact identities such as `yield = conversion × selectivity`. Several observations violate that simple equality—for example, batch 2 reported conversion 0.0066 but yield 0.0170, and batch 9 reported conversion 0.0096 but yield 0.0226. These channels may use different synthetic calibrations, bases, or independent noisy estimators. I therefore use their trends as separate observables rather than imposing a mass-action identity that the public data do not support.

Likewise, UV–visible and final-assay efficiency estimates sometimes differed. This may reflect instrument noise, calibration differences, or latent process variability; no physical change occurred during the instantaneous measurements according to the instrument contract. The final assay is the primary endpoint, while UV–visible results provide supporting rather than interchangeable estimates.

Unidentifiable quantities include delivered current, electrode area, charge-transfer coefficient, formal potential, number of electrons, diffusion coefficients, interfacial concentrations, actual chemical identities, side-product identities, and any electrode conditioning between runs. None should be invented from the anonymous labels. There were no replicated final conditions, so run-to-run variability cannot be separated cleanly from treatment effects. Later optimization also used S3/E2, creating partial material-by-potential and material-by-time confounding.

### 10. Plausible alternatives

One alternative is that the potential response reflects a narrow activation threshold followed by direct product degradation at stronger negative potential, rather than competition at a common intermediate. Another is electrode passivation: +1.5 or −2.5 V might form an inactive surface, while E2/S3 suppresses film formation. A third is that precipitation removes either reagent or an electrolyte component and indirectly changes interfacial transport. A fourth is that the current cap changes temperature or another unobserved state rather than charge alone, although the public observations do not establish such a pathway. The present factorial contrasts cannot distinguish these mechanisms.

### 11. Predictions and boundaries

Within the tested 0.50 M loading, I expect negative potentials between approximately −1.0 and −1.5 V to outperform positive potential and −2.5 V. Increasing duration or cap should generally increase conversion when charge-limited, but target yield should display a flatter or peaked response because the productive fraction falls or saturates. E2/E3-like electrolyte behavior should suppress precipitation relative to E0/E1-like behavior, and S3/E2 should favor the best observed yield/energy balance while carrying higher safety risk than S0.

These are interpolations within the tested domain. Predictions at different reagent concentration, solvent volume, potentials outside ±2.5 V, durations beyond 7200 s, or different material identities are unsupported extrapolations. The data do not establish that batch 12 is a global optimum—only that its S3/E2, −1.0 V, 100 mA-cap, 7200 s condition was the best observed endpoint, with yield 0.0409 and score 0.2738.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.54 | 0.39 | 0.68 |
| Q01 | energy_efficiency | 0.19 | 0.08 | 0.31 |
| Q01 | faradaic_efficiency | 0.31 | 0.21 | 0.41 |
| Q01 | score | 0.11 | 0 | 0.25 |
| Q01 | selective_product_yield | 0.008 | 0 | 0.023 |
| Q01 | transport_efficiency | 0.33 | 0.22 | 0.44 |
| Q02 | electrochemical_selectivity | 0.018 | 0 | 0.065 |
| Q02 | energy_efficiency | 0.008 | 0 | 0.036 |
| Q02 | faradaic_efficiency | 0.02 | 0 | 0.063 |
| Q02 | score | 0.006 | 0 | 0.04 |
| Q02 | selective_product_yield | 0.0015 | 0 | 0.009 |
| Q02 | transport_efficiency | 0.008 | 0 | 0.055 |
| Q03 | electrochemical_selectivity | 0.56 | 0.43 | 0.68 |
| Q03 | energy_efficiency | 0.24 | 0.13 | 0.35 |
| Q03 | faradaic_efficiency | 0.32 | 0.23 | 0.41 |
| Q03 | score | 0.284 | 0.18 | 0.39 |
| Q03 | selective_product_yield | 0.033 | 0.012 | 0.061 |
| Q03 | transport_efficiency | 0.34 | 0.24 | 0.44 |
| Q04 | electrochemical_selectivity | 0.022 | 0 | 0.078 |
| Q04 | energy_efficiency | 0.01 | 0 | 0.044 |
| Q04 | faradaic_efficiency | 0.022 | 0 | 0.071 |
| Q04 | score | 0.01 | 0 | 0.052 |
| Q04 | selective_product_yield | 0.0025 | 0 | 0.012 |
| Q04 | transport_efficiency | 0.012 | 0 | 0.064 |
| Q05 | electrochemical_selectivity | 0.52 | 0.38 | 0.65 |
| Q05 | energy_efficiency | 0.23 | 0.12 | 0.34 |
| Q05 | faradaic_efficiency | 0.33 | 0.23 | 0.43 |
| Q05 | score | 0.273 | 0.14 | 0.38 |
| Q05 | selective_product_yield | 0.027 | 0.007 | 0.053 |
| Q05 | transport_efficiency | 0.3 | 0.2 | 0.4 |
| Q06 | electrochemical_selectivity | 0.02 | 0 | 0.076 |
| Q06 | energy_efficiency | 0.009 | 0 | 0.042 |
| Q06 | faradaic_efficiency | 0.025 | 0 | 0.076 |
| Q06 | score | 0.009 | 0 | 0.052 |
| Q06 | selective_product_yield | 0.0022 | 0 | 0.012 |
| Q06 | transport_efficiency | 0.011 | 0 | 0.064 |
| Q07 | electrochemical_selectivity | 0.54 | 0.4 | 0.67 |
| Q07 | energy_efficiency | 0.27 | 0.15 | 0.39 |
| Q07 | faradaic_efficiency | 0.3 | 0.2 | 0.4 |
| Q07 | score | 0.281 | 0.17 | 0.4 |
| Q07 | selective_product_yield | 0.038 | 0.012 | 0.069 |
| Q07 | transport_efficiency | 0.28 | 0.18 | 0.39 |
| Q08 | electrochemical_selectivity | 0.021 | 0 | 0.08 |
| Q08 | energy_efficiency | 0.012 | 0 | 0.049 |
| Q08 | faradaic_efficiency | 0.023 | 0 | 0.074 |
| Q08 | score | 0.01 | 0 | 0.055 |
| Q08 | selective_product_yield | 0.0024 | 0 | 0.013 |
| Q08 | transport_efficiency | 0.012 | 0 | 0.066 |
| Q09 | electrochemical_selectivity | 0.44 | 0.28 | 0.59 |
| Q09 | energy_efficiency | 0.18 | 0.07 | 0.3 |
| Q09 | faradaic_efficiency | 0.25 | 0.15 | 0.36 |
| Q09 | score | 0.141 | 0.03 | 0.31 |
| Q09 | selective_product_yield | 0.012 | 0 | 0.039 |
| Q09 | transport_efficiency | 0.27 | 0.16 | 0.38 |
| Q10 | electrochemical_selectivity | 0.014 | 0 | 0.062 |
| Q10 | energy_efficiency | 0.007 | 0 | 0.037 |
| Q10 | faradaic_efficiency | 0.016 | 0 | 0.061 |
| Q10 | score | 0.005 | 0 | 0.039 |
| Q10 | selective_product_yield | 0.0013 | 0 | 0.009 |
| Q10 | transport_efficiency | 0.008 | 0 | 0.056 |
| Q11 | electrochemical_selectivity | 0.54 | 0.38 | 0.67 |
| Q11 | energy_efficiency | 0.24 | 0.11 | 0.36 |
| Q11 | faradaic_efficiency | 0.29 | 0.18 | 0.4 |
| Q11 | score | 0.292 | 0.17 | 0.41 |
| Q11 | selective_product_yield | 0.05 | 0.015 | 0.086 |
| Q11 | transport_efficiency | 0.34 | 0.22 | 0.46 |
| Q12 | electrochemical_selectivity | 0.016 | 0 | 0.069 |
| Q12 | energy_efficiency | 0.006 | 0 | 0.037 |
| Q12 | faradaic_efficiency | 0.015 | 0 | 0.061 |
| Q12 | score | 0.004 | 0 | 0.043 |
| Q12 | selective_product_yield | 0.0011 | 0 | 0.01 |
| Q12 | transport_efficiency | 0.007 | 0 | 0.058 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions apply the campaign’s cathodic potential-window and effective-charge account at the nearly matched 0.48 M loading. Negative −0.8 V is interpolated from the productive −1.0/−1.5 V region; longer electrolysis raises conversion and expected yield, while 500 mA may help but is likely partly potential/transport limited. Positive +0.8 V is predicted to remain largely unproductive based on the sharp polarity contrast. Electrolyte and solvent adjustments follow the observed categorical trends, with especially broad intervals because these conditions were unreplicated, ±0.8 V was not directly tested, and reported yield channels were noisy and not algebraically identical to conversion×selectivity. Score estimates incorporate the published weighted components and the selective-yield gate; intervals also cover uncertainty in unrequested conversion and ohmic-efficiency channels.

## K2

1. **Claims and changes in judgment**

No instance-specific prior mechanism, parameter set, or expected result was supplied. The only supplied information was the public workflow, instrument, and scoring contracts; the mechanistic claims were self-developed.

- **Supported:** Productive chemistry requires negative rather than positive potential. Batch 1 at +1.5 V had zero reported selective yield, selectivity 0.0103, and faradaic efficiency 0.0245. Under otherwise matched conditions, batch 2 at −1.5 V had yield 0.0170, selectivity 0.5601, and faradaic efficiency 0.3136. This polarity comparison caused the largest change in my account.
- **Supported:** Performance has a potential window rather than increasing with |V|. Batch 3 at −2.5 V was worse than batch 2 at −1.5 V: yield fell to zero, with lower selectivity and electrochemical efficiencies. Later, batch 12 at −1.0 V outperformed the matched long-duration −1.5 V batch 10 in yield, energy efficiency, and score, despite having lower conversion. This shifted the explanation toward a rate–selectivity compromise near −1.0 to −1.5 V.
- **Supported qualitatively:** Effective charge depends on both duration and current cap. At S3/E2 and −1.5 V, extending electrolysis from 1800 s in batch 9 to 7200 s in batch 10 increased conversion from 0.0096 to 0.0614. At 7200 s, reducing the cap from 100 mA in batch 10 to 20 mA in batch 11 reduced conversion to 0.0225 and yield to 0.0058. This contradicted a simple claim that the current setting was irrelevant, but delivered current was never measured, so linear charge scaling remains unsupported.
- **Supported qualitatively:** Solvent and electrolyte affect more than gross resistance. Electrolyte changes in batches 2 and 4–6 altered conversion, normalized pH, and precipitation, while ohmic efficiency remained near unity. E2/E3 nearly suppressed the precipitation seen with E0/E1. Solvent changes in batches 5 and 7–9 changed yield and efficiency; S1 gave the highest conversion in that screen, whereas S3 gave the highest yield and score. These observations supported separate controls over total conversion and productive branching.
- **Contradicted:** A simple monotonic model in which greater conversion necessarily produces greater selective yield. Batch 10 converted much more material than batch 9 but had slightly lower measured yield. Batch 12 also produced less conversion than batch 10 but much higher yield. Likewise, an exact law `yield = conversion × selectivity` was contradicted by the reported channels themselves—for example, batch 2 reported conversion 0.0066 and yield 0.0170.
- **Untested or unresolved:** Saturation kinetics, formal charge balance, product degradation, electrode passivation, and the microscopic causes of electrolyte/solvent effects were not identified. Concentration dependence was untested because every campaign batch used 0.020 mol in 0.040 L. Material interactions were incompletely mapped, and none of the main conditions was replicated.

2. **One additional discriminating experiment**

I would run one S3/E2 batch at the established loading and 100 mA cap using an alternating potential sequence: −1.0 V for 900 s, UV–visible measurement; −1.5 V for 900 s, measurement; −1.0 V for another 900 s, measurement; then terminate and obtain the final assay. The measurements would be interpreted mainly through transport, faradaic, and energy-efficiency changes rather than through absolute UV–visible yield.

The leading explanation is potential-dependent pathway competition: −1.5 V accelerates overall reaction but sends a greater fraction through unproductive chemistry, while −1.0 V is more product-selective. A plausible alternative is reversible electrode passivation or interfacial inhibition at −1.5 V.

- If the second −1.0 V segment recovered approximately the high transport/faradaic response of the first −1.0 V segment, while the intervening −1.5 V segment showed greater progress but poorer efficiency, I would favor reversible potential-dependent interfacial/pathway selection.
- If performance remained depressed after returning to −1.0 V, I would increase belief in irreversible passivation, reagent/intermediate depletion, or product damage caused during the −1.5 V segment.
- If all three segments behaved similarly within measurement uncertainty, the apparent batch-10 versus batch-12 potential effect would look less reproducible, and I would weaken the potential-window claim.

This crossover would still be imperfect because composition changes over time and sequence cannot be separated completely from potential. A replicated two-arm comparison would be stronger, but it would require more than one additional batch.

3. **Unused evidence, reliability, and goal effects**

The raw UV–visible spectra and final-assay artifacts were not inspected or quantitatively fitted; only processed estimates were used. Most intermediate UV–visible results were used as qualitative consistency checks rather than incorporated into a joint calibration model. Cost was not mechanistically modeled. Safety risk influenced the discussion of S3 but not the mechanism fit. Temperature changes, raw baselines, spectral assignments, mass-balance fields, and explicit uncertainty packets were also unused. Normalized pH and precipitation were observed and discussed, but no direct perturbation established either as causal.

The operating recommendation, batch 12, is less reliable than its rank suggests because it was a single observation and its apparent advantage was concentrated in yield and energy efficiency. Although batch 10 was a useful matched comparison, neither condition was replicated. The recommendation is therefore best understood as the best observed condition, not a demonstrated optimum.

The least reliable blind predictions are Q11 and Q12 because the 500 mA cap was far outside the tested 20–100 mA range. Q01 and Q02 are also weak because 600 s and ±0.8 V were not directly tested. Q05–Q10 combine potential, material, duration, and loading settings not observed together, so their categorical adjustments rely on partial factor transfer. The sign prediction—negative potential outperforming positive potential—is more secure than the exact numerical values, especially near zero where assay clipping and the selective-yield score gate matter.

The assigned goal emphasized explanatory discovery rather than score optimization. That encouraged polarity, potential, electrolyte, solvent, time, and cap contrasts, producing broader mechanistic evidence than repeated local optimization would have. The cost was limited replication and incomplete response-surface coverage, which reduced confidence in exact effect sizes and the final ranking. There was no clear conflict with the goal, but evidence breadth was favored over precision.
