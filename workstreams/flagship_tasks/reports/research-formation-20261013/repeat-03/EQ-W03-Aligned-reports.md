# EQ-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic report

1. Experimental basis

I completed 12 independent aqueous, reagent-only batches near 298.15 K. Nominal reagent loading ranged from 0.0005 to 0.040 mol, liquid volume from 0.018 to 0.072 L, and nominal total concentration C_T = n/V from 0.01389 to 1.111 mol/L. Every batch used water and received a pre-termination pH-meter measurement and a post-termination final assay. No catalyst, added component, heating, or aging interval was tested.

The final-assay results used for cross-batch interpretation were:

Batch 1: n=0.001 mol, V=0.018 L, C_T=0.05556 M; pH_normalized=0.27957, dissociation fraction alpha=0.07617, precipitation_signal=0.15993.
Batch 2: n=0.001 mol, V=0.054 L, C_T=0.01852 M; pH_normalized=0.28108, alpha=0.08080, precipitation_signal=0.15002.
Batch 3: n=0.002 mol, V=0.036 L, C_T=0.05556 M; pH_normalized=0.27700, alpha=0.07612, precipitation_signal=0.16001.
Batch 4: n=0.004 mol, V=0.072 L, C_T=0.05556 M; pH_normalized=0.28017, alpha=0.06733, precipitation_signal=0.15926.
Batch 5: n=0.0005 mol, V=0.036 L, C_T=0.01389 M; pH_normalized=0.28276, alpha=0.07282, precipitation_signal=0.14833.
Batch 6: n=0.001 mol, V=0.036 L, C_T=0.02778 M; pH_normalized=0.28318, alpha=0.06734, precipitation_signal=0.15278.
Batch 7: n=0.004 mol, V=0.036 L, C_T=0.11111 M; pH_normalized=0.27861, alpha=0.06468, precipitation_signal=0.14894.
Batch 8: n=0.008 mol, V=0.036 L, C_T=0.22222 M; pH_normalized=0.27703, alpha=0.06485, precipitation_signal=0.15796.
Batch 9: n=0.016 mol, V=0.036 L, C_T=0.44444 M; pH_normalized=0.27400, alpha=0.07451, precipitation_signal=0.14684.
Batch 10: n=0.024 mol, V=0.036 L, C_T=0.66667 M; pH_normalized=0.27821, alpha=0.07861, precipitation_signal=0.15658.
Batch 11: n=0.040 mol, V=0.036 L, C_T=1.11111 M; pH_normalized=0.27772, alpha=0.07157, precipitation_signal=0.15538.
Batch 12: an exact nominal repeat of Batch 8; pH_normalized=0.28315, alpha=0.07608, precipitation_signal=0.15982.

2. Best effective description

The most strongly supported compact description is a bounded, effective monoprotic-acid relationship rather than a fully identified microscopic mechanism. Let alpha denote the reported acid_dissociation_fraction and let pH = 14*pH_normalized. An effective Henderson-Hasselbalch relation is

pH = pKa_eff + log10(alpha/(1-alpha)),

or equivalently

alpha = 1/[1 + 10^(pKa_eff-pH)].

Applying the first equation to every final assay gave a mean pKa_eff of 5.019, with an observed batchwise range of 4.930 to 5.106. This agrees broadly with the supplied archival 80% interval, 4.969 to 5.069. Thus pH and the reported dissociation fraction behave as coupled observables compatible with an effective acidity constant near 5.02.

This is an effective relationship, not proof that ideal concentrations equal activities or that only freely dissolved HA, H+, and A− exist. The same channel-level relationship could arise from a buffered medium, activity corrections, ion pairing, solid-liquid coupling, or a benchmark observation model constructed around an effective pKa.

3. Dilution, concentration, and total amount

The clearest prospective test was the supplied local dilution contrast. Batches 1 and 2 held total reagent at 0.001 mol while increasing volume from 0.018 to 0.054 L. The final observed changes were

Delta pH_normalized = +0.001506,
Delta alpha = +0.004634.

The archival expectations were +0.001826 and +0.004044, respectively. The direction and magnitude therefore reproduced well. In ordinary pH units, the observed normalized-pH change corresponds to about +0.0211 pH unit. Because this is only one paired comparison and is comparable to the measurement scale, it supports a small local dilution response but not a highly precise universal coefficient.

Batches 1, 3, and 4 tested scale at the same nominal concentration, 0.05556 M, using proportional changes in both amount and volume. Their precipitation signals were essentially identical: 0.15993, 0.16001, and 0.15926. Their pH_normalized values, 0.27957, 0.27700, and 0.28017, also lacked a systematic scale order. Alpha agreed almost exactly between Batches 1 and 3, 0.07617 versus 0.07612, but was lower in Batch 4 at 0.06733. Since the discordance appeared in only one channel and one batch, it does not establish a separate total-amount effect. Overall, concentration is a more economical organizing variable than total amount, while a modest volume or scale effect remains unresolved.

Across all final assays, descriptive least-squares fits against ln(C_T) were

pH_normalized approximately 0.27669 - 0.001202 ln(C_T/M),
alpha approximately 0.07247 - 0.000047 ln(C_T/M),
precipitation_signal approximately 0.15603 + 0.000613 ln(C_T/M).

The pH coefficient corresponds to only about -0.0387 ordinary pH unit per tenfold concentration increase. The alpha and precipitation slopes are practically flat. These fits summarize this dataset; they should not be treated as calibrated mechanistic laws.

In particular, a simple ideal weak-acid mass balance with fixed Ka would normally produce a much stronger concentration dependence of both pH and fractional dissociation. The nearly constant observed alpha and weak pH trend therefore argue against using an unmodified ideal-dilute weak-acid equation over the entire 0.01389-1.111 M range. Background buffering, nonideal activities, an effective rather than literal alpha channel, or other hidden bounded-world couplings are reasonable explanations.

4. Precipitation behavior

No resolved precipitation transition was found. Final precipitation_signal remained between 0.14684 and 0.16001 over an approximately 80-fold concentration range. The equal-concentration scale series was nearly invariant, and the fitted concentration slope was negligible. The exact nominal repeat, Batches 8 and 12, differed by only 0.00187 in precipitation_signal.

The supported statement is therefore narrow: within these water-only, reagent-only, near-ambient conditions, the public precipitation proxy is approximately a baseline near 0.15 and shows no resolved dependence on concentration, total amount, or volume. This does not establish absence of a solid phase. The proxy is bounded and normalized, not a measured precipitate mass. A threshold outside the tested range, an already saturated plateau, a weak response hidden by noise, or a proxy dominated by a background contribution are all observationally equivalent here.

5. How the interpretation changed during the campaign

Batches 1 and 2 supported the archival dilution relationship and initially favored concentration as the main control variable. Batches 3 and 4 then tested whether changing total scale at fixed concentration mattered. Their pH and precipitation results strengthened concentration-based organization, although Batch 4's lower alpha prevented a strong claim of perfect scale invariance.

Batches 5-11 supplied the broad fixed-volume concentration series. They did not reveal the expected monotonic alpha response or a precipitation threshold. This caused me to reject a strong ideal-dilute interpretation and replace it with the weaker effective-pKa account.

Batches 8 and 12 were nominal replicates. Their final differences were 0.00613 in pH_normalized, 0.01123 in alpha, and 0.00187 in precipitation_signal. The pH and alpha differences are large relative to the subtle fitted concentration trends. Consequently, the regressions are descriptive only, whereas the near-constant effective-pKa combination and the absence of a large precipitation transition are more defensible.

Pre-termination pH-meter readings sometimes differed appreciably from final-assay readings. For example, Batch 5 gave alpha=0.10411 by pH meter but 0.07282 by final assay; Batch 10 gave precipitation_signal=0.19471 before termination but 0.15658 in the final assay. Instrument identity and lifecycle stage were confounded, so these differences cannot be attributed specifically to termination or chemistry. I used the consistently positioned final assays for cross-batch comparisons.

6. Equilibrium diagnostics and uncertainty

Final equilibrium_residual values ranged from zero to about 0.0112, with many exactly zero. This indicates no large publicly reported residual in the assayed states, but it does not independently identify the equilibrium law. The reported equilibrium_confidence ranged roughly from 0.364 to 0.544. As specified, this is an environment diagnostic and is not my scientific confidence; I do not use it as evidence that one mechanism is more probable.

The design contains only one exact replicate and mostly one final assay per condition. Final-assay nominal noise scales were 0.002 for pH_normalized and 0.006 for both alpha and precipitation_signal, while the replicate suggests additional run-level variability may matter for pH and alpha. Exact confidence intervals for fitted coefficients are therefore not justified from this campaign.

7. Scope and unresolved alternatives

The report applies only to the tested bounded slice: water, anonymous reagent, near-ambient temperature, no catalyst or added component, nominal C_T from 0.01389 to 1.111 M, amounts from 0.0005 to 0.040 mol, and volumes from 0.018 to 0.072 L. It does not support extrapolation to other solvents, temperatures, electrolyte profiles, catalysts, long equilibration times, or concentrations beyond that interval.

The data do not identify microscopic species, activity coefficients, buffer capacity, nucleation kinetics, solid composition, or actual precipitated mass. At least three explanations remain reasonable:

(1) a monoprotic acid with pKa near 5.02 whose apparent concentration response is flattened by nonideal activities or background buffering;
(2) a more complex coupled speciation/precipitation system whose observable channels collapse to the same effective pKa relation;
(3) an environment-level observation mapping that directly couples pH and alpha around a latent effective acidity parameter, without those channels uniquely representing free-solution species.

Likewise, the flat precipitation proxy may mean no threshold was crossed, a plateau was already present, or the proxy is weakly sensitive in this formulation. The present observations cannot distinguish these possibilities.

My final model is therefore intentionally modest: total concentration C_T=n/V provides the primary loading coordinate; dilution causes a small increase in pH and reported dissociation locally; pH and alpha are coupled through an effective pKa of approximately 5.02; total amount has no clearly resolved independent effect at fixed concentration; and the precipitation proxy remains approximately constant near 0.15 throughout the tested domain. Batch 2 is the selected evidentiary anchor because it is the exact diluted endpoint of the strongest prospective local test, interpreted jointly with Batch 1.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | acid_dissociation_fraction | 0.0776 | 0.058 | 0.098 |
| Q01 | pH_normalized | 0.2817 | 0.275 | 0.289 |
| Q01 | precipitation_signal | 0.1535 | 0.141 | 0.166 |
| Q02 | acid_dissociation_fraction | 0.0776 | 0.06 | 0.096 |
| Q02 | pH_normalized | 0.2817 | 0.276 | 0.288 |
| Q02 | precipitation_signal | 0.1535 | 0.142 | 0.165 |
| Q03 | acid_dissociation_fraction | 0.0918 | 0.045 | 0.155 |
| Q03 | pH_normalized | 0.2874 | 0.27 | 0.31 |
| Q03 | precipitation_signal | 0.1506 | 0.125 | 0.176 |
| Q04 | acid_dissociation_fraction | 0.084 | 0.048 | 0.132 |
| Q04 | pH_normalized | 0.2844 | 0.271 | 0.3 |
| Q04 | precipitation_signal | 0.1521 | 0.13 | 0.174 |
| Q05 | acid_dissociation_fraction | 0.073 | 0.055 | 0.093 |
| Q05 | pH_normalized | 0.2797 | 0.273 | 0.287 |
| Q05 | precipitation_signal | 0.1545 | 0.143 | 0.166 |
| Q06 | acid_dissociation_fraction | 0.073 | 0.055 | 0.093 |
| Q06 | pH_normalized | 0.2797 | 0.273 | 0.287 |
| Q06 | precipitation_signal | 0.1545 | 0.143 | 0.166 |
| Q07 | acid_dissociation_fraction | 0.073 | 0.05 | 0.1 |
| Q07 | pH_normalized | 0.2797 | 0.271 | 0.289 |
| Q07 | precipitation_signal | 0.1545 | 0.138 | 0.171 |
| Q08 | acid_dissociation_fraction | 0.0995 | 0.035 | 0.2 |
| Q08 | pH_normalized | 0.2902 | 0.265 | 0.325 |
| Q08 | precipitation_signal | 0.1491 | 0.115 | 0.18 |
| Q09 | acid_dissociation_fraction | 0.0911 | 0.038 | 0.175 |
| Q09 | pH_normalized | 0.2871 | 0.267 | 0.315 |
| Q09 | precipitation_signal | 0.1507 | 0.12 | 0.18 |
| Q10 | acid_dissociation_fraction | 0.0623 | 0.025 | 0.11 |
| Q10 | pH_normalized | 0.2744 | 0.255 | 0.294 |
| Q10 | precipitation_signal | 0.1572 | 0.125 | 0.19 |
| Q11 | acid_dissociation_fraction | 0.0683 | 0.051 | 0.088 |
| Q11 | pH_normalized | 0.2774 | 0.271 | 0.284 |
| Q11 | precipitation_signal | 0.1556 | 0.144 | 0.167 |
| Q12 | acid_dissociation_fraction | 0.0718 | 0.054 | 0.091 |
| Q12 | pH_normalized | 0.2791 | 0.273 | 0.286 |
| Q12 | precipitation_signal | 0.1548 | 0.143 | 0.166 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions use nominal total concentration C_T=n/V as the primary coordinate. Within the studied domain, the descriptive final-assay relationships were pH_normalized approximately 0.27669-0.001202 ln(C_T/M), with pH and dissociation coupled through pKa_eff approximately 5.019, and precipitation_signal approximately 0.15603+0.000613 ln(C_T/M). Equal-concentration batches supported approximate scale invariance, while Q05-Q07 are therefore treated as endpoint-equivalent unless transient concentration creates unobserved hysteresis. Intervals combine assay noise, the substantial Batch 8 versus Batch 12 repeat dispersion, uncertainty in effective pKa, and additional widening for trace-loading, extreme-concentration, small-volume, or dosing-history extrapolation. The precipitation estimates remain close to the observed baseline because no threshold was resolved during the campaign.

**Q01**: The nominal concentration is 0.015 M, close to the lowest studied concentration. The estimate follows the observed weak dilution response and effective-pKa relation. The interval is moderately widened because the total amount is slightly below the studied loading range.

**Q02**: This has the same 0.015 M endpoint as Q01. The tested equal-concentration scale series showed little reproducible amount or volume dependence, so the point prediction is identical. Its loading and volume are closer to the experimental domain, permitting a slightly narrower interval.

**Q03**: The concentration is approximately 0.000133 M, far below the observed range. Log-concentration extrapolation predicts modestly higher pH and dissociation, while precipitation remains near its observed baseline. The wide interval admits failure of that extrapolation and an unresolved trace-loading or volume effect.

**Q04**: The nominal concentration is 0.00167 M, still below the measured domain but substantially higher than Q03. The model therefore predicts slightly lower pH and dissociation than Q03. Uncertainty remains large because both the trace amount and 0.006 L volume are out of the studied range.

**Q05**: The final state is 0.002 mol in 0.024 L, or 0.0833 M, inside the studied domain. With no waiting or irreversible operation between additions, the primary prediction is endpoint-controlled behavior. The interval includes observed assay and batch-to-batch variability.

**Q06**: Q06 has the same final amount, volume, solvent, and nominal concentration as Q05. The campaign did not identify path dependence, so accumulated solvent-first dosing is predicted to be observationally equivalent to interleaved dosing.

**Q07**: The final endpoint again matches Q05 and Q06. Identical point estimates express the equilibrium endpoint hypothesis, but intervals are wider because reagent is temporarily more concentrated before final dilution and the campaign did not directly test whether such dosing history can seed persistent precipitation or other hysteresis.

**Q08**: At approximately 0.0000133 M, this is the most extreme dilute extrapolation. The weak empirical log-concentration trend and effective pKa imply higher pH and dissociation, but neither the trace-loading limit nor approach toward reagent-free water was observed. The interval is consequently much wider and also allows a changed precipitation baseline.

**Q09**: The concentration, approximately 0.000167 M, is close to Q03 but remains far below the observed domain. The point estimate follows the same effective-acidity extrapolation. Wide limits cover uncertain trace-loading behavior and the untested small liquid volume.

**Q10**: The nominal concentration is 6.67 M, about six times the highest studied concentration and at an untested small volume. Extrapolation predicts slightly lower pH and dissociation but little precipitation change. The broad interval reflects possible nonideality, saturation, or a precipitation transition beyond the campaign range.

**Q11**: The concentration is 0.533 M, well inside the measured concentration series, although the amount-volume combination is new. Fixed-concentration scale tests found no clear independent scale effect, so concentration-based interpolation is used with ordinary predictive uncertainty.

**Q12**: The 0.136 M concentration and both amount and volume lie within the experimental domain. This is an interpolation between studied fixed-volume conditions, so the effective-pKa and nearly flat precipitation relationships are applied with intervals dominated by observed replicate and assay variability.

## K2

1. Assessment of the initial information

The initial packet contained two substantive scientific claims, both explicitly qualified as local rather than universal:

- An effective pKa 80% interval of 4.9694–5.0694.
- At 0.001 mol and approximately 298.15 K, dilution from 0.018 to 0.054 L should increase acid_dissociation_fraction by 0.004044 and pH_normalized by 0.001826.

Both claims received support. Batches 1 and 2 reproduced the specified dilution contrast: the observed changes were +0.004634 in dissociation fraction and +0.001506 in pH_normalized. Across the 12 final assays, the derived effective pKa had a mean of 5.019, inside the archival interval, although individual derived values ranged from 4.930 to 5.106.

That support should not be overstated. The dilution claim was tested by only one independent pair, and its pH change was comparable to measurement and run-to-run variability. The effective-pKa agreement is stronger as a channel-level consistency result, but pH and dissociation may be generated by coupled observables rather than independent measurements of microscopic species. Consequently, the campaign supported the initial claims as useful local effective relationships, not as uniquely identified chemical laws.

No direct contradiction of the two numerical archival claims appeared. However, there was evidence against extending them into a conventional ideal-dilute weak-acid mechanism: the broad concentration series did not show the strong monotonic change in fractional dissociation expected from a simple mass-action model. K1 did revise the interpretation accordingly, replacing a literal ideal model with an effective-pKa description. This is different from merely saying that no counterevidence was found.

The initial material information also stated that no task-specific property dossier was available and that anonymous benchmark identities should not be mapped onto real substances. Nothing in the campaign contradicted that limitation. Claims about catalyst, electrolyte, solvent, temperature, or material identity remained untested because I used only water, reagent, and near-ambient conditions.

2. Experiments that formed or changed the interpretation

Batches 1 and 2 were the most directly prior-driven experiments. Their conditions were chosen specifically to reproduce the archival dilution contrast. Their agreement with the supplied changes established the initial local model as a reasonable starting point.

Batches 3 and 4 were genuine discriminating experiments rather than simple replications. Together with Batch 1, they held nominal concentration at 0.05556 M while scaling amount and volume proportionally. Similar pH and precipitation results across these batches supported concentration as a more economical state coordinate than total amount alone. Batch 4 nevertheless returned alpha=0.06733, below the approximately 0.0761 values in Batches 1 and 3. That result prevented a strong claim of exact scale invariance.

Batches 5–11 changed the interpretation most substantially. They formed a fixed-volume concentration series from 0.01389 to 1.111 M. The absence of a strong monotonic dissociation trend weakened a literal ideal weak-acid model. The precipitation proxy also remained in a narrow band, so my initial conjecture that a threshold might become visible was not supported.

Batches 8 and 12 were the only exact nominal repeat. Their differences—0.00613 in pH_normalized, 0.01123 in dissociation fraction, and 0.00187 in precipitation_signal—materially changed how I treated the regressions. In K1 I consequently described the concentration fits as descriptive rather than calibrated laws. This repeat was especially important because the pH difference exceeded much of the trend attributed to concentration.

Several design choices were not strongly evidence-based. The expectation of a precipitation threshold was an unverified conjecture. Selecting 0.036 L for most of the concentration series was a convenient design decision, not a mechanistic conclusion. Assuming that immediate final assays represented equilibrium endpoints was partly based on the task framing and small reported residuals, not on a time-course experiment. Using water exclusively followed the aqueous research target and reduced confounding, but it left solvent dependence entirely unidentified.

3. Principal competing explanations

The main explanations still compatible with the evidence are:

(a) Effective monoprotic equilibrium with nonideal or buffered behavior. A latent acidity parameter near pKa_eff=5.02 couples pH and dissociation, while background buffering or activities flatten their concentration dependence.

(b) More complex speciation. Ion pairing, multiple effective reservoirs, or solid–liquid coupling could yield the same observed pH–alpha relation without alpha representing the free fraction of a single HA/A− pair.

(c) Observation-model coupling. The public pH and dissociation channels may be constructed from a shared latent state. Their agreement with a Henderson–Hasselbalch transformation would then characterize the measurement mapping, not uniquely establish microscopic chemistry.

(d) A precipitation response outside the sampled window. The nearly constant proxy may represent no precipitation, an existing plateau, a background offset, or a threshold beyond the tested conditions.

The equal-concentration scale comparison distinguishes a strong total-amount-only model from a concentration-organized model: the former is poorly supported. The broad series also distinguishes a strong monotonic precipitation response within 0.01389–1.111 M from a nearly flat response there.

The experiments cannot distinguish buffering from nonideal activity, observation coupling from true chemical coupling, or absence of precipitation from a plateau. They also cannot establish path independence because no dosing-order comparison was performed during the campaign. Pre-termination pH-meter and post-termination final-assay results were confounded by both instrument and lifecycle stage, so they do not isolate a termination effect.

4. One additional experiment

If exactly one additional complete experiment were allowed, I would use 0.075 L water with 0.000001 mol reagent, measure once with the pH meter before termination, terminate, and then obtain the final assay. This is a nominal concentration of about 1.33×10^-5 M, far below the campaign range.

This experiment would probe the most important unresolved asymptote:

- If pH_normalized remained near 0.29 and alpha near 0.10, it would support the compressed, buffered, or latent-state interpretation used in the blind prediction for Q08.
- If pH moved substantially toward neutral water and alpha rose strongly, it would show that the campaign had sampled only a concentration-insensitive middle regime and that log-linear extrapolation was inappropriate.
- If precipitation_signal remained near 0.15, that would support a background or plateau interpretation. A marked decline would instead suggest that the prior flat band concealed a loading-dependent contribution.
- Agreement between the pH meter and final assay would strengthen the endpoint interpretation. A large discrepancy would emphasize instrument mapping or lifecycle effects, although one experiment would still not fully separate them.

I would prefer this boundary experiment over another interior replicate because the existing alternatives make sharply different predictions at trace loading. I would not actually execute it under the present instruction.

5. Tradeoff between identifiability and operational score

The campaign was designed primarily for mechanistic characterization, not scalar-score optimization. I spent all 12 complete batches on dilution, concentration–volume decoupling, a broad concentration series, and one repeat. I did not search catalysts, added components, solvent identity, temperature, or process conditions for a higher score.

This sacrificed possible score improvements for identifiability. For example, Batches 3 and 4 were chosen to separate concentration from total scale, even though they were not expected to improve equilibrium_confidence. The extreme concentration series likewise included conditions with relatively low diagnostic scores. Batch 10 had final equilibrium_confidence=0.3636, yet it remained scientifically useful as part of the loading series.

Conversely, there was little evidence that I sacrificed identifiability in order to optimize. After Batches 8 and 12 showed comparatively high equilibrium_confidence, I did not repeatedly exploit that condition. The task explicitly stated that equilibrium_confidence was an environment diagnostic rather than my confidence or the research objective, and I treated it that way.

There was still a design opportunity cost: using a pH-meter measurement in every batch consumed all intermediate-measurement capacity but did not cleanly isolate instrument bias or time dependence. A more identifiable design might have used those measurements at multiple stages of fewer strategically selected conditions, if the campaign contract had allowed reallocating complete batches or repeated measures differently.

6. Underused evidence and weaknesses in the blind predictions

The raw final-assay artifacts and detailed signal packets were not exploited. My interpretation relied mainly on processed estimates. If raw channel covariance, calibration behavior, or missingness information contained usable structure, I did not extract it.

The paired pH-meter/final-assay observations were also underused. I cited striking discrepancies, such as Batch 5 alpha=0.10411 by pH meter versus 0.07282 by final assay, but the design could not determine whether these arose from instrument bias, sampling variability, termination, or latent state changes. A formal paired comparison might have quantified an average discrepancy, but it would still have remained causally ambiguous.

I did not estimate formal uncertainty for the regression coefficients. The K1 statements that the fits were merely descriptive and that exact confidence intervals were unjustified were appropriate, but the blind predictions nevertheless placed fairly structured intervals around those extrapolations.

The least reliable blind predictions are Q08 and Q10. Q08 extrapolates to approximately 1.33×10^-5 M, more than three orders of magnitude below parts of the measured range. Its pH interval of 0.265–0.325 may be too narrow because it excludes a substantial approach toward neutral water. Q10 extrapolates to 6.67 M at only 0.006 L. Its precipitation interval of 0.125–0.190 is especially vulnerable: K1 explicitly allowed a precipitation threshold outside the tested domain, yet this interval does not accommodate a large threshold response. That is a genuine inconsistency between the stated mechanistic uncertainty and the quantitative interval.

Q03, Q04, and Q09 are also weak because their reagent amounts and concentrations were far below the source domain. Q01 is only slightly outside the tested amount range, so it is less problematic. Q11 is an interpolation in concentration but uses a volume slightly beyond the campaign maximum.

Q05–Q07 assumed approximate endpoint equivalence even though dosing-order dependence was never experimentally tested. I widened Q07 because it temporarily creates the highest intermediate concentration, but Q05 and Q06 may also have intervals that are too narrow if addition order affects nucleation or persistent aggregation. Treating their point estimates as identical was a reasonable equilibrium hypothesis, not an experimentally demonstrated fact.

Thus, the prediction rationales acknowledged extrapolation, but some intervals did not fully honor K1's stated scope limits and competing explanations. In particular, the extreme precipitation intervals should have been much wider if they were intended to represent mechanism uncertainty rather than only local assay variability.

7. Limitations of the sealed recommendation

The sealed recommendation selected Batch 2: 0.001 mol reagent in 0.054 L water. It was selected because it was the exact diluted endpoint of the supplied local contrast and, together with Batch 1, anchored the strongest prospective test. It was not selected because it had the highest scalar score.

Batch 2 was measured only once. Its final equilibrium_confidence was approximately 0.392, below the values near 0.54 observed in Batches 8 and 12. Therefore it is neither the sample-best score condition nor a demonstrated optimum. It is an evidentiary anchor.

Repeatability would require independent replications of both Batch 2 and its Batch 1 comparator. Local robustness would require nearby volumes and loadings—for example, small perturbations around 0.001 mol and 0.054 L—to determine whether the dilution response is smooth and whether its estimated slope is stable.

Robustness to scale would require repeating the same concentration at additional amount–volume pairs. Robustness to dosing history would require comparing single-step, solvent-first, reagent-first, and interleaved preparations at the same final state. Robustness across materials would require testing other permitted solvents or added-component formulations rather than assuming that the water-only effective pKa transfers. Cross-world generalization would require an independent campaign or environment realization using a preregistered model and prediction intervals.

Accordingly, Batch 2 should be described as a locally informative, source-stage recommendation. Neither K1 nor the campaign demonstrated that it is operationally optimal, globally robust, transferable across materials, or optimal in another world.

## EQS

### dissociation precipitation

**assessment**: continuous

**competing explanation**: The nearly flat proxy could represent a background or already-saturated plateau rather than a genuinely continuous mechanistic coupling; alternatively, a precipitation threshold may lie outside the tested range. Because precipitation_signal is normalized rather than precipitated mass, these explanations cannot be separated here.

**supported range**: Water-only, reagent-only, near-ambient batches with 0.0005-0.040 mol reagent, 0.018-0.072 L liquid volume, and nominal total concentration 0.01389-1.111 mol/L. Within this range, final precipitation_signal remained approximately 0.147-0.160 while dissociation_fraction was approximately 0.065-0.081, with no resolved abrupt transition.

### effective pka

**estimate**: 5.02

**identifiable**: True

**lower80**: 4.97

**rationale**: Using pKa_eff = 14*pH_normalized - log10(alpha/(1-alpha)) on the 12 final assays gave a mean of 5.019 and an observed range of 4.930-5.106. The estimate is also consistent with the independently supplied local interval of 4.969-5.069 and with the Batch 1-to-2 dilution response. It identifies an effective channel-level acidity parameter, not a unique microscopic thermodynamic pKa; activity effects, buffering, speciation, and shared observation-model coupling remain confounded.

**upper80**: 5.07

### path dependence

**assessment**: indeterminate

**rationale**: The source campaign did not compare staged-addition paths at an identical final state: each batch used a single solvent addition followed by a single reagent addition. Batches 1, 3, and 4 tested different amount-volume scales at the same nominal concentration and showed similar pH and precipitation, supporting final-state organization under that common preparation path. Batches 8 and 12 were exact nominal repeats and quantified run variability. Neither comparison tests interleaving, reagent-first dilution, or nucleation memory, so reproducible staged-path dependence cannot be established or excluded.
