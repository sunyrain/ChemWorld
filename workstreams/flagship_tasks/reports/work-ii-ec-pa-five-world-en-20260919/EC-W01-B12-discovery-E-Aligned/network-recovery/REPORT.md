# EC-W01-B12-discovery-E-Aligned

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
| 1 | {"cost": 0.35339999198913574, "electrochemical_conversion": 0.008014115504920483, "electrochemical_selectivity": 0.01034972071647644, "energy_efficiency": 0.005256945732980967, "faradaic_efficiency": 0.02452157624065876, "ohmic_efficiency": 0.8842485547065735, "pH_normalized": 0.2322131097316742, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0} |
| 2 | {"cost": 0.35339999198913574, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.6373852491378784, "energy_efficiency": 0.0934688150882721, "faradaic_efficiency": 0.1618695855140686, "ohmic_efficiency": 0.8930863738059998, "pH_normalized": 0.22951775789260864, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.1442980170249939, "selective_product_yield": 0.01293044351041317, "transport_efficiency": 0.18812641501426697} |
| 3 | {"cost": 0.3546000123023987, "electrochemical_conversion": 0.0007435849984176457, "electrochemical_selectivity": 0.48768240213394165, "energy_efficiency": 0.036380425095558167, "faradaic_efficiency": 0.1343572735786438, "ohmic_efficiency": 0.9331657886505127, "pH_normalized": 0.23023276031017303, "precipitation_signal": 0.9868234395980835, "safety_risk": 0.07224962115287781, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.15091417729854584} |
| 4 | {"cost": 0.3524399995803833, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.5867583155632019, "energy_efficiency": 0.21445125341415405, "faradaic_efficiency": 0.4209892749786377, "ohmic_efficiency": 0.9773074388504028, "pH_normalized": 0.22954218089580536, "precipitation_signal": 0.987571656703949, "safety_risk": 0.07224962115287781, "score": 0.03851243853569031, "selective_product_yield": 0.002668586326763034, "transport_efficiency": 0.38950175046920776} |
| 5 | {"cost": 0.3594000041484833, "electrochemical_conversion": 0.040641557425260544, "electrochemical_selectivity": 0.6337980628013611, "energy_efficiency": 0.07717275619506836, "faradaic_efficiency": 0.1705145537853241, "ohmic_efficiency": 0.8914523720741272, "pH_normalized": 0.23450297117233276, "precipitation_signal": 0.9868980646133423, "safety_risk": 0.07224962115287781, "score": 0.228027805685997, "selective_product_yield": 0.0317985936999321, "transport_efficiency": 0.1600050926208496} |
| 6 | {"cost": 0.3853999972343445, "electrochemical_conversion": 0.016188450157642365, "electrochemical_selectivity": 0.602205216884613, "energy_efficiency": 0.332705557346344, "faradaic_efficiency": 0.38522690534591675, "ohmic_efficiency": 0.8256491422653198, "pH_normalized": 0.2046465277671814, "precipitation_signal": 0.7242242693901062, "safety_risk": 0.09564962238073349, "score": 0.27703842520713806, "selective_product_yield": 0.018730945885181427, "transport_efficiency": 0.36054354906082153} |
| 7 | {"cost": 0.436599999666214, "electrochemical_conversion": 0.022440113127231598, "electrochemical_selectivity": 0.4848628640174866, "energy_efficiency": 0.2908009886741638, "faradaic_efficiency": 0.3131462633609772, "ohmic_efficiency": 0.7584023475646973, "pH_normalized": 0.16796524822711945, "precipitation_signal": 0.0, "safety_risk": 0.11364962160587311, "score": 0.16635160148143768, "selective_product_yield": 0.013178887777030468, "transport_efficiency": 0.31654661893844604} |
| 8 | {"cost": 0.40459999442100525, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.5596017837524414, "energy_efficiency": 0.09364564716815948, "faradaic_efficiency": 0.10748729109764099, "ohmic_efficiency": 0.9109378457069397, "pH_normalized": 0.28357234597206116, "precipitation_signal": 0.00031451715040020645, "safety_risk": 0.12624962627887726, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.10099193453788757} |
| 9 | {"cost": 0.3853999972343445, "electrochemical_conversion": 0.00889441929757595, "electrochemical_selectivity": 0.6154546141624451, "energy_efficiency": 0.25434204936027527, "faradaic_efficiency": 0.2691199481487274, "ohmic_efficiency": 0.889053225517273, "pH_normalized": 0.23453307151794434, "precipitation_signal": 0.9987349510192871, "safety_risk": 0.09564962238073349, "score": 0.27096351981163025, "selective_product_yield": 0.02396930567920208, "transport_efficiency": 0.28995123505592346} |
| 10 | {"cost": 0.35339999198913574, "electrochemical_conversion": 0.030613934621214867, "electrochemical_selectivity": 0.6421678066253662, "energy_efficiency": 0.33983999490737915, "faradaic_efficiency": 0.40124601125717163, "ohmic_efficiency": 0.8661380410194397, "pH_normalized": 0.1977735310792923, "precipitation_signal": 0.8540157079696655, "safety_risk": 0.07224962115287781, "score": 0.1095128133893013, "selective_product_yield": 0.007061218377202749, "transport_efficiency": 0.402595579624176} |
| 11 | {"cost": 0.391400009393692, "electrochemical_conversion": 0.09767583012580872, "electrochemical_selectivity": 0.5893590450286865, "energy_efficiency": 0.35096412897109985, "faradaic_efficiency": 0.3633754849433899, "ohmic_efficiency": 0.8283767104148865, "pH_normalized": 0.2026483118534088, "precipitation_signal": 0.7270644307136536, "safety_risk": 0.09564962238073349, "score": 0.3133343458175659, "selective_product_yield": 0.051958516240119934, "transport_efficiency": 0.37055540084838867} |
| 12 | {"cost": 0.4129999876022339, "electrochemical_conversion": 0.32048654556274414, "electrochemical_selectivity": 0.5806371569633484, "energy_efficiency": 0.3294510245323181, "faradaic_efficiency": 0.32705867290496826, "ohmic_efficiency": 0.8417252898216248, "pH_normalized": 0.20316863059997559, "precipitation_signal": 0.7204003930091858, "safety_risk": 0.09564962238073349, "score": 0.373727023601532, "selective_product_yield": 0.2125057727098465, "transport_efficiency": 0.3482836186885834} |

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

All 12 batches used 0.040 mol reagent in 0.080 L solvent (nominal initial concentration 0.50 mol L^-1). Each received one electrolysis period, one UV–visible measurement, termination, and a final assay. Thus, this report describes potential, current-cap, time, solvent, and electrolyte effects at one loading and volume; it does not establish concentration or volume scaling.

Observed polarity and potential dependence

The reaction is predominantly cathodic in the explored convention. Batch 1 (S0/E0, +1.0 V, 500 mA cap, 600 s) produced essentially no response: final conversion 0.0080, selective-product yield 0, faradaic efficiency 0.0245, transport efficiency 0, and energy efficiency 0.0053. Reversing to -1.0 V under otherwise identical conditions in batch 2 raised selectivity to 0.6374, yield to 0.01293, faradaic efficiency to 0.1619, transport efficiency to 0.1881, and energy efficiency to 0.0935. The batch-2 conversion estimate was clipped/noisy at 0, so its nonzero yield should not be treated as an exact mass-balance identity.

More negative potential was not uniformly better. Batch 3 used S0/E0 at -2.0 V, 500 mA, 600 s. Relative to batch 2 at -1.0 V, selectivity decreased from 0.6374 to 0.4877 and energy efficiency from 0.0935 to 0.0364; faradaic efficiency was similar within experimental variability (0.1344 versus 0.1619), and selective yield was reported as 0. This supports an optimum or plateau at moderate cathodic overpotential, followed by parasitic reactions and wasted energy at excessive overpotential. Only +1, -1, and -2 V were tested, principally in S0/E0, so the exact onset potential and the location of the optimum remain unidentified.

Current, transport, and interfacial competition

Batch 4 tested S0/E0 at -1.0 V and a 100 mA current cap rather than 500 mA. Compared with batch 2, the lower cap increased final faradaic efficiency from 0.1619 to 0.4210, transport efficiency from 0.1881 to 0.3895, energy efficiency from 0.0935 to 0.2145, and ohmic efficiency from 0.8931 to 0.9773. However, selective yield decreased from 0.01293 to 0.00267 over the same 600 s. This suggests a rate–efficiency tradeoff: a high current cap passes more productive charge but pushes the interface closer to transport limitation and increases parasitic current, whereas a low cap uses charge more efficiently but supplies less total charge in a fixed time. The actual current trace was not observed, so I cannot tell when the current cap was binding.

A plausible process model is:

eta = applied_potential - effective_redox_potential(solvent,electrolyte,pH,interface)
I_actual = min(I_cap, |eta|/R_total, I_lim × g(eta))
I_lim proportional to n F A D_eff C_bulk / delta_eff
Q_product = integral(FE(eta,I_actual/I_lim,materials,precipitation) × I_actual dt)
conversion approximately 1 - exp[-Q_product/(n F N0)]
yield approximately conversion × product_selectivity.

Here R_total contains the fixed cell resistance plus material-dependent solution resistance. D_eff and delta_eff represent solvent/electrolyte transport. FE should decline when |eta| is excessive or I_actual/I_lim becomes large. These equations are a mechanistic conjecture, not a fitted law: electrode area, electron stoichiometry n, actual current, resistance, and limiting current were not measured.

Time/charge dependence

The clearest kinetic series is S1/E1 at -1.0 V and a 500 mA cap. At 600 s (batch 6), final conversion was 0.01619 and selective yield 0.01873. At 3600 s (batch 11), conversion was 0.09768 and yield 0.05196. At 14,400 s (batch 12), conversion was 0.32049 and yield 0.21251. The approximate proportionality of conversion to time between 600 and 3600 s, followed by sublinear growth by 14,400 s, is compatible with charge-controlled conversion followed by reactant depletion, growing polarization, or product/byproduct competition.

Selectivity in that series changed only moderately: 0.6022, 0.5894, and 0.5806. Final faradaic efficiencies were 0.3852, 0.3634, and 0.3271; transport efficiencies were 0.3605, 0.3706, and 0.3483; ohmic efficiencies were 0.8256, 0.8284, and 0.8417. Energy efficiencies were likewise stable at 0.3327, 0.3510, and 0.3295. Therefore, duration primarily accumulated productive charge rather than changing the operating regime, although the mild decline in selectivity and faradaic efficiency at long time is consistent with depletion or secondary chemistry. Batch 12 had the strongest demonstrated yield and score, but extrapolating beyond 14,400 s is unsafe because neither complete conversion nor late-stage degradation was tested.

Solvent and electrolyte effects

The crossed S0/S1 and E0/E1 experiments separate some medium and electrolyte effects. At -1.0 V, 500 mA, 600 s:

• S0/E0 (batch 2): selectivity 0.6374, FE 0.1619, transport 0.1881, ohmic 0.8931, energy 0.0935, precipitation signal 1.000, pH-normalized 0.2295.
• S1/E0 (batch 9): selectivity 0.6155, FE 0.2691, transport 0.2900, ohmic 0.8891, energy 0.2543, precipitation 0.9987, pH-normalized 0.2345.
• S0/E1 (batch 10): selectivity 0.6422, FE 0.4012, transport 0.4026, ohmic 0.8661, energy 0.3398, precipitation 0.8540, pH-normalized 0.1978.
• S1/E1 (batch 6): selectivity 0.6022, FE 0.3852, transport 0.3605, ohmic 0.8256, energy 0.3327, precipitation 0.7242, pH-normalized 0.2046.

Holding E0 fixed, changing S0 to S1 substantially improved transport, FE, and energy efficiency with little change in ohmic efficiency or pH. Holding S0 fixed, changing E0 to E1 produced an even larger improvement in transport and FE, lowered pH-normalized and precipitation signals, and slightly lowered ohmic efficiency. These effects are not strictly additive: S0/E1 slightly exceeded S1/E1 in FE, transport, energy, and selectivity, while S1/E1 gave the larger measured yield (0.01873 versus 0.00706). Fixed solvent–electrolyte interaction residuals, interfacial solvation, and assay noise are all plausible causes.

The nominal material dossier provides a coherent prior for these observations. E1 has higher diffusivity and a thinner diffusion layer than E0, which should raise limiting current, although its lower bulk conductivity can reduce ohmic efficiency. S1 has higher relative diffusivity but lower relative conductivity than S0, again predicting improved mass transport with some ohmic penalty. The measurements broadly follow this distinction: transport and FE improve strongly while ohmic efficiency changes less or decreases.

The paired-material surveys show that conductivity alone does not control performance. Batch 7 (S2/E2, -1.0 V, 500 mA, 600 s) had FE 0.3131, transport 0.3165, energy 0.2908, ohmic efficiency 0.7584, selectivity 0.4849, pH-normalized 0.1680, and precipitation signal 0. Batch 8 (S3/E3 under the same electrical program) had much poorer FE 0.1075, transport 0.1010, and energy 0.0936 despite higher ohmic efficiency 0.9109; its pH-normalized value was 0.2836 and precipitation was approximately 0.00031. Thus, avoiding precipitation is not sufficient for high conversion efficiency. E3’s nominally thick diffusion layer and the relatively low diffusivity of S3 provide a plausible transport explanation for batch 8.

Acid/base and precipitation coupling

The pH-normalized and precipitation outputs track electrolyte identity more strongly than electrolysis duration. S1/E1 batches 6, 11, and 12 gave pH-normalized values 0.2046, 0.2026, and 0.2032 and precipitation signals 0.7242, 0.7271, and 0.7204 despite a 24-fold duration range. This suggests that these channels mainly describe material-set equilibria rather than progressive electrolysis products.

A plausible equilibrium submodel is acid dissociation coupled to solvent proton activity, plus salt precipitation when an ion product exceeds an effective Ksp:

acid_fraction = f(pKa, acid concentration, solvent proton-activity factor)
P_precip = sigmoid[k × (log10 ion_product - log10 Ksp_effective)]
Ksp_effective = Ksp_electrolyte × solvent solubility factor × latent interaction.

E0’s high precipitating-salt concentration and low nominal Ksp are consistent with near-unit precipitation in batches 2 and 9. E2 and E3 have lower salt concentrations and higher Ksp and gave essentially zero precipitation in batches 7 and 8. Precipitation may remove charge carriers, restrict transport, or foul the interface, but it cannot be the only transport mechanism: batch 9 retained precipitation near 1 while outperforming batch 2, and precipitation-free batch 8 still transported poorly.

Relationship among assay channels

At adequate signal, selective-product yield is broadly consistent with conversion multiplied by selectivity. For batch 11, conversion × selectivity is about 0.0576 versus measured yield 0.05196; for batch 12 it is about 0.186 versus yield 0.2125. At low conversion this identity breaks down visibly: batch 2 reported conversion 0 but yield 0.01293, and batch 9 conversion 0.00889 but yield 0.02397. I interpret those discrepancies as finite assay noise, clipping at zero, and possibly separately calibrated synthetic channels rather than evidence for material creation. Consequently, low-level yield and conversion values should be modeled with censoring/noise rather than forced into an exact algebraic constraint.

Intermediate UV–visible measurements generally supported the final efficiency rankings but were noisy. For example, batch 4 intermediate FE/transport/energy were 0.4052/0.3597/0.2229 and final values were 0.4210/0.3895/0.2145. Batch 10 intermediate values were 0.4083/0.3670/0.4001 and final values 0.4012/0.4026/0.3398. Batch 12 intermediate values were 0.4032/0.4062/0.3049 and final values 0.3271/0.3483/0.3295. These differences set a practical uncertainty scale and warn against interpreting small ranking differences as deterministic.

Working causal account

My preferred explanation is a cathodic electron-transfer network with at least one desired product channel and one or more parasitic channels. Applied potential determines activation and side-reaction driving force. Current cap and duration determine total available charge. Solvent and electrolyte jointly determine effective redox potential, proton availability, diffusivity, diffusion-layer thickness, conductivity, double-layer behavior, and precipitation. These properties control actual current, mass-transfer limitation, FE, and selectivity. Product accumulation is approximately charge-integrating at low conversion, with depletion or secondary chemistry making long-time growth sublinear. Energy efficiency is a correlated composite of productive charge, transport, and ohmic losses, but the data do not support treating it as the exact product of the separately reported efficiency channels.

A useful predictive pseudocode would be:

1. Compute effective potential shift from solvent + electrolyte + interaction.
2. If cathodic driving force is below onset, set productive current near zero.
3. Compute solution resistance from nominal conductivities plus a fixed latent residual.
4. Compute limiting current from diffusivity/diffusion-layer factors and concentration.
5. Set actual current to the minimum of the cap, ohmic current, and polarization-limited current.
6. Decrease FE/selectivity for excessive overpotential, high actual-current/limiting-current ratio, and possibly precipitate fouling.
7. Integrate productive charge over time, with depletion and secondary-reaction corrections.
8. Generate conversion and selective yield, then add instrument/process noise and clip bounded channels to [0,1].

Scope and unresolved alternatives

No replicate batches were run, so latent material effects cannot be cleanly separated from run noise. Loading and volume were fixed, electrode geometry and world-specific resistance were unobserved, and only one current-cap comparison was made. The four-by-four solvent/electrolyte matrix was not completed: only S0/E0, S1/E0, S0/E1, S1/E1 and the confounded S2/E2 and S3/E3 pairs were measured. Potential dependence outside the S0/E0 comparison is largely extrapolative. Therefore, material coefficients, potential shifts, and interactions are only partially identifiable.

Plausible alternatives include direct kinetic inhibition rather than mass-transfer limitation, double-layer/capacitance changes controlling FE, precipitation acting as a beneficial or harmful interfacial film rather than merely removing ions, and two desired-product pathways with different potential dependence. The existing data favor a transport-plus-overpotential account because lower current improved FE/transport, E1’s favorable transport properties improved performance, and -2 V was worse than -1 V. They do not uniquely exclude those alternatives.

The strongest empirical conclusions are: the productive polarity is negative; moderate cathodic potential outperformed both positive and more extreme negative potential in S0/E0; lower current cap improves efficiency but reduces fixed-time yield; accumulated time strongly increases conversion and yield under S1/E1; solvent and electrolyte effects are coupled; and precipitation, conductivity, and acidity each matter but none alone ranks the materials.

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
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.15,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.33,
        "upper80": 0.56
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.023,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0.0,
        "upper80": 0.01
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.01
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.34,
        "upper80": 0.55
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.339,
        "lower80": 0.22,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.31,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.5,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.33,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.44,
        "upper80": 0.7
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.417,
        "lower80": 0.29,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.31
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.17,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.278,
        "lower80": 0.15,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.015,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.14,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.38,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.1,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.26,
        "upper80": 0.53
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.306,
        "lower80": 0.19,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.02,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0.06,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.11,
        "upper80": 0.3
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.317,
        "lower80": 0.23,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.12,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      }
    }
  ],
  "rationale": "Predictions use the observed cathodic polarity, the higher fixed-time efficiency but lower throughput at a 100 mA cap, approximate charge/time scaling with depletion uncertainty, and measured solvent–electrolyte trends. The new 0.48 M loading is close to the studied 0.50 M concentration, but its smaller reagent inventory makes long-time fractional yield uncertain. Positive-potential batches are predicted to remain at the assay floor, as did the +1 V reference. Intervals widen for long-duration, untested material combinations and low-signal score gating."
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

No instance-specific prior mechanism, response law, or expected batch outcome was supplied. The supplied information consisted of nominal material properties and general electrochemical/instrument contracts. I therefore treated claims such as “higher diffusivity should improve transport” as qualitative priors, not as known laws for this particular world.

Supported self-developed claims:
• Product formation is cathodic in the tested voltage convention. Batch 1 at +1 V had zero selective yield and nearly zero FE/transport, whereas otherwise matched batch 2 at -1 V produced yield 0.01293, selectivity 0.637, FE 0.162, and transport efficiency 0.188. This was the clearest early change in my judgment.
• Product formation approximately integrates productive charge over time. In matched S1/E1 batches 6, 11, and 12, increasing duration from 600 to 3,600 to 14,400 s raised conversion from 0.0162 to 0.0977 to 0.3205 and yield from 0.0187 to 0.0520 to 0.2125.
• Current entails a throughput–efficiency tradeoff. Relative to batch 2 at a 500 mA cap, batch 4 at 100 mA increased FE from 0.162 to 0.421, transport efficiency from 0.188 to 0.390, and energy efficiency from 0.093 to 0.214, but reduced 600 s yield from 0.01293 to 0.00267.
• Nominal transport properties are relevant. Under S0, changing E0 to E1 improved FE and transport from 0.162/0.188 in batch 2 to 0.401/0.403 in batch 10. This broadly agreed with E1’s nominally thinner diffusion layer and higher diffusivity.
• Solvent and electrolyte are coupled rather than separable by a simple ranking. Batches 2, 6, 9, and 10 showed substantial crossed S0/S1–E0/E1 effects and nonadditivity.

Contradicted or weakened claims:
• A monotonic “more negative voltage is better” law was contradicted. Batch 3 at -2 V had lower selectivity and energy efficiency than batch 2 at -1 V under S0/E0, and its reported yield was zero.
• Conductivity alone did not explain performance. Batch 8 had high ohmic efficiency (0.911) but poor FE and transport (0.107 and 0.101).
• Avoiding precipitation alone did not guarantee good performance. Batch 8 had essentially no precipitation yet performed poorly, while batch 9 retained a precipitation signal of 0.999 and still outperformed batch 2 in FE, transport, and energy efficiency.
• An exact identity yield = conversion × selectivity was contradicted at low signal, most visibly in batches 2 and 9. It remained approximately useful at higher signal in batches 11 and 12, suggesting assay noise or clipping rather than a literal failure of mass balance.

Untested claims include the proposed exponential depletion law, additive material-dependent potential shifts, the exact limiting-current expression, electron stoichiometry, concentration scaling, and behavior beyond 14,400 s. The campaign did not measure actual current, electrode polarization, or concentration profiles, so mass-transfer limitation remains an inference rather than a uniquely identified mechanism.

2. One discriminating experiment

I would compare batch 2’s continuous S0/E0 electrolysis with one additional batch having the same material loading, -1 V potential, 500 mA cap, and 600 s total active electrolysis, but delivered as short pulses separated by open-circuit or near-zero-driving-force recovery intervals. All other preparation and assay steps would be matched.

My leading transport-depletion explanation predicts that recovery intervals would replenish the interfacial reactant concentration. The pulsed batch should therefore show higher FE, transport efficiency, and selective yield per unit active charge than continuous batch 2. A substantial improvement, especially without a major selectivity change, would strengthen the diffusion-layer explanation.

If pulsing produced essentially the same FE, transport efficiency, and yield as batch 2, I would reduce confidence in transient concentration polarization and favor an alternative based on intrinsic electron-transfer kinetics, fixed solvent/electrolyte interfacial effects, or a current-independent parasitic pathway. If pulsing worsened selectivity or yield, I would consider double-layer charging, repeated surface-state disruption, or beneficial steady-state film formation. Interpretation would still be limited because actual current and interfacial concentration would remain unmeasured.

3. Unused evidence, reliability, and goal effects

The campaign did not exploit raw spectral shapes or artifact-level peak assignments; inference used processed UV–visible and final-assay estimates. No pH-meter measurements were taken. Cost and safety observations were not used mechanistically beyond checking that operations remained viable. Several nominal dossier variables—especially capacitance and quantitative potential shifts—were discussed qualitatively but could not be separately estimated. Intermediate UV–visible data mainly confirmed broad efficiency rankings; they were not sufficient to identify kinetics. There were also no replicates, so fixed material effects and batch noise remain partly confounded.

The least reliable blind predictions are Q05, Q07, and Q09 because they combine long duration, a 100 mA cap, the smaller reagent inventory, and material combinations or current regimes not directly observed. Q07 is particularly uncertain because E3 was observed only in the confounded S3/E3 batch 8. Q11 also extrapolates S0/E0 to a substantially larger charge per mole. The exact near-zero values and scores predicted for positive-potential batches are uncertain because assay clipping dominates there, although the qualitative prediction of negligible productive conversion is comparatively robust.

The sealed recommendation of batch 12 is reliable only as the best demonstrated batch, not as a global optimum. It had the highest observed score and yield, but potential and current were not optimized around that S1/E1 condition, and longer times were not tested.

The explanatory research goal did affect evidence collection. I prioritized polarity, potential, current, duration, material contrasts, and the S0/S1–E0/E1 cross rather than repeatedly optimizing the best early condition. This improved mechanistic coverage but reduced replication and local optimization precision. I see no sharp conflict between the scientific goal and the eventual recommendation, but the broad design made the recommendation and some quantitative predictions less precise than a campaign devoted solely to optimization would have been.

## Evaluation and resource use

```json
{
  "system": "EC",
  "world": {
    "world_id": "EC-W01",
    "world_seed": 0,
    "world_interventions": []
  },
  "goal": "discovery",
  "locus": "E",
  "arm": "Aligned",
  "budget": 12,
  "unit_id": "EC-W01-B12-discovery-E-Aligned",
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
  "prediction_evaluation": {
    "valid": true,
    "metrics": {
      "selective_product_yield": {
        "n": 12,
        "mae": 0.08978781657246872,
        "coverage80": 0.5,
        "mean_width80": 0.07291666666666667
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.44255763401587805,
        "coverage80": 0.5,
        "mean_width80": 0.1525
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.33883348832527793,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.14708333333333334
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.3434821591774622,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.14125000000000001
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.39689020541807013,
        "coverage80": 0.25,
        "mean_width80": 0.12291666666666667
      },
      "score": {
        "n": 12,
        "mae": 0.26198136849949755,
        "coverage80": 0.5,
        "mean_width80": 0.12083333333333333
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.021843821163289246,
          "coverage80": 1.0,
          "mean_width80": 0.13166666666666668
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.022013954122861223,
          "coverage80": 1.0,
          "mean_width80": 0.25166666666666665
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.06987390647331874,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.23833333333333337
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.060943782329559326,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.23833333333333337
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.08833230967322986,
          "coverage80": 0.5,
          "mean_width80": 0.21166666666666667
        },
        "score": {
          "n": 6,
          "mae": 0.035410241161783526,
          "coverage80": 1.0,
          "mean_width80": 0.19333333333333336
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.1577318119816482,
          "coverage80": 0.0,
          "mean_width80": 0.014166666666666666
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.8631013139088948,
          "coverage80": 0.0,
          "mean_width80": 0.05333333333333334
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.6077930701772372,
          "coverage80": 0.0,
          "mean_width80": 0.05583333333333334
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.6260205360253651,
          "coverage80": 0.0,
          "mean_width80": 0.04416666666666667
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.7054481011629105,
          "coverage80": 0.0,
          "mean_width80": 0.03416666666666667
        },
        "score": {
          "n": 6,
          "mae": 0.4885524958372116,
          "coverage80": 0.0,
          "mean_width80": 0.04833333333333334
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.12046783059835434,
          "coverage80": 0.5,
          "mean_width80": 0.1275
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4629648208618164,
          "coverage80": 0.5,
          "mean_width80": 0.13999999999999999
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.09,
          "coverage80": 0.5,
          "mean_width80": 0.125
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.1075,
          "coverage80": 0.5,
          "mean_width80": 0.13
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.08821108564734459,
          "coverage80": 0.5,
          "mean_width80": 0.095
        },
        "score": {
          "n": 2,
          "mae": 0.19271491384506226,
          "coverage80": 0.5,
          "mean_width80": 0.11499999999999999
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.1391621133685112,
          "coverage80": 0.5,
          "mean_width80": 0.0975
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.44814857602119446,
          "coverage80": 0.5,
          "mean_width80": 0.13999999999999999
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.499006153345108,
          "coverage80": 0.0,
          "mean_width80": 0.15749999999999997
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.48900615334510805,
          "coverage80": 0.0,
          "mean_width80": 0.14750000000000002
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.4477391278743744,
          "coverage80": 0.5,
          "mean_width80": 0.1325
        },
        "score": {
          "n": 2,
          "mae": 0.34111991739273073,
          "coverage80": 0.5,
          "mean_width80": 0.14
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.0886675751209259,
          "coverage80": 0.5,
          "mean_width80": 0.065
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.45382818222045895,
          "coverage80": 0.5,
          "mean_width80": 0.17
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.343772052526474,
          "coverage80": 0.5,
          "mean_width80": 0.165
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3661661875247955,
          "coverage80": 0.5,
          "mean_width80": 0.16499999999999998
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.5401009780168533,
          "coverage80": 0.0,
          "mean_width80": 0.13999999999999999
        },
        "score": {
          "n": 2,
          "mae": 0.3064042762517929,
          "coverage80": 0.5,
          "mean_width80": 0.135
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.09976042211055755,
          "coverage80": 0.5,
          "mean_width80": 0.060000000000000005
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4585351324081421,
          "coverage80": 0.5,
          "mean_width80": 0.13999999999999999
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.3489564049243927,
          "coverage80": 0.5,
          "mean_width80": 0.13
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3579553425312042,
          "coverage80": 0.5,
          "mean_width80": 0.12000000000000001
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.4601835882663727,
          "coverage80": 0.0,
          "mean_width80": 0.10500000000000001
        },
        "score": {
          "n": 2,
          "mae": 0.29599883484840395,
          "coverage80": 0.5,
          "mean_width80": 0.135
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.006920116727240384,
          "coverage80": 0.5,
          "mean_width80": 0.01
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4585351324081421,
          "coverage80": 0.5,
          "mean_width80": 0.15
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.3887467670440674,
          "coverage80": 0.5,
          "mean_width80": 0.14
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3977457046508789,
          "coverage80": 0.5,
          "mean_width80": 0.13
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.4899561381340027,
          "coverage80": 0.0,
          "mean_width80": 0.11000000000000001
        },
        "score": {
          "n": 2,
          "mae": 0.17957509218156337,
          "coverage80": 0.5,
          "mean_width80": 0.07
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.08374884150922299,
          "coverage80": 0.5,
          "mean_width80": 0.07750000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.37333396017551423,
          "coverage80": 0.5,
          "mean_width80": 0.17500000000000002
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.3625195521116257,
          "coverage80": 0.5,
          "mean_width80": 0.165
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.34251956701278685,
          "coverage80": 0.5,
          "mean_width80": 0.155
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.35515031456947327,
          "coverage80": 0.5,
          "mean_width80": 0.155
        },
        "score": {
          "n": 2,
          "mae": 0.2560751764774323,
          "coverage80": 0.5,
          "mean_width80": 0.13
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
        "input": 337297,
        "cached_input": 283136,
        "output": 2792,
        "uncached_input": 54161
      },
      {
        "stage": "K1",
        "input": 28496,
        "cached_input": 26240,
        "output": 3250,
        "uncached_input": 2256
      },
      {
        "stage": "Q",
        "input": 104559,
        "cached_input": 67072,
        "output": 5345,
        "uncached_input": 37487
      },
      {
        "stage": "K2",
        "input": 39470,
        "cached_input": 28288,
        "output": 2058,
        "uncached_input": 11182
      }
    ],
    "total": {
      "input": 509822,
      "cached_input": 404736,
      "output": 13445,
      "uncached_input": 105086,
      "input_plus_output": 523267
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 487.954000000027,
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

## Network recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
