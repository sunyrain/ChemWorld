# EC-W01-B12-discovery-S-MisIndexed

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
| 1 | {"cost": 0.2591184079647064, "electrochemical_conversion": 0.04520663619041443, "electrochemical_selectivity": 0.9340003132820129, "energy_efficiency": 0.6457559466362, "faradaic_efficiency": 0.5561560392379761, "ohmic_efficiency": 0.96687251329422, "pH_normalized": 0.2322131097316742, "precipitation_signal": 1.0, "safety_risk": 0.0500902496278286, "score": 0.44438958168029785, "selective_product_yield": 0.020239122211933136, "transport_efficiency": 0.527452290058136} |
| 2 | {"cost": 0.2587152123451233, "electrochemical_conversion": 0.005616204347461462, "electrochemical_selectivity": 0.9305770993232727, "energy_efficiency": 0.9023817777633667, "faradaic_efficiency": 0.8785388469696045, "ohmic_efficiency": 0.9943674206733704, "pH_normalized": 0.22951775789260864, "precipitation_signal": 1.0, "safety_risk": 0.0500902496278286, "score": 0.5574256181716919, "selective_product_yield": 0.021555092185735703, "transport_efficiency": 0.9047956466674805} |
| 3 | {"cost": 0.2597520053386688, "electrochemical_conversion": 0.03163904696702957, "electrochemical_selectivity": 0.915261447429657, "energy_efficiency": 0.28351566195487976, "faradaic_efficiency": 0.21157313883304596, "ohmic_efficiency": 0.9331657886505127, "pH_normalized": 0.23023276031017303, "precipitation_signal": 0.9868234395980835, "safety_risk": 0.0500902496278286, "score": 0.31294527649879456, "selective_product_yield": 0.023699186742305756, "transport_efficiency": 0.228130042552948} |
| 4 | {"cost": 0.2614800035953522, "electrochemical_conversion": 0.03340890258550644, "electrochemical_selectivity": 0.9105417132377625, "energy_efficiency": 0.07787656038999557, "faradaic_efficiency": 0.12394371628761292, "ohmic_efficiency": 0.8653652667999268, "pH_normalized": 0.22954218089580536, "precipitation_signal": 0.987571656703949, "safety_risk": 0.0500902496278286, "score": 0.2556682527065277, "selective_product_yield": 0.03572174906730652, "transport_efficiency": 0.09245617687702179} |
| 5 | {"cost": 0.25263679027557373, "electrochemical_conversion": 0.0034490374382585287, "electrochemical_selectivity": 0.006436008028686047, "energy_efficiency": 0.0, "faradaic_efficiency": 0.01102422270923853, "ohmic_efficiency": 0.9860700964927673, "pH_normalized": 0.23450297117233276, "precipitation_signal": 0.9868980646133423, "safety_risk": 0.0500902496278286, "score": 0.035601284354925156, "selective_product_yield": 0.0084654176607728, "transport_efficiency": 0.0005147586925886571} |
| 6 | {"cost": 0.25211840867996216, "electrochemical_conversion": 0.03227447345852852, "electrochemical_selectivity": 0.6486517786979675, "energy_efficiency": 0.35663095116615295, "faradaic_efficiency": 0.45464208722114563, "ohmic_efficiency": 0.9759330749511719, "pH_normalized": 0.23122702538967133, "precipitation_signal": 0.9975283145904541, "safety_risk": 0.0500902496278286, "score": 0.33857211470603943, "selective_product_yield": 0.029748911038041115, "transport_efficiency": 0.4299587607383728} |
| 7 | {"cost": 0.2516863942146301, "electrochemical_conversion": 0.016650274395942688, "electrochemical_selectivity": 0.921483039855957, "energy_efficiency": 0.6507138013839722, "faradaic_efficiency": 0.5422229170799255, "ohmic_efficiency": 1.0, "pH_normalized": 0.23024162650108337, "precipitation_signal": 0.982570469379425, "safety_risk": 0.0500902496278286, "score": 0.28907886147499084, "selective_product_yield": 0.013108482584357262, "transport_efficiency": 0.545623242855072} |
| 8 | {"cost": 0.25367361307144165, "electrochemical_conversion": 0.13566359877586365, "electrochemical_selectivity": 0.9181596040725708, "energy_efficiency": 0.6010739803314209, "faradaic_efficiency": 0.5107552409172058, "ohmic_efficiency": 0.9927905797958374, "pH_normalized": 0.22854414582252502, "precipitation_signal": 0.9954432845115662, "safety_risk": 0.0500902496278286, "score": 0.46532365679740906, "selective_product_yield": 0.10910798609256744, "transport_efficiency": 0.5042598843574524} |
| 9 | {"cost": 0.2751184105873108, "electrochemical_conversion": 0.052248988300561905, "electrochemical_selectivity": 0.9046849608421326, "energy_efficiency": 0.9163883924484253, "faradaic_efficiency": 0.7653805613517761, "ohmic_efficiency": 0.9980692863464355, "pH_normalized": 0.23453307151794434, "precipitation_signal": 0.9987349510192871, "safety_risk": 0.07349024713039398, "score": 0.5487115979194641, "selective_product_yield": 0.06671109795570374, "transport_efficiency": 0.7862117886543274} |
| 10 | {"cost": 0.2591184079647064, "electrochemical_conversion": 0.07448767870664597, "electrochemical_selectivity": 0.9336842894554138, "energy_efficiency": 0.9039764404296875, "faradaic_efficiency": 0.8540635704994202, "ohmic_efficiency": 0.9614878296852112, "pH_normalized": 0.1977735310792923, "precipitation_signal": 0.8540157079696655, "safety_risk": 0.0500902496278286, "score": 0.5635361075401306, "selective_product_yield": 0.05163421109318733, "transport_efficiency": 0.8554131388664246} |
| 11 | {"cost": 0.30071839690208435, "electrochemical_conversion": 0.05780169740319252, "electrochemical_selectivity": 0.6867519617080688, "energy_efficiency": 0.6655946373939514, "faradaic_efficiency": 0.6361419558525085, "ohmic_efficiency": 0.9412053227424622, "pH_normalized": 0.166952446103096, "precipitation_signal": 0.005239714402705431, "safety_risk": 0.0914902463555336, "score": 0.43432819843292236, "selective_product_yield": 0.0324346087872982, "transport_efficiency": 0.6433219313621521} |
| 12 | {"cost": 0.28471839427948, "electrochemical_conversion": 0.006557117681950331, "electrochemical_selectivity": 0.8147659301757812, "energy_efficiency": 0.5860018730163574, "faradaic_efficiency": 0.2941546142101288, "ohmic_efficiency": 0.992182731628418, "pH_normalized": 0.28477731347084045, "precipitation_signal": 0.0, "safety_risk": 0.10409025102853775, "score": 0.36603137850761414, "selective_product_yield": 0.030164536088705063, "transport_efficiency": 0.3153795599937439} |

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

Mechanism report

1. Experimental scope

The campaign comprised 12 single-run batches. Every batch used 0.012 mol of limiting reagent in 0.040 L of one anonymous solvent, corresponding to a nominal initial loading of 0.30 mol L⁻¹ before sampling. Consequently, the data identify effects of current, potential, electrolysis time, solvent label, and electrolyte label only at this loading and volume. No real chemical identities were disclosed.

The principal reference condition was solvent S0, electrolyte E0, +0.8 V, 90 mA, and 1800 s (batch 1). Batches 2–4 varied current; batches 5–6 varied potential; batches 7–8 varied time; and batches 9–12 tested alternative media. Each batch received a final assay, while UV–visible or pH measurements provided intermediate corroboration.

2. Proposed qualitative mechanism

I infer a charge-driven target-forming pathway operating inside a restricted potential window, in parallel with non-target Faradaic pathways. Product accumulation is controlled jointly by:

• charge passed, proportional to |I|t;
• potential-dependent target selectivity;
• transport efficiency, which decreases strongly at high imposed current;
• Faradaic efficiency, which also decreases with current and at unsuitable potential;
• medium-dependent kinetic, transport, acid/base, and phase-partition factors;
• comparatively mild ohmic loss over most of the tested region.

A useful phenomenological model would be

q = |I|t,
η_useful = η_F(I,V,M) η_T(I,M) η_Ω(I,M) S(V,M),
Y(t) = Y_background(M) + A(M)[1 − exp{−k(M) q η_useful/n₀}],

where M denotes the solvent/electrolyte combination, n₀ is the initial reagent amount, η_F is Faradaic efficiency, η_T is transport efficiency, η_Ω is ohmic efficiency, and S is the potential-dependent probability that electron transfer enters the target pathway. This is a conceptual equation rather than a fitted law: the observations do not support unique parameter estimates, and the reported assay channels are not exactly stoichiometrically self-consistent.

For the current dependence, a plausible representation is

η_T ≈ 1/[1 + (|I|/I_lim(M))^a]

with a related decline in η_F. This represents depletion or polarization near the electrode when imposed current exceeds the rate at which reactive material can be supplied. The measured energy-efficiency channel appears to share these losses rather than being determined by ohmic efficiency alone.

For potential, the target pathway appears to have a maximum or plateau near +0.8 V under S0/E0. A peaked function such as

S(V) ≈ exp[−((V − V*)/w)^2]

could describe the positive-potential branch locally, but the substantial activity at −0.8 V implies either an asymmetric broad response, a second pathway, or a polarity-dependent mechanism. A single symmetric Gaussian should therefore not be treated as established.

3. Current and transport limitation

Batches 1–4 held S0/E0, +0.8 V, and 1800 s constant while changing current. At 20 mA (batch 2), final Faradaic, transport, ohmic, and energy efficiencies were 0.8785, 0.9048, 0.9944, and 0.9024. At 90 mA (batch 1), they fell to 0.5562, 0.5275, 0.9669, and 0.6458. At 200 mA (batch 3), they were 0.2116, 0.2281, 0.9332, and 0.2835. At 500 mA (batch 4), they reached only 0.1239, 0.0925, 0.8654, and 0.0779.

This is the strongest evidence for a limiting-current or polarization process. Transport and Faradaic efficiency collapse together, while ohmic efficiency decreases more gradually. Thus resistance alone cannot explain the loss. UV–visible measurements showed the same ordering: transport efficiency was 0.8942, 0.5015, 0.2382, and 0.0627 in batches 2, 1, 3, and 4, respectively.

Target selectivity changed only modestly across this series: 0.9306 at 20 mA, 0.9340 at 90 mA, 0.9153 at 200 mA, and 0.9105 at 500 mA. This suggests that excessive current predominantly wastes charge or creates transport losses rather than completely changing the identity of the electrochemical pathway.

Selective-product yield nevertheless increased weakly at the highest currents: 0.02156, 0.02024, 0.02370, and 0.03572 at 20, 90, 200, and 500 mA. Therefore, high current can provide some additional absolute product while doing so very inefficiently. Conversion was 0.00562, 0.04521, 0.03164, and 0.03341, which was nonmonotonic and not strictly compatible with the yield channel. I interpret the broad trend, not exact stoichiometry, because these are noisy synthetic assay observables and there was only one replicate per condition.

The supplied initial model claimed that current beyond the middle regime would continue to benefit product while transport and Faradaic efficiencies remained approximately stable. The weak continuing product benefit is partly consistent with batches 3–4, but the stability claim is decisively contradicted: both efficiencies declined by roughly four- to ten-fold from the low-current condition. My revised explanation therefore contains a pronounced transport/Faradaic penalty above the low-current regime.

4. Time dependence and accumulated charge

Batches 7, 1, and 8 form a time series at S0/E0, +0.8 V, and 90 mA. At 300, 1800, and 7200 s, selective-product yield was 0.01311, 0.02024, and 0.10911, while conversion was 0.01665, 0.04521, and 0.13566. This strongly supports progressive charge-driven accumulation.

Selectivity remained comparatively stable at 0.9215, 0.9340, and 0.9182. Faradaic efficiency was 0.5422, 0.5562, and 0.5108; transport efficiency was 0.5456, 0.5275, and 0.5043; and ohmic efficiency was 1.0000, 0.9669, and 0.9928. Their small changes contrast sharply with the yield and conversion increase. I therefore infer that time mainly controls the extent of reaction at fixed current, whereas current controls the instantaneous loss regime.

The 7200 s result does not yet demonstrate a plateau, and the yield increase is not exactly proportional to time. A saturating charge-dose law is plausible but not identified. Alternatives include induction behavior, assay noise, accumulation of a measurable product pool, or changing accessibility of reagent during electrolysis.

5. Potential dependence and competing pathways

Batch 5 changed the potential from +0.8 to +1.6 V at 90 mA and 1800 s. Performance collapsed: selectivity was 0.00644, conversion 0.00345, selective-product yield 0.00847, Faradaic efficiency 0.0110, transport efficiency 0.000515, and energy efficiency 0. The ohmic efficiency remained high at 0.9861. This combination is diagnostic: the failure at +1.6 V cannot be attributed primarily to bulk resistance. It is more consistent with a competing electron-transfer process, electrode polarization/passivation, reactant depletion at the interface, or a benchmark representation of electrochemical degradation outside the productive potential window.

Batch 6 at −0.8 V retained appreciable activity: conversion 0.03227, yield 0.02975, selectivity 0.6487, Faradaic efficiency 0.4546, transport efficiency 0.4300, energy efficiency 0.3566, and ohmic efficiency 0.9759. Thus the sign of potential does not simply switch all conversion off, although −0.8 V is less selective and less efficient than +0.8 V under the reference medium. A plausible interpretation is a second, polarity-dependent conversion route that forms some target together with more side product. Another possibility is that the anonymous benchmark maps potential to a broad asymmetric response rather than representing literal oxidation and reduction chemistry.

Only −0.8, +0.8, and +1.6 V were examined, so the location and width of the productive window are poorly identified. Interpolation near +0.8 V is more defensible than extrapolation toward ±2.5 V.

6. Medium, pH, and phase behavior

At the reference electrical conditions, changing the medium had effects as large as changing current.

Batch 9 used S1/E0. It gave conversion 0.05225, yield 0.06671, selectivity 0.9047, Faradaic efficiency 0.7654, transport efficiency 0.7862, energy efficiency 0.9164, and ohmic efficiency 0.9981. Relative to S0/E0 in batch 1, S1 improved product yield and all principal efficiency channels except for a small selectivity decrease. Because E0 was retained, this is direct evidence for a favorable S1 solvent effect at the tested point. Safety risk increased from 0.05009 to 0.07349.

Batch 10 used S0/E1. It produced conversion 0.07449, yield 0.05163, selectivity 0.9337, Faradaic efficiency 0.8541, transport efficiency 0.8554, energy efficiency 0.9040, and ohmic efficiency 0.9615. This directly shows that E1 improves charge utilization and transport relative to E0 in S0. It also changed pH_normalized from 0.2322 in batch 1 to 0.1978 and precipitation_signal from approximately 1.000 to 0.8540. The result supports electrolyte-dependent conductivity/speciation or interfacial kinetics, although the anonymous labels prevent a molecular assignment.

Batch 11 used S2/E2 and gave yield 0.03243, selectivity 0.6868, Faradaic efficiency 0.6361, transport efficiency 0.6433, pH_normalized 0.1670, and precipitation_signal 0.00524. Batch 12 used S3/E3 and gave yield 0.03016, selectivity 0.8148, Faradaic efficiency 0.2942, transport efficiency 0.3154, pH_normalized 0.2848, and precipitation_signal 0. The corresponding risks were 0.09149 and 0.10409. These results demonstrate that medium choice is coupled to acid/base state, phase behavior, and electrochemical performance. However, solvent and electrolyte were changed together, so no separate S2 versus E2 or S3 versus E3 effect is identifiable.

Precipitation remained near unity for every S0/E0 electrical perturbation and for S1/E0, including batch 5 where target formation nearly vanished. It therefore cannot be treated simply as target precipitation. It could represent reagent, target, byproduct, or a medium-dependent phase proxy. Its disappearance in batches 11–12 may reflect improved solubility rather than improved chemistry, because performance did not increase correspondingly.

The normalized pH was also nearly invariant among the S0/E0 time, current, and potential experiments, generally near 0.23. The larger changes occurred with alternative electrolytes/media. Thus pH is more plausibly a medium-controlled state variable than the principal cause of the current limitation, although it may mediate selectivity and precipitation across media. The measured quantity is normalized pH, not an absolute pH value, so no acid concentration or proton stoichiometry can be inferred.

7. Couplings among reported efficiencies

Faradaic and transport efficiencies covaried strongly in the current series and in alternative media. Energy efficiency followed them, while ohmic efficiency usually remained above 0.93 except at 500 mA, where it was still 0.865. I infer a shared latent loss process: once the requested current exceeds effective mass-transfer capacity, a growing fraction of charge enters nonproductive processes and the energetic cost per target event rises.

The channels are not related by a simple exact product. For example, batch 2 had η_Fη_Tη_Ω of approximately 0.79 while reported energy efficiency was 0.902. The proposed multiplicative equation should therefore be understood as causal bookkeeping, not as the instrument's exact calculation. Separate calibration, hidden normalization, and measurement noise are plausible.

The intermediate instruments generally corroborated final-assay trends but differed numerically. For instance, batch 2 UV–visible energy efficiency was 0.9508 versus 0.9024 in the final assay, and Faradaic efficiency was 0.8510 versus 0.8785. Batch 3 UV–visible and final transport efficiencies were 0.2382 and 0.2281. Such discrepancies caution against fitting precise high-order equations to individual values.

8. Safety and operating envelope

All observed safety risks were far below the stated 0.65 limit. Risk was 0.05009 for S0 batches, 0.07349 for S1/E0, 0.09149 for S2/E2, and 0.10409 for S3/E3. Within a fixed medium, changing electrical settings did not visibly change the reported risk. The evidence therefore points to a medium/loading contribution to this risk metric, but it does not establish that electrical stress is intrinsically risk-free outside the tested ranges.

The highest observed balanced score was batch 10 at 0.56354, followed closely by batch 2 at 0.55743 and batch 9 at 0.54871. This ordering reflects a tradeoff: low current maximized efficiency, favorable media improved transport and conversion, and longer time increased product accumulation. Score is secondary mechanistic evidence because it combines several channels by a predefined objective.

9. What is established, extrapolated, and conjectured

Directly observed: strong loss of Faradaic, transport, and energy efficiencies as current increased from 20 to 500 mA; increasing conversion and yield with time at 90 mA; catastrophic loss of target selectivity at +1.6 V; partial activity at −0.8 V; strong medium effects; and association of medium changes with normalized pH and precipitation.

Reasonable interpolation: within S0/E0 near +0.8 V and 20–90 mA, raising current should shorten the time needed to pass charge but reduce efficiency. At 90 mA, extending time beyond 300 s should generally raise conversion before eventual saturation or degradation. These statements should not be extrapolated far beyond the observed duration or potential range.

Mechanistic conjecture: concentration polarization causes the current-dependent η_T decline; side reactions cause the accompanying η_F decline; +1.6 V activates a dominant competing pathway or passivation process; E1 and S1 increase effective transport or favorable interfacial kinetics; and medium-dependent acid/base or solubility equilibria govern precipitation. None of those microscopic assignments is uniquely identified by anonymous materials and aggregate signals.

10. Limitations and plausible alternatives

There was one batch per condition and no exact replicate, so process variation cannot be separated cleanly from treatment effects. Reagent amount, volume, and initial concentration were fixed; their orders in any kinetic law are unknown. Electrode area, current density, temperature, stirring, mass-transfer geometry, electron stoichiometry, and actual species identities were unavailable. Accordingly, neither a Butler–Volmer law nor a quantitative limiting-current model can be uniquely fitted.

The potential and material designs were sparse. Only three potentials were observed. S2/E2 and S3/E3 were confounded pairs. Interactions among current, time, potential, solvent, and electrolyte were mostly not measured. Batch 9 and batch 10 identify S1 and E1 effects separately at one operating point, but they do not show whether their benefits combine additively.

An alternative to physical mass-transfer limitation is a benchmark controller in which efficiency channels are explicit functions of requested current. Another alternative is electrode passivation rather than diffusion limitation. The strong time stability of efficiencies at 90 mA favors a steady loss regime, but it does not distinguish these cases. Likewise, the negative-potential result could represent a genuinely different electrochemical pathway, an asymmetric empirical response, or noisy overlap of target and byproduct signals.

Finally, conversion and selective-product-yield channels were not always stoichiometrically ordered; batch 2, for example, reported conversion 0.00562 and yield 0.02156. They should be treated as separately calibrated bounded observables rather than forced into an exact material balance. The robust account is therefore structural: charge drives accumulation, excessive current imposes coupled transport/Faradaic losses, potential determines pathway identity, and the solvent/electrolyte medium shifts transport, selectivity, pH, and phase behavior. Precise microscopic chemistry remains unidentifiable.

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
        "estimate": 0.65,
        "lower80": 0.52,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.71
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.33,
        "lower80": 0.18,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.006,
        "upper80": 0.037
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.87,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.62,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.53,
        "upper80": 0.81
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.49,
        "lower80": 0.32,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.008,
        "upper80": 0.042
      },
      "transport_efficiency": {
        "estimate": 0.69,
        "lower80": 0.54,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.49,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.24,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.41,
        "lower80": 0.3,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.075,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.85,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.57,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.49,
        "upper80": 0.78
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.53,
        "lower80": 0.43,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.085,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.49,
        "upper80": 0.79
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.32,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.84
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.09,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.85
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.76,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.96
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.63,
        "lower80": 0.51,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.11,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.87,
        "lower80": 0.71,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.34,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.17,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.14,
        "upper80": 0.57
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.035,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.15,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.66,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.65,
        "lower80": 0.41,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.65
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.44,
        "lower80": 0.3,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.045,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.22,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.37,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.22,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.31,
        "upper80": 0.75
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.4,
        "lower80": 0.26,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.32,
        "upper80": 0.76
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.66,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.56,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.45,
        "upper80": 0.84
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.53,
        "lower80": 0.39,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.47,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.43,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.075,
        "lower80": 0.01,
        "upper80": 0.19
      },
      "faradaic_efficiency": {
        "estimate": 0.13,
        "lower80": 0.045,
        "upper80": 0.25
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.115,
        "lower80": 0.035,
        "upper80": 0.23
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.81,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.035,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.16,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.32,
        "lower80": 0.23,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.065,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.14,
        "lower80": 0.045,
        "upper80": 0.27
      }
    }
  ],
  "rationale": "Predictions interpolate the observed charge-time, polarity, and current-loss trends, with higher concentration from the smaller solvent volume assumed to moderately improve transport. E1 is projected to retain its observed efficiency advantage; E3 and S2 effects receive wider intervals because they were confounded in the campaign. The 500 mA cases reflect the measured collapse of transport, Faradaic, and energy efficiencies. Intervals include final-assay noise, single-replicate uncertainty, and substantial extrapolation uncertainty for untested medium-polarity combinations."
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

1. Assessment of claims and laws

No instance-level quantitative prior was supplied. There was, however, one qualitative supplied world-model claim: at fixed potential, increasing current beyond the middle regime would continue to benefit product while transport and Faradaic efficiencies remained approximately stable.

That claim was split by the evidence. Its product-benefit component received weak support: at +0.8 V and 1800 s, selective-product yield rose from 0.02024 in batch 1 at 90 mA to 0.02370 in batch 3 at 200 mA and 0.03572 in batch 4 at 500 mA. However, conversion was nonmonotonic across those batches, so the benefit was not uniformly supported. The efficiency-stability component was strongly contradicted. Faradaic efficiency fell from 0.5562 in batch 1 to 0.2116 in batch 3 and 0.1239 in batch 4; transport efficiency fell from 0.5275 to 0.2281 and 0.0925. Batch 2 at 20 mA strengthened that judgment because its Faradaic and transport efficiencies were much higher, 0.8785 and 0.9048.

A charge-accumulation relationship developed from the campaign was supported by batches 7, 1, and 8. At otherwise common S0/E0, +0.8 V, and 90 mA conditions, increasing duration from 300 to 1800 to 7200 s raised conversion from 0.01665 to 0.04521 to 0.13566 and yield from 0.01311 to 0.02024 to 0.10911. Selectivity and efficiency changed much less. A precise linear or saturating time law remained untested because only three durations were observed and no plateau was reached.

The proposed productive potential window near +0.8 V was supported by batch 5: changing from +0.8 V in batch 1 to +1.6 V caused selectivity to fall from 0.9340 to 0.00644, Faradaic efficiency from 0.5562 to 0.0110, and transport efficiency from 0.5275 to 0.000515, despite ohmic efficiency remaining high. Batch 6 showed that −0.8 V retained partial activity, with selectivity 0.6487 and yield 0.02975. This supported an asymmetric or second-polarity pathway but did not identify its microscopic chemistry.

The leading current-limitation explanation—concentration polarization or mass-transfer limitation accompanied by side reactions—was supported by the correlated current-dependent declines in transport, Faradaic, and energy efficiencies in batches 2, 1, 3, and 4. It was not uniquely established: passivation, electrode polarization, or a benchmark rule tied directly to requested current could reproduce the same pattern. No concentration, agitation, electrode-area, or recovery test was conducted.

Medium dependence was supported directly where one factor was isolated. Relative to batch 1, S1/E0 in batch 9 raised yield to 0.06671 and transport efficiency to 0.7862, while S0/E1 in batch 10 raised conversion to 0.07449, Faradaic efficiency to 0.8541, and transport efficiency to 0.8554. Medium coupling to normalized pH and precipitation was also observed. By contrast, the separate effects of S2 versus E2 in batch 11 and S3 versus E3 in batch 12 were untested because each pair changed together.

An exact multiplicative efficiency law was unsupported. For example, the product of the reported Faradaic, transport, and ohmic efficiencies in batch 2 does not equal its reported energy efficiency. The multiplicative expression in the sealed report was therefore causal bookkeeping rather than a validated measurement identity. Product saturation, degradation at very long duration, electron stoichiometry, reaction order, and the chemical identity of precipitated material all remained untested.

2. Proposed discriminating experiment

I would run one S0/E0 batch at +0.8 V, 200 mA, and 1800 s with 0.012 mol reagent but half the reference solvent volume, 0.020 L rather than 0.040 L, followed by the same intermediate UV–visible measurement and final assay. Batch 3 provides the historical 0.040 L comparison at the same electrical settings.

The leading mass-transfer explanation predicts that doubling nominal reagent concentration should increase the limiting current and materially raise transport and Faradaic efficiencies above batch 3 values of 0.2281 and 0.2116, potentially moving them toward the 90 mA regime. A large improvement, especially if ohmic efficiency changes much less, would substantially strengthen concentration polarization as the main cause.

If transport and Faradaic efficiencies remained near batch 3 despite the concentration increase, I would reduce confidence in simple bulk mass-transfer limitation and favor a current-programmed loss, electrode passivation, interfacial kinetic saturation, or a limitation insensitive to bulk concentration. If only transport improved while Faradaic efficiency did not, I would infer that mass supply and competing electron-transfer chemistry are separable losses. If both improved but selectivity collapsed, I would infer that concentration relieves transport limitation while introducing a distinct speciation or interfacial-selectivity effect. This single comparison would still not distinguish every alternative, but it directly perturbs the variable that a limiting-current mechanism should depend on.

3. Unused evidence, reliability, and influence of the goal

The analysis relied mainly on processed estimates. Raw UV–visible spectra, peak assignments, replicate traces, final-assay spectral structure, calibration details, and mass-balance packets were not analyzed. Intermediate measurements were used chiefly for qualitative corroboration; their complete raw signals were unused. Cost, sample consumption, and most operation-level risk increments were not incorporated into the mechanistic equations. Normalized pH and precipitation were used qualitatively but not quantitatively fitted. Conversion and ohmic efficiency informed score reasoning, but the blind prediction request did not ask for their explicit prediction intervals.

The least reliable blind predictions are Q07–Q08 for S0/E3 and Q09–Q10 for S2/E0. E3 was observed only together with S3 in batch 12, while S2 was observed only together with E2 in batch 11, so separating those material effects required extrapolation. Q05–Q06 also extrapolate E1 across duration and polarity despite E1 having been measured only at +0.8 V and 1800 s. Q11–Q12 combine 500 mA with 7200 s, whereas 500 mA was observed only for 1800 s; possible long-time passivation, heating, or degradation was not identified. All predictions also extrapolate from 0.040 L to 0.025 L. Their score intervals inherit additional uncertainty because conversion and ohmic efficiency had to be estimated internally, and yields near the 0.02 multiplicative gate can cause disproportionate score changes.

The sealed recommendation is strongest as a statement about the measured batch-10 condition, which had the highest observed score, and is less reliable if generalized to negative potential, longer duration, different concentration, or combined with another solvent.

The assigned goal did affect evidence collection. Because explanatory and predictive discovery was primary and score optimization secondary, the campaign spread its 12 batches across current, time, potential, solvent, and electrolyte rather than concentrating on local optimization or exact replication. That breadth exposed the high-current efficiency collapse, the +1.6 V failure, time accumulation, and material effects. The cost was weak replication, sparse interaction coverage, and confounding of S2/E2 and S3/E3. There was no clear conflict requiring unsafe or score-sacrificing operation—the measured risks stayed well below the limit—but the mechanism-oriented goal favored diagnostic diversity over a narrower, statistically replicated optimization study.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "discovery",
  "locus": "S",
  "system": "EC",
  "unit_id": "EC-W01-B12-discovery-S-MisIndexed",
  "world": {
    "world_id": "EC-W01",
    "world_interventions": [],
    "world_seed": 0
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 12,
  "operations": 84,
  "posttests_completed": 3,
  "exact_replay": {
    "verified": true,
    "checked_steps": 84,
    "max_abs_error": 0.0,
    "mismatches": []
  },
  "failure": null,
  "source_failure": null,
  "interruption": null,
  "prediction_evaluation": {
    "valid": true,
    "metrics": {
      "selective_product_yield": {
        "n": 12,
        "mae": 0.03814056339533999,
        "coverage80": 0.75,
        "mean_width80": 0.16833333333333333
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.03670426636934282,
        "coverage80": 1.0,
        "mean_width80": 0.25666666666666665
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.09762510389089585,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.3279166666666667
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.0955960108836492,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.33166666666666667
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.08204985034962496,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.31708333333333333
      },
      "score": {
        "n": 12,
        "mae": 0.080038167797029,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.2508333333333333
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.04965546611417085,
          "coverage80": 0.5,
          "mean_width80": 0.1585
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.03265562434991202,
          "coverage80": 1.0,
          "mean_width80": 0.33666666666666667
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.12998238712549212,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.33916666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.12835101127624512,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.3458333333333334
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.06764764274160066,
          "coverage80": 1.0,
          "mean_width80": 0.345
        },
        "score": {
          "n": 6,
          "mae": 0.10201259744664033,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.25833333333333336
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.02662566067650914,
          "coverage80": 1.0,
          "mean_width80": 0.17816666666666667
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.04075290838877362,
          "coverage80": 1.0,
          "mean_width80": 0.1766666666666666
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.06526782065629959,
          "coverage80": 1.0,
          "mean_width80": 0.31666666666666665
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.06284101049105326,
          "coverage80": 1.0,
          "mean_width80": 0.3175
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.09645205795764923,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.2891666666666666
        },
        "score": {
          "n": 6,
          "mae": 0.0580637381474177,
          "coverage80": 1.0,
          "mean_width80": 0.24333333333333332
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03168450087308884,
          "coverage80": 1.0,
          "mean_width80": 0.2025
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.027964820861816397,
          "coverage80": 1.0,
          "mean_width80": 0.23499999999999996
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.015,
          "coverage80": 1.0,
          "mean_width80": 0.2175
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.02021956205368041,
          "coverage80": 1.0,
          "mean_width80": 0.21000000000000002
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.03431072846055031,
          "coverage80": 1.0,
          "mean_width80": 0.1975
        },
        "score": {
          "n": 2,
          "mae": 0.025666143894195553,
          "coverage80": 1.0,
          "mean_width80": 0.19999999999999998
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.059162113368511196,
          "coverage80": 0.5,
          "mean_width80": 0.235
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.024040588140487706,
          "coverage80": 1.0,
          "mean_width80": 0.24500000000000002
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.1510575997829437,
          "coverage80": 0.5,
          "mean_width80": 0.3
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.14866346478462217,
          "coverage80": 0.5,
          "mean_width80": 0.3
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.06263291001319887,
          "coverage80": 1.0,
          "mean_width80": 0.29999999999999993
        },
        "score": {
          "n": 2,
          "mae": 0.060021035671234124,
          "coverage80": 1.0,
          "mean_width80": 0.255
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.041555278301239014,
          "coverage80": 1.0,
          "mean_width80": 0.16999999999999998
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.02882818222045902,
          "coverage80": 1.0,
          "mean_width80": 0.36
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.121272052526474,
          "coverage80": 1.0,
          "mean_width80": 0.43999999999999995
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.10366618752479553,
          "coverage80": 1.0,
          "mean_width80": 0.45
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.10760097801685331,
          "coverage80": 0.5,
          "mean_width80": 0.44999999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.055404276251792894,
          "coverage80": 1.0,
          "mean_width80": 0.29
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.04636276304721833,
          "coverage80": 1.0,
          "mean_width80": 0.17
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.006464867591857937,
          "coverage80": 1.0,
          "mean_width80": 0.195
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.0664564049243927,
          "coverage80": 1.0,
          "mean_width80": 0.30000000000000004
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.0664564049243927,
          "coverage80": 1.0,
          "mean_width80": 0.31500000000000006
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.07281612515449526,
          "coverage80": 1.0,
          "mean_width80": 0.29000000000000004
        },
        "score": {
          "n": 2,
          "mae": 0.04651364922523496,
          "coverage80": 1.0,
          "mean_width80": 0.21500000000000002
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.011329883272759616,
          "coverage80": 0.5,
          "mean_width80": 0.0325
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.016464867591857946,
          "coverage80": 1.0,
          "mean_width80": 0.16999999999999998
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.11124676704406739,
          "coverage80": 1.0,
          "mean_width80": 0.295
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.10624676704406744,
          "coverage80": 1.0,
          "mean_width80": 0.29999999999999993
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.09758867502212523,
          "coverage80": 0.5,
          "mean_width80": 0.285
        },
        "score": {
          "n": 2,
          "mae": 0.21892490781843663,
          "coverage80": 0.5,
          "mean_width80": 0.275
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.038748841509222975,
          "coverage80": 0.5,
          "mean_width80": 0.2
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.11646227180957791,
          "coverage80": 1.0,
          "mean_width80": 0.33499999999999996
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.1207177990674973,
          "coverage80": 1.0,
          "mean_width80": 0.415
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.12832367897033692,
          "coverage80": 1.0,
          "mean_width80": 0.41500000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.11734968543052673,
          "coverage80": 1.0,
          "mean_width80": 0.38
        },
        "score": {
          "n": 2,
          "mae": 0.07369899392127993,
          "coverage80": 1.0,
          "mean_width80": 0.27
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
        "input": 284681,
        "cached_input": 243584,
        "output": 2888,
        "uncached_input": 41097
      },
      {
        "stage": "K1",
        "input": 29996,
        "cached_input": 27136,
        "output": 3791,
        "uncached_input": 2860
      },
      {
        "stage": "Q",
        "input": 35628,
        "cached_input": 0,
        "output": 4456,
        "uncached_input": 35628
      },
      {
        "stage": "K2",
        "input": 39997,
        "cached_input": 29824,
        "output": 2652,
        "uncached_input": 10173
      }
    ],
    "total": {
      "input": 390302,
      "cached_input": 300544,
      "output": 13787,
      "uncached_input": 89758,
      "input_plus_output": 404089
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 447.67199999999866,
  "retest_batches": 1,
  "retest_operations": 7,
  "retest_replay": {
    "verified": true,
    "checked_steps": 7,
    "max_abs_error": 0.0,
    "mismatches": []
  },
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
