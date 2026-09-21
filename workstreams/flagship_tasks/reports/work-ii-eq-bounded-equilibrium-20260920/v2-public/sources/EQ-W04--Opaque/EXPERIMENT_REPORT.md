# EQ-W04--Opaque — final public report

World `EQ-W04`; prior arm `Opaque`; status `completed`. The effective result came from `attempt-01`.

## Source campaign

The campaign contains 12/12 completed batches and 60 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.288982 | 0.0755894 | 0.150716 | 0.00363362 |
| 2 | 0.293046 | 0.071013 | 0.146632 | 0.00239195 |
| 3 | 0.290974 | 0.067381 | 0.157945 | 0.0011464 |
| 4 | 0.290337 | 0.0679382 | 0.154117 | 0 |
| 5 | 0.288816 | 0.0791244 | 0.157634 | 0 |
| 6 | 0.293277 | 0.0619171 | 0.151914 | 0 |
| 7 | 0.293625 | 0.069465 | 0.15707 | 0.00198509 |
| 8 | 0.292156 | 0.0707212 | 0.152329 | 0.00472622 |
| 9 | 0.29255 | 0.0732864 | 0.159955 | 0 |
| 10 | 0.292829 | 0.06646 | 0.157717 | 0.00994678 |
| 11 | 0.293711 | 0.0769217 | 0.157806 | 0 |
| 12 | 0.289263 | 0.0743566 | 0.159038 | 0.0017778 |

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## Sealed scientific account

### K1 report

Mechanistic report

1. Experimental basis

I completed 12 independent water-only batches at approximately 297.2 K. Total reagent loading n was varied over 0.004, 0.012, 0.024, and 0.032 mol, and liquid volume V over 0.040, 0.060, and 0.080 L. The resulting nominal total concentrations C_T = n/V covered 0.050–0.800 mol L⁻¹. No catalyst, cosolvent, heating, deliberate aging period, or pH modifier was used. Every batch received an in-process pH-meter measurement and a post-termination final assay. The final assay is the primary quantitative evidence because its declared noise is lower.

Final-assay observations were:

Batch | V (L) | n (mol) | C_T (mol L⁻¹) | pH/14 | dissociated fraction α | precipitation proxy | equilibrium residual
1 | 0.040 | 0.004 | 0.100 | 0.28898 | 0.07559 | 0.15072 | 0.00363
2 | 0.040 | 0.012 | 0.300 | 0.29305 | 0.07101 | 0.14663 | 0.00239
3 | 0.040 | 0.024 | 0.600 | 0.29097 | 0.06738 | 0.15795 | 0.00115
4 | 0.040 | 0.032 | 0.800 | 0.29034 | 0.06794 | 0.15412 | 0
5 | 0.060 | 0.004 | 0.0667 | 0.28882 | 0.07912 | 0.15763 | 0
6 | 0.060 | 0.012 | 0.200 | 0.29328 | 0.06192 | 0.15191 | 0
7 | 0.060 | 0.024 | 0.400 | 0.29362 | 0.06946 | 0.15707 | 0.00199
8 | 0.060 | 0.032 | 0.533 | 0.29216 | 0.07072 | 0.15233 | 0.00473
9 | 0.080 | 0.004 | 0.050 | 0.29255 | 0.07329 | 0.15996 | 0
10 | 0.080 | 0.012 | 0.150 | 0.29283 | 0.06646 | 0.15772 | 0.00995
11 | 0.080 | 0.024 | 0.300 | 0.29371 | 0.07692 | 0.15781 | 0
12 | 0.080 | 0.032 | 0.400 | 0.28926 | 0.07436 | 0.15904 | 0.00178

Across these final assays, mean pH/14 was 0.29163, corresponding to pH 4.0828. The observed pH range was 4.0434–4.1120. Mean α was 0.07118, with range 0.06192–0.07912. Mean precipitation proxy was 0.15524, with range 0.14663–0.15996. The population-scale scatter was 0.00178 for pH/14, 0.00471 for α, and 0.00389 for the precipitation proxy. These are comparable to or smaller than the final assay's declared noise scales of 0.002, 0.006, and 0.006, respectively.

2. Main interpretation

The simplest effective description is a pH-buffered weak-acid equilibrium accompanied by a nearly invariant precipitation-related background or plateau:

HA ⇌ H⁺ + A⁻

C_T = n/V

α = [A⁻]/([HA] + [A⁻])

α ≈ 1/{1 + 10^(pK_a,eff − pH)}.

Using each final-assay pH and α pair gives an apparent pK_a,eff with mean 5.199, observed range 5.109–5.286, and RMS dispersion 0.048. Thus the pH and dissociation measurements are mutually compatible with an effective monoprotic Henderson–Hasselbalch relationship near pK_a,eff ≈ 5.20.

The important qualification is that this does not behave like an isolated, unbuffered weak acid in pure water. An unbuffered weak acid with fixed K_a would generally show a substantial concentration dependence: approximately α ∝ C_T^−1/2 in the low-dissociation limit, together with a noticeable pH shift. Here C_T changed sixteen-fold while both pH and α remained nearly constant. Therefore at least one additional regulating feature is required. The most economical explanation is a latent buffer or proton reservoir that clamps pH near 4.08; once pH is clamped, a fixed effective pK_a naturally gives an almost fixed dissociation fraction near 0.071.

Equivalent physical realizations include a background buffer, a counterion equilibrium, activity-coefficient compensation, or a dissolved/solid reservoir that regulates chemical potentials. The measurements identify the effective relationship but do not distinguish these microscopic implementations.

3. Dependence on loading and dilution

A descriptive least-squares fit against nominal concentration over the tested domain gave:

pH/14 ≈ 0.291710 − 0.000246 C_T, R² ≈ 0.001;

α ≈ 0.073552 − 0.007293 C_T, R² ≈ 0.119;

P ≈ 0.155642 − 0.001238 C_T, R² ≈ 0.005,

where P is the public precipitation proxy and C_T is in mol L⁻¹. Across the entire 0.05–0.80 mol L⁻¹ interval, these fits imply changes of only about −0.00018 in pH/14, −0.0055 in α, and −0.00093 in P. The pH and precipitation slopes explain essentially none of the observed variance. The weak negative α slope is possible but not compelling: its full-range effect is comparable to one final-assay noise scale and individual batches are non-monotonic.

The factorial layout also tested total amount and volume separately. For example, batches 2 and 11 both had C_T = 0.300 mol L⁻¹ but used (0.012 mol, 0.040 L) and (0.024 mol, 0.080 L). Their final values were pH/14 = 0.29305 versus 0.29371, α = 0.07101 versus 0.07692, and P = 0.14663 versus 0.15781. Batches 7 and 12 both had C_T = 0.400 mol L⁻¹; their values were 0.29362 versus 0.28926, 0.06946 versus 0.07436, and 0.15707 versus 0.15904. These pairs do not establish exact concentration-only collapse, but their differences are small enough that noise or minor batch effects remain plausible.

At fixed n = 0.012 mol, dilution from 0.040 to 0.080 L changed P from 0.14663 through 0.15191 to 0.15772, suggesting a possible positive volume effect. That pattern was not reproduced consistently at the other loadings: at n = 0.024 mol, P was 0.15795, 0.15707, and 0.15781 across the same volumes. An additive fit assigned a precipitation change of about +0.0063 across the 0.040 L volume span, but that is only about one declared assay-noise scale. I therefore treat a separate volume effect as tentative, not established.

My supported local response surface is consequently closer to a plateau than to a strong loading law:

pH/14 ≈ 0.2916,
α ≈ 0.0712,
P ≈ 0.1552,

with the observed scatter above, only within the tested aqueous domain.

4. Precipitation coupling

The precipitation proxy remained near 0.15 rather than increasing systematically with total concentration. This rules against a large, directly resolved precipitation transition inside the tested range. It does not prove that no solid phase exists, because P is a bounded normalized proxy rather than a measured solid mass.

Several explanations remain observationally equivalent:

• P may contain an approximately constant baseline unrelated to the amount precipitated.
• The reporter may already be on a low or saturated plateau before C_T = 0.05 mol L⁻¹.
• A solid or ion-pair reservoir may hold the relevant dissolved activity nearly constant while total material changes.
• The precipitation threshold may lie outside the tested concentration range, with the observed variation being instrument noise.
• Two opposing effects, such as increasing available precipitating species and increasing dissolution or complexation, may cancel locally.

Because α and pH were also nearly invariant, the data are compatible with coupled proton and solubility buffering. They do not show whether precipitation causes the pH clamp, merely responds to it, or is independently regulated.

5. Measurements that changed or constrained the explanation

Batches 1–4 first varied loading eight-fold at V = 0.040 L. The absence of a monotonic pH or precipitation response immediately argued against a simple unbuffered concentration-controlled model. Batches 5–8 and 9–12 then repeated the loading series at larger volumes. Their similarly narrow final-assay bands showed that the flat response was not peculiar to the smallest vessel volume.

The matched-concentration pairs, especially batches 2/11 and 7/12, tested whether C_T alone was sufficient. They supported approximate rather than exact concentration collapse and left room for small independent volume, total-amount, or batch effects.

Batch 6, the selected representative experiment, used 0.012 mol in 0.060 L and produced final pH/14 = 0.29328, α = 0.06192, and P = 0.15191. It is useful as a mid-domain anchor, but it was selected for representativeness rather than because it maximized any outcome.

The intermediate pH-meter measurements were noisier than the final assays. Relative to the paired final values, their RMS differences were 0.00401 for pH/14, 0.01750 for α, and 0.02369 for P. Those differences are consistent with the pH meter's larger declared noise scales. For example, its batch-1 P estimate was 0.20043 while the final assay gave 0.15072. I therefore did not reinterpret such individual intermediate outliers as distinct chemical states.

The final equilibrium residual averaged 0.00213 and was at most 0.00995, in batch 10. Several reported residuals were exactly zero, potentially reflecting clipping at the lower bound. These low values indicate internal consistency with the environment's equilibrium calculation, but they do not independently identify a mechanism. Likewise, equilibrium_confidence is explicitly an environment diagnostic and is not used as my epistemic confidence.

No numerical archival local relationship was supplied in the public material packet. The principal candidate law tested here was therefore the ordinary unbuffered weak-acid concentration dependence. Its strong form is not supported; the buffered effective-acid form is supported locally.

6. Identifiability and uncertainty

The identifiable quantities are the local response plateau, the approximate coupling between pH and α, and the lack of a large concentration-driven precipitation transition. The apparent pK_a,eff is a compact empirical parameter, not identification of a named chemical or proof of ideal activities.

The following are not identifiable from this campaign:

• the molecular identity or proton stoichiometry of the anonymous reagent;
• the identity and capacity of any buffer or counterion reservoir;
• activity coefficients and ionic-strength effects;
• the solid phase identity, solubility product, nucleation barrier, or actual precipitated mass;
• whether the precipitation proxy has an offset, nonlinear calibration, or saturation;
• equilibration time, kinetic hysteresis, or aging effects, because time was not deliberately varied;
• temperature dependence, since only the ambient condition was used;
• solvent and catalyst effects, since only water and no catalyst were tested;
• behavior below 0.05 or above 0.80 mol L⁻¹, or outside 0.040–0.080 L and 0.004–0.032 mol.

There were no independent replicate batches at identical n and V, so variance components cannot be separated cleanly into instrument noise, batch noise, and real weak effects. The declared instrument noise and the small observed scatter make the plateau interpretation reasonable, but they do not justify claiming mathematically exact invariance.

7. Supported model and predictions versus speculation

Supported within the measured domain:

1. pH is approximately clamped near 4.08.
2. The dissociated fraction is approximately 0.071 and is consistent with pK_a,eff ≈ 5.20 through a Henderson–Hasselbalch-type relation.
3. Loading and dilution have, at most, weak effects compared with the observed and declared measurement scatter.
4. The precipitation proxy occupies a nearly flat band around 0.155, with no resolved threshold across 0.05–0.80 mol L⁻¹.

Local interpolation, rather than direct observation:

For another water-only batch at approximately 297 K with n and V inside the tested rectangle, I would use pH/14 ≈ 0.292, α ≈ 0.071, and P ≈ 0.155 as central predictions, widening uncertainty enough to cover at least the observed ranges. The small fitted α decline with C_T could be retained as a secondary term, but a constant model is nearly as defensible.

Speculation:

The most plausible microscopic story is a buffered proton reservoir coupled to a weak acid with effective pK_a near 5.2, plus either a precipitation reporter baseline or a solubility-buffered species. A precipitation-controlled proton reservoir is an attractive unified explanation, but the present measurements cannot distinguish it from independent pH buffering plus an unrelated proxy baseline. Claims outside the tested concentration, volume, solvent, temperature, and timing ranges would be extrapolations and are not warranted by these observations.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.085 | 0.05 | 0.14 |
| Q01 | pH_normalized | 0.296 | 0.286 | 0.31 |
| Q01 | precipitation_signal | 0.11 | 0.04 | 0.18 |
| Q02 | acid_dissociation_fraction | 0.085 | 0.05 | 0.14 |
| Q02 | pH_normalized | 0.296 | 0.286 | 0.31 |
| Q02 | precipitation_signal | 0.125 | 0.055 | 0.185 |
| Q03 | acid_dissociation_fraction | 0.22 | 0.07 | 0.48 |
| Q03 | pH_normalized | 0.326 | 0.29 | 0.38 |
| Q03 | precipitation_signal | 0.045 | 0 | 0.145 |
| Q04 | acid_dissociation_fraction | 0.095 | 0.045 | 0.2 |
| Q04 | pH_normalized | 0.296 | 0.278 | 0.325 |
| Q04 | precipitation_signal | 0.065 | 0 | 0.16 |
| Q05 | acid_dissociation_fraction | 0.074 | 0.061 | 0.087 |
| Q05 | pH_normalized | 0.292 | 0.287 | 0.297 |
| Q05 | precipitation_signal | 0.151 | 0.139 | 0.164 |
| Q06 | acid_dissociation_fraction | 0.074 | 0.061 | 0.087 |
| Q06 | pH_normalized | 0.292 | 0.287 | 0.297 |
| Q06 | precipitation_signal | 0.151 | 0.139 | 0.164 |
| Q07 | acid_dissociation_fraction | 0.074 | 0.061 | 0.087 |
| Q07 | pH_normalized | 0.292 | 0.287 | 0.297 |
| Q07 | precipitation_signal | 0.151 | 0.139 | 0.164 |
| Q08 | acid_dissociation_fraction | 0.52 | 0.15 | 0.88 |
| Q08 | pH_normalized | 0.375 | 0.305 | 0.48 |
| Q08 | precipitation_signal | 0.015 | 0 | 0.1 |
| Q09 | acid_dissociation_fraction | 0.2 | 0.06 | 0.45 |
| Q09 | pH_normalized | 0.323 | 0.288 | 0.38 |
| Q09 | precipitation_signal | 0.025 | 0 | 0.12 |
| Q10 | acid_dissociation_fraction | 0.045 | 0.005 | 0.1 |
| Q10 | pH_normalized | 0.285 | 0.255 | 0.305 |
| Q10 | precipitation_signal | 0.3 | 0.12 | 0.65 |
| Q11 | acid_dissociation_fraction | 0.071 | 0.059 | 0.084 |
| Q11 | pH_normalized | 0.292 | 0.287 | 0.297 |
| Q11 | precipitation_signal | 0.157 | 0.144 | 0.171 |
| Q12 | acid_dissociation_fraction | 0.073 | 0.061 | 0.085 |
| Q12 | pH_normalized | 0.292 | 0.287 | 0.296 |
| Q12 | precipitation_signal | 0.154 | 0.143 | 0.165 |

Predictions use the previously sealed interpretation without additional experiments. Inside or near the measured domain, the central model is the observed aqueous plateau: pH_normalized about 0.292, acid dissociation about 0.071, and precipitation signal about 0.155. Intervals combine final-assay noise with observed between-batch scatter. Identical final compositions in Q05–Q07 receive identical predictions because equilibrium observables were treated as state functions. For trace-load and extreme-concentration extrapolations, intervals are deliberately much wider and central estimates allow physically plausible departure from the plateau: increased fractional dissociation and diminished precipitation upon extreme dilution, and the reverse tendency at very high concentration. These extrapolated trends were not directly observed and compete with the alternative of persistent buffering and a nearly constant precipitation-proxy baseline.

### K2 retrospective

1. Initial claims: supported, challenged, or untested

The initial material packet contained no task-specific property dossier, numerical equilibrium law, archival parameter estimate, or named chemical identity. K1 therefore correctly stated: “No numerical archival local relationship was supplied in the public material packet.” There was no substantive quantitative prior to confirm or refute.

Several items in the initial packet were contractual framing rather than empirical claims: this was an aqueous weak-acid/precipitation slice; pH_normalized meant pH/14; acid_dissociation_fraction and precipitation_signal were bounded observables; and equilibrium_confidence was an environment diagnostic rather than epistemic confidence. The campaign respected those definitions, but observing compatible numbers does not independently validate a contract.

The broad weak-acid framing received limited support. In K1 I found that final-assay pH and dissociation pairs were compatible with an effective Henderson–Hasselbalch relationship, with apparent pKa,eff about 5.20. That supports an effective acid/base description, not a molecular identity or an ideal monoprotic mechanism.

A simple unbuffered weak-acid model was challenged by actual evidence. Across nominal concentrations from 0.05 to 0.80 mol/L, pH and dissociation remained nearly flat instead of showing the strong concentration dependence expected for an isolated weak acid in water. K1 explicitly revised this interpretation toward a buffered or otherwise regulated equilibrium. This was positive counterevidence, not merely an absence of evidence.

A large precipitation transition inside the sampled range was also disfavored: the final precipitation proxy stayed between 0.14663 and 0.15996. That does not establish absence of precipitation. It only argues against a large resolved change in the public proxy over the sampled domain.

Important claims remained untested: path independence, equilibration kinetics, buffer capacity, behavior at trace loading, behavior above 0.80 mol/L, solid identity, temperature dependence, and transfer to other solvents or catalysts. In particular, the plateau interpretation had no counterexample within the sampled range, but that is not proof that the plateau continues toward zero loading or extreme concentration.

There was some evidence against an exact concentration-only law. At equal concentration, batches 2 and 11 differed in precipitation signal by about 0.0112, while batches 7 and 12 differed in pH_normalized by about 0.00436. K1 did not completely ignore this: it described concentration collapse as “approximate rather than exact” and retained possible amount, volume, or batch effects. Nevertheless, the final plateau summary arguably emphasized invariance more strongly than these pairwise discrepancies warranted.

2. Experiments that formed or changed the interpretation

Batches 1–4 were the first decisive block. At fixed V = 0.040 L, loading rose from 0.004 to 0.032 mol, yet the final pH_normalized values remained within 0.28898–0.29305 and the precipitation proxy within 0.14663–0.15795. This directly weakened the initially plausible unbuffered concentration-response model.

Batches 5–8 and 9–12 changed the interpretation from “possibly a small-volume artifact” to “a response plateau repeated across the sampled volume range.” The same narrow response bands appeared at 0.060 and 0.080 L.

The matched-concentration comparisons were especially informative. Batches 2 and 11 both had 0.300 mol/L but different total amounts and volumes; batches 7 and 12 both had 0.400 mol/L. These comparisons supported approximate state dependence on concentration while showing that exact collapse was not established.

The paired intermediate and final measurements also changed how I weighted evidence. Their mean differences were small, but RMS differences were much larger for dissociation and precipitation than for the final assays alone. Batch 1, for example, had intermediate precipitation_signal 0.20043 but final precipitation_signal 0.15072. I consequently based K1 primarily on the lower-noise final assay. That was reasonable, although it also meant that possible time-dependent relaxation was treated mainly as measurement noise rather than tested mechanistically.

The original 3 × 4 grid itself was chosen before outcomes were known. It was guided by the research brief’s emphasis on loading, volume, dilution, pH, and precipitation, plus the public stock limits. Choosing water, omitting catalysts, and varying amount and volume factorially were grounded in the aqueous-equilibrium objective. By contrast, the lower bound of 0.004 mol was an unvalidated design guess. It proved sufficient to characterize the plateau but left the trace-loading regime—the most important region in several blind questions—unobserved.

The campaign was not adaptively redesigned after the early flat results. Preserving the planned coverage avoided outcome-driven design changes, but it also meant that later batches continued sampling the same plateau instead of placing one or more points below 0.004 mol. Thus the conclusion was well supported locally and weakly supported at the lower boundary.

3. Principal competing mechanisms

The leading effective explanation in K1 was a buffered weak-acid equilibrium:

HA ⇌ H+ + A−,

with pH held near 4.08 by a latent proton reservoir and an effective pKa near 5.20. This explains why the dissociation fraction remains near 0.071 despite changing total concentration.

The strongest competitors are:

(a) A precipitation- or solid-phase-buffered system. A solid reservoir could regulate dissolved activity and proton balance simultaneously. This could reproduce the same local pH and dissociation plateau without an independent soluble buffer.

(b) An instrument/proxy plateau. The underlying chemistry could vary while the bounded processed observables remain in a compressed or saturated response region. The campaign used processed estimates and did not establish a direct conversion from precipitation_signal to precipitated mass.

(c) A domain-limited saturation model. The sampled 0.004–0.032 mol range may lie entirely above a low-loading transition. This explanation is especially relevant to Q03, Q04, Q08, and Q09. K1 acknowledged that thresholds could lie outside the tested range, but the campaign did not locate them.

(d) Opposing effects that cancel locally. Increasing total concentration could favor precipitation while activity, complexation, or proton regulation offsets the change. A locally flat response would not then imply a single invariant equilibrium constant.

(e) Small independent amount or volume effects. The equal-concentration pairs and the tentative positive volume coefficient for precipitation leave this possibility open.

(f) History-dependent nucleation or relaxation. The disagreement between intermediate and final measurements could be pure sensor noise, but the experiment did not independently vary waiting time or dosing order. Q05–Q07 later required a path-independence assumption that was not directly tested in the campaign.

The existing data distinguish these mechanisms only partially. They reject a strong, monotonic unbuffered weak-acid response across 0.05–0.80 mol/L and disfavor a large precipitation transition within that interval. They cannot distinguish an external buffer from a solid reservoir, a compressed reporter, or a saturated latent response. They also cannot distinguish equilibrium path independence from fast but unobserved kinetic relaxation.

4. One additional legal complete experiment

If exactly one additional complete experiment were permitted, I would choose an extreme dilute condition: 0.075 L water plus 0.000001 mol reagent, followed by an in-process pH-meter measurement, termination, and the required final assay. This is the condition represented by sealed blind query Q08, but I would select it prospectively because it maximizes separation among the leading mechanisms. I would not execute it now.

Possible outcomes would have distinct implications:

• If pH_normalized, dissociation, and precipitation all remain near the K1 plateau—approximately 0.292, 0.071, and 0.155—the persistent-buffer or reporter-baseline explanation would gain substantial support. A simple material-limited precipitation signal would become less plausible.

• If pH rises, dissociation rises strongly, and precipitation approaches zero, that would support a low-loading transition toward dilute weak-acid behavior. It would show that the original campaign sampled only the saturated side of the response.

• If pH and dissociation change but precipitation remains near 0.155, proton speciation and the precipitation proxy would appear partly independent; an instrumental or background offset for precipitation would become more credible.

• If precipitation falls while pH and dissociation stay near their plateau, the proton reservoir would appear persistent while precipitation depends mainly on total material inventory.

• If the intermediate and final assays differ greatly, time dependence or post-termination relaxation would become a priority explanation, although a single experiment would still not cleanly separate kinetics from instrument disagreement.

This experiment would not identify the buffer or solid phase, but it would resolve the largest extrapolation uncertainty left by the campaign.

5. Tradeoff between identifiability and operational score

The research objective was characterization rather than yield or process optimization. I therefore used a factorial amount–volume design rather than searching for the highest scalar score. The design deliberately sacrificed any opportunity to concentrate resources around a high-scoring condition in exchange for comparisons across loading and dilution.

I also did not treat equilibrium_confidence as an optimization target, even though it had substantial weight in the scalar scoring contract. This followed the explicit instruction that it was an environment diagnostic, not scientific confidence. Chasing it would have distorted the mechanistic objective.

There was no meaningful optimization-driven sacrifice of identifiability. The more important weakness was the reverse: the design pursued broad factorial coverage for identifiability but distributed all 12 experiments within what turned out to be a relatively flat region. Once the first several batches suggested a plateau, an adaptive scientific design might have allocated a batch to trace loading or an exact replicate. The fixed grid protected against outcome-driven manipulation but reduced discrimination among plateau mechanisms.

The selected recommendation, batch 6, was not chosen because it maximized score. It was chosen as a representative mid-volume, moderate-loading anchor with both intermediate and final measurements. This was consistent with the characterization objective but should not be described as optimization.

6. Evidence not fully used and weaknesses in the blind predictions

The campaign made limited use of potentially informative structure in the paired measurements. Intermediate-to-final changes were summarized as noise, but they could also contain kinetic information. Without replicate timing conditions, that signal was difficult to interpret, yet K1 could have emphasized the ambiguity more strongly.

The exact factorial structure was used for simple linear regressions and matched-concentration comparisons, but not for nonlinear threshold models, hierarchical measurement-error models, or explicit interaction terms. With only 12 batches and no exact replicates, sophisticated fits would have been weakly identified; nevertheless, the limitation matters.

Processed final estimates dominated the analysis. Any public raw spectral or mass-balance features that might have distinguished baseline signal from genuine precipitation were not incorporated into the sealed report. I cannot now inspect additional evidence, and I do not claim that such features would necessarily have been diagnostic.

Equilibrium residuals were available but difficult to exploit chemically. K1 appropriately avoided converting low residuals into mechanistic confidence. The equilibrium_confidence values were also intentionally excluded from epistemic reasoning.

The least reliable blind predictions are Q08 and Q10. Q08 extrapolates far below the observed loading range and its central estimate assumes a dilute-regime transition. Q10 extrapolates from a maximum observed concentration of 0.80 mol/L to 6.67 mol/L and speculates about stronger precipitation. Their wide intervals appropriately signal uncertainty, but even those intervals depend on qualitative assumptions about how bounded proxies behave outside support.

Q03 and Q09 are also highly uncertain because they probe trace concentrations and total amounts. Their central estimates invoke increased fractional dissociation and reduced precipitation, neither of which was observed directly.

Some intervals were probably too narrow:

• Q05–Q07 used identical, fairly narrow intervals because their final nominal composition was identical. However, 0.002 mol is below the campaign’s minimum amount and 0.024 L is below its minimum volume. More importantly, the campaign never tested dosing-order or nucleation-history effects. Treating these as well-supported interior predictions was too confident.

• Q11 had an in-range concentration but used 0.040 mol, above the observed amount range. Its narrow interval assumed concentration dominance and understated possible independent total-amount effects.

• Q12 was the best-supported prediction because its concentration was interior and its amount and volume were close to the sampled domain, although its volume was still slightly below 0.040 L.

• Q01 and Q02 had wider intervals, appropriately reflecting their low amounts, but assigning different precipitation point estimates at equal concentration introduced an amount effect that the campaign had not reliably quantified.

The narrow Q05–Q07 and Q11 intervals are in some tension with K1’s explicit scope statement limiting support to 0.004–0.032 mol, 0.040–0.080 L, and 0.05–0.80 mol/L. The trace and extreme predictions were more consistent with K1 because their rationales explicitly labeled the trends as extrapolations and used broad intervals.

No prediction truth has been supplied, so these criticisms are prospective calibration concerns, not post hoc explanations of errors.

7. Limitations of the sealed recommendation

The sealed recommendation was batch 6: 0.012 mol reagent in 0.060 L water, with final pH_normalized 0.29328, dissociation fraction 0.06192, and precipitation signal 0.15191. It was selected as a representative evidentiary anchor, not as a best-performing recipe.

Its repeatability has not been established. Testing repeatability would require multiple independent batches with the exact same actions, comparing both intermediate and final measurements and reporting all failures. One observed batch cannot separate instrument noise from batch variability.

Local robustness would require a small neighborhood around batch 6. Useful contrasts would independently perturb amount and volume, include constant-concentration pairs, and vary dosing order or a controlled waiting interval. That would test whether the apparent plateau survives local perturbation and whether the route to the final state matters.

Cross-material generalization is unsupported. Only water was used, no catalyst was added, and the reagent was anonymous. Testing another solvent or catalyst would define a different material context rather than validate the existing aqueous mechanism automatically.

Cross-world generalization is also unsupported. The effective pKa, plateau level, and precipitation proxy may be specific to this bounded synthetic world. Transfer would require preregistered repetition across independent worlds or material instances, with the same measurement contract and explicit criteria for parameter stability.

Finally, batch 6 cannot be called “proven optimal.” It was not selected by an optimization analysis, and the campaign did not search the legal action space for a maximum. I cannot even claim that it was the sample-in highest-scoring batch without a documented comparison of the relevant scalar scores. The defensible statement is only that batch 6 was a representative sampled condition chosen for blind replay. “Sample-in highest,” “locally robust,” and “globally optimal” are separate claims, none of which was established by the sealed recommendation.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `5.2`; 80% interval `[5.14, 5.26]`.

An effective Henderson–Hasselbalch transformation of the 12 paired final-assay pH and dissociation measurements gave a mean apparent pKa of 5.199, with observed values 5.109–5.286 and RMS dispersion 0.048. The interval reflects measurement and batch scatter and identifies only a local effective parameter, not an intrinsic thermodynamic pKa; buffering, activities, precipitation, and processed-observable calibration remain confounded.

Path-dependence assessment: `indeterminate`.

No source-campaign experiment held the final amount and volume fixed while changing staged-addition order. Batches 2 and 11 shared 0.300 mol/L, and batches 7 and 12 shared 0.400 mol/L, but each pair differed in both total amount and volume, so they cannot test path dependence. The generally similar final responses support approximate state-based behavior, while intermediate-to-final differences could reflect either instrument noise or relaxation. Reproducible staged-path dependence was therefore neither demonstrated nor excluded.

Dissociation-precipitation assessment: `continuous`.

Supported range: Supported only for water at approximately 297.2 K, reagent amounts 0.004–0.032 mol, volumes 0.040–0.080 L, and nominal concentrations 0.05–0.80 mol/L. Within this domain, final dissociation ranged from 0.06192 to 0.07912 and precipitation signal from 0.14663 to 0.15996, without an abrupt coordinated change.

Competing explanation: The apparent continuity may be a saturated or baseline-dominated public proxy that masks a threshold below 0.05 or above 0.80 mol/L; assay noise and a latent solid-phase reservoir are also observationally equivalent within this range.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.00838425 | 0.983333 | 0.173917 | 0.17587 |
| pH_normalized | 0.00329017 | 1 | 0.0459167 | 0.0459167 |
| precipitation_signal | 0.0310531 | 0.95 | 0.12075 | 0.122371 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
