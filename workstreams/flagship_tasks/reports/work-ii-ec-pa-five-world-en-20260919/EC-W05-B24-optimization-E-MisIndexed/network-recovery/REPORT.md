# EC-W05-B24-optimization-E-MisIndexed

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


Your primary goal is to find an operating procedure maximizing the public balanced-efficiency-v2 score in this electrochemical system. Choose all experiments autonomously. Use measurements and any mechanistic reasoning you find helpful.

## Batch outcomes

| Batch | Final measured outcomes |
| --- | --- |
| 1 | {"cost": 0.35363999009132385, "electrochemical_conversion": 0.026980267837643623, "electrochemical_selectivity": 0.6436758041381836, "energy_efficiency": 0.30345389246940613, "faradaic_efficiency": 0.43117836117744446, "ohmic_efficiency": 0.9602119326591492, "pH_normalized": 0.23311282694339752, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.402474582195282} |
| 2 | {"cost": 0.35363999009132385, "electrochemical_conversion": 0.037711601704359055, "electrochemical_selectivity": 0.9981916546821594, "energy_efficiency": 0.9446178078651428, "faradaic_efficiency": 0.9809096455574036, "ohmic_efficiency": 0.9690497517585754, "pH_normalized": 0.23041747510433197, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.6066840291023254, "selective_product_yield": 0.05419439822435379, "transport_efficiency": 1.0} |
| 3 | {"cost": 0.36371999979019165, "electrochemical_conversion": 0.04349170997738838, "electrochemical_selectivity": 0.49594420194625854, "energy_efficiency": 0.07126735150814056, "faradaic_efficiency": 0.2352343499660492, "ohmic_efficiency": 0.9558234214782715, "pH_normalized": 0.23113247752189636, "precipitation_signal": 0.9869203567504883, "safety_risk": 0.07225988060235977, "score": 0.15803954005241394, "selective_product_yield": 0.014139342121779919, "transport_efficiency": 0.25179123878479004} |
| 4 | {"cost": 0.36371999979019165, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02824951522052288, "ohmic_efficiency": 0.9679815173149109, "pH_normalized": 0.2304418981075287, "precipitation_signal": 0.9876685738563538, "safety_risk": 0.07225988060235977, "score": 0.00320106977596879, "selective_product_yield": 0.0007897500181570649, "transport_efficiency": 0.0} |
| 5 | {"cost": 0.3928399980068207, "electrochemical_conversion": 0.04687974601984024, "electrochemical_selectivity": 0.4296277165412903, "energy_efficiency": 0.06839850544929504, "faradaic_efficiency": 0.24382568895816803, "ohmic_efficiency": 0.9150911569595337, "pH_normalized": 0.20873160660266876, "precipitation_signal": 0.7142426371574402, "safety_risk": 0.09565988183021545, "score": 0.21324338018894196, "selective_product_yield": 0.02684493362903595, "transport_efficiency": 0.23331621289253235} |
| 6 | {"cost": 0.3928399980068207, "electrochemical_conversion": 0.0021511756349354982, "electrochemical_selectivity": 0.0042426493018865585, "energy_efficiency": 0.0, "faradaic_efficiency": 0.02405594103038311, "ohmic_efficiency": 0.9169479012489319, "pH_normalized": 0.20545567572116852, "precipitation_signal": 0.724872887134552, "safety_risk": 0.09565988183021545, "score": 0.04144962131977081, "selective_product_yield": 0.010337181389331818, "transport_efficiency": 0.0} |
| 7 | {"cost": 0.4440400004386902, "electrochemical_conversion": 0.05614680424332619, "electrochemical_selectivity": 0.43551111221313477, "energy_efficiency": 0.12413156777620316, "faradaic_efficiency": 0.24762462079524994, "ohmic_efficiency": 0.9268651008605957, "pH_normalized": 0.17166884243488312, "precipitation_signal": 0.0, "safety_risk": 0.11365988105535507, "score": 0.22672826051712036, "selective_product_yield": 0.02733507752418518, "transport_efficiency": 0.25102499127388} |
| 8 | {"cost": 0.4440400004386902, "electrochemical_conversion": 0.16580143570899963, "electrochemical_selectivity": 0.8398118615150452, "energy_efficiency": 0.7522996068000793, "faradaic_efficiency": 0.9236548542976379, "ohmic_efficiency": 0.9121610522270203, "pH_normalized": 0.16997136175632477, "precipitation_signal": 0.00031451715040020645, "safety_risk": 0.11365988105535507, "score": 0.5679928660392761, "selective_product_yield": 0.12356206774711609, "transport_efficiency": 0.9171594977378845} |
| 9 | {"cost": 0.41203999519348145, "electrochemical_conversion": 0.03194687142968178, "electrochemical_selectivity": 0.4103149473667145, "energy_efficiency": 0.12149353325366974, "faradaic_efficiency": 0.1727837771177292, "ohmic_efficiency": 0.9862640500068665, "pH_normalized": 0.28518083691596985, "precipitation_signal": 0.008188718929886818, "safety_risk": 0.12625987827777863, "score": 0.21139000356197357, "selective_product_yield": 0.03142451122403145, "transport_efficiency": 0.19361504912376404} |
| 10 | {"cost": 0.41203999519348145, "electrochemical_conversion": 0.04921839386224747, "electrochemical_selectivity": 0.8428930640220642, "energy_efficiency": 0.19145840406417847, "faradaic_efficiency": 0.19046550989151, "ohmic_efficiency": 0.9457149505615234, "pH_normalized": 0.2828666865825653, "precipitation_signal": 0.0, "safety_risk": 0.12625987827777863, "score": 0.28540366888046265, "selective_product_yield": 0.025448516011238098, "transport_efficiency": 0.1918150931596756} |
| 11 | {"cost": 0.3694800138473511, "electrochemical_conversion": 0.18432512879371643, "electrochemical_selectivity": 0.9245491623878479, "energy_efficiency": 0.3428327739238739, "faradaic_efficiency": 0.185390442609787, "ohmic_efficiency": 0.7472465634346008, "pH_normalized": 0.23012854158878326, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.3581373691558838, "selective_product_yield": 0.16104647517204285, "transport_efficiency": 0.19257038831710815} |
| 12 | {"cost": 0.3752399981021881, "electrochemical_conversion": 0.15446490049362183, "electrochemical_selectivity": 0.9587783217430115, "energy_efficiency": 0.2502397894859314, "faradaic_efficiency": 0.14907364547252655, "ohmic_efficiency": 0.8244455456733704, "pH_normalized": 0.23064886033535004, "precipitation_signal": 0.9938013553619385, "safety_risk": 0.07225988060235977, "score": 0.35102710127830505, "selective_product_yield": 0.17784513533115387, "transport_efficiency": 0.17029859125614166} |
| 13 | {"cost": 0.35497406125068665, "electrochemical_conversion": 0.08839622139930725, "electrochemical_selectivity": 0.9853902459144592, "energy_efficiency": 0.9835455417633057, "faradaic_efficiency": 1.0, "ohmic_efficiency": 0.9965339303016663, "pH_normalized": 0.23034444451332092, "precipitation_signal": 0.9979678392410278, "safety_risk": 0.07225988060235977, "score": 0.6254199743270874, "selective_product_yield": 0.07395927608013153, "transport_efficiency": 0.9932950735092163} |
| 14 | {"cost": 0.38675999641418457, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.015194874256849289, "ohmic_efficiency": 0.8612144589424133, "pH_normalized": 0.23075193166732788, "precipitation_signal": 0.9940358996391296, "safety_risk": 0.07225988060235977, "score": 0.0033725472167134285, "selective_product_yield": 0.0009463887545280159, "transport_efficiency": 0.0026746313087642193} |
| 15 | {"cost": 0.3522576093673706, "electrochemical_conversion": 0.008836690336465836, "electrochemical_selectivity": 0.984795868396759, "energy_efficiency": 0.9840731024742126, "faradaic_efficiency": 1.0, "ohmic_efficiency": 1.0, "pH_normalized": 0.23348967730998993, "precipitation_signal": 0.9895151853561401, "safety_risk": 0.07225988060235977, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.9767414331436157} |
| 16 | {"cost": 0.3527759909629822, "electrochemical_conversion": 0.031055469065904617, "electrochemical_selectivity": 0.9820688366889954, "energy_efficiency": 1.0, "faradaic_efficiency": 0.98900306224823, "ohmic_efficiency": 1.0, "pH_normalized": 0.23456893861293793, "precipitation_signal": 0.993626594543457, "safety_risk": 0.07225988060235977, "score": 0.6066761612892151, "selective_product_yield": 0.030273331329226494, "transport_efficiency": 0.984978973865509} |
| 17 | {"cost": 0.3550800085067749, "electrochemical_conversion": 0.09195069968700409, "electrochemical_selectivity": 1.0, "energy_efficiency": 0.9719877243041992, "faradaic_efficiency": 1.0, "ohmic_efficiency": 0.9843316078186035, "pH_normalized": 0.23256264626979828, "precipitation_signal": 0.9913386702537537, "safety_risk": 0.07225988060235977, "score": 0.6282329559326172, "selective_product_yield": 0.08164391666650772, "transport_efficiency": 1.0} |
| 18 | {"cost": 0.3579599857330322, "electrochemical_conversion": 0.18322151899337769, "electrochemical_selectivity": 0.9735657572746277, "energy_efficiency": 0.9591848254203796, "faradaic_efficiency": 0.9205260276794434, "ohmic_efficiency": 0.9568034410476685, "pH_normalized": 0.23214378952980042, "precipitation_signal": 0.9954969882965088, "safety_risk": 0.07225988060235977, "score": 0.6400207877159119, "selective_product_yield": 0.17902889847755432, "transport_efficiency": 0.9106996655464172} |
| 19 | {"cost": 0.35738399624824524, "electrochemical_conversion": 0.16348811984062195, "electrochemical_selectivity": 0.9937134385108948, "energy_efficiency": 0.9452802538871765, "faradaic_efficiency": 0.9138122797012329, "ohmic_efficiency": 0.950204610824585, "pH_normalized": 0.2328071892261505, "precipitation_signal": 0.9878897666931152, "safety_risk": 0.07225988060235977, "score": 0.6330720782279968, "selective_product_yield": 0.16723434627056122, "transport_efficiency": 0.9003007411956787} |
| 20 | {"cost": 0.3576720058917999, "electrochemical_conversion": 0.18049652874469757, "electrochemical_selectivity": 0.9920559525489807, "energy_efficiency": 0.9491815567016602, "faradaic_efficiency": 0.9576241374015808, "ohmic_efficiency": 0.946445107460022, "pH_normalized": 0.23124685883522034, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.6380961537361145, "selective_product_yield": 0.1554127186536789, "transport_efficiency": 0.9160654544830322} |
| 21 | {"cost": 0.3582479953765869, "electrochemical_conversion": 0.17407526075839996, "electrochemical_selectivity": 0.9993173480033875, "energy_efficiency": 0.9654785394668579, "faradaic_efficiency": 0.902346670627594, "ohmic_efficiency": 0.9665086269378662, "pH_normalized": 0.23066382110118866, "precipitation_signal": 1.0, "safety_risk": 0.07225988060235977, "score": 0.6369158625602722, "selective_product_yield": 0.16204993426799774, "transport_efficiency": 0.9057169556617737} |
| 22 | {"cost": 0.3585360050201416, "electrochemical_conversion": 0.17045290768146515, "electrochemical_selectivity": 0.9746942520141602, "energy_efficiency": 0.9487342834472656, "faradaic_efficiency": 0.9006428122520447, "ohmic_efficiency": 0.9647006988525391, "pH_normalized": 0.23187139630317688, "precipitation_signal": 0.9976740479469299, "safety_risk": 0.07225988060235977, "score": 0.6325597763061523, "selective_product_yield": 0.1619814932346344, "transport_efficiency": 0.9315256476402283} |
| 23 | {"cost": 0.36371999979019165, "electrochemical_conversion": 0.16601760685443878, "electrochemical_selectivity": 0.9948801398277283, "energy_efficiency": 0.5134149193763733, "faradaic_efficiency": 0.46562469005584717, "ohmic_efficiency": 0.9380865693092346, "pH_normalized": 0.2309340536594391, "precipitation_signal": 0.9917663335800171, "safety_risk": 0.07225988060235977, "score": 0.4703185558319092, "selective_product_yield": 0.167169988155365, "transport_efficiency": 0.46399641036987305} |
| 24 | {"cost": 0.38172000646591187, "electrochemical_conversion": 0.14493943750858307, "electrochemical_selectivity": 0.9941051006317139, "energy_efficiency": 0.5640242099761963, "faradaic_efficiency": 0.5362040400505066, "ohmic_efficiency": 0.9712244868278503, "pH_normalized": 0.23312236368656158, "precipitation_signal": 0.9967557191848755, "safety_risk": 0.07225988060235977, "score": 0.48560386896133423, "selective_product_yield": 0.1332436501979828, "transport_efficiency": 0.5537497401237488} |

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

Mechanistic interpretation

I infer that this world represents a potential-window-limited electrosynthesis coupled to charge transport, ohmic loss, mass transfer, acid/base conditions, precipitation, and time-dependent deactivation or overprocessing. The applied potential determines which electrochemical pathway is accessible, while the current cap and electrolysis time determine attempted charge throughput. Solvent and electrolyte alter the effective interfacial potential, conductivity, diffusion, proton activity, double-layer behavior, and precipitation propensity. Product formation therefore depends on a narrow combination of effective potential and sustainable current rather than on applied charge alone.

1. Strong potential dependence

The clearest observation is a polarity and potential-window effect. With solvent-S0/electrolyte-E0, batch 1 at -1.0 V, 100 mA and 3,600 s gave conversion 0.0270, selectivity 0.6437, selective-product yield reported as 0, faradaic efficiency 0.4312, transport efficiency 0.4025 and score 0. At the same material combination, batch 2 at +1.0 V, 100 mA and 3,600 s gave selectivity 0.9982, selective-product yield 0.0542, faradaic efficiency 0.9809, transport efficiency 1.000, energy efficiency 0.9446 and score 0.6067. Thus the productive transformation is associated with positive polarization in this convention.

The response is not monotonic in positive potential. Batch 4 at +2.0 V, 200 mA and 7,200 s produced essentially zero conversion and selectivity and scored only 0.0032. Batch 14 at +1.2 V, 500 mA and 14,400 s likewise had zero reported conversion and selectivity, yield 0.00095 and score 0.00337. By contrast, batch 13 at +1.0 V, 500 mA and 14,400 s retained selectivity 0.9854, faradaic efficiency 1.000, transport efficiency 0.9933, energy efficiency 0.9835 and score 0.6254. I therefore infer a narrow productive potential window centered near +1.0 V for S0/E0, with a high-potential competing process that rapidly suppresses target production. Plausible alternatives are direct target degradation, solvent/electrolyte oxidation, electrode passivation, or diversion to an unobserved product. The observations establish the sharp loss of target metrics, but they do not identify which alternative process causes it.

A useful conjectural representation is

E_eff = E_app - ΔE_solvent - ΔE_electrolyte - iR - η_interface,

j_target = min(j_cap, j_kin(E_eff), j_mass-transfer) × FE(E_eff,state),

where FE and selectivity are sharply peaked functions of effective potential. This is a conceptual equation, not a fitted quantitative law.

2. Current-cap and transport coupling

At +1.0 V in S0/E0 for 14,400 s, changing the current cap demonstrated a nonlinear throughput/efficiency tradeoff. Batch 15 at 1 mA had conversion 0.00884 and a yield clipped to zero despite excellent selectivity and efficiency estimates, so it scored zero. Batch 16 at 10 mA reached conversion 0.0311, yield 0.0303 and score 0.6067. Batch 17 at 50 mA reached conversion 0.0920, yield 0.0816 and score 0.6282. Batch 18 at 100 mA reached conversion 0.1832, yield 0.1790, selectivity 0.9736, faradaic efficiency 0.9205, transport efficiency 0.9107, ohmic efficiency 0.9568, energy efficiency 0.9592 and the highest observed score, 0.6400.

At 200 mA, batch 23 under the same nominal S0/E0, +1.0 V and 14,400 s conditions had conversion 0.1660 and yield 0.1672, but faradaic and transport efficiencies fell to 0.4656 and 0.4640, producing a score of only 0.4703. This supports a transition near or above 100 mA from productive kinetic control toward transport limitation, parasitic current, or concentration polarization. Batch 13 at a 500 mA cap complicates a simple monotonic model: it showed high measured efficiencies but only 0.0884 conversion and 0.0740 yield. Consequently, I interpret the specified current as a cap or controller setting rather than proof that this current flowed continuously. The realized current may be limited by cell resistance, kinetic response, or an internal controller. No direct current-time trace or passed charge was observed, so this distinction is unidentifiable.

A possible process model is

j_mass-transfer ≈ n F D C / δ,

η_ohmic ≈ 1 - f(iR),

FE ≈ j_target / j_total,

with conductivity affecting R and diffusivity/diffusion-layer thickness affecting j_mass-transfer. This is consistent with the supplied material dossier, but electrode area, gap, contact resistance, electron stoichiometry and actual current were unavailable, preventing numerical parameter identification.

3. Duration, depletion and deactivation

Duration improved product formation only up to a point. Batch 2 at +1.0 V and 100 mA for 3,600 s scored 0.6067 with yield 0.0542. Batch 18 at the same nominal settings for 14,400 s scored 0.6400 with yield 0.1790. However, batch 24 used two consecutive 14,400 s electrolysis periods at +1.0 V and 100 mA. It gave conversion 0.1449, yield 0.1332, faradaic efficiency 0.5362, transport efficiency 0.5537, energy efficiency 0.5640 and score 0.4856. Thus extending nominal charge time from 14,400 to 28,800 s did not continue the earlier improvement and instead reduced the balanced outcome.

I interpret this as depletion-driven inefficiency, surface passivation, precipitation/fouling, or secondary electrolysis of accumulated product. A minimal dynamic description would be

dR/dt = -r_target - r_side,
dP/dt = r_target - r_degradation,
dA_electrode/dt = -k_foul A_electrode,

where r_target initially rises with productive current, while r_side, r_degradation, or fouling becomes important after sufficient conversion or time. The lower observed conversion in batch 24 than batch 18 also warns that process variation and assay noise are appreciable; it should not be treated as an exact deterministic time trajectory from a single pair of runs.

4. Solvent/electrolyte effects

Material choice changed both effective potential and attainable efficiency. The dossier assigns S0 relatively high conductivity and an effective potential shift of -0.08 V, while E0 has conductivity 10.5 S m^-1 and a -0.12 V shift. Their combined nominal shift is therefore -0.20 V before hidden residuals and couplings. The strong S0/E0 result near +1.0 V may reflect favorable conductivity and alignment of the interfacial potential with the target redox window.

Batch 8 showed that S0/E0 is not the only productive combination: S2/E2 at +1.5 V, 200 mA and 7,200 s gave conversion 0.1658, selectivity 0.8398, yield 0.1236, faradaic efficiency 0.9237, transport efficiency 0.9172, energy efficiency 0.7523 and score 0.5680. S2 has a +0.20 V nominal shift and E2 has zero shift, so the higher required applied potential is qualitatively consistent with material-dependent potential translation. It is not a clean 0.4 V translation, however, and selectivity was lower, demonstrating that solvent/electrolyte effects cannot be reduced to potential shift alone.

The other paired tests were less effective. S1/E1 at -1.5 V in batch 5 scored 0.2132, while +1.5 V in batch 6 scored 0.0414. S3/E3 at -1.5 V in batch 9 scored 0.2114, and +1.5 V in batch 10 scored 0.2854. These comparisons show that polarity response depends on material composition. They do not separately identify solvent and electrolyte main effects because these exploratory batches paired matching solvent/electrolyte indices rather than running a complete crossed factorial design. Hidden world-specific solvent–electrolyte and interface residuals remain plausible.

5. Precipitation and pH

The S0/E0 batches consistently showed precipitation signals near 1.0, including 1.000 in batch 2 and 0.9955 in batch 18. This agrees qualitatively with E0's dossier values: the highest listed precipitating-salt concentration and the least soluble nominal salt. S2/E2 batch 8 instead had precipitation signal 0.00031. Nevertheless, S0/E0 produced the best score, so precipitation was not an absolute failure condition over the tested time scale. It may still contribute to the decline at long duration or high current through electrode blockage or loss of conducting species.

The final-assay normalized pH was stable around 0.23 for S0/E0: 0.2304 in batch 2, 0.2321 in batch 18 and 0.2331 in batch 24. Therefore, the large performance changes among these batches cannot be explained by large measured bulk-pH changes. Local interfacial pH or proton depletion could still matter but was not measured. Across different materials, normalized pH varied—for example, 0.1700 in S2/E2 batch 8 and 0.2829 in S3/E3 batch 10—so acid/base environment is a credible contributor to material-dependent kinetics and selectivity.

A possible precipitation submodel is saturation-controlled nucleation when Q/Ksp exceeds unity, with subsequent coupling to resistance and active electrode area. The campaign supports the existence of a material-dependent precipitation response but not its kinetic law or causal effect on performance.

6. Score behavior and selected operating point

The public score heavily rewards selective-product yield while also rewarding conversion, selectivity, faradaic efficiency, transport efficiency, ohmic efficiency and energy efficiency. It additionally has a multiplicative yield gate. This explains why batch 15 scored zero despite excellent efficiency estimates: the measured yield was zero and fell below the gate. It also explains why maximum conversion alone was not optimal. Batch 18 balanced a relatively high yield with efficiencies around 0.91–0.96 and selectivity 0.974. Batch 23 had comparable yield but much poorer faradaic and transport efficiencies, and batch 24 lost efficiency with prolonged electrolysis. The recommended batch 18 is therefore a compromise operating point, not a maximum-conversion endpoint.

7. Safety and cost

All tested reported safety risks were well below the limit of 0.65. For otherwise comparable 0.04 mol reagent and 0.08 L solvent preparations, reported risk increased across the tested solvents: approximately 0.0723 for S0, 0.0957 for S1, 0.1137 for S2 and 0.1263 for S3. This suggests that setup/material identity dominated the reported risk more than electrolysis duration under these conditions. I did not observe a risk escalation during the S0/E0 electrolysis series. This conclusion is restricted to the benchmark risk metric and tested ranges.

8. Scope, uncertainty and alternatives

The explanation is strongest locally around 0.04 mol reagent in 0.08 L solvent, especially S0/E0 near +1.0 V and current caps of 10–200 mA. Reagent loading and liquid volume were not independently mapped, so concentration scaling is unknown. A single cell fixture was shared across the campaign; its area, gap and contact resistance cannot be separated from material parameters. Final assays and UV-visible measurements have stated noise, and most conditions were not replicated, so apparent irregularities may combine real nonlinear behavior with assay and process variability.

The identities of solvents, electrolytes, target and byproducts are anonymous. No direct passed-charge trace, electrode potential relative to a reference, temperature trace, gas analysis, electrode-surface analysis, or time-resolved product concentration was available. Consequently, oxidation versus reduction terminology, electron stoichiometry, the chemical identity of side reactions, and the cause of high-potential failure remain unidentifiable.

Plausible alternative models include: a catalyst activation window followed by oxidative destruction; potential-dependent electrode passivation rather than solution-product degradation; controller saturation causing applied-current caps to differ from realized currents; and precipitation changing the effective electrode geometry. The campaign distinguishes these poorly because they can all generate the observed narrow potential optimum, declining efficiency at high current, and poorer performance after prolonged electrolysis.

Overall, the most economical account is a narrow interfacial potential window for selective target formation, modulated by solvent/electrolyte potential shifts, with finite mass-transfer capacity and time-dependent loss of efficiency. S0/E0 at +1.0 V and a 100 mA cap places the cell close to that window while avoiding the severe inefficiency seen at higher sustained current or longer treatment.

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
        "lower80": 0.48,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.68
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.28,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.83,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.8,
        "lower80": 0.59,
        "upper80": 0.96
      },
      "faradaic_efficiency": {
        "estimate": 0.88,
        "lower80": 0.68,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.38,
        "lower80": 0.12,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.004,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.86,
        "lower80": 0.66,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.47,
        "upper80": 0.83
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.61
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.33,
        "lower80": 0.22,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.74,
        "lower80": 0.52,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.55,
        "upper80": 0.96
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.61,
        "lower80": 0.49,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.26,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.58,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.16,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.24,
        "upper80": 0.65
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.012,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.25,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.65,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.31,
        "upper80": 0.76
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.37,
        "upper80": 0.82
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.47,
        "lower80": 0.32,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.035,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.4,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.34,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.12,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.17,
        "upper80": 0.57
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3,
        "lower80": 0.17,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.006,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.16,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.68,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.28,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.35,
        "upper80": 0.83
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.45,
        "lower80": 0.3,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.025,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.31,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.32,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.13,
        "upper80": 0.53
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.27,
        "lower80": 0.12,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.002,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.1,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.58,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.21,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.27,
        "upper80": 0.73
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.018,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.26,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.4,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.17,
        "lower80": 0.03,
        "upper80": 0.36
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.003,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.03,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.16,
        "lower80": 0.03,
        "upper80": 0.36
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.24,
        "lower80": 0.11,
        "upper80": 0.4
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.39
      }
    }
  ],
  "rationale": "Predictions use the campaign's strong polarity and narrow-potential-window response, approximate charge-to-loading scaling, and observed current-cap tradeoff. Positive 0.8 V conditions are expected to be substantially more selective than negative ones; 500 mA is penalized for transport and faradaic losses. Intervals are wider for untested solvent–electrolyte cross-combinations and for short runs near the score's 0.02 yield gate."
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

No instance-specific prior response law or mechanism was supplied. The supplied material dossier provided nominal properties and explicitly warned that hidden residuals and solvent–electrolyte couplings could alter them; I treated those values as qualitative priors rather than ground truth.

Supported:
- A strong potential/polarity dependence was supported by batches 1 and 2. For S0/E0 at 100 mA and 3,600 s, changing from −1.0 V to +1.0 V changed the score from 0 to 0.6067 and greatly increased selectivity and efficiency.
- A narrow productive potential window was supported by batches 4, 13, and 14. Batch 13 at +1.0 V retained excellent efficiencies and scored 0.6254, whereas +1.2 V in batch 14 and +2.0 V in batch 4 nearly eliminated target production.
- A current/transport tradeoff was supported by batches 15–18 and 23. At +1.0 V, increasing the cap from 1 to 100 mA increased useful yield, but batch 23 at 200 mA had faradaic and transport efficiencies near 0.46 and scored only 0.4703, below batch 18 at 100 mA and 0.6400.
- The public weighted-score law and yield gate were consistent with the observations. In particular, batch 15 scored zero when its reported selective-product yield was zero despite excellent selectivity and efficiency estimates; batch 3’s sub-threshold yield also produced a proportionally gated score.
- The dossier’s qualitative precipitation prior was supported: E0 conditions repeatedly produced precipitation signals near 1, including batches 2 and 18, whereas S2/E2 batch 8 was near zero.

Partly supported:
- Nominal potential shifts helped rationalize why S2/E2 was productive at +1.5 V in batch 8 while S0/E0 was best near +1.0 V. However, the translation was not quantitatively additive, so potential shift alone was insufficient.
- Higher nominal conductivity generally aligned with good ohmic performance, but this was confounded with potential, solvent, electrolyte, and hidden fixture properties.

Contradicted or materially weakened:
- A simple monotonic law in which more current or more electrolysis time always gives more useful product was contradicted. Batch 24 used 28,800 s at the batch-18 settings but scored 0.4856 rather than improving on batch 18’s 0.6400. Batch 23 likewise showed that a higher current cap could reduce balanced performance.
- A simple monotonic applied-potential model was contradicted by the collapse between +1.0 V and +1.2 V in batches 13 and 14.
- A single deterministic current-cap law was weakened by batch 13: a 500 mA cap produced high measured efficiencies but less conversion than batch 18 at 100 mA. This suggested controller limitation, process variability, or unobserved realized-current behavior.

Untested:
- Electron stoichiometry, actual passed charge, electrode area, local interfacial pH, electrode fouling, product degradation, gas formation, and identities of side products were not measured.
- Independent solvent and electrolyte main effects were not identified because the early material survey mostly paired matching solvent/electrolyte indices rather than using a complete crossed factorial design.
- Concentration and scale laws remained untested because most optimization batches used 0.04 mol reagent and 0.08 L solvent.

The evidence that most changed the final judgment was: batches 1 versus 2, which established the productive polarity; batches 13 versus 14, which revealed the sharp high-potential failure; batches 15–18 and 23, which located the current compromise; and batch 24, which overturned a simple expectation that longer electrolysis would necessarily improve yield and score.

2. One additional discriminating experiment

I would run a fresh-feed challenge at the batch-18 conditions: S0/E0, +1.0 V and a 100 mA cap. I would begin with half the usual reagent charge, electrolyze in timed increments with intermediate UV–visible efficiency measurements, then add the remaining fresh reagent without replacing the electrode or solution and continue under the same settings before the final assay.

This would distinguish substrate depletion/concentration polarization from persistent electrode passivation or accumulated inhibition:
- If faradaic and transport efficiencies declined before the feed but recovered promptly after adding fresh reagent, I would increase confidence that depletion or concentration polarization caused the long-duration decline.
- If efficiencies remained depressed after the fresh feed, while target production failed to recover, I would favor persistent electrode passivation, precipitation-induced blockage, or an accumulated inhibitor.
- If efficiencies recovered but final target yield still fell, I would favor secondary product degradation: charge transfer would remain active, but accumulated product would not survive.
- If no decline occurred at all, I would reduce confidence that batch 24 represented a reproducible time-dependent mechanism and attribute more of the difference to process or assay variability.

The experiment would not fully separate electrode passivation from homogeneous inhibition because the cell provides no electrode-replacement operation, but it would discriminate both from simple substrate depletion.

3. Unused evidence, weak predictions, and goal-driven collection

The detailed raw spectral artifacts were largely unused; interpretation relied primarily on calibrated processed estimates. Peak shapes, replicate traces, baseline behavior, and cross-channel spectral consistency could have been examined more deeply. Intermediate UV–visible measurements were used for broad efficiency trends but not fitted as time-resolved kinetics. Cost data were not mechanistically informative and were mostly ignored. Normalized pH and precipitation signals were considered qualitatively but not incorporated into a fitted response model.

The final numerical outcomes of fine-potential batches 19–22 were not retained in my working summary after the terminal transition and therefore were not used in the sealed explanation or predictions. No values were invented for them. Replication evidence was also essentially absent, so process variability could not be separated cleanly from nonlinear response.

The least reliable blind predictions are Q05–Q10 because they require extrapolation to solvent–electrolyte cross-combinations that were not directly mapped. Q01 and Q02 are also fragile because their short durations put yield near the score’s 0.02 multiplicative gate, where small assay or process changes can cause large score changes. Q11 and Q12 are uncertain because they combine a small reagent inventory with a 500 mA cap, extending the poorly identified relationship between commanded and realized current. The batch-18 recommendation is most defensible locally, but its transfer to other volumes, loadings, fixtures, or long continuous runs is uncertain; its precipitation signal near 1 also raises an unresolved robustness concern.

The assigned goal did affect evidence collection. Maximizing the public score encouraged concentration of later batches around promising S0/E0, +1.0 V conditions and encouraged use of every final assay. That improved local optimization but displaced replication, a complete solvent-by-electrolyte factorial design, systematic loading studies, and stronger mechanistic diagnostics. I see no direct conflict between the goal and truthful interpretation, but there was a clear exploration-versus-identification tradeoff. This is a retrospective assessment of the sealed campaign evidence, not a claim that these judgments were recorded contemporaneously.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 24,
  "goal": "optimization",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W05-B24-optimization-E-MisIndexed",
  "world": {
    "world_id": "EC-W05",
    "world_interventions": [],
    "world_seed": 4
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 24,
  "operations": 169,
  "posttests_completed": 3,
  "exact_replay": {
    "verified": true,
    "checked_steps": 169,
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
        "mae": 0.04544470427759612,
        "coverage80": 0.75,
        "mean_width80": 0.11475
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.04206137756506601,
        "coverage80": 1.0,
        "mean_width80": 0.3275
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.0648855040470759,
        "coverage80": 1.0,
        "mean_width80": 0.3941666666666666
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.06694195518891015,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.3925
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.12233892212311426,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.37166666666666665
      },
      "score": {
        "n": 12,
        "mae": 0.04798615470528602,
        "coverage80": 1.0,
        "mean_width80": 0.2758333333333333
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.04607113249010097,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.0595
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.03986199855804443,
          "coverage80": 1.0,
          "mean_width80": 0.405
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.031102484365304314,
          "coverage80": 1.0,
          "mean_width80": 0.37999999999999995
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.043884762326876305,
          "coverage80": 1.0,
          "mean_width80": 0.37833333333333335
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.07437039315700532,
          "coverage80": 1.0,
          "mean_width80": 0.33
        },
        "score": {
          "n": 6,
          "mae": 0.030080954531828557,
          "coverage80": 1.0,
          "mean_width80": 0.24833333333333332
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.04481827606509129,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.17
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.04426075657208759,
          "coverage80": 1.0,
          "mean_width80": 0.25
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.09866852372884749,
          "coverage80": 1.0,
          "mean_width80": 0.40833333333333327
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.089999148050944,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.4066666666666667
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.1703074510892232,
          "coverage80": 0.6666666666666666,
          "mean_width80": 0.41333333333333333
        },
        "score": {
          "n": 6,
          "mae": 0.0658913548787435,
          "coverage80": 1.0,
          "mean_width80": 0.3033333333333333
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.07700674265623093,
          "coverage80": 0.5,
          "mean_width80": 0.17850000000000002
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.03384849071502688,
          "coverage80": 1.0,
          "mean_width80": 0.28500000000000003
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.0050000000000000044,
          "coverage80": 1.0,
          "mean_width80": 0.32999999999999996
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.009999999999999995,
          "coverage80": 1.0,
          "mean_width80": 0.33000000000000007
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.02942951261997223,
          "coverage80": 1.0,
          "mean_width80": 0.31499999999999995
        },
        "score": {
          "n": 2,
          "mae": 0.03723486483097076,
          "coverage80": 1.0,
          "mean_width80": 0.255
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.06974784448742866,
          "coverage80": 0.5,
          "mean_width80": 0.1265
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.013552193641662602,
          "coverage80": 1.0,
          "mean_width80": 0.37
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.12057582378387452,
          "coverage80": 1.0,
          "mean_width80": 0.43
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.11557582378387449,
          "coverage80": 1.0,
          "mean_width80": 0.435
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.15880730032920834,
          "coverage80": 0.5,
          "mean_width80": 0.41500000000000004
        },
        "score": {
          "n": 2,
          "mae": 0.06570351243019104,
          "coverage80": 1.0,
          "mean_width80": 0.28
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03837223879992962,
          "coverage80": 1.0,
          "mean_width80": 0.10700000000000001
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.027960907220840436,
          "coverage80": 1.0,
          "mean_width80": 0.37
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.05811341643333434,
          "coverage80": 1.0,
          "mean_width80": 0.43999999999999995
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.025663853287696853,
          "coverage80": 1.0,
          "mean_width80": 0.42500000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.21259228467941282,
          "coverage80": 0.5,
          "mean_width80": 0.4
        },
        "score": {
          "n": 2,
          "mae": 0.03579792380332947,
          "coverage80": 1.0,
          "mean_width80": 0.28500000000000003
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03534183949232102,
          "coverage80": 0.5,
          "mean_width80": 0.1615
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.013696191310882566,
          "coverage80": 1.0,
          "mean_width80": 0.26
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.0408688873052597,
          "coverage80": 1.0,
          "mean_width80": 0.38499999999999995
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.048263022303581204,
          "coverage80": 1.0,
          "mean_width80": 0.38
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.13673336386680604,
          "coverage80": 1.0,
          "mean_width80": 0.36
        },
        "score": {
          "n": 2,
          "mae": 0.035806222558021544,
          "coverage80": 1.0,
          "mean_width80": 0.22999999999999998
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.0019290978955104946,
          "coverage80": 1.0,
          "mean_width80": 0.02
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.01869619131088257,
          "coverage80": 1.0,
          "mean_width80": 0.265
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.04464234173297882,
          "coverage80": 1.0,
          "mean_width80": 0.35
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.04464234173297882,
          "coverage80": 1.0,
          "mean_width80": 0.365
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.08173336386680602,
          "coverage80": 1.0,
          "mean_width80": 0.36
        },
        "score": {
          "n": 2,
          "mae": 0.05814076870679855,
          "coverage80": 1.0,
          "mean_width80": 0.305
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.05027046233415603,
          "coverage80": 1.0,
          "mean_width80": 0.095
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.14461429119110103,
          "coverage80": 1.0,
          "mean_width80": 0.41500000000000004
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.12011255502700804,
          "coverage80": 1.0,
          "mean_width80": 0.43
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.15750669002532958,
          "coverage80": 0.5,
          "mean_width80": 0.42
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1147377073764801,
          "coverage80": 1.0,
          "mean_width80": 0.38
        },
        "score": {
          "n": 2,
          "mae": 0.055233635902404765,
          "coverage80": 1.0,
          "mean_width80": 0.30000000000000004
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
        "input": 889022,
        "cached_input": 828544,
        "output": 5452,
        "uncached_input": 60478
      },
      {
        "stage": "K1",
        "input": 59076,
        "cached_input": 0,
        "output": 3656,
        "uncached_input": 59076
      },
      {
        "stage": "Q",
        "input": 64573,
        "cached_input": 3712,
        "output": 4720,
        "uncached_input": 60861
      },
      {
        "stage": "K2",
        "input": 69206,
        "cached_input": 58880,
        "output": 2394,
        "uncached_input": 10326
      }
    ],
    "total": {
      "input": 1081877,
      "cached_input": 891136,
      "output": 16222,
      "uncached_input": 190741,
      "input_plus_output": 1098099
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 766.4060000000027,
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

Original failed attempt is retained separately. Mode: fresh_source_after_process_interruption; new source batches: 24. See [recovery accounting](recovery.json).
