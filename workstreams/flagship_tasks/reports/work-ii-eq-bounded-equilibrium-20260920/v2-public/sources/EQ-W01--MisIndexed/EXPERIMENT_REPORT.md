# EQ-W01--MisIndexed — final public report

World `EQ-W01`; prior arm `MisIndexed`; status `completed`. The effective result came from `attempt-03`.

## Source campaign

The campaign contains 12/12 completed batches and 60 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.252637 | 0.0796597 | 0.157628 | 0 |
| 2 | 0.259376 | 0.0924574 | 0.145908 | 0.00101279 |
| 3 | 0.251178 | 0.0718704 | 0.158944 | 0 |
| 4 | 0.257033 | 0.0717239 | 0.148026 | 0 |
| 5 | 0.256022 | 0.0769326 | 0.149746 | 0.00093063 |
| 6 | 0.251245 | 0.0704351 | 0.154199 | 0.000520905 |
| 7 | 0.255395 | 0.0611356 | 0.151467 | 0.000486603 |
| 8 | 0.250857 | 0.0688975 | 0.156069 | 0 |
| 9 | 0.25317 | 0.0790158 | 0.152057 | 0 |
| 10 | 0.251746 | 0.0690516 | 0.160749 | 0 |
| 11 | 0.252636 | 0.0690026 | 0.148714 | 0 |
| 12 | 0.249344 | 0.074604 | 0.155208 | 0 |

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## Sealed scientific account

### K1 report

Mechanistic report

1. Experimental scope and evidence

I completed 12 water-only batches at approximately ambient temperature without catalyst, heating, or deliberate equilibration-time variation. Nominal reagent amount ranged from 0.001 to 0.040 mol, liquid volume from 0.018 to 0.080 L, and nominal total loading C_T = n/V from 0.0185 to 2.0 mol L^-1. Every batch received an in-process pH-meter measurement and a post-termination final assay. The final assay is the primary quantitative basis below because its declared channel noise is lower. The pH-meter observations are treated as secondary, noisier checks. The reported equilibrium_confidence channel is an environment diagnostic and is not used as my scientific confidence.

Final-assay observations were:

Batch | reagent mol | volume L | C_T mol L^-1 | pH_normalized | dissociated fraction alpha | precipitation proxy
1 | 0.001 | 0.018 | 0.0556 | 0.252637 | 0.079660 | 0.157628
2 | 0.001 | 0.054 | 0.0185 | 0.259376 | 0.092457 | 0.145908
3 | 0.005 | 0.020 | 0.250 | 0.251178 | 0.071870 | 0.158944
4 | 0.005 | 0.060 | 0.0833 | 0.257033 | 0.071724 | 0.148026
5 | 0.010 | 0.020 | 0.500 | 0.256022 | 0.076933 | 0.149746
6 | 0.010 | 0.060 | 0.1667 | 0.251245 | 0.070435 | 0.154199
7 | 0.020 | 0.040 | 0.500 | 0.255395 | 0.061136 | 0.151467
8 | 0.030 | 0.060 | 0.500 | 0.250857 | 0.068897 | 0.156069
9 | 0.040 | 0.080 | 0.500 | 0.253170 | 0.079016 | 0.152057
10 | 0.030 | 0.030 | 1.000 | 0.251746 | 0.069052 | 0.160749
11 | 0.040 | 0.040 | 1.000 | 0.252636 | 0.069003 | 0.148714
12 | 0.040 | 0.020 | 2.000 | 0.249344 | 0.074604 | 0.155208

Across all final assays, mean alpha was 0.07373 with observed range 0.06114–0.09246. Mean pH_normalized was 0.25339 with range 0.24934–0.25938, corresponding to an actual pH range of approximately 3.491–3.631 under the declared pH = 14 pH_normalized mapping. The precipitation proxy averaged 0.15323 and ranged from 0.14591 to 0.16075. Thus all three channels occupied narrow bands despite a roughly 108-fold concentration range.

The in-process pH-meter results were appreciably more variable: alpha ranged from 0.05447 to 0.09022, pH_normalized from 0.24369 to 0.26075, and the precipitation proxy from 0.12959 to 0.17669. Individual pH-meter/final-assay differences sometimes changed the apparent direction of a comparison. I therefore do not interpret a single small pairwise difference as a secure mechanistic effect.

2. Empirical response surface

A compact descriptive fit to the final-assay data, using x = log10(C_T / 1 mol L^-1), is:

alpha_hat = 0.06941 - 0.00817 x
pH_normalized_hat = 0.25169 - 0.00320 x
precipitation_hat = 0.15465 + 0.00269 x

The residual RMS values are approximately 0.00588, 0.00219, and 0.00420, respectively. These equations are empirical interpolants, not universal laws. They indicate a weak tendency for dilution to raise pH and dissociation fraction, and at most a very weak tendency for the precipitation proxy to rise with concentration. The effects are small compared with the scatter and are far weaker than the concentration dependence expected for an isolated, unbuffered monoprotic weak acid.

Absolute scale was not detectably important when concentration was held fixed. Batches 5, 7, 8, and 9 all had C_T = 0.5 mol L^-1 while amount and volume increased fourfold. Their final alpha values were 0.07693, 0.06114, 0.06890, and 0.07902; pH_normalized values were 0.25602, 0.25539, 0.25086, and 0.25317; and precipitation proxies were 0.14975–0.15607. There was no monotonic amount or volume effect. The sharper scale comparison at C_T = 1 mol L^-1, batches 10 and 11, gave nearly identical alpha values, 0.069052 and 0.069003, and pH_normalized values differing by only 0.000890. This supports concentration, rather than total moles or vessel volume separately, as the most economical input coordinate, while still allowing small undetected scale effects.

3. Interpretation of the acid-base coupling

If the public dissociation fraction is interpreted conventionally as alpha = [A-]/([HA]+[A-]), the Henderson–Hasselbalch identity gives the conditional effective parameter

pKa_eff = pH - log10(alpha/(1-alpha))
          = 14 pH_normalized - log10(alpha/(1-alpha)).

Applying this identity to each final assay gives a mean pKa_eff of 4.649 and a batch range of 4.584–4.762. The relative constancy of this transformed value is much stronger than the constancy expected from a model in which pH and alpha are unrelated outputs. It suggests that the pH and dissociation channels share an acid-base ratio coordinate approximating

alpha approximately 1 / (1 + 10^(pKa_eff - pH)),

with pKa_eff near 4.65 over the tested region.

However, the data do not support the additional assumption that the nominal total loading is an isolated weak acid whose own dissociation supplies essentially all H+. Under that stronger model,

Ka = C_T alpha^2/(1-alpha).

The pKa values inferred from this mass-balance equation span about 1.92–3.76 and change systematically with C_T, rather than remaining constant. Moreover, a standalone weak acid should show much larger pH and alpha changes across 0.0185–2.0 mol L^-1. Therefore my preferred mechanism is not simply HA ⇌ H+ + A- in otherwise pure water with C_T equal to the analytical acid concentration.

A parsimonious effective description is instead:

1. The added reagent changes a nominal loading coordinate C_T.
2. A latent aqueous acid/base environment, such as a buffer, counterion reservoir, fixed formulation ratio, or synthetic benchmark response, holds pH near 3.55.
3. The dissociation channel is coupled to that pH through an effective Henderson–Hasselbalch-like ratio with pKa_eff approximately 4.65.
4. Loading produces only a small secondary shift: higher C_T modestly lowers pH and alpha.
5. The precipitation channel has a baseline near 0.153 and only a weak or unresolved loading response over the tested interval.

This model explains why pH and alpha remain mutually consistent through their ratio while failing the electroneutrality/mass-balance prediction of an isolated acid. It also explains the approximate scale invariance at fixed C_T.

4. Test of the supplied archival relationship

The supplied local archival estimate concerned 0.001 mol at 298.15 K diluted from 0.018 to 0.054 L. It predicted increases of 0.001884676 in alpha and 0.000875889 in pH_normalized and reported an effective pKa interval of 5.3294–5.4294.

Batches 1 and 2 directly tested that amount-volume pair. Their final assays showed:

Delta alpha = 0.092457 - 0.079660 = +0.012798.
Delta pH_normalized = 0.259376 - 0.252637 = +0.006738, equivalent to about +0.0943 pH unit.
Delta precipitation proxy = 0.145908 - 0.157628 = -0.011720.

The directions of the alpha and pH changes agree with the archival dilution claim, but their observed magnitudes are larger. This single final-assay pair alone is not sufficient to estimate a precise local derivative because the differences are not large relative to measurement and process scatter. The in-process pH-meter comparison even gave the opposite direction: batch 2 minus batch 1 was -0.00954 in alpha and -0.00156 in pH_normalized. That disagreement is a warning against treating the final pair as an exact law.

Other matched-amount dilution pairs did not reproduce a consistent response. Diluting 0.005 mol threefold from batch 3 to batch 4 left alpha nearly unchanged (-0.000147) while raising pH_normalized by 0.005855. Diluting 0.010 mol threefold from batch 5 to batch 6 instead lowered alpha by 0.006498 and lowered pH_normalized by 0.004777. Consequently, I retain only a weak average dilution trend; I reject a deterministic, loading-independent local dilution increment.

The archival pKa interval is more clearly inconsistent with the current channel pairing. The Henderson–Hasselbalch-derived values for batches 1 and 2 are approximately 4.600 and 4.623, and all 12 final assays lie between 4.584 and 4.762. This is far below 5.329–5.429. The most plausible interpretation is that the archival estimate was misindexed, applied to a different effective species/channel, used a different fraction convention, or belonged to a different local response surface. I would not carry its numerical pKa forward for this world.

5. Precipitation behavior and coupling

No sharp precipitation onset was observed. The final proxy remained within 0.14591–0.16075 from the lowest to the highest nominal concentration. Batch 2, the most dilute condition, had the lowest final proxy, but nearby and repeated conditions do not establish a monotonic threshold. At C_T = 0.5 mol L^-1, the four scale variants differed by only about 0.0063 across the full proxy range. Batches 10 and 11 at C_T = 1 mol L^-1 differed by 0.0120 despite similar acid-base channels, illustrating substantial unexplained or measurement-level variation.

I therefore interpret the proxy as a bounded baseline response with, at most, a small positive concentration term. There is no evidence here for a solubility-product boundary, nucleation threshold, or strong depletion of dissolved acid by precipitation. A model that feeds precipitation back strongly into pH or alpha is unnecessary in the observed region. The proxy may represent incipient precipitation, a normalized latent propensity rather than precipitated mass, or simply a response channel with a nonzero floor.

6. What changed my explanation

The batch 1–2 final-assay pair initially favored the archival qualitative claim because dilution raised both pH and alpha. The subsequent matched pairs, especially batches 3–4 and 5–6, showed that this pairwise response was not reproducible as a fixed dilution law.

The repeated C_T = 0.5 series in batches 5, 7, 8, and 9 and the C_T = 1 pair in batches 10–11 shifted my explanation toward approximate concentration control and away from independent total-mole or volume control.

Batch 12 extended the concentration range to 2 mol L^-1 yet remained in the same narrow response band: alpha 0.07460, pH_normalized 0.24934, and precipitation proxy 0.15521. This ruled against a large high-loading transition within the tested domain.

Finally, transforming all final pH and alpha pairs through Henderson–Hasselbalch produced a fairly stable pKa_eff near 4.65, whereas enforcing standalone weak-acid mass balance produced strongly concentration-dependent apparent pKa values. That contrast motivated the buffered or latent-reservoir interpretation.

7. Unidentified factors and competing explanations

Several explanations remain observationally equivalent:

• Buffered formulation: the reagent or aqueous matrix contains an unreported conjugate pair or supporting electrolyte that fixes pH and acid/base ratio.

• Fixed-composition reagent: each mole added may carry acid and conjugate base in a nearly constant ratio, making alpha approximately loading-invariant while an external reservoir controls H+.

• Activity-coefficient model: strong, concentration-dependent nonideality could weaken the apparent loading response. Nonideality alone would have to be unusually compensating across two orders of magnitude, so I regard it as less parsimonious than buffering.

• Hidden active concentration: nominal reagent moles may not equal the concentration of the species represented by the dissociation channel. A fixed active subfraction or saturation could decouple the channel from C_T.

• Synthetic coupled response surface: because this is a bounded benchmark, pH and alpha may be generated from a common latent coordinate rather than from explicit species balances. This is empirically indistinguishable from a buffered effective mechanism with the available public channels.

• Misindexed archival prior: the old pKa may refer to another species, use alpha for the protonated rather than dissociated fraction, or be attached to the wrong observable.

• Precipitation proxy floor or censoring: the approximately constant signal may represent background propensity rather than physical solid amount. No direct solid-phase measurement was available.

I cannot identify buffer capacity, ionic strength, individual species concentrations, activity coefficients, solid composition, nucleation kinetics, or whether termination changes the chemistry. The disagreement between in-process pH-meter and final-assay differences could reflect sensor noise, process evolution, or instrument-specific calibration; the design does not separate them.

8. Supported range and extrapolation limits

The empirical equations and pKa_eff estimate are supported only for water, nominal C_T = 0.0185–2.0 mol L^-1, reagent amounts 0.001–0.040 mol, volumes 0.018–0.080 L, and the near-ambient conditions actually used. They should not be extrapolated to zero loading, beyond 2 mol L^-1, other solvents, added catalysts, altered temperature, long equilibration times, or different pressure. In particular, the weak fitted precipitation slope must not be used to assert absence of a threshold outside this interval.

Within the supported range, my best effective model is a nearly buffered aqueous acid/base ratio with pKa_eff about 4.65, weak negative dependence of pH and dissociation fraction on log concentration, no detectable independent amount or volume effect at fixed concentration, and an approximately constant low precipitation proxy. The mechanistic labels remain provisional; the response relationships are better identified than the underlying chemical species.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.084312 | 0.071312 | 0.097312 |
| Q01 | pH_normalized | 0.257528 | 0.252728 | 0.262328 |
| Q01 | precipitation_signal | 0.149741 | 0.140741 | 0.158741 |
| Q02 | acid_dissociation_fraction | 0.084312 | 0.071312 | 0.097312 |
| Q02 | pH_normalized | 0.257528 | 0.252728 | 0.262328 |
| Q02 | precipitation_signal | 0.149741 | 0.140741 | 0.158741 |
| Q03 | acid_dissociation_fraction | 0.101073 | 0.077073 | 0.125073 |
| Q03 | pH_normalized | 0.264089 | 0.255089 | 0.273089 |
| Q03 | precipitation_signal | 0.144219 | 0.129219 | 0.159219 |
| Q04 | acid_dissociation_fraction | 0.09211 | 0.07211 | 0.11211 |
| Q04 | pH_normalized | 0.26058 | 0.25308 | 0.26808 |
| Q04 | precipitation_signal | 0.147172 | 0.134172 | 0.160172 |
| Q05 | acid_dissociation_fraction | 0.078227 | 0.067227 | 0.089227 |
| Q05 | pH_normalized | 0.255146 | 0.251146 | 0.259146 |
| Q05 | precipitation_signal | 0.151745 | 0.143745 | 0.159745 |
| Q06 | acid_dissociation_fraction | 0.078227 | 0.067227 | 0.089227 |
| Q06 | pH_normalized | 0.255146 | 0.251146 | 0.259146 |
| Q06 | precipitation_signal | 0.151745 | 0.143745 | 0.159745 |
| Q07 | acid_dissociation_fraction | 0.078227 | 0.067227 | 0.089227 |
| Q07 | pH_normalized | 0.255146 | 0.251146 | 0.259146 |
| Q07 | precipitation_signal | 0.151745 | 0.143745 | 0.159745 |
| Q08 | acid_dissociation_fraction | 0.109245 | 0.077245 | 0.141245 |
| Q08 | pH_normalized | 0.267287 | 0.255287 | 0.279287 |
| Q08 | precipitation_signal | 0.141527 | 0.121527 | 0.161527 |
| Q09 | acid_dissociation_fraction | 0.100281 | 0.075281 | 0.125281 |
| Q09 | pH_normalized | 0.263779 | 0.254779 | 0.272779 |
| Q09 | precipitation_signal | 0.14448 | 0.12848 | 0.16048 |
| Q10 | acid_dissociation_fraction | 0.062675 | 0.040675 | 0.084675 |
| Q10 | pH_normalized | 0.249059 | 0.241059 | 0.257059 |
| Q10 | precipitation_signal | 0.156868 | 0.140868 | 0.172868 |
| Q11 | acid_dissociation_fraction | 0.071639 | 0.060639 | 0.082639 |
| Q11 | pH_normalized | 0.252567 | 0.248567 | 0.256567 |
| Q11 | precipitation_signal | 0.153916 | 0.145916 | 0.161916 |
| Q12 | acid_dissociation_fraction | 0.076479 | 0.065479 | 0.087479 |
| Q12 | pH_normalized | 0.254462 | 0.250462 | 0.258462 |
| Q12 | precipitation_signal | 0.152321 | 0.144321 | 0.160321 |

Point estimates use the final-assay empirical relationships alpha = 0.06941 - 0.00817 log10(C_T), pH_normalized = 0.25169 - 0.00320 log10(C_T), and precipitation_signal = 0.15465 + 0.00269 log10(C_T), where C_T is final reagent amount divided by final water volume in mol L^-1. Equivalent final states receive equal predictions because the completed research supported concentration control and found no independent scale effect; no evidence established addition-order memory. The 80% intervals incorporate observed final-assay residual scatter and are widened for trace-loading and high-concentration extrapolations, where solvent baselines, activity effects, saturation, and precipitation thresholds were not identified.

### K2 retrospective

1. Assessment of the initial claims

The initial material supplied one substantive quantitative claim: for 0.001 mol at about 298.15 K, dilution from 0.018 to 0.054 L was expected to increase the dissociated fraction by 0.001884676 and pH_normalized by 0.000875889. It also supplied an effective pKa interval of 5.3294–5.4294. The remaining material descriptions were mostly scope and identity statements, not quantitative mechanistic claims: the system was described as a bounded weak-acid/precipitation slice, catalyst identities were opaque, and experimental evidence was explicitly authoritative.

The qualitative direction of the archival dilution claim received limited support from the final assays of batches 1 and 2. Dilution increased alpha from 0.079660 to 0.092457 and pH_normalized from 0.252637 to 0.259376. However, the observed changes, +0.012798 and +0.006738, were much larger than the archival increments. The corresponding in-process pH-meter readings changed in the opposite direction. Thus the correct conclusion is not that the archival law was confirmed, but that one final-assay comparison agreed in direction while the noisier paired measurement did not.

Subsequent matched-amount comparisons supplied actual counterevidence to a fixed, loading-independent dilution law. Batches 3 and 4 showed almost no alpha change on threefold dilution, whereas batches 5 and 6 changed in the opposite direction from batches 1 and 2. K1 did revise the interpretation accordingly: it retained only a weak average dilution trend and rejected a deterministic universal increment. This is different from merely saying that no contradiction was found.

The stated pKa interval was contradicted under the ordinary interpretation of the public pH and dissociation channels. K1 calculated an effective Henderson–Hasselbalch value near 4.65, with all 12 final-assay values between 4.584 and 4.762. Batches 1 and 2 gave approximately 4.600 and 4.623, respectively, far from 5.329–5.429. K1 therefore proposed misindexing, a different species, or a different fraction convention rather than retaining the original number.

Several initial framing claims remained untested. I did not test whether catalyst category, non-water solvent, temperature, pressure, or equilibration time altered the response. The archival dilution anchor was specified at 298.15 K, whereas the campaign ran near 297.2 K; the small temperature mismatch was not isolated. The statement that this was a precipitation slice was compatible with the presence of a precipitation signal, but no direct solid measurement established what that normalized proxy represented.

2. Experiments that formed or changed the interpretation

Batches 1 and 2 were chosen directly from the archival claim. They were the only experiments whose exact amount-volume pair was strongly dictated by the initial information. Their final assays initially made the archival qualitative direction look plausible, but the conflicting pH-meter pair already showed that the local effect was not secure.

Batches 3–6 were the most important challenge to that first impression. Batches 3 and 4 held amount at 0.005 mol while changing volume from 0.020 to 0.060 L; batches 5 and 6 repeated the same threefold dilution structure at 0.010 mol. Their incompatible pairwise directions changed my judgment from a simple reproducible dilution law to a weak and noisy average concentration response.

Batches 5, 7, 8, and 9 all ended at 0.5 mol L^-1 while amount and volume varied together. This series was central to the claim of approximate scale invariance. The absence of a monotonic response with absolute amount or volume supported final concentration as a more economical coordinate. Batches 10 and 11 strengthened that conclusion at 1 mol L^-1: alpha was 0.069052 versus 0.069003, and pH_normalized differed by only 0.000890.

Batch 12, at 0.040 mol in 0.020 L, was selected after the earlier results to extend concentration to 2 mol L^-1 rather than duplicate another 0.5 mol L^-1 state. Its continued narrow-band response weakened the case for a large high-loading transition within the tested domain.

The Henderson–Hasselbalch transformation across all batches, rather than any one experiment, produced the effective pKa near 4.65. Conversely, enforcing standalone weak-acid mass balance made apparent pKa vary from about 1.92 to 3.76. That contrast was what shifted the explanation toward a buffered, fixed-ratio, hidden-active-concentration, or synthetic latent-coordinate model.

Some design choices were not compelled by either the prior or established observations. Restricting all batches to water, omitting catalysts, not varying temperature or time, and choosing the particular concentration grid were unverified design assumptions intended to isolate loading and volume. The repeated 0.5 and 1 mol L^-1 scale comparisons were data-driven and mechanistically useful, but the decision to interpret order-free addition as a final-state equilibrium was not experimentally tested during the campaign. That assumption later appeared explicitly in the equal blind predictions for Q05–Q07.

3. Current competing mechanisms and identifiability

The leading effective explanation in K1 is a buffered or reservoir-controlled acid/base response. In that picture, nominal loading weakly shifts pH, while alpha is coupled to pH through an effective ratio with pKa around 4.65. This accounts for the narrow pH and alpha ranges and for their mutual Henderson–Hasselbalch consistency.

A fixed-composition reagent is a close competitor: every increment of reagent could introduce acid and conjugate base in nearly constant proportions. This would also produce approximate scale invariance and could be indistinguishable from external buffering over the observed range.

A hidden-active-concentration explanation is also viable. Nominal reagent amount may not equal the total amount represented by the dissociation channel, or the active species could saturate. This would invalidate the standalone weak-acid mass balance without requiring a literal buffer.

A synthetic latent-response explanation remains equally important. The public pH, alpha, and precipitation channels may be coupled outputs of a bounded benchmark response surface rather than explicit species balances. The experiments can identify the response surface locally, but they cannot distinguish this implementation from a chemically buffered effective model.

Concentration-dependent activity coefficients are another possibility. They could weaken the expected concentration dependence, but explaining near invariance over roughly two orders of magnitude would require substantial compensation. The current data make this less parsimonious, not impossible.

For precipitation, the main alternatives are a genuine low, approximately constant precipitation propensity; a proxy with a nonzero background floor; or a normalized signal not proportional to solid mass. Because no direct solid measurement was made and the signal never showed a clear threshold, these remain unresolved.

The experiments did distinguish these explanations from a simple isolated monoprotic acid whose own dissociation supplies essentially all H+. That model failed the combined mass-balance and concentration-response check. They also provided evidence against strong independent amount or volume effects at fixed concentration. They did not distinguish external buffering from fixed reagent composition, hidden active fraction, activity compensation, or a synthetic shared latent coordinate. They likewise did not establish whether addition order, elapsed time, or termination had memory effects.

4. One additional complete experiment

If only one legal complete experiment were available, I would prepare 0.000001 mol of reagent in 0.080 L of water, measure with the pH meter before termination, terminate, and obtain the required final assay. I would not execute it here. This is a prospective choice, and no blind-prediction truth has been supplied.

This extreme-dilution experiment would target the largest unresolved separation among mechanisms. It would also provide paired in-process and final measurements, which is important because batches 1 and 2 showed instrument-dependent dilution directions.

If pH_normalized and alpha remained close to the campaign bands, approximately 0.25–0.27 and 0.07–0.12, that would strongly favor a background buffer, fixed formulation, hidden concentration floor, or latent bounded response over an isolated acid model. A nearly unchanged precipitation proxy would support the proxy-floor interpretation.

If pH moved substantially toward neutral water while alpha approached a much larger dissociated fraction, the buffered narrow-band extrapolation in K1 would be weakened and an ordinary limiting-dilution acid response would become more credible. It would also show that the log-linear model used for Q03, Q08, and Q09 should bend at trace loading.

If the final assay remained in the narrow band but the pre-termination pH-meter result did not, I would prioritize instrument or termination-state effects rather than infer a new acid equilibrium directly. If the precipitation signal collapsed toward zero while pH and alpha remained buffered, I would separate precipitation from the latent acid/base baseline. If all channels became missing or clipped, the main conclusion would concern the measurement boundary rather than chemistry.

One experiment could reveal a limiting regime, but it could not by itself discriminate a real buffer from a synthetic latent response. A blank or a titration series would be better for that purpose, but those require more than one complete experiment or a different measurement contract.

5. Tradeoff between mechanistic identifiability and operational score

The campaign was designed primarily for characterization rather than score maximization. I used matched amount-volume pairs, repeated concentrations at different absolute scales, and a high-concentration boundary point. Those choices improved identifiability of concentration versus amount and volume, but several conditions had relatively low equilibrium_confidence diagnostics and therefore were not attractive under the scalar scoring weights.

For example, batch 3 had the highest final equilibrium_confidence among the campaign batches, approximately 0.565, near 0.25 mol L^-1. Nevertheless, I continued with 0.5, 1, and 2 mol L^-1 conditions to test scale invariance and boundary behavior. That was an explicit sacrifice of likely score for mechanistic coverage. Similarly, batch 2 was sealed as the recommended replay batch because it was the diluted member of the exact archival pair, not because it had the best scalar score or diagnostic confidence.

There was no deliberate yield or product optimization, consistent with the research goal. I did not use catalysts or alternative solvents to search for a higher score. This protected interpretability of the loading-volume study but sacrificed any opportunity to discover material categories with better diagnostic scores.

The design nevertheless left important identifiability on the table. All batches used water and approximately the same temperature and process history. The concentration grid was much broader than the number of genuine replicates. More exact replication at the archival pair would have improved uncertainty estimation, while a trace-loading or time-course condition would have separated competing mechanisms more sharply. Thus the campaign favored one narrow form of identifiability—loading versus volume—over broader mechanism identification.

6. Underused evidence and weaknesses in the blind predictions

The paired pH-meter and final-assay measurements were not fully exploited statistically. K1 noted their disagreements, especially for batches 1 and 2, but did not construct an explicit hierarchical model with separate instrument noise, batch variation, and possible termination effects. Consequently, the regression residuals used for prediction mixed several uncertainty sources.

The final-assay raw signal, mass-balance metadata, calibration information, and any channel covariance were also not analyzed in detail. K1 relied primarily on processed estimates. The equilibrium_residual channel was mostly zero in final assays, potentially because of clipping or construction, and was not useful mechanistically. The equilibrium_confidence channel was correctly excluded as personal confidence, but its systematic variation with condition might still have contained information about where the environment considered the equilibrium representation well behaved.

The repeated 0.5 mol L^-1 series and 1 mol L^-1 pair were used qualitatively but not incorporated into an explicit model separating concentration and absolute scale. Likewise, the precipitation channel was fitted with a simple log-concentration slope despite evidence that most of its variation could be background or noise.

The least reliable sealed predictions are Q08, Q03, and Q09 at trace loading, followed by Q10 at approximately 6.67 mol L^-1. Q08 extrapolates more than three orders of magnitude below the lowest observed concentration, and Q10 exceeds the observed maximum by more than a factor of three. Their intervals may be too narrow because they extend a log-linear trend without a structural allowance for neutral-water behavior, activity breakdown, saturation, missingness, or a precipitation threshold.

Q05–Q07 also deserve caution. Their equal point predictions follow the final-state equilibrium interpretation, but no campaign experiment varied addition order while holding final state fixed. Their intervals may therefore be too narrow if transient precipitation, irreversible aggregation, or termination memory exists. Q01 and Q02 are only slightly outside the observed concentration range and are less problematic, while Q11 and Q12 are genuine interpolations.

These limitations are partly inconsistent with the strength of the predictive intervals but not with the text of K1. K1 explicitly limited support to 0.0185–2.0 mol L^-1 and warned against extrapolating to zero loading or beyond 2 mol L^-1. The blind task forced predictions outside that range, and the rationale acknowledged extrapolation, but the numerical widening probably did not fully represent the structural uncertainty described in K1. In particular, Q08 and Q10 should be read as conditional predictions under continuation of the fitted effective response, not as well-validated 80% coverage statements across all plausible mechanisms.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 2 for replay because it directly anchored the archival dilution comparison. It was an evidentiary recommendation, not a claim that its recipe was operationally optimal. Batch 2 was a single realization, its pH-meter and final-assay changes relative to batch 1 disagreed in direction, and its final equilibrium_confidence diagnostic was not the campaign maximum.

Repeatability should be tested by exact independent replication of batches 1 and 2, including both instruments and the same operation sequence. The relevant outcome is not merely whether the batch-2 point estimate recurs, but whether the batch-2 minus batch-1 contrast has a stable sign and magnitude across replicates.

Local robustness should be tested with small perturbations around 0.001 mol and 0.054 L, preferably varying amount and volume separately. That would reveal whether batch 2 lies on a smooth local response surface or whether its apparent dilution benefit was dominated by noise. Temperature should also be controlled near both the campaign condition and the archival 298.15 K anchor.

Cross-material robustness would require repeating the local design in the other permitted solvents and, if mechanistically relevant, with the opaque catalyst categories. No current evidence supports transferring the water-derived pKa_eff or precipitation baseline to ethanol, acetonitrile, toluene, or catalyst-containing systems. Cross-world generalization is even less justified because the proposed buffer or latent response may be specific to this bounded benchmark world.

Finally, even a sample with the highest observed scalar score would only be the sample maximum among tested conditions. It would not be proven optimal without a defined optimization target, adequate neighborhood search, replication, and robustness analysis. Batch 2 was not even selected as the sample maximum; it was selected for interpretive relevance. The sealed recommendation should therefore be described as the most useful completed batch for replaying the archival test, not as a demonstrated optimum.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `4.65`; 80% interval `[4.6, 4.7]`.

Using the declared relation pH = 14 × pH_normalized and interpreting acid_dissociation_fraction as alpha = [A-]/([HA]+[A-]), the 12 final assays give pKa_eff = pH - log10(alpha/(1-alpha)) with mean 4.649 and observed batch range 4.584–4.762. The 80% interval includes assay scatter and modest model uncertainty. This is an effective channel-level pKa, not an identified thermodynamic constant: buffering, activity effects, hidden active concentration, or a shared synthetic latent response remain confounded. The archival interval 5.329–5.429 is not supported by the acquired final-assay pairing.

Path-dependence assessment: `indeterminate`.

The source campaign did not contain matched batches with identical final amount and volume but different staged-addition orders, so reproducible path dependence was not directly tested. Batches 5, 7, 8, and 9 reached the same 0.5 mol L^-1 concentration at different absolute scales, and batches 10 and 11 similarly matched at 1.0 mol L^-1; their narrow responses support approximate final-state concentration control, but scale invariance is not evidence about addition order. Final-state dominance is therefore a plausible conjecture, not an experimentally identified path law.

Dissociation-precipitation assessment: `continuous`.

Supported range: Supported only for water near ambient temperature, nominal reagent amounts of 0.001–0.040 mol, volumes of 0.018–0.080 L, and nominal concentrations of 0.0185–2.0 mol L^-1. Within this range, dissociation and the precipitation proxy varied smoothly and narrowly; no reproducible threshold was observed.

Competing explanation: The precipitation proxy may have a nonzero background floor or be dominated by measurement/process scatter, which could conceal a genuine threshold outside or even weakly within the sampled region. It may also represent latent precipitation propensity rather than precipitated mass.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.0992468 | 0.616667 | 0.034 | 0.914539 |
| pH_normalized | 0.0190089 | 0.633333 | 0.0125167 | 0.157434 |
| precipitation_signal | 0.0364757 | 0.616667 | 0.023 | 0.325843 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
