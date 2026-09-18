# EC-W01-B12-discovery-E-MisIndexed

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
| 1 | {"cost": 0.2827799916267395, "electrochemical_conversion": 0.010451862588524818, "electrochemical_selectivity": 0.5603032112121582, "energy_efficiency": 0.1259937584400177, "faradaic_efficiency": 0.3381306529045105, "ohmic_efficiency": 0.976645290851593, "pH_normalized": 0.2322131097316742, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.309426873922348} |
| 2 | {"cost": 0.2827799916267395, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.010023192502558231, "energy_efficiency": 0.0, "faradaic_efficiency": 0.0, "ohmic_efficiency": 0.9854831099510193, "pH_normalized": 0.22951775789260864, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.03845500946044922, "selective_product_yield": 0.00897990819066763, "transport_efficiency": 0.02610676921904087} |
| 3 | {"cost": 0.28268399834632874, "electrochemical_conversion": 0.0, "electrochemical_selectivity": 0.6451374888420105, "energy_efficiency": 0.43773433566093445, "faradaic_efficiency": 0.4218427240848541, "ohmic_efficiency": 0.956011176109314, "pH_normalized": 0.23023276031017303, "precipitation_signal": 0.9868234395980835, "safety_risk": 0.07224962115287781, "score": 0.0, "selective_product_yield": 0.0, "transport_efficiency": 0.43839964270591736} |
| 4 | {"cost": 0.28360798954963684, "electrochemical_conversion": 0.038145512342453, "electrochemical_selectivity": 0.629734456539154, "energy_efficiency": 0.4046115279197693, "faradaic_efficiency": 0.4777546226978302, "ohmic_efficiency": 0.9681692719459534, "pH_normalized": 0.22954218089580536, "precipitation_signal": 0.987571656703949, "safety_risk": 0.07224962115287781, "score": 0.3468962013721466, "selective_product_yield": 0.028396470472216606, "transport_efficiency": 0.4462670683860779} |
| 5 | {"cost": 0.28303200006484985, "electrochemical_conversion": 0.053647320717573166, "electrochemical_selectivity": 0.7268555760383606, "energy_efficiency": 0.6413213014602661, "faradaic_efficiency": 0.5491795539855957, "ohmic_efficiency": 0.9269895553588867, "pH_normalized": 0.23450297117233276, "precipitation_signal": 0.9868980646133423, "safety_risk": 0.07224962115287781, "score": 0.4179077446460724, "selective_product_yield": 0.04462924227118492, "transport_efficiency": 0.5386700630187988} |
| 6 | {"cost": 0.2990320026874542, "electrochemical_conversion": 0.045507267117500305, "electrochemical_selectivity": 0.6825898885726929, "energy_efficiency": 0.5942414402961731, "faradaic_efficiency": 0.4888589382171631, "ohmic_efficiency": 0.8837396502494812, "pH_normalized": 0.2046465277671814, "precipitation_signal": 0.7242242693901062, "safety_risk": 0.09564962238073349, "score": 0.38377952575683594, "selective_product_yield": 0.03974766656756401, "transport_efficiency": 0.46417558193206787} |
| 7 | {"cost": 0.3246319890022278, "electrochemical_conversion": 0.04638069495558739, "electrochemical_selectivity": 0.5405951738357544, "energy_efficiency": 0.44400835037231445, "faradaic_efficiency": 0.3883933126926422, "ohmic_efficiency": 0.8494289517402649, "pH_normalized": 0.16796524822711945, "precipitation_signal": 0.0, "safety_risk": 0.11364962160587311, "score": 0.3141234517097473, "selective_product_yield": 0.026846572756767273, "transport_efficiency": 0.3917936682701111} |
| 8 | {"cost": 0.3086319863796234, "electrochemical_conversion": 0.03155737742781639, "electrochemical_selectivity": 0.6435128450393677, "energy_efficiency": 0.5986399054527283, "faradaic_efficiency": 0.40008243918418884, "ohmic_efficiency": 0.946217954158783, "pH_normalized": 0.28357234597206116, "precipitation_signal": 0.00031451715040020645, "safety_risk": 0.12624962627887726, "score": 0.051367733627557755, "selective_product_yield": 0.002906921086832881, "transport_efficiency": 0.3935870826244354} |
| 9 | {"cost": 0.2847599983215332, "electrochemical_conversion": 0.07110022008419037, "electrochemical_selectivity": 0.7252197265625, "energy_efficiency": 0.4338115453720093, "faradaic_efficiency": 0.14787070453166962, "ohmic_efficiency": 0.6743472218513489, "pH_normalized": 0.23055793344974518, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.290778249502182, "selective_product_yield": 0.07083689421415329, "transport_efficiency": 0.16870197653770447} |
| 10 | {"cost": 0.28268641233444214, "electrochemical_conversion": 0.025332873687148094, "electrochemical_selectivity": 0.736693799495697, "energy_efficiency": 0.7221040725708008, "faradaic_efficiency": 0.5430682301521301, "ohmic_efficiency": 0.974955141544342, "pH_normalized": 0.22824378311634064, "precipitation_signal": 0.9924793243408203, "safety_risk": 0.07224962115287781, "score": 0.09904327988624573, "selective_product_yield": 0.004712161608040333, "transport_efficiency": 0.5444178581237793} |
| 11 | {"cost": 0.28432801365852356, "electrochemical_conversion": 0.21424530446529388, "electrochemical_selectivity": 0.7118160128593445, "energy_efficiency": 0.6821800470352173, "faradaic_efficiency": 0.5403598546981812, "ohmic_efficiency": 0.9315738677978516, "pH_normalized": 0.22922882437705994, "precipitation_signal": 1.0, "safety_risk": 0.07224962115287781, "score": 0.4685223698616028, "selective_product_yield": 0.14625121653079987, "transport_efficiency": 0.5475397706031799} |
| 12 | {"cost": 0.3110800087451935, "electrochemical_conversion": 0.11727461963891983, "electrochemical_selectivity": 0.6031206250190735, "energy_efficiency": 0.5856295228004456, "faradaic_efficiency": 0.324177086353302, "ohmic_efficiency": 0.9736607074737549, "pH_normalized": 0.28477731347084045, "precipitation_signal": 0.0, "safety_risk": 0.12624962627887726, "score": 0.36957377195358276, "selective_product_yield": 0.09399830549955368, "transport_efficiency": 0.3454020321369171} |

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

1. Empirical scope and design

I completed 12 batches. Every batch began with 0.020 mol limiting reagent in 0.040 L solvent, corresponding nominally to 0.50 mol L^-1 before the small analytical withdrawals. Each batch was electrolyzed once, measured by UV–visible spectroscopy after electrolysis, terminated, and then measured by final assay. Thus the campaign directly probes potential, programmed current, electrolysis time, and four matched solvent/electrolyte combinations, but it does not probe reagent concentration or total volume.

The operating conditions were:
B1 S0/E0, -1.5 V, 100 mA, 300 s;
B2 S0/E0, +1.5 V, 100 mA, 300 s;
B3 S0/E0, -0.7 V, 100 mA, 300 s;
B4 S0/E0, -0.7 V, 100 mA, 3600 s;
B5 S0/E0, -0.3 V, 100 mA, 3600 s;
B6 S1/E1, -0.3 V, 100 mA, 3600 s;
B7 S2/E2, -0.3 V, 100 mA, 3600 s;
B8 S3/E3, -0.3 V, 100 mA, 3600 s;
B9 S0/E0, -0.3 V, 500 mA, 3600 s;
B10 S0/E0, -0.3 V, 20 mA, 3600 s;
B11 S0/E0, -0.3 V, 100 mA, 14400 s;
B12 S3/E3, -0.5 V, 100 mA, 14400 s.

2. Main observations

The final-assay values below are observations, not fitted latent values. I abbreviate conversion as X, selectivity as S, selective-product yield as Y, faradaic efficiency as FE, transport efficiency as TE, ohmic efficiency as OE, energy efficiency as EE, normalized pH as pHn, and precipitation signal as P.

B1: X 0.0105, S 0.5603, Y 0, FE 0.3381, TE 0.3094, OE 0.9766, EE 0.1260, pHn 0.2322, P 1.000.
B2: X 0, S 0.0100, Y 0.0090, FE 0, TE 0.0261, OE 0.9855, EE 0, pHn 0.2295, P 1.000.
B3: X 0, S 0.6451, Y 0, FE 0.4218, TE 0.4384, OE 0.9560, EE 0.4377, pHn 0.2302, P 0.9868.
B4: X 0.0381, S 0.6297, Y 0.0284, FE 0.4778, TE 0.4463, OE 0.9682, EE 0.4046, pHn 0.2295, P 0.9876.
B5: X 0.0536, S 0.7269, Y 0.0446, FE 0.5492, TE 0.5387, OE 0.9270, EE 0.6413, pHn 0.2345, P 0.9869.
B6: X 0.0455, S 0.6826, Y 0.0397, FE 0.4889, TE 0.4642, OE 0.8837, EE 0.5942, pHn 0.2046, P 0.7242.
B7: X 0.0464, S 0.5406, Y 0.0268, FE 0.3884, TE 0.3918, OE 0.8494, EE 0.4440, pHn 0.1680, P 0.
B8: X 0.0316, S 0.6435, Y 0.00291, FE 0.4001, TE 0.3936, OE 0.9462, EE 0.5986, pHn 0.2836, P 0.00031.
B9: X 0.0711, S 0.7252, Y 0.0708, FE 0.1479, TE 0.1687, OE 0.6743, EE 0.4338, pHn 0.2306, P 1.000.
B10: X 0.0253, S 0.7367, Y 0.00471, FE 0.5431, TE 0.5444, OE 0.9750, EE 0.7221, pHn 0.2282, P 0.9925.
B11: X 0.2142, S 0.7118, Y 0.1463, FE 0.5404, TE 0.5475, OE 0.9316, EE 0.6822, pHn 0.2292, P 1.000.
B12: X 0.1173, S 0.6031, Y 0.0940, FE 0.3242, TE 0.3454, OE 0.9737, EE 0.5856, pHn 0.2848, P 0.

The UV–visible measurements generally supported the final-assay efficiency ordering. For example, UV/assay FE was 0.560/0.549 in B5, 0.499/0.540 in B11, and 0.400/0.324 in B12. The differences are consistent with instrumental/process uncertainty, although B12 shows that a single UV estimate should not be treated as exact.

3. Proposed electrochemical account

The system behaves primarily as a cathodic conversion with a finite favorable potential window. Positive potential suppresses the desired channel: changing S0/E0 from -1.5 V in B1 to +1.5 V in B2, with the other settings fixed, reduced FE from 0.338 to 0 and TE from 0.309 to 0.026. Both conversions were near the assay floor because only 300 s was used, but the efficiency collapse at +1.5 V is strong evidence about polarity.

Within the negative-potential regime, more negative is not simply better. At S0/E0, 100 mA and 3600 s, moving from -0.7 V (B4) to -0.3 V (B5) increased X from 0.0381 to 0.0536, S from 0.6297 to 0.7269, FE from 0.4778 to 0.5492, TE from 0.4463 to 0.5387, and EE from 0.4046 to 0.6413. B1 at -1.5 V also had substantially lower FE and EE than the milder negative-potential batches. My interpretation is a competing-reaction model: insufficient cathodic drive gives negligible desired current, moderate drive activates the target electron-transfer pathway, and excessive cathodic overpotential increasingly feeds side reactions or nonproductive charge.

A useful qualitative rate expression is

eta = E_eq(materials,pH,state) - E_applied,

j_target = j0,target * f_activation(eta) * f_transport(C,j) * f_surface(state),

j_side = j0,side * g(eta,pH,state),

FE approximately equals j_target/(j_target + j_side + j_nonfaradaic).

Here f_activation rises from zero and then saturates, while g becomes increasingly important at excessive cathodic drive. This produces a band-shaped dependence of FE, selectivity, and energy efficiency on applied potential rather than a monotone dependence.

The nominal material dossier suggests a first-order potential correction

E_eq = E_base + DeltaE_electrolyte + DeltaE_solvent + epsilon_E,

where epsilon_E is the fixed but hidden world residual. The declared combined nominal shifts are approximately +0.20 V for S0/E0, +0.02 V for S1/E1, +0.38 V for S2/E2, and -0.02 V for S3/E3. These shifts plausibly move the useful applied-potential window, but the campaign did not map a complete potential curve for each pair, so this remains a mechanistic prior rather than an identified quantitative law.

4. Charge, time, current, and mass transport

At fixed composition and potential, conversion is approximately charge-controlled at moderate current and incomplete conversion:

Q = I*t,

X_ideal = Q/(n*F*N0),

X approximately equals min[1, X_ideal * FE_charge * U_transport * U_access],

where n is the unidentified electron stoichiometry and U_access collects electrode-area, kinetic, and accessibility effects. The public efficiencies are informative diagnostics, but I do not assume they multiply exactly in the simulator.

The strongest evidence for charge accumulation is B5 versus B11. Both used S0/E0, -0.3 V and 100 mA; increasing time fourfold from 3600 to 14400 s increased conversion from 0.0536 to 0.2142, essentially fourfold. Yield rose from 0.0446 to 0.1463. FE, TE, selectivity, and pHn remained similar: FE 0.549 versus 0.540, TE 0.539 versus 0.548, S 0.727 versus 0.712, and pHn 0.2345 versus 0.2292. This is the clearest evidence that, within this range, time mainly integrates a fairly stable productive current rather than fundamentally changing the mechanism.

Programmed current is not linearly converted into productive current. Relative to B5 at 100 mA, increasing current to 500 mA in B9 raised X only from 0.0536 to 0.0711, while FE fell from 0.549 to 0.148, TE from 0.539 to 0.169, OE from 0.927 to 0.674, and EE from 0.641 to 0.434. This indicates simultaneous concentration polarization and ohmic loss. A plausible compact coupling is

TE approximately equals 1/(1 + I/I_lim),

OE approximately equals clip(1 - I*R_eff/DeltaV_available, 0, 1),

I_productive approximately equals I * FE * TE,

with I_lim depending on diffusivity, diffusion-layer thickness, concentration, electrode area, and solvent coupling. At 20 mA (B10), FE 0.543, TE 0.544, OE 0.975, and EE 0.722 were all favorable, but the available charge was small and observed conversion was only 0.0253. Thus low current is efficient but slow; high current gains some throughput while wasting an increasing fraction of charge and voltage. The best balanced regime observed was therefore intermediate current with long duration, not maximum current.

B10 conversion is higher than a strict one-fifth scaling from B5 would predict, and its yield is unusually low relative to X*S. This may reflect assay noise at low product abundance, a current-dependent accessibility effect, or a hidden yield/capture factor. It prevents precise identification of the current law from only three current levels.

5. Selectivity and selective-product yield

For several informative batches, selective yield is approximately related to conversion and selectivity:

Y approximately equals X*S*R_product,

where R_product is a recovery, survival, or assay-response factor near but not necessarily equal to one. Examples are B4, where X*S = 0.0240 and Y = 0.0284; B5, 0.0390 versus 0.0446; and B11, 0.1525 versus 0.1463. This supports a sequence in which reagent conversion is followed by branching between target and side products.

The relation is not exact. B8 has X*S about 0.0203 but Y only 0.00291, whereas B12 has X*S about 0.0707 but Y 0.0940. B9 also gives X*S about 0.0516 versus Y 0.0708. These deviations are larger than a deterministic identity would allow. Possible explanations are independent measurement noise, a material-dependent product-response/recovery factor, post-electrolysis loss, or another hidden state variable. Because no replicate final assays or explicit degradation measurement were available, I cannot choose among those alternatives. I therefore treat X*S as a structural predictor of Y, not as an exact conservation equation.

6. Material, acid-base, precipitation, transport, and ohmic couplings

The matched-pair comparison B5–B8 shows substantial material effects at the same -0.3 V, 100 mA, and 3600 s. S0/E0 gave the best observed combination among these four: FE 0.549, TE 0.539, S 0.727, X 0.0536, and Y 0.0446. S1/E1 was moderately lower; S2/E2 had lower selectivity and efficiencies; S3/E3 had reasonable selectivity and energy efficiency but lower conversion and a very low measured yield.

The normalized pH ordering closely follows the declared acid properties. B7 with the strongest declared acid electrolyte E2 had pHn 0.1680; B6/E1 had 0.2046; B5/E0 had 0.2345; and B8/E3 had 0.2836. This supports an acid-dissociation equilibrium coupled to solvent proton activity, schematically

HA <-> H+ + A-,

Ka = [H+][A-]/[HA],

with pH and therefore interfacial proton availability controlled jointly by acid concentration, pKa, solvent proton activity, and electrolysis. pH may alter both the target electron-transfer/proton-transfer sequence and competing hydrogen- or degradation-like channels. However, because pH was not independently manipulated, its causal contribution is confounded with electrolyte identity.

Precipitation is strongly material-dependent and agrees qualitatively with the nominal solubility-product information. The S0/E0 batches were essentially saturated at P approximately 0.99–1.00. At otherwise matched conditions, B6 S1/E1 gave P 0.724, B7 S2/E2 gave P 0, and B8 S3/E3 gave approximately 0.0003. B12 S3/E3 also gave P 0. A plausible equilibrium module is

P = sigmoid[a*(log10(IAP) - log10(Ksp_effective))],

Ksp_effective = Ksp_electrolyte * solvent_relative_solubility * exp(epsilon_Ksp).

The public signal appears clipped near zero and one, so it identifies broad precipitation regimes rather than a precise dissolved concentration. Precipitation did not obviously suppress the target reaction in S0/E0: B11 combined P = 1 with the highest conversion and selective yield. It may therefore involve a supporting-electrolyte salt or spectator phase rather than direct target-product precipitation. That interpretation is plausible but conjectural because solid identity was not measured.

Ohmic efficiency is consistent with conductivity and current loading. At 100 mA, the matched batches gave OE 0.927 for B5 S0/E0, 0.884 for B6 S1/E1, 0.849 for B7 S2/E2, and 0.946 for B8 S3/E3. The low nominal conductivities of E1 and especially E2 plausibly contribute to their lower OE, while the high-current S0/E0 batch B9 dropped to OE 0.674. I would model effective resistance as a cell-fixture term plus a material term inversely related to bulk conductivity, with hidden solvent and world residuals.

Transport efficiency should depend on D/delta, solvent relative diffusivity, viscosity-like hidden effects, current density, and possibly precipitation or surface blocking. A conventional prior would be

k_m proportional to D_eff/delta,

I_lim proportional to n*F*A*k_m*C,

TE = h(I/I_lim),

but the observed matched-pair TE values do not follow the nominal D/delta ranking in a simple way. For example, E1 has favorable declared diffusivity and layer thickness yet B6 TE 0.464 was below B5's 0.539. This is evidence that fixed world residuals, solvent coupling, kinetics, or the benchmark's definition of TE are important; the dossier alone is not an objective ranking.

7. How the explanation changed during the campaign

B1 initially showed that negative potential produced nonzero FE and moderate selectivity, but its short duration left conversion near the detection/noise floor. B2, with the sign reversed, drove FE and conversion to zero and established cathodic polarity.

B3 showed that a milder negative potential could preserve high selectivity and substantially improve efficiencies even though 300 s still gave unresolved conversion. B4 extended that condition to 3600 s and established charge/time accumulation. B5 then showed that -0.3 V was superior to -0.7 V in this local S0/E0 comparison; this changed the model from 'more negative gives more reaction' to a finite optimal potential window with side-reaction losses at excessive cathodic drive.

B6–B8 established that electrolyte/solvent identity affects acid-base state, precipitation, ohmic response, transport, selectivity, and yield. They also showed that nominal physical properties alone are insufficient to rank complete performance.

B9 and B10 bracketed the current response. B9 revealed severe high-current transport, faradaic, and ohmic penalties. B10 showed high efficiency but low throughput at small current. These batches motivated a current-limited rather than charge-only model.

B11 was decisive for the time law: at the intermediate current and favorable potential, four times longer electrolysis produced about four times the conversion without collapsing efficiency or selectivity. B12 confirmed that a different low-precipitation material pair can accumulate substantial conversion and yield during long electrolysis, while retaining material-specific pH and lower FE/TE.

8. Recommended predictive structure

For interpolation near the tested domain, I would implement the following modular model:

(1) Compute material state: effective conductivity, diffusivity, diffusion-layer thickness, double-layer capacitance, proton activity, Ksp, and equilibrium-potential shift from the nominal dossier plus fixed solvent/electrolyte interaction residuals.

(2) Compute pH from acid concentration, pKa, solvent proton activity, and an electrolysis-state correction.

(3) Compute effective cathodic overpotential eta from applied potential, material potential shift, pH, and an unknown base formal potential.

(4) Compute target and side kinetic currents with saturating activation functions. Allow excessive cathodic eta to increase side current.

(5) Limit the current through both mass transfer and cell resistance. Current demand above I_lim lowers TE; I*R loss lowers OE.

(6) Define FE from the productive fraction of interfacial current and define EE from FE, OE, overpotential utilization, and transport losses.

(7) Integrate productive current over time to predict conversion, with reactant depletion included for extrapolation toward high conversion.

(8) Predict selectivity from overpotential, pH, material residuals, and possibly extent; predict selective yield as conversion times selectivity times an uncertain product-survival/measurement factor.

(9) Predict precipitation from ion activity product relative to effective Ksp, while allowing precipitation to feed back weakly on transport or surface activity if later evidence supports it.

This model is mechanistic enough to explain the observed potential optimum, approximate time proportionality, current limitation, material-dependent pH and precipitation, and efficiency trade-offs without asserting an unjustified exact simulator equation.

9. Scope, non-identifiability, and alternatives

The strongest supported scope is interpolation around 0.020 mol reagent, 0.040 L volume, cathodic potentials from roughly -0.7 to -0.3 V, currents from 20 to 500 mA, and durations from 300 to 14400 s. Positive-potential behavior was tested only at +1.5 V. The extreme negative condition was tested only at -1.5 V and for 300 s. Quantitative extrapolation to other concentrations, volumes, electrode fixtures, temperatures, or complete conversion is not supported.

Solvent and electrolyte effects are not separately identifiable because B5–B8 changed both together. No cross-factorial S0/E1, S1/E0, and similar batches were run. The electron stoichiometry n, electrode area, electrode gap, true delivered current, formal potential, exchange-current densities, side-product identities, precipitate identity, and degradation kinetics remain unidentified. Electrode area/gap and base contact resistance were fixed across this campaign, so their effects are absorbed into common constants and cannot be separated from kinetic prefactors. There were no true replicate batches, so process variance cannot be distinguished cleanly from instrument noise.

Plausible alternatives include: a surface-adsorption optimum rather than direct competition between target and side reactions; potential-dependent electrode passivation; capacitive/nonfaradaic losses contributing to the short-time batches; precipitation changing interfacial area rather than only bulk transport; and a material-dependent final-assay response or product recovery causing the yield anomalies. The present evidence favors the coupled kinetic/transport/ohmic account, but it does not uniquely exclude these alternatives.

Overall, the most defensible explanation is a cathodic, charge-integrating conversion with a moderate-potential optimum, a target/side-current competition, strong current-dependent transport and ohmic limitations, and separate material-controlled acid-base and precipitation equilibria. Batch 11 is the clearest realization of that regime: long electrolysis at moderate current accumulated conversion while retaining the favorable FE, TE, selectivity, and energy efficiency observed in B5.

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
        "estimate": 0.61,
        "lower80": 0.52,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.455,
        "lower80": 0.37,
        "upper80": 0.54
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.13,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.425,
        "lower80": 0.34,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.024,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.035,
        "lower80": 0.0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.56,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.29,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.455,
        "lower80": 0.4,
        "upper80": 0.51
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.356,
        "lower80": 0.31,
        "upper80": 0.405
      },
      "selective_product_yield": {
        "estimate": 0.078,
        "lower80": 0.052,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.425,
        "lower80": 0.36,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.024,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.035,
        "lower80": 0.0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.57,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.62
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.404,
        "lower80": 0.32,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.094,
        "lower80": 0.05,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.085
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.49,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.33,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.51
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.349,
        "lower80": 0.27,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.064,
        "lower80": 0.028,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.27,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.085
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.43,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.24,
        "upper80": 0.47
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.301,
        "lower80": 0.22,
        "upper80": 0.385
      },
      "selective_product_yield": {
        "estimate": 0.054,
        "lower80": 0.023,
        "upper80": 0.091
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.24,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.25
      },
      "energy_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.034,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.01,
        "upper80": 0.16
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.52,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.11,
        "lower80": 0.06,
        "upper80": 0.17
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.26,
        "lower80": 0.21,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.07,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.07,
        "upper80": 0.2
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.017,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.09
      }
    }
  ],
  "rationale": "Predictions use the observed cathodic potential window, near-linear charge accumulation at moderate current, and the strong transport/faradaic/ohmic penalties seen at 500 mA. Positive-potential batches are predicted near the measurement floor. Intervals are wider for short low-product runs, untested solvent–electrolyte pairings, and high-current extrapolation; score uncertainty also reflects the selective-yield gate."
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

No mechanism-specific instance prior was supplied. The only supplied prior was the nominal material-property dossier, explicitly qualified as incomplete and subject to fixed hidden residuals.

Supported claims and self-developed laws:
- Cathodic polarity was strongly supported. B1 at -1.5 V retained nonzero FE (0.338), whereas otherwise matched B2 at +1.5 V gave FE and conversion of zero.
- Charge integration at moderate current was supported by B5 versus B11. At S0/E0, -0.3 V and 100 mA, four times the duration produced approximately four times the conversion: 0.0536 to 0.2142, while FE, transport efficiency and selectivity remained similar.
- High-current transport and ohmic limitation was supported by B9. Raising current from 100 mA in B5 to 500 mA in B9 increased conversion only from 0.0536 to 0.0711 while FE fell from 0.549 to 0.148, transport efficiency from 0.539 to 0.169, and ohmic efficiency from 0.927 to 0.674.
- Material-controlled acid/base and precipitation behavior was supported. Across B5–B8, normalized pH broadly followed the declared acid properties, while precipitation changed from about 0.99 for S0/E0 to 0.724 for S1/E1 and approximately zero for S2/E2 and S3/E3.
- The approximate relation Y ≈ conversion × selectivity was supported in B4, B5 and B11, within measurement/process variation.

Claims contradicted or weakened:
- A simple “more negative potential is better” law was contradicted. B5 at -0.3 V outperformed B4 at -0.7 V in conversion, selectivity, FE, transport efficiency and energy efficiency. B1 at -1.5 V was poorer still. This changed my judgment toward a finite favorable potential window with increasing side losses at excessive cathodic drive.
- Nominal transport properties alone did not correctly rank observed transport. For example, the favorable nominal diffusivity/layer-thickness combination of E1 did not make B6 outperform B5. Hidden residuals, solvent coupling or kinetics therefore mattered.
- An exact identity Y = conversion × selectivity was contradicted by discrepancies such as B8, where their product was about 0.020 but measured selective yield was only 0.00291. B9 and B12 deviated in the opposite direction.
- Purely linear scaling with programmed current was contradicted by B9; current-dependent transport, faradaic and ohmic losses were necessary.

Important untested elements include the exact activation law, electron stoichiometry, formal potential, identities of side products and precipitate, surface coverage or passivation, and whether precipitation affects the electrode. Solvent and electrolyte effects were not separately identified because B5–B8 changed them together. Behavior at other concentrations, volumes, temperatures, electrode fixtures and near-complete conversion also remains untested.

2. One discriminating experiment

I would use S0/E0 at the established loading of 0.020 mol in 0.040 L, set -1.5 V and 100 mA, and electrolyze in four consecutive 3600 s segments, obtaining a UV–visible efficiency measurement after each segment before the final assay.

The leading competing-current explanation predicts that excessive overpotential immediately gives a relatively low but approximately stable FE/selectivity regime; productive conversion should still accumulate roughly with charge. A surface-passivation alternative predicts progressive deterioration: FE and transport efficiency should decline systematically across segments, with final conversion markedly sublinear in total time.

Stable low efficiencies across all segments would strengthen the competing-reaction interpretation. A strong monotonic decline would shift my judgment toward passivation or surface blocking. An initial improvement followed by decline would favor activation or conditioning followed by poisoning. Stable efficiencies combined with unexpectedly poor final conversion would instead challenge both accounts and raise the probability of nonfaradaic charge, product destruction, or an incorrect conversion/yield observation model.

3. Unused evidence, reliability, and goal effects

I did not exploit the complete raw UV spectra or final-assay signal packets; my account used their processed estimates. I also did not collect intermediate pH measurements, replicate batches, blank electrolysis controls, or cross-factorial solvent/electrolyte combinations. Nominal capacitance, supporting-electrolyte concentration and several detailed calibration fields were not quantitatively incorporated. Cost and safety observations were monitored operationally but were not useful for identifying the electrochemical mechanism beyond the absence of a reported safety termination.

The least reliable sealed predictions are those for unseen solvent/electrolyte pairings, especially Q05–Q10, because material effects were confounded in the campaign. The positive-potential predictions are also uncertain in relative terms because they extrapolate near a clipped measurement floor from essentially one positive-potential batch. Q01 is uncertain because short electrolysis puts selective yield near the score gate and assay floor. Q11 and Q12 are uncertain because 500 mA combines current, duration and loading extrapolations. The batch-11 recommendation is comparatively reliable only locally: S0/E0, approximately the tested concentration, moderate current and long electrolysis. It should not be read as a universal material or scale recommendation.

The assigned explanatory goal materially affected evidence collection. I deliberately covered polarity, potential, duration, material identity and current rather than repeatedly optimizing the public score. This produced evidence for a mechanism but left too few batches for replication and a full solvent-by-electrolyte design. The secondary optimization objective did not create a clear conflict, although the final recommendation naturally favored B11 because it combined the best observed score with mechanistically interpretable performance.

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
  "arm": "MisIndexed",
  "budget": 12,
  "unit_id": "EC-W01-B12-discovery-E-MisIndexed",
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
  "prediction_evaluation": {
    "valid": true,
    "metrics": {
      "selective_product_yield": {
        "n": 12,
        "mae": 0.08169529836174722,
        "coverage80": 0.5833333333333334,
        "mean_width80": 0.042583333333333334
      },
      "electrochemical_selectivity": {
        "n": 12,
        "mae": 0.4317243006825447,
        "coverage80": 0.5,
        "mean_width80": 0.15083333333333335
      },
      "faradaic_efficiency": {
        "n": 12,
        "mae": 0.3266414983669917,
        "coverage80": 0.5,
        "mean_width80": 0.11083333333333334
      },
      "transport_efficiency": {
        "n": 12,
        "mae": 0.3089354195197423,
        "coverage80": 0.5,
        "mean_width80": 0.1425
      },
      "energy_efficiency": {
        "n": 12,
        "mae": 0.37376996159056824,
        "coverage80": 0.4166666666666667,
        "mean_width80": 0.12833333333333333
      },
      "score": {
        "n": 12,
        "mae": 0.2467211788520217,
        "coverage80": 0.5,
        "mean_width80": 0.13041666666666665
      }
    },
    "groups": {
      "potential_domain:negative": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.01082545140851289,
          "coverage80": 1.0,
          "mean_width80": 0.0665
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.03368062078952792,
          "coverage80": 1.0,
          "mean_width80": 0.18333333333333332
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.03848992655674618,
          "coverage80": 1.0,
          "mean_width80": 0.17666666666666667
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.025183636347452798,
          "coverage80": 1.0,
          "mean_width80": 0.18666666666666665
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.048925155351559314,
          "coverage80": 0.8333333333333334,
          "mean_width80": 0.20166666666666666
        },
        "score": {
          "n": 6,
          "mae": 0.028723195200165114,
          "coverage80": 1.0,
          "mean_width80": 0.16833333333333333
        }
      },
      "potential_domain:positive": {
        "selective_product_yield": {
          "n": 6,
          "mae": 0.15256514531498153,
          "coverage80": 0.16666666666666666,
          "mean_width80": 0.018666666666666665
        },
        "electrochemical_selectivity": {
          "n": 6,
          "mae": 0.8297679805755616,
          "coverage80": 0.0,
          "mean_width80": 0.11833333333333333
        },
        "faradaic_efficiency": {
          "n": 6,
          "mae": 0.6147930701772372,
          "coverage80": 0.0,
          "mean_width80": 0.045000000000000005
        },
        "transport_efficiency": {
          "n": 6,
          "mae": 0.5926872026920319,
          "coverage80": 0.0,
          "mean_width80": 0.09833333333333333
        },
        "energy_efficiency": {
          "n": 6,
          "mae": 0.6986147678295772,
          "coverage80": 0.0,
          "mean_width80": 0.055
        },
        "score": {
          "n": 6,
          "mae": 0.46471916250387824,
          "coverage80": 0.0,
          "mean_width80": 0.09250000000000001
        }
      },
      "context:current_cap": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.10918450087308884,
          "coverage80": 0.5,
          "mean_width80": 0.054
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4679648208618164,
          "coverage80": 0.5,
          "mean_width80": 0.13499999999999995
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.08282544195652009,
          "coverage80": 0.5,
          "mean_width80": 0.07500000000000001
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.06771956205368042,
          "coverage80": 0.5,
          "mean_width80": 0.11
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.1482110856473446,
          "coverage80": 0.0,
          "mean_width80": 0.11000000000000001
        },
        "score": {
          "n": 2,
          "mae": 0.17216614389419554,
          "coverage80": 0.5,
          "mean_width80": 0.0925
        }
      },
      "context:electrolyte_1": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.1236621133685112,
          "coverage80": 0.5,
          "mean_width80": 0.054000000000000006
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.46564857602119447,
          "coverage80": 0.5,
          "mean_width80": 0.14500000000000002
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.47450615334510804,
          "coverage80": 0.5,
          "mean_width80": 0.12499999999999999
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.451506153345108,
          "coverage80": 0.5,
          "mean_width80": 0.1575
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.4712391278743744,
          "coverage80": 0.5,
          "mean_width80": 0.13749999999999998
        },
        "score": {
          "n": 2,
          "mae": 0.3236199173927307,
          "coverage80": 0.5,
          "mean_width80": 0.1225
        }
      },
      "context:electrolyte_3": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.0816675751209259,
          "coverage80": 0.5,
          "mean_width80": 0.0475
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.426328182220459,
          "coverage80": 0.5,
          "mean_width80": 0.14999999999999997
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.3197946708202362,
          "coverage80": 0.5,
          "mean_width80": 0.125
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3036661875247955,
          "coverage80": 0.5,
          "mean_width80": 0.1575
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.43603315865993497,
          "coverage80": 0.5,
          "mean_width80": 0.14249999999999996
        },
        "score": {
          "n": 2,
          "mae": 0.2610508838891983,
          "coverage80": 0.5,
          "mean_width80": 0.1225
        }
      },
      "context:long": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.09576042211055755,
          "coverage80": 0.5,
          "mean_width80": 0.0355
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4535351324081421,
          "coverage80": 0.5,
          "mean_width80": 0.105
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.3564564049243927,
          "coverage80": 0.5,
          "mean_width80": 0.0725
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.34045534253120424,
          "coverage80": 0.5,
          "mean_width80": 0.11
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.41281612515449523,
          "coverage80": 0.5,
          "mean_width80": 0.1
        },
        "score": {
          "n": 2,
          "mae": 0.27549883484840393,
          "coverage80": 0.5,
          "mean_width80": 0.09250000000000001
        }
      },
      "context:short": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.00714833718817681,
          "coverage80": 1.0,
          "mean_width80": 0.0195
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.4535351324081421,
          "coverage80": 0.5,
          "mean_width80": 0.13999999999999996
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.39624676704406736,
          "coverage80": 0.5,
          "mean_width80": 0.10250000000000002
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3802457046508789,
          "coverage80": 0.5,
          "mean_width80": 0.13
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.44258867502212523,
          "coverage80": 0.5,
          "mean_width80": 0.11499999999999999
        },
        "score": {
          "n": 2,
          "mae": 0.2114161166101694,
          "coverage80": 0.5,
          "mean_width80": 0.20500000000000002
        }
      },
      "context:solvent_2": {
        "selective_product_yield": {
          "n": 2,
          "mae": 0.07274884150922298,
          "coverage80": 0.5,
          "mean_width80": 0.045
        },
        "electrochemical_selectivity": {
          "n": 2,
          "mae": 0.32333396017551425,
          "coverage80": 0.5,
          "mean_width80": 0.23000000000000004
        },
        "faradaic_efficiency": {
          "n": 2,
          "mae": 0.33001955211162565,
          "coverage80": 0.5,
          "mean_width80": 0.16499999999999998
        },
        "transport_efficiency": {
          "n": 2,
          "mae": 0.3100195670127868,
          "coverage80": 0.5,
          "mean_width80": 0.19
        },
        "energy_efficiency": {
          "n": 2,
          "mae": 0.3317315971851349,
          "coverage80": 0.5,
          "mean_width80": 0.16499999999999998
        },
        "score": {
          "n": 2,
          "mae": 0.23657517647743223,
          "coverage80": 0.5,
          "mean_width80": 0.14750000000000002
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
        "input": 422466,
        "cached_input": 390784,
        "output": 5115,
        "uncached_input": 31682
      },
      {
        "stage": "K1",
        "input": 28230,
        "cached_input": 0,
        "output": 5885,
        "uncached_input": 28230
      },
      {
        "stage": "Q",
        "input": 35956,
        "cached_input": 0,
        "output": 4225,
        "uncached_input": 35956
      },
      {
        "stage": "K2",
        "input": 40094,
        "cached_input": 28032,
        "output": 1759,
        "uncached_input": 12062
      }
    ],
    "total": {
      "input": 526746,
      "cached_input": 418816,
      "output": 16984,
      "uncached_input": 107930,
      "input_plus_output": 543730
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 476.10899999993853,
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

## Network recovery

Original failed attempt is retained separately. Mode: fresh_source; new source batches: 12. See [recovery accounting](recovery.json).
