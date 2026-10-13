# C-W05-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Process and recommended batch
The sealed recommendation is batch 8. It used 0.040 mol reagent, 0.005 mol catalyst C0, 0.080 L solvent S1, reaction control at 350 K for 1800 s, 0.050 g seed, and slow crystallization to 295 K over 14,400 s. Its final assay reported crystal recovery 0.495, purity 0.977, and fines number fraction 0.492.

### Reaction-stage material effects
Conversion was generally near unity, so catalyst and solvent primarily affected selectivity, byproduct formation, and degradation rather than whether reagent disappeared. A useful approximation is

Y_rxn ≈ X × S,

where X is conversion, S is target selectivity, and Y_rxn is target-product yield before separation.

C0 was the strongest catalyst observed in the relevant screen. With S2 at 350 K for 1800 s, batch 3 gave final reaction yield 0.575 and selectivity 0.577. Under comparable reaction conditions, C2/S2 in batch 4 gave yield 0.466 and selectivity 0.482. C1 and C3 were tested with S2 at the hotter, longer 373 K/3600 s condition: batch 1 gave yield 0.466, selectivity 0.468, and degradation warning 0.193; batch 2 gave yield 0.347, selectivity 0.359, and degradation warning 0.408. These observations support C0, but they do not constitute a clean four-catalyst comparison because C1/C3 experienced a different thermal history. An untested alternative is that C1 or C3 could perform better at the milder C0 conditions.

Solvent affected both reaction selectivity and crystallization behavior. With C0 at 350 K/1800 s, S1 produced high reaction yield/selectivity repeatedly: batch 5 reported 0.647/0.654, batch 8 reported 0.639/0.648, and batch 11 reported 0.635/0.655. S0 also gave substantial reaction yield in batch 7 (0.641), whereas S3 in batch 6 was lower (0.548). Thus reaction yield alone did not determine an acceptable solid product.

### Crystallization and reaction–separation coupling
Crystal recovery is conditional on the target product present before separation, not on the original reagent charge. Overall seed-excluded isolated target relative to reagent can therefore be approximated as

Y_overall ≈ Y_rxn × R_cryst.

For batch 8 this is approximately 0.639 × 0.495 ≈ 0.316. The same calculation is about 0.223 for batch 3. This shows why both reaction selectivity and crystallization recovery matter even though the formal campaign objective focused on crystallization-stage recovery.

Moderate reaction selectivity did not prevent high crystal purity. All important C0 batches produced crystals around 0.975–0.992 purity despite reaction selectivities near 0.58–0.65. This is consistent with preferential incorporation of target product and rejection of reaction byproducts during crystallization. It also means the purity constraint was comparatively inactive; fines were the limiting quality attribute.

The solvent ranking for particle quality differed from the reaction ranking. At a 290 K endpoint with C0 and 0.050 g seed:

- S1, batch 5: recovery 0.486, purity 0.975, fines 0.518.
- S0, batch 7: recovery 0.452, purity 0.976, fines 0.758.
- S3, batch 6: recovery 0.345, purity 0.989, fines 0.787.

S2 gave a more conservative particle distribution: batch 3, crystallized to 300 K, had recovery 0.388, purity 0.989, and fines 0.380. This agrees qualitatively with the nominal dossier, in which S2 had favorable growth, low nucleation tendency, low impurity occlusion, and low solubility. S1 offered greater observed recovery but operated near the fines boundary. S0 and S3 appear to promote excessive secondary nucleation or insufficient growth under the tested cooling program. Those mechanistic assignments are interpretations; microscopy or time-resolved supersaturation data were not available.

### Process-history dependence
Cooling endpoint and history controlled the recovery–fines balance. For the C0/S1 system with 0.050 g seed:

- Batch 5, 290 K: recovery 0.486 and fines 0.518.
- Batch 8, 295 K: recovery 0.495 and fines 0.492.
- Batch 11, 297.5 K: recovery 0.470 and fines 0.497.
- Batch 12, 295 K with an additional 14,400 s crystallization hold: recovery 0.481 and fines 0.507.

The broad interpretation is that greater supersaturation can improve recovery but risks generating more sub-20 µm particles. The individual results are not strictly monotonic: batch 8 had slightly greater recovery than the colder batch 5. Fixed-world variability, reaction-to-reaction differences, and measurement noise are sufficient alternative explanations, so these batches do not define a precise temperature-response equation.

Seed dose also showed a directional effect. Batch 8 used 0.050 g seed and gave recovery 0.495, fines 0.492, and normalized size 0.105. Batch 9 used 0.020 g under otherwise similar C0/S1/295 K conditions and gave recovery 0.486, fines 0.509, and size 0.055. This is consistent with insufficient seed surface allowing more spontaneous nucleation and less subsequent growth, but it is a single comparison near the measurement-noise scale.

The tested digestion strategy was unsuccessful. Batch 10 was cooled to 285 K, reheated to about 315 K, and recooled to 290 K. It retained recovery of 0.482 but produced fines of 0.666. Thus reheating did not selectively dissolve fines under that profile; it may instead have erased the controlled seed history and caused renewed nucleation during recooling. Other digestion temperatures, durations, or agitation rates remain untested.

Batch 2 cannot cleanly support a staged-cooling mechanism. Its nominal 330 K hold used an uncontrolled wait operation during which temperature drifted toward 299 K before the final cooling step. Its poor result—recovery 0.230 and fines 0.819—is consequently confounded by unintended thermal history and severe reaction degradation.

### Revisions and uncertainty
The initial expectation favored S2 because its nominal properties suggested strong growth, low nucleation, low solubility, and low impurity occlusion. Experiments confirmed that S2 gave robust particle quality, but the study was revised when S1 delivered substantially higher recovery and reaction yield. Subsequent work located a narrow S1 operating region around 295–297.5 K rather than establishing a broad, robust optimum.

The main unresolved issue is the recovery–fines boundary. Batch 8 passed by only 0.008 in fines fraction. The declared final-assay noise scale for fines was 0.018, larger than that margin; moreover, the in-process particle measurement in batch 8 was 0.504 while its final assay was 0.492. Differences among batches 5, 8, 9, 11, and 12 therefore should not be treated as definitive evidence for small condition effects. Replication would be required to estimate the probability of meeting the 0.50 specification.

Purity is much less uncertain as a constraint because observed values were roughly 0.975–0.992, far above the 0.80 minimum. The outstanding development problem is to preserve the approximately 0.49 crystallization recovery of the S1 process while creating a reproducible fines margin. Untested possibilities include narrower cooling ramps near the supersaturation onset, seed-size control rather than seed mass alone, controlled agitation profiles, and milder digestion followed by feedback-triggered cooling.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.44 |
| Q01 | crystal_purity | 0.96 | 0.91 | 0.99 |
| Q01 | crystal_size | 0.18 | 0.11 | 0.27 |
| Q01 | crystal_yield | 0.72 | 0.6 | 0.82 |
| Q02 | crystal_fines_fraction | 0.56 | 0.4 | 0.71 |
| Q02 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q02 | crystal_size | 0.1 | 0.05 | 0.18 |
| Q02 | crystal_yield | 0.59 | 0.44 | 0.72 |
| Q03 | crystal_fines_fraction | 0.7 | 0.54 | 0.83 |
| Q03 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.11 |
| Q03 | crystal_yield | 0.57 | 0.42 | 0.7 |
| Q04 | crystal_fines_fraction | 0.43 | 0.29 | 0.58 |
| Q04 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q04 | crystal_size | 0.14 | 0.08 | 0.23 |
| Q04 | crystal_yield | 0.61 | 0.47 | 0.73 |
| Q05 | crystal_fines_fraction | 0.4 | 0.27 | 0.55 |
| Q05 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q05 | crystal_size | 0.15 | 0.09 | 0.24 |
| Q05 | crystal_yield | 0.62 | 0.48 | 0.74 |
| Q06 | crystal_fines_fraction | 0.64 | 0.48 | 0.78 |
| Q06 | crystal_purity | 0.9 | 0.81 | 0.96 |
| Q06 | crystal_size | 0.075 | 0.035 | 0.14 |
| Q06 | crystal_yield | 0.65 | 0.51 | 0.77 |
| Q07 | crystal_fines_fraction | 0.38 | 0.25 | 0.53 |
| Q07 | crystal_purity | 0.94 | 0.86 | 0.98 |
| Q07 | crystal_size | 0.16 | 0.09 | 0.25 |
| Q07 | crystal_yield | 0.63 | 0.49 | 0.75 |
| Q08 | crystal_fines_fraction | 0.66 | 0.5 | 0.8 |
| Q08 | crystal_purity | 0.94 | 0.86 | 0.98 |
| Q08 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q08 | crystal_yield | 0.56 | 0.4 | 0.7 |
| Q09 | crystal_fines_fraction | 0.91 | 0.79 | 0.98 |
| Q09 | crystal_purity | 0.9 | 0.79 | 0.97 |
| Q09 | crystal_size | 0.018 | 0.005 | 0.05 |
| Q09 | crystal_yield | 0.08 | 0.02 | 0.18 |
| Q10 | crystal_fines_fraction | 0.74 | 0.57 | 0.87 |
| Q10 | crystal_purity | 0.92 | 0.83 | 0.97 |
| Q10 | crystal_size | 0.05 | 0.018 | 0.105 |
| Q10 | crystal_yield | 0.28 | 0.15 | 0.43 |
| Q11 | crystal_fines_fraction | 0.4 | 0.27 | 0.55 |
| Q11 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q11 | crystal_size | 0.15 | 0.085 | 0.24 |
| Q11 | crystal_yield | 0.62 | 0.48 | 0.74 |
| Q12 | crystal_fines_fraction | 0.58 | 0.42 | 0.73 |
| Q12 | crystal_purity | 0.88 | 0.78 | 0.95 |
| Q12 | crystal_size | 0.105 | 0.05 | 0.18 |
| Q12 | crystal_yield | 0.75 | 0.63 | 0.84 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and reach supersaturation, so particles are expected in every batch. Q01–Q02: the prior campaign and material dossier indicate that S1 has lower solubility, lower nucleation tendency, faster growth and less impurity occlusion than S3; I therefore predict higher recovery, larger particles and fewer fines for Q01. Q03–Q04: increasing seed from 0.001 to 0.045 g should provide enough growth surface to suppress uncontrolled secondary nucleation, with only a modest effect on equilibrium recovery. Q05–Q06: a gradual temperature ramp should limit the supersaturation peak and fines, whereas the 120 s plunge should establish many small particles that prolonged aging may not remove. Q07–Q08: the 315 K reheat and rapid recooling are predicted to partly dissolve product and then renucleate it; this follows the campaign’s unsuccessful digestion experiment, although another annealing window remains plausible. Q09–Q10: 60 s permits little seed-excluded deposition; a two-hour hold raises recovery and size but is still expected to leave a fine-rich population. Q11–Q12: doubling reagent concentration should increase fractional recovery at 278.15 K, but the same seed charge must accommodate more product and a larger supersaturation, increasing fines and occlusion risk. Intervals are deliberately broad because these recipes extrapolate to much longer cooling histories, lower charge, catalyst C1, and solvent S0; several fines predictions straddle the 0.50 specification, and purity is less uncertain than particle quality.

## K2

## 1. Status of the main claims

### Supported within the tested campaign scope

- **C0/S1 was a consistently productive reaction system.** Direct observations from batches 5, 8, 9, 11 and 12 gave near-unity conversion, reaction yields of about 0.63–0.65, and final crystal purities of 0.975–0.992. The interpretation that C0/S1 is productive is supported; the deeper claim that it is globally optimal is untested.
- **Purity was not the active constraint; particle quality was.** The principal C0/S1 batches were comfortably above the 0.80 purity threshold, while fines clustered around the 0.50 limit: 0.518 in batch 5, 0.492 in batch 8, 0.509 in batch 9, 0.497 in batch 11, and 0.507 in batch 12. This is a direct observation.
- **S2 provided a more conservative particle-quality region.** Batch 3 gave purity 0.989 and fines 0.380 at recovery 0.388; batch 4 gave purity 1.000 and fines 0.339 at recovery 0.339. Interpreting this as an S2 growth/nucleation advantage is reasonable but not isolated from catalyst and endpoint effects.
- **The tested digestion history was unfavorable.** Batch 10, cooled to 285 K, reheated near 315 K and recooled to 290 K, gave fines 0.666. This directly contradicts the expectation that that particular digestion profile would remove fines.
- **Reduced seed was not beneficial in the tested comparison.** Batch 9 used 0.020 g seed and gave recovery 0.486, size 0.055 and fines 0.509, versus batch 8 with 0.050 g seed, recovery 0.495, size 0.105 and fines 0.492. The numerical direction supports greater seeded growth, but a single close comparison does not establish causality.

### Contradicted or revised

- **The initial expectation that S2 would be the best overall solvent was revised.** S2 did give robust fines control, but S1 produced higher recovery: batch 8 reached 0.495 versus 0.388 for batch 3. Thus S2 was not the observed recovery leader.
- **A simple monotonic rule that colder endpoints always increase recovery was contradicted numerically.** Batch 5 at 290 K recovered 0.486, whereas batch 8 at 295 K recovered 0.495. Because the difference is small and the batches were independent, this contradicts a deterministic monotonic account but not an underlying average temperature effect.
- **Extra aging at 295 K did not demonstrably improve quality.** Batch 12’s additional crystallization hold ended with recovery 0.481 and fines 0.507, compared with 0.495 and 0.492 in batch 8. The proposed ripening benefit was therefore unsupported under that history.

### Still untested or unresolved

- Catalyst ranking was not cleanly isolated: C0 and C2 were tested at 350 K/1800 s, whereas C1 and C3 were tested at 373 K/3600 s. The claim that C0 is intrinsically superior to every catalyst remains untested.
- Preferential impurity rejection, secondary nucleation and Ostwald ripening are mechanistic interpretations. No supersaturation trace, seed-size distribution, full particle-size distribution or solid-composition trajectory directly demonstrated them.
- The S1 endpoint response remains unresolved because its observed fines differences are comparable to measurement uncertainty and no condition was replicated sufficiently.
- Effects of seed size, agitation during cooling, feedback-controlled nucleation onset and alternative mild digestion profiles remain untested.

## 2. One additional experiment

I would perform one matched split-batch experiment. A single C0/S1 reaction would be prepared under the batch-8 reaction conditions, homogenized after reaction, and divided equally into two vessels. Both arms would receive the same seed lot and seed concentration and the same cooling duration; one would end at 295 K and the other at 290 K. Particle-size measurements would be taken immediately before filtration, followed by matched final assays.

This would distinguish two competing explanations:

1. **A real supersaturation tradeoff:** the 290 K arm should show higher recovery but more fines and possibly slightly lower purity, while the 295 K arm should show fewer fines with modestly lower recovery.
2. **Batch variation or measurement noise dominating the apparent trend:** the two arms would show little consistent difference, or the 295 K arm could again equal or exceed the 290 K arm in recovery.

Sharing the reaction solution would remove reaction conversion, selectivity and impurity composition as between-arm confounders. It would not by itself establish reproducibility across independent batches, but it would be more diagnostic of crystallization endpoint than another unsplit campaign batch.

## 3. Least-effective use and least-reliable prediction

The account used **batch 4** least effectively. C2/S2 at 290 K produced very low fines (0.339) and purity 1.000 despite poorer reaction yield than C0/S2. I mainly treated catalyst as a reaction-stage variable and solvent/temperature as crystallization variables. Batch 4 suggests that catalyst-dependent byproduct composition could materially alter nucleation or growth, or alternatively that its excellent particle result was variability. That reaction–crystallization coupling deserved more explicit treatment.

**Q09 is the least reliable held-out prediction.** Its crystallization consists of a 60-second drop to 292 K followed immediately by filtration. The campaign supplied no comparable seconds-scale crystallization data, and added seed makes `particles_present` straightforward while making seed-excluded recovery and number-weighted fines difficult to infer. My predicted recovery of 0.08 and fines of 0.91 therefore rest largely on qualitative kinetic extrapolation rather than calibrated evidence. Q10 is somewhat less uncertain because its additional two-hour hold is closer to the campaign’s time scale.
