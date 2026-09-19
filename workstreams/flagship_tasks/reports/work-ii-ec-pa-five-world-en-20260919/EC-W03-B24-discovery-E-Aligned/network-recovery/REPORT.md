# EC-W03-B24-discovery-E-Aligned

Development experiment; one independent source session.

Status: failed; completed batches: 24/24; posttests: 2/3.

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
| 1 | {"cost": 0.30107998847961426, "electrochemical_conversion": 0.021278144791722298, "electrochemical_selectivity": 0.5583956837654114, "energy_efficiency": 0.21988677978515625, "faradaic_efficiency": 0.411141037940979, "ohmic_efficiency": 0.9659870862960815, "pH_normalized": 0.23028121888637543, "precipitation_signal": 1.0, "safety_risk": 0.07217483222484589, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.3824372887611389} |
| 2 | {"cost": 0.30107998847961426, "electrochemical_conversion": 0.004870278295129538, "electrochemical_selectivity": 0.8374620079994202, "energy_efficiency": 0.35512781143188477, "faradaic_efficiency": 0.38289520144462585, "ohmic_efficiency": 0.9748249650001526, "pH_normalized": 0.22758588194847107, "precipitation_signal": 1.0, "safety_risk": 0.07217483222484589, "score": 0.32587918639183044, "selective_product_yield": 0.0186315905302763, "transport_efficiency": 0.4091520309448242} |
| 3 | {"cost": 0.30156001448631287, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.0, "ohmic_efficiency": 0.9740350842475891, "pH_normalized": 0.22830086946487427, "precipitation_signal": 0.9871162176132202, "safety_risk": 0.07217483222484589, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0} |
| 4 | {"cost": 0.30156001448631287, "electrochemical_conversion": 0.005110995378345251, "electrochemical_selectivity": 0.4084523618221283, "energy_efficiency": 0.015384434722363949, "faradaic_efficiency": 0.274258553981781, "ohmic_efficiency": 0.9861932396888733, "pH_normalized": 0.2276102900505066, "precipitation_signal": 0.9878644347190857, "safety_risk": 0.07217483222484589, "score": 0.04160572588443756, "selective_product_yield": 0.004131453577429056, "transport_efficiency": 0.24277101457118988} |
| 5 | {"cost": 0.3006240129470825, "electrochemical_conversion": 0.005291064735502005, "electrochemical_selectivity": 0.835480272769928, "energy_efficiency": 0.3394869267940521, "faradaic_efficiency": 0.3926891088485718, "ohmic_efficiency": 0.9731909036636353, "pH_normalized": 0.232571080327034, "precipitation_signal": 0.987190842628479, "safety_risk": 0.07217483222484589, "score": 0.15344582498073578, "selective_product_yield": 0.008956234902143478, "transport_efficiency": 0.3821796476840973} |
| 6 | {"cost": 0.30347999930381775, "electrochemical_conversion": 0.06811419129371643, "electrochemical_selectivity": 0.8230348229408264, "energy_efficiency": 0.36711350083351135, "faradaic_efficiency": 0.413364052772522, "ohmic_efficiency": 0.9750476479530334, "pH_normalized": 0.22929514944553375, "precipitation_signal": 0.9978211522102356, "safety_risk": 0.07217483222484589, "score": 0.37080633640289307, "selective_product_yield": 0.06332369148731232, "transport_efficiency": 0.38868072628974915} |
| 7 | {"cost": 0.3006480038166046, "electrochemical_conversion": 0.01296241208910942, "electrochemical_selectivity": 0.8236761689186096, "energy_efficiency": 0.4166933298110962, "faradaic_efficiency": 0.4484793543815613, "ohmic_efficiency": 1.0, "pH_normalized": 0.2283097356557846, "precipitation_signal": 0.9828632473945618, "safety_risk": 0.07217483222484589, "score": 0.15520109236240387, "selective_product_yield": 0.008414683863520622, "transport_efficiency": 0.45187970995903015} |
| 8 | {"cost": 0.30300000309944153, "electrochemical_conversion": 0.007903870195150375, "electrochemical_selectivity": 0.8219478726387024, "energy_efficiency": 0.06910847872495651, "faradaic_efficiency": 0.08466049283742905, "ohmic_efficiency": 0.8924130201339722, "pH_normalized": 0.22661225497722626, "precipitation_signal": 0.9957361221313477, "safety_risk": 0.07217483222484589, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.07816513627767563} |
| 9 | {"cost": 0.2964800000190735, "electrochemical_conversion": 0.06359576433897018, "electrochemical_selectivity": 0.8096392154693604, "energy_efficiency": 0.40387672185897827, "faradaic_efficiency": 0.38065478205680847, "ohmic_efficiency": 1.0, "pH_normalized": 0.22863508760929108, "precipitation_signal": 1.0, "safety_risk": 0.07217483222484589, "score": 0.37528643012046814, "selective_product_yield": 0.07024093717336655, "transport_efficiency": 0.40148603916168213} |
| 10 | {"cost": 0.2964800000190735, "electrochemical_conversion": 0.19265004992485046, "electrochemical_selectivity": 0.9733767509460449, "energy_efficiency": 0.9434533715248108, "faradaic_efficiency": 0.9556201696395874, "ohmic_efficiency": 0.9634454846382141, "pH_normalized": 0.20117665827274323, "precipitation_signal": 0.8431473970413208, "safety_risk": 0.07217483222484589, "score": 0.6440463066101074, "selective_product_yield": 0.16603240370750427, "transport_efficiency": 0.9569697380065918} |
| 11 | {"cost": 0.2964800000190735, "electrochemical_conversion": 0.18159854412078857, "electrochemical_selectivity": 0.881405234336853, "energy_efficiency": 0.8728576302528381, "faradaic_efficiency": 0.8998115658760071, "ohmic_efficiency": 0.9712008237838745, "pH_normalized": 0.15179164707660675, "precipitation_signal": 0.005239714402705431, "safety_risk": 0.07217483222484589, "score": 0.6028459668159485, "selective_product_yield": 0.15058015286922455, "transport_efficiency": 0.9069915413856506} |
| 12 | {"cost": 0.2964800000190735, "electrochemical_conversion": 0.12182840704917908, "electrochemical_selectivity": 0.8336132764816284, "energy_efficiency": 0.7764626145362854, "faradaic_efficiency": 0.703142523765564, "ohmic_efficiency": 0.9938047528266907, "pH_normalized": 0.27355894446372986, "precipitation_signal": 0.0, "safety_risk": 0.07217483222484589, "score": 0.5284268260002136, "selective_product_yield": 0.12804797291755676, "transport_efficiency": 0.7243674993515015} |
| 13 | {"cost": 0.31248000264167786, "electrochemical_conversion": 0.06863031536340714, "electrochemical_selectivity": 0.8989061117172241, "energy_efficiency": 0.4544335603713989, "faradaic_efficiency": 0.4406810402870178, "ohmic_efficiency": 0.976938009262085, "pH_normalized": 0.23482239246368408, "precipitation_signal": 0.9926277995109558, "safety_risk": 0.09557483345270157, "score": 0.398288756608963, "selective_product_yield": 0.0477677583694458, "transport_efficiency": 0.4305769205093384} |
| 14 | {"cost": 0.31248000264167786, "electrochemical_conversion": 0.16880695521831512, "electrochemical_selectivity": 0.962989091873169, "energy_efficiency": 0.9251410961151123, "faradaic_efficiency": 0.9641196131706238, "ohmic_efficiency": 0.9525253772735596, "pH_normalized": 0.20997990667819977, "precipitation_signal": 0.6583259701728821, "safety_risk": 0.09557483345270157, "score": 0.6389337182044983, "selective_product_yield": 0.17259062826633453, "transport_efficiency": 0.9515993595123291} |
| 15 | {"cost": 0.31248000264167786, "electrochemical_conversion": 0.17664498090744019, "electrochemical_selectivity": 0.9469624161720276, "energy_efficiency": 0.8968172669410706, "faradaic_efficiency": 0.9224323034286499, "ohmic_efficiency": 0.9521773457527161, "pH_normalized": 0.16214023530483246, "precipitation_signal": 0.0, "safety_risk": 0.09557483345270157, "score": 0.616215705871582, "selective_product_yield": 0.15180890262126923, "transport_efficiency": 0.8957552313804626} |
| 16 | {"cost": 0.31248000264167786, "electrochemical_conversion": 0.16415522992610931, "electrochemical_selectivity": 0.9328447580337524, "energy_efficiency": 0.9438522458076477, "faradaic_efficiency": 0.8096321821212769, "ohmic_efficiency": 0.9786503911018372, "pH_normalized": 0.2848714590072632, "precipitation_signal": 0.0, "safety_risk": 0.09557483345270157, "score": 0.5999771952629089, "selective_product_yield": 0.15349483489990234, "transport_efficiency": 0.8056080937385559} |
| 17 | {"cost": 0.34439709782600403, "electrochemical_conversion": 0.05023211985826492, "electrochemical_selectivity": 0.7685509920120239, "energy_efficiency": 0.3840562701225281, "faradaic_efficiency": 0.3966931402683258, "ohmic_efficiency": 0.9657435417175293, "pH_normalized": 0.251470148563385, "precipitation_signal": 0.9807608127593994, "safety_risk": 0.11357483267784119, "score": 0.3502441644668579, "selective_product_yield": 0.02764838933944702, "transport_efficiency": 0.3917269706726074} |
| 18 | {"cost": 0.3450799882411957, "electrochemical_conversion": 0.1818799078464508, "electrochemical_selectivity": 0.8749845027923584, "energy_efficiency": 0.8502261638641357, "faradaic_efficiency": 0.9071586728096008, "ohmic_efficiency": 0.9441109895706177, "pH_normalized": 0.22566556930541992, "precipitation_signal": 0.483462393283844, "safety_risk": 0.11357483267784119, "score": 0.5990545749664307, "selective_product_yield": 0.15987935662269592, "transport_efficiency": 0.8973323106765747} |
| 19 | {"cost": 0.3450799882411957, "electrochemical_conversion": 0.14525501430034637, "electrochemical_selectivity": 0.8428373336791992, "energy_efficiency": 0.7745895981788635, "faradaic_efficiency": 0.809849202632904, "ohmic_efficiency": 0.9220711588859558, "pH_normalized": 0.17546449601650238, "precipitation_signal": 0.0, "safety_risk": 0.11357483267784119, "score": 0.5453628897666931, "selective_product_yield": 0.12547335028648376, "transport_efficiency": 0.7963376641273499} |
| 20 | {"cost": 0.3450799882411957, "electrochemical_conversion": 0.1148219183087349, "electrochemical_selectivity": 0.7905243635177612, "energy_efficiency": 0.6724526286125183, "faradaic_efficiency": 0.5992464423179626, "ohmic_efficiency": 0.9469985365867615, "pH_normalized": 0.2961054742336273, "precipitation_signal": 0.008003811351954937, "safety_risk": 0.11357483267784119, "score": 0.4549877941608429, "selective_product_yield": 0.06873603910207748, "transport_efficiency": 0.5576877593994141} |
| 21 | {"cost": 0.3277340233325958, "electrochemical_conversion": 0.0499991774559021, "electrochemical_selectivity": 0.7316380143165588, "energy_efficiency": 0.48484376072883606, "faradaic_efficiency": 0.47811007499694824, "ohmic_efficiency": 0.9688965678215027, "pH_normalized": 0.23847323656082153, "precipitation_signal": 0.9928951859474182, "safety_risk": 0.12617483735084534, "score": 0.3783102035522461, "selective_product_yield": 0.026016857475042343, "transport_efficiency": 0.48148036003112793} |
| 22 | {"cost": 0.3290799856185913, "electrochemical_conversion": 0.1675146371126175, "electrochemical_selectivity": 0.8360752463340759, "energy_efficiency": 0.818361759185791, "faradaic_efficiency": 0.8787121176719666, "ohmic_efficiency": 0.9628384113311768, "pH_normalized": 0.2143886834383011, "precipitation_signal": 0.5772829651832581, "safety_risk": 0.12617483735084534, "score": 0.5787705183029175, "selective_product_yield": 0.13473822176456451, "transport_efficiency": 0.9095948934555054} |
| 23 | {"cost": 0.3290799856185913, "electrochemical_conversion": 0.1456563025712967, "electrochemical_selectivity": 0.7882827520370483, "energy_efficiency": 0.7391547560691833, "faradaic_efficiency": 0.8082121014595032, "ohmic_efficiency": 0.9609560370445251, "pH_normalized": 0.16279830038547516, "precipitation_signal": 0.0, "safety_risk": 0.12617483735084534, "score": 0.5326947569847107, "selective_product_yield": 0.11497732251882553, "transport_efficiency": 0.806583821773529} |
| 24 | {"cost": 0.3290799856185913, "electrochemical_conversion": 0.09977776557207108, "electrochemical_selectivity": 0.754851758480072, "energy_efficiency": 0.6143904328346252, "faradaic_efficiency": 0.5137226581573486, "ohmic_efficiency": 0.9775200486183167, "pH_normalized": 0.28679168224334717, "precipitation_signal": 0.001529996981844306, "safety_risk": 0.12617483735084534, "score": 0.4277251064777374, "selective_product_yield": 0.06461945921182632, "transport_efficiency": 0.5312683582305908} |

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

1. Experimental scope

All 24 batches used 0.020 mol of limiting reagent in 0.040 L of one solvent, corresponding to a nominal initial concentration of 0.50 mol L^-1. Each electrolysis was divided into two equal time segments with one intermediate measurement between them, followed by termination and a final assay. Thus, material comparisons are internally controlled at a fixed loading and volume, but concentration and dilution effects were not tested.

Batches 1–8 examined potential, duration, and current cap using solvent-S0/electrolyte-E0. Batches 9–24 were a complete 4 × 4 solvent/electrolyte grid at +1.0 V, a 100 mA current cap, and 7200 s total electrolysis. Reported quantities below are final-assay processed estimates unless explicitly described as intermediate measurements.

2. Main empirical picture

I infer that useful target formation occurs inside a fairly narrow positive-potential operating window. Conversion is then controlled jointly by time, charge/transport limitations, electrolyte identity, and solvent–electrolyte coupling. Faradaic and transport efficiencies are especially sensitive to material choice and excessive current. Precipitation and acidity are predominantly electrolyte-controlled, with solvent-dependent modulation. Ohmic efficiency remained comparatively high in almost every tested condition and therefore was usually not the main limitation.

A compact causal sketch is:

material properties + hidden fixed cell properties -> effective formal potential, interfacial kinetics, mass transport, solution resistance, acidity, precipitation

applied potential and current cap -> realized target current, side-reaction current, ohmic loss, heating or polarization

time-integrated target current -> conversion

conversion × product selectivity -> selective product yield

precipitation can additionally reduce active area or transport, although the campaign does not uniquely establish that causal direction.

3. Potential dependence and polarity

The first four batches strongly shaped the potential-window explanation.

At -1.0 V and 100 mA for 1200 s, batch 1 gave conversion 0.0213, selectivity 0.558, faradaic efficiency 0.411, transport efficiency 0.382, and zero reported selective-product yield. Reversing polarity to +1.0 V in batch 2 increased selectivity to 0.837 and gave yield 0.0186 and score 0.326, despite the small and noisy conversion estimate of 0.00487. This showed that positive polarization favors the designated product pathway even when total conversion is near the assay noise floor.

More extreme potentials were detrimental. Batch 3 at +2.0 V produced final estimates of zero conversion, selectivity, faradaic efficiency, transport efficiency, energy efficiency, and yield. Batch 4 at -2.0 V retained only conversion 0.00511, selectivity 0.408, faradaic efficiency 0.274, transport efficiency 0.243, yield 0.00413, and score 0.0416. I therefore reject a monotonic ‘more absolute voltage gives more product’ model. A peaked potential response, with +1 V near the useful window for S0/E0, is much more consistent with the observations.

One possible representation is to define an effective overpotential

eta = V_applied - [E_base + DeltaE_solvent(s) + DeltaE_electrolyte(e) + DeltaE_hidden(s,e)],

where the declared standard-potential shifts provide prior information but hidden campaign-specific residuals remain. Target kinetics could have a finite window such as

j_target = j0(s,e,pH) × exp[-((eta-eta*)/w_target)^2] × f_transport,

while side reactions rise outside that window. The Gaussian form is illustrative rather than identified: a Butler–Volmer target reaction plus rapidly growing competing reactions could generate similar behavior. Only four potentials, all for S0/E0, were tested, so the exact peak, width, asymmetry, and material dependence of the voltage response remain unknown.

The collapse at +2 V could reflect side reactions, passivation, degradation, or an unfavorable effective potential rather than absence of electrochemical current. Likewise, negative-potential conversion may represent unselective consumption or a different product family. Those alternatives cannot be separated because actual current, charge, product identities, and degradation species were not measured.

4. Time dependence

At +1.0 V and 100 mA with S0/E0, batch 5 used only 60 s total and gave conversion 0.00529 and yield 0.00896. Batch 2 used 1200 s and gave conversion 0.00487 and yield 0.0186. Batch 6 used 7200 s and increased conversion to 0.0681 and yield to 0.0633, while retaining selectivity 0.823. Batch 9 repeated the 7200 s S0/E0 condition and gave conversion 0.0636, selectivity 0.810, and yield 0.0702. Agreement between batches 6 and 9 is good relative to the stated assay noise and supports a real time-dependent accumulation process.

The 60 s and 1200 s conversions are too close to zero to establish an early-time rate law. The data are compatible with a lag, a small realized target current, or simple censoring by measurement noise. For interpolation I would use a saturating charge/time expression,

X(t) = X_max(s,e,V,I_cap) × [1-exp(-k_eff t)],

or, more physically,

X = 1-exp[-alpha × integral j_target(t) dt /(n F C0 V_liquid)].

Neither X_max nor k_eff is identifiable from the sparse time series. Extrapolating the approximately tenfold increase from 1200 to 7200 s linearly would be unsafe because reagent depletion, passivation, precipitation, and evolving side reactions should eventually cause saturation.

5. Current-cap and efficiency effects

Batches 2, 7, and 8 compared current caps of 100, 10, and 500 mA at +1.0 V for 1200 s with S0/E0.

Batch 7 at 10 mA had final energy efficiency 0.417, faradaic efficiency 0.448, transport efficiency 0.452, and ohmic efficiency 1.000. Batch 2 at 100 mA gave 0.355, 0.383, 0.409, and 0.975 respectively. Batch 8 at 500 mA deteriorated sharply to energy efficiency 0.0691, faradaic efficiency 0.0847, transport efficiency 0.0782, ohmic efficiency 0.892, and zero reported yield. This is strong evidence that excessive imposed current overwhelms useful transport or interfacial selectivity.

A plausible current model is

j_realized = min(j_cap, j_kinetic, j_lim),

with

j_lim proportional to n F D_eff(s,e) C/delta_eff(s,e).

When the current request approaches or exceeds j_lim, concentration polarization and side reactions reduce both faradaic and transport efficiencies. Ohmic efficiency could be approximated by a decreasing function such as

eta_ohm approximately 1/[1 + I R_cell/|V_applied|],

although the actual current rather than the current cap is required to fit this equation. The high-current observation is qualitatively consistent with it.

At low conversion the yield estimates are noisy: the 10 mA condition had conversion 0.0130 and yield 0.00841, whereas the 100 mA condition had conversion 0.00487 and yield 0.0186. Therefore the campaign supports an efficiency advantage for a low current cap much more clearly than it supports a yield advantage at 1200 s.

Intermediate UV–visible estimates were often higher than final-assay efficiency estimates. For example, batch 2 after 600 s showed energy/faradaic/transport efficiencies of 0.765/0.731/0.774, whereas the final assay after 1200 s gave 0.355/0.383/0.409. Batch 6 after 3600 s showed 0.685/0.748/0.723, followed by final values of 0.367/0.413/0.389 at 7200 s. This might indicate deterioration, depletion, or increasing side reactions with accumulated charge. However, it may also reflect differences between UV–visible and final-assay calibration or their effective sample bases. I therefore treat the direction as suggestive, not as a quantitatively established within-run decay law.

6. Electrolyte effects

The 4 × 4 grid made electrolyte identity the largest reproducible material effect.

At +1.0 V, 100 mA, and 7200 s, electrolyte-E1 was consistently strong. Across solvents S0–S3, E1 gave:

conversion: 0.193, 0.169, 0.182, 0.168;
selectivity: 0.973, 0.963, 0.875, 0.836;
yield: 0.166, 0.173, 0.160, 0.135;
faradaic efficiency: 0.956, 0.964, 0.907, 0.879;
transport efficiency: 0.957, 0.952, 0.897, 0.910.

E2 was generally second-best, with conversions of 0.182, 0.177, 0.145, and 0.146 and yields of 0.151, 0.152, 0.125, and 0.115 across S0–S3. E3 was intermediate and more solvent-sensitive. E0 was weakest: conversions were only 0.0636, 0.0686, 0.0502, and 0.0500, with yields 0.0702, 0.0478, 0.0276, and 0.0260.

These rankings are mechanistically consistent with, but not proved by, the nominal dossier. E1 has the largest declared diffusivity and a relatively thin diffusion layer, which agrees with its high observed transport efficiency. E0 has low diffusivity, the thickest diffusion layer among E0–E2, and severe precipitation, consistent with transport loss. E3 has high nominal conductivity but the thickest declared diffusion layer and did not outperform E1; this illustrates why conductivity alone is not predictive.

I would model the effective rate constant as a coupled quantity rather than an additive material score:

log k_eff = beta0 + beta_s[s] + beta_e[e] + beta_se[s,e] + beta_V eta + beta_V2 eta^2 + beta_I g(I_cap),

and similarly use bounded logistic models for selectivity and efficiency. The interaction term is important because solvent rankings change with electrolyte.

7. Solvent effects and solvent–electrolyte coupling

Solvent-S1 was the strongest general medium in the grid, especially for selectivity. Its final selectivities for E0–E3 were 0.899, 0.963, 0.947, and 0.933. Corresponding S0 values were 0.810, 0.973, 0.881, and 0.834; S2 values were 0.769, 0.875, 0.843, and 0.791; S3 values were 0.732, 0.836, 0.788, and 0.755. Thus S1 particularly improved the E0, E2, and E3 selectivities.

The highest observed selective-product yield was 0.1726 in batch 14 (S1/E1), while the highest score was 0.644 in batch 10 (S0/E1), narrowly above 0.639 in batch 14. Batch 10 benefited from conversion 0.193, selectivity 0.973, and energy efficiency 0.943. Batch 14 had conversion 0.169, selectivity 0.963, and energy efficiency 0.925. This near tie shows that the best solvent depends on whether the emphasis is yield, total balanced score, or robustness.

The dossier suggests possible explanations. S1 has high relative diffusivity, reduced proton activity, and greater nominal solubility product than S0, which could improve mass transfer and suppress some parasitic proton-coupled or precipitation processes. S2 and S3 also have greater nominal salt solubility but lower conductivity or diffusivity factors and positive standard-potential shifts; at a fixed +1 V they may therefore experience a less favorable effective overpotential. These explanations are plausible extrapolations from public nominal properties, not direct measurements of molecular mechanisms.

8. Acidity and precipitation

Normalized pH was primarily electrolyte-dependent and followed a stable order across solvents. E2 was lowest, approximately 0.152–0.175; E1 was about 0.201–0.226; E0 was about 0.229–0.251; and E3 was highest, about 0.274–0.296. This agrees qualitatively with the nominal acid concentrations and pKa values: E2 is the strongest/more concentrated acid profile, whereas E3 is the weakest/dilute profile. Solvent shifts were real but smaller than electrolyte shifts.

Precipitation showed an even sharper electrolyte signature. E0 produced signals near saturation in every solvent: 1.000, 0.993, 0.981, and 0.993 for S0–S3. E2 produced approximately zero in all solvents. E3 was also approximately zero. E1 was intermediate and solvent-dependent: 0.843 in S0, 0.658 in S1, 0.483 in S2, and 0.577 in S3. The trend from S0 toward the more solubilizing solvents broadly matches their declared relative solubility-product factors, although the S2/S3 ordering is not perfectly monotonic and may reflect hidden residuals or noise.

Precipitation plausibly lowers active area or raises the effective diffusion barrier, helping explain the poor E0 performance. However, E0 simultaneously differs in diffusivity, diffusion-layer thickness, potential shift, acidity, and conductivity. The material grid does not isolate precipitation from these correlated electrolyte properties. It could therefore be a marker of the E0 regime rather than the sole cause of poor performance.

9. Yield relationship

A useful first approximation is

Y_selective approximately X_electrochemical × S_electrochemical × r_balance,

where r_balance accounts for recovery, assay noise, or definitions differing slightly between channels. The data broadly follow this relationship but not exactly. For example, batch 10 had X × S = 0.193 × 0.973 = about 0.187, compared with reported yield 0.166. Batch 14 had X × S = about 0.163, compared with yield 0.173. Batch 9 had X × S = about 0.0515, compared with yield 0.0702. Differences of roughly 0.01–0.02 are comparable to low-signal uncertainty and show that the reported channels should not be treated as exact algebraic transforms.

Energy efficiency also covaries with faradaic, transport, and ohmic efficiencies, but it is not their simple product. These should be regarded as coupled indicators produced by a shared electrochemical state rather than forced into an exact identity without calibration data.

10. Scope and predictive use

Within the tested domain, I would predict high performance near positive potentials around +1 V, moderate rather than extreme current, sufficiently long electrolysis, electrolyte-E1, and solvent-S0 or S1. E2 is a plausible second-choice electrolyte, particularly where precipitation avoidance is important. E0 is likely to remain limited by precipitation and transport under similar conditions. Current caps near 500 mA are strongly disfavored for S0/E0, and both +2 and -2 V are outside the demonstrated productive window for that pair.

For quantitative interpolation, I would use a hierarchical model with: (i) a peaked response in effective potential; (ii) a saturating time or charge term; (iii) current limitation through kinetic, transport, and imposed-current minima; (iv) categorical solvent, electrolyte, and interaction effects; and (v) separate bounded models for selectivity, faradaic efficiency, transport efficiency, ohmic efficiency, pH, and precipitation. The final yield would be linked approximately to conversion and selectivity rather than independently extrapolated.

11. Unidentifiable factors and limitations

Several important quantities remain unidentifiable:

- Actual current and passed charge were not reported; only current caps were controlled.
- Electrode area, gap, and contact resistance were fixed within this world but unknown.
- Target, impurity, and degradation species have only public role labels, so molecular reaction steps cannot be assigned.
- Hidden solvent–electrolyte and interface residuals are fixed but unobserved.
- Potential sweeps, duration sweeps, and current sweeps were performed only for S0/E0; their interactions with the other 15 material pairs are extrapolations.
- Concentration, solvent volume, reagent loading, mixing, temperature, and electrode geometry were not varied.
- There was one close process replicate, batches 6 and 9, but no systematic replication of the full grid.
- pH is normalized rather than a directly interpretable physical pH in the final summary, and precipitation is a signal rather than isolated solid mass.
- Intermediate and final instruments have different noise and calibration contracts, limiting direct kinetic comparisons.

Plausible alternative explanations include electrode passivation rather than bulk transport limitation, a material-dependent formal-potential shift rather than intrinsic catalytic activity, precipitation as an innocent correlated marker rather than a cause, and instrument/sample-basis differences rather than true late-time efficiency decay. The present mechanism is therefore a predictive phenomenology of this benchmark world, not a uniquely identified molecular mechanism.

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
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.51
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.12,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.024
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.28,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.78,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.3,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.33,
        "upper80": 0.56
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.35,
        "lower80": 0.15,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.019,
        "lower80": 0.006,
        "upper80": 0.038
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.33,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.13,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.53
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.33,
        "lower80": 0.22,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.035,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.27,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.8,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.37,
        "upper80": 0.66
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.41,
        "upper80": 0.68
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.46,
        "lower80": 0.36,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.075,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.41,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.54,
        "upper80": 0.83
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.75,
        "upper80": 0.99
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.17,
        "lower80": 0.085,
        "upper80": 0.26
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.8,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.97,
        "lower80": 0.92,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.68,
        "lower80": 0.61,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.25,
        "lower80": 0.18,
        "upper80": 0.33
      },
      "transport_efficiency": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.28,
        "upper80": 0.63
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.47,
        "upper80": 0.81
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.7,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.66,
        "lower80": 0.51,
        "upper80": 0.8
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.52,
        "lower80": 0.42,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.1,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.55,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.01,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.26,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.74,
        "lower80": 0.62,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.25,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.29,
        "upper80": 0.54
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.29,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0.02,
        "upper80": 0.2
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.19,
        "lower80": 0.08,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.09,
        "lower80": 0.01,
        "upper80": 0.19
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.71,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.08,
        "lower80": 0.01,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0.01,
        "upper80": 0.2
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.015,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.09,
        "lower80": 0.01,
        "upper80": 0.2
      }
    }
  ],
  "rationale": "Predictions interpolate the S0/E0 potential, time, and current studies and the 4×4 material grid. I treated +0.8 V as near the productive positive window, negative polarity as less selective, E1 as strongly transport- and faradaic-efficient, E3 as moderately effective but disadvantaged at the lower positive potential, S2/E0 as transport-limited, and 500 mA as strongly efficiency-limited. Yield was adjusted upward at long duration for the smaller reagent inventory while preserving the nearly unchanged concentration. Intervals include assay noise and are widened substantially for negative-potential material combinations, long-time extrapolation, and high-current conditions that were not directly crossed in the campaign."
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

```json
null
```

Failure: provider_failure

## Evaluation and resource use

```json
{
  "arm": "Aligned",
  "budget": 24,
  "goal": "discovery",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W03-B24-discovery-E-Aligned",
  "world": {
    "world_id": "EC-W03",
    "world_interventions": [],
    "world_seed": 2
  },
  "status": "failed",
  "source_status": "completed",
  "completed_batches": 24,
  "operations": 192,
  "posttests_completed": 2,
  "exact_replay": {
    "verified": true,
    "checked_steps": 192,
    "max_abs_error": 0.0,
    "mismatches": []
  },
  "failure": {
    "type": "posttest_failure",
    "stage": "K2",
    "message": "provider_failure"
  },
  "source_failure": null,
  "interruption": null,
  "prediction_evaluation": {
    "valid": true,
    "metrics": {
      "selective_product_yield": {
        "n": 12,
        "mae": 0.03825648515120459,
        "coverage80": 0.75,
        "mean_width80": 0.09799999999999999
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.05708664615948994,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.22999999999999998
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.13143836637338002,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.23583333333333337
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.13991147259871164,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.235
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.1268467500557502,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.25416666666666665
      },
      "score": {
        "n": 12,
        "mae": 0.07279172000475227,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.23666666666666666
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.039480398362036796,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.09483333333333333
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.061223395665486645,
          "coverage80": 1.0,
          "mean_width80": 0.3
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.14925149480501812,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.2466666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.1653275231520335,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.24166666666666667
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.08991189256310463,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.26499999999999996
        },
        "score": {
          "n": 6,
          "mae": 0.08184726659829418,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.2633333333333333
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.037032571940372384,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.10116666666666667
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.052949896653493235,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.16
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.11362523794174194,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.225
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.1144954220453898,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.22833333333333336
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.16378160754839577,
          "coverage80": 0.5,
          "mean_width80": 0.24333333333333332
        },
        "score": {
          "n": 6,
          "mae": 0.06373617341121038,
          "coverage80": 1.0,
          "mean_width80": 0.20999999999999996
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.09047701761126518,
          "coverage80": 0.0,
          "mean_width80": 0.09
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.04707179784774779,
          "coverage80": 1.0,
          "mean_width80": 0.27
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.037816433906555175,
          "coverage80": 1.0,
          "mean_width80": 0.185
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.05021056890487671,
          "coverage80": 1.0,
          "mean_width80": 0.185
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.05301664903759956,
          "coverage80": 1.0,
          "mean_width80": 0.15
        },
        "score": {
          "n": 2,
          "mae": 0.05851893752813339,
          "coverage80": 1.0,
          "mean_width80": 0.20499999999999996
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.062015711367130286,
          "coverage80": 0.5,
          "mean_width80": 0.1625
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.08884527444839474,
          "coverage80": 0.5,
          "mean_width80": 0.18499999999999994
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.31445934653282165,
          "coverage80": 0.0,
          "mean_width80": 0.18
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3220652413368225,
          "coverage80": 0.0,
          "mean_width80": 0.16499999999999998
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1869856041669845,
          "coverage80": 0.5,
          "mean_width80": 0.26
        },
        "score": {
          "n": 2,
          "mae": 0.1358544629812241,
          "coverage80": 0.5,
          "mean_width80": 0.22999999999999998
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.015947720184922215,
          "coverage80": 1.0,
          "mean_width80": 0.1275
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.027443346977233884,
          "coverage80": 1.0,
          "mean_width80": 0.255
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.1468276035785675,
          "coverage80": 0.5,
          "mean_width80": 0.31500000000000006
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.1646498560905456,
          "coverage80": 0.5,
          "mean_width80": 0.31499999999999995
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.07041638553142546,
          "coverage80": 1.0,
          "mean_width80": 0.32499999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.049046200513839705,
          "coverage80": 1.0,
          "mean_width80": 0.24999999999999997
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.026729311347007755,
          "coverage80": 1.0,
          "mean_width80": 0.1
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.08479043841362,
          "coverage80": 0.5,
          "mean_width80": 0.20499999999999996
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.053929272294044484,
          "coverage80": 1.0,
          "mean_width80": 0.26
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.06543744981288907,
          "coverage80": 1.0,
          "mean_width80": 0.26
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.13958105981349944,
          "coverage80": 0.5,
          "mean_width80": 0.275
        },
        "score": {
          "n": 2,
          "mae": 0.032123920917510984,
          "coverage80": 1.0,
          "mean_width80": 0.21999999999999997
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.008315959420520812,
          "coverage80": 1.0,
          "mean_width80": 0.028
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.07479043841361999,
          "coverage80": 1.0,
          "mean_width80": 0.2
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.14420333087444306,
          "coverage80": 0.5,
          "mean_width80": 0.22000000000000003
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.15071150839328765,
          "coverage80": 0.5,
          "mean_width80": 0.22999999999999995
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.19193782269954682,
          "coverage80": 0.5,
          "mean_width80": 0.24500000000000002
        },
        "score": {
          "n": 2,
          "mae": 0.11447365595027803,
          "coverage80": 1.0,
          "mean_width80": 0.3
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.026053190976381303,
          "coverage80": 1.0,
          "mean_width80": 0.08
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.019578580856323247,
          "coverage80": 1.0,
          "mean_width80": 0.265
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.09139421105384829,
          "coverage80": 1.0,
          "mean_width80": 0.255
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.08639421105384829,
          "coverage80": 1.0,
          "mean_width80": 0.255
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1191429790854454,
          "coverage80": 0.5,
          "mean_width80": 0.27
        },
        "score": {
          "n": 2,
          "mae": 0.04673314213752747,
          "coverage80": 1.0,
          "mean_width80": 0.21499999999999997
        }
      }
    }
  },
  "token_accounting": {
    "valid": true,
    "complete": false,
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "stages": [
      {
        "stage": "source",
        "input": 569425,
        "cached_input": 503936,
        "output": 3886,
        "uncached_input": 65489
      },
      {
        "stage": "K1",
        "input": 32147,
        "cached_input": 0,
        "output": 5478,
        "uncached_input": 32147
      },
      {
        "stage": "Q",
        "input": 39466,
        "cached_input": 0,
        "output": 5811,
        "uncached_input": 39466
      }
    ],
    "total": {
      "input": 641038,
      "cached_input": 503936,
      "output": 15175,
      "uncached_input": 137102,
      "input_plus_output": 656213
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 662.0310000000027,
  "retest_batches": 1,
  "retest_operations": 8,
  "retest_replay": {
    "verified": true,
    "checked_steps": 8,
    "max_abs_error": 0.0,
    "mismatches": []
  },
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: fresh_source_after_partial_network_failure; new source batches: 24. See [recovery accounting](recovery.json).
