# EQ-E-W03--Opaque — final English experiment report

World `EQ-E-W03`; information arm `Opaque`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 61 recorded operations. Exact replay is `True`; rollbacks: 2.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.04 | 0.004 | ph_meter, final_assay, final_assay | 0.157466 | 0.00692352 | 0.0493206 | 0 |
| 2 | 0 | 0.04 | 0.016 | ph_meter, final_assay | 0.0907716 | 0.00169903 | 0.124465 | 0 |
| 3 | 0 | 0.08 | 0.008 | ph_meter, final_assay | 0.152149 | 0.0113299 | 0.0609174 | 0 |
| 4 | 0 | 0.08 | 0.032 | ph_meter, final_assay | 0.0922084 | 0.00514249 | 0.115781 | 0.000789334 |
| 5 | 1 | 0.04 | 0.004 | ph_meter, final_assay | 0.184503 | 0.00594355 | 0.01864 | 0 |
| 6 | 1 | 0.04 | 0.016 | ph_meter, final_assay | 0.119248 | 0.0062421 | 0.0560375 | 0.00155326 |
| 7 | 1 | 0.08 | 0.008 | ph_meter, final_assay | 0.188776 | 0 | 0.0259192 | 0.00128943 |
| 8 | 1 | 0.08 | 0.032 | ph_meter, final_assay | 0.122054 | 0 | 0.0495945 | 0 |
| 9 | 2 | 0.04 | 0.004 | ph_meter, final_assay | 0.233049 | 0.0216643 | 0 | 0.00237571 |
| 10 | 2 | 0.04 | 0.016 | ph_meter, final_assay | 0.148319 | 0 | 0 | 0.000788686 |
| 11 | 2 | 0.08 | 0.008 | ph_meter, final_assay | 0.232869 | 0.00889268 | 0 | 0 |
| 12 | 2 | 0.08 | 0.032 | ph_meter, final_assay | 0.152157 | 0.00236041 | 0.0131899 | 0 |

### Sealed evidentiary anchor

Batch `4`: Batch 4 is a useful evidentiary anchor because its high-loading, large-scale medium-0 response shows a clear precipitation signal and directly pairs with the same-concentration small-scale batch for transfer assessment; this is an anchor choice, not an optimum claim.

## K1 — sealed open mechanistic report

Mechanistic report

1. Scope and experimental design

I completed 12 batches spanning three anonymous aqueous-medium identities (0, 1, and 2). For every medium I used a 2 × 2 concentration–scale design:

- low concentration, small scale: 0.004 mol reagent in 0.040 L, C = 0.10 mol L^-1;
- high concentration, small scale: 0.016 mol in 0.040 L, C = 0.40 mol L^-1;
- low concentration, large scale: 0.008 mol in 0.080 L, C = 0.10 mol L^-1;
- high concentration, large scale: 0.032 mol in 0.080 L, C = 0.40 mol L^-1.

Thus, doubling both reagent amount and volume held concentration fixed and tested scale transfer. I added no catalyst and applied no heat, programmed waiting, or quench. Conditions therefore describe the bounded, nominally ambient response near 297.4 K, not a kinetic or catalyst study.

All 12 batches produced valid terminal final assays. Eleven also had valid in-process pH-meter measurements. In batch 1, an attempted pH measurement containing an unsupported replicate-count field failed validation and produced no measurement or instrument charge. An initial final-assay request in the same batch failed for the same interface reason; a subsequent valid request completed the assay. These were validation failures, not adverse chemical outcomes. I treat the terminal final assay as the primary comparable endpoint across all 12 batches.

The reported pH variable is pH_normalized = pH/14. Precipitation_signal is a bounded proxy rather than a recovered precipitate mass. Acid_dissociation_fraction is also a processed bounded estimate. Equilibrium_confidence is an environment diagnostic and is not my confidence in this report.

2. Primary observations

The terminal results were:

Batch | Medium | C (mol L^-1) | Volume (L) | pH_normalized | Acid dissociation fraction | Precipitation signal | Equilibrium residual | Environment equilibrium diagnostic
1 | 0 | 0.10 | 0.040 | 0.15747 | 0.00692 | 0.04932 | 0 | 0.94662
2 | 0 | 0.40 | 0.040 | 0.09077 | 0.00170 | 0.12446 | 0 | 0.95088
3 | 0 | 0.10 | 0.080 | 0.15215 | 0.01133 | 0.06092 | 0 | 0.93394
4 | 0 | 0.40 | 0.080 | 0.09221 | 0.00514 | 0.11578 | 0.00079 | 0.95623
5 | 1 | 0.10 | 0.040 | 0.18450 | 0.00594 | 0.01864 | 0 | 0.84920
6 | 1 | 0.40 | 0.040 | 0.11925 | 0.00624 | 0.05604 | 0.00155 | 0.87542
7 | 1 | 0.10 | 0.080 | 0.18878 | 0 | 0.02592 | 0.00129 | 0.84335
8 | 1 | 0.40 | 0.080 | 0.12205 | 0 | 0.04959 | 0 | 0.87495
9 | 2 | 0.10 | 0.040 | 0.23305 | 0.02166 | 0 | 0.00238 | 0.81527
10 | 2 | 0.40 | 0.040 | 0.14832 | 0 | 0 | 0.00079 | 0.80671
11 | 2 | 0.10 | 0.080 | 0.23287 | 0.00889 | 0 | 0 | 0.81242
12 | 2 | 0.40 | 0.080 | 0.15216 | 0.00236 | 0.01319 | 0 | 0.80078

Averaging the two scales at each concentration gives the clearest empirical entity map:

- Medium 0: pH_normalized fell from 0.15481 at 0.10 M to 0.09149 at 0.40 M, while precipitation_signal rose from 0.05512 to 0.12012.
- Medium 1: pH_normalized fell from 0.18664 to 0.12065, while precipitation_signal rose from 0.02228 to 0.05282.
- Medium 2: pH_normalized fell from 0.23296 to 0.15024, while precipitation_signal changed only from 0 to 0.00659 and remained at or near the response floor.

Multiplying pH_normalized by 14, solely using the declared transformation, these averaged endpoints correspond approximately to pH 2.17 and 1.28 for medium 0, 2.61 and 1.69 for medium 1, and 3.26 and 2.10 for medium 2. These are transformed observations, not independent measurements.

3. Working explanation of how the bounded world operates

The most economical explanation has three parts.

First, reagent concentration is the dominant tested control of the acid response. Increasing C from 0.10 to 0.40 M lowered pH_normalized in every medium by 0.0633, 0.0660, and 0.0827 for media 0, 1, and 2 respectively. Doubling total amount and volume together produced only small changes, so the response transfers primarily with concentration rather than total reagent amount over 0.04–0.08 L.

Second, the medium identity shifts both the acid-response baseline and its precipitation coupling. At either tested concentration the ordering of pH_normalized was medium 2 > medium 1 > medium 0. The precipitation ordering was the reverse in practical terms: medium 0 showed the strongest signal, medium 1 an intermediate signal, and medium 2 essentially no detectable signal. Consequently, medium identity cannot be represented merely as a common additive pH offset if precipitation is also to be explained; it changes the effective precipitation propensity.

Third, precipitation and acidity are coupled but not by a single medium-independent function of measured pH. Within media 0 and 1, raising concentration simultaneously lowered pH_normalized and increased precipitation_signal. However, medium 2 underwent a similarly large pH shift without a comparable precipitation response. Thus pH or proton activity alone is insufficient. A latent medium-conditioned solubility, association, nucleation, or activity term is required.

A useful descriptive representation is:

C = n_reagent / V

H_m(C) = h_m + f_m(C)

P_m(C) = clip[g_m(C, H_m, a_m), 0, 1]

where H is pH_normalized, P is precipitation_signal, m is medium identity, and a_m represents unobserved medium-specific activity/solubility/nucleation effects. Over only the observed interval, a linear interpolation is adequate as a descriptive model:

H_m(C) ≈ H_m(0.10) + beta_m(C - 0.10)

with beta approximately -0.211, -0.220, and -0.276 normalized-pH units per mol L^-1 for media 0, 1, and 2. Corresponding precipitation slopes were approximately +0.217, +0.102, and +0.022 signal units per mol L^-1. These slopes are interpolants between two concentrations, not established laws and not justified for extrapolation outside 0.10–0.40 M.

A mechanistic cartoon consistent with the data is:

reagent in medium m ⇌ protonated/deprotonated dissolved forms

dissolved forms + medium-conditioned counter-species/association environment ⇌ precipitating form

precipitating form → bounded precipitation proxy

Medium identity changes effective activities and/or the precipitation branch. Concentration pushes the acid equilibrium toward lower measured pH in all three media, but the same change accesses the precipitation branch strongly in medium 0, moderately in medium 1, and weakly or not detectably in medium 2.

4. Evidence that formed or changed this explanation

Batch 1 established a low-concentration medium-0 endpoint with pH_normalized 0.15747 and precipitation_signal 0.04932. Batch 2 then raised concentration at the same volume and changed those values to 0.09077 and 0.12446. That large paired change first suggested coupled concentration-dependent acidification and precipitation.

Batches 3 and 4 repeated the two concentrations at twice the scale. Their endpoints closely reproduced batches 1 and 2. In particular, batches 2 and 4, both at 0.40 M, gave precipitation signals 0.12446 and 0.11578. This supported concentration rather than absolute reagent amount as the transferable coordinate. Batch 4 was therefore selected as the final evidentiary anchor: it provides a clear high-loading response at the larger scale and pairs directly with batch 2. The selection is not an optimization claim.

Batches 5–8 showed that the concentration relationship transfers qualitatively to medium 1, but with higher pH_normalized and substantially weaker precipitation. This modified the initial explanation from a universal concentration curve to a medium-conditioned family of curves.

Batches 9–12 forced the more important revision. Medium 2 retained a strong pH response to concentration, yet three of four final precipitation signals were exactly zero and the fourth was only 0.01319. Therefore I reject a simple universal rule such as “lower pH directly determines more precipitation.” The data instead require an additional medium-specific gate or susceptibility for direct precipitation.

Scale matching was strong overall. Across the six medium-by-concentration pairs, the mean absolute small-versus-large difference was 0.00297 for pH_normalized and 0.00787 for precipitation_signal. The declared final-assay noise scales are 0.002 and 0.006 respectively, so the observed scale discrepancies are modest and of roughly the same order as measurement/process uncertainty. There is no compelling scale effect in the tested range, although the design cannot prove exact scale invariance.

5. Acid-dissociation estimate and sensor agreement

The acid_dissociation_fraction estimates were generally small and often comparable to the declared final-assay noise scale of 0.006. Several readings were clipped at zero. Medium 2 at low concentration gave the largest values, 0.02166 in batch 9 and 0.00889 in batch 11, but the high-concentration medium-2 values were 0 and 0.00236. This might indicate concentration-dependent effective dissociation, but the floor, noise, and absence of direct species measurements prevent a secure quantitative law.

I therefore give greater weight to the reproducible pH_normalized contrasts than to fine differences in acid_dissociation_fraction. The data do not justify equating that processed fraction with a single molecular dissociation equilibrium or applying a Henderson–Hasselbalch model without additional composition and activity information.

The 11 valid in-process pH-meter measurements agreed qualitatively with the final assays on concentration and medium trends. Exact precipitation estimates sometimes differed by several hundredths between instruments, consistent with the pH meter's larger declared precipitation uncertainty and with the fact that these are processed proxies. Instrument agreement supports the broad relationships but not high-precision parameterization.

6. Equilibrium residual and diagnostic

Terminal equilibrium_residual values ranged from 0 to 0.00238; most were zero. These values are small relative to the declared 0.004 final-assay uncertainty scale. They show that the environment's endpoint consistency criterion was usually satisfied, but they do not independently establish a physical equilibrium mechanism.

The mean environment equilibrium diagnostic was approximately 0.947 for medium 0, 0.861 for medium 1, and 0.809 for medium 2. This medium ordering is reproducible, but equilibrium_confidence is explicitly an environment diagnostic. I do not interpret it as statistical confidence, chemical certainty, or a goodness-of-fit probability.

7. Supported relationships

Within the tested domain, the evidence supports the following statements:

- Reagent concentration, not total reagent amount alone, is the main transferable control across 0.040–0.080 L.
- Raising concentration from 0.10 to 0.40 M lowers pH_normalized in all three media.
- Medium identity strongly shifts the pH response.
- Medium identity even more strongly conditions precipitation propensity.
- Media 0 and 1 show coupled acidification and increased precipitation with concentration.
- Medium 2 shows acidification without substantial precipitation, demonstrating that precipitation is not a universal one-variable function of pH_normalized.
- Any scale effect in the tested twofold range is smaller than the concentration and medium effects and is close to the combined measurement/process variation.

8. Boundaries and unidentified factors

The report applies only to the bounded synthetic weak-acid/direct-precipitation benchmark, the three tested medium identities, concentrations 0.10 and 0.40 M, volumes 0.040 and 0.080 L, nominal ambient temperature, no catalyst, and the particular operation ordering used. It is not evidence about arbitrary aqueous chemistry or real named solvent systems.

Only two concentration levels were tested, so curvature, thresholds, saturation, and non-monotonicity remain unidentified. Only two scales were tested, so larger-volume mixing, heat-transfer, and nucleation effects remain open. There were no time courses, deliberate equilibration waits, temperature changes, catalyst interventions, isolated-solid measurements, or direct species concentrations. Precipitation_signal cannot be converted into precipitate mass, yield, solubility product, or crystal population from these data.

No task-specific nominal property dossier or qualitative identity-to-mechanism mapping was supplied beyond the selectable anonymous categories. Accordingly, I can map empirical behaviors to medium indices 0–2, but I cannot infer hidden molecular identities or validate a named-material explanation.

The design provides matched scale pairs rather than true repeated assays at identical amount and volume. Consequently, the small between-scale differences combine possible scale effects with run-to-run variation. Formal significance claims are not warranted.

9. Reasonable competing explanations

Several mechanisms remain observationally equivalent:

1. Thermodynamic explanation: each medium changes effective acid activities and the solubility of a precipitating form. Medium 0 has the greatest precipitation propensity and medium 2 the least.

2. Activity-coefficient explanation: reagent concentration changes ionic strength or other nonideal activities; nominal molarity is only a proxy for the relevant thermodynamic coordinate.

3. Speciation or complexation explanation: a hidden medium-dependent associated species may feed precipitation independently of the measured acid fraction.

4. Kinetic/nucleation explanation: the endpoint proxy may reflect nucleation or aggregation rates rather than equilibrium solubility. The apparent scale transfer argues against a large effect over the tested twofold scale range but cannot eliminate it because no time course was measured.

5. Matrix/sensor explanation: medium identity may alter calibration or response factors for the processed pH and precipitation proxies. Cross-instrument qualitative agreement reduces, but does not remove, this possibility.

6. Detection-floor explanation for medium 2: its true precipitation response may be small but nonzero and masked by clipping/noise. The observations establish “near or below the benchmark's detectable floor,” not absolute absence of a solid phase.

10. Testable predictions, clearly marked as extrapolative

Within 0.10–0.40 M and 0.040–0.080 L, I would predict that intermediate concentrations produce monotonically intermediate pH_normalized values for all media. I would also predict intermediate precipitation signals for media 0 and 1, while medium 2 remains close to the floor. These are interpolations from two concentration levels, not new observations.

For a further twofold scale change at fixed concentration, I would predict much smaller changes in pH_normalized and precipitation_signal than would result from changing concentration from 0.10 to 0.40 M. This extrapolates the observed scale transfer and could fail if mixing or nucleation becomes important.

A direct test distinguishing thermodynamic from kinetic explanations would require time-resolved measurements or controlled waiting, while distinguishing activity/speciation explanations would require independent species or ionic-activity measurements. Neither was performed here.

Overall, the defensible model is a family of medium-conditioned concentration-response relationships with a shared acidification trend but a strongly medium-specific precipitation branch. The concentration relationship transfers across the tested twofold scale change; a universal pH-to-precipitation law does not.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.292 | 0.23 | 0.36 |
| Q01 | acid_dissociation_fraction | 0.041 | 0.006 | 0.09 |
| Q01 | precipitation_signal | 0.035 | 0.005 | 0.07 |
| Q02 | pH_normalized | 0.329 | 0.26 | 0.4 |
| Q02 | acid_dissociation_fraction | 0.014 | 0 | 0.05 |
| Q02 | precipitation_signal | 0.013 | 0 | 0.045 |
| Q03 | pH_normalized | 0.412 | 0.32 | 0.5 |
| Q03 | acid_dissociation_fraction | 0.055 | 0 | 0.14 |
| Q03 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q04 | pH_normalized | 0.165 | 0.153 | 0.178 |
| Q04 | acid_dissociation_fraction | 0.01 | 0 | 0.026 |
| Q04 | precipitation_signal | 0.051 | 0.032 | 0.071 |
| Q05 | pH_normalized | 0.197 | 0.184 | 0.211 |
| Q05 | acid_dissociation_fraction | 0.004 | 0 | 0.018 |
| Q05 | precipitation_signal | 0.02 | 0.004 | 0.039 |
| Q06 | pH_normalized | 0.246 | 0.231 | 0.262 |
| Q06 | acid_dissociation_fraction | 0.017 | 0 | 0.043 |
| Q06 | precipitation_signal | 0.002 | 0 | 0.018 |
| Q07 | pH_normalized | 0.073 | 0.051 | 0.096 |
| Q07 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q07 | precipitation_signal | 0.163 | 0.125 | 0.205 |
| Q08 | pH_normalized | 0.101 | 0.078 | 0.126 |
| Q08 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q08 | precipitation_signal | 0.073 | 0.041 | 0.109 |
| Q09 | pH_normalized | 0.126 | 0.098 | 0.156 |
| Q09 | acid_dissociation_fraction | 0.001 | 0 | 0.013 |
| Q09 | precipitation_signal | 0.011 | 0 | 0.041 |
| Q10 | pH_normalized | 0.165 | 0.155 | 0.176 |
| Q10 | acid_dissociation_fraction | 0.01 | 0 | 0.024 |
| Q10 | precipitation_signal | 0.051 | 0.035 | 0.068 |
| Q11 | pH_normalized | 0.197 | 0.187 | 0.208 |
| Q11 | acid_dissociation_fraction | 0.004 | 0 | 0.016 |
| Q11 | precipitation_signal | 0.02 | 0.006 | 0.036 |
| Q12 | pH_normalized | 0.246 | 0.234 | 0.259 |
| Q12 | acid_dissociation_fraction | 0.017 | 0 | 0.039 |
| Q12 | precipitation_signal | 0.002 | 0 | 0.015 |

### Q rationales

- **Q01**: Far-below-range extrapolation for medium 0. A log-concentration acid-response continuation predicts higher normalized pH, while the empirical precipitation trend approaches a small positive baseline. The interval is widened substantially because 0.005 M and 0.024 L were not studied.

- **Q02**: Medium 1 is predicted to retain its higher-pH and lower-precipitation behavior relative to medium 0. This is a long concentration extrapolation, so the interval includes weak or undetectable precipitation and substantial model uncertainty.

- **Q03**: Medium 2 had the highest normalized pH and precipitation at the response floor in the observed study. The very dilute prediction preserves that ordering, but both the dissociation estimate and pH extrapolation are highly uncertain because the requested concentration is twentyfold below the lowest observation.

- **Q04**: This is only slightly below the observed 0.10 M medium-0 condition. Concentration-based interpolation/extrapolation predicts a modestly higher pH and modestly lower precipitation. The smaller volume adds limited uncertainty because scale effects were weak.

- **Q05**: The prediction extends the medium-1 low-concentration response from 0.10 M to 0.08 M. It retains medium 1's intermediate pH and weak precipitation, with uncertainty covering near-floor precipitation.

- **Q06**: Medium 2 is predicted to remain the highest-pH identity and to produce essentially floor-level precipitation at 0.08 M. The dissociation interval is broad because observed fractions were small, noisy, and sometimes clipped at zero.

- **Q07**: This extrapolates the medium-0 high-concentration branch beyond 0.40 M. The predicted endpoint has the lowest pH and strongest precipitation among the three media, but uncertainty is widened for possible curvature or saturation.

- **Q08**: Medium 1 is projected to continue its concentration-dependent acidification and moderate precipitation response. The estimate preserves its position between media 0 and 2 while allowing appreciable uncertainty outside the studied concentration range.

- **Q09**: Medium 2 should acidify at 0.60 M but is predicted to retain a strongly suppressed precipitation branch. The interval permits a small detectable response because batch 12 produced a nonzero signal and the high-concentration extrapolation is uncertain.

- **Q10**: This shares concentration with Q04 but uses a volume inside the previously tested scale range. The point estimate is therefore concentration-matched, with a slightly narrower interval because the study supported transfer across 0.040–0.080 L.

- **Q11**: The medium-1 prediction matches Q05 in concentration and differs only in scale. The observed scale pairs showed much smaller variation than the concentration and identity contrasts, so the central prediction is unchanged.

- **Q12**: At the scale-controlled 0.08 M condition, medium 2 is predicted to preserve its high-pH, precipitation-suppressed phenotype. The interval remains asymmetric at the physical zero boundary.

Shared rationale:

Predictions use the 12 completed final assays from the concentration-by-scale study. Normalized pH was extrapolated primarily as a medium-specific function of log concentration; precipitation used the observed medium-specific concentration trend with clipping at zero; acid dissociation used a weak-acid-style dilution trend but was assigned broad intervals because the measured fractions were close to assay noise and frequently clipped. Point estimates are concentration-driven because matched 0.040 and 0.080 L experiments showed mean absolute scale differences of only about 0.003 in normalized pH and 0.008 in precipitation signal. Intervals combine observed paired-scale variation, declared final-assay noise, response-floor effects, and additional model uncertainty. They are widest at 0.005 M and 0.60 M because both lie outside the observed 0.10–0.40 M range; no new experiments were performed.

## K2 — sealed seven-part retrospective

1. Assessment of claims in the initial information

The initial packet did not provide a substantive task-specific mechanism, numerical parameterization, or qualitative mapping of medium identities to response classes. It explicitly stated that no task-specific nominal property dossier was supplied, that experimental evidence was authoritative, and that the selectable formulations had categorical benchmark effects rather than validated real-material implications. The prior record was null. Therefore, there was no meaningful initial claim such as “medium 0 precipitates most” or “pH uniquely controls precipitation” to confirm or refute.

Several contractual statements were respected but were not experimental hypotheses: pH_normalized was defined as pH/14; precipitation_signal and acid_dissociation_fraction were bounded processed quantities; the instruments were synthetic benchmark instruments; and equilibrium_confidence was an environment diagnostic rather than epistemic confidence. The observations were consistent with those definitions, but that does not constitute empirical validation of them.

The research brief described a coupled weak-acid/direct-precipitation slice. The campaign supported the existence of an acid-response/precipitation association in media 0 and 1: from 0.10 to 0.40 M, mean pH_normalized decreased while mean precipitation_signal increased. It did not support a universal coupling law, because medium 2 underwent substantial acidification while precipitation remained at or near the response floor. This was correctly incorporated into K1 as: “a universal pH-to-precipitation law does not.”

The initial material list named selectable categories but expressly warned against treating their runtime behavior as predictions from real solvent properties. I did not infer hidden real chemistry from those names. Consequently, claims about dielectric constant, real aqueous solubility, named ions, or real solvent acidity were neither tested nor supported.

There was no initial scale-transfer claim. My data supplied limited positive evidence for transfer from 0.040 to 0.080 L at fixed nominal concentration, but only over that twofold range. K1 appropriately called this a concentration-controlled relationship with weak observed scale dependence rather than proven scale invariance.

I am not aware of an initial substantive claim for which contrary evidence appeared and was then knowingly left uncorrected. The important contrary observation was the medium-2 decoupling, and I did revise the explanation in response. More generally, absence of visible scale failure is only “no detected counterexample within two scales,” not proof of universal transfer.

2. Experiments that formed or changed the judgment

The four medium-0 batches formed the initial model. Batch 1, at 0.10 M and 0.040 L, gave pH_normalized 0.15747 and precipitation_signal 0.04932. Batch 2 increased concentration to 0.40 M at the same volume and moved those quantities to 0.09077 and 0.12446. This was the first strong evidence for a coupled concentration response.

Batches 3 and 4 were important because they doubled both reagent amount and volume while reproducing the two concentrations. Batch 3 approximately reproduced the low-concentration state, and batch 4 approximately reproduced the high-concentration state. In particular, batches 2 and 4 gave precipitation signals of 0.12446 and 0.11578 at the same 0.40 M concentration. Those comparisons generated the K1 judgment that concentration transferred better than absolute amount across the tested scale range.

Batches 5–8 changed the model from a single response curve to an entity-conditioned family. Medium 1 showed nearly the same qualitative concentration-induced pH decrease but materially weaker precipitation. The scale pairs again behaved similarly.

Batches 9–12 produced the largest conceptual revision. Medium 2 showed a strong concentration-associated decrease in pH_normalized, yet batches 9, 10, and 11 had final precipitation_signal exactly zero, and batch 12 gave only 0.01319. These observations directly undermined the provisional idea that acidification alone governed precipitation. They led to the K1 requirement for an additional medium-conditioned solubility, association, nucleation, activity, or measurement-response term.

The valid in-process pH-meter measurements provided qualitative cross-instrument support, but they did not principally determine the mechanism. The terminal final assays did. Batch 1 lacked a valid intermediate measurement because my unsupported replicate-count field caused validation failure; that absence should not be silently treated as a negative chemical result.

The major experimental choices were made before observing outcomes. The 2 × 2 concentration–scale matrix was driven by the stated goal of testing transfer across concentration and scale, the availability of exactly 12 complete batches, and the presence of three target selectors. Choosing 0.10 and 0.40 M, and 0.040 and 0.080 L, was a design judgment rather than something supplied by the initial dossier. It was partly an unvalidated guess that these levels would reveal useful separation without creating operational failures. The decision to allocate four batches per medium was based on symmetry and identifiability, not prior data.

The choice to avoid catalysts, heat, and programmed waiting was also a design choice. It isolated concentration, identity, and scale, but it implicitly assumed that endpoint behavior would be informative without a kinetic intervention. That assumption remained untested and is a principal limitation.

3. Most important competing mechanisms and what the experiments distinguish

The leading explanatory family remains a medium-conditioned acid/speciation equilibrium coupled to a separate precipitation branch. In compact form, concentration and medium determine an acid-response state, while precipitation additionally depends on a latent medium-specific susceptibility. This explains why all media acidified with concentration but did not share the same precipitation response.

The main competitors are:

- Thermodynamic solubility control: medium identity changes effective activities and the solubility of a precipitating form.
- Activity-coefficient control: nominal molarity changes ionic strength or other nonideal activities, so concentration is merely a proxy for the true thermodynamic coordinate.
- Hidden speciation or complexation: medium-specific soluble associations control how much material enters the precipitation pathway independently of the reported dissociation fraction.
- Kinetic or nucleation control: media differ primarily in induction time, aggregation rate, or nucleation barrier rather than equilibrium solubility.
- Matrix-dependent measurement response: medium identity changes the processed precipitation or pH proxy without an equally large change in the underlying physical state.
- Detection-floor behavior: medium 2 may have a small nonzero precipitation response that is clipped or obscured, rather than absolutely no precipitation.

The existing experiment distinguishes a universal one-dimensional pH-to-precipitation model from medium-conditioned models. Medium 2 is the counterexample: its pH changed substantially without the precipitation change seen in media 0 and 1. The scale pairs also argue against a large dependence on absolute reagent amount or volume within 0.040–0.080 L.

The experiment does not distinguish thermodynamic solubility from activity coefficients or hidden complexation, because no independent activities or species concentrations were measured. It also cannot distinguish equilibrium from delayed nucleation: there were no time courses or controlled waiting interventions. Instrument agreement supports the broad entity and concentration ordering, but the instruments report related synthetic processed proxies, so it cannot eliminate shared matrix-response effects. Exact zeros for medium 2 cannot distinguish physical absence from a response below the effective floor.

The acid_dissociation_fraction channel did not resolve these alternatives. Values were small, noisy, and frequently at zero. Fine mechanistic interpretation of that channel would exceed what the evidence supports.

4. One additional legal complete experiment

If allowed exactly one additional complete experiment, I would repeat the batch-10 composition—medium 2, 0.40 M, 0.040 L—but introduce a predeclared controlled waiting interval after reagent addition, for example 3,600 seconds at a fixed moderate stirring rate. I would obtain one legal in-process pH-meter reading before the wait, then terminate and obtain the required final assay after the wait. I would not change the condition in response to the intermediate result.

This condition is preferable to sampling an entirely new concentration because it has a direct historical comparator: batch 10 gave final pH_normalized 0.14832 and precipitation_signal 0. Its purpose would be discrimination, not optimization.

Possible outcomes would have different implications:

- If precipitation_signal rose clearly above the batch-10/floor region while pH remained similar, delayed nucleation or aggregation would become substantially more plausible. The K1 description of medium 2 as having a suppressed precipitation branch would need qualification as a timescale-dependent suppression.
- If precipitation remained near zero and pH remained close to batch 10, that would support a persistent medium-specific suppression under the longer residence time. It would weaken, but not eliminate, a simple induction-time explanation.
- If both pH and precipitation changed materially during the wait, then the original no-wait endpoints were not stationary. A coupled slow acid/speciation process would become plausible, and the original use of the word “equilibrium” would need still greater caution despite the small environment residual.
- If pH changed but precipitation remained at the floor, the evidence would favor slow acid/speciation adjustment without access to the precipitation branch.
- If the result were highly discrepant in all channels without a coherent time effect, run-to-run variability or hidden operational sensitivity would become more important, weakening the claimed transferability.

Even a null result would not prove thermodynamic equilibrium; one waiting time and one replicate cannot exclude slower processes or a measurement floor.

5. Trade-off between mechanistic identifiability and operational score

The design favored mechanistic contrast over score optimization. The scoring contract placed substantial weight on equilibrium_confidence and penalized equilibrium_residual, but I did not screen catalysts, tune waiting time, select only the apparently favorable medium, or adapt subsequent concentrations to maximize the scalar score. I instead spent all 12 complete batches on a balanced medium × concentration × scale matrix.

That choice sacrificed the possibility of finding a higher-scoring operation. Media 1 and 2 had lower environment equilibrium diagnostics than medium 0, yet they were retained because entity mapping was central to the research goal. Likewise, matched scale cells consume batches without necessarily improving the best score, but they were required to test whether relationships depended on concentration or total amount.

The in-process pH-meter measurements also served characterization rather than direct score optimization. They provided cross-instrument context, although the first attempted measurement failed validation.

Conversely, identifiability was not maximized in every dimension. I used only two concentrations and two scales, with no exact same-condition replicates, time intervention, temperature perturbation, or catalyst control. A richer concentration series would have distinguished linear, logarithmic, threshold, and saturating responses. A waiting intervention would have addressed kinetics. The finite 12-batch budget forced a choice, and I prioritized balanced entity and scale coverage.

There was no deliberate sacrifice of identifiability to optimize the score. If anything, the sacrifice ran in the other direction: potential score improvement was forgone to preserve a symmetric characterization design. The final selection of batch 4 should not be mistaken for an optimization step; it was chosen as an evidentiary anchor because it paired with batch 2 at the same concentration across scale.

6. Underused evidence and weaknesses in the blind predictions

Several acquired evidence types were not fully exploited. The final-assay artifacts included multichannel synthetic spectra and peak information, but the mechanism report relied mainly on processed estimates. Without an independently validated mapping from those peaks to chemical species, this restraint avoided overinterpretation, but potentially useful covariance or quality information remained unused.

The 11 paired pH-meter/final-assay observations were discussed qualitatively rather than fit in a measurement-error model. Such a model might have separated instrument disagreement from process variation. The two-scale pairs were summarized by mean absolute differences, but no hierarchical model was fit to estimate scale effects, entity effects, and assay noise jointly. The acid_dissociation_fraction observations were largely set aside because of noise and clipping; that was defensible, but it left uncertainty about whether their medium-2 low-concentration elevation was signal or fluctuation.

The small equilibrium_residuals and medium-dependent environment diagnostics were reported, but they are difficult to use mechanistically. In particular, a high environment diagnostic cannot establish thermodynamic equilibrium. Raw evidence about zero clipping and missingness also limits interpretation of medium 2.

The least reliable sealed predictions are Q01–Q03. Their concentration, 0.005 M, is twentyfold below the lowest experimental concentration. I used a medium-specific log-concentration continuation for pH and a weak-acid-style dilution heuristic for acid_dissociation_fraction. Neither functional form was identified by two observed concentrations. Q03 was especially fragile: its dissociation estimate of 0.055 with an 80% interval of 0–0.14 combined noisy, partly contradictory channels, and its pH estimate of 0.412 was a long extrapolation.

Q07–Q09 are also unreliable because 0.60 M lies above the observed 0.40 M maximum. The linear precipitation continuation could fail through thresholding, curvature, depletion, or saturation. Q07's precipitation interval of 0.125–0.205 and Q08's interval of 0.041–0.109 may therefore be too narrow. Q09 is vulnerable to the medium-2 floor: its point estimate of 0.011 cannot discriminate true low precipitation from clipped noise.

Even the near-range Q04–Q06 and Q10–Q12 predictions may be overconfident. Although 0.08 M is close to 0.10 M, it still lies outside the measured concentration range, and only two concentration levels were available to determine shape. The narrower intervals assigned to Q10–Q12 because 0.048 L lies within the tested volume range imply more quantitative knowledge of the scale effect than the design truly supplied. Q04–Q09 also use 0.024 L, below the smallest tested 0.040 L, so they combine concentration and scale extrapolation.

The high-concentration dissociation intervals in Q07–Q09, with upper bounds near 0.013–0.014, may be too narrow because the processed fraction was poorly identified and zero-clipped. More broadly, the 80% intervals were judgmental rather than calibrated against held-out worlds.

There is a real tension with K1's stated boundary. K1 said that its concentration slopes were descriptive interpolants and “not justified for extrapolation outside 0.10–0.40 M.” The prediction task necessarily required such extrapolation. The prediction rationales disclosed that fact, but the precise point estimates may visually imply more structural certainty than K1 warranted. The low-concentration pH extrapolation and high-concentration linear precipitation continuation are therefore best viewed as forced forecasting assumptions, not extensions established by the sealed mechanism report. The prediction set did remain consistent with K1's more defensible qualitative judgments: medium-specific curves, weak scale dependence within the observed neighborhood, and no universal pH-to-precipitation law.

7. Limitations of the sealed recommended operation

The sealed recommendation selected experiment 4: medium 0, 0.40 M, 0.080 L, with final pH_normalized 0.09221 and precipitation_signal 0.11578. Its stated rationale was that it provided a clear high-loading response and paired directly with the same-concentration small-scale experiment 2. It was explicitly an evidentiary anchor, not an optimum claim.

Experiment 4 was observed only once. Its apparent scale consistency relies on comparison with batch 2, whose precipitation signal was 0.12446, but that pair is not a set of exact technical replicates. The recommendation therefore has unquantified repeatability. It is also local to one selector, one concentration, one nominal temperature, one operation order, no catalyst, and no programmed residence time.

A proper repeatability test would preregister several independent repetitions of the exact batch-4 recipe and retain every outcome. Local robustness would require small symmetric perturbations around concentration, volume, temperature, stirring, residence time, and order of addition. A useful neighborhood might bracket 0.40 M rather than merely retest one point, allowing detection of thresholds or steep curvature.

Cross-material generalization would require applying the same perturbation design to media 1 and 2 rather than assuming the medium-0 relationship transfers. The campaign already shows that precipitation behavior does not transfer uniformly across identities. Cross-world generalization would require independent benchmark worlds or seeds with the same public contract, followed by a predeclared analysis of whether the concentration and scale relationships recur. Neither form of generalization was established here.

Finally, “sample-in highest” and “proven optimal” must be separated. Batch 4 was not selected because I had demonstrated that it maximized the scalar score, precipitation, or any scientific utility. Indeed, batch 2 had a slightly higher observed precipitation signal. No adaptive optimization or sufficiently dense local search was performed, and the research objective explicitly concerned characterization rather than medium ranking. The defensible statement is only that batch 4 was a useful observed anchor within the completed design. It is not a demonstrated optimum, and even a sample-in maximum—had one been selected—would not establish optimality outside the twelve measured conditions.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0233706 | 0.9 | 0.0625833 | 0.0953163 |
| acid_dissociation_fraction | 0.0126246 | 0.9 | 0.0400833 | 0.0551947 |
| precipitation_signal | 0.010556 | 0.916667 | 0.0411667 | 0.0448918 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0455723 |
| 0.08 | 0.00566754 |
| 0.6 | 0.011105 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.0012684 |
| 1 | 0.00179311 |
| 2 | 0.00303772 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
