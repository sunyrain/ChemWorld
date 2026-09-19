# EC-W04-B24-discovery-E-Aligned

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
| 1 | {"cost": 0.35263198614120483, "electrochemical_conversion": 0.008014115504920483, "electrochemical_selectivity": 0.01034972071647644, "energy_efficiency": 0.005256945732980967, "faradaic_efficiency": 0.02452157624065876, "ohmic_efficiency": 0.9628238677978516, "pH_normalized": 0.2343980222940445, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0} |
| 2 | {"cost": 0.35263198614120483, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.6321769952774048, "energy_efficiency": 0.1992095410823822, "faradaic_efficiency": 0.39083513617515564, "ohmic_efficiency": 0.9716616868972778, "pH_normalized": 0.23170267045497894, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.17404963076114655, "selective_product_yield": 0.011816189624369144, "transport_efficiency": 0.417091965675354} |
| 3 | {"cost": 0.3529199957847595, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.0, "faradaic_efficiency": 0.0, "ohmic_efficiency": 0.9696498513221741, "pH_normalized": 0.23241767287254333, "precipitation_signal": 0.9863388538360596, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.0} |
| 4 | {"cost": 0.3529199957847595, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.4909871220588684, "energy_efficiency": 0.03493475541472435, "faradaic_efficiency": 0.30103063583374023, "ohmic_efficiency": 0.9818079471588135, "pH_normalized": 0.23172709345817566, "precipitation_signal": 0.9870871305465698, "safety_risk": 0.07211905717849731, "score": 0.02702035754919052, "selective_product_yield": 0.0024425878655165434, "transport_efficiency": 0.2695430815219879} |
| 5 | {"cost": 0.3524160087108612, "electrochemical_conversion": 0.011048580519855022, "electrochemical_selectivity": 0.9392327666282654, "energy_efficiency": 0.8525975346565247, "faradaic_efficiency": 0.6627970337867737, "ohmic_efficiency": 0.9419913291931152, "pH_normalized": 0.23668788373470306, "precipitation_signal": 0.9864134788513184, "safety_risk": 0.07211905717849731, "score": 0.38471049070358276, "selective_product_yield": 0.015554246492683887, "transport_efficiency": 0.6522876024246216} |
| 6 | {"cost": 0.3524160087108612, "electrochemical_conversion": 0.008123055100440979, "electrochemical_selectivity": 0.7163205742835999, "energy_efficiency": 0.6318327188491821, "faradaic_efficiency": 0.5362326502799988, "ohmic_efficiency": 0.9438481330871582, "pH_normalized": 0.23341193795204163, "precipitation_signal": 0.997043788433075, "safety_risk": 0.07211905717849731, "score": 0.29064202308654785, "selective_product_yield": 0.014589624479413033, "transport_efficiency": 0.5115492939949036} |
| 7 | {"cost": 0.3532800078392029, "electrochemical_conversion": 0.01795276068150997, "electrochemical_selectivity": 0.959305465221405, "energy_efficiency": 0.2190060168504715, "faradaic_efficiency": 0.13251198828220367, "ohmic_efficiency": 0.7511193752288818, "pH_normalized": 0.23242653906345367, "precipitation_signal": 0.9820858836174011, "safety_risk": 0.07211905717849731, "score": 0.19891364872455597, "selective_product_yield": 0.014598957262933254, "transport_efficiency": 0.13591234385967255} |
| 8 | {"cost": 0.35222160816192627, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.9209724068641663, "energy_efficiency": 0.9166983366012573, "faradaic_efficiency": 0.8750558495521545, "ohmic_efficiency": 1.0, "pH_normalized": 0.23072905838489532, "precipitation_signal": 0.994958758354187, "safety_risk": 0.07211905717849731, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.8685604929924011} |
| 9 | {"cost": 0.35436001420021057, "electrochemical_conversion": 0.07154697924852371, "electrochemical_selectivity": 0.9236385226249695, "energy_efficiency": 0.9119606018066406, "faradaic_efficiency": 0.6212756037712097, "ohmic_efficiency": 0.9736465811729431, "pH_normalized": 0.23274284601211548, "precipitation_signal": 1.0, "safety_risk": 0.07211905717849731, "score": 0.5248715877532959, "selective_product_yield": 0.08573854714632034, "transport_efficiency": 0.642106831073761} |
| 10 | {"cost": 0.35436001420021057, "electrochemical_conversion": 0.07508878409862518, "electrochemical_selectivity": 0.7311118245124817, "energy_efficiency": 0.6517730355262756, "faradaic_efficiency": 0.5212047100067139, "ohmic_efficiency": 0.9330974221229553, "pH_normalized": 0.23042869567871094, "precipitation_signal": 0.9919947981834412, "safety_risk": 0.07211905717849731, "score": 0.41641539335250854, "selective_product_yield": 0.04008663445711136, "transport_efficiency": 0.5225542783737183} |
| 11 | {"cost": 0.35651999711990356, "electrochemical_conversion": 0.013452183455228806, "electrochemical_selectivity": 0.0, "energy_efficiency": 0.012963879853487015, "faradaic_efficiency": 0.002204522956162691, "ohmic_efficiency": 0.9746119976043701, "pH_normalized": 0.23141373693943024, "precipitation_signal": 0.9998839497566223, "safety_risk": 0.07211905717849731, "score": 0.006618361920118332, "selective_product_yield": 0.0015959294978529215, "transport_efficiency": 0.009384461678564548} |
| 12 | {"cost": 0.3529199957847595, "electrochemical_conversion": 0.057040467858314514, "electrochemical_selectivity": 0.8351866006851196, "energy_efficiency": 0.700555145740509, "faradaic_efficiency": 0.5958170294761658, "ohmic_efficiency": 0.8477790951728821, "pH_normalized": 0.231934055685997, "precipitation_signal": 0.9932199120521545, "safety_risk": 0.07211905717849731, "score": 0.459191232919693, "selective_product_yield": 0.07367116212844849, "transport_efficiency": 0.6170419454574585} |
| 13 | {"cost": 0.3473599851131439, "electrochemical_conversion": 0.08937768638134003, "electrochemical_selectivity": 0.8322089314460754, "energy_efficiency": 0.7928599715232849, "faradaic_efficiency": 0.784683108329773, "ohmic_efficiency": 0.948910117149353, "pH_normalized": 0.2016102373600006, "precipitation_signal": 0.8500597476959229, "safety_risk": 0.07211905717849731, "score": 0.5185768604278564, "selective_product_yield": 0.061153508722782135, "transport_efficiency": 0.7745789885520935} |
| 14 | {"cost": 0.3473599851131439, "electrochemical_conversion": 0.08159827440977097, "electrochemical_selectivity": 0.8696749806404114, "energy_efficiency": 0.8064618110656738, "faradaic_efficiency": 0.7914191484451294, "ohmic_efficiency": 0.9187095165252686, "pH_normalized": 0.15867379307746887, "precipitation_signal": 0.0, "safety_risk": 0.07211905717849731, "score": 0.5300230979919434, "selective_product_yield": 0.0802859291434288, "transport_efficiency": 0.7788988947868347} |
| 15 | {"cost": 0.3473599851131439, "electrochemical_conversion": 0.0752808228135109, "electrochemical_selectivity": 0.7256304621696472, "energy_efficiency": 0.6873125433921814, "faradaic_efficiency": 0.6024109125137329, "ohmic_efficiency": 0.9501306414604187, "pH_normalized": 0.27307945489883423, "precipitation_signal": 0.0, "safety_risk": 0.07211905717849731, "score": 0.43771660327911377, "selective_product_yield": 0.04124647378921509, "transport_efficiency": 0.5757338404655457} |
| 16 | {"cost": 0.37935999035835266, "electrochemical_conversion": 0.09895264357328415, "electrochemical_selectivity": 0.8593034744262695, "energy_efficiency": 0.8360376358032227, "faradaic_efficiency": 0.7415057420730591, "ohmic_efficiency": 0.9342013597488403, "pH_normalized": 0.23920120298862457, "precipitation_signal": 0.9885087013244629, "safety_risk": 0.095519058406353, "score": 0.5276705622673035, "selective_product_yield": 0.08669723570346832, "transport_efficiency": 0.7374816536903381} |
| 17 | {"cost": 0.37935999035835266, "electrochemical_conversion": 0.07431410253047943, "electrochemical_selectivity": 0.731808066368103, "energy_efficiency": 0.6549128293991089, "faradaic_efficiency": 0.6615942716598511, "ohmic_efficiency": 0.9134802222251892, "pH_normalized": 0.20710694789886475, "precipitation_signal": 0.7141063809394836, "safety_risk": 0.095519058406353, "score": 0.4467773735523224, "selective_product_yield": 0.04401763528585434, "transport_efficiency": 0.6566280722618103} |
| 18 | {"cost": 0.37935999035835266, "electrochemical_conversion": 0.09704188257455826, "electrochemical_selectivity": 0.8406057953834534, "energy_efficiency": 0.7682156562805176, "faradaic_efficiency": 0.7309402823448181, "ohmic_efficiency": 0.8842080235481262, "pH_normalized": 0.16329695284366608, "precipitation_signal": 0.00027130584931001067, "safety_risk": 0.095519058406353, "score": 0.506371021270752, "selective_product_yield": 0.0826091468334198, "transport_efficiency": 0.721113920211792} |
| 19 | {"cost": 0.43055999279022217, "electrochemical_conversion": 0.06741884350776672, "electrochemical_selectivity": 0.8827984929084778, "energy_efficiency": 0.7984161376953125, "faradaic_efficiency": 0.6394084095954895, "ohmic_efficiency": 0.9040241837501526, "pH_normalized": 0.25028496980667114, "precipitation_signal": 0.9774043560028076, "safety_risk": 0.11351905763149261, "score": 0.49025678634643555, "selective_product_yield": 0.06564030051231384, "transport_efficiency": 0.6258968710899353} |
| 20 | {"cost": 0.43055999279022217, "electrochemical_conversion": 0.08711909502744675, "electrochemical_selectivity": 0.821039080619812, "energy_efficiency": 0.7132543921470642, "faradaic_efficiency": 0.7063068151473999, "ohmic_efficiency": 0.859618067741394, "pH_normalized": 0.1749081164598465, "precipitation_signal": 0.008003811351954937, "safety_risk": 0.11351905763149261, "score": 0.47399234771728516, "selective_product_yield": 0.05045120045542717, "transport_efficiency": 0.6647481322288513} |
| 21 | {"cost": 0.43055999279022217, "electrochemical_conversion": 0.06527211517095566, "electrochemical_selectivity": 0.6597188711166382, "energy_efficiency": 0.6097603440284729, "faradaic_efficiency": 0.5187310576438904, "ohmic_efficiency": 0.9263707399368286, "pH_normalized": 0.2865735590457916, "precipitation_signal": 0.005525000859051943, "safety_risk": 0.11351905763149261, "score": 0.3955540060997009, "selective_product_yield": 0.033458027988672256, "transport_efficiency": 0.5221013426780701} |
| 22 | {"cost": 0.3985599875450134, "electrochemical_conversion": 0.05013627931475639, "electrochemical_selectivity": 0.8512651324272156, "energy_efficiency": 0.80760258436203, "faradaic_efficiency": 0.4182821214199066, "ohmic_efficiency": 0.9310024976730347, "pH_normalized": 0.24110116064548492, "precipitation_signal": 0.9892283082008362, "safety_risk": 0.12611906230449677, "score": 0.43448910117149353, "selective_product_yield": 0.03684926778078079, "transport_efficiency": 0.4491649270057678} |
| 23 | {"cost": 0.3985599875450134, "electrochemical_conversion": 0.07352213561534882, "electrochemical_selectivity": 0.7947904467582703, "energy_efficiency": 0.7220537662506104, "faradaic_efficiency": 0.6798622012138367, "ohmic_efficiency": 0.9290036559104919, "pH_normalized": 0.2100011706352234, "precipitation_signal": 0.6196641325950623, "safety_risk": 0.12611906230449677, "score": 0.47663190960884094, "selective_product_yield": 0.06008635833859444, "transport_efficiency": 0.6782339215278625} |
| 24 | {"cost": 0.3985599875450134, "electrochemical_conversion": 0.04987889155745506, "electrochemical_selectivity": 0.6944303512573242, "energy_efficiency": 0.6684567928314209, "faradaic_efficiency": 0.4036327600479126, "ohmic_efficiency": 0.9458562135696411, "pH_normalized": 0.2807285785675049, "precipitation_signal": 0.001529996981844306, "safety_risk": 0.12611906230449677, "score": 0.383282870054245, "selective_product_yield": 0.02546551637351513, "transport_efficiency": 0.4211784303188324} |

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

I interpret this world as a charge-driven electrochemical conversion with four coupled limitations: potential-dependent interfacial selectivity, finite charge delivery, mass transport, and ohmic loss. Solvent and electrolyte alter all four through conductivity, diffusivity, proton activity, double-layer properties, precipitation, and shifts of the effective electrode potential. The response is therefore not monotonic in either applied potential or current.

1. Core process model

A useful conceptual model is:

E_eff = E_applied - E_shift(solvent,electrolyte) - I R_cell

j_product = j_available × FE(E_eff,S,E) × T(I,S,E) × A_active(t,S,E)

n_product(t) ≈ integral[j_product/(zF)] dt

conversion ≈ min(n_product/n_reagent, conversion ceiling)

selective_product_yield ≈ conversion × product selectivity, subject to assay noise and possibly a different benchmark normalization.

Here S and E denote solvent and electrolyte identities, T is a transport factor, R_cell is an effective resistance, and A_active allows precipitation or other surface changes to alter the active electrode area. I cannot identify z, the true exchange current, R_cell, or the separate solvent/electrolyte residuals from the available observables.

The efficiency channels are consistent with related but distinct factors. Faradaic efficiency reports how much delivered charge reaches productive chemistry; transport efficiency penalizes mass-transfer limitation; ohmic efficiency penalizes resistive loss; energy efficiency combines these with potential utilization. These quantities should not be treated as independent causes, because they respond to the same current, potential, and material properties.

2. Potential dependence and polarity

Potential has a window-shaped rather than monotonic effect. At S0/E0, 100 mA, 900 s, batch 5 at +0.6 V produced the best short-run response: selectivity 0.939, selective-product yield 0.0156, faradaic efficiency 0.663, transport efficiency 0.652, energy efficiency 0.853, and score 0.385. Batch 6 at -0.6 V remained active but was worse: selectivity 0.716, yield 0.0146, faradaic efficiency 0.536, transport efficiency 0.512, energy efficiency 0.632, and score 0.291. Thus the process is not exclusively one-polarity, but positive moderate potential favors the target under this material combination.

Moving farther from that region was harmful. At -1.2 V, batch 2 had selectivity 0.632, yield 0.0118, and score 0.174. At -2.0 V, batch 4 fell to selectivity 0.491, yield 0.00244, energy efficiency 0.0349, and score 0.0270. The positive high-potential side collapsed even more sharply: batch 1 at +1.2 V and 900 s had zero reported yield and near-zero productive efficiencies, while batch 3 at +2.0 V was likewise inactive. Extending +1.2 V to 9000 s in batch 11 did not rescue it: yield was only 0.00160, selectivity was reported as zero, and score was 0.00662.

This suggests at least two competing potential-dependent pathways. A moderate-potential pathway makes target product, while excessive overpotential directs charge into an unobserved side reaction, destroys an active intermediate, or moves the interface outside the target redox window. A compact empirical representation would be a peaked function such as

FE_target(E_eff) ≈ A exp[-(E_eff-E*)^2/(2w^2)] × g_polarity(E_eff),

with an asymmetric polarity factor g_polarity. A threshold-plus-side-reaction model could fit equally well; the experiments do not distinguish a Gaussian kinetic window from inhibition, passivation, or a sequence requiring an intermediate oxidation state.

3. Time and charge delivery

Duration primarily controls extent until substrate depletion or another ceiling becomes important. Comparing otherwise matched S0/E0 experiments at +0.6 V and 100 mA, increasing duration from 900 s in batch 5 to 9000 s in batch 9 raised selective-product yield from 0.0156 to 0.0857 and final electrochemical conversion from 0.0110 to 0.0715. Selectivity stayed high (0.939 versus 0.924), while faradaic efficiency changed only from 0.663 to 0.621. This is strong evidence that accumulated productive charge, not a slow change in selectivity, explains most of the time effect over this interval.

The approximately tenfold increase in time caused only about a five- to eightfold increase in the extent signals, depending on which noisy assay channel is used. That sublinearity is compatible with depletion near the electrode, declining active area, back reaction, or a nonlinear assay floor at low conversion. There was only one long-duration point at each of +0.2, +0.6, -0.6, and +1.2 V, so a unique time law cannot be established.

4. Current, transport, and resistance

Current exhibits a classic throughput-efficiency tradeoff. At +0.6 V for 900 s, reducing the configured current from 100 mA in batch 5 to 10 mA in batch 8 gave very high reported efficiencies—selectivity 0.921, faradaic efficiency 0.875, transport efficiency 0.869, energy efficiency 0.917, and ohmic efficiency 1.0—but product yield was reported as zero. The likely explanation is insufficient total charge and a signal near or below the product assay floor, not failure of the selective pathway.

Increasing current to 500 mA in batch 7 also failed to increase yield: yield was 0.0146, close to the 0.0156 at 100 mA, while faradaic efficiency fell to 0.133, transport efficiency to 0.136, energy efficiency to 0.219, and ohmic efficiency to 0.751. Thus most additional nominal current at 500 mA is lost to transport limitation, resistance, or side chemistry. A plausible empirical factorization is

T(I) ≈ 1/[1+(I/I_lim)^m]

and

eta_ohmic ≈ max(0,1-I R_eff/|E_drive|),

although the exact forms and I_lim are unidentifiable from three current levels. Around 100 mA was the best tested compromise between delivering enough charge and retaining efficiency.

5. Material effects

The material dossier predicts that solvents and electrolytes alter conductivity, diffusion, interfacial capacitance, proton activity, solubility, and standard-potential position. The experiments support those qualitative couplings but also reveal fixed world-specific interactions not captured by a simple nominal-property ranking.

At the common condition +0.6 V, 100 mA, 9000 s, the S0 electrolyte series was:

• E0, batch 9: yield 0.0857, selectivity 0.924, FE 0.621, transport 0.642, score 0.5249.
• E1, batch 13: yield 0.0612, selectivity 0.832, FE 0.785, transport 0.775, score 0.5186.
• E2, batch 14: yield 0.0803, selectivity 0.870, FE 0.791, transport 0.779, score 0.5300.
• E3, batch 15: yield 0.0412, selectivity 0.726, FE 0.602, transport 0.576, score 0.4377.

E0 generated the largest yield in this solvent but sacrificed charge and transport efficiency. E2 offered nearly as much yield with substantially better FE and transport, producing the highest observed balanced score. E3 was consistently poor at this applied potential. Because electrolyte standard-potential shifts differ, part of this ordering may reflect displacement of each electrolyte relative to the fixed +0.6 V optimum rather than an intrinsic activity ordering.

Solvent also matters. With E0, batch 16 using S1 gave yield 0.0867, FE 0.742, transport efficiency 0.737, and score 0.5277. Batch 19 using S2 gave yield 0.0656 and score 0.4903, and batch 22 using S3 gave yield 0.0368, FE 0.418, transport 0.449, and score 0.4345. Thus S1 improved charge utilization relative to S0/E0, while S3 appeared transport-limited despite its nominally respectable conductivity. Hidden solvation and interface residuals are therefore important.

The material effects are not purely additive. For example, E1 produced yield 0.0612 with S0 in batch 13, only 0.0440 with S1 in batch 17, but 0.0601 with S3 in batch 23. E2 produced 0.0803 with S0 in batch 14, 0.0826 with S1 in batch 18, and 0.0505 with S2 in batch 20. E3 declined from 0.0412 with S0 in batch 15 to 0.0335 with S2 in batch 21 and 0.0255 with S3 in batch 24. A predictive model therefore needs solvent-electrolyte interaction terms or mechanistic property products, for example conductivity × diffusivity, potential-shift sums, and proton-activity-dependent kinetics.

6. Acidity and precipitation

The pH-normalized channel was primarily electrolyte-controlled. At the common long-run setting, E2 gave the lowest values: 0.159 in batch 14, 0.163 in batch 18, and 0.175 in batch 20. E1 was intermediate at about 0.202–0.210 in batches 13, 17, and 23. E0 was generally about 0.231–0.250 in batches 9, 16, 19, and 22. E3 was highest at about 0.273–0.287 in batches 15, 21, and 24. This agrees qualitatively with the nominal acid concentrations and pKa values: E2 is the strongest/most concentrated acid profile and E3 the weakest.

Precipitation separated the electrolytes even more strongly. E0 was near complete signal, approximately 0.98–1.00 across batches 9, 16, 19, and 22. E1 remained substantial but solvent-dependent: 0.850 in batch 13, 0.714 in batch 17, and 0.620 in batch 23. E2 and E3 were essentially nonprecipitating in the tested solvents, with values near zero in batches 14, 15, 18, 20, 21, and 24. This is consistent with the nominal precipitating-salt concentrations and Ksp information.

Precipitation did not simply eliminate electrochemical activity: E0 batches could still give high yield and score. It may instead alter active area, local transport, or long-run reproducibility. The campaign lacks time-resolved precipitation data and electrode characterization, so it is unclear whether the signal corresponds to benign bulk precipitation, an electrode-blocking deposit, or both.

7. Safety and cost structure

At the fixed reagent and solvent amounts, safety risk and cost were predominantly solvent-dependent rather than electrolyte- or electrolysis-dependent. Final safety risk was 0.0721 for S0 batches, 0.0955 for S1, 0.1135 for S2, and 0.1261 for S3. All were well below the stated 0.65 limit. Corresponding final costs were approximately 0.347–0.356 for S0 depending on electrical conditions, 0.379 for S1, 0.431 for S2, and 0.399 for S3. These are observations within the fixed 0.04 mol reagent/0.08 L solvent recipe and should not be extrapolated linearly to other loadings without evidence.

8. Experiments that formed or changed the account

Batches 1–6 established the potential window and polarity asymmetry. The failure of +1.2 and +2.0 V, contrasted with the strong response at +0.6 V, rejected a simple model in which more positive potential always increases conversion. The residual activity at negative potentials showed that a strict one-direction redox threshold was also inadequate.

Batches 7 and 8 established the current tradeoff. Their similar or lower yield than batch 5 despite fivefold higher or tenfold lower current, respectively, motivated the separation of delivered charge from FE, transport, and ohmic factors.

Batches 9–12 established the duration effect and confirmed the potential window at longer time. Batch 9 showed that useful yield accumulates at +0.6 V; batch 12 showed that +0.2 V is also productive but less efficient; batch 10 showed substantial negative-potential activity; and batch 11 confirmed that +1.2 V remains a poor regime even after long electrolysis.

Batches 13–24 revealed electrolyte control of acidity and precipitation, solvent-dependent transport and risk, and nonadditive solvent-electrolyte performance. In particular, batches 9, 14, and 16 showed three different ways to obtain scores near 0.525: high selectivity/yield with S0/E0, more efficient charge and transport with S0/E2, and strong yield plus improved transport with S1/E0.

9. Scope and uncertainty

This account is supported only for 0.04 mol reagent in 0.08 L of a single solvent, with the tested potentials, currents, and durations. Reagent concentration, solvent volume, mixed solvents, staged potentials, pulse protocols, and repeated electrolysis segments were not varied. Most material combinations were tested only at +0.6 V, 100 mA, and 9000 s; three of the sixteen solvent-electrolyte combinations were not tested there. Consequently, material-specific optimum potentials cannot be identified, and rankings at +0.6 V should not be assumed to hold at either polarity or at shorter times.

The assays include stated noise. Small conversion and yield values near zero should not be overinterpreted, and conversion, selectivity, and selective-product yield do not always satisfy an exact algebraic identity in individual batches. I treat their broad trends as authoritative but not their last digits. There were no replicates, so run-to-run process variability is confounded with instrumental noise.

Unidentifiable factors include electron stoichiometry, electrode area and gap, cell resistance, mass-transfer coefficient, true current versus configured current, exchange-current kinetics, substrate and product concentrations through time, identities of side products, and whether high-potential failure is caused by competing electrolysis, degradation, passivation, or loss of an intermediate. The fixed hidden world residuals also prevent derivation of performance from nominal material properties alone.

Plausible alternative accounts include: (i) a sequential mechanism in which moderate potential creates a productive intermediate but high potential consumes it; (ii) two parallel target-forming routes of opposite polarity with different selectivity; (iii) electrode passivation at high positive potential; or (iv) strong potential-dependent analytical visibility rather than chemistry. The last alternative is less plausible because several independent efficiency channels collapse together at high positive potential, but it cannot be completely excluded.

Overall, the most defensible predictive picture is a moderate-potential reaction window centered near +0.6 V for S0/E0, productive but less selective negative-potential chemistry, approximately charge-controlled accumulation at moderate current, severe transport/ohmic losses at 500 mA, insufficient charge at 10 mA and short duration, and strong solvent-electrolyte coupling through effective potential, conductivity, diffusion, acidity, and precipitation.

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
        "lower80": 0.52,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.47,
        "lower80": 0.29,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.59
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.36,
        "lower80": 0.19,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.008,
        "upper80": 0.058
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.34,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.58,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.43,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.36,
        "upper80": 0.7
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.43,
        "lower80": 0.22,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.007,
        "upper80": 0.072
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.37,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.56,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.35,
        "upper80": 0.63
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.36,
        "upper80": 0.58
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.41,
        "lower80": 0.34,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.066,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.37,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.57,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.41,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.53,
        "lower80": 0.34,
        "upper80": 0.69
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.5,
        "lower80": 0.36,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.105,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.54,
        "lower80": 0.36,
        "upper80": 0.69
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.47,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.45,
        "upper80": 0.76
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.46,
        "lower80": 0.35,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.061,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.63,
        "lower80": 0.47,
        "upper80": 0.76
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.76,
        "lower80": 0.57,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.5,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.83
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.54,
        "lower80": 0.41,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.105,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.53,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.21,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.27,
        "upper80": 0.58
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.36,
        "lower80": 0.26,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.03,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.61,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.54,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.47,
        "upper80": 0.79
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.077,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.63,
        "lower80": 0.46,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.43,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.59
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.56
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.76,
        "lower80": 0.57,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.64,
        "lower80": 0.42,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.67
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.47,
        "lower80": 0.35,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.076,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.43,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.02,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0.035,
        "upper80": 0.19
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.24,
        "lower80": 0.17,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.038,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.22
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.5,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.035,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0.025,
        "upper80": 0.2
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.29,
        "lower80": 0.19,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.04,
        "upper80": 0.23
      }
    }
  ],
  "rationale": "Predictions interpolate the observed S0/E0 potential window between ±0.6 and ±1.2 V, scale product formation by charge per mole at the nearly unchanged reagent concentration, and apply measured electrolyte/solvent efficiency shifts. Long runs are allowed sublinear yield growth; 500 mA cases receive the severe transport, Faradaic, and energy penalties observed in batch 7. Intervals are widened for the untested ±0.8 V points, changed batch size, material-by-potential interactions, and assay/process noise."
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

No instance-specific response law or instance prior was supplied. The material dossier supplied nominal mechanistic properties, but explicitly presented them as incomplete prior evidence rather than an objective ranking. Consequently, the potential window, current law, kinetic form, and material performance ranking were self-developed from the campaign.

Supported:
• A finite productive potential window was strongly supported. At S0/E0, +0.6 V gave high selectivity and energy efficiency in batches 5 and 9, whereas +1.2 V was nearly inactive in batches 1 and 11 and +2.0 V was inactive in batch 3. Negative potentials remained productive but generally less favorable: batches 2, 4, 6, and 10 showed progressively poorer performance away from -0.6 V.
• Product formation depends on accumulated charge or time, but sublinearly. At otherwise matching +0.6 V and 100 mA conditions, extending electrolysis from 900 s in batch 5 to 9000 s in batch 9 increased selective-product yield from 0.0156 to 0.0857 while selectivity remained high.
• Current creates a throughput–efficiency tradeoff. Relative to batch 5 at 100 mA, batch 8 at 10 mA retained excellent efficiency but produced no detected yield during 900 s, while batch 7 at 500 mA produced no additional yield and suffered large Faradaic, transport, energy, and ohmic penalties.
• Electrolyte identity governs acidity and precipitation. E0 was associated with precipitation signals near one in batches 9, 16, 19, and 22; E2 and E3 were near zero in batches 14, 15, 18, 20, 21, and 24. The pH-normalized ordering also broadly followed the supplied acid properties.
• Solvent and electrolyte effects are coupled rather than strictly additive. For example, E1 yield varied from 0.0612 with S0 in batch 13 to 0.0440 with S1 in batch 17 and 0.0601 with S3 in batch 23.

Contradicted or weakened:
• A simple monotonic “more positive potential gives more conversion” law was contradicted by batches 1, 3, and 11 compared with batches 5 and 9.
• A strict single-polarity mechanism was contradicted because batches 2, 4, 6, and 10 showed target formation at negative potentials.
• A model in which configured current directly determines productive rate was contradicted by batch 7: five times the current of batch 5 did not improve short-run yield.
• A direct ranking from nominal conductivity alone was weakened. S3/E0 in batch 22 performed poorly despite S3’s nominal conductivity, indicating that diffusion, solvation, potential shifts, and hidden interfacial residuals matter.
• Precipitation as a simple on/off poison was contradicted or at least weakened: strongly precipitating E0 still performed well in batches 9 and 16.

The evidence that most materially changed the justified account was the collapse at +1.2 V in batches 1 and 11, which requires a window, inhibition, or competing pathway rather than monotonic activation; the large efficiency collapse at 500 mA in batch 7, which requires transport/ohmic terms; and the material interaction pattern in batches 13–24, which prevents a purely additive material model.

Untested claims include the proposed Gaussian-like shape of the potential response, the identities of any intermediates or side products, electron stoichiometry, whether high positive potential causes passivation rather than a soluble side reaction, scaling with reagent concentration or volume, and responses to mixed solvents, pulses, or staged potentials. The factorized equations in the report are explanatory approximations, not uniquely identified laws.

2. One additional discriminating experiment

I would use one staged S0/E0 experiment with the campaign’s standard 0.04 mol reagent and 0.08 L solvent: apply +1.2 V at 100 mA for 900 s, take one UV–visible measurement, then switch to +0.6 V at 100 mA for 8100 s, terminate, and perform the final assay. Its historical comparator would be batch 9, which received +0.6 V for 9000 s.

This distinguishes an irreversible high-potential damage/passivation explanation from a merely nonproductive parallel-reaction explanation. If the final target yield and efficiencies remained far below batch 9 even after 8100 s at +0.6 V, I would increase belief in irreversible passivation, substrate degradation, or destruction of a required intermediate. If performance approached what roughly 8100 s of productive +0.6 V electrolysis should deliver, I would favor a reversible potential-window or parallel side-reaction account: the +1.2 V segment wastes charge but does not permanently damage the system. If the staged experiment exceeded batch 9, that would support a sequential mechanism in which the high-potential segment creates a useful precursor or conditions the interface. A UV–visible change after the first segment would provide supporting, though not species-specific, evidence. Because there are no replicates, only a large deviation from batch 9 should materially change the judgment.

3. Unused evidence, reliability, and goal effects

The full raw UV–visible spectra, replicate traces, calibration details, and any characterization artifacts were not analyzed; only processed public estimates were used. Intermediate measurements were mainly treated as confirmation rather than fitted jointly with final assays. Several nominal dossier properties—double-layer capacitance, diffusion-layer thickness, diffusivity, and standard-potential shifts—were used qualitatively but not quantitatively estimated. Cost and safety data were described but did not enter the mechanistic fit. Three solvent–electrolyte combinations were absent from the long-run material grid, and no condition was replicated.

The operating recommendation for batch 14 is less certain than its rank suggests. Its score of 0.5300 was only slightly above batch 16 at 0.5277 and batch 9 at 0.5249, well within plausible assay and process uncertainty. It is best regarded as one member of a near-tied region, not proof of a uniquely optimal recipe.

The least reliable blind predictions are Q11 and Q12 because they combine 500 mA with a much longer duration and smaller reagent inventory than any observed 500 mA experiment. Q02, Q04, Q06, Q08, Q10, and Q12 are also uncertain because +0.8 V lies between the highly productive +0.6 V regime and the sharply collapsed +1.2 V regime, so interpolation depends strongly on the unknown response shape. Material-specific negative-potential predictions Q05, Q07, and Q09 extrapolate solvent/electrolyte effects across polarity without direct factorial evidence. Q01 and Q02 additionally sit near the selective-yield score gate, so small yield errors can cause disproportionate score errors.

The explanatory goal did affect evidence collection. I allocated batches across polarity, potential, current, duration, solvents, and electrolytes rather than repeatedly optimizing the public score. That breadth exposed the potential window and material interactions, but it left no replication and weak local resolution near +0.6 to +1.2 V. The fixed concentration and mostly fixed long-run control condition improved comparability but limited concentration scaling. I see no clear conflict between the goal and the evidence actually collected, although a purely optimization-focused campaign would likely have spent more batches replicating and refining batches 9, 14, and 16.

## Evaluation and resource use

```json
{
  "arm": "Aligned",
  "budget": 24,
  "goal": "discovery",
  "locus": "E",
  "system": "EC",
  "unit_id": "EC-W04-B24-discovery-E-Aligned",
  "world": {
    "world_id": "EC-W04",
    "world_interventions": [],
    "world_seed": 3
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 24,
  "operations": 168,
  "posttests_completed": 3,
  "exact_replay": {
    "verified": true,
    "checked_steps": 168,
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
        "mae": 0.025855811881677557,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.1535
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.09218340754508973,
        "coverage80": 0.6666666666666666,
        "mean_width80": 0.325
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.06720381766557693,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.27999999999999997
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.0642695006231467,
        "coverage80": 0.8333333333333334,
        "mean_width80": 0.2708333333333333
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.07372182490924994,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.34875000000000006
      },
      "score": {
        "n": 12,
        "mae": 0.07764562100172043,
        "coverage80": 0.9166666666666666,
        "mean_width80": 0.215
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.02956225469242781,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.12333333333333334
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.03685951987902323,
          "coverage80": 1.0,
          "mean_width80": 0.3166666666666667
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.0582977317770322,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.2575
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.05583301886916161,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.2483333333333333
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.06940380528569222,
          "coverage80": 1.0,
          "mean_width80": 0.315
        },
        "score": {
          "n": 6,
          "mae": 0.08653369903564452,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.18833333333333335
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.022149369070927304,
          "coverage80": 1.0,
          "mean_width80": 0.18366666666666667
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.14750729521115621,
          "coverage80": 0.3333333333333333,
          "mean_width80": 0.3333333333333334
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.07610990355412166,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.3025
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.07270598237713177,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.2933333333333333
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.07803984453280767,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.3825
        },
        "score": {
          "n": 6,
          "mae": 0.06875754296779633,
          "coverage80": 1.0,
          "mean_width80": 0.2416666666666667
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.014914135336875911,
          "coverage80": 1.0,
          "mean_width80": 0.191
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.15107378602027893,
          "coverage80": 0.5,
          "mean_width80": 0.365
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.01589060723781585,
          "coverage80": 1.0,
          "mean_width80": 0.165
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.0032847347855567977,
          "coverage80": 1.0,
          "mean_width80": 0.18
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.01678957894444466,
          "coverage80": 1.0,
          "mean_width80": 0.24250000000000002
        },
        "score": {
          "n": 2,
          "mae": 0.028226301670074477,
          "coverage80": 1.0,
          "mean_width80": 0.175
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.0407036916911602,
          "coverage80": 1.0,
          "mean_width80": 0.187
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.08204327225685121,
          "coverage80": 1.0,
          "mean_width80": 0.32500000000000007
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.17662072837352755,
          "coverage80": 0.0,
          "mean_width80": 0.30999999999999994
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.18162072837352755,
          "coverage80": 0.0,
          "mean_width80": 0.29
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1409902650117874,
          "coverage80": 1.0,
          "mean_width80": 0.365
        },
        "score": {
          "n": 2,
          "mae": 0.08855805456638335,
          "coverage80": 1.0,
          "mean_width80": 0.21500000000000005
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.03476484946906567,
          "coverage80": 1.0,
          "mean_width80": 0.1565
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.05392533779144287,
          "coverage80": 1.0,
          "mean_width80": 0.33
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.10604576110839845,
          "coverage80": 1.0,
          "mean_width80": 0.315
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.0886516261100769,
          "coverage80": 1.0,
          "mean_width80": 0.295
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.04243799269199372,
          "coverage80": 1.0,
          "mean_width80": 0.355
        },
        "score": {
          "n": 2,
          "mae": 0.05315795779228211,
          "coverage80": 1.0,
          "mean_width80": 0.205
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.029032241404056552,
          "coverage80": 1.0,
          "mean_width80": 0.1645
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.10251070737838741,
          "coverage80": 0.5,
          "mean_width80": 0.29000000000000004
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.021180809736251804,
          "coverage80": 1.0,
          "mean_width80": 0.2849999999999999
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.021180809736251804,
          "coverage80": 1.0,
          "mean_width80": 0.27499999999999997
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.06584975481033323,
          "coverage80": 1.0,
          "mean_width80": 0.37
        },
        "score": {
          "n": 2,
          "mae": 0.024456249475479114,
          "coverage80": 1.0,
          "mean_width80": 0.19499999999999998
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.025642715306021274,
          "coverage80": 0.5,
          "mean_width80": 0.057499999999999996
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.09751070737838746,
          "coverage80": 0.5,
          "mean_width80": 0.31000000000000005
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.042383755445480314,
          "coverage80": 1.0,
          "mean_width80": 0.30499999999999994
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.04477786064147948,
          "coverage80": 1.0,
          "mean_width80": 0.2899999999999999
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.07435835361480714,
          "coverage80": 1.0,
          "mean_width80": 0.395
        },
        "score": {
          "n": 2,
          "mae": 0.2403916013240814,
          "coverage80": 0.5,
          "mean_width80": 0.30000000000000004
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.010077238082885742,
          "coverage80": 1.0,
          "mean_width80": 0.1645
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.06603663444519042,
          "coverage80": 0.5,
          "mean_width80": 0.33000000000000007
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.04110124409198759,
          "coverage80": 1.0,
          "mean_width80": 0.30000000000000004
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.0461012440919876,
          "coverage80": 1.0,
          "mean_width80": 0.29500000000000004
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.10190500438213348,
          "coverage80": 0.5,
          "mean_width80": 0.365
        },
        "score": {
          "n": 2,
          "mae": 0.0310835611820221,
          "coverage80": 1.0,
          "mean_width80": 0.19999999999999998
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
        "input": 440569,
        "cached_input": 409984,
        "output": 3375,
        "uncached_input": 30585
      },
      {
        "stage": "K1",
        "input": 30898,
        "cached_input": 3456,
        "output": 4312,
        "uncached_input": 27442
      },
      {
        "stage": "Q",
        "input": 37051,
        "cached_input": 3712,
        "output": 4575,
        "uncached_input": 33339
      },
      {
        "stage": "K2",
        "input": 41539,
        "cached_input": 30720,
        "output": 2086,
        "uncached_input": 10819
      }
    ],
    "total": {
      "input": 550057,
      "cached_input": 447872,
      "output": 14348,
      "uncached_input": 102185,
      "input_plus_output": 564405
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 604.9689999999973,
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

Original failed attempt is retained separately. Mode: fresh_source_after_partial_network_failure; new source batches: 24. See [recovery accounting](recovery.json).
