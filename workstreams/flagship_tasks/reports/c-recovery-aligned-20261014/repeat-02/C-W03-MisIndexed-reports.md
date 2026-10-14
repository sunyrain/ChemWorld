# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Overall picture
The process appears to be governed by two coupled efficiencies:

\[
Y_{crystal}=Y_{reaction}\,f_{capture}
\]

where \(Y_{crystal}\) is seed-excluded target in the isolated solid divided by initial reagent, \(Y_{reaction}\) is upstream target yield, and \(f_{capture}\) is the fraction of that target recovered during crystallization and isolation. A useful qualitative decomposition is

\[
Y_{reaction}\approx X\,S
\]

with conversion \(X\) and effective selectivity \(S\). These equations are bookkeeping relationships rather than a fitted kinetic law.

The experiments indicate that solvent identity controls both reaction performance and the balance between crystal growth and new-particle nucleation; catalyst and hot residence determine the amount and composition of material entering crystallization; and the complete temperature history determines capture and particle-number distribution.

### Material effects

**Solvent.** At the common C1, 360 K/1800 s condition, S2 gave the best joint outcome: batch 3 produced crystal yield 0.557, purity 0.990, and fines fraction 0.423. S1 gave similar but lower recovery and failed the fines limit (batch 2: 0.531 yield, 0.986 purity, 0.557 fines). S3 was worse in both recovery and fines (batch 4: 0.447 and 0.854), while S0 also generated many fines (batch 1: 0.478 and 0.867).

This supports the interpretation suggested by the nominal material dossier: S2 combines relatively low solubility and nucleation tendency with high crystal-growth tendency and low impurity occlusion. Such a solvent should direct supersaturation toward growth on existing crystals rather than creation of many small particles, while also increasing cold-stage capture. S2 may additionally improve the reaction itself: its upstream yield in batch 3 was 0.683, higher than the corresponding S0 and S3 results. These two solvent roles were not independently isolated.

The S0 comparison is especially uncertain because batch 1 was inadvertently allowed to warm from 275 K to about 295 K before filtration. Its recovery therefore should not be treated as a clean solvent-only contrast. Batches 2–4 provide the more consistent solvent screen, but all solvent conditions were single runs.

**Catalyst.** With S2 and otherwise common processing, C3 gave the highest observed catalyst-screen recovery (batch 7: 0.577), followed closely by C0 (batch 5: 0.568) and C1 (batch 3: 0.557); C2 was appreciably lower (batch 6: 0.481). C3 nevertheless showed substantial byproduct and degradation signals in the long reaction: byproduct 0.249 and degradation warning 0.129. C0 achieved slightly higher apparent selectivity than C3 under the same history, so the C3–C0 ranking is not mechanistically definitive. The nominal catalyst activities alone did not predict the realized ordering, consistent with fixed hidden catalyst–reaction residuals.

### Reaction mechanism and residence-time interpretation
At 360 K for 1800 s, conversion was essentially complete in the C3 experiment, but selectivity was only 0.649 and upstream yield 0.675 (batch 7). Shortening the hot residence to 900 s retained high conversion (0.990) while increasing selectivity to 0.730 and upstream yield to 0.736; byproduct and degradation signals fell to 0.177 and 0.058 (batch 9). This is consistent with a consecutive or parallel loss network such as

\[
R \xrightarrow{k_1} P,\qquad R \xrightarrow{k_2} I,\qquad P \xrightarrow{k_3} D,
\]

where desired product \(P\) accumulates early but longer exposure promotes impurity formation or product degradation. This equation is an interpretation, not an identified reaction law.

At 600 s, conversion fell to 0.948, while selectivity rose to 0.768 and degradation remained low; upstream yield was effectively unchanged from the 900 s optimized case at about 0.731 (batch 12). Thus, the local optimum is broad: reducing residence below 900 s trades conversion against selectivity rather than clearly improving the amount of target. The nearly identical downstream recovery of batches 11 and 12 supports this interpretation.

Lowering the reaction temperature to 340 K for 1800 s did not help. Batch 8 still showed complete measured conversion but lower upstream yield (0.635), crystal yield 0.547, and fines 0.651. One interpretation is that the lower hot starting temperature altered the subsequent supersaturation trajectory or provided less dissolution/conditioning of nuclei. An alternative is that temperature changed reaction selectivity or impurity identity in a way not captured by the scalar byproduct signal. These possibilities were not separately tested.

### Crystallization coupling and process-history dependence
The estimated capture fraction, \(Y_{crystal}/Y_{reaction}\), increased from roughly 0.81–0.85 in the initial 275 K experiments to approximately 0.86 in batch 9, 0.89 at 260 K in batch 10, and 0.91 at 250 K in batches 11–12. This trend supports ordinary solubility-driven recovery: colder terminal temperatures leave less target in the mother liquor.

Cooling more deeply did not cause a catastrophic fines penalty in S2. Batch 9 at 275 K gave crystal yield 0.634 and fines 0.389; batch 10 at 260 K gave 0.660 and 0.461; batch 11 at 250 K gave 0.662 and 0.441. The data therefore show a modest recovery gain on going from 275 to 260 K, followed by an apparent plateau near 250 K. They also show a possible quality/recovery tradeoff—deeper cooling can raise supersaturation and fines—but the fines response was noisy and not monotonic between 260 and 250 K.

The full trajectory matters, not merely the final temperature. The successful batches used a hot reaction, 0.05 g seeding, a 7200 s controlled cool to the target, and a second 7200 s controlled cold stage. The seed provides surfaces for growth, while slow cooling and the cold hold allow desupersaturation without relying entirely on spontaneous nucleation. In contrast, an uncontrolled wait in batch 1 warmed the slurry before isolation. Batch 8 further suggests that the starting temperature and reaction history influence the eventual particle population even when the same nominal cold program is applied.

Particle size and fines were clearly not functions of recovery alone. For example, batches 3, 5, 6, and 7 all used S2 and had fines between about 0.39 and 0.45 despite crystal yields spanning 0.481–0.577. Conversely, S1 achieved respectable recovery in batch 2 but failed the fines constraint. Solvent-dependent nucleation and growth therefore dominate the particle-number distribution, with supersaturation magnitude and impurity profile acting as secondary coupled variables.

### Purity
All successful S2 conditions produced very high measured crystal purity, generally 0.978–1.000. This is consistent with S2's low nominal impurity-occlusion tendency and with selective lattice incorporation during growth. However, the purity result does not prove chemical purification from every impurity: the assay reports a bounded aggregate metric, and no mother-liquor mass balance or impurity-specific solid analysis was performed. Because observed purity remained far above the 0.80 requirement, the active optimization tension was recovery versus fines rather than recovery versus purity.

### Revisions to the working account
The initial expectation that S2 would favor larger, cleaner crystals with fewer fines was supported. The expectation that C1 would be the best catalyst was revised after the catalyst screen: C3 gave the highest observed recovery, although C0 remained a close alternative. The early assumption that simply providing a long reaction residence would be beneficial was also revised; 900 s substantially outperformed 1800 s for C3 because reduced degradation outweighed the small conversion loss. Finally, deeper cooling was expected to improve recovery but potentially violate the fines limit. Recovery did improve, yet S2 retained acceptable fines down to 250 K, so the anticipated penalty was milder than expected.

### Uncertainty and unresolved alternatives
The declared final-assay noise scales are about 0.01 for crystal yield and 0.018 for fines, and no optimized condition was replicated. Consequently, the 0.001 difference between batch 11 (yield 0.662, fines 0.441) and batch 12 (yield 0.661, fines 0.461) is not evidence of a real recovery difference. Batch 11 is better supported operationally because a separate pre-filtration particle measurement also indicated acceptable fines (0.452), whereas batch 12 had no additional particle measurement.

Similarly, the small recovery differences among C3, C0, and C1 could reflect assay or process variation. Untested alternatives include intermediate residence times between 600 and 900 s, temperatures between 250 and 260 K, altered seed loading, slower multistage cooling, different agitation during crystallization, and direct replication. Lower seed loading might reduce seed-derived particle counts or encourage larger crystals, but it could instead permit uncontrolled primary nucleation; this was not tested. A warmer growth hold followed by a final cold polish might improve size while retaining recovery, but it was also not tested.

The principal unresolved tradeoff is therefore not purity, which had ample margin, but whether additional cold capture can be obtained without moving the true fines fraction above 0.50. Batches 10–12 suggest that the current process lies near a recovery plateau with only about 0.04–0.11 absolute margin on fines. Replication would be required to quantify that operating margin and distinguish the nearly tied 600 and 900 s reaction histories.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.38 | 0.24 | 0.54 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.12 | 0.075 | 0.19 |
| Q01 | crystal_yield | 0.42 | 0.3 | 0.54 |
| Q02 | crystal_fines_fraction | 0.59 | 0.41 | 0.76 |
| Q02 | crystal_purity | 0.98 | 0.93 | 1 |
| Q02 | crystal_size | 0.065 | 0.035 | 0.12 |
| Q02 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q03 | crystal_fines_fraction | 0.67 | 0.48 | 0.83 |
| Q03 | crystal_purity | 0.97 | 0.91 | 1 |
| Q03 | crystal_size | 0.05 | 0.025 | 0.1 |
| Q03 | crystal_yield | 0.3 | 0.19 | 0.42 |
| Q04 | crystal_fines_fraction | 0.43 | 0.27 | 0.6 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.105 | 0.06 | 0.17 |
| Q04 | crystal_yield | 0.32 | 0.21 | 0.44 |
| Q05 | crystal_fines_fraction | 0.41 | 0.25 | 0.57 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.115 | 0.065 | 0.18 |
| Q05 | crystal_yield | 0.33 | 0.22 | 0.45 |
| Q06 | crystal_fines_fraction | 0.66 | 0.47 | 0.82 |
| Q06 | crystal_purity | 0.96 | 0.89 | 1 |
| Q06 | crystal_size | 0.052 | 0.025 | 0.105 |
| Q06 | crystal_yield | 0.34 | 0.22 | 0.46 |
| Q07 | crystal_fines_fraction | 0.38 | 0.23 | 0.54 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.125 | 0.07 | 0.195 |
| Q07 | crystal_yield | 0.34 | 0.23 | 0.46 |
| Q08 | crystal_fines_fraction | 0.24 | 0.12 | 0.4 |
| Q08 | crystal_purity | 0.99 | 0.95 | 1 |
| Q08 | crystal_size | 0.18 | 0.105 | 0.27 |
| Q08 | crystal_yield | 0.31 | 0.19 | 0.43 |
| Q09 | crystal_fines_fraction | 0.78 | 0.59 | 0.91 |
| Q09 | crystal_purity | 0.96 | 0.86 | 1 |
| Q09 | crystal_size | 0.032 | 0.012 | 0.07 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.1 |
| Q10 | crystal_fines_fraction | 0.59 | 0.4 | 0.76 |
| Q10 | crystal_purity | 0.97 | 0.9 | 1 |
| Q10 | crystal_size | 0.068 | 0.035 | 0.125 |
| Q10 | crystal_yield | 0.16 | 0.08 | 0.27 |
| Q11 | crystal_fines_fraction | 0.4 | 0.24 | 0.57 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.12 | 0.068 | 0.19 |
| Q11 | crystal_yield | 0.33 | 0.22 | 0.45 |
| Q12 | crystal_fines_fraction | 0.58 | 0.39 | 0.75 |
| Q12 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q12 | crystal_size | 0.067 | 0.034 | 0.12 |
| Q12 | crystal_yield | 0.44 | 0.3 | 0.57 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are extrapolations from the sealed campaign, with broad 80% intervals because the queried recipes use lower concentration, a hotter quenched reaction, and much longer cooling histories than the experiments. Q01–Q02: S1 is expected to give higher upstream target formation and fewer fines than the poorly performing S3 observed in the solvent screen, although S3 may retain a small purity advantage. Q03–Q04: 0.001 g seed is unlikely to provide enough growth area in strongly nucleating S0, so uncontrolled nucleation raises fines; 0.045 g seed should improve size distribution with little equilibrium-yield change. Q05–Q06: gradual cooling limits peak supersaturation, whereas the rapid drop promotes many small particles; their very long common aging makes yields similar. Q07–Q08: the 315 K thermal cycle should dissolve preferentially small crystals and improve size/fines through dissolution–regrowth, at the cost of some unrecovered product and hence lower yield. Q09–Q10: particles are expected because both are seeded, but 60 seconds at 292 K gives little seed-excluded recovery; the added hold permits growth and recovery, though probably not enough to overcome S0's fines tendency. Q11–Q12: doubling reagent increases absolute supersaturation and normalized capture, but the fixed catalyst charge halves the catalyst-to-reagent ratio and the higher supersaturation increases impurity occlusion and fines. Feasibility labels use the point estimates; several fines intervals cross 0.50, so those classifications are uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S2 was the strongest tested solvent for the joint objective.** Under the common C1/360 K/1800 s recipe, batch 3 gave yield 0.557, purity 0.990 and fines 0.423. Batch 2 with S1 had similar recovery but failed fines at 0.557; batch 4 with S3 had lower recovery and fines 0.854. This directly supports the empirical S2 choice. Attribution to lower nucleation, faster growth and lower occlusion is an interpretation, not a measured mechanism. Batch 1 is a weak S0 comparator because it warmed before filtration.
- **C2 was inferior at the screened recipe.** Batch 6 yielded 0.481 versus 0.557–0.577 for batches 3, 5 and 7. C3 had the best point estimate in batch 7, but its advantage over C0 in batch 5 was only 0.009—comparable to assay noise—so a definitive C3>C0 ranking is not established.
- **Long residence was detrimental for C3.** Batch 7 at 1800 s had upstream yield 0.675, degradation warning 0.129 and crystal yield 0.577. Batch 9 at 900 s had upstream yield 0.736, degradation 0.058 and crystal yield 0.634. Batch 12 at 600 s retained upstream yield near 0.731 despite lower conversion. These observations support a local conversion–selectivity tradeoff.
- **Colder crystallization increased capture to a plateau while retaining feasibility.** Batches 9–11 moved from 275 to 260 to 250 K and produced crystal yields 0.634, 0.660 and 0.662, all with high purity and fines below 0.50. The corresponding inferred capture fractions increased from about 0.86 to 0.89–0.91.

### Contradicted or revised
- The initial expectation that **C1 would be best** was revised: C3 and C0 had higher point-estimate recoveries in batches 7 and 5.
- The expectation that **longer reaction time would improve recovery** was contradicted by batches 7, 9 and 12. The data instead favor an intermediate or broad 600–900 s region.
- The anticipated strong **fines penalty from deeper cooling** was not observed within S2: batches 10 and 11 remained feasible. A smaller tradeoff may exist, but fines were noisy and non-monotonic.

### Still untested
- The proposed consecutive network—reactant to product followed by product degradation—was not directly identified. The scalar byproduct and degradation signals are consistent with it, but parallel impurity formation or batch variation could give similar results.
- The causal roles of solvent solubility, nucleation, growth and impurity occlusion were not isolated from solvent effects on the reaction.
- Seed loading was never varied, so claims about seed area suppressing primary nucleation remain untested.
- No optimized condition was replicated. The apparent 0.001 yield advantage of batch 11 over batch 12 is not meaningful.
- Reheating, dissolution–regrowth, rapid versus gradual cooling, high upstream loading and the very long cooling histories in the held-out recipes were outside the experimental campaign.

## 2. One additional experiment

I would run a **matched split-residence experiment** using S2/C3 at 360 K. A single well-mixed parent charge would react for 900 s and then be divided equally. One arm would be quenched immediately; the second would remain at 360 K for another 900 s. Both arms would then receive matched seed loading and identical 250 K cooling, hold and filtration histories. HPLC immediately after the split treatments, particle-size measurements after crystallization, and final assays would be collected for both arms.

This would distinguish:
- **Consecutive product degradation:** the 1800 s arm should show similar conversion but lower target yield/selectivity, higher byproduct/degradation signals and lower final crystal recovery.
- **A crystallization-history explanation:** reaction assays would be similar, but final recovery or CSD would differ because the longer hot treatment changes nuclei, impurities or solution conditioning.
- **Ordinary between-batch variation:** the large batch-7 versus batch-9 difference should shrink when both arms share the same parent mixture and handling history.
- **A pure parallel-reaction model without product loss:** target yield should approach a plateau rather than decline between 900 and 1800 s, although impurity may continue accumulating.

If both upstream assays and final outcomes agree within uncertainty, the earlier residence-time conclusion would be weakened. If upstream target decreases while the crystallization capture ratio remains similar, consecutive degradation would be strongly favored.

## 3. Weakest use of evidence and least reliable prediction

The account used the **crystal-size observations least effectively**. It emphasized recovery and fines but did not build a defensible relationship between reported normalized size, fines and CSD quality. Some final assays were internally awkward—for example, batch 3 had fines below 0.50 but normalized size about 0.071, nominally corresponding to a d50 below 20 µm. Independent particle and final-assay values also shifted between sampling times. These discrepancies could reflect measurement noise, distribution shape, filtration history or differing estimators, and they warranted more caution than the mechanistic narrative gave them.

The **Q08 held-out prediction is least reliable**. Its predicted benefit from reheating the crystal slurry to 315 K relied on an untested dissolution–regrowth/Ostwald-ripening argument. No campaign batch reheated an established crystal population, so the degree of dissolution, product loss, impurity rejection, secondary nucleation on recooling and net effect on fines are unknown. Q08 is also path-dependent: the same final 278 K temperature does not determine whether reheating improves size or destroys recoverable solids. Its point estimates—especially the large fines reduction—should therefore be treated as substantially more speculative than predictions based on monotonic cooling.
