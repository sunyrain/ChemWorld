# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended operating point
The sealed recommendation is **batch 11**: charge 0.040 mol limiting reagent, 0.080 L solvent S1, and 0.005 mol catalyst C0; heat at 380 K for 600 s with 600 rpm stirring; add 0.10 g seed in two 0.05 g additions; cool to 250 K over 14,400 s; filter immediately. Its final assay gave crystal yield 0.7255, purity 0.9937, and fines fraction 0.4072, satisfying purity ≥0.80 and fines ≤0.50.

### Material effects
**Catalyst.** The initial nominal-property prior favored C1, but the matched S2 screen at 360 K for 1,800 s revised that view. C0 gave the best reaction yield/selectivity and crystal recovery: batch 3 produced reaction yield 0.7035 and crystal yield 0.6170, compared with 0.6580/0.5781 for C1 in batch 2, 0.4902/0.4362 for C2 in batch 4, and 0.6254/0.5458 for C3 in batch 5. I interpret this as a fixed-world catalyst effect on competition between target formation and byproduct formation; nominal reference-panel activity did not capture selectivity in this reaction. The C0–C2 contrast is large, whereas smaller catalyst differences remain uncertain because each recipe was assayed once.

**Solvent.** Solvent controlled both reaction performance and crystallization behavior. With C0 at 360 K for 1,800 s, S1 gave the best feasible combination in batch 7: crystal yield 0.6843, purity 0.9785, and fines 0.4181. S0 supported stronger apparent chemistry and crystal yield 0.6670 in batch 6, but fines were 0.7400, so it was ineligible. This agrees qualitatively with S0’s nominal high nucleation tendency and impurity-occlusion tendency: rapid creation of many nuclei can produce a large number fraction of small particles even when mass recovery is high. S2, with nominally lower solubility and nucleation and higher growth tendency, consistently gave cleaner particle distributions; batch 3 had fines 0.3260 and purity 0.9912, although its recovery was below S1’s. S3 was intermediate chemically but batch 8 failed on fines at 0.5567. These comparisons support a real solvent effect, but they do not uniquely separate solvent effects on reaction kinetics, solubility, nucleation, and growth.

### Reaction–crystallization coupling
A useful bookkeeping relation is

`Y_crystal = X × S_target × R_cryst`,

where `X` is reagent conversion, `S_target` is target selectivity on converted reagent, and `R_cryst` is the fraction of produced target recovered as seed-excluded solid. The reported liquid-phase reaction yield is an empirical proxy for `X × S_target`. Thus an apparent downstream recovery can be estimated as

`R_cryst,app ≈ crystal_yield / reaction_yield`.

This ratio was about 0.88 in batch 3 and approximately 0.91 in batches 7, 10, 11, and 12. Therefore, near the final operating region, crystallization recovered roughly nine-tenths of the target indicated by the reaction assay; improving reaction selectivity was the major route to higher overall recovery. This decomposition is approximate because the two assay channels have noise and may not represent an exact mass-balance identity.

The observations are consistent with parallel or consecutive chemistry such as

`A → P`, `A → B`, and possibly `P → B/degradation`,

with rates `r_i = k_i(T) f_i(concentration)` and Arrhenius temperature dependence `k_i = A_i exp(−E_i/RT)`. A hotter, shorter exposure can be beneficial when desired conversion accelerates quickly but byproduct accumulation depends strongly on residence time. This is an interpretation rather than identification of a unique reaction network.

### Process-history dependence
The reaction results demonstrate that temperature and time cannot be reduced to a single endpoint temperature. In S1/C0:

- Batch 9, 340 K for 3,600 s: reaction yield 0.6456, selectivity 0.6319, crystal yield 0.5822, and fines 0.7294.
- Batch 7, 360 K for 1,800 s: reaction yield 0.7514 and crystal yield 0.6843, with fines 0.4181.
- Batch 10, 370 K for 1,200 s: reaction yield 0.7932, crystal yield 0.7190, and fines 0.4637.
- Batch 11, 380 K for 600 s: conversion 0.9559, selectivity 0.8539, reaction yield 0.7981, crystal yield 0.7255, and fines 0.4072.
- Batch 12, 380 K for 900 s: conversion 0.9963 and reaction yield 0.8151, but selectivity fell to 0.8156.

Thus the best feasible region shifted toward a short, hot reaction: batch 11 sacrificed a little conversion relative to batch 12 but retained higher selectivity and low degradation warning. The 340 K result shows that a longer, cooler exposure was not intrinsically gentler in this system.

Crystallization history was also important. A classical qualitative description uses supersaturation `σ = C/C* − 1`, nucleation rate increasing steeply with supersaturation, and crystal growth rate increasing more gradually. Solvent, cooling rate, seed surface area, and mixing determine whether supersaturation is consumed by growth on existing crystals or by formation of new fine particles. S2’s nominal low nucleation/high-growth profile is consistent with its low fines. The two seed additions in batch 11 plausibly supplied growth surface and limited secondary nucleation, but that mechanism was not independently tested against an otherwise identical single-seed batch.

The batch 1 warm hold illustrates history sensitivity: after cooling to 275 K, an uncontrolled 7,200 s wait allowed the material to warm toward ambient before filtration. Its crystal yield was only 0.4785. Batch 2 used colder final cooling and immediate filtration and reached 0.5781, although reaction temperature/time also changed, so the effect cannot be assigned solely to rewarming. A plausible interpretation is partial redissolution during warming.

### Unresolved recovery–quality tradeoff
Batch 12 had the highest observed recovery, 0.7409, and purity 0.9948, but its fines fraction was 0.5647 and therefore failed the specification. It combined a longer 380 K reaction with staged cooling through 320 and 280 K before reaching 250 K. Relative to batch 11, both reaction residence time and cooling program changed, so the increase in fines cannot be attributed uniquely to either higher product loading/supersaturation or staged cooling. This remains the central unresolved tradeoff: pushing target production and recovery higher can raise the number of fine particles beyond the allowed limit.

Batch 10 versus batch 11 also requires caution. Their crystal-yield difference is only about 0.0065, smaller than would justify a strong mechanistic ranking from single noisy assays. Batch 11 nevertheless had the highest observed feasible recovery and a more comfortable fines margin. Purity was not limiting in the optimized region; particle-number distribution was.

### Revisions and uncertainty
The main revisions were: C1 was replaced by C0 after the matched catalyst screen; S2 was replaced by S1 after solvent screening showed higher feasible recovery; and the reaction policy moved from moderate-temperature/longer residence to 380 K/600 s after batches 9–11. Claims about exact optima remain local because the campaign used single realizations rather than recipe replication. Instrument uncertainty, coupled recipe changes, and hidden fixed-world residuals prevent assigning precise kinetic constants or proving a unique nucleation mechanism. Untested alternatives include independently varying seed mass, cooling stages, agitation during cooling, and reaction time while holding every crystallization variable fixed. Those alternatives could potentially recover batch-12-level mass while restoring fines below 0.50, but the existing evidence does not establish that outcome.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.44 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q01 | crystal_yield | 0.56 | 0.44 | 0.67 |
| Q02 | crystal_fines_fraction | 0.26 | 0.14 | 0.4 |
| Q02 | crystal_purity | 0.989 | 0.956 | 1 |
| Q02 | crystal_size | 0.2 | 0.1 | 0.32 |
| Q02 | crystal_yield | 0.53 | 0.41 | 0.64 |
| Q03 | crystal_fines_fraction | 0.61 | 0.43 | 0.77 |
| Q03 | crystal_purity | 0.974 | 0.927 | 1 |
| Q03 | crystal_size | 0.075 | 0.025 | 0.15 |
| Q03 | crystal_yield | 0.47 | 0.34 | 0.59 |
| Q04 | crystal_fines_fraction | 0.36 | 0.21 | 0.52 |
| Q04 | crystal_purity | 0.982 | 0.943 | 1 |
| Q04 | crystal_size | 0.16 | 0.075 | 0.27 |
| Q04 | crystal_yield | 0.48 | 0.36 | 0.6 |
| Q05 | crystal_fines_fraction | 0.32 | 0.18 | 0.47 |
| Q05 | crystal_purity | 0.984 | 0.947 | 1 |
| Q05 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q05 | crystal_yield | 0.49 | 0.37 | 0.61 |
| Q06 | crystal_fines_fraction | 0.59 | 0.4 | 0.75 |
| Q06 | crystal_purity | 0.976 | 0.932 | 1 |
| Q06 | crystal_size | 0.105 | 0.04 | 0.2 |
| Q06 | crystal_yield | 0.5 | 0.37 | 0.62 |
| Q07 | crystal_fines_fraction | 0.3 | 0.17 | 0.45 |
| Q07 | crystal_purity | 0.985 | 0.949 | 1 |
| Q07 | crystal_size | 0.19 | 0.095 | 0.31 |
| Q07 | crystal_yield | 0.49 | 0.37 | 0.61 |
| Q08 | crystal_fines_fraction | 0.52 | 0.34 | 0.69 |
| Q08 | crystal_purity | 0.988 | 0.951 | 1 |
| Q08 | crystal_size | 0.14 | 0.06 | 0.25 |
| Q08 | crystal_yield | 0.42 | 0.29 | 0.55 |
| Q09 | crystal_fines_fraction | 0.82 | 0.65 | 0.93 |
| Q09 | crystal_purity | 0.96 | 0.89 | 0.997 |
| Q09 | crystal_size | 0.035 | 0.01 | 0.09 |
| Q09 | crystal_yield | 0.08 | 0.015 | 0.18 |
| Q10 | crystal_fines_fraction | 0.66 | 0.47 | 0.81 |
| Q10 | crystal_purity | 0.971 | 0.918 | 1 |
| Q10 | crystal_size | 0.075 | 0.025 | 0.16 |
| Q10 | crystal_yield | 0.24 | 0.12 | 0.38 |
| Q11 | crystal_fines_fraction | 0.33 | 0.19 | 0.49 |
| Q11 | crystal_purity | 0.984 | 0.946 | 1 |
| Q11 | crystal_size | 0.18 | 0.085 | 0.3 |
| Q11 | crystal_yield | 0.49 | 0.37 | 0.61 |
| Q12 | crystal_fines_fraction | 0.58 | 0.39 | 0.74 |
| Q12 | crystal_purity | 0.966 | 0.912 | 0.997 |
| Q12 | crystal_size | 0.12 | 0.045 | 0.23 |
| Q12 | crystal_yield | 0.42 | 0.29 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes add seed, so particles are expected even where little seed-excluded product crystallizes. Q01–Q02: S1 is predicted to give somewhat greater chemical production, while S3's lower nominal solubility, nucleation, and occlusion tendencies give slightly better size, fines, and purity; their overall yields remain close. Q03–Q04: increasing seed from 0.001 to 0.045 g should direct supersaturation toward seeded growth and sharply reduce uncontrolled fines, with only a small effect on seed-excluded recovery. Q05–Q06: gradual cooling should suppress the nucleation burst produced by the rapid crash; the long low-temperature hold makes their yields similar but is not expected to erase all CSD history. Q07–Q08: the 315 K reheating step may redissolve product, followed by rapid renucleation during the short recool, reducing recovered yield and worsening fines; beneficial Ostwald ripening is an untested alternative, hence wide intervals. Q09–Q10: an additional 7200 s at 292 K permits further growth and recovery, but the relatively warm endpoint and S0's high solubility leave recovery low and fines likely above specification. Q11–Q12: doubling reagent at fixed catalyst lowers catalyst fraction and raises supersaturation, so normalized recovery and particle quality are predicted to fall despite more absolute product. Intervals are deliberately broad because these recipes extrapolate far beyond the campaign in scale, seed-to-reagent ratio, and multi-day cooling history; purity is better constrained than yield or particle distribution.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C0 was the best catalyst in the matched S2 screen.** At 360 K for 1,800 s, batch 3 (C0) gave crystal yield 0.6170, versus 0.5781 for C1 (batch 2), 0.4362 for C2 (batch 4), and 0.5458 for C3 (batch 5). The observation supports a catalyst effect; attributing it specifically to target/byproduct kinetic competition is interpretation.
- **Solvent strongly affected particle quality.** Under matched C0 reaction conditions, S0 gave high recovery but excessive fines in batch 6 (yield 0.6670; fines 0.7400), S1 was feasible in batch 7 (0.6843; 0.4181), and S3 failed narrowly in batch 8 (0.5626; 0.5567). S2 also produced low fines in batch 3 (0.3260). The ranking is observed; assigning it to nominal solubility, nucleation, growth, and occlusion properties is mechanistic interpretation.
- **A short, hot reaction was locally favorable for C0/S1.** Batch 9 at 340 K/3,600 s gave reaction yield 0.6456 and crystal yield 0.5822; batch 10 at 370 K/1,200 s gave 0.7932 and 0.7190; batch 11 at 380 K/600 s gave 0.7981 and 0.7255. Batch 12 at 380 K/900 s increased conversion and reaction yield but reduced selectivity relative to batch 11. These observations support a temperature–residence-time dependence, although they do not identify kinetic constants.
- **Particle quality, rather than purity, became limiting.** Purity was approximately 0.98–1.00 throughout the optimized region, while fines crossed the 0.50 limit in batches 8, 9, and 12. Batch 12 had the highest recovery, 0.7409, but failed on fines at 0.5647.

### Contradicted or revised
- **The initial prior favoring C1 was contradicted** by the matched catalyst screen; C0 was superior in this world.
- **The initial expectation that S2 would be the overall best solvent was revised.** S2 gave good particle quality, but S1 delivered higher feasible recovery in batch 7.
- **A simple claim that slower or staged cooling necessarily reduces fines is not supported.** Batch 12 used staged cooling yet had more fines than batch 11. Because reaction residence time also changed, this is not a clean contradiction of the cooling mechanism alone.

### Still untested or unresolved
- The proposed parallel/consecutive network—target formation competing with byproduct formation or product degradation—was not uniquely identified.
- The approximate 0.88–0.91 ratio of crystal yield to reaction yield is useful bookkeeping, not proof of a constant crystallization-recovery coefficient.
- The claim that additional seed suppresses secondary nucleation remains untested: batches 10 and 11 differed in both reaction history and seed charge.
- The redissolution explanation for batch 1’s low recovery remains unresolved because batch 2 also changed reaction and cooling conditions.
- The cause of batch 12’s fines increase—longer reaction, greater product loading, staged cooling, or an interaction—was not separated.

## 2. One additional experiment

I would repeat the **batch-12 staged cooling program while keeping the batch-11 upstream process fixed**: C0/S1, 380 K for 600 s, 0.10 g total seed, then cool through 320 K and 280 K to 250 K using batch 12’s stage durations before immediate filtration.

This experiment uses batch 11 as the single-cool reference and distinguishes two principal explanations:

1. **Cooling-history explanation:** staged cooling itself produced excess secondary nucleation. The new experiment should retain batch-11-like reaction yield/selectivity but move fines upward toward batch 12’s 0.565, possibly with a broader size distribution.
2. **Upstream-loading explanation:** the extra 300 s at 380 K in batch 12 created more target or impurities and drove excessive supersaturation. The new experiment should remain near batch 11’s fines of 0.407 despite staged cooling; its recovery might change modestly through altered crystallization recovery.

An intermediate fines result would indicate contributions from both factors or a reaction–cooling interaction. This single experiment is preferable to another optimization run because it resolves the main confound behind the highest-recovery but infeasible batch.

## 3. Least effectively used observation and least reliable prediction

The account used the **crystal-size observation least effectively**, especially the fact that batch 12 had both higher normalized size (0.0946) and higher fines (0.5647) than batch 11 (0.0795 and 0.4072). I emphasized excess nucleation but did not fully reconcile those channels. Their coexistence could indicate a broadened or bimodal population containing both grown crystals and many new fines, rather than a uniform shift toward smaller particles. Single noisy summary statistics cannot establish that distributional interpretation.

The **least reliable held-out prediction is Q08**, the reheating-and-recooling thermal-history case. No campaign batch cleanly tested reheating an established slurry to 315 K and then recooling. Batch 1 only supplied a confounded warm-hold comparison and did not include the same recrystallization cycle. Reheating could cause net product loss and rapid renucleation, as predicted, but it could instead dissolve fines selectively and promote Ostwald ripening, producing larger particles and fewer fines. The held-out recipe also extrapolates to much lower loading and a multi-day cooling history, so both the point estimates and feasibility classification for Q08 are particularly uncertain.
