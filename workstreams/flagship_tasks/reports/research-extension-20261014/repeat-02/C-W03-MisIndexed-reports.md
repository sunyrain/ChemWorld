# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Process and observed operating window
The recommended process is batch 10: 0.010 mol reagent and 0.080 L solvent S2 with 0.005 mol catalyst C1; react at 350 K for 3,600 s under nitrogen, quench, add 0.10 g seed, cool slowly to 300 K, hold twice for 14,400 s, cool slowly to 250 K, hold twice again, then filter. Its final assay gave seed-excluded crystal recovery 0.579, purity 0.981, and fines number fraction 0.291. Batch 12 repeated this recipe and gave 0.573 recovery, 0.997 purity, and 0.281 fines. Thus the observed recovery difference is not persuasive relative to assay uncertainty, while the duplicate supports a robust compliant region.

### Material effects
S2 was consistent with its nominal profile: relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. Under the optimized dilute conditions it supported high purity, useful recovery, and compliant fines. However, material choice alone was insufficient: batches 1, 2, and 4 also used S2 but at 0.040 mol reagent and produced fines fractions near 1 despite slow cooling, additional seed, long aging, or thermal cycling.

The high-loading solvent comparisons were directionally consistent with S2 being preferable but were not controlled enough to establish a quantitative solvent effect. Batch 3 used S3 and gave 0.245 recovery, 0.977 purity, and 0.995 fines; batch 5 used S1 and gave 0.410 recovery, 0.978 purity, and fines of 1.000. Comparable high-loading S2 batches gave about 0.45–0.46 recovery but likewise failed the fines constraint. Thermal histories and seed doses differed, so the lower S3 result cannot be assigned uniquely to solvent identity.

Only C1 was experimentally used. Its selection was based on the nominal activity dossier, not a campaign comparison. Effects of C0, C2, and C3—and catalyst–solvent interactions—remain untested.

### Reaction–crystallization coupling
Loading affected both reaction composition and crystallization behavior. At 0.040 mol reagent in 0.080 L, batch 1 showed complete conversion but only about 0.587 selectivity and 0.585 reaction yield, together with a substantial byproduct signal. In the 0.010 mol S2 batches, reported reaction yield and selectivity were generally about 0.78. Dilution therefore appears to have reduced competing chemistry or impurity formation as well as supersaturation.

A useful bookkeeping relationship is

`overall recovered target per charged reagent ≈ reaction target yield × crystallization recovery`,

while the campaign objective used only the second factor, defined as seed-excluded recovered target divided by target present before separation. For batch 10, the two reported factors were approximately 0.788 and 0.579. This distinction matters: improving crystallization recovery cannot compensate for target never formed upstream, and reaction impurities can change nucleation and occlusion even when final crystal purity remains high.

My mechanistic interpretation is that the high-loading mixtures crossed a nucleation-dominated supersaturation boundary. Numerous new crystallites then dominated the number-weighted distribution, explaining why added seed and long holds did not remove the fines problem. Dilution lowered both target and impurity concentrations enough for growth on a limited particle population to compete successfully with secondary nucleation. This interpretation is supported by the large fines change but was not directly verified by time-resolved concentration or nucleation measurements.

### Process-history dependence
History mattered, not merely final temperature. The successful batches used quenching, seeding before crystallization, a 300 K growth stage, extended low-agitation holds, and only then a colder recovery stage. This sequence plausibly allowed seeds or early crystals to establish growth area before stronger supersaturation developed.

At 0.010 mol loading, decreasing the second-stage endpoint generated a coherent recovery trend:

- Batch 6, 280 K: recovery 0.390, purity 1.000, fines 0.450.
- Batch 8, 270 K: recovery 0.480, purity 0.983, fines 0.296.
- Batch 9, 260 K: recovery 0.532, purity 0.985, fines 0.283.
- Batch 10, 250 K: recovery 0.579, purity 0.981, fines 0.291.

This is consistent with progressively lower equilibrium solubility increasing recovery after a growth-controlled population had formed. The lack of a fines penalty—and its apparent improvement relative to batch 6—suggests that the staged history kept these batches within a seeded-growth regime. Nevertheless, the series was not randomized or replicated at every temperature, and batch 6 used 0.05 g rather than 0.10 g seed. Therefore the endpoint-temperature effect is well supported for recovery but partly confounded for particle quality.

At high loading, process intensification did not rescue quality. Batch 2 used 0.50 g seed and two cooling stages but ended at fines 1.000; batch 4 added a reheating/ripening cycle and still ended at fines 1.000. Batch 3 used 1.0 g seed and long warm aging but remained at 0.995 fines. These results revised the initial hypothesis that more seed, slower cooling, or ripening alone would control the distribution.

### Loading boundary and quality/recovery tradeoff
The sharpest unresolved tradeoff is close to the loading boundary. Batch 10 at 0.010 mol and 250 K gave 0.579 recovery with 0.291 fines. Batch 11 increased loading to 0.011 mol at the same nominal endpoint and remained compliant, with 0.573 recovery, 0.995 purity, and 0.408 fines. In contrast, batch 7 at 0.0125 mol and 280 K gave 0.439 recovery but 0.986 fines. Because batch 7 also had a warmer endpoint, the exact threshold cannot be isolated; nonetheless, loading increases clearly consumed substantial fines margin without demonstrating better fractional recovery.

For a simple solubility-limited interpretation,

`R_c ≈ 1 − C*_mother(T_final, composition) V_mother / n_target,before separation`,

subject to kinetic losses, filtration retention, impurity effects, and the exclusion of seed mass. Lowering final temperature reduces the residual dissolved-target term. Increasing initial concentration can also raise supersaturation, but once the nucleation threshold is crossed it damages number-weighted particle quality. The data indicate that the latter penalty dominates between the tested 0.010–0.0125 mol loadings.

Purity was not the active constraint in the optimized region; fines were. Batch 10 had ample fines margin, while batch 11 traded much of that margin for no measured recovery gain. Thus the conservative 0.010 mol loading is justified even though a narrow intermediate loading or modified cooling schedule might eventually exceed batch 10’s recovery.

### Revisions and uncertainty
The initial expectation was that S2, seeding, and slow cooling would by themselves yield large, clean crystals. Batches 1–5 rejected that claim at high loading. The working mechanism was revised to treat concentration-dependent supersaturation—and its coupling to upstream selectivity—as the dominant control. Batches 6–12 supported that revision.

Final-assay standard-noise scales were approximately 0.010 for crystal recovery and purity and 0.018 for fines, with additional process uncertainty represented only indirectly. Accordingly, small differences such as batch 10 versus batch 12 recovery should not be overinterpreted. The large contrast between approximately 0.29 and approximately 0.99 fines is mechanistically meaningful, but the precise loading threshold is unresolved.

Other untested alternatives include different catalysts, mixed or staged solvent composition, seed-size distributions rather than seed mass alone, agitation below the available 100 rpm minimum, controlled antisolvent addition, selective fines removal, and direct mother-liquor analysis. Particle-size values were number-weighted and noisy; they do not establish crystal habit, breakage, or agglomeration. The proposed growth-versus-nucleation mechanism is therefore a compact explanation of the observations, not a uniquely identified microscopic mechanism.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.49 | 0.34 | 0.66 |
| Q01 | crystal_purity | 0.96 | 0.91 | 0.99 |
| Q01 | crystal_size | 0.09 | 0.05 | 0.14 |
| Q01 | crystal_yield | 0.36 | 0.26 | 0.47 |
| Q02 | crystal_fines_fraction | 0.35 | 0.22 | 0.51 |
| Q02 | crystal_purity | 0.98 | 0.94 | 1 |
| Q02 | crystal_size | 0.12 | 0.07 | 0.18 |
| Q02 | crystal_yield | 0.48 | 0.37 | 0.59 |
| Q03 | crystal_fines_fraction | 0.74 | 0.56 | 0.9 |
| Q03 | crystal_purity | 0.93 | 0.86 | 0.98 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.1 |
| Q03 | crystal_yield | 0.25 | 0.15 | 0.36 |
| Q04 | crystal_fines_fraction | 0.47 | 0.31 | 0.64 |
| Q04 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q04 | crystal_size | 0.085 | 0.04 | 0.14 |
| Q04 | crystal_yield | 0.29 | 0.19 | 0.4 |
| Q05 | crystal_fines_fraction | 0.43 | 0.28 | 0.59 |
| Q05 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q05 | crystal_size | 0.095 | 0.05 | 0.15 |
| Q05 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q06 | crystal_fines_fraction | 0.68 | 0.5 | 0.84 |
| Q06 | crystal_purity | 0.92 | 0.85 | 0.98 |
| Q06 | crystal_size | 0.06 | 0.025 | 0.11 |
| Q06 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q07 | crystal_fines_fraction | 0.41 | 0.26 | 0.57 |
| Q07 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q07 | crystal_size | 0.1 | 0.05 | 0.16 |
| Q07 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q08 | crystal_fines_fraction | 0.34 | 0.2 | 0.51 |
| Q08 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q08 | crystal_size | 0.12 | 0.065 | 0.18 |
| Q08 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q09 | crystal_fines_fraction | 0.86 | 0.68 | 0.98 |
| Q09 | crystal_purity | 0.95 | 0.87 | 1 |
| Q09 | crystal_size | 0.035 | 0.01 | 0.08 |
| Q09 | crystal_yield | 0.025 | 0 | 0.075 |
| Q10 | crystal_fines_fraction | 0.68 | 0.49 | 0.85 |
| Q10 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q10 | crystal_size | 0.055 | 0.02 | 0.1 |
| Q10 | crystal_yield | 0.11 | 0.04 | 0.2 |
| Q11 | crystal_fines_fraction | 0.44 | 0.29 | 0.61 |
| Q11 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q11 | crystal_size | 0.095 | 0.05 | 0.15 |
| Q11 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q12 | crystal_fines_fraction | 0.95 | 0.82 | 1 |
| Q12 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q12 | crystal_size | 0.05 | 0.015 | 0.1 |
| Q12 | crystal_yield | 0.49 | 0.37 | 0.61 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where seed-excluded product recovery is very small. Q01/Q02 isolate solvent: S3 is predicted to give higher recovery, faster growth, less occlusion and fewer nuclei than S1, although Q01 is borderline on fines. Q03/Q04 isolate seed mass in nucleation-prone S0; the larger seed charge provides substantially more growth surface and is predicted to move fines just below the specification. Q05/Q06 compare an extended ramp with an immediate crash to 278.15 K: the crash gives somewhat more recovery from longer residence at low temperature but generates many more fines. Q07/Q08 compare continued low-temperature aging with a 315 K dissolution/ripening cycle; the cycle is expected to sacrifice some recovery while dissolving fines and increasing mean size. Q09/Q10 show the effect of a two-hour hold at 292 K: recovery and size increase, but the short history remains fines-dominated. Q11/Q12 isolate loading; doubling reagent raises supersaturation and fractional recovery but is predicted to cross strongly into nucleation-dominated, non-feasible operation. Intervals include substantial extrapolation uncertainty because S0 and these very long, finely staged ramps were not directly studied; feasibility assignments use the point estimates, and Q01, Q04, Q05, Q07 and Q11 are especially sensitive to the fines uncertainty.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Loading was the strongest identified control of fines.** High-loading S2 batches 1, 2, and 4 (0.040 mol reagent in 0.080 L) had final fines near 1. In contrast, batch 6 at 0.010 mol had fines 0.450, and batches 8–10 at the same loading had fines about 0.28–0.30. The magnitude is much larger than assay noise. Interpreting this as a supersaturation-driven transition from growth to nucleation is plausible, but nucleation rates were not measured directly.
- **Colder second-stage endpoints increased crystallization recovery within the tested low-loading sequence.** Recovery rose from 0.390 at 280 K in batch 6 to 0.480, 0.532, and 0.579 at 270, 260, and 250 K in batches 8–10. Fines remained compliant. This is direct evidence for a recovery–endpoint relationship over that recipe family, although batch 6 also differed in seed dose.
- **The recommended operating region was reproducible at the resolution tested.** Batches 10 and 12 used the same nominal recipe and gave recovery 0.579 and 0.573, purity 0.981 and 0.997, and fines 0.291 and 0.281. The recovery difference is small relative to measurement/process uncertainty.
- **Purity was not the binding constraint in the studied region.** Every completed crystallization had high final purity, including batches that failed badly on fines. Fines, rather than purity, determined feasibility.

### Contradicted or substantially weakened
- **The initial claim that S2 plus seeding and slow cooling would be sufficient at high loading was contradicted.** Batch 1 failed on fines, as did batch 2 despite 0.50 g seed and extended staged cooling. Batch 4 remained fines-dominated after a reheating/ripening cycle.
- **Increasing seed mass alone was not shown to rescue an overloaded process.** Batches 2 and 3 used much more seed than batch 1 but still had fines near 1. Because solvent and thermal history also varied, this contradicts a strong rescue claim but does not quantify an isolated seed effect.
- **A single thermal cycle was not a general cure for fines.** Batch 4 still had fines of 1.000. That observation applies to its high-loading S2 regime; it does not rule out useful ripening cycles at lower loading.

### Still untested or unresolved
- Catalyst effects are untested because only C1 was used.
- A controlled solvent comparison is absent. Batches 3 and 5 suggest that S3 and S1 did not solve high-loading fines, but they differed in endpoint, seed dose, and history from the S2 batches.
- The precise loading boundary is unresolved. Batch 11 at 0.011 mol was compliant with fines 0.408, whereas batch 7 at 0.0125 mol had fines 0.986, but their final temperatures differed.
- Seed-dose effects are unresolved because seed changes were confounded with endpoint and loading.
- The proposed growth-versus-nucleation mechanism remains an interpretation. No time-resolved supersaturation, mother-liquor concentration, nucleation count, habit, agglomeration, or breakage measurements were obtained.

## 2. Most informative single additional experiment

I would repeat the batch-10 procedure exactly but charge **0.0125 mol reagent instead of 0.010 mol**, retaining S2, 0.005 mol C1, 0.080 L solvent, 0.10 g seed, the 300 K growth stage, the 250 K endpoint, and all hold times. I would make non-destructive particle-size measurements after the final 300 K hold and after the final 250 K hold, then filter and assay normally.

This experiment would separate two explanations for batch 7:

1. **Loading-threshold explanation:** 0.0125 mol crosses into a nucleation-dominated regime regardless of the colder endpoint. Expected result: fines rise sharply, possibly toward batch 7’s near-unity value, while recovery may increase only modestly or not at all. An early high-fines reading at 300 K would show that the poor distribution formed before final cooling.
2. **Thermal-history/endpoint explanation:** batch 7 failed because its warmer endpoint or specific history did not provide sufficient growth or ripening. Expected result: the batch-10 history at 250 K restores fines below 0.50 and could produce recovery above batch 10. A good distribution at 300 K followed by deterioration at 250 K would instead implicate secondary nucleation during the cold stage.

An intermediate outcome—such as fines near 0.5—would locate the practical loading boundary and quantify how little operating margin remains. This single batch is more discriminating than another replicate because it removes the main confound between batches 7 and 10.

## 3. Least effectively used observation and least reliable prediction

The account used the **crystal-size observations** least effectively. It emphasized recovery and fines, but normalized median size did not always move consistently with the fines fraction: for example, batch 7 reported size 0.081 with fines 0.986, whereas batch 9 reported the smaller size 0.066 with fines 0.283. This is possible because a median-size summary and the fraction below a fixed 20 µm threshold describe different aspects of a broad or multimodal distribution, but the campaign did not resolve that distribution. Instrument noise, seed inclusion, agglomeration, and filtration effects further limit mechanistic interpretation of size.

The least reliable held-out prediction is **Q08**, the S0 slow-cooling recipe followed by heating to 315 K and rapid recooling. It extrapolates simultaneously to an untested solvent, a different concentration and scale, an extremely long multistage history, and a dissolution–recrystallization cycle. The prediction assumed that the heat cycle would dissolve fines, increase mean size, and slightly reduce recovery. The only campaign evidence involving reheating was batch 4, where cycling did not rescue fines, and that batch was in a different, highly overloaded S2 regime. Consequently, even the direction of Q08’s fines and size changes relative to Q07 is less secure than the other paired predictions.
