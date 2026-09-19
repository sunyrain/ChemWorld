# EC-W05-B12-discovery-E-MisIndexed

Development experiment; one independent source session.

Status: completed; completed batches: 12/12; posttests: 3/3.

## Research assignment

You are an autonomous scientist in a simulated electrochemical laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem,
network, repository inspection, external knowledge retrieval, or hidden simulator access.
Read material_information first. The task's research_goal is authoritative for this campaign.
Complete 12 independent batches; repetition is allowed. You have 12 intermediate instrument
uses across the campaign plus 12 final assays. Measurements are optional up to their budget.
Use the public operation and instrument contracts and actual current legal parameter ranges.
current_mA is a nonnegative magnitude cap, not a guaranteed delivered current.
You can choose materials, conditions, segmented operation, comparisons, and measurements freely.
Later prediction will cover both potential signs, short/long electrolysis, material changes,
and current caps, at a fixed stated loading; the actual conditions are withheld until reporting.
Use English for all research notes, explanations and final reports.
There are no mandatory belief snapshots, expression templates, or decision-audit fields.
For every batch explicitly terminate then measure final_assay. A batch ending is not the
campaign ending: continue with the returned next_state until campaign_ended is true.
After the campaign ends, use commit_final_recommendation to select one completed batch
(1-based lifecycle index) as your operating recommendation, with a short rationale. For the
discovery task this recommendation is only a secondary readout. Then return the required
status/summary JSON. Keep that handoff concise: a separate turn will invite your full scientific
account, then blind prediction, then a retrospective interview. Do not answer those early.
Public scores and diagnostics are observations; supplied prior information may be incomplete
or inaccurate, and observations are authoritative. No particular scientific result is required.


Your primary goal is to discover and test an explanatory, predictive account of this electrochemical system. Choose all experiments autonomously. You may propose, revise, combine or reject mechanisms and equations freely. Seek informative observations. The public optimization score is a secondary observation, not the research objective.

## Batch outcomes

| Batch | Final measured outcomes |
| --- | --- |
| 1 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.023405056446790695, "electrochemical_selectivity": 0.998518168926239, "energy_efficiency": 0.9631397724151611, "faradaic_efficiency": 1.0, "ohmic_efficiency": 0.9602119326591492, "pH_normalized": 0.23311282694339752, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.032431427389383316, "selective_product_yield": 0.001095070969313383, "transport_efficiency": 0.9858177900314331} |
| 2 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.643349289894104, "energy_efficiency": 0.28493189811706543, "faradaic_efficiency": 0.4065067172050476, "ohmic_efficiency": 0.9690497517585754, "pH_normalized": 0.23041747510433197, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.20301413536071777, "selective_product_yield": 0.012983827851712704, "transport_efficiency": 0.43276354670524597} |
| 3 | {"cost": 0.28271999955177307, "electrochemical_conversion": 0.006863243877887726, "electrochemical_selectivity": 0.8742918968200684, "energy_efficiency": 0.8269296288490295, "faradaic_efficiency": 0.7710249423980713, "ohmic_efficiency": 0.9251751899719238, "pH_normalized": 0.23113247752189636, "precipitation_signal": 0.9869203567504883, "safety_risk": 0.07225988060235977, "score": 0.004641509614884853, "selective_product_yield": 0.0001852083660196513, "transport_efficiency": 0.7875818610191345} |
| 4 | {"cost": 0.2829599976539612, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02824951522052288, "ohmic_efficiency": 0.9781976342201233, "pH_normalized": 0.2304418981075287, "precipitation_signal": 0.9876685738563538, "safety_risk": 0.07225988060235977, "score": 0.0032333421986550093, "selective_product_yield": 0.0007897500181570649, "transport_efficiency": 0.0} |
| 5 | {"cost": 0.2826479971408844, "electrochemical_conversion": 0.006524859927594662, "electrochemical_selectivity": 0.9942246675491333, "energy_efficiency": 0.9538390040397644, "faradaic_efficiency": 1.0, "ohmic_efficiency": 0.9919342994689941, "pH_normalized": 0.2354026883840561, "precipitation_signal": 0.9869949817657471, "safety_risk": 0.07225988060235977, "score": 0.342029333114624, "selective_product_yield": 0.011503680609166622, "transport_efficiency": 0.9897539615631104} |
| 6 | {"cost": 0.28332000970840454, "electrochemical_conversion": 0.01764504797756672, "electrochemical_selectivity": 0.9924110770225525, "energy_efficiency": 0.3747962415218353, "faradaic_efficiency": 0.3562629222869873, "ohmic_efficiency": 0.9079760909080505, "pH_normalized": 0.23212674260139465, "precipitation_signal": 0.9976252913475037, "safety_risk": 0.07225988060235977, "score": 0.3630875051021576, "selective_product_yield": 0.025647737085819244, "transport_efficiency": 0.3315795660018921} |
| 7 | {"cost": 0.2826240062713623, "electrochemical_conversion": 0.01189231127500534, "electrochemical_selectivity": 0.9860008955001831, "energy_efficiency": 0.9579402208328247, "faradaic_efficiency": 0.9921573996543884, "ohmic_efficiency": 1.0, "pH_normalized": 0.2311413437128067, "precipitation_signal": 0.9826673865318298, "safety_risk": 0.07225988060235977, "score": 0.26176583766937256, "selective_product_yield": 0.008813085965812206, "transport_efficiency": 0.9955577850341797} |
| 8 | {"cost": 0.28404000401496887, "electrochemical_conversion": 0.08441632986068726, "electrochemical_selectivity": 0.9826774597167969, "energy_efficiency": 0.9533127546310425, "faradaic_efficiency": 0.9667616486549377, "ohmic_efficiency": 0.9861299991607666, "pH_normalized": 0.22944386303424835, "precipitation_signal": 0.995540201663971, "safety_risk": 0.07225988060235977, "score": 0.6100314855575562, "selective_product_yield": 0.06754304468631744, "transport_efficiency": 0.9602663516998291} |
| 9 | {"cost": 0.30004000663757324, "electrochemical_conversion": 0.06313936412334442, "electrochemical_selectivity": 0.7232394218444824, "energy_efficiency": 0.7182890176773071, "faradaic_efficiency": 0.6886232495307922, "ohmic_efficiency": 0.9674895405769348, "pH_normalized": 0.20478656888008118, "precipitation_signal": 0.7306620478630066, "safety_risk": 0.09565988183021545, "score": 0.47298115491867065, "selective_product_yield": 0.06486181169748306, "transport_efficiency": 0.7094545364379883} |
| 10 | {"cost": 0.3256399929523468, "electrochemical_conversion": 0.08345033973455429, "electrochemical_selectivity": 0.7737419009208679, "energy_efficiency": 0.7101370692253113, "faradaic_efficiency": 0.7388896942138672, "ohmic_efficiency": 0.9107071161270142, "pH_normalized": 0.16967099905014038, "precipitation_signal": 0.0, "safety_risk": 0.11365988105535507, "score": 0.4811570346355438, "selective_product_yield": 0.04894297942519188, "transport_efficiency": 0.7402392625808716} |
| 11 | {"cost": 0.30963999032974243, "electrochemical_conversion": 0.047300588339567184, "electrochemical_selectivity": 0.7222159504890442, "energy_efficiency": 0.4834989309310913, "faradaic_efficiency": 0.36507949233055115, "ohmic_efficiency": 0.9700570106506348, "pH_normalized": 0.2838517129421234, "precipitation_signal": 0.005239714402705431, "safety_risk": 0.12625987827777863, "score": 0.3521272540092468, "selective_product_yield": 0.026333004236221313, "transport_efficiency": 0.3722594380378723} |
| 12 | {"cost": 0.28404000401496887, "electrochemical_conversion": 0.021524257957935333, "electrochemical_selectivity": 0.6160007119178772, "energy_efficiency": 0.2896477282047272, "faradaic_efficiency": 0.3725444972515106, "ohmic_efficiency": 0.985348641872406, "pH_normalized": 0.23064886033535004, "precipitation_signal": 0.9938013553619385, "safety_risk": 0.07225988060235977, "score": 0.3114335536956787, "selective_product_yield": 0.03507893905043602, "transport_efficiency": 0.39376944303512573} |

Public operations and purchased measurements: [trajectory](public-trajectory.json).

## K1

### Question

The experimental campaign has ended and the operating recommendation is sealed.
Submit a complete, self-contained mechanism report in English. Explain how you think this
world works: important variables, relationships, couplings, possible equations or processes;
which experiments formed or changed your explanation; its scope, unidentifiable factors,
and plausible alternatives. Use natural language, mathematics or pseudocode of your choice;
no prescribed model form or certain answer is required. Cite actual batch numbers and values,
distinguishing observations, extrapolations and conjectures. Do not perform new experiments
or invent unmeasured information. Develop your account fully, rather than compressing it
into a short abstract. Return the JSON report field. Prediction questions follow sealing.


### Response

MECHANISM REPORT

1. Experimental scope

I completed 12 batches. Every batch used the same stated loading: 0.020 mol limiting reagent in 0.040 L solvent, corresponding nominally to 0.50 mol/L before sampling. Thus, the campaign identifies effects of potential, current cap, electrolysis duration, solvent/electrolyte choice, and their couplings only at this loading. Each batch had one UV-visible intermediate measurement and one final assay. Final-assay numerical uncertainty was approximately 0.010 for conversion and selective-product yield, 0.012 for selectivity and Faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Values near zero are therefore especially uncertain and sometimes clipped at zero.

The reference condition was solvent S0, electrolyte E0, +1.0 V, a 100 mA current cap, and 600 s electrolysis (batch 1). The other batches were: batch 2, the same condition at -1.0 V; batch 3, +0.5 V; batch 4, +1.5 V; batch 5, +1.0 V with a 20 mA cap; batch 6, +1.0 V with a 300 mA cap; batch 7, +1.0 V for 60 s; batch 8, +1.0 V for 3600 s; batches 9–11, respectively S1/E1, S2/E2, and S3/E3 at +1.0 V, 100 mA, and 3600 s; and batch 12, S0/E0 at -1.0 V, 100 mA, and 3600 s.

2. Central mechanistic account

My working explanation is a charge-driven conversion with three separable but coupled bottlenecks:

(a) an interfacial potential window that determines whether the desired electron-transfer pathway is activated and selective;
(b) mass transport and current density, which determine how much of the imposed current can reach reagent rather than side reactions;
(c) bulk and interfacial material properties—conductivity, diffusivity, diffusion-layer thickness, proton activity, double-layer capacitance, and potential shifts—which alter both (a) and (b).

A compact phenomenological model is:

E_eff = E_applied - E_eq(S,E),

i_kin = i0(S,E,pH) f(E_eff),

i_lim proportional to A F D_eff(S,E) C / delta_eff(S,E),

i_product = min(I_cap, i_kin, i_lim) × FE(E_eff,I_cap/i_lim,S,E),

X(t) approximately 1 - exp[-k_q |i_product| t / n0],

dP/dt approximately selectivity(E_eff,S,E) × dX/dt - k_degrade(E_eff,S,E)P.

Here X is conversion and P is desired product. This is a proposed structure, not a fitted law: actual current, electrode area, electron stoichiometry, rate constants, and hidden material residuals were not observable. I infer that FE and selectivity have a favorable window near +1 V for S0/E0, while transport losses and side reactions increase when the current cap greatly exceeds the transport-supported current. At sufficiently positive potential, a competing or destructive pathway dominates. Negative potential accesses a weaker, less selective pathway.

3. Potential dependence and polarity

The strongest evidence for a potential window comes from batches 1, 3, and 4, which differed only in applied positive potential at 600 s and 100 mA.

At +0.5 V, batch 3 produced conversion 0.00686, selectivity 0.8743, Faradaic efficiency 0.7710, transport efficiency 0.7876, energy efficiency 0.8269, and selective-product yield 0.00019. At +1.0 V, batch 1 gave conversion 0.02341, selectivity 0.9985, Faradaic efficiency 1.000, transport efficiency 0.9858, energy efficiency 0.9631, and selective-product yield 0.00110. Despite the yield channel being too close to its uncertainty to distinguish those two low yields confidently, every efficiency and selectivity channel favored +1.0 V.

Increasing to +1.5 V did not continue this trend. Batch 4 had conversion clipped to 0, selectivity clipped to 0, transport efficiency clipped to 0, energy efficiency clipped to 0, and Faradaic efficiency only 0.02825, while ohmic efficiency remained 0.9782. This changed my initial possibility of a monotonic Butler–Volmer-like improvement into a peaked-window explanation. The cell was still ohmically competent at +1.5 V, but charge was no longer producing or transporting the desired electrochemical outcome. Plausible causes are a high-overpotential side reaction, rapid destruction of the target or intermediate, electrode passivation represented through the transport channel, or a benchmark response that explicitly penalizes departure from an optimal potential. The measurements cannot distinguish these alternatives.

Potential sign mattered strongly. At -1.0 V and 600 s, batch 2 had conversion clipped to 0, selectivity 0.6433, Faradaic efficiency 0.4065, transport efficiency 0.4328, and energy efficiency 0.2849. At the corresponding +1.0 V condition, batch 1 had near-unity selectivity, Faradaic efficiency, and transport efficiency. Extending the negative-potential run to 3600 s in batch 12 raised measured conversion to 0.02152 and selective-product yield to 0.03508, but selectivity remained only 0.6160, Faradaic efficiency 0.3725, transport efficiency 0.3938, and energy efficiency 0.2896. Thus negative potential is not completely inactive; rather, it appears to operate through a lower-efficiency branch that accumulates some product with time. This polarity conclusion is an observation-supported interpolation around ±1 V, not a claim about all negative potentials.

4. Time and accumulated charge

Batches 7, 1, and 8 form the duration series at S0/E0, +1.0 V, and 100 mA: 60, 600, and 3600 s. Conversion increased monotonically from 0.01189 to 0.02341 to 0.08442. The 3600 s conversion was about 3.6 times the 600 s value despite six times the duration, which is compatible with gradual reagent depletion, decreasing effective current, transport limitation, or simple measurement scatter. The dataset is not sufficient to choose among these.

Selectivity remained high across this duration series: 0.9860, 0.9985, and 0.9827. Final Faradaic efficiencies were 0.9922, 1.000, and 0.9668; transport efficiencies were 0.9956, 0.9858, and 0.9603. Therefore, there is no clear evidence that one hour at the favorable potential causes a major selectivity collapse. The slight efficiency decreases at 3600 s may indicate increasing depletion or surface change, but they are small enough to be partly assay noise.

Selective-product yields for the same series were 0.00881, 0.00110, and 0.06754. The middle value is non-monotonic, but both the 60 s and 600 s yields are of the same order as the stated 0.010 assay noise. I therefore give more weight to the monotonic conversion series and to the clearly elevated 3600 s yield than to the apparent 60-to-600 s yield decrease. At high signal, batch 8 also approximately respects the expected relationship between conversion, selectivity, and product yield: conversion × selectivity is about 0.083, compared with measured selective-product yield 0.0675. The difference shows that these independently calibrated assay channels should not be forced into an exact mass-balance identity.

Bulk acid conditions changed little during the S0/E0 duration series. Normalized pH was 0.2311 in batch 7, 0.2331 in batch 1, and 0.2294 in batch 8. Precipitation signal was also consistently near saturation: 0.9827, 1.000, and 0.9955. Hence the time-dependent conversion at this condition is unlikely to be explained primarily by a large measured bulk-pH shift or by an evolving bulk precipitation transition.

5. Current-cap and transport coupling

Batches 5, 1, and 6 varied the current cap at +1.0 V and 600 s: 20, 100, and 300 mA. At 20 mA, final Faradaic efficiency was 1.000, transport efficiency 0.9898, ohmic efficiency 0.9919, and energy efficiency 0.9538. At 100 mA, the corresponding values were 1.000, 0.9858, 0.9602, and 0.9631. These conditions are essentially equally efficient within measurement uncertainty, suggesting either that both caps are below the damaging transport threshold or that the imposed cap is not always the actual operating current.

At 300 mA, efficiency changed sharply: Faradaic efficiency fell to 0.3563, transport efficiency to 0.3316, and energy efficiency to 0.3748, while ohmic efficiency remained comparatively high at 0.9080. This combination supports a transport-limited side-reaction account more strongly than a purely resistive-loss account. In the proposed model, I_cap/i_lim becomes too large, reagent concentration at the interface falls, and excess current is diverted to nonproductive processes.

Conversion was 0.00652, 0.02341, and 0.01765 at 20, 100, and 300 mA, respectively, while selective-product yield was 0.01150, 0.00110, and 0.02565. These low-signal channels are not internally monotonic and differ by only a few assay standard deviations. They do not justify a precise current optimum. The robust conclusion is narrower: raising the cap to 300 mA severely harms FE, transport efficiency, and energy efficiency; 20–100 mA lies on a much better efficiency plateau at the tested loading and time.

6. Solvent/electrolyte effects

Material effects were tested only as diagonal pairs, so solvent and electrolyte contributions are confounded. At +1.0 V, 100 mA, and 3600 s, batch 8 used S0/E0, batch 9 used S1/E1, batch 10 used S2/E2, and batch 11 used S3/E3.

S0/E0 (batch 8) gave conversion 0.08442, selectivity 0.9827, yield 0.06754, Faradaic efficiency 0.9668, transport efficiency 0.9603, ohmic efficiency 0.9861, and energy efficiency 0.9533.

S1/E1 (batch 9) gave conversion 0.06314, selectivity 0.7232, yield 0.06486, Faradaic efficiency 0.6886, transport efficiency 0.7095, ohmic efficiency 0.9675, and energy efficiency 0.7183.

S2/E2 (batch 10) gave conversion 0.08345, selectivity 0.7737, yield 0.04894, Faradaic efficiency 0.7389, transport efficiency 0.7402, ohmic efficiency 0.9107, and energy efficiency 0.7101.

S3/E3 (batch 11) gave conversion 0.04730, selectivity 0.7222, yield 0.02633, Faradaic efficiency 0.3651, transport efficiency 0.3723, ohmic efficiency 0.9701, and energy efficiency 0.4835.

These results suggest that materials act on selectivity and interfacial/transport efficiency more strongly than on simple bulk resistance. Ohmic efficiency remained at least 0.91 in all four diagonal pairs, whereas FE and transport efficiency ranged from about 0.36 to 0.97. S0/E0 is therefore a jointly favorable electrochemical environment, S1/E1 and S2/E2 are intermediate, and S3/E3 is transport/Faradaic-poor at this operating point. S2/E2 nearly matched S0/E0 conversion but had lower selectivity and yield, showing that conversion alone does not identify productive chemistry.

The nominal property dossier provides plausible causes but not a unique explanation. A useful prior model would combine conductivity approximately multiplicatively, D_eff from electrolyte diffusivity times the solvent relative-diffusivity factor, double-layer capacitance similarly, and equilibrium potential shifts additively. For example, E_eq(S,E) could contain both listed solvent and electrolyte standard-potential shifts. However, fixed hidden world residuals and unknown couplings were explicitly allowed, and the diagonal design prevents empirical separation of those terms.

7. Acid/base and precipitation subsystem

The material pairs produced large, systematic differences in normalized pH and precipitation. At the 3600 s positive-potential condition, normalized pH was 0.2294 for S0/E0, 0.2048 for S1/E1, 0.1697 for S2/E2, and 0.2839 for S3/E3. These values are consistent with a material-controlled acid/base equilibrium rather than a strong time-controlled electrochemical drift.

A possible equilibrium submodel is based on solvent-adjusted proton activity and the electrolyte acid concentration/pKa, such as an effective Henderson–Hasselbalch relationship followed by the benchmark's normalization. I cannot reconstruct that normalization or obtain a physical pH from the normalized channel, so this remains structural conjecture.

Precipitation signal was 0.9955 for S0/E0, 0.7307 for S1/E1, 0 for S2/E2, and 0.00524 for S3/E3. A plausible form is:

precipitation signal approximately sigmoid[a(log10 ionic product - log10 Ksp_eff)],

where Ksp_eff includes the solvent's relative-solubility-product factor and ionic product depends on the listed precipitating-salt concentration and acid/base speciation. The qualitative pattern agrees with strong precipitation in the high-salt, low-Ksp S0/E0 formulation and little precipitation in S2/E2 and S3/E3. Because S0/E0 nevertheless had the best electrochemical efficiencies, the measured precipitate is not necessarily the desired product and does not simply poison performance. It may be a spectator salt, or its adverse and beneficial effects may compensate. No direct solid characterization was performed, so its identity is unidentifiable.

8. Relationship among efficiency channels

Ohmic efficiency was generally high, including under conditions where chemistry failed: 0.9782 in batch 4 at +1.5 V and 0.9853 in batch 12 at -1.0 V. Therefore, poor performance at those conditions should not be attributed mainly to bulk voltage loss.

Faradaic and transport efficiencies moved together more strongly: both were near unity around +1.0 V with moderate caps, both fell to roughly 0.35 at 300 mA, both collapsed at +1.5 V, and both were about 0.4 on the negative branch. This could reflect a real causal chain—transport starvation causes side-current—or correlated latent scoring factors. The final energy-efficiency channel tracked their broad direction but was not their exact product. I would model energy efficiency as an unknown monotone aggregate of Faradaic, transport, ohmic, and potential-loss terms rather than impose a strict multiplication rule.

The UV-visible intermediate measurements broadly corroborated these regimes despite having higher uncertainty. For example, batch 1 UV-visible FE/transport/ohmic/energy values were 0.9790/0.9599/0.9819/0.9143, compared with final values 1.000/0.9858/0.9602/0.9631. Batch 6 UV-visible values were 0.3431/0.3181/0.8922/0.3556, compared with final 0.3563/0.3316/0.9080/0.3748. Batch 4 showed the same collapse by both methods. This agreement supports treating the efficiency regimes as real rather than final-assay noise.

9. How the explanation evolved

Batch 1 established a highly selective and efficient positive-potential regime but, because its conversion and yield were small, did not establish whether performance was time-, potential-, or transport-limited. Batch 2 revealed a much poorer negative-potential branch, establishing polarity dependence. Batches 3 and 4 were decisive for the nonmonotonic potential-window model: +0.5 V was partially active, +1.0 V was efficient, and +1.5 V collapsed rather than improving.

Batches 5 and 6 separated current cap from potential. The similarity of 20 and 100 mA efficiencies and the collapse at 300 mA motivated the transport-ceiling component of the mechanism. Batches 7 and 8 established that favorable +1.0 V operation accumulates conversion over time without a major selectivity loss; batch 8 provided the clearest high-signal product observation.

Batches 9–11 showed that the favorable potential alone is not universal: material selection strongly rescales FE, transport, pH, precipitation, and selectivity. Finally, batch 12 demonstrated that the negative branch accumulates some product over long duration but remains much less efficient and selective than the positive branch, replacing a possible 'wrong sign gives no reaction' explanation with 'wrong sign gives a weak competing pathway.'

10. Scope, unidentifiable quantities, and plausible alternatives

The model is applicable only near the tested loading, volume, potential range (-1.0 to +1.5 V, with no data between -1.0 and +0.5 V or beyond the endpoints), current caps of 20–300 mA, durations of 60–3600 s, and the tested material combinations. Predictions outside that region are extrapolations.

Unidentifiable factors include actual current versus current cap, charge passed, electrode area and gap, electron stoichiometry, exchange-current density, true equilibrium potential, kinetic transfer coefficients, concentration profiles, temperature, surface state, product-degradation rate, and the fixed hidden residuals attached to materials and fixture. Solvent and electrolyte main effects cannot be separated because only S0/E0 and three diagonal pairs were tested. There were no exact replicate batches, so process variability cannot be separated cleanly from instrument noise. The assay channels are independent synthetic calibrations and do not enforce exact identities such as yield = conversion × selectivity.

Several alternatives remain plausible. The +1.5 V collapse might be chemical degradation, a parasitic electrolysis reaction, passivation, or a benchmark-defined optimum rather than classical kinetics. The 300 mA loss might be diffusion limitation, capacitive current, gas evolution, or another side reaction. The correlation between FE and transport might be causal or might arise from a common latent material factor. The precipitation signal may describe a spectator salt rather than product isolation. Material performance could be dominated by potential shifts rather than diffusivity, or vice versa; diagonal material testing cannot resolve this.

Overall, the best-supported qualitative account is: desired formation is charge-accumulating and polarity-selective; S0/E0 has a narrow favorable region around +1.0 V; moderate current caps preserve nearly unity FE and transport efficiency; excessive potential or current diverts charge from the desired pathway; duration raises conversion until depletion or transport effects cause sublinear growth; and solvent/electrolyte properties jointly determine potential alignment, transport, acid/base state, precipitation, and selectivity. Quantitative prediction should therefore use a potential-window term, a duration/charge term, a current-to-transport ratio, and material-specific modifiers, while retaining large uncertainty for untested material combinations and near-zero assay signals.

## Q

### Question

Using your own research, blindly predict the final results of these 12 independent new batches. Each starts from the same initial world state. For each metric give a point estimate and an 80% prediction interval, accounting for uncertainty. No additional experiments are allowed. Metrics follow the public instrument and scoring contracts. No mechanism form is prescribed. Do not modify your sealed report. Return complete predictions and one shared concise rationale in English; do not repeat the action lists for every question.
[{"query_id": "Q01", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 600}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q02", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 600}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q03", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q04", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q05", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 100, "electrolyte_profile": 1}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q06", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 100, "electrolyte_profile": 1}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q07", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 100, "electrolyte_profile": 3}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q08", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 100, "electrolyte_profile": 3}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q09", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q10", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 100, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q11", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": -0.8, "current_mA": 500, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q12", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.025}, {"operation": "add_reagent", "amount_mol": 0.012}, {"operation": "set_potential", "potential_V": 0.8, "current_mA": 500, "electrolyte_profile": 0}, {"operation": "electrolyze", "duration_s": 7200}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}]

### Response

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.58,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.36,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.17,
        "lower80": 0.03,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.37,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.9,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.86,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.58,
        "lower80": 0.18,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.004,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.55,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.32,
        "upper80": 0.56
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.356,
        "lower80": 0.25,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.91,
        "lower80": 0.81,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.93,
        "lower80": 0.82,
        "upper80": 1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.627,
        "lower80": 0.5,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.1,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.9,
        "lower80": 0.78,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.68
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.37,
        "lower80": 0.22,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.025,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.54,
        "lower80": 0.35,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.65,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.59,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.6,
        "upper80": 0.91
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.536,
        "lower80": 0.39,
        "upper80": 0.63
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.055,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.62,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.1,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.5
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.281,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.01,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.14,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.55,
        "upper80": 0.85
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.18,
        "upper80": 0.57
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.376,
        "lower80": 0.24,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.025,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.19,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.21,
        "upper80": 0.6
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.325,
        "lower80": 0.19,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.015,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.23,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.61,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.69,
        "lower80": 0.5,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.71,
        "lower80": 0.52,
        "upper80": 0.86
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.504,
        "lower80": 0.37,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.53,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.28
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.201,
        "lower80": 0.07,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.74,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0,
        "upper80": 0.34
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.284,
        "lower80": 0.15,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.012,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0,
        "upper80": 0.33
      }
    }
  ],
  "rationale": "Predictions interpolate the observed S0/E0 potential window: positive 0.8 V should remain highly selective and efficient, whereas negative potential follows the weaker branch seen at -1 V. Longer electrolysis and the smaller reagent inventory increase yield, but 7200 s is an extrapolation, so its intervals are wider. Material substitutions use the diagonal material results and nominal transport/potential-shift trends; uncertainty is enlarged because solvent and electrolyte effects were not separately identified. The 500 mA cases extrapolate the sharp Faradaic and transport losses already observed at 300 mA. Score estimates apply the published weighted components and selective-yield gate, making low-yield score intervals especially asymmetric and broad."
}
```

## K2

### Question

Your mechanism report and predictions are sealed; no prediction truth has been supplied.
Answer three questions in English, citing batch numbers without repeating your entire report:
1. Which supplied claims or self-developed laws were supported, contradicted or untested?
Which actual evidence changed your judgment? State explicitly if no instance prior was supplied.
2. With one more experiment, how would you distinguish your leading explanation from an
alternative, and how would different outcomes change your judgment? Do not execute it.
3. What evidence was unused, and which predictions or recommendations are least reliable?
Did the assigned goal affect evidence collection? It is acceptable to report no clear conflict.
Do not present hindsight as thoughts recorded at the time. Return the JSON report field.


### Response

1. Supported, contradicted, and untested claims

No instance-specific mechanistic prior or response law was supplied. The material dossier supplied nominal properties—conductivity, diffusivity, potential shifts, acid properties, capacitance, and precipitation parameters—but explicitly presented them as incomplete priors rather than an outcome model.

Supported self-developed claims:
- A favorable positive-potential window exists near +1.0 V for S0/E0. Batch 3 at +0.5 V was partly active, batch 1 at +1.0 V had near-unity selectivity, Faradaic efficiency, and transport efficiency, and batch 4 at +1.5 V collapsed. This evidence changed my judgment from a possible monotonic potential-response law to a peaked-window law.
- Negative potential accesses a weaker pathway rather than giving strictly no reaction. Batch 2 at -1.0 V and 600 s had low efficiencies, but batch 12 at -1.0 V and 3600 s accumulated measurable conversion and product while remaining less selective and efficient than the positive branch.
- Duration accumulates conversion in the favorable regime. Batches 7, 1, and 8 increased from 60 to 600 to 3600 s, with conversion rising from 0.0119 to 0.0234 to 0.0844 while selectivity remained near unity.
- Excessive current cap causes predominantly Faradaic/transport loss rather than purely ohmic loss. Batches 5 and 1 were efficient at 20 and 100 mA, whereas batch 6 at 300 mA had Faradaic and transport efficiencies near 0.35 but ohmic efficiency near 0.91.
- Materials strongly alter multiple coupled subsystems. Batches 8–11 showed large changes in selectivity, Faradaic efficiency, transport, normalized pH, and precipitation among the diagonal material pairs.

Contradicted or weakened claims:
- A monotonic benefit from increasing positive potential was contradicted by batch 4.
- A simple “wrong polarity means no chemistry” rule was contradicted by batch 12.
- A simple conductivity-only explanation was weakened because ohmic efficiency stayed high even when chemical performance failed, notably in batches 4 and 12.
- Exact identities such as selective yield = conversion × selectivity were not supported closely enough at low signal. Independent assay uncertainty and clipping were material, especially in batches 1–7.

Untested claims include the exact kinetic equation, actual current relative to its cap, electrode passivation, product degradation, electron stoichiometry, and whether precipitation is a spectator salt or causally affects conversion. Solvent and electrolyte main effects were also untested separately because batches 9–11 changed them together.

2. Most informative additional experiment

I would run S0/E0 at the fixed campaign loading, +1.5 V, 100 mA, but terminate after 60 s and obtain the final assay. This directly compares with batch 4 at +1.5 V for 600 s and batch 7 at +1.0 V for 60 s.

My leading explanation is that +1.5 V immediately favors a competing electrochemical pathway outside the desired potential window. An alternative is that desired product forms initially but is subsequently destroyed, or that the electrode becomes passivated over time.

If the 60 s +1.5 V experiment already showed near-zero selectivity, Faradaic efficiency, and transport efficiency like batch 4, I would strengthen the immediate competing-pathway or rapid interfacial-failure explanation. If it instead showed substantial product and efficiencies resembling batch 7, followed by the collapse seen only at 600 s, I would shift toward time-dependent product degradation or passivation. If Faradaic efficiency remained reasonable but transport alone collapsed, I would favor rapid surface blockage or mass-transfer failure. This single experiment would not identify the chemical species, but it would distinguish an immediate potential-selection effect from a time-dependent loss process.

3. Unused evidence, reliability, and effect of the goal

I did not fully exploit the raw spectral traces and individual peak structures in the characterization artifacts; the analysis relied mainly on processed estimates. Cost and leaderboard score were observed but were not used to construct the mechanism because optimization was secondary. UV-visible processed efficiency estimates were used as corroboration, but their full wavelength-dependent signals were not modeled. The nominal material properties were used qualitatively rather than fitted quantitatively. No dedicated pH-meter experiment was performed, so acid/base interpretation relied on the final-assay normalized-pH channel.

The least reliable predictions are Q11 and Q12 because 500 mA extrapolates beyond the highest tested cap of 300 mA; Q03–Q10 because 7200 s exceeds the longest tested duration of 3600 s; and Q05–Q10 because they use off-diagonal solvent/electrolyte combinations not directly observed. Q01 and Q02 also have unstable score predictions because their predicted yields lie near the 0.02 multiplicative score gate. The sealed recommendation of batch 8 is reliable as the best observed batch in this campaign, but its transfer to different loadings or longer durations is less reliable because it was not replicated.

The explanatory research goal materially shaped evidence collection: I prioritized contrasts in sign, potential, duration, current cap, and material pair rather than repeatedly optimizing or replicating the best condition. That breadth exposed the potential window and transport-current coupling, but it left process variability poorly estimated and solvent/electrolyte effects confounded. I see no clear conflict between the assigned goal and the evidence collected; the principal tradeoff was mechanistic coverage versus replication and precise optimization.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W05-B12-discovery-E-MisIndexed",
  "world": {
    "world_id": "EC-W05",
    "world_interventions": [],
    "world_seed": 4
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 12,
  "operations": 84,
  "posttests_completed": 3,
  "exact_replay": {
    "checked_steps": 84,
    "max_abs_error": 0.0,
    "mismatches": [],
    "verified": true
  },
  "failure": null,
  "source_failure": null,
  "interruption": null,
  "prediction_evaluation": {
    "valid": true,
    "metrics": {
      "selective_product_yield": {
        "n": 12,
        "mae": 0.052887171840450414,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.10241666666666667
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.061799090902010585,
        "coverage80": 1.0,
        "mean_width80": 0.2525
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.05519904881715775,
        "coverage80": 1.0,
        "mean_width80": 0.2991666666666667
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.05322636316219966,
        "coverage80": 1.0,
        "mean_width80": 0.30666666666666664
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.08338684727748236,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.2658333333333333
      },
      "score": {
        "n": 12,
        "mae": 0.062241340468327196,
        "coverage80": 1.0,
        "mean_width80": 0.26833333333333337
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.03128843475288401,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.085
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.05973586797714233,
          "coverage80": 1.0,
          "mean_width80": 0.2866666666666667
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.051662821471691135,
          "coverage80": 1.0,
          "mean_width80": 0.315
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.058586074312527985,
          "coverage80": 1.0,
          "mean_width80": 0.325
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.07192189872264863,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.26333333333333336
        },
        "score": {
          "n": 6,
          "mae": 0.06076628547906876,
          "coverage80": 1.0,
          "mean_width80": 0.25666666666666665
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.07448590892801682,
          "coverage80": 0.5,
          "mean_width80": 0.11983333333333333
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.06386231382687885,
          "coverage80": 1.0,
          "mean_width80": 0.21833333333333335
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.05873527616262436,
          "coverage80": 1.0,
          "mean_width80": 0.2833333333333334
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.047866652011871326,
          "coverage80": 1.0,
          "mean_width80": 0.28833333333333333
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.09485179583231607,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.26833333333333337
        },
        "score": {
          "n": 6,
          "mae": 0.06371639545758565,
          "coverage80": 1.0,
          "mean_width80": 0.27999999999999997
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.16200674265623094,
          "coverage80": 0.0,
          "mean_width80": 0.1015
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.08384849071502681,
          "coverage80": 1.0,
          "mean_width80": 0.31
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.0484022694826126,
          "coverage80": 1.0,
          "mean_width80": 0.31000000000000005
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.05079638957977295,
          "coverage80": 1.0,
          "mean_width80": 0.32
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.061548128724098206,
          "coverage80": 1.0,
          "mean_width80": 0.29000000000000004
        },
        "score": {
          "n": 2,
          "mae": 0.09973486483097077,
          "coverage80": 1.0,
          "mean_width80": 0.28
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.05016474887728691,
          "coverage80": 0.5,
          "mean_width80": 0.13
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.05014878273010254,
          "coverage80": 1.0,
          "mean_width80": 0.28500000000000003
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.0655758237838745,
          "coverage80": 1.0,
          "mean_width80": 0.3350000000000001
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.07557582378387451,
          "coverage80": 1.0,
          "mean_width80": 0.335
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.03761706471443177,
          "coverage80": 1.0,
          "mean_width80": 0.30500000000000005
        },
        "score": {
          "n": 2,
          "mae": 0.043093417406082135,
          "coverage80": 1.0,
          "mean_width80": 0.25
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03337223879992962,
          "coverage80": 1.0,
          "mean_width80": 0.10250000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.08203909277915955,
          "coverage80": 1.0,
          "mean_width80": 0.315
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.09688658356666566,
          "coverage80": 1.0,
          "mean_width80": 0.385
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.08928070366382598,
          "coverage80": 1.0,
          "mean_width80": 0.39
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.24759228467941286,
          "coverage80": 0.0,
          "mean_width80": 0.32500000000000007
        },
        "score": {
          "n": 2,
          "mae": 0.08229792380332945,
          "coverage80": 1.0,
          "mean_width80": 0.26
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.04619461268186569,
          "coverage80": 0.5,
          "mean_width80": 0.11249999999999999
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.006447696685790982,
          "coverage80": 1.0,
          "mean_width80": 0.14999999999999997
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.050967196822166466,
          "coverage80": 1.0,
          "mean_width80": 0.21000000000000005
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.03173697769641878,
          "coverage80": 1.0,
          "mean_width80": 0.21999999999999995
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.0416506564617157,
          "coverage80": 1.0,
          "mean_width80": 0.17499999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.014306222558021553,
          "coverage80": 1.0,
          "mean_width80": 0.19999999999999998
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.006079223294742405,
          "coverage80": 1.0,
          "mean_width80": 0.0355
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.023696191310882575,
          "coverage80": 1.0,
          "mean_width80": 0.14500000000000002
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.038521574139595005,
          "coverage80": 1.0,
          "mean_width80": 0.19
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.031127439141273472,
          "coverage80": 1.0,
          "mean_width80": 0.20500000000000002
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.04665065646171568,
          "coverage80": 1.0,
          "mean_width80": 0.16
        },
        "score": {
          "n": 2,
          "mae": 0.10974925011396407,
          "coverage80": 1.0,
          "mean_width80": 0.38
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.019505464732646943,
          "coverage80": 1.0,
          "mean_width80": 0.13249999999999998
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.12461429119110107,
          "coverage80": 1.0,
          "mean_width80": 0.31
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.030840845108032255,
          "coverage80": 1.0,
          "mean_width80": 0.365
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.04084084510803224,
          "coverage80": 1.0,
          "mean_width80": 0.37
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.06526229262351987,
          "coverage80": 1.0,
          "mean_width80": 0.33999999999999997
        },
        "score": {
          "n": 2,
          "mae": 0.024266364097595222,
          "coverage80": 1.0,
          "mean_width80": 0.24
        }
      }
    }
  },
  "token_accounting": {
    "valid": true,
    "complete": true,
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "stages": [
      {
        "stage": "source",
        "input": 282204,
        "cached_input": 254080,
        "output": 2803,
        "uncached_input": 28124
      },
      {
        "stage": "K1",
        "input": 33723,
        "cached_input": 31360,
        "output": 4382,
        "uncached_input": 2363
      },
      {
        "stage": "Q",
        "input": 39946,
        "cached_input": 3712,
        "output": 5749,
        "uncached_input": 36234
      },
      {
        "stage": "K2",
        "input": 45608,
        "cached_input": 33536,
        "output": 2102,
        "uncached_input": 12072
      }
    ],
    "total": {
      "input": 401481,
      "cached_input": 322688,
      "output": 15036,
      "uncached_input": 78793,
      "input_plus_output": 416517
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 539.3119999999908,
  "retest_batches": 1,
  "retest_operations": 7,
  "retest_replay": {
    "checked_steps": 7,
    "max_abs_error": 0.0,
    "mismatches": [],
    "verified": true
  },
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
