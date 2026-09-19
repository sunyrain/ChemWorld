# EC-W04-B24-discovery-E-MisIndexed

Development experiment; one independent source session.

Status: completed; completed batches: 24/24; posttests: 3/3.

## Research assignment

You are an autonomous scientist in a simulated electrochemical laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem,
network, repository inspection, external knowledge retrieval, or hidden simulator access.
Read material_information first. The task's research_goal is authoritative for this campaign.
Complete 24 independent batches; repetition is allowed. You have 24 intermediate instrument
uses across the campaign plus 24 final assays. Measurements are optional up to their budget.
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
| 1 | {"cost": 0.28308001160621643, "electrochemical_conversion": 0.012254880741238594, "electrochemical_selectivity": 0.5300162434577942, "energy_efficiency": 0.07954847067594528, "faradaic_efficiency": 0.2973026931285858, "ohmic_efficiency": 0.9740383625030518, "pH_normalized": 0.2343980222940445, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.26859891414642334} |
| 2 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.6608133912086487, "energy_efficiency": 0.2785569429397583, "faradaic_efficiency": 0.4276559054851532, "ohmic_efficiency": 0.9660544395446777, "pH_normalized": 0.23170267045497894, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.21219435334205627, "selective_product_yield": 0.013308212161064148, "transport_efficiency": 0.4539127051830292} |
| 3 | {"cost": 0.2828400135040283, "electrochemical_conversion": 0.0045663961209356785, "electrochemical_selectivity": 0.9767236113548279, "energy_efficiency": 0.6692426204681396, "faradaic_efficiency": 0.6232835054397583, "ohmic_efficiency": 0.952828049659729, "pH_normalized": 0.23241767287254333, "precipitation_signal": 0.9863388538360596, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.6398404240608215} |
| 4 | {"cost": 0.28308001160621643, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02824951522052288, "ohmic_efficiency": 0.9818079471588135, "pH_normalized": 0.23172709345817566, "precipitation_signal": 0.9870871305465698, "safety_risk": 0.07211905717849731, "score": 0.003244747407734394, "selective_product_yield": 0.0007897500181570649, "transport_efficiency": 0.0} |
| 5 | {"cost": 0.2826288044452667, "electrochemical_conversion": 0.0034490374382585287, "electrochemical_selectivity": 0.006436008028686047, "energy_efficiency": 0.0, "faradaic_efficiency": 0.01102422270923853, "ohmic_efficiency": 0.9700276255607605, "pH_normalized": 0.23668788373470306, "precipitation_signal": 0.9864134788513184, "safety_risk": 0.07211905717849731, "score": 0.03505805879831314, "selective_product_yield": 0.0084654176607728, "transport_efficiency": 0.0005147586925886571} |
| 6 | {"cost": 0.28274399042129517, "electrochemical_conversion": 0.0021511756349354982, "electrochemical_selectivity": 0.0042426493018865585, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02405594103038311, "ohmic_efficiency": 0.9718843698501587, "pH_normalized": 0.23341193795204163, "precipitation_signal": 0.997043788433075, "safety_risk": 0.07211905717849731, "score": 0.04372117668390274, "selective_product_yield": 0.010337181389331818, "transport_efficiency": 0.0} |
| 7 | {"cost": 0.2831760048866272, "electrochemical_conversion": 0.010353217832744122, "electrochemical_selectivity": 0.0, "energy_efficiency": 5.735348167945631e-05, "faradaic_efficiency": 0.0021574273705482483, "ohmic_efficiency": 1.0, "pH_normalized": 0.23242653906345367, "precipitation_signal": 0.9820858836174011, "safety_risk": 0.07211905717849731, "score": 0.030644113197922707, "selective_product_yield": 0.007292202208191156, "transport_efficiency": 0.005557783879339695} |
| 8 | {"cost": 0.28432801365852356, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.008051441982388496, "ohmic_efficiency": 0.988741934299469, "pH_normalized": 0.23072905838489532, "precipitation_signal": 0.994958758354187, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0015560885658487678} |
| 9 | {"cost": 0.28265759348869324, "electrochemical_conversion": 0.0025195640046149492, "electrochemical_selectivity": 0.9595815539360046, "energy_efficiency": 0.9981709718704224, "faradaic_efficiency": 0.9392823576927185, "ohmic_efficiency": 1.0, "pH_normalized": 0.23274284601211548, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.5890927314758301, "selective_product_yield": 0.02150890789926052, "transport_efficiency": 0.9601136445999146} |
| 10 | {"cost": 0.2828879952430725, "electrochemical_conversion": 0.037542518228292465, "electrochemical_selectivity": 0.9892414212226868, "energy_efficiency": 0.9746527671813965, "faradaic_efficiency": 0.9598387479782104, "ohmic_efficiency": 0.9786564111709595, "pH_normalized": 0.23042869567871094, "precipitation_signal": 0.9919947981834412, "safety_risk": 0.07211905717849731, "score": 0.5661711096763611, "selective_product_yield": 0.019074155017733574, "transport_efficiency": 0.9611883163452148} |
| 11 | {"cost": 0.2837519943714142, "electrochemical_conversion": 0.07265578955411911, "electrochemical_selectivity": 0.9671278595924377, "energy_efficiency": 0.824368417263031, "faradaic_efficiency": 0.6369022130966187, "ohmic_efficiency": 0.9605938792228699, "pH_normalized": 0.23141373693943024, "precipitation_signal": 0.9998839497566223, "safety_risk": 0.07211905717849731, "score": 0.511482834815979, "selective_product_yield": 0.05936274304986, "transport_efficiency": 0.6440821886062622} |
| 12 | {"cost": 0.2872079908847809, "electrochemical_conversion": 0.04279555752873421, "electrochemical_selectivity": 0.972674548625946, "energy_efficiency": 0.1972682774066925, "faradaic_efficiency": 0.12456215173006058, "ohmic_efficiency": 0.8477790951728821, "pH_normalized": 0.231934055685997, "precipitation_signal": 0.9932199120521545, "safety_risk": 0.07211905717849731, "score": 0.2980195879936218, "selective_product_yield": 0.06966698914766312, "transport_efficiency": 0.1457870900630951} |
| 13 | {"cost": 0.28524959087371826, "electrochemical_conversion": 0.165621817111969, "electrochemical_selectivity": 0.8945451378822327, "energy_efficiency": 0.8707783222198486, "faradaic_efficiency": 0.9041427373886108, "ohmic_efficiency": 0.9706090092658997, "pH_normalized": 0.2016102373600006, "precipitation_signal": 0.8500597476959229, "safety_risk": 0.07211905717849731, "score": 0.5974629521369934, "selective_product_yield": 0.13517504930496216, "transport_efficiency": 0.8940386176109314} |
| 14 | {"cost": 0.3015376031398773, "electrochemical_conversion": 0.13549457490444183, "electrochemical_selectivity": 0.7820049524307251, "energy_efficiency": 0.7403425574302673, "faradaic_efficiency": 0.7892352342605591, "ohmic_efficiency": 0.9382238388061523, "pH_normalized": 0.20529623329639435, "precipitation_signal": 0.7168036103248596, "safety_risk": 0.095519058406353, "score": 0.5238010287284851, "selective_product_yield": 0.11487270891666412, "transport_efficiency": 0.7767149806022644} |
| 15 | {"cost": 0.32765600085258484, "electrochemical_conversion": 0.1689092516899109, "electrochemical_selectivity": 0.8525598049163818, "energy_efficiency": 0.8104576468467712, "faradaic_efficiency": 0.8846709728240967, "ohmic_efficiency": 0.9534428119659424, "pH_normalized": 0.22070665657520294, "precipitation_signal": 0.5592669248580933, "safety_risk": 0.11351905763149261, "score": 0.573547899723053, "selective_product_yield": 0.12989675998687744, "transport_efficiency": 0.8579939007759094} |
| 16 | {"cost": 0.3113679885864258, "electrochemical_conversion": 0.1696721911430359, "electrochemical_selectivity": 0.8768781423568726, "energy_efficiency": 0.8823370337486267, "faradaic_efficiency": 0.8429415225982666, "ohmic_efficiency": 0.9682149291038513, "pH_normalized": 0.21363607048988342, "precipitation_signal": 0.621524453163147, "safety_risk": 0.12611906230449677, "score": 0.5885263681411743, "selective_product_yield": 0.1505831629037857, "transport_efficiency": 0.8389174342155457} |
| 17 | {"cost": 0.3011919856071472, "electrochemical_conversion": 0.15769155323505402, "electrochemical_selectivity": 0.93869948387146, "energy_efficiency": 0.8790280818939209, "faradaic_efficiency": 0.8682445287704468, "ohmic_efficiency": 0.9513875246047974, "pH_normalized": 0.23719489574432373, "precipitation_signal": 0.9862207770347595, "safety_risk": 0.095519058406353, "score": 0.5960285067558289, "selective_product_yield": 0.13657338917255402, "transport_efficiency": 0.8632783889770508} |
| 18 | {"cost": 0.3015376031398773, "electrochemical_conversion": 0.15675918757915497, "electrochemical_selectivity": 0.7743469476699829, "energy_efficiency": 0.7502585649490356, "faradaic_efficiency": 0.7786800861358643, "ohmic_efficiency": 0.9367601275444031, "pH_normalized": 0.20668809115886688, "precipitation_signal": 0.7182646989822388, "safety_risk": 0.095519058406353, "score": 0.5268681049346924, "selective_product_yield": 0.12411195784807205, "transport_efficiency": 0.7688537240028381} |
| 19 | {"cost": 0.3023439943790436, "electrochemical_conversion": 0.17419739067554474, "electrochemical_selectivity": 1.0, "energy_efficiency": 0.9500227570533752, "faradaic_efficiency": 0.9712172150611877, "ohmic_efficiency": 0.936607301235199, "pH_normalized": 0.16396035254001617, "precipitation_signal": 0.0, "safety_risk": 0.095519058406353, "score": 0.6514853239059448, "selective_product_yield": 0.18105658888816833, "transport_efficiency": 0.9577056169509888} |
| 20 | {"cost": 0.3020560145378113, "electrochemical_conversion": 0.13562779128551483, "electrochemical_selectivity": 0.7243726849555969, "energy_efficiency": 0.6904121041297913, "faradaic_efficiency": 0.7171143889427185, "ohmic_efficiency": 0.946834146976471, "pH_normalized": 0.2742166519165039, "precipitation_signal": 0.008003811351954937, "safety_risk": 0.095519058406353, "score": 0.47842198610305786, "selective_product_yield": 0.07761821150779724, "transport_efficiency": 0.6755557060241699} |
| 21 | {"cost": 0.30608800053596497, "electrochemical_conversion": 0.3663586676120758, "electrochemical_selectivity": 1.0, "energy_efficiency": 0.9489791393280029, "faradaic_efficiency": 0.959751546382904, "ohmic_efficiency": 0.9480465054512024, "pH_normalized": 0.16181699931621552, "precipitation_signal": 0.005525000859051943, "safety_risk": 0.095519058406353, "score": 0.7221258878707886, "selective_product_yield": 0.35272344946861267, "transport_efficiency": 0.9631218314170837} |
| 22 | {"cost": 0.3010214865207672, "electrochemical_conversion": 0.11702314764261246, "electrochemical_selectivity": 0.9765258431434631, "energy_efficiency": 0.9555862545967102, "faradaic_efficiency": 0.9580477476119995, "ohmic_efficiency": 0.9617440104484558, "pH_normalized": 0.16302455961704254, "precipitation_signal": 0.002448364859446883, "safety_risk": 0.095519058406353, "score": 0.6251370906829834, "selective_product_yield": 0.1093989685177803, "transport_efficiency": 0.9889305233955383} |
| 23 | {"cost": 0.30004000663757324, "electrochemical_conversion": 0.07773929834365845, "electrochemical_selectivity": 0.6744158864021301, "energy_efficiency": 0.5744202733039856, "faradaic_efficiency": 0.450391560792923, "ohmic_efficiency": 0.8754907250404358, "pH_normalized": 0.16208721697330475, "precipitation_signal": 0.0, "safety_risk": 0.095519058406353, "score": 0.3801021873950958, "selective_product_yield": 0.0534675195813179, "transport_efficiency": 0.44876328110694885} |
| 24 | {"cost": 0.32919201254844666, "electrochemical_conversion": 0.1413060426712036, "electrochemical_selectivity": 0.9043777585029602, "energy_efficiency": 0.876171350479126, "faradaic_efficiency": 0.7426983714103699, "ohmic_efficiency": 0.9330436587333679, "pH_normalized": 0.16427552700042725, "precipitation_signal": 0.001529996981844306, "safety_risk": 0.095519058406353, "score": 0.5561782717704773, "selective_product_yield": 0.11724545061588287, "transport_efficiency": 0.7602440118789673} |

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

1. Evidence base and scope

I completed 24 batches. Every batch used 0.020 mol limiting reagent in 0.040 L of one solvent (nominal initial concentration 0.50 mol L^-1), so the campaign identifies effects of potential, current cap, duration, solvent, electrolyte, and polarity only at that loading. Final-assay estimates are noisy and bounded to [0,1]; values reported as exactly 0 or 1 may be clipped. I therefore treat small differences near zero, and isolated values at unity, cautiously.

The strongest overall observation was batch 21: solvent-S1/electrolyte-E2, +1.30 V, 100 mA cap, 14,400 s. It produced conversion 0.3664, selective-product yield 0.3527, selectivity 1.000, faradaic efficiency 0.9598, transport efficiency 0.9631, ohmic efficiency 0.9480, energy efficiency 0.9490, precipitation signal 0.0055, and score 0.7221. These are synthetic benchmark responses, not claims about a real chemical identity.

2. Central explanatory picture

I infer a potential-controlled electrochemical conversion with two polarity branches. The positive branch is substantially more selective and efficient than the negative branch. Product formation depends on an effective overpotential rather than raw applied potential. Solvent and electrolyte shift the location of the productive potential window, while conductivity, diffusivity, interfacial capacitance, proton activity, precipitation, and fixed latent material residuals alter the attainable current, transport, selectivity, and efficiency.

A useful first-order potential coordinate is

  eta_plus = V - [E_plus,0 + DeltaE_solvent + DeltaE_electrolyte],

where the nominal dossier shifts are used for the two DeltaE terms. The campaign suggests E_plus,0 is approximately +1.0 V. Thus the predicted positive optimum is approximately

  V_plus,opt = 1.0 V + DeltaE_solvent + DeltaE_electrolyte.

For example, S0 has a -0.08 V nominal shift and E0 has -0.12 V, predicting +0.80 V. The E0/S0 current series at +0.80 V indeed gave high selectivity and efficiency. Likewise, the adjusted potentials used in batches 13–20—+0.92 V for E1/S0, +1.02 V for E1/S1, +1.20 V for E1/S2, +1.10 V for E1/S3, +0.90 V for E0/S1, +1.30 V for E2/S1, and +1.20 V for E3/S1—generally placed every material pair in a productive region. This agreement is strong evidence for an approximately additive potential-shift coupling, although those material scans did not independently sweep potential around each predicted optimum, so the exact coefficient of each nominal shift remains uncertain.

The negative branch can be summarized provisionally as

  V_minus,opt approximately -0.8 V + DeltaE_solvent + DeltaE_electrolyte.

This gives -1.0 V for E0/S0 and -0.5 V for E2/S1, matching the two deliberately tested negative-branch conditions. This negative-branch relation is much less securely identified because it rests on only a few potentials.

3. Potential dependence and polarity

Potential response is narrow and non-monotonic. More voltage is not necessarily better. At E0/S0, 100 mA and 600 s:

- Batch 1, -2.0 V: faradaic efficiency 0.2973, transport efficiency 0.2686, energy efficiency 0.0795, selectivity 0.5300, and conversion 0.0123.
- Batch 2, -1.0 V: faradaic efficiency 0.4277, transport efficiency 0.4539, energy efficiency 0.2786, and selectivity 0.6608. Conversion was reported as 0 while yield was 0.0133, an inconsistency at the scale of the endpoint noise.
- Batch 3, +1.0 V: faradaic efficiency 0.6233, transport efficiency 0.6398, energy efficiency 0.6692, and selectivity 0.9767.
- Batch 4, +2.0 V: faradaic efficiency 0.0282, transport and energy efficiency 0, selectivity 0, and conversion 0.

Thus the positive branch is superior near its window, but excessive positive potential activates an unproductive pathway or causes severe polarization. The collapse already appears at +1.20 V for E0/S0: batches 5–8 had final faradaic efficiencies of only 0.0110, 0.0241, 0.0022, and 0.0081 across 60–3,600 s, with essentially zero transport and energy efficiency. Importantly, +1.20 V is not intrinsically bad: it was productive for material pairs whose nominal shifts moved the window there. Batch 15, E1/S2 at +1.20 V, gave conversion 0.1689, selectivity 0.8526, faradaic efficiency 0.8847, and energy efficiency 0.8105. Batch 20, E3/S1 at the same raw voltage, was also productive, though weaker. This contrast is the clearest evidence that effective overpotential, not raw voltage, governs the response.

A possible empirical potential factor is a peaked function such as

  f_plus(eta) = exp[-(eta/w_plus)^2]

combined with an asymmetric high-overpotential penalty. A second, lower-amplitude peak could represent the negative branch:

  f_V(V) = A_plus f_plus(eta_plus) + A_minus exp[-(eta_minus/w_minus)^2],

with A_minus < A_plus. The observations establish the qualitative peaks and asymmetry but do not uniquely distinguish Gaussian peaks from Butler–Volmer kinetics followed by mass-transfer limitation and side-reaction onset.

4. Current, transport, and ohmic coupling

At E0/S0, +0.80 V and 3,600 s, changing the commanded current cap gave:

- Batch 9, 5 mA: conversion 0.0025, yield 0.0215, faradaic efficiency 0.9393, transport efficiency 0.9601, ohmic efficiency 1.000, energy efficiency 0.9982.
- Batch 10, 25 mA: conversion 0.0375, yield 0.0191, faradaic efficiency 0.9598, transport efficiency 0.9612, ohmic efficiency 0.9787, energy efficiency 0.9747.
- Batch 11, 100 mA: conversion 0.0727, yield 0.0594, faradaic efficiency 0.6369, transport efficiency 0.6441, ohmic efficiency 0.9606, energy efficiency 0.8244.
- Batch 12, 400 mA: conversion 0.0428, yield 0.0697, faradaic efficiency 0.1246, transport efficiency 0.1458, ohmic efficiency 0.8478, energy efficiency 0.1973.

The low-current endpoint yields are comparable to assay noise and should not be used literally, but the efficiency trend is clear. Increasing the current cap initially increases conversion rate, then drives transport limitation and faradaic loss; ohmic loss appears later and is milder than the transport penalty. A plausible representation is

  T(I) = 1/[1 + (I/I_lim)^n],
  O(I) approximately 1 - a I R_eff,
  FE = FE_material f_V(V) g(I/I_lim),

where I_lim depends on diffusivity, diffusion-layer thickness, solvent transport factors, reagent concentration, and electrode geometry. Productive charge could then be

  Q_productive = integral I_actual(t) FE(t) T(t) S(t) dt,

and conversion could follow

  X = 1 - exp[-k_Q Q_productive/(n_e F n_0)].

Absolute n_e, electrode area, gap, contact resistance, I_actual, and therefore true current density are unidentifiable from the public observations.

The E2/S1 comparison shows that a larger current cap is not automatically beneficial even for a favorable material. Batch 19 at +1.30 V, 100 mA, and 7,200 s gave conversion 0.1742, yield 0.1811, faradaic efficiency 0.9712, and transport efficiency 0.9577. Batch 22 at the same potential and duration but a 250 mA cap gave lower conversion 0.1170 and yield 0.1094, despite endpoint faradaic and transport estimates still near 0.96–0.99. This could reflect early transient polarization, current clipping, local depletion, or a nonlinear controller response not captured by the endpoint efficiency channels. It is evidence against a model in which commanded current simply multiplies charge at fixed efficiency.

5. Time and charge accumulation

At a well-tuned, moderate-current condition, duration approximately accumulated productive conversion. E2/S1 at +1.30 V and 100 mA gave:

- Batch 19, 7,200 s: conversion 0.1742 and yield 0.1811.
- Batch 21, 14,400 s: conversion 0.3664 and yield 0.3527.

Doubling time approximately doubled conversion and yield while retaining high efficiencies. This is consistent with charge-controlled conversion in the low-to-moderate conversion regime and provides no evidence yet for strong reagent depletion by 36.6% conversion. I would not extrapolate linearly to complete conversion because depletion, product degradation, and mass-transfer changes were not tested beyond 14,400 s.

The duration series in batches 5–8 does not contradict this relationship because it was conducted at an ineffective E0/S0 potential of +1.20 V. Even 3,600 s could not rescue a condition whose faradaic pathway had collapsed. Time and potential therefore couple multiplicatively rather than substituting for each other.

6. Solvent and electrolyte effects

The materials act through at least four coupled roles: potential shift, transport/conductivity, acid environment, and precipitation/solubility. Fixed world-specific latent residuals also matter.

Electrolyte-E2 was the best tested electrolyte when paired with S1 and shifted to +1.30 V. Batch 19 had selectivity clipped at 1.000, faradaic efficiency 0.9712, transport efficiency 0.9577, conversion 0.1742, and essentially no precipitation. E2's dossier combines high bulk conductivity, low precipitating-salt concentration, weak predicted precipitation, low double-layer capacitance, and a +0.28 V potential shift. The experiment supports that overall combination, but it does not identify which descriptor is causal.

At S1, 100 mA and 7,200 s, with potential adjusted by nominal shifts:

- Batch 17, E0 at +0.90 V: conversion 0.1577, selectivity 0.9387, faradaic efficiency 0.8682, precipitation 0.9862.
- Batch 18, E1 at +1.02 V: conversion 0.1568, selectivity 0.7743, faradaic efficiency 0.7787, precipitation 0.7183.
- Batch 19, E2 at +1.30 V: conversion 0.1742, selectivity 1.000, faradaic efficiency 0.9712, precipitation 0.
- Batch 20, E3 at +1.20 V: conversion 0.1356, selectivity 0.7244, faradaic efficiency 0.7171, precipitation 0.0080.

This shows that avoiding precipitation alone is insufficient: E3 had little precipitation but was substantially worse than E2. E2 likely benefits from a favorable combination of interface kinetics, transport, conductivity, and hidden residuals. E0 can remain electrochemically effective despite almost complete precipitation signal, so precipitation is not an absolute shutdown indicator at this loading, though it may remove material, foul surfaces, or limit longer operation.

At E1, 100 mA and 7,200 s, with solvent-adjusted potential:

- Batch 13, S0 at +0.92 V: conversion 0.1656, yield 0.1352, faradaic efficiency 0.9041, precipitation 0.8501.
- Batch 14, S1 at +1.02 V: conversion 0.1355, yield 0.1149, faradaic efficiency 0.7892, precipitation 0.7168.
- Batch 15, S2 at +1.20 V: conversion 0.1689, yield 0.1299, faradaic efficiency 0.8847, precipitation 0.5593.
- Batch 16, S3 at +1.10 V: conversion 0.1697, yield 0.1506, faradaic efficiency 0.8429, precipitation 0.6215.

Solvent therefore shifts potential and changes precipitation without imposing a simple ranking on electrochemical performance. S0 had the highest faradaic efficiency but also the most precipitation; S3 had the highest measured yield in this four-batch comparison. These differences include latent solvent–electrolyte interactions and assay noise.

Safety risk was well below the 0.65 limit in every tested batch, but it varied systematically with solvent at the fixed loading: approximately 0.0721 for S0, 0.0955 for S1, 0.1135 for S2, and 0.1261 for S3. This appears to be primarily a solvent-associated cost/risk term rather than a consequence of conversion because it was stable across conditions using the same solvent.

7. Acid/base and precipitation submodel

Final pH-normalized values were strongly electrolyte-dependent: about 0.23–0.24 for E0, 0.20–0.22 for E1, approximately 0.164 for E2, and 0.274 for E3 in the material scan. These values are consistent with a fixed equilibrium response to each electrolyte/solvent pair at this composition, rather than a strong dependence on electrolysis time. I did not measure time-resolved pH, so whether proton activity directly controls electron-transfer selectivity or merely covaries with electrolyte identity is unresolved.

The precipitation observations broadly track the nominal precipitating-salt and solubility information. E0 produced signals near 1; E1 produced intermediate signals that decreased from S0 toward the higher-solubility-factor solvents; E2 and E3 produced signals near zero. A plausible equilibrium component is

  P = sigmoid[b(log10 IAP - log10 Ksp_eff)],
  Ksp_eff = Ksp_electrolyte × solvent_solubility_factor × latent_pair_factor.

However, the reported precipitation signal is not calibrated to precipitated moles, so this is a qualitative process equation only.

8. Polarity switching and state dependence

Batch 23 tested the negative branch for E2/S1 at -0.50 V, 100 mA, and 7,200 s. It gave conversion 0.0777, selectivity 0.6744, yield 0.0535, faradaic efficiency 0.4504, transport efficiency 0.4488, and energy efficiency 0.5744. This supports a genuine but weaker negative-polarity pathway near the shifted negative optimum.

Batch 24 applied +1.30 V for 3,600 s and then -0.50 V for 3,600 s to E2/S1. Its final conversion was 0.1413, selectivity 0.9044, yield 0.1172, faradaic efficiency 0.7427, transport efficiency 0.7602, and energy efficiency 0.8762. These endpoints lie between the pure positive and pure negative behaviors. The result is broadly consistent with charge-weighted contributions from the two branches and does not reveal catastrophic irreversible poisoning after the polarity reversal. Nevertheless, because there was no intermediate assay between segments and no reverse-order batch, the presence and direction of hysteresis remain unidentifiable.

9. A compact predictive model

For interpolation near the investigated domain, I would use the following pseudocode:

  shift = solvent.standard_potential_shift + electrolyte.standard_potential_shift
  eta_plus  = V - (1.0 + shift)
  eta_minus = V - (-0.8 + shift)

  positive_activity = A_plus(pair) * peaked_response(eta_plus)
  negative_activity = A_minus(pair) * peaked_response(eta_minus)
  branch_activity = positive_activity + negative_activity

  I_lim = C1 * concentration * diffusivity_eff(pair) / diffusion_layer_eff(pair)
  transport = 1 / (1 + (I_command/I_lim)^n)
  ohmic = clipped_function(I_command, conductivity_eff(pair), fixed_cell_resistance)
  faradaic = branch_activity * current_penalty(I_command/I_lim)
  selectivity = polarity_and_pair_selectivity(V, pair) * high_overpotential_penalty(eta)

  productive_rate proportional to I_actual * faradaic * transport * selectivity
  conversion = 1 - exp(-integral(productive_rate) dt / charge_scale)
  selective_yield approximately conversion * selectivity, plus assay/process error

  precipitation = equilibrium_signal(Ksp_eff, ion_activity, solvent)
  energy_efficiency approximately faradaic * voltage_utilization * ohmic_factor,
  with an additional transport/polarization penalty.

This model explains the shifted potential optima, positive/negative asymmetry, current optimum, approximate time accumulation, precipitation differences, and the advantage of E2/S1. It should be treated as a structured hypothesis rather than a fitted quantitative law.

10. What changed my explanation

The early potential sweep changed the initial assumption that conversion would increase monotonically with voltage. Batches 3 and 4 showed a transition from high positive-branch selectivity at +1.0 V to complete collapse at +2.0 V. Batches 5–8 showed that longer duration cannot compensate for a poorly chosen potential.

Batches 9–12 changed the current model from simple charge proportionality to a transport-limited optimum: low current preserved efficiency, 100 mA gave greater conversion with moderate efficiency loss, and 400 mA strongly damaged transport and faradaic efficiency.

Batches 13–20 provided the strongest support for additive nominal potential shifts. Conditions adjusted by the solvent and electrolyte dossier remained productive across widely different raw voltages. They also showed that precipitation and electrochemical quality are distinct axes.

Batches 19 and 21 established useful near-linear time accumulation at the best material/potential/current condition. Batch 22 showed that raising the current cap can reduce rather than accelerate net conversion. Batch 23 confirmed a weaker negative branch, and batch 24 suggested that polarity segments combine approximately rather than causing immediate irreversible failure.

11. Limits, unidentifiable factors, and alternatives

The concentration effect is unidentified because all completed batches used the same reagent and solvent amounts. Temperature, electrode area, gap, surface identity, mixing, electron stoichiometry, actual current trace, and product degradation were not publicly observed. The fixture was fixed within this world, so its resistance and mass-transfer geometry are inseparable from kinetic parameters. Material scans confounded each material with its deliberately shifted potential, which supports the shift hypothesis but cannot precisely estimate material-specific optimum offsets. There were few true replicates, and assay noise is important for conversion and yield near zero.

The additive potential-shift account is not unique. A plausible alternative is that each solvent/electrolyte pair has an unrelated latent optimum that happened to correlate with the nominal shifts. Another is a Butler–Volmer process whose apparent optimum arises from the intersection of desired reaction kinetics, mass-transfer limitation, and a rapidly growing side reaction, rather than an intrinsically Gaussian potential response. The negative response could be a different chemical product pathway, reverse conversion, or the same target reached through another interfacial state; the observable channels do not identify species or electron-transfer steps. High-current losses could reflect concentration polarization, uncompensated resistance, controller clipping, gas or film formation, or transient surface passivation. Precipitation could be a spectator equilibrium rather than the cause of electrochemical losses.

Within the measured domain, the most defensible conclusions are: use material-shifted effective potential rather than raw voltage; operate near the positive branch; avoid excessive overpotential and excessive current cap; regard time as productive only when potential and transport are favorable; and model solvent/electrolyte effects jointly rather than as a single ranking. Extrapolation outside the tested 0.50 mol L^-1 loading, 1–14,400 s duration range, -2.0 to +2.0 V explored potentials, and 5–400 mA informative current range is not justified by this campaign.

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
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.26,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.15,
        "lower80": 0,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.026
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.28,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.9,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.7,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.66,
        "lower80": 0.5,
        "upper80": 0.8
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.42,
        "lower80": 0.13,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.017,
        "lower80": 0.003,
        "upper80": 0.037
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.52,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.35,
        "lower80": 0.26,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.04,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.91,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.91
      },
      "faradaic_efficiency": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.76
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.57,
        "lower80": 0.5,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.15,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.52,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.31,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.3,
        "upper80": 0.62
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.045,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.34,
        "upper80": 0.66
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.74,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.8,
        "lower80": 0.66,
        "upper80": 0.91
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.68,
        "upper80": 0.93
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.6,
        "lower80": 0.51,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.14,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.84,
        "lower80": 0.7,
        "upper80": 0.94
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.21,
        "upper80": 0.52
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.33,
        "lower80": 0.23,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.021,
        "upper80": 0.115
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.24,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.4,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.23,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.21,
        "upper80": 0.56
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.35,
        "lower80": 0.23,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.02,
        "upper80": 0.125
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.24,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.47,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.47,
        "lower80": 0.29,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.26,
        "upper80": 0.58
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.37,
        "lower80": 0.27,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.03,
        "upper80": 0.135
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.28,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.34,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.3,
        "upper80": 0.64
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.032,
        "upper80": 0.145
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.31,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.24
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0.015,
        "upper80": 0.23
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.003,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.26
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.83,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.03,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0.015,
        "upper80": 0.21
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.27,
        "lower80": 0.19,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.02,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.1,
        "lower80": 0.015,
        "upper80": 0.23
      }
    }
  ],
  "rationale": "Predictions use the campaign’s material-shifted potential windows, positive/negative polarity asymmetry, duration-dependent charge accumulation, and strong high-current transport penalty. The new concentration is close to that studied, but the smaller reagent inventory raises expected long-run fractional conversion. Intervals widen for untested material–polarity combinations, short runs near the yield gate, and 500 mA extrapolations."
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

No instance-specific prior law or expected answer was supplied. The material dossier supplied nominal physical properties and potential shifts, explicitly as incomplete mechanistic prior evidence rather than a ranking or complete response law.

Supported claims and self-developed laws:

- An effective-potential description was supported. My approximate law was V_opt,+ ≈ 1.0 V + ΔE_solvent + ΔE_electrolyte. For E0/S0, the two nominal shifts sum to -0.20 V, placing the predicted optimum near +0.80 V; batches 9–12 were productive there. Material scans at their shift-adjusted potentials also remained productive: batches 13–16 covered four solvents with E1, and batches 17–20 covered four electrolytes with S1. Batch 19, E2/S1 at the predicted +1.30 V, was especially strong. This evidence changed my view from treating raw voltage as the main variable to treating overpotential relative to the material pair as central. However, because identity and adjusted potential were changed together, the exact additive coefficients were not independently identified.

- A positive and a weaker negative polarity branch were supported. At E0/S0 and 100 mA for 600 s, batch 3 at +1.0 V had selectivity 0.9767 and faradaic efficiency 0.6233, whereas batch 2 at -1.0 V had selectivity 0.6608 and faradaic efficiency 0.4277. For E2/S1 at 7,200 s, positive batch 19 gave conversion 0.1742 and faradaic efficiency 0.9712, while negative batch 23 gave conversion 0.0777 and faradaic efficiency 0.4504. These comparisons made polarity asymmetry part of the leading explanation.

- A transport-limited current optimum was supported. In batches 9–12 at E0/S0, +0.80 V and 3,600 s, raising the cap from 5 to 400 mA reduced transport efficiency from 0.9601 to 0.1458 and faradaic efficiency from 0.9393 to 0.1246. Conversion rose through 100 mA but then fell from 0.0727 at 100 mA to 0.0428 at 400 mA. This evidence changed my judgment from simple charge proportionality to a coupled kinetic/transport model.

- Productive charge accumulated approximately with time when the condition was well tuned. E2/S1 at +1.30 V and 100 mA gave conversion 0.1742 after 7,200 s in batch 19 and 0.3664 after 14,400 s in batch 21, while maintaining high efficiencies. This supported approximate time proportionality over that limited conversion range.

- The dossier’s qualitative precipitation information was supported. E0 conditions had precipitation signals near one, E1 was intermediate, and E2/E3 were near zero in batches 17–20. With E1, the precipitation signal declined from 0.8501 for S0 in batch 13 to 0.5593 for S2 in batch 15, broadly following the supplied solvent solubility factors. The evidence did not show that precipitation alone controlled performance: batch 17 remained electrochemically effective despite precipitation 0.9862, and low-precipitation E3 in batch 20 was worse than E2 in batch 19.

Contradicted or materially weakened claims:

- A monotonic voltage-benefit law was contradicted. Batch 3 was productive at +1.0 V, but batch 4 at +2.0 V collapsed to essentially zero conversion, selectivity, transport efficiency, and energy efficiency. Batches 5–8 showed that extending time could not rescue E0/S0 at the off-window +1.20 V.

- A model in which commanded current simply multiplies productive charge was contradicted. Besides batches 9–12, batch 22 at 250 mA produced less conversion than batch 19 at 100 mA under otherwise matching E2/S1 conditions and duration: 0.1170 versus 0.1742. The high endpoint efficiencies in batch 22 mean the exact cause—transient polarization, controller clipping, local depletion, or another state effect—remains unresolved.

- A one-dimensional material ranking was contradicted. E0 combined high precipitation with useful electrochemical performance, while E3 combined negligible precipitation with only moderate efficiencies. Solvent rankings also depended on the chosen response: in batches 13–16, S0 had the highest faradaic efficiency, while S3 had the highest measured selective yield.

Untested or inadequately identified claims:

- Concentration and total-volume laws were untested because every research batch used 0.020 mol in 0.040 L.
- The exact Gaussian peak equations, Butler–Volmer parameters, electron stoichiometry, limiting-current equation, actual current trace, electrode area, and resistance were not identified.
- A causal pH effect was untested; pH-normalized values covaried with electrolyte identity, and no time-resolved pH measurements were made.
- A causal role for precipitation, rather than correlation with electrolyte properties, remained untested.
- Polarity hysteresis and reversibility remained uncertain. Batch 24 showed an intermediate endpoint after positive and negative segments, but there was no assay between segments or reverse-order control.
- Depletion, degradation, and linear time scaling beyond batch 21’s 36.6% conversion were untested.
- Exact generalization of the additive shift law to all sixteen solvent/electrolyte pairs was untested.

2. One additional discriminating experiment

I would run one batch at the original campaign loading with solvent-S2/electrolyte-E2, +1.48 V, 100 mA, and 7,200 s, followed by the final assay. This pair was not tested, and +1.48 V follows directly from the additive law: 1.0 + 0.20 V for S2 + 0.28 V for E2. It is deliberately far from the approximately +0.8 V raw optimum observed for E0/S0.

The leading additive-shift explanation predicts that this condition should remain strongly productive, with high selectivity, faradaic efficiency, and transport efficiency, comparable in broad terms to adjusted-potential batches 15 and 19. A high-efficiency result would be difficult to reconcile with the alternative that all materials share a nearly universal raw-voltage optimum around +0.8 to +1.0 V, and it would strengthen the additive-shift law.

If the condition instead collapsed in the manner of batches 4–8, I would substantially reduce confidence in simple additivity and favor a pair-specific optimum or a strong non-additive solvent–electrolyte interaction. An intermediate result would suggest that nominal shifts provide the correct direction but require a coefficient below one or a latent pair correction. One experiment could not rule out an arbitrary pair-specific latent optimum, but this condition maximizes practical separation between the additive prediction and the universal-raw-voltage alternative.

3. Unused evidence, weak predictions, and goal effects

The detailed raw UV-visible spectra and characterization artifacts were not analyzed; I used the processed endpoint estimates. I also did not use the pH meter as an intermediate instrument, so acid/base dynamics were largely unused. Cost observations were secondary to the mechanistic objective. No concentration series, true replicate series, blank electrolysis, no-current control, reverse-order polarity sequence, or time-resolved assay was collected. Very small conversion and yield estimates in batches 1–8 were partly clipped or inconsistent, so they carried little quantitative weight.

The least reliable blind predictions are Q11 and Q12 because 500 mA exceeds the campaign’s highest tested cap of 400 mA; Q11 additionally combines high current with a negative-polarity regime never tested at high current. Q07–Q10 are also weak because they require cross-material and polarity interpolation for combinations not directly studied. Q01 and Q02 have uncertain scores because their short duration places selective yield near the multiplicative scoring gate, where assay noise can cause a large score change. All twelve predictions extrapolate from 0.020 mol/0.040 L to 0.012 mol/0.025 L; the concentrations are similar, but dependence on total reagent inventory and volume was not experimentally separated.

The recommendation based on batch 21 is most reliable as an interpolation within the tested E2/S1 system, not as proof of global optimality. It relies on a single 14,400 s endpoint and lacks a replicate. Longer operation, higher conversion, other loadings, and other untested material pairs could change the ranking.

The assigned goal did affect evidence collection. Because explanation and prediction were primary and public optimization score was secondary, I spent batches on negative polarity, deliberately poor potentials, a current sweep, several materials, and a polarity-switch sequence rather than repeatedly exploiting batch 21’s region. This broadened mechanistic coverage but reduced replication and left concentration effects unexplored. There was no clear conflict between the mechanistic goal and the final operating recommendation: the explanatory campaign identified E2/S1 at its shifted positive window as both informative and the best observed operating region.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 24,
  "goal": "discovery",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W04-B24-discovery-E-MisIndexed",
  "world": {
    "world_id": "EC-W04",
    "world_interventions": [],
    "world_seed": 3
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 24,
  "operations": 170,
  "posttests_completed": 3,
  "exact_replay": {
    "verified": true,
    "checked_steps": 170,
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
        "mae": 0.0375376431918703,
        "coverage80": 0.75,
        "mean_width80": 0.09491666666666666
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.0618726436297099,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.2608333333333333
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.055918294092019406,
        "coverage80": 1.0,
        "mean_width80": 0.2833333333333334
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.054650653650363305,
        "coverage80": 1.0,
        "mean_width80": 0.2920833333333333
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.09644365333020687,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.29583333333333334
      },
      "score": {
        "n": 12,
        "mae": 0.06675613731145859,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.2275
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.02321701425841699,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.082
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.05754025578498841,
          "coverage80": 1.0,
          "mean_width80": 0.31
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.041624994973341614,
          "coverage80": 1.0,
          "mean_width80": 0.28583333333333333
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.044958327064911534,
          "coverage80": 1.0,
          "mean_width80": 0.2966666666666667
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.060160635262727725,
          "coverage80": 1.0,
          "mean_width80": 0.30833333333333335
        },
        "score": {
          "n": 6,
          "mae": 0.046538166205088306,
          "coverage80": 1.0,
          "mean_width80": 0.22499999999999998
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.051858272125323616,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.10783333333333332
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.0662050314744314,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.21166666666666667
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.0702115932106972,
          "coverage80": 1.0,
          "mean_width80": 0.2808333333333333
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.06434298023581507,
          "coverage80": 1.0,
          "mean_width80": 0.28750000000000003
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.13272667139768599,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.2833333333333333
        },
        "score": {
          "n": 6,
          "mae": 0.08697410841782886,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.23
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.10491413533687592,
          "coverage80": 0.0,
          "mean_width80": 0.0735
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.07607378602027898,
          "coverage80": 1.0,
          "mean_width80": 0.27
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.020890607237815856,
          "coverage80": 1.0,
          "mean_width80": 0.20500000000000002
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.013284734785556793,
          "coverage80": 1.0,
          "mean_width80": 0.22750000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.006789578944444666,
          "coverage80": 1.0,
          "mean_width80": 0.25
        },
        "score": {
          "n": 2,
          "mae": 0.05822630167007445,
          "coverage80": 1.0,
          "mean_width80": 0.19999999999999998
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.0107036916911602,
          "coverage80": 1.0,
          "mean_width80": 0.13249999999999998
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.04204327225685123,
          "coverage80": 1.0,
          "mean_width80": 0.25499999999999995
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.03662072837352756,
          "coverage80": 1.0,
          "mean_width80": 0.28500000000000003
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.04662072837352754,
          "coverage80": 1.0,
          "mean_width80": 0.28
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.05099026501178738,
          "coverage80": 1.0,
          "mean_width80": 0.29000000000000004
        },
        "score": {
          "n": 2,
          "mae": 0.028558054566383384,
          "coverage80": 1.0,
          "mean_width80": 0.18500000000000003
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03313428483903408,
          "coverage80": 1.0,
          "mean_width80": 0.0995
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.1050185465812683,
          "coverage80": 1.0,
          "mean_width80": 0.36
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.09047996044158935,
          "coverage80": 1.0,
          "mean_width80": 0.33000000000000007
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.09047996044158937,
          "coverage80": 1.0,
          "mean_width80": 0.34
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.18040460884571077,
          "coverage80": 0.5,
          "mean_width80": 0.36
        },
        "score": {
          "n": 2,
          "mae": 0.07173355460166933,
          "coverage80": 1.0,
          "mean_width80": 0.22499999999999998
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.030496520102024076,
          "coverage80": 1.0,
          "mean_width80": 0.125
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.013531811237335212,
          "coverage80": 1.0,
          "mean_width80": 0.175
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.06881919026374816,
          "coverage80": 1.0,
          "mean_width80": 0.255
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.05881919026374818,
          "coverage80": 1.0,
          "mean_width80": 0.27
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.09415024518966672,
          "coverage80": 1.0,
          "mean_width80": 0.24000000000000005
        },
        "score": {
          "n": 2,
          "mae": 0.04054375052452086,
          "coverage80": 1.0,
          "mean_width80": 0.17
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.006142715306021273,
          "coverage80": 1.0,
          "mean_width80": 0.03
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.028531811237335225,
          "coverage80": 1.0,
          "mean_width80": 0.185
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.05259803414344788,
          "coverage80": 1.0,
          "mean_width80": 0.29500000000000004
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.04759806394577029,
          "coverage80": 1.0,
          "mean_width80": 0.30499999999999994
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.07064164638519285,
          "coverage80": 1.0,
          "mean_width80": 0.285
        },
        "score": {
          "n": 2,
          "mae": 0.1303916013240814,
          "coverage80": 1.0,
          "mean_width80": 0.37
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03983451187610626,
          "coverage80": 0.5,
          "mean_width80": 0.109
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.10603663444519046,
          "coverage80": 0.5,
          "mean_width80": 0.32
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.06610124409198762,
          "coverage80": 1.0,
          "mean_width80": 0.32999999999999996
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.07110124409198762,
          "coverage80": 1.0,
          "mean_width80": 0.32999999999999996
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.17568557560443876,
          "coverage80": 0.5,
          "mean_width80": 0.35
        },
        "score": {
          "n": 2,
          "mae": 0.07108356118202208,
          "coverage80": 0.5,
          "mean_width80": 0.215
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
        "input": 405523,
        "cached_input": 354304,
        "output": 4704,
        "uncached_input": 51219
      },
      {
        "stage": "K1",
        "input": 28382,
        "cached_input": 0,
        "output": 5867,
        "uncached_input": 28382
      },
      {
        "stage": "Q",
        "input": 36090,
        "cached_input": 0,
        "output": 4890,
        "uncached_input": 36090
      },
      {
        "stage": "K2",
        "input": 40893,
        "cached_input": 3456,
        "output": 2916,
        "uncached_input": 37437
      }
    ],
    "total": {
      "input": 510888,
      "cached_input": 357760,
      "output": 18377,
      "uncached_input": 153128,
      "input_plus_output": 529265
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 699.3589999999967,
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
