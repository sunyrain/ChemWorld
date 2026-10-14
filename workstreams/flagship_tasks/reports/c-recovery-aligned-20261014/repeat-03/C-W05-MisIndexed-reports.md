# C-W05-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended process (unchanged): batch 10 used 0.040 mol reagent, 0.080 L solvent S1, 0.005 mol catalyst C3, reaction at 360 K for 1,800 s with 500 rpm stirring, 0.050 g seed, cooling to 250 K over 14,400 s, filtration, termination, and final assay. It produced observed seed-excluded crystal yield 0.630, purity 0.981, and fines number fraction 0.433.

Reaction mechanism and material effects

A useful empirical decomposition is

Y_crystal ≈ X · S_target · f_capture,

where X is conversion, S_target is reaction selectivity to target, and f_capture is the fraction of formed target recovered as seed-excluded crystals. This is a bookkeeping relationship rather than an identified elementary mechanism. Nearly complete conversion was common, so differences in target inventory were governed mainly by selectivity and degradation, while solvent and thermal history governed capture and particle quality.

The initial material dossier suggested catalyst C1 because of its high nominal activity, but the matched S2 catalyst screen revised that expectation. At 360 K for 1,800 s with identical seeding and cooling, final crystal yields were 0.502 for C0 (batch 2), 0.413 for C2 (batch 3), 0.528 for C3 (batch 4), and 0.484 for C1 (batch 5). C3 also gave final selectivity 0.615 in batch 4, compared with 0.606, 0.508, and 0.582 for C0, C2, and C1. Thus C3 was the best empirical choice in this process region, although the C3–C0 difference is modest and each condition was run only once.

Temperature and residence time affected the reaction inventory before crystallization. Batch 1 used C1/S2 at 380 K for 3,600 s and reached complete conversion, but final selectivity was only 0.492 and degradation warning was 0.243. The milder 360 K/1,800 s batches retained approximately complete conversion while showing degradation warnings of roughly 0.07–0.12 and generally better selectivity. I interpret the severe batch as having driven parallel byproduct or degradation pathways after conversion was already high. An untested alternative is that catalyst-specific temperature sensitivity, rather than temperature alone, caused part of the difference; batch 1 was not a controlled temperature-only comparison.

Solvent identity affected both reaction selectivity and crystallization morphology. In the matched C3/360 K/1,800 s/270 K series, S0 gave crystal yield 0.582 but fines 0.755 (batch 6); S1 gave yield 0.605 and fines 0.346 (batch 7); S2 gave yield 0.528 and fines 0.337 (batch 4); and S3 gave yield 0.490 and fines 0.694 (batch 8). All four products were high-purity, approximately 0.972–1.000. S1 therefore supplied the best observed combination of target formation, recovery, and acceptable particle distribution. S0's nominal high nucleation tendency and low growth tendency are consistent with its high fines, but this interpretation is not unique: fixed-world solvent residuals and solvent effects on reaction selectivity also contributed. The nominal prior that S2 would be optimal was only partly correct—S2 controlled fines well but did not maximize recovery.

Reaction–crystallization coupling

Reaction selectivity sets the maximum target available for crystallization, while impurities can alter nucleation, growth, and occlusion. Nevertheless, solid purity stayed very high even when reaction selectivity was only about 0.5–0.7. This indicates strong solid-phase rejection of byproducts under the tested filtration conditions. High purity therefore did not imply a clean reaction; substantial non-target material apparently remained in the mother or cake liquor.

Using final reaction yield as a noisy proxy for target inventory, the ratio Y_crystal/Y_reaction was about 0.88 in batch 4, 0.89 in batch 7, 0.90 in batch 10, 0.92 in batch 11, and 0.92 in batch 12. These ratios suggest that the 250 K S1 process captured a greater fraction of available target than the 270 K process. They should not be treated as exact stage recoveries because both quantities are noisy final-assay channels, and the formal crystal-yield definition is relative to initial reagent charge.

A useful crystallization description is

σ(t) = C(t)/C*(T(t), solvent) − 1,

with nucleation rate increasing strongly with supersaturation σ and growth depending on σ, solvent, available crystal surface, and impurity adsorption. Crystal recovery rises when lower temperature reduces C*, but excessive σ favors secondary nucleation and therefore fines. Purity can be represented qualitatively as decreasing with impurity occlusion during rapid growth or nucleation. These relationships explain the observed recovery–fines tradeoff without identifying a unique microscopic nucleation law.

Process-history dependence

Cooling history mattered, not merely final temperature. Batch 1 was cooled to 270 K over 7,200 s and then held with a generic wait operation that allowed the slurry to warm back toward 297 K before filtration. It gave crystal yield 0.409 and fines 0.527. Batches 2–5 instead cooled to 270 K over 14,400 s and were filtered directly; their fines were 0.319–0.337. This supports slow, controlled cooling and prompt isolation, but batch 1 also differed in reaction temperature, time, catalyst, seed amount, and warming history, so it does not isolate cooling rate.

Within S1/C3 conditions, lowering the endpoint from 270 to 250 K increased recovery. Batch 9, with 0.050 g seed and a 270 K endpoint, gave yield 0.601 and fines 0.361. Batch 10, otherwise matched but cooled to 250 K, gave yield 0.630 and fines 0.433. The interpretation is increased thermodynamic capture at lower temperature accompanied by additional nucleation and a higher fines fraction.

Seed loading did not have a resolved effect. At 270 K, increasing seed from 0.010 g in batch 7 to 0.050 g in batch 9 changed yield from 0.605 to 0.601 and fines from 0.346 to 0.361. At 250 K, batches 10 and 11 used 0.050 and 0.010 g seed and gave yields 0.630 and 0.621 with fines 0.433 and 0.415. These small, inconsistent differences are comparable to measurement uncertainty and single-run variation. More seed may provide growth surface but may also raise the number count of small particles; neither effect was resolved here.

Concentration exposed the main unresolved quality/recovery tradeoff. Batch 12 reduced S1 volume from 0.080 to 0.040 L while otherwise matching batch 10. Its observed yield was 0.633, only 0.002–0.003 above batch 10, but fines increased from 0.433 to 0.487 and safety risk rose from 0.183 to 0.231. The higher concentration plausibly increased supersaturation and nucleation. Because 0.487 lies only 0.013 below the 0.50 constraint, while the stated final-assay fines standard deviation is 0.018, batch 12 has an uncertain constraint margin. This is why it did not displace batch 10.

Revisions and uncertainty

The principal revisions were: C1 was replaced by empirically superior C3; the prior preference for S2 was replaced by S1 after the solvent screen; and colder crystallization was adopted after it increased recovery while remaining nominally feasible. The initial belief that more seed would clearly suppress fines was not supported.

Final-assay standard deviations were approximately 0.010 for crystal yield, 0.010 for purity, and 0.018 for fines. Consequently, the yield difference between batches 10 and 12 is not resolved, whereas their fines difference is operationally important because batch 12 approaches the hard limit. Catalyst and solvent comparisons are also mostly unreplicated, so observed rankings combine true process effects with assay noise and possible batch variation. Untested alternatives include staged cooling, a controlled isothermal cold hold that does not warm toward ambient, intermediate solvent volumes, lower reaction temperature with longer residence, and replicated confirmation of C3 versus C0. These could improve recovery or establish robustness, but the sealed recommendation remains batch 10 because it offers essentially maximal observed recovery with materially greater fines-margin confidence.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.25 | 0.14 | 0.39 |
| Q01 | crystal_purity | 0.975 | 0.93 | 1 |
| Q01 | crystal_size | 0.21 | 0.12 | 0.32 |
| Q01 | crystal_yield | 0.52 | 0.4 | 0.63 |
| Q02 | crystal_fines_fraction | 0.42 | 0.27 | 0.59 |
| Q02 | crystal_purity | 0.965 | 0.9 | 1 |
| Q02 | crystal_size | 0.16 | 0.08 | 0.27 |
| Q02 | crystal_yield | 0.44 | 0.32 | 0.56 |
| Q03 | crystal_fines_fraction | 0.39 | 0.24 | 0.57 |
| Q03 | crystal_purity | 0.978 | 0.92 | 1 |
| Q03 | crystal_size | 0.18 | 0.09 | 0.3 |
| Q03 | crystal_yield | 0.45 | 0.33 | 0.57 |
| Q04 | crystal_fines_fraction | 0.34 | 0.21 | 0.5 |
| Q04 | crystal_purity | 0.978 | 0.92 | 1 |
| Q04 | crystal_size | 0.17 | 0.09 | 0.28 |
| Q04 | crystal_yield | 0.47 | 0.35 | 0.59 |
| Q05 | crystal_fines_fraction | 0.31 | 0.19 | 0.46 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.19 | 0.1 | 0.31 |
| Q05 | crystal_yield | 0.47 | 0.35 | 0.59 |
| Q06 | crystal_fines_fraction | 0.58 | 0.42 | 0.73 |
| Q06 | crystal_purity | 0.97 | 0.9 | 1 |
| Q06 | crystal_size | 0.12 | 0.05 | 0.22 |
| Q06 | crystal_yield | 0.48 | 0.36 | 0.6 |
| Q07 | crystal_fines_fraction | 0.3 | 0.18 | 0.45 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.2 | 0.11 | 0.32 |
| Q07 | crystal_yield | 0.47 | 0.35 | 0.59 |
| Q08 | crystal_fines_fraction | 0.23 | 0.12 | 0.39 |
| Q08 | crystal_purity | 0.985 | 0.94 | 1 |
| Q08 | crystal_size | 0.24 | 0.13 | 0.38 |
| Q08 | crystal_yield | 0.45 | 0.32 | 0.58 |
| Q09 | crystal_fines_fraction | 0.67 | 0.47 | 0.84 |
| Q09 | crystal_purity | 0.93 | 0.81 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.1 |
| Q09 | crystal_yield | 0.06 | 0.01 | 0.16 |
| Q10 | crystal_fines_fraction | 0.46 | 0.29 | 0.64 |
| Q10 | crystal_purity | 0.96 | 0.87 | 1 |
| Q10 | crystal_size | 0.09 | 0.035 | 0.18 |
| Q10 | crystal_yield | 0.18 | 0.08 | 0.32 |
| Q11 | crystal_fines_fraction | 0.32 | 0.19 | 0.48 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.19 | 0.1 | 0.31 |
| Q11 | crystal_yield | 0.47 | 0.35 | 0.59 |
| Q12 | crystal_fines_fraction | 0.4 | 0.25 | 0.57 |
| Q12 | crystal_purity | 0.97 | 0.9 | 1 |
| Q12 | crystal_size | 0.16 | 0.08 | 0.27 |
| Q12 | crystal_yield | 0.49 | 0.37 | 0.61 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where little seed-excluded product has crystallized. For Q01/Q02, prior campaign evidence favors S1 over S3 for both recovery and particle quality. For Q03/Q04, the seed effect was unresolved experimentally; I assign only a modest recovery and fines advantage to the larger seed charge, with strongly overlapping intervals. Q05/Q06 separates slow programmed cooling from a rapid crash followed by an equal-duration cold residence: similar equilibrium recovery is expected, but the crash should cause substantially more primary/secondary nucleation, smaller particles, and excessive fines. Q07/Q08 adds a dissolution–regrowth cycle; reheating may sacrifice a little retained yield but should dissolve fines and produce larger, cleaner crystals after recooling. Q09/Q10 predicts that continued growth at 292 K raises seed-excluded recovery and size and lowers fines, although recovery remains limited by the mild endpoint. Q11/Q12 doubles upstream concentration: based on the earlier concentration comparison, the fractional recovery gain should be small while supersaturation raises fines and reduces size. Purity is expected to remain high because prior solids strongly rejected reaction impurities. Intervals are deliberately broad because these recipes extrapolate far beyond the tested cooling durations, use C1/S0 conditions not optimized in the campaign, and most source comparisons were single runs; several feasibility classifications, especially Q02, Q04, Q10, and Q12, are therefore threshold-sensitive.

## K2

1. Status of the main claims

Supported by direct observations:
- **C3 was the best catalyst in the matched S2 screen.** Under the same 360 K/1,800 s reaction and crystallization recipe, crystal yields were 0.502, 0.413, 0.528, and 0.484 for C0, C2, C3, and C1 in batches 2–5. This supports using C3 in that tested region, although the C3–C0 difference was unreplicated and modest relative to uncertainty.
- **S1 gave the best observed recovery–fines balance.** In the matched solvent comparison, S0, S1, S2, and S3 gave yield/fines of 0.582/0.755 (batch 6), 0.605/0.346 (batch 7), 0.528/0.337 (batch 4), and 0.490/0.694 (batch 8). The direct result is the ranking under that recipe; attributing it specifically to solvent-dependent nucleation, growth, or reaction selectivity is interpretation.
- **Cooling to 250 K raised recovery but also increased fines.** Batches 9 and 10 were matched except for endpoints of 270 and 250 K. Yield rose from 0.601 to 0.630, while fines rose from 0.361 to 0.433. This directly supports a recovery–quality tradeoff with endpoint temperature.
- **Higher concentration approached the fines boundary without resolving a yield benefit.** Relative to batch 10, batch 12 halved solvent volume and produced yield 0.633 rather than 0.630, but fines rose from 0.433 to 0.487 and risk from about 0.183 to 0.231. The fines increase is consistent with higher supersaturation; the 0.003 yield difference is below useful resolution.
- **Solid purity was consistently high despite only moderate reaction selectivity.** Final purities were approximately 0.972–1.000 across the relevant batches, while selectivities were often about 0.5–0.7. Selective rejection of byproducts into liquor is a plausible interpretation, not a directly measured partition mechanism.

Contradicted or revised:
- **The initial nominal-prior preference for C1 was contradicted by the matched catalyst screen:** C3 outperformed C1 in batches 4 and 5.
- **The initial expectation that S2 would maximize the full objective was contradicted:** S2 controlled fines, but S1 produced greater feasible recovery in batches 4 and 7.
- **A strong claim that more seed suppresses fines was not supported and was directionally contradicted by point estimates.** At 270 K, batches 7 and 9 used 0.010 and 0.050 g seed and gave fines 0.346 and 0.361. At 250 K, batches 11 and 10 gave 0.415 and 0.433. These differences are small, so the defensible conclusion is unresolved rather than a proven adverse seed effect.

Still untested or confounded:
- Batch 1 associated 380 K/3,600 s operation with degradation warning 0.243 and poor selectivity, but it also differed in catalyst, cooling duration, seed charge, and post-cooling warming. A causal temperature/time degradation law was not isolated.
- The apparent benefit of slow cooling was not established by a clean equal-endpoint, equal-duration comparison. Batch 1 is too confounded for that purpose.
- Elementary reaction pathways, impurity identities, nucleation laws, and direct impurity partitioning were not observed. The relation `crystal yield ≈ conversion × target selectivity × capture fraction` was a useful balance, not proof of a molecular mechanism.
- Annealing, staged cooling, controlled cold holds, and repeatability of the best recipes remain untested.

2. One additional experiment

I would repeat the batch-10 chemistry through seeding, then replace its 14,400 s gradual cooling with a 120 s crash to 250 K followed by 14,280 s at 250 K. I would measure particle size immediately after the crash and again after the hold, then filter and perform the final assay. Thus endpoint, total cold-processing time, composition, and seed charge would match batch 10 while cooling history would differ.

This would distinguish three explanations:
- **Nucleation-history control:** the crash should initially give much higher fines and smaller particles; if the cold hold cannot erase that population, final fines should remain above batch 10, possibly exceeding 0.50, while recovery stays similar or rises slightly.
- **Endpoint/time control:** after the equal total duration, yield, size, and fines should approach batch 10 regardless of the initial ramp.
- **Ripening during the hold:** the first particle measurement should show a fine crash-generated population, but the second should show increasing size and falling fines. That would demonstrate history dependence followed by partial annealing.

This experiment is more diagnostic than another endpoint screen because it directly tests the cooling-rate interpretation that remained confounded in the campaign.

3. Least effectively used observation and least reliable prediction

The least effectively used observation was the **pre-filtration particle-size result in batch 10**: fines were about 0.412 before filtration, whereas the final assay reported 0.433. I relied mainly on the final result. The paired readings could have been used more explicitly to bound instrument disagreement, assess whether filtration or sampling altered the representative slurry measurement, and quantify how precarious near-threshold decisions are. Similar pre-/post-filter differences occurred in batches 6–12, but there were too few replicated measurements to separate process evolution from instrument noise.

The least reliable held-out prediction is **Q09**. It extrapolated to only 60 s of cooling at 292 K, far outside the campaign’s multi-hour crystallizations. The solids would likely be seed-dominated, making seed-excluded yield near a boundary and leaving uncertainty about how the number-weighted particle metrics respond before appreciable target deposition. No campaign batch tested this short-time regime or established whether seeded particles rapidly acquire enough product for final crystal-quality metrics to behave continuously. Accordingly, its predicted yield, fines, size, and even the practical meaning of its feasibility classification are less reliable than those for the long, fully developed crystallizations.
