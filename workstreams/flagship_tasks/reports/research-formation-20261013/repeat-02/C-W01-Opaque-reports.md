# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### System and useful definitions
The materials were anonymous benchmark identities, so the evidence supports process relationships, not claims about real chemical structures.

I interpret the measured quantities using:

- Reaction target yield: approximately \(Y_{rxn}=X\,S\), where \(X\) is conversion and \(S\) is selectivity.
- Seed-excluded crystal recovery: \(R_c=n_{target,recovered\ solid}/n_{target,before\ separation}\). This is a crystallization-stage recovery, not overall yield from the initial charge.
- Crystal purity: \(P=n_{target,solid}/n_{total,solid}\).
- Fines fraction: \(F_{20}=N(d<20\,\mu m)/N_{total}\).
- A rough overall recovered-target fraction can be estimated as \(Y_{rxn}R_c\), but this was not the stated optimization metric.

All principal comparisons used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, reaction at 360 K for 3600 s under nitrogen, 0.05 g seed, cooling, filtration, and final assay.

### Material effects

**Observation—solvent:** Solvent S2 was the clearest determinant of acceptable particle quality. At a 290 K endpoint with catalyst C1, batch 6 (S2) gave crystal recovery 0.429, purity 1.000, and fines 0.273. The corresponding S0, S1, and S3 batches gave fines of 0.709 (batch 2), 0.532 (batch 5), and 0.696 (batch 7), respectively. Their recoveries were 0.428, 0.349, and 0.305.

**Interpretation:** S2 likely changed the balance among solubility, primary/secondary nucleation, and growth. It enabled target deposition onto a relatively limited particle population rather than producing predominantly new fine particles. This is supported by every tested S2/catalyst combination meeting both specifications: batches 6, 8, 9, and 10 had fines of 0.273, 0.223, 0.279, and 0.279, with purities of 0.979–1.000.

**Untested alternatives:** The experiments cannot distinguish whether S2 acts mainly through target solubility, impurity solubility, interfacial kinetics, aggregation, or a catalyst–solvent interaction. No solubility curve, induction-time experiment, microscopy, or polymorph identification was performed.

**Observation—catalyst:** Within S2 at the common 290 K crystallization endpoint, C0 was best: batch 8 gave recovery 0.456, versus 0.429 for C1 (batch 6), 0.365 for C2 (batch 9), and 0.423 for C3 (batch 10). Batch 8 also had the lowest observed fines, 0.223. Reaction yields/selectivities differed as well: batch 8 measured reaction yield 0.576 and selectivity 0.584, while batches 6, 9, and 10 measured yields of 0.557, 0.491, and 0.557.

**Interpretation:** Catalyst identity controls the amount and impurity composition of the target-bearing liquor delivered to crystallization. C0/S2 appears to give a favorable combination of target loading and impurity environment rather than merely maximizing conversion, which was already near unity in many batches.

### Reaction–crystallization coupling
Reaction performance and crystallization recovery were related but not interchangeable. For example, batch 2 had strong reaction metrics—yield 0.640 and selectivity 0.651—but only 0.428 crystal recovery and excessive fines of 0.709. Batch 12 had lower reaction yield, 0.575, but higher crystal recovery, 0.512, with fines 0.265. Thus, maximizing reaction yield alone would not select the recommended process.

Purities remained high even when reaction selectivity was moderate. Batch 12 had reaction selectivity 0.570 but crystal purity 0.995. This suggests selective rejection of byproduct into the mother liquor or preferential incorporation of target into the solid. The separation therefore partially decoupled final solid purity from reaction selectivity.

The rough products \(Y_{rxn}R_c\) are about 0.295 for batch 12 and 0.316 for batch 1. Batch 1 therefore might have recovered more target relative to initial charge, but it failed the particle constraint badly (fines 0.849). This illustrates why the official crystallization-stage objective and quality constraints must not be replaced by an overall-yield surrogate.

### Process-history dependence
The initial hypothesis was that seeding plus slow cooling would generally suppress fines. The data forced a revision: that strategy was insufficient outside a favorable solvent environment.

- Batch 1 used C0/S0, cooling to 270 K over 7200 s followed by a 7200 s uncontrolled wait. During the wait, the slurry warmed to about 291.6 K before filtration. It gave recovery 0.500 but fines 0.849.
- Batch 2 used a longer direct 14400 s cooling period to 290 K and improved fines to 0.709, but remained infeasible.
- Batch 4 included thermal preconditioning near 325 K before seeding and then cooling to 270 K; it still produced fines of 0.845 in S0.

These observations show that elapsed time alone was not sufficient. However, they do not isolate the effects of cooling duration, warming, catalyst, and seeding temperature because those factors were not varied orthogonally.

Within the better-controlled C0/S2 series, endpoint history showed a consistent recovery trend:

- Batch 8: 290 K endpoint, recovery 0.456, purity 0.981, fines 0.223.
- Batch 11: 270 K endpoint, recovery 0.483, purity 0.994, fines 0.254.
- Batch 12: 250 K endpoint, recovery 0.512, purity 0.995, fines 0.265.

Because each cooling period was 14400 s, the nominal average cooling rates increased from 0.00486 K/s at 290 K to 0.00625 K/s at 270 K and 0.00764 K/s at 250 K. Despite the faster average rate and greater supersaturation at lower endpoints, S2 kept fines well below 0.50. My interpretation is that the greater thermodynamic driving force increased deposition and recovery, while S2 and seeding limited uncontrolled nucleation sufficiently to retain acceptable particle quality.

### Revisions and uncertainty
The first revision was from a general “seeded slow cooling controls fines” hypothesis to a solvent-specific mechanism after batches 1–7. The second was from an initial preference for C1, based on the S0 reaction screen, to C0 after the catalyst comparison in S2 revealed a catalyst–solvent dependence. The final revision was that colder endpoints were beneficial within C0/S2 rather than necessarily creating an unacceptable fines penalty.

Each recipe received only one final assay; there were no exact process replicates. Final-assay standard deviations were approximately 0.010 for crystal recovery and purity and 0.018 for fines. The recovery increments from batch 8 to 11 (+0.027) and batch 11 to 12 (+0.030) exceed one assay-noise standard deviation, but process variability is not independently quantified. Consequently, the apparent monotonic endpoint relationship is credible but provisional.

The particle-quality margin in batch 12 is large relative to the constraint: fines 0.265 versus the 0.50 limit, and purity 0.995 versus the 0.80 minimum. Still, there is an unresolved quality/recovery tradeoff: lowering the endpoint from 290 to 250 K raised recovery by about 0.057 but also raised fines by about 0.042 and reduced normalized crystal size from 0.122 to 0.109. These changes remained acceptable in the tested range, but further cooling, faster cooling, or scale-up could eventually cross the fines boundary.

### Mechanistic conclusion
The most defensible mechanism is hierarchical: catalyst identity determines reaction selectivity and liquor composition; solvent identity then controls both reaction behavior and, more decisively, the nucleation-versus-growth balance; seeding and thermal history determine how supersaturation is consumed. S2 created a broad feasible particle-quality region across catalysts, C0 gave the best recovery within that region, and deeper cooling increased seed-excluded recovery while retaining ample purity and fines margins. This evidence supports the sealed recommendation of batch 12 without establishing a universal chemical mechanism beyond the tested anonymous system.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.25 | 0.11 | 0.43 |
| Q01 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q01 | crystal_size | 0.27 | 0.14 | 0.41 |
| Q01 | crystal_yield | 0.47 | 0.34 | 0.6 |
| Q02 | crystal_fines_fraction | 0.38 | 0.19 | 0.59 |
| Q02 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q02 | crystal_size | 0.23 | 0.1 | 0.38 |
| Q02 | crystal_yield | 0.41 | 0.28 | 0.55 |
| Q03 | crystal_fines_fraction | 0.64 | 0.42 | 0.83 |
| Q03 | crystal_purity | 0.97 | 0.9 | 0.997 |
| Q03 | crystal_size | 0.11 | 0.03 | 0.23 |
| Q03 | crystal_yield | 0.45 | 0.31 | 0.59 |
| Q04 | crystal_fines_fraction | 0.28 | 0.13 | 0.47 |
| Q04 | crystal_purity | 0.98 | 0.93 | 0.999 |
| Q04 | crystal_size | 0.28 | 0.15 | 0.42 |
| Q04 | crystal_yield | 0.5 | 0.37 | 0.63 |
| Q05 | crystal_fines_fraction | 0.24 | 0.1 | 0.42 |
| Q05 | crystal_purity | 0.98 | 0.93 | 0.999 |
| Q05 | crystal_size | 0.3 | 0.17 | 0.44 |
| Q05 | crystal_yield | 0.5 | 0.38 | 0.63 |
| Q06 | crystal_fines_fraction | 0.55 | 0.33 | 0.74 |
| Q06 | crystal_purity | 0.97 | 0.9 | 0.998 |
| Q06 | crystal_size | 0.17 | 0.07 | 0.3 |
| Q06 | crystal_yield | 0.51 | 0.38 | 0.64 |
| Q07 | crystal_fines_fraction | 0.26 | 0.11 | 0.45 |
| Q07 | crystal_purity | 0.98 | 0.92 | 0.999 |
| Q07 | crystal_size | 0.29 | 0.16 | 0.43 |
| Q07 | crystal_yield | 0.5 | 0.37 | 0.63 |
| Q08 | crystal_fines_fraction | 0.18 | 0.07 | 0.39 |
| Q08 | crystal_purity | 0.985 | 0.92 | 1 |
| Q08 | crystal_size | 0.35 | 0.18 | 0.52 |
| Q08 | crystal_yield | 0.47 | 0.31 | 0.61 |
| Q09 | crystal_fines_fraction | 0.84 | 0.66 | 0.96 |
| Q09 | crystal_purity | 0.96 | 0.84 | 0.997 |
| Q09 | crystal_size | 0.06 | 0.01 | 0.14 |
| Q09 | crystal_yield | 0.18 | 0.05 | 0.33 |
| Q10 | crystal_fines_fraction | 0.68 | 0.46 | 0.85 |
| Q10 | crystal_purity | 0.97 | 0.88 | 0.998 |
| Q10 | crystal_size | 0.12 | 0.04 | 0.24 |
| Q10 | crystal_yield | 0.36 | 0.21 | 0.51 |
| Q11 | crystal_fines_fraction | 0.24 | 0.1 | 0.43 |
| Q11 | crystal_purity | 0.98 | 0.92 | 0.999 |
| Q11 | crystal_size | 0.3 | 0.16 | 0.45 |
| Q11 | crystal_yield | 0.5 | 0.37 | 0.63 |
| Q12 | crystal_fines_fraction | 0.42 | 0.23 | 0.63 |
| Q12 | crystal_purity | 0.95 | 0.84 | 0.993 |
| Q12 | crystal_size | 0.23 | 0.1 | 0.38 |
| Q12 | crystal_yield | 0.66 | 0.51 | 0.79 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and reach supersaturation, so particles are expected. Q01–Q02: the earlier solvent screen favored S1 over S3 for recovery and fines, while the exceptionally long staged cooling should improve both relative to the tested short process. Q03–Q04: greater seed loading should suppress secondary nucleation and reduce number-weighted fines, with only a modest recovery effect. Q05–Q06: gradual cooling and crash cooling have similar endpoint driving force, but the crash should leave a persistent nucleation/fines penalty despite the long cold hold. Q07–Q08: the post-crystallization heat/cool cycle is interpreted as partial dissolution and regrowth, increasing size and lowering fines, at some risk to recovered yield. Q09–Q10: two hours at 292 K should increase recovery and growth relative to immediate filtration, but likely not erase the fines created by the 60-second drop. Q11–Q12: doubling reagent concentration should raise fractional recovery through greater supersaturation, while increasing nucleation, fines, and impurity-incorporation risk. Intervals are deliberately wider than final-assay noise because these recipes extrapolate far beyond the campaign in concentration, temperature, duration, and thermal cycling; several fines intervals cross the 0.50 specification even where the point estimate is feasible.

## K2

## 1. Status of the main claims

### Supported within the tested domain

**S2 was the strongest low-fines solvent.** Direct observation: with C1 and the same 290 K cooling endpoint, batch 6 (S2) produced fines 0.273, versus 0.709 in batch 2 (S0), 0.532 in batch 5 (S1), and 0.696 in batch 7 (S3). Moreover, all tested S2 batches—6, 8, 9, and 10—met purity and fines specifications across catalysts C0–C3. Interpretation: S2 favors a better nucleation/growth balance. The causal molecular reason remains unknown.

**C0 was best among catalysts under the tested S2/290 K conditions.** Direct observation: batch 8 had recovery 0.456 and fines 0.223, compared with recoveries of 0.429, 0.365, and 0.423 for C1, C2, and C3 in batches 6, 9, and 10. Interpretation: C0 creates a liquor composition favorable to subsequent crystallization. Because each condition was run once, this is evidence for a local optimum, not a universal catalyst ranking.

**Colder endpoints increased recovery in the C0/S2 series without violating quality limits.** Direct observation: batches 8, 11, and 12 gave recoveries of 0.456, 0.483, and 0.512 at 290, 270, and 250 K; fines were 0.223, 0.254, and 0.265, respectively. Interpretation: greater supersaturation increased deposition while S2 and seeding kept secondary nucleation controlled. The trend is provisional because endpoint and average cooling rate changed together and there were no exact replicates.

**Crystallization partially decoupled solid purity from reaction selectivity.** Direct observation: batch 12 had reaction selectivity 0.570 but crystal purity 0.995; similarly high solid purities occurred throughout the campaign. Interpretation: byproducts were preferentially retained in the mother liquor or excluded from the crystal lattice. Direct phase-composition measurements were not made.

### Contradicted or substantially revised

**The initial claim that seeding plus slow cooling would generally control fines was contradicted.** Batches 1–4 all used S0 and remained fines-rich: 0.849, 0.709, 0.909, and 0.845. Batch 4’s pre-seeding thermal adjustment also failed to rescue particle quality. The revised claim was narrower: seeding and cooling history worked only in a favorable solvent domain, especially S2.

**The early preference for C1 was not general.** C1 looked strongest in the S0 reaction screen, but the matched S2 catalyst comparison favored C0 in batch 8. This supports a catalyst–solvent interaction or, at minimum, context-dependent catalyst ranking.

**A simple rule that slower cooling alone minimizes fines was not supported.** The C0/S2 endpoint series retained acceptable fines even as the nominal average cooling rate increased toward the colder endpoint. Solvent and supersaturation history mattered more than a one-variable cooling-rate rule.

### Still untested

The experiments did not distinguish whether S2 acts through equilibrium solubility, induction time, interfacial growth kinetics, aggregation, impurity adsorption, or polymorph selection. Exact reproducibility, scale dependence, seed-size distribution, and the consequences of very long staged cooling or deliberate annealing also remain untested. The held-out recipes extrapolated into those regions but supplied no truth.

## 2. One additional experiment

I would run an exact matched analogue of batch 8, replacing S2 with S0 while keeping C0, charge concentrations, 360 K/3600 s reaction, 0.05 g seed, 14400 s cooling to 290 K, filtration, and assay unchanged. Existing batch 1 is not an adequate matched control because it used a different endpoint, shorter cooling, and an uncontrolled warming hold.

This would distinguish three explanations:

1. **General S2 solvent effect:** matched C0/S0 should return to the S0-like fines-rich regime, plausibly above 0.50, while C0/S2 batch 8 remains at 0.223.
2. **C0 alone or the 14400 s cooling history is sufficient:** matched C0/S0 should also give fines at or below 0.50 and approach batch 8.
3. **Solvent mainly changes equilibrium recovery rather than nucleation:** the two batches could have similar fines but materially different crystal recovery.

A high-fines C0/S0 result would strengthen the solvent-main-effect account. A low-fines result would instead indicate that the earlier S0 failures were caused by catalyst or thermal-history confounding, weakening the claimed general advantage of S2.

## 3. Least effectively used observation and least reliable prediction

**Least effectively used observation:** the account underused the mismatch between crystal-size and fines measurements. For example, batch 2 had normalized crystal size 0.097 but fines 0.709, whereas batch 6 had the smaller size estimate 0.067 but much lower fines, 0.273. Similar non-monotonicity appeared elsewhere. I treated S2’s result mainly as evidence for suppressed nucleation, but these paired metrics could instead indicate broad or bimodal particle distributions, aggregation, or inconsistency between noisy summary channels. A stronger account would have avoided equating larger reported size with fewer fines and would have emphasized the full CSD uncertainty.

**Least reliable held-out prediction:** Q08. Its post-crystallization excursion to 315 K followed by recooling to 278.15 K had no close campaign analogue. Partial dissolution could remove fines and promote regrowth, as assumed in the sealed prediction, but the same excursion could dissolve nearly all product and cause renewed nucleation during the relatively rapid recooling. Even the direction of the effect on size and fines is therefore less secure than for the other paired comparisons. Q06 and Q12 were also large extrapolations, but Q08 uniquely depended on an untested non-monotonic thermal-cycle mechanism.
