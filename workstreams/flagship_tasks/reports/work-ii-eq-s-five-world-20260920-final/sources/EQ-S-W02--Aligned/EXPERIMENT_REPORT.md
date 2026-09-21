# EQ-S-W02--Aligned — final English experiment report

World `EQ-S-W02`; information arm `Aligned`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 72 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.02 | 0.005 | ph_meter, final_assay | 0.121744 | 0 | 0 | 0 |
| 2 | 0.04 | 0.005 | ph_meter, final_assay | 0.141307 | 0.00153829 | 0.0093379 | 0.00119764 |
| 3 | 0.06 | 0.005 | ph_meter, final_assay | 0.158588 | 0.00545865 | 0 | 0 |
| 4 | 0.08 | 0.005 | ph_meter, final_assay | 0.163627 | 0 | 0.00871064 | 0 |
| 5 | 0.02 | 0.02 | ph_meter, final_assay | 0.0733352 | 0 | 0.0581407 | 0 |
| 6 | 0.04 | 0.02 | ph_meter, final_assay | 0.102281 | 0 | 0.00835322 | 0.000255394 |
| 7 | 0.06 | 0.02 | ph_meter, final_assay | 0.114944 | 0 | 0.00940091 | 0.00357884 |
| 8 | 0.08 | 0.02 | ph_meter, final_assay | 0.119523 | 0 | 0 | 0.00733996 |
| 9 | 0.02 | 0.035 | ph_meter, final_assay | 0.0486177 | 0.0021439 | 0.0835044 | 0.00379147 |
| 10 | 0.04 | 0.035 | ph_meter, final_assay | 0.0737681 | 0.00141844 | 0.050919 | 0.00238089 |
| 11 | 0.06 | 0.035 | ph_meter, final_assay | 0.0955474 | 0.00584671 | 0.0202351 | 0 |
| 12 | 0.08 | 0.035 | ph_meter, final_assay | 0.104694 | 0.00826818 | 0 | 0.00361943 |

### Sealed evidentiary anchor

Batch `9`: Batch 9 is a useful high-loading, low-volume anchor: it gives the clearest nonzero precipitation response alongside the most acidic pH endpoint, bounding the factorial concentration trend rather than claiming an optimum.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

Scope and study design

The campaign comprised 12 completed aqueous batches in a 3 × 4 factorial design. Anonymous reagent loading was 0.005, 0.020, or 0.035 mol; water volume was 0.020, 0.040, 0.060, or 0.080 L. Every batch also received 0.003 mol of Catalyst A. Thus the nominal reagent concentration C_R = n_R/V ranged from 0.0625 to 1.75 mol L^-1. Conditions were otherwise approximately ambient, near 297 K. No temperature, time, solvent-identity, catalyst-identity, or catalyst-loading series was performed. Each batch received one pre-termination pH-meter measurement and one post-termination final assay.

The selected evidentiary anchor was batch 9, containing 0.035 mol reagent in 0.020 L water. It was selected because it is the high-loading, low-volume boundary and produced the clearest precipitation response and lowest normalized pH. It is an evidentiary boundary point, not an optimized process.

OBSERVATIONS

1. Normalized pH was governed primarily by reagent concentration.

The final-assay normalized-pH values fell monotonically as concentration increased, apart from only small scatter:

• At 0.020 L, raising reagent loading from 0.005 to 0.020 to 0.035 mol changed normalized pH from 0.12174 in batch 1 to 0.07334 in batch 5 and 0.04862 in batch 9.
• At 0.040 L, the corresponding values were 0.14131 in batch 2, 0.10228 in batch 6, and 0.07377 in batch 10.
• At 0.060 L, they were 0.15859 in batch 3, 0.11494 in batch 7, and 0.09555 in batch 11.
• At 0.080 L, they were 0.16363 in batch 4, 0.11952 in batch 8, and 0.10469 in batch 12.

Dilution at fixed loading produced the complementary response. For example, diluting 0.035 mol from 0.020 to 0.080 L raised normalized pH from 0.04862 in batch 9 to 0.10469 in batch 12. For 0.020 mol, the same dilution raised it from 0.07334 in batch 5 to 0.11952 in batch 8.

A useful descriptive interpolation of all 12 final-assay observations is

pH_normalized ≈ 0.07345 - 0.03400 ln(C_R / 1 mol L^-1).

Equivalently, because pH_normalized = pH/14,

pH ≈ 1.028 - 0.476 ln(C_R / 1 mol L^-1)
   ≈ 1.028 - 1.096 log10(C_R / 1 mol L^-1).

The root-mean-square residual of this descriptive fit is approximately 0.0036 normalized-pH units, or about 0.050 pH unit. This fit is empirical and local; it is not itself an equilibrium law.

A particularly informative concentration match is provided by batches 1 and 8. Both had C_R = 0.25 mol L^-1, despite differing fourfold in both reagent amount and water volume. Their final normalized pH values were 0.12174 and 0.11952. Catalyst concentration and catalyst-to-reagent ratio also differed between these batches, so this close agreement indicates that nominal reagent concentration was the dominant pH coordinate under the tested conditions. It does not prove that catalyst concentration has no effect.

2. The precipitation proxy rose mainly at the concentrated boundary.

The clearest final-assay signals were 0.08350 in batch 9 at 1.75 mol L^-1, 0.05814 in batch 5 at 1.00 mol L^-1, 0.05092 in batch 10 at 0.875 mol L^-1, and 0.02024 in batch 11 at 0.583 mol L^-1. Batch 6 at 0.50 mol L^-1 gave 0.00835, while batch 12 at 0.4375 mol L^-1 was at zero. At concentrations at or below 0.333 mol L^-1, all final signals lay between zero and 0.00940.

The dilution response was clearest at high loading: batches 9–12, all containing 0.035 mol reagent, gave precipitation signals of 0.08350, 0.05092, 0.02024, and 0 as water volume increased from 0.020 to 0.080 L. For 0.020 mol, batches 5–8 declined from 0.05814 at 0.020 L to zero at 0.080 L, although intermediate values contained floor-level scatter. The low-loading series, batches 1–4, remained at or near the floor and did not show a resolvable monotonic trend.

These results support a concentration-dependent onset region roughly around 0.4–0.6 mol L^-1, but the signal is a bounded proxy rather than a measured solid amount. Consequently, neither a sharp solubility boundary nor a precipitation yield can be extracted.

3. The free acid-dissociation-fraction channel was mostly floor-censored and weakly informative.

Final-assay fractions were zero in 6 of 12 batches and ranged only from zero to 0.00827; their overall mean was about 0.00206. The nonzero final values were 0.00154 in batch 2, 0.00546 in batch 3, 0.00214 in batch 9, 0.00142 in batch 10, 0.00585 in batch 11, and 0.00827 in batch 12. These values are comparable to the declared final-assay noise scale of 0.006, and zero is a physical reporting bound. A quantitative dissociation curve therefore cannot be identified from the final assays.

The pre-termination pH-meter estimates were more often positive at low loading: batches 1–4 gave fractions from 0.01478 to 0.02385, whereas batches 9–12 gave 0 to 0.00356. This is qualitatively compatible with a larger fractional dissociation upon dilution or reduced loading. However, the pH-meter fraction noise scale was 0.015, and the paired final assays did not consistently reproduce those magnitudes. The defensible conclusion is only that the fraction is small throughout this tested slice and may increase toward dilute conditions. Its exact functional dependence is not resolved.

4. Instrument diagnostics do not replace scientific uncertainty.

Final equilibrium residuals ranged from zero to 0.00734, and final equilibrium-confidence values ranged approximately from 0.635 to 0.704. Equilibrium confidence is an environment diagnostic, not my confidence in the mechanism. The low residual values indicate internally well-behaved reported states, but they do not establish that a particular molecular topology is uniquely correct.

PLAUSIBLE UNIFIED EQUILIBRIUM NETWORK

The supplied qualitative structural account proposed the following network:

HA(aq) ⇌ H+(aq) + A-(aq)
M+(aq) + A-(aq) ⇌ MA(aq)
M+(aq) + A-(aq) ⇌ MA(s)

A thermodynamic representation is

K_a = a_H a_A / a_HA,
β_MA = a_MA / (a_M a_A),
K_sp = a_M a_A when solid MA is present,
K_w = a_H a_OH.

Here activities, rather than concentrations, are required at the upper end of the tested concentration range. If the anonymous reagent supplies the acid family and Catalyst A supplies or controls the M family, illustrative total balances are

C_A,T = [HA] + [A-] + [MA(aq)] + S,
C_M,T = [M+] + [MA(aq)] + S,

where S is precipitated MA expressed per solution-volume basis. The dossier's stated dissolved-acid balance is the corresponding balance without the solid term:

n_A,dissolved = n_HA + n_A- + n_MA(aq).

An electroneutrality equation must also include H+, A-, OH-, M+, and the unreported counterions associated with the anonymous formulations. Because those counterions were not observed, a unique charge-balance calculation cannot be completed.

This network gives a coherent qualitative explanation of all three channels. Increasing C_R raises hydrogen activity and lowers pH. For a weak acid, fractional dissociation generally becomes smaller at greater analytical concentration, consistent in direction with the tentative fraction data. Simultaneously, greater A-family and M-family activities increase the ion product a_M a_A, generating a larger precipitation proxy. Binding or precipitation removes free A-, so acid dissociation, ion pairing, and solid formation are coupled rather than independent outputs.

The observed pH relation is closer to an approximately unit slope in pH versus -log10 C_R than to the ideal one-half slope expected for a simple dilute monoprotic weak acid with constant K_a. That difference does not by itself falsify the network. Possible causes inside the same broad topology include activity-coefficient changes, formulation counterions, concentration-dependent ion pairing, precipitation coupling, or an effective mixture of acid sources. It does mean that an ideal-dilute HA-only equation is inadequate across the full 0.0625–1.75 mol L^-1 interval.

CAN ONE NETWORK EXPLAIN ALL THREE CHANNELS?

Yes, one coupled acid-dissociation/association/precipitation network can explain the directions of all three responses: concentration lowers normalized pH, tends to suppress the free dissociation fraction, and increases the precipitation proxy. The strong concentration collapse of pH and the high-concentration rise of the precipitation signal make this a parsimonious account.

However, the campaign demonstrates adequacy, not uniqueness. The dissociation-fraction channel is too close to its lower bound to provide an independent, quantitative constraint on the network. Thus the evidence does not prove that the three channels arise from the proposed species graph rather than from another graph with the same effective concentration response.

TOPOLOGY CLAIM VERSUS PARAMETER REFITTING

A topology claim concerns which states and edges exist: whether there is a free acid equilibrium, a distinct dissolved MA intermediate, and a solid MA branch. Parameter refitting within that topology changes K_a, β_MA, K_sp, activity coefficients, and the scale or threshold mapping from solid amount or supersaturation to the public proxy. Such refitting can shift curves while retaining the same species graph.

The data support the broad topology of an acid response coupled to a concentration-activated precipitation branch. They do not identify the distinct aqueous MA intermediate. Removing MA(aq) and refitting an effective K_sp could reproduce the measured channels. Conversely, retaining MA(aq) and changing β_MA could also reproduce them. Those are different topology choices, not merely different constants, but they are observationally equivalent with the present measurements. No species-resolved assay, independent M-loading series, or direct solid quantification was available to distinguish them.

HOW THE EXPERIMENTS FORMED AND REVISED THE ACCOUNT

The initial qualitative world model suggested HA dissociation plus dissolved and solid M–A branches. The loading series at each fixed volume—especially batches 1, 5, and 9—established that pH acidity and the precipitation proxy both increased strongly with loading. The dilution series at fixed loading—especially batches 9–12—showed that those effects reversed continuously with added water. These two orthogonal manipulations supported concentration, rather than reagent amount or volume alone, as the main state variable.

The matched-concentration comparison between batches 1 and 8 strengthened that conclusion because their pH values nearly coincided despite different total amounts. The high-loading dilution series supported a precipitation branch. By contrast, the numerous zero and near-zero dissociation-fraction results forced a revision in evidentiary strength: the campaign cannot supply a numerical K_a or a resolved fraction law, even though a weak-acid interpretation remains plausible.

DOSSIER ASSESSMENT

A qualitative initial world model was supplied: HA dissociation, a distinct aqueous MA intermediate, and an MA solid branch. No task-specific nominal property dossier was supplied, and no numerical instance prior was supplied; the public prior record was null.

The supplied model was supported at the family level by the coordinated pH and precipitation responses to loading and dilution. It was not contradicted by any clear observation. It was revised in evidentiary status because the distinct aqueous intermediate was left untested, the free-fraction response was poorly resolved, and ideal-dilute behavior was insufficient for the concentrated range. No equilibrium constants from the model could be confirmed or refitted uniquely.

SUPPORTED INTERPOLATION

Within water, Catalyst A at 0.003 mol, approximately 297 K, reagent loadings of 0.005–0.035 mol, volumes of 0.020–0.080 L, and C_R of 0.0625–1.75 mol L^-1, interpolation of normalized pH using the stated logarithmic empirical relation is supported. A rising precipitation proxy above roughly 0.4–0.6 mol L^-1 is also supported qualitatively, with substantial floor uncertainty near the onset. Only a small, poorly resolved free dissociation fraction is supported.

EXTRAPOLATION

Behavior outside the measured loading, volume, or concentration ranges is untested. In particular, the logarithmic pH relation must not be extended to zero concentration or arbitrarily high concentration. The proxy cannot be assumed to keep increasing, to represent a fixed solid yield, or to possess a universal threshold. Responses for other catalysts, catalyst amounts, solvents, temperatures, pressures, waiting times, or mixing histories are unknown.

CONJECTURE AND UNIDENTIFIABLE FACTORS

The assignments of the anonymous reagent to HA and Catalyst A to an M source are mechanistic conjectures, not measured identities. Unidentifiable quantities include K_a, β_MA, K_sp, activity coefficients, counterion concentrations, actual dissolved and solid species amounts, solid stoichiometry, nucleation kinetics, and the transfer function relating precipitation to its public proxy. The experiment also cannot distinguish true equilibrium from a fast, reproducible operational endpoint because no time course or waiting-time perturbation was performed.

REASONABLE COMPETING EXPLANATIONS

1. Direct precipitation without a distinct aqueous intermediate: HA dissociation followed by M+ + A- ⇌ MA(s) could reproduce the observed channels after refitting effective constants.
2. Ion pairing without actual bulk precipitation: the public precipitation signal could track supersaturation or aggregation while little macroscopic solid forms.
3. A formulation-driven acidity model: unreported catalyst counterions or formulation acidity could dominate pH, while reagent concentration independently controls the precipitation proxy.
4. A concentration-dependent effective acid model: strong nonideality or multiple unresolved acid states could generate the near-unit pH/log-concentration slope without the proposed MA(aq) state.
5. A purely empirical common-coordinate model: all three channels could be different response functions of C_R, with no uniquely inferable molecular coupling. This is less mechanistically informative but cannot be rejected by the available observables.

Overall conclusion

The strongest defensible result is a local, concentration-controlled aqueous response. Across 0.0625–1.75 mol L^-1, normalized pH follows a tight logarithmic decline with reagent concentration, while the precipitation proxy becomes appreciable toward the concentrated end. The free acid-dissociation fraction remains near its lower bound and is not quantitatively identifiable. A coupled HA dissociation, M–A association, and MA precipitation network explains the three channels parsimoniously, but only its broad family is supported. The distinct aqueous MA intermediate, equilibrium constants, species identities, and direct amount of solid remain unconfirmed, and several simpler or differently parameterized networks are observationally equivalent over this campaign.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.259 | 0.22 | 0.32 |
| Q01 | acid_dissociation_fraction | 0.562 | 0.3 | 0.82 |
| Q01 | precipitation_signal | 0.002 | 0 | 0.012 |
| Q02 | pH_normalized | 0.215 | 0.18 | 0.25 |
| Q02 | acid_dissociation_fraction | 0.235 | 0.08 | 0.42 |
| Q02 | precipitation_signal | 0.002 | 0 | 0.012 |
| Q03 | pH_normalized | 0.185 | 0.16 | 0.22 |
| Q03 | acid_dissociation_fraction | 0.104 | 0.02 | 0.2 |
| Q03 | precipitation_signal | 0.002 | 0 | 0.014 |
| Q04 | pH_normalized | 0.159 | 0.135 | 0.181 |
| Q04 | acid_dissociation_fraction | 0.048 | 0 | 0.11 |
| Q04 | precipitation_signal | 0.003 | 0 | 0.02 |
| Q05 | pH_normalized | 0.137 | 0.1 | 0.162 |
| Q05 | acid_dissociation_fraction | 0.024 | 0 | 0.07 |
| Q05 | precipitation_signal | 0.006 | 0 | 0.045 |
| Q06 | pH_normalized | 0.123 | 0.06 | 0.15 |
| Q06 | acid_dissociation_fraction | 0.015 | 0 | 0.06 |
| Q06 | precipitation_signal | 0.018 | 0 | 0.08 |
| Q07 | pH_normalized | 0.137 | 0.095 | 0.17 |
| Q07 | acid_dissociation_fraction | 0.024 | 0 | 0.08 |
| Q07 | precipitation_signal | 0.006 | 0 | 0.05 |
| Q08 | pH_normalized | 0.154 | 0.132 | 0.178 |
| Q08 | acid_dissociation_fraction | 0.042 | 0 | 0.1 |
| Q08 | precipitation_signal | 0.003 | 0 | 0.022 |
| Q09 | pH_normalized | 0.17 | 0.151 | 0.19 |
| Q09 | acid_dissociation_fraction | 0.067 | 0.025 | 0.13 |
| Q09 | precipitation_signal | 0.002 | 0 | 0.014 |
| Q10 | pH_normalized | 0.177 | 0.156 | 0.2 |
| Q10 | acid_dissociation_fraction | 0.083 | 0.035 | 0.15 |
| Q10 | precipitation_signal | 0.002 | 0 | 0.013 |
| Q11 | pH_normalized | 0.185 | 0.155 | 0.22 |
| Q11 | acid_dissociation_fraction | 0.104 | 0.015 | 0.22 |
| Q11 | precipitation_signal | 0.002 | 0 | 0.015 |
| Q12 | pH_normalized | 0.185 | 0.162 | 0.21 |
| Q12 | acid_dissociation_fraction | 0.104 | 0.025 | 0.2 |
| Q12 | precipitation_signal | 0.002 | 0 | 0.014 |

### Q rationales

- **Q01**: This is far below the experimentally covered concentration range. A weak-acid limiting calculation predicts substantial fractional dissociation and a normalized pH near 0.26. The interval is wide because the low-concentration asymptote was not observed and no Catalyst A is present. With no introduced M-bearing catalyst, the precipitation branch should remain inactive; the small point estimate represents bounded assay-floor noise.

- **Q02**: At 0.00417 M the prediction remains an extrapolation below the measured range, but weak-acid mass action implies less fractional dissociation than Q01 and greater acidity. The absence of Catalyst A favors negligible association-driven precipitation. Parameter and topology uncertainty, rather than final-assay noise alone, determines the broad fraction interval.

- **Q03**: The concentration is still below the observed 0.0625 M boundary, although only by a factor of 2.5. Weak-acid mass action gives roughly 10% free dissociation and normalized pH near 0.185. Precipitation is expected to remain at the assay floor, but the interval allows uncertainty about whether the anonymous reagent itself supplies a small amount of the association partner.

- **Q04**: The 0.125 M concentration is directly represented by batch 2, whose catalyst-containing final assay gave normalized pH 0.14131 and precipitation signal 0.00934. Removing Catalyst A should weaken anion sequestration, increase the free dissociation fraction, raise pH somewhat, and reduce precipitation. The interval includes the catalyst-containing response because the identity of the M source was not established.

- **Q05**: At 0.5 M, batch 6 with Catalyst A gave normalized pH 0.10228 and precipitation signal 0.00835. The no-catalyst weak-acid projection is less acidic, near 0.137 normalized pH, with a small free fraction. A low precipitation point is assigned because the proposed solid branch requires an M partner, while the wide upper bound covers the competing possibility that M is endogenous to the anonymous formulation.

- **Q06**: The concentration lies inside the campaign's concentration span but near its upper boundary and uses no catalyst. Weak-acid mass action predicts a small free fraction and normalized pH near 0.123. This is the most topology-sensitive prediction: if Catalyst A supplied M, precipitation should be weak; if M is inherent to the reagent system, interpolation from batches 5, 9, 10, and 11 permits a much larger precipitation response. The interval covers both accounts.

- **Q07**: This has the same 0.5 M analytical concentration as Q05, so a concentration-controlled equilibrium gives the same point estimates. Its 0.006 L scale is below the 0.020 L minimum used in the campaign, so its intervals are wider. Agreement of Q05 and Q07 would support concentration rather than absolute amount as the controlling coordinate.

- **Q08**: At 0.1667 M this condition lies within the observed concentration range but between tested grid points. The weak-acid projection gives about 4% free dissociation. The K1 concentration trend supports normalized pH in the mid-0.15 range. Without Catalyst A, precipitation should be near its floor, although the interval allows a weak association response around the proposed transition region.

- **Q09**: The 0.0625 M concentration equals the lowest campaign concentration, represented by batch 4. That catalyst-containing batch gave normalized pH 0.16363 and precipitation signal 0.00871. The no-catalyst calculation predicts slightly higher pH and a resolvable free fraction, while precipitation remains effectively at the floor.

- **Q10**: This is a modest extrapolation below the campaign's concentration boundary but uses a tested-scale volume. Further dilution should raise both normalized pH and the free dissociation fraction relative to Q09. The precipitation branch should remain inactive apart from bounded measurement noise.

- **Q11**: The equilibrium point estimate matches Q03 because both have 0.025 M analytical concentration. The 0.012 L volume is below the campaign's scale range, so scale-dependent and formulation uncertainties widen the intervals. Precipitation remains predicted at the floor in the no-catalyst topology.

- **Q12**: This is the large-scale 0.025 M counterpart to Q03 and Q11. Concentration control gives identical point estimates. Its 0.072 L volume lies inside the tested volume range, so its interval is narrower than Q11's, although the concentration itself remains below the experimental boundary.

Shared rationale:

The sealed K1 account identified analytical reagent concentration as the dominant coordinate but did not identify equilibrium constants or the source of M. These new recipes also omit the 0.003 mol Catalyst A used in every K1 batch, making catalyst removal an out-of-design mechanistic intervention. Point predictions therefore use the simplest no-catalyst HA ⇌ H+ + A− limit, with an effective weak-acid scale near 3×10^-4 used only as a predictive regularizer, not as a newly identified K1 constant. This gives x = (−Ka + sqrt(Ka^2 + 4KaC))/2, acid_dissociation_fraction = x/C, and pH_normalized = −log10(x)/14. The resulting pH predictions are reconciled with the empirical K1 concentration trend, while intervals include model discrepancy, final-assay noise, bounded censoring, and uncertainty about whether Catalyst A was the M source. The proposed M–A precipitation branch predicts near-zero precipitation when catalyst is absent; small positive points represent clipped assay-floor noise, and upper bounds allow the competing endogenous-M topology. Equal-concentration scale controls receive equal point estimates, with wider intervals only where absolute volume lies outside the K1 scale range.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

No task-specific instance dossier, numerical property dossier, or numerical instance prior was supplied; the public prior record was null. A qualitative structural model was supplied, however: HA(aq) ⇌ H+(aq) + A−(aq), a distinct aqueous association step M+ + A− ⇌ MA(aq), and a solid branch M+ + A− ⇌ MA(s), together with the proposed dissolved acid balance n_HA + n_A− + n_MA(aq).

The broad claim of a concentration-coupled acid/precipitation network was supported. At fixed 0.020 L volume, increasing reagent from 0.005 mol in batch 1 to 0.020 mol in batch 5 and 0.035 mol in batch 9 lowered final normalized pH from 0.12174 to 0.07334 and 0.04862, while precipitation signal rose from 0 to 0.05814 and 0.08350. At fixed 0.035 mol loading, dilution through batches 9–12 raised normalized pH from 0.04862 to 0.10469 and reduced precipitation signal from 0.08350 to 0. These observations supported an acid response and a concentration-activated solid or aggregation branch.

The existence of a distinct MA(aq) intermediate was untested. No species-resolved observation separated free M+, free A−, dissolved MA, and solid MA. The proposed balances were chemically plausible but could not be closed because counterions and species amounts were not observed. Assignment of the anonymous reagent to HA and Catalyst A to the M family was also untested.

There was no decisive observed contradiction of the broad network. There was, however, tension with a simple ideal-dilute, single-Ka HA model: final pH changed approximately as 1.10 pH units per decade of reagent concentration rather than the ideal weak-acid half-slope. That tension was explicitly retained and attributed provisionally to activity effects, association, precipitation coupling, or formulation acidity; it was not treated as a falsification or silently removed. The free acid-dissociation channel also failed to provide the clean monotonic confirmation anticipated by the dossier: 6 of 12 final values were zero and the overall mean was about 0.00206, comparable to the declared assay noise. This weakened support but did not constitute a resolved contradiction.

2. Experiments and assumptions that formed the account

The orthogonal loading and dilution comparisons formed the core account. Batches 1, 5, and 9 established the response to increasing loading at 0.020 L. Batches 9–12 established reversal under dilution at fixed 0.035 mol. Similar directionality in batches 5–8 and across the fixed-volume series showed that the result was not based solely on the sealed anchor.

Batches 1 and 8 were especially informative because both had nominal reagent concentration 0.25 M despite fourfold differences in amount and volume. Their final normalized pH values, 0.12174 and 0.11952, supported concentration rather than absolute scale as the primary pH coordinate. This observation motivated the local logarithmic concentration interpolation in K1.

The dossier influenced the decision to include 0.003 mol Catalyst A in every experiment as a fixed putative association partner. That was an untested mechanistic assumption, not an observed identity mapping. Fixing it avoided a catalyst confound within the factorial grid but prevented identification of catalyst dependence. The choice of water and the loading-by-volume factorial reflected the characterization objective and the dossier’s aqueous-equilibrium scope. The conclusion that precipitation had an onset region near 0.4–0.6 M arose from accumulated observations, especially batches 6, 11, 10, 5, and 9, rather than from the supplied structure alone.

The dissociation-fraction account was revised downward in strength after observing floor censoring and disagreement in magnitude between pre-termination pH-meter estimates and final assays. For example, batch 1 gave 0.02385 on the pH meter but zero on the final assay. K1 therefore declined to identify Ka even though the qualitative weak-acid topology remained plausible.

3. Strongest competing explanation

The strongest competing network is a two-branch model without a distinct dissolved MA intermediate:

HA ⇌ H+ + A−
M+ + A− ⇌ MA(s).

With refitted effective acidity, activity coefficients, solubility threshold, and proxy-response scale, this simpler topology can reproduce lower pH at higher concentration and a rising precipitation signal. The evidence cannot distinguish it from the supplied three-state topology containing MA(aq).

A parameter-only alternative retains the supplied topology but allows concentration-dependent activities, an effective Ka, association constant, Ksp, and proxy calibration. This can explain the non-ideal pH slope without deleting any state. The campaign can distinguish neither this parameter refit nor the topology deletion because it lacks direct species measurements and independent variation of the proposed M source.

A further serious explanation is that Catalyst A or its counterions primarily changed acidity, while precipitation was an independent empirical response to reagent concentration. Conversely, M might have been endogenous to the anonymous reagent rather than supplied by Catalyst A. K1 could not distinguish those possibilities. It could support a common concentration coordinate, but not prove that all three channels were generated by one unique molecular graph.

4. One additional complete experiment

I would run one water batch containing 0.020 mol reagent in 0.040 L water, with no catalyst. I would measure it once with the pH meter, terminate it, and obtain the required final assay. This exactly matches the reagent amount and volume of batch 6 while changing only the presence of 0.003 mol Catalyst A.

If the no-catalyst result remained near batch 6—final normalized pH 0.10228, precipitation signal 0.00835, and acid fraction at the lower bound—that would argue that Catalyst A was not the essential M source and that the equilibrium partners were endogenous to the reagent formulation or environment. It would also strengthen concentration-only generalization.

If normalized pH rose substantially, the free fraction became clearly positive, and precipitation collapsed to the assay floor, that would support the working interpretation used cautiously in the blind predictions: Catalyst A supplies or activates the association/precipitation partner and suppresses free A−. If pH changed but precipitation did not, catalyst-controlled acidity and precipitation would need to be separated into different mechanisms. If precipitation changed but pH and fraction did not, the solid branch would appear weakly coupled to acid dissociation. A single experiment would not estimate all constants, but this controlled contrast would resolve the campaign’s largest design ambiguity.

5. Objective-driven trade-offs

The objective was characterization rather than score maximization. I therefore used all 12 complete batches for a planned 3 × 4 loading-volume grid rather than repeatedly running a condition with a favorable scalar score. The design covered reagent concentration from 0.0625 to 1.75 M and provided both fixed-volume loading comparisons and fixed-loading dilution comparisons.

The main trade-off was coverage versus replication. Twelve distinct cells gave broad local structural information and the useful matched-concentration comparison between batches 1 and 8, but no exact replicate estimates of process variation. Local identification of catalyst effects was sacrificed by holding catalyst identity and amount fixed. Solvent, temperature, waiting time, and catalyst identity were likewise held fixed so that loading and dilution remained interpretable.

The native score and equilibrium-confidence diagnostic were not used as optimization targets. Batch 9 was sealed as an evidentiary boundary anchor because it showed the clearest high-concentration response, not because it was claimed to be optimal. The absence of replication and catalyst controls is the cost paid for factorial coverage.

6. Underused evidence and least reliable predictions

The paired pre-termination pH-meter observations were underused. They could have been analyzed more formally as a paired-method dataset, particularly where fraction estimates differed from final assays. Raw signal shapes and calibration metadata were also not developed into an independent species argument, because their public assignments were proxy-level rather than mechanistically specific. The low residual diagnostics were noted but appropriately not converted into molecular proof.

The dissociation-fraction observations were acquired but yielded little identification because of noise and lower-bound censoring. The constant-concentration pair of batches 1 and 8 was useful for pH but could not identify scale effects on precipitation because both precipitation values were at or near the floor.

The least reliable blind predictions are Q01 and Q02, which extrapolate from the K1 lower concentration boundary of 0.0625 M down to 0.0004167 and 0.004167 M. Q03, Q11, and Q12 at 0.025 M also extrapolate below the observed concentration range. Q06 is especially topology-sensitive because it combines high concentration with removal of Catalyst A. Q07 and Q11 use volumes of 0.006 and 0.012 L, below the 0.020 L minimum studied.

More generally, every blind recipe omitted Catalyst A, whereas every K1 experiment contained 0.003 mol. The Q prediction intervals attempted to represent that intervention, but several may still be too narrow because the sealed K1 account explicitly judged the catalyst-to-M mapping and Ka unidentifiable. The acid-fraction intervals for Q04–Q07 and precipitation intervals for Q05–Q07 are particularly dependent on whether Catalyst A was the M source. The effective weak-acid constant used as a predictive regularizer in Q was not a K1-identified parameter and should not be mistaken for one.

7. Limits of the anchor, repeatability, robustness, and generalization

Batch 9 is a single boundary observation: 0.035 mol reagent, 0.020 L water, and 0.003 mol Catalyst A, with final normalized pH 0.04862, acid fraction 0.00214, and precipitation signal 0.08350. It anchors the concentrated end of this grid. It does not establish repeatability, a universal threshold, a solid yield, or an optimum.

There were no exact experimental replicates, so repeatability cannot be separated empirically from observation noise and batch variability. Local robustness is supported only by neighboring cells: batches 5 and 10 gave precipitation signals 0.05814 and 0.05092, while batch 11 gave 0.02024, consistent with a graded concentration response. That neighborhood supports continuity but not precise parameter stability.

Generalization is strongest for interpolation in water with Catalyst A fixed at 0.003 mol, approximately ambient temperature, volumes of 0.020–0.080 L, loadings of 0.005–0.035 mol, and concentrations of 0.0625–1.75 M. It is weaker when amount and volume are changed beyond those bounds, and substantially weaker when catalyst is omitted or changed. Nothing in K1 establishes transfer to ethanol, acetonitrile, toluene, other catalyst identities, different temperatures, altered equilibration times, named real chemicals, or other ChemWorld instances.

The sealed anchor and K1 account therefore provide a bounded local mechanism family and useful concentration-response interpolation. They do not prove a unique topology, identified constants, cross-material invariance, world-to-world transfer, or operational optimality.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `1, 5, 9, 12`
- Rationale: The source campaign supports a common acid-dissociation and precipitation framework: at 0.020 L, batches 1, 5, and 9 showed decreasing normalized pH and increasing precipitation signal with loading, while dilution from batch 9 to batch 12 reversed both responses. However, no species-resolved measurement distinguished a discrete aqueous MA ion pair from direct free-ion precipitation. Both topologies remain compatible with the observed public channels, so the aqueous intermediate is indeterminate.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0219067 | 0.883333 | 0.0620833 | 0.0639388 |
| acid_dissociation_fraction | 0.0982047 | 0.416667 | 0.171667 | 0.405384 |
| precipitation_signal | 0.00607176 | 1 | 0.0259167 | 0.0259167 |

## Structural evaluation

Truth family: `aqueous_ion_pair_intermediate`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `False`; equation-set Jaccard: `0.666667`.

## Response-shape evaluation

Concentration slope MAE `0.0544008` and curvature MAE `0.0352432`. Dilution slope MAE `0.0347323` and curvature MAE `0.013026`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
