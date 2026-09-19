# EC-W05-B12-optimization-E-MisIndexed

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


Your primary goal is to find an operating procedure maximizing the public balanced-efficiency-v2 score in this electrochemical system. Choose all experiments autonomously. Use measurements and any mechanistic reasoning you find helpful.

## Batch outcomes

| Batch | Final measured outcomes |
| --- | --- |
| 1 | {"cost": 0.35289350152015686, "electrochemical_conversion": 0.03025129623711109, "electrochemical_selectivity": 0.998518168926239, "energy_efficiency": 0.978839635848999, "faradaic_efficiency": 1.0, "ohmic_efficiency": 0.9760997295379639, "pH_normalized": 0.23311282694339752, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.2352813184261322, "selective_product_yield": 0.007860309444367886, "transport_efficiency": 0.9858177900314331} |
| 2 | {"cost": 0.38100001215934753, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.010023192502558231, "energy_efficiency": 0.0, "faradaic_efficiency": 0.0, "ohmic_efficiency": 0.9230774641036987, "pH_normalized": 0.23041747510433197, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.03621342033147812, "selective_product_yield": 0.00897990819066763, "transport_efficiency": 0.02610676921904087} |
| 3 | {"cost": 0.35497406125068665, "electrochemical_conversion": 0.08339525014162064, "electrochemical_selectivity": 0.9748920202255249, "energy_efficiency": 0.9673487544059753, "faradaic_efficiency": 0.9623376131057739, "ohmic_efficiency": 0.9717112183570862, "pH_normalized": 0.23113247752189636, "precipitation_signal": 0.9869203567504883, "safety_risk": 0.07225988060235977, "score": 0.6139007806777954, "selective_product_yield": 0.07706084847450256, "transport_efficiency": 0.9788945317268372} |
| 4 | {"cost": 0.3882000148296356, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02824951522052288, "ohmic_efficiency": 0.8760369420051575, "pH_normalized": 0.2304418981075287, "precipitation_signal": 0.9876685738563538, "safety_risk": 0.07225988060235977, "score": 0.002910616574808955, "selective_product_yield": 0.0007897500181570649, "transport_efficiency": 0.0} |
| 5 | {"cost": 0.42451998591423035, "electrochemical_conversion": 0.0034490374382585287, "electrochemical_selectivity": 0.006436008028686047, "energy_efficiency": 0.0, "faradaic_efficiency": 0.01102422270923853, "ohmic_efficiency": 0.7758153676986694, "pH_normalized": 0.20873160660266876, "precipitation_signal": 0.7142426371574402, "safety_risk": 0.09565988183021545, "score": 0.028481705114245415, "selective_product_yield": 0.0084654176607728, "transport_efficiency": 0.0005147586925886571} |
| 6 | {"cost": 0.4129999876022339, "electrochemical_conversion": 0.551027774810791, "electrochemical_selectivity": 0.7788298726081848, "energy_efficiency": 0.5282812714576721, "faradaic_efficiency": 0.6124841570854187, "ohmic_efficiency": 0.6887727379798889, "pH_normalized": 0.20545567572116852, "precipitation_signal": 0.724872887134552, "safety_risk": 0.09565988183021545, "score": 0.5691964030265808, "selective_product_yield": 0.4354899525642395, "transport_efficiency": 0.5878008008003235} |
| 7 | {"cost": 0.4641999900341034, "electrochemical_conversion": 0.6467952728271484, "electrochemical_selectivity": 0.807762086391449, "energy_efficiency": 0.4922400414943695, "faradaic_efficiency": 0.6844610571861267, "ohmic_efficiency": 0.6391679644584656, "pH_normalized": 0.17166884243488312, "precipitation_signal": 0.0, "safety_risk": 0.11365988105535507, "score": 0.6185644268989563, "selective_product_yield": 0.5227655172348022, "transport_efficiency": 0.6878613829612732} |
| 8 | {"cost": 0.43220001459121704, "electrochemical_conversion": 0.06154044345021248, "electrochemical_selectivity": 0.747082531452179, "energy_efficiency": 0.09069807082414627, "faradaic_efficiency": 0.07939816266298294, "ohmic_efficiency": 0.8538217544555664, "pH_normalized": 0.2831670343875885, "precipitation_signal": 0.00031451715040020645, "safety_risk": 0.12625987827777863, "score": 0.2257225513458252, "selective_product_yield": 0.029258718714118004, "transport_efficiency": 0.07290280610322952} |
| 9 | {"cost": 0.38100001215934753, "electrochemical_conversion": 0.5999608039855957, "electrochemical_selectivity": 0.9434145092964172, "energy_efficiency": 0.7669422626495361, "faradaic_efficiency": 0.636578381061554, "ohmic_efficiency": 0.8018114566802979, "pH_normalized": 0.15447473526000977, "precipitation_signal": 0.008188718929886818, "safety_risk": 0.07225988060235977, "score": 0.6999879479408264, "selective_product_yield": 0.5905436277389526, "transport_efficiency": 0.6574096083641052} |
| 10 | {"cost": 0.4129999876022339, "electrochemical_conversion": 0.7789651155471802, "electrochemical_selectivity": 0.9190443158149719, "energy_efficiency": 0.6235523819923401, "faradaic_efficiency": 0.8276472091674805, "ohmic_efficiency": 0.6657252311706543, "pH_normalized": 0.1538267880678177, "precipitation_signal": 0.0, "safety_risk": 0.09565988183021545, "score": 0.7502031326293945, "selective_product_yield": 0.6848057508468628, "transport_efficiency": 0.8289968371391296} |
| 11 | {"cost": 0.41012001037597656, "electrochemical_conversion": 0.777047336101532, "electrochemical_selectivity": 0.8713827729225159, "energy_efficiency": 0.5766980051994324, "faradaic_efficiency": 0.8208237290382385, "ohmic_efficiency": 0.6432651877403259, "pH_normalized": 0.154811829328537, "precipitation_signal": 0.005239714402705431, "safety_risk": 0.09565988183021545, "score": 0.7297419905662537, "selective_product_yield": 0.6735491752624512, "transport_efficiency": 0.8280036449432373} |
| 12 | {"cost": 0.40724000334739685, "electrochemical_conversion": 0.6128008961677551, "electrochemical_selectivity": 0.8696801662445068, "energy_efficiency": 0.6489384770393372, "faradaic_efficiency": 0.8090742826461792, "ohmic_efficiency": 0.7572410106658936, "pH_normalized": 0.15533214807510376, "precipitation_signal": 0.0, "safety_risk": 0.09565988183021545, "score": 0.7005211710929871, "selective_product_yield": 0.5691672563552856, "transport_efficiency": 0.8302992582321167} |

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

Mechanistic report

1. Scope and evidence base

This account is an empirical mechanism for the bounded synthetic electrochemical world, not a claim about any real solvent, electrolyte, or reaction. All 12 batches used 0.040 mol limiting reagent in 0.080 L solvent. Most used 500 mA and 14,400 s; the main exceptions were batches 1 and 2 (shorter electrolysis) and batch 12 (400 mA). Each batch received one final assay. Thus, material, voltage, time, and current effects are only partially separated, and none of the conditions was replicated.

The strongest observed operating point was batch 10: solvent S1, electrolyte E2, 1.00 V, 500 mA, and 14,400 s. Its score was 0.7502, with conversion 0.7790, selectivity 0.9190, selective-product yield 0.6848, Faradaic efficiency 0.8276, transport efficiency 0.8290, ohmic efficiency 0.6657, and energy efficiency 0.6236.

2. Proposed process structure

I interpret the world as a competition among desired electron transfer, mass transport, ohmic loss, precipitation/passivation, and a steep high-potential parasitic pathway. A useful qualitative model is:

I_effective = min(I_set, I_kinetic(V, medium), I_transport(medium, concentration, time))

rate_target ≈ k_target(medium) × f_target(overpotential) × reactant_available × transport_factor

rate_side ≈ k_side(medium) × f_side(overpotential) + passivation/degradation terms

conversion ≈ 1 − exp(−integral(rate_target + rate_side) dt / initial_reagent)

selectivity ≈ integral(rate_target dt) / integral((rate_target + rate_side) dt)

selective yield ≈ conversion × selectivity × retention/recovery factor + assay/process noise.

The efficiency channels appear related but not identical. Transport efficiency reports how closely reactant delivery supports the requested current; Faradaic efficiency reports the fraction of charge assigned to productive chemistry; ohmic efficiency falls with resistive voltage loss; and energy efficiency combines productive charge use with voltage and resistive penalties. The public score then rewards all of these, with especially high weight on selective-product yield, while imposing a gate when yield is very small.

3. Potential dependence and the narrow productive window

The clearest mechanistic feature is a narrow useful potential region near 1.0 V under the tested conditions. Batch 3 used S0/E0, 1.00 V, 500 mA, and 14,400 s. It retained very high selectivity (0.9749), Faradaic efficiency (0.9623), transport efficiency (0.9789), ohmic efficiency (0.9717), and energy efficiency (0.9673), although conversion was only 0.0834 and yield 0.0771. Its score was 0.6139.

In the same S0/E0 medium, raising the potential to 1.25 V in batch 4 collapsed the observed conversion and selectivity to 0, reduced yield to 0.00079, gave energy and transport efficiencies of 0, and produced a score of only 0.00291. At 2.00 V in batch 2, conversion was again reported as 0, selectivity was 0.0100, Faradaic and energy efficiencies were 0, transport efficiency was 0.0261, and the score was 0.0362. Likewise, S1/E1 at 1.40 V in batch 5 gave conversion 0.00345, selectivity 0.00644, Faradaic efficiency 0.0110, and score 0.0285, whereas the same material pair at 1.00 V in batch 6 gave conversion 0.5510, selectivity 0.7788, yield 0.4355, and score 0.5692.

These observations changed my initial expectation that more positive potential would monotonically accelerate conversion. Instead, I infer that the productive electron-transfer window ends sharply above roughly 1.0 V in the tested media. Beyond it, current is diverted to an unproductive reaction, degradation, severe polarization, or an interface state that blocks productive transport. The final assay does not identify which of these alternatives is responsible. Values such as the small nonzero yield in batch 2 despite reported zero conversion are plausibly assay noise, clipping, or different estimators rather than evidence for a separate productive channel.

A local comparison around the best medium also favors 1.00 V over 0.90 V. Batch 11, using S1/E2 at 0.90 V, had nearly the same conversion as batch 10 (0.7770 versus 0.7790) but lower selectivity (0.8714 versus 0.9190), lower yield (0.6735 versus 0.6848), lower energy efficiency (0.5767 versus 0.6236), and a lower score (0.7297 versus 0.7502). This suggests that 0.90 V is slightly below the optimum for productive selectivity or energetic operation, while potentials of 1.25 V and above are already far beyond the safe productive window. The exact optimum between 0.90 and 1.00 V remains unresolved.

4. Time and charge

Batches 1 and 3 isolate electrolysis duration within S0/E0 at 1.00 V and 500 mA. At 3,600 s, batch 1 showed conversion 0.0303, selectivity 0.9985, yield 0.00786, and score 0.2353. At 14,400 s, batch 3 showed conversion 0.0834, selectivity 0.9749, yield 0.0771, and score 0.6139. The longer run therefore accumulated substantially more product while preserving high efficiencies. The increase is not simply proportional to elapsed time, suggesting kinetic slowdown, depletion, passivation, precipitation, or a nonlinear yield estimator. Batch 1 also lay below the score's selective-yield gate, explaining why its excellent efficiency channels did not translate into a high total score.

No batch tested more than 14,400 s, so I cannot determine whether batch 10 would continue improving, plateau, or degrade at longer times.

5. Electrolyte and solvent effects

E2 was the strongest electrolyte among the tested combinations. Its nominal dossier lists the largest diffusivity (1.25×10^-9 m²/s), intermediate conductivity, moderate acid concentration, and substantially less precipitation tendency than E0. All three 1.00 V, 500 mA, 14,400 s E2 batches were competitive:

• Batch 7, S2/E2: conversion 0.6468, selectivity 0.8078, yield 0.5228, Faradaic efficiency 0.6845, transport efficiency 0.6879, energy efficiency 0.4922, score 0.6186.
• Batch 9, S0/E2: conversion 0.6000, selectivity 0.9434, yield 0.5905, Faradaic efficiency 0.6366, transport efficiency 0.6574, energy efficiency 0.7669, score 0.7000.
• Batch 10, S1/E2: conversion 0.7790, selectivity 0.9190, yield 0.6848, Faradaic efficiency 0.8276, transport efficiency 0.8290, energy efficiency 0.6236, score 0.7502.

These results imply a solvent-electrolyte coupling rather than a single universally best solvent. With E2, S1 produced the greatest conversion, yield, Faradaic efficiency, and transport efficiency. This agrees qualitatively with S1's nominal high relative diffusivity (1.25). S0/E2 sacrificed some conversion and transport but improved selectivity, ohmic efficiency, and energy efficiency, consistent with S0's greater nominal conductivity. S2/E2 was intermediate in conversion but had poorer ohmic and energy efficiencies, consistent with S2's low relative conductivity.

Matched-pair results reinforce that material effects are substantial but do not independently identify electrolyte and solvent contributions. Batch 6 (S1/E1) reached score 0.5692, batch 7 (S2/E2) reached 0.6186, and batch 8 (S3/E3) reached only 0.2257. Batch 8 had conversion 0.0615, yield 0.0293, Faradaic efficiency 0.0794, and transport efficiency 0.0729 despite ohmic efficiency 0.8538. Thus, good bulk conduction or low precipitation alone is insufficient; interfacial kinetics and transport must also match the productive reaction.

6. Precipitation and acid-state indicators

Precipitation correlates strongly with electrolyte identity. E0 batches 1–4 had precipitation signals near 0.987–1.000. E1 batches 5–6 were around 0.714–0.725. E2 batches 7 and 10–12 reported 0, while batch 9 reported only 0.00819. E3 in batch 8 was also near zero (0.000315). This ordering is consistent with the nominal salt concentration and solubility information.

High precipitation plausibly limits accessible electrode area or transport in E0, helping explain why batch 3 retained excellent instantaneous efficiencies but reached only 0.083 conversion after four hours. However, this remains an inference: precipitation was not independently manipulated while all other variables were held fixed, so it may instead be a correlated marker of electrolyte identity.

Final normalized pH values also tracked electrolyte choice: approximately 0.230–0.233 for E0, about 0.205–0.209 for E1, and approximately 0.154–0.155 for E2. E3/S3 gave 0.283. The best conversion occurred in the lower normalized-pH E2 environment, but the experiment does not show whether proton activity directly accelerates the desired process, changes selectivity, or merely covaries with E2's transport properties.

7. Current-density tradeoff

Batch 12 repeated the S1/E2, 1.00 V, 14,400 s region at 400 rather than 500 mA. Relative to batch 10, the lower-current batch improved ohmic efficiency from 0.6657 to 0.7572 and energy efficiency from 0.6236 to 0.6489. Transport efficiency remained similar (0.8303 versus 0.8290). However, conversion fell from 0.7790 to 0.6128, selectivity fell from 0.9190 to 0.8697, yield fell from 0.6848 to 0.5692, and score fell to 0.7005.

This supports an ordinary charge-throughput versus resistive-loss tradeoff: lower current reduces ohmic and energetic penalties, but over the fixed duration it transfers insufficient productive charge to maximize the yield-weighted balanced score. It is not clear why measured Faradaic efficiency was also slightly lower at 400 mA; this could reflect process nonlinearity, assay noise, or an interface that is most selective near the higher rate.

8. Why batch 10 was selected

Batch 10 did not maximize every individual efficiency. Batch 3 had much higher Faradaic, transport, ohmic, and energy efficiencies, and batch 9 had better selectivity and energy efficiency than batch 10. Batch 10 nevertheless achieved the best observed balance because it combined high conversion and yield with still-good selectivity and charge/transport efficiencies. The comparison suggests that the score heavily rewards moving beyond the low-yield regime, after which efficiency tradeoffs matter more smoothly.

The recommended empirical procedure is therefore 0.040 mol reagent in 0.080 L S1, E2 electrolyte, 1.00 V, 500 mA, electrolysis for 14,400 s. This is an interpolation only in the sense that 0.90 and 1.00 V were compared; the exact local optimum has not been mapped.

9. Unidentifiable factors and plausible alternatives

Several mechanisms remain observationally equivalent:

• The high-potential collapse could be chemical degradation, solvent/electrolyte oxidation, gas evolution, electrode passivation, or a synthetic voltage-window penalty. No product-resolved spectrum was used to distinguish them.
• Low conversion in E0 could result from precipitation/passivation, slow intrinsic kinetics, hidden solvent-electrolyte residuals, or limited accessible electrode area.
• The superior S1/E2 result could arise primarily from diffusion, interfacial solvation, hidden kinetic residuals, or a favorable formal-potential shift. The sparse cross-design cannot separate these contributions.
• The common cell fixture was fixed but unknown. Therefore absolute resistance, electrode area, gap, and mass-transfer coefficients cannot be recovered from these observations.
• Final-assay noise and the absence of replicates prevent assigning statistical significance to small differences, especially the 0.0205 score gap between batches 10 and 11.
• Only positive potentials near 1 V were productively examined. Negative potentials, potentials below 0.9 V, the interval from 1.0 to 1.25 V, other currents, other concentrations, mixed solvents, staged potentials, and durations beyond 14,400 s remain outside the evidence.

Accordingly, the report supports a narrow-window, transport-coupled electrochemical model and the specific observed recommendation, but not a universal kinetic law or an identification of the hidden chemical species.

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
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.55,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.5,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.55,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.09,
        "lower80": 0.02,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.0025,
        "lower80": 0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.9,
        "lower80": 0.68,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.78,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.85,
        "lower80": 0.64,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.7,
        "upper80": 1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.45,
        "lower80": 0.23,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.007,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.95,
        "lower80": 0.78,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.73,
        "lower80": 0.5,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.62,
        "upper80": 0.97
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.64,
        "lower80": 0.48,
        "upper80": 0.78
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.055,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.82,
        "lower80": 0.6,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.5,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.18,
        "upper80": 0.68
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.2,
        "upper80": 0.74
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.007,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.22,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.66,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.57,
        "lower80": 0.3,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.43,
        "upper80": 0.93
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.37,
        "lower80": 0.16,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.004,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.47,
        "upper80": 0.95
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0,
        "upper80": 0.01
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.8,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.58,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.7,
        "upper80": 1
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.62,
        "lower80": 0.46,
        "upper80": 0.77
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.028,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.75,
        "upper80": 1
      }
    }
  ],
  "rationale": "The campaign showed productive operation only at positive potentials near 0.9–1.0 V and a sharp collapse outside that window, so negative-potential batches are predicted near the clipped assay floor. Positive 0.8 V batches are extrapolated below the observed optimum: longer duration raises yield, E1 should outperform precipitation-prone E0, and E3 remains transport-limited. Higher current increases charge throughput and predicted yield but carries greater polarization uncertainty. Intervals are deliberately broad because polarity, 0.8 V, the lower loading, and most solvent–electrolyte crosses were not directly tested; they include final-assay noise and mechanism uncertainty."
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

No instance-specific prior response law was supplied. The only priors were the public nominal material dossier, instrument/scoring contracts, and general electrochemical reasoning; the dossier explicitly warned that hidden, fixed residuals and solvent–electrolyte couplings could alter nominal expectations.

Supported:
• Productive performance depends strongly and nonlinearly on potential. At S0/E0, batch 3 at 1.00 V scored 0.6139, whereas batch 4 at 1.25 V scored 0.00291 and batch 2 at 2.00 V scored 0.0362. Batch 6 likewise showed that S1/E1 worked at 1.00 V, while batch 5 at 1.40 V nearly failed. These observations support a narrow productive voltage window with rapidly increasing parasitic behavior above it.
• Longer electrolysis can increase product formation. Holding S0/E0, 1.00 V, and 500 mA fixed, extending the duration from 3,600 s in batch 1 to 14,400 s in batch 3 increased conversion from 0.0303 to 0.0834, yield from 0.00786 to 0.0771, and score from 0.2353 to 0.6139.
• Material properties act through coupled transport, resistance, selectivity, and interfacial effects rather than a single ranking. With E2, S0 in batch 9 favored selectivity and energy efficiency, while S1 in batch 10 favored conversion, yield, Faradaic efficiency, and transport efficiency. Batch 10 consequently produced the best observed balance.
• Lower current reduces some electrical penalties but does not necessarily maximize the balanced score. Relative to batch 10 at 500 mA, batch 12 at 400 mA improved ohmic efficiency from 0.6657 to 0.7572 but reduced yield from 0.6848 to 0.5692 and score from 0.7502 to 0.7005.
• The nominal precipitation ordering was qualitatively supported. E0 batches had precipitation signals near one, E1 batches near 0.72, and E2 batches generally near zero.

Contradicted or revised:
• A simple initial expectation that raising positive potential would monotonically accelerate useful conversion was contradicted decisively by batches 2, 4, and 5. Those failures changed the interpretation from a monotonic kinetic law to a narrow-window model involving parasitic current, degradation, or passivation.
• Nominal conductivity alone did not predict performance. Batch 8 used the nominally high-conductivity E3 family but had transport efficiency 0.0729 and score 0.2257. Conversely, E2 combinations performed well despite only intermediate nominal conductivity.
• A simple rule that lower current should improve the whole efficiency profile was not supported: batch 12 improved ohmic efficiency but had slightly lower measured Faradaic efficiency and substantially lower product yield than batch 10.

Untested:
• The campaign did not establish whether the desired process is impossible at negative potential; no negative-potential experiment was run.
• The exact optimum between 0.90 and 1.00 V, and the location of the collapse between 1.00 and 1.25 V, remain untested.
• No experiment isolated precipitation while holding electrolyte identity and all other properties constant, so precipitation has not been proven causal.
• Absolute kinetic orders, exchange-current relationships, electron stoichiometry, electrode-area effects, and the identities of side products remain unidentified.
• The campaign did not test concentrations other than approximately 0.5 mol/L, durations above 14,400 s, currents below 400 mA, mixed solvents, or staged potentials.

The evidence that most changed my judgment was the sharp batch 3 versus batch 4 contrast, followed by the failure of batch 5 at 1.40 V. The cross-material result in batch 10 then changed the emphasis from finding a universally superior material to optimizing a solvent–electrolyte coupling.

2. Most informative additional experiment

I would run one staged-potential recovery experiment in S0/E0 at the established loading. I would first operate at 1.00 V for a defined period and take a UV–visible efficiency measurement, briefly expose the same batch to 1.25 V, return to 1.00 V for an equal period, take a second UV–visible measurement, then terminate and perform the final assay.

This would distinguish my leading irreversible-passivation/degradation explanation for the high-voltage collapse from the main alternative of a reversible, instantaneous voltage-dependent diversion of current. If efficiencies and productive behavior recovered after returning to 1.00 V, I would favor reversible competition or polarization at high voltage. If the second 1.00 V segment remained strongly impaired relative to the first, I would increase confidence in irreversible passivation, reagent degradation, or persistent interface modification. If the 1.25 V exposure unexpectedly increased later conversion without destroying selectivity, I would reject the simple collapse model and consider induction, surface activation, or time-dependent state changes. The experiment would not by itself distinguish chemical degradation from electrode passivation, but it would resolve the important reversible-versus-persistent distinction.

3. Unused evidence, reliability, and goal effects

Raw spectral shapes, peak assignments, and characterization artifacts were not analyzed; decisions used processed efficiency estimates and final-assay values. No pH-meter measurements were taken. The nominal double-layer capacitance, formal-potential shifts, acid dissociation parameters, diffusion-layer thicknesses, and hidden fixture properties were not quantitatively fitted. Cost and safety observations were monitored but did not drive comparisons because all tested recipes remained well below the safety limit. The intermediate UV–visible measurements were used mainly as consistency checks rather than to construct a time-resolved kinetic model.

The least reliable blind predictions are those for negative potential because polarity was never tested. Predictions at 0.80 V are also extrapolations below the observed 0.90–1.00 V region. Predictions involving S0/E1, S0/E3, and S2/E0 are weak because those exact solvent–electrolyte crosses were absent from the campaign. The blind batches also use lower loading, lower volume, and often 100 mA, all outside the directly studied operating set. Consequently, their interval estimates depend heavily on assumed charge scaling and on the conjectured potential window.

The batch 10 recommendation is more reliable as a choice among the 12 observed batches than as a claim of global optimality. It was not replicated, its score exceeded batch 11 by only about 0.0205, and nearby potentials, currents, and durations were sparsely sampled.

The assigned objective did affect evidence collection. Maximizing the public balanced score encouraged rapid exploitation after batch 10, use of long electrolysis times, and comparison of high-performing material combinations. It discouraged spending scarce batches on negative controls, replicates, detailed potential bracketing, pH measurements, or deliberately diagnostic low-scoring conditions. There was no direct conflict between the goal and honest interpretation, but the resulting evidence is better suited to selecting an operating recipe than to uniquely identifying the mechanism.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "optimization",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W05-B12-optimization-E-MisIndexed",
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
        "mae": 0.09366877961081142,
        "coverage80": 0.16666666666666666,
        "mean_width80": 0.05275
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.32657291313012443,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.22083333333333333
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.2543948229153951,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.24166666666666667
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.2529506320754687,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.24166666666666667
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.2744222554564476,
        "coverage80": 0.3333333333333333,
        "mean_width80": 0.2525
      },
      "score": {
        "n": 12,
        "mae": 0.22717611115177472,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.20916666666666664
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.07031835876001666,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.011666666666666667
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.5838984672228494,
          "coverage80": 0.0,
          "mean_width80": 0.11666666666666665
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.35010011365016297,
          "coverage80": 0.0,
          "mean_width80": 0.07666666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.34832757453123725,
          "coverage80": 0.0,
          "mean_width80": 0.11499999999999999
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.3318703931570053,
          "coverage80": 0.0,
          "mean_width80": 0.056666666666666664
        },
        "score": {
          "n": 6,
          "mae": 0.27111761492490766,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.06833333333333334
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.11701920046160619,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.09383333333333332
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.0692473590373993,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.32499999999999996
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.1586895321806272,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.4066666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.15757368961970009,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.36833333333333335
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.2169741177558899,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.4483333333333333
        },
        "score": {
          "n": 6,
          "mae": 0.18323460737864175,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.35000000000000003
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.16625674265623092,
          "coverage80": 0.0,
          "mean_width80": 0.081
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.3438484907150269,
          "coverage80": 0.5,
          "mean_width80": 0.14999999999999997
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.4475,
          "coverage80": 0.0,
          "mean_width80": 0.18000000000000002
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.46499999999999997,
          "coverage80": 0.0,
          "mean_width80": 0.16999999999999998
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.3719295126199722,
          "coverage80": 0.0,
          "mean_width80": 0.225
        },
        "score": {
          "n": 2,
          "mae": 0.2670615521669388,
          "coverage80": 0.0,
          "mean_width80": 0.185
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.07624784448742866,
          "coverage80": 0.5,
          "mean_width80": 0.10350000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.3064478063583374,
          "coverage80": 0.5,
          "mean_width80": 0.2
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.19942417621612546,
          "coverage80": 0.5,
          "mean_width80": 0.215
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.19442417621612545,
          "coverage80": 0.5,
          "mean_width80": 0.25
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.23380730032920838,
          "coverage80": 0.5,
          "mean_width80": 0.24000000000000002
        },
        "score": {
          "n": 2,
          "mae": 0.18890658259391785,
          "coverage80": 0.5,
          "mean_width80": 0.18500000000000003
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.07737223879992962,
          "coverage80": 0.0,
          "mean_width80": 0.047499999999999994
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.3020390927791595,
          "coverage80": 0.5,
          "mean_width80": 0.29
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.18688658356666565,
          "coverage80": 0.5,
          "mean_width80": 0.31
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.17928070366382598,
          "coverage80": 0.5,
          "mean_width80": 0.34
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.3925922846794129,
          "coverage80": 0.0,
          "mean_width80": 0.28
        },
        "score": {
          "n": 2,
          "mae": 0.21579792380332946,
          "coverage80": 0.5,
          "mean_width80": 0.22999999999999998
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.15019461268186568,
          "coverage80": 0.0,
          "mean_width80": 0.035
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.316447696685791,
          "coverage80": 0.5,
          "mean_width80": 0.16999999999999998
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.25096719682216645,
          "coverage80": 0.5,
          "mean_width80": 0.19000000000000003
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.2709671968221664,
          "coverage80": 0.5,
          "mean_width80": 0.16999999999999998
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.22673336386680604,
          "coverage80": 0.5,
          "mean_width80": 0.21
        },
        "score": {
          "n": 2,
          "mae": 0.27580622255802156,
          "coverage80": 0.5,
          "mean_width80": 0.25
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.007670776705257594,
          "coverage80": 0.5,
          "mean_width80": 0.013000000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.36130380868911743,
          "coverage80": 0.5,
          "mean_width80": 0.285
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.266478425860405,
          "coverage80": 0.5,
          "mean_width80": 0.26499999999999996
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.22887256085872648,
          "coverage80": 0.5,
          "mean_width80": 0.21999999999999997
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.271733363866806,
          "coverage80": 0.5,
          "mean_width80": 0.27
        },
        "score": {
          "n": 2,
          "mae": 0.21525074988603593,
          "coverage80": 0.5,
          "mean_width80": 0.16
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.08427046233415603,
          "coverage80": 0.0,
          "mean_width80": 0.0365
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.3293505835533142,
          "coverage80": 0.0,
          "mean_width80": 0.22999999999999998
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.17511255502700807,
          "coverage80": 0.5,
          "mean_width80": 0.29
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.17915915489196776,
          "coverage80": 0.5,
          "mean_width80": 0.3
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.14973770737648012,
          "coverage80": 0.5,
          "mean_width80": 0.29000000000000004
        },
        "score": {
          "n": 2,
          "mae": 0.20023363590240478,
          "coverage80": 0.5,
          "mean_width80": 0.24499999999999997
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
        "input": 495812,
        "cached_input": 440704,
        "output": 4458,
        "uncached_input": 55108
      },
      {
        "stage": "K1",
        "input": 28828,
        "cached_input": 3456,
        "output": 4018,
        "uncached_input": 25372
      },
      {
        "stage": "Q",
        "input": 34687,
        "cached_input": 0,
        "output": 3528,
        "uncached_input": 34687
      },
      {
        "stage": "K2",
        "input": 38128,
        "cached_input": 28672,
        "output": 1872,
        "uncached_input": 9456
      }
    ],
    "total": {
      "input": 597455,
      "cached_input": 472832,
      "output": 13876,
      "uncached_input": 124623,
      "input_plus_output": 611331
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 470.59300000000076,
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

Original failed attempt is retained separately. Mode: fresh_source; new source batches: 12. See [recovery accounting](recovery.json).
