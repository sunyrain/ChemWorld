# C-W05-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended operating region and observations
The sealed recommendation remains **batch 8**. It used 0.04 mol reagent and 0.005 mol catalyst C1 in 0.060 L solvent S1, reacted at 360 K for 3600 s with 400 rpm stirring, received 0.050 g seed, was cooled first to 310 K over 7200 s and then to 250 K over 14400 s, held for 7200 s at 150 rpm, filtered, and assayed. Its final measurements were crystal recovery 0.537, crystal purity 0.985, and fines number fraction 0.403. Reaction conversion was 1.000, selectivity 0.587, reaction yield 0.579, and degradation warning 0.156.

The closest support for this operating region is batch 6, which used the same S1 process with catalyst C3: recovery 0.534, purity 1.000, and fines 0.409. Batch 10, with catalyst C1 but twice the seed mass (0.100 g), also remained feasible: recovery 0.529, purity 0.983, and fines 0.428. Batch 12 shortened the final cold hold to 3600 s and gave recovery 0.523, purity 0.999, and fines 0.418. Thus the recommendation rests more strongly on a reproducible S1/staged-cooling region than on the very small numerical advantage of batch 8 alone.

### Reaction–crystallization coupling
Two distinct yield quantities are important. A useful accounting approximation is

`overall isolated target/feed ≈ reaction target yield × crystallization recovery`,

where crystallization recovery is

`R_c = seed-excluded target recovered in crystals / target present before separation`.

It is therefore conditional on the target already produced and is not the overall synthetic yield. For batch 8, the approximate combined fraction is 0.579 × 0.537 ≈ 0.31. Batch 6 is similarly about 0.585 × 0.534 ≈ 0.31. Catalyst or reaction changes can alter total isolated material through conversion and selectivity even when their conditional crystal recoveries are similar.

The reaction also establishes target concentration, impurity loading, and degradation products before cooling. These quantities affect supersaturation and possible impurity adsorption or occlusion. Across the campaign, conversion was usually near unity, while selectivity varied materially—for example, approximately 0.463 in batch 3, 0.505 in batch 4, 0.582 in batch 6, and 0.587 in batch 8. Nevertheless, final crystal purity was generally 0.97–1.00. The observation is that crystallization rejected most reaction impurities under the tested conditions; the interpretation is that impurity partitioning favored the mother liquor. Direct impurity partition coefficients were not measured, so selective rejection rather than a specific molecular interaction is the defensible mechanism.

Catalyst effects were clearer in reaction metrics than in crystal recovery. C2/S2 batch 3 had relatively low selectivity and reaction yield, while C1/S1 batch 8 and C3/S1 batch 6 were similar. Because catalyst comparisons also changed solvent or other histories in several batches, a catalyst-specific causal ranking remains unresolved. The near equality of batches 6 and 8 specifically indicates that C1 versus C3 was not a dominant determinant of crystallization recovery in this operating window.

### Material effects
Before experimentation, S2 appeared attractive from its nominal low solubility, high growth, low nucleation, and low impurity-occlusion descriptors. Experiments revised that expectation. S2 did produce very pure crystals and could satisfy the fines constraint: batch 4 gave recovery 0.444, purity 1.000, and fines 0.320. However, S1 gave substantially higher feasible recoveries in batches 6 and 8, around 0.53–0.54. This is consistent with the stated possibility of fixed world-specific solvent residuals overriding nominal reference-panel trends.

Solvent identity strongly shifted the recovery–quality tradeoff. Under otherwise similar staged conditions:

- S1, batch 6: recovery 0.534 and fines 0.409—feasible.
- S2, batch 4: recovery 0.444 and fines 0.320—cleaner particle distribution but lower recovery.
- S3, batch 5: recovery 0.408 and fines 0.662—failed the fines constraint.
- S0, batch 7: recovery 0.560, the highest numerical recovery observed, but fines 0.645—also failed.

Thus S0 demonstrated that maximizing precipitation alone was not sufficient: the additional recovered material was associated with excessive particle-number nucleation. S2 favored particle quality at the expense of recovery, whereas S1 gave the best observed balance. Purity did not create the main tradeoff because it remained above 0.80 in all cited final assays; fines were the binding quality constraint.

### Supersaturation and process-history dependence
A conventional qualitative description is

`S = C/C*`,

with crystal growth often represented as `G = k_g(S − 1)^g` and primary nucleation as `J ≈ k_n exp[-B/(ln S)^2]`. These are explanatory relationships, not fitted laws for this benchmark. They express why rapid or deep supersaturation can raise recovery while disproportionately increasing the number of fines.

Batch 2 illustrates that tradeoff. It used S2, a larger total seed dose, a single deep cool to 250 K, and a cold hold. Recovery rose to 0.472, but fines rose to 0.566 and failed the constraint. In contrast, staged cooling through 310 K before reaching the low-temperature endpoint generally allowed existing seeds and crystals to consume supersaturation before a large secondary-nucleation burst. Batch 4, for example, retained fines near 0.320 while recovering 0.444.

Concentration also mattered. Batch 9 reduced S1 solvent volume from 0.060 to 0.040 L. It did not improve recovery relative to batches 6 or 8 (0.534) but moved fines to 0.505, just beyond the specification. The mechanistic interpretation is that the higher concentration generated a larger supersaturation excursion and more nucleation. Because its fines result lies only slightly above 0.50, measurement noise makes the exact classification uncertain; nevertheless, it lacks the quality margin of the recommended 0.060 L process.

Seed addition provides crystal surface area on which supersaturation can be relieved by growth, but more seed was not monotonically beneficial. Increasing seed from 0.050 g in batch 8 to 0.100 g in batch 10 produced similar recovery and fines rather than a clear improvement. Batch 2 also combined more seed with excessive fines, although several other variables changed. The data therefore support using seed to control nucleation, but they do not establish an optimal seed mass or a causal benefit from doses above 0.050 g.

Residence time had a non-monotonic effect. The ordinary 7200 s cold hold in batches 6 and 8 was feasible, and the shorter 3600 s hold in batch 12 was also feasible. By contrast, batch 11 used three consecutive 14400 s cold holds and ended with recovery 0.478 and fines 0.660. Possible explanations include late secondary nucleation, agitation-driven attrition, transformation or dissolution/reprecipitation, or an unfavorable interaction with its lower 340 K reaction history. Because batch 11 changed both reaction temperature and hold duration, these alternatives were not separated. Its result rejects the simple assumption that indefinitely extending the cold hold must improve recovery or particle size.

### Revisions, uncertainty, and unresolved tradeoffs
The principal revision was from a nominal-property preference for S2 to an experimentally supported preference for S1. A second revision was abandoning the simple expectation that deeper cooling, more seed, or longer holding would monotonically improve recovery without compromising fines. The observed response depended on the entire supersaturation history.

The final-assay noise scales were approximately 0.01 for crystal recovery and 0.018 for fines, before considering process variation. Consequently, the 0.003 recovery difference between batches 8 and 6 is not persuasive evidence that C1 is intrinsically better than C3. Their agreement instead supports the robustness of the broader S1 staged-cooling region. Batch 8 was selected because it had the highest measured recovery among batches satisfying both constraints, not because its small lead was mechanistically definitive.

The unresolved optimization frontier is between roughly 0.53–0.54 feasible recovery with fines around 0.40–0.43 in S1 and roughly 0.56 recovery with unacceptable fines around 0.65 in S0. Batch 9 suggests that increasing S1 supersaturation approaches the same boundary without increasing recovery. Purity had ample margin, but the fines constraint remained sensitive to solvent, concentration, cooling history, and excessive holding. Untested alternatives include finer multistage cooling schedules, controlled seed-size distributions, agitation changes separated from residence-time changes, and independent factorial tests of reaction temperature and cold-hold duration. None of those alternatives was experimentally established in this campaign.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.32 | 0.2 | 0.46 |
| Q01 | crystal_purity | 0.975 | 0.93 | 0.998 |
| Q01 | crystal_size | 0.18 | 0.11 | 0.26 |
| Q01 | crystal_yield | 0.4 | 0.29 | 0.51 |
| Q02 | crystal_fines_fraction | 0.53 | 0.38 | 0.68 |
| Q02 | crystal_purity | 0.965 | 0.9 | 0.995 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q02 | crystal_yield | 0.33 | 0.22 | 0.45 |
| Q03 | crystal_fines_fraction | 0.58 | 0.42 | 0.73 |
| Q03 | crystal_purity | 0.955 | 0.88 | 0.99 |
| Q03 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q03 | crystal_yield | 0.34 | 0.21 | 0.47 |
| Q04 | crystal_fines_fraction | 0.31 | 0.19 | 0.46 |
| Q04 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q04 | crystal_size | 0.19 | 0.11 | 0.28 |
| Q04 | crystal_yield | 0.37 | 0.25 | 0.5 |
| Q05 | crystal_fines_fraction | 0.28 | 0.17 | 0.42 |
| Q05 | crystal_purity | 0.972 | 0.92 | 0.997 |
| Q05 | crystal_size | 0.2 | 0.12 | 0.29 |
| Q05 | crystal_yield | 0.38 | 0.26 | 0.51 |
| Q06 | crystal_fines_fraction | 0.65 | 0.49 | 0.79 |
| Q06 | crystal_purity | 0.935 | 0.84 | 0.985 |
| Q06 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q06 | crystal_yield | 0.43 | 0.3 | 0.57 |
| Q07 | crystal_fines_fraction | 0.27 | 0.16 | 0.41 |
| Q07 | crystal_purity | 0.972 | 0.92 | 0.997 |
| Q07 | crystal_size | 0.21 | 0.13 | 0.3 |
| Q07 | crystal_yield | 0.39 | 0.27 | 0.52 |
| Q08 | crystal_fines_fraction | 0.21 | 0.11 | 0.36 |
| Q08 | crystal_purity | 0.982 | 0.94 | 0.999 |
| Q08 | crystal_size | 0.24 | 0.15 | 0.34 |
| Q08 | crystal_yield | 0.36 | 0.23 | 0.49 |
| Q09 | crystal_fines_fraction | 0.72 | 0.55 | 0.86 |
| Q09 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q09 | crystal_size | 0.045 | 0.02 | 0.08 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.14 |
| Q10 | crystal_fines_fraction | 0.58 | 0.41 | 0.73 |
| Q10 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q10 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q10 | crystal_yield | 0.17 | 0.08 | 0.29 |
| Q11 | crystal_fines_fraction | 0.29 | 0.17 | 0.44 |
| Q11 | crystal_purity | 0.97 | 0.91 | 0.997 |
| Q11 | crystal_size | 0.2 | 0.12 | 0.3 |
| Q11 | crystal_yield | 0.39 | 0.26 | 0.52 |
| Q12 | crystal_fines_fraction | 0.54 | 0.37 | 0.69 |
| Q12 | crystal_purity | 0.94 | 0.85 | 0.987 |
| Q12 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q12 | crystal_yield | 0.55 | 0.41 | 0.68 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even where seed-excluded product recovery is small. Q01–Q02 apply the observed solvent ranking: S1 gave a much better recovery/fines balance than S3 in batches 6–8 versus batch 5, although the unusually slow cooling should improve both relative to the source runs. Q03–Q04 assign the larger seed charge more surface area for growth and suppression of secondary nucleation; its effect on seed-excluded recovery is modest. Q05–Q06 contrast gradual supersaturation generation with a temperature crash: the crash may precipitate slightly more target but should produce substantially more fines and smaller particles, consistent with the campaign's recovery–fines tradeoff. Q07–Q08 treat the 315 K anneal as partial dissolution of fines followed by regrowth, increasing size and purity and lowering fines at a small recovery cost. Q09–Q10 predict that a two-hour 292 K hold raises recovery and permits some growth, but neither short process reliably clears the fines limit. Q11–Q12 express the concentration tradeoff: doubling reagent loading raises fractional recovery but also nucleation, occlusion risk, and fines. The 80% intervals are deliberately broad because these recipes extrapolate to lower scale, 385 K reaction conditions, and multi-day cooling histories not directly tested; classifications near fines=0.50 are consequently uncertain.

## K2

## 1. Status of the main claims

### Supported by observations
- **S1 plus staged cooling defines a reproducibly feasible region.** Batches 6, 8, 10, and 12 all had purity above 0.98 and fines below 0.50, with crystal recovery from 0.523 to 0.537. This is a direct observation. Interpreting it as a robust operating region is reasonable, although the experiments were not full independent replicates.
- **Solvent materially changes the recovery–fines balance.** Under closely matched staged processes, S1 batch 6 gave recovery 0.534 and fines 0.409; S2 batch 4 gave 0.444 and 0.320; S3 batch 5 gave 0.408 and 0.662; and S0 batch 7 gave 0.560 and 0.645. The numerical differences are observed. Assigning them specifically to solvent-dependent solubility, growth, or nucleation is mechanistic interpretation because those rates were not measured directly.
- **Fines, rather than purity, were the binding constraint.** The cited final assays generally showed purity around 0.97–1.00, while several batches failed because fines exceeded 0.50. This is directly observed.
- **Increasing concentration did not improve the tested S1 process.** Reducing S1 volume from 0.060 L in batch 8 to 0.040 L in batch 9 left recovery essentially unchanged—0.537 versus 0.534—but raised fines from 0.403 to 0.505. The result is observed; attributing it to a larger supersaturation excursion is an interpretation.
- **Additional seed did not provide a clear benefit in the tested range.** Batch 10 used 0.100 g seed versus 0.050 g in batch 8 but gave similar recovery and fines. This supports “no demonstrated improvement,” not equivalence of the seed doses.

### Contradicted or revised
- **The original nominal-property preference for S2 was contradicted as an optimization choice.** S2 produced good purity and sometimes fewer fines, but its best tested feasible recovery, 0.444 in batch 4, was below the approximately 0.53–0.54 feasible recoveries of S1 batches 6 and 8.
- **A simple monotonic benefit from deeper cooling, more seed, or longer holding was contradicted.** Batch 2 combined deeper cooling and more seed with recovery 0.472 but unacceptable fines of 0.566. Batch 11 had a much longer cold residence yet gave recovery 0.478 and fines 0.660. These observations contradict monotonic improvement, although they do not identify which mechanism caused the deterioration.
- **A strong catalyst effect on crystallization recovery was not supported.** Batches 6 and 8, using C3 and C1 respectively in otherwise similar S1 processes, differed in recovery by only 0.003—smaller than the assay noise scale. Catalyst effects on reaction selectivity remain plausible, but the data do not establish a catalyst ranking for crystallization recovery.

### Still untested
- The proposed causes of excessive fines—secondary nucleation, attrition, polymorphic change, or dissolution/reprecipitation—were not observed directly.
- Impurity partition coefficients and the proposed rejection of impurities into mother liquor were not measured; high final crystal purity only supports that interpretation indirectly.
- The nucleation and growth equations were qualitative organizing models, not fitted kinetic laws.
- Seed size distribution, controlled agitation effects, annealing, and independent effects of reaction temperature versus cold residence remain untested.
- The apparent recovery–fines frontier between high-recovery S0 and feasible S1 is based on a limited design and is not proven to be globally optimal.

## 2. Most informative additional experiment

I would repeat the batch 8 recipe exactly—S1, C1, 360 K reaction, 0.050 g seed, staged cooling through 310 K to 250 K—but replace its 7200 s final hold with the three consecutive 14400 s holds used in batch 11. All other variables would remain fixed.

This would distinguish three competing explanations for batch 11:

1. **Long cold residence causes secondary nucleation or attrition.** Expected outcome: fines rise substantially toward the batch-11 value near 0.66, crystal size declines, and recovery fails to improve or decreases.
2. **Batch 11 was poor mainly because of its lower 340 K reaction history or resulting composition.** Expected outcome: with the 360 K batch-8 reaction retained, fines remain near 0.40 despite the long hold.
3. **Classical ripening dominates during prolonged residence.** Expected outcome: fines decrease and number-weighted size increases, possibly with similar or slightly reduced recovery because smaller crystals dissolve and feed larger ones.

This single experiment is preferable to another solvent screen because it removes the largest confound in the process-history claim and directly tests whether the adverse long-hold behavior is reproducible.

## 3. Least effectively used observation and least reliable prediction

The account used the **pre-crystallization HPLC observations from batches 1 and 2** least effectively. For example, batch 2 showed HPLC conversion 0.984, selectivity 0.532, and reaction yield 0.503 before crystallization, while the final assay reported somewhat different reaction metrics. Those measurements could have been used more explicitly to assess whether composition continued changing during cooling and holding. Instead, the account relied mainly on final-assay reaction metrics and treated reaction–crystallization coupling qualitatively. Interpretation is also limited because only two such intermediate HPLC measurements were available and sampling/instrument differences complicate direct comparisons.

The **Q08 annealing prediction** is the least reliable held-out prediction. It assumed that reheating a developed crystal slurry to 315 K would preferentially dissolve fines and that the subsequent recooling would favor regrowth, producing larger particles and fewer fines at a modest recovery cost. No campaign batch reheated an established crystal population, so the extent of dissolution, possible phase transformation, impurity redistribution, and renucleation during the 3600 s recool are unconstrained. The direction could reverse if reheating dissolved most crystals or if recooling caused a new nucleation burst. Accordingly, Q08 involved a more substantial process-history extrapolation than predictions based on solvent, seed dose, concentration, or simple holding, all of which had at least partial experimental analogues.
