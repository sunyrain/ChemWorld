# EC-discovery — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanism report

1. Experimental scope

The campaign comprised 12 completed batches. Every batch used 0.020 mol of limiting reagent in 0.040 L of solvent. Unless otherwise stated, the electrical program was +1.0 V, a 100 mA current cap, electrolyte E0, and 1,800 s total electrolysis. Solvent, electrolyte, potential, current cap, or duration was varied one at a time. Consequently, the evidence supports comparisons within this fixed loading and volume, but it does not identify concentration or reagent-loading effects. Each condition was run once, so repeatability and batch variance remain unmeasured.

2. Proposed phenomenological mechanism

I infer four coupled stages:

(a) Charge delivery and transport. The imposed potential and current cap act through solvent/electrolyte-dependent conductivity and mass transport. A useful latent exposure variable is

q_eff = I_eff(S,E,V,I_cap,t) t / N0,

where N0 is initial reagent amount and I_eff is the actual effective current, bounded by the programmed current cap. Actual current was not measured, so I_eff cannot be separated into conductivity, electrode kinetics, and mass-transfer contributions.

(b) Electrochemical activation. Within a viable potential window, conversion should rise with effective exposure approximately as

C = C_max(S,E,V) [1 − exp(−k(S,E,V) q_eff)].

This is a proposed predictive form, not a fitted law. The data identify a positive time dependence at +1 V but are insufficient to determine k, C_max, reaction order, or electron stoichiometry.

(c) Competing potential-dependent pathways. Potential sign is not merely a direction switch. I propose at least two branches: a target-forming branch and one or more non-target or destructive branches. Their rates depend differently on potential sign and magnitude. A schematic selectivity term is

Sel_target = r_target(V,S,E) / [r_target + r_side + r_degradation].

A sharp window or degradation factor, W(V), is required because +2 V did not behave as a stronger version of +1 V. A possible model is W≈1 in a moderate operating window but falling steeply once an overpotential threshold is exceeded.

(d) Recovery/phase-state coupling. The reported selective-product yield cannot safely be treated as conversion × electrochemical selectivity. At low signals, several batches reported selective-product yield larger than conversion. I therefore model the observable yield as a separate calibrated channel influenced by pathway branching, recovery or phase state, and measurement noise:

Y_obs = G(C, Sel_target, S, E, precipitation state) + ε_Y.

This is preferable to forcing an invalid mass-balance identity onto the public channels. Precipitation and pH appear to be electrolyte-sensitive state indicators, but precipitation is not a sufficient causal explanation for yield.

3. Evidence that formed and changed the account

Potential polarity first changed the simple “one favored sign” hypothesis. Batch 1 (+1 V, S0/E0, 100 mA, 1,800 s) gave conversion 0.02768, electrochemical selectivity 0.94848, selective-product yield 0.00316, faradaic efficiency 0.43412, transport efficiency 0.40542, energy efficiency 0.40728, and score 0.05970. Batch 2 changed only the potential to −1 V and gave lower conversion (0.01275), selectivity (0.64683), and energy efficiency (0.22601), but a higher reported yield (0.02142) and score (0.31172). Thus neither sign is uniformly superior across observables. This led me to infer polarity-dependent branching rather than a symmetric response to |V|.

Batch 3 tested +2 V under the Batch 1 conditions. Its final assay reported zero conversion, zero selectivity, zero selective-product yield, and zero faradaic, transport, and energy efficiencies, while ohmic efficiency remained 0.97581. This strongly rejected a monotonic “more voltage gives more conversion” model. My preferred explanation is an operating-window failure: excessive positive potential may redirect charge into destructive or unobserved processes. Plausible alternatives are an abrupt electrode-state transition, signal-channel masking, or conversion to species outside the reported target channels. The experiment cannot distinguish these possibilities.

Duration established the clearest kinetic relationship. At +1 V, 100 mA, S0/E0, Batch 4 used 300 s and gave conversion 0.00061 and yield 0.00374; Batch 1 used 1,800 s and gave conversion 0.02768 and yield 0.00316; Batch 5 used 7,200 s and gave conversion 0.07260 and yield 0.07194. Selectivity remained high—0.91036, 0.94848, and 0.94118, respectively. The tiny difference between the 300 s and 1,800 s yields is not convincing because both are in a low-signal regime, but the 7,200 s batch clearly produced much more conversion and target yield. This supports a charge/time-limited process over the tested range. It does not establish saturation, and no sufficiently long run was performed to test eventual degradation.

The intermediate UV-vis observations are qualitatively compatible with efficient early charge use, but they should not be interpreted as a clean time series because the intermediate and terminal readings came from different instruments. For example, Batch 1’s 900 s UV-vis estimates for energy, faradaic, and transport efficiency were 0.74976, 0.79402, and 0.77491, whereas its 1,800 s final-assay values were 0.40728, 0.43412, and 0.40542. This could represent declining process efficiency, but instrument/channel differences are a complete confound.

Current-cap evidence suggests a rate–efficiency tradeoff. Batch 6 used 10 mA rather than 100 mA at +1 V for 1,800 s. Relative to Batch 1, conversion fell from 0.02768 to 0.00549, while faradaic efficiency rose from 0.43412 to 0.48946, transport efficiency from 0.40542 to 0.46478, and energy efficiency from 0.40728 to 0.45173. Batch 6’s yield was 0.01230, but both yield values are sufficiently small that I do not regard their ordering as established. The observations are consistent with lower current slowing production while reducing losses. Because actual current was not observed and current was tested at only two caps, alternatives include a cap that binds only intermittently or a nonlinear electrode response.

4. Solvent coupling

Batches 7–9 changed solvent while retaining E0, +1 V, 100 mA, and 1,800 s. Compared with S0 in Batch 1:

• Batch 7, S1: conversion 0.03070, selectivity 0.95168, yield 0.02551, energy efficiency 0.47705, and score 0.40173.
• Batch 8, S2: conversion 0.03227, selectivity 0.76978, yield 0.00711, energy efficiency 0.74092, faradaic efficiency 0.78108, transport efficiency 0.77458, and score 0.17129.
• Batch 9, S3: conversion 0.01486, selectivity 0.83462, yield 0.03032, energy efficiency 0.66403, faradaic efficiency 0.58333, transport efficiency 0.60416, and score 0.44580.

These patterns show that solvent effects cannot be represented by one scalar “good solvent” factor. S2 favored electrical/transport efficiency but not target selectivity or yield; S3 gave lower conversion but the largest yield among the solvent variants; S1 preserved high selectivity and improved yield relative to S0. A plausible mechanism is that solvent separately changes ionic transport, interfacial electron-transfer kinetics, and relative stabilization or recovery of target and side products. Because the solvent identities are anonymous and no physical properties were supplied, polarity, viscosity, dielectric response, or donor ability cannot be assigned. Each solvent was also tested with only E0, leaving solvent–electrolyte interactions unidentifiable.

Observed safety risk also depended on solvent: approximately 0.0722 for S0, 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3 under these conditions. All were well below the 0.65 limit. The cause of this difference is not identifiable from the measurements.

5. Electrolyte coupling, pH, and precipitation

Batches 10–12 varied electrolyte in S0 at +1 V, 100 mA, and 1,800 s:

• Batch 10, E1: conversion 0.05803, selectivity 0.99140, yield 0.03783, faradaic efficiency 0.96317, transport efficiency 0.96452, ohmic efficiency 0.96613, energy efficiency 0.96405, pH-normalized value 0.19773, precipitation signal 0.85419, and score 0.59979.
• Batch 11, E2: conversion 0.05731, selectivity 0.94428, yield 0.04220, faradaic efficiency 0.91631, transport efficiency 0.92349, ohmic efficiency 0.97317, energy efficiency 0.93571, pH-normalized value 0.15112, precipitation signal 0.00524, and score 0.58055.
• Batch 12, E3: conversion 0.01780, selectivity 0.93642, yield 0.04249, faradaic efficiency 0.67308, transport efficiency 0.69430, ohmic efficiency 0.99684, energy efficiency 0.85504, pH-normalized value 0.27335, precipitation signal 0, and score 0.51319.

E1 and E2 substantially improved conversion and all major efficiency channels relative to E0 in Batch 1. I infer that electrolyte strongly controls both charge transport and productive interfacial chemistry. E1 gave the most uniformly strong balanced response, while E2 almost eliminated precipitation without sacrificing much conversion or efficiency. E3 eliminated the precipitation signal and retained a high yield despite relatively low conversion.

The precipitation series argues against treating precipitation as a simple target-loss gate. E0 batches were near the top of the precipitation scale, E1 remained high, and E2/E3 were near zero, yet E2 and E3 had similar or higher yield than E1. Precipitation may instead indicate electrolyte-dependent salt formation, phase transfer, or a spectator equilibrium. Likewise, pH-normalized values covaried with electrolyte but do not by themselves establish proton-coupled electron transfer. Proton involvement remains plausible because electrochemical kinetics, precipitation, and pH shifted together, but no independent pH intervention was performed.

6. Integrated predictive account

For interpolation near the tested loading, I would predict outcomes in the following order:

1. Determine whether the potential lies inside the viable sign-specific window. Do not extrapolate linearly from +1 V through +2 V or from +1 V to negative potentials.
2. Estimate effective delivered exposure from duration and the solvent/electrolyte-dependent effective current. Conversion should rise toward a material-specific ceiling with exposure.
3. Apply separate pathway factors for potential sign, solvent, and electrolyte to predict selectivity and reported target yield.
4. Predict faradaic, transport, ohmic, and energy efficiencies from shared latent transport and loss processes, but retain separate response channels rather than assuming their product or equality.
5. Treat precipitation and pH as coupled diagnostic states whose relationship to yield depends on electrolyte, not as universal monotonic penalties.

Qualitatively, longer electrolysis at moderate +1 V should increase conversion and yield within the observed range. Increasing positive voltage to +2 V should not be expected to help and may collapse the productive pathway. Lowering the current cap should reduce the production rate but may improve efficiency. E1 or E2 should outperform E0 for balanced electrochemical performance in S0 at the tested conditions. These are interpolations or short-range extrapolations, not universal laws.

7. What is not identifiable

The campaign does not identify electron stoichiometry, reaction order, actual current, electrode area, resistance, temperature dependence, detailed species, rate constants, equilibrium constants, or whether losses arise at the electrode, during transport, or during final recovery. Solvent and electrolyte labels are anonymous, so no real-material chemical interpretation is justified. No blank or zero-potential control was run. There were no replicates, no crossed solvent-by-electrolyte matrix, no long-time current series, and no independent manipulation of pH or precipitation. Instrument differences confound intermediate-versus-final temporal comparisons. Low-signal inconsistencies between conversion and yield prevent strict mass-balance interpretation.

Plausible alternative accounts include electrode passivation rather than molecular degradation at +2 V; electrolyte-dependent assay recovery rather than true kinetic improvement; phase partitioning rather than altered intrinsic selectivity; and stochastic low-level signal variation for some early yield differences. The large E1/E2 efficiency gains, the +2 V collapse, and the 7,200 s increase are the strongest observations because their magnitudes are much larger than the declared final-assay noise scales, but replication would still be required for empirical confirmation.

8. Operating interpretation

Batch 10 was the sealed balanced recommendation because it had the highest observed score (0.59979), conversion 0.05803, selectivity 0.99140, and approximately 0.96 faradaic, transport, ohmic, and energy efficiencies at low safety risk. It is not the universal yield maximum: Batch 5 achieved yield 0.07194 by extending electrolysis to 7,200 s, and Batches 11–12 slightly exceeded Batch 10’s yield at the standard duration. Thus the recommended condition reflects a balanced efficiency/selectivity objective, whereas a yield-prioritized process might rationally choose longer duration or a different electrolyte.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.66 | 0.48 | 0.8 |
| Q01 | energy_efficiency | 0.24 | 0.12 | 0.38 |
| Q01 | faradaic_efficiency | 0.42 | 0.3 | 0.55 |
| Q01 | score | 0.13 | 0.01 | 0.3 |
| Q01 | selective_product_yield | 0.01 | 0 | 0.028 |
| Q01 | transport_efficiency | 0.44 | 0.31 | 0.58 |
| Q02 | electrochemical_selectivity | 0.94 | 0.84 | 0.99 |
| Q02 | energy_efficiency | 0.41 | 0.27 | 0.55 |
| Q02 | faradaic_efficiency | 0.45 | 0.32 | 0.59 |
| Q02 | score | 0.1 | 0 | 0.27 |
| Q02 | selective_product_yield | 0.005 | 0 | 0.022 |
| Q02 | transport_efficiency | 0.43 | 0.29 | 0.57 |
| Q03 | electrochemical_selectivity | 0.68 | 0.47 | 0.84 |
| Q03 | energy_efficiency | 0.24 | 0.1 | 0.4 |
| Q03 | faradaic_efficiency | 0.42 | 0.27 | 0.58 |
| Q03 | score | 0.34 | 0.19 | 0.52 |
| Q03 | selective_product_yield | 0.09 | 0.035 | 0.17 |
| Q03 | transport_efficiency | 0.45 | 0.29 | 0.62 |
| Q04 | electrochemical_selectivity | 0.94 | 0.83 | 0.99 |
| Q04 | energy_efficiency | 0.4 | 0.25 | 0.56 |
| Q04 | faradaic_efficiency | 0.44 | 0.29 | 0.59 |
| Q04 | score | 0.42 | 0.29 | 0.57 |
| Q04 | selective_product_yield | 0.1 | 0.05 | 0.18 |
| Q04 | transport_efficiency | 0.43 | 0.28 | 0.59 |
| Q05 | electrochemical_selectivity | 0.7 | 0.45 | 0.89 |
| Q05 | energy_efficiency | 0.82 | 0.5 | 0.99 |
| Q05 | faradaic_efficiency | 0.85 | 0.56 | 0.99 |
| Q05 | score | 0.54 | 0.33 | 0.74 |
| Q05 | selective_product_yield | 0.13 | 0.05 | 0.25 |
| Q05 | transport_efficiency | 0.86 | 0.57 | 0.99 |
| Q06 | electrochemical_selectivity | 0.98 | 0.89 | 1 |
| Q06 | energy_efficiency | 0.92 | 0.72 | 1 |
| Q06 | faradaic_efficiency | 0.92 | 0.73 | 1 |
| Q06 | score | 0.63 | 0.49 | 0.77 |
| Q06 | selective_product_yield | 0.17 | 0.08 | 0.3 |
| Q06 | transport_efficiency | 0.93 | 0.74 | 1 |
| Q07 | electrochemical_selectivity | 0.68 | 0.42 | 0.87 |
| Q07 | energy_efficiency | 0.73 | 0.43 | 0.93 |
| Q07 | faradaic_efficiency | 0.62 | 0.36 | 0.84 |
| Q07 | score | 0.47 | 0.27 | 0.67 |
| Q07 | selective_product_yield | 0.11 | 0.035 | 0.22 |
| Q07 | transport_efficiency | 0.65 | 0.38 | 0.87 |
| Q08 | electrochemical_selectivity | 0.94 | 0.82 | 0.99 |
| Q08 | energy_efficiency | 0.82 | 0.61 | 0.96 |
| Q08 | faradaic_efficiency | 0.66 | 0.44 | 0.84 |
| Q08 | score | 0.54 | 0.39 | 0.7 |
| Q08 | selective_product_yield | 0.14 | 0.065 | 0.25 |
| Q08 | transport_efficiency | 0.69 | 0.47 | 0.87 |
| Q09 | electrochemical_selectivity | 0.58 | 0.34 | 0.78 |
| Q09 | energy_efficiency | 0.65 | 0.39 | 0.84 |
| Q09 | faradaic_efficiency | 0.7 | 0.46 | 0.88 |
| Q09 | score | 0.44 | 0.24 | 0.64 |
| Q09 | selective_product_yield | 0.06 | 0.018 | 0.13 |
| Q09 | transport_efficiency | 0.72 | 0.47 | 0.9 |
| Q10 | electrochemical_selectivity | 0.78 | 0.62 | 0.9 |
| Q10 | energy_efficiency | 0.72 | 0.54 | 0.87 |
| Q10 | faradaic_efficiency | 0.76 | 0.59 | 0.89 |
| Q10 | score | 0.49 | 0.3 | 0.66 |
| Q10 | selective_product_yield | 0.055 | 0.016 | 0.12 |
| Q10 | transport_efficiency | 0.75 | 0.57 | 0.89 |
| Q11 | electrochemical_selectivity | 0.65 | 0.4 | 0.84 |
| Q11 | energy_efficiency | 0.22 | 0.07 | 0.4 |
| Q11 | faradaic_efficiency | 0.34 | 0.17 | 0.53 |
| Q11 | score | 0.33 | 0.16 | 0.53 |
| Q11 | selective_product_yield | 0.12 | 0.035 | 0.25 |
| Q11 | transport_efficiency | 0.38 | 0.19 | 0.58 |
| Q12 | electrochemical_selectivity | 0.9 | 0.72 | 0.98 |
| Q12 | energy_efficiency | 0.32 | 0.14 | 0.51 |
| Q12 | faradaic_efficiency | 0.35 | 0.17 | 0.55 |
| Q12 | score | 0.4 | 0.23 | 0.59 |
| Q12 | selective_product_yield | 0.15 | 0.055 | 0.29 |
| Q12 | transport_efficiency | 0.38 | 0.19 | 0.59 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions interpolate the observed sign-specific response near ±1 V and scale productive exposure with duration and reagent-normalized charge. E1 is assigned the strong efficiency advantage observed experimentally, E3 an intermediate advantage, and S2 high transport/faradaic efficiency but weaker target selectivity. The 500 mA cases allow faster production but lower efficiencies from current-related losses. Intervals are deliberately wide for untested polarity-by-material interactions, long-duration behavior, current-cap extrapolation, and the low-yield score gate.

## K2

1. Claims and laws

No instance-specific prior mechanism, nominal property dossier, or expected result was supplied. The solvent and electrolyte labels were explicitly anonymous. The task supplied measurement and scoring contracts, but those are not chemical priors.

My initial “one favored potential sign” claim was only partly supported. Batches 1 and 2 showed strong polarity sensitivity, but contradicted the idea that one sign would dominate every metric: +1 V in Batch 1 gave higher conversion and selectivity, whereas −1 V in Batch 2 gave higher reported selective-product yield and score. This evidence changed my judgment from a simple favorable-sign model to sign-dependent pathway branching.

The proposed monotonic potential-magnitude relationship was contradicted. Batch 3 at +2 V reported zero conversion, yield, selectivity, and most efficiencies, despite Batch 1 producing a measurable response at +1 V. I therefore replaced a smooth “stronger field gives more conversion” law with a finite operating-window hypothesis. Whether the collapse reflects molecular destruction, electrode passivation, or an unobserved product channel remains untested.

A positive exposure/time relationship was supported within the +1 V, S0/E0, 100 mA domain. Conversion increased from 0.00061 in the 300 s Batch 4 to 0.02768 in the 1,800 s Batch 1 and 0.07260 in the 7,200 s Batch 5. Batch 5 also gave a much larger yield, 0.07194. However, saturation, reaction order, and eventual long-time degradation were untested; the data support rising response, not the particular exponential equation I proposed.

The current-cap tradeoff was tentatively supported. Relative to Batch 1, the 10 mA Batch 6 had lower conversion but somewhat higher faradaic, transport, and energy efficiencies. Only two current caps were tested, actual current was not measured, and current was not crossed with duration, so this remains provisional.

Material-dependent transport and pathway effects were supported. The solvent screen in Batches 7–9 separated electrical efficiency from target performance: S2 in Batch 8 had strong transport/faradaic efficiency but relatively low selectivity and yield, while S3 in Batch 9 had lower conversion but higher yield. The electrolyte screen supplied stronger evidence: E1 and E2 in Batches 10 and 11 greatly improved conversion and multiple efficiencies over E0 in Batch 1. The stronger claim that solvent and electrolyte effects are independent was untested because no crossed solvent-by-electrolyte matrix was run.

A universal precipitation penalty was contradicted. Batch 10 had substantial precipitation signal and good performance, while Batches 11 and 12 had approximately zero precipitation but similar or higher yield. Precipitation is therefore a material-dependent state indicator, not a sufficient monotonic yield gate. Proton-coupled chemistry remained untested because pH was observed but never independently manipulated.

2. One additional discriminating experiment

I would use a two-stage rescue experiment at the original S0/E0 loading scale. First, expose an initial reagent portion to +2 V long enough to reproduce the Batch 3 collapse and take a nondestructive intermediate UV-vis measurement. Then add a fresh reagent portion, change to +1 V, electrolyze for a long interval comparable to Batch 5, terminate, and perform the final assay.

This would distinguish my leading “+2 V redirects or destroys molecular material while the electrochemical interface remains usable” explanation from the alternative of persistent electrode passivation. Recovery of conversion and target yield after adding fresh reagent and returning to +1 V would favor molecular destruction or a reversible operating-window effect. Continued near-zero response despite fresh reagent would substantially increase belief in persistent passivation or another irreversible cell-state transition. Partial recovery would imply mixed substrate loss and electrode-state damage. Recovery without target yield would instead favor formation of persistent inhibitors or altered pathway selectivity. The experiment would not completely distinguish every alternative, but it directly tests whether productive activity survives the +2 V excursion.

3. Unused evidence, reliability, and goal effects

I did not analyze the full raw spectra or characterization artifacts; the account used processed instrument estimates. Most intermediate UV-vis traces, especially those from the material-screen batches, were not incorporated quantitatively. Intermediate and final efficiency estimates were also not treated as a clean time series because they came from different instruments. Cost, sample consumption, and detailed raw mass-balance fields were largely unused. pH-normalized and precipitation values were used descriptively but not fitted. No replication evidence existed.

The least reliable blind predictions are Q05, Q07, and Q09 because they combine negative polarity with electrolytes or solvent never tested at that polarity. Q11 and Q12 are also weak because 500 mA was outside the observed current-cap comparison and actual delivered current was unknown. All 7,200 s predictions at ±0.8 V extrapolate jointly in potential, loading, and duration. Q01 and Q02 are especially sensitive to measurement noise and the score’s low-yield multiplicative gate. The sealed Batch 10 recommendation is supported by the best observed balanced score, but its generality is limited by lack of replication and untested solvent–electrolyte interactions; Batch 5 remains a plausible alternative when yield matters more than time or efficiency.

The explanatory research goal did affect evidence collection. I prioritized polarity, voltage magnitude, duration, current, solvent, and electrolyte contrasts rather than replicating the best condition or performing a dense local optimization. That breadth improved mechanism discrimination but weakened variance estimates and recommendation certainty. The score was secondary, so I did not spend remaining design capacity solely refining Batch 10. I see no clear conflict with the assigned goal, but a purely optimization-focused campaign would likely have collected narrower, more replicated evidence.
