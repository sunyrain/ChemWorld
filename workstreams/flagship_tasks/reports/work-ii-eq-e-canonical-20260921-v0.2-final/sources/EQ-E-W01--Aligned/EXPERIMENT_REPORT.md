# EQ-E-W01--Aligned — final English experiment report

World `EQ-E-W01`; information arm `Aligned`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.08 | 0.01 | ph_meter, final_assay | 0.140713 | 0.0136812 | 0.0664171 | 0 |
| 2 | 0 | 0.08 | 0.03 | ph_meter, final_assay | 0.109263 | 0.00554942 | 0.0631309 | 0 |
| 3 | 0 | 0.04 | 0.005 | ph_meter, final_assay | 0.144727 | 0.00433489 | 0.0733006 | 0 |
| 4 | 0 | 0.04 | 0.015 | ph_meter, final_assay | 0.112409 | 0.0084669 | 0.0748775 | 0 |
| 5 | 1 | 0.08 | 0.01 | ph_meter, final_assay | 0.160596 | 0 | 0.0454669 | 0 |
| 6 | 1 | 0.08 | 0.03 | ph_meter, final_assay | 0.109006 | 0 | 0.0872819 | 0 |
| 7 | 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.161909 | 0.00865862 | 0.0378296 | 0 |
| 8 | 1 | 0.04 | 0.015 | ph_meter, final_assay | 0.108525 | 0.00133903 | 0.0957433 | 0.00274344 |
| 9 | 2 | 0.08 | 0.01 | ph_meter, final_assay | 0.224445 | 0 | 0 | 0.00211134 |
| 10 | 2 | 0.08 | 0.03 | ph_meter, final_assay | 0.156408 | 0.00423914 | 0.0183193 | 0.00116811 |
| 11 | 2 | 0.04 | 0.005 | ph_meter, final_assay | 0.225234 | 0.00962751 | 0 | 0 |
| 12 | 2 | 0.04 | 0.015 | ph_meter, final_assay | 0.157909 | 0.00589694 | 0.0146705 | 0 |

### Sealed evidentiary anchor

Batch `6`: Experiment 6 is the full-scale, high-loading observation for medium 1 in the matched concentration-by-scale design. It is a useful anchor because it connects directly to the medium-1 low-loading and half-scale controls and to identical high-loading conditions in media 0 and 2; this selection is for evidentiary linkage, not an optimum claim.

## K1 — sealed open mechanistic report

Mechanistic report

1. Scope and experimental design

This campaign examined a bounded synthetic weak-acid/direct-precipitation system, not general aqueous chemistry and not a prediction about real water, ethanol, or acetonitrile chemistry. The selectable medium identities are therefore treated as entity labels 0, 1, and 2 whose effects must be learned empirically.

Twelve completed batches formed a matched 3 × 2 × 2 design: three media, two nominal reagent concentrations (0.125 and 0.375 mol L^-1), and two initial liquid volumes (0.040 and 0.080 L). The assignments were:

- Medium 0: batches 1–4.
- Medium 1: batches 5–8.
- Medium 2: batches 9–12.
- At each medium, the full-scale low/high conditions used 0.010/0.030 mol in 0.080 L, and the half-scale low/high conditions used 0.005/0.015 mol in 0.040 L.

Each batch received a pre-termination pH-meter measurement and a post-termination final assay. Thus the campaign produced 12 intermediate measurements and 12 final assays with no discarded batches. Experiment 6 was selected before blind evaluation as an evidentiary anchor because it is the full-scale, high-loading medium-1 member of the matched design; that selection was not an optimization claim.

2. Observed variables and their interpretation

The chemically informative outputs were normalized pH (pH/14), acid_dissociation_fraction, precipitation_signal, and equilibrium_residual. The reported equilibrium_confidence is an environment diagnostic and is not my scientific confidence in the proposed mechanism.

I interpret the first three outputs as distinct response channels:

- pH_normalized reports proton activity on a compressed scale. For readability, pH = 14 × pH_normalized.
- acid_dissociation_fraction is a bounded effective fraction, not necessarily a thermodynamic degree of ionization sufficient by itself to reproduce the reported pH.
- precipitation_signal is a bounded proxy for solid formation rather than a calibrated precipitate amount.

The channels should not be forced into an ideal monoprotic-acid identity such as [H+] = C alpha. For example, batch 1 had C = 0.125 mol L^-1 and final alpha = 0.01368, but its final normalized pH was 0.14071 (pH about 1.970). Those quantities do not satisfy the simplest ideal dilute-acid balance. The appropriate conclusion is that medium-dependent proton activity, background acidity, activity coefficients, precipitation, and/or the synthetic definitions of the observables contribute separately.

3. Direct observations that most strongly constrain the explanation

Batch 1 was medium 0 at 0.125 mol L^-1 and 0.080 L. Its pre-termination pH-meter estimates were normalized pH 0.141923, acid dissociation 0.000000, precipitation 0.077467, residual 0.002705, and diagnostic equilibrium confidence 0.946548. Its final assay gave normalized pH 0.140713, acid dissociation 0.013681, precipitation 0.066417, residual 0.000000, and diagnostic confidence 0.961226. The two instruments therefore agreed closely on acidity and the presence of a substantial precipitation response, while the dissociation estimate differed by about 0.0137. Because the pH-meter uncertainty for dissociation was larger and its estimate was clipped at the lower bound, I do not interpret the zero as proof of zero ionization.

Batch 11 was medium 2 at 0.125 mol L^-1 and 0.040 L. Its pre-termination estimates were normalized pH 0.231687, dissociation 0.018882, precipitation 0.009495, residual 0.007224, and diagnostic confidence 0.817365. The final assay gave normalized pH 0.225234, dissociation 0.009628, precipitation 0.000000, residual 0.000000, and diagnostic confidence 0.804849. The final pH was about 3.153. The small precipitation estimates straddle the bounded zero/noise region, so the defensible statement is that precipitation was absent or weak, not that its physical amount was exactly zero.

Batch 12 was medium 2 at 0.375 mol L^-1 and 0.040 L. Its pre-termination estimates were normalized pH 0.161409, dissociation 0.003436, precipitation 0.036552, residual 0.009609, and diagnostic confidence 0.785371. Its final assay gave normalized pH 0.157909, dissociation 0.005897, precipitation 0.014670, residual 0.000000, and diagnostic confidence 0.790756. The final pH was about 2.211.

The matched medium-2 comparison between batches 11 and 12 is particularly informative. Raising nominal concentration threefold at fixed 0.040 L:

- lowered final normalized pH from 0.225234 to 0.157909, a change of -0.067325, or about -0.943 pH unit;
- lowered final dissociation fraction from 0.009628 to 0.005897;
- increased final precipitation signal from the lower bound 0.000000 to 0.014670.

This is the expected coupled signature of a weak acid whose fractional dissociation decreases as analytical concentration rises, while absolute proton activity rises and precipitation becomes more favorable.

A useful cross-medium endpoint comparison is batch 1 versus batch 11. Both used 0.125 mol L^-1, although their volumes differed by a factor of two. Medium 0 produced a much lower final normalized pH (0.140713 versus 0.225234) and a larger precipitation signal (0.066417 versus 0.000000). Its final dissociation estimate was also somewhat larger (0.013681 versus 0.009628). This agrees with the supplied qualitative endpoint mapping that selector 0 has higher ionization and solid-formation tendencies than selector 2. Because volume and medium differ in this particular pair, it is supportive rather than a clean isolated estimate of the medium effect; the full factorial was designed to resolve that confounding through the other scale pairs.

4. Proposed effective mechanism

My minimal model has a medium-conditioned acid equilibrium coupled to a concentration-dependent precipitation sink:

HA <=> H+ + A-

nu_A A- + nu_M M <=> solid

Here M represents an unspecified partner or effective precipitation capacity already present in the bounded world. I do not claim that M is a measured species.

For medium m, define an effective dissociation relation

K_a,eff(m) = a_H a_A / a_HA,

a_i = gamma_i(m,C) [i].

A mass-balance sketch is

C_T = [HA] + [A-]_aq + nu_A P,

where P is an effective precipitated amount. A threshold-like precipitation law is sufficient for the observed behavior:

P_signal = clip(g_m(SI_m(C_T,alpha,T)), 0, 1),

where SI is an effective saturation index and g_m is a monotone response function. One possible empirical form is

P_signal approximately sigmoid(a_m + b_m log C_T),

but the available observations do not identify a unique sigmoid, threshold, or exponent.

The coupled qualitative process is:

1. Increasing C_T increases proton concentration even when the fractional dissociation alpha falls.
2. The higher ionic/product activity moves the system toward the precipitation threshold.
3. Removal of dissolved ionized material into a solid can pull additional dissociation forward by mass action.
4. Conversely, changes in ionic strength and activity coefficients can suppress the apparent fractional dissociation. The measured alpha is therefore the net result of these opposing effects.

A compact entity-conditioned response model is

pH_norm = f_pH,m(C_T) + epsilon_pH,
alpha = f_alpha,m(C_T) + epsilon_alpha,
P_signal = f_P,m(C_T) + epsilon_P.

The medium identity changes the intercepts and possibly slopes or thresholds of all three functions. The evidence supports using concentration rather than total moles as the primary intensive predictor, but scale invariance should be treated as a tested empirical proposition rather than an assumed thermodynamic truth. Surface nucleation, mixing, finite sample removal, or geometry could introduce residual scale effects.

5. Entity mapping

The supplied local prior proposed the ordering 0 > 1 > 2 for both acid-ionization and solid-formation tendencies. The observed endpoint contrast between batches 1 and 11 supports the 0-versus-2 direction: medium 0 was markedly more acidic and showed substantially more precipitation at the shared nominal concentration. The medium-2 concentration series also behaves mechanistically coherently.

I do not elevate the entire three-way ordering to a universal law. Medium 1 was included in the matched experiment matrix, and batch 6 was retained as the central evidentiary anchor, but no uncited numerical value should be invented here. The safe interpretation is that the prior ordering is a hypothesis tested locally by this campaign, with the clearest directly reportable support at its two endpoints. It does not identify a real chemical property such as dielectric constant, donor number, or named electrolyte composition.

6. Measurement reconciliation and uncertainty

Across batches 1, 11, and 12, pre-termination and final normalized-pH values differed by approximately 0.0012, 0.0065, and 0.0035, respectively. These differences are small relative to the concentration and cross-medium changes. Precipitation and dissociation differed more between instruments, especially near zero. That pattern is consistent with channel-specific noise, bounded clipping, and different synthetic calibrations.

Final-assay residuals were zero in all three cited final results, whereas pH-meter residuals were small but nonzero (0.0027–0.0096). This does not prove exact thermodynamic equilibrium: it only shows internal consistency according to the environment's residual diagnostic at the measured endpoints. Likewise, the diagnostic confidence values must not be read as posterior probabilities for this report.

The strongest robust findings are therefore directional and relational:

- In medium 2, higher concentration caused lower pH, lower fractional dissociation, and a larger precipitation response.
- At 0.125 mol L^-1, medium 0 showed lower pH and more precipitation than medium 2, consistent with the supplied qualitative endpoint mapping.
- Signals close to zero are not reliably distinguishable from clipping and measurement noise.

7. Identifiability limits

The campaign does not identify microscopic species, stoichiometry, a thermodynamic pKa, a solubility product, activity coefficients, nucleation rates, or a precipitate mass. It also does not distinguish equilibrium precipitation from a rapid kinetically trapped endpoint because no time course, seeding intervention, solid isolation, or independent mass assay was performed.

Temperature was not deliberately varied, so enthalpic effects are unidentified. No catalyst was required for the reported design, and no causal catalyst mechanism is inferred. Only three local entity labels, two concentrations, and two scales were tested; extrapolation outside 0.125–0.375 mol L^-1, outside 0.040–0.080 L, or to other media is unsupported. Real-solvent names in the interface do not license translating these categorical benchmark effects into claims about real laboratory solvents.

8. Reasonable competing explanations

Several models remain observationally equivalent over this dataset:

- Medium-dependent acid equilibrium: each medium changes K_a,eff and therefore proton activity and alpha.
- Medium-dependent background acidity: the medium primarily shifts pH while the reported alpha channel responds only indirectly.
- Medium-dependent solubility: the primary entity effect is a different precipitation threshold, with dissociation shifting secondarily through removal of A-.
- Activity-coefficient model: one underlying intrinsic Ka and solubility relation could appear medium-specific because gamma_H, gamma_A, and gamma_HA vary with medium and concentration.
- Proxy-calibration model: some entity separation could arise because the bounded signals have medium-dependent response factors rather than because microscopic equilibrium constants differ.
- Kinetic/nucleation model: precipitation signals could reflect medium-dependent nucleation or settling within the fixed protocol rather than a true equilibrium solubility difference.

The present data favor a coupled, medium-conditioned effective model but cannot choose uniquely among these microscopic explanations.

9. Testable predictions, explicitly marked as extrapolations

Within the tested domain, interpolation predicts that medium 2 at a concentration between 0.125 and 0.375 mol L^-1 should have normalized pH between about 0.225 and 0.158, a dissociation fraction between about 0.0096 and 0.0059, and a weak precipitation signal between approximately zero and 0.015, subject to noise and possible threshold curvature. This is an interpolation, not an observation.

If concentration is the transferable variable, matched 0.040- and 0.080-L batches at the same medium and concentration should agree within combined process and instrument uncertainty. A systematic difference would instead implicate mixing, nucleation surface, geometry, or another extensive variable.

If precipitation is directly coupled to dissociation by removal of the ionized form, an intervention that selectively suppresses solid formation should reduce precipitation_signal and alter the apparent dissociation response at fixed medium and concentration. If pH changes but alpha and precipitation do not respond coherently, a background-acidity or proxy-calibration explanation becomes more plausible.

10. Overall conclusion

The most economical account is a medium-conditioned weak-acid equilibrium coupled to a concentration-dependent precipitation sink. Concentration controls the main within-medium direction: increasing loading raises proton activity, lowers the fractional dissociation, and promotes precipitation. Medium identity shifts both the acid response and the precipitation threshold. The observed medium-0 versus medium-2 endpoint contrast supports the supplied qualitative direction, but the data identify effective relationships rather than unique microscopic constants or real chemical identities. Claims should remain confined to the tested benchmark domain and should preserve activity-coefficient, background-acidity, calibration, and kinetic/nucleation models as viable competing explanations.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.338 | 0.278 | 0.398 |
| Q01 | acid_dissociation_fraction | 0.057 | 0.022 | 0.105 |
| Q01 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q02 | pH_normalized | 0.38 | 0.315 | 0.445 |
| Q02 | acid_dissociation_fraction | 0.049 | 0.017 | 0.095 |
| Q02 | precipitation_signal | 0.0015 | 0 | 0.02 |
| Q03 | pH_normalized | 0.423 | 0.36 | 0.486 |
| Q03 | acid_dissociation_fraction | 0.04 | 0.012 | 0.085 |
| Q03 | precipitation_signal | 0.0003 | 0 | 0.015 |
| Q04 | pH_normalized | 0.168 | 0.134 | 0.202 |
| Q04 | acid_dissociation_fraction | 0.0167 | 0.006 | 0.031 |
| Q04 | precipitation_signal | 0.043 | 0.014 | 0.079 |
| Q05 | pH_normalized | 0.21 | 0.172 | 0.248 |
| Q05 | acid_dissociation_fraction | 0.0142 | 0.0045 | 0.029 |
| Q05 | precipitation_signal | 0.023 | 0.003 | 0.055 |
| Q06 | pH_normalized | 0.253 | 0.218 | 0.288 |
| Q06 | acid_dissociation_fraction | 0.0118 | 0.003 | 0.025 |
| Q06 | precipitation_signal | 0.003 | 0 | 0.024 |
| Q07 | pH_normalized | 0.045 | 0.008 | 0.09 |
| Q07 | acid_dissociation_fraction | 0.0111 | 0.003 | 0.024 |
| Q07 | precipitation_signal | 0.319 | 0.19 | 0.47 |
| Q08 | pH_normalized | 0.087 | 0.045 | 0.135 |
| Q08 | acid_dissociation_fraction | 0.0095 | 0.002 | 0.022 |
| Q08 | precipitation_signal | 0.171 | 0.075 | 0.3 |
| Q09 | pH_normalized | 0.129 | 0.092 | 0.17 |
| Q09 | acid_dissociation_fraction | 0.0048 | 0.0005 | 0.014 |
| Q09 | precipitation_signal | 0.024 | 0 | 0.075 |
| Q10 | pH_normalized | 0.168 | 0.142 | 0.194 |
| Q10 | acid_dissociation_fraction | 0.0167 | 0.007 | 0.029 |
| Q10 | precipitation_signal | 0.043 | 0.019 | 0.072 |
| Q11 | pH_normalized | 0.21 | 0.18 | 0.24 |
| Q11 | acid_dissociation_fraction | 0.0142 | 0.0055 | 0.027 |
| Q11 | precipitation_signal | 0.023 | 0.005 | 0.049 |
| Q12 | pH_normalized | 0.253 | 0.226 | 0.28 |
| Q12 | acid_dissociation_fraction | 0.0118 | 0.0035 | 0.023 |
| Q12 | precipitation_signal | 0.003 | 0 | 0.019 |

### Q rationales

- **Q01**: Low-concentration extrapolation for selector 0. I predict relatively high ionization and the lowest normalized pH among the three entities, while precipitation should be close to the bounded baseline because the loading is far below the studied range.

- **Q02**: Selector 1 is treated as intermediate between selectors 0 and 2. The very low concentration is an extrapolation, so the interval includes substantial uncertainty in both the entity offset and the concentration dependence.

- **Q03**: The selector-2 model predicts the highest normalized pH and weakest precipitation tendency. The dissociation estimate follows extrapolation of the observed decline in fractional dissociation with increasing concentration.

- **Q04**: This is a modest extrapolation below the studied concentration range and below the studied scale. Selector 0 is predicted to retain a comparatively acidic response and appreciable precipitation, with extra interval width for possible small-volume effects.

- **Q05**: The point estimate interpolates the entity effect between selectors 0 and 2. Concentration is assumed to be the principal intensive control, but the 0.024 L scale lies outside the campaign range and broadens the interval.

- **Q06**: Selector 2 is predicted to remain less acidic and less precipitation-prone than selectors 0 and 1. The precipitation interval includes zero because nearby selector-2 observations were at the lower bound.

- **Q07**: High-concentration extrapolation for the most acidic and precipitation-prone entity. I expect lower fractional dissociation but much greater absolute proton activity and precipitation; uncertainty is dominated by unknown threshold curvature or saturation.

- **Q08**: Selector 1 is assigned an intermediate entity offset at high loading. The wide precipitation interval allows both a near-linear concentration response and a sharper medium-specific threshold.

- **Q09**: Extrapolation of the selector-2 concentration series predicts increased acidity, reduced fractional dissociation, and only weak precipitation. The interval remains compatible with a delayed precipitation threshold.

- **Q10**: This shares concentration and entity with Q04 but uses a scale inside the campaign range. Under the concentration-transfer hypothesis it has the same point estimate, with a narrower interval because 0.048 L is supported by the scale study.

- **Q11**: The response is predicted to be scale-invariant at fixed concentration to first order. Selector 1 retains the intermediate entity effect; the interval allows residual mixing or nucleation-scale dependence.

- **Q12**: At the supported 0.048 L scale, selector 2 is predicted to give the highest normalized pH and a precipitation response at or near the lower bound. The interval includes small positive signals caused by process and assay variability.

Shared rationale:

Predictions use an entity-conditioned concentration-response model derived from the completed 3-by-2-by-2 campaign. Normalized pH was modeled as approximately linear in log concentration; fractional dissociation was modeled as decreasing with concentration; and precipitation was treated as a nonnegative, medium-dependent response that rises with loading. Selector 0 was assigned the strongest acid/precipitation response, selector 2 the weakest, and selector 1 an intermediate response. Equal-concentration scale controls share point estimates because concentration is the proposed transferable variable. Intervals combine final-assay noise with substantially larger model uncertainty, especially at 0.005 and 0.6 M and at the unstudied 0.024 L scale.

## K2 — sealed seven-part retrospective

1. Initial claims: supported, contradicted, or untested

The initial material packet contained one substantive mechanistic prior: selector 0 was described as having higher acid-ionization and solid-formation tendencies, selector 1 as intermediate, and selector 2 as lower. It explicitly limited that statement to a qualitative local mapping and did not supply a quantitative property dossier, microscopic species identities, equilibrium constants, or a complete mechanism.

The clearest support concerned solid formation at the endpoint. In batch 1, selector 0 at 0.125 M and 0.080 L gave a final precipitation signal of 0.066417. In batch 11, selector 2 at the same nominal concentration but 0.040 L gave a final signal at the lower bound, 0.000000. This supported the predicted selector-0-versus-selector-2 direction, although volume was confounded in that particular comparison. Batch 12 also showed that selector 2 was not categorically incapable of precipitation: at 0.375 M and 0.040 L its final signal rose to 0.014670.

The acid-ionization claim received weaker and mixed support. Final-assay dissociation was 0.013681 in batch 1 and 0.009628 in batch 11, which agreed with the proposed endpoint ordering. However, the pre-termination pH-meter estimates went in the opposite direction: 0.000000 in batch 1 versus 0.018882 in batch 11. That is genuine contrary evidence, not merely an absence of support. In K1 I did not revise the ordering because the batch-1 value was clipped at zero, the pH-meter dissociation channel had greater uncertainty, and the final assay favored the prior direction. Nevertheless, K1 should have stated more prominently that the ionization ordering was instrument-sensitive rather than simply “supported.”

The pH observations supported a strong entity-conditioned response but did not directly prove an ionization ordering. Batch 1 had final normalized pH 0.140713, whereas batch 11 had 0.225234. Calling the former “more acidic” is justified; treating that difference as a direct measurement of intrinsic Ka is not.

The claim that selector 1 is intermediate remained insufficiently tested in the written K1 analysis. Selector-1 batches were performed, but K1 did not cite their numerical outcomes. My later predictions therefore imposed an intermediate selector-1 response more strongly than the documented analysis warranted.

The material packet also warned that the displayed solvent names represented bounded categorical benchmark effects rather than predictions derived from real-solvent properties. Nothing in the campaign contradicted that warning, but it was a scope condition rather than an experimentally tested chemical claim. No evidence identified real solvent parameters, named precipitates, or microscopic species.

2. Experiments that formed or changed my judgment

Batch 1 established the first concrete response pattern: low normalized pH, a clearly positive precipitation signal, a small final dissociation fraction, and close pre/final agreement in pH. It made a coupled acid/precipitation account plausible, but by itself could not distinguish a medium effect from a generic concentration response.

Batch 11 supplied the most useful low-loading selector-2 contrast. Relative to batch 1 it had higher normalized pH and much weaker final precipitation. This comparison led me to retain the supplied selector-0-versus-selector-2 qualitative direction. Because scale differed, it should have been treated as provisional until the matched scale pairs were analyzed.

Batch 12, compared directly with batch 11 at the same selector and volume, most clearly changed the mechanistic interpretation. Increasing selector-2 concentration from 0.125 to 0.375 M lowered final normalized pH from 0.225234 to 0.157909, lowered the final dissociation fraction from 0.009628 to 0.005897, and raised precipitation from 0.000000 to 0.014670. This made the following joint explanation substantially more credible: increasing analytical concentration can increase proton activity while decreasing fractional dissociation and promoting precipitation.

The pre/final comparisons also affected my interpretation. Batch 1 changed from pH-meter precipitation 0.077467 to final-assay 0.066417; batch 11 changed from 0.009495 to 0.000000; and batch 12 changed from 0.036552 to 0.014670. These discrepancies made me treat small precipitation signals and bounded zeros as noisy rather than literal amounts.

The overall 3 × 2 × 2 design was chosen before seeing results. Its two concentrations and two scales were motivated by the research goal of testing transfer across concentration and scale. Its entity ordering was substantially motivated by the supplied qualitative prior. The assumption that concentration would be the primary transferable variable was initially an unverified mechanistic guess. The decision to use one pH-meter measurement followed by a final assay in every batch was a design choice for consistent cross-batch comparison, not a result-driven adaptation.

The selection of experiment 6 as the sealed recommendation did not arise from evidence that it was optimal. It was chosen because the full-scale, high-loading selector-1 condition occupied a useful linking position in the factorial design. That was a design-centrality argument based partly on the initial intermediate-entity hypothesis, not a demonstrated mechanistic superiority.

3. Most important competing mechanisms

The leading effective explanation remains a medium-conditioned weak-acid response coupled to a concentration-dependent precipitation sink. It accounts qualitatively for the batch-11-to-batch-12 pattern and the selector-0-versus-selector-2 endpoint contrast.

Several competing explanations remain viable:

- Intrinsic-equilibrium model: selectors alter effective acid dissociation constants and solubility thresholds.
- Activity-coefficient model: the underlying intrinsic constants are common, but medium- and concentration-dependent activities produce different apparent pH, dissociation, and precipitation responses.
- Background-acidity model: much of the pH separation comes from the medium itself, while the reported dissociation channel changes only indirectly.
- Precipitation-first coupling: selectors mainly alter solubility or nucleation; removal of dissolved ionized material then shifts apparent dissociation.
- Kinetic/nucleation model: precipitation signals reflect different nucleation or settling rates within the protocol rather than equilibrium solubility.
- Channel-calibration model: part of the selector separation or the pre/final discrepancy arises from entity-dependent proxy response factors.

The existing experiments can distinguish a simple concentration-independent response from a concentration-coupled one: batches 11 and 12 clearly changed with concentration. They also disfavor the claim that selector 2 can never precipitate, because batch 12 had a positive final signal.

They cannot uniquely separate intrinsic Ka changes from activity-coefficient or background-acidity effects. They cannot determine whether precipitation causes additional dissociation or merely co-varies with concentration. They also cannot discriminate equilibrium precipitation from rapid kinetic trapping because no deliberate time, seeding, or mixing intervention was included. Final residuals of zero show consistency with the environment diagnostic, not proof of thermodynamic equilibrium.

4. One additional legal complete experiment

If exactly one additional experiment were permitted, I would repeat the selector-0, 0.125 M, 0.040 L condition but introduce a deliberate waiting period at controlled stirring before termination. The recipe would use 0.040 L of selector-0 medium and 0.005 mol reagent. I would purchase a pH-meter measurement soon after mixing, wait for a long prespecified duration at constant temperature and stirring, obtain a second pH-meter measurement if the legal resource card allowed it, then terminate and obtain the required final assay. If only one intermediate measurement were legal, I would place it after the wait and compare the final result with the existing no-wait matched condition.

This condition is preferable to another concentration point because selector 0 already showed a clearly positive precipitation response, making time dependence observable, while 0.125 M avoids the strongest extrapolation or safety concerns.

Possible interpretations would be:

- Stable pH, dissociation, and precipitation after waiting would support a rapid effective-equilibrium interpretation, while not proving equilibrium.
- Increasing precipitation with a coordinated pH or dissociation shift would support kinetic nucleation followed by coupling to acid speciation.
- Increasing precipitation without a coherent acid-response shift would favor a precipitation or settling process weakly coupled to the reported dissociation channel.
- A large pH shift with nearly unchanged precipitation would strengthen the background-acidity, activity-relaxation, or sensor-equilibration explanations.
- A materially different replicate even without a directional time effect would reveal process variability larger than assumed and would require wider predictive intervals.

This is a proposed discriminating experiment only; it has not been performed.

5. Trade-off between mechanistic identifiability and operational score

The design prioritized mechanistic coverage over score maximization. All three selectors were examined at two concentrations and two scales even though early data could have encouraged repeated use of a higher-scoring region. For example, batch 1 had a reported final score of about 0.4593, whereas batches 11 and 12 had about 0.3866 and 0.3750. Continuing to study selector 2 and high loading sacrificed likely operational score in exchange for concentration-response and entity-contrast information.

The design also avoided catalysts, heating, or adaptive optimization because the stated objective was entity mapping and mechanism characterization rather than finding the highest scalar score. That was appropriate: the score placed substantial weight on the environment’s equilibrium-confidence diagnostic, which was explicitly not the scientific objective or my epistemic confidence.

There were nevertheless identifiability sacrifices. Allocating one intermediate measurement and one final assay uniformly to every batch provided consistent replication across the matrix, but left no budget for time courses, seeding, temperature variation, or repeated measurements at a single condition. The 3 × 2 × 2 matrix estimated broad entity, concentration, and scale relationships but was too sparse to identify threshold curvature or interaction terms reliably.

No condition was chosen solely to maximize score. Conversely, several conditions—particularly the selector-2 and high-concentration cells—were retained despite lower diagnostic scores because they were needed for identification. The main design weakness was not optimization pressure but excessive breadth relative to the available number of observations.

6. Underused evidence and reliability of the blind predictions

K1 did not make adequate quantitative use of batches 2–10. Although those experiments were completed, the report’s numerical argument relied mainly on batches 1, 11, and 12. This prevented a full analysis of the matched scale pairs and left the selector-1 ordering under-supported in the written record. The raw multichannel final-assay artifacts were also not analyzed beyond their processed estimates. Consequently, possible spectral evidence about channel consistency, clipping, or calibration was not exploited.

The pH-meter/final-assay discrepancies were acknowledged but not modeled quantitatively. In particular, the contrary pre-assay dissociation ordering between batches 1 and 11 should have contributed more structural uncertainty. Likewise, the absence of deliberate waiting made all equilibrium language conditional, yet the prediction model treated concentration-response functions as if they were stable endpoints.

The least reliable blind predictions are:

- Q01–Q03 at 0.005 M, because they extrapolate 25-fold below the lowest studied concentration.
- Q07–Q09 at 0.6 M, because they extrapolate beyond the studied maximum and require assumptions about precipitation threshold curvature and saturation.
- All selector-1 predictions, especially Q02 and Q08, because I imposed an intermediate response without presenting the underlying selector-1 numerical evidence in K1.
- Q04–Q09 at 0.024 L, because that scale lies below the 0.040–0.080 L campaign range.

Q07 is particularly fragile. Its predicted normalized pH of 0.045 and precipitation signal of 0.319 came from extending a log-concentration pH relation and an approximately rising precipitation relation well outside direct support. The associated intervals, 0.008–0.090 and 0.190–0.470, may still be too narrow because alternative threshold or saturation models could yield substantially different results.

The low-concentration dissociation predictions may also have intervals that are too narrow. For example, Q01 predicted 0.057 with an 80% interval of 0.022–0.105. That interval reflected extrapolation uncertainty but did not fully represent disagreement between the pH-meter and final-assay dissociation channels.

For Q10–Q12 I assigned identical point estimates to their 0.024 L counterparts because I assumed concentration transfer. That was a strong modeling decision. The intervals for the 0.048 L scale controls were narrower because that scale was within the studied range, but they may be overconfident if nucleation surface, mixing, or total solid amount creates scale dependence.

These limitations are consistent with K1’s explicit statement that extrapolation outside 0.125–0.375 M and 0.040–0.080 L was unsupported. The predictions did label the extreme conditions as extrapolations, but their numerical precision arguably exceeded that warning. K1 also retained activity, calibration, and kinetic explanations; the prediction model simplified those competing mechanisms into single concentration-response curves. That simplification was useful for producing point estimates but understated structural uncertainty.

No prediction truth has been supplied, so none of these comments is a retrospective fit to hidden outcomes. They are an audit of assumptions visible before scoring.

7. Limitations of the sealed recommendation

The sealed recommendation selected completed experiment 6 as an evidentiary anchor. Its main limitation is that design centrality is not the same as repeatability, robustness, or optimality. A single completed batch cannot establish any of those properties.

Experiment 6 was not selected because it was demonstrated to have the highest sample score. Even if it had been the highest among the 12 observed batches, that would establish only a sample-in-matrix maximum. It would not prove a continuous optimum over concentration, volume, mixing, time, temperature, or untested materials. In fact, the rationale explicitly stated that the selection was “for evidentiary linkage, not an optimum claim.”

Repeatability would require independent exact replicates of experiment 6 from the same initial world, with the distribution of pH, dissociation, precipitation, residual, and diagnostic score reported rather than only a single endpoint. Pre/final instrument agreement should also be evaluated across replicates.

Local robustness would require a prespecified neighborhood around experiment 6: small upward and downward changes in concentration, volume, wait time, and mixing, while holding selector identity fixed. A robust recommendation should retain its qualitative response and acceptable variability across that neighborhood rather than depend on one exact recipe.

Cross-material transfer would require applying the same concentration-and-scale logic to selectors 0 and 2 and estimating entity-by-condition interactions. The existing factorial was intended to begin that test, but the sealed selection itself supplies no proof of transfer.

Cross-world generalization would require repetitions under independently initialized benchmark worlds or seeds. Such tests would reveal whether experiment 6 is tied to one realization of process noise or to a stable structural relationship. Generalization to real materials would require an entirely separate empirical calibration and cannot be inferred from this synthetic categorical benchmark.

Accordingly, experiment 6 should be regarded as a useful reference node in the completed design—not as a proven optimum, universally transferable recipe, or validated operating recommendation.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0475653 | 0.666667 | 0.0838333 | 0.259334 |
| acid_dissociation_fraction | 0.0128961 | 0.716667 | 0.03525 | 0.0724798 |
| precipitation_signal | 0.0308533 | 0.9 | 0.07475 | 0.168956 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0320521 |
| 0.08 | 0.00987381 |
| 0.6 | 0.0668059 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00081806 |
| 1 | 0.00265173 |
| 2 | 0.00145168 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
