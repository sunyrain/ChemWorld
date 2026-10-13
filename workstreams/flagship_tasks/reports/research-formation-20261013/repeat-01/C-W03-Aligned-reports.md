# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The materials are anonymous benchmark identities, so the account is phenomenological rather than a claim about real chemical structures.

### 1. Material effects

**Observation.** Solvent S2 was the most useful crystallization medium overall. At full reagent loading, the simple S2/C1 process in batch 1 gave crystal recovery 0.471, purity 0.985 and fines fraction 0.683. S2 also gave recoveries near 0.49 in batches 5, 6, 10 and 11, generally with purity above 0.97. In broadly similar direct-cooling screens, S3 gave lower recovery (0.380) and fines 0.811 in batch 8, while S0 gave recovery 0.481 but fines clipped at 1.0 in batch 9. The S1/C2 batch 4 gave recovery 0.403, purity 1.0 and fines 1.0, although its catalyst differed.

**Interpretation.** These results are qualitatively consistent with the dossier for S2: relatively low solubility, high crystal-growth tendency and low impurity occlusion support recovery and purity. Its nominally low nucleation tendency was not enough to prevent secondary nucleation under the tested supersaturation histories. S0 and S1 did not improve the number-weighted fines distribution, and S3 produced somewhat larger particles but sacrificed recovery.

Catalyst effects were less securely resolved because catalyst comparisons were confounded with solvent, temperature or crystallization history. C1 was retained because it gave a strong practical baseline. C2 in batch 4 had lower reaction yield and selectivity, while C3 at 350 K in batch 2 was also inferior to the C1 baseline, but these are not controlled catalyst comparisons. C0 in batch 5 performed reasonably, showing that C1 superiority is not established as a general mechanistic law.

### 2. Reaction–crystallization coupling

The reaction and crystallization objectives are related but not identical. Crystal recovery was defined as

R_xtal = recovered seed-excluded target / target present before separation,

so it is a crystallization-stage fraction, not an overall yield from charged reagent. A useful approximate overall recovered-target fraction is

Y_overall ≈ Y_rxn × R_xtal.

For example, this is about 0.27 in batch 1, 0.32 in batch 11 and 0.29 in batch 12. Thus batch 11 was attractive even though its final particle specification failed.

The coupling probably operated through concentration and impurity loading. In a simple representation,

S = (C − C*)/C*,
J ≈ k_n S^n,
G ≈ k_g S^g,

where S is supersaturation, J is nucleation rate and G is growth rate. Reaction conversion and selectivity determine the target and impurity concentrations entering crystallization; solvent and temperature determine C* and the kinetic coefficients. When nucleation rises more steeply with S than growth does, deep cooling can recover substantial target while producing many sub-20-µm particles.

This explains the principal unresolved tradeoff: most S2 processes achieved recovery around 0.47–0.50 and very high purity, but the same supersaturation that drove recovery also generated excessive fines. Purity was never the binding constraint; particle count distribution was.

### 3. Process-history dependence

The results show that final temperature alone did not determine the crystal population.

* Batch 1 used 0.020 g seed, direct cooling to 278 K and a subsequent hold. It gave the best full-loading fines result: 0.683, with recovery 0.471 and CSD quality 0.624.
* Lower seed plus staged slow cooling and long holds in batch 2 produced fines 1.0 and recovery 0.412. Raising seed to 0.050 g with another staged path in batch 3 still gave fines 0.838 and recovery 0.473. Seed amount therefore did not have a simple monotonic effect.
* Unseeded direct cooling in batch 5 gave recovery 0.490 but fines 1.0. Seed omission did not suppress formation of a numerous fine population.
* A partial 310 K reheat followed by recooling in batch 6 gave recovery 0.497 but fines 1.0 and smaller crystals. The likely interpretation is that reheating did not selectively eliminate fines; subsequent recooling regenerated nuclei or redistributed product into a fine population.
* Shallow cooling to 320 K in batch 7 lowered recovery to 0.359 without solving the problem: fines remained 0.987. This contradicted the prospective hypothesis that simply avoiding deep cooling would cross the fines threshold.
* Filtration, S2 resuspension and refiltration in batch 10 left fines at 1.0. The tested wash did not act as an effective size classifier and may have introduced additional handling risk.

Collectively, these observations imply population memory. Once a large number of nuclei formed, later holds, reheating or washing did not reliably convert them into a low-fines product. Possible mechanisms include secondary nucleation, seed-size effects, attrition during agitation, and insufficient Ostwald ripening. These alternatives were not separately measured.

### 4. Loading effect and revision of the mechanism

The strongest late-stage result came from changing upstream loading. Batch 11 reduced reagent charge from 0.040 to 0.020 mol while using 0.075 L S2, C1, 0.020 g seed and direct cooling to 278 K. It gave recovery 0.492, purity 0.994 and the campaign-low fines fraction of 0.591. Reaction yield and selectivity also rose to 0.654 and 0.674.

This initially supported the interpretation that lower concentration reduced supersaturation and secondary nucleation without sacrificing crystallization recovery. However, batch 12 tested 0.010 mol reagent under the same nominal framework and contradicted a monotonic loading law: recovery fell to 0.402 and fines rose to 0.846, although purity remained 0.996 and reaction selectivity increased further.

A plausible interpretation is an interior operating window near the batch-11 loading. At still lower target concentration, the fixed 0.020 g seed dose becomes larger relative to available product, growth per seed may be limited, and the number-weighted distribution can again be dominated by small seed-derived or newly nucleated particles. This explanation is consistent with the observations but remains untested because seed number and initial seed-size distribution were not measured.

### 5. Revisions and uncertainty

The initial hypothesis was that S2, modest seeding and slow cooling would jointly yield large, low-fines crystals. S2 was supported for recovery and purity but not for fines. The subsequent hypothesis that less seed would reduce fines was rejected by batch 2; a high seed dose also failed in batch 3. Reheat/recool, shallow cooling, solvent substitution, unseeded operation and washing were then tested and shelved. Moderate loading reduction was promising in batch 11, but batch 12 showed that its benefit was non-monotonic.

Final-assay standard deviations were approximately 0.018 for fines, 0.010 for recovery and 0.010 for purity. Batch 11 exceeded the fines limit by 0.091, much larger than its stated instrumental noise, so it cannot reasonably be called compliant. Between-batch process variability is less well characterized because most recipes were single, partially confounded experiments without replicates.

No batch met both required constraints. Batch 11 remains the closest observed compromise—recovery 0.492, purity 0.994 and fines 0.591—but the quality/recovery tradeoff is unresolved. The most informative future tests would map loading around 0.020 mol while independently varying seed mass and seed-size distribution, or introduce a genuine post-crystallization size-classification step. Those alternatives were not tested here.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.2 | 0.5 |
| Q01 | crystal_purity | 0.98 | 0.94 | 1 |
| Q01 | crystal_size | 0.16 | 0.1 | 0.23 |
| Q01 | crystal_yield | 0.5 | 0.39 | 0.61 |
| Q02 | crystal_fines_fraction | 0.55 | 0.38 | 0.72 |
| Q02 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q02 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q02 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q03 | crystal_fines_fraction | 0.73 | 0.56 | 0.89 |
| Q03 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q03 | crystal_size | 0.08 | 0.04 | 0.14 |
| Q03 | crystal_yield | 0.4 | 0.28 | 0.52 |
| Q04 | crystal_fines_fraction | 0.47 | 0.31 | 0.64 |
| Q04 | crystal_purity | 0.96 | 0.9 | 1 |
| Q04 | crystal_size | 0.12 | 0.07 | 0.19 |
| Q04 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q05 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q05 | crystal_purity | 0.97 | 0.91 | 1 |
| Q05 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q05 | crystal_yield | 0.44 | 0.32 | 0.56 |
| Q06 | crystal_fines_fraction | 0.82 | 0.66 | 0.95 |
| Q06 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q06 | crystal_size | 0.07 | 0.03 | 0.12 |
| Q06 | crystal_yield | 0.47 | 0.35 | 0.59 |
| Q07 | crystal_fines_fraction | 0.38 | 0.23 | 0.55 |
| Q07 | crystal_purity | 0.97 | 0.91 | 1 |
| Q07 | crystal_size | 0.15 | 0.09 | 0.22 |
| Q07 | crystal_yield | 0.45 | 0.33 | 0.57 |
| Q08 | crystal_fines_fraction | 0.76 | 0.58 | 0.91 |
| Q08 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q08 | crystal_size | 0.08 | 0.04 | 0.14 |
| Q08 | crystal_yield | 0.39 | 0.27 | 0.52 |
| Q09 | crystal_fines_fraction | 0.94 | 0.81 | 1 |
| Q09 | crystal_purity | 0.96 | 0.89 | 1 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.08 |
| Q09 | crystal_yield | 0.07 | 0.01 | 0.16 |
| Q10 | crystal_fines_fraction | 0.82 | 0.65 | 0.95 |
| Q10 | crystal_purity | 0.96 | 0.89 | 1 |
| Q10 | crystal_size | 0.06 | 0.02 | 0.11 |
| Q10 | crystal_yield | 0.17 | 0.08 | 0.29 |
| Q11 | crystal_fines_fraction | 0.42 | 0.26 | 0.59 |
| Q11 | crystal_purity | 0.97 | 0.91 | 1 |
| Q11 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q11 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q12 | crystal_fines_fraction | 0.62 | 0.44 | 0.79 |
| Q12 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q12 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q12 | crystal_yield | 0.52 | 0.4 | 0.64 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even when little new product is recovered. Q01–Q02 isolates solvent: S1 is predicted to outperform S3 through lower solubility, lower nucleation tendency and lower impurity occlusion. Q03–Q04 compares seed dose in nucleation-prone S0; more seed should moderate supersaturation and reduce secondary nucleation, although uncertainty spans the fines limit. Q05–Q06 compares slow ramping with a rapid temperature crash followed by equal low-temperature residence; the crash is expected to generate substantially more fines. Q07–Q08 tests post-ramp history: reheating and rapid recooling are predicted to dissolve some product and regenerate nuclei, unlike a simple growth hold. Q09–Q10 tests a shallow 292 K hold; added residence should increase recovery and size, but both remain fine-rich. Q11–Q12 compares loading: higher loading should raise recovery but also supersaturation and fines. Purity is expected to remain above 0.80 throughout. Intervals are deliberately broad because the campaign contained mostly single, confounded runs and did not directly validate these exceptionally long ramps, high seed-to-product ratios, or the exact 0.004–0.008 mol loading range.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Purity was not the binding constraint.** All 12 final assays reported crystal purity above 0.97, whereas every batch had fines above 0.50. Thus the campaign directly supports the conclusion that particle population, not chemical purity, limited feasibility.
- **S2 was a robust recovery/purity medium within the tested domain.** S2 batches commonly gave recovery near 0.47–0.50 with high purity: batch 1 (0.471, 0.985), batch 5 (0.490, 0.976), batch 6 (0.497, approximately 1.00), batch 10 (0.479, 0.977), and batch 11 (0.492, 0.994). Interpreting this as low effective solubility and favorable growth/occlusion behavior is plausible, but those kinetic causes were not directly measured.
- **Batch 11 was the closest observed compromise.** Its recovery was 0.492, purity 0.994 and fines 0.591. The 0.091 fines exceedance is much larger than the stated final-assay fines noise of 0.018, so it was not plausibly compliant merely because of measurement uncertainty.
- **A moderate loading reduction was beneficial, but the response was non-monotonic.** Relative to full-loading S2 recipes, batch 11 at 0.020 mol reagent had the lowest fines result. Further reduction to 0.010 mol in batch 12 lowered recovery to 0.402 and increased fines to 0.846. The direct observation contradicts a monotonic “less reagent always means fewer fines” law.
- **Final outcome depended on process history.** With broadly related S2 systems, batch 1’s simple cooling history gave fines 0.683, whereas staged long cooling in batches 2–3 gave 1.000 and 0.838, and reheating/recooling in batch 6 gave 1.000. These are observed differences, although their individual causal attribution is limited by other recipe changes.

### Contradicted or substantially weakened
- **Slow or staged cooling alone prevents fines:** contradicted by batches 2 and 3.
- **Reducing seed mass suppresses fines:** contradicted by batch 2, where 0.001 g seed still produced fines 1.000. Conversely, 0.050 g in batch 3 also failed, so no simple monotonic seed rule was supported.
- **No seed avoids a fine population:** contradicted by batch 5, which had fines 1.000.
- **A shallow endpoint solves secondary nucleation:** contradicted by batch 7; recovery fell to 0.359 while fines remained 0.987.
- **Partial reheating selectively removes fines:** contradicted for the tested 310 K cycle in batch 6, which finished at fines 1.000.
- **Resuspension/refiltration acts as useful size classification:** contradicted by batch 10, also at fines 1.000.

### Still untested
- Secondary nucleation, attrition and Ostwald ripening were interpretations; none was measured independently.
- Initial seed number, seed-size distribution and seed breakage were not characterized.
- Catalyst rankings remain unresolved because catalyst changes were confounded with solvent, temperature or crystallization history.
- An interior optimum near 0.020 mol loading is plausible but unconfirmed without neighboring points and replication.
- No genuine size-classification operation was tested; washing is not equivalent to sieving or selective fines removal.

## 2. One additional experiment

I would repeat the batch-12 chemistry—0.010 mol reagent, 0.075 L S2, C1 and the same reaction/direct-cooling history—but reduce seed from 0.020 to 0.010 g so that the seed-to-reagent ratio matches batch 11. I would characterize the seed population immediately after addition and again after cooling with the non-destructive particle-size measurement before filtration.

This uses batches 11 and 12 as existing controls and distinguishes two main explanations:

1. **Excess seed number relative to available product caused batch 12’s poor CSD.** Each seed received too little product to grow beyond the fines threshold. If so, halving seed should move fines substantially down from 0.846, potentially toward or below batch 11’s 0.591, while size increases. Recovery could remain around 0.40–0.48.
2. **Low product concentration intrinsically creates the unfavorable population through weak growth or cooling-induced nucleation.** If so, reducing seed will not rescue the result: terminal fines should remain high, recovery near batch 12’s 0.402, and the post-cooling measurement should show many newly formed fines relative to the initial seed measurement.

A third possible outcome—large run-to-run movement without a coherent change in seed-to-product behavior—would indicate that process variability is large enough that the apparent batch-11 loading optimum requires replication before mechanistic interpretation.

## 3. Least effectively used evidence and least reliable prediction

The account used the joint **crystal-size and fines observations** least effectively. It focused on fines but did not fully exploit their relationship to the number-weighted distribution. Batch 11’s size of 0.072 corresponds to an estimated d50 of about 18 µm, already below the 20 µm specification boundary, consistent with fines above 0.50. Conversely, batches such as 8 and 12 showed relatively larger reported size alongside unexpectedly high fines. That discordance could indicate a broad or multimodal population, independent channel noise, or imperfect consistency between the synthetic size summaries. It should have prompted more emphasis on distribution shape and seed characterization rather than treating “larger size” and “lower fines” as interchangeable.

**Q04 is the least reliable held-out prediction.** It classified a high-seed, very long, slowly cooled S0 process as feasible with predicted fines 0.47, but the 80% interval crossed the 0.50 boundary. More importantly, the campaign provided no controlled evidence that raising seed from 0.001 to 0.045 g under an otherwise identical S0 history reduces fines. The nearest evidence was confounded, while the actual S0 batch 9 and high-seed batch 3 both remained strongly fine-rich. Q04 therefore extrapolated a seed-mediated supersaturation mechanism across solvent, concentration and an exceptionally long cooling schedule; its feasibility label is much less secure than its numerical interval suggests.
