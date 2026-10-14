# C-W05-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Coupled reaction–crystallization picture

The measured seed-excluded crystal recovery is

**Y_crystal = n(target product in recovered solid, excluding seed) / n(initial limiting reagent).**

A useful approximate decomposition is

**Y_crystal ≈ Y_reaction × F_capture**,

where `Y_reaction` is the chemically produced target yield and `F_capture` is the fraction subsequently crystallized and retained. This is an interpretive mass-balance relation rather than a fitted kinetic law; assay noise and impurities prevent exact factorization.

For the S2 sequence, the apparent capture ratios `Y_crystal/Y_reaction` increased from about 0.801 in batch 5 to 0.866, 0.879, 0.910, and 0.916 in batches 9–12. Thus, most of the later recovery gain came from improved downstream capture rather than a large increase in reaction yield, which remained near 0.59–0.60.

### 2. Material effects

**Observation:** Solvent identity had the clearest effect on particle quality. Under the common C0, 360 K/1800 s reaction and seeded slow-cooling framework:

- Batch 4, S1: crystal yield 0.531, purity 1.000, fines 0.536.
- Batch 5, S2: yield 0.470, purity 0.976, fines 0.451.
- Batch 6, S3: yield 0.389, purity 0.989, fines 0.798.
- S0 batches 1 and 3 had fines of 0.974 and 0.976, respectively.

**Interpretation:** The anonymous solvents probably alter product solubility, supersaturation, interfacial free energy, nucleation rate, and/or crystal-growth anisotropy. S1 supported high chemical and crystal recovery but sat near the fines limit. S2 provided a more favorable nucleation/growth balance and became the robust feasible solvent. S0 and S3 promoted populations dominated numerically by sub-20 µm particles.

A conventional framework is `S = C/C*(T, solvent)`, with nucleation increasing steeply with supersaturation while growth often varies more gradually. The data establish solvent-dependent behavior but do not identify which microscopic property—solubility, interfacial energy, viscosity, aggregation, or polymorph selection—is responsible.

**Catalyst evidence was weaker.** At 370 K for 3600 s in S0, the HPLC snapshot for C0 in batch 1 gave conversion 1.000, target yield 0.627, and selectivity 0.633; C1 in batch 2 gave 0.985, 0.556, and 0.586. This suggests C0 was more productive in that window, but the comparison was not replicated and downstream histories differed. Catalysts C2 and C3 were not tested, so catalyst optimality remains unproven.

### 3. Reaction conditions and their coupling to crystallization

C0 at 360 K for 1800 s generally produced high conversion with reaction yield around 0.59–0.64. Raising severity to 370 K for 3600 s did not clearly improve the complete process: batch 1 showed crystal yield 0.494 with degradation warning 0.125 and excessive fines. Batch 3 at the milder reaction condition still had poor recovery and morphology in S0, showing that crystallization—not conversion alone—was limiting there.

Reaction selectivity sets the maximum target inventory available to crystallize and also changes impurity loading. Those impurities may modify solubility or inhibit/promote nucleation. S1 illustrates this coupling: batch 4 had strong reaction yield/selectivity (0.642/0.656) and high crystal recovery, but fines marginally exceeded specification. S2 sacrificed some chemical yield but enabled acceptable particle populations and ultimately higher feasible recovery after colder crystallization.

Purity was not the main limiting response in the refined region: batches 5 and 9–12 all exceeded 0.80 purity by a wide margin. The active optimization constraint was fines.

### 4. Process-history dependence

The standard refined history was: react at 360 K for 1800 s; cool to 325 K over 3600 s; add 0.05 g seed; cool over 14400 s to the endpoint; hold for 14400 s at low agitation; then filter.

**Seeding and slow cooling were not universally sufficient.** S0 remained at roughly 0.97–0.98 fines in batches 1 and 3. Batch 2 used a modified, repeated-seed history but still produced fines near 1.0; because several conditions changed and the effective dose history was not independently verified, it is not clean seed-dose evidence.

**S1 history changes did not solve the boundary problem.** The base 290 K process in batch 4 gave fines 0.536. A mild 305→290 K thermal cycle in batch 7 gave 0.528, and a warmer 295 K endpoint in batch 8 gave 0.527. Their yields stayed near 0.532–0.535. These differences are small relative to single-run uncertainty, so neither intervention demonstrated a reliable benefit.

**S2 showed the strongest endpoint dependence.** With otherwise similar histories:

- Batch 5, 290 K: yield 0.470; fines 0.451.
- Batch 9, 280 K: yield 0.509; fines 0.404.
- Batch 10, 270 K: yield 0.529; fines 0.398.
- Batch 11, 250 K: yield 0.547; fines 0.372.

Colder endpoints increased observed capture and, unexpectedly, did not increase the number fraction of fines. This contradicts a simplistic claim that greater supersaturation must produce more fines. Plausible explanations include preferential growth on existing crystals, rapid depletion of solution concentration, aggregation, dissolution/recrystallization during the long hold, or solvent-specific suppression of secondary nucleation. Particle imaging is number-weighted, so the fines response cannot be interpreted as a fines mass fraction.

The endpoint comparisons also used the same 14400 s cooling duration, meaning the average cooling rate actually increased as the endpoint fell. The favorable result therefore cannot be attributed simply to slower cooling.

### 5. Recommended process and unresolved tradeoff

The sealed recommendation remains **batch 12**: C0, S2, 0.04 mol reagent in 0.06 L solvent, 360 K for 1800 s, pre-cool to 325 K, add 0.05 g seed, cool to 250 K over 14400 s, hold 14400 s at 100 rpm, and filter. Its final assay gave:

- crystal yield: **0.554**
- crystal purity: **0.997**
- fines below 20 µm: **0.414**
- normalized crystal size: **0.102**
- CSD quality: **0.701**

Compared with batch 11 at 0.08 L solvent, batch 12 increased nominal concentration from 0.50 to about 0.67 mol/L and showed slightly higher recovery, purity, and size, but fines rose from 0.372 to 0.414. I interpret the concentration increase as improving supersaturation and capture, while consuming part of the fines safety margin. This is a single, confounded comparison rather than a validated concentration law.

The unresolved quality/recovery tradeoff is therefore between batch 12’s highest observed feasible recovery and batch 11’s larger fines margin. Both met the stated constraints, but no replicate series quantified process variance. Batch 12’s fines margin is still substantial relative to the 0.50 limit, although assay noise, batch variability, scale-up mixing, and filtration effects remain uncertain.

### 6. Revisions and uncertainty

The initial working view emphasized catalyst selection, seeding, and slow cooling. The campaign revised that view: solvent identity was the dominant observed morphology factor, while nominal seeding and generic slow cooling did not rescue unfavorable solvents. A second expectation—that warmer endpoints or thermal cycling would reduce S1 fines—was not supported by batches 7 and 8. Conversely, the S2 data revised the expectation that colder operation would necessarily worsen fines; batches 9–11 showed improving recovery and lower observed fines.

These conclusions are empirical and local to anonymous benchmark materials. Most settings were tested once; endpoint and concentration effects were sequential rather than randomized; final-assay noise and latent process variability remain; no polymorph identity, solubility curve, induction time, or growth-rate measurement was available. Catalyst C2/C3, alternative seed size distributions, intermediate concentrations, longer ripening, and controlled replicate studies remain untested alternatives.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.34 | 0.2 | 0.5 |
| Q01 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q01 | crystal_size | 0.18 | 0.12 | 0.25 |
| Q01 | crystal_yield | 0.5 | 0.39 | 0.6 |
| Q02 | crystal_fines_fraction | 0.69 | 0.5 | 0.86 |
| Q02 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q02 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q02 | crystal_yield | 0.39 | 0.28 | 0.5 |
| Q03 | crystal_fines_fraction | 0.8 | 0.62 | 0.94 |
| Q03 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q03 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q03 | crystal_yield | 0.45 | 0.34 | 0.55 |
| Q04 | crystal_fines_fraction | 0.46 | 0.29 | 0.65 |
| Q04 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q04 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q04 | crystal_yield | 0.46 | 0.35 | 0.56 |
| Q05 | crystal_fines_fraction | 0.42 | 0.26 | 0.6 |
| Q05 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q05 | crystal_size | 0.15 | 0.09 | 0.22 |
| Q05 | crystal_yield | 0.47 | 0.36 | 0.57 |
| Q06 | crystal_fines_fraction | 0.67 | 0.48 | 0.84 |
| Q06 | crystal_purity | 0.96 | 0.89 | 0.99 |
| Q06 | crystal_size | 0.085 | 0.04 | 0.15 |
| Q06 | crystal_yield | 0.48 | 0.37 | 0.58 |
| Q07 | crystal_fines_fraction | 0.4 | 0.24 | 0.58 |
| Q07 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q07 | crystal_size | 0.16 | 0.1 | 0.23 |
| Q07 | crystal_yield | 0.48 | 0.37 | 0.58 |
| Q08 | crystal_fines_fraction | 0.55 | 0.35 | 0.74 |
| Q08 | crystal_purity | 0.96 | 0.88 | 0.99 |
| Q08 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q08 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q09 | crystal_fines_fraction | 0.87 | 0.69 | 0.97 |
| Q09 | crystal_purity | 0.98 | 0.9 | 1 |
| Q09 | crystal_size | 0.06 | 0.025 | 0.11 |
| Q09 | crystal_yield | 0.02 | 0.003 | 0.07 |
| Q10 | crystal_fines_fraction | 0.66 | 0.45 | 0.84 |
| Q10 | crystal_purity | 0.97 | 0.89 | 0.995 |
| Q10 | crystal_size | 0.095 | 0.045 | 0.16 |
| Q10 | crystal_yield | 0.18 | 0.08 | 0.31 |
| Q11 | crystal_fines_fraction | 0.41 | 0.25 | 0.59 |
| Q11 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q11 | crystal_size | 0.16 | 0.1 | 0.23 |
| Q11 | crystal_yield | 0.48 | 0.37 | 0.58 |
| Q12 | crystal_fines_fraction | 0.57 | 0.38 | 0.76 |
| Q12 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q12 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q12 | crystal_yield | 0.44 | 0.32 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: the campaign showed much better morphology and recovery with S1 than S3, so S1 is predicted feasible while S3 remains fines-limited. Q03–Q04: increasing seed from 0.001 to 0.045 g should mainly suppress secondary nucleation and enlarge particles, with little equilibrium-yield effect. Q05–Q06: gradual cooling should favor seed growth; an immediate temperature crash should create a persistent fine population even after a long hold. Q07–Q08: the long gradual history should be favorable, whereas reheating to 315 K followed by only a short recool may lose recovery and regenerate fines; this is especially uncertain because the tested milder thermal cycle had only a small effect. Q09–Q10: seed ensures particles in both, but 60 s permits almost no seed-excluded recovery; a 7200 s continuation raises recovery and size but is not expected to fully resolve fines. Q11–Q12: doubling reagent at fixed solvent and catalyst raises supersaturation but halves the catalyst-to-reagent ratio, so normalized recovery and purity may fall while fines rise. Intervals are deliberately broad because these recipes extrapolate to C1/S0, much lower scale and concentration, exceptionally long staged cooling, and reaction conditions not directly replicated in the campaign.

## K2

## 1. Status of the main claims

**Supported by direct observations:**

- **Solvent strongly affected crystal morphology.** Under closely related C0/360 K recipes, batch 4 (S1) gave yield 0.531 and fines 0.536, batch 5 (S2) gave 0.470 and 0.451, and batch 6 (S3) gave 0.389 and 0.798. S0 also gave very high fines in batches 1 and 3 (0.974 and 0.976). Interpreting this as solvent-dependent solubility, interfacial energy, or growth kinetics is plausible but not directly measured.
- **S2 was the most robust feasible solvent in the tested region.** Batches 5 and 9–12 all met the purity and fines constraints.
- **Within the S2 series, colder endpoints were associated with greater recovery and fewer fines.** From batches 5, 9, 10, and 11, endpoints of 290, 280, 270, and 250 K corresponded to yields of 0.470, 0.509, 0.529, and 0.547 and fines of 0.451, 0.404, 0.398, and 0.372. This is an observed sequence, not a validated causal law: the batches were unreplicated and process variability could contribute.
- **Purity was not the active limitation in the refined S2 region.** Batches 5 and 9–12 all had purity well above 0.80; fines controlled feasibility.

**Contradicted or weakened:**

- **Generic seeding plus slow cooling is sufficient to control fines** was contradicted by S0 batches 1 and 3, which remained almost entirely fine by number. Batch 2’s altered seed history also failed, although it was too confounded to establish a quantitative seed-dose effect.
- **A warmer endpoint or mild thermal cycle would make S1 reliably feasible** was not supported. Batch 4 gave fines 0.536, the 305→290 K cycle in batch 7 gave 0.528, and the 295 K endpoint in batch 8 gave 0.527.
- **Colder operation must increase fines through greater supersaturation** was contradicted as a general description of the tested S2 system: batches 9–11 showed the opposite association. The microscopic reason remains interpretive.

**Still untested or only tentative:**

- Catalyst optimality is unresolved. C0 outperformed C1 in the limited S0 comparison of batches 1 and 2, but their histories differed, and C2/C3 were never tested.
- The suggested mechanisms—growth on seeds, suppression of secondary nucleation, aggregation, ripening, or solvent-dependent polymorphism—were not directly characterized.
- The concentration claim from batch 12 versus batch 11 is tentative. Batch 12 used 0.06 L rather than 0.08 L and showed slightly higher yield (0.554 versus 0.547), but this was a single comparison.
- The approximate decomposition `crystal yield ≈ reaction yield × capture fraction` is a useful interpretation, not an independently verified kinetic model.

## 2. One additional experiment

I would run the missing factorial condition: repeat the batch-12 chemistry—C0, S2, 0.04 mol reagent in 0.06 L solvent, 360 K for 1800 s, pre-cool to 325 K, add 0.05 g seed—but cool only to **290 K** over 14400 s, hold 14400 s, filter, and assay.

Together with batch 5 (0.08 L/290 K), batch 11 (0.08 L/250 K), and batch 12 (0.06 L/250 K), this would complete a small 2×2 concentration–endpoint comparison.

- If **higher concentration principally caused batch 12’s recovery gain**, the new 0.06 L/290 K batch should outperform batch 5 and approach batch 12, probably with some fines penalty.
- If **the 250 K endpoint principally caused the gain**, the new batch should remain near batch 5 in recovery, while batches 11 and 12 remain higher.
- If there is a **concentration–temperature interaction**, the concentrated 290 K condition could show disproportionate fines or fail to gain recovery, indicating that deep cooling is needed to capture product at the higher loading.

One run would still not quantify repeatability, but it would be more discriminating than another isolated optimization.

## 3. Least effectively used observation and least reliable prediction

The account used the paired particle-size and final-assay readings least effectively. For example, batch 4 changed from particle-measurement fines 0.501 to final-assay fines 0.536; batches 7 and 8 moved from about 0.542/0.539 to 0.528/0.527. These discrepancies could reflect instrument noise, sampling state, filtration, or process evolution. I treated the final assay as authoritative but did not explicitly model how this disagreement increases classification uncertainty near the 0.50 boundary.

The least reliable held-out prediction is **Q08**. It combines a long gradual history with reheating to 315 K and only a 3600 s recool in the poorly characterized C1/S0 system. The only campaign analogue, batch 7, used a milder 305 K excursion, a longer recool, and different catalyst/solvent conditions, and its effect was small. At 315 K, selective fines dissolution, loss of recovered mass, renewed nucleation during recooling, and possible habit changes could act in opposing directions. Consequently, even the sign of Q08’s fines and size changes relative to Q07 is less secure than for the other paired predictions.
