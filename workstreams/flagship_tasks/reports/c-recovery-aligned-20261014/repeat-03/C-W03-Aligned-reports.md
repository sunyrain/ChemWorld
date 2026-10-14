# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome
The sealed recommendation is **batch 9**. It used 0.040 mol reagent in 0.080 L solvent S3 with 0.005 mol catalyst C1, heated near 373 K for 1 h under nitrogen, quenched, charged with 0.05 g seed, cooled first to 300 K and then to 250 K, held at 250 K for twelve 4 h periods (48 h total), filtered, and assayed.

Its final observations were:
- seed-excluded crystal recovery: **0.4275**;
- crystal purity: **0.9764**;
- number fraction below 20 µm: **0.3881**;
- reaction yield: **0.4975**;
- conversion: approximately **1.00**.

Thus it was the only tested batch satisfying both purity ≥0.80 and fines ≤0.50 while retaining substantial recovery.

### Material effects
The initially favored solvent was S2 because its dossier suggested high growth, low nucleation, low solubility, and low impurity occlusion. Experimentally, S2 did support high recovery and purity, but not acceptable particle quality. Batch 1 (S2/C1) gave recovery 0.476 and purity 0.985, yet fines were 0.997. Batch 3 used very slow staged cooling and still gave recovery 0.474, purity 0.988, and fines 0.995. Batch 4 reached the largest observed recovery, 0.503, but its fines were clipped at 1.00. The empirical solvent response therefore overrode the nominal prior.

The standard C1 solvent screen separated chemical yield from particle quality:
- batch 5, S1: recovery 0.477, purity 0.979, fines 1.00;
- batch 6, S3: recovery 0.376, purity 0.993, fines 0.662;
- batch 7, S0: recovery 0.494, purity 0.980, fines 0.987.

S0 was favorable for reaction output—batch 7 had reaction yield about 0.619 and comparatively low degradation warning—but unfavorable for the number-weighted particle distribution. S3 lowered chemical yield but uniquely opened a route toward compliant particle quality. Purity was high throughout, suggesting that crystallization rejected much of the reaction-derived impurity even when reaction selectivity was only moderate.

Catalyst effects were also coupled to crystallization. Under the S3 deep-cooling/long-hold workup, changing C1 to C0, C2, or C3 produced batches 10–12. Their recoveries were 0.435, 0.349, and 0.372, but fines remained 0.693, 0.675, and 0.675. C0 therefore gave slightly higher recovery than recommended batch 9 but failed the fines constraint. This indicates that catalyst-dependent reaction composition or residual catalyst affected nucleation/growth, not merely conversion.

### Reaction–crystallization coupling
A useful recovery decomposition is

`Y_crystal = Y_reaction × f_precipitation × f_separation`,

where the last two factors are not separately observed. Because recovery is defined relative to initial reagent and excludes seed material, this expression is mechanistic bookkeeping rather than a fitted law. For batch 9, `Y_crystal/Y_reaction ≈ 0.4275/0.4975 ≈ 0.86`; for batch 7 the analogous ratio was about 0.80. S3/C1 therefore converted a smaller chemical product inventory into isolated crystals more efficiently under the deep-cold history, but it did not maximize upstream reaction yield.

The results are consistent with classical competition between nucleation and growth. If `S=C/C*(T,solvent)` is supersaturation, useful qualitative relations are

`J ∝ exp[-B/(ln S)^2]` for primary nucleation,

and

`G ∝ (S−1)^g` for crystal growth.

Solvent, impurities, catalyst residues, seed surface, cooling history, and agitation can change both coefficients. A high nucleation-to-growth ratio creates many particles below 20 µm; growth or maturation that carries particles across the 20 µm threshold lowers the reported number fraction. These equations organize the evidence but were not quantitatively fitted.

### Process-history dependence
Batch 9 demonstrates that endpoint composition and temperature alone were insufficient descriptors. At 300 K, before the deep-cold stage, its particle measurement showed fines of about 0.756. After cooling to 250 K and holding for 48 h, the final fines fell to 0.388 while recovery rose to 0.427. The observation supports a strong history effect from the combined deeper cooling and long maturation period.

Possible interpretations include continued growth of initially fine particles beyond 20 µm, consumption of dissolved product during the long hold, or population restructuring/aggregation. These mechanisms were not distinguished. Deep cooling and hold duration were changed together, so the data do not identify which was causal.

History effects were material-specific. In S2, increasing seed from 0.05 g to 1 g, extending low-temperature holds, adding a 300 K reheat/recool cycle, and using extremely slow multistage cooling all failed to lower fines materially (batches 2–4). Batch 2 did increase the size index to about 0.092, but fines remained 1.00. Thus larger apparent size did not guarantee an acceptable number fraction, presumably because a persistent fine-particle population dominated the count distribution.

With S3, raising seed to 2 g and adding extended holding plus reheating improved fines only modestly, from 0.662 in batch 6 to 0.633 in batch 8. Seed loading was therefore not the principal control variable in the tested range. Likewise, stopping at 300 K in batch 9 gave worse fines than the final deep-cold history.

### Revision of the working mechanism
The initial expectation was that S2 and C1 or C3, combined with slow cooling and seeding, would jointly maximize reaction performance and crystal growth. Batches 1–4 revised that view: S2 reliably gave good recovery and purity, but its fines remained near unity despite large changes in seed dose, cooling rate, hold time, and thermal cycling.

The next hypothesis was that solvent identity controlled the attainable particle regime. Batches 5–7 supported that revision by identifying S3 as the only solvent with substantially lower fines. A subsequent hypothesis that heavy seeding and ripening would be sufficient was weakened by batch 8. Batch 9 then showed that the combined 250 K endpoint and 48 h hold was the decisive tested history. Finally, batches 10–12 showed that this favorable S3 history was catalyst-specific: substituting C0, C2, or C3 lost compliance.

### Uncertainty and unresolved tradeoff
The recommendation is supported by one compliant batch rather than a replicate series. Instrument noise was much smaller than the approximately 0.112 margin between batch 9’s fines estimate and the 0.50 limit, but process repeatability was not established. The causal contributions of cooling to 250 K and holding for 48 h remain confounded. Seed size distribution, aggregation, and the identity of impurity species were not independently measured.

A clear recovery–quality tradeoff remains. Batches 4 and 7 achieved higher recoveries, approximately 0.503 and 0.494, but failed the fines constraint severely. Batch 10 slightly exceeded batch 9’s recovery under the S3 deep-cold workup, at 0.435, but had fines near 0.693. Purity was not the active limitation; particle-number distribution was. Accordingly, batch 9 is the best demonstrated feasible process, not proof of a global optimum.

Untested alternatives include separately varying the 250 K hold duration, using intermediate endpoints between 250 and 273 K, changing agitation during maturation, blending solvents, washing or classification after filtration, and optimizing the S3/C1 reaction temperature to raise upstream yield without changing the crystallization-active impurity profile.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.96 | 0.86 | 1 |
| Q01 | crystal_purity | 0.982 | 0.95 | 1 |
| Q01 | crystal_size | 0.065 | 0.035 | 0.1 |
| Q01 | crystal_yield | 0.27 | 0.19 | 0.35 |
| Q02 | crystal_fines_fraction | 0.62 | 0.5 | 0.74 |
| Q02 | crystal_purity | 0.978 | 0.945 | 1 |
| Q02 | crystal_size | 0.08 | 0.045 | 0.12 |
| Q02 | crystal_yield | 0.19 | 0.12 | 0.27 |
| Q03 | crystal_fines_fraction | 0.98 | 0.9 | 1 |
| Q03 | crystal_purity | 0.981 | 0.95 | 1 |
| Q03 | crystal_size | 0.068 | 0.035 | 0.105 |
| Q03 | crystal_yield | 0.26 | 0.18 | 0.35 |
| Q04 | crystal_fines_fraction | 0.94 | 0.83 | 1 |
| Q04 | crystal_purity | 0.982 | 0.95 | 1 |
| Q04 | crystal_size | 0.086 | 0.05 | 0.13 |
| Q04 | crystal_yield | 0.27 | 0.19 | 0.36 |
| Q05 | crystal_fines_fraction | 0.95 | 0.84 | 1 |
| Q05 | crystal_purity | 0.982 | 0.95 | 1 |
| Q05 | crystal_size | 0.09 | 0.052 | 0.135 |
| Q05 | crystal_yield | 0.27 | 0.19 | 0.36 |
| Q06 | crystal_fines_fraction | 0.985 | 0.91 | 1 |
| Q06 | crystal_purity | 0.969 | 0.925 | 0.998 |
| Q06 | crystal_size | 0.063 | 0.032 | 0.1 |
| Q06 | crystal_yield | 0.27 | 0.18 | 0.36 |
| Q07 | crystal_fines_fraction | 0.95 | 0.84 | 1 |
| Q07 | crystal_purity | 0.982 | 0.95 | 1 |
| Q07 | crystal_size | 0.091 | 0.053 | 0.137 |
| Q07 | crystal_yield | 0.27 | 0.19 | 0.36 |
| Q08 | crystal_fines_fraction | 0.9 | 0.76 | 0.99 |
| Q08 | crystal_purity | 0.986 | 0.955 | 1 |
| Q08 | crystal_size | 0.112 | 0.065 | 0.17 |
| Q08 | crystal_yield | 0.23 | 0.14 | 0.33 |
| Q09 | crystal_fines_fraction | 0.9 | 0.7 | 1 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.055 | 0.025 | 0.095 |
| Q09 | crystal_yield | 0.018 | 0.002 | 0.06 |
| Q10 | crystal_fines_fraction | 0.84 | 0.65 | 0.98 |
| Q10 | crystal_purity | 0.985 | 0.94 | 1 |
| Q10 | crystal_size | 0.068 | 0.035 | 0.115 |
| Q10 | crystal_yield | 0.105 | 0.04 | 0.19 |
| Q11 | crystal_fines_fraction | 0.95 | 0.84 | 1 |
| Q11 | crystal_purity | 0.982 | 0.95 | 1 |
| Q11 | crystal_size | 0.09 | 0.052 | 0.135 |
| Q11 | crystal_yield | 0.27 | 0.19 | 0.36 |
| Q12 | crystal_fines_fraction | 0.985 | 0.91 | 1 |
| Q12 | crystal_purity | 0.965 | 0.91 | 0.995 |
| Q12 | crystal_size | 0.061 | 0.03 | 0.1 |
| Q12 | crystal_yield | 0.4 | 0.3 | 0.5 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes include seeding, so particles are expected even where seed-excluded product recovery is small. For Q01–Q02, prior batches indicate that S3 should greatly reduce fines relative to S1 but also lower recovery; the 278 K endpoint is not deep enough to confidently reproduce the compliant S3/C1 result obtained after cooling to 250 K and holding 48 h. Q03–Q04 assign the larger seed charge a modest reduction in secondary nucleation and increase in number-weighted size, with little effect on seed-excluded yield. Q05–Q06 predict that gradual cooling produces fewer fines and larger particles than a rapid temperature drop followed by an equal-duration hold, while equilibrium recovery remains similar. Q07–Q08 treat the 315 K thermal cycle as partial dissolution/ripening: larger, cleaner crystals but some unrecovered product after the short recool. Q09–Q10 predict very low immediate recovery at 292 K and appreciable growth during the additional two-hour hold. Q11–Q12 assign higher loading more overall fractional recovery through greater supersaturation, but also more nucleation, impurity occlusion, and fines. Intervals are broad because these recipes use lower concentration and catalyst loading, a hotter/shorter reaction, and cooling histories not replicated in the campaign; paired directions are more certain than absolute values.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Solvent identity strongly affects particle quality.** Under comparable C1 workups, S3 gave much lower fines in batch 6 (0.662) than S1 in batch 5 (1.00), S0 in batch 7 (0.987), or S2 in batches 1–4 (approximately 0.98–1.00). This is a direct comparative observation; the proposed explanation in terms of solvent-dependent nucleation and growth remains interpretive.
- **Good recovery and acceptable fines were in tension.** Batch 4 had the highest observed recovery, about 0.503, but fines of 1.00. Batch 7 gave recovery 0.494 with fines 0.987. Batch 9 reduced recovery to 0.427 but met the fines constraint at 0.388. Purity remained above 0.96 in these cases, so fines—not purity—were the active constraint.
- **Process history mattered in S3.** In batch 9, the intermediate particle measurement at 300 K gave fines of about 0.756; after cooling to 250 K and holding for 48 h, the final estimate was 0.388. The direct observation supports an effect of the combined subsequent history, but does not separate temperature from elapsed hold time.
- **The successful S3 workup was catalyst-specific within the screen.** With the deep-cooling/long-hold workup, C0, C2, and C3 in batches 10–12 all gave fines near 0.68–0.69, whereas C1 in batch 9 gave 0.388. The direct result is catalyst dependence; attributing it specifically to residual catalyst or a changed impurity spectrum is interpretation.
- **Large seed additions and slow cooling were not sufficient in S2.** Batch 2 used much more seed and extended holding/thermal cycling, while batch 3 used very slow staged cooling. Both still had fines near 1.00. This contradicts the initial expectation that seeding or slow cooling alone would solve the S2 fines problem.

### Contradicted or weakened
- **The nominal dossier prediction that S2 would be the best crystallization solvent was contradicted for the constrained objective.** S2 supported recovery and purity but consistently failed the fines limit.
- **The hypothesis that more seed would be the principal route to acceptable particles was weakened.** Moving from the low-seed S3 process in batch 6 to the 2 g seeded, extended-history process in batch 8 improved fines only from about 0.662 to 0.633, still noncompliant. Because other history variables also changed, this is not a clean estimate of seed effect.
- **The claim that apparent crystal size alone diagnoses fines control is contradicted by the reported channels.** Batch 2 had a final size index near 0.092 but fines reported at 1.00. At face value, a number-weighted d50 above 20 µm is incompatible with all particles being below 20 µm. This may reflect independent noisy synthetic channels or a reporting inconsistency rather than physical behavior.

### Still untested
- Whether **250 K itself**, the **48 h hold**, or their interaction caused batch 9’s improvement.
- Whether the batch-9 result is reproducible; no replicate established process variance.
- Whether agitation, solvent blends, seed size distribution, washing, or post-filtration classification could improve recovery while retaining fines compliance.
- Whether catalyst effects on fines arise from catalyst residues, different byproduct profiles, degradation, or another correlated reaction-state variable.
- Quantitative nucleation and growth equations were organizational hypotheses only; their parameters were not fitted.

## 2. Most informative additional experiment

I would repeat the batch-9 S3/C1 recipe as one longitudinal experiment, using non-destructive particle-size measurements immediately upon reaching 250 K and after 4, 12, 24, and 48 h at 250 K, followed by filtration and final assay. All upstream conditions, seed charge, cooling path, and agitation would remain fixed.

This would distinguish two primary explanations:

1. **Low-temperature endpoint mechanism:** Cooling to 250 K directly establishes the favorable population. Fines should already be ≤0.50 at the first 250 K measurement, with little subsequent change.
2. **Time-dependent maturation mechanism:** Deep cooling initially creates a noncompliant population, but prolonged growth, aggregation, or population restructuring moves particles beyond 20 µm. Fines should begin above 0.50 and decline systematically during the hold, accompanied by increasing size.

A third outcome—little change followed by a late discontinuous shift—would suggest induction, aggregation, or another nonlinear transformation. If fines never fall below 0.50, batch 9 was likely a favorable realization or insufficiently reproducible. The final assay would show whether any particle improvement is accompanied by increasing recovery or by a loss of dissolved/solid target.

## 3. Least effectively used observation and least reliable prediction

The account used the **joint size and fines observation from batch 2** least effectively. It explained the larger size index alongside fines near 1.00 as a broad distribution with persistent fines, but that explanation does not respect the stated number-weighted definitions: a size index of 0.092 corresponds to a d50 near 23 µm, which should imply fewer than half the particles below 20 µm, not essentially all of them. This inconsistency should have been treated explicitly as a measurement-channel or model-coherence warning rather than mechanistically rationalized.

The least reliable held-out prediction is **Q09**. It filters only 60 s after cooling to 292 K, far outside the long crystallization histories observed in the campaign. Its seed-excluded yield depends on poorly constrained short-time nucleation and growth kinetics, while particle presence and reported purity may be dominated by the added seed even though seed material is excluded from the yield numerator. The recipe also uses lower reagent concentration and catalyst loading and a hotter, shorter reaction than the campaign. Consequently, both the small predicted recovery and the particle-quality estimates are extrapolations with little direct experimental support.
