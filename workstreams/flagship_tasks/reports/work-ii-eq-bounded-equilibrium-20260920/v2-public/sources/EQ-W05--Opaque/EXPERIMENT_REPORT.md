# EQ-W05--Opaque — final public report

World `EQ-W05`; prior arm `Opaque`; status `completed`. The effective result came from `attempt-01`.

## Source campaign

The campaign contains 12/12 completed batches and 72 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.305592 | 0.0575142 | 0.152494 | 0 |
| 2 | 0.3074 | 0.0549095 | 0.152068 | 0 |
| 3 | 0.30344 | 0.0692742 | 0.146243 | 0 |
| 4 | 0.304382 | 0.0679346 | 0.155131 | 0.00047714 |
| 5 | 0.300925 | 0.0663952 | 0.155585 | 0.00140167 |
| 6 | 0.301947 | 0.0585161 | 0.154772 | 0.00572561 |
| 7 | 0.303098 | 0.0747966 | 0.155817 | 0.00837261 |
| 8 | 0.303472 | 0.0653996 | 0.150851 | 0 |
| 9 | 0.302139 | 0.0696015 | 0.155099 | 0.000671668 |
| 10 | 0.30422 | 0.0642419 | 0.155676 | 0 |
| 11 | 0.305321 | 0.0616056 | 0.151301 | 0 |
| 12 | 0.302687 | 0.0699228 | 0.155604 | 0.00080387 |

## Sealed scientific account

### K1 report

Mechanistic report

1. Experimental basis

I completed 12 aqueous batches using water only, with no catalyst, heating, or deliberate waiting period. The design crossed four reagent loadings (0.004, 0.012, 0.024, and 0.040 mol) with three final nominal liquid volumes (0.030, 0.060, and 0.090 L). Thus the final nominal loading concentration C = n/V covered 0.0444 to 1.333 mol/L, a 30-fold range. Each batch was measured once with the pH meter at half its final water volume, diluted twofold with water, terminated, and measured by final assay. The final-assay endpoints are the most comparable evidence because every design cell used the same instrument and stage.

2. Main empirical conclusion

Within the tested domain, the observable equilibrium state is approximately buffered or plateaued rather than controlled strongly by nominal reagent concentration. The final pH, reported acid-dissociation fraction, and public precipitation proxy changed little across the 10-fold loading range, threefold volume range, and 30-fold concentration range.

Across the 12 final assays:
- mean pH_normalized = 0.30372, with range 0.30092-0.30740 and across-cell RMS spread 0.00172;
- because pH_normalized = pH/14, this corresponds to mean pH 4.252 and observed range 4.213-4.304;
- mean acid_dissociation_fraction = 0.06501, with range 0.05491-0.07480 and RMS spread 0.00564;
- mean precipitation_signal = 0.15339, with range 0.14624-0.15582 and RMS spread 0.00279.

Those spreads are comparable to, or smaller than, the declared final-assay noise scales (0.002, 0.006, and 0.006 respectively). A constant-response model is therefore an adequate description of the final data. This does not prove exact invariance; it means that any systematic effects are weak relative to the resolution and replication available here.

3. Effective quantitative relationship

A descriptive log-linear fit over only the tested range was

  y = y0 + beta_n ln(n/0.01465 mol) + beta_V ln(V/0.05451 L).

The fitted relationships were:

  pH_normalized = 0.30372 - 0.000694 ln(n/0.01465) - 0.001444 ln(V/0.05451),

  acid_dissociation_fraction = 0.06501 + 0.002886 ln(n/0.01465) - 0.000054 ln(V/0.05451),

  precipitation_signal = 0.15339 + 0.001602 ln(n/0.01465) - 0.001864 ln(V/0.05451).

Approximate 95% intervals for the loading and volume slopes were, respectively:
- pH_normalized: beta_n about [-0.00198, 0.00059], beta_V about [-0.00389, 0.00100];
- dissociation fraction: beta_n about [-0.00154, 0.00731], beta_V about [-0.00848, 0.00837];
- precipitation proxy: beta_n about [-0.00038, 0.00358], beta_V about [-0.00563, 0.00190].

All intervals include zero. The fitted response to doubling volume at fixed loading is only about -0.00100 in normalized pH, -0.000038 in dissociation fraction, and -0.00129 in precipitation signal. These coefficients should be treated as local descriptive bounds, not established laws.

4. Batch-level observations that shaped the interpretation

The extreme final concentrations did not produce the response expected for an ordinary unbuffered weak acid. Batch 3 contained 0.004 mol in 0.090 L (C = 0.0444 mol/L) and gave pH_normalized 0.30344, dissociation fraction 0.06927, and precipitation signal 0.14624. Batch 10 contained 0.040 mol in 0.030 L (C = 1.333 mol/L) and gave 0.30422, 0.06424, and 0.15568. Despite a 30-fold concentration difference, normalized pH differed by only 0.00078, while the other responses did not move monotonically in the simple weak-acid direction.

Matched-concentration comparisons also showed little independent dependence on total amount or volume. Batches 1 and 6 both had final C = 0.1333 mol/L but differed threefold in both loading and volume. Batch 1 gave pH_normalized 0.30559, dissociation 0.05751, and precipitation 0.15249; batch 6 gave 0.30195, 0.05852, and 0.15477. Similarly, batches 4 and 8 both had C = 0.400 mol/L. Their results were 0.30438/0.06793/0.15513 and 0.30347/0.06540/0.15085, respectively. These differences are small on the declared assay scales and do not reveal a separate total-loading effect.

At fixed 0.040 mol loading, batches 10-12 increased final volume from 0.030 to 0.060 to 0.090 L. Dissociation fractions were 0.06424, 0.06161, and 0.06992; precipitation signals were 0.15568, 0.15130, and 0.15560. The nonmonotonic sequence caused me to reject a strong simple dilution law for these endpoints.

Batch 8 was selected as the replay anchor because it was a representative mid-range case with an explicit twofold dilution. Before dilution, its pH-meter values were pH_normalized 0.30364, dissociation 0.08627, and precipitation 0.12009. After dilution and termination, its final assay gave 0.30347, 0.06540, and 0.15085. This shows stable pH but apparently changing secondary channels. However, it cannot by itself identify a dilution effect because dilution, termination/stage, and instrument identity all changed together.

Across all 12 paired measurements, the mean final-minus-intermediate changes were -0.000205 in normalized pH, -0.01061 in dissociation fraction, and -0.00501 in precipitation signal. Individual directions were inconsistent. Intermediate precipitation ranged from 0.12009 to 0.18648, much more widely than final precipitation, and the pH meter has larger declared noise for these secondary channels. I therefore modified the initial interpretation from a direct within-batch dilution response to an instrument/stage-confounded observation. Only the nearly zero average pH change is robustly compatible with dilution-resistant buffering.

5. Chemical interpretation

A useful minimal mechanism is a buffered weak-acid equilibrium coupled to a bounded precipitation-related reporter:

  HA <=> H+ + A-

  alpha = a(A-)/(a(HA) + a(A-))
        approximately Ka/(Ka + a(H+))

plus an unspecified precipitation equilibrium such as

  dissolved species <=> solid-associated species,

with precipitation_signal = g(saturation state, solid fraction, or reporter response), where g is bounded and may plateau.

The observations suggest that an unobserved reservoir fixes hydrogen-ion activity near pH 4.25. Once hydrogen-ion activity is clamped, alpha can also remain near a constant value. If a precipitation or solubility equilibrium additionally clamps one or more dissolved activities, adding more nominal reagent can mainly change an unobserved reservoir or solid-associated amount while leaving pH and the normalized proxy nearly unchanged. Because the precipitation channel is explicitly a bounded proxy, constancy of the signal does not imply constancy of actual precipitate mass.

If the reported alpha is inserted into the monoprotic Henderson-Hasselbalch relation, an effective conditional value can be defined:

  pKa_eff = pH + log10((1-alpha)/alpha).

The 12 final assays give mean pKa_eff about 5.412, with individual values 5.336-5.539. This is a compact empirical coupling between the two reported channels. It is not an identified molecular pKa, because activities, ionic strength, species identity, and the mapping of the reported fraction are unknown.

6. Why a naive unbuffered-acid model is inadequate

If the anonymous limiting reagent itself were simply monoprotic HA and alpha were literally the fraction of that total concentration dissociated, electroneutrality would require approximately [H+] = C alpha in an otherwise simple solution. That fails by large factors.

For batch 3, C alpha = 0.00308 mol/L, whereas the measured pH implies [H+] = 5.65e-5 mol/L, a factor of about 55 lower. For batch 10, C alpha = 0.0857 mol/L while pH implies 5.51e-5 mol/L, a factor of about 1,555 lower. The disagreement grows with loading. Therefore at least one of the naive assumptions is false: alpha may describe a reporter pool rather than all loaded reagent; counterions or buffering species may dominate charge balance; activities may be strongly transformed; precipitation may remove relevant species; or the public channels may be separately normalized latent observables.

This mass-balance contradiction is stronger mechanistic evidence than the superficially plausible pKa_eff calculation. I retain pKa_eff only as an effective channel relationship.

7. Precipitation coupling

The final precipitation proxy was essentially pinned near 0.153. Its fitted loading coefficient was weakly positive and its volume coefficient weakly negative, which is the sign pattern expected for a concentration-driven response, but neither coefficient was distinguishable from zero. The lowest-concentration point, batch 3, had the lowest final signal (0.14624), while several higher-concentration cases were near 0.155-0.156. This is compatible with a shallow approach to a plateau, but one low point is insufficient to identify a threshold, exponent, or solubility product.

Thus my preferred description is

  precipitation_signal approximately 0.153 within the sampled domain,

possibly with a small increasing function of concentration that is already close to saturation. I cannot infer solid mass, nucleation kinetics, crystal identity, or stoichiometry from this proxy.

8. Equilibration and residuals

Final equilibrium_residual averaged 0.00145 and ranged from 0 to 0.00837; six final values were exactly zero at the reported precision. This supports internal consistency with the environment's equilibrium representation. It does not establish that a real chemical equilibrium was independently verified, especially because no time course or wait-duration perturbation was conducted.

The reported equilibrium_confidence values are environment diagnostics. I did not use them as statistical confidence in this report or as evidence for a particular mechanism.

9. Reasonable competing explanations

Several models remain observationally equivalent:

A. Buffer-reservoir model: an unreported acid/base reservoir dominates pH, and the reported dissociation fraction belongs to a small reporter pool. This naturally gives nearly constant pH and alpha.

B. Precipitation-buffer model: dissolution/precipitation clamps dissolved activities while extra total loading changes an unmeasured solid-associated inventory. A saturated precipitation reporter then remains nearly constant.

C. Bounded-observable model: all three public channels are nonlinear, normalized transforms of latent variables and happen to lie on broad plateaus. This requires no literal chemical buffer, although it is less chemically specific.

D. Hidden-background or ionic-strength model: a large fixed background electrolyte controls activities and charge balance. Changes in analytical concentration then have weak effects on activity-based pH and alpha.

E. Instrument/stage model for the paired differences: the pH-meter and final assay have different noise and channel calibrations, and termination may alter the reported state. This can explain why intermediate dissociation and precipitation scatter much more than final values without invoking real dilution kinetics.

F. Unresolved threshold model: the sampled concentrations may all lie above a buffering or precipitation onset. Strong concentration dependence could exist below 0.0444 mol/L or outside the tested volume/loading domain.

The current data distinguish these explanations from a simple unbuffered monoprotic acid, but do not distinguish them from one another.

10. Scope and uncertainty

The conclusions apply only to water, approximately ambient temperature near 297 K, anonymous reagent loadings 0.004-0.040 mol, nominal final volumes 0.030-0.090 L, and nominal final concentrations 0.0444-1.333 mol/L under the tested operation sequence. They should not be extrapolated to other solvents, catalysts, temperatures, ionic backgrounds, much lower concentration, or long equilibration times.

There was one final assay per factorial cell and no same-condition replicate. Consequently, interaction terms, nonlinear thresholds, batch variability, and small slopes are poorly identifiable. The before/after dilution comparison is confounded by instrument and process stage. No direct speciation, dissolved concentration, solid mass, turbidity calibration, ionic strength, counterion content, or kinetic time series was measured. No task-specific material dossier or explicit archival local equation was supplied, so there was no numerical prior law to validate verbatim.

11. Most defensible working model and testable implication

For prediction strictly inside the observed domain, I would use the constant or weak log-linear endpoint model, centered at:

  pH_normalized approximately 0.304,
  acid_dissociation_fraction approximately 0.065,
  precipitation_signal approximately 0.153.

The mechanistic gloss is: a hidden buffer and/or phase reservoir clamps hydrogen-ion and dissolved-species activities, while the public precipitation channel is a bounded proxy near a plateau. The principal testable implication is that moderate changes in loading or twofold dilution within the studied range should alter these final endpoints by less than roughly one assay-noise scale. A strong monotonic Henderson-Hasselbalch-plus-mass-balance response to nominal C would contradict this working model. This is an interpolation claim only; behavior outside the measured bounds remains unknown.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.065 | 0.048 | 0.085 |
| Q01 | pH_normalized | 0.304 | 0.298 | 0.311 |
| Q01 | precipitation_signal | 0.135 | 0.112 | 0.155 |
| Q02 | acid_dissociation_fraction | 0.065 | 0.048 | 0.085 |
| Q02 | pH_normalized | 0.304 | 0.298 | 0.311 |
| Q02 | precipitation_signal | 0.135 | 0.112 | 0.155 |
| Q03 | acid_dissociation_fraction | 0.157 | 0.09 | 0.25 |
| Q03 | pH_normalized | 0.334 | 0.316 | 0.356 |
| Q03 | precipitation_signal | 0.009 | 0 | 0.032 |
| Q04 | acid_dissociation_fraction | 0.065 | 0.03 | 0.14 |
| Q04 | pH_normalized | 0.304 | 0.296 | 0.322 |
| Q04 | precipitation_signal | 0.066 | 0.025 | 0.115 |
| Q05 | acid_dissociation_fraction | 0.065 | 0.052 | 0.079 |
| Q05 | pH_normalized | 0.304 | 0.299 | 0.309 |
| Q05 | precipitation_signal | 0.151 | 0.14 | 0.161 |
| Q06 | acid_dissociation_fraction | 0.065 | 0.052 | 0.079 |
| Q06 | pH_normalized | 0.304 | 0.299 | 0.309 |
| Q06 | precipitation_signal | 0.151 | 0.14 | 0.161 |
| Q07 | acid_dissociation_fraction | 0.065 | 0.052 | 0.079 |
| Q07 | pH_normalized | 0.304 | 0.299 | 0.309 |
| Q07 | precipitation_signal | 0.151 | 0.14 | 0.161 |
| Q08 | acid_dissociation_fraction | 0.413 | 0.2 | 0.7 |
| Q08 | pH_normalized | 0.376 | 0.335 | 0.43 |
| Q08 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q09 | acid_dissociation_fraction | 0.141 | 0.07 | 0.27 |
| Q09 | pH_normalized | 0.331 | 0.305 | 0.36 |
| Q09 | precipitation_signal | 0.011 | 0 | 0.04 |
| Q10 | acid_dissociation_fraction | 0.065 | 0.045 | 0.088 |
| Q10 | pH_normalized | 0.304 | 0.296 | 0.312 |
| Q10 | precipitation_signal | 0.155 | 0.141 | 0.168 |
| Q11 | acid_dissociation_fraction | 0.065 | 0.055 | 0.075 |
| Q11 | pH_normalized | 0.304 | 0.3 | 0.308 |
| Q11 | precipitation_signal | 0.155 | 0.146 | 0.163 |
| Q12 | acid_dissociation_fraction | 0.065 | 0.055 | 0.075 |
| Q12 | pH_normalized | 0.304 | 0.3 | 0.308 |
| Q12 | precipitation_signal | 0.153 | 0.144 | 0.162 |

Predictions use the sealed research interpretation without additional experiments. Within the observed domain, final-assay pH_normalized, acid_dissociation_fraction, and precipitation_signal were adequately described by plateaus near 0.304, 0.065, and 0.153. For low-concentration extrapolation, I used an effective monoprotic weak-acid relationship with conditional pKa near 5.41, joined to the observed pH/dissociation plateau. For precipitation, I used a bounded saturating concentration response consistent with the slight depression at the lowest measured concentrations, with an approximate half-saturation concentration near 0.0022 mol/L and an upper signal near 0.155. Batches with identical final amount and volume receive identical predictions because no path dependence was identified. Intervals combine final-assay noise, observed variation, and increasingly large structural uncertainty outside the measured loading and concentration ranges. The environment's equilibrium_confidence diagnostic was not treated as inferential confidence.

### K2 retrospective

1. Initial claims: supported, challenged, or untested

The initial material packet contained no substantive task-specific mechanistic claim. It explicitly said that no nominal property dossier was supplied, the reagent was anonymous, and experimental evidence was authoritative. The research brief likewise had prior_record = null. Therefore there was no archival equilibrium equation, pKa, solubility threshold, or precipitation law that I could directly confirm or refute. In K1 I stated this explicitly: “No task-specific material dossier or explicit archival local equation was supplied.”

Several contractual statements were definitions rather than hypotheses: pH_normalized = pH/14; acid dissociation and precipitation_signal are bounded observables; water was the selected real reference solvent; and equilibrium_confidence was an environment diagnostic rather than epistemic confidence. The observations were consistent with those definitions, but this is not empirical validation of a mechanism.

The initial research framing did imply that loading, volume or dilution, pH, dissociation, and precipitation might be related. My factorial results did not show a strong relationship within the sampled range. That is evidence against a large monotonic effect there, but not against effects at lower loading or outside the range.

A simple unbuffered monoprotic-acid interpretation was not supplied initially; it was a candidate explanation I examined later. K1 identified direct counterevidence: in batch 3, C alpha was about 55 times the hydrogen-ion concentration implied by pH, and in batch 10 it was about 1,555 times larger. I did revise the interpretation in K1 by rejecting the claim that the reported alpha was simply the dissociated fraction of the entire nominal reagent concentration. I did not leave that counterevidence unacknowledged.

By contrast, the buffered-reservoir, precipitation-buffer, hidden-electrolyte, and bounded-observable explanations encountered no direct contradiction, but they were not positively identified. “No contradiction found” should not be confused with “mechanism established.” No direct solid measurement, background composition measurement, or activity measurement was made.

2. Experiments that formed or changed my judgment

The main design was a 4 x 3 factorial crossing 0.004, 0.012, 0.024, and 0.040 mol with final water volumes of 0.030, 0.060, and 0.090 L. This choice came primarily from the stated research goal and available stock budget, not from prior evidence about where a mechanistic transition lay. Choosing water followed the “aqueous-equilibrium” brief. Omitting catalysts followed the same logic: catalyst effects were not central to the commissioned acid-dissociation and precipitation question.

The experiments that most strongly shaped K1 were:

- Batches 3 and 10 provided the widest final concentration contrast: 0.0444 versus 1.333 mol/L. Their final pH_normalized values were 0.30344 and 0.30422, dissociation fractions 0.06927 and 0.06424, and precipitation signals 0.14624 and 0.15568. The near-constant pH across a 30-fold concentration span drove the plateau or buffering interpretation.

- Batches 1 and 6 both ended at 0.1333 mol/L but differed threefold in amount and volume. Their dissociation fractions were 0.05751 and 0.05852, and precipitation signals were 0.15249 and 0.15477. Batches 4 and 8 formed another equal-concentration comparison at 0.400 mol/L. These comparisons weakened the case for a large independent total-amount or volume effect.

- Batches 10-12 held the amount at 0.040 mol while varying final volume from 0.030 to 0.090 L. The dissociation sequence 0.06424, 0.06161, 0.06992 and precipitation sequence 0.15568, 0.15130, 0.15560 were nonmonotonic. This caused me to reject a strong simple dilution law within that region.

- Batch 8 changed how I treated the within-batch measurements. Its pH_normalized was nearly unchanged across the nominal twofold dilution, but dissociation changed from 0.08627 to 0.06540 and precipitation from 0.12009 to 0.15085. Because the first reading came from the pH meter and the second from the final assay after termination, I concluded that dilution, stage, and instrument were confounded. I therefore did not treat those changes as clean causal dilution effects.

Some choices rested on unverified guesses. In particular, I assumed that 0.004-0.040 mol and 0.030-0.090 L would span an informative response region. The blind questions later revealed that trace loadings down to 1e-6 mol were considered relevant, but no truth has been disclosed. My experimental range may therefore have sampled only a plateau. I also guessed that measuring each batch at half-volume and then after dilution would efficiently reveal dilution response. That design was weaker than intended because it changed the instrument and process stage at the same time.

3. Leading competing mechanisms and what is identifiable

The principal explanations remain:

A. A chemical buffer or hidden acid/base reservoir clamps hydrogen-ion activity near pH 4.25. The reported dissociation fraction then belongs to a reporter or sub-pool rather than to all nominal reagent.

B. A dissolution/precipitation reservoir clamps dissolved activities while added material changes an unobserved solid or reservoir inventory. The bounded precipitation signal is already near saturation.

C. The public observables are nonlinear bounded transformations with broad plateaus. Apparent buffering could therefore be a measurement or world-mapping property rather than a literal chemical buffer.

D. A large fixed background electrolyte controls activity coefficients and charge balance, making analytical concentration a poor proxy for chemical activity.

E. The system is concentration-dependent below the studied range but had already crossed a threshold in every completed experiment.

F. Some of the intermediate/final disagreement reflects instrument or termination-stage differences rather than chemistry.

The study can distinguish these collectively from the naive model in which nominal reagent is the only monoprotic acid, alpha directly measures its dissociated fraction, and [H+] is approximately C alpha. That model fails the observed mass-balance check. The study also constrains any smooth loading or volume dependence to be small within the final measured domain.

It cannot distinguish A from B, C, or D. It cannot determine whether a low-loading transition exists, whether precipitation_signal measures solid quantity or only saturation state, or whether addition order matters. It also cannot separate instrument effects from termination effects in the paired observations. K1 correctly presented these as observationally equivalent explanations rather than selecting one as proven.

4. One additional complete experiment I would choose

If one legal complete experiment were available, I would use 0.075 L water and 1e-5 mol reagent, giving 1.33e-4 mol/L. I would measure once with the pH meter without changing composition, terminate, and then obtain the required final assay at essentially the same composition. I would not actually execute it here.

This condition is preferable because it lies far below the completed concentration range and near where the later weak-acid extrapolation predicted a transition. Measuring the same nominal state with both instruments would also reduce the instrument-versus-dilution confounding present in the original design. The small pH-meter sample consumption would need to be included in the nominal final volume calculation.

Possible outcomes would alter my view as follows:

- If the final assay remained near pH_normalized 0.304, dissociation 0.065, and precipitation 0.153, the broad plateau or fixed-background explanation would gain support, and my low-concentration blind predictions for Q03 and related trace cases would be undermined.

- If normalized pH rose toward approximately 0.33, dissociation rose toward roughly 0.15, and precipitation fell close to zero, that would support a low-concentration weak-acid transition plus a saturating precipitation response. It would not by itself prove a molecular weak-acid mechanism.

- If pH changed but dissociation did not follow the effective pKa relationship, the two channels would likely be separately transformed observables or would refer to different pools.

- If precipitation changed strongly while pH and dissociation stayed on their plateaus, precipitation would appear to have a distinct concentration scale rather than being tightly coupled to acid dissociation.

- If the pH-meter and final assay disagreed systematically at unchanged composition, instrument or termination-stage effects would become a leading explanation for the original paired discrepancies.

One experiment still could not fully distinguish amount from concentration. A second matched-concentration or matched-amount condition would be required for that.

5. Tradeoff between mechanistic identifiability and operational score

The research goal was characterization, not yield or score optimization. I therefore prioritized a factorial loading-volume design, equal-concentration comparisons, and within-batch dilution attempts. I did not vary catalysts, solvents, or conditions merely to raise the scalar score. I also did not interpret equilibrium_confidence as a target to maximize.

This sacrificed possible operational score because many resources were spent on deliberately different loading and volume combinations rather than repeatedly using whichever early condition happened to score best. The selected batch 8 was chosen as an evidentiary anchor, not because it had been demonstrated to maximize the diagnostic score.

However, the design did not maximize identifiability as effectively as intended. All four loadings were high enough that the final responses were nearly flat, and the stock budget was exhausted without probing trace loading. Every nonfinal measurement was used in a dilution sequence where instrument, stage, and volume changed together. A same-state cross-instrument comparison or a logarithmic low-loading series would have been more informative.

There is no clear instance where I knowingly sacrificed mechanistic identifiability to optimize the score. The larger failure was a design guess: I spent substantial coverage on a plateau because I had not first located its boundary. Conversely, I did sacrifice potential score optimization for breadth, but that was appropriate to the stated scientific objective.

6. Underused evidence and weakest blind predictions

Several evidence sources were not fully exploited:

- I relied on processed estimates and did not inspect the complete final characterization artifact or raw spectral and mass-balance fields. Those data might have revealed whether the precipitation proxy, channel saturation, or missingness behaved differently across conditions.

- The intermediate measurements contained potentially useful information, but the systematic instrument/stage confounding made them hard to interpret. Their greater scatter was summarized but not modeled jointly with instrument-specific noise.

- Equilibrium_residual was low, but I used it only as an internal-consistency indicator. That was cautious, although a more explicit relation between residual and the endpoint deviations might have been explored.

- The factorial design could estimate only simple main effects reliably. With one final assay per cell, nonlinearities and interactions were not identifiable.

- I did not directly test addition order, time dependence, or replicate variability, even though Q05-Q07 later required path-independence predictions.

The least reliable blind predictions are Q08, Q03, Q09, and Q04 because they extrapolate orders of magnitude below the observed loading range. Q10 is also weak because 6.67 mol/L is five times the highest tested concentration and may encounter a new boundary.

Some submitted 80% intervals were too narrow relative to K1's stated model uncertainty:

- Q03 predicted pH_normalized 0.334 with interval 0.316-0.356 and dissociation 0.157 with interval 0.09-0.25. Those intervals exclude or nearly exclude the empirical plateau values, even though K1 explicitly said that a bounded-observable or fixed-reservoir model remained equivalent. This was an unjustified commitment to the weak-acid extrapolation.

- Q08 predicted dissociation 0.413 with interval 0.20-0.70 and precipitation 0.003 with interval 0-0.025. These intervals exclude both the observed dissociation plateau near 0.065 and precipitation plateau near 0.153. That is inconsistent with K1's statement that the behavior below 0.0444 mol/L was unknown.

- Q09 had the same structural problem, although its intervals were somewhat broader.

- The Q01 and Q02 precipitation interval of 0.112-0.155 relied heavily on a fitted saturating curve inferred from very small differences among noisy plateau observations. It should have allowed more probability for a constant response.

- Q10's intervals acknowledged extrapolation but were still narrow for an entirely untested high-concentration regime.

Q12 is the most defensible prediction because it is an interior interpolation. Q11 and the endpoint totals of Q05-Q07 are also relatively close to the studied concentration range, but the path-independence claim for Q05-Q07 was not experimentally tested. No prediction truth has yet been supplied, so these are prospective criticisms of calibration, not post hoc reactions to correctness.

7. Limitations of the sealed recommendation

The sealed recommendation selected completed experiment 8: 0.024 mol reagent, initially 0.030 L water, followed by dilution to a nominal 0.060 L final volume. It was selected because it was a representative mid-range case with both an intermediate pH-meter reading and a final assay, not because it was the highest-scoring batch.

Its limitations are substantial. It has only one independent realization, its before/after comparison is instrument- and stage-confounded, and its precipitation readings changed from 0.12009 to 0.15085. It therefore provides an informative replay target but not a clean estimate of dilution causality. It also samples the response plateau and is poorly suited to locating the low-loading boundary.

Repeatability should be tested by preregistered independent repetitions of the exact batch-8 sequence, retaining every result and estimating between-batch variation separately from declared instrument noise. Same-state pH-meter and final-assay measurements would help isolate modality effects.

Local robustness should be tested around the selected condition, for example by small independent perturbations of amount, final volume, dilution order, and equilibration time. A neighborhood such as approximately 0.020-0.028 mol and 0.050-0.070 L would determine whether the result is stable or merely one noisy point on a plateau.

Cross-material generalization would require repeating the design with other permitted solvent categories or relevant material profiles. Because the material information explicitly warned that runtime effects are categorical benchmark effects, such results must not be interpreted as predictions about real ethanol, acetonitrile, toluene, or a named catalyst.

Cross-world generalization would require blinded replication across independently instantiated worlds under the same public contract, followed by an analysis that separates within-world repeatability from between-world mechanism variation. One successful replay in the present world would establish only local reproducibility.

Finally, “sample-best” and “proven optimal” must remain distinct. I did not establish that batch 8 was even the highest-scoring member of the 12, and I selected it for evidentiary value rather than score. Even if it had been sample-best, a maximum among 12 noisy, sparsely sampled conditions would not demonstrate global or local optimality. Proving optimality would require a prespecified objective, replicated neighboring conditions, uncertainty-aware comparison, and coverage of plausible alternatives.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `5.41`; 80% interval `[5.38, 5.45]`.

An operational, conditional pKa is identifiable from the paired final-assay channels using pKa_eff = pH + log10((1-alpha)/alpha). The 12 batch estimates averaged 5.412, with observed values 5.336-5.539; the stated interval reflects uncertainty in their common effective value. This is not an identified molecular pKa: activity coefficients, hidden buffering, species identity, precipitation, and the mapping of acid_dissociation_fraction remain confounded.

Path-dependence assessment: `indeterminate`.

No source-campaign experiment compared different staged-addition paths at the same final amount and volume. All batches followed essentially the same half-volume, reagent, intermediate-measurement, final-dilution sequence. Batch 8 changed from 0.08627 to 0.06540 in dissociation and from 0.12009 to 0.15085 in precipitation across dilution, but instrument identity and termination stage changed simultaneously. Thus there is no reproducible evidence of path dependence, yet final-state dominance was not directly tested; treating the world as equilibrium-state-dominant remains a conjecture rather than an observation.

Dissociation-precipitation assessment: `indeterminate`.

Supported range: Water-only final states with 0.004-0.040 mol reagent, 0.030-0.090 L nominal volume, and 0.0444-1.333 mol/L nominal concentration. Within this range, final dissociation was 0.0549-0.0748 and precipitation_signal was 0.1462-0.1558, with no reproducible monotonic relationship above assay-scale variation.

Competing explanation: Both observables may be independently compressed onto bounded plateaus by a hidden buffer or phase reservoir, or by the public observable mapping. Such compression could conceal either a continuous underlying coupling or a threshold lying below the sampled range.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.0167198 | 0.933333 | 0.100667 | 0.103013 |
| pH_normalized | 0.00271059 | 1 | 0.0253333 | 0.0253333 |
| precipitation_signal | 0.0127559 | 0.75 | 0.0331667 | 0.0684296 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
