# EQ-Sol — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic report

1. Scope and experimental basis

I completed 12 independent water-only batches near ambient temperature and pressure. Nominal reagent loading n ranged from 0.005 to 0.040 mol, liquid volume V from 0.020 to 0.080 L, and nominal analytical concentration C = n/V from 0.0625 to 2.0 mol/L. Each batch received a pre-terminal pH-meter measurement and a post-terminal final assay. Batch 12 was deliberately diluted after its pH-meter measurement, from approximately 0.50 to 0.25 mol/L. The 30-microliter pH-meter sample loss was negligible relative to the 20–80 mL batch volumes, although it makes the final concentration in batch 12 very slightly greater than 0.250 mol/L.

The final assay is the primary quantitative basis because its declared noise is lower than that of the pH meter. Its noise scales are 0.002 for normalized pH, 0.006 for dissociation fraction, 0.006 for precipitation signal, 0.004 for equilibrium residual, and 0.006 for equilibrium confidence. Equilibrium confidence is treated only as an environment diagnostic, not as my scientific confidence.

2. Actual final-assay observations

The following table gives nominal final C and the five relevant final-assay outputs:

Batch | C (mol/L) | pH_normalized | dissociation fraction | precipitation proxy | residual | environment equilibrium confidence
1 | 0.0625 | 0.25529 | 0.06336 | 0.15942 | 0.00000 | 0.43266
2 | 0.125 | 0.25423 | 0.07356 | 0.16183 | 0.00055 | 0.46772
3 | 0.250 | 0.25015 | 0.07915 | 0.15777 | 0.00000 | 0.57625
4 | 0.500 | 0.25339 | 0.06917 | 0.15902 | 0.00000 | 0.36140
5 | 0.125 | 0.25183 | 0.07798 | 0.15908 | 0.00425 | 0.48465
6 | 0.250 | 0.25213 | 0.06942 | 0.14433 | 0.00000 | 0.56814
7 | 0.500 | 0.25522 | 0.06910 | 0.16131 | 0.00770 | 0.36222
8 | 1.000 | 0.25234 | 0.06957 | 0.15399 | 0.00000 | 0.38158
9 | 0.500 | 0.25594 | 0.06664 | 0.15095 | 0.00071 | 0.36888
10 | 1.000 | 0.25237 | 0.06700 | 0.15658 | 0.00195 | 0.37511
11 | 2.000 | 0.25489 | 0.07873 | 0.15150 | 0.00000 | 0.37472
12 | approximately 0.250 after dilution | 0.25289 | 0.06488 | 0.15118 | 0.00195 | 0.57422

Across all final assays, the means were approximately:

pH_normalized = 0.2534, corresponding to pH = 3.55;
acid dissociation fraction = 0.0707;
precipitation_signal = 0.1556.

The observed final-assay ranges were approximately pH 3.50–3.58, dissociation fraction 0.0634–0.0791, and precipitation proxy 0.1443–0.1618. Their RMS scatter around constant values was about 0.00167 normalized-pH units, 0.00518 dissociation-fraction units, and 0.00505 precipitation-signal units. These are comparable to the declared final-assay noise scales.

3. Effective relationship supported by the observations

Within the tested domain, the most economical effective model is

C = n/V,

pH_normalized = mu_p + epsilon_p,
alpha = mu_alpha + epsilon_alpha,
P = mu_P + epsilon_P,

where alpha is the reported acid-dissociation fraction, P is the bounded precipitation proxy, and the central values are approximately

mu_p = 0.2534,
mu_alpha = 0.0707,
mu_P = 0.1556.

A descriptive linear fit against ln(C), not asserted as a physical law, gave

pH_normalized approximately 0.25350 + 0.000105 ln(C),
alpha approximately 0.07148 + 0.000733 ln(C),
P approximately 0.15386 - 0.00165 ln(C),

with C expressed numerically in mol/L. Across a 32-fold concentration range, these fitted slopes are negligible compared with the observed scatter and declared measurement noise. Thus the data do not resolve a loading dependence in pH, dissociation fraction, or precipitation proxy.

Matched-concentration comparisons show that amount and volume also did not have separately detectable effects. Batches 2 and 5 both had C = 0.125 mol/L despite different n and V; batches 3 and 6 had C = 0.25 mol/L; batches 4, 7, and 9 had C = 0.50 mol/L. Batch 12 reached approximately 0.25 mol/L by a different dilution history. The higher-precision final outputs within these groups showed no reproducible amount-only or volume-only separation.

Consequently, saying that the response is a function of concentration alone is formally compatible with the observations, but it is not a uniquely established mechanistic law: over this range that function is nearly constant. Constant response, concentration-only response on a broad plateau, and background-dominated response are observationally equivalent here.

4. A distinct concentration coupling in the environment diagnostic

Unlike the chemical-response channels, equilibrium_confidence showed a reproducible, nonmonotonic association with C. Replicate concentration groups were especially informative:

C = 0.125 mol/L: 0.4677 and 0.4847;
C = 0.250 mol/L: 0.5763, 0.5681, and 0.5742;
C = 0.500 mol/L: 0.3614, 0.3622, and 0.3689;
C = 1.000 mol/L: 0.3816 and 0.3751.

Thus an empirical diagnostic function g(C) has a local maximum near 0.25 mol/L, approximately 0.573, followed by a sharp decrease to approximately 0.364 at 0.50 mol/L. At 0.125 mol/L it is approximately 0.476; at 0.0625 mol/L it was 0.433; at 1–2 mol/L it was approximately 0.375–0.378. The within-group agreement is close relative to the declared 0.006 noise scale, so this concentration association is much better supported than any slope in the chemical-response channels.

I would represent this diagnostic by an empirical lookup or flexible g(log C), rather than impose a symmetric bell-shaped law: the decrease between 0.25 and 0.50 mol/L is much sharper than the low-concentration side. Because equilibrium_confidence is explicitly an environment diagnostic, this feature should not be interpreted as a thermodynamic equilibrium constant, fraction equilibrated, or epistemic probability.

The equilibrium residual remained close to its lower bound: six final values were exactly zero, and the largest was 0.00770 in batch 7. There was no evident monotonic residual trend with concentration. Zero values may include lower-bound clipping, so they should be read as “unresolved from zero at this scale,” not exact mathematical equality.

5. How the experiments changed the interpretation

My initial weak-acid expectation was that increasing analytical concentration would lower pH and reduce the dissociated fraction, while dilution would reverse those changes. I also allowed for a precipitation onset at high concentration.

Batches 1–4 supplied the first concentration scan, from 0.0625 to 0.50 mol/L. They did not show the expected monotonic pH or dissociation response. Batches 5–7 then created matched-concentration conditions using different amounts and volumes. Their final assays showed that the earlier numerical fluctuations were not reproducible amount or volume effects. Batches 8–11 extended the range to 1 and 2 mol/L; they still produced essentially the same pH, dissociation fraction, and precipitation proxy, ruling out a simple missed onset over that extended range.

Batch 12 was measured by the pH meter near 0.50 mol/L, diluted to approximately 0.25 mol/L, and then measured by final assay. Before dilution, the pH-meter outputs were pH_normalized 0.24944, dissociation fraction 0.05049, precipitation proxy 0.14644, residual 0, and equilibrium confidence 0.38070. After dilution, the final assay gave 0.25289, 0.06488, 0.15118, 0.00195, and 0.57422, respectively. The confidence change agrees closely with the independent 0.50 and 0.25 mol/L cohorts and therefore supports the concentration coupling of that diagnostic. The other before/after differences cannot establish chemical reversibility because the two states were measured using instruments with different noise profiles; their magnitudes are compatible with cross-instrument scatter.

6. Relation to a conventional weak-acid mechanism

For an ideal monoprotic weak acid,

HA <=> H+ + A-,
Ka = [H+][A-]/[HA],
alpha = Ka/(Ka + [H+]),

and, without a dominant external buffer or other charged species, mass balance and electroneutrality normally make pH and alpha depend on analytical acid concentration.

That simple closed acid-only model is not supported. The observed mean pH of about 3.55 corresponds to [H+] of roughly 2.8 x 10^-4 mol/L, while C times the reported alpha would vary enormously across the tested loading range. Those quantities cannot be identified with each other under the simplest acid-only charge balance. Therefore at least one assumption of that textbook model is inapplicable to the public channels.

A reasonable effective process description is:

1. Reagent and water establish nominal loading C = n/V.
2. A hidden background or benchmark formulation fixes the acid/base observable state near pH 3.55 and alpha near 0.071 over the tested C range.
3. The precipitation proxy remains on a broad baseline or plateau near 0.156, with no resolved loading threshold.
4. A separate environment diagnostic evaluates C, favoring a neighborhood around 0.25 mol/L and penalizing conditions at or above about 0.50 mol/L.
5. Instrument noise and lower-bound clipping generate most of the observed batch-to-batch fluctuations in the chemical channels and residual.

This is an identifiable input-output description, not a claim that the hidden implementation literally contains a buffer or a particular acid species.

7. Competing explanations that remain equivalent

Several mechanisms fit the observations:

• Background-buffer dominance: an implicit acid/base reservoir fixes [H+] and the reported dissociation state, making added analytical loading nearly irrelevant.

• Inactive-role explanation: the anonymous limiting reagent varied in these experiments may not be the chemically active acid-loading variable. A fixed, unvaried component could control the acid and precipitation channels.

• Broad response plateau: the varied reagent could be chemically active, but all tested conditions may lie on a flat region between transitions.

• Proxy-baseline explanation: precipitation_signal may primarily report a bounded background response rather than precipitated mass. A nearly constant nonzero proxy does not prove that a fixed amount of solid was present.

• Hidden compensation: concentration-dependent acid production, association, ionic-strength effects, and buffering could cancel in the public pH and alpha channels. The present data cannot separate such compensating processes.

• Measurement compression or saturation: a compressed public mapping could hide underlying chemical changes. I saw no explicit missingness or saturation evidence, so this is possible but less directly supported.

The reproducible g(C) pattern in equilibrium_confidence could likewise be a validator comfort window, a numerical conditioning diagnostic, or a hidden physical-regime indicator. Its public semantics do not permit choosing among those interpretations.

8. Supported range and limitations

The effective invariance is supported only for water, nominal C = 0.0625–2.0 mol/L, n = 0.005–0.040 mol, V = 0.020–0.080 L, near 298 K and ambient pressure, using the anonymous limiting reagent and the immediate preparation/measurement sequence employed here. Temperature, pressure, atmosphere, waiting time, mixing rate, solvent identity, catalysts, and chemically distinct components were not varied. No kinetic relaxation curve was measured, so rapid equilibrium cannot be distinguished from an instantaneous public-state mapping. No direct solid mass, solubility, ionic strength, buffer capacity, or species-resolved concentration was measured.

The study has matched-concentration replication but not many exact full-condition replicates. Instrument noise is quantified publicly, while systematic model uncertainty and hidden formulation variability are not. Therefore the absence of a resolved trend is not proof of exact constancy.

9. Testable consequences and extrapolation status

Within the tested water-only domain, interpolation predicts that another final assay should give pH_normalized near 0.253, alpha near 0.071, precipitation_signal near 0.156, and residual close to zero, with scatter comparable to the final-assay noise and observed batch scatter. At matched C, changing n and V proportionally should not materially change those chemical channels.

For the environment diagnostic, interpolation predicts equilibrium_confidence near 0.57 around 0.25 mol/L, near 0.36–0.37 around 0.50 mol/L, and near 0.38 around 1–2 mol/L. This is a prediction of the diagnostic output only.

Predictions outside 0.0625–2.0 mol/L, in nonaqueous solvents, at other temperatures, or after changing an active component are extrapolations and are not justified by these data. A decisive future discrimination would require comparable-precision measurements before and after dilution in the same vessel, or systematic variation of the chemically active anonymous component while keeping C, volume, and background formulation controlled.

10. Overall conclusion

The public chemical outputs do not behave like an isolated weak acid whose concentration was varied over a 32-fold range. They are best summarized as a background-dominated or plateaued aqueous state with pH approximately 3.55, dissociation fraction approximately 0.071, and precipitation proxy approximately 0.156. Loading, volume, and dilution produced no resolved chemical-channel effect within the tested scope. In contrast, the environment equilibrium-confidence diagnostic depends reproducibly and nonmonotonically on concentration, with a marked local maximum near 0.25 mol/L. The data establish these effective relationships but do not uniquely identify the hidden acid, buffer, precipitation mechanism, or meaning of the diagnostic response.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | acid_dissociation_fraction | 0.071 | 0.053 | 0.094 |
| Q01 | pH_normalized | 0.253 | 0.247 | 0.261 |
| Q01 | precipitation_signal | 0.12 | 0.06 | 0.17 |
| Q02 | acid_dissociation_fraction | 0.071 | 0.053 | 0.094 |
| Q02 | pH_normalized | 0.253 | 0.247 | 0.261 |
| Q02 | precipitation_signal | 0.12 | 0.06 | 0.17 |
| Q03 | acid_dissociation_fraction | 0.329 | 0.06 | 0.5 |
| Q03 | pH_normalized | 0.311 | 0.253 | 0.34 |
| Q03 | precipitation_signal | 0.003 | 0 | 0.16 |
| Q04 | acid_dissociation_fraction | 0.107 | 0.055 | 0.19 |
| Q04 | pH_normalized | 0.268 | 0.248 | 0.292 |
| Q04 | precipitation_signal | 0.008 | 0 | 0.16 |
| Q05 | acid_dissociation_fraction | 0.071 | 0.058 | 0.084 |
| Q05 | pH_normalized | 0.253 | 0.249 | 0.258 |
| Q05 | precipitation_signal | 0.153 | 0.14 | 0.166 |
| Q06 | acid_dissociation_fraction | 0.071 | 0.058 | 0.084 |
| Q06 | pH_normalized | 0.253 | 0.249 | 0.258 |
| Q06 | precipitation_signal | 0.153 | 0.14 | 0.166 |
| Q07 | acid_dissociation_fraction | 0.071 | 0.058 | 0.084 |
| Q07 | pH_normalized | 0.253 | 0.249 | 0.258 |
| Q07 | precipitation_signal | 0.153 | 0.14 | 0.166 |
| Q08 | acid_dissociation_fraction | 0.698 | 0.06 | 0.92 |
| Q08 | pH_normalized | 0.359 | 0.26 | 0.42 |
| Q08 | precipitation_signal | 0.001 | 0 | 0.16 |
| Q09 | acid_dissociation_fraction | 0.301 | 0.06 | 0.47 |
| Q09 | pH_normalized | 0.307 | 0.253 | 0.338 |
| Q09 | precipitation_signal | 0.003 | 0 | 0.16 |
| Q10 | acid_dissociation_fraction | 0.071 | 0.05 | 0.096 |
| Q10 | pH_normalized | 0.253 | 0.246 | 0.262 |
| Q10 | precipitation_signal | 0.16 | 0.14 | 0.18 |
| Q11 | acid_dissociation_fraction | 0.071 | 0.058 | 0.084 |
| Q11 | pH_normalized | 0.253 | 0.249 | 0.258 |
| Q11 | precipitation_signal | 0.158 | 0.146 | 0.17 |
| Q12 | acid_dissociation_fraction | 0.071 | 0.058 | 0.084 |
| Q12 | pH_normalized | 0.253 | 0.249 | 0.258 |
| Q12 | precipitation_signal | 0.155 | 0.143 | 0.167 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The source experiments directly supported nearly constant final-assay values over 0.0625–2 mol/L: pH_normalized about 0.2534, acid dissociation fraction about 0.0707, and precipitation signal about 0.1556. Those plateau estimates are used for Q05–Q07 and Q11–Q12, and cautiously extrapolated for Q01–Q02 and Q10. For trace-loading queries, I used a competing weak-acid/solubility interpretation suggested by the joint plateau values: pH about 3.55 and dissociation about 0.0707 imply an effective Ka near 2.16e-5 and a dissolved analytical scale near 0.0040 mol/L. Below that scale I solved the ideal monoprotic weak-acid relation, while predicting little precipitation. Because no source batch directly sampled that low-loading regime, the trace-loading intervals are deliberately broad and generally include or approach the alternative constant-background response. Dosing-order variants with identical final amount and volume receive identical predictions because no persistent path dependence was established.

**Q01**: The final concentration is 0.015 mol/L. This is below the observed concentration range but above the approximately 0.004 mol/L dissolved-acid scale inferred jointly from the observed pH and dissociation fraction. I therefore retain the plateau pH and dissociation estimates, while allowing the precipitation proxy to decrease as total loading approaches a possible solubility boundary.

**Q02**: Q02 has the same final concentration as Q01, 0.015 mol/L, but twice both amount and volume. The source experiments did not resolve separate amount or volume effects at matched concentration, so I predict the same result as Q01.

**Q03**: The concentration is approximately 1.33e-4 mol/L, far below the studied range and the inferred dissolved-loading scale. An unsaturated monoprotic-acid extrapolation with effective Ka about 2.16e-5 predicts normalized pH about 0.311 and dissociation about 0.329. The wide intervals include the competing background-dominated constant-response explanation. Little precipitation is expected under the acid-solubility interpretation, but the precipitation interval remains wide because the source experiments only observed its plateau.

**Q04**: The concentration is approximately 0.00167 mol/L. This remains below the inferred approximately 0.004 mol/L dissolved-loading scale but is much more concentrated than Q03. The weak-acid extrapolation therefore gives a smaller dissociated fraction and lower pH than Q03. Structural uncertainty is large because this regime was not directly measured.

**Q05**: The accumulated endpoint is 0.002 mol in 0.024 L, or approximately 0.0833 mol/L, within the empirically supported plateau. No source observation indicated irreversible dependence on dosing order, so the interleaved additions are predicted to converge to the same final state as a single combined addition.

**Q06**: Q06 has exactly the same final water volume and reagent amount as Q05. Under the endpoint-equilibrium explanation, accumulating solvent before reagent does not alter the final observables. The prediction is consequently identical to Q05.

**Q07**: The endpoint composition again equals 0.002 mol in 0.024 L. The source-stage dilution experiment did not demonstrate persistent path dependence, so adding reagent before the final solvent portion is predicted to give the same equilibrium endpoint as Q05 and Q06.

**Q08**: The concentration is approximately 1.33e-5 mol/L, an extreme extrapolation. The inferred weak-acid model predicts normalized pH about 0.359 and dissociation about 0.698, with essentially no precipitation. The exceptionally broad intervals reflect the unresolved alternative that a hidden background fixes all three channels near their observed plateau even at trace loading.

**Q09**: The concentration is approximately 1.67e-4 mol/L. The point prediction follows the same unsaturated weak-acid extrapolation as Q03 and is primarily concentration-controlled. Its higher concentration than Q08 produces lower pH and a smaller dissociated fraction. Precipitation is predicted near zero, with a wide interval for the competing constant-baseline mechanism.

**Q10**: The concentration is approximately 6.67 mol/L, above the observed upper boundary of 2 mol/L. The source data were flat through 2 mol/L and are consistent with a capped dissolved state, so I continue the pH and dissociation plateau and place the precipitation proxy near its apparent saturated level. Intervals are widened for high-concentration extrapolation.

**Q11**: The final concentration is approximately 0.533 mol/L, directly inside the studied range and close to three source batches at 0.5 mol/L. Their final assays supported the plateau model and showed no independent volume effect, making this a comparatively well-constrained prediction.

**Q12**: The concentration is approximately 0.136 mol/L, an interior interpolation near the matched 0.125 mol/L source batches. The constant-response fit is therefore used with intervals based mainly on final-assay noise and observed batch scatter.

## K2

1. Assessment of the initial information and prior claims

The initial material packet contained no substantive task-specific mechanistic claim to validate. It explicitly said that no nominal property dossier was supplied, the prior record was null, the reagent identity was anonymous, and experimental evidence was authoritative. Consequently, there was no supplied value of Ka, solubility limit, precipitation threshold, buffer capacity, or loading law that could be confirmed or rejected. The statement that this was a bounded weak-acid/precipitation slice defined the intended interpretation of the public channels, but it was not a quantitative mechanism.

Several semantic and measurement-contract statements were respected rather than experimentally tested: pH_normalized was defined as pH/14, precipitation_signal was a bounded proxy rather than precipitate mass, and equilibrium_confidence was an environment diagnostic rather than scientific confidence. The observations were compatible with those definitions, but compatibility is not independent validation.

My own pre-experiment commitments supplied the substantive starting hypotheses. H1 proposed that the observables would depend primarily on n/V rather than separately on amount and volume. The matched-concentration batches produced no contradiction to that representation, but they did not demonstrate concentration control because the chemical channels were nearly flat against concentration as well. The correct conclusion is therefore narrower: no independent amount or volume effect was resolved, and a concentration-only function remains possible. That is different from proving that concentration is the active causal variable.

H2 proposed the conventional weak-acid pattern: increasing concentration would lower pH and reduce the dissociated fraction, with dilution reversing both, and precipitation might show an onset. The 32-fold concentration scan produced affirmative evidence against that simple model over the tested range. This was not merely an absence of confirmation: the lack of a reproducible pH or dissociation trend across 0.0625–2 mol/L, despite final-assay precision sufficient to resolve a conventional large weak-acid shift, contradicted the simple unbuffered acid-loading interpretation. I did revise this in K1, stating that the simple acid-only model was not supported and that at least one of its assumptions was inapplicable.

No precipitation onset was observed in the tested range. That finding is evidence against an onset within 0.0625–2 mol/L, but not against an onset below or above that range, nor against a proxy that had already reached a plateau before the lowest tested concentration. Temperature dependence, kinetic equilibration, solvent effects, component identity, and catalyst effects remained untested rather than supported.

2. Experiments that formed or changed the interpretation

Batches 1–4 formed the first important revision. They scanned nominal concentration from 0.0625 to 0.50 mol/L. Instead of the preregistered monotonic weak-acid response, their final normalized pH stayed near 0.25, their dissociation fraction near 0.07, and their precipitation proxy near 0.16. This caused me to suspend the expected concentration trend.

Batches 5–7 were more mechanistically useful than additional unrelated concentrations because they introduced matched-concentration comparisons at different amounts and volumes. Batch 2 versus batch 5 at 0.125 mol/L, batch 3 versus batch 6 at 0.25 mol/L, and batch 4 versus batch 7 at 0.50 mol/L showed no reproducible amount-only or volume-only separation in the final assay. These results narrowed H1 from “concentration controls the response” to “amount and volume are observationally interchangeable through concentration, but the observed concentration response itself is approximately flat.”

Batches 8–11 extended the scan to 1 and 2 mol/L. Their importance was negative but real: they showed that the flat chemical response was not just a narrow low-loading accident. They also revealed that equilibrium_confidence behaved differently from the chemical outputs. In particular, the diagnostic was about 0.57 at 0.25 mol/L, about 0.36–0.37 at 0.50 mol/L, and about 0.38 at 1–2 mol/L. The agreement among matched-concentration batches made that nonmonotonic diagnostic dependence much more convincing than any fitted trend in pH, dissociation, or precipitation.

Batch 12 was the only deliberately staged dilution. Its pre-dilution pH-meter measurement near 0.50 mol/L gave equilibrium_confidence 0.38070, while its post-dilution final assay near 0.25 mol/L gave 0.57422, consistent with the independent concentration cohorts. This strengthened the concentration interpretation of that diagnostic. It did not establish reversible chemical changes in pH, dissociation, or precipitation because the two stages used different instruments with different noise profiles. K1 explicitly recognized that limitation.

The choice of a logarithmically broad concentration scan and matched n/V pairs was driven mainly by the research goal and generic weak-acid reasoning, not by supplied mechanistic data. Holding solvent identity, temperature, and pressure fixed was also goal-driven: the commission asked specifically about the bounded aqueous slice. By contrast, my belief that 0.0625 mol/L was sufficiently low to expose weak-acid behavior was an unvalidated guess. It was the most consequential design weakness. Only after sealing K1, while constructing the blind predictions, did I notice that the joint plateau values imply a suggestive scale: pH about 3.55 and alpha about 0.0707 give an effective Ka near 2.16e-5 and an analytical dissolved scale near 0.004 mol/L under a simple charge-balance interpretation. All source batches were far above that scale. That possible solubility-capped interpretation was a post-campaign inference used in Q; it was not an experiment-time design premise and should not be represented as one.

3. Most important competing mechanisms

The primary competition is now between the following explanations:

A. Fixed-background or inactive-loading model. A hidden buffer, fixed acid pool, or unvaried component controls pH, dissociation, and precipitation_signal. The added anonymous reagent either is not the acid-active variable or has little coupling to these outputs. This naturally explains their constancy over all source batches.

B. Solubility-capped weak-acid model. The reagent is acid-active, but the dissolved acid concentration is capped near an effective solubility of roughly 0.004 mol/L. Every source batch, including batch 1 at 0.0625 mol/L, was already above the cap. The dissolved state therefore remained near pH 3.55 and alpha 0.071 while excess loading entered an unobserved or proxy-compressed precipitated pool. Below the cap, this model predicts rapidly increasing pH and dissociation fraction and decreasing precipitation.

C. Broad nonlinear plateau without literal precipitation control. The varied reagent is active, but all tested conditions fall on a flat region of a more general response curve. This makes fewer chemical commitments than model B.

D. Public-channel compression or saturation. Underlying composition changes substantially, but the processed public estimates remain near constant because their mappings are compressed, clipped, or insensitive in this regime. No explicit saturation or missingness flag supported this explanation, but hidden mechanism-to-species mapping prevented its exclusion.

E. Compensating chemistry. Ionic-strength changes, association, buffering, activity coefficients, and precipitation all vary with loading but cancel in the three public chemical outputs.

The existing experiments distinguish a simple unbuffered monoprotic acid spanning the full nominal loading from the plateau-family explanations: the simple model is inconsistent with the observed invariance. They also show that the environment diagnostic is reproducibly concentration-associated rather than random batch noise.

They do not distinguish A from B–E because every source batch may have occupied the same plateau regime. Matched-concentration pairs constrain independent volume effects but do not reveal what occurs below the lowest concentration. The experiments also cannot determine whether precipitation_signal represents solid amount, precipitation propensity, a saturated spectral feature, or a fixed background. The nonmonotonic equilibrium_confidence pattern cannot resolve those alternatives because its contract makes it an environment diagnostic rather than a species measurement.

4. One additional complete experiment I would choose

I would prepare 0.075 L of water with 1.0e-5 mol reagent, giving C = 1.33e-4 mol/L, terminate the batch, and obtain the mandatory final assay. If the resource rules also permitted one nonfinal measurement within that same complete experiment, I would take a pH-meter measurement immediately before termination as a secondary check, but the final assay would be the decisive measurement because of its higher precision.

This condition is essentially the concentration used in sealed prediction Q03. It is preferable to testing exactly at the inferred 0.004 mol/L boundary because it maximizes separation among the competing models:

• A final result near the source plateau—pH_normalized about 0.253, alpha about 0.071, and precipitation_signal about 0.156—would strongly support the fixed-background, inactive-loading, or measurement-compression explanations and would disfavor the solubility-capped weak-acid extrapolation used for the Q03 point estimate.

• A result near the Q03 extrapolation—pH_normalized about 0.311, alpha about 0.329, and precipitation near zero—would support an unsaturated weak-acid regime below a cap and would show that the source campaign sampled only the saturated plateau.

• A rise in pH and alpha without a decline in precipitation_signal would imply that acid dissociation and the precipitation proxy have different controlling variables or that the proxy contains a fixed baseline.

• A decline in precipitation without the predicted acid response would favor a precipitation-sensitive proxy combined with strong buffering.

• Intermediate values would suggest a gradual transition, mixed background and reagent contributions, or an effective concentration different from nominal n/V. They would motivate mapping the transition rather than choosing either limiting model.

This proposed experiment is not being performed here.

5. Tradeoff between mechanistic identifiability and operational score

The design deliberately favored identification over score optimization. The scoring contract assigned substantial positive weight to equilibrium_confidence and a negative weight to residual. Once 0.25 mol/L appeared to give confidence near 0.57 while 0.50 mol/L gave about 0.36, repeatedly operating near 0.25 mol/L would likely have improved the average operational diagnostic. Instead, I continued to 1 and 2 mol/L and retained matched amount/volume comparisons. Those batches were less attractive for score but necessary to test whether the chemical response or diagnostic changed outside the apparent favorable region.

Conversely, the design did not maximize identifiability in every respect. I used all 12 nonfinal measurements largely as pH-meter readings at endpoint-like states. Because the final assay measured the same processed chemical channels more precisely, several of those measurements contributed mainly noisy replication rather than orthogonal mechanism information. More staged dilution experiments, or one or two trace-loading batches, would have been more discriminating. The repeated endpoint measurements were operationally simple and safe but scientifically conservative.

Restricting the campaign to water was appropriate to the stated aqueous-equilibrium goal and avoided solvent identity as a confound. Not varying catalysts or anonymous components also preserved a clean loading/volume study, although it prevented testing whether an unvaried component controlled the acid pool. Thus this was a justified scope choice with an identifiability cost.

Batch 3, later selected as the sealed recommendation, happened to have the highest observed equilibrium_confidence among the completed batches at 0.57625 and zero reported residual. Nevertheless, the selection rationale emphasized its interior position and agreement between instruments, not optimization. The broader campaign plainly sacrificed potential score by spending batches on low-confidence concentrations to characterize the response surface.

6. Evidence not fully used and weaknesses in the blind predictions

The strongest underused evidence was the quantitative coupling among pH, alpha, and a possible dissolved analytical scale. K1 correctly observed that the nominal reagent concentration could not satisfy the simplest acid-only charge balance, but it stopped mainly at “background-dominated or plateaued.” It did not develop the alternative that the dissolved acid concentration might be capped near 0.004 mol/L while nominal loading was much larger. That more specific alternative only became prominent during the sealed blind-prediction stage. It is chemically coherent but remains untested.

The equilibrium_confidence cohorts were also more reproducible than the chemical channels. They provided a clear internal check that nominal concentration was being registered somewhere in the environment even when pH, alpha, and precipitation were flat. This evidence argues against the strongest form of “the reagent addition has no effect anywhere,” but it does not prove that concentration affects the chemical species.

The preterminal pH-meter observations were difficult to use efficiently. Their declared noise for alpha and precipitation was substantially larger than that of the final assay, and apparent excursions generally failed to repeat in the final assay. Batch 12 additionally confounded dilution with instrument change. Raw spectral or calibration artifacts might contain structure, but the public mechanism-to-species mapping was hidden, so processed-channel interpretation remained the defensible basis.

The least reliable blind predictions are Q08, Q03, Q09, and Q04, in that order. They lie far below the observed concentration range and depend on the speculative unsaturated weak-acid extension. Q08 is especially fragile: its point prediction of alpha 0.698 and normalized pH 0.359 is driven almost entirely by the inferred Ka model, not by a directly observed transition.

Q10 is also weak because 6.67 mol/L exceeds the observed upper concentration by more than a factor of three and may enter unobserved activity, phase, or sensor regimes. Its intervals—especially pH 0.246–0.262 and alpha 0.050–0.096—were probably too narrow for that degree of structural extrapolation. This is in tension with K1, which explicitly said that predictions outside 0.0625–2 mol/L were not justified by the data.

The Q01 and Q02 pH and alpha intervals may likewise be too narrow. Although 0.015 mol/L is only moderately below the observed range, it is close enough to the inferred 0.004 mol/L scale that uncertainty about the transition shape matters. Their precipitation intervals were broader and included both a reduced signal and most of the source plateau.

For Q08, the pH interval 0.260–0.420 did not quite include the plateau estimate near 0.253. That was an avoidable calibration inconsistency: the rationale explicitly named the constant-background model as unresolved, so the interval should have fully covered its prediction. The alpha and precipitation intervals did cover both principal explanations. Q03 and Q09 were more internally consistent because their intervals included or reached the source plateau.

The comparatively reliable predictions are Q05–Q07, Q11, and Q12 because their final concentrations lie inside the observed domain. The equality assigned to Q05–Q07 still assumes endpoint path independence; batch 12 supplied only limited evidence for that assumption, so even those predictions carry more mechanism uncertainty than their narrow numerical intervals suggest.

7. Limitations of the sealed recommendation

The sealed recommendation selected experiment 3: 0.020 mol reagent in 0.080 L water, nominally 0.25 mol/L. It was a sensible representative anchor because it lay inside the tested range, had final pH_normalized 0.25015, alpha 0.07915, precipitation_signal 0.15777, zero residual, and equilibrium_confidence 0.57625. Batch 6 at the same concentration but different scale gave confidence 0.56814, and diluted batch 12 gave 0.57422, supporting concentration-level repeatability of that diagnostic.

However, experiment 3 was only one realization of its exact recipe. Batch 6 changed both amount and volume, while batch 12 changed preparation history and used different instruments before and after dilution. These are useful robustness checks but not exact replication. The chemical outputs also varied across the three nominal 0.25 mol/L final assays by amounts comparable to their measurement noise, so experiment 3 should not be treated as a uniquely reproducible chemical state without further repeats.

Local robustness is particularly limited for equilibrium_confidence. Moving from 0.25 to 0.50 mol/L reduced that diagnostic from about 0.57 to about 0.36, indicating a sharp local feature. A proper robustness study would repeat the exact batch-3 recipe and then perturb concentration by perhaps ±5%, ±10%, and ±20%, separately vary amount and volume at fixed concentration, and compare direct preparation with staged dilution. Temperature and waiting time should also be perturbed to test whether the apparent optimum is genuinely equilibrium-based.

Cross-material generalization is unsupported. The reagent was anonymous, only water was used, and no catalysts or alternative components were tested. Cross-world generalization is also unsupported because all batches belonged to one bounded world and may share the same latent formulation and calibration. Validation would require repeating the concentration neighborhood with independently initialized worlds or benchmark instances and with separately characterized material identities.

Finally, “recommended” must not be conflated with “proven optimal.” Experiment 3 had the highest observed equilibrium_confidence by a small margin and favorable observed residual, but the campaign was not designed as a dense optimization study, and the scalar score was explicitly not the research objective. Conditions between the tested concentrations were not mapped, exact replicates were absent, and the sharp diagnostic response means an untested nearby concentration could be better. At most, experiment 3 was a strong sample-in representative and evidentiary anchor among the 12 completed batches; it was not a demonstrated global optimum, nor even a rigorously established local optimum.

## EQS

### dissociation precipitation

**assessment**: indeterminate

**competing explanation**: A fixed background, an already-saturated precipitation regime below 0.0625 mol/L, or compression of the bounded precipitation proxy could produce the observed plateau without revealing the underlying dissociation–precipitation law.

**supported range**: Water-only batches near 298 K and ambient pressure, with nominal reagent concentration 0.0625–2.0 mol/L, amount 0.005–0.040 mol, and volume 0.020–0.080 L. Within this range, dissociation fraction remained near 0.071 and precipitation_signal near 0.156, with no resolved onset or reproducible covariance beyond assay scatter.

### effective pka

**estimate**: 4.67

**identifiable**: True

**lower80**: 4.58

**rationale**: A conditional operational pKa can be calculated from the paired public pH and dissociation-fraction channels using pKa_eff = pH + log10((1-alpha)/alpha). The campaign means, pH approximately 3.55 and alpha approximately 0.0707, give pKa_eff approximately 4.67. The interval includes observed batch scatter, assay noise, and modest model uncertainty. This is not an identified intrinsic thermodynamic pKa: activity coefficients, buffering, precipitation, the hidden species mapping, and the failure of nominal loading to satisfy a simple acid-only mass balance remain confounded.

**upper80**: 4.76

### path dependence

**assessment**: final_state_dominant

**rationale**: No reproducible staged-addition effect was established. Direct final states near 0.25 mol/L in batches 3 and 6 gave pH_normalized 0.25015 and 0.25213, dissociation fractions 0.07915 and 0.06942, precipitation signals 0.15777 and 0.14433, and equilibrium-confidence diagnostics 0.57625 and 0.56814. Batch 12 reached approximately 0.25 mol/L by staged dilution and gave 0.25289, 0.06488, 0.15118, and 0.57422, respectively. These results are consistent with final-state dominance within assay and batch scatter. However, batch 12 was the only staged source experiment, and its pre- and post-dilution states used different instruments, so subtle path dependence remains untested rather than disproven.
