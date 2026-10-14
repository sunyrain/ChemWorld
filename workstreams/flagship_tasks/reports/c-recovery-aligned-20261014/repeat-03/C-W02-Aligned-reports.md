# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Overall outcome
The campaign found a robust route to high-purity, moderate-to-high crystal recovery, but not to an acceptable particle-size distribution. All 12 batches had final crystal purity above 0.97, and several exceeded 0.50 seed-excluded recovery. However, every final assay reported a number fraction below 20 µm of approximately 0.987–1.000, far above the required 0.50. Thus fines control, rather than reaction conversion or purity, was the binding limitation.

The recommended batch remains batch 8 because it had the highest observed seed-excluded recovery: 0.6404, with purity 0.9810. Its fines fraction, 0.9870, was explicitly noncompliant.

### Reaction mechanism and material effects
A useful reaction bookkeeping relationship is

product yield ≈ conversion × selectivity,

with departures expected from measurement noise and the benchmark’s detailed species accounting. Conversion was generally near unity, so differences in target formation were governed mainly by selectivity and byproduct formation rather than incomplete reagent consumption.

Catalyst C0 emerged as the most useful tested catalyst. Under the C0/S2 reaction conditions in batch 2—353 K for 1800 s—the pre-crystallization HPLC showed conversion 0.985, selectivity 0.673, yield 0.643, and byproduct signal 0.201. The initial C1/S2 process in batch 1, operated more severely at 373 K for 3600 s, gave conversion 1.000 but selectivity only 0.590, yield 0.584, and byproduct signal 0.322. C2 was clearly poor in its tested setting: batch 3 gave selectivity 0.432 and ultimately only 0.334 crystal recovery. C3 was intermediate: batch 4 produced 0.481 recovery.

I interpret these results as evidence that driving conversion to completion by a hotter or longer reaction can sacrifice selectivity through competing byproduct or degradation pathways. A minimal kinetic picture is

R → P, rate kP(T,C); R → B, rate kB(T,C); P → D, rate kD(T),

where the catalyst changes the relative rates and elevated temperature or prolonged residence increases the accumulated B/D burden. This accounts qualitatively for batch 1’s complete conversion but worse selectivity and byproduct signal. The apparent C0 advantage is not a fully isolated catalyst effect, because batch 1 also differed in temperature and duration. The comparison among C0, C2, and C3 at approximately 353 K is more supportive, although downstream crystallization histories still differed.

Solvent affected both reaction selectivity and crystallization. The nominal dossier suggested S2 would combine low solubility, low nucleation tendency, rapid growth, and low impurity occlusion. Experimentally, S2 did support the maximum recovery in batch 8 and consistently high purity. S1 also appeared favorable for reaction selectivity: after its more complex reheat/recool history, batch 5’s final assay reported selectivity 0.729 and reaction yield 0.722, with crystal recovery 0.607. S0 in batch 11 likewise gave selectivity 0.734 and reaction yield 0.708, but recovery was only 0.539. S3 in batch 6 gave 0.472 recovery. Because these solvent batches did not share identical crystallization histories, they establish useful process-level contrasts rather than clean solvent coefficients.

### Reaction–crystallization coupling
Crystal recovery is defined by the campaign as

Ycrystal = n(target product in isolated solid, excluding seed) / n(initial reagent),

clipped to [0,1]. A useful approximate factorization is

Ycrystal ≈ X · S · Fcryst · Frecovery,

where X is reaction conversion, S is target selectivity, Fcryst is the fraction of target product transferred from solution into solid, and Frecovery represents filtration/handling retention. Consequently, crystallization cannot recover target product that was lost to reaction byproducts, while greater supersaturation or deeper cooling can raise solid recovery only for product actually formed.

This coupling is visible across the campaign. Batch 3’s poor reaction selectivity was followed by low crystal recovery despite high purity. In contrast, the selective C0 reactions in batches 5, 8, and 12 supported recoveries of 0.607, 0.640, and 0.626. Purity remained high because impurities largely stayed in the mother liquor or were weakly occluded, but that favorable rejection did not produce an acceptable particle population.

For crystallization, the mechanistically useful driving force is supersaturation,

σ = (C − C*)/C*,

with nucleation and growth represented schematically by

J ≈ kJ σ^m, G ≈ kG σ^g.

When nucleation J is large relative to growth G, product mass is divided among many crystals, giving a small number-weighted median and a high fines fraction. The campaign results indicate that this nucleation-dominated regime persisted throughout the tested space. Even the best normalized crystal-size result was only about 0.068 in batch 8—roughly 17 µm if the normalized value is d50/250 µm—consistent with its fines fraction near 0.99.

### Process-history dependence
Process history mattered, but none of the tested modifications changed the qualitative fines outcome.

- Batch 2 used no seed, slow cooling to 288 K, and a cold hold. It gave recovery 0.551, purity 0.983, normalized size 0.065, and fines 1.000.
- Batch 8 used the same principal C0/S2 reaction family but deeper cooling to 250 K. Recovery increased to 0.640, and normalized size reached 0.068, yet fines remained 0.987. This suggests deeper cooling increased precipitation sufficiently to improve recovery, but also retained or generated a very large population of sub-20-µm particles.
- Batch 10 stopped at a much warmer 303 K after adding 0.05 g seed. It still gave fines 1.000 and lower recovery, 0.540. Avoiding deep cooling therefore did not isolate a small population of acceptably coarse crystals in this run.
- Batch 9 extended cold aging through ten long holds. Rather than showing clear Ostwald ripening, its final normalized size was only 0.017 and fines were 1.000. Long residence alone was therefore not an effective coarsening strategy under the tested conditions.
- Batch 5 included reheating and recooling in S1. It achieved good recovery, 0.607, but normalized size fell to 0.021 and fines remained 1.000. The cycle may have redissolved some existing solids and then triggered renewed nucleation on recooling, although this interpretation was not directly measured.
- Batch 7 added 0.5 g seed before cooling. It achieved recovery 0.601 but fines 0.987. Batch 12 added 3 g seed only after deep cooling; recovery was 0.626, purity 0.996, normalized size 0.059, and fines 1.000. Thus neither warm seeding nor a very large late seed addition displaced the fine population.

These results revise the original hypothesis that moderate seeding plus slow cooling would suppress spontaneous nucleation. Seeding did not demonstrate a reproducible fines benefit. One possibility is that seeds partially dissolved when introduced warm, fragmented under agitation, or were overwhelmed by secondary nucleation. The late seeds in batch 12 were added after the fine population had already formed, so they could not reverse its number dominance. These mechanisms are interpretations; seed dissolution, attrition, and primary-versus-secondary nucleation were not separately observed.

### Purity–recovery–quality tradeoff
Purity and recovery were not strongly antagonistic in the explored domain: batch 8 combined 0.640 recovery with 0.981 purity, and batch 12 combined 0.626 recovery with 0.996 purity. The unresolved tradeoff was instead recovery versus particle quality. Deep cooling favored recovery, but the isolated solids remained overwhelmingly fine. Warmer termination, long aging, reheat/recool treatment, and larger seed charges all failed to reach the fines limit.

The gap from the specification is much larger than the stated final-assay noise: observed fines were near 0.99 versus a limit of 0.50, while the nominal fines noise was about 0.018. The conclusion that all tested batches failed the fines constraint is therefore robust, even though small rankings among their fines or size values are not.

### Revisions, uncertainty, and untested alternatives
The initial material-based prediction favored C1/S2 and expected slow cooling with modest seed to yield coarse, compliant crystals. The campaign revised that view in two ways: C0 gave better process performance in the tested reaction regime, and S2’s favorable nominal growth/nucleation properties were insufficient to prevent pervasive fines.

Many causal effects remain uncertain because the batches were adaptive rather than a replicated factorial design. Catalyst, solvent, reaction severity, cooling endpoint, holding time, and seed history were sometimes changed together. Instrument noise and fixed hidden material residuals further limit fine numerical comparisons. Accordingly, claims about C0 and S2 are strongest as recipe-family conclusions, not universal rankings.

Untested alternatives include controlled antisolvent addition, solvent blending, independently optimized supersaturation trajectories, filtration or classification that removes fines, deliberate agglomeration, lower-shear mixing, seed-size classification, and direct control around a measured metastable-zone boundary. These could plausibly alter the nucleation-to-growth ratio, but the campaign provides no experimental evidence for them. The existing data support pursuing a qualitatively different nucleation-control or post-crystallization classification strategy rather than merely repeating longer holds or larger seed additions.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.16 | 0.57 |
| Q01 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q01 | crystal_size | 0.28 | 0.15 | 0.44 |
| Q01 | crystal_yield | 0.51 | 0.4 | 0.62 |
| Q02 | crystal_fines_fraction | 0.47 | 0.25 | 0.7 |
| Q02 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q02 | crystal_size | 0.21 | 0.1 | 0.37 |
| Q02 | crystal_yield | 0.55 | 0.43 | 0.67 |
| Q03 | crystal_fines_fraction | 0.67 | 0.43 | 0.87 |
| Q03 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q03 | crystal_size | 0.16 | 0.07 | 0.3 |
| Q03 | crystal_yield | 0.41 | 0.29 | 0.53 |
| Q04 | crystal_fines_fraction | 0.39 | 0.18 | 0.63 |
| Q04 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q04 | crystal_size | 0.25 | 0.13 | 0.41 |
| Q04 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q05 | crystal_fines_fraction | 0.35 | 0.15 | 0.58 |
| Q05 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q05 | crystal_size | 0.28 | 0.15 | 0.44 |
| Q05 | crystal_yield | 0.44 | 0.32 | 0.56 |
| Q06 | crystal_fines_fraction | 0.87 | 0.68 | 0.98 |
| Q06 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q06 | crystal_size | 0.08 | 0.03 | 0.18 |
| Q06 | crystal_yield | 0.46 | 0.34 | 0.58 |
| Q07 | crystal_fines_fraction | 0.32 | 0.13 | 0.55 |
| Q07 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q07 | crystal_size | 0.3 | 0.16 | 0.47 |
| Q07 | crystal_yield | 0.44 | 0.32 | 0.56 |
| Q08 | crystal_fines_fraction | 0.74 | 0.49 | 0.93 |
| Q08 | crystal_purity | 0.96 | 0.9 | 0.995 |
| Q08 | crystal_size | 0.12 | 0.05 | 0.25 |
| Q08 | crystal_yield | 0.4 | 0.27 | 0.53 |
| Q09 | crystal_fines_fraction | 0.94 | 0.79 | 1 |
| Q09 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.11 |
| Q09 | crystal_yield | 0.12 | 0.04 | 0.24 |
| Q10 | crystal_fines_fraction | 0.78 | 0.56 | 0.94 |
| Q10 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q10 | crystal_size | 0.08 | 0.03 | 0.18 |
| Q10 | crystal_yield | 0.25 | 0.13 | 0.39 |
| Q11 | crystal_fines_fraction | 0.37 | 0.17 | 0.61 |
| Q11 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q11 | crystal_size | 0.27 | 0.14 | 0.43 |
| Q11 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q12 | crystal_fines_fraction | 0.68 | 0.43 | 0.87 |
| Q12 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q12 | crystal_size | 0.15 | 0.06 | 0.29 |
| Q12 | crystal_yield | 0.49 | 0.35 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are noise-free process predictions; the intervals represent extrapolation and mechanistic uncertainty rather than final-assay noise. Q01–Q02: S3 is expected to increase reaction activity and recovery relative to S1, but its greater nominal nucleation and impurity-occlusion tendencies should reduce purity and particle quality. Q03–Q04: adequate seeding should suppress uncontrolled primary nucleation, so 0.045 g seed is predicted to lower fines and enlarge d50 versus 0.001 g, with little recovery change. Q05–Q06: a staged slow ramp should favor growth over nucleation, whereas the 120 s crash is expected to create a persistent fine population that long cold residence cannot fully repair. Q07–Q08: continued cold growth is favored over reheating to 315 K and rapid recooling; the latter may dissolve part of the crop and trigger renewed nucleation, improving purity slightly but reducing recovery and size. Q09–Q10: particles are expected even after the short 292 K step because seed is present, but an additional two-hour hold should increase recovery and size without yet reaching the fines specification. Q11–Q12: doubling reagent loading should raise recovered product through greater supersaturation, but the fixed catalyst charge and increased nucleation/occlusion burden are expected to worsen purity, size, and fines. Uncertainty is widest for particle metrics because the campaign did not directly test these unusually long, finely stepped ramps; feasibility classifications near the 0.50 fines boundary, especially Q02, are correspondingly fragile.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Fines were the binding constraint.** Every completed batch had final purity above 0.97, whereas final fines fractions were approximately 0.987–1.000. Thus the tested processes reliably produced pure solids but never met fines ≤0.50.
- **High conversion did not guarantee high target recovery.** Batch 1 had HPLC conversion 1.000 but selectivity only 0.590 and byproduct signal 0.322; its crystal recovery was 0.479. Batch 2 had slightly lower measured conversion, 0.985, but better selectivity, 0.673, lower byproduct signal, 0.201, and higher recovery, 0.551. Interpreting this as competition between target and byproduct pathways is reasonable, although individual rate constants were not measured.
- **C0 was the best catalyst in the tested S2 recipe family.** Batch 2 with C0 substantially exceeded batch 3 with C2 in HPLC selectivity and final recovery; C3 in batch 4 was intermediate. The C0–C1 comparison is less clean because batch 1 used a hotter, longer reaction.
- **Deep cooling increased recovery without solving fines.** Batch 8, cooled to 250 K, gave the campaign’s highest recovery, 0.640, but fines remained 0.987. Batch 10, stopped at 303 K, had lower recovery, 0.540, and fines 1.000. The recovery contrast is observed; attributing it specifically to equilibrium solubility is an interpretation because these histories were not replicated.
- **Simple increases in seed charge or cold residence did not solve the problem.** Batch 7 used 0.5 g warm seed, batch 12 used 3 g cold seed, and batch 9 used ten long cold holds; all retained near-unity fines. This directly contradicts the original expectation that more seed or more aging alone would produce a compliant distribution.

### Contradicted or substantially revised
- **The initial C1/S2 recommendation was not supported.** The C1/S2 baseline in batch 1 was inferior to the subsequent C0/S2 family in reaction selectivity and recovery, although reaction severity was a confound.
- **The nominal S2 growth/nucleation profile did not translate into coarse crystals.** S2 did support high purity and the best recovery, but batches 1–4, 7–10, and 12 all remained dominated by fines.
- **A modest seed plus slow cooling was expected to be sufficient.** Batch 1 directly contradicted that expectation: purity and recovery were acceptable, but fines were 0.997.
- **Long cold aging as a simple ripening treatment was contradicted in the tested regime.** Batch 9 became neither coarse nor compliant after extended aging. This does not rule out ripening under a different solvent, temperature, or agitation regime.

### Still untested or unresolved
- Whether the fines arose mainly from primary nucleation, secondary nucleation, seed dissolution, or mechanical attrition was not directly observed.
- Solvent and catalyst effects were not established by a replicated factorial design; several comparisons changed reaction or crystallization history simultaneously.
- The campaign did not locate a metastable-zone boundary or measure supersaturation directly.
- Agglomeration, classified seeds, lower-shear operation, antisolvent control, solvent blending, and post-crystallization fines classification remain untested.
- The apparent purity–recovery compatibility is well observed, but the recovery–particle-quality tradeoff remains unresolved because no batch approached the fines threshold.

## 2. Most informative additional experiment

I would repeat the C0/S2 reaction used in batch 2—0.04 mol reagent, 0.08 L S2, 0.005 mol C0, 353 K for 1800 s—then standardize the quenched liquor at 300 K, add a modest classified seed charge, and apply a genuinely staged slow ramp to 278 K. I would collect non-destructive particle-size measurements immediately after particles first appear, at several intermediate temperatures, at 278 K, and after a final cold hold. A pre-quench HPLC measurement and a terminal final assay would separate reaction formation from crystallization recovery.

This single time-resolved experiment would distinguish three explanations:

1. **Primary-nucleation domination:** fines would jump toward unity as soon as supersaturation crosses the nucleation threshold and remain high thereafter. The remedy would require better supersaturation/seed control rather than longer aging.
2. **Insufficient growth time:** the early population would be fine, but d50 would steadily increase and fines would decrease during the staged ramp and hold. The earlier campaign’s one-step cooling and ordinary waits would then have been poor approximations to controlled growth.
3. **Secondary nucleation or attrition:** the population would initially be relatively coarse, followed by increasing fines during prolonged stirred residence. That result would motivate lower shear, shorter residence, or different solids handling.

If no particles appeared until deep cooling and then appeared abruptly, that would additionally indicate a wide metastable region followed by an uncontrolled nucleation burst. If particles appeared near 300 K and grew without a rising fine population, the staged-cooling hypothesis underlying several held-out predictions would gain support.

## 3. Least-used observation and least-reliable prediction

The account used **batch 5’s intermediate particle measurement** least effectively. Before reheating and recooling, that batch had normalized size about 0.048 and fines 1.000; its final assay after the thermal cycle had size about 0.021 and fines 1.000, while recovery reached 0.607. This within-batch comparison is stronger evidence about history than comparisons between independently prepared batches. It suggests that the reheat/recool cycle reduced the number-weighted size rather than promoting useful ripening, although measurement noise and continued precipitation prevent a unique mechanistic attribution.

The least reliable held-out prediction is **Q02**. I predicted fines 0.47 and therefore classified it as feasible, but that estimate lies just inside the 0.50 boundary. It extrapolates an unusually long staged cooling trajectory that was never tested in the campaign, uses S3 with C1 at lower loading and higher reaction temperature, and relies heavily on nominal solvent properties. The only experimental S3 batch, batch 6, used C0 and a very different cooling history and still had final fines 1.000. Consequently, both the estimated particle improvement and the binary feasibility classification for Q02 are fragile; its recovery and purity predictions are more defensible than its fines prediction.
