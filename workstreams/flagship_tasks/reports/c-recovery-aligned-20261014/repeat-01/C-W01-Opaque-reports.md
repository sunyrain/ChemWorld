# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Scope and evidence
The catalyst and solvent labels are anonymous benchmark identities, so the mechanism below is phenomenological rather than a claim about real molecular structures. Each condition was tested once; observed differences therefore combine material effects, process effects, and measurement/process variability.

### Reaction-stage material effects
Catalyst C0 was the most promising catalyst in the screened space. Batch 1 (C0/S0) gave reaction yield 0.616 and final crystal yield 0.518. Under broadly comparable C1–C3/S0 experiments, batches 2–4 gave final crystal yields of 0.318, 0.200, and 0.312. This motivated focusing subsequent work on C0. However, batch 1 had a different crystallization history, so the exact catalyst effect size is not isolated; the evidence supports a practical ranking, not a detailed catalytic pathway.

Solvent altered both reaction selectivity and solid formation. With C0 and the later staged-cooling process, S1, S2, and S3 gave final crystal yields of 0.341, 0.443, and 0.290 in batches 5–7. S2 also gave the best morphology: batch 6 had purity 1.000 and fines fraction 0.257. S1 was compliant but less productive, while S3 was approximately at the fines boundary and had lower recovery. A 1:1 S0/S2 mixture in batch 8 was also compliant (yield 0.449, purity 0.977, fines 0.306), but was not clearly superior to neat S2.

The observations are consistent with solvent-dependent changes in reaction selectivity, product solubility, and nucleation kinetics. Those individual contributions were not independently measured, so alternative explanations—such as solvent-dependent catalyst activity or impurity incorporation—remain possible.

### Reaction–crystallization coupling
A useful bookkeeping relationship is

Y_crystal = Y_reaction × R_apparent,

where Y_crystal is seed-excluded solid target divided by initial reagent, Y_reaction is the measured reaction-stage target yield, and R_apparent is an apparent downstream recovery. It is not a separately calibrated mechanistic constant, because the measurements are noisy and taken at different process stages.

For batches 6, 11, and 12, the approximate Y_crystal/Y_reaction ratios were 0.902, 0.917, and 0.926. Thus, once C0/S2 generated target product, the staged crystallization recovered roughly nine-tenths of the measured reaction yield. In batch 1 this ratio was lower, about 0.841, and its fines fraction was 0.872. This suggests that improving reaction yield alone is insufficient: the solvent and thermal history must also deliver the product into an acceptable particle population.

Purity was generally high—about 0.97–1.00 in the important later batches—even when recovery and morphology varied strongly. The dominant optimization conflict was therefore recovery versus particle-number quality, rather than recovery versus chemical purity.

### Process-history dependence
The successful later history used reaction at 350 K for 3600 s, followed by staged cooling toward 315 K, seeding with 0.05 g, long low-agitation holds, further cooling through 285 K, and a final 250 K hold before filtration. In S2 this produced compliant material in batch 6 and, at higher concentration, batch 11.

A qualitative nucleation/growth framework is useful:

S = C/C*,
J approximately proportional to exp[-B/(ln S)^2],
G approximately proportional to (S − 1)^g,

where S is supersaturation, J is primary nucleation rate, and G is crystal growth rate. Slow staged cooling and seeding provide existing surface area and limit sudden supersaturation, favoring growth over creation of many new particles. Conversely, once supersaturation becomes too large, J can rise very sharply and generate a large number fraction of fines.

The concentration series supports that interpretation. With 0.04 mol reagent:

- Batch 6 used 0.08 L S2 (nominal 0.5 mol/L) and gave yield 0.443, purity 1.000, and fines 0.257.
- Batch 11 used 0.04 L S2 (nominal 1.0 mol/L) and improved yield to 0.488 while retaining purity 0.997 and fines 0.280.
- Batch 12 used 0.02 L S2 (nominal 2.0 mol/L) and increased yield to 0.518, but its fines fraction rose to 1.000.

Thus concentration improved reaction yield and overall recovery up to a point, but the 2.0 mol/L experiment crossed a strong morphology boundary. Its safety risk also increased to about 0.330 versus 0.214 for batch 11, although both remained below the stated 0.65 limit.

Temperature history also mattered. Batch 9 used C0/S2 at 330 K for 7200 s and produced only 0.316 crystal yield with fines 0.502, compared with 0.443–0.488 for the 350 K/3600 s S2 processes. Since both temperature and time changed, this result favors the 350 K process operationally but does not uniquely identify an activation-energy or degradation mechanism.

An attempted warm ripening cycle in batch 3 did not rescue morphology: yield was 0.200 and fines 0.828. Because that batch also used catalyst C2, it does not provide a clean test of ripening for the C0/S2 system.

### Revisions during the campaign
The initial expectation was that slow cooling and seeding would generally suppress fines. The results narrowed this claim: staged cooling worked well in favorable solvents, especially S2, but did not overcome all material effects. Solvent identity was at least as important as the cooling schedule.

The initial catalyst screen shifted attention from broad catalyst exploration to C0. Subsequent solvent screening shifted the preferred medium from high-reaction-yield S0 toward S2 because S0 produced unacceptable fines in batch 1. Finally, concentration was recognized as a coupled control variable: increasing S2 concentration from 0.5 to 1.0 mol/L improved recovery without sacrificing quality, whereas increasing it to 2.0 mol/L caused catastrophic fines formation.

### Uncertainty and unresolved tradeoff
Batch 11 remains the selected operating experiment because it had the highest observed crystal yield among clearly compliant batches: 0.488 yield, 0.997 purity, and 0.280 fines. Batches 1 and 12 had numerically higher yields near 0.518 but violated the fines constraint severely.

No condition was replicated, so reproducibility and between-batch variance are unresolved. Final-assay noise was stated as approximately 0.010 for crystal yield, 0.010 for purity, and 0.018 for fines; process variability may be larger. The particle-size and final-assay readings generally supported the same classifications, although batch 9 was borderline at fines 0.502 and should not be treated as robustly compliant.

The principal untested opportunity is an intermediate S2 concentration between 1.0 and 2.0 mol/L. It might recover some of batch 12’s additional yield while remaining below the fines limit. Other unresolved alternatives include changing seed temperature or seed loading, using a still slower concentration-aware cooling profile, testing solvent composition between neat S2 and the mixtures, independently varying reaction time and temperature, and replicating batch 11. These could clarify whether the observed recovery–fines boundary is abrupt, gradual, or sensitive to uncontrolled batch variation.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.14 | 0.05 | 0.28 |
| Q01 | crystal_purity | 0.98 | 0.93 | 1 |
| Q01 | crystal_size | 0.19 | 0.11 | 0.29 |
| Q01 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q02 | crystal_fines_fraction | 0.24 | 0.1 | 0.42 |
| Q02 | crystal_purity | 0.97 | 0.9 | 1 |
| Q02 | crystal_size | 0.15 | 0.08 | 0.25 |
| Q02 | crystal_yield | 0.23 | 0.14 | 0.34 |
| Q03 | crystal_fines_fraction | 0.36 | 0.18 | 0.58 |
| Q03 | crystal_purity | 0.97 | 0.91 | 1 |
| Q03 | crystal_size | 0.12 | 0.06 | 0.21 |
| Q03 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q04 | crystal_fines_fraction | 0.16 | 0.06 | 0.31 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.19 | 0.11 | 0.29 |
| Q04 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q05 | crystal_fines_fraction | 0.15 | 0.05 | 0.29 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.19 | 0.11 | 0.3 |
| Q05 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q06 | crystal_fines_fraction | 0.63 | 0.42 | 0.82 |
| Q06 | crystal_purity | 0.96 | 0.87 | 1 |
| Q06 | crystal_size | 0.08 | 0.03 | 0.16 |
| Q06 | crystal_yield | 0.31 | 0.2 | 0.42 |
| Q07 | crystal_fines_fraction | 0.17 | 0.06 | 0.32 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.18 | 0.1 | 0.29 |
| Q07 | crystal_yield | 0.3 | 0.2 | 0.41 |
| Q08 | crystal_fines_fraction | 0.12 | 0.03 | 0.28 |
| Q08 | crystal_purity | 0.99 | 0.94 | 1 |
| Q08 | crystal_size | 0.23 | 0.13 | 0.35 |
| Q08 | crystal_yield | 0.27 | 0.16 | 0.39 |
| Q09 | crystal_fines_fraction | 0.72 | 0.48 | 0.91 |
| Q09 | crystal_purity | 0.94 | 0.75 | 1 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.1 |
| Q09 | crystal_yield | 0.02 | 0 | 0.07 |
| Q10 | crystal_fines_fraction | 0.49 | 0.28 | 0.7 |
| Q10 | crystal_purity | 0.96 | 0.85 | 1 |
| Q10 | crystal_size | 0.08 | 0.03 | 0.16 |
| Q10 | crystal_yield | 0.1 | 0.04 | 0.19 |
| Q11 | crystal_fines_fraction | 0.16 | 0.05 | 0.31 |
| Q11 | crystal_purity | 0.98 | 0.92 | 1 |
| Q11 | crystal_size | 0.19 | 0.1 | 0.3 |
| Q11 | crystal_yield | 0.3 | 0.19 | 0.41 |
| Q12 | crystal_fines_fraction | 0.27 | 0.11 | 0.47 |
| Q12 | crystal_purity | 0.98 | 0.92 | 1 |
| Q12 | crystal_size | 0.16 | 0.08 | 0.27 |
| Q12 | crystal_yield | 0.35 | 0.24 | 0.47 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are extrapolations from the sealed campaign, not new experimental results. For the solvent pair, S1 is predicted to outperform S3 in recovery and morphology, consistent with the observed S1/S3 ordering, although catalyst C1 and the much longer cooling history make the transfer uncertain. More seed is expected to suppress secondary nucleation and improve size and fines (Q04 versus Q03), with only a modest yield effect. Slow distributed cooling should strongly outperform a rapid crash in morphology (Q05 versus Q06), while total recovery may remain similar after the long common residence time. The reheating cycle is interpreted as partial dissolution/ripening, giving larger particles and fewer fines but some recovery loss (Q08 versus Q07); rapid renucleation on recooling is an unresolved alternative. Continuing growth at 292 K should increase deposited target, size particles, and reduce fines (Q10 versus Q09), but Q10 remains close to the fines threshold. Doubling upstream loading should increase normalized recovery while increasing supersaturation and fines (Q12 versus Q11), analogous to the campaign's concentration-dependent recovery/quality tradeoff. Intervals are deliberately broad because these recipes use C1, 385 K reaction conditions, very long cooling histories, and reagent/seed scales not directly replicated in the campaign; uncertainty includes model transfer and process-history effects, not final-assay noise alone.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C0 was the best practical catalyst in the screened campaign.** Batch 1 with C0/S0 gave crystal yield 0.518, versus 0.318, 0.200, and 0.312 for C1–C3 in batches 2–4. This supports the operational choice of C0. The exact catalyst effect remains partly confounded because batch 1 did not share the later crystallization history.
- **S2 provided the best recovery–morphology balance among the tested solvents.** With C0 and staged cooling, batch 6 gave yield 0.443, purity 1.000, and fines 0.257. Batch 5/S1 was compliant but lower-yielding (0.341), while batch 7/S3 gave lower yield (0.290) and fines near the limit (0.505). Batch 8 showed that a 1:1 S0/S2 mixture was also compliant, but not clearly better than S2.
- **There was a concentration-dependent recovery/quality boundary.** In S2, batch 6 at nominal 0.5 mol/L gave yield 0.443 and fines 0.257; batch 11 at 1.0 mol/L gave yield 0.488 and fines 0.280; batch 12 at 2.0 mol/L gave higher yield, 0.518, but fines 1.000. These are direct observations supporting a recovery–fines tradeoff.
- **The selected process was constraint-compliant.** Batch 11 directly measured purity 0.997 and fines 0.280 at crystal yield 0.488.

### Supported as interpretations, but not isolated causally
- **Slow staged cooling and seeding favored growth over secondary nucleation.** Later S2 batches had much lower fines than batch 1’s less controlled S0 history, but solvent, concentration, and thermal history changed together. The population-balance interpretation is plausible rather than uniquely demonstrated.
- **Reaction and crystallization were coupled through solvent and concentration.** Reaction-stage yield and final crystal yield moved together in several batches, and the apparent downstream recovery was roughly 0.90–0.93 for batches 6, 11, and 12. That ratio is useful bookkeeping, not proof of a constant physical recovery factor.
- **The 350 K/3600 s reaction was preferable to 330 K/7200 s.** Batch 9 gave only 0.316 crystal yield and fines 0.502, below the performance of batches 6 and 11. Because time and temperature changed simultaneously, the result does not separately identify kinetic and degradation effects.

### Contradicted or narrowed
- **A general claim that slow cooling and seeding alone guarantee low fines was contradicted.** Batches 2–4 remained mediocre or noncompliant despite extended growth histories, showing that material identity and upstream product quality also mattered.
- **A simple “higher concentration is better” claim was contradicted by batch 12.** Recovery increased, but morphology failed completely.
- **Reheating as a universally effective ripening treatment was not supported.** Batch 3’s reheating cycle still produced yield 0.200 and fines 0.828. Because it used C2, this is not a clean contradiction for C0/S2 thermal cycling.

### Still untested
- Replication and between-batch variability.
- Intermediate S2 concentrations between 1.0 and 2.0 mol/L.
- Independent variation of reaction temperature and time.
- A controlled cooling-history comparison at fixed catalyst, solvent, concentration, and total residence time.
- Whether thermal cycling improves C0/S2 morphology.
- Whether the solvent effects arise primarily from reaction selectivity, solubility, nucleation kinetics, or impurity-mediated crystallization.

## 2. One additional experiment

I would test **0.04 mol reagent in 0.030 L S2**—nominally 1.33 mol/L—with C0, using exactly batch 11’s catalyst charge, 350 K/3600 s reaction, seed charge, staged cooling, agitation, filtration, and assay sequence. I would include the same pre-filtration particle-size measurement.

This experiment would probe two competing explanations:

1. **A smooth concentration tradeoff:** increasing concentration gradually raises recovery and gradually worsens fines.
2. **A nonlinear nucleation threshold:** morphology remains similar to batch 11 until a critical supersaturation is crossed, after which fines rise sharply, as in batch 12.

Expected outcomes:
- **Yield around 0.49–0.52 with fines still below 0.50** would support an exploitable intermediate window and a threshold above 1.33 mol/L.
- **Fines near 1.0 despite intermediate loading** would place the threshold between 1.0 and 1.33 mol/L.
- **Intermediate fines with intermediate recovery** would support a smoother tradeoff.
- **Performance resembling neither neighboring batch** would strengthen concerns about batch variability or an unrecognized history-dependent effect.

A single intermediate experiment cannot by itself distinguish deterministic nonlinearity from random batch variation; replication would still be required.

## 3. Least effectively used evidence and least reliable prediction

The account used the **pre-filtration particle-size measurements** least effectively. For example, batch 6 measured fines 0.218 before filtration and 0.257 in the final assay; batch 11 measured 0.291 before filtration and 0.280 finally. I treated these mainly as confirmation of the same compliance classification. A stronger analysis would have used the paired readings to discuss measurement disagreement, whether filtration changed the representative slurry, and how confidently near-threshold batches such as batch 9 could be classified.

The least reliable held-out prediction is **Q09**, the batch filtered only 60 seconds after cooling to 292 K. No campaign batch sampled that immediate post-seeding regime. Its predicted particles-present status depends heavily on whether introduced seed alone counts in the particle population, while seed-excluded target yield may still be nearly zero. Crystal purity, normalized size, and fines at that moment were therefore extrapolated far beyond the observed growth histories. Q08’s thermal-cycle prediction is also weak because batch 3 was a confounded analogue, but Q09 is the largest temporal and state-regime extrapolation.
