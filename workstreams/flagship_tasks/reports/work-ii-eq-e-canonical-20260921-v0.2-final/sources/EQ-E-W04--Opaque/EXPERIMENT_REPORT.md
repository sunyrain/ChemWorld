# EQ-E-W04--Opaque — final English experiment report

World `EQ-E-W04`; information arm `Opaque`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 12.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.06 | 0.006 | ph_meter, final_assay | 0.201343 | 0.00227455 | 0.0118076 | 0 |
| 2 | 1 | 0.06 | 0.006 | ph_meter, final_assay | 0.154411 | 0.00509367 | 0.0587585 | 0 |
| 3 | 2 | 0.06 | 0.006 | ph_meter, final_assay | 0.223482 | 0.00774591 | 0.00186836 | 0 |
| 4 | 0 | 0.04 | 0.012 | ph_meter, final_assay | 0.137899 | 0.00106206 | 0.0365979 | 0.00468163 |
| 5 | 1 | 0.04 | 0.012 | ph_meter, final_assay | 0.106708 | 0.00197894 | 0.110944 | 0 |
| 6 | 2 | 0.04 | 0.012 | ph_meter, final_assay | 0.166993 | 0 | 0.0129438 | 0.000718692 |
| 7 | 0 | 0.08 | 0.024 | ph_meter, final_assay | 0.136583 | 0.00291118 | 0.0455284 | 0 |
| 8 | 1 | 0.08 | 0.024 | ph_meter, final_assay | 0.105919 | 0 | 0.0993161 | 0 |
| 9 | 2 | 0.08 | 0.024 | ph_meter, final_assay | 0.164185 | 0.00748048 | 0.0154756 | 0 |
| 10 | 0 | 0.06 | 0.03 | ph_meter, final_assay | 0.117004 | 0 | 0.0545408 | 0.00270517 |
| 11 | 1 | 0.06 | 0.03 | ph_meter, final_assay | 0.0878197 | 0.0027781 | 0.128525 | 9.31114e-05 |
| 12 | 2 | 0.06 | 0.03 | ph_meter, final_assay | 0.129694 | 0 | 0.0367749 | 0.00735362 |

### Sealed evidentiary anchor

Batch `5`: A useful evidentiary anchor because its 0.30 mol/L, 0.04 L medium-1 condition sits in both the cross-medium comparison and the matched-concentration scale pair, with a clear precipitation response; this is an anchor, not an optimum claim.

## K1 — sealed open mechanistic report

Mechanistic report

1. Scope and evidence base

I completed 12 batches spanning three selectable medium identities, three nominal reagent concentrations, and one matched-concentration scale comparison. The tested identities were medium 0 (the interface called it Water), medium 1 (Ethanol), and medium 2 (Acetonitrile). These names identify selectable materials, but the supplied material information explicitly says their reaction effects are categorical benchmark effects rather than predictions from real-solvent property correlations. I therefore treat 0, 1, and 2 as empirical entity labels, not as permission to import external solvent chemistry.

The design for each medium was:
- 0.10 mol/L at 0.060 L: 0.006 mol reagent.
- 0.30 mol/L at 0.040 L: 0.012 mol reagent.
- 0.30 mol/L at 0.080 L: 0.024 mol reagent.
- 0.50 mol/L at 0.060 L: 0.030 mol reagent.

No catalyst, heating, or deliberate waiting intervention was used. Each batch received an intermediate pH-meter measurement and, after termination, a final assay. The numerical analysis below uses the recorded final-assay endpoints. I do not invent values for intermediate packets that were not retained in my public observations.

The final observations were:

Batch | Medium | C (mol/L) | V (L) | pH/14 | Dissociation fraction | Precipitation signal | Equilibrium residual | Environment equilibrium diagnostic
1 | 0 | 0.10 | 0.060 | 0.201343 | 0.002275 | 0.011808 | 0.000000 | 0.825072
2 | 1 | 0.10 | 0.060 | 0.154411 | 0.005094 | 0.058758 | 0.000000 | 0.946030
3 | 2 | 0.10 | 0.060 | 0.223482 | 0.007746 | 0.001868 | 0.000000 | 0.820029
4 | 0 | 0.30 | 0.040 | 0.137899 | 0.001062 | 0.036598 | 0.004682 | 0.855648
5 | 1 | 0.30 | 0.040 | 0.106708 | 0.001979 | 0.110944 | 0.000000 | 0.970702
6 | 2 | 0.30 | 0.040 | 0.166993 | 0.000000 | 0.012944 | 0.000719 | 0.794162
7 | 0 | 0.30 | 0.080 | 0.136583 | 0.002911 | 0.045528 | 0.000000 | 0.851691
8 | 1 | 0.30 | 0.080 | 0.105919 | 0.000000 | 0.099316 | 0.000000 | 0.967295
9 | 2 | 0.30 | 0.080 | 0.164185 | 0.007480 | 0.015476 | 0.000000 | 0.809633
10 | 0 | 0.50 | 0.060 | 0.117004 | 0.000000 | 0.054541 | 0.002705 | 0.865838
11 | 1 | 0.50 | 0.060 | 0.087820 | 0.002778 | 0.128525 | 0.000093 | 0.945179
12 | 2 | 0.50 | 0.060 | 0.129694 | 0.000000 | 0.036775 | 0.007354 | 0.825534

The last column is an environment diagnostic, not my confidence in the interpretation.

2. Empirical entity mapping

Across every tested concentration, medium 1 produced the lowest normalized pH and the largest precipitation signal. Medium 2 produced the highest normalized pH and the smallest precipitation signal. Medium 0 was intermediate. This repeated ordering is the strongest entity-conditioned result:

pH/14: medium 1 < medium 0 < medium 2
precipitation: medium 1 > medium 0 > medium 2

At 0.10 mol/L, for example, the normalized pH values were 0.1544, 0.2013, and 0.2235 for media 1, 0, and 2, while precipitation signals were 0.0588, 0.0118, and 0.00187. At 0.50 mol/L the same ordering remained: pH/14 was 0.0878, 0.1170, and 0.1297, and precipitation was 0.1285, 0.0545, and 0.0368.

This is an empirical phenotype mapping, not a ranking of media for an optimization objective. It also should not be translated into claims about real ethanol, water, or acetonitrile because the runtime contract states that the effects are benchmark-categorical.

No task-specific qualitative property dossier was supplied. Consequently, there was no independent nominal mapping such as “identity X must be most acidic” that could be prospectively confirmed or falsified. The defensible mapping is the one learned from these observations: entity 1 is the lower-pH/high-precipitation phenotype, entity 2 is the higher-pH/low-precipitation phenotype, and entity 0 is intermediate over the tested range.

3. Concentration relationships

For all three entities, increasing nominal reagent concentration from 0.10 to 0.50 mol/L lowered pH/14 and increased precipitation. Thus concentration and medium identity act jointly rather than either variable replacing the other.

A compact descriptive representation over 0.10–0.50 mol/L is

    y_pH(m,C) = a_m + b_m ln(C / 1 mol L^-1) + error,
    P(m,C) = alpha_m + beta_m C + error,

where y_pH is pH/14 and P is the bounded precipitation signal. Least-squares fits to the four observations for each medium, including both 0.30 mol/L scales, give:

- Medium 0: y_pH = 0.07554 - 0.05379 ln C; P = 0.00507 + 0.10683 C.
- Medium 1: y_pH = 0.05706 - 0.04194 ln C; P = 0.04706 + 0.17442 C.
- Medium 2: y_pH = 0.09413 - 0.05697 ln C; P = -0.00941 + 0.08727 C.

The descriptive root-mean-square residuals are 0.00320, 0.00131, and 0.00313 for normalized pH and 0.00505, 0.00706, and 0.00271 for precipitation in media 0, 1, and 2, respectively. These fits summarize the measured window; they are not established physical laws. In particular, the negative precipitation intercept for medium 2 demonstrates why the linear precipitation equation must not be extrapolated toward zero concentration. A thresholded or saturating law would be more physically plausible outside the observed interval.

Converted to ordinary pH units, the fitted changes per tenfold concentration increase are approximately -1.73, -1.35, and -1.84 pH units for media 0, 1, and 2. These slopes are much steeper than the -0.5 pH-unit-per-decade dependence of an isolated ideal monoprotic weak acid in its simplest asymptotic regime. Therefore a bare ideal weak-acid equation is insufficient here. Activity effects, concentration-dependent effective parameters, precipitation coupling, or an intentionally non-ideal benchmark response are needed.

The precipitation slopes differ by entity: medium 1 has the largest fitted slope, medium 0 is intermediate, and medium 2 is smallest. Thus the medium effect is not merely a constant precipitation offset; it plausibly changes both baseline propensity and concentration sensitivity. With only four points per medium, however, offset and slope differences are not sharply separable.

4. Scale transfer

Batches 4–9 provide the direct scale test at fixed nominal concentration, 0.30 mol/L, comparing 0.040 and 0.080 L.

For medium 0, doubling volume changed pH/14 from 0.137899 to 0.136583 and precipitation from 0.036598 to 0.045528. For medium 1, the corresponding changes were 0.106708 to 0.105919 and 0.110944 to 0.099316. For medium 2, they were 0.166993 to 0.164185 and 0.012944 to 0.015476.

The absolute normalized-pH differences were only 0.00079–0.00281. Precipitation differences were 0.00253–0.01163. Relative to the declared final-assay noise scales of 0.002 for normalized pH and 0.006 for precipitation, these are small to modest single-comparison discrepancies. The entity ordering was unchanged at both scales. The evidence therefore supports concentration-based transfer between 0.040 and 0.080 L more strongly than it supports a material scale term.

This does not prove exact scale invariance. Each scale was run only once, so random batch variability is inseparable from volume effects. The data bound any large scale effect but do not resolve a subtle one.

5. Proposed effective mechanism

A minimal process representation is:

    HA ⇌ H+ + A-                     effective acid dissociation
    r A- + counter-species ⇌ Solid   direct precipitation proxy

with medium-conditioned effective parameters:

    K_a,eff = K_a,eff(m, C)
    K_sp,eff = K_sp,eff(m, C)
    activity coefficients = gamma_i(m, C)

A possible qualitative sequence is:

1. Adding reagent establishes a medium-dependent proton-activity response.
2. The same medium changes the effective solubility or nucleation propensity of an anion-containing or otherwise acid-coupled solid.
3. Increasing total concentration raises supersaturation, so the precipitation proxy increases.
4. Precipitation may remove one dissolved equilibrium participant, shifting acid dissociation and proton activity by mass action.
5. At fixed concentration, these effective equilibria are approximately intensive across the tested twofold volume change.

In pseudocode:

    input: entity m, total concentration C, volume V
    h = acid_activity_response(m, C)
    supersaturation = precipitation_drive(m, C, h)
    P = bounded_response(supersaturation)
    h = coupled_mass_action_update(h, P, m)
    output pH = -log10(h), precipitation P

The observations establish the signs of two net relationships in the tested domain:

    d(pH)/dC < 0
    dP/dC > 0

and establish persistent entity offsets/orderings. They do not establish which arrow in the proposed coupling is causal. Lower pH could promote precipitation, precipitation could shift acid equilibrium, or medium identity and concentration could drive both responses in parallel.

The acid-dissociation-fraction channel does not presently identify a useful law. Every final value was between 0 and 0.00775, comparable to the declared assay noise standard deviation of 0.006; four batches were reported at the lower boundary of zero. Those zeros should be interpreted as noisy, clipped near-zero estimates, not proof of exactly zero dissociation. The channel was neither monotonic in concentration nor consistently ordered by medium. It is therefore unsafe to estimate a microscopic Ka, precipitation stoichiometry, or dissolved-species balance from it.

Likewise, the equilibrium residuals were small (0 to 0.00735), but that only indicates close agreement with the environment’s internal effective-equilibrium diagnostic. It does not uniquely validate the two-reaction mechanism above. The environment equilibrium diagnostic ranged from 0.794 to 0.971 and is not used as epistemic confidence.

6. How the evidence changed the interpretation

Batches 1–3 first established that the entity effect was large and structured: medium 1 was already lower in pH and higher in precipitation, while medium 2 showed the opposite phenotype. This made a single medium-independent acid curve untenable.

Batches 4–6 showed that the same ordering survived at 0.30 mol/L and that precipitation increased substantially for all entities. Batch 5 was particularly useful because its central concentration and small scale participated in both the cross-entity comparison and the subsequent scale comparison; it was therefore selected as the evidentiary anchor, not as an optimum.

Batches 7–9 tested the matched-concentration scale transfer. Their close pH agreement with batches 4–6 shifted the interpretation toward concentration-controlled, approximately intensive behavior rather than a dominant dependence on total reagent amount or vessel volume.

Batches 10–12 confirmed the entity ordering at 0.50 mol/L. They also discouraged a pure fixed-offset model: the gaps and fitted precipitation slopes vary by medium. Batch 12 had the largest equilibrium residual, 0.00735, which cautions against treating the high-concentration endpoint as perfectly represented by a simple equilibrium curve.

The near-zero and irregular dissociation-fraction measurements throughout caused me to weaken any microscopic weak-acid interpretation. The robust evidence concerns pH response and precipitation proxy, not a quantitatively identified molecular dissociation fraction.

7. Competing explanations

Several explanations remain observationally equivalent or nearly so:

- Parallel medium effects: the medium separately changes effective acidity and precipitation propensity, with no direct causal coupling between the two outputs.
- Precipitation-driven acid shift: removal of a dissolved species by precipitation drives additional dissociation or changes proton activity through mass action.
- Acidity-driven precipitation: proton activity changes the form or availability of the precipitating species.
- Shared activity-coefficient effect: medium and concentration change non-ideal activities, producing correlated pH and precipitation without a simple stoichiometric coupling.
- Kinetic or nucleation response: the precipitation proxy may partly reflect nucleation or finite-time particle formation rather than a thermodynamic solubility boundary.
- Measurement-floor explanation for dissociation: true differences could exist below the resolution of the dissociation channel, making the apparently irregular fractions largely noise and clipping.
- Campaign-order drift: concentrations were executed in ascending blocks rather than randomized. Consequently, the concentration trend is partially confounded with run order. The repeated within-block entity ordering is less vulnerable to this issue, but an unmodelled temporal drift could imitate part of the concentration dependence.

The current observations cannot distinguish these explanations decisively.

8. Applicability and evidence boundaries

Supported domain:
- Only media 0, 1, and 2.
- Nominal concentrations from 0.10 to 0.50 mol/L.
- Volumes from 0.040 to 0.080 L.
- Near the ambient initial conditions used here, without deliberate heating, catalyst addition, or controlled residence-time variation.
- The benchmark’s normalized precipitation proxy and synthetic pH/final-assay channels, not real-sample behavior.

Not identified:
- A microscopic Ka, Ksp, activity coefficient, solid stoichiometry, nucleation order, or species identity.
- Whether equilibrium was reached kinetically at a particular physical time.
- Small scale effects hidden by batch and measurement variability.
- Behavior below 0.10 mol/L, above 0.50 mol/L, outside 0.040–0.080 L, at other temperatures, or for the untested fourth selectable medium.
- Whether the observed concentration slopes would persist under randomized run order.
- A causal direction between acidity and precipitation.

9. Bottom-line world model

Within the measured slice, the world behaves as a medium-conditioned, non-ideal weak-acid/direct-precipitation system. Total concentration is the main continuous driver: greater concentration lowers pH and raises precipitation. Medium identity shifts both responses and probably changes their sensitivities. The entity-conditioned relationships transfer approximately across a twofold scale change when concentration is held fixed. Medium 1 consistently realizes a lower-pH, more precipitation-prone effective state; medium 2 realizes a higher-pH, less precipitation-prone state; medium 0 lies between them. A coupled mass-action model with medium-dependent effective acidity and solubility is plausible, but the data equally permit parallel medium effects, activity-coefficient changes, or finite-time precipitation behavior. The pH and precipitation relationships are supported; a microscopic dissociation mechanism is not yet identifiable.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.361 | 0.3 | 0.422 |
| Q01 | acid_dissociation_fraction | 0.006 | 0 | 0.022 |
| Q01 | precipitation_signal | 0.006 | 0 | 0.022 |
| Q02 | pH_normalized | 0.279 | 0.229 | 0.331 |
| Q02 | acid_dissociation_fraction | 0.01 | 0 | 0.028 |
| Q02 | precipitation_signal | 0.048 | 0.025 | 0.071 |
| Q03 | pH_normalized | 0.396 | 0.33 | 0.463 |
| Q03 | acid_dissociation_fraction | 0.022 | 0.002 | 0.046 |
| Q03 | precipitation_signal | 0.001 | 0 | 0.015 |
| Q04 | pH_normalized | 0.211 | 0.201 | 0.222 |
| Q04 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q04 | precipitation_signal | 0.014 | 0 | 0.028 |
| Q05 | pH_normalized | 0.163 | 0.155 | 0.172 |
| Q05 | acid_dissociation_fraction | 0.005 | 0 | 0.016 |
| Q05 | precipitation_signal | 0.061 | 0.043 | 0.08 |
| Q06 | pH_normalized | 0.238 | 0.227 | 0.249 |
| Q06 | acid_dissociation_fraction | 0.009 | 0 | 0.022 |
| Q06 | precipitation_signal | 0.002 | 0 | 0.014 |
| Q07 | pH_normalized | 0.103 | 0.093 | 0.113 |
| Q07 | acid_dissociation_fraction | 0.001 | 0 | 0.011 |
| Q07 | precipitation_signal | 0.069 | 0.055 | 0.084 |
| Q08 | pH_normalized | 0.078 | 0.071 | 0.087 |
| Q08 | acid_dissociation_fraction | 0.001 | 0 | 0.012 |
| Q08 | precipitation_signal | 0.152 | 0.132 | 0.172 |
| Q09 | pH_normalized | 0.123 | 0.113 | 0.134 |
| Q09 | acid_dissociation_fraction | 0.001 | 0 | 0.012 |
| Q09 | precipitation_signal | 0.043 | 0.032 | 0.055 |
| Q10 | pH_normalized | 0.211 | 0.204 | 0.219 |
| Q10 | acid_dissociation_fraction | 0.003 | 0 | 0.013 |
| Q10 | precipitation_signal | 0.014 | 0.003 | 0.025 |
| Q11 | pH_normalized | 0.163 | 0.157 | 0.169 |
| Q11 | acid_dissociation_fraction | 0.005 | 0 | 0.015 |
| Q11 | precipitation_signal | 0.061 | 0.047 | 0.075 |
| Q12 | pH_normalized | 0.238 | 0.23 | 0.246 |
| Q12 | acid_dissociation_fraction | 0.009 | 0 | 0.02 |
| Q12 | precipitation_signal | 0.002 | 0 | 0.012 |

### Q rationales

- **Q01**: This is a substantial downward concentration extrapolation for selector 0. The pH estimate extends its observed log-concentration relationship, while precipitation is projected near its lower boundary. The interval is widened for extrapolation and the untested 0.024 L scale.

- **Q02**: Selector 1 retained a sizable precipitation offset throughout the observed range, so its low-concentration precipitation estimate remains above those of the other selectors. The broad interval reflects extrapolation twentyfold below the lowest studied concentration.

- **Q03**: Selector 2 had the highest pH and lowest precipitation at every measured concentration. Its fitted dissociation trend rises toward dilution, but that channel was close to its noise floor, so the dissociation interval is deliberately broad.

- **Q04**: The concentration is only slightly below the measured 0.10 mol/L endpoint. The point estimate follows the selector-0 concentration curves; uncertainty is enlarged modestly because 0.024 L is below the tested scale range.

- **Q05**: Selector 1 is predicted to preserve its lower-pH, higher-precipitation phenotype near the observed low-concentration boundary. The precipitation interval includes model scatter and the smaller untested volume.

- **Q06**: Selector 2 is projected to remain the highest-pH and least-precipitating entity at 0.08 mol/L. Its precipitation estimate is near the bounded floor, and its dissociation estimate is uncertain because measured fractions were noise-dominated.

- **Q07**: This is a modest extrapolation above the measured 0.50 mol/L selector-0 endpoint. The estimate continues the observed decrease in pH and increase in precipitation, with additional allowance for high-concentration curvature and the smaller scale.

- **Q08**: Selector 1 consistently gave the lowest pH and strongest precipitation response. Extrapolating its fitted trends from 0.50 to 0.60 mol/L yields the largest predicted precipitation signal among the three selectors.

- **Q09**: The estimate extends selector 2 only slightly beyond the measured range. Its higher-pH, lower-precipitation ordering is retained, while the dissociation prediction remains near zero because that channel did not support a stable concentration law.

- **Q10**: The point estimate matches Q04 because the research supported concentration-based transfer across scale. The 0.048 L volume lies within the studied scale interval, so its interval is narrower than the corresponding 0.024 L prediction.

- **Q11**: The point estimate is shared with Q05 under the supported approximate scale invariance. Selector 1 remains the lower-pH, higher-precipitation entity, with reduced scale uncertainty at 0.048 L.

- **Q12**: The prediction uses the same concentration response as Q06 because the measured twofold scale comparison showed no stable volume effect. Selector 2 remains near the precipitation floor, so the bounded interval is asymmetric.

Shared rationale:

Predictions use only the sealed 12-batch study. For each selector, normalized pH was extrapolated from a descriptive linear relationship with log concentration; precipitation used a local linear concentration relationship clipped at the physical zero bound. The matched 0.30 mol/L experiments supported approximate concentration-based scale transfer, so equal-concentration scale-control pairs share point estimates. Intervals include final-assay noise, observed model scatter, weakly identified scale effects, and extra uncertainty outside the studied concentration or volume ranges. Acid-dissociation fractions were comparable to the declared assay noise and frequently clipped to zero, so those intervals are broad and should not be read as precise microscopic Ka predictions.

## K2 — sealed seven-part retrospective

No prediction truth has been disclosed, and I performed no additional experiment. This is therefore a prospective self-audit of the sealed K1 mechanism report and the sealed Q predictions, not a post-outcome explanation.

1. Initial claims: supported, challenged, or untested

The initial material contained little substantive, falsifiable chemistry. It defined the world as a bounded synthetic weak-acid/direct-precipitation slice, stated that pH_normalized = pH/14, and warned that selectable material effects were categorical benchmark effects rather than predictions from real-solvent properties. It supplied no task-specific property dossier and no qualitative ordering of selectors 0–2. Consequently, there was no prior claim such as “selector 1 must precipitate most” that the campaign could genuinely validate.

Supported claims or framing:
- Medium identity matters. Batches 1–3, 4–6, and 10–12 repeatedly gave the same ordering: selector 1 had lower pH and more precipitation than selector 0, while selector 2 had higher pH and less precipitation. This supports the stated premise that entity identity conditions the response.
- Concentration matters within this weak-acid/precipitation slice. For every selector, the measured progression from 0.10 to 0.50 mol/L lowered normalized pH and increased precipitation.
- The response is approximately intensive over the tested scale interval. At 0.30 mol/L, batches 4 versus 7, 5 versus 8, and 6 versus 9 showed small pH differences across 0.040 and 0.080 L. This supports limited concentration-based transfer, not universal scale invariance.
- The warning not to interpret the public material names as real-solvent mechanistic predictions remains appropriate. Nothing in the experiment independently linked the observed categorical effects to real water, ethanol, or acetonitrile properties.

Challenged or narrowed claims:
- A simple microscopic weak-acid interpretation was not supported quantitatively. Dissociation estimates ranged only from 0 to 0.00775, were often clipped at zero, and were comparable to the declared final-assay noise of 0.006. K1 explicitly revised the interpretation to: “The robust evidence concerns pH response and precipitation proxy, not a quantitatively identified molecular dissociation fraction.”
- A bare ideal monoprotic weak-acid law was inconsistent with the descriptive pH slopes. K1 noted fitted changes of about -1.35 to -1.84 pH units per decade of concentration, much steeper than the simplest ideal weak-acid asymptote.
- The word “coupled” was not causally established. Correlated pH and precipitation changes are compatible with coupling, but also with two parallel selector- and concentration-dependent responses.

Still untested:
- No supplied qualitative selector mapping existed, so none was tested against an independent prior.
- Molecular Ka, Ksp, precipitate identity, stoichiometry, nucleation law, activity coefficients, and causal direction remain unidentified.
- Equilibrium versus finite-time kinetics was not tested because residence time was not varied.
- Temperature dependence, catalyst effects, the fourth selectable material, and behavior outside 0.10–0.50 mol/L and 0.040–0.080 L were not tested.
- The synthetic-boundary statement is a scope condition, not a chemical hypothesis that these experiments could falsify.

I distinguish lack of contradiction from affirmative support: the scale pairs produced no compelling evidence of a large volume effect, but one batch at each scale cannot prove exact scale invariance. I do not identify a substantive initial claim for which clear counterevidence appeared and was knowingly ignored. The main counterevidence was against my natural but optional simple-acid hypothesis, and K1 did revise that hypothesis rather than preserving it unchanged.

2. Experiments that formed or changed the interpretation

Batches 1–3 genuinely formed the entity mapping. At 0.10 mol/L, normalized pH was 0.2013, 0.1544, and 0.2235 for selectors 0, 1, and 2, while precipitation was 0.0118, 0.0588, and 0.00187. This immediately ruled out a single selector-independent response curve.

Batches 4–6 changed the interpretation from a one-point selector contrast to a concentration-dependent phenotype. At 0.30 mol/L and 0.040 L, the same selector ordering remained, and batch 5 showed a particularly clear selector-1 response: pH_normalized 0.1067 and precipitation 0.1109.

Batches 7–9 were the most direct mechanism-oriented intervention because they held concentration at 0.30 mol/L while doubling volume from 0.040 to 0.080 L. Their close pH agreement with batches 4–6 shifted my view toward approximately intensive, concentration-controlled behavior. They did not prove it, because scale and independent batch variation were not separable.

Batches 10–12 established that the ordering survived to 0.50 mol/L. They also weakened a pure common-slope/fixed-offset description. For example, selector 1 reached precipitation 0.1285 in batch 11, whereas selector 2 reached only 0.0368 in batch 12. Batch 12’s equilibrium residual of 0.00735, the largest observed, was one reason K1 did not claim a perfectly described high-concentration equilibrium curve.

The irregular dissociation measurements across all batches changed my confidence in microscopic interpretation. For example, selector 2 gave 0.00775 in batch 3, zero in batch 6, 0.00748 in batch 9, and zero in batch 12. That sequence is not a credible basis for a precise Ka law.

Several design choices were made before relevant evidence existed:
- Choosing selectors 0–2 and leaving selector 3 untested was based on my interpretation of the requested three-entity study, not on empirical evidence that these were the most informative three.
- The concentrations 0.10, 0.30, and 0.50 mol/L and the 0.040/0.080 L scale pair were design guesses intended to span loading and test intensivity.
- Concentrations were executed in ascending blocks rather than randomized. That was convenient for a structured comparison but left concentration partially confounded with campaign order.
- I used one intermediate pH measurement per batch because the measurement contract made it relevant, but I did not preserve and analyze the detailed intermediate outputs adequately.

Thus the selector ordering, concentration signs, and limited scale transfer were data-driven judgments. The functional forms—log-linear pH and locally linear precipitation—were post-campaign descriptive choices, not laws specified by the initial material.

3. Most important competing mechanisms

The leading explanations remain:

A. Direct thermodynamic coupling. A weak-acid equilibrium produces an anionic or otherwise coupled dissolved form, and precipitation removes one participant. Mass action then shifts proton activity and precipitation together.

B. Parallel medium effects. Selector identity separately changes effective acidity and precipitation propensity. The two outputs correlate because they share selector and concentration as causes, not because either output causes the other.

C. Non-ideal activity effects. Concentration- and selector-dependent activity coefficients generate the steep pH response and alter supersaturation. This could mimic a coupled two-equilibrium mechanism without constant microscopic Ka or Ksp.

D. Finite-time nucleation or growth. The precipitation signal may report a kinetic particle-formation state rather than a thermodynamic solubility endpoint. Different selectors could change nucleation rate, while pH responds rapidly and independently.

E. Campaign-order or instrumental drift. Because concentration increased with run order, part of the concentration trend could be temporal rather than chemical. Repeated selector ordering within each concentration block makes a purely temporal explanation less plausible for the entity contrast, but it does not eliminate drift as a contributor to slopes.

What the campaign distinguished:
- The repeated entity ordering rejects a single selector-independent curve.
- The 0.30 mol/L scale pairs argue against a dominant dependence on total moles or volume over 0.040–0.080 L.
- The concentration series argues against a constant response within each selector.
- The dissociation data fail to support a precise microscopic weak-acid law.

What it did not distinguish:
- Coupling from common-cause parallel responses.
- Thermodynamic precipitation from finite-time nucleation.
- Activity-coefficient changes from concentration-dependent effective equilibrium constants.
- Small scale effects from batch noise.
- Chemical concentration effects from the portion of the trend attributable to campaign order.

K1 correctly described a coupled mass-action model as “plausible” rather than uniquely established. The most important unresolved contrast is direct acid/precipitation coupling versus parallel selector-conditioned responses, followed closely by equilibrium versus kinetics.

4. One additional legal complete experiment

If exactly one additional complete experiment were allowed, I would repeat the batch-5 composition—selector 1, 0.012 mol reagent in 0.040 L, nominally 0.30 mol/L—but add an explicit time-course perturbation. I would measure with the pH meter immediately after mixing, wait for a declared period such as 3600 s under fixed stirring and unchanged temperature, measure again with the pH meter, terminate, and obtain the required final assay. This should be regarded as a proposed experiment only; I did not execute it.

Why this condition:
- Selector 1 had the strongest precipitation signal, increasing sensitivity to kinetic change.
- The composition exactly anchors to batch 5, which had pH_normalized 0.1067 and precipitation 0.1109.
- Batch 8 supplies a related 0.30 mol/L large-scale comparison.
- A time intervention addresses the most important untested distinction more directly than another concentration point.

Interpretation of possible outcomes:
- Little or no change between the two pH-meter readings, followed by a final assay close to batch 5, would support approximate equilibration and repeatability. It would weaken, but not eliminate, a slow nucleation explanation.
- A progressive rise in precipitation signal with a corresponding pH shift would support finite-time coupling or slow equilibration. The direction of the pH shift would constrain, though not uniquely identify, the mass-action relationship.
- Precipitation changing without a meaningful pH change would favor parallel kinetics or weak coupling.
- pH changing without precipitation changing would favor slow acid/base or activity equilibration rather than precipitation-driven feedback.
- Stable within-batch readings but a final endpoint far from batch 5 would point toward batch variability, campaign drift, or an instrument/channel discrepancy.

One batch still could not establish a kinetic law or independently estimate repeatability. Repeated randomized time courses would be required for that, but they exceed the one-experiment restriction.

5. Trade-off between mechanistic identifiability and operational score

The research goal explicitly asked for characterization and entity mapping, not medium ranking or optimization. I therefore allocated all 12 batches to balanced coverage: four conditions for each of three selectors, including a matched-concentration scale pair. This sacrificed opportunities to concentrate runs in conditions likely to maximize the scalar score, especially selector-1 conditions with high environment equilibrium diagnostics and strong precipitation.

Conversely, the design was not maximally identifiable either. It spent one batch per condition and used the two 0.30 mol/L volumes as both a scale test and the only repeated-concentration evidence. It lacked randomized order, same-condition replication, time variation, and temperature perturbation. A more rigorous mechanism study would have sacrificed some concentration breadth to obtain replication and a kinetic intervention.

There is no evidence that I altered conditions adaptively to chase favorable outcomes. The crossed plan was fixed before the endpoint pattern was known. Low-response selector-2 batches were retained rather than replaced, which is appropriate for characterization but potentially unfavorable for operational scoring.

Batch 5 was sealed as an evidentiary anchor because it lay at the intersection of the entity contrast and scale comparison, not because it was proven optimal. It did have the largest recorded environment equilibrium diagnostic, 0.9707, but that diagnostic was explicitly not the research objective or my epistemic confidence. Batch 11, not batch 5, had the largest observed precipitation signal, 0.1285. Different metrics therefore identify different sample-in “best” batches.

Overall, I favored breadth and identifiability over score optimization, but not enough to achieve strong causal identification. The principal sacrifice for identifiability was running all three selectors and the scale pairs rather than repeatedly exploiting selector 1. The principal remaining weakness was sacrificing replication and randomization for coverage.

6. Underused evidence and weaknesses in the blind predictions

Underused or difficult evidence:
- I purchased an intermediate pH-meter measurement in every batch, but the concise outputs I retained did not expose the numerical processed values. I therefore failed to use the possible within-batch comparison between intermediate and final pH/precipitation channels.
- I did not systematically retain or model the raw final-assay spectra, replicate signals, calibration metadata, or channel-level uncertainty. Batch 1 visibly returned a detailed packet, but I did not build a comparable channel-level dataset across all 12 batches.
- Equilibrium residuals and the environment diagnostic were summarized but not incorporated into a heteroscedastic model.
- The scale pairs were used descriptively, but one observation at each scale could not estimate a scale-effect variance separately from batch variance.
- The declared instrument noise was used heuristically rather than through a formal censored-error model, especially for dissociation values clipped at zero.

Least reliable blind predictions:
- Q01–Q03 at 0.005 mol/L are the least reliable. They extrapolate twentyfold below the lowest studied concentration. The sealed predictions extended the log-linear pH model to 0.361, 0.279, and 0.396, respectively. K1 had explicitly limited support to 0.10–0.50 mol/L, so these are model-dependent extrapolations, not evidence-backed interpolation.
- Q03’s dissociation estimate of 0.022 with an 80% interval of 0.002–0.046 is particularly weak. Giving it a positive lower bound conflicts with K1’s conclusion that the dissociation channel was noise-dominated and frequently clipped to zero. Its interval should likely have included zero.
- Q02’s precipitation prediction of 0.048 with interval 0.025–0.071 may be too confident. It extends a fitted selector-1 intercept far below the measured domain, although precipitation might instead approach zero through a threshold or nonlinear law.
- Q04–Q06 are close to the concentration range at 0.08 mol/L, but their 0.024 L volume is below the studied minimum of 0.040 L. The pH intervals, especially Q05’s 0.155–0.172 and Q06’s 0.227–0.249, may be too narrow because they do not fully account for model-form, order-confounding, and scale-extrapolation uncertainty.
- Q07–Q09 at 0.60 mol/L are only modest concentration extrapolations, but they combine high-concentration curvature risk with the untested 0.024 L scale. Their point ordering is better supported than their exact intervals.
- Q10–Q12 at 0.08 mol/L and 0.048 L are comparatively the most defensible because their volume lies within the studied scale range and concentration is close to 0.10 mol/L. Even these are not true interpolations in concentration and lack independent replication.

The shared point estimates assigned to Q04/Q10, Q05/Q11, and Q06/Q12 appropriately reflected K1’s approximate scale-transfer judgment. However, K1 said that the evidence “supports concentration-based transfer ... more strongly than it supports a material scale term,” not that volume has exactly zero effect. The Q intervals may not fully represent that distinction.

The largest inconsistency between K1 and Q is therefore not the selector ordering; that was strongly supported. It is the degree of quantitative confidence assigned outside K1’s stated applicability domain, especially the low-concentration dissociation and precipitation predictions. Without prediction truth, I cannot say these predictions are inaccurate, only that their evidential calibration is weaker than their numerical precision suggests.

7. Limitations of the sealed recommendation

The sealed recommendation selected experiment 5: selector 1, 0.30 mol/L, 0.040 L. Its rationale was that it served as a central evidentiary anchor participating in both the cross-selector comparison and the matched-concentration scale comparison. That is a defensible archival selection, but it has several limitations:

- It is a single realization with no exact replicate.
- It does not establish repeatability or distinguish batch variation from instrument noise.
- Its strong precipitation response and high environment diagnostic do not make it universally preferable.
- It was not tested under timing, temperature, mixing, or small concentration perturbations.
- It says nothing direct about selector 3 or worlds with different latent parameterizations.
- It is an evidence anchor, not a validated operating recommendation for real materials.

Repeatability should be tested by several independent exact repeats of batch 5 distributed across randomized campaign positions, with the same final assay and retained intermediate measurements. This would estimate within-condition variance and reveal order drift.

Local robustness should be tested with small perturbations around the anchor, for example 0.25, 0.30, and 0.35 mol/L; nearby volumes while holding concentration fixed; and declared waiting or stirring changes. A robust local region would preserve the selector phenotype and yield smoothly varying endpoints rather than a narrow accidental maximum.

Cross-material generalization requires the same local perturbation design for selectors 0 and 2 and inclusion of the untested selector 3. The observed selector-1 behavior cannot be assumed to transfer to other identities.

Cross-world generalization requires independent benchmark worlds or latent parameter draws under the same public contract. Repeating only within this one world would establish reproducibility here, not portability across worlds.

Finally, “sample-in highest” and “proven optimal” are categorically different. Batch 5 had the highest observed environment equilibrium diagnostic, while batch 11 had the highest observed precipitation signal; neither fact defines a unique overall optimum. Even if batch 5 had achieved the highest scalar score among the 12 tested batches, that would only make it the best observed member of a sparse, non-optimization design. Proving an optimum would require a declared objective, systematic local and boundary search, replication, uncertainty-aware comparisons, and validation on held-out runs. None of those conditions was satisfied, and the sealed recommendation did not claim otherwise.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0235573 | 0.683333 | 0.0430833 | 0.112811 |
| acid_dissociation_fraction | 0.0110335 | 0.833333 | 0.0190833 | 0.0777905 |
| precipitation_signal | 0.0104824 | 0.75 | 0.0263333 | 0.051798 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0446062 |
| 0.08 | 0.00637973 |
| 0.6 | 0.00332589 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00176991 |
| 1 | 0.0016389 |
| 2 | 0.00178524 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
