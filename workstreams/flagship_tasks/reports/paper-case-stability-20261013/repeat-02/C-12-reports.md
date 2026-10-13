# C-12 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Reaction–crystallization coupling

The process has two linked but distinct yield stages. A useful decomposition is

\[
Y_{\text{overall}} \approx Y_{\text{reaction}}\,Y_{\text{crystal}},
\]

provided the reported reaction yield and pre-separation target basis are compatible. Here, crystal yield is specifically the seed-excluded recovered target divided by target present before separation. Thus upstream conversion/selectivity controls how much target and impurity enter crystallization, whereas crystal yield measures recovery of that available target.

This distinction matters. Batch 5 (C1/S1) had the strongest observed reaction performance—reaction yield about 0.603 and selectivity about 0.609—and the highest crystal recovery, 0.474, but its fines fraction was 1.00. Batch 11 (C1/S2) had lower reaction yield, about 0.499, and crystal recovery 0.448, but much better, though still noncompliant, fines of 0.587. Therefore maximizing target formation alone did not produce an acceptable particle population.

Purity was comparatively insensitive: every completed batch exceeded 0.80, generally reaching 0.97–1.00. Even where reaction byproduct signals were appreciable, the recovered crystals remained pure. This suggests effective impurity rejection by the tested crystallizations, although it does not establish whether rejection arose from equilibrium partitioning, growth-face selectivity, washing during filtration, or the synthetic benchmark’s response law.

### 2. Material effects

The initial prior favored S2 because its nominal properties combined low relative solubility (0.70), low nucleation tendency (0.65), high growth (1.30), and low impurity occlusion (0.65). The campaign qualitatively supported S2 for particle quality:

- Batch 5, S1/C1: crystal yield 0.474, purity 0.979, fines 1.00.
- Batch 9, S3/C1: yield 0.345, purity 0.971, fines 0.699.
- Several S2/C1 batches produced fines near 0.58–0.60, notably batches 2, 7, 10, and 11.

Thus S1 favored recovery but strongly disfavored the measured number-weighted size distribution. S2 provided the best observed compromise. S3 was intermediate. S0 was not experimentally tested, so no empirical claim about it is justified.

For a qualitative crystallization model, define supersaturation as

\[
S=C/C^*(T,\text{solvent}), \qquad \Delta\mu=RT\ln S.
\]

Typical relationships are

\[
J\propto \exp\left[-B/(\ln S)^2\right],\qquad
G=k_g(S-1)^g,
\]

where nucleation rate \(J\) rises sharply with supersaturation while crystal growth \(G\) usually rises more smoothly. S2’s lower nominal solubility can raise recovery at low temperature, while its lower nucleation tendency and higher growth tendency can direct material toward existing crystals rather than new fines. The data are consistent with that interpretation, but they do not uniquely prove these equations or identify their parameters.

Catalyst C1 was the most useful tested catalyst. Batch 3 substituted C3 in S2 and gave lower reaction selectivity (0.383), higher degradation warning (0.386), lower reaction yield (0.383), and lower crystal recovery (0.281) than the principal C1/S2 trials. However, catalyst, reaction temperature, reaction duration, and seed protocol were changed together, so this is not an isolated catalyst comparison. C3 should be described as inferior under the tested batch-3 history, not intrinsically inferior.

### 3. Seeding and number-weighted fines

The relevant quality metric was

\[
f_{<20}=\frac{N(d<20\,\mu\mathrm m)}{N_{\mathrm{total}}}.
\]

Because this is number-weighted, a small mass of numerous tiny particles can dominate the result even when most solid mass resides in larger crystals.

The seed response was nonmonotone:

- Batch 3 used only 0.005 g seed and ended with fines about 0.995 and recovery 0.281.
- Batch 4 used 0.20 g total seed and ended with fines 1.00 and recovery 0.261.
- Moderate doses of 0.03–0.05 g gave substantially better outcomes: batch 2 had fines 0.593, batch 10 had 0.602, and batch 11 had 0.587.

My interpretation is that too little seed did not provide enough growth surface to intercept supersaturation, allowing secondary nucleation. Excessive seed likely introduced too many number-counted small particles and distributed available product over too many growth centers. Moderate seeding balanced nucleation suppression and growth per particle. This revised the original assumption that simply increasing seed would continually suppress fines.

### 4. Process-history dependence

Final temperature alone did not determine the outcome. The entire thermal and solids history mattered:

- Batch 8 crystallized and aged at 300 K but produced fines 0.987, despite purity 0.979 and recovery 0.364.
- Batches 10 and 11 cooled to 250 K and underwent long aging, giving much lower fines of 0.602 and 0.587 and higher recoveries of 0.457 and 0.448.
- Batch 12 first formed and aged crystals at 250 K, then received a final 315 K warming before filtration. Fines returned to 1.00 and recovery fell to 0.297.

The adverse batch-12 result indicates that final warming was not a benign size-polishing step. Possible interpretations include preferential dissolution that left many small seed-derived particles, dissolution followed by rapid secondary precipitation during subsequent handling, or a benchmark-specific population-balance response. These alternatives cannot be separated from the available observations.

Reheat/recool cycles also failed to give a decisive improvement. Batch 6, with a 305 K reheat and recooling, had fines 0.604. Batch 7 used stronger repeated warm cycles plus filtration, resuspension, recooling, and refiltration; it reached the campaign’s lowest numerical fines result, 0.575, but only with recovery 0.401. This is not evidence that repeated cycling is reliably beneficial because the improvement was small, the protocol was highly confounded, and there were no replicates.

Long low-temperature aging appeared more useful than warm aging, but the mechanism remains unresolved. It could reflect continued growth, Ostwald ripening, delayed precipitation, or simply the combined effects of deeper cooling and elapsed time. Stirring was also confounded: batch 10 used 300 rpm aging while batch 11 used 100 rpm, alongside different seed doses and aging durations. Consequently, shear-induced breakage versus mass-transfer enhancement was not isolated.

### 5. Revisions and uncertainty

The initial expectations were partly revised:

1. **S2 preference:** qualitatively supported for fines control, although it did not achieve specification.
2. **More seed is better:** rejected; the observed response was nonmonotone, with both low and excessive seed performing poorly.
3. **Warm dissolution/recrystallization removes fines:** rejected for the tested implementations. Mild cycles did not cross the limit, and the final 315 K treatment in batch 12 was strongly adverse.
4. **Reaction optimization is sufficient:** rejected. Batch 5 showed that strong reaction performance and high recovery can coexist with unacceptable particle quality.

The final-assay noise specification for fines was about 0.018. The difference between batch 7 (0.575) and batch 11 (0.587) was only about 0.012, smaller than one assay-noise scale, so their ordering on fines is unresolved. Batch 11 nevertheless had higher recovery, 0.448 versus 0.401, much higher reported purity, 0.995 versus 0.981, and a simpler history. That supports the sealed choice of batch 11 as the best fallback, not as a specification-compliant process.

No batch met the fines requirement of 0.50. The best results remained roughly 0.075–0.10 above it, while purity was comfortably compliant. Moreover, the study lacked replicated recipes, so fixed process variability and several-factor confounding cannot be quantified. The remaining central tradeoff is therefore unresolved: S1 gave the best recovery but extremely poor fines, whereas S2 lowered fines substantially while giving somewhat lower recovery, yet still did not cross the quality boundary.

Untested alternatives include narrower seed-dose optimization around 0.03–0.05 g, independently varied cooling ramps and aging times, controlled fines classification or size-selective separation, a carefully mapped partial-dissolution window below the harmful batch-12 treatment, and direct testing of S0. These are hypotheses for future work, not conclusions from the completed campaign.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.4 | 0.24 | 0.59 |
| Q01 | crystal_purity | 0.98 | 0.94 | 1 |
| Q01 | crystal_size | 0.12 | 0.07 | 0.18 |
| Q01 | crystal_yield | 0.32 | 0.2 | 0.45 |
| Q02 | crystal_fines_fraction | 0.54 | 0.36 | 0.72 |
| Q02 | crystal_purity | 0.96 | 0.91 | 0.99 |
| Q02 | crystal_size | 0.095 | 0.05 | 0.15 |
| Q02 | crystal_yield | 0.23 | 0.12 | 0.36 |
| Q03 | crystal_fines_fraction | 0.86 | 0.67 | 1 |
| Q03 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q03 | crystal_size | 0.035 | 0.012 | 0.075 |
| Q03 | crystal_yield | 0.17 | 0.06 | 0.3 |
| Q04 | crystal_fines_fraction | 0.43 | 0.25 | 0.64 |
| Q04 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q04 | crystal_size | 0.105 | 0.052 | 0.17 |
| Q04 | crystal_yield | 0.22 | 0.1 | 0.36 |
| Q05 | crystal_fines_fraction | 0.43 | 0.25 | 0.63 |
| Q05 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q05 | crystal_size | 0.11 | 0.055 | 0.175 |
| Q05 | crystal_yield | 0.22 | 0.1 | 0.36 |
| Q06 | crystal_fines_fraction | 0.7 | 0.5 | 0.88 |
| Q06 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q06 | crystal_size | 0.065 | 0.027 | 0.12 |
| Q06 | crystal_yield | 0.25 | 0.12 | 0.4 |
| Q07 | crystal_fines_fraction | 0.41 | 0.23 | 0.61 |
| Q07 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q07 | crystal_size | 0.115 | 0.058 | 0.18 |
| Q07 | crystal_yield | 0.23 | 0.11 | 0.37 |
| Q08 | crystal_fines_fraction | 0.86 | 0.68 | 1 |
| Q08 | crystal_purity | 0.96 | 0.89 | 1 |
| Q08 | crystal_size | 0.052 | 0.02 | 0.1 |
| Q08 | crystal_yield | 0.18 | 0.07 | 0.32 |
| Q09 | crystal_fines_fraction | 0.96 | 0.8 | 1 |
| Q09 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q09 | crystal_size | 0.025 | 0.006 | 0.06 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.9 | 0.71 | 1 |
| Q10 | crystal_purity | 0.95 | 0.86 | 0.99 |
| Q10 | crystal_size | 0.037 | 0.012 | 0.08 |
| Q10 | crystal_yield | 0.055 | 0.008 | 0.14 |
| Q11 | crystal_fines_fraction | 0.44 | 0.26 | 0.64 |
| Q11 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q11 | crystal_size | 0.11 | 0.055 | 0.175 |
| Q11 | crystal_yield | 0.22 | 0.1 | 0.36 |
| Q12 | crystal_fines_fraction | 0.68 | 0.47 | 0.87 |
| Q12 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q12 | crystal_size | 0.07 | 0.03 | 0.125 |
| Q12 | crystal_yield | 0.4 | 0.25 | 0.56 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and a crystallization step, so particles are expected even when seed-excluded recovery is small. Q01–Q02: I expect S1 to outperform S3 in the very slow ramp because of its lower nominal solubility/nucleation and higher growth tendency, although prior batches make this extrapolation uncertain. Q03–Q04: 0.001 g seed likely leaves inadequate growth surface and permits secondary nucleation; 0.045 g should markedly reduce fines. Q05–Q06: the slow staircase should suppress the nucleation burst relative to a 120 s crash; prolonged cold holding may recover material but cannot reliably erase the crash-generated number population. Q07–Q08: the 315 K reheat/rapid recool is predicted to undo much of the slow-ramp particle benefit, consistent with the adverse final warming in batch 12. Q09–Q10: two hours at 292 K should increase seed-excluded deposition relative to immediate filtration, but both remain low-recovery and fines-rich. Q11–Q12: doubling concentration should raise recovery while increasing supersaturation, occlusion risk and secondary nucleation, creating a quality/recovery tradeoff. Intervals are deliberately broad because S0 was untested, these charges are below the campaign scale, recipes are unreplicated, and several nominally feasible central estimates lie close enough to the fines boundary that their feasibility is uncertain.

## K2

## 1. Status of the main claims

### Supported within the tested scope

- **S2 was the most promising tested solvent for fines control.** Direct observation: several C1/S2 batches ended near 0.58–0.60 fines—batch 2: 0.593; batch 7: 0.575; batch 10: 0.602; batch 11: 0.587—whereas C1/S1 batch 5 gave 1.00 and C1/S3 batch 9 gave 0.699. Interpretation: S2 likely favored growth relative to secondary nucleation. This is qualitative because the histories were not identical.
- **Purity was not the binding constraint.** All final batches had purity above 0.80, generally 0.97–1.00. The direct observation is robust; the proposed explanation—selective impurity rejection during crystallization—is plausible but not uniquely established.
- **Reaction performance and particle quality were separable.** Batch 5 had strong reaction yield/selectivity and the highest crystal recovery, about 0.474, but fines of 1.00. Batch 11 had lower reaction yield and recovery, about 0.448, but substantially lower fines. This directly contradicts any claim that maximizing reaction performance alone guarantees acceptable crystals.
- **The final thermal history mattered.** Batch 12’s 315 K final warming produced fines of 1.00 and reduced recovery to 0.297, despite prior cold aging. Batch 8, aged at 300 K, also gave fines near 0.987, while deeply cooled batches 10 and 11 were near 0.60. The observation supports history dependence; dissolution, renucleation, and population-selection explanations remain interpretations.

### Contradicted or revised

- **“More seed continually reduces fines” was contradicted.** Batch 3 with 0.005 g seed gave fines about 0.995, but batch 4 with 0.20 g also gave 1.00. Moderate 0.03–0.05 g doses in batches 2, 10, and 11 were better. A nonmonotone seed response is consistent with the observations, although seed was confounded with other conditions.
- **Warm dissolution/recrystallization as a reliable polishing operation was contradicted for the tested implementations.** Batch 6 remained at 0.604 fines after a reheat/recool cycle; batch 7 reached only 0.575 after a complex sequence; batch 12 became markedly worse after final warming. A narrower useful temperature window remains possible but unshown.
- **The initial feasibility expectation was not achieved.** No batch satisfied fines ≤0.50, even though all satisfied purity ≥0.80.

### Still untested or unresolved

- S0 was never tested in the campaign; conclusions about it in the sealed predictions relied only on nominal properties and extrapolation.
- The individual effects of seed dose, aging duration, and agitation remain unresolved because batches 10 and 11 changed all three.
- No recipe was replicated, so process repeatability and between-batch variance are unknown.
- The apparent fines ordering of batches 7 and 11 is unresolved: 0.575 versus 0.587 is smaller than the declared assay-noise scale.
- Whether a narrowly controlled partial-dissolution step can selectively remove fines without sacrificing recovery remains untested.

## 2. One additional experiment

I would repeat the complete batch-11 process unchanged except for increasing seed from 0.030 g to 0.050 g: C1/S2 at the same charges, 373 K reaction for 3600 s, quench, cool to 250 K over 14400 s, fifteen 14400 s aging periods at 100 rpm, then filtration and final assay. A pre-filtration particle-size measurement would be included if instrument access permitted.

This uses batch 11 as a direct control and distinguishes two competing explanations for its improvement over batch 10:

1. **Seed-dose explanation:** 0.030 g was nearer the optimum than 0.050 g.
2. **History/agitation explanation:** the longer aging and lower stirring in batch 11, rather than seed dose, caused the difference.

Expected outcomes:

- If the new 0.050 g batch has appreciably higher fines than batch 11 under the otherwise identical history, that supports a seed optimum near 0.030 g.
- If it matches or improves on batch 11, the batch-10/batch-11 difference was more likely caused by aging duration, stirring, or ordinary variability rather than seed dose.
- If it crosses fines ≤0.50 while retaining recovery near 0.4–0.45, that would indicate a favorable interaction between adequate seeding and the long, gently agitated cold history.
- If both fines and recovery vary substantially without a coherent seed effect, the dominant conclusion would be that replication and process-variance estimation are needed before further mechanism discrimination.

## 3. Least effectively used evidence and least reliable prediction

The account used the **within-batch intermediate particle measurements** least effectively. For example, batch 6 measured about 0.565 fines before filtration but 0.604 in the final assay, while batch 7 measured about 0.590 before its first filtration and 0.575 at final assay. These paired observations show that differences of a few hundredths can arise from measurement modality, sampling time, filtration/resuspension history, or noise. I should have used them more explicitly to caution against attributing small final-assay differences to a mechanistic treatment effect.

The least reliable held-out prediction is **Q04**, especially its prediction of quality feasibility with fines centered at 0.43. It extrapolated to S0, which was entirely untested, at smaller charge and concentration, and assumed that a very slow ramp plus 0.045 g seed would overcome S0’s nominally high nucleation and low growth tendencies. The campaign’s evidence for a moderate-seed optimum was itself confounded, and even the best tested S2 processes did not cross 0.50. Accordingly, Q04’s direction relative to the 0.001 g-seed Q03 is more defensible than its absolute claim of feasibility.
