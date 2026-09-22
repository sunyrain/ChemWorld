# EQ-E-W01--MisIndexed — final English experiment report

World `EQ-E-W01`; information arm `MisIndexed`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.04 | 0.01 | ph_meter, final_assay | 0.118885 | 0.00766614 | 0.0679871 | 0 |
| 2 | 0 | 0.04 | 0.02 | ph_meter, final_assay | 0.098877 | 0 | 0.0830033 | 0.0010793 |
| 3 | 0 | 0.08 | 0.02 | ph_meter, final_assay | 0.121229 | 0.00150804 | 0.0710477 | 0.00114902 |
| 4 | 0 | 0.06 | 0.03 | ph_meter, final_assay | 0.0988154 | 0.00825629 | 0.0740982 | 0 |
| 5 | 1 | 0.04 | 0.01 | ph_meter, final_assay | 0.128563 | 0.00495687 | 0.0700881 | 0.0089726 |
| 6 | 1 | 0.04 | 0.02 | ph_meter, final_assay | 0.0927054 | 0.000810672 | 0.0900995 | 0 |
| 7 | 1 | 0.08 | 0.02 | ph_meter, final_assay | 0.127663 | 0.00612466 | 0.0781453 | 0 |
| 8 | 1 | 0.06 | 0.03 | ph_meter, final_assay | 0.0960157 | 0.0086625 | 0.0846408 | 0.000159884 |
| 9 | 2 | 0.04 | 0.01 | ph_meter, final_assay | 0.181068 | 0.00132247 | 0.00246129 | 0 |
| 10 | 2 | 0.04 | 0.02 | ph_meter, final_assay | 0.141201 | 0.000366217 | 0.0232318 | 0.0038383 |
| 11 | 2 | 0.08 | 0.02 | ph_meter, final_assay | 0.182331 | 0 | 0.0182165 | 0 |
| 12 | 2 | 0.06 | 0.03 | ph_meter, final_assay | 0.144676 | 0 | 0.0207823 | 0 |

### Sealed evidentiary anchor

Batch `3`: Batch 3 is a useful evidentiary anchor because its medium-0, 0.25 mol/L condition at 0.08 L directly supports the scale-transfer comparison with batch 1 while retaining clearly measurable pH and precipitation responses; this is an anchor choice, not an optimum claim.

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## K1 — sealed open mechanistic report

Mechanistic report

1. Scope and experimental basis

I completed 12 batches spanning three medium selectors (0, 1, and 2), two nominal reagent concentrations, and two scales at each concentration. No catalyst, deliberate heating, or imposed aging period was used. The tested state was therefore the platform's ambient, immediate-response regime near 297 K and atmospheric pressure.

For each medium, the four designs were:
- 0.010 mol in 0.040 L: C = 0.25 mol/L, small scale.
- 0.020 mol in 0.040 L: C = 0.50 mol/L, small scale.
- 0.020 mol in 0.080 L: C = 0.25 mol/L, larger scale.
- 0.030 mol in 0.060 L: C = 0.50 mol/L, larger scale.

Every batch received an intermediate pH-meter measurement and a terminal final assay. The final-assay observations used below are:

Batch | Medium | C (mol/L) | Volume (L) | pH_normalized | Dissociation fraction | Precipitation signal | Equilibrium residual | Environment diagnostic
1 | 0 | 0.25 | 0.040 | 0.11889 | 0.00767 | 0.06799 | 0.00000 | 0.96429
2 | 0 | 0.50 | 0.040 | 0.09888 | 0.00000 | 0.08300 | 0.00108 | 0.94838
3 | 0 | 0.25 | 0.080 | 0.12123 | 0.00151 | 0.07105 | 0.00115 | 0.95840
4 | 0 | 0.50 | 0.060 | 0.09882 | 0.00826 | 0.07410 | 0.00000 | 0.93927
5 | 1 | 0.25 | 0.040 | 0.12856 | 0.00496 | 0.07009 | 0.00897 | 0.94102
6 | 1 | 0.50 | 0.040 | 0.09271 | 0.00081 | 0.09010 | 0.00000 | 0.95678
7 | 1 | 0.25 | 0.080 | 0.12766 | 0.00612 | 0.07815 | 0.00000 | 0.93290
8 | 1 | 0.50 | 0.060 | 0.09602 | 0.00866 | 0.08464 | 0.00016 | 0.94451
9 | 2 | 0.25 | 0.040 | 0.18107 | 0.00132 | 0.00246 | 0.00000 | 0.79619
10 | 2 | 0.50 | 0.040 | 0.14120 | 0.00037 | 0.02323 | 0.00384 | 0.80987
11 | 2 | 0.25 | 0.080 | 0.18233 | 0.00000 | 0.01822 | 0.00000 | 0.79628
12 | 2 | 0.50 | 0.060 | 0.14468 | 0.00000 | 0.02078 | 0.00000 | 0.80745

The last column is equilibrium_confidence, which I treat only as an environment diagnostic, not as my confidence in a mechanism.

2. Main empirical relationships

Concentration was the clearest transferable control variable. Doubling C from 0.25 to 0.50 mol/L lowered pH_normalized in every matched comparison. Averaging the two scales within each medium, the changes were:
- Medium 0: approximately -0.02121.
- Medium 1: approximately -0.03375.
- Medium 2: approximately -0.03876.

Across all six low/high pairs, the mean change was -0.03124 normalized units. Since pH_normalized = pH/14, that corresponds to an average pH decrease of about 0.44 units. This is consistent with a larger analytical weak-acid loading producing greater hydrogen-ion activity, although it does not by itself identify a thermodynamic Ka.

Precipitation generally increased with concentration. Averaged across scales, the 0.25-to-0.50 mol/L changes were about +0.00903, +0.01325, and +0.01167 for media 0, 1, and 2, respectively. The direction was consistent in all three media, but the magnitude depended on scale and was less stable than the pH response. For example, the small-scale medium-0 change was +0.01502 (batches 1 to 2), whereas the larger-scale change was only +0.00305 (batches 3 to 4).

Medium identity imposed a large offset. Four-batch final-assay means for pH_normalized were 0.10945 for medium 0, 0.11124 for medium 1, and 0.16232 for medium 2. Thus media 0 and 1 were very similar in average acidity response, while medium 2 gave substantially higher pH at both concentrations. Mean precipitation signals were 0.07403, 0.08074, and 0.01617, respectively. Medium 2 therefore strongly suppressed the measured solid-formation proxy relative to the other two media.

Scale transfer was strongest for pH. At fixed medium and concentration, changing total amount and volume while holding C constant changed pH_normalized by only -0.00090 to +0.00348 across the six comparisons. The largest difference is less than 0.049 ordinary pH unit. This makes concentration, rather than total reagent amount or vessel fill within the tested range, the best supported state variable for pH.

Precipitation transferred less exactly across scale. Its paired scale differences ranged from about -0.00891 to +0.01576. This could reflect measurement noise, finite-particle/nucleation effects, surface-to-volume effects, or a dependence on total precipitable amount that pH lacks. With one observation per scale-condition cell, these explanations cannot be separated.

3. Working mechanism

A minimal chemical representation is:

HA <-> H+ + A-
A- + X <-> S(s)

Here HA is the anonymous weak-acid-like reagent, X represents whatever medium-conditioned counter-species or precipitation partner is available, and S is the directly formed solid or solid-like state behind precipitation_signal. This notation is deliberately effective: the observations do not establish molecular identities or stoichiometry.

A useful state model would contain:
- C = added reagent amount / liquid volume.
- j = medium selector.
- a_H = hydrogen-ion activity.
- alpha = dissolved acid dissociation fraction.
- q = amount or fraction transferred into the precipitated state.
- possible nucleation or finite-scale variables governing the measured precipitation proxy.

The acid relation could be written schematically as

K_eff,j = a_H * a_A / a_HA,
pH_normalized = -log10(a_H) / 14.

The word effective is essential. Medium-dependent activity coefficients, proton buffering, ion pairing, and removal of A- into a solid can all alter an apparent equilibrium without changing an intrinsic molecular Ka.

For precipitation, a generic relation is

Q_j = a_A * a_X,
solid formation becomes favorable when Q_j exceeds Ksp_eff,j,
P_obs = clip(F_j(Q_j, C, scale, history) + measurement error, 0, 1).

This naturally couples acid dissociation to precipitation: removing A- can pull HA dissociation forward, while proton activity and medium-specific ion pairing alter the available A-. However, the observed dissociation-fraction channel is too close to its zero boundary to quantify that coupling. The final values span only 0 to 0.00866, with several exact zeros and instrument noise of comparable order. Those readings support only the statement that the observable fraction is very small under these conditions; they do not support a reliable ordering of Ka among the media.

For prediction inside the tested window, a simpler empirical model may be more defensible than a detailed equilibrium model:

pHn(j,C,V) = a_j - b_j * log10(C/C0) + small_scale_term,
P(j,C,V) = clip(p_j + g_j * (C-C0) + scale_or_nucleation_term, 0, 1).

Only two concentrations were tested, so linear-in-C, linear-in-log(C), and more mechanistic mass-action curves cannot be distinguished. The near equality of fixed-C pH pairs indicates that the scale term for pH is small over 0.04-0.08 L. It is not demonstrably negligible for precipitation.

4. How the interpretation developed

Batches 1-4 established the initial medium-0 pattern. Batches 1 versus 2 showed the concentration response at 0.040 L: pH_normalized fell from 0.11889 to 0.09888 and precipitation rose from 0.06799 to 0.08300. Batches 3 and 4 then reproduced the lower pH at 0.50 mol/L at larger scale. Batch 3 was selected as the final evidentiary anchor because its 0.25 mol/L, 0.080 L result directly supports the scale-transfer comparison with batch 1; this was not an optimization claim.

Batches 5-8 showed that medium 1 largely preserves the same concentration-controlled structure. In fact, its pH response to concentration was somewhat larger than medium 0, while its precipitation level was only modestly higher. This changed the interpretation from a single universal curve to a shared qualitative law with medium-conditioned intercepts and slopes.

Batches 9-12 produced the decisive entity separation. Medium 2 retained the same direction of concentration response, but its pH_normalized was much higher and its precipitation signal much lower. For example, at 0.25 mol/L and 0.040 L, batch 9 had pH_normalized 0.18107 and precipitation 0.00246, compared with 0.11889 and 0.06799 in batch 1. At 0.50 mol/L and 0.040 L, batch 10 had 0.14120 and 0.02323, compared with 0.09888 and 0.08300 in batch 2. These contrasts caused me to treat medium identity as a first-order modifier rather than a minor correction.

The supplied qualitative prior described selector 0 as intermediate, selector 1 as lower, and selector 2 as higher in both ionization and solid-formation tendency. The measured precipitation response does not support that mapping: selector 2 was clearly the lowest observed precipitation medium. The dissociation-fraction channel also did not confirm higher ionization for selector 2; its four-batch mean was approximately 0.00042, versus 0.00436 and 0.00514 for selectors 0 and 1, but all of these values are near the noisy, clipped zero boundary. Therefore the proper conclusion is not that the prior ordering has been precisely reversed for dissociation, but that the proposed mapping failed this observational test. For precipitation, the failure is much clearer.

5. Evidence boundaries and competing explanations

The supported domain is narrow: selectors 0-2, C = 0.25-0.50 mol/L, volumes 0.04-0.08 L, ambient temperature, no catalyst, and the specific immediate-measurement sequence used here. Interpolation within that window is more defensible than extrapolation beyond it. I would expect an intermediate concentration to have intermediate pH and usually intermediate precipitation, but that is an interpolation based on two levels, not a directly observed law. I make no claim about more dilute or concentrated solutions, other temperatures, long aging times, different mixing, or other selectors.

Several mechanisms remain observationally equivalent:

1. Medium-dependent acid thermodynamics. Medium 2 could have a smaller effective Ka or different hydrogen-ion activity coefficient, giving higher measured pH.

2. Medium buffering or background proton activity. A medium-specific acid/base reservoir could shift pH without a change in intrinsic dissociation.

3. Ion pairing or complexation. Medium 2 might bind A- or X in a soluble form, suppressing both free-ion activity and precipitation.

4. Changed precipitation thermodynamics. Medium 2 may have a larger effective solubility product, independently of acid behavior.

5. Changed nucleation or detection response. Similar equilibrium solid amounts could produce different particle populations or optical responses. The imperfect scale transfer of precipitation leaves this possibility open.

6. Direct rather than dissociation-mediated precipitation. Precipitation could depend primarily on total reagent concentration through a separate pathway, with the apparent acid/solid correlation arising because both respond to C.

7. Nonequilibrium response. Without a time series, low residuals and the platform's diagnostic cannot prove thermodynamic equilibrium. Rapid acid response combined with slower nucleation could reproduce the observations.

The experiment does not identify molecular species, activities, stoichiometric coefficients, intrinsic Ka, Ksp, kinetic constants, or solid mass. precipitation_signal is a bounded normalized proxy, not a gravimetric yield. Exact zero dissociation or precipitation values should not be interpreted as proof of physical absence because the channels are bounded and noisy. Likewise, the lower environment diagnostic for medium 2 is an observed platform diagnostic, not evidence that my medium-2 conclusions are less credible.

6. Overall conclusion

The most defensible description is an entity-conditioned, concentration-driven weak-acid/precipitation system. Increasing analytical concentration reliably lowers pH and modestly raises precipitation. The pH relationship transfers well across the tested scales, suggesting concentration control. Medium identity changes the response surface: selectors 0 and 1 behave similarly, whereas selector 2 produces higher pH and strongly suppressed precipitation while preserving the direction of the concentration effect. Acid dissociation and solid formation may be coupled through removal of a conjugate species, but the near-zero dissociation observations do not identify the coupling strength or even uniquely establish that pathway. The data support effective response relationships and reject the supplied selector-2 high-precipitation mapping, but they do not select uniquely among altered acid thermodynamics, buffering, complexation, solubility, nucleation, and nonequilibrium alternatives.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.24 | 0.17 | 0.33 |
| Q01 | acid_dissociation_fraction | 0.012 | 0 | 0.055 |
| Q01 | precipitation_signal | 0.061 | 0.03 | 0.09 |
| Q02 | pH_normalized | 0.284 | 0.19 | 0.4 |
| Q02 | acid_dissociation_fraction | 0.014 | 0 | 0.065 |
| Q02 | precipitation_signal | 0.061 | 0.03 | 0.095 |
| Q03 | pH_normalized | 0.352 | 0.235 | 0.49 |
| Q03 | acid_dissociation_fraction | 0.003 | 0 | 0.025 |
| Q03 | precipitation_signal | 0.001 | 0 | 0.02 |
| Q04 | pH_normalized | 0.155 | 0.128 | 0.188 |
| Q04 | acid_dissociation_fraction | 0.007 | 0 | 0.026 |
| Q04 | precipitation_signal | 0.063 | 0.035 | 0.092 |
| Q05 | pH_normalized | 0.174 | 0.138 | 0.216 |
| Q05 | acid_dissociation_fraction | 0.008 | 0 | 0.03 |
| Q05 | precipitation_signal | 0.065 | 0.035 | 0.098 |
| Q06 | pH_normalized | 0.231 | 0.19 | 0.278 |
| Q06 | acid_dissociation_fraction | 0.0015 | 0 | 0.013 |
| Q06 | precipitation_signal | 0.003 | 0 | 0.024 |
| Q07 | pH_normalized | 0.093 | 0.08 | 0.108 |
| Q07 | acid_dissociation_fraction | 0.0035 | 0 | 0.015 |
| Q07 | precipitation_signal | 0.083 | 0.06 | 0.105 |
| Q08 | pH_normalized | 0.087 | 0.072 | 0.103 |
| Q08 | acid_dissociation_fraction | 0.004 | 0 | 0.017 |
| Q08 | precipitation_signal | 0.093 | 0.067 | 0.12 |
| Q09 | pH_normalized | 0.135 | 0.118 | 0.152 |
| Q09 | acid_dissociation_fraction | 0.0005 | 0 | 0.008 |
| Q09 | precipitation_signal | 0.027 | 0.01 | 0.046 |
| Q10 | pH_normalized | 0.155 | 0.132 | 0.18 |
| Q10 | acid_dissociation_fraction | 0.007 | 0 | 0.023 |
| Q10 | precipitation_signal | 0.064 | 0.045 | 0.083 |
| Q11 | pH_normalized | 0.174 | 0.145 | 0.205 |
| Q11 | acid_dissociation_fraction | 0.008 | 0 | 0.026 |
| Q11 | precipitation_signal | 0.066 | 0.045 | 0.089 |
| Q12 | pH_normalized | 0.231 | 0.198 | 0.266 |
| Q12 | acid_dissociation_fraction | 0.0015 | 0 | 0.011 |
| Q12 | precipitation_signal | 0.004 | 0 | 0.022 |

### Q rationales

- **Q01**: Far-below-range extrapolation for selector 0. The pH estimate extends its observed log-concentration trend; dissociation and precipitation intervals are wide because 0.005 M was not studied.

- **Q02**: Far-below-range extrapolation for selector 1, with its observed steeper pH response partially shrunk toward the common concentration trend. Near-zero dissociation readings make dilution behavior poorly identified.

- **Q03**: Selector 2 had higher pH and strongly suppressed precipitation in every studied contrast. The very low concentration requires substantial extrapolation, reflected in the broad pH interval.

- **Q04**: Selector-0 response extrapolated moderately below 0.25 M. Concentration should dominate pH, while the smaller-than-studied volume adds uncertainty to precipitation.

- **Q05**: Prediction follows selector 1's lower-concentration pH rise and modestly higher precipitation than selector 0. Both concentration and volume extend beyond direct coverage.

- **Q06**: The selector-2 entity offset is retained while extrapolating to 0.08 M. Its precipitation estimate remains near the bounded floor, but a nonzero upper interval allows scale and model-form effects.

- **Q07**: Only a short extrapolation above the studied 0.50 M selector-0 condition. The observed direction implies slightly lower pH and slightly stronger precipitation.

- **Q08**: Short high-concentration extrapolation for selector 1. Its observed concentration slope supports lower pH and the largest predicted precipitation among the three selectors.

- **Q09**: Short extrapolation from selector 2 at 0.50 M. Higher concentration should lower pH and raise precipitation, while the strong selector-specific suppression remains.

- **Q10**: The 0.048 L scale lies within the studied volume range. Observed fixed-concentration pairs showed nearly scale-invariant pH, so this shares Q04's center with a narrower interval.

- **Q11**: Within-range scale control for selector 1. Concentration governs the central prediction; residual precipitation uncertainty reflects imperfect scale transfer in the completed batches.

- **Q12**: Within-range scale control for selector 2. The center preserves its high-pH, low-precipitation entity response, with uncertainty allowing the scale variation seen in batches 9 and 11.

Shared rationale:

Predictions use only the completed 12-batch study. For pH_normalized, I extended a medium-conditioned log-concentration relationship, partially shrinking the noisier selector-specific slopes toward a common concentration effect. Fixed-concentration comparisons supported little pH dependence on volume. Precipitation was modeled as a bounded, approximately local concentration response with medium-specific offsets and additional scale uncertainty. Acid-dissociation observations were at or near the zero boundary and comparable to instrument noise, so their estimates are conservative and their intervals intentionally broad. The 0.005 M cases are far extrapolations, 0.08 M cases are moderate extrapolations, and 0.60 M cases are short extrapolations from the observed 0.25-0.50 M range.

## K2 — sealed seven-part retrospective

1. Initial claims: supported, contradicted, or untested

The initial material did contain one substantive task-specific claim: a qualitative selector mapping. It described selector 0 as intermediate, selector 1 as lower, and selector 2 as higher in both acid-ionization tendency and solid-formation tendency. It explicitly characterized this as a local qualitative prior rather than a complete mechanism. The material catalog also warned that the selectable media had categorical benchmark effects and should not be interpreted as real-solvent predictions.

The solid-formation part of that mapping encountered direct counterevidence. In K1 I reported mean final precipitation signals of 0.07403, 0.08074, and 0.01617 for selectors 0, 1, and 2. Selector 2 was therefore not the highest observed solid-forming entity; it was clearly the lowest. The direct contrasts were large: batch 9 versus batch 1 gave 0.00246 versus 0.06799 at 0.25 M and 0.040 L, while batch 10 versus batch 2 gave 0.02323 versus 0.08300 at 0.50 M and 0.040 L. Selector 1 also did not show the proposed lower precipitation tendency relative to selector 0; its mean was modestly higher. Thus this was not merely an absence of confirmation. It was observed counterevidence, and K1 explicitly revised the interpretation by stating that the supplied selector-2 high-precipitation mapping failed its observational test.

The ionization mapping was not resolved. The final acid_dissociation_fraction means were approximately 0.00436, 0.00514, and 0.00042 for selectors 0, 1, and 2. Taken literally, that ordering also disagrees with the prior. However, the values were comparable to the assay noise, several were exactly at the bounded zero floor, and individual results were unstable across nominally related conditions. K1 therefore did not claim that the ionization ranking had been reversed. It said that the proposed mapping was not confirmed and that the channel was too weak to identify a reliable Ka ordering. That distinction remains appropriate: precipitation produced affirmative counterevidence, whereas ionization remained largely unidentifiable despite an unfavorable observed ordering.

The broad task framing of a coupled weak-acid/direct-precipitation response received partial support but was not mechanistically proven. Increasing concentration lowered pH_normalized in every matched comparison and usually increased precipitation. This is compatible with coupling, but the experiments did not establish that precipitation consumes the conjugate base or that one response causes the other. A shared dependence on analytical concentration would produce the same qualitative association.

The catalog warning against treating the categorical runtime effects as predictions about real water, ethanol, or acetonitrile chemistry was respected rather than experimentally tested. Likewise, there was no substantive nominal property dossier to validate. K1 accordingly discussed selectors and effective medium effects, not real-solvent thermodynamic constants.

2. Experiments that formed or changed the interpretation

Batches 1 and 2 formed the first concentration-response judgment. At selector 0 and 0.040 L, doubling concentration from 0.25 to 0.50 M moved pH_normalized from 0.11889 to 0.09888 and precipitation_signal from 0.06799 to 0.08300. That pair motivated the preliminary view that concentration lowers pH and promotes precipitation.

Batches 3 and 4 were important because they tested whether the selector-0 pattern survived a scale change. Batch 3 reproduced the low-concentration pH near batch 1: 0.12123 versus 0.11889. Batch 4 reproduced the high-concentration pH near batch 2: 0.09882 versus 0.09888. Those comparisons were the strongest basis for K1's statement that pH was primarily concentration-controlled over the tested scales. Precipitation transferred less cleanly, particularly batch 4 versus batch 2, which prevented an equally strong scale-invariance claim for the solid response.

Batches 5-8 changed the explanation from a single response curve to a shared qualitative relationship with entity-conditioned parameters. Selector 1 preserved the concentration direction, but its averaged pH change was larger than selector 0's and its precipitation was modestly higher. Batch 5 also had the largest final equilibrium_residual, 0.00897, showing that not every diagnostic was uniformly near zero. I did not use that isolated residual to redefine the mechanism, which was reasonable, but neither did I investigate its reproducibility.

Batches 9-12 produced the most important revision. Selector 2 preserved the direction of the concentration response while shifting the entire observed response surface: higher pH and much lower precipitation. This was the evidence that made medium identity a first-order term in K1 rather than a small correction. These batches also forced rejection of the prior solid-formation mapping.

Some experimental choices were principled but not data-derived. The four-condition pattern per selector was chosen to create two concentrations and two scale realizations at each concentration. That was a sensible factorial structure for transfer testing. However, the actual concentration range of 0.25-0.50 M was chosen before observing the response and was strongly influenced by a convenient use of the stock and vessel budgets. It was not justified by an initial dissociation constant, solubility threshold, or pilot curve. The decision to use one pH-meter measurement and one final assay in every batch maximized balanced coverage, but it left no instrument budget for time courses or genuine same-condition replicates.

The choice to omit catalyst, heating, quenching, and deliberate waiting followed the research focus on the basic medium/concentration response. It also rested on an unverified assumption that the immediate ambient sequence was adequate to represent the relevant state. K1 later listed nonequilibrium response as a competing explanation; that concern was not tested during the campaign.

Finally, I effectively committed to the repeated four-condition matrix early rather than adapting the later batches to the surprising selector-2 observations. This protected comparability and avoided outcome-driven redesign, but it meant that no dedicated follow-up tested whether selector 2's suppressed precipitation was thermodynamic, kinetic, or a measurement-boundary effect.

3. Most important competing mechanisms

The leading description remains K1's effective entity-conditioned response model: analytical concentration controls the main pH trend, while medium identity changes the effective acid and precipitation behavior. Several underlying mechanisms remain compatible with it.

First, the selectors may change acid thermodynamics or hydrogen-ion activity coefficients. This could explain different pH values at the same analytical concentration. The pH data distinguish selector 2 from selectors 0 and 1 very well, but they do not separate intrinsic Ka from activity effects.

Second, a medium-specific buffer or background acid/base reservoir could shift pH without materially changing intrinsic dissociation. The current experiment cannot distinguish this from a changed effective Ka because there was no titration, independent buffer measurement, or activity calibration.

Third, soluble ion pairing or complex formation could lower free conjugate-base or precipitation-partner activity. This could jointly produce higher pH and lower precipitation for selector 2. It is a plausible coupled explanation, but no composition-sensitive observable identified a complex.

Fourth, precipitation may have its own medium-dependent solubility or nucleation behavior. Selector 2 could suppress precipitation because the effective solubility product is larger, because nucleation is slower, or because its particles generate less final-assay signal. The scale variability in precipitation leaves all three possibilities open.

Fifth, acid and precipitation responses may be parallel rather than causally coupled. Both could respond independently to concentration and selector. The consistent concentration directions do not prove that removal of A- pulls HA dissociation forward. The near-zero dissociation channel provides little leverage on that causal question.

Sixth, the final state may retain kinetic history. No explicit wait-time series was performed. Low equilibrium_residual values and equilibrium_confidence values cannot establish thermodynamic equilibrium, especially because the latter is an environment diagnostic rather than epistemic confidence. Existing experiments can identify reproducible response differences under the used sequence, but they cannot distinguish equilibrium suppression from slow precipitation.

The present data do distinguish several empirical propositions: selector 2 gives higher measured pH and lower measured precipitation under the tested sequence; concentration has a consistent pH effect; and pH transfers across the tested scales better than precipitation. They do not identify molecular species, intrinsic Ka, Ksp, stoichiometry, nucleation constants, buffering capacity, or causal coupling.

4. One additional complete experiment, if it were permitted

I would choose an explicit aging perturbation that exactly revisits batch 9's recipe: selector 2, 0.25 M, 0.040 L, but with a preregistered one-hour wait under fixed moderate stirring before a pH-meter measurement, termination, and final assay. I would not execute it now.

This condition is preferable to another unstructured concentration point because batch 9 gave the most extreme medium contrast: pH_normalized 0.18107 and precipitation_signal 0.00246. Repeating the recipe with a controlled delay would directly probe the unresolved kinetic-versus-thermodynamic explanation while retaining batch 9 as a historical reference. It would not be a perfect causal test because the original condition lacked an exact independent replicate, but it would be highly informative for one batch.

If delayed precipitation remained near batch 9 while pH also remained near 0.181, I would increase confidence that selector 2's low precipitation is a stable medium-conditioned state rather than merely slow nucleation. It still would not prove a thermodynamic Ksp mechanism.

If precipitation rose substantially after waiting while pH remained nearly constant, I would revise K1 toward a nucleation- or growth-limited explanation with weak feedback on proton activity. The assumption that the terminal assay represented a time-independent equilibrium response would become untenable.

If both precipitation increased and pH shifted downward or upward beyond assay variability, I would favor a coupled relaxation process in which solid formation and acid speciation co-evolve. The direction of the pH shift would constrain, but not uniquely identify, which dissolved species is removed.

If pH changed substantially while precipitation remained near zero, I would favor slow acid/base equilibration, buffering, or activity relaxation rather than precipitation-controlled coupling.

If the result differed erratically from batch 9 without a coherent shift, the immediate priority would become repeatability rather than adding mechanistic complexity.

5. Tradeoff between identifiability and operational score

The campaign was designed primarily for mechanism characterization, not optimization. That choice was aligned with the stated research goal. I used all three selectors and deliberately retained selector 2 even though its environment diagnostic was much lower, about 0.80 rather than about 0.94-0.95 for selectors 0 and 1. A score-seeking strategy using the published scoring weights might instead have concentrated on conditions with high equilibrium_confidence, low residual, and stronger precipitation. Allocating one-third of the campaign to selector 2 therefore sacrificed likely scalar score in exchange for identifying the entity contrast and testing the supplied mapping.

Likewise, the fixed concentration-by-scale structure sacrificed opportunities to adaptively search for a high-scoring condition. Batches 3, 7, and 11 were not necessary if the only objective had been maximizing a scalar result; they were included to assess transfer at constant concentration. This was an identifiability-oriented choice.

There was nevertheless an important limitation: the design favored broad, balanced mapping over deep mechanistic identifiability. It did not include true replicates, a time perturbation, a temperature perturbation, or a concentration close to a precipitation onset. Those omissions made the empirical response surface identifiable but left causal mechanisms underdetermined. In that sense, the campaign did not sacrifice identifiability for optimization; it sacrificed deeper identifiability for economical coverage.

There was also no deliberate attempt to improve score through catalysts, heating, or process manipulation. Avoiding those operations made the interpretation cleaner because concentration and selector remained the principal variables. Conversely, the concentration range may have been unnecessarily narrow for identifying the acid law, even though it generated stable, reasonably high-diagnostic batches. The research objective justified not chasing the best score, but it did not fully justify the lack of a low-concentration mechanistic anchor.

6. Underused evidence and weaknesses in the blind predictions

The intermediate pH-meter data were underused. They broadly agreed with the final pH assay in the printed results, but I did not formally construct a paired measurement-error model. Their precipitation and dissociation channels could also have helped quantify floor clipping and cross-instrument consistency. In particular, the intermediate observations for selector 2 frequently reported zero precipitation while the final assay returned small positive values. That pattern was relevant to distinguishing detection-boundary behavior from real growth during the sequence, yet it was not developed quantitatively in K1.

The referenced characterization artifacts and raw spectral packets were not inspected during the campaign. Consequently, peak structure, calibration metadata, missingness, and possible saturation flags were not used. I relied almost entirely on processed estimates. This was an evidentiary loss, even though it would not have authorized inference of hidden composition.

The scale pairs were also only partially exploited. They could serve as approximate reproducibility checks, but the scale ratios differed: the low-concentration comparison doubled volume, whereas the high-concentration comparison increased it only from 0.040 to 0.060 L. Thus a single generic scale term was not cleanly identified. K1 correctly noted precipitation's poorer transfer, but the sealed predictions still treated the scale effect rather simply.

The least reliable blind predictions are Q01-Q03. Their concentration, 0.005 M, is fifty times below the lowest studied value, and their volume, 0.024 L, is also below the studied range. I extrapolated selector-conditioned log-concentration pH relationships from only two concentration levels. Q02 and Q03 are especially fragile because their selector-specific slopes were estimated from four noisy batches and then only informally shrunk toward a common trend. The 80% pH intervals may still be too narrow for uncertainty about functional form. The low-concentration acid_dissociation_fraction intervals may also be too narrow because a true dilution-driven increase could be much stronger than my conservative estimates.

Q04-Q06 and Q10-Q12 are also extrapolations, not interpolations: 0.08 M is more than threefold below the studied minimum. The Q10-Q12 volumes fall within the studied volume range, but that does not resolve concentration-law uncertainty. My sealed rationales called these moderate extrapolations, yet their pH and precipitation intervals—especially Q10's pH interval of 0.132-0.180 and Q12's precipitation interval of 0-0.022—may understate the possibility of curvature or a precipitation threshold.

Q07-Q09 are closer in concentration, at 0.60 M versus the studied maximum of 0.50 M, but their 0.024 L volume lies outside the scale range. They are more reliable than Q01-Q06 because the concentration extrapolation is short, although precipitation could still respond to total amount or nucleation volume in an unmodeled way.

The precipitation predictions at 0.005 M are particularly model-dependent. The sealed predictions retained approximately 0.061 signals for selectors 0 and 1 by extending an empirical medium-specific offset. A physically amount-dependent or threshold model could instead approach zero. K1 explicitly listed both direct concentration response and nucleation/detection alternatives, so the point estimates selected one extrapolation more strongly than the report justified.

These weaknesses are consistent with, rather than revisions to, K1's declared evidence boundary. K1 limited support to 0.25-0.50 M and 0.04-0.08 L and warned that interpolation was more defensible than extrapolation. Every blind query is outside that domain in concentration, volume, or both. The sealed Q rationale acknowledged this, but some numerical intervals did not fully propagate the model-form uncertainty that K1 had described.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 3: selector 0, 0.25 M, 0.080 L. K1 was explicit that this was an evidentiary anchor because it paired with batch 1 for a scale-transfer comparison, not an optimum claim.

Batch 3 has only one final assay. Its apparent agreement with batch 1 does not establish repeatability because the two batches used different total amounts and volumes and therefore are not exact replicates. A repeatability test would require multiple independent executions of the exact batch-3 recipe, analyzed with the same measurement sequence and with all outcomes retained.

Local robustness would require preregistered perturbations around batch 3: small changes in concentration, volume at constant concentration, waiting time, mixing, and temperature. Those experiments would determine whether the observed response sits on a smooth plateau, near a threshold, or in a history-sensitive region. The current evidence only shows one nearby scale comparison and one higher-concentration comparison.

Cross-material generalization would require repeating the same local design for selectors 1 and 2 and then for genuinely different material systems. The existing batches show that transfer across selectors cannot be assumed: selector 2 shifts both pH and precipitation substantially. Cross-world generalization is even less justified because the catalog describes bounded categorical benchmark effects rather than a universal physical solvent model. It would require independent worlds with the same preregistered protocol and a hierarchical analysis of which relationships persist.

The recommendation should therefore not be described as either sample-in highest or proven optimal. It was not selected by comparing all batches for the maximum scalar score, and I did not establish that it was the best member of the sampled set for any optimization criterion. Even a sample-in maximum would only mean highest among 12 noisy observations. Demonstrating an optimum would require replicated local search, robustness checks, an explicitly declared objective, and evidence that nearby legal conditions do not perform better. None of those conditions was met. The defensible claim is narrower: batch 3 was a useful, completed reference condition for the observed concentration-versus-scale relationship.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0128189 | 1 | 0.0933333 | 0.0933333 |
| acid_dissociation_fraction | 0.0204213 | 0.816667 | 0.0261667 | 0.105347 |
| precipitation_signal | 0.0182529 | 0.683333 | 0.0439167 | 0.111709 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0525976 |
| 0.08 | 0.01191 |
| 0.6 | 0.00439048 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00115139 |
| 1 | 0.00298506 |
| 2 | 0.00178501 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
