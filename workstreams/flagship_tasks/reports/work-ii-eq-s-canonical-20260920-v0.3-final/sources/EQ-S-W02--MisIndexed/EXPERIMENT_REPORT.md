# EQ-S-W02--MisIndexed — final English experiment report

World `EQ-S-W02`; information arm `MisIndexed`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 72 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.04 | 0.004 | ph_meter, final_assay | 0.148337 | 0 | 0.00107888 | 0 |
| 2 | 0.06 | 0.004 | ph_meter, final_assay | 0.165952 | 0 | 0 | 0.00201976 |
| 3 | 0.08 | 0.004 | ph_meter, final_assay | 0.174298 | 0.00531568 | 0.0102555 | 0 |
| 4 | 0.04 | 0.012 | ph_meter, final_assay | 0.118223 | 0.00165967 | 0 | 0 |
| 5 | 0.06 | 0.012 | ph_meter, final_assay | 0.1304 | 0.00130424 | 0 | 0 |
| 6 | 0.08 | 0.012 | ph_meter, final_assay | 0.138001 | 0 | 0.000194243 | 0 |
| 7 | 0.04 | 0.024 | ph_meter, final_assay | 0.0898408 | 0.00280845 | 0.0154742 | 0.000206568 |
| 8 | 0.06 | 0.024 | ph_meter, final_assay | 0.105251 | 0 | 0 | 0.00424874 |
| 9 | 0.08 | 0.024 | ph_meter, final_assay | 0.115473 | 0.000809062 | 0 | 0 |
| 10 | 0.04 | 0.04 | ph_meter, final_assay | 0.0676313 | 0.00213151 | 0.0572493 | 0 |
| 11 | 0.06 | 0.04 | ph_meter, final_assay | 0.0867987 | 0.000624026 | 0.0386733 | 0 |
| 12 | 0.08 | 0.04 | ph_meter, final_assay | 0.0995204 | 0 | 0 | 0 |

### Sealed evidentiary anchor

Batch `10`: Batch 10 is a useful high-loading, low-volume anchor: its final assay clearly captures the acidic, precipitating edge of the factorial loading–dilution response for comparison with the more dilute batches.

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## K1 — sealed open mechanistic report (primary mechanism artifact)

Mechanistic report

1. Experimental basis

I completed a 4 × 3 factorial study in water at approximately 297.2 K. Reagent loading n was 0.004, 0.012, 0.024, or 0.040 mol, and liquid volume V was 0.040, 0.060, or 0.080 L. Every batch also received 0.003 mol of Catalyst A. Thus the nominal reagent concentration C = n/V covered 0.050–1.000 mol L^-1. Each batch was measured with the pH meter before termination and with the final assay after termination. The discussion below emphasizes the more precise final assay while using the pH-meter results as a consistency check.

Final-assay observations were:

Batch 1: n=0.004 mol, V=0.040 L, C=0.100 M; pH_normalized=0.14834, acid fraction=0, precipitation=0.00108.
Batch 2: n=0.004 mol, V=0.060 L, C=0.0667 M; pH_normalized=0.16595, acid fraction=0, precipitation=0.
Batch 3: n=0.004 mol, V=0.080 L, C=0.050 M; pH_normalized=0.17430, acid fraction=0.00532, precipitation=0.01026.
Batch 4: n=0.012 mol, V=0.040 L, C=0.300 M; pH_normalized=0.11822, acid fraction=0.00166, precipitation=0.
Batch 5: n=0.012 mol, V=0.060 L, C=0.200 M; pH_normalized=0.13040, acid fraction=0.00130, precipitation=0.
Batch 6: n=0.012 mol, V=0.080 L, C=0.150 M; pH_normalized=0.13800, acid fraction=0, precipitation=0.00019.
Batch 7: n=0.024 mol, V=0.040 L, C=0.600 M; pH_normalized=0.08984, acid fraction=0.00281, precipitation=0.01547.
Batch 8: n=0.024 mol, V=0.060 L, C=0.400 M; pH_normalized=0.10525, acid fraction=0, precipitation=0.
Batch 9: n=0.024 mol, V=0.080 L, C=0.300 M; pH_normalized=0.11547, acid fraction=0.00081, precipitation=0.
Batch 10: n=0.040 mol, V=0.040 L, C=1.000 M; pH_normalized=0.06763, acid fraction=0.00213, precipitation=0.05725.
Batch 11: n=0.040 mol, V=0.060 L, C=0.6667 M; pH_normalized=0.08680, acid fraction=0.00062, precipitation=0.03867.
Batch 12: n=0.040 mol, V=0.080 L, C=0.500 M; pH_normalized=0.09952, acid fraction=0, precipitation=0.

The environmental quantity equilibrium_confidence is not treated as scientific confidence. It ranged roughly from 0.644 to 0.695 in the final assays. Final equilibrium_residual values were zero or very small, at most 0.00425, but these diagnostics do not by themselves establish a chemical mechanism.

2. Empirical loading–dilution relationship

Normalized pH is governed predominantly by the ratio n/V rather than by n or V independently. At fixed loading, dilution consistently raised normalized pH. For example, at n=0.004 mol it rose from 0.14834 in 0.040 L (batch 1) to 0.17430 in 0.080 L (batch 3). At n=0.040 mol it rose from 0.06763 (batch 10) to 0.09952 (batch 12). Conversely, increasing loading at fixed volume lowered pH: at V=0.040 L, the value fell from 0.14834 at 0.004 mol to 0.06763 at 0.040 mol.

A descriptive least-squares fit over all 12 final assays is

pH_normalized = 0.072998 - 0.034278 ln(C / 1 M),

with an RMS residual of 0.00249 in normalized-pH units. Because pH_normalized=pH/14, this is equivalently

pH approximately 1.022 - 1.105 log10(C / 1 M).

This fit is empirical and should only be used over C=0.05–1.0 M under the tested formulation. The two independently prepared C=0.300 M batches support concentration collapse: batches 4 and 9 gave 0.11822 and 0.11547 despite having twofold different total loadings and volumes. Their difference, 0.00275, is comparable to the overall regression residual.

The corresponding purely descriptive hydrogen-ion relation is [H+] approximately 0.095 C^1.105 when concentrations are expressed in mol L^-1. This should not be mistaken for an independently validated activity-based law.

3. Acid-dissociation fraction

The reported final-assay acid-dissociation fraction was at or very near its lower boundary throughout the entire design. Seven of twelve final values were exactly zero, the largest was only 0.00532, and the mean was 0.00122. These values are comparable to the stated final-assay noise scale of 0.006. Therefore the data support only an upper-bound conclusion: the reported free acid-dissociation channel is unresolved and close to zero over the tested range. They do not support a reliable loading or dilution exponent for that channel.

The noisier pH-meter estimates were larger, with a mean of 0.0138 and individual values up to 0.0302, but its stated noise scale for this observable was 0.015 and several measurements were clipped to zero. The difference between the two instruments is consequently consistent with a combination of noise, lower-bound clipping, and possible instrument-specific bias; it is not evidence for a reproducible change caused by termination.

There is an important mechanistic inconsistency if the reported fraction is interpreted literally as alpha=[A-]/([HA]+[A-]) in a simple monoprotic-acid solution. The measured pH values imply appreciable hydrogen-ion concentrations, whereas the fraction channel is essentially zero. For example, batch 1 has pH_normalized=0.14834, or pH about 2.077, implying [H+] around 8 × 10^-3 M, which is incompatible with alpha approximately zero at C=0.1 M under a closed, electroneutral HA-only model. Thus at least one additional feature is required: counterions or background acidity, removal of A- into a solid or complex, activity effects, or a semantic/calibration mismatch in what the public fraction channel represents.

4. Precipitation response

The final precipitation proxy was mostly indistinguishable from zero below about 0.5 M and became reproducibly positive in the concentrated regime. The clearest high-concentration observations were batch 7 at 0.600 M (0.01547), batch 11 at 0.6667 M (0.03867), and batch 10 at 1.000 M (0.05725). Batch 12 at 0.500 M was zero. This suggests an onset region around 0.5–0.6 M followed by increasing precipitation signal, rather than a smooth response across the full range.

The isolated batch-3 value of 0.01026 at only 0.050 M is not enough to establish low-concentration precipitation: it is less than twice the stated 0.006 final-assay noise scale, and neighboring low-concentration batches were near zero. The pre-termination pH-meter precipitation channel showed the same broad high-loading tendency but substantial scatter—for example, 0.03975 in batch 7 and 0.08803 in batch 10—consistent with its larger stated noise scale of 0.02.

The proxy is bounded and has no supplied conversion to solid amount, so I infer only a threshold-like response, not a precipitated mole balance, solubility product, or crystal identity.

5. Defensible reaction-network interpretation

The supplied structural hypothesis was:

HA(aq) <=> H+(aq) + A-(aq)
M+(aq) + A-(aq) <=> MA(s),

with no distinct aqueous MA intermediate. This topology remains chemically capable of explaining the qualitative observations: increasing analytical acid concentration lowers pH, while sufficiently high free-ion activity crosses a precipitation boundary. A thermodynamic representation would be

Ka,eff = a_H a_A / a_HA,
Ksp,eff = a_M a_A,

combined with acid, metal, charge, and solid mass balances. Precipitation can be represented by complementarity conditions

P >= 0,
Ksp,eff - a_M a_A >= 0,
P(Ksp,eff - a_M a_A)=0,

where P is solid amount, followed by an unknown monotone instrument mapping precipitation_signal=g(P).

However, the experiment does not uniquely validate that topology. In particular, merely refitting a constant Ka in the simplest ideal HA model is inadequate. The empirical pH slope is about -1.105 per decade of concentration, whereas the conventional weak-acid limiting slope is -0.5. An exact finite-dissociation model can deviate from the limiting slope, but the near-zero reported alpha and the observed pH cannot both be reconciled by changing Ka alone. Therefore this is a topology/measurement issue rather than just a parameter-estimation issue.

My preferred bounded interpretation is an effective coupled network:

(1) Reagent loading establishes a total acid-like pool C=n/V.
(2) A rapid acid/base process generates the observed hydrogen activity, with substantial nonideality or an unobserved charge-balancing/background component.
(3) An anionic or otherwise precipitation-active form couples to a metal-like component associated with the fixed formulation.
(4) Above an activity threshold near the concentrated end, that component is removed into a solid-like reservoir, producing the public precipitation proxy.
(5) The public acid-fraction channel measures a much narrower free pool than the amount inferred from pH, or is effectively floor-limited in this regime.

This preserves the useful direct-free-ion skeleton without claiming that the nominal two-equilibrium ideal model is quantitatively established.

6. Experiments that shaped or modified the interpretation

Batches 1–3 first established that dilution at fixed 0.004 mol systematically raises pH. Batches 4–6 and 7–9 reproduced the direction at higher loadings, making a concentration artifact less likely. Batches 4 and 9 were especially diagnostic because both had C=0.300 M despite different n and V; their similar pH and zero precipitation supported n/V as the leading state variable.

Batches 10–12 established the concentrated precipitation regime. Batch 10, the selected evidentiary anchor, combined the lowest final normalized pH (0.06763) with the largest final precipitation signal (0.05725). Batch 12 showed that dilution of the same 0.040 mol loading to 0.500 M suppressed the final proxy to zero. These observations changed the working picture from a pH-only concentration response to a coupled pH-plus-threshold precipitation response.

Across all batches, the near-zero final acid-fraction channel forced a modification of the literal supplied model. Rather than treating the dossier's equation graph and its observable mapping as simultaneously proven, I retain the graph only as one effective topology and explicitly separate it from the unresolved mapping between species and reported fraction.

7. Competing explanations

Several alternatives are observationally equivalent with the available data:

• Aqueous complexation: M+ + A- <=> MA(aq), followed by MA(aq) <=> MA(s). A soluble intermediate could keep free A- near zero while allowing acidity and eventual precipitation. No species-selective measurement was made to exclude it.

• Background-ion or buffer model: an unobserved electrolyte supplies charge balance and modifies hydrogen activity; precipitation may involve that background component rather than the nominal free M+/A- pair.

• Activity-coefficient model: the topology may be correct, but strong concentration-dependent activities over 0.05–1.0 M make concentration-based Ka and Ksp appear variable.

• Multiple-acid or ion-pair model: the limiting reagent could populate more than one protonated or ion-paired state, making the single reported fraction an incomplete acid balance.

• Observable-mapping mismatch: the acid-fraction channel may represent only one free species, may be effectively misassigned, or may have a near-floor calibration in this slice. This directly explains the disagreement with pH but cannot be distinguished from real sequestration using the existing aggregate channels.

• Empirical threshold model without literal solid equilibrium: precipitation_signal could be a bounded concentration-triggered proxy rather than a calibrated solid amount. The observed data alone cannot establish a true Ksp law.

8. Scope and non-identifiability

The supported scope is water, Catalyst A, 0.003 mol catalyst per batch, 297 K, reagent concentrations of 0.05–1.0 M, volumes of 0.040–0.080 L, and the particular preparation/termination sequence used here. The pH fit and approximate precipitation onset should not be extrapolated to other solvents, catalysts, temperatures, times, or concentrations.

Catalyst amount was fixed in moles, not concentration. Its nominal concentration therefore changed from 0.075 M at 0.040 L to 0.0375 M at 0.080 L. The close agreement of batches 4 and 9 suggests reagent concentration is dominant, but catalyst concentration remains a partial confound and the metal stoichiometry is not identifiable. Only Catalyst A and water were tested. There were no deliberate equilibration-time, temperature, catalyst-identity, or metal-loading series, and no direct solid or species assay. Kinetic versus equilibrium control, solid stoichiometry, true Ka, true Ksp, activity coefficients, and the existence of aqueous MA therefore remain unresolved.

9. Testable predictions, stated as extrapolations

Within the studied formulation and range, an untested batch at C=0.25 M should have pH_normalized near 0.1205 from the empirical logarithmic fit and little resolvable precipitation. At C=0.8 M, the same fit predicts pH_normalized near 0.0806 and a positive precipitation proxy, probably between the batch-11 and batch-10 values. These are interpolation predictions, not new observations.

If concentration is truly the controlling variable, changing n and V together while holding n/V fixed should preserve normalized pH to within roughly 0.003, after accounting for the catalyst-concentration confound. If a soluble MA intermediate is important, a species-selective assay should reveal it before the precipitation proxy turns on. If the near-zero fraction is only an observable-mapping problem, an independent acid balance or titration should disagree systematically with that public channel while remaining consistent with pH.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.34 | 0.27 | 0.43 |
| Q01 | acid_dissociation_fraction | 0.02 | 0 | 0.12 |
| Q01 | precipitation_signal | 0 | 0 | 0.01 |
| Q02 | pH_normalized | 0.261 | 0.22 | 0.31 |
| Q02 | acid_dissociation_fraction | 0.01 | 0 | 0.08 |
| Q02 | precipitation_signal | 0 | 0 | 0.01 |
| Q03 | pH_normalized | 0.199 | 0.175 | 0.23 |
| Q03 | acid_dissociation_fraction | 0.005 | 0 | 0.04 |
| Q03 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q04 | pH_normalized | 0.144 | 0.132 | 0.157 |
| Q04 | acid_dissociation_fraction | 0.002 | 0 | 0.018 |
| Q04 | precipitation_signal | 0.001 | 0 | 0.014 |
| Q05 | pH_normalized | 0.097 | 0.083 | 0.112 |
| Q05 | acid_dissociation_fraction | 0.002 | 0 | 0.014 |
| Q05 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q06 | pH_normalized | 0.065 | 0.045 | 0.085 |
| Q06 | acid_dissociation_fraction | 0.002 | 0 | 0.015 |
| Q06 | precipitation_signal | 0.075 | 0.03 | 0.14 |
| Q07 | pH_normalized | 0.097 | 0.078 | 0.118 |
| Q07 | acid_dissociation_fraction | 0.002 | 0 | 0.018 |
| Q07 | precipitation_signal | 0.003 | 0 | 0.03 |
| Q08 | pH_normalized | 0.134 | 0.121 | 0.149 |
| Q08 | acid_dissociation_fraction | 0.002 | 0 | 0.018 |
| Q08 | precipitation_signal | 0.001 | 0 | 0.014 |
| Q09 | pH_normalized | 0.168 | 0.153 | 0.185 |
| Q09 | acid_dissociation_fraction | 0.003 | 0 | 0.025 |
| Q09 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q10 | pH_normalized | 0.183 | 0.166 | 0.203 |
| Q10 | acid_dissociation_fraction | 0.004 | 0 | 0.032 |
| Q10 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q11 | pH_normalized | 0.199 | 0.172 | 0.232 |
| Q11 | acid_dissociation_fraction | 0.005 | 0 | 0.045 |
| Q11 | precipitation_signal | 0.001 | 0 | 0.014 |
| Q12 | pH_normalized | 0.199 | 0.176 | 0.228 |
| Q12 | acid_dissociation_fraction | 0.005 | 0 | 0.04 |
| Q12 | precipitation_signal | 0.001 | 0 | 0.012 |

### Q rationales

- **Q01**: This concentration is far below the observed 0.05–1.0 M range. Log-concentration extrapolation gives normalized pH near 0.34, but the low-concentration asymptote is poorly constrained. Precipitation should be absent. The acid-fraction interval is deliberately broad because dilution could lift the channel from its observed floor.

- **Q02**: The empirical pH relation predicts 0.261, although this remains a substantial low-side extrapolation. No precipitation is expected. The fraction estimate remains close to the assay floor but allows a dilution-driven increase.

- **Q03**: At 0.025 M, the concentration-only pH fit gives 0.199. This is just below the supported concentration range, so uncertainty is moderate. The precipitation proxy should remain at its lower boundary.

- **Q04**: This is an interpolation between studied concentrations. The predicted normalized pH is 0.144, with negligible precipitation. The reported acid fraction was unresolved near zero throughout the experiments, so only a small value is predicted.

- **Q05**: The pH prediction is an interpolation and agrees with the observed half-molar neighborhood. Precipitation onset appeared near 0.5–0.6 M, so the point estimate is small but the interval admits a weak positive signal.

- **Q06**: This lies above the observed 1.0 M boundary. The pH estimate follows the fitted logarithmic trend. Positive precipitation is expected by extrapolating the concentrated-regime response, but its magnitude is uncertain because the proxy-to-solid mapping and saturation behavior were not identified.

- **Q07**: Concentration collapse predicts the same central pH as Q05. The wider interval accounts for the much smaller absolute scale and for the fact that exact scale invariance was only weakly tested. The half-molar state is near the apparent precipitation onset.

- **Q08**: This is within the concentration range where pH followed n/V closely. The fitted value is 0.134. It is well below the observed precipitation onset, and the acid-fraction channel is predicted to remain near its floor.

- **Q09**: The concentration lies near the dilute edge of the observed campaign, giving a normalized-pH estimate of 0.168. Precipitation should be absent; the fraction remains poorly resolved but may rise slightly under dilution.

- **Q10**: This is a modest extrapolation below the lowest studied concentration. The pH estimate follows the observed dilution trend. No precipitation is expected, while the acid-fraction interval allows an unresolved low-concentration increase.

- **Q11**: Concentration invariance gives the same central prediction as Q03. The small absolute scale is outside the campaign design, so intervals are widened for possible finite-loading or volume effects.

- **Q12**: At the same 0.025 M concentration as Q03 and Q11, the leading model predicts the same normalized pH and negligible precipitation. The relatively large volume reduces concern about very-small-scale effects, although this remains below the directly studied concentration range.

Shared rationale:

The central pH predictions use the campaign fit pH_normalized = 0.072998 - 0.034278 ln(C/1 M), which had an RMS residual of about 0.00249 over 0.05–1.0 M. Intervals expand outside that range and for scale controls. Final-assay acid-dissociation fractions were predominantly clipped at zero, with mean 0.00122 and no identifiable concentration law; predictions therefore remain near the floor while low-concentration intervals allow a possible dissociation upturn. The precipitation proxy was effectively zero through about 0.5 M and positive at 0.6–1.0 M, motivating a threshold-like extrapolation for Q06. All blind batches omit the fixed Catalyst A addition used in the research campaign, so formulation transfer is an additional unmeasured uncertainty, especially for acid fraction and precipitation.

## K2 — sealed seven-part retrospective

1. Assessment of the initial claims

The initial material did contain substantive mechanistic claims. It proposed the local network HA(aq) ⇌ H+(aq) + A−(aq), followed by M+(aq) + A−(aq) ⇌ MA(s), and specifically asserted that there was no distinct aqueous MA intermediate. It also proposed the dissolved-acid balance n_HA+n_A− and said that the three public metrics should follow this species graph.

The acid-like concentration response received qualitative support. Increasing n/V consistently lowered normalized pH: for example, batch 1 at 0.100 M gave 0.14834, whereas batch 10 at 1.000 M gave 0.06763. Batches 4 and 9, both at 0.300 M but at different scales, gave similar values of 0.11822 and 0.11547. This supports concentration as an important state variable and is compatible with acid dissociation, but it does not uniquely establish HA ⇌ H+ + A−.

The precipitation branch also received only qualitative support. Positive signals appeared mainly at the concentrated end: 0.01547 in batch 7 at 0.600 M, 0.03867 in batch 11 at 0.6667 M, and 0.05725 in batch 10 at 1.000 M. That is compatible with a solubility threshold, but neither the identity MA(s), its stoichiometry, nor the equation a_Ma_A=Ksp was measured.

The assertion that aqueous MA is absent was not tested. No species-selective measurement distinguished free ions, soluble ion pairs, aqueous MA, or other complexes. Absence of a detected intermediate is therefore not evidence of its absence.

The proposed dissolved-acid balance and the claimed mapping of the three metrics to the graph were actively challenged by the data. In batch 1, pH_normalized=0.14834 corresponds to pH about 2.08, yet the final reported acid-dissociation fraction was exactly zero. The same disagreement persisted throughout the campaign: seven final fraction values were zero, the maximum was only 0.00532, and the mean was 0.00122. A literal single-acid, closed electroneutral interpretation cannot make these observations mutually consistent without additional species, sequestration, background charge, activity effects, or an observable-mapping problem.

This is an instance where counterevidence had already appeared, not merely a case of finding no counterevidence. After batch 1, I should have recognized the pH/fraction contradiction as a reason to change the experimental design. Instead, I continued the planned factorial series with the same catalyst condition. I did revise the interpretation in K1, stating that “at least one additional feature is required” and that changing Ka alone was inadequate, but that revision occurred mainly in the final analysis rather than through adaptive experiments during the campaign.

The initial qualification that the claim was local to a bounded benchmark was appropriate and remains supported. There was no task-specific numerical property dossier, so there were no supplied Ka, Ksp, activity coefficients, or calibrated solid-response parameters to confirm or refute.

2. Experiments that formed or changed the judgment

The full loading–volume grid was the main source of the concentration-response judgment. Batches 1–3 established the dilution direction at n=0.004 mol. Batches 4–6 and 7–9 reproduced it at larger loadings. Batches 10–12 showed the same direction at n=0.040 mol. This repetition across loading levels made the n/V interpretation substantially stronger than it would have been from one dilution series.

Batches 4 and 9 were especially informative because both had C=0.300 M while total loading and volume differed by a factor of two. Their close pH values supported approximate concentration scaling. However, this was only one same-concentration comparison, not a general proof of scale invariance.

Batches 7, 10, 11, and 12 changed the precipitation interpretation. Batch 12 at 0.500 M gave zero final precipitation signal, while batches 7, 11, and 10 at 0.600, 0.6667, and 1.000 M were positive. That motivated the K1 judgment of an onset region around 0.5–0.6 M. The isolated 0.01026 signal in batch 3 at 0.050 M was treated as likely noise rather than evidence of a second low-concentration precipitation regime.

The persistent acid-fraction floor across all batches changed my view of the supplied graph most strongly. It led K1 to separate equation topology from observable mapping and to retain the direct-free-ion graph only as an effective candidate.

The factorial choices primarily came from the research goal and available resource limits: four reagent loadings crossed with three volumes used all 0.24 mol reagent and 0.72 L solvent exactly. The decision to hold water and Catalyst A constant was intended to isolate loading and dilution.

The Catalyst A addition itself depended on an unverified mechanistic guess. I implicitly treated the catalyst as a useful fixed formulation component and possibly as related to the metal-like precipitation branch. The public material information did not establish that Catalyst A was M+, and it described catalyst identities as opaque benchmark formulations. This assumption was not validated. More importantly, using 0.003 mol in every batch meant that catalyst concentration changed with volume—from 0.075 M at 0.040 L to 0.0375 M at 0.080 L—so the nominal dilution experiment also varied catalyst concentration. The later blind queries omitted catalyst entirely, exposing this as the most consequential design weakness.

3. Principal competing mechanisms and current discriminating power

The leading effective explanation remains a concentration-dependent acid-like response coupled to a high-concentration precipitation or association threshold. A direct-free-ion implementation is:

HA ⇌ H+ + A−
M+ + A− ⇌ MA(s).

Its chief competitor is a soluble-association network:

HA ⇌ H+ + A−
M+ + A− ⇌ MA(aq)
MA(aq) ⇌ MA(s).

The current metrics cannot distinguish these networks because neither free M+, free A−, aqueous MA, nor solid amount was measured directly. A soluble complex could explain why the public free-fraction channel remains near zero while the pH remains acidic.

A second competitor is an activity/background-electrolyte model. Strongly concentration-dependent activities, an unobserved counterion, or background acidity could generate the pH trend without requiring the reported acid fraction to equal [H+]/C. The observed logarithmic pH fit distinguishes a simple constant-Ka ideal weak acid poorly: its pH slope was about −1.105 per concentration decade, rather than the conventional −0.5 weak-acid limit. It does not distinguish activity effects from extra equilibria.

A third explanation is an observable-indexing or calibration mismatch. The public “acid_dissociation_fraction” may describe a narrow free pool, may be clipped at its lower boundary, or may not correspond to the species fraction inferred from pH. The experiments strongly reveal an inconsistency but cannot decide whether it is chemical sequestration or a measurement-semantic problem.

A fourth alternative is that Catalyst A materially changed the equilibrium. If it promoted association, supplied a metal-like component, or altered the public proxy, then the campaign characterized a catalyst-containing subsystem rather than the catalyst-free world used in the blind queries. Because every research batch contained the same catalyst amount, the existing experiments cannot distinguish catalyst causation from intrinsic concentration response.

The experiments can distinguish gross concentration dependence from a purely total-mole-controlled model, particularly through batches 4 and 9. They can also distinguish a uniformly linear precipitation response from an apparent threshold-like response. They cannot identify Ka, Ksp, solid stoichiometry, catalyst role, aqueous intermediates, kinetic versus equilibrium control, or the exact mapping from latent species to the public channels.

4. One additional complete experiment

I would run a catalyst-omission matched control at exactly the batch-4 reagent and solvent condition: 0.040 L water plus 0.012 mol reagent, with no catalyst, giving C=0.300 M. I would measure once with the pH meter before termination, then terminate and perform the required final assay. This is a legal complete experiment and differs from batch 4 primarily by removal of the 0.003 mol Catalyst A addition.

The comparison has several diagnostic outcomes:

• If pH remains near batch 4’s 0.11822, the final acid fraction remains near zero, and precipitation remains zero, Catalyst A is probably not responsible for the central pH/fraction inconsistency at 0.300 M. That would strengthen the observable-mismatch, background-ion, or intrinsic-complexation explanations.

• If removal of catalyst raises the acid fraction substantially while leaving pH similar, Catalyst A likely sequesters or reassigns the free A−-like pool without controlling hydrogen activity. The direct precipitation/association branch would become more credible, and my catalyst-free blind fraction predictions would need to be much higher than the campaign values.

• If removal of catalyst changes both pH and acid fraction, the entire concentration fit is formulation-specific. The K1 empirical equation would then not transfer directly to the blind queries.

• If precipitation changes while pH and fraction remain similar, Catalyst A likely affects the solid/proxy branch selectively.

• If the pH-meter and final assay again disagree systematically, an instrument-specific bias, termination-state effect, or censoring model would deserve priority over fine mechanistic fitting.

I prefer this matched control over another concentration point because catalyst omission is the largest untested intervention separating the completed campaign from the blind-prediction recipes.

5. Tradeoff between identifiability and operational score

The stated goal was mechanism characterization rather than scalar-score optimization, and my design largely honored that. I chose a broad factorial loading–dilution grid rather than repeatedly operating near conditions likely to maximize equilibrium_confidence or minimize residual. High-concentration batches 7, 10, and 11 were retained because they probed precipitation onset even though batch 10 had a relatively low environment diagnostic equilibrium_confidence of 0.64378. This sacrificed potential score for response-surface coverage.

The design also spent every final assay and every intermediate-measurement allowance across twelve distinct conditions instead of using replicates. That improved coverage and concentration-range identifiability but weakened uncertainty estimation and made isolated signals, such as batch 3’s precipitation value, difficult to classify.

There was no deliberate attempt to optimize the published scalar score. In particular, K1 correctly treated equilibrium_confidence as an environment diagnostic rather than personal scientific confidence. The selected batch 10 was chosen as an informative high-loading anchor, not because it was demonstrated to optimize the score.

Nevertheless, the design was not maximally identifiable. Fixing catalyst identity and amount, using only water, omitting a no-catalyst control, and making no time or temperature perturbation left several mechanisms aliased. The tidy 4×3 grid favored an easily modeled response surface over adaptive diagnosis of the unexpected acid-fraction contradiction. Thus I sacrificed some mechanistic identifiability for systematic coverage—not for score optimization, but for design regularity and efficient use of stocks.

6. Underused evidence and weaknesses in the blind predictions

The paired pH-meter and final-assay data were not used as fully as they could have been. I noted that the pH-meter acid fractions averaged 0.0138 while final assays averaged 0.00122, but I did not fit an explicit censored-error or instrument-bias model. Likewise, pre-termination precipitation values in batches 7 and 10 were higher than their final-assay values, yet I did not determine whether the difference was consistent with noise, termination, or instrument mapping.

I used processed estimates almost exclusively. The richer public signal packets, calibration metadata, and any spectral or mass-balance structure were not incorporated into the final model. The near-zero values should also have been treated formally as boundary-censored observations rather than ordinary measurements.

The residual structure around the logarithmic pH fit was summarized only by an RMS value. I did not fit separate n, V, and catalyst-concentration terms, even though fixed catalyst moles caused its concentration to covary with volume. The single same-C comparison between batches 4 and 9 was useful but insufficient to eliminate those terms.

The least reliable blind predictions are Q01 and Q02, at 0.0004167 and 0.0041667 M, because they extrapolate one to two orders of magnitude below the studied 0.05 M boundary. Q01’s pH interval of 0.27–0.43 is broad, but even that may not cover a water/background-electrolyte asymptote or a change in acid regime. Their acid-fraction estimates are also highly model-dependent.

Q06 is similarly fragile at 1.25 M. Its precipitation estimate of 0.075 and interval of 0.03–0.14 extrapolate a bounded proxy beyond the highest observed concentration and assume that the apparent threshold continues monotonically. Saturation or a different phase regime could invalidate that interval.

Q07 is particularly uncertain despite being at the nominally familiar 0.5 M concentration. Its volume is only 0.006 L, well below the campaign minimum of 0.040 L, and it contains no catalyst. The pH interval 0.078–0.118 and precipitation interval 0–0.03 may therefore be too narrow.

Q03, Q11, and Q12 test scale invariance at 0.025 M, below the observed concentration range and across volumes of 0.012–0.072 L. Assigning the same pH central estimate of 0.199 was consistent with the K1 concentration-collapse model, but the intervals may understate finite-volume, total-loading, and catalyst-omission uncertainty.

More generally, every blind recipe omitted Catalyst A, whereas every research batch contained it. The final blind rationale acknowledged this as “an additional unmeasured uncertainty,” but several in-range pH intervals—especially Q04, Q05, Q08, Q09, and Q10—were still based mainly on regression residual and are probably too narrow for cross-formulation transfer. This is partly inconsistent with K1’s stated scope, which explicitly restricted support to “water, Catalyst A, 0.003 mol catalyst per batch.” Applying the same central law to catalyst-free queries was an extrapolation beyond that scope. The prediction response disclosed the extrapolation, but its numerical intervals did not always fully reflect it.

The acid-fraction predictions attempted to hedge by using lower bounds of zero and broad upper bounds at low concentration. However, their point estimates combined two incompatible ideas: the observed near-zero public channel and a possible dilution-driven dissociation increase inferred indirectly from pH. Without a catalyst-free control, those point estimates have little empirical identification.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 10: 0.040 mol reagent in 0.040 L water with 0.003 mol Catalyst A. It was selected because it was an informative edge condition, with the lowest observed final normalized pH, 0.06763, and the largest observed precipitation signal, 0.05725. This made it useful for blind replay and for anchoring the concentrated regime.

It was not demonstrated to be an optimal operation. The research objective explicitly rejected score optimization, and batch 10’s equilibrium_confidence diagnostic was lower than many dilute batches. Its distinction is “largest precipitation signal and lowest pH among the twelve sampled conditions,” not “best condition,” and certainly not a global optimum. Even calling it the sample-best condition would require specifying a metric; it was sample-highest only for precipitation signal and sample-lowest for pH.

Repeatability should first be tested with independent exact replicates of batch 10, including both the pre-termination pH measurement and final assay. This would quantify whether the observed 0.05725 precipitation signal is stable relative to the stated assay noise and whether the pre/final difference recurs.

Local robustness should be tested around batch 10 by small independent perturbations of reagent loading and volume—for example, nearby concentrations on both sides of 1.0 M—while separately holding catalyst moles and catalyst concentration constant. The original design could not do both simultaneously. Small changes in equilibration time and temperature would test whether the apparent endpoint is genuinely equilibrated rather than path-dependent.

Material robustness requires catalyst omission, variation of catalyst amount, testing Catalysts B–D, and repeating in other permitted solvents. Because the identities are opaque benchmark formulations, success with Catalyst A cannot be translated into a real material claim.

Cross-world generalization would require repetition under independently instantiated benchmark worlds or parameterizations. The K1 law and the recommendation were fitted to one bounded world and one campaign trajectory. They establish neither universality nor transportability. The proper conclusion is that batch 10 is an informative sampled extreme within this campaign, not a proven optimum or generally recommended chemical process.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0085109 | 1 | 0.054 | 0.054 |
| acid_dissociation_fraction | 0.0145158 | 0.916667 | 0.03875 | 0.0612433 |
| precipitation_signal | 0.00154523 | 1 | 0.0229167 | 0.0229167 |

## Response-shape evaluation

Concentration slope MAE `0.0156192` and curvature MAE `0.0145201`. Dilution slope MAE `0.00627168` and curvature MAE `0.0108662`.

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form mechanism artifact. No candidate mechanism family, equation menu, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. No closed-set family-accuracy or single composite mechanism score is authorized.
