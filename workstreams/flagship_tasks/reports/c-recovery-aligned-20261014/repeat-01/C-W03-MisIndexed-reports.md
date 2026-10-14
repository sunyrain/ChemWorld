# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Overall picture
The process behaves as two coupled selections:

1. **Catalytic reaction** determines how much target product is available and how much byproduct/degradation material enters crystallization.
2. **Crystallization and isolation** determine what fraction of that target becomes seed-excluded solid, how efficiently impurities are rejected, and whether primary or secondary nucleation creates excessive fines.

A useful bookkeeping relationship is

\[
Y_{crystal}=Y_{reaction}\,f_{capture}\,f_{handling},
\]

where crystal yield is defined relative to the initial reagent charge and excludes added seed. Reaction yield may be viewed approximately as conversion times selectivity. The data show that both reaction selectivity and solid capture matter, although particle quality—not purity—was the binding constraint.

### Material effects

**Solvent S2 was the best tested crystallization medium overall.** Its nominal dossier indicated relatively low solubility, low impurity occlusion and nucleation tendency, and high crystal growth. Experimentally, S2 repeatedly produced very pure crystals with substantial recovery. Batch 1, using C1/S2 at full loading, gave crystal yield 0.393 and purity 0.986; the replicate Batch 7 gave 0.420 and 0.979. Batch 11, with a slightly larger seed charge, gave 0.408 and 0.993. This supports favorable target capture and impurity rejection in S2.

However, the initial interpretation that S2 would itself solve particle quality was revised. Those same batches had fines fractions of 0.725, 0.714 and 0.720, respectively. Thus the nominal low-nucleation tendency was qualitatively helpful but insufficient at full loading.

The solvent comparisons were not fully factorial and should not be treated as isolated causal estimates. With C0, S3 in Batch 4 gave only 0.139 crystal yield despite 0.999 purity and had fines at 1.0. S1 with a thermal recycle in Batch 5 gave 0.351 yield, 0.970 purity and fines at 1.0. S2 recipes generally retained more product. This is consistent with S2’s lower nominal solubility and impurity occlusion, but catalyst and thermal-history differences remain confounders.

**Catalyst identity mainly affected the reaction inventory presented to crystallization.** Across the tested recipes, conversion was near unity, while final reaction selectivity remained only about 0.42–0.55. This means selectivity, rather than conversion, limited target formation. Under the direct C1/S2 recipe, Batch 1 had final selectivity 0.503 and reaction yield 0.501; an in-process HPLC measurement had already shown complete conversion, selectivity about 0.511 and substantial byproduct signal. The crystals nevertheless reached 0.986 purity, showing strong impurity rejection during crystallization.

C3 under a closely similar S2 history in Batch 10 gave crystal yield 0.395, purity 0.978 and fines 0.766, with a larger degradation warning of 0.253. This was inferior to the replicated C1 process. C0 sometimes gave somewhat higher measured selectivity—0.546 in Batch 2—but its particle results depended strongly on the altered seeding and cooling history. C2 in Batch 3 gave selectivity 0.444 and only 0.243 crystal yield. Consequently, C1 remained the most defensible material choice, but the campaign does not establish a fully isolated catalyst ranking.

### Reaction–crystallization coupling

High conversion did not guarantee high crystal recovery because roughly half of the converted material was not target product. Crystallization then recovered only a fraction of the available target. For example:

- Batch 1: reaction yield 0.501 and crystal yield 0.393, corresponding to approximately 78% capture of the reaction target if handling losses are combined with crystallization losses.
- Batch 12: reaction yield 0.535 and crystal yield 0.409, approximately 77% target capture.
- Batch 4: reaction yield 0.405 but crystal yield only 0.139, approximately 34% capture under its S3/310 K history.

These ratios are descriptive rather than independently measured stage yields, but they illustrate why optimizing only conversion would be misleading.

Crystallization also decoupled solid purity from reaction selectivity. Even when liquid-phase selectivity was near 0.5 and byproduct signal near 0.33–0.40, most isolated solids had purity around 0.97–1.00. A simple interpretation is

\[
P_{crystal}=\frac{n_{target,solid}}{n_{target,solid}+n_{impurity,occluded}},
\]

with a small impurity distribution or occlusion coefficient in S2. This favorable purification came without solving the number-based fines problem.

### Supersaturation and particle-history interpretation

The observations are consistent with competition between nucleation and growth. If supersaturation is represented by

\[
\sigma=(C-C^*)/C^*,
\]

then a useful qualitative model is

\[
N_{new}\sim\int J(\sigma,T)\,dt, \qquad L\sim\frac{\int G(\sigma,T)\,dt}{N_{particles}},
\]

where nucleation rate increases very steeply with supersaturation, while growth distributes available product over the existing particle population. Fines increase when the integrated nucleation or fragmentation rate is large relative to growth on existing crystals.

The history experiments show that nominally “gentler” or longer processing was not monotonically beneficial:

- Batch 2 used 0.05 g seed and two 14,400 s cooling stages. It gave 0.413 recovery but fines at 1.0. The larger seed charge and long exposure did not suppress fines and may have increased the number of growth sites or secondary-nucleation opportunities.
- Batch 6 used only 0.005 g seed and staged cooling; it reached the campaign-high crystal yield of 0.435 but also had fines at 1.0. This is direct evidence of the unresolved recovery–particle-quality tradeoff.
- Batch 9 used rapid cooling steps separated by long, low-stirring holds. Its fines fraction was 0.871, worse than the direct 7,200 s cool in Batches 1 and 7. Long isothermal residence therefore did not simply ripen the distribution under the tested conditions.
- Batch 8 tested filtration, resuspension in fresh S2, mild reheating and recrystallization. The selective-fines-dissolution hypothesis was not supported: fines rose to 0.987, although purity remained 0.980 and recovery 0.393. Extra solvent, heating, redispersion and renewed nucleation are inseparable in this result.

The direct cooling recipe therefore performed better than the more elaborate annealing and recycle histories, even though it still failed the fines limit.

### Loading effect and final revision

The strongest morphology improvement came from reducing solution loading. Batch 12 used 0.020 mol reagent, 0.060 L S2, 0.0025 mol C1 and 0.010 g seed, followed by a 3,600 s reaction at a 370 K control target, quenching, and a 14,400 s direct cool to 278 K. It produced:

- crystal yield: 0.409;
- crystal purity: 0.995;
- fines fraction: 0.559;
- CSD quality: 0.662;
- normalized crystal size: 0.094;
- reaction yield: 0.535;
- selectivity: 0.530.

This was the best overall morphology and composite result, and it retained recovery comparable to the best full-loading C1/S2 batches. The mechanistic interpretation is that lower concentration reduced the supersaturation trajectory and primary/secondary nucleation burden, allowing a larger share of material to grow on existing crystals. This interpretation is plausible and consistent with the change, but it is based on one reduced-loading batch and is not a fitted law.

### Revisions and uncertainty

The initial hypotheses were revised in three important ways:

1. **S2 remained preferred for purity and recovery, but its nominal low-nucleation character did not ensure compliant fines.**
2. **More seed, longer cooling and thermal cycling were rejected as monotonic particle-quality rules.** Several such histories produced fines near 1.0.
3. **Lower loading replaced elaborate thermal manipulation as the leading particle-control hypothesis.** Batch 12 reduced fines to 0.559 while maintaining 0.409 recovery.

No completed batch met both purity ≥0.80 and fines ≤0.50. Batch 12 exceeded the fines limit by 0.059. The final-assay fines noise scale was stated as about 0.018, so this is not merely a tiny rounding difference, although a single observation cannot establish repeatability or a precise confidence interval. Differences such as 0.714 versus 0.725 between replicated full-loading batches are small relative to experimental and process variability and should not be interpreted as meaningful seed-dose effects.

The central unresolved tradeoff is that conditions giving high recovery frequently generated many fines: Batch 6 reached 0.435 recovery with fines at 1.0, while Batch 12 reduced fines substantially with only a modest recovery penalty but still failed specification. A modest further loading reduction is an untested alternative that might cross the fines boundary, but it could reduce productivity or endpoint recovery. Other untested alternatives include controlled antisolvent addition, different seed-size distributions, explicit supersaturation feedback, and gentler solids handling; none should be claimed effective from this campaign.

Accordingly, the sealed recommendation of Batch 12 is best understood as the closest tested basis for further development, not as a specification-compliant process.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.42 | 0.28 | 0.57 |
| Q01 | crystal_purity | 0.948 | 0.89 | 0.99 |
| Q01 | crystal_size | 0.16 | 0.1 | 0.23 |
| Q01 | crystal_yield | 0.35 | 0.26 | 0.44 |
| Q02 | crystal_fines_fraction | 0.3 | 0.18 | 0.44 |
| Q02 | crystal_purity | 0.974 | 0.94 | 0.998 |
| Q02 | crystal_size | 0.21 | 0.14 | 0.29 |
| Q02 | crystal_yield | 0.4 | 0.31 | 0.49 |
| Q03 | crystal_fines_fraction | 0.68 | 0.53 | 0.84 |
| Q03 | crystal_purity | 0.925 | 0.85 | 0.98 |
| Q03 | crystal_size | 0.085 | 0.035 | 0.15 |
| Q03 | crystal_yield | 0.31 | 0.22 | 0.4 |
| Q04 | crystal_fines_fraction | 0.43 | 0.29 | 0.58 |
| Q04 | crystal_purity | 0.944 | 0.88 | 0.99 |
| Q04 | crystal_size | 0.16 | 0.09 | 0.23 |
| Q04 | crystal_yield | 0.32 | 0.23 | 0.41 |
| Q05 | crystal_fines_fraction | 0.39 | 0.25 | 0.54 |
| Q05 | crystal_purity | 0.952 | 0.89 | 0.993 |
| Q05 | crystal_size | 0.175 | 0.105 | 0.25 |
| Q05 | crystal_yield | 0.33 | 0.24 | 0.42 |
| Q06 | crystal_fines_fraction | 0.73 | 0.57 | 0.88 |
| Q06 | crystal_purity | 0.932 | 0.86 | 0.982 |
| Q06 | crystal_size | 0.09 | 0.035 | 0.16 |
| Q06 | crystal_yield | 0.35 | 0.26 | 0.44 |
| Q07 | crystal_fines_fraction | 0.36 | 0.22 | 0.51 |
| Q07 | crystal_purity | 0.956 | 0.9 | 0.994 |
| Q07 | crystal_size | 0.19 | 0.115 | 0.27 |
| Q07 | crystal_yield | 0.34 | 0.25 | 0.43 |
| Q08 | crystal_fines_fraction | 0.27 | 0.14 | 0.45 |
| Q08 | crystal_purity | 0.97 | 0.92 | 0.998 |
| Q08 | crystal_size | 0.23 | 0.14 | 0.33 |
| Q08 | crystal_yield | 0.29 | 0.19 | 0.39 |
| Q09 | crystal_fines_fraction | 0.52 | 0.32 | 0.75 |
| Q09 | crystal_purity | 0.97 | 0.9 | 1 |
| Q09 | crystal_size | 0.055 | 0.02 | 0.11 |
| Q09 | crystal_yield | 0.025 | 0.002 | 0.075 |
| Q10 | crystal_fines_fraction | 0.44 | 0.27 | 0.64 |
| Q10 | crystal_purity | 0.965 | 0.9 | 0.998 |
| Q10 | crystal_size | 0.095 | 0.045 | 0.17 |
| Q10 | crystal_yield | 0.11 | 0.05 | 0.19 |
| Q11 | crystal_fines_fraction | 0.41 | 0.27 | 0.56 |
| Q11 | crystal_purity | 0.95 | 0.885 | 0.992 |
| Q11 | crystal_size | 0.17 | 0.1 | 0.245 |
| Q11 | crystal_yield | 0.32 | 0.23 | 0.41 |
| Q12 | crystal_fines_fraction | 0.58 | 0.42 | 0.74 |
| Q12 | crystal_purity | 0.928 | 0.85 | 0.982 |
| Q12 | crystal_size | 0.15 | 0.08 | 0.23 |
| Q12 | crystal_yield | 0.37 | 0.28 | 0.47 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when little seed-excluded product has deposited. Q01/Q02: S3 is predicted to outperform S1 through lower solubility, nucleation and impurity occlusion, despite S1's stronger nominal reaction activity. Q03/Q04: greater seed mass should distribute growth over established particles and suppress uncontrolled nucleation, with little effect on overall recovery. Q05/Q06: gradual staged cooling should reduce fines and increase size relative to an immediate temperature crash; the crash may recover slightly more product. Q07/Q08: reheating is expected to dissolve preferentially smaller particles and improve size and fines, but with some recovery loss; this pair has elevated uncertainty because the campaign's more complex resuspension/reheat history behaved adversely. Q09/Q10: the added 292 K hold permits continued deposition and growth, raising seed-excluded yield and size. Q11/Q12: doubled reagent loading should increase fractional recovery but also supersaturation, fines and impurity occlusion. Intervals are epistemic 80% ranges for noise-free outcomes; they are broad because these recipes extrapolate to S0, very long cooling histories, small scale and high seed-to-reagent ratios. Feasibility labels use point estimates, so cases near fines=0.50 remain uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **S2 favored purity and useful recovery.** Full-loading C1/S2 batches produced high purity and substantial crystal yield: Batch 1 gave 0.986 purity and 0.393 yield; its replicate Batch 7 gave 0.979 and 0.420; Batch 11 gave 0.993 and 0.408. This directly supports reproducible purification in S2.
- **Reaction selectivity, not conversion, limited target availability.** Batch 1 had essentially complete conversion but only about 0.50 selectivity and reaction yield. Nevertheless, its crystals were 0.986 pure. The observation is direct; the interpretation is that crystallization strongly rejected reaction impurities.
- **Recovery and particle quality traded off in the tested region.** Batch 6 achieved the highest crystal yield, 0.435, but fines were 1.0. Batch 12 retained 0.409 yield while reducing fines to 0.559. No batch met the fines limit, although purity was usually well above 0.80.
- **More seed or more time was not monotonically beneficial.** Batch 2 used 0.05 g seed and prolonged two-stage cooling but had fines of 1.0. Direct C1/S2 batches with 0.02–0.03 g seed had fines near 0.71–0.72. Batch 9 added long holds yet had fines of 0.871. These observations contradict a simple “more seed/longer aging always reduces fines” rule.

### Supported, but incompletely isolated
- **Lower loading was associated with better morphology.** Batch 12 had the campaign-low fines fraction, 0.559, and best CSD quality, 0.662. This supports the supersaturation interpretation, but Batch 12 also differed from Batches 1 and 7 in solvent volume and cooling duration. Therefore concentration is a leading explanation, not a proven isolated cause.
- **C1 was the most defensible catalyst choice.** A closely similar C3/S2 process in Batch 10 gave lower recovery, higher fines and a larger degradation warning than the C1 replicates. Other catalyst comparisons were confounded by different seed and thermal histories, so a complete catalyst ranking remains unresolved.

### Contradicted or substantially weakened
- **The initial expectation that S2 alone would ensure fines ≤0.50 was contradicted.** Replicated C1/S2 batches remained around 0.71–0.72 fines.
- **Selective fines removal by resuspension and thermal recycling was contradicted under the tested conditions.** Batch 8 ended with fines of 0.987 after filtration, S2 resuspension, reheating and recooling. Because several operations changed together, this rejects that complete procedure, not every possible ripening cycle.
- **Long low-temperature holds as a simple ripening remedy were weakened.** Batch 9 was worse in fines than the direct-cooling C1/S2 batches.

### Still untested
Controlled antisolvent addition, explicit supersaturation feedback, seed-size-distribution control, lower-shear isolation, and loading below Batch 12 were not tested. Likewise, the proposed nucleation/growth equations were explanatory relationships rather than fitted kinetic laws.

## 2. One additional experiment

I would run a matched low-concentration C1/S2 experiment using the Batch 1 history: 0.020 mol reagent in 0.080 L S2, 0.0025 mol C1, 0.010 g seed, reaction at the same 370 K target for 3,600 s, then a single 7,200 s cool to 278 K, filtration and final assay.

This would compare directly with the replicated full-concentration Batches 1 and 7 while removing Batch 12’s longer 14,400 s cooling period as an explanation.

Competing explanations and expected outcomes:
- **Concentration/supersaturation controls fines:** fines should remain near Batch 12’s approximately 0.56, or improve further, despite the shorter cooling period; purity should remain high and recovery near 0.4.
- **Long cooling time caused Batch 12’s improvement:** fines should rebound toward the 0.71–0.72 range of Batches 1 and 7.
- **The improvement reflects a recovery–supersaturation tradeoff:** fines should improve, but crystal yield should fall materially because the more dilute mother liquor retains more target.
- **Batch 12 was mainly an unrepeatable process realization:** results would fail to reproduce either its morphology or the full-loading baseline, motivating replication before further mechanism claims.

One experiment cannot separate every scale and seed-number effect, but this design most directly tests the key revision underlying the recommendation.

## 3. Least effectively used observation and least reliable prediction

The account used Batch 8’s reaction-channel changes least effectively. After resuspension and reheating, its final byproduct signal and degradation warning fell dramatically to about 0.027 and 0.021, yet selectivity was only about 0.429 and fines were 0.987. I emphasized the adverse particle result but did not adequately resolve whether the reaction-channel changes represented selective impurity removal, altered phase sampling, or limited comparability of post-filtration assay channels. They should not be interpreted as reversal of the original reaction chemistry without phase-specific mass balances.

The least reliable held-out prediction is **Q09**. It contains seed but only a 60 s crystallization step at 292 K before filtration. Consequently, particles may be dominated by the introduced seed while crystal yield explicitly excludes seed-derived solid. The campaign contained no close analogue with almost no product deposition, so the predicted yield, size and fines depend strongly on how little new target grows and how the seeded population enters the number-weighted particle measurement. Its particles-present judgment is robust because seed is added, but its quantitative particle-quality estimates and feasibility classification are highly uncertain.
