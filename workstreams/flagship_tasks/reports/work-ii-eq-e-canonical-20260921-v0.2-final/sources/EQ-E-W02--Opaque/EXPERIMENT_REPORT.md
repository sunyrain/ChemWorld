# EQ-E-W02--Opaque — final English experiment report

World `EQ-E-W02`; information arm `Opaque`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 61 recorded operations. Exact replay is `True`; rollbacks: 2.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.04 | 0.005 | ph_meter, final_assay, final_assay | 0.174416 | 0.0115342 | 0.0140831 | 0 |
| 2 | 0 | 0.04 | 0.015 | ph_meter, final_assay | 0.123144 | 0.00386339 | 0.0395602 | 0 |
| 3 | 0 | 0.08 | 0.01 | ph_meter, final_assay | 0.175109 | 0.0128072 | 0.0119842 | 0 |
| 4 | 0 | 0.08 | 0.03 | ph_meter, final_assay | 0.124725 | 0.0110026 | 0.0387811 | 0 |
| 5 | 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.167315 | 0 | 0.0329535 | 0 |
| 6 | 1 | 0.04 | 0.015 | ph_meter, final_assay | 0.111571 | 0 | 0.0676845 | 0.00620838 |
| 7 | 1 | 0.08 | 0.01 | ph_meter, final_assay | 0.164365 | 0.0016244 | 0.0330735 | 0.00165429 |
| 8 | 1 | 0.08 | 0.03 | ph_meter, final_assay | 0.113901 | 0 | 0.0755487 | 0 |
| 9 | 2 | 0.04 | 0.005 | ph_meter, final_assay | 0.161201 | 0 | 0.0551025 | 0 |
| 10 | 2 | 0.04 | 0.015 | ph_meter, final_assay | 0.103951 | 0 | 0.0906246 | 0 |
| 11 | 2 | 0.08 | 0.01 | ph_meter, final_assay | 0.156913 | 0 | 0.0402942 | 0 |
| 12 | 2 | 0.08 | 0.03 | ph_meter, final_assay | 0.102079 | 0.000879095 | 0.0792834 | 0.00444169 |

### Sealed evidentiary anchor

Batch `12`: Batch 12 is a useful anchor because its medium-2 high-loading, large-volume condition completes both the within-medium loading contrast and the matched-concentration scale comparison.

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## K1 — sealed open mechanistic report

Mechanistic report

1. Experimental scope and design

I completed 12 terminated batches and obtained one valid final assay for every batch. I studied selectable medium identities 0, 1, and 2 in a balanced 3 × 2 × 2 design:

- Low concentration: 0.005 mol in 0.040 L or 0.010 mol in 0.080 L, both giving nominal C = 0.125 mol L⁻¹.
- High concentration: 0.015 mol in 0.040 L or 0.030 mol in 0.080 L, both giving nominal C = 0.375 mol L⁻¹.
- The two volumes therefore test scale at matched concentration, while the two concentrations differ by a factor of three.

The public selector labels identities 0, 1, and 2 as Water, Ethanol, and Acetonitrile, respectively. However, the material information explicitly states that their runtime effects are calibrated categorical benchmark effects, not predictions from real-solvent property correlations. I therefore interpret them primarily as medium identities 0–2 and do not attribute the results to real-water, real-ethanol, or real-acetonitrile chemistry.

Eleven batches also received a pre-termination pH-meter measurement. The attempted pH measurement in batch 1 failed validation because I supplied an undeclared replicate-count field; it produced no chemical measurement and was not charged as an instrument use. Batch 1 nevertheless has a valid final assay. No batch was discarded.

2. Final-assay observations

The table reports normalized pH h = pH/14, acid-dissociation fraction α, precipitation signal P, equilibrium residual R, and the environment diagnostic D. D is reported for completeness but is not my epistemic confidence.

Batch | Medium | Volume (L) | Reagent (mol) | C (mol L⁻¹) | h | α | P | R | D
1 | 0 | 0.040 | 0.005 | 0.125 | 0.17442 | 0.01153 | 0.01408 | 0 | 0.82107
2 | 0 | 0.040 | 0.015 | 0.375 | 0.12314 | 0.00386 | 0.03956 | 0 | 0.87340
3 | 0 | 0.080 | 0.010 | 0.125 | 0.17511 | 0.01281 | 0.01198 | 0 | 0.81836
4 | 0 | 0.080 | 0.030 | 0.375 | 0.12472 | 0.01100 | 0.03878 | 0 | 0.87386
5 | 1 | 0.040 | 0.005 | 0.125 | 0.16731 | 0 | 0.03295 | 0 | 0.87110
6 | 1 | 0.040 | 0.015 | 0.375 | 0.11157 | 0 | 0.06768 | 0.00621 | 0.92969
7 | 1 | 0.080 | 0.010 | 0.125 | 0.16437 | 0.00162 | 0.03307 | 0.00165 | 0.86574
8 | 1 | 0.080 | 0.030 | 0.375 | 0.11390 | 0 | 0.07555 | 0 | 0.93199
9 | 2 | 0.040 | 0.005 | 0.125 | 0.16120 | 0 | 0.05510 | 0 | 0.91305
10 | 2 | 0.040 | 0.015 | 0.375 | 0.10395 | 0 | 0.09062 | 0 | 0.95466
11 | 2 | 0.080 | 0.010 | 0.125 | 0.15691 | 0 | 0.04029 | 0 | 0.90090
12 | 2 | 0.080 | 0.030 | 0.375 | 0.10208 | 0.00088 | 0.07928 | 0.00444 | 0.96719

3. Effective relationships supported by the experiment

Concentration is the dominant transferable variable. At every medium and both scales, increasing nominal concentration from 0.125 to 0.375 mol L⁻¹ lowered normalized pH and increased precipitation signal. Averaging the two scales gives:

Medium | h at low C | h at high C | P at low C | P at high C
0 | 0.17476 | 0.12393 | 0.01303 | 0.03917
1 | 0.16584 | 0.11274 | 0.03301 | 0.07162
2 | 0.15906 | 0.10301 | 0.04770 | 0.08495

Thus the threefold concentration increase changed h by −0.05083, −0.05310, and −0.05604 for media 0, 1, and 2. In ordinary pH units these correspond to changes of approximately −0.712, −0.743, and −0.785. The associated P changes were +0.02614, +0.03860, and +0.03726. These changes are much larger than the declared final-assay noise scales of 0.002 for normalized pH and 0.006 for precipitation signal.

A compact descriptive interpolation over the tested interval is

h_m(C) ≈ a_m − b_m ln(C/0.125),
P_m(C) ≈ c_m + d_m ln(C/0.125),

where C is in mol L⁻¹. From the two tested concentrations:

- Medium 0: a₀ = 0.17476, b₀ = 0.04627, c₀ = 0.01303, d₀ = 0.02379.
- Medium 1: a₁ = 0.16584, b₁ = 0.04834, c₁ = 0.03301, d₁ = 0.03514.
- Medium 2: a₂ = 0.15906, b₂ = 0.05101, c₂ = 0.04770, d₂ = 0.03391.

These are two-point empirical interpolations, not fitted equilibrium constants and not justified outside 0.125–0.375 mol L⁻¹.

Medium identity contributes reproducible offsets in addition to the shared concentration response. Moving from identity 0 to 1 to 2 is associated with progressively lower h and larger P at both loadings. At low concentration, mean P is 0.0130, 0.0330, and 0.0477; at high concentration it is 0.0392, 0.0716, and 0.0850. Corresponding h values show the reverse ordering. Because the same pattern appears at both scales and both concentrations, it is unlikely to be merely a single noisy result. This is an entity mapping, not a claim that one medium is globally “better.”

The negative P–h association is also approximately transferable but not universal. The two-level slopes ΔP/Δh are about −0.514, −0.727, and −0.665 for media 0–2. A common negative coupling is therefore plausible, while the strength of the precipitation response remains medium-conditioned.

Scale transfer is strong for normalized pH. Matched-concentration 0.040-versus-0.080 L differences are at most 0.00429 for low concentration and 0.00233 for high concentration, except that all remain small relative to the approximately 0.05 concentration effect. Medium 0 also shows nearly exact scale transfer in P: its paired differences are only 0.00210 at low concentration and 0.00078 at high concentration. Medium 1 transfers closely at low concentration, but its large-volume high-concentration P is 0.07555 versus 0.06768 at small volume. Medium 2 shows a repeated possible scale effect in the opposite direction: large-volume P is lower by 0.01481 at low concentration and 0.01134 at high concentration. Because this direction repeats at both loadings and exceeds the declared single-assay precipitation noise, it is evidence for a medium-2 scale interaction, although two paired contrasts are insufficient to establish its physical origin.

4. Proposed operating mechanism

My preferred minimal mechanism is a coupled weak-acid and precipitation system with medium-conditioned effective activities and solubility:

HA ⇌ H⁺ + A⁻

K_a,m^eff = a(H⁺)a(A⁻)/a(HA)

νA⁻ + X ⇌ S(s)

K_sp,m^eff = activity product at saturation.

Here m denotes medium identity, X is an unspecified precipitation partner, and S is an unspecified solid or directly precipitated state. A generic balance is

C_T = [HA] + [A⁻] + νS_T,

with electroneutrality and medium-dependent activity coefficients completing the equilibrium description. The measured precipitation signal need not equal S_T directly; a safer observation equation is

P = clip(g_m(S_T, particle state, volume, mixing) + measurement error, 0, 1).

In this picture, increasing total loading raises hydrogen activity and the amount or supersaturation of precipitable material. That produces the observed simultaneous fall in pH and rise in P. Medium identity can modify effective acid dissociation, ionic activities, the solubility threshold, nucleation/scattering response, or several of these together. The medium ordering in both h and P suggests a shared latent medium effect, but it does not prove that precipitation causes the pH shift.

The observed pH response is steeper than the simplest ideal, nonprecipitating weak-acid approximation. For an ideal weak acid with fixed K_a, a threefold concentration increase would change pH by approximately −0.5 log10(3) = −0.239 pH unit. The observed changes are roughly −0.71 to −0.78. This discrepancy motivates the coupled/activity-dependent model rather than a single ideal Henderson–Hasselbalch-style law. Plausible sources include precipitation-linked mass balance, concentration-dependent activity coefficients, or an effective benchmark response that does not correspond to a single ideal acid.

5. Acid-dissociation fraction and measurement reconciliation

The α channel is close to its lower boundary and is much less identifiable than h or P. Final α values are zero or below 0.004 in most medium-1 and medium-2 batches. Exact zeros should be interpreted as clipped/noise-limited estimates, not proof of no dissociation, because the declared final-assay noise scale is 0.006. Medium 0 at low concentration is the clearest reproducible nonzero feature: α = 0.01153 in batch 1 and 0.01281 in batch 3. Medium 0 at high concentration is less consistent across scale: 0.00386 in batch 2 versus 0.01100 in batch 4. I therefore do not infer a reliable concentration law for α.

The eleven valid pre-termination pH-meter readings broadly reproduce the final normalized-pH structure. Their mean absolute difference from the corresponding final-assay h values is approximately 0.00267. Some individual examples are particularly close: batch 7 gave 0.16431 before termination and 0.16437 in the final assay; batch 5 gave 0.16708 and 0.16731. Larger differences occurred in batches 3, 4, and 12, with absolute h differences around 0.007–0.008. These comparisons conflate instrument noise, calibration differences, and any termination-associated evolution, so they do not identify one source.

Precipitation and α agreement between the two instruments is weaker. For example, batch 5 had pre-termination P = 0.06982 but final P = 0.03295, while batch 11 had pre-termination α = 0.03285 but final α = 0. This reinforces the decision to base the quantitative relationships on the uniform final-assay series and to regard near-zero α and single intermediate P values cautiously.

Equilibrium residuals were zero in most final assays and no larger than 0.00621. This supports internal consistency with the environment’s bounded equilibrium evaluator, but it does not uniquely validate my chemical mechanism. Likewise, the reported equilibrium-confidence diagnostic ranged from 0.818 to 0.967; by contract it is an environment diagnostic, not my confidence or a probability that the proposed mechanism is correct.

6. How the evidence changed the interpretation

The first medium-0 pair, batches 1 and 2, established the basic loading signature: h fell from 0.17442 to 0.12314 while P rose from 0.01408 to 0.03956. Batches 3 and 4 largely reproduced that signature at twice the volume, leading me to treat concentration rather than absolute amount as the primary pH control.

Batches 5–8 then showed that the form of the loading response transferred to medium 1 but with a lower-pH, higher-precipitation offset. This changed the interpretation from a single concentration curve to a family of entity-conditioned curves.

Batches 9–12 extended that family to medium 2 and revealed the clearest possible volume dependence in P. In particular, batches 9 versus 11 and 10 versus 12 preserved the pH response but produced lower P at the larger scale. That observation led me to include a possible medium-specific scale or particle-state term in g_m rather than asserting perfect scale invariance.

7. Evidence boundaries and competing explanations

The experiment identifies effective input–output relationships, not molecular identities or unique constants. There are only two concentrations, two volumes, one final assay per condition, one order of addition, no time course, no temperature variation, and no independent solid-mass measurement. Consequently, K_a, K_sp, activity coefficients, stoichiometry, nucleation kinetics, and the mapping from precipitated amount to precipitation signal cannot be separately estimated.

Several explanations remain observationally equivalent within this design:

1. Coupled equilibrium: precipitation removes a dissolved species and shifts acid dissociation or hydrogen activity.
2. Common-cause response: concentration and medium independently alter acid activity and precipitation propensity, with little direct causal coupling between the two outputs.
3. Activity-coefficient mechanism: the steep pH response arises mainly from nonideal medium- and concentration-dependent activities, while precipitation is a parallel consequence.
4. Kinetic or optical mechanism: P partly reflects nucleation, particle size, settling, or scattering rather than equilibrium solid amount. This is especially plausible for the medium-2 scale effect.
5. Benchmark categorical mapping: because the environment declares categorical calibrated solvent effects, the observations may be generated by effective response surfaces rather than a physically unique molecular model.

No task-specific qualitative property dossier was supplied, so there was no independent nominal medium-to-mechanism mapping to confirm or reject. The selector labels alone do not justify importing real-solvent expectations.

8. Supported predictions versus extrapolation

Within the tested concentration and volume domain, I would predict that increasing C in any of identities 0–2 lowers normalized pH by about 0.05 for a threefold loading increase and raises P by roughly 0.026–0.039, with medium-specific offsets. I would also predict that pH approximately transfers between 0.040 and 0.080 L at fixed C. Those are interpolative conclusions directly supported by paired observations.

I would not claim the logarithmic equations outside 0.125–0.375 mol L⁻¹, assume linear precipitation response at higher concentration, infer a precipitation threshold, or transfer these coefficients to a fourth medium, another temperature, another order of addition, or real laboratory solvents. The medium-2 volume term is a testable hypothesis rather than a settled law. Batch 12 was committed as the evidentiary anchor because its medium-2, high-loading, large-volume condition closes both the concentration contrast and the matched-concentration scale comparison.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.323 | 0.285 | 0.36 |
| Q01 | acid_dissociation_fraction | 0.026 | 0 | 0.065 |
| Q01 | precipitation_signal | 0.002 | 0 | 0.018 |
| Q02 | pH_normalized | 0.322 | 0.282 | 0.36 |
| Q02 | acid_dissociation_fraction | 0.004 | 0 | 0.025 |
| Q02 | precipitation_signal | 0.004 | 0 | 0.025 |
| Q03 | pH_normalized | 0.325 | 0.282 | 0.365 |
| Q03 | acid_dissociation_fraction | 0.004 | 0 | 0.025 |
| Q03 | precipitation_signal | 0.006 | 0 | 0.032 |
| Q04 | pH_normalized | 0.1948 | 0.181 | 0.209 |
| Q04 | acid_dissociation_fraction | 0.014 | 0 | 0.03 |
| Q04 | precipitation_signal | 0.0031 | 0 | 0.017 |
| Q05 | pH_normalized | 0.1876 | 0.174 | 0.202 |
| Q05 | acid_dissociation_fraction | 0.002 | 0 | 0.016 |
| Q05 | precipitation_signal | 0.0153 | 0.003 | 0.032 |
| Q06 | pH_normalized | 0.1834 | 0.168 | 0.199 |
| Q06 | acid_dissociation_fraction | 0.002 | 0 | 0.016 |
| Q06 | precipitation_signal | 0.0391 | 0.02 | 0.06 |
| Q07 | pH_normalized | 0.1016 | 0.087 | 0.116 |
| Q07 | acid_dissociation_fraction | 0.005 | 0 | 0.02 |
| Q07 | precipitation_signal | 0.0511 | 0.034 | 0.07 |
| Q08 | pH_normalized | 0.0902 | 0.075 | 0.106 |
| Q08 | acid_dissociation_fraction | 0.001 | 0 | 0.015 |
| Q08 | precipitation_signal | 0.0861 | 0.064 | 0.109 |
| Q09 | pH_normalized | 0.0806 | 0.064 | 0.098 |
| Q09 | acid_dissociation_fraction | 0.001 | 0 | 0.015 |
| Q09 | precipitation_signal | 0.1074 | 0.079 | 0.136 |
| Q10 | pH_normalized | 0.196 | 0.183 | 0.209 |
| Q10 | acid_dissociation_fraction | 0.014 | 0 | 0.03 |
| Q10 | precipitation_signal | 0.0017 | 0 | 0.016 |
| Q11 | pH_normalized | 0.1873 | 0.174 | 0.201 |
| Q11 | acid_dissociation_fraction | 0.002 | 0 | 0.016 |
| Q11 | precipitation_signal | 0.0193 | 0.005 | 0.037 |
| Q12 | pH_normalized | 0.1803 | 0.164 | 0.197 |
| Q12 | acid_dissociation_fraction | 0.002 | 0 | 0.016 |
| Q12 | precipitation_signal | 0.026 | 0.007 | 0.049 |

### Q rationales

- **Q01**: This is a long extrapolation below the studied 0.125–0.375 M range. The medium-0 log-concentration relation predicts a substantially higher normalized pH and essentially no precipitation. The dissociation estimate is weakly extrapolated from medium 0 and is assigned a wide, lower-bounded interval.

- **Q02**: The medium-1 concentration curve was extrapolated far below the observed domain. Precipitation is expected to approach the bounded floor, while the dissociation channel remains poorly identified because most medium-1 final values were at or near zero.

- **Q03**: The medium-2 response is extrapolated by a factor of 25 below the lowest studied concentration. The fitted precipitation curve reaches the zero boundary; a small positive estimate and broad interval allow for a residual medium-conditioned signal and model-form error.

- **Q04**: At 0.08 M this is a short extrapolation below the observed range. The medium-0 log-concentration relationship predicts higher pH and precipitation close to its floor. A small-volume correction was transferred from the paired 0.040/0.080 L comparisons.

- **Q05**: This uses the medium-1 entity offset and concentration slope, with the observed scale contrast applied to the 0.024 L condition. The dissociation estimate remains near the measurement floor, whereas a modest precipitation signal is supported by the medium-1 observations.

- **Q06**: The medium-2 curve predicts lower pH and more precipitation than the other identities. The small-volume precipitation estimate includes the repeated direction of the medium-2 scale effect, but its interval is enlarged because that effect was inferred from only two paired contrasts.

- **Q07**: A modest extrapolation above 0.375 M continues the robust medium-0 pattern of falling pH and rising precipitation. The acid-fraction interval is broad because that channel was variable across matched-concentration medium-0 batches.

- **Q08**: The medium-1 high-concentration relation is extended from 0.375 to 0.6 M. Both studied scales supported lower pH and larger precipitation at increased loading, while acid dissociation remained effectively unresolved near zero.

- **Q09**: This applies the medium-2 concentration slope plus its small-volume precipitation correction. It is the largest predicted precipitation response, but the interval incorporates extrapolation and uncertainty about whether the observed scale effect reflects equilibrium amount or particle-dependent signal.

- **Q10**: This is the scale-control partner of Q04. Medium 0 showed nearly exact concentration transfer across the two studied volumes, so Q10 differs only slightly from Q04 and remains close to the precipitation floor.

- **Q11**: This is paired with Q05 at twice the volume. The prediction transfers the small average medium-1 scale effect: nearly unchanged pH and a slightly larger precipitation signal at the larger scale.

- **Q12**: This is the medium-2 scale-control partner of Q06. The point estimate carries forward the repeated observation that larger-volume medium-2 batches had lower precipitation signals at matched concentration; the wide interval reflects limited replication and uncertain mechanism.

Shared rationale:

Predictions use the entity-conditioned log-concentration relationships inferred from the 12 final assays. For normalized pH, those relationships were strongly shared across media, with medium-specific offsets and small scale corrections. Precipitation used the corresponding entity-conditioned concentration slopes plus average paired scale effects; the medium-2 scale correction was retained but given extra uncertainty. Acid-dissociation predictions were shrunk toward zero because that channel was commonly clipped at its lower bound and was much less reproducible than pH or precipitation. Intervals include declared final-assay noise, between-batch variation, uncertainty in transferring the observed twofold scale contrasts, and model-form uncertainty. Q01–Q03 receive the widest intervals because 0.005 M is far outside the studied 0.125–0.375 M range; 0.08 M is a short downward extrapolation, and 0.6 M is a moderate upward extrapolation. All predictions are bounded to the public metric range.

## K2 — sealed seven-part retrospective

1. Assessment of the initial information

The initial packet did not provide a substantive task-specific mechanism, numerical parameter set, or qualitative ordering of the three tested identities. It explicitly said that no nominal property dossier was supplied and that experimental evidence was authoritative. The solvent selectors had public names, but the catalog also warned that runtime coupling was a categorical benchmark effect rather than a prediction from real-solvent properties. I therefore had no defensible initial claim such as “selector 2 must precipitate most” to confirm or refute.

Several framework-level statements were consistent with the observations:

- The system was described as a bounded weak-acid/direct-precipitation slice. Every final assay returned the corresponding pH, dissociation, and precipitation channels, and concentration changed pH and precipitation coherently. This supports using that framework as an effective description, but it does not independently prove the stated molecular chemistry.
- The definition pH_normalized = pH/14 was used directly throughout K1.
- The warning that equilibrium_confidence was an environment diagnostic rather than epistemic confidence was important. K1 preserved that distinction even though the diagnostic increased from approximately 0.82 in the low-loading selector-0 conditions to as high as 0.967 in batch 12.
- The categorical-medium warning was respected: K1 discussed identities 0–2 and explicitly declined to infer real water, ethanol, or acetonitrile causation.

The research goal implicitly invited testing whether relationships transfer across scale. Unconditional scale invariance was not fully supported. Selector 0 transferred closely, but selector 2 showed lower large-volume precipitation at both loadings: batch 11 versus batch 9 differed by −0.01481, and batch 12 versus batch 10 by −0.01134. K1 did revise the explanation by adding a possible medium-specific scale or particle-state term. Thus this was counterevidence to universal scale transfer, not merely an absence of supporting evidence.

I am not aware of a substantive initial claim for which clear counterevidence appeared and was knowingly left uncorrected. The more important limitation is that some framework claims—especially “direct precipitation” as a physical solid-forming process—were never independently tested. A bounded precipitation signal is consistent with that claim but cannot distinguish solid amount from scattering, nucleation state, or another calibrated proxy.

2. Experiments that formed or changed the interpretation

The design itself was driven mainly by the stated research goal and resource constraints. I chose a balanced 3 × 2 × 2 matrix: three selectors, two concentrations, and two volumes at matched concentration. The concentration levels, 0.125 and 0.375 M, and the 0.040/0.080 L scales were not supplied as scientifically privileged values. They were an unvalidated design choice that exactly used the available reagent and solvent while providing a threefold concentration contrast and a twofold scale contrast.

The experiments that materially shaped K1 were:

- Batches 1 and 2 established the first loading contrast for selector 0: normalized pH changed from 0.17442 to 0.12314, while precipitation changed from 0.01408 to 0.03956. This formed the initial concentration-response hypothesis.
- Batches 3 and 4 repeated those nominal concentrations at twice the volume. Their pH and precipitation results were close to batches 1 and 2, shifting my judgment toward concentration as the primary control rather than absolute reagent amount.
- Batches 5–8 showed the same directional concentration response for selector 1 but with lower pH and higher precipitation than selector 0. This changed the model from a single transferable curve to entity-conditioned curves.
- Batches 9–12 extended the entity ordering to selector 2. The repeated large-versus-small precipitation differences in batches 9/11 and 10/12 caused the important modification from scale invariance to possible selector-specific scale dependence.

The pre-termination pH-meter measurements provided secondary support but did not drive the experimental sequence, which was already balanced. Their mean absolute difference from final-assay normalized pH was about 0.00267. They also exposed weak reproducibility in the dissociation and precipitation channels; for example, batch 11 gave pre-termination acid dissociation of 0.03285 but a final value of zero. K1 consequently treated acid dissociation as poorly identified.

Several choices were based on assumptions rather than established data. I assumed that two concentrations would be enough to reveal a useful response form, that the selected range would avoid complete signal saturation, and that doubling volume would be an informative scale test. I also assumed that the same order of addition without waiting or heating was a suitable common protocol. None of these assumptions was independently validated. The failed batch-1 pH-meter attempt, caused by an undeclared replicate-count field, also made the intermediate-measurement coverage asymmetric.

3. Principal competing mechanisms

K1’s preferred minimal account was a coupled system,

HA ⇌ H⁺ + A⁻,
νA⁻ + X ⇌ S(s),

with medium-conditioned effective acid and solubility terms and a precipitation observation function that could depend on particle state, volume, and mixing. That remains a concise effective explanation, but it is not uniquely identified.

The leading alternatives are:

- Coupled equilibrium: precipitation removes a dissolved participant and shifts acid dissociation or hydrogen activity.
- Parallel common-cause responses: concentration and identity independently affect acidity and precipitation, without precipitation materially controlling pH.
- Nonideal activity effects: concentration-dependent activities principally generate the steep pH response, while precipitation is a separate consequence.
- Kinetic or optical precipitation: the precipitation channel depends strongly on nucleation, particle size, settling, or scattering rather than only on equilibrium solid amount. This could explain the selector-2 scale pattern.
- A categorical benchmark response surface: the environment may encode effective relationships that need not correspond to a unique molecular mechanism.

The existing experiments distinguish several coarse features. They establish a robust directional concentration response, reproducible entity-conditioned offsets, and approximate pH transfer across the tested scales. They also provide limited evidence against universal scale invariance of precipitation.

They cannot distinguish causal precipitation–acid coupling from two parallel concentration responses. They cannot separately identify effective Ka, Ksp, activity coefficients, precipitation stoichiometry, or the mapping from solid amount to signal. Because there was no time course, solid-specific measurement, order-of-addition variation, or temperature perturbation, equilibrium, kinetic, and optical accounts remain confounded. The near-zero and clipped acid-dissociation measurements are particularly unhelpful for discriminating these explanations.

4. One additional complete experiment

If allowed exactly one additional legal experiment, I would perform an exact repeat of batch 11: selector 2, 0.010 mol reagent in 0.080 L solvent, nominally 0.125 M, using the same order of addition, one pre-termination pH-meter measurement, termination, and one final assay. I would not add waiting, heating, or another procedural change because the purpose would be to test repeatability of the most consequential scale anomaly rather than introduce a new confounder.

The critical comparison would be with batch 11 itself and with its matched-concentration small-scale partner, batch 9:

- If the repeated final precipitation signal were again near batch 11’s 0.0403 and clearly below batch 9’s 0.0551, while normalized pH remained near 0.157–0.161, confidence in a reproducible selector-2 scale or particle-state effect would increase. I would retain the scale term used in Q06/Q12 and prioritize optical or nucleation explanations.
- If it were near batch 9’s 0.0551, the original scale contrast would look more like measurement or batch variation. I would shrink the selector-2 scale correction toward zero and widen predictions involving volume transfer.
- If it were outside both values by much more than the declared precipitation noise, the main lesson would be excess process variability. A deterministic scale law would become less credible.
- If pH also shifted strongly with precipitation, that would strengthen the case for genuine chemical coupling. If precipitation varied while pH remained stable, a particle-state or optical explanation would become more plausible.
- Repeating a near-zero versus clearly positive acid-dissociation result could also inform that channel, but one repeat would still be insufficient to overcome clipping and noise.

This single experiment would not prove a mechanistic scale law. It would test whether the observation that most affected the scale interpretation and several blind predictions is repeatable.

5. Trade-off between identifiability and operational score

The design prioritized characterization over maximizing the scalar score. The task explicitly stated that the native score and equilibrium-confidence diagnostic were not the research objective. I therefore distributed all 12 batches across identities, concentrations, and scales instead of repeatedly selecting conditions that appeared to produce a high diagnostic value.

That choice improved identifiability of main effects and paired scale contrasts but likely sacrificed operational score. For example, low-loading selector-0 batches 1 and 3 had diagnostics around 0.82, whereas selector-2 high-loading batches 10 and 12 were around 0.955 and 0.967. An optimization campaign could have concentrated on the latter region, but doing so would have weakened the evidence for transfer, entity offsets, and scale interactions.

There was no major instance in which I knowingly sacrificed identifiability to optimize score during the campaign. The matrix remained balanced rather than adaptively moving toward favorable results. Conversely, identifiability was sacrificed in other ways that were unrelated to score: only two concentration levels were used, every condition lacked a final-assay replicate, and no time, temperature, or protocol perturbation was included.

The sealed recommendation of batch 12 may superficially resemble optimization because it had the largest equilibrium-confidence diagnostic. My stated rationale, however, was evidentiary: it closed both the selector-2 loading contrast and the matched-concentration scale comparison. It was not presented as a globally best recipe.

6. Underused evidence and weaknesses in the blind predictions

Several acquired evidence streams were not fully exploited:

- K1 used processed final estimates but did not analyze the referenced raw characterization artifacts or spectra. Consequently, possible saturation, baseline, peak-shape, or particle-scattering information was not incorporated.
- The eleven pre-termination measurements were discussed mainly as agreement checks. A formal instrument-error or latent-state model could have separated pH reproducibility from the much poorer acid-dissociation and precipitation agreement.
- The pattern of clipped acid-dissociation values was recognized but not modeled as censored data.
- The small nonzero equilibrium residuals and public process telemetry were not used quantitatively. This was appropriate for avoiding overinterpretation, but it left potentially useful heteroscedasticity or process-stability information unexplored.
- The failed batch-1 intermediate measurement reduced symmetry and should be regarded as missing evidence, not as a zero or successful observation.

The least reliable blind predictions are Q01–Q03. They extrapolated from a lowest observed concentration of 0.125 M down to 0.005 M, a factor of 25. K1 had explicitly said: “I would not claim the logarithmic equations outside 0.125–0.375 mol L⁻¹.” The sealed Q rationale disclosed that these were long extrapolations, but it nevertheless used the same log form to produce normalized-pH estimates near 0.32 and precipitation estimates near zero. The 80% pH intervals, only about 0.075–0.083 wide, are probably too narrow for such profound model-form uncertainty. The low-concentration precipitation intervals may also be too narrow because no threshold or asymptotic behavior was observed. Q01’s acid-dissociation estimate of 0.026 was especially speculative.

Q09 is also vulnerable: it combines upward concentration extrapolation with a selector-2 small-volume correction to predict precipitation of 0.1074. Its interval may insufficiently cover curvature or saturation. Q06 and Q12 depend heavily on transferring the selector-2 scale effect from 0.040/0.080 L to the new 0.024/0.048 L pair. That assumes relative scale, rather than absolute volume or an uncontrolled batch effect, governs the response. Their intervals should arguably have been wider.

Q04–Q06 and Q10–Q12 are only modest concentration extrapolations to 0.08 M, but predictions close to the precipitation floor—especially Q04 and Q10—remain sensitive to the unknown response shape. All acid-dissociation predictions are weak because K1 already judged that channel poorly identifiable.

Thus the predictions did not silently contradict K1: their rationales labeled extrapolation and model uncertainty. Nevertheless, the numerical intervals did not always fully honor K1’s stated applicability boundary. The conflict is most pronounced for Q01–Q03, where the point estimates were required but the intervals should have expressed much greater uncertainty.

7. Limitations of the sealed recommendation

Batch 12 is an evidentiary anchor, not a demonstrated optimum. It is a single realization at selector 2, 0.375 M, and 0.080 L. Its final values included normalized pH 0.10208, precipitation 0.07928, and equilibrium-confidence diagnostic 0.96719. Batch 10 actually had a larger precipitation signal, 0.09062, at the matched concentration and smaller scale. Moreover, the diagnostic is not epistemic confidence or the sole objective.

Even if batch 12 were the sample-best batch under some scalar summary, “highest among 12 sampled conditions” would not imply local or global optimality. The design tested only two concentrations, two scales, three selectors, one order of addition, and one procedural timing pattern. It did not search a continuous response surface.

Repeatability should first be tested by exact independent replication of batch 12, including both the pre-termination and final measurements. Local robustness would require nearby concentrations and volumes—for example, bracketing 0.375 M and 0.080 L—while holding the protocol fixed. Order of addition, waiting time, and minor volume perturbations would then test procedural robustness.

Cross-material generalization would require applying the same concentration–scale neighborhood to selectors 0 and 1 and, if legally available in a future study, to an unstudied selector. Cross-world generalization would require independent campaign instances or benchmark worlds, because the current evidence comes from one bounded world. Real-material generalization would require empirical chemistry outside this synthetic benchmark and cannot be inferred from the selector names.

Accordingly, the sealed recommendation is best understood as a replayable, information-rich member of the completed matrix. It was selected because it anchors two contrasts, not because the campaign proved it optimal, universally robust, or transferable beyond the tested world.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.018996 | 0.75 | 0.0419167 | 0.106609 |
| acid_dissociation_fraction | 0.0147058 | 0.75 | 0.0240833 | 0.0759785 |
| precipitation_signal | 0.00447909 | 0.983333 | 0.0324167 | 0.0324379 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0206524 |
| 0.08 | 0.00758114 |
| 0.6 | 0.00613014 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00135864 |
| 1 | 0.00593923 |
| 2 | 0.0044155 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
