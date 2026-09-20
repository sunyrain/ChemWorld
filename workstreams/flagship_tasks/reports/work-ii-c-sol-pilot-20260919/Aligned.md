# Aligned crystallization pilot

Status: completed; failure: None
Original status: completed; retest repair present: False.

## Source batches

| Batch | Recovery | Purity | Size index | Fines |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.4740741550922394 | 1.0 | 0.06264730542898178 | 0.9891600012779236 |
| 2 | 0.3418150842189789 | 0.9640939235687256 | 0.041908834129571915 | 1.0 |
| 3 | 0.34253984689712524 | 0.9944008588790894 | 0.03798506408929825 | 1.0 |
| 4 | 0.48802947998046875 | 0.9827663898468018 | 0.022635415196418762 | 1.0 |
| 5 | 0.5366407632827759 | 0.9794542193412781 | 0.053533248603343964 | 0.9844710826873779 |
| 6 | 0.4388686716556549 | 0.978193998336792 | 0.0988544449210167 | 1.0 |
| 7 | 0.2869434058666229 | 0.9965469837188721 | 0.06602251529693604 | 0.3960028290748596 |
| 8 | 0.46339312195777893 | 1.0 | 0.07463626563549042 | 0.9972096681594849 |
| 9 | 0.4369089901447296 | 0.9820610284805298 | 0.045640263706445694 | 0.6718798279762268 |
| 10 | 0.345439612865448 | 0.9998974800109863 | 0.045606084167957306 | 0.9813616871833801 |
| 11 | 0.3924792408943176 | 0.9747421145439148 | 0.07007840275764465 | 0.6205791234970093 |
| 12 | 0.38876527547836304 | 0.9918789863586426 | 0.10705773532390594 | 0.4164462685585022 |

## K1

Mechanistic account

The campaign supports a coupled reaction–crystallization mechanism in which chemical production and crystal quality are controlled by different, sometimes opposing, variables. Crystal purity was usually high once solids formed, but high product inventories produced excessive secondary nucleation and fines. The recommended batch 12 best balanced these effects.

Observed material effects

Catalyst C1 was used throughout, so the experiments establish a process for C1 but do not experimentally rank C0, C2, or C3. C1’s high nominal activity was consistent with the rapid reaction: in batch 12, 0.005 mol C1 with 0.016 mol reagent reached final conversion 0.964 after heating at 370 K for 900 s. Its final selectivity and liquid-phase yield were 0.817 and 0.808. Any claim that C1 is globally optimal would be untested.

Solvent choice affected both recovery and particle formation. At otherwise similar high-temperature reaction and staged-cooling conditions, S2 in batch 5 gave crystal yield 0.537, whereas S1 in batch 6 gave 0.439. This is consistent with the nominal lower solubility and higher growth tendency of S2. However, both high-loading batches had unacceptable fines: 0.984 for batch 5 and 1.000 for batch 6. S1 produced a larger normalized crystal-size signal in batch 6 (0.099 versus 0.054 in batch 5), suggesting less severe nucleation or better growth, although the comparison is not replicated. S1 subsequently enabled feasible fines at reduced loading in batches 7 and 12.

Reaction mechanism and time–temperature effects

A useful lumped scheme is

A → P,  A → I,  P → D,

where P is the crystallizable target, I represents competing byproducts, and D represents degradation. A simple kinetic approximation is

X(t) = 1 − exp[−(kP + kI)t],

with early selectivity approximately kP/(kP+kI), followed by loss if P undergoes degradation. The rate constants depend on catalyst, solvent, and temperature.

The observations favor a short, hot reaction over a long, cooler exposure for the conditions tested. Batch 1 used S2, 360 K for 3600 s and produced final selectivity 0.547 with degradation warning 0.156. Batch 2 used 330 K for 7200 s and gave selectivity 0.430 and degradation warning 0.207. Batch 3 at 320 K for 3600 s improved degradation warning to 0.093 but retained only 0.485 selectivity. In contrast, batch 5 at 370 K for 900 s gave selectivity 0.685 and degradation warning 0.045. Batch 12, using lower loading in S1 under the same nominal 370 K/900 s reaction, reached selectivity 0.817 with degradation warning 0.044.

Interpretation: rapid heating drives conversion before prolonged exposure accumulates impurity or degradation. This inference is mechanistically plausible but remains partly confounded by loading, solvent, and subsequent process history. The final-assay and preceding HPLC values also differed; for example, batch 12 HPLC reported conversion/selectivity/yield of 0.980/0.787/0.772, while the final assay reported 0.964/0.817/0.808. These differences reflect instrument noise and continued processing rather than a precisely resolved kinetic trajectory.

Reaction–crystallization coupling

The approximate target inventory entering crystallization scales as

nP ≈ nA,0 X S,

and the concentration driving crystallization as

ΔC(T) = nP/V − C*(T, solvent).

Crystal growth can be represented as G ∝ kgΔC, while secondary nucleation commonly rises more sharply, J ∝ kn(ΔC)^m with m > 1. Thus increasing target inventory can increase recovery but cause J/G to rise sharply, generating many particles below 20 µm.

The campaign strongly supports this nonlinear supersaturation interpretation. High-loading S1 batches gave high recovery but failed the fines constraint:

• Batch 8, 0.025 mol reagent and 0.005 mol C1: crystal yield 0.463, purity 1.000, fines 0.997.
• Batch 9, 0.020 mol reagent and 0.005 mol C1: yield 0.437, purity 0.982, fines 0.672.
• Batch 11, 0.018 mol reagent and 0.005 mol C1: yield 0.392, purity 0.975, fines 0.621.
• Batch 12, 0.016 mol reagent and 0.005 mol C1: yield 0.389, purity 0.992, fines 0.416.

The small loss in recovery from batch 11 to batch 12 was accompanied by a large improvement in fines, indicating a nucleation threshold rather than a smooth proportional response. Batch 12’s normalized size of 0.107 corresponds to a number-weighted d50 of about 26.8 µm under the declared size definition, consistent with its fines fraction falling below 0.50.

Purity behaved differently from particle size. Even batches with only moderate reaction selectivity frequently gave crystal purity near unity. For example, batch 5 had reaction selectivity 0.685 but crystal purity 0.979; batch 12 had selectivity 0.817 and purity 0.992. This indicates preferential incorporation of target into the solid and rejection of soluble impurities. Purity was therefore not the limiting attribute; number-based fines were.

Process-history dependence

Seeding, quench temperature, cooling path, and residence time affected the state from which crystallization began. The successful low-loading process quenched from the short hot reaction to approximately 319 K, added 0.05 g seed, cooled to 310 K over 14,400 s, held for 14,400 s at low stirring, cooled to 295 K over another 14,400 s, held again, and then filtered. This history allows seed growth before the lower-temperature precipitation step.

Initial revisions showed that simply extending or softening the crystallization was insufficient at high inventory. Batch 1 used 0.05 g seed, deep cooling to 260 K, and a long hold; it achieved crystal yield 0.474 and purity 1.000 but fines 0.989. Batch 3 cooled only to 295 K and held much longer, yet fines remained 1.000. Batch 4 used only 0.01 g seed plus a cool–reheat–recool cycle; its yield was 0.488, but fines remained 1.000 and normalized crystal size fell to 0.023. This argues that annealing cannot rescue a particle population after extensive primary or secondary nucleation, at least under the tested cycle.

Batch 10 also demonstrated that higher final temperature alone was not a reliable remedy. With 0.020 mol reagent and full C1 loading, its final crystallization temperature was 305 K rather than 295 K, but it still gave fines 0.981 and reduced yield to 0.345. Consequently, the successful revision was reduction of product inventory, not merely warmer isolation.

Development revisions

The campaign began with maximum reagent loading in S2 to establish conversion and attainable recovery. Those batches revealed excellent purity but nearly all-number fines. Longer holds, milder cooling, a lower seed charge, and a thermal cycle did not solve the problem. The process was then shifted to S1 and reduced reagent loading. Batch 7 first demonstrated feasibility: 0.020 mol reagent, 0.0025 mol C1, crystal yield 0.287, purity 0.997, and fines 0.396. Restoring the full 0.005 mol C1 increased reaction conversion and recovery but pushed batches 9 and 11 above the fines limit. Reducing reagent charge to 0.016 mol in batch 12 retained a yield of 0.389 while restoring acceptable fines at 0.416.

Uncertainty and unresolved tradeoff

The clearest unresolved tradeoff is recovery versus nucleation. The highest recoveries—0.537 in batch 5, 0.488 in batch 4, 0.463 in batch 8, and 0.437 in batch 9—were all infeasible because fines ranged from 0.672 to 1.000. Batch 12 is the highest observed recovery satisfying both purity ≥0.80 and fines ≤0.50. Its fines margin is 0.084, larger than the declared final-assay noise scale of 0.018, but process reproducibility was not measured because no recipe was replicated.

Other uncertainties include confounding among solvent, loading, catalyst ratio, and thermal history; unknown seed-size distribution; and fixed-world material residuals. Untested alternatives include intermediate reagent charges between 0.016 and 0.018 mol, other catalysts, different seed masses near 0.05 g, and alternative staged holds designed to increase growth without crossing the nucleation threshold. These could potentially improve recovery, but the present evidence does not establish that they would remain below the fines limit.

## Q

{
  "predictions": [
    {
      "crystal_fines_fraction": {
        "estimate": 0.96,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q01"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.985,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.92,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "crystal_size": {
        "estimate": 0.025,
        "lower80": 0.008,
        "upper80": 0.06
      },
      "crystal_yield": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.66
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q02"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.96,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q03"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.78,
        "lower80": 0.52,
        "upper80": 0.96
      },
      "crystal_purity": {
        "estimate": 0.975,
        "lower80": 0.91,
        "upper80": 0.998
      },
      "crystal_size": {
        "estimate": 0.085,
        "lower80": 0.035,
        "upper80": 0.15
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.39,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q04"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.96,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q05"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.995,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.965,
        "lower80": 0.89,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.022,
        "lower80": 0.006,
        "upper80": 0.052
      },
      "crystal_yield": {
        "estimate": 0.57,
        "lower80": 0.39,
        "upper80": 0.71
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q06"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.975,
        "lower80": 0.83,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.031,
        "lower80": 0.01,
        "upper80": 0.067
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q07"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.72,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.997
      },
      "crystal_size": {
        "estimate": 0.043,
        "lower80": 0.015,
        "upper80": 0.09
      },
      "crystal_yield": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.69
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q08"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.975,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.032,
        "lower80": 0.01,
        "upper80": 0.07
      },
      "crystal_yield": {
        "estimate": 0.53,
        "lower80": 0.35,
        "upper80": 0.68
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q09"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.955,
        "lower80": 0.77,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.038,
        "lower80": 0.013,
        "upper80": 0.08
      },
      "crystal_yield": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q10"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.88,
        "lower80": 0.6,
        "upper80": 0.99
      },
      "crystal_purity": {
        "estimate": 0.98,
        "lower80": 0.92,
        "upper80": 0.999
      },
      "crystal_size": {
        "estimate": 0.045,
        "lower80": 0.016,
        "upper80": 0.095
      },
      "crystal_yield": {
        "estimate": 0.49,
        "lower80": 0.3,
        "upper80": 0.65
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q11"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.995,
        "lower80": 0.91,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 0.995
      },
      "crystal_size": {
        "estimate": 0.019,
        "lower80": 0.005,
        "upper80": 0.048
      },
      "crystal_yield": {
        "estimate": 0.62,
        "lower80": 0.42,
        "upper80": 0.76
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q12"
    }
  ],
  "rationale": "Q01, Q03, and Q05 are identical recipes and therefore receive identical predictions. For the solvent pair, S3 is expected to retain more target in solution, occlude more impurity, and support poorer growth than S1, reducing Q02 recovery, purity, and size while increasing fines. Increasing seed from 0.006 g to 0.05 g in Q04 should suppress some secondary nucleation and enlarge particles, but the high target concentration and deep 278.15 K endpoint are still expected to leave fines above 0.50. Staged cooling in Q05 should be less nucleating than the immediate deep-cooling history in Q06. The reheat in Q08 may dissolve some small particles and modestly improve size versus Q07, although the campaign's thermal-cycle batch showed that this effect is uncertain and unlikely to restore feasibility. The extra low-temperature growth period in Q10 should modestly increase recovery and size relative to Q09. Lower loading in Q11 reduces supersaturation and fines but increases the fractional loss of dissolved product; Q12 improves fractional recovery but is predicted to undergo extensive nucleation. Uncertainty is broad because these recipes use much less solvent and catalyst than the campaign batches, a smaller seed charge, a hotter and longer reaction history, and a deeper cooling endpoint. The intervals represent epistemic process uncertainty around noise-free outcomes, not final-assay noise."
}

## K2

1. Status of the main claims

Supported by direct observations:

• A sharp recovery–fines tradeoff with target loading is the strongest result. Under closely related S1/C1 reaction and staged-cooling conditions, batches 8, 9, 11, and 12 used 0.025, 0.020, 0.018, and 0.016 mol reagent. Their crystal yields were 0.463, 0.437, 0.392, and 0.389, while fines fell from 0.997 to 0.672, 0.621, and finally 0.416. Thus batch 12 lost little recovery relative to batch 11 but crossed the fines specification. Interpreting this as a nonlinear supersaturation/nucleation threshold is plausible, although supersaturation itself was not measured.

• Crystallization strongly purified the target. Examples include batch 5, with reaction selectivity 0.685 but crystal purity 0.979, and batch 12, with selectivity 0.817 but crystal purity 0.992. Preferential target crystallization is an interpretation; the direct observation is the large difference between liquid-phase selectivity and solid purity.

• High recovery alone did not imply acceptable particle quality. Batches 4, 5, 8, and 9 produced crystal yields of 0.488, 0.537, 0.463, and 0.437, but their fines were 1.000, 0.984, 0.997, and 0.672. Batch 12 was the highest observed yield satisfying both specifications.

• S2 favored recovery, whereas S1 gave a larger size signal in the closest solvent comparison. Batch 5 using S2 gave yield 0.537 and normalized size 0.054; batch 6 using S1 gave yield 0.439 and size 0.099. Both failed the fines constraint, and this was only one unreplicated comparison, so it supports a solvent effect but not a universal solvent ranking.

• Simply extending or warming the crystallization did not reliably cure fines. Batch 3 had prolonged holds but fines of 1.000. Batch 4 included a reheat/recool cycle and also had fines of 1.000. Batch 10 ended at 305 K rather than 295 K yet gave fines of 0.981 and lower yield than batch 9. These directly contradict a simple claim that more time, annealing, or a warmer endpoint must improve the distribution.

Partially supported or confounded:

• The short, hot reaction appeared preferable to longer exposure. Batch 5 at 370 K for 900 s had selectivity 0.685 and degradation warning 0.045, versus batch 1 at 360 K for 3600 s with 0.547 and 0.156, and batch 2 at 330 K for 7200 s with 0.430 and 0.207. Temperature, duration, subsequent history, and sometimes crystallization conditions were not independently varied, so the proposed A→P, A→I, P→D scheme remains a useful interpretation rather than an identified kinetic law.

• The decisive variable may be target inventory n₀XS/V rather than reagent loading alone. Batch 7 and batch 9 both charged 0.020 mol reagent in S1, but batch 7 used 0.0025 mol catalyst and had liquid yield 0.624, crystal yield 0.287, and fines 0.396; batch 9 used 0.005 mol catalyst and had liquid yield 0.771, crystal yield 0.437, and fines 0.672. This supports an inventory mechanism, but catalyst concentration might also affect impurity identity or nucleation directly.

Still untested:

• C1 was never compared experimentally with C0, C2, or C3, so C1 optimality is untested.

• Seed-mass effects were confounded. Batch 4 used 0.01 g seed, but it also used a distinct thermal cycle; the 0.05 g batches therefore do not isolate seed mass.

• The proposed nucleation and growth relationships, J ∝ ΔC^m and G ∝ ΔC, were not measured directly. No supersaturation, nucleation-rate, growth-rate, or seed-size measurements were available.

• Reproducibility is unresolved because no final recipe was replicated. The final-assay noise scale does not cover batch-to-batch process variability.

2. One additional experiment

I would run one inventory-matching experiment between batches 11 and 12: charge 0.018 mol reagent in 0.080 L S1, use about 0.0035 mol C1, heat at 370 K for 900 s, measure the liquid by HPLC, then apply batch 12’s quench, 0.05 g seed, 310 K and 295 K staged cooling/holds, filtration, and final assay. The catalyst amount is chosen to seek approximately the same absolute target inventory as batch 12 while retaining batch 11’s initial reagent loading.

This would distinguish two explanations:

• If fines are governed mainly by target inventory/supersaturation, matching batch 12’s pre-crystallization target moles should give fines near batch 12’s 0.416, high purity, and approximately the same absolute crystal amount. Because the denominator is 0.018 rather than 0.016 mol, the fractional crystal yield would be expected around 0.35 rather than 0.389.

• If initial reagent loading, catalyst ratio, impurity composition, or another history-dependent variable controls nucleation independently of target inventory, the result should resemble batch 11 more closely: fines near or above 0.62 and crystal yield near 0.39.

The intermediate HPLC result is essential: if it fails to match the intended target inventory, the experiment would primarily refine reaction kinetics rather than cleanly test the crystallization explanations.

3. Least effectively used observation and least reliable prediction

The account used batch 10 least effectively. It noted that the warmer 305 K endpoint produced lower recovery and much worse fines than expected, but the simple equilibrium/supersaturation equations did not explain that result. Batch 10 indicates that nucleation timing, seed survival, cooling trajectory, or an unobserved state variable matters—not merely final temperature and equilibrium solubility. That observation should have led to wider uncertainty for all thermal-history claims.

Q02 is the least reliable held-out prediction. It is the only solvent-S3 case, while no campaign batch used S3. Its prediction therefore depended almost entirely on nominal dossier properties, despite the explicit possibility of fixed hidden solvent residuals or misindexing. The simultaneous extrapolation to much lower solvent volume, much lower catalyst charge, 385 K reaction conditions, small seed mass, and deep cooling further compounds the uncertainty. Q08 is also weak because the sole thermal-cycle precedent, batch 4, was confounded, but Q02 has the largest unsupported material extrapolation.

## Evaluation and resources

```json
{
  "prediction_evaluation": {
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "covered": 10,
        "mae": 0.07689785933132777,
        "mean_interval_width": 0.22166666666666668,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "covered": 12,
        "mae": 0.017827401721018588,
        "mean_interval_width": 0.10366666666666664,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "covered": 8,
        "mae": 0.03407047604050193,
        "mean_interval_width": 0.06525,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "covered": 0,
        "mae": 0.34431084410061735,
        "mean_interval_width": 0.32916666666666666,
        "n": 12,
        "planned": 12
      }
    },
    "pair_correct": 16,
    "pair_n": 24,
    "pairs": [
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "solvent"
      },
      {
        "correct": false,
        "metric": "crystal_purity",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "solvent"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "seed"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "seed"
      },
      {
        "correct": false,
        "metric": "crystal_size",
        "pair": "seed"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "seed"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "cooling_history"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "cooling_history"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "cooling_history"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "cooling_history"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "thermal_history"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "thermal_history"
      },
      {
        "correct": false,
        "metric": "crystal_yield",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "continue_growth"
      },
      {
        "correct": false,
        "metric": "crystal_yield",
        "pair": "upstream_loading"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "upstream_loading"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "upstream_loading"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "upstream_loading"
      }
    ],
    "presence_correct": 12,
    "quality_correct": 12,
    "valid": true
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 1123200,
        "input": 1193029,
        "output": 9344,
        "stage": "source",
        "uncached_input": 69829
      },
      {
        "cached_input": 0,
        "input": 32632,
        "output": 3131,
        "stage": "K1",
        "uncached_input": 32632
      },
      {
        "cached_input": 0,
        "input": 39757,
        "output": 4536,
        "stage": "Q",
        "uncached_input": 39757
      },
      {
        "cached_input": 32512,
        "input": 44213,
        "output": 2722,
        "stage": "K2",
        "uncached_input": 11701
      }
    ],
    "total": {
      "cached_input": 1155712,
      "input": 1309631,
      "input_plus_output": 1329364,
      "output": 19733,
      "uncached_input": 153919
    },
    "valid": true
  },
  "elapsed_s": 1207.4070000000065,
  "recommendation": {
    "selected_experiment_index": 12,
    "selection_rationale": "Batch 12 gave the highest observed seed-excluded crystal yield among batches meeting both constraints: crystal_yield 0.389, crystal_purity 0.992, and crystal_fines_fraction 0.416."
  }
}
```
