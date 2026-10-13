# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### System and metric interpretation
The catalyst and solvent labels are anonymous benchmark materials, so the mechanism below is phenomenological rather than a claim about real chemical identities. The process consists of catalytic conversion of a limiting reagent, followed by solution crystallization, filtration, and assay.

Useful reaction quantities are

- conversion: `X = (nR,0 − nR)/nR,0`,
- selectivity to target: `S = nP/(nR,0 − nR)`,
- target formed: approximately `nP = nR,0 X S`.

The reported crystal yield has a different denominator:

`Ycryst = recovered target in crystals, excluding seed / target present before separation`.

Consequently, reaction yield controls how much target is available and the impurity environment, but `Ycryst` primarily measures crystallization-stage recovery rather than overall synthesis yield.

### Reaction–crystallization coupling
Conversion was near unity in most batches, while selectivity and byproduct/degradation signals varied substantially. Crystallization nevertheless produced very pure crystals—typically about 0.98–1.00 purity—despite reaction selectivities of only roughly 0.50–0.67. I interpret this as selective lattice incorporation plus rejection of reactant/byproduct into the mother liquor. Filtration then separates the purified solid.

This separation is not independent of reaction chemistry. Byproducts can change target solubility, heterogeneous nucleation, growth kinetics, and liquid occlusion. Thus catalysts can affect crystallization recovery even though the recovery denominator is target present immediately before separation. For example, under the common S2/0.08 L/250 K program:

- Batch 6, C0: reaction yield 0.599, selectivity 0.598, crystal yield 0.552, purity 1.000, fines 0.301.
- Batch 2, C1: reaction yield 0.582, selectivity 0.593, crystal yield 0.512, purity 0.987, fines 0.266.
- Batch 7, C2: reaction yield 0.526, selectivity 0.499, crystal yield 0.481, purity 0.980, fines 0.292.
- Batch 8, C3: reaction yield 0.569, selectivity 0.577, crystal yield 0.532, purity 0.980, fines 0.265.

These observations made C0 the provisional catalyst choice. They are single-run comparisons, however, so they do not establish a universal catalyst ranking; fixed catalyst residuals, process variability, and assay noise remain alternatives.

### Solvent effects
The initial material dossier suggested S2 would be favorable because it combined low relative solubility (0.7), low nucleation tendency (0.65), high growth tendency (1.3), and low impurity occlusion (0.65). The experiments broadly supported that expectation.

With C1 and the long cooling program:

- Batch 2, S2: crystal yield 0.512, purity 0.987, fines 0.266.
- Batch 3, S3: yield 0.425, purity 0.987, fines 0.576.
- Batch 4, S1: yield 0.472, purity 1.000, fines 0.535.
- Batch 5, S0: yield 0.573, purity 0.980, fines 0.695.

S0 illustrates the central recovery/quality tradeoff: it gave high recovery and relatively favorable reaction selectivity, but excessive nucleation produced too many sub-20 µm particles. S2 sacrificed some unconstrained recovery relative to S0 but was much more robust against fines. Because S0, S1, and S3 were each tested only once under that recipe, solvent effects remain partially confounded with run-to-run variation.

### Supersaturation and the nonlinear fines threshold
A useful qualitative description is

`σ = (C − C*)/C*`,

with nucleation and growth represented schematically by

`J ≈ kJ σ^m` and `G ≈ kG σ^g`,

where nucleation commonly has the stronger supersaturation dependence. Lower solvent volume raises target concentration and can improve recovery, approximately through a balance such as

`Ycryst ≈ 1 − Ceq(Tfilter)V/nP,0`,

but only while nucleation remains controlled.

At fixed 0.04 mol reagent, nominal reagent concentrations were 0.50 M at 0.08 L, 1.00 M at 0.04 L, 1.33 M at 0.03 L, and 2.00 M at 0.02 L. The C0/S2 results show a sharp rather than gradual quality transition:

- Batch 6, 0.08 L and 0.02 g seed: yield 0.552, fines 0.301.
- Batch 9, 0.04 L and 0.02 g seed: yield 0.566, fines 0.249.
- Batch 11, 0.03 L and 0.05 g seed: yield 0.561, fines 0.281.
- Batch 10, 0.02 L and 0.02 g seed: yield 0.575, fines 1.000.
- Batch 12, 0.02 L and 0.05 g seed: yield 0.569, fines 1.000.

Thus moderate concentration improved or preserved recovery without harming the particle distribution, but the 2 M regime crossed a strong nucleation threshold. Raising seed from 0.02 to 0.05 g did not rescue that regime. This disconfirmed the late hypothesis that extra seed surface alone could suppress uncontrolled primary or secondary nucleation at 0.02 L. Untested alternatives include staged solvent removal, seeding at a lower supersaturation, an intermediate-temperature growth hold under active temperature control, or an even slower/multistage cooling profile.

### Process-history dependence
The final temperature is insufficient to describe the outcome; the complete thermal history matters. Batch 1 was brought to about 363.9 K, cooled to 278 K over 7,200 s, and then held without active low-temperature control. During that hold it warmed to about 297.5 K before filtration. It gave crystal yield 0.436 and fines 0.428.

Batch 2 used cooling from approximately 365 to 250 K over 14,400 s—an average cooling rate near 0.0080 K/s—and was filtered immediately. It gave yield 0.512 and fines 0.266. The numerical recovery gain was 0.076.

This supports the importance of deeper, slower cooling and avoiding a warm post-crystallization excursion. Mechanistically, the warm hold could redissolve product, alter the size distribution through dissolution/reprecipitation, or change retained mother liquor. However, endpoint temperature, cooling duration, and immediate filtration all changed together, so the experiments do not isolate which factor dominated. Batch 1 also used a different control implementation, adding another confound.

Seeding provides growth surface and can reduce the supersaturation available for spontaneous nucleation, but seed mass alone was not decisive. The seed-excluded definition also prevents added seed mass from artificially inflating recovery. Particle quality depends on when seed is introduced, seed size distribution, supersaturation at seeding, cooling rate, and subsequent attrition or secondary nucleation; most of those variables were not independently varied.

### Revisions during the campaign
1. The initial expectation that S2 would be the most balanced crystallization solvent was retained and strengthened by the solvent comparison.
2. C1 was initially favored from nominal activity data, but the operating hypothesis shifted to C0 after batch 6 produced the strongest valid result in the catalyst comparison.
3. The initial general belief that slow, deep cooling would improve growth and reduce fines was supported directionally, but the batch-1/batch-2 comparison revealed that warming before filtration was an important confound.
4. The hypothesis that progressively increasing concentration would monotonically improve useful recovery was narrowed: improvement held from 0.08 to 0.04 L, but 0.02 L caused catastrophic fines.
5. The proposed rescue of the 0.02 L regime with more seed was rejected by batch 12.

### Uncertainty and unresolved tradeoff
Final-assay standard deviations were approximately 0.01 for crystal yield, 0.01 for purity, and 0.018 for fines. Batch 9 exceeded batch 11 in observed recovery by only 0.0045, smaller than the approximately 0.014 combined single-measurement yield uncertainty. Therefore, their ordering is an observed ranking, not convincing evidence that 0.04 L is intrinsically superior to 0.03 L. No recipe was replicated, so process variance cannot be separated from instrument noise.

The major unresolved tradeoff is clear: stronger supersaturation increases recovery only until excessive nucleation sharply increases the number fraction of fines. Because the fines metric is number-weighted, a large population of small particles can fail the constraint even if those particles contain a modest fraction of total crystal mass. Batch 10 demonstrated this directly: its recovery was numerically higher than batch 9, but fines were 1.000 and therefore unacceptable.

The sealed recommendation remains batch 9: S2 0.04 L, reagent 0.04 mol, C0 0.005 mol, reaction at 365 K for 3,600 s, 0.02 g seed, cooling to 250 K over 14,400 s, immediate filtration. Its observed crystal yield was 0.566, purity 0.987, and fines fraction 0.249. It was selected because it had the highest observed recovery among batches satisfying both quality constraints, while acknowledging that batches 6 and 11 are close alternatives requiring replication to resolve.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.24 | 0.12 | 0.38 |
| Q01 | crystal_purity | 0.95 | 0.9 | 0.99 |
| Q01 | crystal_size | 0.28 | 0.18 | 0.39 |
| Q01 | crystal_yield | 0.3 | 0.19 | 0.41 |
| Q02 | crystal_fines_fraction | 0.15 | 0.06 | 0.27 |
| Q02 | crystal_purity | 0.97 | 0.93 | 1 |
| Q02 | crystal_size | 0.34 | 0.23 | 0.46 |
| Q02 | crystal_yield | 0.4 | 0.28 | 0.52 |
| Q03 | crystal_fines_fraction | 0.56 | 0.39 | 0.73 |
| Q03 | crystal_purity | 0.93 | 0.86 | 0.98 |
| Q03 | crystal_size | 0.16 | 0.08 | 0.27 |
| Q03 | crystal_yield | 0.24 | 0.13 | 0.35 |
| Q04 | crystal_fines_fraction | 0.29 | 0.16 | 0.44 |
| Q04 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q04 | crystal_size | 0.28 | 0.17 | 0.4 |
| Q04 | crystal_yield | 0.28 | 0.17 | 0.39 |
| Q05 | crystal_fines_fraction | 0.22 | 0.1 | 0.36 |
| Q05 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q05 | crystal_size | 0.32 | 0.21 | 0.44 |
| Q05 | crystal_yield | 0.29 | 0.19 | 0.39 |
| Q06 | crystal_fines_fraction | 0.39 | 0.24 | 0.56 |
| Q06 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q06 | crystal_size | 0.23 | 0.13 | 0.35 |
| Q06 | crystal_yield | 0.34 | 0.23 | 0.45 |
| Q07 | crystal_fines_fraction | 0.19 | 0.08 | 0.32 |
| Q07 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q07 | crystal_size | 0.35 | 0.23 | 0.48 |
| Q07 | crystal_yield | 0.3 | 0.2 | 0.4 |
| Q08 | crystal_fines_fraction | 0.13 | 0.04 | 0.25 |
| Q08 | crystal_purity | 0.97 | 0.92 | 1 |
| Q08 | crystal_size | 0.41 | 0.28 | 0.55 |
| Q08 | crystal_yield | 0.27 | 0.16 | 0.38 |
| Q09 | crystal_fines_fraction | 0.86 | 0.72 | 0.97 |
| Q09 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q09 | crystal_size | 0.05 | 0.02 | 0.1 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.09 |
| Q10 | crystal_fines_fraction | 0.65 | 0.47 | 0.82 |
| Q10 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q10 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q10 | crystal_yield | 0.12 | 0.05 | 0.21 |
| Q11 | crystal_fines_fraction | 0.24 | 0.11 | 0.39 |
| Q11 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q11 | crystal_size | 0.32 | 0.21 | 0.45 |
| Q11 | crystal_yield | 0.3 | 0.19 | 0.41 |
| Q12 | crystal_fines_fraction | 0.41 | 0.25 | 0.59 |
| Q12 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q12 | crystal_size | 0.25 | 0.14 | 0.38 |
| Q12 | crystal_yield | 0.49 | 0.37 | 0.61 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are noise-free pre-sampling predictions, with 80% intervals reflecting extrapolation and process-model uncertainty rather than final-assay noise. Q01–Q02: S3 is predicted to give greater recovery, growth, and purity with fewer fines than S1 because of its lower nominal solubility/nucleation and occlusion tendencies. Q03–Q04: increasing seed from 0.001 to 0.045 g should provide enough growth surface to suppress uncontrolled S0 nucleation; Q03 is therefore predicted to fail the fines constraint while Q04 passes. Q05–Q06: the very slow ramp should favor larger, less fine crystals, whereas rapid chilling should raise recovery but retain more nuclei even after the long cold hold; Q06 is feasible by its point estimate but its fines interval crosses 0.50. Q07–Q08: the 315 K anneal/recrystallization cycle is expected to dissolve smaller particles and improve size, fines, and purity, at a modest recovery cost. Q09–Q10: the 292 K endpoint provides weak driving force; a two-hour hold increases deposition and growth but is still predicted to leave excessive fines. Q11–Q12: doubling reagent loading should markedly raise recovery, but also increase supersaturation, impurity occlusion, and fines; the very slow ramp and heavy seeding keep Q12 marginally feasible by the point estimate, although its fines interval crosses the specification. All batches contain added seed and are therefore expected to contain particles. The broadest uncertainty concerns long multistage aging, annealing, and classification near the fines threshold; K1 and the sealed recommendation are unchanged.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **S2 was the most robust tested solvent for the constrained objective.** Under the common C1, 250 K cooling program, batch 2 passed comfortably: crystal yield 0.512, purity 0.987, and fines 0.266. Batches 3–5 using S3, S1, and S0 respectively all exceeded the fines limit. This directly supports an empirical recipe-specific ranking, not a universal solvent mechanism.
- **There is a nonlinear concentration–quality tradeoff in S2.** With C0, batch 9 at 0.04 L S2 gave yield 0.566 and fines 0.249. At 0.02 L, batches 10 and 12 gave slightly higher or similar recovery, 0.575 and 0.569, but fines were 1.000. Batch 11 at 0.03 L passed with yield 0.561 and fines 0.281. The discontinuous deterioration at 0.02 L is directly observed; attributing it specifically to a supersaturation-driven nucleation threshold is an interpretation.
- **More seed did not rescue the tested 0.02 L regime.** Batch 10 used 0.02 g seed and batch 12 used 0.05 g, yet both had fines of 1.000. This contradicts the prospective hypothesis that added seed surface alone would restore acceptable particle quality there.
- **Crystallization strongly purified the target.** Final crystal purities were generally 0.98–1.00 despite reaction selectivities near 0.50–0.67. The purification itself is directly observed. Selective lattice incorporation, impurity rejection, and mother-liquor removal are plausible explanations but were not separately measured.

### Supported only provisionally or with confounding

- **C0 was the best working catalyst choice.** In the S2 catalyst comparison, batch 6/C0 gave yield 0.552, versus 0.512 for batch 2/C1, 0.481 for batch 7/C2, and 0.532 for batch 8/C3. These are direct numerical observations, but every catalyst condition was run once. The differences could include process variability and assay noise, so a general catalyst ranking remains unresolved.
- **Deep, slow cooling with immediate filtration was preferable to the batch-1 history.** Batch 1 yielded 0.436 with fines 0.428, whereas batch 2 yielded 0.512 with fines 0.266. However, endpoint temperature, cooling duration, control mode, and the presence of a warming hold all changed. The performance difference is observed; its allocation among those causes is unresolved.
- **The warm hold in batch 1 probably traded recovery against particle maturation.** Before the hold, particle imaging reported size 0.062 and fines 0.452; the final assay after warming reported size 0.076 and fines 0.428, while final recovery was only 0.436. This is consistent with some ripening or dissolution of fines, but the comparison spans different instruments and lacks a pre-hold recovery assay.

### Contradicted or revised

- The initial operational preference for **C1 based on nominal activity information** was revised after the catalyst comparison favored C0 numerically.
- The idea that **increasing concentration would monotonically improve useful recovery** was contradicted: gross recovery rose slightly at 0.02 L, but the product became unacceptable because all counted particles were fines.
- The proposed **high-seed rescue at 0.02 L** was directly contradicted by batch 12.

### Still untested

- Whether the fines at high loading arise primarily from primary nucleation, secondary nucleation, attrition, or insufficient growth time.
- Whether a staged solvent-removal or controlled seeding-temperature strategy could recover the high-loading material without excessive fines.
- Independent effects of cooling endpoint, cooling rate, and post-cooling hold.
- Replicability of the close batch-9 versus batch-11 recovery ranking; their 0.0045 difference is smaller than the combined single-assay uncertainty.
- The proposed kinetic equations for nucleation and growth. They organize the observations but were not fitted or independently validated.

## 2. One additional experiment

I would repeat the **batch-11 recipe exactly but reduce seed from 0.05 g to 0.02 g**: C0, S2 0.03 L, reagent 0.04 mol, 365 K for 3,600 s, cooling to 250 K over 14,400 s, immediate filtration. I would include particle-size measurement immediately before filtration and the required final assay.

This isolates seed dose at the intermediate loading and distinguishes two explanations:

1. **Seed-controlled explanation:** batch 11 passed because 0.05 g seed absorbed supersaturation and suppressed uncontrolled nucleation. With 0.02 g seed, the new batch should show smaller crystals, markedly higher fines—possibly above 0.50—and perhaps similar or slightly higher gross recovery.
2. **Concentration-threshold explanation:** 0.03 L is intrinsically below the severe nucleation threshold, while 0.02 L is above it; seed dose was not responsible for batch 11’s acceptable quality. The new batch should then remain near batch 11’s fines of 0.281 and yield of 0.561.

An intermediate outcome would indicate contributions from both mechanisms. A result differing substantially from both expectations would emphasize batch variability and the need for replication. One experiment cannot estimate reproducibility, but this comparison removes the major seed/loading confound between batches 9–12.

## 3. Least-used observation and least-reliable held-out prediction

### Observation used least effectively

The account underused the **within-batch particle measurement in batch 1 before its warm hold**. It showed size 0.062 and fines 0.452, whereas the final assay after warming showed size 0.076 and fines 0.428. That information could have been used more explicitly to argue that the warm excursion may have dissolved or matured fines even while reducing recovery. I treated the entire batch-1/batch-2 difference mainly as a cooling-history comparison. The limitation is that the two readings came from different instruments with different noise, and there was no pre-hold crystal-yield measurement.

The single pre-crystallization HPLC measurement from batch 1 was also weakly exploited because no matched HPLC measurements existed for the other batches; it could not separate reaction chemistry from crystallization effects.

### Least-reliable held-out prediction

**Q12 is the least reliable.** It doubles reagent loading relative to Q11 while using S0, an exceptionally long multistage cooling history, small absolute scale, and a seed-to-charge ratio outside the source experiments. The prediction extrapolated the S2 loading threshold to S0 even though solvent-dependent solubility and nucleation behavior can shift that threshold substantially. Its estimated fines value of 0.41 classified it as feasible, but its 80% interval of 0.25–0.59 crossed the 0.50 specification. Thus both the numerical estimate and the feasibility label are sensitive to an unvalidated interaction among loading, solvent, seed fraction, and prolonged aging. No prediction truth has been used, and the sealed prediction remains unchanged.
