# EC-W04-B12-discovery-E-MisIndexed

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
| 1 | {"cost": 0.28271999955177307, "electrochemical_conversion": 0.013086915947496891, "electrochemical_selectivity": 1.0, "energy_efficiency": 0.6824511289596558, "faradaic_efficiency": 0.6771227121353149, "ohmic_efficiency": 0.9572166204452515, "pH_normalized": 0.2343980222940445, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.6484189629554749} |
| 2 | {"cost": 0.28271999955177307, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.6608133912086487, "energy_efficiency": 0.2785569429397583, "faradaic_efficiency": 0.4276559054851532, "ohmic_efficiency": 0.9660544395446777, "pH_normalized": 0.23170267045497894, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.1773260086774826, "selective_product_yield": 0.011144060641527176, "transport_efficiency": 0.4539127051830292} |
| 3 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.0, "ohmic_efficiency": 0.9696498513221741, "pH_normalized": 0.23241767287254333, "precipitation_signal": 0.9863388538360596, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0} |
| 4 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.4909871220588684, "energy_efficiency": 0.03493475541472435, "faradaic_efficiency": 0.30103063583374023, "ohmic_efficiency": 0.9818079471588135, "pH_normalized": 0.23172709345817566, "precipitation_signal": 0.9870871305465698, "safety_risk": 0.07211905717849731, "score": 0.020910058170557022, "selective_product_yield": 0.0018916419940069318, "transport_efficiency": 0.2695430815219879} |
| 5 | {"cost": 0.28380000591278076, "electrochemical_conversion": 0.053034573793411255, "electrochemical_selectivity": 0.9964359998703003, "energy_efficiency": 0.6340478658676147, "faradaic_efficiency": 0.6489278078079224, "ohmic_efficiency": 0.9644203782081604, "pH_normalized": 0.23668788373470306, "precipitation_signal": 0.9864134788513184, "safety_risk": 0.07211905717849731, "score": 0.4860093593597412, "selective_product_yield": 0.057555098086595535, "transport_efficiency": 0.6384183168411255} |
| 6 | {"cost": 0.28835999965667725, "electrochemical_conversion": 0.21875295042991638, "electrochemical_selectivity": 0.9942426681518555, "energy_efficiency": 0.5971070528030396, "faradaic_efficiency": 0.604580819606781, "ohmic_efficiency": 0.9662771224975586, "pH_normalized": 0.23341193795204163, "precipitation_signal": 0.997043788433075, "safety_risk": 0.07211905717849731, "score": 0.535851240158081, "selective_product_yield": 0.22477294504642487, "transport_efficiency": 0.5798974633216858} |
| 7 | {"cost": 0.28835999965667725, "electrochemical_conversion": 0.3548843562602997, "electrochemical_selectivity": 0.911453902721405, "energy_efficiency": 0.8794814348220825, "faradaic_efficiency": 0.9255519509315491, "ohmic_efficiency": 0.9940516948699951, "pH_normalized": 0.2024071365594864, "precipitation_signal": 0.8347593545913696, "safety_risk": 0.07211905717849731, "score": 0.6842333078384399, "selective_product_yield": 0.32206326723098755, "transport_efficiency": 0.9289522767066956} |
| 8 | {"cost": 0.28835999965667725, "electrochemical_conversion": 0.3417273461818695, "electrochemical_selectivity": 0.9536837339401245, "energy_efficiency": 0.9142008423805237, "faradaic_efficiency": 0.9373606443405151, "ohmic_efficiency": 0.9746547341346741, "pH_normalized": 0.15736572444438934, "precipitation_signal": 0.00031451715040020645, "safety_risk": 0.07211905717849731, "score": 0.691424548625946, "selective_product_yield": 0.311756432056427, "transport_efficiency": 0.9308652877807617} |
| 9 | {"cost": 0.28835999965667725, "electrochemical_conversion": 0.20064347982406616, "electrochemical_selectivity": 0.7866674661636353, "energy_efficiency": 0.7193522453308105, "faradaic_efficiency": 0.5341969132423401, "ohmic_efficiency": 0.9984561204910278, "pH_normalized": 0.2710474133491516, "precipitation_signal": 0.008188718929886818, "safety_risk": 0.07211905717849731, "score": 0.4989752173423767, "selective_product_yield": 0.17841653525829315, "transport_efficiency": 0.5550282001495361} |
| 10 | {"cost": 0.3043600022792816, "electrochemical_conversion": 0.3398071527481079, "electrochemical_selectivity": 0.9547810554504395, "energy_efficiency": 0.8924268484115601, "faradaic_efficiency": 0.878567636013031, "ohmic_efficiency": 0.9272238612174988, "pH_normalized": 0.16029666364192963, "precipitation_signal": 0.0, "safety_risk": 0.095519058406353, "score": 0.6690056324005127, "selective_product_yield": 0.3011533319950104, "transport_efficiency": 0.8799172639846802} |
| 11 | {"cost": 0.3299599885940552, "electrochemical_conversion": 0.31031396985054016, "electrochemical_selectivity": 0.8789082765579224, "energy_efficiency": 0.837060272693634, "faradaic_efficiency": 0.797838032245636, "ohmic_efficiency": 0.9311953186988831, "pH_normalized": 0.17378978431224823, "precipitation_signal": 0.005239714402705431, "safety_risk": 0.11351905763149261, "score": 0.618683934211731, "selective_product_yield": 0.2650642395019531, "transport_efficiency": 0.8050180077552795} |
| 12 | {"cost": 0.3139599859714508, "electrochemical_conversion": 0.28202733397483826, "electrochemical_selectivity": 0.8725355267524719, "energy_efficiency": 0.8378998637199402, "faradaic_efficiency": 0.7657387256622314, "ohmic_efficiency": 0.9672118425369263, "pH_normalized": 0.16626106202602386, "precipitation_signal": 0.0, "safety_risk": 0.12611906230449677, "score": 0.6157164573669434, "selective_product_yield": 0.27662140130996704, "transport_efficiency": 0.786963701248169} |

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

Mechanistic account

1. Experimental scope

All 12 batches used the same initial loading: 0.020 mol limiting reagent in 0.040 L solvent, corresponding nominally to 0.50 mol/L before sampling. Every electrolysis used a 100 mA current cap. Thus the campaign identifies effects of polarity, applied potential, electrolysis time, electrolyte profile, and solvent identity at this loading, but it does not independently identify concentration or current-cap effects.

2. Proposed process model

I interpret the system as a charge-driven, potential-window-selective electrochemical conversion with three coupled layers:

(a) Electrode kinetics determine whether the desired electron-transfer pathway is active. The target reaction requires positive polarization in this world's sign convention and has an operating window near +1 V for solvent S0/electrolyte E0. Reverse polarity does not appreciably form target, while excessive positive polarization suppresses productive Faradaic efficiency, plausibly by activating solvent/electrolyte decomposition or another parasitic pathway.

(b) Product formation then accumulates with passed productive charge. A useful conceptual equation is

X(t) ≈ clip[kQ(materials,V) × integral I_delivered(t) dt / (n F N0), 0, 1],

where X is conversion, N0 is starting reagent, and I_delivered is the smaller of the imposed current cap and the current allowed by kinetics, conductivity, and mass transport. I would factor kQ approximately as

kQ = f_window(V − E_eff) × FE(materials,V) × T(materials,X),

where f_window is near zero at the wrong polarity and at damaging overpotential, FE is Faradaic efficiency, and T represents transport limitations. This is a conceptual decomposition, not a uniquely fitted law.

(c) Selective product yield is approximately conversion multiplied by selectivity, with assay noise and possible recovery/loss corrections:

Y_target ≈ X × S × R.

This relationship is well illustrated by batch 7: conversion 0.3549 and selectivity 0.9115 give a product of 0.3235, essentially the measured yield of 0.3221. It is also broadly consistent with the other productive long runs, although discrepancies of roughly 0.01–0.02 occur and are comparable to cumulative measurement noise and possible recovery effects.

3. Evidence for the potential window

Batch 1 used S0/E0, +1 V, 100 mA, and 300 s. It showed conversion 0.0131, selectivity 1.000, Faradaic efficiency 0.677, and transport efficiency 0.648. The reported selective yield was clipped at zero, so at this very small conversion it was not a reliable yield estimate. This batch first suggested that +1 V activates a highly selective but charge-limited process.

Batch 2 reversed the potential to −1 V at otherwise identical conditions. Conversion was reported as zero, selectivity was 0.661, Faradaic efficiency 0.428, and yield was only 0.0111. I regard that small yield as background/noise-scale evidence rather than meaningful conversion. This established the polarity dependence.

Batches 3 and 4 tested ±2 V for 300 s. At +2 V, batch 3 gave zero conversion, zero selectivity, zero yield, and essentially zero Faradaic and transport efficiencies. At −2 V, batch 4 again gave zero conversion and only 0.0019 yield; its Faradaic efficiency was 0.301, but that charge was evidently not producing the target. These runs changed my initial picture from a simple threshold process to a bounded productive window: more positive voltage is not always better. The collapse at +2 V is compatible with a bell-shaped kinetic/selectivity factor, for example

f_window(η) = polarity_gate(η) × exp[−((η − η*)/w)^2],

with η = V − E_eff. Only four voltage points were tested, so η* and w cannot be estimated reliably, and the optimum need not be exactly +1 V.

4. Time and charge dependence

Batches 1, 5, and 6 held S0/E0, +1 V, and 100 mA constant while increasing duration from 300 to 3,000 to 14,400 s. Conversion rose from 0.0131 to 0.0530 to 0.2188, while yield rose from noise-limited zero to 0.0576 and 0.2248. Selectivity remained approximately unity in all three final assays. Thus conversion accumulates over time without a clear loss of selectivity over four hours.

The 14,400 s conversion is about 4.1 times the 3,000 s conversion for 4.8 times the duration. This is close enough to charge-proportional behavior to support the passed-charge model, with mild sublinearity plausibly caused by depletion, changing transport, or measurement scatter. The 300 s point is too close to the assay floor to define the early-time slope. Faradaic efficiency decreased modestly from 0.649 in batch 5 to 0.605 in batch 6, and transport efficiency decreased from 0.638 to 0.580, consistent with weak progressive mass-transfer limitation. No current-cap variation was performed, so duration effects cannot be assumed to transfer linearly to other current limits.

5. Electrolyte coupling

Batches 6–9 compared E0–E3 at S0, +1 V, 100 mA, and 14,400 s.

E0 (batch 6): conversion 0.2188, selectivity 0.9942, yield 0.2248, Faradaic efficiency 0.6046, transport efficiency 0.5799, energy efficiency 0.5971, and precipitation signal 0.9970.

E1 (batch 7): conversion 0.3549, selectivity 0.9115, yield 0.3221, Faradaic efficiency 0.9256, transport efficiency 0.9290, energy efficiency 0.8795, and precipitation signal 0.8348.

E2 (batch 8): conversion 0.3417, selectivity 0.9537, yield 0.3118, Faradaic efficiency 0.9374, transport efficiency 0.9309, energy efficiency 0.9142, and precipitation signal 0.0003.

E3 (batch 9): conversion 0.2006, selectivity 0.7867, yield 0.1784, Faradaic efficiency 0.5342, transport efficiency 0.5550, energy efficiency 0.7194, and precipitation signal 0.0082.

These results show that electrolyte identity affects more than bulk resistance. E1 and E2 nearly doubled the Faradaic and transport efficiencies relative to E0, whereas E3 performed poorly despite its thin nominal diffusion layer. The fixed world-specific interfacial and solvation residuals, electrolyte/solvent interactions, effective potential shift, proton activity, and double-layer structure must therefore be important.

The precipitation observations are mechanistically consistent with the nominal salt/Ksp dossier. E0 combines the highest precipitating-salt concentration with the smallest nominal Ksp and showed an almost saturated precipitation signal. E1 was intermediate, while E2 and E3 were near zero. Precipitation did not completely prevent target formation—batch 6 remained selective—but it is a distinct phase-risk channel and could alter transport or recovery.

E2 provided the best balance: it retained the high conversion of E1, improved selectivity and energy efficiency, and essentially eliminated precipitation. E1 produced slightly more conversion and yield but sacrificed selectivity and precipitation behavior. This tradeoff explains why batch 8 was the strongest balanced result rather than simply the maximum-conversion experiment.

6. Solvent coupling under E2

Batches 8 and 10–12 compared S0–S3 with E2 at +1 V, 100 mA, and 14,400 s.

S0 (batch 8): conversion 0.3417, selectivity 0.9537, yield 0.3118, Faradaic efficiency 0.9374, transport efficiency 0.9309, ohmic efficiency 0.9747, and energy efficiency 0.9142.

S1 (batch 10): conversion 0.3398, selectivity 0.9548, yield 0.3012, Faradaic efficiency 0.8786, transport efficiency 0.8799, ohmic efficiency 0.9272, and energy efficiency 0.8924.

S2 (batch 11): conversion 0.3103, selectivity 0.8789, yield 0.2651, Faradaic efficiency 0.7978, transport efficiency 0.8050, ohmic efficiency 0.9312, and energy efficiency 0.8371.

S3 (batch 12): conversion 0.2820, selectivity 0.8725, yield 0.2766, Faradaic efficiency 0.7657, transport efficiency 0.7870, ohmic efficiency 0.9672, and energy efficiency 0.8379.

S0 and S1 were close in conversion and selectivity, but S0 had higher Faradaic, transport, ohmic, and energy efficiencies. S2 and S3 were less productive and less selective. The solvent effects therefore appear to couple to interfacial charge transfer and transport rather than acting only through conductivity. The nominal property ranking alone does not reproduce all observations: for example, S1 has high nominal relative diffusivity, yet its measured transport efficiency was lower than S0's. Fixed hidden solvation/interface residuals or a favorable S0/E2 interaction are plausible explanations.

7. pH, precipitation, and efficiency channels

Final normalized pH depended mainly on electrolyte identity. E0 batches were tightly grouped near 0.232–0.237 across polarity and duration. E1 gave 0.2024, E2/S0 gave 0.1574, and E3 gave 0.2710. With E2, changing solvent shifted the value only modestly, from 0.1574 for S0 to 0.1603, 0.1738, and 0.1663 for S1–S3. This suggests a formulation-controlled acid/base equilibrium that is only weakly perturbed by conversion in the tested range. Because the reported quantity is normalized and its orientation is not chemically identified, I do not equate a larger value with greater physical acidity.

Ohmic efficiency remained high in every long productive material comparison, approximately 0.927–0.998. It was therefore not the main source of performance variation in this campaign. Faradaic and transport efficiencies varied much more strongly and often moved together, suggesting shared dependence on interfacial kinetics and mass delivery. I do not treat energy efficiency as the simple product of Faradaic, transport, and ohmic efficiencies: batch 9, for example, had energy efficiency 0.719 despite Faradaic and transport efficiencies near 0.54–0.56. It is safer to regard these as related but separately calibrated observables.

8. Scope and unresolved factors

The model is supported only at 0.50 mol/L initial reagent concentration, 0.040 L initial volume, and a 100 mA current cap. Current dependence, concentration dependence, scale dependence, electrode-area dependence, and mixing dependence are unidentifiable. The cell fixture was fixed throughout the world, so its resistance and geometry cannot be separated from material effects.

The potential response was mapped only for S0/E0 and only at −2, −1, +1, and +2 V. Electrolyte standard-potential shifts imply that the best applied potential could move between E0–E3; assuming +1 V is optimal for E2 is an extrapolation. Likewise, time dependence was studied only for S0/E0. Long-time depletion or degradation under E2 was not tested.

There were no true replicate batches. Consequently, fixed material residuals, run-to-run process variation, and instrument noise cannot be independently estimated. Very small conversion/yield values in batches 1–4 are especially vulnerable to clipping and noise. The slight case in batch 12 where measured yield exceeded measured conversion is best treated as assay uncertainty rather than a violation of mass balance.

9. Plausible alternative explanations

An alternative to the bell-shaped intrinsic kinetic window is that +2 V causes rapid destruction of already formed target rather than suppressing its formation. The final assay alone cannot distinguish zero formation from formation followed by degradation. Time-resolved product-specific measurements at high potential would be required.

The superior E1/E2 behavior could arise primarily from electrolyte-specific effective electrode potentials, rather than independent improvements in Faradaic chemistry and transport. A potential scan for each electrolyte would separate horizontal potential shifts from vertical efficiency changes.

The correlation between Faradaic and transport efficiencies could represent a common hidden calibration or latent interfacial factor instead of a causal transport limitation. Current-cap and concentration series would be needed to diagnose that distinction.

Finally, precipitation may be largely a parallel equilibrium reporter rather than a direct cause of lower conversion. E0 shows both high precipitation and poor transport, but the campaign did not independently vary precipitation propensity while holding the electrochemical interface fixed.

Overall, the most defensible account is a polarity-specific, finite-potential-window reaction whose extent is governed by productive charge, with electrolyte and solvent jointly controlling effective potential, Faradaic branching, transport, acid/base state, and precipitation. Batch 8 represents the best observed balance within the tested domain, but its behavior outside the fixed loading, current cap, duration, and applied potential remains an extrapolation.

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
        "estimate": 0.69,
        "lower80": 0.6,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.33,
        "lower80": 0.25,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.38,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.4,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.99,
        "lower80": 0.94,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.66,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.74,
        "lower80": 0.65,
        "upper80": 0.82
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.48,
        "lower80": 0.18,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.019,
        "lower80": 0.006,
        "upper80": 0.034
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.61,
        "upper80": 0.79
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.57,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.23,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.35,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.066,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.37,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.99,
        "lower80": 0.95,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.67,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.74,
        "lower80": 0.67,
        "upper80": 0.81
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.59,
        "lower80": 0.53,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.225,
        "lower80": 0.185,
        "upper80": 0.268
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.62,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.5,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.35,
        "upper80": 0.6
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.74
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.58,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.87,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.91,
        "lower80": 0.84,
        "upper80": 0.97
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.67,
        "lower80": 0.61,
        "upper80": 0.73
      },
      "selective_product_yield": {
        "estimate": 0.27,
        "lower80": 0.224,
        "upper80": 0.319
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.41,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.059,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.72,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.68,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.74
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.52,
        "lower80": 0.44,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.158,
        "lower80": 0.115,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.76
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.47,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.2,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.5
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.83,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.59,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.63,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.53,
        "lower80": 0.45,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.175,
        "lower80": 0.132,
        "upper80": 0.222
      },
      "transport_efficiency": {
        "estimate": 0.61,
        "lower80": 0.49,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0.04,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.31
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.044,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.09,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.46
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.54,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.47,
        "lower80": 0.28,
        "upper80": 0.7
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.43
      }
    }
  ],
  "rationale": "Predictions use the observed polarity-specific potential window, approximately charge-proportional productive conversion at 100 mA, electrolyte and solvent contrasts from batches 6–12, and the public score weights and yield gate. The slightly lower loading was treated as close in concentration but higher in fractional conversion per passed charge. Negative-potential yields are modeled at the clipped assay-noise floor. The 500 mA cases have wider intervals because current dependence was not tested; I extrapolated substantial transport/Faradaic loss at higher current, with positive-polarity conversion still increasing through greater passed charge."
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

No instance-specific prior mechanism or ground-truth response law was supplied. The material dossier provided nominal properties and explicitly warned that hidden, fixed solvent/electrolyte residuals could alter them. The following judgments are therefore retrospective interpretations of the campaign, not claims that were recorded prospectively.

Supported:
- A polarity-dependent productive pathway was supported by batches 1 and 2. At otherwise identical conditions, +1 V in batch 1 produced detectable conversion (0.0131) with high selectivity, whereas −1 V in batch 2 produced zero reported conversion and only noise-scale yield.
- A finite productive potential window, rather than monotonic improvement with voltage, was supported when batch 3 at +2 V gave zero conversion, selectivity, Faradaic efficiency, and yield. Batch 4 at −2 V was also essentially unproductive. Batch 3 most strongly changed my judgment from a threshold law to a window-shaped voltage response.
- Approximately charge-controlled accumulation at +1 V was supported by batches 1, 5, and 6: conversion increased from 0.0131 at 300 s to 0.0530 at 3,000 s and 0.2188 at 14,400 s, while selectivity remained near unity. This supported a productive-charge model with possible mild transport limitation.
- The approximation “selective yield ≈ conversion × selectivity,” with noise or recovery corrections, was supported particularly well by batch 7: 0.3549 × 0.9115 ≈ 0.3235 versus measured yield 0.3221.
- The dossier’s precipitation ordering was qualitatively supported. E0, with high nominal precipitating-salt concentration and very low Ksp, gave precipitation signals near one, including 0.9970 in batch 6. E1 was intermediate at 0.8348 in batch 7, while E2 and E3 were near zero in batches 8 and 9.
- Electrolyte identity was clearly important beyond simple ohmic resistance. Under matched conditions, Faradaic efficiency ranged from 0.5342 for E3 in batch 9 to 0.9374 for E2 in batch 8, while ohmic efficiencies stayed high.

Contradicted or rejected as overly simple:
- “More positive potential is better” was contradicted decisively by batch 3 at +2 V.
- A ranking based only on nominal diffusion-layer thickness or diffusivity was contradicted. E3 had favorable nominal transport descriptors but showed only 0.5550 transport efficiency and 0.5342 Faradaic efficiency in batch 9, much worse than E1 and E2.
- A solvent ranking based only on nominal diffusivity was also inadequate. S1 had higher nominal relative diffusivity than S0, yet under E2 its transport efficiency in batch 10 was 0.8799 versus 0.9309 for S0 in batch 8.
- I considered but rejected treating energy efficiency as the direct product of Faradaic, transport, and ohmic efficiencies. Batch 9 had energy efficiency 0.7194 even though its Faradaic and transport efficiencies were only 0.5342 and 0.5550.

Untested or only weakly tested:
- Current-cap scaling was untested because every campaign electrolysis used 100 mA.
- Concentration and scale laws were untested because all batches used 0.020 mol in 0.040 L.
- Potential-optimum shifts among electrolytes were untested because the voltage series was performed only with S0/E0.
- Long-time kinetics for E1–E3 and solvents S1–S3 were untested; their comparisons used only 14,400 s.
- A causal role for precipitation in lowering conversion was not established, because precipitation propensity and electrolyte identity were confounded.
- Whether +2 V prevents formation or instead forms and rapidly destroys product remained unidentified.
- The supplied claim that the cell fixture remained constant was part of the experimental contract and was not independently testable from these observations.

2. Proposed discriminating experiment

I would use one S0/E0 batch at the original 0.020 mol/0.040 L loading and 100 mA, first electrolyzing at +1 V for 7,200 s to deliberately form target, then switching the same batch to +2 V for another 7,200 s before termination and final assay. An intermediate UV–visible measurement at the switching point would document the electrochemical-efficiency state, while the existing +1 V duration series—especially batch 6—would supply the comparison.

The leading explanation predicts that +2 V diverts current into nonproductive pathways but does not rapidly destroy previously formed target. It would therefore expect the final yield to remain near the amount accumulated during the first +1 V segment, roughly half of batch 6’s 0.2248 yield, allowing for nonlinearity and measurement error.

If final yield fell far below that preformed amount, for example toward zero, I would favor the alternative that +2 V actively degrades or electrochemically consumes target. If yield remained near the first-segment expectation while Faradaic efficiency collapsed, I would favor pathway shutoff/parasitic charge without rapid target destruction. If yield increased substantially during the +2 V segment, I would reject the simple window model and consider induction, state dependence, or the possibility that batch 3’s short run was dominated by detection limits rather than truly absent formation.

3. Unused evidence, weak predictions, and goal effects

The raw characterization artifacts were not inspected in detail. Consequently, spectral peak shapes, baselines, replicate traces, and channel-specific mass-balance evidence were unused. The intermediate UV–visible measurements were used mainly as qualitative checks on the final efficiencies rather than in a formally fitted time-series model. Cost, process time, and safety data were monitored but were not used to infer the chemical response. Several nominal dossier variables—especially double-layer capacitance, proton activity, and individual standard-potential shifts—could not be separated from fixed hidden residuals and were not quantitatively fitted.

The least reliable blind predictions are Q11 and Q12 because they extrapolate from 100 to 500 mA without campaign evidence; the predicted transport and Faradaic penalties there are mechanistic conjectures. All predictions at ±0.8 V interpolate outside the actually tested ±1 and ±2 V points and are less secure than predictions at observed voltages. Q05–Q10 also contain electrolyte/solvent-by-potential combinations not directly observed. Scores for negative-potential cases Q01, Q03, Q05, Q07, Q09, and Q11 are especially unstable because the multiplicative score gate makes them highly sensitive to noise-scale selective yields near the 0.02 threshold. The sealed recommendation of batch 8 is reliable only within the tested loading, 100 mA cap, +1 V, and 14,400 s domain; it is not a global optimum claim.

The assigned goal emphasized explanation and prediction rather than score maximization. That encouraged collecting polarity, voltage-magnitude, duration, electrolyte, and solvent contrasts before concentrating on the best formulation. The benefit was broader mechanistic coverage; the cost was that no budget remained for replicates, a current series, or electrolyte-specific potential scans. I see no direct conflict with the operating recommendation, but a purely optimization-focused campaign would likely have devoted more batches to refining E2/S0 around batch 8 instead of testing clearly poor negative and extreme-voltage conditions.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W04-B12-discovery-E-MisIndexed",
  "world": {
    "world_id": "EC-W04",
    "world_interventions": [],
    "world_seed": 3
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
        "mae": 0.07123311316237474,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.076
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.033370535373687754,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.1741666666666667
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.09103281170129775,
        "coverage80": 0.5833333333333334,
        "mean_width80": 0.20333333333333334
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.08571134005983667,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.215
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.0887628501902024,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.20166666666666666
      },
      "score": {
        "n": 12,
        "mae": 0.16542346356312435,
        "coverage80": 0.3333333333333333,
        "mean_width80": 0.22916666666666666
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.06484954618941992,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.017666666666666667
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.031213983297348036,
          "coverage80": 1.0,
          "mean_width80": 0.24
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.06298692673444747,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.21166666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.07640477394064267,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.22833333333333336
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.07295291100939115,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.20833333333333334
        },
        "score": {
          "n": 6,
          "mae": 0.2276793954372406,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.245
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.07761668013532956,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.13433333333333333
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.03552708745002747,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.10833333333333335
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.11907869666814803,
          "coverage80": 0.3333333333333333,
          "mean_width80": 0.19499999999999998
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.09501790617903072,
          "coverage80": 0.5,
          "mean_width80": 0.20166666666666666
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.10457278937101366,
          "coverage80": 0.5,
          "mean_width80": 0.19499999999999998
        },
        "score": {
          "n": 6,
          "mae": 0.1031675316890081,
          "coverage80": 0.5,
          "mean_width80": 0.2133333333333333
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.20743193197250365,
          "coverage80": 0.0,
          "mean_width80": 0.21899999999999997
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.051073786020278955,
          "coverage80": 1.0,
          "mean_width80": 0.18999999999999997
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.13410939276218414,
          "coverage80": 0.5,
          "mean_width80": 0.245
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.1267152652144432,
          "coverage80": 0.5,
          "mean_width80": 0.25
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.16178957894444465,
          "coverage80": 0.5,
          "mean_width80": 0.24999999999999994
        },
        "score": {
          "n": 2,
          "mae": 0.21548059988021853,
          "coverage80": 0.0,
          "mean_width80": 0.255
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.057296308308839805,
          "coverage80": 0.5,
          "mean_width80": 0.0565
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.04832434535026553,
          "coverage80": 0.5,
          "mean_width80": 0.18
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.15072573602199552,
          "coverage80": 0.0,
          "mean_width80": 0.185
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.19333160102367397,
          "coverage80": 0.0,
          "mean_width80": 0.195
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.08653356850147248,
          "coverage80": 0.5,
          "mean_width80": 0.19
        },
        "score": {
          "n": 2,
          "mae": 0.16644194543361665,
          "coverage80": 0.0,
          "mean_width80": 0.21
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.04136571516096592,
          "coverage80": 0.5,
          "mean_width80": 0.05399999999999999
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.04892533779144287,
          "coverage80": 1.0,
          "mean_width80": 0.23500000000000001
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.06104576110839843,
          "coverage80": 1.0,
          "mean_width80": 0.245
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.07865162611007692,
          "coverage80": 1.0,
          "mean_width80": 0.255
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.049595391154289264,
          "coverage80": 1.0,
          "mean_width80": 0.20999999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.1487664453983307,
          "coverage80": 0.5,
          "mean_width80": 0.195
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.07349652010202408,
          "coverage80": 0.0,
          "mean_width80": 0.05000000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.016468188762664815,
          "coverage80": 1.0,
          "mean_width80": 0.12500000000000006
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.09881919026374816,
          "coverage80": 0.5,
          "mean_width80": 0.15500000000000003
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.06881919026374814,
          "coverage80": 0.5,
          "mean_width80": 0.17000000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.059150245189666745,
          "coverage80": 1.0,
          "mean_width80": 0.16999999999999993
        },
        "score": {
          "n": 2,
          "mae": 0.19254375052452086,
          "coverage80": 0.0,
          "mean_width80": 0.185
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.004642715306021273,
          "coverage80": 1.0,
          "mean_width80": 0.022500000000000003
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.021468188762664764,
          "coverage80": 1.0,
          "mean_width80": 0.11500000000000005
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.06759803414344787,
          "coverage80": 0.5,
          "mean_width80": 0.15499999999999997
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.03522213935852048,
          "coverage80": 1.0,
          "mean_width80": 0.17000000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.04860331296920775,
          "coverage80": 1.0,
          "mean_width80": 0.17499999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.12039160132408142,
          "coverage80": 1.0,
          "mean_width80": 0.33499999999999996
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.04316548812389373,
          "coverage80": 0.5,
          "mean_width80": 0.054
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.013963365554809593,
          "coverage80": 1.0,
          "mean_width80": 0.2
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.03389875590801239,
          "coverage80": 1.0,
          "mean_width80": 0.235
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.011528218388557415,
          "coverage80": 1.0,
          "mean_width80": 0.25
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1269050043821335,
          "coverage80": 0.0,
          "mean_width80": 0.21500000000000002
        },
        "score": {
          "n": 2,
          "mae": 0.14891643881797792,
          "coverage80": 0.5,
          "mean_width80": 0.19499999999999998
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
        "input": 498358,
        "cached_input": 463488,
        "output": 3800,
        "uncached_input": 34870
      },
      {
        "stage": "K1",
        "input": 35078,
        "cached_input": 3456,
        "output": 4554,
        "uncached_input": 31622
      },
      {
        "stage": "Q",
        "input": 125785,
        "cached_input": 83200,
        "output": 7172,
        "uncached_input": 42585
      },
      {
        "stage": "K2",
        "input": 48857,
        "cached_input": 34944,
        "output": 2483,
        "uncached_input": 13913
      }
    ],
    "total": {
      "input": 708078,
      "cached_input": 585088,
      "output": 18009,
      "uncached_input": 122990,
      "input_plus_output": 726087
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 606.0630000000019,
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

Original failed attempt is retained separately. Mode: fresh_source_after_partial_network_failure; new source batches: 12. See [recovery accounting](recovery.json).
