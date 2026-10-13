# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The materials are anonymous benchmark identities, so the evidence supports process-level mechanisms, not claims about real molecular structures.

### Observed material effects

**Solvent identity was the dominant crystallization variable.** With catalyst C0, 0.040 mol reagent, 0.080 L solvent, 360 K reaction, 0.005 g seed, staged cooling, and a cold hold, changing only the solvent produced large differences:

- Batch 2, S0: crystal recovery 0.431, purity 0.977, fines 0.709.
- Batch 3, S1: recovery 0.445, purity 0.987, fines 0.393.
- Batch 4, S2: recovery 0.476, purity 1.000, fines 0.281.
- Batch 5, S3: recovery 0.341, purity 0.968, fines 0.680.

These differences greatly exceed the stated final-assay noise (approximately 0.010 for recovery and 0.018 for fines). I interpret S2 as providing a favorable solubility/nucleation/growth balance: sufficient supersaturation for recovery, but less secondary nucleation or better growth of existing particles. S1 was also feasible, while S0 and S3 generated excessive numbers of sub-20-µm particles. An alternative explanation is solvent-dependent agglomeration or attrition rather than primary nucleation; the measurements do not distinguish these mechanisms.

**Catalyst identity affected both reaction composition and downstream recovery.** Under the common S2, 250 K, 0.05 g seed crystallization recipe, C0 gave recoveries of 0.537 and 0.523 in batches 8 and 12. C1, C2, and C3 gave 0.524, 0.448, and 0.474 in batches 9–11. Their reaction yields were about 0.573, 0.500, and 0.522, versus 0.578 and 0.577 for C0. This supports coupling through the amount and composition of target entering crystallization. C0 versus C1 is a modest difference, whereas C2 and C3 were clearly less favorable in this tested process. Catalyst cost and molecular chemistry cannot be interpreted because the identities are opaque.

### Reaction–crystallization coupling

The reported crystallization recovery was

R_cryst = (seed-excluded recovered target product)/(target product present before separation).

It is therefore not an overall yield from charged reagent. A useful approximate decomposition is

Y_isolated ≈ Y_reaction × R_cryst × η_transfer,

where η_transfer represents unmeasured transfer and handling losses. Ignoring such losses, batch 8 corresponds to roughly 0.578 × 0.537 ≈ 0.31 target per charged-reactant basis, while batch 12 gives about 0.30.

For a simplified equilibrium-limited crystallization, recovery should rise approximately as

R_cryst ≈ 1 − C*(T_final)/C_initial,

subject to kinetic limitations, where C* is target solubility. Thus better reaction yield can increase the target concentration and supersaturation, while reaction byproducts can alter nucleation, growth, occlusion, or effective solubility. The data are consistent with this coupling but do not establish which contribution dominates. Notably, all optimized S2 batches retained high crystal purity, about 0.98–1.00, despite reaction selectivities near 0.54–0.59, indicating that crystallization rejected much of the reaction impurity.

### Process-history dependence

The successful history used reaction at 360 K for 3,600 s with 600 rpm stirring, seeding while hot, then staged cooling. In batch 8 the stages were 320 K for 7,200 s, 285 K for 10,000 s, and 250 K for 14,400 s, followed by a 14,400 s hold at 200 rpm before filtration.

A useful conceptual relation is

supersaturation S = C/C*(T),

with nucleation increasing strongly at high S, while growth occurs over a broader moderate-S range. Staged cooling and a long low-speed hold plausibly limit abrupt supersaturation, allow deposited mass to grow on existing particles, and reduce attrition. However, the initial direct-versus-staged comparison is confounded: batch 1 used S0, 0.05 g seed, and direct cooling to 278 K, while batch 2 used 0.005 g seed, staged cooling, and a hold. Both had fines near 0.70, although batch 2 had a somewhat larger normalized size. Consequently, thermal staging alone was not shown to rescue an unfavorable solvent.

Within S2, lowering the final temperature was associated with greater recovery without a fines penalty:

- Batch 4, 278 K: recovery 0.476, fines 0.281.
- Batch 6, 260 K: recovery 0.515, fines 0.267.
- Batch 7, 250 K: recovery 0.532, fines 0.219.

This is consistent with reduced terminal solubility. Intermediate stage temperatures and durations also changed, so the series is not a pure final-temperature experiment. No temperature below 250 K was tested, and the observed favorable trend should not be extrapolated indefinitely; deeper or faster cooling could eventually cause excessive nucleation, impurity trapping, or handling problems.

### Seed loading and particle quality

At 250 K in S2, increasing seed from 0.005 g in batch 7 to 0.05 g in batch 8 changed recovery from 0.532 to 0.537 and fines from 0.219 to 0.228. Those differences are comparable to assay and process variability, so no strong seed-dose effect is established. The higher seed charge may provide more growth surface and reliable nucleation, but it might also create more particle counts or dilute seed-excluded productivity. Both mechanisms remain plausible.

The optimized products met the fines constraint with substantial margin but had only moderate number-weighted median size: normalized crystal-size values of 0.122 in batch 8 and 0.114 in batch 12 correspond to d50 values of roughly 31 and 28 µm. Thus the process suppressed the sub-20-µm population effectively without producing exceptionally large crystals.

### Revisions and uncertainty

The initial hypothesis emphasized moderate seeding, slow cooling, and a cold hold. Batch 1 demonstrated good recovery and purity but failed the fines requirement badly, leading to a revision: solvent-dependent morphology became the principal hypothesis. The solvent screen identified S2, after which deeper cooling was prioritized to raise recovery. A late catalyst screen then showed that upstream reaction performance also influenced downstream recovery.

Batch 8 had the highest observed compliant recovery: 0.537, with purity 0.981 and fines 0.228. Batch 12 repeated the same recipe and returned recovery 0.523, purity 0.996, and fines 0.243. The 0.014 recovery difference and 0.015 fines difference are comparable to combined measurement uncertainty and process variation. The replicate therefore supports recipe feasibility and robust constraint satisfaction, but it also warns against treating the single highest result as a deterministic process value.

No unresolved purity–recovery tradeoff appeared within the tested S2 window: deeper cooling increased observed recovery while purity remained above 0.98 and fines improved. Nevertheless, that conclusion is local. More aggressive cooling, different concentrations, or scale-up could produce impurity occlusion or fines. Solvent mixtures, altered concentration, agitation profiles, seed-size distributions, washing/resuspension, atmosphere, catalyst loading, and reaction-temperature optimization were not tested. These remain credible alternatives rather than excluded mechanisms.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.43 |
| Q01 | crystal_purity | 0.98 | 0.94 | 1 |
| Q01 | crystal_size | 0.16 | 0.09 | 0.24 |
| Q01 | crystal_yield | 0.34 | 0.24 | 0.44 |
| Q02 | crystal_fines_fraction | 0.63 | 0.48 | 0.77 |
| Q02 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q02 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q02 | crystal_yield | 0.25 | 0.15 | 0.36 |
| Q03 | crystal_fines_fraction | 0.56 | 0.41 | 0.7 |
| Q03 | crystal_purity | 0.97 | 0.92 | 1 |
| Q03 | crystal_size | 0.15 | 0.07 | 0.24 |
| Q03 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q04 | crystal_fines_fraction | 0.48 | 0.34 | 0.62 |
| Q04 | crystal_purity | 0.97 | 0.92 | 1 |
| Q04 | crystal_size | 0.13 | 0.06 | 0.21 |
| Q04 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q05 | crystal_fines_fraction | 0.46 | 0.32 | 0.6 |
| Q05 | crystal_purity | 0.97 | 0.92 | 1 |
| Q05 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q05 | crystal_yield | 0.31 | 0.21 | 0.42 |
| Q06 | crystal_fines_fraction | 0.6 | 0.45 | 0.74 |
| Q06 | crystal_purity | 0.96 | 0.9 | 1 |
| Q06 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q06 | crystal_yield | 0.31 | 0.2 | 0.42 |
| Q07 | crystal_fines_fraction | 0.43 | 0.29 | 0.57 |
| Q07 | crystal_purity | 0.97 | 0.92 | 1 |
| Q07 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q07 | crystal_yield | 0.32 | 0.22 | 0.43 |
| Q08 | crystal_fines_fraction | 0.57 | 0.4 | 0.73 |
| Q08 | crystal_purity | 0.96 | 0.89 | 1 |
| Q08 | crystal_size | 0.1 | 0.04 | 0.18 |
| Q08 | crystal_yield | 0.24 | 0.13 | 0.36 |
| Q09 | crystal_fines_fraction | 0.88 | 0.72 | 0.98 |
| Q09 | crystal_purity | 0.94 | 0.84 | 1 |
| Q09 | crystal_size | 0.025 | 0.005 | 0.06 |
| Q09 | crystal_yield | 0.008 | 0 | 0.035 |
| Q10 | crystal_fines_fraction | 0.74 | 0.57 | 0.88 |
| Q10 | crystal_purity | 0.96 | 0.89 | 1 |
| Q10 | crystal_size | 0.05 | 0.015 | 0.11 |
| Q10 | crystal_yield | 0.1 | 0.04 | 0.19 |
| Q11 | crystal_fines_fraction | 0.45 | 0.31 | 0.59 |
| Q11 | crystal_purity | 0.97 | 0.92 | 1 |
| Q11 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q11 | crystal_yield | 0.32 | 0.22 | 0.43 |
| Q12 | crystal_fines_fraction | 0.54 | 0.39 | 0.68 |
| Q12 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q12 | crystal_size | 0.11 | 0.05 | 0.19 |
| Q12 | crystal_yield | 0.43 | 0.32 | 0.54 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and a crystallization step, so particles are expected. Q01–Q02 applies the observed solvent ranking: S1 should give fewer fines, larger particles and higher recovery than S3. Q03–Q04 assigns the larger seed charge a modest kinetic-recovery and fines-control benefit, while allowing the low-seed case a somewhat larger median among surviving particles. Q05–Q06 predicts that a gradual ramp suppresses burst nucleation relative to an initial temperature crash; the long cold aging in Q06 partly narrows, but does not erase, that history effect. Q07–Q08 treats the 315 K excursion as substantial partial dissolution followed by only a one-hour recool, lowering recovery and reintroducing fines rather than providing a fully controlled anneal. Q09–Q10 predicts very little seed-excluded recovery after the 60-second step, with a two-hour hold improving growth but remaining fines-rich. Q11–Q12 predicts that doubled reagent concentration increases supersaturation and recovery but also increases secondary nucleation and impurity-occlusion risk. Intervals are deliberately broad because these recipes extrapolate from the campaign in scale, catalyst loading, reaction temperature, quench use, and exceptionally long cooling histories; estimates near the 0.50 fines boundary therefore have uncertain feasibility.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Solvent identity strongly affected crystallization.** Batches 2–5 used closely matched C0 reaction, seed, cooling, and hold conditions while changing solvent. S2 in batch 4 gave recovery 0.476 and fines 0.281; S1 in batch 3 gave 0.445 and 0.393; S0 in batch 2 gave 0.431 and 0.709; S3 in batch 5 gave 0.341 and 0.680. Thus the ranking of S2/S1 over S0/S3 for fines is directly observed and substantially larger than assay noise.

- **S2 was the best tested solvent under the campaign conditions.** Batches 4, 6–8, and 12 all used S2 and remained well within both quality constraints, with recovery 0.476–0.537, purity 0.981–1.000, and fines 0.219–0.281. This is direct evidence for local robustness, not proof that S2 is optimal under every concentration or temperature history.

- **Lower final temperature was associated with higher recovery in S2.** Batch 4 at 278 K gave 0.476 recovery, batch 6 at 260 K gave 0.515, and batch 7 at 250 K gave 0.532. Fines did not worsen. The trend is observed, but its attribution solely to final temperature remains interpretive because intermediate temperatures and durations also changed.

- **Catalyst choice affected the combined reaction–crystallization outcome.** Under the common S2/250 K/0.05 g seed process, C0 gave recoveries of 0.537 and 0.523 in batches 8 and 12, while C1, C2, and C3 gave 0.524, 0.448, and 0.474 in batches 9–11. C2 and C3 were clearly inferior in this scope. C0 versus C1 remains only weakly resolved because their difference is comparable to observed run-to-run variation.

- **The selected recipe was reproducibly feasible.** Batches 8 and 12 used the same recipe and both passed comfortably: purity 0.981/0.996 and fines 0.228/0.243. Their recovery difference, 0.537 versus 0.523, shows that the highest single value should not be treated as an exact deterministic expectation.

### Challenged or not demonstrated

- **A general claim that slow staged cooling alone prevents fines is challenged by S0.** Batch 1 used direct cooling and had fines 0.705; batch 2 used staged cooling plus a long hold and still had fines 0.709. Because seed dose and other details differed, this does not cleanly contradict a cooling-rate effect, but it shows that staging could not overcome the unfavorable S0 morphology in those runs.

- **A strong beneficial seed-dose effect was not demonstrated.** Raising seed from 0.005 g in batch 7 to 0.05 g in batch 8 changed recovery only from 0.532 to 0.537 and fines from 0.219 to 0.228. Batch 12 then gave 0.523 and 0.243 at the high seed dose. These differences are too small and variable to support a firm seed mechanism; the slight increase in fines also does not support a simple “more seed always reduces fines” rule.

- **The proposed solubility/nucleation explanation is interpretation, not direct molecular evidence.** The S2 results are consistent with a favorable solubility curve, reduced secondary nucleation, or better growth, but solvent-dependent agglomeration, breakage, or filtration retention could produce similar final measurements. No mother-liquor concentration, nucleation-rate, or time-resolved CSD data were used to distinguish them.

- **Reaction–crystallization coupling is plausible but incompletely isolated.** Catalyst comparisons show that reaction yield and crystal recovery moved broadly together, especially for C2 and C3, but catalyst identity may also directly change impurity-mediated nucleation or solubility. The approximate relation `overall isolated yield ≈ reaction yield × crystallization recovery` is useful bookkeeping, not a fitted mechanistic law.

- **The absence of a purity/recovery tradeoff is only local.** In S2, deeper cooling increased observed recovery while purity stayed above 0.98. Temperatures below 250 K, faster cooling at high concentration, solvent mixtures, washing, and scale-up were not tested, so impurity occlusion at more aggressive conditions remains unresolved.

## 2. One additional experiment

I would repeat the batch-8 chemistry exactly—S2, C0, the same charge, 360 K reaction, and 0.05 g seed—but replace the 320→285→250 K staged cooling with a rapid drop to 250 K, then age at 250 K so that the total post-seeding time matches batch 8. I would obtain non-destructive particle-size measurements immediately after reaching 250 K and again before filtration.

This would distinguish two main explanations:

1. **Cooling-history-controlled nucleation:** the slow ramp limits the supersaturation peak and secondary nucleation.
2. **Solvent/end-point-controlled morphology:** S2, the 250 K endpoint, and prolonged aging determine the final CSD largely independently of the path.

Expected outcomes would differ as follows:

- If cooling history is important, the rapid-drop batch should initially show more fines and smaller particles. Recovery could be similar or slightly higher, because supersaturation is generated sooner. Persistence of the fines after matched total aging would strongly support path dependence.
- If endpoint and aging dominate, the initially different CSD should converge toward the batch-8/12 range—roughly 0.22–0.24 fines and normalized size around 0.11–0.12—while recovery approaches about 0.52–0.54.
- If rapid cooling initially creates fines but prolonged cold aging removes them, the two particle measurements would support Ostwald ripening or agglomeration as the controlling late-stage mechanism.
- If recovery or purity changes substantially despite a similar final CSD, that would implicate filtration retention, impurity occlusion, or path-dependent solid form rather than nucleation alone.

This is more discriminating than another endpoint-only replicate because it isolates the major unresolved process-history claim while retaining batches 8 and 12 as matched references.

## 3. Least-used observation and least-reliable prediction

The account used the **batch-1 pre-crystallization HPLC observation** least effectively. Before crystallization it measured conversion 1.000, yield about 0.585, selectivity about 0.592, and byproduct signal about 0.269. The batch-1 final assay later gave very similar reaction metrics, alongside crystal recovery 0.432. That agreement could have been used more explicitly to show that the downstream operations did not materially change the inferred reaction composition and to anchor the separation between reaction yield and crystallization-stage recovery. Its limitation is that it was the only upstream HPLC measurement and came from the nonpreferred S0 recipe, so it cannot establish coupling trends across catalysts or solvents. The intermediate particle-size measurements were also underexploited because the report relied primarily on final-assay CSD values.

The **Q08 held-out prediction is least reliable**. It contains a long slow crystallization followed by reheating to 315 K and then recooling to 278.15 K in only one hour. No campaign batch tested reheating an established crystal population. My sealed prediction assumed substantial dissolution followed by rapid renucleation, producing lower recovery and more fines than Q07. The opposite is mechanistically credible: partial dissolution could selectively remove fines and promote regrowth of larger survivors, improving the CSD. The outcome depends on an unmeasured S0 solubility curve, dissolution kinetics, whether all or only small crystals disappear at 315 K, and the nucleation response during recooling. Consequently, even the direction of the Q07–Q08 difference is less secure than the solvent and endpoint-temperature comparisons.
