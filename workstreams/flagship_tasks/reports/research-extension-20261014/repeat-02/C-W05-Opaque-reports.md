# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material and reaction effects

The materials were anonymous benchmark identities, so the evidence supports empirical rankings rather than claims about real chemical structures. At 350 K for 1,800 s, all four tested diagonal catalyst/solvent pairs gave nearly complete conversion, but their product distributions differed substantially:

- Batch 1, C0/S0: final selectivity ≈0.651 and reaction yield ≈0.645.
- Batch 4, C1/S1: selectivity ≈0.630 and yield ≈0.616.
- Batch 5, C2/S2: selectivity ≈0.500 and yield ≈0.493.
- Batch 6, C3/S3: selectivity ≈0.582 and yield ≈0.584, with the largest degradation warning, ≈0.127.

Thus C0/S0 was the strongest of the tested paired systems, whereas C2/S2 diverted substantially more material away from target. This is an observation about pairs, not separate catalyst and solvent effects: catalyst and solvent were changed together, so their individual contributions and interactions remain unresolved.

A useful approximate reaction relation is

Y_rxn ≈ X × S_target,

where X is conversion and S_target is target selectivity. The measured yields were broadly consistent with this interpretation. Near-unity conversion therefore did not guarantee high target formation; selectivity was the more important reaction-stage discriminator.

Batch 12 used C0/S0 but reduced the charge to 0.010 mol reagent, 0.040 L solvent, and 0.0025 mol catalyst. It produced selectivity ≈0.827 and reaction yield ≈0.825, markedly above the full-charge C0/S0 batches. Lower loading may have suppressed competing chemistry, but this causal interpretation is uncertain because reagent concentration, total volume, and catalyst-to-reagent ratio changed together. It was not a controlled single-factor comparison.

### 2. Reaction–crystallization coupling

The reported crystal recovery was a crystallization-stage quantity:

R_cryst = (seed-excluded recovered target)/(target present before separation).

It therefore should not be confused with overall yield from the charged reagent. An approximate overall isolated-target fraction is

Y_overall ≈ Y_rxn × R_cryst.

For example, this product is about 0.316 for batch 1, 0.375 for batch 8, 0.361 for batch 7, and 0.525 for batch 12. Batch 12 consequently benefited twice: it generated a larger target pool at the reaction stage and recovered a larger fraction of that pool during crystallization.

Crystal purity was not the limiting property. Final purity was approximately 0.966–1.000 across the material and process screens, and batch 12 gave ≈0.996. In contrast, particle-number fines were consistently unacceptable. This decoupling indicates that chemical impurity rejection was effective even when the population balance strongly favored small particles.

A conventional qualitative framework is supersaturation

S(t) = C(t)/C*(T(t), solvent),

with nucleation rate B increasing steeply with supersaturation and crystal growth rate G responding more moderately. The measured fines fraction was

F20 = N(d < 20 µm)/N_total,

so even a modest mass of newly nucleated particles can dominate F20 because it is number-weighted. This explains how good mass recovery and purity can coexist with a very poor fines result.

### 3. Process-history dependence

The initial hypothesis was that seeding, slow cooling, and a growth hold would reduce secondary nucleation and fines. Batch 1 followed that general strategy and reached crystal recovery ≈0.490 and purity ≈0.985, but F20 was ≈0.997. Subsequent interventions tested several distinct histories:

- Batch 2: shallow reheat and recooling; recovery ≈0.472, F20 reported as 1.000.
- Batch 3: approximately 1 g total seed addition; recovery ≈0.503, F20 ≈0.995.
- Batch 7: greatly extended low-agitation holds and deeper cooling; recovery ≈0.556, F20 ≈0.987.
- Batch 8: three progressively milder reheat/recool cycles followed by deep cooling; recovery ≈0.580, F20 ≈0.987.
- Batch 9: unseeded crystallization with high agitation and long holds; recovery ≈0.570, F20 = 1.000.
- Batch 10: ultra-slow staged cooling in approximately 1 K increments; recovery ≈0.553, F20 = 1.000.
- Batch 11: filtration, resuspension in fresh S0, a hold, and refiltration; recovery ≈0.539, F20 ≈0.994.
- Batch 12: reduced upstream loading with staged cooling; recovery ≈0.636, purity ≈0.996, but F20 = 1.000.

These results revise the original mechanism. Within the tested ranges, ordinary seeding, added seed mass, long residence time, agitation changes, slow cooling, thermal cycling, and resuspension were not sufficient to control the number-based fines population. Some histories raised recovery—especially deeper cooling and cycling—but did not yield a credible fines improvement.

The most plausible interpretations are: (1) a strong nucleation burst occurred during quench or the early supersaturation crossing, before later growth controls could act; (2) secondary nucleation remained dominant over growth throughout cooling; (3) the anonymous solvent–solute system intrinsically favored a small-particle habit under every tested condition; or (4) an important untested variable, such as a different catalyst/solvent cross-combination, quench profile, concentration path, seed-size distribution, or solids-classification step, controlled F20. These alternatives were not distinguished experimentally.

The mild reheat in batch 2 and more extensive cycles in batch 8 did not selectively eliminate enough fines, so a simple Ostwald-ripening explanation is not supported. Batch 11’s wash/resuspension lowered the final byproduct signal to ≈0.030 from the ≈0.21 range seen in many C0/S0 batches, consistent with impurity removal or a changed assay basis, but it did not improve the particle population.

### 4. Revisions, uncertainty, and unresolved tradeoff

The principal revision is rejection of the initial expectation that slower seeded cooling would meet the fines constraint. The repeated near-unity F20 values, including in paid particle measurements before filtration and final assays after filtration, make the failure qualitatively robust. Nevertheless, there were no true recipe replicates, and the final-assay noise model included uncertainty in recovery, purity, size, and fines. Small numerical differences such as F20 ≈0.987 versus 1.000 should therefore not be interpreted as established process effects.

Reported normalized crystal-size values correspond to d50 through

crystal_size = min(d50/250 µm, 1).

For example, batch 12’s normalized value ≈0.0819 corresponds to a nominal d50 of about 20.5 µm. Its simultaneous F20 of 1.000 appears counterintuitive but can arise from noise, a sharply concentrated distribution near the 20 µm boundary, or differences between separately noisy summary channels. It reinforces the need not to infer constraint satisfaction from d50 alone; the explicit number fraction below 20 µm is the controlling metric.

The unresolved tradeoff is therefore clear: deeper or more elaborate crystallization histories and lower upstream loading improved seed-excluded recovery, but none established acceptable fines. Batch 12 was the strongest recovery/purity result, not a fully feasible result. No completed batch satisfied both purity ≥0.80 and F20 ≤0.50, so the campaign did not identify a quality-compliant optimum. The evidence supports a high-recovery chemical process coupled to an unresolved particle-population problem.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.98 | 0.88 | 1 |
| Q01 | crystal_purity | 0.985 | 0.94 | 1 |
| Q01 | crystal_size | 0.058 | 0.025 | 0.105 |
| Q01 | crystal_yield | 0.56 | 0.38 | 0.72 |
| Q02 | crystal_fines_fraction | 0.99 | 0.9 | 1 |
| Q02 | crystal_purity | 0.975 | 0.91 | 1 |
| Q02 | crystal_size | 0.048 | 0.02 | 0.095 |
| Q02 | crystal_yield | 0.48 | 0.29 | 0.67 |
| Q03 | crystal_fines_fraction | 0.95 | 0.78 | 1 |
| Q03 | crystal_purity | 0.987 | 0.94 | 1 |
| Q03 | crystal_size | 0.072 | 0.03 | 0.13 |
| Q03 | crystal_yield | 0.53 | 0.34 | 0.71 |
| Q04 | crystal_fines_fraction | 0.98 | 0.87 | 1 |
| Q04 | crystal_purity | 0.987 | 0.94 | 1 |
| Q04 | crystal_size | 0.057 | 0.025 | 0.105 |
| Q04 | crystal_yield | 0.57 | 0.39 | 0.73 |
| Q05 | crystal_fines_fraction | 0.97 | 0.83 | 1 |
| Q05 | crystal_purity | 0.988 | 0.945 | 1 |
| Q05 | crystal_size | 0.063 | 0.028 | 0.115 |
| Q05 | crystal_yield | 0.59 | 0.41 | 0.75 |
| Q06 | crystal_fines_fraction | 0.995 | 0.91 | 1 |
| Q06 | crystal_purity | 0.985 | 0.935 | 1 |
| Q06 | crystal_size | 0.043 | 0.018 | 0.085 |
| Q06 | crystal_yield | 0.61 | 0.42 | 0.77 |
| Q07 | crystal_fines_fraction | 0.965 | 0.81 | 1 |
| Q07 | crystal_purity | 0.988 | 0.945 | 1 |
| Q07 | crystal_size | 0.066 | 0.03 | 0.12 |
| Q07 | crystal_yield | 0.61 | 0.43 | 0.76 |
| Q08 | crystal_fines_fraction | 0.99 | 0.88 | 1 |
| Q08 | crystal_purity | 0.987 | 0.935 | 1 |
| Q08 | crystal_size | 0.052 | 0.021 | 0.1 |
| Q08 | crystal_yield | 0.47 | 0.27 | 0.67 |
| Q09 | crystal_fines_fraction | 0.995 | 0.9 | 1 |
| Q09 | crystal_purity | 0.99 | 0.92 | 1 |
| Q09 | crystal_size | 0.04 | 0.015 | 0.08 |
| Q09 | crystal_yield | 0.008 | 0 | 0.035 |
| Q10 | crystal_fines_fraction | 0.99 | 0.87 | 1 |
| Q10 | crystal_purity | 0.988 | 0.925 | 1 |
| Q10 | crystal_size | 0.047 | 0.018 | 0.09 |
| Q10 | crystal_yield | 0.13 | 0.035 | 0.27 |
| Q11 | crystal_fines_fraction | 0.975 | 0.84 | 1 |
| Q11 | crystal_purity | 0.989 | 0.945 | 1 |
| Q11 | crystal_size | 0.062 | 0.028 | 0.115 |
| Q11 | crystal_yield | 0.63 | 0.45 | 0.78 |
| Q12 | crystal_fines_fraction | 0.99 | 0.89 | 1 |
| Q12 | crystal_purity | 0.978 | 0.92 | 1 |
| Q12 | crystal_size | 0.05 | 0.02 | 0.098 |
| Q12 | crystal_yield | 0.55 | 0.35 | 0.73 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed crystals, so particles are expected even when seed-excluded product recovery is minimal. The campaign repeatedly produced purity above 0.96 but fines near unity despite slow cooling, long holds, seed changes, thermal cycling, agitation changes and resuspension; accordingly none is predicted quality-feasible. Pairwise: Q01/Q02 assigns somewhat better recovery to S1 than S3, but solvent effects are uncertain because prior material screens were confounded. Q03/Q04 predicts fewer seeds give slightly larger particles and fewer fines, with only a modest recovery penalty. Q05/Q06 predicts gradual cooling gives better size and fines than a rapid crash, while the long cold hold keeps recovery similar. Q07/Q08 predicts reheating to 315 K partially redissolves product and the short recooling period does not fully restore recovery or particle quality. Q09/Q10 isolates continued growth at 292 K: immediate filtration gives almost no seed-excluded recovery, whereas two hours adds modest recovery but remains fines-dominated. Q11/Q12 predicts the doubled reagent loading increases supersaturation and nucleation and modestly reduces fractional crystallization recovery and purity, consistent with the observed advantage of lower loading, though that earlier comparison was confounded. Intervals are deliberately broad because catalyst C1/S0 cross-effects, very long aging, and these exact loading histories were not directly tested.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Chemical purity was not the limiting quality attribute.** Every completed batch had final crystal purity above about 0.96. Examples include batch 1 at ≈0.985, batch 5 at ≈0.967, and batch 12 at ≈0.996.
- **The fines constraint was consistently unmet.** Final fines estimates remained approximately 0.987–1.000 across batches 1–12. Intermediate particle measurements in batches 2–12 also generally remained near unity. Thus the conclusion that no tested process was quality-feasible is directly supported.
- **Several large process changes failed to solve fines.** These include a large seed charge in batch 3, extended low-agitation aging in batch 7, repeated reheating and recooling in batch 8, unseeded/high-agitation operation in batch 9, very slow staged cooling in batch 10, and filtration/resuspension in batch 11.
- **Among the four diagonal material pairs, C0/S0 gave the strongest reaction performance.** Batch 1 gave selectivity ≈0.651 and yield ≈0.645, compared with ≈0.630/0.616 for C1/S1 in batch 4, ≈0.500/0.493 for C2/S2 in batch 5, and ≈0.582/0.584 for C3/S3 in batch 6. This ranking applies only to the tested pairs.
- **Batch 12 had the largest observed seed-excluded recovery.** Its crystal yield was ≈0.636 with purity ≈0.996, although its fines fraction was 1.000.

### Contradicted or substantially weakened

- **The initial claim that ordinary seeded, slow cooling would suppress fines was contradicted.** Batch 1 already failed, and batches 3, 7, and 10 showed that more seed, longer aging, and much slower cooling did not rescue the particle distribution.
- **A simple Ostwald-ripening remedy was weakened.** Mild recycling in batch 2 and more extensive thermal cycling in batch 8 did not produce a convincing reduction in fines. Batch 8 improved recovery to ≈0.580 but retained F20 ≈0.987.
- **Seed quantity as the principal fines-control lever was contradicted over the tested range.** Batch 3 used about 1 g total seed yet remained at F20 ≈0.995, while the unseeded batch 9 also remained at 1.000. Seed quantity alone therefore does not explain the failure.

### Interpretations that remain untested

- **Separate catalyst and solvent effects remain unidentified.** Batches 1, 4, 5, and 6 changed catalyst and solvent together. Saying C0 or S0 individually is superior would exceed the evidence.
- **The proposed early nucleation burst is an interpretation, not a direct observation.** No particle measurement was made during quench or at the first supersaturation crossing.
- **Persistent secondary nucleation is also untested.** End-point measurements cannot show whether fines appeared immediately or accumulated during cooling and stirring.
- **The apparent advantage of lower loading is not causally established.** Batch 12 changed reagent amount, solvent volume, and catalyst-to-reagent ratio simultaneously. Its superior selectivity and recovery may reflect any combination of those changes.
- **The reason batch 11’s byproduct signal fell to ≈0.030 is unresolved.** Selective impurity washing is plausible, but altered sampling basis after resuspension is an alternative.
- **The normalized size/fines relationship remains uncertain.** Batch 12’s size value implies a nominal d50 near 20.5 µm while F20 was reported as 1.000. Measurement noise or a distribution concentrated near 20 µm could explain this, but neither was tested.

## 2. One additional experiment

I would run one low-loading C1/S0 batch with repeated, non-destructive particle-size measurements along a deliberately diagnostic thermal history:

1. Use the low-loading reaction recipe and quench/reheat to 300 K.
2. Add a moderate, characterized seed charge.
3. Measure immediately after seeding and after small cooling increments near 298, 294, and 290 K.
4. Continue to 278 K and measure again after both a short and a long hold.
5. Warm the same slurry to about 315 K, measure, then recool slowly to 278 K and measure once more before filtration.

This single trajectory would distinguish three competing explanations:

- **Early nucleation burst:** F20 would rise sharply at the first supersaturation crossing and then remain nearly constant, even as recovery grows.
- **Persistent secondary nucleation:** F20 would continue increasing during cooling or the isothermal hold, particularly with continued stirring.
- **Reversible dissolution/ripening limitation:** Warming to 315 K would selectively remove small particles, lowering F20 and increasing normalized size; slow recooling would preserve at least part of that improvement.

If measurements remained saturated near F20=1 while recovery and d50 changed appreciably, that would instead raise concern about an unusually narrow distribution at the threshold or insufficient discrimination in the particle-summary channel. This experiment would not independently resolve catalyst and solvent main effects, but it targets the campaign’s dominant unresolved failure more directly than another endpoint-only material screen.

## 3. Least effectively used observation and least reliable prediction

### Least effectively used observation

Batch 11’s large decrease in byproduct signal after filtration, resuspension, and refiltration was used least effectively. I noted it as possible impurity removal but did not integrate it into a quantitative separation mechanism. It could indicate that washing strongly decouples chemical purity from reaction selectivity, or it could be an artifact of the changed analytical phase and sample basis. Because there was no matched final assay immediately before resuspension, the observation cannot presently distinguish those explanations.

### Least reliable held-out prediction

**Q09 is the least reliable prediction.** It stops after only 60 seconds of cooling to 292 K, whereas all campaign crystallizations were observed after hours of cooling or aging. The predicted near-zero seed-excluded yield therefore requires a large temporal extrapolation. In addition, the recipe contains seed crystals, creating uncertainty about how seed-only solids influence `particles_present`, purity, size, and fines when almost no new target has deposited. Q01/Q02 and Q12 also carry substantial material and loading uncertainty, but Q09 combines an entirely untested time regime with ambiguous seed-dominated particle metrics.
