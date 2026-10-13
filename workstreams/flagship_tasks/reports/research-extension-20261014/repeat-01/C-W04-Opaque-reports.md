# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Observed material effects

The materials were anonymous benchmark identities, so the data support only empirical effects—not assignments such as polarity, acidity, or a named catalytic mechanism.

Reaction conversion was consistently high (approximately 0.985–1.00), but selectivity and byproduct formation depended on the catalyst/solvent pairing. For example, batches 1–2 using S0 gave final selectivities near 0.60–0.64, whereas repeated C1/S2 batches were generally near 0.45–0.49. Because the initial screen changed catalyst and solvent together, most individual catalyst and solvent effects remain confounded.

S2 was the most useful crystallization medium tested. Under staged cooling, S2 batches 4, 6, 8, and 10 combined high crystal purity (about 0.98–1.00) with fines fractions of about 0.18–0.28. S3 was feasible in batch 5 but was much closer to the fines limit (0.455). This could reflect differences in target solubility, supersaturation development, nucleation kinetics, or impurity rejection, but those alternatives were not independently measured.

### 2. Reaction–crystallization coupling

A useful bookkeeping relationship is

`overall recovered target yield ≈ reaction target yield × crystallization recovery`,

with reaction target yield approximately `conversion × selectivity` under a simple two-product interpretation. The reported crystal recovery was instead

`R_c = seed-excluded target recovered in crystals / target present before separation`.

Thus, crystal recovery does not measure overall production from the reagent charge. A condition can have favorable crystallization recovery while producing relatively little target upstream.

This distinction mattered here. C1/S2 gave only moderate reaction selectivity, but crystallization produced highly pure solids. Batch 8 had conversion near 1, reaction selectivity about 0.487, and reaction yield about 0.479, yet its isolated crystals had purity about 0.982 and stage recovery about 0.451. The crystallization therefore acted as a strong purification step, rejecting much of the byproduct into the liquid phases. Conversely, the higher reaction selectivity observed with S0 did not make batches 1–2 acceptable because their particle populations violated the fines constraint.

### 3. Supersaturation and process-history dependence

The principal mechanistic interpretation is based on supersaturation,

`σ = (C − C*) / C*`,

where `C*` is the temperature- and solvent-dependent solubility. Qualitatively, nucleation and growth may be represented as

`J ≈ k_n σ^b` and `G ≈ k_g σ^g`,

usually with nucleation becoming especially sensitive at high supersaturation. Rapidly generating a large `σ` should therefore cause a nucleation burst and many small particles, whereas staged cooling should keep the supersaturation peak lower and allow existing crystals to grow.

The observations strongly support this history effect. Direct cooling to 250 K gave the highest apparent recoveries in batches 1 and 2 (0.511 and 0.530), but both failed badly on fines (0.805 and 0.817). Batch 1 additionally warmed toward ambient during a subsequent ordinary wait, but batch 2 retained the same high-fines outcome without that warming, so the initial direct cooling remains the leading explanation.

Changing to staged 300→250 K cooling reduced fines substantially: batch 3 gave 0.331, batch 4 gave 0.274, and batch 5 gave 0.455. Later C1/S2 batches gave fines between approximately 0.23 and 0.28. This improvement came with lower recovery, generally 0.42–0.45. The observed quality/recovery tradeoff is therefore unresolved mechanistically: direct cooling recovered more target but generated unacceptable fines, while controlled cooling sacrificed some observed recovery to obtain a compliant particle population.

The gentler three-stage 320→285→250 K history in batch 10 reduced final-assay fines further to 0.178, but its recovery was 0.445 rather than exceeding batch 8. A prolonged additional 250 K stage in batch 11 did not improve recovery (0.435). These results suggest that final temperature alone did not determine the outcome; the path and time spent at intermediate supersaturation mattered. They do not establish whether the small recovery differences arose from genuine kinetic effects, mother-liquor retention, filtration behavior, or run-to-run variation.

### 4. Seeding and thermal cycling

At otherwise similar C1/S2 conditions, reducing seed from 0.05 g in batch 6 to 0.01 g in batch 8 numerically improved recovery from 0.440 to 0.451, reduced fines from 0.277 to 0.232, and increased normalized crystal size from 0.065 to 0.120. The unseeded batch 9 was intermediate in recovery (0.442) and fines (0.243), but had smaller crystals (0.071).

One interpretation is that excessive seed surface or seed-derived fragments distributed growth over too many sites, while a small seed charge provided nucleation control without overpopulating the slurry. However, each condition was tested only once, and the recovery differences are close to experimental uncertainty. Seed dose therefore remains a provisional rather than proven causal effect.

Batch 12 tested a 310 K reheat followed by recooling. Such a cycle could, in principle, dissolve fine crystals and promote Ostwald ripening. Instead, batch 12 gave lower recovery (0.417) and more fines (0.297) than batch 8, with a higher degradation-warning signal (about 0.208 versus 0.183). Possible explanations include loss of already recovered target to solution, renewed nucleation during recooling, or additional thermal degradation. A single cycle does not distinguish these alternatives.

### 5. Revisions and uncertainty

The initial expectation that a direct deep cool plus a cold hold would maximize recovery while seed suppressed fines was revised after batches 1–2: recovery was high, but fines were unacceptable. Staged cooling then became the central control strategy. S2/C1 and a low seed dose emerged during refinement rather than from the initial categorical screen.

The final-assay nominal standard deviations were about 0.01 for crystal recovery and purity, 0.018 for fines, and 0.025 for normalized size, in addition to process variability. Consequently, the recovery differences among batches 6, 8, 9, and 10 are modest. Batch 8 had the highest observed compliant recovery (0.451), but its advantage over batch 10 (0.445) is not compelling evidence of a reproducible mechanistic superiority. Batch 10 offered a much larger margin to the fines limit, while batch 8 offered the best observed recovery. This is the main unresolved quality/recovery tradeoff.

The sealed recommendation remains batch 8: C1/S2, 0.04 mol reagent, 0.08 L solvent, 0.005 mol catalyst, reaction at 360 K for 1 h, 0.01 g seed, then 300→250 K cooling for 4 h per stage, followed by filtration. Its observed crystal recovery was about 0.451, purity 0.982, and fines 0.232. Replication would be required to quantify robustness and establish whether its small recovery advantage over the gentler batch-10 profile is real.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.43 | 0.3 | 0.56 |
| Q01 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q01 | crystal_size | 0.09 | 0.045 | 0.15 |
| Q01 | crystal_yield | 0.3 | 0.21 | 0.39 |
| Q02 | crystal_fines_fraction | 0.56 | 0.42 | 0.7 |
| Q02 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q02 | crystal_size | 0.065 | 0.03 | 0.12 |
| Q02 | crystal_yield | 0.28 | 0.18 | 0.38 |
| Q03 | crystal_fines_fraction | 0.1 | 0.03 | 0.23 |
| Q03 | crystal_purity | 0.985 | 0.95 | 1 |
| Q03 | crystal_size | 0.22 | 0.13 | 0.33 |
| Q03 | crystal_yield | 0.32 | 0.23 | 0.41 |
| Q04 | crystal_fines_fraction | 0.47 | 0.34 | 0.61 |
| Q04 | crystal_purity | 0.982 | 0.94 | 1 |
| Q04 | crystal_size | 0.08 | 0.04 | 0.14 |
| Q04 | crystal_yield | 0.31 | 0.22 | 0.4 |
| Q05 | crystal_fines_fraction | 0.43 | 0.3 | 0.56 |
| Q05 | crystal_purity | 0.984 | 0.94 | 1 |
| Q05 | crystal_size | 0.09 | 0.045 | 0.15 |
| Q05 | crystal_yield | 0.32 | 0.23 | 0.41 |
| Q06 | crystal_fines_fraction | 0.73 | 0.59 | 0.85 |
| Q06 | crystal_purity | 0.975 | 0.92 | 1 |
| Q06 | crystal_size | 0.045 | 0.02 | 0.085 |
| Q06 | crystal_yield | 0.34 | 0.25 | 0.43 |
| Q07 | crystal_fines_fraction | 0.35 | 0.23 | 0.49 |
| Q07 | crystal_purity | 0.985 | 0.945 | 1 |
| Q07 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q07 | crystal_yield | 0.34 | 0.25 | 0.43 |
| Q08 | crystal_fines_fraction | 0.52 | 0.38 | 0.66 |
| Q08 | crystal_purity | 0.97 | 0.91 | 1 |
| Q08 | crystal_size | 0.075 | 0.035 | 0.135 |
| Q08 | crystal_yield | 0.27 | 0.17 | 0.37 |
| Q09 | crystal_fines_fraction | 0.9 | 0.76 | 0.98 |
| Q09 | crystal_purity | 0.99 | 0.94 | 1 |
| Q09 | crystal_size | 0.035 | 0.015 | 0.06 |
| Q09 | crystal_yield | 0.008 | 0.001 | 0.025 |
| Q10 | crystal_fines_fraction | 0.72 | 0.55 | 0.86 |
| Q10 | crystal_purity | 0.988 | 0.94 | 1 |
| Q10 | crystal_size | 0.055 | 0.025 | 0.1 |
| Q10 | crystal_yield | 0.065 | 0.025 | 0.12 |
| Q11 | crystal_fines_fraction | 0.44 | 0.31 | 0.58 |
| Q11 | crystal_purity | 0.983 | 0.94 | 1 |
| Q11 | crystal_size | 0.085 | 0.04 | 0.145 |
| Q11 | crystal_yield | 0.33 | 0.24 | 0.42 |
| Q12 | crystal_fines_fraction | 0.34 | 0.21 | 0.5 |
| Q12 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q12 | crystal_size | 0.14 | 0.075 | 0.23 |
| Q12 | crystal_yield | 0.46 | 0.35 | 0.57 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when seed-excluded recovery is very low. Q01–Q02 attributes better impurity rejection and particle control to S1 than S3, although the solvent extrapolation is uncertain. Q03–Q04 predicts that very low seed loading permits fewer, larger crystals and far fewer fines, with only a small recovery change. Q05–Q06 assigns similar eventual recovery but a strong fines penalty to the rapid temperature drop, because prolonged cold residence cannot fully undo an initial nucleation burst. Q07–Q08 predicts that reheating partially redissolves recovered material and that rapid recooling renews nucleation, lowering recovery and worsening fines. Q09–Q10 expects little seed-excluded crystallization after only 60 seconds; the two-hour hold raises recovery and size but probably remains fines-limited. Q11–Q12 predicts that doubling concentration increases supersaturation, recovery, and growth mass per seed; the slow ramp moderates secondary nucleation, though purity may decline slightly. The 80% intervals are epistemic extrapolation ranges, not final-assay noise, and are widest near the fines threshold and for histories unlike the completed campaign.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Cooling history strongly affects particle quality.** Direct cooling in batches 1–2 produced high recovery (0.511–0.530) but excessive fines (0.805–0.817). Staged-cooling batches 3–11 generally produced fines of 0.178–0.455 while retaining recovery of roughly 0.420–0.451. This directly supports a process-history effect. The interpretation that staged cooling limits peak supersaturation and suppresses burst nucleation is plausible, but supersaturation and nucleation rates were not measured directly.
- **Crystallization provided substantial purification.** Despite final reaction selectivities of only about 0.45–0.64, recovered-crystal purities were approximately 0.97–1.00. Batch 8, for example, had reaction selectivity about 0.487 but crystal purity about 0.982. Impurity rejection during crystallization is therefore observed; the exact partitioning mechanism remains interpretive.
- **Batch 8 was the highest observed feasible-recovery result.** Its crystal yield was about 0.451, purity 0.982, and fines 0.232. Batch 10 provided a larger fines margin (0.178) but slightly lower recovery (0.445). The numerical ranking is observed, although the difference is smaller than a convincing demonstration of reproducible superiority.
- **Extra cold residence and reheating did not improve recovery in their tested forms.** The additional 250 K stage in batch 11 gave recovery 0.435. Reheating to 310 K and recooling in batch 12 gave recovery 0.417 and fines 0.297. Thus, those particular histories did not outperform batch 8.

### Partially supported or still uncertain

- **C1/S2 was the most useful tested combination.** Repeated C1/S2 batches 6–12 consistently met the purity requirement and usually had low fines. However, the early material screen was not factorial: catalyst and solvent often changed together. The data support an empirical operating region, not independent causal rankings of C1 and S2.
- **A 0.01 g seed dose is preferable to 0.05 g.** Batch 8, using 0.01 g, had higher recovery, larger particles, and fewer fines than batch 6 using 0.05 g. Batch 9 without seed was intermediate in recovery and fines but had smaller particles. These are single runs, and the recovery differences are near combined measurement and process uncertainty. A seed-dose effect is therefore suggestive rather than established.
- **The apparent recovery–fines tradeoff is real operationally but not fully resolved mechanistically.** Direct cooling gave more recovery but failed the fines constraint; staged cooling gave compliant particles with lower recovery. It remains unclear how much of the recovery difference came from kinetic trapping, equilibrium solubility, filtration/cake-liquor effects, or categorical material confounding.

### Contradicted or not supported

- **More concentrated liquor necessarily gives greater fractional crystal recovery** was not supported by batches 6 and 7. Reducing S2 volume from 0.08 to 0.06 L did not increase recovery: it changed from about 0.440 to 0.436 under otherwise closely matched conditions. The difference is small, so this contradicts a strong monotonic claim rather than proving that concentration has no effect.
- **More elaborate thermal processing necessarily improves the result** was contradicted by batches 10–12. Three-stage cooling improved fines but not recovery; prolonged cold residence and reheat/recool also failed to improve recovery.

### Still untested

Solubility curves, supersaturation trajectories, nucleation and growth rates, impurity partition coefficients, seed-size distributions, and mother-liquor target concentrations were never measured. Consequently, the proposed nucleation-growth equations and Ostwald-ripening explanation remain mechanistic hypotheses rather than directly validated laws.

## 2. One additional experiment

I would perform a **matched split-batch cooling experiment**. A single C1/S2 reaction mixture would be prepared under the batch-8 upstream conditions and divided equally after reaction. Both arms would receive the same 0.01 g seed dose per normalized liquid volume and finish at 250 K with the same total processing time. One arm would cool directly to 250 K; the other would use the 300→250 K staged profile. Particle-size measurements would be taken immediately after the first cooling segment and before filtration, followed by matched final assays and mother-liquor target measurements.

This would distinguish three explanations:

1. **Peak-supersaturation/burst-nucleation mechanism:** the direct arm should develop many fines early, remain smaller at filtration, and possibly show higher or faster recovery; the staged arm should have fewer fines and larger particles.
2. **Material-confounding explanation:** if the previous direct-versus-staged contrast mainly arose because batches 1–5 used different catalyst/solvent combinations, the two matched arms should finish much more similarly.
3. **Final-temperature or cold-residence control:** if only time at 250 K and equilibrium solubility matter, early differences may disappear after equal total residence, giving similar final recovery and CSD. Persistent early and final differences would instead demonstrate genuine path dependence.

A split design is preferable to another independent batch because it removes most reaction-composition and run-to-run variation.

## 3. Least effectively used observation and least reliable prediction

The account used **batch 7** least effectively. It was a relatively clean concentration comparison with batch 6: both used C1/S2, 0.05 g seed, and the same staged cooling, while solvent volume changed from 0.08 to 0.06 L. Recovery did not improve, fines were similar, and size increased numerically. This observation could have constrained the concentration–supersaturation explanation more strongly. I treated it mainly as a negative result because the recovery difference was close to uncertainty and the altered fill/headspace introduced a secondary confound.

**Q09 is the least reliable held-out prediction.** It filters only 60 seconds after a rapid cool to 292 K. No campaign batch sampled such an early crystallization state, so the predicted seed-excluded yield is a large temporal extrapolation. Moreover, particle presence is guaranteed by added seed, while the reported number-weighted size and fines could be dominated by the unknown seed-size distribution rather than newly crystallized product. The estimates for recovery, size, and fines therefore depend on unmeasured early-time kinetics and ambiguous seed-versus-grown-particle contributions more than any other held-out query.
